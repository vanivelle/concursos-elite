#!/usr/bin/env python3
"""
🤖 PROTOCOLO DE INGESTÃO AUTOMÁTICA PARA OPENHANDS
Operação: Aquecimento de Banco de Dados com Crawl4AI + Ollama

Missão: Extrair 300 questões reais (Bacen/Transpetro/PMDF) e injetar via API
Performance Target: 300 questões em <3 minutos
"""

import requests
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any

# ============================================================
# CONFIGURAÇÃO
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# URLs e Credenciais
API_BASE = "http://localhost:8000"
API_INGEST = f"{API_BASE}/api/v1/ingest"
API_KEY = "elite-concursos-hunter-2024"
OLLAMA_API = "http://localhost:11434"

# Alvos de Ingestão
ALVOS_INGESTAO = {
    "Banco Central (Bacen)": {
        "total": 100,
        "banca": "ESAF",
        "materias": ["Direito Administrativo", "Português", "Conhecimentos Gerais"],
        "dificuldades": ["Fácil", "Médio", "Difícil"]
    },
    "Transpetro (Petrobras)": {
        "total": 100,
        "banca": "Cesgranrio",
        "materias": ["Português", "Logística", "Conhecimentos Gerais"],
        "dificuldades": ["Fácil", "Médio", "Difícil"]
    },
    "PMDF": {
        "total": 100,
        "banca": "Cebraspe",
        "materias": ["Direito Penal", "Direito Administrativo", "Português"],
        "dificuldades": ["Fácil", "Médio", "Difícil"]
    }
}

# ============================================================
# GENERATOR DE QUESTÕES SINTÉTICAS (Mockup para demo)
# Substitua com Crawl4AI real em produção
# ============================================================

def gerar_questoes_mockup(concurso: str, total: int) -> List[Dict[str, Any]]:
    """
    Gera questões sintéticas como placeholder.
    EM PRODUÇÃO: Usar Crawl4AI para extrair dados reais de portais públicos.
    """
    questoes = []
    config = ALVOS_INGESTAO[concurso]
    
    for i in range(1, total + 1):
        materia = config["materias"][i % len(config["materias"])]
        dificuldade = config["dificuldades"][i % len(config["dificuldades"])]
        
        questao = {
            "concurso": concurso,
            "materia": materia,
            "banca": config["banca"],
            "dificuldade": dificuldade,
            "tipo": "Múltipla Escolha",
            "enunciado": f"Questão {i} de {concurso}: Qual é o conceito correto relacionado a {materia}?",
            "alternativas": {
                "A": "Alternativa incorreta genérica",
                "B": "Outra alternativa incorreta",
                "C": "Resposta correta e bem fundamentada",
                "D": "Distrator plausível"
            },
            "resposta_correta": "C",
            "explicacao": f"A resposta C é correta porque representa o conceito fundamental de {materia}.",
            "diagnostico_erro": f"As alternativas A e B representam erros comuns: confundem conceitos similares que a banca {config['banca']} usa para testar atenção.",
            "nucleo_acerto": f"A regra seca: {materia} em {concurso} por {config['banca']} sempre testa conhecimento técnico preciso.",
            "pegadinha_banca": f"Armadilha {config['banca']}: usar sinônimos próximos para confundir candidatos desatentos.",
            "padroes_banca": {
                config["banca"]: f"Padrão de pegadinha: {config['banca']} coloca alternativas com vocabulário técnico similar ao correto."
            }
        }
        questoes.append(questao)
    
    return questoes

# ============================================================
# INGESTÃO EM LOTE
# ============================================================

def ingerir_questoes_lote(questoes: List[Dict], concurso: str) -> bool:
    """
    Envia questões para a API local via bulk insert.
    Retorna True se sucesso, False se falha.
    """
    payload = {"questoes": questoes}
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        logger.info(f"📤 Enviando {len(questoes)} questões de {concurso}...")
        response = requests.post(
            API_INGEST,
            json=payload,
            headers=headers,
            timeout=60
        )
        
        if response.status_code == 200:
            resultado = response.json()
            logger.info(f"✅ INGESTÃO SUCESSO: {resultado.get('total_inserido', 0)}/{len(questoes)} inseridas")
            logger.info(f"   Total no banco: {resultado.get('total_no_banco', 0)}")
            return resultado.get('total_inserido', 0) > 0
        else:
            logger.error(f"❌ API retornou {response.status_code}: {response.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        logger.error(f"❌ Erro de conexão: API não responde em {API_INGEST}")
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao ingerir: {str(e)}")
        return False

# ============================================================
# ENRIQUECIMENTO COM OLLAMA (Diagnóstico + Núcleo)
# ============================================================

def enriquecer_questao_com_ia(questao: Dict) -> Dict:
    """
    Usa Ollama (Gemma 2) para gerar automaticamente:
    - diagnostico_erro: análise detalhada dos distratores
    - nucleo_acerto: regra seca da resposta correta
    """
    if questao.get("diagnostico_erro") and questao.get("nucleo_acerto"):
        return questao  # Já enriquecida
    
    prompt = f"""Analise esta questão de concurso e forneça APENAS um JSON com dois campos:
Questão: {questao['enunciado']}
Alternativas: {json.dumps(questao['alternativas'])}
Resposta Correta: {questao['resposta_correta']}

Formato JSON (sem explicação):
{{
  "diagnostico_erro": "Explique por que as alternativas ERRADAS estão erradas. Seja específico sobre os erros de conceito.",
  "nucleo_acerto": "A regra seca do porquê a resposta correta está certa. Uma linha apenas."
}}"""
    
    try:
        response = requests.post(
            f"{OLLAMA_API}/api/generate",
            json={"model": "gemma2:2b", "prompt": prompt, "stream": False},
            timeout=15
        )
        
        if response.status_code == 200:
            resultado = response.json().get("response", "")
            # Tentar extrair JSON
            import re
            json_match = re.search(r'\{[^}]+\}', resultado, re.DOTALL)
            if json_match:
                dados = json.loads(json_match.group())
                questao["diagnostico_erro"] = dados.get("diagnostico_erro", questao.get("diagnostico_erro", ""))
                questao["nucleo_acerto"] = dados.get("nucleo_acerto", questao.get("nucleo_acerto", ""))
                logger.debug(f"✨ Questão enriquecida por IA")
    except:
        logger.debug(f"⚠️ Ollama indisponível, usando fallback")
    
    return questao

# ============================================================
# ORQUESTRAÇÃO PRINCIPAL
# ============================================================

def executar_operacao_aquecimento():
    """
    Orquestra a ingestão em massa de todas as 300 questões.
    """
    logger.info("="*80)
    logger.info("🔥 OPERAÇÃO DE AQUECIMENTO: Ingestão em Massa")
    logger.info("="*80)
    
    inicio = time.time()
    total_inseridos = 0
    
    for concurso, config in ALVOS_INGESTAO.items():
        logger.info(f"\n🎯 Alvo: {concurso} ({config['total']} questões)")
        
        # Gerar questões (em produção: Crawl4AI aqui)
        questoes = gerar_questoes_mockup(concurso, config["total"])
        logger.info(f"   ✅ {len(questoes)} questões geradas")
        
        # Enriquecer com IA (opcional, descomenta para ativar)
        # questoes = [enriquecer_questao_com_ia(q) for q in questoes]
        
        # Ingerir em lote
        sucesso = ingerir_questoes_lote(questoes, concurso)
        if sucesso:
            total_inseridos += config["total"]
        
        time.sleep(2)  # Respeitar rate limit
    
    duracao = time.time() - inicio
    logger.info(f"\n{'='*80}")
    logger.info(f"✅ OPERAÇÃO CONCLUÍDA")
    logger.info(f"   Total inserido: {total_inseridos} questões")
    logger.info(f"   Duração: {duracao:.1f}s")
    logger.info(f"   Velocidade: {total_inseridos/duracao:.0f} Q/s")
    logger.info(f"{'='*80}\n")
    
    return total_inseridos > 0

# ============================================================
# VERIFICAÇÃO PÓS-INGESTÃO
# ============================================================

def verificar_banco():
    """
    Consulta o status final do banco de dados.
    """
    try:
        response = requests.get(f"{API_BASE}/info")
        if response.status_code == 200:
            dados = response.json()
            total_questoes = dados.get("estadisticas", {}).get("questoes_banco", 0)
            logger.info(f"\n📊 STATUS DO BANCO:")
            logger.info(f"   Total de questões: {total_questoes}")
            logger.info(f"   Pronto para operação: {'✅ SIM' if total_questoes >= 300 else '❌ NÃO'}")
    except:
        logger.warning("Não foi possível verificar o banco")

# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    try:
        # Executar operação
        sucesso = executar_operacao_aquecimento()
        
        # Verificar resultado
        time.sleep(2)
        verificar_banco()
        
        # Exit code
        exit(0 if sucesso else 1)
    
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Operação interrompida pelo usuário")
        exit(2)
    except Exception as e:
        logger.error(f"\n❌ Erro fatal: {str(e)}")
        exit(1)
