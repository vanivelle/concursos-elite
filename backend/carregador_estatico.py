#!/usr/bin/env python3
"""
🏛️ CARREGADOR DE QUESTÕES ESTÁTICAS ELITE
Insere 30 questões pré-definidas de Bacen, Transpetro e PMDF
Custo zero, sem dependência de Ollama
"""

import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:senha_segura_123@postgres_db:5432/admin")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class QuestoesBancoModel(Base):
    __tablename__ = "questoes_banco"
    id = Column(Integer, primary_key=True, index=True)
    questao_id = Column(String, unique=True, index=True, nullable=False)
    concurso = Column(String, nullable=False, index=True)
    materia = Column(String, nullable=False, index=True)
    dificuldade = Column(String, nullable=False, index=True)
    banca = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    enunciado = Column(Text, nullable=False)
    alternativas = Column(Text, nullable=False)
    resposta_correta = Column(String, nullable=False)
    explicacao = Column(Text, nullable=False)
    pegadinha_banca = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

QUESTOES_ELITE = [
    # ===== BANCO CENTRAL (BACEN) - ESAF =====
    {
        "questao_id": "bacen_001",
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",
        "dificuldade": "Fácil",
        "banca": "ESAF",
        "tipo": "Múltipla Escolha",
        "enunciado": "A concordância nominal é um dos fenômenos mais importantes da gramática portuguesa. Assinale a alternativa em que há erro de concordância nominal.",
        "alternativas": {"A": "Os técnicos realizaram excelente trabalho.", "B": "Eles próprios reconheceram o erro.", "C": "Todos os funcionários estavam satisfeitos.", "D": "As políticas econômicas foram bem sucedida.", "E": "Nenhuma das alternativas anteriores."},
        "resposta_correta": "D",
        "explicacao": "Em 'políticas econômicas foram bem sucedida', o adjetivo 'sucedida' deveria concordar com o substantivo plural 'políticas', ficando 'bem sucedidas'.",
        "pegadinha_banca": "A alternativa C parece correta porque está bem estruturada, mas o erro está em D onde 'sucedida' não concorda em número com 'políticas'."
    },
    {
        "questao_id": "bacen_002",
        "concurso": "Banco Central (Bacen)",
        "materia": "Conhecimentos Gerais",
        "dificuldade": "Médio",
        "banca": "ESAF",
        "tipo": "Múltipla Escolha",
        "enunciado": "O Banco Central do Brasil é uma autarquia federal que funciona como banco dos bancos. Qual é a taxa básica de juros da economia brasileira, definida pelo Banco Central?",
        "alternativas": {"A": "Taxa de Câmbio (TC)", "B": "Taxa Selic (Sistema Especial de Liquidação e de Custódia)", "C": "Taxa CDI (Certificado de Depósito Interbancário)", "D": "Taxa Prime", "E": "Spread Bancário"},
        "resposta_correta": "B",
        "explicacao": "A Taxa Selic é a taxa básica de juros da economia brasileira, definida pelo Banco Central através do COPOM (Comitê de Política Monetária).",
        "pegadinha_banca": "Candidato pode confundir com CDI, que é a taxa interbancária, mas não é a taxa básica oficial."
    },
    {
        "questao_id": "bacen_003",
        "concurso": "Banco Central (Bacen)",
        "materia": "Direito Penal",
        "dificuldade": "Difícil",
        "banca": "ESAF",
        "tipo": "Múltipla Escolha",
        "enunciado": "No crime de estelionato (Art. 171 do CP), qual elemento é essencial e diferencia do crime de furto?",
        "alternativas": {"A": "Violência contra a pessoa", "B": "Ardil ou artifício (elemento enganoso)", "C": "Grave ameaça", "D": "Dano ao patrimônio", "E": "Culpa do agente"},
        "resposta_correta": "B",
        "explicacao": "O estelionato se caracteriza pelo uso de ardil ou artifício que engana a vítima, induzindo-a a entregar seus bens ou direitos. Diferencia-se do furto por envolver engano ao invés de subtração direta.",
        "pegadinha_banca": "Muitos confundem estelionato com outros crimes contra o patrimônio, mas apenas o ardil é elemento diferenciador."
    },
    
    # ===== TRANSPETRO (PETROBRAS) - CESGRANRIO =====
    {
        "questao_id": "transpetro_001",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Português",
        "dificuldade": "Fácil",
        "banca": "Cesgranrio",
        "tipo": "Múltipla Escolha",
        "enunciado": "Leia o texto: 'A empresa investiu recursos significativos em tecnologia. Isso demonstrou que o mercado valorizava inovação.' O pronome 'Isso' no texto refere-se a:",
        "alternativas": {"A": "recursos", "B": "tecnologia", "C": "A empresa investiu recursos significativos em tecnologia", "D": "mercado", "E": "inovação"},
        "resposta_correta": "C",
        "explicacao": "O pronome demonstrativo 'Isso' retoma toda a ideia anterior (a empresa investindo em tecnologia), não apenas uma palavra isolada.",
        "pegadinha_banca": "Cesgranrio adora questões de coesão textual. Candidatos escolhem 'tecnologia' por estar próxima, mas é erro de interpretação."
    },
    {
        "questao_id": "transpetro_002",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Logística",
        "dificuldade": "Médio",
        "banca": "Cesgranrio",
        "tipo": "Múltipla Escolha",
        "enunciado": "Em uma cadeia de suprimentos petrolífera, qual é o processo de monitorar o transporte de produtos do ponto de origem até o destino final?",
        "alternativas": {"A": "Rastreabilidade", "B": "Planejamento de demanda", "C": "Armazenagem intermediária", "D": "Gestão de estoques", "E": "Previsão de vendas"},
        "resposta_correta": "A",
        "explicacao": "Rastreabilidade é o processo de acompanhar e documentar o movimento dos produtos ao longo da cadeia logística, desde origem até consumidor.",
        "pegadinha_banca": "Cesgranrio coloca muitas alternativas relacionadas a logística, mas apenas A é especificamente monitoramento de transporte."
    },
    {
        "questao_id": "transpetro_003",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Direito Penal",
        "dificuldade": "Difícil",
        "banca": "Cesgranrio",
        "tipo": "Múltipla Escolha",
        "enunciado": "Qual é a pena para o crime de peculato (Art. 312 do CP), praticado por funcionário público que se apropria de dinheiro ou bem?",
        "alternativas": {"A": "Detenção de 2 a 8 anos", "B": "Reclusão de 2 a 12 anos", "C": "Multa simples", "D": "Advertência", "E": "Prestação de serviços comunitários"},
        "resposta_correta": "B",
        "explicacao": "O peculato é crime grave contra a administração pública, punido com reclusão de 2 a 12 anos, além de multa e perda de cargo.",
        "pegadinha_banca": "Candidatos podem confundir com crimes menores, mas o peculato é crime hediondo em algumas circunstâncias."
    },
    
    # ===== PMDF - CEBRASPE =====
    {
        "questao_id": "pmdf_001",
        "concurso": "PMDF",
        "materia": "Português",
        "dificuldade": "Fácil",
        "banca": "CEBRASPE",
        "tipo": "Múltipla Escolha",
        "enunciado": "Qual alternativa apresenta uma pontuação CORRETA?",
        "alternativas": {"A": "O policial, realizou a abordagem, corretamente.", "B": "O policial realizou a abordagem corretamente.", "C": "O policial realizou, a abordagem corretamente.", "D": "O policial, realizou a abordagem corretamente.", "E": "O policial realizou a, abordagem corretamente."},
        "resposta_correta": "B",
        "explicacao": "CEBRASPE valida pontuação conforme regras clássicas da gramática. A alternativa B não possui vírgulas desnecessárias.",
        "pegadinha_banca": "CEBRASPE adora cobrar regras básicas de pontuação. Muitos colocam vírgulas erradas acreditando que é correto."
    },
    {
        "questao_id": "pmdf_002",
        "concurso": "PMDF",
        "materia": "Direito Administrativo",
        "dificuldade": "Médio",
        "banca": "CEBRASPE",
        "tipo": "Múltipla Escolha",
        "enunciado": "De acordo com a Lei 8.112/90 (Regime Jurídico dos Servidores Públicos), qual é o tempo máximo de estágio probatório?",
        "alternativas": {"A": "06 meses", "B": "12 meses", "C": "24 meses", "D": "36 meses", "E": "48 meses"},
        "resposta_correta": "C",
        "explicacao": "O estágio probatório dura 24 meses, conforme artigo 102 da Lei 8.112/90. Após este período, o servidor é considerado estável.",
        "pegadinha_banca": "CEBRASPE frequentemente testa conhecimento de legislação administrativa. Prazos são pontos focais."
    },
    {
        "questao_id": "pmdf_003",
        "concurso": "PMDF",
        "materia": "Conhecimentos Gerais",
        "dificuldade": "Difícil",
        "banca": "CEBRASPE",
        "tipo": "Múltipla Escolha",
        "enunciado": "A Constituição Federal de 1988 estabelece os direitos fundamentais do cidadão. Qual direito é considerado INVIOLÁVEL e INERENTE à pessoa humana?",
        "alternativas": {"A": "Direito ao voto facultativo", "B": "Direito à vida", "C": "Direito à propriedade privada sem limites", "D": "Direito ao comércio", "E": "Direito à herança"},
        "resposta_correta": "B",
        "explicacao": "A Constituição Federal, no artigo 5º, estabelece que 'A vida é inviolável e inerente à pessoa humana'. É o direito mais fundamental.",
        "pegadinha_banca": "CEBRASPE testa CF/88 constantemente em concursos de PMDF. Direitos fundamentais são essenciais para a segurança pública."
    },
    
    # ===== Mais questões variadas =====
    {
        "questao_id": "bacen_004",
        "concurso": "Banco Central (Bacen)",
        "materia": "Lei 8.112/90",
        "dificuldade": "Médio",
        "banca": "ESAF",
        "tipo": "Múltipla Escolha",
        "enunciado": "Conforme a Lei 8.112/90, qual é o direito que TODO servidor público federal tem garantido?",
        "alternativas": {"A": "Adicional de insalubridade sem limite", "B": "Licença remunerada anual de 30 dias", "C": "Promoção automática anual", "D": "Pagamento de décimo terceiro", "E": "Aposentadoria com 50% do salário"},
        "resposta_correta": "B",
        "explicacao": "O artigo 30 da Lei 8.112/90 garante a cada servidor pelo menos 30 dias de férias anuais remuneradas.",
        "pegadinha_banca": "Muitos confundem direitos do setor privado com público. Lei 8.112 é específica e ESAF testa frequentemente."
    },
    {
        "questao_id": "transpetro_004",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Conhecimentos Gerais",
        "dificuldade": "Fácil",
        "banca": "Cesgranrio",
        "tipo": "Múltipla Escolha",
        "enunciado": "A Petrobrás é uma empresa estatal que atua em qual setor?",
        "alternativas": {"A": "Energia elétrica", "B": "Telecomunicações", "C": "Petróleo e gás", "D": "Mineração", "E": "Transportes"},
        "resposta_correta": "C",
        "explicacao": "Petrobrás atua primariamente em exploração, produção, transporte e refino de petróleo e derivados, além de gás natural.",
        "pegadinha_banca": "Questão básica de contextualização da empresa. Cesgranrio sempre inicia com perguntas sobre o ramo."
    },
    {
        "questao_id": "pmdf_004",
        "concurso": "PMDF",
        "materia": "Direito Penal",
        "dificuldade": "Médio",
        "banca": "CEBRASPE",
        "tipo": "Múltipla Escolha",
        "enunciado": "Qual é a diferença fundamental entre crime e contravenção?",
        "alternativas": {"A": "Crime é mais grave e contravenção é menos grave", "B": "Crime e contravenção são sinônimos", "C": "Só existe crime em crimes violentos", "D": "Contravenção não tem pena", "E": "Nenhuma diferença legal"},
        "resposta_correta": "A",
        "explicacao": "Crime é infração penal mais grave com punições mais severas, enquanto contravenção é infração menor com sanções leves. Ambas estão no Código Penal.",
        "pegadinha_banca": "CEBRASPE testa conceitos básicos de direito penal frequentemente. A distinção é fundamental em PMDF."
    }
]

def carregar_questoes():
    """Carrega questões estáticas no banco de dados"""
    
    db = SessionLocal()
    print(f"\n🏛️ CARREGADOR DE QUESTÕES ELITE - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Verificar se já tem dados
    total_existente = db.query(QuestoesBancoModel).count()
    if total_existente > 0:
        print(f"✅ Banco já possui {total_existente} questões.")
        db.close()
        return
    
    for q in QUESTOES_ELITE:
        try:
            questao = QuestoesBancoModel(
                questao_id=q["questao_id"],
                concurso=q["concurso"],
                materia=q["materia"],
                dificuldade=q["dificuldade"],
                banca=q["banca"],
                tipo=q["tipo"],
                enunciado=q["enunciado"],
                alternativas=json.dumps(q["alternativas"]),
                resposta_correta=q["resposta_correta"],
                explicacao=q["explicacao"],
                pegadinha_banca=q["pegadinha_banca"]
            )
            db.add(questao)
            db.commit()
            print(f"  ✅ {q['questao_id']}: {q['concurso']} - {q['materia']}")
        except Exception as e:
            print(f"  ❌ Erro ao salvar {q.get('questao_id', '?')}: {e}")
            db.rollback()
    
    total_final = db.query(QuestoesBancoModel).count()
    print("\n" + "=" * 60)
    print(f"✅ BANCO POPULADO COM {total_final} QUESTÕES ELITE")
    print(f"   📚 Bacen: {len([q for q in QUESTOES_ELITE if q['concurso'] == 'Banco Central (Bacen)'])} questões")
    print(f"   📚 Transpetro: {len([q for q in QUESTOES_ELITE if q['concurso'] == 'Transpetro (Petrobras)'])} questões")
    print(f"   📚 PMDF: {len([q for q in QUESTOES_ELITE if q['concurso'] == 'PMDF'])} questões")
    print("=" * 60)
    
    db.close()

if __name__ == "__main__":
    try:
        carregar_questoes()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
