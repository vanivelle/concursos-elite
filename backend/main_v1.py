import os
import json
import secrets
import random
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, Float, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import requests

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:senha_segura_123@postgres_db:5432/admin")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "concursos-elite")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UsuarioModel(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    minutos_estudados = Column(Float, default=0.0)

class SessaoAtivaModel(Base):
    __tablename__ = "sessoes_ativas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_email = Column(String, unique=True, index=True, nullable=False)
    token_sessao = Column(String, nullable=False)
    ip_ultimo = Column(String, nullable=False)
    aparelho_user_agent = Column(String, nullable=False)

class HistoricoQuestoesModel(Base):
    __tablename__ = "historico_questoes"
    id = Column(Integer, primary_key=True, index=True)
    usuario_email = Column(String, nullable=False)
    questao_id = Column(String, nullable=False)
    resultado_acerto = Column(Boolean, nullable=False)

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
    alternativas = Column(Text, nullable=False)
    resposta_correta = Column(String, nullable=False)
    explicacao = Column(Text, nullable=False)
    pegadinha_banca = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="🏛️ IA Concursos Elite - Motor de Questões Instantâneo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CadastroDados(BaseModel):
    email: str
    senha: str
    nome: str

class LoginDados(BaseModel):
    email: str
    senha: str

class SolicitacaoQuestao(BaseModel):
    email: str
    token: str
    concurso: str
    materia: str
    dificuldade: str

class RespostaUsuario(BaseModel):
    email: str
    token: str
    questao_id: str
    resposta_escolhida: str
    resposta_correta: str

class SinalTempo(BaseModel):
    email: str
    token: str
    timestamp: int

def verificar_seguranca_sessao(email: str, token_enviado: str, db: Session):
    email_limpo = email.strip().lower()
    sessao = db.query(SessaoAtivaModel).filter(SessaoAtivaModel.usuario_email == email_limpo).first()
    if not sessao:
        raise HTTPException(status_code=401, detail="Sessão não encontrada. Faça login novamente.")
    if sessao.token_sessao != token_enviado:
        raise HTTPException(
            status_code=403,
            detail="⚠️ ACESSO BLOQUEADO: Seu login foi aberto em outro aparelho. O rateio de contas é proibido."
        )
    return True

@app.post("/cadastro")
def cadastrar_usuario(dados: CadastroDados, db: Session = Depends(get_db)):
    email_limpo = dados.email.strip().lower()
    usuario_existe = db.query(UsuarioModel).filter(UsuarioModel.email == email_limpo).first()
    if usuario_existe:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado no sistema.")
    novo_usuario = UsuarioModel(email=email_limpo, senha=dados.senha, nome=dados.nome)
    db.add(novo_usuario)
    db.commit()
    return {"status": "sucesso", "mensagem": "Usuário cadastrado com sucesso!"}

@app.post("/login")
def login(dados: LoginDados, request: Request, db: Session = Depends(get_db)):
    email_limpo = dados.email.strip().lower()
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == email_limpo).first()
    if not usuario or usuario.senha != dados.senha:
        raise HTTPException(status_code=400, detail="E-mail ou senha inválidos.")
    
    novo_token = f"sess_{secrets.token_hex(16)}"
    sessao_existente = db.query(SessaoAtivaModel).filter(SessaoAtivaModel.usuario_email == email_limpo).first()
    
    if sessao_existente:
        sessao_existente.token_sessao = novo_token
        sessao_existente.ip_ultimo = request.client.host
        sessao_existente.aparelho_user_agent = request.headers.get("user-agent", "Desconhecido")
    else:
        nova_sessao = SessaoAtivaModel(
            usuario_email=email_limpo,
            token_sessao=novo_token,
            ip_ultimo=request.client.host,
            aparelho_user_agent=request.headers.get("user-agent", "Desconhecido")
        )
        db.add(nova_sessao)
    
    db.commit()
    return {"status": "sucesso", "token": novo_token, "nome": usuario.nome, "email": usuario.email}

@app.post("/gerar-questao")
def gerar_questao(dados: SolicitacaoQuestao, db: Session = Depends(get_db)):
    """
    ENTREGA INSTANTÂNEA: Sorteio aleatório do banco de dados.
    Tempo de resposta: ~0.1 segundos
    """
    verificar_seguranca_sessao(dados.email, dados.token, db)
    
    questao = db.query(QuestoesBancoModel).filter(
        QuestoesBancoModel.concurso == dados.concurso,
        QuestoesBancoModel.materia == dados.materia,
        QuestoesBancoModel.dificuldade == dados.dificuldade
    ).order_by(func.random()).first()
    
    if not questao:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhuma questão encontrada para {dados.concurso} - {dados.materia} - {dados.dificuldade}. Aguarde o populador de dados!"
        )
    
    alternativas_dict = json.loads(questao.alternativas)
    
    return {
        "id": questao.questao_id,
        "enunciado": questao.enunciado,
        "tipo": questao.tipo,
        "alternativas": alternativas_dict,
        "resposta_correta": questao.resposta_correta,
        "explicacao": questao.explicacao,
        "pegadinha_banca": questao.pegadinha_banca
    }

@app.post("/salvar-resposta")
def salvar_resposta(dados: RespostaUsuario, db: Session = Depends(get_db)):
    verificar_seguranca_sessao(dados.email, dados.token, db)
    
    acertou = dados.resposta_escolhida.upper() == dados.resposta_correta.upper()
    novo_historico = HistoricoQuestoesModel(
        usuario_email=dados.email.strip().lower(),
        questao_id=dados.questao_id,
        resultado_acerto=acertou
    )
    db.add(novo_historico)
    db.commit()
    
    return {"status": "salvo", "acertou": acertou}

@app.post("/registrar-tempo")
def registrar_tempo(dados: SinalTempo, db: Session = Depends(get_db)):
    email_limpo = dados.email.strip().lower()
    verificar_seguranca_sessao(email_limpo, dados.token, db)
    
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == email_limpo).first()
    if usuario:
        usuario.minutos_estudados += 1.0
        db.commit()
        horas = round(usuario.minutos_estudados / 60, 2)
        return {"status": "sincronizado", "total_horas": horas}
    
    raise HTTPException(status_code=404, detail="Usuário não encontrado.")

@app.get("/estatisticas")
def obter_estatisticas(email: str, token: str, db: Session = Depends(get_db)):
    email_limpo = email.strip().lower()
    verificar_seguranca_sessao(email_limpo, token, db)
    
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == email_limpo).first()
    questoes = db.query(HistoricoQuestoesModel).filter(HistoricoQuestoesModel.usuario_email == email_limpo).all()
    
    total = len(questoes)
    if total == 0:
        return {"total": 0, "acertos": 0, "percentual": "0.00%", "horas_estudadas": 0.0}
    
    acertos = sum(1 for q in questoes if q.resultado_acerto)
    percentual = (acertos / total) * 100
    horas = round(usuario.minutos_estudados / 60, 2) if usuario else 0.0
    
    return {
        "total": total,
        "acertos": acertos,
        "percentual": f"{percentual:.2f}%",
        "horas_estudadas": horas
    }

@app.get("/")
def ler_raiz():
    caminho_arquivo = "/app/frontend/index.html"
    return FileResponse(caminho_arquivo, media_type="text/html; charset=utf-8")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "modo": "ELITE (Banco Pré-Populado)",
        "ollama_url": OLLAMA_API_URL,
        "ollama_model": OLLAMA_MODEL
    }
