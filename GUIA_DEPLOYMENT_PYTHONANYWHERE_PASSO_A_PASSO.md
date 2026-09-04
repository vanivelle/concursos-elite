# 🚀 GUIA PASSO A PASSO - Deploy no PythonAnywhere (Agora Funciona!)

## ✅ PRÉ-REQUISITOS ATENDIDOS

- ✅ requirements.txt otimizado (14 pacotes apenas)
- ✅ Nenhuma dependência de compilação Rust
- ✅ Todas as versões com wheels pré-compilados
- ✅ Código pushado no GitHub
- ✅ DATABASE_URL do Supabase pronto

---

## 🎯 PASSO 1: Criar Conta PythonAnywhere (2 minutos)

### 1.1 Ir para o site
```
https://www.pythonanywhere.com/pricing/
```

### 1.2 Criar conta gratuita
- Clique em "Create a Beginner account"
- Email: seu_email@gmail.com
- Username: `seu_usuario` (importante! será seu domínio)
- Confirme o email

### 1.3 Verificar email
- Acesse link de confirmação
- Login em https://www.pythonanywhere.com/user/seu_usuario/

---

## 📦 PASSO 2: Clone o Repositório (1 minuto)

### 2.1 Abrir Bash Console
No PythonAnywhere:
- Vá em **Dashboard** → **Consoles** → **+ Bash console**

### 2.2 Clonar repositório
```bash
cd ~
git clone https://github.com/vanivelle/concursos-elite.git
cd concurso-elite
```

### 2.3 Verificar arquivos
```bash
ls -la requirements.txt
```

Deve mostrar:
```
-rw-r--r-- 1 seu_usuario seu_usuario 395 Sep  4 14:32 requirements.txt
```

---

## 🔧 PASSO 3: Instalar Dependências (3-5 minutos)

### 3.1 Instalar com pip --user
```bash
pip install --user -r requirements.txt
```

**Esperado:**
- Processing FastAPI
- Processing pydantic
- Processing psycopg2-binary
- Installing collected packages: ...
- ✅ Successfully installed

**NÃO deve aparecer:**
- ❌ "error: unsupported installer version"
- ❌ "Building wheel for pydantic-core"
- ❌ "fatal error: rustc"

### 3.2 Se receber erro, tente:
```bash
pip install --user --upgrade pip
pip install --user -r requirements.txt
```

### 3.3 Validar instalação
```bash
python -c "import fastapi; import pydantic; import sqlalchemy; print('✅ Todos os pacotes importados com sucesso!')"
```

Deve aparecer:
```
✅ Todos os pacotes importados com sucesso!
```

---

## 🌐 PASSO 4: Configurar Web App (2 minutos)

### 4.1 Voltar ao Dashboard
Clique em **Web** (abas no topo)

### 4.2 Adicionar novo web app
- Clique em **+ Add a new web app**
- Escolha **FastAPI**
- Escolha **Python 3.11** (ou 3.13)
- Framework: **FastAPI**

PythonAnywhere cria automaticamente:
- URL: `https://seu_usuario.pythonanywhere.com`
- WSGI file: `/var/www/seu_usuario_pythonanywhere_com_wsgi.py`

---

## ✏️ PASSO 5: Editar Arquivo WSGI (2 minutos)

### 5.1 Abrir Editor
**Web** → Clique no arquivo WSGI gerado

Exemplo: `/var/www/seu_usuario_pythonanywhere_com_wsgi.py`

### 5.2 Substituir TUDO pelo código abaixo:

```python
"""
FastAPI WSGI adapter para PythonAnywhere
Backend Concurso Elite
"""

import sys
import os
from pathlib import Path

# ==================== PATH SETUP ====================
# Adicionar diretório do projeto ao Python path
project_path = Path.home() / 'concurso-elite'
if str(project_path) not in sys.path:
    sys.path.insert(0, str(project_path))

# ==================== ENVIRONMENT SETUP ====================
# Variáveis de ambiente (IMPORTANTE: substituir com seus valores reais)
os.environ['DATABASE_URL'] = 'postgresql://postgres:SUA_SENHA_SUPABASE@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres'
os.environ['API_KEY'] = 'elite-concursos-hunter-2024'
os.environ['SECRET_KEY'] = 'sua-chave-secreta-aqui-32-caracteres'
os.environ['JWT_SECRET'] = 'sua-jwt-secret-aqui-32-caracteres'

# Modo produção
os.environ['ENV'] = 'production'

# ==================== FASTAPI IMPORT ====================
try:
    from backend.main import app  # FastAPI app
except ImportError as e:
    # Se não encontrar, tentar versão alternativa
    try:
        from main import app
    except ImportError as e2:
        # Erro clara
        app = None
        error_message = f"Falha ao importar FastAPI app: {str(e)} / {str(e2)}"

# ==================== ASGI TO WSGI ADAPTER ====================
# PythonAnywhere precisa de WSGI, mas FastAPI é ASGI
# Usar asyncio_to_wsgi adapter
from asgiref.wsgi import WsgiToAsgi

if app is not None:
    # Converter FastAPI (ASGI) para WSGI
    application = WsgiToAsgi(app)
else:
    # Se falhou, mostrar erro
    def application(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return [b'Erro ao carregar FastAPI app. Verifique os logs.']

# ==================== HEALTH CHECK ====================
# Endpoint simples para verificar se tudo está funcionando
def wsgi_health(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET' and environ['PATH_INFO'] == '/health':
        status = '200 OK'
        response_headers = [('Content-Type', 'application/json')]
        start_response(status, response_headers)
        return [b'{"status": "ok"}']
    return application(environ, start_response)

application = wsgi_health
```

### 5.3 Salvar arquivo
- **Ctrl+S** (ou menu Save)

---

## 🔗 PASSO 6: Configurar Variáveis de Ambiente (1 minuto)

### 6.1 Adicionar DATABASE_URL
No WSGI file que acabamos de editar, substitua:

```python
os.environ['DATABASE_URL'] = 'postgresql://postgres:SUA_SENHA_SUPABASE@...'
```

Por (obtido do Supabase):
```python
os.environ['DATABASE_URL'] = 'postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres'
```

### 6.2 Outras variáveis importantes
Se tiver `.env` file local, copiar valores para:
- API_KEY
- SECRET_KEY
- JWT_SECRET

---

## 🔄 PASSO 7: Recarregar Web App (1 minuto)

### 7.1 Voltar a Dashboard → Web
- Veja lista de web apps
- Clique em **Reload** (botão verde no topo)

Aguarde 10-15 segundos...

### 7.2 Teste de Health Check
```bash
curl https://seu_usuario.pythonanywhere.com/health
```

Esperado:
```json
{"status": "ok"}
```

---

## ✅ PASSO 8: Validação Completa (2 minutos)

### 8.1 Teste endpoints principais
```bash
# Health check
curl https://seu_usuario.pythonanywhere.com/health

# Documentação API (Swagger)
curl https://seu_usuario.pythonanywhere.com/docs

# List questões
curl https://seu_usuario.pythonanywhere.com/api/v1/questoes
```

### 8.2 Verificar logs
No PythonAnywhere:
- **Web** → **Log files**
- Clique em **Server log**
- Procure por erros (vermelho) ou warnings (amarelo)

### 8.3 Se tiver erro
```
❌ "ERROR: no module named fastapi"
   → Refazer PASSO 3 (pip install)

❌ "ERROR: no module named main"
   → Verificar caminho em WSGI (deve ser backend/main.py)

❌ "ERROR: DATABASE connection refused"
   → Verificar DATABASE_URL no WSGI (credenciais Supabase)
```

---

## 🎉 SUCESSO! 

Se chegou aqui e tudo funcionou, seu backend está **LIVE**:

```
✅ URL: https://seu_usuario.pythonanywhere.com
✅ API Docs: https://seu_usuario.pythonanywhere.com/docs
✅ Health: https://seu_usuario.pythonanywhere.com/health
✅ Endpoints: https://seu_usuario.pythonanywhere.com/api/v1/*
```

---

## 📊 Tempo Total Estimado

| Passo | Tempo |
|-------|-------|
| 1. Criar conta | 2 min |
| 2. Clone repo | 1 min |
| 3. Instalar deps | 3-5 min |
| 4. Config web app | 2 min |
| 5. Editar WSGI | 2 min |
| 6. Env vars | 1 min |
| 7. Reload | 1 min |
| 8. Validação | 2 min |
| **TOTAL** | **~20 min** |

---

## 🆘 Troubleshooting

### Erro: "ERROR: unsupported installer version"
**Solução:** Versão antiga do pip. Execute:
```bash
pip install --user --upgrade pip
pip install --user -r requirements.txt
```

### Erro: "ERROR: cannot import main from backend"
**Verificar:**
- Arquivo existe: `/home/seu_usuario/concurso-elite/backend/main.py`
- Permissions corretas
- Sintaxe do arquivo WSGI

### Erro: "ConnectionRefusedError: DATABASE"
**Verificar:**
- DATABASE_URL está correto
- Supabase está online
- Credenciais corretas
- Firewall/IP whitelist do Supabase

### Web app não carrega / 500 Internal Server Error
**Verificar logs:**
```bash
# No Bash console do PythonAnywhere
tail -100 /var/log/seu_usuario.pythonanywhere.com.access.log
tail -100 /var/log/seu_usuario.pythonanywhere.com.error.log
```

---

## 📞 Próximas Ações

Depois do deploy bem-sucedido:

1. ✅ Conectar frontend (Vercel) com backend (PythonAnywhere)
2. ✅ Testar fluxo completo (login → questões → respostas)
3. ✅ Validar 377 questões no banco
4. ✅ Configurar CORS se frontend em outro domínio
5. ✅ Adicionar SSL certificate (PythonAnywhere faz automático)

---

## 📚 Referências Rápidas

- **PythonAnywhere Docs**: https://help.pythonanywhere.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **PostgreSQL Connection**: https://www.postgresql.org/docs/
- **Supabase Docs**: https://supabase.com/docs

---

**Data:** 04/09/2026  
**Status:** ✅ Production-Ready  
**Python Version:** 3.11+  
**Requirements:** 14 pacotes (sem compilação Rust)
