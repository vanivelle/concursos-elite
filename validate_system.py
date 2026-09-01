#!/usr/bin/env python3
"""
validate_system.py
==================

Script simples para validar se o sistema está funcionando corretamente.

Uso:
    python validate_system.py
"""

import requests
import sys

def validate():
    """Validação rápida do sistema"""
    
    print("\n" + "="*60)
    print("✅ VALIDAÇÃO DO SISTEMA - IA Concursos Elite v1.0")
    print("="*60 + "\n")
    
    checks = []
    
    # Check 1: Health
    try:
        resp = requests.get("http://localhost:8000/health", timeout=3)
        if resp.status_code == 200:
            print("✅ API está online")
            checks.append(True)
        else:
            print("❌ API retornou status não esperado")
            checks.append(False)
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        checks.append(False)
    
    # Check 2: Info
    try:
        resp = requests.get("http://localhost:8000/info", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            qs = data.get('questoes_banco', 0)
            print(f"✅ Banco de dados: {qs} questões")
            checks.append(True)
        else:
            print("❌ Erro ao obter informações")
            checks.append(False)
    except Exception as e:
        print(f"❌ Erro: {e}")
        checks.append(False)
    
    # Check 3: API-KEY (negativo)
    try:
        resp = requests.post(
            "http://localhost:8000/api/v1/ingest",
            headers={"X-API-KEY": "invalid"},
            json={"questoes": []},
            timeout=3
        )
        if resp.status_code == 401:
            print("✅ Autenticação funcionando (401 para chave inválida)")
            checks.append(True)
        else:
            print("❌ Autenticação não está funcionando")
            checks.append(False)
    except Exception as e:
        print(f"❌ Erro: {e}")
        checks.append(False)
    
    # Resultado
    print("\n" + "="*60)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ {passed}/{total} verificações passaram!")
        print("\n🟢 SISTEMA PRONTO PARA USO")
        print("\nPróximos passos:")
        print("  1. Ler QUICK_START.md")
        print("  2. Executar: python teste_ingestao_completo.py")
        print("  3. Consultar: INDEX.md para documentação")
        print("="*60 + "\n")
        return 0
    else:
        print(f"❌ {total - passed} verificação(ões) falharam!")
        print("\nTroubleshoot:")
        print("  docker-compose up -d")
        print("  docker logs backend_questoes")
        print("="*60 + "\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = validate()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário.")
        sys.exit(1)
