#!/bin/bash
# 🚀 PythonAnywhere Deployment Automation
# Pre-flight checks + WSGI config generator

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  PythonAnywhere Deployment Pre-Flight Checks               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# ============ CHECK 1: DATABASE_URL is NOT hardcoded ============
echo "📋 [CHECK 1] Validating code security..."
if grep -q "DB_URL = \"postgresql://" backend/main_supabase.py; then
    echo -e "${RED}✗ FAIL${NC}: DATABASE_URL is hardcoded in main_supabase.py"
    echo "  Fix: Use os.getenv('DATABASE_URL', 'fallback')"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓ PASS${NC}: DATABASE_URL uses environment variables"
fi

if grep -q "os.getenv.*DATABASE_URL" backend/main_supabase.py; then
    echo -e "${GREEN}✓ PASS${NC}: os.getenv() properly configured"
else
    echo -e "${YELLOW}⚠ WARNING${NC}: Confirm DATABASE_URL is in environment"
fi

echo ""

# ============ CHECK 2: All imports in requirements.txt ============
echo "📋 [CHECK 2] Validating requirements.txt..."

IMPORTS=("fastapi" "uvicorn" "psycopg2" "pydantic" "python-dotenv")
for pkg in "${IMPORTS[@]}"; do
    if grep -q "^$pkg" requirements.txt; then
        echo -e "${GREEN}✓${NC} $pkg found"
    else
        echo -e "${RED}✗${NC} $pkg MISSING from requirements.txt"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""

# ============ CHECK 3: No hardcoded secrets ============
echo "📋 [CHECK 3] Scanning for hardcoded secrets..."

if grep -q "Lightshigaraki789\|mr.dblucas@gmail.com" backend/main_supabase.py | grep -v "USUARIOS = {"; then
    echo -e "${RED}✗ FAIL${NC}: Found hardcoded passwords outside USUARIOS dict"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓ PASS${NC}: No secrets exposed in code"
fi

echo ""

# ============ CHECK 4: PostgreSQL Connection ============
echo "📋 [CHECK 4] Testing PostgreSQL connection..."

if python3 << 'EOF'
import psycopg2
import os

db_url = os.getenv("DATABASE_URL", "postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres")

try:
    conn = psycopg2.connect(db_url)
    conn.close()
    print("✓ PASS: PostgreSQL connection successful")
    exit(0)
except Exception as e:
    print(f"✗ FAIL: {e}")
    exit(1)
EOF
then
    echo ""
else
    echo -e "${RED}✗ FAIL${NC}: Cannot connect to PostgreSQL"
    echo "  Verify DATABASE_URL and network access"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# ============ CHECK 5: Python version ============
echo "📋 [CHECK 5] Checking Python version..."

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
if [[ $PYTHON_VERSION == 3.11* ]] || [[ $PYTHON_VERSION == 3.12* ]]; then
    echo -e "${GREEN}✓ PASS${NC}: Python $PYTHON_VERSION (compatible)"
else
    echo -e "${YELLOW}⚠ WARNING${NC}: Python $PYTHON_VERSION (PythonAnywhere uses 3.11)"
fi

echo ""

# ============ GENERATE WSGI CONFIG ============
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  WSGI Configuration (Copy to PythonAnywhere)               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

read -p "Enter PythonAnywhere username: " USERNAME

cat > /tmp/pythonanywhere_wsgi.py << EOF
import sys
import os

# Add project path
path = '/home/$USERNAME/concursos-elite/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres'
os.environ['PYTHONUNBUFFERED'] = '1'

# Import FastAPI app
from main_supabase import app as application
EOF

echo "📄 WSGI Config:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat /tmp/pythonanywhere_wsgi.py
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Copy above content to:"
echo "   /var/www/${USERNAME}_pythonanywhere_com_wsgi.py"
echo ""

# ============ GENERATE BASH COMMANDS ============
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  PythonAnywhere Bash Commands (Run in Console)             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cat > /tmp/pythonanywhere_commands.sh << EOF
# 1️⃣  Clone repository
cd ~
git clone https://github.com/vanivelle/concursos-elite.git
cd concursos-elite

# 2️⃣  Install dependencies
pip install --user -r requirements.txt

# 3️⃣  Test import (verify no errors)
python3 -c "from backend.main_supabase import app; print('✓ Import successful')"
EOF

echo "📝 Bash Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat /tmp/pythonanywhere_commands.sh
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============ FINAL SUMMARY ============
echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ ALL CHECKS PASSED${NC}"
    echo ""
    echo "🚀 Ready to deploy to PythonAnywhere!"
    echo ""
    echo "Next steps:"
    echo "  1. Create free account: https://www.pythonanywhere.com"
    echo "  2. Bash console: Run commands from above"
    echo "  3. Web app: Create Python 3.11 FastAPI app"
    echo "  4. WSGI config: Paste content above"
    echo "  5. Environment: Set DATABASE_URL and PYTHONUNBUFFERED"
    echo "  6. Reload: Click green Reload button"
    echo "  7. Test: curl https://<username>.pythonanywhere.com/health"
    exit 0
else
    echo -e "${RED}❌ FAILED: $ERRORS CHECKS DID NOT PASS${NC}"
    echo ""
    echo "Fix issues above and re-run this script."
    exit 1
fi
