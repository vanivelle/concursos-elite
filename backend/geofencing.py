#!/usr/bin/env python3
"""
📍 GEOFENCING - 3 PONTOS DE CONFIANÇA
Apenas: Valparaíso 2, Gama (14h), SENAI (manhã)
"""

from typing import Dict, Tuple, Optional
from datetime import datetime, time
import math
import logging

# ============================================================================
# 🗺️ CONFIGURAÇÃO DE PONTOS CONFIÁVEIS
# ============================================================================

PONTOS_CONFIANCIA = {
    "valparaiso_2": {
        "nome": "Valparaíso 2, Céu Azul",
        "latitude": -15.8268,  # Brasília - Valparaíso II
        "longitude": -48.0409,
        "raio_metros": 500,    # 500m de tolerância
        "horario_inicio": "00:00",
        "horario_fim": "23:59",
        "dias": ["seg", "ter", "qua", "qui", "sex", "sab", "dom"],
        "descricao": "Casa - Qualquer hora"
    },
    
    "gama": {
        "nome": "GAMA",
        "latitude": -15.8500,  # Gama - Brasília
        "longitude": -48.0600,
        "raio_metros": 1000,   # 1km de tolerância
        "horario_inicio": "14:00",
        "horario_fim": "22:00",  # 14h até 22h
        "dias": ["seg", "ter", "qua", "qui", "sex"],
        "descricao": "Trabalho - 14h em diante"
    },
    
    "senai": {
        "nome": "SENAI",
        "latitude": -15.7975,  # SENAI - Brasília (estimado)
        "longitude": -48.0494,
        "raio_metros": 500,    # 500m de tolerância
        "horario_inicio": "08:00",
        "horario_fim": "13:00",  # Manhã até 13h
        "dias": ["seg", "ter", "qua", "qui", "sex"],
        "descricao": "SENAI - Manhã (até 13h)"
    }
}


# ============================================================================
# 📍 CALCULADORA DE DISTÂNCIA (HAVERSINE)
# ============================================================================

class CalculadoraDistancia:
    """Calcula distância entre duas coordenadas"""
    
    @staticmethod
    def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula distância em metros entre dois pontos (Haversine)
        lat/lon em graus decimais
        """
        R = 6371000  # Raio da Terra em metros
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c


# ============================================================================
# 🔒 VERIFICADOR DE GEOFENCING
# ============================================================================

class VerificadorGeofencing:
    """Verifica se local é permitido (geofencing)"""
    
    def __init__(self):
        self.logger = logging.getLogger("GEOFENCING")
        self.calculadora = CalculadoraDistancia()
    
    def _verificar_horario(self, ponto: Dict, agora: datetime) -> bool:
        """Verifica se horário está dentro do permitido"""
        hora_inicio = datetime.strptime(ponto["horario_inicio"], "%H:%M").time()
        hora_fim = datetime.strptime(ponto["horario_fim"], "%H:%M").time()
        hora_atual = agora.time()
        
        return hora_inicio <= hora_atual <= hora_fim
    
    def _verificar_dia(self, ponto: Dict, agora: datetime) -> bool:
        """Verifica se dia da semana é permitido"""
        dias_semana = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
        dia_num = agora.weekday()  # 0=seg, 6=dom
        dia_permitido = dias_semana[dia_num]
        
        return dia_permitido in ponto["dias"]
    
    def _calcular_distancia_para_ponto(self, lat: float, lon: float, 
                                       ponto: Dict) -> float:
        """Calcula distância até um ponto confiável"""
        return self.calculadora.haversine(
            lat, lon,
            ponto["latitude"],
            ponto["longitude"]
        )
    
    def verificar_localizacao(self, lat: float, lon: float) -> Dict:
        """
        Verifica se localização está em ponto confiável
        Retorna: {autorizado, ponto, distancia, motivo}
        """
        agora = datetime.now()
        resultados = []
        
        for chave, ponto in PONTOS_CONFIANCIA.items():
            distancia = self._calcular_distancia_para_ponto(lat, lon, ponto)
            
            # Verificar se dentro do raio
            dentro_raio = distancia <= ponto["raio_metros"]
            
            # Verificar horário
            horario_ok = self._verificar_horario(ponto, agora)
            
            # Verificar dia
            dia_ok = self._verificar_dia(ponto, agora)
            
            # Tudo ok?
            autorizado = dentro_raio and horario_ok and dia_ok
            
            resultados.append({
                "ponto": ponto["nome"],
                "chave": chave,
                "distancia_metros": round(distancia, 2),
                "dentro_raio": dentro_raio,
                "horario_ok": horario_ok,
                "dia_ok": dia_ok,
                "autorizado": autorizado,
                "descricao": ponto["descricao"]
            })
            
            if autorizado:
                self.logger.info(f"✅ Localização autorizada: {ponto['nome']}")
                return {
                    "autorizado": True,
                    "ponto_autorizado": chave,
                    "nome_ponto": ponto["nome"],
                    "distancia_metros": round(distancia, 2),
                    "motivo": f"Dentro de {ponto['nome']}"
                }
        
        # Nenhum ponto autorizado
        ponto_mais_proximo = min(resultados, key=lambda x: x["distancia_metros"])
        
        self.logger.warning(f"❌ Localização não autorizada")
        self.logger.info(f"   Ponto mais próximo: {ponto_mais_proximo['ponto']} "
                        f"({ponto_mais_proximo['distancia_metros']}m)")
        
        return {
            "autorizado": False,
            "ponto_mais_proximo": ponto_mais_proximo["chave"],
            "distancia_metros": ponto_mais_proximo["distancia_metros"],
            "nome_ponto": ponto_mais_proximo["ponto"],
            "motivo": f"Fora de zona permitida. "
                     f"Mais próximo: {ponto_mais_proximo['ponto']} "
                     f"({ponto_mais_proximo['distancia_metros']}m)",
            "detalhes": resultados
        }
    
    def obter_proximos_pontos(self, lat: float, lon: float) -> list:
        """Retorna pontos confiáveis ordenados por distância"""
        resultados = []
        
        for chave, ponto in PONTOS_CONFIANCIA.items():
            distancia = self._calcular_distancia_para_ponto(lat, lon, ponto)
            resultados.append({
                "chave": chave,
                "nome": ponto["nome"],
                "distancia_metros": round(distancia, 2),
                "horario": f"{ponto['horario_inicio']} - {ponto['horario_fim']}"
            })
        
        # Ordenar por distância
        resultados.sort(key=lambda x: x["distancia_metros"])
        return resultados


# ============================================================================
# 🚨 ALERTAS DE GEOFENCING
# ============================================================================

class AlertasGeofencing:
    """Gera alertas quando usuário sai dos pontos permitidos"""
    
    def __init__(self):
        self.logger = logging.getLogger("ALERTAS_GEOFENCING")
        self.verificador = VerificadorGeofencing()
    
    def verificar_e_alertar(self, email: str, mac: str, lat: float, 
                           lon: float, cidade: str) -> Dict:
        """Verifica localização e gera alertas se necessário"""
        verificacao = self.verificador.verificar_localizacao(lat, lon)
        
        if verificacao["autorizado"]:
            self.logger.info(f"✅ {email} em local autorizado: "
                            f"{verificacao['nome_ponto']}")
            return {
                "autorizado": True,
                "alerta": False,
                "mensagem": f"Login de {email} em {verificacao['nome_ponto']}"
            }
        
        else:
            # Gerar alerta
            alerta = {
                "autorizado": False,
                "alerta": True,
                "severidade": "ALTA",
                "tipo": "ACESSO_FORA_ZONA",
                "email": email,
                "mac_address": mac,
                "latitude": lat,
                "longitude": lon,
                "cidade": cidade,
                "ponto_esperado": verificacao["nome_ponto"],
                "distancia_metros": verificacao["distancia_metros"],
                "mensagem": f"ALERTA: {email} tentando acessar de "
                           f"{cidade} (fora da zona permitida!)",
                "proximos_pontos": self.verificador.obter_proximos_pontos(lat, lon),
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.warning(f"🚨 ALERTA: {alerta['mensagem']}")
            return alerta


# ============================================================================
# 📝 EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""
    📍 GEOFENCING - 3 PONTOS DE CONFIANÇA
    
    PONTOS:
    1. Valparaíso 2 (Casa) - Qualquer hora
    2. Gama (Trabalho) - 14h em diante
    3. SENAI (Manhã) - Até 13h
    
    Uso:
    verificador = VerificadorGeofencing()
    resultado = verificador.verificar_localizacao(lat, lon)
    
    Se fora dos pontos:
    - Retorna False
    - Alerta gerado
    - Bloqueia acesso
    """)
    
    # Teste
    verificador = VerificadorGeofencing()
    alertas = AlertasGeofencing()
    
    # Simular acesso em Valparaíso (autorizado)
    print("\n✅ Teste 1: Em Valparaíso 2")
    resultado = verificador.verificar_localizacao(-15.8268, -48.0409)
    print(f"Autorizado: {resultado['autorizado']}")
    
    # Simular acesso fora dos pontos (não autorizado)
    print("\n❌ Teste 2: Em São Paulo")
    resultado = verificador.verificar_localizacao(-23.5505, -46.6333)
    print(f"Autorizado: {resultado['autorizado']}")
    print(f"Motivo: {resultado['motivo']}")
