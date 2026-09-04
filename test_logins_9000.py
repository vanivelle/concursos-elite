#!/usr/bin/env python3
import requests

backend = 'http://localhost:9000'
users = [
    {'email': 'mr.dblucas@gmail.com', 'password': 'Lightshigaraki789', 'name': 'Admin', 'lat': -15.8268, 'lon': -48.0409},
    {'email': 'cabo.md@email.com', 'password': 'cabo123', 'name': 'Cabo', 'lat': -15.8268, 'lon': -48.0409},
    {'email': 'matheus@email.com', 'password': 'matheus123', 'name': 'Motoboy', 'lat': -15.8500, 'lon': -48.0600}
]

print('\n' + '='*70)
print('🧪 TESTE DOS 3 LOGINS - PORTA 9000')
print('='*70 + '\n')

for i, u in enumerate(users, 1):
    try:
        r = requests.post(f'{backend}/api/auth/login-novo', 
            json={'email': u['email'], 'password': u['password'], 'latitude': u['lat'], 'longitude': u['lon']},
            timeout=5)
        status = '✅ OK' if r.status_code == 200 else f'❌ ERRO {r.status_code}'
        print(f'{i}. {u["name"]} ({u["email"]}) ... {status}')
    except Exception as e:
        print(f'{i}. {u["name"]} ({u["email"]}) ... ❌ {str(e)[:50]}')

print('\n' + '='*70)
