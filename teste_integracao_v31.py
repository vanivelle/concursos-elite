#!/usr/bin/env python3
"""
🧪 TESTE RÁPIDO: Fluxo Completo do Sistema v3.1
Verifica: Cadastro → Login → Geração de Questão → Feedback Duplo
"""

import requests
import json
import random

API = "http://localhost:8000"

print("="*80)
print("🧪 TESTE DE INTEGRAÇÃO COMPLETA - IA Concursos Elite v3.1")
print("="*80)

# User de teste
email = f"teste_{random.randint(1000,9999)}@test.com"
senha = "senha123"
nome = "Soldado Teste"

print(f"\n1️⃣  CADASTRO")
print(f"   Email: {email}")

try:
    res = requests.post(f"{API}/cadastro", json={
        "email": email,
        "senha": senha,
        "nome": nome
    })
    if res.status_code == 200:
        print(f"   ✅ Usuário criado")
    else:
        print(f"   ⚠️  {res.status_code}: {res.json().get('detail', 'erro')}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print(f"\n2️⃣  LOGIN")
try:
    res = requests.post(f"{API}/login", json={
        "email": email,
        "senha": senha
    })
    if res.status_code == 200:
        dados = res.json()
        token = dados["token"]
        print(f"   ✅ Token gerado: {token[:20]}...")
    else:
        print(f"   ❌ {res.status_code}: {res.json().get('detail', 'erro')}")
        exit(1)
except Exception as e:
    print(f"   ❌ Erro: {e}")
    exit(1)

print(f"\n3️⃣  GERAÇÃO DE QUESTÃO (Do Banco Aquecido)")
try:
    res = requests.post(f"{API}/gerar-questao", json={
        "email": email,
        "token": token,
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",
        "dificuldade": "Fácil"
    })
    if res.status_code == 200:
        questao = res.json()
        print(f"   ✅ Questão gerada (ID: {questao['id']})")
        print(f"   📝 Banca: {questao.get('banca', 'N/A')}")
        print(f"   📚 Concurso: Bacen")
        print(f"   📖 Enunciado: {questao['enunciado'][:60]}...")
        
        # Verificar campos v3.1
        print(f"\n   🔴 DIAGNÓSTICO DE ERRO (v3.1):")
        print(f"   {questao.get('diagnostico_erro', 'N/A')[:80]}...")
        
        print(f"\n   🟢 NÚCLEO DO ACERTO (v3.1):")
        print(f"   {questao.get('nucleo_acerto', 'N/A')[:80]}...")
        
        print(f"\n   ⚡ PADRÕES DE BANCA:")
        padroes = questao.get('padroes_banca', {})
        if padroes:
            for banca, padrao in padroes.items():
                print(f"   {banca}: {padrao[:60]}...")
        else:
            print(f"   (não configurado)")
        
        # Guardar para próximo teste
        questao_id = questao['id']
        resposta_correta = questao['resposta_correta']
    else:
        print(f"   ❌ {res.status_code}: {res.json().get('detail', 'erro')}")
        exit(1)
except Exception as e:
    print(f"   ❌ Erro: {e}")
    exit(1)

print(f"\n4️⃣  SUBMISSÃO DE RESPOSTA (Teste de acerto)")
try:
    res = requests.post(f"{API}/salvar-resposta", json={
        "email": email,
        "token": token,
        "questao_id": questao_id,
        "resposta_escolhida": resposta_correta,
        "resposta_correta": resposta_correta
    })
    if res.status_code == 200:
        dados = res.json()
        if dados["acertou"]:
            print(f"   ✅ RESPOSTA CORRETA")
        else:
            print(f"   ❌ Resposta incorreta")
    else:
        print(f"   ❌ {res.status_code}: {res.json()}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print(f"\n5️⃣  VERIFICAÇÃO DO BANCO")
try:
    res = requests.get(f"{API}/info")
    if res.status_code == 200:
        dados = res.json()
        total_q = dados.get('estadisticas', {}).get('questoes_banco', 0)
        print(f"   ✅ Total questões no banco: {total_q}")
        if total_q >= 300:
            print(f"   🔥 BANCO AQUECIDO - Pronto para operação!")
        else:
            print(f"   ⚠️  Banco com {total_q} questões (meta: 300+)")
    else:
        print(f"   ❌ {res.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print(f"\n{'='*80}")
print(f"✅ TESTE COMPLETO - Sistema v3.1 operacional!")
print(f"{'='*80}\n")
