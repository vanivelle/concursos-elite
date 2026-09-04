#!/usr/bin/env bash
# CHECKLIST - Deployment PythonAnywhere (Marque conforme avança)

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   CONCURSO ELITE - PythonAnywhere Deployment Checklist         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_mark() {
    echo -e "${GREEN}✅${NC} $1"
}

pending() {
    echo -e "${YELLOW}⏳${NC} $1"
}

todo() {
    echo -e "${RED}❌${NC} $1"
}

echo "════════════════════════════════════════════════════════════════"
echo "📋 FASE 1: PRÉ-REQUISITOS (LOCAL)"
echo "════════════════════════════════════════════════════════════════"
echo ""

check_mark "requirements.txt atualizado com 14 pacotes"
check_mark "Pacotes problemáticos removidos (Celery, Redis, GeoIP2)"
check_mark "Versão pydantic==2.5.0 confirmada"
check_mark "PyJWT==2.13.0 confirmado"
check_mark "Git commit feito: bb6ca3a"
check_mark "GitHub push realizado"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "🌐 FASE 2: SETUP PYTHONANYWHERE"
echo "════════════════════════════════════════════════════════════════"
echo ""

todo "1. Criar conta em https://www.pythonanywhere.com (5 min)"
echo "   └─ Escolher username: seu_usuario"
echo ""

todo "2. Clonar repositório (1 min)"
echo "   └─ git clone https://github.com/vanivelle/concursos-elite.git"
echo ""

todo "3. Instalar dependências (3-5 min)"
echo "   └─ pip install --user -r requirements.txt"
echo ""

todo "4. Configurar FastAPI web app (2 min)"
echo "   └─ Web → + Add a new web app → FastAPI → Python 3.11"
echo ""

todo "5. Editar arquivo WSGI (2 min)"
echo "   └─ Ver: GUIA_DEPLOYMENT_PYTHONANYWHERE_PASSO_A_PASSO.md"
echo ""

todo "6. Recarregar web app (1 min)"
echo "   └─ Web → Reload (botão verde)"
echo ""

todo "7. Validar instalação (2 min)"
echo "   └─ curl https://seu_usuario.pythonanywhere.com/health"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo "✅ VALIDAÇÃO FINAL"
echo "════════════════════════════════════════════════════════════════"
echo ""

todo "Health check retorna {\"status\": \"ok\"}"
todo "API Docs acessível em /docs"
todo "Endpoints de API respondem corretamente"
todo "Database conecta com Supabase"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "📞 REFERÊNCIAS RÁPIDAS"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Documentação Principal:"
echo "  → RESUMO_SOLUCAO_PYTHONANYWHERE.md"
echo "  → GUIA_DEPLOYMENT_PYTHONANYWHERE_PASSO_A_PASSO.md"
echo "  → DIAGNOSTICO_PYTHONANYWHERE_PROBLEMA.md"
echo ""
echo "Comandos Essenciais:"
echo "  # No seu PC (validar):
echo "  pip install -r requirements.txt --dry-run"
echo ""
echo "  # No PythonAnywhere (instalar):"
echo "  pip install --user -r requirements.txt"
echo ""
echo "  # No PythonAnywhere (validar):"
echo "  python -c \"import fastapi; import pydantic; print('✅ OK')\""
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "⏱️  TEMPO ESTIMADO: 20 MINUTOS (8 passos)"
echo "════════════════════════════════════════════════════════════════"
