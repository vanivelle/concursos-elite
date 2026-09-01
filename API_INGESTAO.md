# 🔌 API de Ingestão v1.0 - Guia Completo

**IA Concursos Elite** - Integração para Agentes Autônomos (Crawl4AI, OpenHands, etc.)

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Rota de Ingestão](#rota-de-ingestão)
3. [Autenticação](#autenticação)
4. [Formato de Dados](#formato-de-dados)
5. [Exemplos de Uso](#exemplos-de-uso)
6. [Script Agent Bridge](#script-agent-bridge)
7. [Integração com Crawl4AI](#integração-com-crawl4ai)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

A API de ingestão v1.0 permite que **agentes autônomos** (Crawl4AI, OpenHands, bots personalizados) coletem questões da internet e as injetem diretamente no banco PostgreSQL da IA Concursos Elite.

### Características
- ✅ **Bulk Insert**: Ingestão de múltiplas questões em um único request
- ✅ **Segurança**: API-KEY simples mas eficaz para ambiente local
- ✅ **Validação**: Schema Pydantic valida todos os campos obrigatórios
- ✅ **Auditoria**: Logging estruturado de todas as operações
- ✅ **Tolerância a Falhas**: Erros em questões individuais não afetam o lote inteiro

---

## 🔌 Rota de Ingestão

### Endpoint
```
POST /api/v1/ingest
```

### URL Completa
```
http://localhost:8000/api/v1/ingest
```

### Headers Obrigatórios
```
Content-Type: application/json
X-API-KEY: elite-concursos-hunter-2024
```

### Status Codes
- **200**: ✅ Ingestão bem-sucedida (pode ter erros parciais)
- **401**: ❌ API-KEY inválida
- **422**: ❌ Validação Pydantic falhou
- **500**: ❌ Erro interno do servidor

---

## 🔐 Autenticação

### Chave de API Padrão
```
X-API-KEY: elite-concursos-hunter-2024
```

### Definir Chave Customizada
```bash
# Via variável de ambiente
export API_KEY_INGESTAO="minha-chave-super-secreta-2024"

# Reiniciar container
docker restart backend_questoes
```

### Em Produção
⚠️ **IMPORTANTE**: Use uma chave forte e variáveis de ambiente:
```bash
export API_KEY_INGESTAO=$(openssl rand -hex 32)  # Gera chave aleatória
```

---

## 📊 Formato de Dados

### Request JSON (Exemplo Completo)

```json
{
  "questoes": [
    {
      "concurso": "Banco Central (Bacen)",
      "materia": "Português",
      "banca": "ESAF",
      "dificuldade": "Médio",
      "tipo": "Múltipla Escolha",
      "enunciado": "Qual é a alternativa correta sobre regência nominal?",
      "alternativas": {
        "A": "Primeira alternativa",
        "B": "Segunda alternativa",
        "C": "Terceira alternativa (gabarito)",
        "D": "Quarta alternativa"
      },
      "resposta_correta": "C",
      "explicacao": "A alternativa C está correta porque contém a resposta adequada à questão formulada.",
      "pegadinha_banca": "ESAF costuma oferecer alternativas que parecem corretas mas contêm erros sutis de regência."
    }
  ]
}
```

### Schema Pydantic (Obrigatório)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `concurso` | String | ✅ | Um de: "Banco Central (Bacen)", "Transpetro (Petrobras)", "PMDF" |
| `materia` | String | ✅ | Ex: "Português", "Direito Administrativo", "Conhecimentos Gerais" |
| `banca` | String | ✅ | Ex: "ESAF", "Cesgranrio", "CEBRASPE" |
| `dificuldade` | String | ✅ | Um de: "Fácil", "Médio", "Difícil" |
| `tipo` | String | ✅ | Um de: "Múltipla Escolha", "Certo/Errado", "Discursiva" |
| `enunciado` | String | ✅ | Texto completo da questão |
| `alternativas` | Object | ✅ | Dict com chaves A/B/C/D e valores (strings) |
| `resposta_correta` | String | ✅ | Uma das chaves de alternativas (ex: "C") |
| `explicacao` | String | ✅ | Justificativa da resposta correta |
| `pegadinha_banca` | String | ✅ | Armadilha comum dessa banca neste tipo de questão |
| `questao_id` | String | ❌ | ID único (auto-gerado se omitido) |

### Response JSON (Sucesso - 200)

```json
{
  "status": "sucesso",
  "total_inserido": 5,
  "total_no_banco": 127,
  "timestamp": "2024-01-15T23:45:30.123456",
  "detalhes": {
    "tentativas": 5,
    "sucesso": 5,
    "erros": 0,
    "mensagens_erro": null
  }
}
```

### Response JSON (Erro de Autenticação - 401)

```json
{
  "detail": "❌ API-KEY inválida. Acesso negado à ingestão."
}
```

---

## 🧪 Exemplos de Uso

### 1. cURL (Terminal)

```bash
# Ingerir uma questão
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: elite-concursos-hunter-2024" \
  -d '{
    "questoes": [
      {
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",
        "banca": "ESAF",
        "dificuldade": "Médio",
        "tipo": "Múltipla Escolha",
        "enunciado": "Qual é a alternativa correta?",
        "alternativas": {
          "A": "Opção A",
          "B": "Opção B",
          "C": "Opção C",
          "D": "Opção D"
        },
        "resposta_correta": "C",
        "explicacao": "Porque...",
        "pegadinha_banca": "A banca tenta..."
      }
    ]
  }'
```

### 2. Python (Requests)

```python
import requests
import json

url = "http://localhost:8000/api/v1/ingest"
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": "elite-concursos-hunter-2024"
}

questoes = [
    {
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",
        "banca": "ESAF",
        "dificuldade": "Médio",
        "tipo": "Múltipla Escolha",
        "enunciado": "Qual é a alternativa correta?",
        "alternativas": {
            "A": "Opção A",
            "B": "Opção B",
            "C": "Opção C (gabarito)",
            "D": "Opção D"
        },
        "resposta_correta": "C",
        "explicacao": "Explicação detalhada...",
        "pegadinha_banca": "Pegadinha da banca..."
    }
]

response = requests.post(
    url,
    headers=headers,
    json={"questoes": questoes}
)

print(response.json())
```

### 3. Python Async (HTTPX)

```python
import httpx
import asyncio

async def ingerir_questoes(questoes):
    url = "http://localhost:8000/api/v1/ingest"
    headers = {
        "X-API-KEY": "elite-concursos-hunter-2024"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={"questoes": questoes},
            headers=headers
        )
        return response.json()

# Uso
questoes = [...]  # lista de dicts
resultado = asyncio.run(ingerir_questoes(questoes))
print(resultado)
```

### 4. PowerShell (Windows)

```powershell
$url = "http://localhost:8000/api/v1/ingest"
$headers = @{
    "X-API-KEY" = "elite-concursos-hunter-2024"
    "Content-Type" = "application/json"
}

$questoes = @(
    @{
        concurso = "Banco Central (Bacen)"
        materia = "Português"
        banca = "ESAF"
        dificuldade = "Médio"
        tipo = "Múltipla Escolha"
        enunciado = "Qual é a alternativa?"
        alternativas = @{
            A = "Opção A"
            B = "Opção B"
            C = "Opção C"
            D = "Opção D"
        }
        resposta_correta = "C"
        explicacao = "Explicação..."
        pegadinha_banca = "Pegadinha..."
    }
)

$body = @{questoes = $questoes} | ConvertTo-Json

$response = Invoke-WebRequest -Uri $url -Method POST -Headers $headers -Body $body
Write-Host $response.Content
```

---

## 🤖 Script Agent Bridge

### Uso Básico

```bash
# Ingerir questões de exemplo do Bacen
cd backend
python agent_bridge.py --concurso "Banco Central (Bacen)" --modo local

# Ingerir de arquivo JSON
python agent_bridge.py --arquivo questoes.json --tamanho-lote 20

# Modo scraper (integrado com Crawl4AI)
python agent_bridge.py --concurso "Transpetro (Petrobras)" --modo scraper
```

### Argumentos Disponíveis

```bash
python agent_bridge.py --help

Options:
  --concurso TEXT         Concurso alvo (default: "Banco Central (Bacen)")
  --modo {local,scraper,hybrid}  Modo de operação
  --arquivo TEXT         Caminho para arquivo JSON com questões
  --endpoint TEXT        URL da API (default: http://localhost:8000)
  --api-key TEXT         Chave de API
  --tamanho-lote INT     Tamanho dos lotes (default: 10)
```

### Variáveis de Ambiente

```bash
# Customizar endpoint e chave
export API_ENDPOINT="http://api.meuserver.com:8000"
export API_KEY_INGESTAO="sua-chave-segura"
export BATCH_SIZE="50"

python agent_bridge.py --concurso "PMDF" --modo scraper
```

### Arquivo JSON de Entrada

```json
{
  "questoes": [
    {
      "concurso": "Banco Central (Bacen)",
      "materia": "Português",
      "banca": "ESAF",
      "dificuldade": "Difícil",
      "tipo": "Múltipla Escolha",
      "enunciado": "...",
      "alternativas": {...},
      "resposta_correta": "C",
      "explicacao": "...",
      "pegadinha_banca": "..."
    }
  ]
}
```

---

## 🕷️ Integração com Crawl4AI

### Passo 1: Instalar Crawl4AI

```bash
pip install crawl4ai
```

### Passo 2: Script de Scraping

```python
# backend/scraper_crawl4ai.py
import asyncio
from crawl4ai import AsyncWebCrawler
import requests
import json

class CrawlerConcursos:
    def __init__(self, api_endpoint="http://localhost:8000", api_key="elite-concursos-hunter-2024"):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
    
    async def raspar_bacen(self):
        """Raspa questões do portal do Bacen"""
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url="https://www.bcb.gov.br/conteudo/publicacoes/",
                js_code="return document.querySelectorAll('.questao')",
                headless=True
            )
            
            questoes = self.extrair_questoes(result.extracted_content)
            return questoes
    
    def extrair_questoes(self, html_content):
        """Extrai dados estruturados do HTML"""
        # Parse HTML e retorna lista de dicts estruturados
        questoes = []
        # ... lógica de extração
        return questoes
    
    def ingerir(self, questoes):
        """Envia questões para a API de ingestão"""
        url = f"{self.api_endpoint}/api/v1/ingest"
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key
        }
        
        response = requests.post(
            url,
            json={"questoes": questoes},
            headers=headers
        )
        
        return response.json()

# Uso
async def main():
    crawler = CrawlerConcursos()
    
    # Raspar Bacen
    questoes_bacen = await crawler.raspar_bacen()
    resultado = crawler.ingerir(questoes_bacen)
    
    print(f"Inseridas: {resultado['total_inserido']} questões")

if __name__ == "__main__":
    asyncio.run(main())
```

### Passo 3: Executar em Background

```bash
# Terminal 1: Iniciar API
docker-compose up -d

# Terminal 2: Executar scraper
python backend/scraper_crawl4ai.py &

# Ou agendar com Cron (Linux/Mac)
0 2 * * * cd /path/to/open-notebook && python backend/scraper_crawl4ai.py
```

---

## 📋 Integração com OpenHands

### Instrução para OpenHands

```markdown
# Tarefa: Coletar questões e injetar na IA Concursos Elite

Objetivo: Raspar questões do portal da Transpetro e injetar na API local.

Passos:
1. Acessar: https://www.transpetro.com.br/concursos/questoes
2. Extrair cada questão com campos:
   - Enunciado (texto completo)
   - Alternativas (A, B, C, D com textos)
   - Gabarito (resposta correta)
   - Tipo (múltipla escolha)
3. Fazer POST para http://localhost:8000/api/v1/ingest
   - Header: X-API-KEY: elite-concursos-hunter-2024
   - Body: {"questoes": [...]}
4. Validar sucesso (status_code 200, total_inserido > 0)

Constraints:
- Máximo 50 questões por batch
- Timeout máximo 30s por batch
- Não deixar páginas em aberto
```

---

## 🐛 Troubleshooting

### Erro: "API-KEY inválida"
```
❌ 401: {"detail": "❌ API-KEY inválida. Acesso negado à ingestão."}
```
**Solução:**
```bash
# Verificar chave padrão
echo "elite-concursos-hunter-2024"

# Ou verificar variável de ambiente
echo $API_KEY_INGESTAO

# Testar com curl
curl -H "X-API-KEY: elite-concursos-hunter-2024" http://localhost:8000/api/v1/ingest -X POST ...
```

### Erro: "Conexão recusada"
```
❌ ConnectionError: Failed to establish a new connection
```
**Solução:**
```bash
# Verificar se API está rodando
curl http://localhost:8000/health

# Reiniciar container
docker restart backend_questoes

# Verificar logs
docker logs backend_questoes -f
```

### Erro: "Campo obrigatório faltando"
```
❌ 422: Validação Pydantic falhou
```
**Solução:**
```python
# Validar dados localmente antes de enviar
campos_obrigatorios = [
    'concurso', 'materia', 'banca', 'enunciado',
    'alternativas', 'resposta_correta', 'explicacao', 'pegadinha_banca'
]

for questao in questoes:
    for campo in campos_obrigatorios:
        if campo not in questao:
            print(f"Falta: {campo}")
```

### Erro: "Resposta correta não está nas alternativas"
```
❌ Questão descartada: resposta_correta não está em alternativas
```
**Solução:**
```python
# Garantir que resposta_correta é uma chave válida
questao = {
    ...
    "alternativas": {"A": "...", "B": "...", "C": "..."},
    "resposta_correta": "C"  # ✅ Deve estar em alternativas
}
```

### Erro: "Timeout ao enviar"
```
❌ Timeout: API levou mais de 30s
```
**Solução:**
```python
# Reduzir tamanho do lote
python agent_bridge.py --tamanho-lote 5  # Era 10

# Ou aumentar timeout na requisição (Python)
response = requests.post(url, json=payload, timeout=60)
```

---

## 📊 Monitoramento

### Verificar Total de Questões Inseridas

```bash
curl http://localhost:8000/info | grep questoes_banco
```

### Ver Questões por Concurso

```bash
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT concurso, COUNT(*) FROM questoes_banco GROUP BY concurso;"
```

### Ver Últimas Questões Inseridas

```bash
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT questao_id, concurso, materia, data_criacao FROM questoes_banco ORDER BY data_criacao DESC LIMIT 10;"
```

### Logs da API

```bash
docker logs backend_questoes -f --tail 50
```

---

## 🔒 Segurança em Produção

### Checklist de Segurança

- [ ] Mudar `API_KEY_INGESTAO` para uma chave forte (128+ bits)
- [ ] Usar HTTPS em vez de HTTP
- [ ] Limitar acesso via firewall/VPC (whitelist de IPs)
- [ ] Rate limiting na rota `/api/v1/ingest` (máx 100 requests/minuto)
- [ ] Monitorar logs para tentativas de acesso não autorizado
- [ ] Backup diário do PostgreSQL
- [ ] Validar dados de entrada com mais rigor

### Exemplo: Chave Forte

```bash
# Gerar chave aleatória
openssl rand -hex 32
# Output: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6

# Definir na variável de ambiente
export API_KEY_INGESTAO="a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"
```

---

## 📚 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Validation](https://docs.pydantic.dev/)
- [Crawl4AI GitHub](https://github.com/unclecode/crawl4ai)
- [PostgreSQL Bulk Insert](https://www.postgresql.org/docs/current/sql-insert.html)

---

**Última atualização:** 29/08/2024  
**Versão:** 1.0  
**Status:** Production-Ready ✅
