#!/usr/bin/env bash
# Script para rodar populador DENTRO do container

echo "🏛️ Executando populador dentro do container..."
cd /app && python populate.py
