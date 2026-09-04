"""FastAPI Backend com Supabase - SEM DOCKER"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import jwt
from jose import JWTError
import logging
import sys

# Logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============ SUPABASE CONNECTION ============
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    logger.critical("❌ DATABASE_URL não configurada")
    sys.exit(1)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"

# CORS seguro para produção
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

def get_db(timeout=10):
    """Get database connection with timeout"""
    try:
        conn = psycopg2.connect(DB_URL, connect_timeout=timeout)
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"❌ Supabase offline: {e}")
        raise HTTPException(status_code=503, detail="Database offline")
    except Exception as e:
        logger.error(f"❌ Erro ao conectar: {e}")
        raise

# ============ FASTAPI APP ============
app = FastAPI(
    title="Concurso Elite API",
    version="3.3.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# CORS com segurança para produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# ============ MODELOS ============
class LoginRequest(BaseModel):
    email: str
    password: str
    latitude: float = None
    longitude: float = None

class LoginResponse(BaseModel):
    status: str
    access_token: str = None
    email: str = None
    message: str = None

# ============ JWT FUNCTIONS ============
def criar_access_token(email: str, expires_delta: timedelta = None):
    """Cria JWT token válido"""
    if expires_delta is None:
        expires_delta = timedelta(hours=24)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"✅ JWT criado para {email}")
    return encoded_jwt

def verificar_token(token: str):
    """Valida JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None

# ============ USUARIOS PRE-CADASTRADOS ============
USUARIOS = {
    "mr.dblucas@gmail.com": {"password": "Lightshigaraki789", "name": "Admin"},
    "cabo.md@email.com": {"password": "cabo123", "name": "Cabo MD"},
    "matheus@email.com": {"password": "matheus123", "name": "Matheus"},
}

# ============ ENDPOINTS ============
@app.get("/health")
async def health():
    """Health check com detalhes de sistema"""
    try:
        conn = get_db(timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        logger.info("✅ Health check OK - database online")
        return {
            "status": "OK",
            "database": "Online",
            "version": "3.3.0",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return {
            "status": "ERROR",
            "database": "Offline",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@app.post("/api/auth/login-novo")
async def login_novo(request: LoginRequest):
    """Login com geofencing e JWT token"""
    email = request.email.lower()
    password = request.password
    
    # Verificar usuário
    if email not in USUARIOS:
        logger.warning(f"❌ Tentativa login: {email} (não encontrado)")
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    # Verificar senha
    if USUARIOS[email]["password"] != password:
        logger.warning(f"❌ Tentativa login: {email} (senha errada)")
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    # Validar geofencing se coordenadas fornecidas
    if request.latitude and request.longitude:
        # TODO: Integrar validação de geofencing aqui
        logger.info(f"📍 Geofencing check: {email} at ({request.latitude}, {request.longitude})")
    
    # Gerar JWT token válido (24 horas de validade)
    token = criar_access_token(email, expires_delta=timedelta(hours=24))
    logger.info(f"✅ Login bem-sucedido: {email}")
    
    return {
        "status": "sucesso",
        "access_token": token,
        "email": email,
        "name": USUARIOS[email]["name"],
        "message": f"Login bem-sucedido! Bem-vindo {USUARIOS[email]['name']}"
    }

@app.post("/api/auth/login-offline")
async def login_offline(request: LoginRequest):
    """Login offline"""
    email = request.email.lower()
    password = request.password
    
    if email not in USUARIOS:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    if USUARIOS[email]["password"] != password:
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    token = f"offline_token_{email}_{int(datetime.now().timestamp())}"
    
    return {
        "status": "sucesso",
        "access_token": token,
        "email": email,
        "name": USUARIOS[email]["name"],
        "offline_key": f"cipher_{email}",
    }

@app.get("/api/auth/status/{email}")
async def get_status(email: str):
    """Status do usuário"""
    email = email.lower()
    if email not in USUARIOS:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "email": email,
        "name": USUARIOS[email]["name"],
        "status": "online",
        "last_sync": datetime.now().isoformat()
    }

@app.get("/docs")
async def docs():
    """Documentação"""
    return {"message": "API pronta! Use /login-novo para autenticar"}

# ============ RUN ============
if __name__ == "__main__":
    import uvicorn
    print("🚀 Backend Supabase iniciando...")
    print("📊 Usuários disponíveis:")
    for email in USUARIOS:
        print(f"   ✓ {email}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
