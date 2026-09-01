#!/usr/bin/env python3
"""
Agent Bridge - IA Concursos Elite v2.0
========================================

Script modelo para agentes autônomos (Crawl4AI, OpenHands, etc.)
consumirem dados de questões e injetar na API de ingestão.

Uso:
    python agent_bridge.py --concurso "Banco Central (Bacen)" --modo local
    python agent_bridge.py --concurso "Transpetro (Petrobras)" --modo scraper
    python agent_bridge.py --concurso "PMDF" --modo hybrid

Variáveis de Ambiente:
    API_ENDPOINT: URL da API (default: http://localhost:8000)
    API_KEY_INGESTAO: Chave de ingestão (default: elite-concursos-hunter-2024)
    BATCH_SIZE: Tamanho do lote para ingestão (default: 10)
"""

import os
import json
import requests
import logging
import argparse
from typing import List, Dict, Optional
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURAÇÃO DO CLIENTE API
# ============================================================

API_ENDPOINT = os.getenv("API_ENDPOINT", "http://localhost:8000")
API_KEY_INGESTAO = os.getenv("API_KEY_INGESTAO", "elite-concursos-hunter-2024")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))

class ClienteIngestao:
    """Cliente para ingestão de questões via API v1"""
    
    def __init__(self, endpoint: str = API_ENDPOINT, api_key: str = API_KEY_INGESTAO):
        self.endpoint = endpoint
        self.api_key = api_key
        self.sessao = requests.Session()
        self.sessao.headers.update({
            "Content-Type": "application/json",
            "X-API-KEY": api_key
        })
    
    def ingerir_questoes(self, questoes: List[Dict]) -> Dict:
        """
        Envia lote de questões para a API de ingestão
        
        Args:
            questoes: Lista de dicts contendo os dados das questões
            
        Returns:
            Response dict da API com status de ingestão
        """
        if not questoes:
            logger.warning("⚠️ Lista vazia de questões")
            return {"status": "vazio", "total_inserido": 0}
        
        url = f"{self.endpoint}/api/v1/ingest"
        payload = {"questoes": questoes}
        
        try:
            logger.info(f"📤 Enviando {len(questoes)} questões para {url}")
            
            response = self.sessao.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Ingestão bem-sucedida: {data.get('total_inserido')} questões inseridas")
                logger.info(f"📊 Total no banco: {data.get('total_no_banco')} questões")
                return data
            else:
                logger.error(f"❌ Erro HTTP {response.status_code}: {response.text}")
                return {"status": "erro", "codigo": response.status_code, "mensagem": response.text}
                
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ Timeout ao enviar questões (>30s)")
            return {"status": "timeout"}
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ Erro de conexão com a API: {e}")
            return {"status": "conexao_erro"}
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")
            return {"status": "erro_desconhecido", "mensagem": str(e)}
    
    def validar_questao(self, questao: Dict) -> bool:
        """Valida se a questão tem todos os campos obrigatórios"""
        campos_obrigatorios = [
            'concurso', 'materia', 'banca', 'enunciado',
            'alternativas', 'resposta_correta', 'explicacao', 'pegadinha_banca'
        ]
        
        for campo in campos_obrigatorios:
            if campo not in questao or not questao[campo]:
                logger.warning(f"⚠️ Campo obrigatório faltando: {campo}")
                return False
        
        # Validar alternativas (deve ser dict)
        if not isinstance(questao['alternativas'], dict):
            logger.warning("⚠️ Alternativas deve ser um dicionário (A, B, C, D, ...)")
            return False
        
        # Validar resposta_correta (deve estar nas alternativas)
        if questao['resposta_correta'] not in questao['alternativas']:
            logger.warning(f"⚠️ Resposta correta ({questao['resposta_correta']}) não está nas alternativas")
            return False
        
        return True

# ============================================================
# EXEMPLO: DADOS ESTÁTICOS PARA TESTE
# ============================================================

QUESTOES_EXEMPLO_BACEN = [
    {
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",
        "banca": "ESAF",
        "dificuldade": "Difícil",
        "tipo": "Múltipla Escolha",
        "enunciado": "A regência nominal em 'insistência em participar da reunião' está correta porque:",
        "alternativas": {
            "A": "O nome 'insistência' rege complemento nominal com preposição 'em'",
            "B": "O verbo 'insistir' é transitivo indireto",
            "C": "A preposição 'de' seria mais adequada",
            "D": "Não há complemento nominal nesta frase"
        },
        "resposta_correta": "A",
        "explicacao": "O nome 'insistência' (derivado do verbo insistir) rege complemento nominal com a preposição 'em'. A regência nominal segue as mesmas preposições do verbo de origem.",
        "pegadinha_banca": "ESAF costuma cobrar nomes derivados de verbos transitivos indiretos que mantêm a mesma preposição. Não confundir com nomes que mudam a preposição."
    },
    {
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",
        "banca": "ESAF",
        "dificuldade": "Médio",
        "tipo": "Múltipla Escolha",
        "enunciado": "Identifique a alternativa onde a concordância verbal está incorreta:",
        "alternativas": {
            "A": "Faz dez anos que não o vejo.",
            "B": "Havia muitos candidatos na sala.",
            "C": "A maioria dos alunos chegou atrasada.",
            "D": "Mais de um candidato se inscreveu."
        },
        "resposta_correta": "C",
        "explicacao": "Quando 'maioria' vem seguida de nome plural, o verbo pode concordar com 'maioria' (singular) ou com o nome plural. Aqui: 'A maioria chegou' (correto) ou 'A maioria chegaram' (também correto). A alternativa está correta grammaticalmente.",
        "pegadinha_banca": "ESAF tenta induzir o candidato a achar que 'maioria + plural' sempre exige verbo no plural. Na verdade, ambas as construções são corretas."
    }
]

QUESTOES_EXEMPLO_TRANSPETRO = [
    {
        "concurso": "Transpetro (Petrobras)",
        "materia": "Logística",
        "banca": "Cesgranrio",
        "dificuldade": "Médio",
        "tipo": "Múltipla Escolha",
        "enunciado": "Na cadeia de suprimentos, o termo 'Just-In-Time' refere-se a:",
        "alternativas": {
            "A": "Estoque máximo que a empresa pode manter",
            "B": "Entrega de materiais exatamente quando necessário, reduzindo estoques",
            "C": "Processo de logística reversa",
            "D": "Sistema de rastreamento de carga em tempo real"
        },
        "resposta_correta": "B",
        "explicacao": "Just-In-Time (JIT) é uma filosofia de gestão que minimiza estoques através da entrega sincronizada. Os materiais chegam exatamente quando são necessários à produção, reduzindo custos de armazenagem.",
        "pegadinha_banca": "Cesgranrio pode oferecer alternativas sobre rastreamento ou estoque que parecem plausíveis, mas JIT é especificamente sobre o timing de entrega."
    }
]

QUESTOES_EXEMPLO_PMDF = [
    {
        "concurso": "PMDF",
        "materia": "Direito Administrativo",
        "banca": "CEBRASPE",
        "dificuldade": "Difícil",
        "tipo": "Certo/Errado",
        "enunciado": "É correto afirmar que a discricionariedade administrativa é ilimitada e o agente público pode agir conforme sua conveniência pessoal.",
        "alternativas": {
            "Certo": "Sim, a discricionariedade é ilimitada",
            "Errado": "Não, a discricionariedade é vinculada pela lei"
        },
        "resposta_correta": "Errado",
        "explicacao": "A discricionariedade administrativa não é ilimitada. O agente público deve atuar dentro dos limites legais, ainda que tenha liberdade de escolha quanto ao modo de agir. A lei sempre vincula a atuação.",
        "pegadinha_banca": "CEBRASPE costuma testar se o candidato confunde 'discricionariedade' com 'arbitrariedade'. Discricionariedade é liberdade dentro dos limites da lei, não fora deles."
    }
]

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def carregar_questoes_json(caminho_arquivo: str) -> List[Dict]:
    """Carrega questões de um arquivo JSON local"""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        questoes = dados if isinstance(dados, list) else dados.get('questoes', [])
        logger.info(f"✅ Carregadas {len(questoes)} questões de {caminho_arquivo}")
        return questoes
    except Exception as e:
        logger.error(f"❌ Erro ao carregar arquivo: {e}")
        return []

def obter_questoes_exemplo(concurso: str) -> List[Dict]:
    """Retorna questões de exemplo por concurso"""
    mapa = {
        "Banco Central (Bacen)": QUESTOES_EXEMPLO_BACEN,
        "Transpetro (Petrobras)": QUESTOES_EXEMPLO_TRANSPETRO,
        "PMDF": QUESTOES_EXEMPLO_PMDF
    }
    return mapa.get(concurso, [])

def ingerir_em_lotes(cliente: ClienteIngestao, questoes: List[Dict], tamanho_lote: int = BATCH_SIZE):
    """Ingere questões em lotes para evitar timeouts"""
    total_inserido = 0
    
    for i in range(0, len(questoes), tamanho_lote):
        lote = questoes[i:i + tamanho_lote]
        
        # Validar questões do lote
        lote_valido = []
        for q in lote:
            if cliente.validar_questao(q):
                lote_valido.append(q)
            else:
                logger.warning(f"⚠️ Questão descartada por falta de validação")
        
        if not lote_valido:
            logger.warning(f"⚠️ Nenhuma questão válida no lote {i//tamanho_lote + 1}")
            continue
        
        # Ingerir lote
        resultado = cliente.ingerir_questoes(lote_valido)
        total_inserido += resultado.get('total_inserido', 0)
        
        logger.info(f"📊 Progresso: {i + len(lote)}/{len(questoes)} questões processadas")
    
    return total_inserido

# ============================================================
# MAIN E ARGUMENTOS CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Agent Bridge - Ingestão de questões na IA Concursos Elite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Ingerir questões de exemplo do Bacen
  python agent_bridge.py --concurso "Banco Central (Bacen)" --modo local
  
  # Ingerir de arquivo JSON
  python agent_bridge.py --arquivo questoes.json --tamanho-lote 20
  
  # Modo scraper (seria integrado com Crawl4AI/Selenium)
  python agent_bridge.py --concurso "Transpetro (Petrobras)" --modo scraper
        """
    )
    
    parser.add_argument('--concurso', type=str, default="Banco Central (Bacen)",
                        help='Concurso alvo: "Banco Central (Bacen)", "Transpetro (Petrobras)", "PMDF"')
    parser.add_argument('--modo', type=str, default='local', choices=['local', 'scraper', 'hybrid'],
                        help='Modo de operação')
    parser.add_argument('--arquivo', type=str, default=None,
                        help='Caminho para arquivo JSON com questões')
    parser.add_argument('--endpoint', type=str, default=API_ENDPOINT,
                        help='Endpoint da API')
    parser.add_argument('--api-key', type=str, default=API_KEY_INGESTAO,
                        help='Chave de API para ingestão')
    parser.add_argument('--tamanho-lote', type=int, default=BATCH_SIZE,
                        help='Tamanho dos lotes de ingestão')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("🏛️  AGENT BRIDGE - IA Concursos Elite v2.0")
    print("="*70)
    print(f"📍 Endpoint: {args.endpoint}")
    print(f"🏢 Concurso: {args.concurso}")
    print(f"⚙️  Modo: {args.modo}")
    print(f"📦 Tamanho do lote: {args.tamanho_lote}")
    print("="*70 + "\n")
    
    # Inicializar cliente
    cliente = ClienteIngestao(endpoint=args.endpoint, api_key=args.api_key)
    
    # Obter questões baseado no modo
    questoes = []
    
    if args.arquivo:
        logger.info(f"📂 Carregando questões de {args.arquivo}...")
        questoes = carregar_questoes_json(args.arquivo)
    elif args.modo == 'local':
        logger.info(f"📚 Usando questões de exemplo do {args.concurso}...")
        questoes = obter_questoes_exemplo(args.concurso)
    elif args.modo == 'scraper':
        logger.info(f"🕷️  Modo scraper: integração com Crawl4AI/OpenHands")
        logger.warning("⚠️  Modo scraper não implementado neste exemplo")
        logger.info("💡 Implemente a lógica de scraping aqui usando Crawl4AI ou similar")
        questoes = []
    elif args.modo == 'hybrid':
        logger.info(f"🔄 Modo hybrid: local + scraper")
        questoes = obter_questoes_exemplo(args.concurso)
    
    if not questoes:
        logger.error("❌ Nenhuma questão para ingerir")
        return False
    
    # Ingerir em lotes
    logger.info(f"🚀 Iniciando ingestão de {len(questoes)} questões...\n")
    total = ingerir_em_lotes(cliente, questoes, args.tamanho_lote)
    
    # Resumo final
    print("\n" + "="*70)
    print("✅ INGESTÃO CONCLUÍDA")
    print("="*70)
    print(f"📊 Total inserido: {total} questões")
    print(f"🏢 Concurso: {args.concurso}")
    print(f"⏱️  Timestamp: {datetime.now().isoformat()}")
    print("="*70 + "\n")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
