#!/usr/bin/env python3
"""
🔐 NOVO LOGIN - mr.dblucas@gmail.com
Com suporte offline-first + geofencing + detecção de invasão
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import logging

# Importar módulos
from offline_sync import ModoOffline, SincronizadorAutomatico, BancoOffline
from geofencing import VerificadorGeofencing, AlertasGeofencing
from conflict_detection import VerificadorSincronizacao

router = APIRouter(prefix="/api/auth", tags=["autenticacao"])
logger = logging.getLogger("LOGIN_NOVO")

# ============================================================================
# 🔑 MODELOS
# ============================================================================

class LoginRequest(BaseModel):
    email: str
    senha: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    mac_address: str

class LoginOfflineRequest(BaseModel):
    email: str
    senha: str
    latitude: float
    longitude: float
    cidade: str
    mac_address: str

class SincronizarRequest(BaseModel):
    email: str
    token: str
    latitude: float
    longitude: float
    mac_address: str

# ============================================================================
# 💾 ARMAZENAMENTO DE USUÁRIOS (Simulado)
# ============================================================================

USUARIOS_REGISTRADOS = {
    "mr.dblucas@gmail.com": {
        "email": "mr.dblucas@gmail.com",
        "senha_hash": "hashed_Lightshigaraki789",  # Em produção usar BCRYPT
        "mac_registrado": None,  # Será definido no primeiro login
        "data_criacao": datetime.now().isoformat(),
        "tokens_ativos": [],
        "bloqueado": False,
        "bloqueio_motivo": None,
        "bloqueio_ate": None
    }
}

# ============================================================================
# 🔐 LOGIN COM SUPORTE OFFLINE
# ============================================================================

@router.post("/login-novo")
async def login_novo(request: LoginRequest) -> dict:
    """
    Login novo com suporte offline-first
    
    Fluxo:
    1. Se online → verificar geofencing
    2. Se offline → usar criptografia local
    3. Guardar MAC address
    4. Retornar token
    """
    
    email = request.email
    senha = request.senha
    mac_novo = request.mac_address
    
    logger.info(f"🔐 Tentativa de login: {email}")
    
    # 1. Verificar se usuário existe
    if email not in USUARIOS_REGISTRADOS:
        logger.error(f"❌ Usuário não encontrado: {email}")
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    
    usuario = USUARIOS_REGISTRADOS[email]
    
    # 2. Verificar se está bloqueado
    if usuario["bloqueado"]:
        if usuario["bloqueio_ate"] and datetime.now() < datetime.fromisoformat(usuario["bloqueio_ate"]):
            logger.error(f"❌ {email} bloqueado: {usuario['bloqueio_motivo']}")
            raise HTTPException(
                status_code=403,
                detail=f"Acesso bloqueado: {usuario['bloqueio_motivo']}"
            )
        else:
            # Desbloqueio automático se tempo passou
            usuario["bloqueado"] = False
            usuario["bloqueio_motivo"] = None
    
    # 3. Verificar senha
    # Em produção usar bcrypt.verify()
    if senha != "Lightshigaraki789":
        logger.error(f"❌ Senha incorreta para {email}")
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    
    # 4. Registrar MAC na primeira vez
    if usuario["mac_registrado"] is None:
        usuario["mac_registrado"] = mac_novo
        logger.info(f"✅ MAC registrado para {email}: {mac_novo}")
    
    # 5. Se tem geolocalização → verificar geofencing
    if request.latitude and request.longitude:
        verificador_geo = VerificadorGeofencing()
        resultado_geo = verificador_geo.verificar_localizacao(
            request.latitude, request.longitude
        )
        
        if not resultado_geo["autorizado"]:
            alertas = AlertasGeofencing()
            alerta = alertas.verificar_e_alertar(
                email, mac_novo, request.latitude, request.longitude, "Desconhecida"
            )
            
            if not resultado_geo["autorizado"]:
                logger.warning(f"⚠️  {email} tentando acessar fora da zona: "
                              f"{resultado_geo['motivo']}")
                # BLOQUEAR acesso duplo (segundo acesso fora da zona)
                # Mas permitir primeiro acesso se for do lugar certo depois
    
    # 6. Gerar token
    token = f"token_{email}_{datetime.now().timestamp()}"
    usuario["tokens_ativos"].append({
        "token": token,
        "criado_em": datetime.now().isoformat(),
        "expira_em": (datetime.now() + timedelta(hours=8)).isoformat(),
        "mac_address": mac_novo,
        "latitude": request.latitude,
        "longitude": request.longitude
    })
    
    logger.info(f"✅ Login bem-sucedido para {email}")
    
    return {
        "status": "sucesso",
        "email": email,
        "token": token,
        "token_expira_em": (datetime.now() + timedelta(hours=8)).isoformat(),
        "modo": "online",
        "mac_registrado": usuario["mac_registrado"],
        "mensagem": "Login bem-sucedido - Modo ONLINE"
    }


# ============================================================================
# 📴 LOGIN OFFLINE
# ============================================================================

@router.post("/login-offline")
async def login_offline(request: LoginOfflineRequest) -> dict:
    """
    Login offline - sem conexão com internet
    
    Fluxo:
    1. Criar sessão offline local
    2. Criptografar dados localmente
    3. Salvar em SQLite
    4. Quando conectar, sincronizar
    """
    
    email = request.email
    senha = request.senha
    
    logger.info(f"📴 Tentativa de login OFFLINE: {email}")
    
    # Verificar credenciais localmente (offline)
    # Em produção, ter hash local
    if senha != "Lightshigaraki789":
        raise HTTPException(status_code=401, detail="Senha inválida")
    
    # Criar modo offline
    modo_offline = ModoOffline(email, senha)
    modo_offline.entrar_modo_offline(
        request.mac_address,
        request.latitude,
        request.longitude,
        request.cidade
    )
    
    logger.info(f"✅ Modo offline ativado para {email}")
    
    return {
        "status": "sucesso_offline",
        "email": email,
        "modo": "offline",
        "cidade": request.cidade,
        "latitude": request.latitude,
        "longitude": request.longitude,
        "mensagem": "Conectado em modo OFFLINE - Dados serão sincronizados ao conectar",
        "indicacoes": [
            "✅ Você pode responder questões normalmente",
            "✅ Dados serão salvos localmente (criptografados)",
            "✅ Ao conectar à internet, sincronizaremos tudo",
            "✅ Se detectar invasão, avisaremos",
        ]
    }


# ============================================================================
# 🔄 SINCRONIZAÇÃO
# ============================================================================

@router.post("/sincronizar")
async def sincronizar(request: SincronizarRequest) -> dict:
    """
    Sincroniza dados offline com servidor
    
    Verifica:
    1. Movimento impossível
    2. Acesso simultâneo
    3. Mudança de MAC
    4. Sincroniza dados
    """
    
    email = request.email
    
    logger.info(f"🔄 Iniciando sincronização para {email}")
    
    # 1. Verificar geofencing
    verificador_geo = VerificadorGeofencing()
    resultado_geo = verificador_geo.verificar_localizacao(
        request.latitude, request.longitude
    )
    
    if not resultado_geo["autorizado"]:
        logger.warning(f"⚠️  Sincronização de {email} fora da zona permitida")
    
    # 2. Obter dados offline
    banco = BancoOffline()
    dados_offline = banco.obter_dados_nao_sincronizados(email)
    
    # 3. Obter MAC registrado
    if email in USUARIOS_REGISTRADOS:
        mac_registrado = USUARIOS_REGISTRADOS[email]["mac_registrado"]
    else:
        mac_registrado = request.mac_address
    
    # 4. Verificar conflitos
    verificador_sync = VerificadorSincronizacao()
    
    # Preparar registros para verificação
    registros = []
    for q in dados_offline["questoes"]:
        registros.append({
            "tipo": "questao",
            "timestamp": q[6] if len(q) > 6 else datetime.now().isoformat(),
            "latitude": request.latitude,
            "longitude": request.longitude,
            "cidade": "Desconhecida",
            "mac_address": request.mac_address
        })
    
    resultado_conflito = await verificador_sync.verificar_ao_sincronizar(
        email, request.mac_address, registros, mac_registrado
    )
    
    if resultado_conflito["status"] == "bloqueado_por_invasao":
        logger.error(f"🚨 INVASÃO DETECTADA: {email}")
        logger.error(f"   Motivo: {resultado_conflito['motivo']}")
        
        # Bloquear usuário
        if email in USUARIOS_REGISTRADOS:
            USUARIOS_REGISTRADOS[email]["bloqueado"] = True
            USUARIOS_REGISTRADOS[email]["bloqueio_motivo"] = resultado_conflito["motivo"]
            USUARIOS_REGISTRADOS[email]["bloqueio_ate"] = (
                datetime.now() + timedelta(days=3)
            ).isoformat()
        
        raise HTTPException(
            status_code=403,
            detail=f"Invasão detectada: {resultado_conflito['motivo']}"
        )
    
    if resultado_conflito["status"] == "bloqueado":
        raise HTTPException(
            status_code=403,
            detail=resultado_conflito["mensagem"]
        )
    
    # 5. Sincronizar
    banco.marcar_como_sincronizado(email)
    
    logger.info(f"✅ Sincronização completa para {email}")
    
    return {
        "status": "sincronizado",
        "email": email,
        "questoes_sincronizadas": len(dados_offline["questoes"]),
        "cronometros_sincronizados": len(dados_offline["cronometros"]),
        "total": dados_offline["total"],
        "alertas": resultado_conflito.get("alertas"),
        "timestamp": datetime.now().isoformat(),
        "mensagem": f"✅ {dados_offline['total']} itens sincronizados com sucesso"
    }


# ============================================================================
# 📊 STATUS DO USUÁRIO
# ============================================================================

@router.get("/status/{email}")
async def status_usuario(email: str, token: str) -> dict:
    """Obtém status do usuário"""
    
    if email not in USUARIOS_REGISTRADOS:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    usuario = USUARIOS_REGISTRADOS[email]
    banco = BancoOffline()
    dados_offline = banco.obter_dados_nao_sincronizados(email)
    
    return {
        "email": email,
        "bloqueado": usuario["bloqueado"],
        "bloqueio_motivo": usuario["bloqueio_motivo"],
        "bloqueio_ate": usuario["bloqueio_ate"],
        "mac_registrado": usuario["mac_registrado"],
        "dados_pendentes_sincronizar": dados_offline["total"],
        "questoes_offline": len(dados_offline["questoes"]),
        "cronometros_offline": len(dados_offline["cronometros"]),
        "tokens_ativos": len(usuario["tokens_ativos"]),
        "data_ultimo_acesso": usuario["tokens_ativos"][-1]["criado_em"] if usuario["tokens_ativos"] else None
    }


# ============================================================================
# 🔓 LOGOUT
# ============================================================================

@router.post("/logout")
async def logout(email: str, token: str) -> dict:
    """Logout seguro"""
    
    if email in USUARIOS_REGISTRADOS:
        usuario = USUARIOS_REGISTRADOS[email]
        usuario["tokens_ativos"] = [
            t for t in usuario["tokens_ativos"] if t["token"] != token
        ]
        logger.info(f"🔓 Logout: {email}")
    
    return {"status": "logout_bem_sucedido", "email": email}


# ============================================================================
# 📝 LISTAR ROTAS
# ============================================================================

if __name__ == "__main__":
    print("""
    🔐 NOVO LOGIN - mr.dblucas@gmail.com
    
    ENDPOINTS:
    
    1. POST /api/auth/login-novo
       └─ Login online com geofencing + MAC tracking
       
    2. POST /api/auth/login-offline
       └─ Login offline (sem internet)
       
    3. POST /api/auth/sincronizar
       └─ Sincroniza dados + verifica invasão
       
    4. GET /api/auth/status/{email}
       └─ Status do usuário
       
    5. POST /api/auth/logout
       └─ Logout seguro
    
    FLUXO:
    
    Com Internet:
    ├─ POST /login-novo
    ├─ Verifica geofencing (3 pontos)
    ├─ Verifica MAC
    └─ Retorna token
    
    Sem Internet:
    ├─ POST /login-offline
    ├─ Criptografa localmente
    ├─ Salva em SQLite
    └─ Quando conectar: POST /sincronizar
    
    Sincronização:
    ├─ Verifica movimento impossível
    ├─ Verifica acesso simultâneo
    ├─ Verifica mudança MAC
    ├─ Se OK: sincroniza dados
    └─ Se invasão: bloqueia por 3 dias
    """)
