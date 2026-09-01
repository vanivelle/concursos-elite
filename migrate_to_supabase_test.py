#!/usr/bin/env python3
"""
Migração de 377 questões para Supabase PostgreSQL
Conecta ao Supabase e popula com todas as questões
"""

import psycopg2
from psycopg2.extras import execute_values
import json
import sys

# ========== CREDENTIALS SUPABASE ==========
SUPABASE_HOST = "db.lnnwefppeaaqhpjqpdvz.supabase.co"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "Lightshigaraki789"
SUPABASE_DB = "postgres"
SUPABASE_PORT = 5432

# Connection string
CONNECTION_STRING = f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_HOST}:{SUPABASE_PORT}/{SUPABASE_DB}"

# ========== QUESTÕES DE EXEMPLO ==========
# Em produção, isso viria do arquivo populador_expandido_v33_final.py
# Aqui temos um subset para teste

QUESTOES_BACEN = [
    {
        "questao_id": "BACEN_PORT_001",
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",
        "dificuldade": "Fácil",
        "banca": "CEBRASPE",
        "tipo": "múltipla",
        "enunciado": "A função primordial do Banco Central é:",
        "alternativas": json.dumps({"A": "Emitir moeda e executar política monetária", "B": "Cobrar impostos federais", "C": "Fazer empréstimos pessoais", "D": "Vender ações na bolsa"}),
        "resposta_correta": "A",
        "explicacao": "O Banco Central é responsável pela política monetária, emissão de moeda e estabilidade do sistema financeiro.",
        "diagnostico_erro": "Confundir com funções da Receita Federal ou da Bolsa de Valores",
        "nucleo_acerto": "Compreender o papel do Banco Central no SFN",
        "pegadinha_banca": "Alternativas B e C parecem plausíveis mas são de outros órgãos",
        "padroes_banca": "CEBRASPE frequentemente testa conceitos básicos de instituições financeiras"
    }
]

def conectar_supabase():
    """Conectar ao banco Supabase"""
    try:
        conn = psycopg2.connect(CONNECTION_STRING, sslmode='require')
        print("✅ Conectado ao Supabase PostgreSQL!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Erro de conexão: {e}")
        print(f"   Verificar: host={SUPABASE_HOST}, user={SUPABASE_USER}, db={SUPABASE_DB}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro desconhecido: {e}")
        sys.exit(1)

def criar_tabela(conn):
    """Criar tabela questoes_banco com esquema completo"""
    print("\n📋 Criando tabela...")
    
    with conn.cursor() as cur:
        # Criar tabela
        cur.execute("""
            DROP TABLE IF EXISTS questoes_banco CASCADE;
            
            CREATE TABLE questoes_banco (
                id SERIAL PRIMARY KEY,
                questao_id VARCHAR(100) UNIQUE NOT NULL,
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
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
            
            CREATE INDEX idx_concurso ON questoes_banco(concurso);
            CREATE INDEX idx_materia ON questoes_banco(materia);
            CREATE INDEX idx_dificuldade ON questoes_banco(dificuldade);
            CREATE INDEX idx_banca ON questoes_banco(banca);
        """)
        conn.commit()
        print("✅ Tabela questoes_banco criada!")

def inserir_questoes(conn, questoes):
    """Inserir questões no banco"""
    if not questoes:
        print("❌ Nenhuma questão para inserir!")
        return 0
    
    print(f"\n📥 Inserindo {len(questoes)} questões...")
    
    with conn.cursor() as cur:
        # Preparar tuplas de dados
        dados = [
            (
                q.get("questao_id"),
                q.get("concurso"),
                q.get("materia"),
                q.get("dificuldade"),
                q.get("banca"),
                q.get("tipo"),
                q.get("enunciado"),
                q.get("alternativas"),  # Já é JSON string
                q.get("resposta_correta"),
                q.get("explicacao"),
                q.get("diagnostico_erro"),
                q.get("nucleo_acerto"),
                q.get("pegadinha_banca"),
                q.get("padroes_banca")
            )
            for q in questoes
        ]
        
        # Inserir valores
        sql = """
            INSERT INTO questoes_banco 
            (questao_id, concurso, materia, dificuldade, banca, tipo, 
             enunciado, alternativas, resposta_correta, explicacao,
             diagnostico_erro, nucleo_acerto, pegadinha_banca, padroes_banca)
            VALUES %s
            ON CONFLICT (questao_id) DO NOTHING
        """
        
        execute_values(cur, sql, dados, page_size=100)
        conn.commit()
        
        # Contar total
        cur.execute("SELECT COUNT(*) FROM questoes_banco")
        total = cur.fetchone()[0]
        print(f"✅ Inseridas {len(questoes)} questões! Total no banco: {total}")
        
        return total

def verificar_dados(conn):
    """Verificar e exibir estatísticas"""
    print("\n📊 VERIFICAÇÃO DOS DADOS:")
    
    with conn.cursor() as cur:
        # Total
        cur.execute("SELECT COUNT(*) as total FROM questoes_banco")
        total = cur.fetchone()[0]
        print(f"   Total de questões: {total}")
        
        # Por concurso
        cur.execute("""
            SELECT concurso, COUNT(*) as qty 
            FROM questoes_banco 
            GROUP BY concurso 
            ORDER BY qty DESC
        """)
        
        print(f"\n   Distribuição por concurso:")
        for concurso, qty in cur.fetchall():
            print(f"   • {concurso}: {qty}")
        
        # Por dificuldade
        cur.execute("""
            SELECT dificuldade, COUNT(*) as qty 
            FROM questoes_banco 
            GROUP BY dificuldade 
            ORDER BY qty DESC
        """)
        
        print(f"\n   Distribuição por dificuldade:")
        for dif, qty in cur.fetchall():
            print(f"   • {dif}: {qty}")
        
        # Amostra de uma questão
        cur.execute("SELECT questao_id, enunciado FROM questoes_banco LIMIT 1")
        row = cur.fetchone()
        if row:
            print(f"\n   Amostra de questão:")
            print(f"   ID: {row[0]}")
            print(f"   Enunciado: {row[1][:80]}...")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 MIGRAÇÃO PARA SUPABASE PostgreSQL")
    print("=" * 60)
    
    # Conectar
    conn = conectar_supabase()
    
    # Criar tabela
    criar_tabela(conn)
    
    # Inserir questões (começar com exemplo)
    print("\n⚠️  NOTA: Inserindo questões de exemplo para teste!")
    print("   Para inserir as 377 questões completas, execute:")
    print("   python populate_supabase_full.py")
    
    total = inserir_questoes(conn, QUESTOES_BACEN)
    
    # Verificar
    verificar_dados(conn)
    
    # Fechar
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Migração de teste completa!")
    print("=" * 60)
