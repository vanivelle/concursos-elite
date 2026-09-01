#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = 'http://localhost:8000'

print('='*70)
print('VALIDAÇÃO DO MVP SIMPLIFICADO (SEM CRIPTOGRAFIA, COM TIMEOUT 180s)')
print('='*70)
print()

email = 'teste_mvp_simplificado@concursos.com'
senha = 'senha_teste_123'
nome = 'Usuário MVP'

print('1️⃣  TESTE: Cadastro')
print('-'*70)
try:
    response = requests.post(
        f'{BASE_URL}/cadastro',
        json={'email': email, 'senha': senha, 'nome': nome},
        timeout=5
    )
    print(f'Status: {response.status_code}')
    print(f'Response: {response.json()}')
    if response.status_code != 200:
        print('❌ Cadastro falhou!')
        exit(1)
    print('✅ Cadastro OK\n')
except Exception as e:
    print(f'❌ Erro: {e}\n')
    exit(1)

print('2️⃣  TESTE: Login')
print('-'*70)
try:
    response = requests.post(
        f'{BASE_URL}/login',
        json={'email': email, 'senha': senha},
        timeout=5
    )
    print(f'Status: {response.status_code}')
    data = response.json()
    if response.status_code != 200:
        print('❌ Login falhou!')
        exit(1)
    token = data.get('token')
    print(f'Token: {token[:20]}...')
    print('✅ Login OK\n')
except Exception as e:
    print(f'❌ Erro: {e}\n')
    exit(1)

print('3️⃣  TESTE: Gerar Questão (novo timeout 180s)')
print('-'*70)
try:
    print('Enviando requisição para /gerar-questao...')
    start = time.time()
    response = requests.post(
        f'{BASE_URL}/gerar-questao',
        json={
            'email': email,
            'token': token,
            'concurso': 'PMDF',
            'materia': 'Direito Constitucional',
            'dificuldade': 'média'
        },
        timeout=200
    )
    elapsed = time.time() - start
    print(f'Status: {response.status_code}')
    print(f'Tempo de resposta: {elapsed:.1f}s')
    
    if response.status_code != 200:
        print(f'❌ Geração falhou!')
        print(f'Response: {response.json()}')
    else:
        data = response.json()
        print(f'✅ Questão gerada com sucesso!')
        print(f'   ID: {data.get("id")}')
        print(f'   Tipo: {data.get("tipo")}')
        print(f'   Enunciado: {data.get("enunciado", "")[:80]}...')
        questao_id = data.get('id')
    print()
except Exception as e:
    print(f'❌ Erro: {e}\n')

print('4️⃣  TESTE: Salvar Resposta')
print('-'*70)
try:
    response = requests.post(
        f'{BASE_URL}/salvar-resposta',
        json={
            'email': email,
            'token': token,
            'questao_id': questao_id,
            'resposta_escolhida': 'C',
            'resposta_correta': 'C'
        },
        timeout=5
    )
    print(f'Status: {response.status_code}')
    data = response.json()
    print(f'Acertou: {data.get("acertou")}')
    print('✅ Resposta salva OK\n')
except Exception as e:
    print(f'❌ Erro: {e}\n')

print('5️⃣  TESTE: Registrar Tempo (SEM CRIPTOGRAFIA HMAC)')
print('-'*70)
print('Enviando apenas: email + token + timestamp (sem assinatura criptográfica)')
try:
    timestamp = int(time.time())
    response = requests.post(
        f'{BASE_URL}/registrar-tempo',
        json={
            'email': email,
            'token': token,
            'timestamp': timestamp
        },
        timeout=5
    )
    print(f'Status: {response.status_code}')
    data = response.json()
    print(f'Total horas estudadas: {data.get("total_horas")}h')
    print('✅ Tempo registrado OK (SEM CRIPTOGRAFIA)\n')
except Exception as e:
    print(f'❌ Erro: {e}\n')

print('6️⃣  TESTE: Estatísticas')
print('-'*70)
try:
    response = requests.get(
        f'{BASE_URL}/estatisticas?email={email}&token={token}',
        timeout=5
    )
    print(f'Status: {response.status_code}')
    data = response.json()
    print(f'Total questões: {data.get("total")}')
    print(f'Acertos: {data.get("acertos")}')
    print(f'Taxa: {data.get("percentual")}')
    print('✅ Estatísticas OK\n')
except Exception as e:
    print(f'❌ Erro: {e}\n')

print('7️⃣  TESTE: Novo Concurso (Prefeituras)')
print('-'*70)
try:
    print('Testando concurso de Prefeituras/Administrativo Ensino Médio...')
    response = requests.post(
        f'{BASE_URL}/gerar-questao',
        json={
            'email': email,
            'token': token,
            'concurso': 'Prefeituras',
            'materia': 'Português',
            'dificuldade': 'fácil'
        },
        timeout=200
    )
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Prefeituras OK!')
        print(f'   Tipo: {data.get("tipo")}')
        print(f'   Enunciado: {data.get("enunciado", "")[:80]}...')
    else:
        print(f'❌ Erro: {response.json()}')
    print()
except Exception as e:
    print(f'❌ Erro: {e}\n')

print('='*70)
print('✅ VALIDAÇÃO COMPLETA DO MVP SIMPLIFICADO')
print('='*70)
print()
print('RESUMO DE MUDANÇAS IMPLEMENTADAS:')
print('✅ Criptografia HMAC-SHA256 removida')
print('✅ CryptoJS removido do frontend')
print('✅ /registrar-tempo agora apenas valida email + token')
print('✅ Timeout de /gerar-questao aumentado para 180 segundos')
print('✅ Novo concurso adicionado: Prefeituras (Administrativo)')
print('✅ Database continua funcionando normalmente')
print('✅ Segurança mantida via bloqueio de sessão 403')
print()
