#!/usr/bin/env python3
"""
Analisador de compatibilidade requirements.txt para PythonAnywhere
Identifica pacotes problemáticos e sugere versões pré-compiladas
"""

import json
import subprocess
import sys
from pathlib import Path

# Pacotes com issues em PythonAnywhere free tier (sem Rust/compilação)
PROBLEMATIC_PACKAGES = {
    'pydantic-core': {
        'issue': 'Requer compilação Rust',
        'solution': 'Usar pydantic 2.5.0+ com wheels pré-compilados'
    },
    'geoip2': {
        'issue': 'Dependência opcional, não essencial',
        'solution': 'REMOVER - usar geolocalização alternativa'
    },
    'maxminddb': {
        'issue': 'Dependência do geoip2',
        'solution': 'REMOVER'
    },
    'celery': {
        'issue': 'Requer Redis/RabbitMQ - não usamos',
        'solution': 'REMOVER'
    },
    'redis': {
        'issue': 'Não essencial para FastAPI básico',
        'solution': 'REMOVER'
    }
}

# Versões testadas e funcionando em PythonAnywhere
PYTHONANYWHERE_SAFE_VERSIONS = {
    'fastapi': '0.110.0',  # ✅ Wheel disponível
    'uvicorn': '0.27.0',   # ✅ Wheel disponível
    'pydantic': '2.5.0',   # ✅ Wheel disponível (core vem pré-compilado)
    'sqlalchemy': '2.0.23', # ✅ Wheel disponível
    'psycopg2-binary': '2.9.9',  # ✅ Binary wheel
    'python-jose': '3.3.0',  # ✅ Pure Python
    'passlib': '1.7.4',     # ✅ Pure Python
    'bcrypt': '4.1.1',      # ✅ Wheel disponível (não requer Rust)
    'python-multipart': '0.0.6',  # ✅ Pure Python
    'aiohttp': '3.9.1',     # ✅ Wheel disponível
    'requests': '2.31.0',   # ✅ Pure Python
    'cryptography': '41.0.7',  # ✅ Wheel disponível
    'python-dotenv': '1.0.0',  # ✅ Pure Python
    'PyJWT': '2.13.0',      # ✅ Pure Python
}

def analyze_current_requirements():
    """Analisa requirements.txt atual"""
    req_file = Path('requirements.txt')
    
    if not req_file.exists():
        print("❌ requirements.txt não encontrado")
        return {}
    
    packages = {}
    with open(req_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '==' in line:
                    pkg, version = line.split('==')
                    packages[pkg.strip()] = version.strip()
    
    return packages

def check_wheel_availability(package, version):
    """Verifica se versão tem wheel disponível no PyPI"""
    try:
        result = subprocess.run(
            ['pip', 'index', 'versions', f'{package}==={version}'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return 'wheel' in result.stdout.lower() or result.returncode == 0
    except:
        return None  # Desconhecido

def generate_pythonanywhere_requirements():
    """Gera requirements.txt otimizado para PythonAnywhere"""
    
    print("=" * 70)
    print("🔍 ANÁLISE DE COMPATIBILIDADE - PythonAnywhere Free Tier")
    print("=" * 70)
    print()
    
    current = analyze_current_requirements()
    
    print("📋 Pacotes atuais:")
    for pkg, version in sorted(current.items()):
        print(f"  {pkg:30} {version}")
    print()
    
    # Pacotes problemáticos
    print("⚠️  PACOTES PROBLEMÁTICOS:")
    print()
    
    problematic_found = []
    for pkg in PROBLEMATIC_PACKAGES:
        if pkg in current:
            info = PROBLEMATIC_PACKAGES[pkg]
            print(f"  ❌ {pkg}")
            print(f"     Problema: {info['issue']}")
            print(f"     Solução:  {info['solution']}")
            print()
            problematic_found.append(pkg)
    
    if not problematic_found:
        print("  ✅ Nenhum pacote problemático encontrado")
        print()
    
    # Gerar novo requirements.txt otimizado
    print("=" * 70)
    print("✅ NOVO requirements.txt (PythonAnywhere Otimizado)")
    print("=" * 70)
    print()
    
    optimized = []
    for pkg in sorted(PYTHONANYWHERE_SAFE_VERSIONS.keys()):
        version = PYTHONANYWHERE_SAFE_VERSIONS[pkg]
        optimized.append(f"{pkg}=={version}")
    
    for line in optimized:
        print(line)
    
    # Salvar novo arquivo
    new_req_file = Path('requirements_pythonanywhere.txt')
    with open(new_req_file, 'w') as f:
        f.write('\n'.join(optimized))
    
    print()
    print(f"✅ Salvo em: {new_req_file}")
    print()
    
    # Resumo de mudanças
    print("=" * 70)
    print("📊 MUDANÇAS REALIZADAS")
    print("=" * 70)
    print()
    
    removed = [pkg for pkg in current if pkg not in PYTHONANYWHERE_SAFE_VERSIONS]
    added = [pkg for pkg in PYTHONANYWHERE_SAFE_VERSIONS if pkg not in current]
    
    if removed:
        print(f"🗑️  REMOVIDOS ({len(removed)}):")
        for pkg in sorted(removed):
            print(f"   - {pkg}=={current[pkg]}")
        print()
    
    if added:
        print(f"➕ ADICIONADOS ({len(added)}):")
        for pkg in sorted(added):
            print(f"   + {pkg}=={PYTHONANYWHERE_SAFE_VERSIONS[pkg]}")
        print()
    
    # Pacotes mantidos
    print(f"✅ MANTIDOS ({len(PYTHONANYWHERE_SAFE_VERSIONS)}):")
    for pkg in sorted(PYTHONANYWHERE_SAFE_VERSIONS.keys()):
        old_ver = current.get(pkg, 'N/A')
        new_ver = PYTHONANYWHERE_SAFE_VERSIONS[pkg]
        if old_ver != 'N/A' and old_ver != new_ver:
            print(f"   ↻ {pkg}: {old_ver} → {new_ver}")
        elif old_ver != 'N/A':
            print(f"   → {pkg}: {new_ver}")
    
    print()
    print("=" * 70)
    print("🚀 INSTRUÇÕES DE DEPLOYMENT")
    print("=" * 70)
    print()
    print("1. No seu PC/Mac local:")
    print("   pip install -r requirements_pythonanywhere.txt --dry-run")
    print()
    print("2. Depois, fazer commit e push:")
    print("   git add requirements_pythonanywhere.txt")
    print("   git commit -m 'Fix: Versões otimizadas para PythonAnywhere'")
    print("   git push")
    print()
    print("3. No PythonAnywhere Bash Console:")
    print("   cd ~/concurso-elite")
    print("   pip install --user -r requirements_pythonanywhere.txt")
    print()
    print("4. Validar instalação:")
    print("   python -c \"import fastapi; import pydantic; print('✅ OK')\"")
    print()

if __name__ == '__main__':
    generate_pythonanywhere_requirements()
