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
# 🗺️ CONFIGURAÇÃO DE PONTOS CONFIÁVEIS GLOBAIS
# ============================================================================

PONTOS_CONFIANCIA_GLOBAIS = {
    "valparaiso_2": {
        "nome": "Valparaíso 2, Céu Azul",
        "latitude": -15.8268,
        "longitude": -48.0409,
        "raio_metros": 500,
        "horario_inicio": "00:00",
        "horario_fim": "23:59",
        "dias": ["seg", "ter", "qua", "qui", "sex", "sab", "dom"],
        "descricao": "Casa - Qualquer hora"
    },
    
    "gama": {
        "nome": "GAMA",
        "latitude": -15.8500,
        "longitude": -48.0600,
        "raio_metros": 1000,
        "horario_inicio": "06:00",
        "horario_fim": "23:59",
        "dias": ["seg", "ter", "qua", "qui", "sex", "sab", "dom"],
        "descricao": "Trabalho - Gama (Motoboy Matheus)"
    },
    
    "plano_piloto": {
        "nome": "Plano Piloto",
        "latitude": -15.7975,
        "longitude": -47.8822,
        "raio_metros": 2000,
        "horario_inicio": "08:00",
        "horario_fim": "18:00",
        "dias": ["seg", "ter", "qua", "qui", "sex"],
        "descricao": "Trabalho - Plano Piloto (Cabo do MD)"
    },
    
    "senai": {
        "nome": "SENAI",
        "latitude": -15.7975,
        "longitude": -48.0494,
        "raio_metros": 500,
        "horario_inicio": "08:00",
        "horario_fim": "13:00",
        "dias": ["seg", "ter", "qua", "qui", "sex"],
        "descricao": "SENAI - Manhã (até 13h)"
    }
}

# ============================================================================
# 👤 CONFIGURAÇÃO POR USUÁRIO (Pontos Permitidos)
# ============================================================================

PONTOS_POR_USUARIO = {
    "mr.dblucas@gmail.com": {
        "nome": "Admin",
        "pontos_permitidos": ["valparaiso_2"],
        "descricao": "Admin - Apenas casa"
    },
    
    "cabo.md@email.com": {
        "nome": "Cabo Do MD",
        "pontos_permitidos": ["valparaiso_2", "plano_piloto"],
        "descricao": "Cabo - Casa + Trabalho (Plano Piloto)"
    },
    
    "matheus@email.com": {
        "nome": "Motoboy Matheus",
        "pontos_permitidos": ["gama"],
        "descricao": "Motoboy - Trabalho (Gama)"
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
    
    def verificar_localizacao(self, lat: float, lon: float, email: str = None) -> Dict:
        """
        Verifica se localização está em ponto confiável
        Se email fornecido, verifica apenas os pontos permitidos para esse usuário
        Retorna: {autorizado, ponto, distancia, motivo}
        """
        agora = datetime.now()
        resultados = []
        
        # Se email fornecido, pegar apenas pontos daquele usuário
        if email and email in PONTOS_POR_USUARIO:
            pontos_permitidos = PONTOS_POR_USUARIO[email]["pontos_permitidos"]
            pontos_verificar = {k: v for k, v in PONTOS_CONFIANCIA_GLOBAIS.items() 
                               if k in pontos_permitidos}
        else:
            pontos_verificar = PONTOS_CONFIANCIA_GLOBAIS
        
        for chave, ponto in pontos_verificar.items():
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
        if not pontos_verificar:
            return {
                "autorizado": False,
                "motivo": "Nenhum ponto de confiança configurado para este usuário"
            }
        
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
    
    def obter_proximos_pontos(self, lat: float, lon: float, email: str = None) -> list:
        """Retorna pontos confiáveis ordenados por distância"""
        resultados = []
        
        # Se email fornecido, pegar apenas pontos daquele usuário
        if email and email in PONTOS_POR_USUARIO:
            pontos_permitidos = PONTOS_POR_USUARIO[email]["pontos_permitidos"]
            pontos_verificar = {k: v for k, v in PONTOS_CONFIANCIA_GLOBAIS.items() 
                               if k in pontos_permitidos}
        else:
            pontos_verificar = PONTOS_CONFIANCIA_GLOBAIS
        
        for chave, ponto in pontos_verificar.items():
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
        verificacao = self.verificador.verificar_localizacao(lat, lon, email)
        
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
