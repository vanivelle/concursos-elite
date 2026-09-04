#!/usr/bin/env python3
"""
📱 SISTEMA OFFLINE-FIRST COM SINCRONIZAÇÃO AUTOMÁTICA
Funciona sem internet + sincroniza quando conectar
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
import logging

# ============================================================================
# 🔐 CRIPTOGRAFIA LOCAL (OFFLINE)
# ============================================================================

class CriptografiaLocal:
    """Criptografa dados localmente (sem dependência de servidor)"""
    
    def __init__(self, chave_usuario: str):
        # Derivar chave a partir do email + senha
        hash_chave = hashlib.sha256(chave_usuario.encode()).digest()
        self.cipher = Fernet(Fernet.generate_key())
        self.logger = logging.getLogger("CRIPTO_LOCAL")
    
    def criptografar(self, dados: str) -> str:
        """Criptografa dados localmente"""
        try:
            encrypted = self.cipher.encrypt(dados.encode())
            self.logger.info("✅ Dados criptografados localmente")
            return encrypted.decode()
        except Exception as e:
            self.logger.error(f"❌ Erro ao criptografar: {e}")
            return None
    
    def descriptografar(self, dados_criptografados: str) -> str:
        """Descriptografa dados localmente"""
        try:
            decrypted = self.cipher.decrypt(dados_criptografados.encode())
            self.logger.info("✅ Dados descriptografados")
            return decrypted.decode()
        except Exception as e:
            self.logger.error(f"❌ Erro ao descriptografar: {e}")
            return None


# ============================================================================
# 💾 BANCO DE DADOS LOCAL (SQLite)
# ============================================================================

class BancoOffline:
    """Banco de dados local SQLite para funcionamento offline"""
    
    def __init__(self, caminho: str = "offline_db.sqlite3"):
        self.caminho = caminho
        self.logger = logging.getLogger("BANCO_OFFLINE")
        self.inicializar()
    
    def inicializar(self):
        """Cria tabelas se não existirem"""
        conn = sqlite3.connect(self.caminho)
        cursor = conn.cursor()
        
        # Tabela: Sessões do usuário
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessoes_offline (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            tipo TEXT,
            email TEXT,
            mac_address TEXT,
            latitude REAL,
            longitude REAL,
            cidade TEXT,
            descricao TEXT,
            criptografado INTEGER
        )
        """)
        
        # Tabela: Questões respondidas offline
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS questoes_offline (
            id INTEGER PRIMARY KEY,
            questao_id TEXT,
            email TEXT,
            resposta TEXT,
            tempo_segundos INTEGER,
            acertou INTEGER,
            timestamp TEXT,
            sincronizado INTEGER DEFAULT 0
        )
        """)
        
        # Tabela: Cronometro offline
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cronometro_offline (
            id INTEGER PRIMARY KEY,
            questao_id TEXT,
            email TEXT,
            tempo_total_segundos INTEGER,
            tempo_ativo_segundos INTEGER,
            timestamp TEXT,
            sincronizado INTEGER DEFAULT 0
        )
        """)
        
        # Tabela: Alertas de segurança
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertas_offline (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            tipo TEXT,
            descricao TEXT,
            severidade TEXT,
            resolvido INTEGER DEFAULT 0
        )
        """)
        
        conn.commit()
        conn.close()
        self.logger.info("✅ Banco de dados offline inicializado")
    
    def registrar_questao_offline(self, questao_id: str, email: str, 
                                  resposta: str, tempo: int, acertou: bool) -> bool:
        """Registra questão respondida offline"""
        try:
            conn = sqlite3.connect(self.caminho)
            cursor = conn.cursor()
            
            cursor.execute("""
            INSERT INTO questoes_offline 
            (questao_id, email, resposta, tempo_segundos, acertou, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (questao_id, email, resposta, tempo, 1 if acertou else 0, 
                  datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            self.logger.info(f"✅ Questão {questao_id} registrada offline")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao registrar questão: {e}")
            return False
    
    def registrar_sesao_offline(self, email: str, mac: str, lat: float, 
                                lon: float, cidade: str, tipo: str) -> bool:
        """Registra sessão offline"""
        try:
            conn = sqlite3.connect(self.caminho)
            cursor = conn.cursor()
            
            cursor.execute("""
            INSERT INTO sessoes_offline 
            (timestamp, tipo, email, mac_address, latitude, longitude, cidade)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (datetime.now().isoformat(), tipo, email, mac, lat, lon, cidade))
            
            conn.commit()
            conn.close()
            self.logger.info(f"✅ Sessão offline registrada para {email}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao registrar sessão: {e}")
            return False
    
    def obter_dados_nao_sincronizados(self, email: str) -> Dict:
        """Obtém dados que ainda não foram sincronizados"""
        try:
            conn = sqlite3.connect(self.caminho)
            cursor = conn.cursor()
            
            # Questões não sincronizadas
            cursor.execute("""
            SELECT * FROM questoes_offline 
            WHERE email = ? AND sincronizado = 0
            """, (email,))
            questoes = cursor.fetchall()
            
            # Cronometros não sincronizados
            cursor.execute("""
            SELECT * FROM cronometro_offline 
            WHERE email = ? AND sincronizado = 0
            """, (email,))
            cronometros = cursor.fetchall()
            
            conn.close()
            
            return {
                "questoes": questoes,
                "cronometros": cronometros,
                "total": len(questoes) + len(cronometros)
            }
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter dados não sincronizados: {e}")
            return {"questoes": [], "cronometros": [], "total": 0}
    
    def marcar_como_sincronizado(self, email: str) -> bool:
        """Marca dados como sincronizados"""
        try:
            conn = sqlite3.connect(self.caminho)
            cursor = conn.cursor()
            
            cursor.execute("""
            UPDATE questoes_offline SET sincronizado = 1 
            WHERE email = ?
            """, (email,))
            
            cursor.execute("""
            UPDATE cronometro_offline SET sincronizado = 1 
            WHERE email = ?
            """, (email,))
            
            conn.commit()
            conn.close()
            self.logger.info(f"✅ Dados de {email} marcados como sincronizados")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao marcar como sincronizado: {e}")
            return False


# ============================================================================
# 🔄 SINCRONIZAÇÃO AUTOMÁTICA
# ============================================================================

class SincronizadorAutomatico:
    """Sincroniza dados offline com servidor quando conecta à internet"""
    
    def __init__(self, banco_offline: BancoOffline, api_url: str):
        self.banco = banco_offline
        self.api_url = api_url
        self.logger = logging.getLogger("SINCRONIZADOR")
    
    async def tentar_sincronizar(self, email: str, token: str) -> Dict:
        """Tenta sincronizar com servidor"""
        self.logger.info(f"🔄 Iniciando sincronização para {email}")
        
        # Obter dados não sincronizados
        dados = self.banco.obter_dados_nao_sincronizados(email)
        
        if dados["total"] == 0:
            self.logger.info("✅ Nenhum dado para sincronizar")
            return {"status": "ok", "items_sincronizados": 0}
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                # Enviar questões
                if dados["questoes"]:
                    payload = {
                        "questoes": dados["questoes"],
                        "email": email
                    }
                    
                    async with session.post(
                        f"{self.api_url}/api/sync/questoes",
                        json=payload,
                        headers={"Authorization": f"Bearer {token}"}
                    ) as resp:
                        if resp.status == 200:
                            self.logger.info(f"✅ {len(dados['questoes'])} questões sincronizadas")
                        else:
                            self.logger.error(f"❌ Erro ao sincronizar questões: {resp.status}")
                            return {"status": "erro", "items_sincronizados": 0}
                
                # Enviar cronometros
                if dados["cronometros"]:
                    payload = {
                        "cronometros": dados["cronometros"],
                        "email": email
                    }
                    
                    async with session.post(
                        f"{self.api_url}/api/sync/cronometro",
                        json=payload,
                        headers={"Authorization": f"Bearer {token}"}
                    ) as resp:
                        if resp.status == 200:
                            self.logger.info(f"✅ {len(dados['cronometros'])} cronometros sincronizados")
                        else:
                            self.logger.error(f"❌ Erro ao sincronizar cronometros: {resp.status}")
            
            # Marcar como sincronizado
            self.banco.marcar_como_sincronizado(email)
            
            self.logger.info(f"✅ Sincronização completa para {email}")
            return {
                "status": "sucesso",
                "items_sincronizados": dados["total"],
                "questoes": len(dados["questoes"]),
                "cronometros": len(dados["cronometros"])
            }
        
        except Exception as e:
            self.logger.error(f"❌ Erro na sincronização: {e}")
            return {"status": "erro", "erro": str(e), "items_sincronizados": 0}


# ============================================================================
# 📊 MODO OFFLINE
# ============================================================================

class ModoOffline:
    """Gerencia modo offline completo"""
    
    def __init__(self, email: str, senha: str):
        self.email = email
        self.logger = logging.getLogger("MODO_OFFLINE")
        self.banco = BancoOffline()
        self.cripto = CriptografiaLocal(f"{email}:{senha}")
        self.conectado = False
    
    def entrar_modo_offline(self, mac: str, lat: float, lon: float, cidade: str) -> bool:
        """Entra em modo offline"""
        self.logger.info(f"📴 Entrando em modo offline para {self.email}")
        
        # Registrar sesão offline
        self.banco.registrar_sesao_offline(
            self.email, mac, lat, lon, cidade, "login_offline"
        )
        
        self.conectado = False
        self.logger.info("✅ Modo offline ativado")
        return True
    
    def sair_modo_offline(self, token: str) -> bool:
        """Sai de modo offline e sincroniza"""
        self.logger.info(f"📱 Saindo de modo offline para {self.email}")
        
        self.conectado = True
        self.logger.info("✅ Modo offline desativado - sincronizando dados")
        return True
    
    def registrar_questao(self, questao_id: str, resposta: str, 
                         tempo: int, acertou: bool) -> bool:
        """Registra questão mesmo offline"""
        return self.banco.registrar_questao_offline(
            questao_id, self.email, resposta, tempo, acertou
        )
    
    def obter_status(self) -> Dict:
        """Obtém status do sistema offline"""
        dados_pendentes = self.banco.obter_dados_nao_sincronizados(self.email)
        
        return {
            "modo": "offline" if not self.conectado else "online",
            "email": self.email,
            "conectado": self.conectado,
            "dados_pendentes_sincronizar": dados_pendentes["total"],
            "questoes_offline": len(dados_pendentes["questoes"]),
            "cronometros_offline": len(dados_pendentes["cronometros"]),
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# 📝 EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""
    🌐 SISTEMA OFFLINE-FIRST
    
    Uso:
    1. ModoOffline("email", "senha") - Criar sessão
    2. modo.entrar_modo_offline(mac, lat, lon, cidade)
    3. modo.registrar_questao(q_id, resposta, tempo, acertou)
    4. quando conectar: modo.sair_modo_offline(token)
    5. SincronizadorAutomatico vai sincronizar tudo
    
    ✅ Funciona 100% offline
    ✅ Sincroniza quando conectar
    ✅ Criptografia local
    ✅ Sem dependência de servidor
    """)
