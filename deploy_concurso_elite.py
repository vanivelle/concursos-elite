#!/usr/bin/env python3
"""
🚀 DEPLOYMENT AUTOMÁTICO - Concurso Elite no PythonAnywhere
USO: python deploy_concurso_elite.py <username> <database_url> <secret_key>

Exemplo:
  python deploy_concurso_elite.py my-user \
    "postgresql://postgres:...@db....supabase.co:5432/postgres" \
    "my-super-secret-key-123"
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

# ============ COLOR CODES ============
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(title):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}  {title:<66}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_step(step_num, title):
    print(f"\n{Colors.OKBLUE}[STEP {step_num}] {title}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'-'*70}{Colors.ENDC}")

def print_ok(msg):
    print(f"{Colors.OKGREEN}[OK] {msg}{Colors.ENDC}")

def print_warn(msg):
    print(f"{Colors.WARNING}[WARN] {msg}{Colors.ENDC}")

def print_fail(msg):
    print(f"{Colors.FAIL}[ERROR] {msg}{Colors.ENDC}")

def run_cmd(cmd, check=True):
    """Executa comando e retorna sucesso/erro"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print_fail(f"Command failed: {cmd}")
        print_fail(f"Error: {result.stderr}")
        return None
    return result.stdout.strip()

def main():
    if len(sys.argv) < 4:
        print("""
USAGE:
  python deploy_concurso_elite.py <username> <database_url> <secret_key>

EXAMPLE:
  python deploy_concurso_elite.py my-username \\
    "postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres" \\
    "my-secret-key-12345"

NOTES:
  - username: Seu username no PythonAnywhere
  - database_url: Connection string do Supabase (com senha!)
  - secret_key: Gere uma chave segura (min 32 caracteres)
        """)
        sys.exit(1)
    
    username = sys.argv[1]
    database_url = sys.argv[2]
    secret_key = sys.argv[3]
    
    print_header(f"CONCURSO ELITE - DEPLOYMENT AUTOMATIZADO")
    
    print(f"""
Configuracao:
  Username: {username}
  Database: {database_url[:50]}...
  Secret Key: {'*' * 30}
  Timestamp: {datetime.now().isoformat()}
    """)
    
    # ============ STEP 1: Validar arquivos locais ============
    print_step(1, "Validando arquivos locais")
    
    required_files = {
        "backend/main_supabase.py": "Backend principal",
        "backend/geofencing.py": "Módulo de geofencing",
        "requirements.txt": "Dependências",
        "wsgi_pythonanywhere.py": "WSGI wrapper",
    }
    
    missing = []
    for file, desc in required_files.items():
        if os.path.exists(file):
            print_ok(f"{file} ({desc})")
        else:
            print_fail(f"{file} ({desc})")
            missing.append(file)
    
    if missing:
        print_fail(f"Arquivos faltando: {missing}")
        sys.exit(1)
    
    # ============ STEP 2: Validar DATABASE_URL ============
    print_step(2, "Validando conexão com banco de dados")
    
    try:
        import psycopg2
        try:
            conn = psycopg2.connect(database_url, connect_timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            print_ok("✅ Conexão com Supabase bem-sucedida")
            cursor.close()
            conn.close()
        except psycopg2.OperationalError as e:
            print_warn(f"Banco não acessível neste momento: {e}")
            print_warn("(Isso é OK - será validado no PythonAnywhere)")
        except Exception as e:
            print_warn(f"Erro ao conectar: {e}")
    except ImportError:
        print_warn("psycopg2 não instalado localmente (OK - será instalado no PythonAnywhere)")
    
    # ============ STEP 3: Gerar .env ============
    print_step(3, "Gerando arquivo .env")
    
    env_content = f"""# AUTO-GENERATED - {datetime.now().isoformat()}
# Concurso Elite Production Environment

# === DATABASE ===
DATABASE_URL={database_url}

# === SECURITY ===
SECRET_KEY={secret_key}

# === CORS ===
CORS_ORIGINS=https://open-notebook-8x8twkj23.vercel.app,https://{username}.pythonanywhere.com,http://localhost:3000

# === ENVIRONMENT ===
ENVIRONMENT=production
DEBUG=false
PYTHONUNBUFFERED=1

# === APP ===
APP_TITLE=Concurso Elite v3.3
APP_VERSION=3.3.0
"""
    
    env_file = ".env"
    with open(env_file, "w") as f:
        f.write(env_content)
    
    # Proteger arquivo .env
    os.chmod(env_file, 0o600)
    print_ok(f".env criado e protegido (chmod 600)")
    
    # ============ STEP 4: Gerar WSGI config para PythonAnywhere ============
    print_step(4, "Gerando WSGI config")
    
    wsgi_config = f"""
# WSGI CONFIGURATION FOR PYTHONANYWHERE
# Copy and paste this content to:
# https://www.pythonanywhere.com/user/{username}/webapps/
# Edit WSGI file -> /var/www/{username}_pythonanywhere_com_wsgi.py

import sys
import os
from pathlib import Path

# Environment variables
os.environ['DATABASE_URL'] = '''{database_url}'''
os.environ['SECRET_KEY'] = '''{secret_key}'''
os.environ['CORS_ORIGINS'] = 'https://open-notebook-8x8twkj23.vercel.app,https://{username}.pythonanywhere.com'
os.environ['PYTHONUNBUFFERED'] = '1'

# Path configuration
home = Path.home()
project_path = home / 'concursos-elite'
backend_path = str(project_path / 'backend')

if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import FastAPI app
from main_supabase import app as application
"""
    
    wsgi_file = "WSGI_CONFIG_PYTHONANYWHERE.py"
    with open(wsgi_file, "w") as f:
        f.write(wsgi_config)
    
    print_ok(f"WSGI config salvo em {wsgi_file}")
    print_warn("Copiar conteudo deste arquivo para PythonAnywhere Web WSGI file")
    
    # ============ STEP 5: Gerar Bash commands ============
    print_step(5, "Gerando Bash commands para PythonAnywhere")
    
    bash_commands = f"""#!/bin/bash
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
DATABASE_URL={database_url}
SECRET_KEY={secret_key}
CORS_ORIGINS=https://open-notebook-8x8twkj23.vercel.app,https://{username}.pythonanywhere.com
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
    print(f"Database connection FAILED: {{e}}")
    exit(1)
PYEOF

echo "DEPLOYMENT CONCLUIDO!"
echo ""
echo "PROXIMAS ACOES NO PYTHONANYWHERE:"
echo "  1. Abrir: https://www.pythonanywhere.com/user/{username}/webapps/"
echo "  2. Click 'Add a new web app'"
echo "  3. Escolher Python 3.11 e FastAPI"
echo "  4. Editar WSGI file com conteudo de WSGI_CONFIG_PYTHONANYWHERE.py"
echo "  5. Recarregar (botao verde)"
echo ""
echo "Endpoints:"
echo "  Health: https://{username}.pythonanywhere.com/health"
echo "  Login:  https://{username}.pythonanywhere.com/api/auth/login-novo"
echo "  Status: https://{username}.pythonanywhere.com/api/auth/status/mr.dblucas@gmail.com"
"""
    
    bash_file = "deploy_pythonanywhere.sh"
    with open(bash_file, "w") as f:
        f.write(bash_commands)
    
    os.chmod(bash_file, 0o755)
    print_ok(f"Bash commands salvo em {bash_file}")
    print_warn("Copiar e executar este script no Bash Console do PythonAnywhere")
    
    # ============ STEP 6: Gerar Checklist ============
    print_step(6, "Gerando Checklist de Deployment")
    
    checklist = f"""
# 📋 CHECKLIST - CONCURSO ELITE DEPLOYMENT

## PRÉ-REQUISITOS
- [ ] Conta criada em https://www.pythonanywhere.com/
- [ ] Username: {username}
- [ ] Email verificado

## DEPLOYMENT STEPS

### 1. Bash Console (PythonAnywhere)
- [ ] Copiar e executar comandos de deploy_pythonanywhere.sh
- [ ] Aguardar 2-3 minutos
- [ ] Confirmar: "✅ DEPLOYMENT CONCLUÍDO!"

### 2. Web App Configuration
- [ ] Acessar: https://www.pythonanywhere.com/user/{username}/webapps/
- [ ] Click: "+ Add a new web app"
- [ ] Escolher: Python 3.11
- [ ] Escolher: FastAPI
- [ ] Confirmar

### 3. WSGI File
- [ ] Edit WSGI file: /var/www/{username}_pythonanywhere_com_wsgi.py
- [ ] Substituir CONTEÚDO COMPLETO por WSGI_CONFIG_PYTHONANYWHERE.py
- [ ] Save

### 4. Environment Variables
- [ ] Web → Environment variables
- [ ] Adicionar (ou confirmar):
  - DATABASE_URL={database_url}
  - SECRET_KEY={secret_key}
  - CORS_ORIGINS=...
  - PYTHONUNBUFFERED=1

### 5. Reload Web App
- [ ] Click botão verde "Reload"
- [ ] Aguardar ~10 segundos
- [ ] Verificar se está "Online" (cor verde)

## TESTES

### Health Check
```bash
curl https://{username}.pythonanywhere.com/health
```
Esperado: {{"status": "OK", ...}}

### Login Test (Admin)
```bash
curl -X POST https://{username}.pythonanywhere.com/api/auth/login-novo \\
  -H "Content-Type: application/json" \\
  -d '{{"email":"mr.dblucas@gmail.com","password":"Lightshigaraki789","lat":-15.8268,"lng":-48.0409}}'
```
Esperado: {{"status": "sucesso", "access_token": "...", ...}}

### Login Test (Cabo)
```bash
curl -X POST https://{username}.pythonanywhere.com/api/auth/login-novo \\
  -H "Content-Type: application/json" \\
  -d '{{"email":"cabo.md@email.com","password":"cabo123","lat":-15.8268,"lng":-48.0409}}'
```

### Login Test (Matheus)
```bash
curl -X POST https://{username}.pythonanywhere.com/api/auth/login-novo \\
  -H "Content-Type: application/json" \\
  -d '{{"email":"matheus@email.com","password":"matheus123","lat":-15.85,"lng":-48.06}}'
```

## TROUBLESHOOTING

### 502 Bad Gateway
- [ ] Verificar logs em Web → Log files
- [ ] Confirmar DATABASE_URL em Environment variables
- [ ] Confirmar importações em requirements.txt
- [ ] Reload

### Database Connection Error
- [ ] Testar DATABASE_URL localmente: `psql <DATABASE_URL>`
- [ ] Confirmar password correta
- [ ] Confirmar IP não está bloqueado (Supabase)

### WSGI Import Error
- [ ] Verificar caminho em wsgi file
- [ ] Confirmar backend/ existe em /home/{username}/concursos-elite/

## MONITORING

### Logs
- [ ] Web → Log files → Error log (verificar)
- [ ] Web → Log files → Access log (verificar)

### Health
- [ ] Executar health check regularmente
- [ ] Monitorar CPU/Mem em PythonAnywhere Dashboard

## MOBILE ACCESS

### Frontend Update
- [ ] Arquivo: frontend/index.html
- [ ] Linha: ~1170
- [ ] Atualizar: `const API = "https://{username}.pythonanywhere.com"`
- [ ] Git push para redeploy automático em Vercel

### Test on Mobile
- [ ] iPhone: Abrir https://open-notebook-8x8twkj23.vercel.app
- [ ] Android: Abrir https://open-notebook-8x8twkj23.vercel.app
- [ ] Fazer login com 3 usuários
- [ ] Verificar geofencing

---

Generated: {datetime.now().isoformat()}
Username: {username}
Backend: https://{username}.pythonanywhere.com
Frontend: https://open-notebook-8x8twkj23.vercel.app
"""
    
    checklist_file = "CHECKLIST_DEPLOYMENT.md"
    with open(checklist_file, "w") as f:
        f.write(checklist)
    
    print_ok(f"Checklist salvo em {checklist_file}")
    
    # ============ FINAL SUMMARY ============
    print_header("DEPLOYMENT AUTOMATICO COMPLETO")
    
    print(f"""
Arquivos Gerados:
  1. .env - Variaveis de ambiente (PROTEGIDO - chmod 600)
  2. WSGI_CONFIG_PYTHONANYWHERE.py - Config WSGI para PythonAnywhere
  3. deploy_pythonanywhere.sh - Bash commands para Bash Console
  4. CHECKLIST_DEPLOYMENT.md - Guia passo-a-passo completo

Proximas Acoes:
  1. Abrir PythonAnywhere Bash Console
  2. Copiar e executar comandos de deploy_pythonanywhere.sh
  3. Seguir CHECKLIST_DEPLOYMENT.md
  4. Testar endpoints

URLs de Teste:
  Health:  https://{username}.pythonanywhere.com/health
  API:     https://{username}.pythonanywhere.com
  Docs:    https://{username}.pythonanywhere.com/docs

Informacoes de Seguranca:
  - .env esta protegido (chmod 600)
  - Nao commitar .env no Git!
  - SECRET_KEY deve ser alterado periodicamente
  - DATABASE_URL contem credenciais - manter seguro

[OK] Tudo pronto! Proximo passo: Executar deploy_pythonanywhere.sh no PythonAnywhere
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_fail("\n⚠️  Operação cancelada pelo usuário")
        sys.exit(0)
    except Exception as e:
        print_fail(f"❌ Erro durante deployment: {e}")
        sys.exit(1)
