# 🚀 DEPLOY CONCURSOELITE - GUIA EXECUÇÃO

**Status**: Pronto para ir ao ar  
**URL Final**: https://concursoelite.pythonanywhere.com  
**Tempo**: 5-10 minutos  

---

## PASSO 1: Bash Console (2 minutos)

**Você está aqui:**
https://www.pythonanywhere.com/user/concursoelite/

**Próximo:**
1. Click em **"Consoles"** no topo (lado esquerdo)
2. Click em **"+ New console"** → **"Bash"**
3. Aguarde terminal abrir

**Copie TODO este código:**

```bash
#!/bin/bash
# Execute these commands in PythonAnywhere Bash Console

set -e

cd ~

# Clone repository
if [ ! -d "concursos-elite" ]; then
    echo "Clonando repositorio..."
    git clone https://github.com/vanivelle/concursos-elite.git
    cd concursos-elite
else
    echo "Atualizando repositorio..."
    cd concursos-elite
    git pull origin main
fi

# Install dependencies
echo "Instalando dependencias..."
pip install --user -r requirements.txt

# Create .env
echo "Configurando ambiente..."
cat > .env << 'EOF'
DATABASE_URL=postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres
SECRET_KEY=super-secret-key-min-32-chars-xyz123
CORS_ORIGINS=https://open-notebook-8x8twkj23.vercel.app,https://concursoelite.pythonanywhere.com
ENVIRONMENT=production
DEBUG=false
PYTHONUNBUFFERED=1
EOF

# Test database connection
echo "Testando conexao com banco..."
python3 << 'PYEOF'
import os
import psycopg2
db_url = os.getenv('DATABASE_URL')
try:
    conn = psycopg2.connect(db_url, connect_timeout=5)
    print("Database connection OK")
    conn.close()
except Exception as e:
    print(f"Database connection FAILED: {e}")
    exit(1)
PYEOF

echo "DEPLOYMENT CONCLUIDO!"
```

**Cole no terminal e aguarde** ~2-3 minutos

Esperado ver:
```
Clonando repositorio...
Instalando dependencias...
Configurando ambiente...
Testando conexao com banco...
Database connection OK
DEPLOYMENT CONCLUIDO!
```

---

## PASSO 2: Web App Configuration (2 minutos)

**Próximo:**
1. Click em **"Web"** (no menu topo)
2. Click em **"+ Add a new web app"**
3. Escolha **"Python 3.11"** → **"FastAPI"**
4. Confirme

Vai aparecer uma URL como:
```
https://concursoelite.pythonanywhere.com
```

---

## PASSO 3: WSGI File (1 minuto)

**Ainda em Web:**
1. Procure por "WSGI configuration file"
2. Click no link que aparece (tipo `/var/www/concursoelite_pythonanywhere_com_wsgi.py`)
3. **Apague TUDO** que tem lá
4. **Cole TODO isto:**

```python
# WSGI CONFIGURATION FOR PYTHONANYWHERE
# Copy and paste this content to:
# https://www.pythonanywhere.com/user/concursoelite/webapps/
# Edit WSGI file -> /var/www/concursoelite_pythonanywhere_com_wsgi.py

import sys
import os
from pathlib import Path

# Environment variables
os.environ['DATABASE_URL'] = '''postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres'''
os.environ['SECRET_KEY'] = '''super-secret-key-min-32-chars-xyz123'''
os.environ['CORS_ORIGINS'] = 'https://open-notebook-8x8twkj23.vercel.app,https://concursoelite.pythonanywhere.com'
os.environ['PYTHONUNBUFFERED'] = '1'

# Path configuration
home = Path.home()
project_path = home / 'concursos-elite'
backend_path = str(project_path / 'backend')

if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import FastAPI app
from main_supabase import app as application
```

5. Click em **"Save"** (botão verde)

---

## PASSO 4: Reload (30 segundos)

**Volta para Web:**
1. Você verá seu web app: `concursoelite.pythonanywhere.com`
2. Click no botão verde **"Reload"** (lado direito)
3. Aguarde 10-15 segundos
4. Verifique o status (deve ficar verde = "Online")

---

## PASSO 5: Testar (1 minuto)

**No seu navegador, acesse:**
```
https://concursoelite.pythonanywhere.com/health
```

**Esperado ver:**
```json
{
  "status": "OK",
  "database": "Online",
  "version": "3.3.0",
  "timestamp": "2026-09-04T..."
}
```

---

## PASSO 6: Frontend Update (2 minutos)

**No seu PC:**

1. Abra `frontend/index.html` (linha ~1170)
2. Mude:
   ```javascript
   // ANTES:
   const API = "http://localhost:8000"
   
   // DEPOIS:
   const API = "https://concursoelite.pythonanywhere.com"
   ```

3. Salve e faça push:
   ```bash
   git add frontend/index.html
   git commit -m "Update API to production"
   git push
   ```

(Vercel auto-redeploy em ~1 minuto)

---

## ✅ PRONTO!

Seu app está live em:
```
https://concursoelite.pythonanywhere.com
```

### Testar no Celular:
- iPhone: Abra Safari e acesse `https://concursoelite.pythonanywhere.com`
- Android: Abra Chrome e acesse `https://concursoelite.pythonanywhere.com`

### Logins de Teste:
1. **Admin** (Valparaíso - 500m):
   - Email: `mr.dblucas@gmail.com`
   - Senha: `Lightshigaraki789`

2. **Cabo** (Plano Piloto - 2km):
   - Email: `cabo.md@email.com`
   - Senha: `cabo123`

3. **Matheus** (Gama - 1km):
   - Email: `matheus@email.com`
   - Senha: `matheus123`

---

## 🆘 Se Algo Falhar

### Erro: "Database connection FAILED"
- Verificar DATABASE_URL em .env
- Confirmar Supabase online: https://app.supabase.com

### Erro: "ModuleNotFoundError"
- Rodar Bash console novamente
- Garantir que `pip install --user -r requirements.txt` completou sem erro

### Web app mostra erro 500
- Verificar Web → Log files → Error log
- Garantir WSGI file foi copiado corretamente (sem truncar)

---

**Próximo passo:** Executar Bash commands no Passo 1 👆
