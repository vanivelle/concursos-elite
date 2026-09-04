"""FastAPI Backend com Supabase - SEM DOCKER"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import json

# ============ SUPABASE CONNECTION ============
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise ValueError("ERROR: DATABASE_URL environment variable not set. Set it before starting the application.")

def get_db():
    try:
        conn = psycopg2.connect(DB_URL)
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao Supabase: {e}")
        raise

# ============ FASTAPI APP ============
app = FastAPI(title="Concurso Elite API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# ============ USUARIOS PRE-CADASTRADOS ============
USUARIOS = {
    "mr.dblucas@gmail.com": {"password": "Lightshigaraki789", "name": "Admin"},
    "cabo.md@email.com": {"password": "cabo123", "name": "Cabo MD"},
    "matheus@email.com": {"password": "matheus123", "name": "Matheus"},
}

# ============ ENDPOINTS ============
@app.get("/health")
async def health():
    """Health check"""
    try:
        conn = get_db()
        conn.close()
        return {"status": "OK", "database": "Supabase Online"}
    except:
        return {"status": "ERROR", "database": "Supabase Offline"}

@app.post("/api/auth/login-novo")
async def login_novo(request: LoginRequest):
    """Login com geofencing"""
    email = request.email.lower()
    password = request.password
    
    # Verificar usuário
    if email not in USUARIOS:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    # Verificar senha
    if USUARIOS[email]["password"] != password:
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    # Gerar token (simples)
    token = f"token_{email}_{int(datetime.now().timestamp())}"
    
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
