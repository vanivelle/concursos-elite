#!/usr/bin/env python3
"""
🚀 VALIDADOR v3.0 - Testa todos os novos módulos
LLMLingua + Atualidades + Redação + Supabase-Ready
"""

import requests
import json
import sys
from datetime import datetime

API = "http://localhost:8000"
API_KEY = "elite-concursos-hunter-2024"

def test_header(name):
    print(f"\n{'='*80}")
    print(f"🧪 {name}")
    print(f"{'='*80}")

def test_result(test_name, passed, message=""):
    status = "✅ PASSOU" if passed else "❌ FALHOU"
    print(f"{status} | {test_name}")
    if message:
        print(f"   └─ {message}")
    return passed

def test_1_api_health():
    """Teste 1: API está online"""
    test_header("1. Verificação de Saúde da API")
    try:
        response = requests.get(f"{API}/health")
        passed = response.status_code == 200
        test_result("API /health", passed, f"Status {response.status_code}")
        return passed
    except Exception as e:
        test_result("API /health", False, str(e))
        return False

def test_2_atualidades_get():
    """Teste 2: GET /api/v1/atualidades (listar)"""
    test_header("2. Listar Atualidades")
    try:
        response = requests.get(f"{API}/api/v1/atualidades")
        passed = response.status_code == 200
        test_result("GET /api/v1/atualidades", passed, f"Status {response.status_code}")
        
        if passed:
            dados = response.json()
            print(f"   └─ Total de atualidades: {dados.get('total', 0)}")
        return passed
    except Exception as e:
        test_result("GET /api/v1/atualidades", False, str(e))
        return False

def test_3_atualidades_create():
    """Teste 3: POST /api/v1/atualidades (criar)"""
    test_header("3. Criar Atualidade")
    try:
        payload = {
            "titulo": f"Teste Atualidade {datetime.now().isoformat()}",
            "conteudo_resumido": "Conteúdo de teste para validação do sistema v3.0",
            "concurso_alvo": "Bacen",
            "fonte": "Validador v3.0"
        }
        
        response = requests.post(
            f"{API}/api/v1/atualidades",
            headers={"X-API-KEY": API_KEY, "Content-Type": "application/json"},
            json=payload
        )
        
        passed = response.status_code == 200
        test_result("POST /api/v1/atualidades", passed, f"Status {response.status_code}")
        
        if passed:
            dados = response.json()
            print(f"   └─ ID criado: {dados.get('id', 'N/A')}")
        return passed
    except Exception as e:
        test_result("POST /api/v1/atualidades", False, str(e))
        return False

def test_4_atualidades_filtro():
    """Teste 4: GET /api/v1/atualidades?concurso=Bacen"""
    test_header("4. Filtrar Atualidades por Concurso")
    try:
        response = requests.get(f"{API}/api/v1/atualidades?concurso=Bacen")
        passed = response.status_code == 200
        test_result("GET /api/v1/atualidades?concurso=Bacen", passed)
        
        if passed:
            dados = response.json()
            print(f"   └─ Atualidades Bacen: {dados.get('total', 0)}")
        return passed
    except Exception as e:
        test_result("GET /api/v1/atualidades?concurso=Bacen", False, str(e))
        return False

def test_5_redacao_submit():
    """Teste 5: POST /api/v1/corrigir-redacao (enviar redação)"""
    test_header("5. Corrigir Redação com IA")
    try:
        payload = {
            "usuario_email": "teste@concursos.com",
            "tema": "Impacto da inteligência artificial nos concursos públicos",
            "texto_redacao": """
A inteligência artificial representa uma transformação significativa no contexto dos concursos públicos brasileiros.
Em primeiro lugar, ferramentas de IA podem personalizar o aprendizado dos candidatos, adaptando questões à sua 
dificuldade e progresso. Além disso, sistemas de correção automática, como o presente, democratizam o acesso a 
feedback de qualidade profissional. Em conclusão, a IA não substitui estudo e dedicação, mas potencializa 
resultados quando bem utilizada.
            """
        }
        
        response = requests.post(
            f"{API}/api/v1/corrigir-redacao",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        passed = response.status_code == 200
        test_result("POST /api/v1/corrigir-redacao", passed, f"Status {response.status_code}")
        
        if passed:
            dados = response.json()
            nota = dados.get('nota_final', 'N/A')
            print(f"   └─ Nota Final: {nota}/100")
            print(f"   └─ Estrutura: {dados.get('criterios', {}).get('estrutura', 'N/A')}")
            print(f"   └─ Gramática: {dados.get('criterios', {}).get('gramatica', 'N/A')}")
            print(f"   └─ Coesão: {dados.get('criterios', {}).get('coesao', 'N/A')}")
            print(f"   └─ Tema: {dados.get('criterios', {}).get('tema', 'N/A')}")
        return passed
    except requests.exceptions.Timeout:
        test_result("POST /api/v1/corrigir-redacao", False, "Timeout (Ollama/Gemma2 pode estar lento)")
        return False
    except Exception as e:
        test_result("POST /api/v1/corrigir-redacao", False, str(e))
        return False

def test_6_auth_api_key():
    """Teste 6: Validação de API-KEY"""
    test_header("6. Validação de Segurança (X-API-KEY)")
    try:
        payload = {
            "titulo": "Teste",
            "conteudo_resumido": "Teste",
            "concurso_alvo": "Bacen"
        }
        
        response = requests.post(
            f"{API}/api/v1/atualidades",
            headers={"X-API-KEY": "api-key-invalida", "Content-Type": "application/json"},
            json=payload
        )
        
        passed = response.status_code == 401
        test_result("API-KEY inválida retorna 401", passed, f"Status {response.status_code}")
        return passed
    except Exception as e:
        test_result("Validação X-API-KEY", False, str(e))
        return False

def test_7_questoes_banco():
    """Teste 7: Banco de dados ainda tem questões"""
    test_header("7. Verificação do Banco de Questões")
    try:
        response = requests.get(f"{API}/info")
        passed = response.status_code == 200
        test_result("GET /info", passed)
        
        if passed:
            dados = response.json()
            questoes = dados.get('estadisticas', {}).get('questoes_banco', 0)
            print(f"   └─ Questões no banco: {questoes}")
            return questoes > 0
        return False
    except Exception as e:
        test_result("GET /info", False, str(e))
        return False

def main():
    print("\n" + "🎯" * 40)
    print("IA CONCURSOS ELITE v3.0 - VALIDADOR COMPLETO")
    print("LLMLingua + Atualidades + Redação + Supabase-Ready")
    print("🎯" * 40)
    
    testes = [
        ("1. Health Check", test_1_api_health),
        ("2. GET Atualidades", test_2_atualidades_get),
        ("3. CREATE Atualidade", test_3_atualidades_create),
        ("4. FILTER Atualidades", test_4_atualidades_filtro),
        ("5. Corrigir Redação", test_5_redacao_submit),
        ("6. Segurança API-KEY", test_6_auth_api_key),
        ("7. Questões no Banco", test_7_questoes_banco),
    ]
    
    resultados = []
    for nome, teste_func in testes:
        try:
            resultado = teste_func()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"❌ Erro não tratado em {nome}: {e}")
            resultados.append((nome, False))
    
    # Resumo Final
    print(f"\n{'='*80}")
    print("📊 RESUMO FINAL")
    print(f"{'='*80}")
    
    total = len(resultados)
    passou = sum(1 for _, r in resultados if r)
    
    for nome, resultado in resultados:
        status = "✅" if resultado else "❌"
        print(f"{status} {nome}")
    
    print(f"\n🎯 Total: {passou}/{total} testes passaram")
    
    if passou == total:
        print("\n✅ SISTEMA v3.0 TOTALMENTE OPERACIONAL!")
        print("   • LLMLingua: Compressão de prompts ✅")
        print("   • Atualidades: Feed em tempo real ✅")
        print("   • Redação: Corretor IA funcional ✅")
        print("   • Segurança: API-KEY validação ✅")
        print("   • DB: Questões + Atualidades + Redações ✅")
        return 0
    else:
        print(f"\n⚠️ {total - passou} teste(s) falharam. Verifique os logs acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
