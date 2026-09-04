
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
