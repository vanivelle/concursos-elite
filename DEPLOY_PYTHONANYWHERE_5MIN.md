# 🚀 DEPLOY PYTHONANYWHERE (5 MIN) - PASSO A PASSO

## ⚡ QUICK START

### Passo 1: Criar Conta (2 min)
```
1. Acesse: https://www.pythonanywhere.com/pricing/
2. Click "Create a Beginner account" (FREE)
3. Email: seu_email@gmail.com
4. Username: seu_usuario (vai ser seu domínio: seu_usuario.pythonanywhere.com)
5. Confirme email
```

### Passo 2: Upload Código (1 min)
```
Em PythonAnywhere → Bash Console:

cd ~
git clone https://github.com/vanivelle/concursos-elite.git
cd concurso-elite
pip install --user -r requirements.txt
```

### Passo 3: Configurar Web App (1 min)

**Em PythonAnywhere Web Tab:**

1. Click "+ Add a new web app"
2. Escolha: **Python 3.11** → **FastAPI**
3. Será criado automático

### Passo 4: Editar WSGI (1 min)

**File** → `/var/www/seu_usuario_pythonanywhere_com_wsgi.py`

**Substitua TUDO por:**

```python
import sys
import os

# Adicione path
path = '/home/seu_usuario/concurso-elite/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Database URL
os.environ['DATABASE_URL'] = 'postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres'

# Import app
from main_supabase import app as application
```

### Passo 5: Configurar Environment Variables (30 seg)

**Web** → **Environment variables:**

```
DATABASE_URL = postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres
PYTHONUNBUFFERED = 1
```

### Passo 6: Reload (5 seg)

**Web** → Click "Reload" (botão verde grande)

### ✅ PRONTO!

**URL DO APP:**
```
https://seu_usuario.pythonanywhere.com
```

**Testar:**
```
https://seu_usuario.pythonanywhere.com/health
```

---

## 📱 ACESSAR NO MOBILE

### iPhone (Matheus)
```
https://seu_usuario.pythonanywhere.com
Login: matheus@email.com / matheus123
```

### Android (Cabo)
```
https://seu_usuario.pythonanywhere.com
Login: cabo.md@email.com / cabo123
```

---

## ❌ TROUBLESHOOTING

**Erro 502 Bad Gateway?**
- Bash: `pip install --user fastapi uvicorn psycopg2-binary pydantic`
- Web: Reload

**Database connection refused?**
- Confirma DATABASE_URL em Environment variables
- Testa conexão no Bash: `python -c "import psycopg2; psycopg2.connect('postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres')"`

**Endpoint retorna 404?**
- Verifica se main_supabase.py está no path correto
- Reload web app

---

## 🎯 TEMPO TOTAL

- Criar conta: 2 min
- Upload: 1 min
- Config: 1.5 min
- **TOTAL: 4.5 min** ✅

**Status**: Pronto pra Matheus e Cabo usarem do celular
