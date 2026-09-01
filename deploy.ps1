# Deploy PowerShell Script for Vercel
# Usage: .\deploy.ps1 -VercelToken "your_token_here"

param(
    [string]$VercelToken = $env:VERCEL_TOKEN
)

if (-not $VercelToken) {
    Write-Host "❌ ERRO: VERCEL_TOKEN não definido!"
    Write-Host "Use: .\deploy.ps1 -VercelToken 'seu_token_aqui'"
    exit 1
}

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectPath

Write-Host "🚀 DEPLOYING CONCURSO ELITE v3.3 TO VERCEL"
Write-Host "==========================================="
Write-Host ""

# Verificar vercel.json
if (-not (Test-Path "vercel.json")) {
    Write-Host "❌ vercel.json não encontrado!"
    exit 1
}

Write-Host "✓ Configuração vercel.json OK"
Write-Host "✓ Arquivos prontos para deploy"
Write-Host ""

# Fazer deploy sem prompts
Write-Host "📦 Iniciando deployment..."
Write-Host ""

$env:VERCEL_TOKEN = $VercelToken
& vercel --prod --yes 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ DEPLOYMENT COMPLETADO COM SUCESSO!"
    Write-Host ""
    Write-Host "🌐 URL do Frontend:"
    Write-Host "   https://concursos-elite.vercel.app"
    Write-Host ""
    Write-Host "📊 Dashboard:"
    Write-Host "   https://vercel.com/vanivelle/concursos-elite"
}
else {
    Write-Host ""
    Write-Host "❌ Erro no deployment!"
    exit 1
}
