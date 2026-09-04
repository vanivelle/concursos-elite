"""
WSGI wrapper para PythonAnywhere - FastAPI Concurso Elite
Auto-gerado para deployment production
"""

import sys
import os
from pathlib import Path

# ============ PATH CONFIGURATION ============
# Detectar path automaticamente
home_dir = Path.home()
project_dirs = [
    home_dir / "concursos-elite" / "backend",  # PythonAnywhere default
    home_dir / "concurso_elite" / "backend",
    Path(__file__).parent,  # Fallback: script location
]

backend_path = None
for path in project_dirs:
    if path.exists():
        backend_path = str(path)
        break

if not backend_path:
    raise RuntimeError(f"❌ Backend path not found. Checked: {project_dirs}")

if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# ============ ENVIRONMENT VARIABLES ============
# Estas devem estar configuradas em PythonAnywhere
# Web → Environment variables

required_env = ["DATABASE_URL", "SECRET_KEY"]
missing_env = [var for var in required_env if not os.getenv(var)]

if missing_env:
    raise RuntimeError(f"❌ Missing environment variables: {missing_env}")

# Configurar WSGI
os.environ.setdefault("PYTHONUNBUFFERED", "1")

# ============ IMPORT FASTAPI APP ============
try:
    from main_supabase import app as application
except ImportError as e:
    raise RuntimeError(f"❌ Failed to import main_supabase: {e}")

# ============ LOGGING ============
import logging
logger = logging.getLogger("concurso-elite-wsgi")
logger.info(f"✅ WSGI initialized successfully")
logger.info(f"   Backend path: {backend_path}")
logger.info(f"   Database: {'configured' if os.getenv('DATABASE_URL') else 'MISSING'}")
logger.info(f"   JWT Secret: {'configured' if os.getenv('SECRET_KEY') else 'using default (INSECURE)'}")

# ============ WSGI CALLABLE ============
# PythonAnywhere will call this
if __name__ == "__main__":
    application.run()
