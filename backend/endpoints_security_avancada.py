"""
🔒 ENDPOINTS AVANÇADOS DE SEGURANÇA
Adicione estes endpoints ao main_enterprise.py
"""

# ============================================================
# NOVO ENDPOINT: Verificar bloqueios de segurança
# ============================================================

@app.get("/security/bloqueios-status")
async def verificar_bloqueios_seguranca(request: Request):
    """
    Verifica status de bloqueios de segurança para IP do cliente
    Retorna detalhes sobre IPv6, VPN, VM e GPU Cloud
    """
    
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    
    hostname = ""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
    except (socket.herror, OSError):
        hostname = f"ip-{ip.replace('.', '-')}"
    
    # Executar verificação completa
    resultado = DetectorSegurancaAvancada.verificacao_completa(
        ip, user_agent, hostname
    )
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "seu_ip": ip,
        "hostname": hostname,
        "status_geral": resultado["status"],
        "acesso_permitido": not resultado["bloqueado"],
        "bloqueios_detectados": resultado["razoes"],
        "detalhes": resultado["detalhes"],
        "mensagem": resultado["mensagem"]
    }


# ============================================================
# NOVO ENDPOINT: Listar tipos de bloqueios
# ============================================================

@app.get("/security/tipos-bloqueio")
async def listar_tipos_bloqueio():
    """Lista todos os tipos de bloqueio implementados"""
    
    return {
        "bloqueios_implementados": [
            {
                "tipo": "IPv6",
                "descricao": "Bloqueio de conexões via IPv6",
                "motivo": "Segurança: Força uso de IPv4 verificável",
                "status": "✅ ATIVO"
            },
            {
                "tipo": "VPN/Tor",
                "descricao": "Bloqueio de VPN e rede Tor",
                "motivo": "Segurança: Impede anonimização de IP",
                "vpn_providers_detectadas": [
                    "NordVPN", "ExpressVPN", "Surfshark", "Mullvad",
                    "ProtonVPN", "CyberGhost", "Windscribe", "IPVanish",
                    "Hotspot Shield", "Private Internet Access"
                ],
                "status": "✅ ATIVO"
            },
            {
                "tipo": "Máquina Virtual",
                "descricao": "Bloqueio de acesso via VM (VirtualBox, VMware, etc)",
                "motivo": "Segurança: Força acesso de dispositivo real",
                "vm_detectadas": [
                    "VirtualBox", "VMware", "Parallels", "QEMU", "Xen",
                    "Hyper-V", "Vagrant", "Docker", "Proxmox", "KVM"
                ],
                "status": "✅ ATIVO"
            },
            {
                "tipo": "GPU Cloud",
                "descricao": "Bloqueio de acesso via ambientes cloud",
                "motivo": "Segurança: Impede acesso via GPUs/servidores em nuvem",
                "cloud_providers_detectados": [
                    "AWS", "Azure", "Google Cloud Platform", "Linode",
                    "DigitalOcean", "Heroku", "Vultr", "Kaggle Colab"
                ],
                "status": "✅ ATIVO"
            }
        ],
        "total_bloqueios": 4,
        "status_geral": "🔒 SISTEMA COMPLETO DE BLOQUEIOS ATIVO"
    }


# ============================================================
# NOVO ENDPOINT: Histórico de bloqueios (auditoria)
# ============================================================

@app.get("/security/historico-bloqueios")
async def obter_historico_bloqueios(token: str = Depends(verificar_token_jwt)):
    """
    Obtém histórico de bloqueios de segurança
    Requer autenticação JWT
    """
    
    db = SessionLocal()
    
    try:
        # Buscar usuario
        usuario = db.query(UsuarioModel).filter_by(email=token).first()
        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        # Buscar logins falhados
        logins_falhados = db.query(LoginAuditadoModel).filter(
            LoginAuditadoModel.email == usuario.email,
            LoginAuditadoModel.sucesso == False
        ).order_by(LoginAuditadoModel.timestamp.desc()).limit(50).all()
        
        return {
            "usuario": usuario.email,
            "total_bloqueios": len(logins_falhados),
            "historico": [
                {
                    "timestamp": l.timestamp.isoformat(),
                    "ip": l.ip,
                    "mac": l.mac_address,
                    "cidade": l.cidade,
                    "sucesso": l.sucesso
                }
                for l in logins_falhados
            ]
        }
    
    finally:
        db.close()


# ============================================================
# NOVO ENDPOINT: Teste de conectividade (debug)
# ============================================================

@app.get("/security/teste-bloqueios")
async def testar_bloqueios(request: Request):
    """
    Executa teste de conectividade mostrando detalhes do cliente
    Útil para debug
    """
    
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    
    # Tentar descobrir informações adicionais
    try:
        hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
    except:
        hostname = "desconhecido"
        ipaddrlist = [ip]
    
    # Testar IPv6
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        eh_ipv6 = True
    except:
        eh_ipv6 = False
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "seu_ip": ip,
        "versao_ip": "IPv6" if eh_ipv6 else "IPv4",
        "hostname": hostname,
        "user_agent": user_agent,
        "headers_completos": dict(request.headers),
        "nota": "Este endpoint é apenas para debug. Em produção, use /security/bloqueios-status"
    }
