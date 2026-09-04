# 🚀 SETUP PYTHONANYWHERE (5 MIN)

## PASSO 1: Criar Conta
1. Vá para: https://www.pythonanywhere.com/
2. Click "Create Account" 
3. Escolha username (ex: `concurso-elite`)
4. Use email: `mr.dblucas@gmail.com`
5. Confirme email

## PASSO 2: Upload do Código
1. Em PythonAnywhere → "Files"
2. Upload ZIP:
   - backend/main.py
   - backend/main_supabase.py
   - requirements.txt
   - .env (com DATABASE_URL)

**OU via Git:**
```bash
cd ~
git clone https://github.com/vanivelle/concursos-elite.git
cd concurso-elite
```

## PASSO 3: Criar Web App

1. **Web** → **Add a new web app**
2. Escolha: **Python 3.11** → **FastAPI**
3. PythonAnywhere gera wsgi_file automaticamente

## PASSO 4: Configurar WSGI

**Edit wsgi file:** `/var/www/concursoelite_pythonanywhere_com_wsgi.py`

```python
# WSGI configuration for FastAPI
import sys
import os

# Adicionar caminho do backend
path = '/home/concurso-elite/concurso-elite/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Importar app
from main_supabase import app as application

# Variável de ambiente
os.environ['DATABASE_URL'] = 'postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres'
```

## PASSO 5: Configurar Ambiente

**Web → Environment variables:**
```
DATABASE_URL=postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres
CORS_ORIGINS=https://open-notebook-8x8twkj23.vercel.app,https://concurso-elite.pythonanywhere.com,http://localhost:3000
PYTHONUNBUFFERED=1
```

## PASSO 6: Instalar Dependências

**Bash console em PythonAnywhere:**
```bash
cd /home/concurso-elite/concurso-elite
pip install --user -r requirements.txt
```

## PASSO 7: Reload

**Web → Reload** (botão verde)

## ✅ PRONTO!

**Seu backend estará em:**
```
https://concurso-elite.pythonanywhere.com
```

**Endpoints:**
- Health: https://concurso-elite.pythonanywhere.com/health
- Login: https://concurso-elite.pythonanywhere.com/api/auth/login-novo
- Status: https://concurso-elite.pythonanywhere.com/api/auth/status/mr.dblucas@gmail.com

---

## TESTAR NO MOBILE

### Frontend (já online em Vercel):
```
https://open-notebook-8x8twkj23.vercel.app
```

### Abra em qualquer navegador mobile e:
1. Email: mr.dblucas@gmail.com
2. Senha: Lightshigaraki789
3. Locação: Valparaíso

✅ **Funciona em qualquer device/lugar**
