#!/bin/bash
# Script de deployment CLI para Vercel

echo "🚀 VERCEL DEPLOYMENT - CONCURSO ELITE v3.3"
echo "==========================================="

# Verificar se está no diretório correto
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json não encontrado!"
    exit 1
fi

echo "✓ vercel.json encontrado"

# Deploy para produção
echo "📦 Iniciando deployment..."
vercel --prod --yes --token $VERCEL_TOKEN

if [ $? -eq 0 ]; then
    echo "✅ Deployment completado com sucesso!"
    echo "🌐 Frontend disponível em:"
    vercel ls --token $VERCEL_TOKEN 2>&1 | grep "concursos-elite"
else
    echo "❌ Erro no deployment!"
    exit 1
fi
