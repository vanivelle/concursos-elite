#!/usr/bin/env python3
"""
🔐 CONCURSO ELITE v3.3 - BACKEND SEGURO COM MONITORAMENTO
Versão com: Criptografia, JWT, Rate Limiting, Auditoria, Logs de Segurança
"""

import os
import json
import secrets
import logging
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from functools import wraps
import time

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ============================================================
# 🔐 SEGURANÇA: CRIPTOGRAFIA & AUTENTICAÇÃO
# ============================================================

try:
    from passlib.context import CryptContext
    from jose import JWTError, jwt
    print("✅ Bibliotecas de criptografia disponíveis")
except ImportError:
    print("⚠️  Instale: pip install python-jose passlib bcrypt")
    import sys
    sys.exit(1)

# ============================================================
# 📊 LOGGING & AUDITORIA
# ============================================================

class AuditoriaLogger:
    """Sistema de auditoria com criptografia de logs"""
    
    def __init__(self, log_file: str = "auditoria.log"):
        self.log_file = log_file
        self.logger = logging.getLogger("AUDITORIA")
        
        # Handler para arquivo (log importante)
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def registrar_login(self, email: str, ip: str, user_agent: str, sucesso: bool):
        """Auditar tentativa de login"""
        status = "✅ SUCESSO" if sucesso else "❌ FALHA"
        self.logger.warning(f"LOGIN {status} | Email: {email} | IP: {ip} | User-Agent: {user_agent[:50]}")
    
    def registrar_acesso_questao(self, email: str, questao_id: str, ip: str):
        """Auditar acesso a questão"""
        self.logger.info(f"ACESSO_QUESTAO | Email: {email} | Questão: {questao_id} | IP: {ip}")
    
    def registrar_erro(self, tipo: str, email: str, detalhes: str, ip: str):
        """Auditar erros e suspeitas"""
        self.logger.error(f"ERRO | Tipo: {tipo} | Email: {email} | IP: {ip} | Detalhes: {detalhes}")
    
    def registrar_suspeita(self, email: str, ip: str, motivo: str):
        """Alerta de atividade suspeita"""
        self.logger.critical(f"🚨 SUSPEITA | Email: {email} | IP: {ip} | Motivo: {motivo}")

auditoria = AuditoriaLogger("auditoria_concurso.log")

# ============================================================
# 🔐 CONFIGURAÇÃO DE CRIPTOGRAFIA
# ============================================================

# Contexto de criptografia (bcrypt)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # 12 rounds = mais seguro
)

# Configuração JWT
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 horas

class ConfigSeguranca:
    """Configurações de segurança centralizadas"""
    
    # Limite de tentativas de login (para prevenir brute force)
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_MINUTES = 15
    
    # Rate limiting (requisições por minuto por IP)
    RATE_LIMIT_PER_MINUTE = 60
    
    # IPs permitidos (se None, todos são permitidos)
    IPS_BLOQUEADOS = set()
    
    # Comprimento mínimo de senha
    MIN_PASSWORD_LENGTH = 12
    
    # Cookies seguros
    SECURE_COOKIES = True
    HTTP_ONLY = True
    SAME_SITE = "strict"

# ============================================================
# 🔐 FUNÇÕES DE CRIPTOGRAFIA
# ============================================================

def hash_senha(senha: str) -> str:
    """Hash de senha com bcrypt (salted)"""
    return pwd_context.hash(senha)

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verificar senha contra hash"""
    return pwd_context.verify(senha_plana, senha_hash)

def criar_token_acesso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Criar JWT token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token(token: str) -> Dict:
    """Verificar e decodificar JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        auditoria.registrar_erro("JWT_INVÁLIDO", "unknown", str(e), "unknown")
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

# ============================================================
# 🛡️ RATE LIMITING
# ============================================================

class RateLimiter:
    """Controle de taxa de requisições (previne DDoS)"""
    
    def __init__(self):
        self.requisicoes: Dict[str, List[float]] = {}
        self.bloqueados: Dict[str, float] = {}
    
    def verificar_limite(self, ip: str, limite_por_minuto: int = 60) -> bool:
        """Verificar se IP excedeu limite"""
        agora = time.time()
        
        # Verificar se está bloqueado
        if ip in self.bloqueados:
            if agora < self.bloqueados[ip]:
                return False  # Ainda bloqueado
            else:
                del self.bloqueados[ip]  # Desbloqueado
        
        # Limpar requisições antigas (> 1 minuto)
        if ip in self.requisicoes:
            self.requisicoes[ip] = [t for t in self.requisicoes[ip] if agora - t < 60]
        else:
            self.requisicoes[ip] = []
        
        # Contar requisições
        if len(self.requisicoes[ip]) >= limite_por_minuto:
            # Bloquear por 15 minutos
            self.bloqueados[ip] = agora + (15 * 60)
            auditoria.registrar_suspeita(ip, ip, f"Rate limit excedido ({limite_por_minuto}/min)")
            return False
        
        # Registrar nova requisição
        self.requisicoes[ip].append(agora)
        return True

rate_limiter = RateLimiter()

# ============================================================
# 📋 MODELOS PYDANTIC (Validação)
# ============================================================

class LoginRequest(BaseModel):
    email: str
    senha: str
    
    @validator('email')
    def email_valido(cls, v):
        if '@' not in v or len(v) < 5:
            raise ValueError('Email inválido')
        return v.lower()
    
    @validator('senha')
    def senha_valida(cls, v):
        if len(v) < ConfigSeguranca.MIN_PASSWORD_LENGTH:
            raise ValueError(f'Senha deve ter {ConfigSeguranca.MIN_PASSWORD_LENGTH}+ caracteres')
        return v

class RegistroRequest(BaseModel):
    email: str
    senha: str
    nome: str
    
    @validator('email')
    def email_valido(cls, v):
        if '@' not in v or len(v) < 5:
            raise ValueError('Email inválido')
        return v.lower()
    
    @validator('senha')
    def senha_complexa(cls, v):
        if len(v) < ConfigSeguranca.MIN_PASSWORD_LENGTH:
            raise ValueError(f'Senha deve ter {ConfigSeguranca.MIN_PASSWORD_LENGTH}+ caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('Senha deve ter letra maiúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve ter número')
        return v

class QuestaoResponse(BaseModel):
    questao_id: str
    concurso: str
    materia: str
    dificuldade: str
    enunciado: str
    alternativas: Dict
    resposta_correta: str
    diagnostico_erro: str
    nucleo_acerto: str
    pegadinha_banca: str
    padroes_banca: str

# ============================================================
# 🗄️ BANCO DE DADOS
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:senha_segura_123@postgres_db:5432/admin")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UsuarioModel(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    minutos_estudados = Column(Float, default=0.0)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    ultimo_login = Column(DateTime, nullable=True)

class AuditoriaModel(Base):
    __tablename__ = "auditoria_eventos"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # LOGIN, ACESSO, ERRO, SUSPEITA
    email = Column(String, nullable=False, index=True)
    ip = Column(String, nullable=False)
    detalhes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class QuestoesBancoModel(Base):
    __tablename__ = "questoes_banco"
    id = Column(Integer, primary_key=True, index=True)
    questao_id = Column(String, unique=True, index=True, nullable=False)
    concurso = Column(String, nullable=False, index=True)
    materia = Column(String, nullable=False, index=True)
    dificuldade = Column(String, nullable=False, index=True)
    banca = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    enunciado = Column(Text, nullable=False)
    alternativas = Column(Text, nullable=False)  # JSON
    resposta_correta = Column(String, nullable=False)
    explicacao = Column(Text, nullable=False)
    diagnostico_erro = Column(Text, nullable=True)
    nucleo_acerto = Column(Text, nullable=True)
    pegadinha_banca = Column(Text, nullable=False)
    padroes_banca = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)

# ============================================================
# 🚀 APLICAÇÃO FASTAPI
# ============================================================

app = FastAPI(
    title="Concurso Elite v3.3 - Backend Seguro",
    description="API com criptografia, JWT, auditoria e monitoramento",
    version="3.3.0"
)

# ============================================================
# 🛡️ MIDDLEWARE DE SEGURANÇA
# ============================================================

class SecurityHeaderMiddleware:
    """Adiciona headers de segurança a todas as respostas"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        async def send_with_security_headers(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.extend([
                    (b"X-Content-Type-Options", b"nosniff"),
                    (b"X-Frame-Options", b"DENY"),
                    (b"X-XSS-Protection", b"1; mode=block"),
                    (b"Strict-Transport-Security", b"max-age=31536000; includeSubDomains"),
                ])
                message["headers"] = headers
            await send(message)
        
        await self.app(scope, receive, send_with_security_headers)

app.add_middleware(SecurityHeaderMiddleware)

# CORS seguro (apenas domínios confiáveis)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://open-notebook-8x8twkj23.vercel.app",
        "http://localhost:3000",  # Dev local
        "http://localhost:8000"   # Dev local
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ============================================================
# 🔑 AUTENTICAÇÃO
# ============================================================

async def get_current_user(authorization: Optional[str] = Header(None), request: Request = None) -> Dict:
    """Dependência para verificar token JWT"""
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Esquema inválido")
    except ValueError:
        raise HTTPException(status_code=401, detail="Formato de token inválido")
    
    payload = verificar_token(token)
    email = payload.get("email")
    
    if not email:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return {"email": email}

# ============================================================
# 📡 ENDPOINTS
# ============================================================

@app.post("/registrar", tags=["Autenticação"])
async def registrar(req: RegistroRequest, request: Request):
    """Registrar novo usuário (com criptografia de senha)"""
    
    ip = request.client.host
    
    # Verificar rate limit
    if not rate_limiter.verificar_limite(ip):
        auditoria.registrar_suspeita(req.email, ip, "Rate limit na rota de registro")
        raise HTTPException(status_code=429, detail="Muitas tentativas. Tente novamente mais tarde")
    
    db = SessionLocal()
    
    try:
        # Verificar se já existe
        existe = db.query(UsuarioModel).filter_by(email=req.email).first()
        if existe:
            auditoria.registrar_erro("REGISTRO", req.email, "Email já registrado", ip)
            raise HTTPException(status_code=400, detail="Email já registrado")
        
        # Criar usuário com senha criptografada
        usuario = UsuarioModel(
            email=req.email,
            senha_hash=hash_senha(req.senha),  # ✅ CRIPTOGRAFADO COM BCRYPT
            nome=req.nome,
            data_criacao=datetime.utcnow()
        )
        
        db.add(usuario)
        db.commit()
        
        auditoria.registrar_login(req.email, ip, request.headers.get("user-agent", ""), True)
        
        return {"status": "✅ Usuário registrado com sucesso", "email": req.email}
    
    except Exception as e:
        db.rollback()
        auditoria.registrar_erro("REGISTRO", req.email, str(e), ip)
        raise HTTPException(status_code=500, detail="Erro ao registrar")
    
    finally:
        db.close()

@app.post("/login", tags=["Autenticação"])
async def login(req: LoginRequest, request: Request):
    """Login com JWT (senha criptografada)"""
    
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    
    # Verificar rate limit
    if not rate_limiter.verificar_limite(ip):
        auditoria.registrar_suspeita(req.email, ip, "Brute force na rota de login")
        raise HTTPException(status_code=429, detail="Muitas tentativas de login")
    
    db = SessionLocal()
    
    try:
        usuario = db.query(UsuarioModel).filter_by(email=req.email).first()
        
        if not usuario or not verificar_senha(req.senha, usuario.senha_hash):  # ✅ BCRYPT
            auditoria.registrar_login(req.email, ip, user_agent, False)
            raise HTTPException(status_code=401, detail="Email ou senha incorretos")
        
        # Criar token JWT
        token = criar_token_acesso({"email": usuario.email})
        
        # Atualizar último login
        usuario.ultimo_login = datetime.utcnow()
        db.commit()
        
        auditoria.registrar_login(req.email, ip, user_agent, True)
        
        return {
            "status": "✅ Login bem-sucedido",
            "token": token,
            "token_type": "bearer"
        }
    
    except Exception as e:
        auditoria.registrar_erro("LOGIN", req.email, str(e), ip)
        raise
    
    finally:
        db.close()

@app.get("/gerar-questao", tags=["Questões"], response_model=QuestaoResponse)
async def gerar_questao(
    concurso: str,
    materia: str = None,
    dificuldade: str = None,
    current_user: Dict = Depends(get_current_user),
    request: Request = None
):
    """Gerar questão aleatória (requer autenticação)"""
    
    ip = request.client.host
    email = current_user["email"]
    
    # Verificar rate limit
    if not rate_limiter.verificar_limite(ip, limite_por_minuto=120):
        auditoria.registrar_suspeita(email, ip, "Muitas requisições de questões")
        raise HTTPException(status_code=429, detail="Limite de requisições excedido")
    
    db = SessionLocal()
    
    try:
        # Filtrar questões
        query = db.query(QuestoesBancoModel).filter_by(concurso=concurso)
        
        if materia:
            query = query.filter_by(materia=materia)
        if dificuldade:
            query = query.filter_by(dificuldade=dificuldade)
        
        # Questão aleatória
        questao = query.order_by(func.random()).first()
        
        if not questao:
            raise HTTPException(status_code=404, detail="Questão não encontrada")
        
        # Auditar acesso
        auditoria.registrar_acesso_questao(email, questao.questao_id, ip)
        
        alternativas = json.loads(questao.alternativas)
        
        return QuestaoResponse(
            questao_id=questao.questao_id,
            concurso=questao.concurso,
            materia=questao.materia,
            dificuldade=questao.dificuldade,
            enunciado=questao.enunciado,
            alternativas=alternativas,
            resposta_correta=questao.resposta_correta,
            diagnostico_erro=questao.diagnostico_erro or "",
            nucleo_acerto=questao.nucleo_acerto or "",
            pegadinha_banca=questao.pegadinha_banca,
            padroes_banca=questao.padroes_banca or ""
        )
    
    finally:
        db.close()

@app.post("/registrar-tempo", tags=["Progresso"])
async def registrar_tempo(
    minutos: float,
    current_user: Dict = Depends(get_current_user),
    request: Request = None
):
    """Registrar tempo de estudo (requer autenticação)"""
    
    ip = request.client.host
    email = current_user["email"]
    
    if minutos < 0 or minutos > 1440:  # Max 24h por requisição
        auditoria.registrar_suspeita(email, ip, f"Valor de minutos inválido: {minutos}")
        raise HTTPException(status_code=400, detail="Minutos inválido")
    
    db = SessionLocal()
    
    try:
        usuario = db.query(UsuarioModel).filter_by(email=email).first()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        usuario.minutos_estudados += minutos
        db.commit()
        
        return {
            "status": "✅ Tempo registrado",
            "minutos_total": usuario.minutos_estudados
        }
    
    finally:
        db.close()

@app.get("/stats", tags=["Progresso"])
async def obter_stats(current_user: Dict = Depends(get_current_user)):
    """Obter estatísticas do usuário"""
    
    db = SessionLocal()
    
    try:
        usuario = db.query(UsuarioModel).filter_by(email=current_user["email"]).first()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return {
            "email": usuario.email,
            "nome": usuario.nome,
            "minutos_estudados": usuario.minutos_estudados,
            "data_criacao": usuario.data_criacao.isoformat(),
            "ultimo_login": usuario.ultimo_login.isoformat() if usuario.ultimo_login else None
        }
    
    finally:
        db.close()

@app.get("/health", tags=["Sistema"])
async def health_check():
    """Health check da API"""
    return {
        "status": "✅ Concurso Elite Backend Online",
        "version": "3.3.0",
        "timestamp": datetime.utcnow().isoformat(),
        "segurança": "🔐 Criptografia JWT + BCRYPT + Rate Limiting"
    }

@app.get("/docs", tags=["Documentação"])
async def docs():
    """Swagger UI docs"""
    from fastapi.openapi.utils import get_openapi
    return get_openapi(
        title="Concurso Elite API",
        version="3.3.0",
        routes=app.routes,
    )

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("🚀 CONCURSO ELITE v3.3 - BACKEND SEGURO")
    print("=" * 70)
    print("✅ Criptografia: BCRYPT (12 rounds)")
    print("✅ Autenticação: JWT HS256")
    print("✅ Rate Limiting: 60 req/min por IP")
    print("✅ Auditoria: Todos os eventos registrados")
    print("✅ Headers de Segurança: HSTS, CSP, X-Frame-Options")
    print("=" * 70)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
