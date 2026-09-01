import requests
import time

API = 'http://localhost:8000'
email = 'candidato_elite@bacen.gov.br'
senha = 'seguranca2026'

print('🏛️ TESTE DE FLUXO ELITE')
print('=' * 60)

# 1. Cadastro
print('\n1️⃣ CADASTRANDO...')
r = requests.post(f'{API}/cadastro', json={'email': email, 'senha': senha, 'nome': 'Fiscal Bacen'})
print(f'   Status: {r.status_code}')

# 2. Login
print('\n2️⃣ FAZENDO LOGIN...')
r = requests.post(f'{API}/login', json={'email': email, 'senha': senha})
data = r.json()
token = data['token']
print(f'   Status: {r.status_code}')
print(f'   Token: {token[:30]}...')

# 3. Gerar questão (INSTANTÂNEA - medir tempo)
print('\n3️⃣ GERANDO QUESTÃO (medindo latência)...')
payload = {
    'email': email,
    'token': token,
    'concurso': 'Banco Central (Bacen)',
    'materia': 'Português',
    'dificuldade': 'Fácil'
}

inicio = time.time()
r = requests.post(f'{API}/gerar-questao', json=payload)
latencia = (time.time() - inicio) * 1000

quest = r.json()
print(f'   Status: {r.status_code}')
print(f'   Latência: {latencia:.2f}ms')
print(f'   Tipo: {quest.get("tipo")}')
print(f'   Enunciado: {quest.get("enunciado")[:60]}...')

print('\n' + '=' * 60)
print('✅ SISTEMA ELITE OPERACIONAL')
print(f'   Resposta em {latencia:.1f}ms (objetivo: <100ms)')
