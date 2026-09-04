#!/usr/bin/env python3
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

users = [
    {"name": "👤 ADMIN (mr.dblucas)", "email": "mr.dblucas@gmail.com", "password": "Lightshigaraki789"},
    {"name": "👤 CABO (cabo.md)", "email": "cabo.md@email.com", "password": "cabo123"},
    {"name": "👤 MATHEUS (matheus)", "email": "matheus@email.com", "password": "matheus123"},
]

print("\n" + "="*70)
print("🔐 TESTE DE LOGINS - CONCURSO ELITE")
print("="*70)
print(f"Testando em: {BASE_URL}")
print(f"Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

for i, user in enumerate(users, 1):
    print(f"\n{i}️⃣  {user['name']}")
    print("-" * 70)
    
    try:
        payload = {
            "email": user["email"],
            "password": user["password"],
            "latitude": -15.7942,
            "longitude": -47.8822
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/login-novo",
            json=payload,
            timeout=10
        )
        
        data = response.json()
        
        status_code = response.status_code
        token = data.get("access_token", "")
        email = data.get("email", "")
        
        # Mostrar resultado
        if status_code == 200 and token:
            print(f"✅ STATUS: {status_code} - SUCESSO")
            print(f"📧 EMAIL: {email}")
            print(f"🔑 TOKEN: {token[:50]}...")
            print(f"✨ Login funcionando perfeitamente!")
        else:
            print(f"❌ STATUS: {status_code} - ERRO")
            print(f"💬 Resposta: {data}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ ERRO: Não conseguiu conectar em {BASE_URL}")
        print("   Certifique-se que o backend está rodando: uvicorn backend.main_enterprise:app --reload")
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")

print("\n" + "="*70)
print("✅ TESTE CONCLUÍDO")
print("="*70 + "\n")
