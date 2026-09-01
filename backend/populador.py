#!/usr/bin/env python3
"""
🏛️ POPULADOR DE QUESTÕES ELITE
Carrega questões reais de Bacen, Transpetro e PMDF no banco PostgreSQL
Usa Ollama para estruturação, depois insere direto na tabela questoes_banco
"""

import os
import json
import requests
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:senha_segura_123@postgres_db:5432/admin")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma2:2b")

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

def limpar_json(texto):
    """Remove markdown e extrai JSON puro"""
    if texto.startswith("```json"):
        texto = texto.replace("```json", "").replace("```", "").strip()
    elif texto.startswith("```"):
        texto = texto.replace("```", "").strip()
    return texto.strip()

def gerar_questao_ollama(concurso, materia, dificuldade):
    """Usa Ollama para gerar 1 questão estruturada"""
    
    if concurso == "Banco Central (Bacen)":
        banca = "ESAF"
        tipo = "Múltipla Escolha"
        estilo = """Questão de fiscal/administrativo com foco em:
- Lei de Responsabilidade Fiscal (LRF)
- COFINS/PIS
- Administração Pública
- Lei 8.112/90
Use 5 alternativas (A-E) com pegadinha técnica clássica."""
    
    elif concurso == "Transpetro (Petrobras)":
        banca = "Cesgranrio"
        tipo = "Múltipla Escolha"
        estilo = """Questão de administração/logística com foco em:
- Gestão de Operações
- Logística e Supply Chain
- Licitação (Lei 14.133/21)
- Contratos Públicos
Use 5 alternativas (A-E) com detalhe técnico esperado em Cesgranrio."""
    
    else:  # PMDF
        banca = "CEBRASPE"
        tipo = "Certo/Errado" if dificuldade == "Difícil" else "Múltipla Escolha"
        estilo = """Questão de segurança pública/admin com foco em:
- Código de Ética Profissional
- Lei Geral de Proteção de Dados (LGPD)
- Estrutura Administrativa
- Direitos e Deveres Funcionários
Se Certo/Errado: afirmativas múltiplas com pegadinha clássica CEBRASPE.
Se Múltipla: 5 alternativas (A-E)."""
    
    prompt = f"""Você é um especialista em concursos públicos de élite.
Gere EXATAMENTE 1 questão para:
- Concurso: {concurso}
- Matéria: {materia}
- Dificuldade: {dificuldade}
- Estilo: {estilo}

RETORNE APENAS este JSON (sem nada mais):
{{
    "questao_id": "q_{concurso.split()[0].lower()}_{materia.split()[0].lower()}_{dificuldade.lower()}_{datetime.now().timestamp()}",
    "enunciado": "[enunciado da questão com 2-3 linhas]",
    "tipo": "{tipo}",
    "alternativas": {{"A": "[alternativa A]", "B": "[alternativa B]", "C": "[alternativa C]", "D": "[alternativa D]", "E": "[alternativa E]"}},
    "resposta_correta": "C",
    "explicacao": "[explicação clara em 2-3 linhas]",
    "pegadinha_banca": "[qual é o truque que a banca usa aqui]"
}}

Nenhum texto fora do JSON. Retorne direto o JSON."""
    
    try:
        print(f"  ⏳ Gerando {concurso} - {materia} ({dificuldade})...", end=" ")
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        
        if response.status_code != 200:
            print("❌ Ollama Error")
            return None
        
        resultado = response.json()
        texto = limpar_json(resultado.get("response", ""))
        dados = json.loads(texto)
        
        print("✅")
        return dados
        
    except Exception as e:
        print(f"❌ {str(e)}")
        return None

def popular_banco():
    """Popula o banco com questões de elite"""
    
    db = SessionLocal()
    print(f"\n🏛️ POPULADOR DE QUESTÕES ELITE - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Verificar se já tem dados
    total_existente = db.query(QuestoesBancoModel).count()
    if total_existente > 0:
        print(f"✅ Banco já possui {total_existente} questões. Pulando população.")
        db.close()
        return
    
    # Configuração de questões por concurso
    config = {
        "Banco Central (Bacen)": {
            "bancas": ["ESAF"],
            "materias": ["Português", "Direito Penal", "Lei 8.112/90", "Conhecimentos Gerais"],
            "dificuldades": ["Fácil", "Médio", "Difícil"],
            "quantidade": 3  # 3 por matéria = 12 total
        },
        "Transpetro (Petrobras)": {
            "bancas": ["Cesgranrio"],
            "materias": ["Português", "Logística", "Direito Penal", "Conhecimentos Gerais"],
            "dificuldades": ["Fácil", "Médio", "Difícil"],
            "quantidade": 3
        },
        "PMDF": {
            "bancas": ["CEBRASPE"],
            "materias": ["Português", "Direito Penal", "Direito Administrativo", "Conhecimentos Gerais"],
            "dificuldades": ["Fácil", "Médio", "Difícil"],
            "quantidade": 2
        }
    }
    
    total_gerado = 0
    
    for concurso, config_concurso in config.items():
        print(f"\n📚 {concurso}")
        
        for materia in config_concurso["materias"]:
            print(f"   📖 {materia}")
            
            for dificuldade in config_concurso["dificuldades"]:
                for _ in range(config_concurso["quantidade"]):
                    questao_data = gerar_questao_ollama(concurso, materia, dificuldade)
                    
                    if questao_data:
                        try:
                            questao = QuestoesBancoModel(
                                questao_id=questao_data.get("questao_id", f"q_{total_gerado}"),
                                concurso=concurso,
                                materia=materia,
                                dificuldade=dificuldade,
                                banca=config_concurso["bancas"][0],
                                tipo=questao_data.get("tipo", "Múltipla Escolha"),
                                enunciado=questao_data.get("enunciado", ""),
                                alternativas=json.dumps(questao_data.get("alternativas", {})),
                                resposta_correta=questao_data.get("resposta_correta", "A"),
                                explicacao=questao_data.get("explicacao", ""),
                                pegadinha_banca=questao_data.get("pegadinha_banca", "")
                            )
                            db.add(questao)
                            db.commit()
                            total_gerado += 1
                        except Exception as e:
                            print(f"      ❌ Erro ao salvar: {e}")
                            db.rollback()
    
    print("\n" + "=" * 60)
    print(f"✅ POPULAÇÃO CONCLUÍDA: {total_gerado} questões inseridas")
    print(f"   Bacen: ~12 | Transpetro: ~12 | PMDF: ~8")
    print(f"   Total esperado: ~32 questões de elite")
    print("=" * 60)
    
    db.close()

if __name__ == "__main__":
    try:
        popular_banco()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {e}")
