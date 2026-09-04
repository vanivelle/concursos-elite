#!/usr/bin/env python3
"""
🚀 PythonAnywhere Deployment Automation
Pre-flight validation + WSGI config generator (Windows/Mac/Linux)
"""

import os
import sys
import subprocess
from pathlib import Path

# Color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def print_header(title):
    print(f"\n{BLUE}╔════════════════════════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║  {title:<56}║{NC}")
    print(f"{BLUE}╚════════════════════════════════════════════════════════════╝{NC}")
    print()

def check_pass(msg):
    print(f"{GREEN}✓ PASS{NC}: {msg}")

def check_fail(msg):
    print(f"{RED}✗ FAIL{NC}: {msg}")

def check_warn(msg):
    print(f"{YELLOW}⚠ WARNING{NC}: {msg}")

def main():
    print_header("PythonAnywhere Pre-Flight Checks")
    
    errors = 0
    
    # ============ CHECK 1: DATABASE_URL not hardcoded ============
    print("📋 [CHECK 1] Validating code security...")
    
    main_file = Path("backend/main_supabase.py")
    if not main_file.exists():
        check_fail(f"{main_file} not found")
        errors += 1
    else:
        content = main_file.read_text(encoding='utf-8')
        
        # Check if hardcoded
        if 'DB_URL = "postgresql://' in content:
            check_fail("DATABASE_URL is hardcoded in main_supabase.py")
            check_fail("  Fix: Use os.getenv('DATABASE_URL', 'fallback')")
            errors += 1
        elif "os.getenv" in content and "DATABASE_URL" in content:
            check_pass("DATABASE_URL uses environment variables")
        else:
            check_warn("DATABASE_URL configuration unclear - verify manually")
    
    print()
    
    # ============ CHECK 2: requirements.txt ============
    print("📋 [CHECK 2] Validating requirements.txt...")
    
    req_file = Path("requirements.txt")
    if not req_file.exists():
        check_fail("requirements.txt not found")
        errors += 1
    else:
        req_content = req_file.read_text(encoding='utf-8')
        required = ["fastapi", "uvicorn", "psycopg2", "pydantic", "python-dotenv"]
        
        for pkg in required:
            if pkg in req_content:
                print(f"{GREEN}✓{NC} {pkg}")
            else:
                check_fail(f"{pkg} missing from requirements.txt")
                errors += 1
    
    print()
    
    # ============ CHECK 3: No secrets in code ============
    print("📋 [CHECK 3] Scanning for hardcoded secrets in connection strings...")
    
    if main_file.exists():
        content = main_file.read_text(encoding='utf-8')
        # Look for password in os.getenv() calls (connection string exposure)
        suspicious_lines = [
            line for line in content.split('\n')
            if 'os.getenv' in line and 'Lightshigaraki789' in line
        ]
        
        if suspicious_lines:
            check_fail("Found password exposed in os.getenv() - must use environment variable only")
            errors += 1
        else:
            check_pass("Connection strings are environment-variable based (secure)")

    
    print()
    
    # ============ CHECK 4: PostgreSQL Connection ============
    print("📋 [CHECK 4] Testing PostgreSQL connection...")
    
    try:
        import psycopg2
        
        db_url = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres"
        )
        
        try:
            conn = psycopg2.connect(db_url)
            conn.close()
            check_pass("PostgreSQL connection successful")
        except Exception as e:
            check_fail(f"Cannot connect to PostgreSQL: {e}")
            errors += 1
    except ImportError:
        check_warn("psycopg2 not installed - install with: pip install psycopg2-binary")
    
    print()
    
    # ============ CHECK 5: Python version ============
    print("📋 [CHECK 5] Checking Python version...")
    
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if sys.version_info.major == 3 and sys.version_info.minor >= 11:
        check_pass(f"Python {py_version} (compatible)")
    else:
        check_warn(f"Python {py_version} (PythonAnywhere recommends 3.11+)")
    
    print()
    
    # ============ GENERATE WSGI CONFIG ============
    print_header("WSGI Configuration (Copy to PythonAnywhere)")
    
    username = input("📝 Enter PythonAnywhere username: ").strip()
    
    wsgi_content = f"""import sys
import os

# Add project path
path = '/home/{username}/concursos-elite/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres'
os.environ['PYTHONUNBUFFERED'] = '1'

# Import FastAPI app
from main_supabase import app as application
"""
    
    print("📄 WSGI Config:")
    print("━" * 60)
    print(wsgi_content)
    print("━" * 60)
    print()
    print(f"{YELLOW}ℹ️  Copy above to: /var/www/{username}_pythonanywhere_com_wsgi.py{NC}")
    print()
    
    # ============ BASH COMMANDS ============
    print_header("PythonAnywhere Bash Commands (Run in Console)")
    
    bash_commands = f"""# 1️⃣  Clone repository
cd ~
git clone https://github.com/vanivelle/concursos-elite.git
cd concursos-elite

# 2️⃣  Install dependencies
pip install --user -r requirements.txt

# 3️⃣  Test import (verify no errors)
python3 -c "from backend.main_supabase import app; print('✓ Import successful')"
"""
    
    print("📝 Bash Commands:")
    print("━" * 60)
    print(bash_commands)
    print("━" * 60)
    print()
    
    # ============ FINAL SUMMARY ============
    print_header("Deployment Summary")
    
    if errors == 0:
        print(f"{GREEN}✅ ALL CHECKS PASSED{NC}")
        print()
        print("🚀 Ready to deploy to PythonAnywhere!")
        print()
        print("Next steps:")
        print("  1. Create free account: https://www.pythonanywhere.com")
        print("  2. Bash console: Run commands from above")
        print("  3. Web app: Create Python 3.11 FastAPI app")
        print("  4. WSGI config: Paste content above")
        print("  5. Environment variables:")
        print("     DATABASE_URL = postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres")
        print("     PYTHONUNBUFFERED = 1")
        print("  6. Reload: Click green Reload button")
        print("  7. Test: curl https://<username>.pythonanywhere.com/health")
        print()
        return 0
    else:
        print(f"{RED}❌ FAILED: {errors} CHECKS DID NOT PASS{NC}")
        print()
        print("Fix issues above and re-run this script.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
