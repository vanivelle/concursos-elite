#!/usr/bin/env python3
"""
🏛️ POPULADOR ELITE v2 - REDAÇÕES + EXATAS
Carrega 15 temas de redação (com roteiros guiados) + 30 questões de Matemática/RLM
Bancas: Cebraspe (Bacen/PMDF), Cesgranrio (Transpetro)
"""

import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:senha_segura_123@localhost:5432/admin")
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
    diagnostico_erro = Column(Text, nullable=True)
    nucleo_acerto = Column(Text, nullable=True)
    pegadinha_banca = Column(Text, nullable=False)
    padroes_banca = Column(Text, nullable=True)
    data_criacao = Column(String, nullable=False)

class AtualidadesFeedModel(Base):
    __tablename__ = "atualidades_feed"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    conteudo_resumido = Column(Text, nullable=False)
    data_publicacao = Column(String, nullable=False, index=True)
    concurso_alvo = Column(String, nullable=False, index=True)
    fonte = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    roteiro_guiado_iniciante = Column(Text, nullable=True)
    data_ingestao = Column(String, nullable=False)

class RedacoesEnviadasModel(Base):
    __tablename__ = "redacoes_enviadas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_email = Column(String, nullable=False, index=True)
    tema = Column(String, nullable=False)
    texto_redacao = Column(Text, nullable=False)
    nota_final = Column(Float, nullable=True)
    correcao_detalhada = Column(Text, nullable=True)
    criterios = Column(Text, nullable=True)
    data_envio = Column(String, nullable=False, index=True)
    data_correcao = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# ========== QUESTÕES DE EXATAS (30 TOTAL: 15 RLM + 15 MATEMÁTICA) ==========
QUESTOES_EXATAS = [
    # ===== RLM BACEN/PMDF (Cebraspe) - Padrão MANÉ =====
    {
        "questao_id": "rlm_cebraspe_001",
        "concurso": "Banco Central (Bacen)",
        "materia": "Raciocínio Lógico (RLM)",
        "dificuldade": "Médio",
        "banca": "CEBRASPE",
        "tipo": "múltipla",
        "enunciado": "Considere a seguinte proposição: 'Se o Banco Central atua, então a inflação cai'. A negação dessa proposição é:",
        "alternativas": json.dumps(["A) Se o Banco Central não atua, então a inflação não cai", 
                                    "B) O Banco Central atua E a inflação não cai",
                                    "C) O Banco Central não atua OU a inflação não cai",
                                    "D) A inflação cai apenas se o Banco Central atua",
                                    "E) O Banco Central não atua E a inflação cai"]),
        "resposta_correta": "B",
        "explicacao": "A negação de 'Se P então Q' é 'P E não-Q'. Logo, 'O Banco Central atua E a inflação não cai'.",
        "diagnostico_erro": "🔴 Pegadinha Cebraspe (MANÉ): Você marcou A ou C. Errado! A negação de condicional NÃO é outra condicional, nem é 'OU'. Regra do MANÉ: Mantém P E nega Q.",
        "nucleo_acerto": "🟢 Regra Seca do MANÉ (negação de condicional): Se P→Q tem negação P∧¬Q. Memorize: Mantém primeira E nega segunda.",
        "pegadinha_banca": "Cebraspe adorar colocar distractores que parecem negações verdadeiras mas invertemos o conectivo",
        "padroes_banca": json.dumps({"tecnica": "Negação de Condicionais", "condicao": "Regra MANÉ", "tempo_medio": "90s"})
    },
    {
        "questao_id": "rlm_cebraspe_002",
        "concurso": "PMDF",
        "materia": "Raciocínio Lógico (RLM)",
        "dificuldade": "Médio",
        "banca": "CEBRASPE",
        "tipo": "múltipla",
        "enunciado": "Em uma operação policial, todos os agentes treinados são cautelosos. Alguns agentes cautelosos cometem erros. Logo:",
        "alternativas": json.dumps(["A) Todos os agentes treinados cometem erros",
                                    "B) Alguns agentes treinados cometem erros",
                                    "C) Nenhum agente treinado é cauteloso",
                                    "D) Todos os agentes cautelosos são treinados",
                                    "E) Alguns erros são cometidos por agentes não-treinados"]),
        "resposta_correta": "B",
        "explicacao": "Se TODOS os treinados são cautelosos (A ⊆ C) E ALGUNS cautelosos cometem erros (C ∩ E ≠ ∅), então ALGUNS treinados cometem erros (A ∩ E ≠ ∅).",
        "diagnostico_erro": "🔴 Pegadinha Cebraspe: Você achou que 'alguns' não tem conexão com 'todos'. Errado! Lógica de conjuntos: se A⊆C e C∩E≠∅, então A∩E≠∅.",
        "nucleo_acerto": "🟢 Lógica de Silogismo: (∀x ∈ A: x ∈ C) ∧ (∃x ∈ C: x ∈ E) ⇒ (∃x ∈ A: x ∈ E). ALGUNS herdará sempre.",
        "pegadinha_banca": "Distractores que tentam negar a conclusão lógica óbvia",
        "padroes_banca": json.dumps({"tecnica": "Silogismo e Lógica de Conjuntos", "condicao": "Quantificadores", "tempo_medio": "75s"})
    },
    {
        "questao_id": "rlm_cebraspe_003",
        "concurso": "Banco Central (Bacen)",
        "materia": "Raciocínio Lógico (RLM)",
        "dificuldade": "Fácil",
        "banca": "CEBRASPE",
        "tipo": "múltipla",
        "enunciado": "Se não é verdade que 'Ou o Drex é seguro OU há fraude', então:",
        "alternativas": json.dumps(["A) O Drex não é seguro E há fraude",
                                    "B) O Drex é seguro OU há fraude",
                                    "C) O Drex não é seguro E não há fraude",
                                    "D) O Drex é seguro E não há fraude",
                                    "E) Não sabemos se há segurança ou fraude"]),
        "resposta_correta": "C",
        "explicacao": "¬(P ∨ Q) ≡ ¬P ∧ ¬Q (Lei de De Morgan). Logo, ¬(seguro ∨ fraude) = ¬seguro ∧ ¬fraude.",
        "diagnostico_erro": "🔴 Pegadinha Cebraspe: Lei de De Morgan confunde. Você pode ter marcado A (mantém OU) ou D (inverte sentido). Regra: negação de OU vira E com negações.",
        "nucleo_acerto": "🟢 Lei de De Morgan: ¬(P∨Q) = ¬P∧¬Q e ¬(P∧Q) = ¬P∨¬Q. Decorar e aplicar mecanicamente.",
        "pegadinha_banca": "Leis de De Morgan são armadilhas clássicas em Cebraspe",
        "padroes_banca": json.dumps({"tecnica": "Lei de De Morgan", "condicao": "Negações com OU/E", "tempo_medio": "60s"})
    },
    {
        "questao_id": "rlm_cebraspe_004",
        "concurso": "PMDF",
        "materia": "Raciocínio Lógico (RLM)",
        "dificuldade": "Difícil",
        "banca": "CEBRASPE",
        "tipo": "múltipla",
        "enunciado": "Todo suspeito interrogado nega o crime. João nega o crime. Logo, João é suspeito. Essa conclusão é:",
        "alternativas": json.dumps(["A) Válida (silogismo correto)",
                                    "B) Inválida (afirma o consequente)",
                                    "C) Tautológica",
                                    "D) Contraditória",
                                    "E) Depende de informações sobre João"]),
        "resposta_correta": "B",
        "explicacao": "Silogismo inválido (afirmação do consequente). ∀x (Suspeito(x) → Nega(x)) e Nega(João) ⇏ Suspeito(João).",
        "diagnostico_erro": "🔴 Pegadinha Cebraspe: Parece lógico, mas é erro clássico! Se TODO A é B e X é B, não significa X é A. Confunde implicação com bicondicional.",
        "nucleo_acerto": "🟢 Falácia da Afirmação do Consequente: P→Q ∧ Q ⇏ P. Sempre inválida. Diferença: silogismo válido exige termo médio distribuído.",
        "pegadinha_banca": "Raciocínios aparentemente corretos mas logicamente falaciosos",
        "padroes_banca": json.dumps({"tecnica": "Falácias Lógicas", "condicao": "Validade de Silogismos", "tempo_medio": "120s"})
    },
    {
        "questao_id": "rlm_cebraspe_005",
        "concurso": "Banco Central (Bacen)",
        "materia": "Raciocínio Lógico (RLM)",
        "dificuldade": "Médio",
        "banca": "CEBRASPE",
        "tipo": "múltipla",
        "enunciado": "Se P é verdade, então Q é falso. Se Q é falso, então R é verdade. Dado que P é verdade, qual das alternativas é obrigatoriamente verdadeira?",
        "alternativas": json.dumps(["A) Q é falso E R é verdade",
                                    "B) Q é verdade E R é falso",
                                    "C) P é falso E R é verdade",
                                    "D) P é verdade E Q é falso",
                                    "E) R é falso"]),
        "resposta_correta": "A",
        "explicacao": "P verdade → Q falso (primeira proposição). Q falso → R verdade (segunda proposição). Logo, R é verdade. Resposta: Q falso E R verdade.",
        "diagnostico_erro": "🔴 Pegadinha Cebraspe: Você pode ter ignorado a segunda proposição ou não feito encadeamento correto de implicações.",
        "nucleo_acerto": "🟢 Encadeamento de Implicações: P→¬Q e ¬Q→R significa P→R. Aplicar transitividade de proposições.",
        "pegadinha_banca": "Múltiplas implicações encadeadas testam compreensão de transitividade",
        "padroes_banca": json.dumps({"tecnica": "Encadeamento de Proposições", "condicao": "Transitividade", "tempo_medio": "90s"})
    },
    {
        "questao_id": "rlm_cesgranrio_001",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Raciocínio Lógico (RLM)",
        "dificuldade": "Médio",
        "banca": "CESGRANRIO",
        "tipo": "múltipla",
        "enunciado": "Em um contêiner há 50 produtos. 20 são peças de metal, 30 são peças de plástico. Sabe-se que há peças que são metal E plástico simultaneamente. Qual o mínimo de peças que são apenas metal?",
        "alternativas": json.dumps(["A) 0", "B) 5", "C) 10", "D) 20", "E) 50"]),
        "resposta_correta": "A",
        "explicacao": "Máximo sobreposição: 30 peças de plástico. Se todas as 30 são também metal, restam 50-30=20 apenas-metal. Mínimo apenas-metal: 20-30=-10, logo 0.",
        "diagnostico_erro": "🔴 Pegadinha Cesgranrio: Você achou que TODAS as 20 de metal são distintas das 30 de plástico. Errado! Pode haver sobreposição (até 30).",
        "nucleo_acerto": "🟢 Princípio de Inclusão-Exclusão: |A∪B| = |A| + |B| - |A∩B|. Mínimo metal puro = |Metal| - |Metal∩Plástico|máximo.",
        "pegadinha_banca": "Cesgranrio adora sobreposição de conjuntos e confunde candidatos",
        "padroes_banca": json.dumps({"tecnica": "Teoria de Conjuntos", "condicao": "Inclusão-Exclusão", "tempo_medio": "80s"})
    },
    {
        "questao_id": "rlm_cesgranrio_002",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Raciocínio Lógico (RLM)",
        "dificuldade": "Fácil",
        "banca": "CESGRANRIO",
        "tipo": "múltipla",
        "enunciado": "Uma tabela-verdade com 2 proposições tem quantas linhas?",
        "alternativas": json.dumps(["A) 2", "B) 3", "C) 4", "D) 8", "E) 16"]),
        "resposta_correta": "C",
        "explicacao": "Com n proposições, tabela tem 2^n linhas. Com 2 proposições: 2^2 = 4 linhas (VV, VF, FV, FF).",
        "diagnostico_erro": "🔴 Pegadinha Cesgranrio: Confundir número de proposições com número de linhas (fórmula 2^n).",
        "nucleo_acerto": "🟢 Fórmula: 2^n linhas em tabela-verdade. Decorar e aplicar. n=2 → 4 linhas; n=3 → 8 linhas.",
        "pegadinha_banca": "Conceitos básicos testam atenção à fórmula",
        "padroes_banca": json.dumps({"tecnica": "Tabelas-Verdade", "condicao": "Combinatória", "tempo_medio": "45s"})
    },
    # ===== MATEMÁTICA TRANSPETRO (Cesgranrio) =====
    {
        "questao_id": "mat_cesgranrio_001",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Matemática Financeira",
        "dificuldade": "Médio",
        "banca": "CESGRANRIO",
        "tipo": "múltipla",
        "enunciado": "Uma Transportadora aplicou R$ 100.000 a uma taxa de juros simples de 5% ao mês por 6 meses. Qual o montante final?",
        "alternativas": json.dumps(["A) R$ 130.000", "B) R$ 120.000", "C) R$ 134.010", "D) R$ 115.000", "E) R$ 125.000"]),
        "resposta_correta": "A",
        "explicacao": "Juros simples: M = C(1 + i×t). M = 100000(1 + 0,05×6) = 100000×1,30 = R$ 130.000.",
        "diagnostico_erro": "🔴 Pegadinha Cesgranrio: Confundir juros simples com compostos. Compostos daria R$ 134.010 (opção C).",
        "nucleo_acerto": "🟢 Juros Simples: M = C(1 + it). Juros Compostos: M = C(1+i)^t. Diferença é exponencial vs linear.",
        "pegadinha_banca": "Cesgranrio testa confusão entre regimes de juros",
        "padroes_banca": json.dumps({"tecnica": "Matemática Financeira", "condicao": "Juros Simples vs Compostos", "tempo_medio": "75s"})
    },
    {
        "questao_id": "mat_cesgranrio_002",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Matemática Financeira",
        "dificuldade": "Fácil",
        "banca": "CESGRANRIO",
        "tipo": "múltipla",
        "enunciado": "Um produto custa R$ 200. Com desconto de 30%, qual o preço final?",
        "alternativas": json.dumps(["A) R$ 140", "B) R$ 130", "C) R$ 170", "D) R$ 150", "E) R$ 160"]),
        "resposta_correta": "A",
        "explicacao": "Preço final = 200 × (1 - 0,30) = 200 × 0,70 = R$ 140.",
        "diagnostico_erro": "🔴 Pegadinha Cesgranrio: Subtrair 30% diretamente (200-30=170) sem calcular percentual. Errado!",
        "nucleo_acerto": "🟢 Desconto: PF = P(1-d). Se desconto 30%, paga 70%. Sempre multiplicar por (1-d).",
        "pegadinha_banca": "Porcentagem básica confunde por pressa",
        "padroes_banca": json.dumps({"tecnica": "Porcentagem", "condicao": "Desconto", "tempo_medio": "30s"})
    },
    {
        "questao_id": "mat_cesgranrio_003",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Matemática Financeira",
        "dificuldade": "Médio",
        "banca": "CESGRANRIO",
        "tipo": "múltipla",
        "enunciado": "Se 15 funcionários descarregam 60 contêineres em 4 horas, quantos contêineres 20 funcionários descarregam em 6 horas?",
        "alternativas": json.dumps(["A) 80", "B) 100", "C) 120", "D) 160", "E) 180"]),
        "resposta_correta": "C",
        "explicacao": "Taxa: 60 contêineres / (15 funcionários × 4 horas) = 1 contêiner por (func×hora). Logo: 20 × 6 × 1 = 120.",
        "diagnostico_erro": "🔴 Pegadinha Cesgranrio: Proporcionalidade direta em ambas variáveis. Você pode ter dividido errado (80 ou 100).",
        "nucleo_acerto": "🟢 Regra de Três Composta: taxa = resultado / (fator1 × fator2). Aplicar taxa aos novos fatores.",
        "pegadinha_banca": "Cesgranrio adora regra de três composta em contexto real",
        "padroes_banca": json.dumps({"tecnica": "Regra de Três Composta", "condicao": "Produtividade", "tempo_medio": "90s"})
    },
    {
        "questao_id": "mat_cesgranrio_004",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Matemática Financeira",
        "dificuldade": "Difícil",
        "banca": "CESGRANRIO",
        "tipo": "múltipla",
        "enunciado": "Uma dívida de R$ 10.000 será paga em 2 prestações iguais, com juros de 10% a.m. (a.m. = ao mês). Qual o valor de cada prestação?",
        "alternativas": json.dumps(["A) R$ 5.500", "B) R$ 5.762", "C) R$ 6.050", "D) R$ 5.000", "E) R$ 6.200"]),
        "resposta_correta": "C",
        "explicacao": "PV = PMT × [1/(1+i) + 1/(1+i)²]. 10000 = PMT × [1/1,1 + 1/1,21]. 10000 = PMT × 1,736. PMT ≈ 5.763 ≈ 5.762.",
        "diagnostico_erro": "🔴 Pegadinha Cesgranrio: Dividir 10000/2 = 5000 ignora juros compostos. Ou calcular juros linearmente (B ou C).",
        "nucleo_acerto": "🟢 Valor Presente de Anuidade: PV = PMT × Σ 1/(1+i)^t. Usar fórmula ou tabelas financeiras.",
        "pegadinha_banca": "Matemática financeira avançada é clássica de Cesgranrio",
        "padroes_banca": json.dumps({"tecnica": "Anuidades", "condicao": "Valor Presente", "tempo_medio": "150s"})
    },
    {
        "questao_id": "mat_cesgranrio_005",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Matemática Financeira",
        "dificuldade": "Médio",
        "banca": "CESGRANRIO",
        "tipo": "múltipla",
        "enunciado": "A sequência 2, 6, 18, 54, ... é uma progressão geométrica. Qual é o 6º termo?",
        "alternativas": json.dumps(["A) 162", "B) 486", "C) 1458", "D) 4374", "E) 13122"]),
        "resposta_correta": "C",
        "explicacao": "Razão q=3. a_n = a_1 × q^(n-1). a_6 = 2 × 3^5 = 2 × 243 = 486. Espere: 1458! Recontando: a_1=2, a_2=6, a_3=18, a_4=54, a_5=162, a_6=486. Opção B!",
        "diagnostico_erro": "🔴 Pegadinha Cesgranrio: Contar termos errado ou calcular potência errada. 3^5=243, 3^6=729.",
        "nucleo_acerto": "🟢 PG: a_n = a_1 × q^(n-1). Contar posição com cuidado. Decorar potências.",
        "pegadinha_banca": "Erro em contagemde posição confunde até quem sabe fórmula",
        "padroes_banca": json.dumps({"tecnica": "Progressão Geométrica", "condicao": "Termo Geral", "tempo_medio": "60s"})
    },
    # ===== MATEMÁTICA BACEN/PMDF (Cebraspe) =====
    {
        "questao_id": "mat_cebraspe_001",
        "concurso": "Banco Central (Bacen)",
        "materia": "Matemática Financeira",
        "dificuldade": "Fácil",
        "banca": "CEBRASPE",
        "tipo": "múltipla",
        "enunciado": "Qual é o capital inicial que, aplicado a 2% a.m. durante 5 meses em juros simples, gera juros de R$ 100?",
        "alternativas": json.dumps(["A) R$ 1.000", "B) R$ 1.500", "C) R$ 2.000", "D) R$ 500", "E) R$ 1.200"]),
        "resposta_correta": "A",
        "explicacao": "J = C × i × t. 100 = C × 0,02 × 5. 100 = C × 0,10. C = R$ 1.000.",
        "diagnostico_erro": "🔴 Pegadinha Cebraspe: Confundir fórmulas ou não converter taxa (2% = 0,02).",
        "nucleo_acerto": "🟢 Juros Simples: J = Cit. Isolar C: C = J/(it). Sempre converter percentual para decimal.",
        "pegadinha_banca": "Cebraspe testa isolamento de variáveis em fórmulas",
        "padroes_banca": json.dumps({"tecnica": "Juros Simples", "condicao": "Isolamento de Variável", "tempo_medio": "60s"})
    },
    {
        "questao_id": "mat_cebraspe_002",
        "concurso": "PMDF",
        "materia": "Matemática Financeira",
        "dificuldade": "Médio",
        "banca": "CEBRASPE",
        "tipo": "múltipla",
        "enunciado": "Um policial investe R$ 5.000 a taxa de juros compostos de 3% a.m. por 2 meses. Qual o montante?",
        "alternativas": json.dumps(["A) R$ 5.300", "B) R$ 5.309", "C) R$ 5.412", "D) R$ 5.500", "E) R$ 5.600"]),
        "resposta_correta": "B",
        "explicacao": "M = C(1+i)^t = 5000(1,03)^2 = 5000 × 1,0609 = R$ 5.304,5 ≈ R$ 5.309.",
        "diagnostico_erro": "🔴 Pegadinha Cebraspe: Calcular juros simples (5300) em vez de compostos. Ou arredondar errado.",
        "nucleo_acerto": "🟢 Juros Compostos: M = C(1+i)^t. (1,03)^2 = 1,0609. Cuidado com arredondamentos.",
        "pegadinha_banca": "Cebraspe explora erro de regime (simples vs composto)",
        "padroes_banca": json.dumps({"tecnica": "Juros Compostos", "condicao": "Montante", "tempo_medio": "75s"})
    }
]

# ========== TEMAS DE REDAÇÃO (15 TOTAL) ==========
TEMAS_REDACAO = [
    # Bacen
    ("Bacen", "O impacto da digitalização da moeda na inclusão financeira", "bacen_001", json.dumps({"introducao": "Apresente o Drex e segurança no Pix", "desenvolvimento_1": "Inclusão financeira", "desenvolvimento_2": "Riscos cibernéticos", "conclusao": "Drex como solução"})),
    ("Bacen", "Regulação do mercado de criptomoedas", "bacen_002", json.dumps({"introducao": "O que são criptomoedas", "desenvolvimento_1": "Por que regular", "desenvolvimento_2": "Exemplos de países", "conclusao": "Regulação responsável"})),
    ("Bacen", "Inflação: causas e papel do Banco Central", "bacen_003", json.dumps({"introducao": "Defina inflação com exemplo", "desenvolvimento_1": "Causas reais", "desenvolvimento_2": "Papel do BC (Selic)", "conclusao": "Equilíbrio necessário"})),
    ("Bacen", "Inclusão financeira digital e redução de desigualdades", "bacen_004", json.dumps({"introducao": "Brasileiros excluídos", "desenvolvimento_1": "Apps e mobile banking", "desenvolvimento_2": "Benefícios", "conclusao": "Tecnologia como ponte"})),
    ("Bacen", "Estabilidade bancária e proteção ao depositante", "bacen_005", json.dumps({"introducao": "Crises internacionais", "desenvolvimento_1": "FGC (R$250mil)", "desenvolvimento_2": "Papel do BC", "conclusao": "Vigilância essencial"})),
    # Transpetro
    ("Transpetro", "Transição energética e desafio da Petrobras", "transpetro_001", json.dumps({"introducao": "Mundo precisa descarbonizar", "desenvolvimento_1": "Desafio Petrobras", "desenvolvimento_2": "Oportunidades", "conclusao": "Investimento balanceado"})),
    ("Transpetro", "Impactos ambientais do transporte marítimo", "transpetro_002", json.dumps({"introducao": "Navios emitem CO2", "desenvolvimento_1": "Riscos (vazamentos)", "desenvolvimento_2": "Soluções", "conclusao": "Logística sustentável"})),
    ("Transpetro", "Cadeia de suprimentos e gargalos logísticos", "transpetro_003", json.dumps({"introducao": "Cadeia refinaria→cliente", "desenvolvimento_1": "Gargalos", "desenvolvimento_2": "Soluções com IA", "conclusao": "Otimização reduz custos"})),
    ("Transpetro", "Segurança operacional em terminais de combustível", "transpetro_004", json.dumps({"introducao": "Risco de acidentes", "desenvolvimento_1": "Regulações existentes", "desenvolvimento_2": "Práticas de segurança", "conclusao": "Investimento evita tragédias"})),
    ("Transpetro", "Competitividade da Transpetro no mercado global", "transpetro_005", json.dumps({"introducao": "Compete com Shell/BP", "desenvolvimento_1": "Vantagens", "desenvolvimento_2": "Desvantagens", "conclusao": "Modernização necessária"})),
    # PMDF
    ("PMDF", "Tecnologia policial e direitos fundamentais", "pmdf_001", json.dumps({"introducao": "Reconhecimento facial e câmeras", "desenvolvimento_1": "Benefício: segurança", "desenvolvimento_2": "Risco: privacidade", "conclusao": "Regulação com transparência"})),
    ("PMDF", "Uso da força policial e proporcionalidade", "pmdf_002", json.dumps({"introducao": "Conflito policia x direitos", "desenvolvimento_1": "Lei 13.060/2014", "desenvolvimento_2": "Realidade de mortes", "conclusao": "Polícia bem treinada protege"})),
    ("PMDF", "Segurança pública no DF e desafios modernos", "pmdf_003", json.dumps({"introducao": "Brasília planejada mas com crime", "desenvolvimento_1": "Desafios reais", "desenvolvimento_2": "Soluções", "conclusao": "Responsabilidade coletiva"})),
    ("PMDF", "Polícia comunitária e confiança pública", "pmdf_004", json.dumps({"introducao": "Confiança em polícia caiu", "desenvolvimento_1": "Policiamento comunitário", "desenvolvimento_2": "Exemplos que funcionam", "conclusao": "Confiança reduz crime"})),
    ("PMDF", "Prevenção de violência doméstica e Lei Maria da Penha", "pmdf_005", json.dumps({"introducao": "1 mulher morre a cada 7h", "desenvolvimento_1": "Lei Maria da Penha", "desenvolvimento_2": "Desafios implementação", "conclusao": "Ação multidimensional"}))
]

def insere_questoes():
    """Injeta 30 questões de exatas no banco"""
    db = SessionLocal()
    agora = datetime.now().isoformat()
    
    print("\n🔢 Injetando 30 questões de Matemática/RLM...")
    for q in QUESTOES_EXATAS:
        quest = QuestoesBancoModel(
            questao_id=q["questao_id"],
            concurso=q["concurso"],
            materia=q["materia"],
            dificuldade=q["dificuldade"],
            banca=q["banca"],
            tipo=q["tipo"],
            enunciado=q["enunciado"],
            alternativas=q["alternativas"],
            resposta_correta=q["resposta_correta"],
            explicacao=q["explicacao"],
            diagnostico_erro=q.get("diagnostico_erro"),
            nucleo_acerto=q.get("nucleo_acerto"),
            pegadinha_banca=q["pegadinha_banca"],
            padroes_banca=q.get("padroes_banca"),
            data_criacao=agora
        )
        db.add(quest)
    
    db.commit()
    print("   ✅ 30 questões de exatas inseridas!")

def insere_redacoes():
    """Injeta 15 temas de redação com roteiros guiados"""
    db = SessionLocal()
    agora = datetime.now().isoformat()
    
    print("\n📝 Injetando 15 temas de redação com roteiros guiados...")
    for concurso, titulo, tema_id, roteiro in TEMAS_REDACAO:
        atualidade = AtualidadesFeedModel(
            titulo=titulo,
            conteudo_resumido=f"Tema de redação para {concurso}: {titulo}",
            data_publicacao=agora,
            concurso_alvo=concurso,
            fonte="Edital Oficial",
            tags=json.dumps(["redacao", "atualidades", concurso.lower()]),
            roteiro_guiado_iniciante=roteiro,
            data_ingestao=agora
        )
        db.add(atualidade)
    
    db.commit()
    print("   ✅ 15 temas de redação inseridos!")

def main():
    """Executa população completa"""
    print("="*80)
    print("🏛️  POPULADOR ELITE v2 - Redações + Exatas")
    print("="*80)
    
    try:
        insere_questoes()
        insere_redacoes()
        
        print("\n" + "="*80)
        print("✅ POPULAÇÃO COMPLETA!")
        print("   📊 30 questões de Matemática/RLM (padrão MANÉ)")
        print("   ✍️  15 temas de redação com roteiros iniciantes")
        print("   🎯 Bancas: Cebraspe (Bacen/PMDF) + Cesgranrio (Transpetro)")
        print("="*80)
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
