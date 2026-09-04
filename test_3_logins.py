#!/usr/bin/env python3
"""
Teste de los 3 logins - Validação Final
"""
import requests
import json
from datetime import datetime

print(f"\n{'='*70}")
print(f"🧪 TESTE DOS 3 LOGINS - {datetime.now().strftime('%H:%M:%S')}")
print(f"{'='*70}\n")

backend = "http://localhost:8000"
users = [
    {"email": "mr.dblucas@gmail.com", "password": "Lightshigaraki789", "name": "Admin", "lat": -15.8268, "lon": -48.0409},
    {"email": "cabo.md@email.com", "password": "cabo123", "name": "Cabo", "lat": -15.8268, "lon": -48.0409},
    {"email": "matheus@email.com", "password": "matheus123", "name": "Motoboy", "lat": -15.8500, "lon": -48.0600}
]

print("📝 Health Check:")
try:
    r = requests.get(f"{backend}/health", timeout=5)
    print(f"   ✅ Backend respondendo: {r.json()}\n")
except Exception as e:
    print(f"   ❌ Backend NÃO responde: {e}\n")
    exit(1)

results = []
for i, user in enumerate(users, 1):
    print(f"{i}️⃣  USUÁRIO: {user['name']}")
    print(f"   Email: {user['email']}")
    print(f"   Localização: ({user['lat']}, {user['lon']})")
    
    try:
        r = requests.post(
            f"{backend}/api/auth/login-novo",
            json={
                "email": user['email'],
                "password": user['password'],
                "latitude": user['lat'],
                "longitude": user['lon']
            },
            timeout=5
        )
        
        if r.status_code == 200:
            data = r.json()
            print(f"   ✅ LOGIN SUCESSO")
            print(f"   Status: {data.get('status')}")
            print(f"   Token: {data.get('access_token')[:30]}...")
            print(f"   Message: {data.get('message')}")
            results.append(True)
        else:
            print(f"   ❌ FALHA - Status {r.status_code}")
            print(f"   Response: {r.json()}")
            results.append(False)
    except Exception as e:
        print(f"   ❌ ERRO: {e}")
        results.append(False)
    
    print()

print(f"{'='*70}")
if all(results):
    print(f"✅ TODOS 3 LOGINS TESTADOS COM SUCESSO!")
else:
    print(f"⚠️  {sum(results)}/3 logins funcionam")
print(f"{'='*70}\n")
