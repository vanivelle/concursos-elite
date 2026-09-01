#!/usr/bin/env python3
"""
Script para migrar 377 questões para Supabase
"""

import psycopg2
from psycopg2.extras import execute_values
import sys

# Connection string do Supabase
SUPABASE_URL = "postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres"

# Dados das 377 questões (já temos no sistema)
QUESTOES_DATA = [
    # Bacen - 10 questões de exemplo (usando dados reais)
    {
        "questao_id": "BACEN_001",
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",
        "dificuldade": "Fácil",
        "banca": "CEBRASPE",
        "tipo": "múltipla",
        "enunciado": "Qual é a função primordial do Banco Central?",
        "alternativas": '{"A": "Emitir moeda", "B": "Cobrar impostos", "C": "Fazer empréstimos", "D": "Vender ações"}',
        "resposta_correta": "A",
        "explicacao": "O Banco Central é responsável pela política monetária e emissão de moeda.",
        "diagnostico_erro": "Confundir com funções de outros órgãos",
        "nucleo_acerto": "Conhecimento de estrutura do Sistema Financeiro Nacional",
        "pegadinha_banca": "Alternativas com funções parciais do BC",
        "padroes_banca": "CEBRASPE sempre testa conceitos fundamentais de economia"
    },
    # ... (aqui viriam todas as 377 questões)
]

def connect_supabase():
    """Conectar ao Supabase"""
    try:
        conn = psycopg2.connect(SUPABASE_URL, sslmode='require')
        print("✅ Conectado ao Supabase!")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        sys.exit(1)

def create_table(conn):
    """Criar tabela questoes_banco se não existir"""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS questoes_banco (
                id SERIAL PRIMARY KEY,
                questao_id VARCHAR(50) UNIQUE NOT NULL,
                concurso VARCHAR(200) NOT NULL,
                materia VARCHAR(200) NOT NULL,
                dificuldade VARCHAR(50),
                banca VARCHAR(100),
                tipo VARCHAR(50),
                enunciado TEXT,
                alternativas JSONB,
                resposta_correta VARCHAR(10),
                explicacao TEXT,
                diagnostico_erro TEXT,
                nucleo_acerto TEXT,
                pegadinha_banca TEXT,
                padroes_banca TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
            
            CREATE INDEX IF NOT EXISTS idx_concurso ON questoes_banco(concurso);
            CREATE INDEX IF NOT EXISTS idx_materia ON questoes_banco(materia);
            CREATE INDEX IF NOT EXISTS idx_dificuldade ON questoes_banco(dificuldade);
        """)
        conn.commit()
        print("✅ Tabela questoes_banco criada!")

def insert_questoes(conn, questoes):
    """Inserir questões na tabela"""
    if not questoes:
        print("❌ Nenhuma questão para inserir!")
        return 0
    
    with conn.cursor() as cur:
        # Preparar dados
        data_tuples = [
            (
                q["questao_id"],
                q["concurso"],
                q["materia"],
                q["dificuldade"],
                q["banca"],
                q["tipo"],
                q["enunciado"],
                q["alternativas"],
                q["resposta_correta"],
                q["explicacao"],
                q["diagnostico_erro"],
                q["nucleo_acerto"],
                q["pegadinha_banca"],
                q["padroes_banca"]
            )
            for q in questoes
        ]
        
        # Inserir com ON CONFLICT para evitar duplicatas
        query = """
            INSERT INTO questoes_banco 
            (questao_id, concurso, materia, dificuldade, banca, tipo, 
             enunciado, alternativas, resposta_correta, explicacao,
             diagnostico_erro, nucleo_acerto, pegadinha_banca, padroes_banca)
            VALUES %s
            ON CONFLICT (questao_id) DO NOTHING
        """
        
        execute_values(cur, query, data_tuples)
        conn.commit()
        
        # Contar quantas foram inseridas
        cur.execute("SELECT COUNT(*) FROM questoes_banco")
        total = cur.fetchone()[0]
        print(f"✅ {len(questoes)} questões inseridas! Total: {total} questões")
        return total

def verify_data(conn):
    """Verificar dados inseridos"""
    with conn.cursor() as cur:
        # Total de questões
        cur.execute("SELECT COUNT(*) FROM questoes_banco")
        total = cur.fetchone()[0]
        
        # Por concurso
        cur.execute("""
            SELECT concurso, COUNT(*) as total 
            FROM questoes_banco 
            GROUP BY concurso 
            ORDER BY total DESC
        """)
        distribution = cur.fetchall()
        
        print(f"\n📊 VERIFICAÇÃO:")
        print(f"   Total de questões: {total}")
        print(f"\n   Distribuição por concurso:")
        for concurso, count in distribution:
            print(f"   - {concurso}: {count} questões")
        
        return total

if __name__ == "__main__":
    print("🚀 MIGRATION: Supabase PostgreSQL")
    print("=" * 50)
    
    # Conectar
    conn = connect_supabase()
    
    # Criar tabela
    create_table(conn)
    
    # Inserir questões (por enquanto só exemplo)
    inserted = insert_questoes(conn, QUESTOES_DATA)
    
    # Verificar
    verify_data(conn)
    
    # Fechar conexão
    conn.close()
    print("\n✅ Migração completa!")
