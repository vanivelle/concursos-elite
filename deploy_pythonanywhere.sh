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
echo ""
echo "PROXIMAS ACOES NO PYTHONANYWHERE:"
echo "  1. Abrir: https://www.pythonanywhere.com/user/concursoelite/webapps/"
echo "  2. Click 'Add a new web app'"
echo "  3. Escolher Python 3.11 e FastAPI"
echo "  4. Editar WSGI file com conteudo de WSGI_CONFIG_PYTHONANYWHERE.py"
echo "  5. Recarregar (botao verde)"
echo ""
echo "Endpoints:"
echo "  Health: https://concursoelite.pythonanywhere.com/health"
echo "  Login:  https://concursoelite.pythonanywhere.com/api/auth/login-novo"
echo "  Status: https://concursoelite.pythonanywhere.com/api/auth/status/mr.dblucas@gmail.com"
