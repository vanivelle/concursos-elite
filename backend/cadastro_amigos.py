#!/usr/bin/env python3
"""
👥 ENDPOINT DE CADASTRO - Convidar Amigos
Apenas admin (mr.dblucas) pode convidar
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import logging

router = APIRouter(prefix="/api/users", tags=["usuarios"])
logger = logging.getLogger("CADASTRO_AMIGOS")

# ============================================================================
# 👥 MODELOS
# ============================================================================

class CadastroRequest(BaseModel):
    nome: str
    email: str
    senha: str
    convite_por: str  # Email do admin que convidou

class ConviteRequest(BaseModel):
    email_amigo: str
    nome_amigo: str
    admin_email: str  # Deve ser mr.dblucas@gmail.com

# ============================================================================
# 📋 BANCO DE USUÁRIOS SIMULADO
# ============================================================================

USUARIOS = {
    "mr.dblucas@gmail.com": {
        "nome": "Admin",
        "email": "mr.dblucas@gmail.com",
        "tipo": "admin",
        "offline_permitido": True,
        "criado_em": datetime.now().isoformat(),
        "convidados": []
    }
}

# ============================================================================
# 🔐 CADASTRO SIMPLES
# ============================================================================

@router.post("/cadastro")
async def cadastro(request: CadastroRequest) -> dict:
    """
    Cadastro de novo usuário
    Pode ser convidado por admin ou se registrar sozinho (sem offline)
    """
    
    email = request.email.lower()
    
    # Verificar se já existe
    if email in USUARIOS:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    # Verificar se foi convidado por admin
    offline_permitido = False
    if request.convite_por == "mr.dblucas@gmail.com":
        offline_permitido = True
        logger.info(f"✅ {email} convidado por admin para teste")
    
    # Criar usuário
    USUARIOS[email] = {
        "nome": request.nome,
        "email": email,
        "tipo": "usuario",
        "offline_permitido": offline_permitido,
        "criado_em": datetime.now().isoformat(),
        "convidados_por": request.convite_por
    }
    
    logger.info(f"✅ Novo usuário cadastrado: {email} (offline: {offline_permitido})")
    
    return {
        "status": "cadastro_bem_sucedido",
        "email": email,
        "nome": request.nome,
        "offline_permitido": offline_permitido,
        "mensagem": f"Bem-vindo {request.nome}!" if not offline_permitido else f"Bem-vindo {request.nome}! Modo offline ativado para teste."
    }


# ============================================================================
# 📨 CONVITE DE AMIGOS (Apenas Admin)
# ============================================================================

@router.post("/convidar")
async def convidar_amigo(request: ConviteRequest) -> dict:
    """
    Admin convida amigo para testar
    """
    
    # Verificar se é admin
    if request.admin_email != "mr.dblucas@gmail.com":
        raise HTTPException(status_code=403, detail="Apenas admin pode convidar")
    
    email_amigo = request.email_amigo.lower()
    
    # Verificar se já está registrado
    if email_amigo in USUARIOS:
        raise HTTPException(status_code=400, detail="Este email já está registrado")
    
    # Registrar convite
    if "mr.dblucas@gmail.com" in USUARIOS:
        USUARIOS["mr.dblucas@gmail.com"]["convidados"].append({
            "email": email_amigo,
            "nome": request.nome_amigo,
            "convidado_em": datetime.now().isoformat(),
            "status": "aguardando_cadastro"
        })
    
    logger.info(f"📨 Convite enviado para {email_amigo} por {request.admin_email}")
    
    return {
        "status": "convite_enviado",
        "email_amigo": email_amigo,
        "nome_amigo": request.nome_amigo,
        "link_cadastro": f"https://open-notebook-8x8twkj23.vercel.app?convite={email_amigo}",
        "instrucoes": [
            f"Seu amigo {request.nome_amigo} pode acessar:",
            "https://open-notebook-8x8twkj23.vercel.app",
            "Email: " + email_amigo,
            "Senha: será criada no primeiro acesso",
            "",
            "🛡️ Ele testará o BLOQUEIO junto com você!"
        ]
    }


# ============================================================================
# 📊 LISTAR USUÁRIOS (Admin)
# ============================================================================

@router.get("/listar")
async def listar_usuarios(admin_email: str) -> dict:
    """Admin vê todos os usuários registrados"""
    
    if admin_email != "mr.dblucas@gmail.com":
        raise HTTPException(status_code=403, detail="Apenas admin")
    
    usuarios_lista = []
    for email, dados in USUARIOS.items():
        usuarios_lista.append({
            "email": email,
            "nome": dados["nome"],
            "tipo": dados["tipo"],
            "offline_permitido": dados.get("offline_permitido", False),
            "criado_em": dados["criado_em"]
        })
    
    return {
        "total": len(usuarios_lista),
        "usuarios": usuarios_lista,
        "convidados_pendentes": len(USUARIOS["mr.dblucas@gmail.com"]["convidados"])
    }


# ============================================================================
# 🗑️ DELETAR USUÁRIO (Admin)
# ============================================================================

@router.delete("/deletar/{email}")
async def deletar_usuario(email: str, admin_email: str) -> dict:
    """Admin deleta usuário"""
    
    if admin_email != "mr.dblucas@gmail.com":
        raise HTTPException(status_code=403, detail="Apenas admin")
    
    if email not in USUARIOS:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if email == "mr.dblucas@gmail.com":
        raise HTTPException(status_code=400, detail="Não pode deletar admin")
    
    nome = USUARIOS[email]["nome"]
    del USUARIOS[email]
    
    logger.warning(f"🗑️ Usuário deletado: {email}")
    
    return {
        "status": "usuario_deletado",
        "email": email,
        "nome": nome
    }


if __name__ == "__main__":
    print("""
    👥 ENDPOINT DE CADASTRO
    
    ENDPOINTS:
    
    1. POST /api/users/cadastro
       └─ Novo usuário se registra
       
    2. POST /api/users/convidar
       └─ Admin convida amigo
       └─ Amigo recebe link + credenciais
       
    3. GET /api/users/listar
       └─ Admin vê todos os usuários
       
    4. DELETE /api/users/deletar/{email}
       └─ Admin deleta usuário
    
    FLUXO:
    
    1. Admin chama POST /convidar com email do Cabo
    2. Sistema gera link com código do convite
    3. Cabo acessa link e se cadastra
    4. Cabo faz login (com offline)
    5. Admin + Cabo testam BLOQUEIO
    """)
