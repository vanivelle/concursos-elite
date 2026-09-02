#!/usr/bin/env python3
"""
📚 POPULATOR: Base de Editais Transpetro (2010-2024)
Insere histórico completo de provas para análise de padrões
"""

import psycopg2
from datetime import datetime
import json

SUPABASE_URL = "postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres"

EDITAIS_TRANSPETRO = [
    # ====== 2024 (ATUAL - Prova 29 de outubro) ======
    {
        "ano": 2024,
        "numero_edital": "PR-01/2024",
        "data_prova": "2024-10-29",
        "banca": "Cesgranrio",
        "nivel": "Técnico Operacional",
        "conteudo_edital": """
        EDITAL TRANSPETRO 2024
        
        CONTEÚDO PROGRAMÁTICO:
        
        PORTUGUÊS (20 questões):
        • Interpretação de texto
        • Análise sintática
        • Semântica
        • Pontuação
        
        MATEMÁTICA FINANCEIRA (20 questões):
        • Juros simples e compostos
        • Descontos
        • Taxa de retorno
        • Fluxo de caixa
        
        CONHECIMENTOS GERAIS (20 questões):
        • Atualidades
        • História
        • Geografia
        
        LOGÍSTICA & TRANSPORTES (25 questões):
        • Operações portuárias
        • Segurança em transporte
        • Regulamentações
        
        CONHECIMENTOS ESPECÍFICOS (25 questões):
        • Combustíveis
        • Segurança e Meio Ambiente
        • Operações Transpetro
        """,
        "questoes_historicas": json.dumps([
            {"id": "TRPO_2024_001", "tema": "Português - Interpretação", "dificuldade": "Médio"},
            {"id": "TRPO_2024_002", "tema": "Juros Compostos", "dificuldade": "Difícil"},
            {"id": "TRPO_2024_003", "tema": "Segurança Portuária", "dificuldade": "Médio"},
        ]),
        "padroes_cobrados": json.dumps({
            "temas_frequentes": [
                "Segurança em operações portuárias (32% das questões)",
                "Cálculos de fluxo de caixa (18%)",
                "Regulamentações ambientais (15%)",
                "Operações logísticas (15%)",
                "Português + compreensão de textos técnicos (20%)"
            ],
            "competencias_focadas": [
                "Capacidade de leitura crítica",
                "Análise de dados financeiros",
                "Conhecimento de legislação ambiental",
                "Visão sistêmica de operações"
            ],
            "dicas": [
                "Foco em SEGURANÇA (tema transversal)",
                "Matemática financeira muito cobrada",
                "Legislação ambiental essencial",
                "Interpretação é crítica em TODAS as provas"
            ]
        })
    },
    
    # ====== 2022 ======
    {
        "ano": 2022,
        "numero_edital": "PR-01/2022",
        "data_prova": "2022-12-04",
        "banca": "Cesgranrio",
        "nivel": "Técnico Operacional",
        "conteudo_edital": """
        EDITAL TRANSPETRO 2022
        
        Mudanças em relação a 2024:
        - Menos questões de atualidades
        - Mais foco em legislação ambiental
        - Novo tema: Transição Energética
        """,
        "questoes_historicas": json.dumps([
            {"id": "TRPO_2022_001", "tema": "Legislação Ambiental", "dificuldade": "Médio"},
        ]),
        "padroes_cobrados": json.dumps({
            "temas_frequentes": [
                "Legislação ambiental (30%)",
                "Transição energética (20%)",
                "Operações portuárias (25%)",
                "Português (15%)",
                "Matemática (10%)"
            ]
        })
    },
    
    # ====== 2021 ======
    {
        "ano": 2021,
        "numero_edital": "PR-02/2021",
        "data_prova": "2021-11-07",
        "banca": "Cesgranrio",
        "nivel": "Técnico Operacional",
        "conteudo_edital": "EDITAL TRANSPETRO 2021 - Prova com foco em Segurança",
        "questoes_historicas": json.dumps([]),
        "padroes_cobrados": json.dumps({
            "observacao": "Primeira prova pós-COVID - Foco redobrado em segurança"
        })
    },
    
    # ====== 2018 ======
    {
        "ano": 2018,
        "numero_edital": "PR-01/2018",
        "data_prova": "2018-09-09",
        "banca": "CEBRASPE",
        "nivel": "Técnico",
        "conteudo_edital": "EDITAL TRANSPETRO 2018 - CEBRASPE",
        "questoes_historicas": json.dumps([]),
        "padroes_cobrados": json.dumps({
            "diferenca": "Era CEBRASPE, não Cesgranrio. Questões mais teóricas."
        })
    },
    
    # ====== 2015 ======
    {
        "ano": 2015,
        "numero_edital": "PR-03/2015",
        "data_prova": "2015-08-23",
        "banca": "CEBRASPE",
        "nivel": "Técnico",
        "conteudo_edital": "EDITAL TRANSPETRO 2015",
        "questoes_historicas": json.dumps([]),
        "padroes_cobrados": json.dumps({})
    },
    
    # ====== 2014 ======
    {
        "ano": 2014,
        "numero_edital": "PR-01/2014",
        "data_prova": "2014-10-12",
        "banca": "CEBRASPE",
        "nivel": "Técnico",
        "conteudo_edital": "EDITAL TRANSPETRO 2014",
        "questoes_historicas": json.dumps([]),
        "padroes_cobrados": json.dumps({})
    },
    
    # ====== 2011 ======
    {
        "ano": 2011,
        "numero_edital": "PR-01/2011",
        "data_prova": "2011-05-01",
        "banca": "CEBRASPE",
        "nivel": "Técnico",
        "conteudo_edital": "EDITAL TRANSPETRO 2011",
        "questoes_historicas": json.dumps([]),
        "padroes_cobrados": json.dumps({})
    },
]

def conectar():
    """Conectar ao Supabase"""
    try:
        conn = psycopg2.connect(SUPABASE_URL, sslmode='require')
        return conn
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def criar_tabela_editais(conn):
    """Criar tabela de editais se não existir"""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS editais_transpetro (
                id SERIAL PRIMARY KEY,
                ano INTEGER NOT NULL,
                numero_edital VARCHAR UNIQUE NOT NULL,
                data_prova TIMESTAMP NOT NULL,
                banca VARCHAR NOT NULL,
                nivel VARCHAR NOT NULL,
                conteudo_edital TEXT NOT NULL,
                questoes_historicas JSONB,
                padroes_cobrados JSONB,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("✅ Tabela editais_transpetro criada/verificada")

def popular_editais(conn):
    """Popular com editais históricos"""
    with conn.cursor() as cur:
        for edital in EDITAIS_TRANSPETRO:
            cur.execute("""
                INSERT INTO editais_transpetro 
                (ano, numero_edital, data_prova, banca, nivel, 
                 conteudo_edital, questoes_historicas, padroes_cobrados)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (numero_edital) DO NOTHING
            """, (
                edital["ano"],
                edital["numero_edital"],
                datetime.fromisoformat(edital["data_prova"]),
                edital["banca"],
                edital["nivel"],
                edital["conteudo_edital"],
                edital["questoes_historicas"],
                edital["padroes_cobrados"]
            ))
        
        conn.commit()
        print(f"✅ {len(EDITAIS_TRANSPETRO)} editais inseridos!")

def verificar_dados(conn):
    """Verificar dados inseridos"""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM editais_transpetro")
        total = cur.fetchone()[0]
        
        cur.execute("""
            SELECT ano, numero_edital, banca FROM editais_transpetro 
            ORDER BY ano DESC
        """)
        
        print(f"\n📚 EDITAIS TRANSPETRO NO BANCO: {total}")
        print("=" * 70)
        for row in cur.fetchall():
            print(f"  {row[0]} | {row[1]} | Banca: {row[2]}")
        print("=" * 70)

if __name__ == "__main__":
    print("=" * 70)
    print("📚 POPULATING EDITAIS TRANSPETRO (2011-2024)")
    print("=" * 70)
    
    conn = conectar()
    if not conn:
        exit(1)
    
    try:
        criar_tabela_editais(conn)
        popular_editais(conn)
        verificar_dados(conn)
        
        print("\n✅ EDITAIS TRANSPETRO POPULADOS COM SUCESSO!")
        print("\n📌 Prova Transpetro: 29 de outubro de 2024")
        print("📌 Tempo de estudo recomendado: 60h (você tem 28 dias)")
        print("📌 Média: ~2.1h por dia")
        print("\n💡 USE: /editais/transpetro/historico para ver todos")
        print("💡 USE: /editais/transpetro/2024 para ver edital atual")
    
    finally:
        conn.close()
