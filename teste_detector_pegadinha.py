#!/usr/bin/env python3
"""
✅ VALIDAÇÃO: Mapeamento de Banca no Detector de Pegadinha v3.1
Simula diferentes variações de banca recebidas do PostgreSQL
"""

import requests
import json

API = "http://localhost:8000"

# Dados de teste
email = "teste@detector.com"
senha = "teste123"
nome = "Validador Detector"

print("="*80)
print("🧪 TESTE: Detector de Pegadinha - Mapeamento de Banca")
print("="*80)

# 1. Cadastro
print("\n1️⃣ Cadastrando usuário...")
try:
    res = requests.post(f"{API}/cadastro", json={"email": email, "senha": senha, "nome": nome})
    if res.status_code == 200:
        print("   ✅ Usuário criado")
    else:
        print(f"   ⚠️  {res.status_code}: {res.text}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 2. Login
print("\n2️⃣ Fazendo login...")
try:
    res = requests.post(f"{API}/login", json={"email": email, "senha": senha})
    if res.status_code == 200:
        token = res.json()["token"]
        print(f"   ✅ Token gerado")
    else:
        print(f"   ❌ Login falhou")
        exit(1)
except Exception as e:
    print(f"   ❌ Erro: {e}")
    exit(1)

# 3. Testar com diferentes concursos/bancas
print("\n3️⃣ Testando Detector com diferentes Concursos...")

test_cases = [
    ("Banco Central (Bacen)", "Português", "Fácil", "ESAF"),
    ("Transpetro (Petrobras)", "Português", "Fácil", "Cesgranrio"),
    ("PMDF", "Português", "Fácil", "CEBRASPE"),  # ← Caso crítico!
]

for concurso, materia, dificuldade, banca_esperada in test_cases:
    print(f"\n   🎯 {concurso} → Esperado: {banca_esperada}")
    try:
        res = requests.post(f"{API}/gerar-questao", json={
            "email": email,
            "token": token,
            "concurso": concurso,
            "materia": materia,
            "dificuldade": dificuldade
        })
        
        if res.status_code == 200:
            dados = res.json()
            banca_recebida = dados.get("banca", "N/A")
            
            # Verificar correspondência
            if banca_recebida.upper() == banca_esperada.upper():
                print(f"      ✅ Banca: {banca_recebida} (CORRETO)")
                
                # Validar campos v3.1
                diag = dados.get("diagnostico_erro", "N/A")[:50]
                nucleo = dados.get("nucleo_acerto", "N/A")[:50]
                padroes = dados.get("padroes_banca", {})
                
                print(f"      ✅ diagnostico_erro: {diag}...")
                print(f"      ✅ nucleo_acerto: {nucleo}...")
                print(f"      ✅ padroes_banca: {len(padroes)} bancas configuradas")
            else:
                print(f"      ⚠️  Banca: {banca_recebida} (esperava {banca_esperada})")
        else:
            print(f"      ❌ {res.status_code}: {res.json().get('detail', 'erro')}")
    except Exception as e:
        print(f"      ❌ Erro: {e}")

print("\n" + "="*80)
print("✅ TESTE CONCLUÍDO")
print("="*80)
print("\n📝 Instrução: Abra browser (F12 → Console) para ver logs de mapeamento:")
print("   [DETECTOR DE PEGADINHA] Entrada: \"CEBRASPE\" | Concurso: \"PMDF\" | ...\n")
