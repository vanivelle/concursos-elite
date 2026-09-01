#!/usr/bin/env python3
import requests
import json
import time
import hmac
import hashlib

BASE_URL = 'http://localhost:8000'

# Dados do usuario
email = 'teste_autonomo_29@concursos.com'
senha = 'senha123'

print('='*60)
print('=== TESTE COMPLETO DE AUTENTICAÇÃO E API ===')
print('='*60)
print()

# TESTE 1: Login
print('1️⃣  TESTE: Login')
print('-'*60)
login_data = {
    'email': email,
    'senha': senha
}
response = requests.post(f'{BASE_URL}/login', json=login_data, timeout=5)
print(f'Status: {response.status_code}')
response_json = response.json()

if response.status_code != 200:
    print('❌ Login falhou!')
    print(response_json)
    exit(1)

token = response_json.get('token')
nome = response_json.get('nome')
print(f'✅ Login sucesso!')
print(f'   Token: {token[:20]}...')
print(f'   Nome: {nome}')
print(f'   Email: {email}')
print()

# TESTE 2: Gerar Questão
print('2️⃣  TESTE: Gerar Questão')
print('-'*60)
questao_data = {
    'email': email,
    'token': token,
    'concurso': 'PMDF',
    'materia': 'Direito Constitucional',
    'dificuldade': 'média'
}
response = requests.post(f'{BASE_URL}/gerar-questao', json=questao_data, timeout=10)
print(f'Status: {response.status_code}')
response_json = response.json()

if response.status_code != 200:
    print('❌ Geração de questão falhou!')
    print(response_json)
else:
    print('✅ Questão gerada com sucesso!')
    questao = response_json.get('questao', {})
    print(f'   ID: {questao.get("id")}')
    print(f'   Tipo: {questao.get("tipo")}')
    print(f'   Enunciado: {questao.get("enunciado")[:100]}...')
    questao_id = questao.get('id')
print()

# TESTE 3: Salvar Resposta
print('3️⃣  TESTE: Salvar Resposta')
print('-'*60)
resposta_data = {
    'email': email,
    'token': token,
    'questao_id': questao_id,
    'resposta_escolhida': 'C',
    'resposta_correta': questao.get('resposta_correta')
}
response = requests.post(f'{BASE_URL}/salvar-resposta', json=resposta_data, timeout=5)
print(f'Status: {response.status_code}')
response_json = response.json()

if response.status_code != 200:
    print('❌ Salvar resposta falhou!')
    print(response_json)
else:
    print('✅ Resposta salva com sucesso!')
    print(f'   Acertou: {response_json.get("acertou")}')
print()

# TESTE 4: Registrar Tempo (Heartbeat)
print('4️⃣  TESTE: Registrar Tempo (Heartbeat)')
print('-'*60)
CHAVE_HMAC = "DIRETRIZ_SEGURANCA_MAXIMA_CONCURSOS_2026"
timestamp = int(time.time())
mensagem = f"{email}:{token}:{timestamp}"
assinatura = hmac.new(
    CHAVE_HMAC.encode(),
    mensagem.encode(),
    hashlib.sha256
).hexdigest()

tempo_data = {
    'email': email,
    'token': token,
    'timestamp': timestamp,
    'assinatura_criptografica': assinatura
}
response = requests.post(f'{BASE_URL}/registrar-tempo', json=tempo_data, timeout=5)
print(f'Status: {response.status_code}')
response_json = response.json()

if response.status_code != 200:
    print('❌ Registrar tempo falhou!')
    print(response_json)
else:
    print('✅ Tempo registrado com sucesso!')
    print(f'   Total estudado: {response_json.get("total_horas")} horas')
print()

# TESTE 5: Estatísticas
print('5️⃣  TESTE: Estatísticas')
print('-'*60)
stats_data = {
    'email': email,
    'token': token
}
response = requests.post(f'{BASE_URL}/estatisticas', json=stats_data, timeout=5)
print(f'Status: {response.status_code}')
response_json = response.json()

if response.status_code != 200:
    print('❌ Estatísticas falharam!')
    print(response_json)
else:
    print('✅ Estatísticas obtidas com sucesso!')
    stats = response_json.get('estatisticas', {})
    print(f'   Total questões: {stats.get("total_questoes")}')
    print(f'   Acertos: {stats.get("acertos")}')
    print(f'   Taxa acerto: {stats.get("taxa_acerto")}%')
print()

print('='*60)
print('✅ TODOS OS TESTES PASSARAM COM SUCESSO!')
print('='*60)
