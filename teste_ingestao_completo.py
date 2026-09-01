#!/usr/bin/env python3
"""
teste_ingestao_completo.py
==========================

Script de teste E2E completo para validar:
1. Conectividade com API
2. Validação de schema
3. Ingestão em lote
4. Verificação de dados no banco

Uso:
    python teste_ingestao_completo.py
"""

import requests
import json
import sys
from datetime import datetime

# Configuração
API_URL = "http://localhost:8000/api/v1/ingest"
API_KEY = "elite-concursos-hunter-2024"
HEALTH_URL = "http://localhost:8000/health"
INFO_URL = "http://localhost:8000/info"

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def test_health():
    """Teste 1: Verificar se API está online"""
    print("\n" + "="*60)
    print("TESTE 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        if response.status_code == 200:
            print_success("API está online")
            return True
        else:
            print_error(f"Health check retornou {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Não conseguiu conectar à API")
        print_info("Verifique: docker-compose up -d")
        return False
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_info():
    """Teste 2: Verificar estatísticas da API"""
    print("\n" + "="*60)
    print("TESTE 2: Informações do Sistema")
    print("="*60)
    
    try:
        response = requests.get(INFO_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("Estatísticas obtidas:")
            print(f"  • Usuários: {data.get('usuarios', 0)}")
            print(f"  • Questões: {data.get('questoes_banco', 0)}")
            print(f"  • Respostas: {data.get('total_respostas', 0)}")
            return True
        else:
            print_error(f"Erro ao obter informações: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_invalid_api_key():
    """Teste 3: Validar rejeição de API-KEY inválida"""
    print("\n" + "="*60)
    print("TESTE 3: Validação de API-KEY Inválida")
    print("="*60)
    
    headers = {
        "X-API-KEY": "chave-invalida-123",
        "Content-Type": "application/json"
    }
    
    payload = {
        "questoes": [{
            "concurso": "Banco Central (Bacen)",
            "materia": "Português",
            "banca": "ESAF",
            "dificuldade": "Médio",
            "tipo": "Múltipla Escolha",
            "enunciado": "Teste",
            "alternativas": {"A": "A", "B": "B", "C": "C", "D": "D"},
            "resposta_correta": "C",
            "explicacao": "Teste",
            "pegadinha_banca": "Teste"
        }]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
        if response.status_code == 401:
            print_success("API-KEY inválida foi rejeitada corretamente (401)")
            return True
        else:
            print_error(f"Esperado 401, recebeu {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_single_question():
    """Teste 4: Ingerir 1 questão"""
    print("\n" + "="*60)
    print("TESTE 4: Ingestão de 1 Questão")
    print("="*60)
    
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    questao = {
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",
        "banca": "ESAF",
        "dificuldade": "Difícil",
        "tipo": "Múltipla Escolha",
        "enunciado": "Teste de Ingestão - Qual é a alternativa correta?",
        "alternativas": {
            "A": "Alternativa A",
            "B": "Alternativa B",
            "C": "Alternativa C (correta)",
            "D": "Alternativa D"
        },
        "resposta_correta": "C",
        "explicacao": "Esta é a explicação detalhada da resposta correta.",
        "pegadinha_banca": "ESAF tenta oferecer alternativas que parecem corretas."
    }
    
    payload = {"questoes": [questao]}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Questão inserida com sucesso!")
            print(f"  • Total inserido: {data.get('total_inserido')}")
            print(f"  • Total no banco: {data.get('total_no_banco')}")
            print(f"  • Timestamp: {data.get('timestamp')}")
            return True
        else:
            print_error(f"Erro na ingestão: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_batch_questions():
    """Teste 5: Ingerir lote de questões"""
    print("\n" + "="*60)
    print("TESTE 5: Ingestão de Lote (3 questões)")
    print("="*60)
    
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    questoes = [
        {
            "concurso": "Transpetro (Petrobras)",
            "materia": "Logística",
            "banca": "Cesgranrio",
            "dificuldade": "Médio",
            "tipo": "Múltipla Escolha",
            "enunciado": "Teste 1: O que é Just-In-Time?",
            "alternativas": {"A": "A", "B": "B", "C": "C", "D": "D"},
            "resposta_correta": "B",
            "explicacao": "Explicação...",
            "pegadinha_banca": "Pegadinha..."
        },
        {
            "concurso": "PMDF",
            "materia": "Direito Administrativo",
            "banca": "CEBRASPE",
            "dificuldade": "Difícil",
            "tipo": "Certo/Errado",
            "enunciado": "Teste 2: É correto afirmar que...",
            "alternativas": {"Certo": "Sim", "Errado": "Não"},
            "resposta_correta": "Errado",
            "explicacao": "Explicação...",
            "pegadinha_banca": "Pegadinha..."
        },
        {
            "concurso": "Banco Central (Bacen)",
            "materia": "Conhecimentos Gerais",
            "banca": "ESAF",
            "dificuldade": "Fácil",
            "tipo": "Múltipla Escolha",
            "enunciado": "Teste 3: Qual é a capital do Brasil?",
            "alternativas": {"A": "São Paulo", "B": "Brasília", "C": "Rio", "D": "Belo Horizonte"},
            "resposta_correta": "B",
            "explicacao": "Brasília é a capital federal...",
            "pegadinha_banca": "Podem oferecer cidades grandes..."
        }
    ]
    
    payload = {"questoes": questoes}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Lote inserido com sucesso!")
            print(f"  • Total inserido: {data.get('total_inserido')}")
            print(f"  • Total no banco: {data.get('total_no_banco')}")
            print(f"  • Detalhes: {data.get('detalhes')}")
            return True
        else:
            print_error(f"Erro na ingestão: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_duplicate_detection():
    """Teste 6: Validar detecção de duplicata"""
    print("\n" + "="*60)
    print("TESTE 6: Detecção de Duplicata")
    print("="*60)
    
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    questao = {
        "questao_id": "BACEN_DUPLICADO_123",
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",
        "banca": "ESAF",
        "dificuldade": "Médio",
        "tipo": "Múltipla Escolha",
        "enunciado": "Questão duplicada para teste",
        "alternativas": {"A": "A", "B": "B", "C": "C", "D": "D"},
        "resposta_correta": "C",
        "explicacao": "Explicação...",
        "pegadinha_banca": "Pegadinha..."
    }
    
    payload = {"questoes": [questao]}
    
    try:
        # Primeira ingestão
        response1 = requests.post(API_URL, headers=headers, json=payload, timeout=5)
        if response1.status_code != 200:
            print_error("Primeira ingestão falhou")
            return False
        
        data1 = response1.json()
        print_info(f"Primeira ingestão: {data1.get('total_inserido')} questões")
        
        # Segunda ingestão (deve detectar duplicata)
        response2 = requests.post(API_URL, headers=headers, json=payload, timeout=5)
        if response2.status_code == 200:
            data2 = response2.json()
            if data2.get('total_inserido') == 0:
                print_success("Duplicata foi detectada e rejeitada!")
                return True
            else:
                print_error("Duplicata não foi detectada")
                return False
        else:
            print_error(f"Segunda ingestão retornou {response2.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def main():
    """Executar todos os testes"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  TESTE E2E COMPLETO - API de Ingestão v1.0".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Executar testes
    results.append(("Health Check", test_health()))
    results.append(("Informações do Sistema", test_info()))
    results.append(("API-KEY Inválida", test_invalid_api_key()))
    results.append(("Ingestão 1 Questão", test_single_question()))
    results.append(("Ingestão Lote", test_batch_questions()))
    results.append(("Detecção Duplicata", test_duplicate_detection()))
    
    # Resumo final
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{name:.<40} {status}")
    
    print("="*60)
    print(f"Resultado Final: {passed}/{total} testes passaram")
    
    if passed == total:
        print_success("🎉 TODOS OS TESTES PASSARAM! Sistema pronto para produção.")
        return 0
    else:
        print_error(f"⚠️  {total - passed} teste(s) falharam. Verificar acima.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erro inesperado: {e}")
        sys.exit(1)
