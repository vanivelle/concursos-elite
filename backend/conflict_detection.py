#!/usr/bin/env python3
"""
🚨 DETECÇÃO DE CONFLITOS E INVASÕES
Verifica sincronização para detectar acessos suspeitos
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

# ============================================================================
# 🔍 DETECTOR DE CONFLITOS
# ============================================================================

class DetectorConflitos:
    """Detecta conflitos ao sincronizar dados"""
    
    def __init__(self):
        self.logger = logging.getLogger("DETECTOR_CONFLITOS")
    
    def verificar_movimento_impossivel(self, registros: List[Dict]) -> Dict:
        """
        Verifica se há movimento impossível entre registros
        (exemplo: São Paulo para Brasília em 5 minutos)
        """
        conflitos = []
        
        # Ordenar por timestamp
        registros_ordenados = sorted(registros, 
                                    key=lambda x: datetime.fromisoformat(x.get("timestamp", "")))
        
        for i in range(len(registros_ordenados) - 1):
            reg1 = registros_ordenados[i]
            reg2 = registros_ordenados[i + 1]
            
            # Calcular diferença de tempo
            tempo1 = datetime.fromisoformat(reg1.get("timestamp", ""))
            tempo2 = datetime.fromisoformat(reg2.get("timestamp", ""))
            diferenca_minutos = (tempo2 - tempo1).total_seconds() / 60
            
            # Calcular distância (Haversine)
            from math import radians, sin, cos, sqrt, atan2
            
            lat1, lon1 = reg1.get("latitude", 0), reg1.get("longitude", 0)
            lat2, lon2 = reg2.get("latitude", 0), reg2.get("longitude", 0)
            
            R = 6371  # Raio Terra km
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distancia_km = R * c
            
            # Velocidade necessária (km/min)
            if diferenca_minutos > 0:
                velocidade_kmh = (distancia_km / diferenca_minutos) * 60
            else:
                velocidade_kmh = float('inf')
            
            # Verificar movimento impossível (>900 km/h é supersônico)
            if velocidade_kmh > 900 and diferenca_minutos < 60:
                conflito = {
                    "tipo": "MOVIMENTO_IMPOSSIVEL",
                    "severidade": "ALTA",
                    "de": reg1.get("cidade", "Desconhecido"),
                    "para": reg2.get("cidade", "Desconhecido"),
                    "distancia_km": round(distancia_km, 2),
                    "tempo_minutos": round(diferenca_minutos, 2),
                    "velocidade_kmh": round(velocidade_kmh, 2),
                    "timestamp1": reg1.get("timestamp"),
                    "timestamp2": reg2.get("timestamp"),
                    "motivo": f"Movimento de {distancia_km:.0f}km em {diferenca_minutos:.0f}min "
                             f"({velocidade_kmh:.0f}km/h - impossível!)"
                }
                conflitos.append(conflito)
                self.logger.warning(f"🚨 CONFLITO: {conflito['motivo']}")
        
        return {
            "conflitos": conflitos,
            "total_conflitos": len(conflitos),
            "movimento_suspeitoso": len(conflitos) > 0
        }
    
    def verificar_acesso_simultaneo(self, registros: List[Dict]) -> Dict:
        """
        Verifica acessos simultâneos em locais diferentes
        (indica alguém usando conta ao mesmo tempo)
        """
        conflitos = []
        
        for i in range(len(registros)):
            for j in range(i + 1, len(registros)):
                reg1 = registros[i]
                reg2 = registros[j]
                
                # Comparar timestamps (diferença < 5 minutos = simultâneo)
                tempo1 = datetime.fromisoformat(reg1.get("timestamp", ""))
                tempo2 = datetime.fromisoformat(reg2.get("timestamp", ""))
                diferenca = abs((tempo2 - tempo1).total_seconds() / 60)
                
                # Se diferença < 5 minutos e locais diferentes = suspeitoso
                if diferenca < 5:
                    lat1, lon1 = reg1.get("latitude"), reg1.get("longitude")
                    lat2, lon2 = reg2.get("latitude"), reg2.get("longitude")
                    
                    # Se distância > 10km = acesso simultâneo suspeito
                    if abs(lat1 - lat2) > 0.1 or abs(lon1 - lon2) > 0.1:
                        conflito = {
                            "tipo": "ACESSO_SIMULTANEO",
                            "severidade": "CRITICA",
                            "local1": reg1.get("cidade"),
                            "local2": reg2.get("cidade"),
                            "timestamp1": reg1.get("timestamp"),
                            "timestamp2": reg2.get("timestamp"),
                            "diferenca_minutos": round(diferenca, 2),
                            "mac1": reg1.get("mac_address"),
                            "mac2": reg2.get("mac_address"),
                            "motivo": f"Acesso simultâneo em {reg1.get('cidade')} "
                                     f"e {reg2.get('cidade')} com {diferenca:.0f}min de diferença!"
                        }
                        conflitos.append(conflito)
                        self.logger.error(f"🚨 CRÍTICO: {conflito['motivo']}")
        
        return {
            "conflitos": conflitos,
            "total_conflitos": len(conflitos),
            "acesso_simultaneo_detectado": len(conflitos) > 0
        }
    
    def verificar_mudanca_mac(self, email: str, mac_novo: str, 
                             mac_registrado: str) -> Dict:
        """Verifica se MAC address mudou"""
        
        if mac_novo.upper() != mac_registrado.upper():
            alerta = {
                "tipo": "MUDANCA_MAC",
                "severidade": "MEDIA",
                "email": email,
                "mac_antigo": mac_registrado,
                "mac_novo": mac_novo,
                "motivo": "MAC address diferente do registrado - verificar se é device legítimo",
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.warning(f"⚠️  ALERTA: MAC mudou para {email}")
            return alerta
        
        return {"tipo": "OK", "mac_verificado": True}


# ============================================================================
# 🔐 GERENCIADOR DE BLOQUEIOS
# ============================================================================

class GerenciadorBloqueios:
    """Gerencia bloqueios de acesso após detectar invasão"""
    
    def __init__(self):
        self.logger = logging.getLogger("GERENCIADOR_BLOQUEIOS")
        self.bloqueios = {}  # {email: {timestamp, motivo, severidade}}
    
    def bloquear_acesso(self, email: str, motivo: str, 
                       severidade: str, duracao_horas: int = 24) -> Dict:
        """Bloqueia acesso de um usuário"""
        
        agora = datetime.now()
        desbloqueio = agora + timedelta(hours=duracao_horas)
        
        self.bloqueios[email] = {
            "motivo": motivo,
            "severidade": severidade,
            "bloqueado_em": agora.isoformat(),
            "desbloqueio_em": desbloqueio.isoformat(),
            "duracao_horas": duracao_horas
        }
        
        self.logger.critical(f"🔒 BLOQUEADO: {email} por {duracao_horas}h")
        self.logger.critical(f"   Motivo: {motivo}")
        
        return self.bloqueios[email]
    
    def desbloquear_acesso(self, email: str) -> Dict:
        """Desbloqueia acesso de um usuário"""
        
        if email in self.bloqueios:
            del self.bloqueios[email]
            self.logger.info(f"🔓 DESBLOQUEADO: {email}")
            return {"status": "desbloqueado"}
        
        return {"status": "nao_estava_bloqueado"}
    
    def verificar_bloqueio(self, email: str) -> Dict:
        """Verifica se usuário está bloqueado"""
        
        if email not in self.bloqueios:
            return {"bloqueado": False}
        
        bloqueio = self.bloqueios[email]
        desbloqueio = datetime.fromisoformat(bloqueio["desbloqueio_em"])
        
        if datetime.now() > desbloqueio:
            # Tempo de bloqueio passou
            self.desbloquear_acesso(email)
            return {"bloqueado": False}
        
        return {
            "bloqueado": True,
            "motivo": bloqueio["motivo"],
            "severidade": bloqueio["severidade"],
            "desbloqueio_em": bloqueio["desbloqueio_em"]
        }


# ============================================================================
# 🔄 VERIFICADOR DE SINCRONIZAÇÃO
# ============================================================================

class VerificadorSincronizacao:
    """Verifica integridade ao sincronizar"""
    
    def __init__(self):
        self.logger = logging.getLogger("VERIFICADOR_SYNC")
        self.detector = DetectorConflitos()
        self.gerenciador = GerenciadorBloqueios()
    
    async def verificar_ao_sincronizar(self, email: str, mac_novo: str, 
                                      registros: List[Dict], 
                                      mac_registrado: str) -> Dict:
        """Verifica antes de sincronizar"""
        
        self.logger.info(f"🔍 Verificando sincronização de {email}")
        
        # 1. Verificar bloqueio
        bloqueio = self.gerenciador.verificar_bloqueio(email)
        if bloqueio["bloqueado"]:
            return {
                "status": "bloqueado",
                "mensagem": f"Acesso bloqueado: {bloqueio['motivo']}",
                "desbloqueio_em": bloqueio["desbloqueio_em"]
            }
        
        # 2. Verificar movimento impossível
        resultado_movimento = self.detector.verificar_movimento_impossivel(registros)
        if resultado_movimento["movimento_suspeitoso"]:
            self.gerenciador.bloquear_acesso(
                email,
                f"Movimento impossível detectado: {resultado_movimento['conflitos'][0]['motivo']}",
                "ALTA",
                duracao_horas=24
            )
            return {
                "status": "bloqueado_por_invasao",
                "motivo": "Movimento impossível",
                "detalhes": resultado_movimento["conflitos"][0]
            }
        
        # 3. Verificar acesso simultâneo
        resultado_simultaneo = self.detector.verificar_acesso_simultaneo(registros)
        if resultado_simultaneo["acesso_simultaneo_detectado"]:
            self.gerenciador.bloquear_acesso(
                email,
                f"Acesso simultâneo detectado: {resultado_simultaneo['conflitos'][0]['motivo']}",
                "CRITICA",
                duracao_horas=72  # 3 dias
            )
            return {
                "status": "bloqueado_por_invasao",
                "motivo": "Acesso simultâneo",
                "detalhes": resultado_simultaneo["conflitos"][0]
            }
        
        # 4. Verificar mudança MAC
        resultado_mac = self.detector.verificar_mudanca_mac(email, mac_novo, mac_registrado)
        if resultado_mac["tipo"] != "OK":
            self.logger.warning(f"⚠️  {resultado_mac['motivo']}")
        
        # Tudo ok
        self.logger.info(f"✅ Sincronização segura para {email}")
        return {
            "status": "permitido",
            "mensagem": "Sincronização segura",
            "alertas": resultado_mac if resultado_mac["tipo"] != "OK" else None
        }


# ============================================================================
# 📝 EXEMPLO
# ============================================================================

if __name__ == "__main__":
    print("""
    🚨 DETECTOR DE INVASÃO
    
    Verifica durante sincronização:
    1. Movimento impossível (ex: SP para Brasília em 5min)
    2. Acesso simultâneo (conta em 2 lugares ao mesmo tempo)
    3. Mudança de MAC address
    
    Se detectar:
    - Bloqueia acesso
    - Alerta admin
    - Registra em logs
    
    Severidades:
    - MEDIA: Mudança MAC (pode ser novo device)
    - ALTA: Movimento impossível (pode ser invasão)
    - CRITICA: Acesso simultâneo (certeza de invasão)
    """)
