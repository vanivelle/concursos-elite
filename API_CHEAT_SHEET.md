# 🎯 API CHEAT SHEET - Referência Rápida

## 📍 Endpoint
```
POST http://localhost:8000/api/v1/ingest
```

## 🔐 Headers Obrigatórios
```
Content-Type: application/json
X-API-KEY: elite-concursos-hunter-2024
```

---

## 📤 REQUEST MÍNIMO

```json
{
  "questoes": [
    {
      "concurso": "Banco Central (Bacen)",
      "materia": "Português",
      "banca": "ESAF",
      "dificuldade": "Médio",
      "tipo": "Múltipla Escolha",
      "enunciado": "O que é?",
      "alternativas": {
        "A": "A", "B": "B", "C": "C", "D": "D"
      },
      "resposta_correta": "C",
      "explicacao": "Porque...",
      "pegadinha_banca": "..."
    }
  ]
}
```

---

## 📥 RESPONSE SUCESSO (200)

```json
{
  "status": "sucesso",
  "total_inserido": 1,
  "total_no_banco": 21,
  "timestamp": "2026-08-29T20:13:24.609005",
  "detalhes": {
    "tentativas": 1,
    "sucesso": 1,
    "erros": 0,
    "mensagens_erro": null
  }
}
```

---

## 🚨 RESPONSE ERRO (401)

```json
{
  "detail": "❌ API-KEY inválida. Acesso negado à ingestão."
}
```

---

## 🔤 VALORES VÁLIDOS

### Concursos
- `"Banco Central (Bacen)"`
- `"Transpetro (Petrobras)"`
- `"PMDF"`

### Matérias
- `"Português"`
- `"Direito Administrativo"`
- `"Conhecimentos Gerais"`
- `"Direito Penal"`
- `"Logística"`

### Bancas
- `"ESAF"`
- `"Cesgranrio"`
- `"CEBRASPE"`

### Dificuldade
- `"Fácil"`
- `"Médio"`
- `"Difícil"`

### Tipo
- `"Múltipla Escolha"`
- `"Certo/Errado"`
- `"Discursiva"`

---

## 💻 EXEMPLOS RÁPIDOS

### cURL
```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "X-API-KEY: elite-concursos-hunter-2024" \
  -H "Content-Type: application/json" \
  -d '{"questoes":[{"concurso":"Banco Central (Bacen)","materia":"Português","banca":"ESAF","dificuldade":"Médio","tipo":"Múltipla Escolha","enunciado":"?","alternativas":{"A":"a","B":"b","C":"c","D":"d"},"resposta_correta":"C","explicacao":"x","pegadinha_banca":"y"}]}'
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/ingest",
    headers={"X-API-KEY": "elite-concursos-hunter-2024"},
    json={
        "questoes": [{
            "concurso": "Banco Central (Bacen)",
            "materia": "Português",
            "banca": "ESAF",
            "dificuldade": "Médio",
            "tipo": "Múltipla Escolha",
            "enunciado": "Qual é?",
            "alternativas": {"A": "A", "B": "B", "C": "C", "D": "D"},
            "resposta_correta": "C",
            "explicacao": "Porque...",
            "pegadinha_banca": "..."
        }]
    }
)
print(response.json())
```

### JavaScript
```javascript
fetch("http://localhost:8000/api/v1/ingest", {
  method: "POST",
  headers: {
    "X-API-KEY": "elite-concursos-hunter-2024",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    questoes: [{
      concurso: "Banco Central (Bacen)",
      materia: "Português",
      banca: "ESAF",
      dificuldade: "Médio",
      tipo: "Múltipla Escolha",
      enunciado: "Qual é?",
      alternativas: {"A":"A", "B":"B", "C":"C", "D":"D"},
      resposta_correta": "C",
      explicacao: "Porque...",
      pegadinha_banca: "..."
    }]
  })
})
.then(r => r.json())
.then(data => console.log(data))
```

---

## 📋 CAMPOS OBRIGATÓRIOS

| Campo | Tipo | Exemplo |
|-------|------|---------|
| `concurso` | String | "Banco Central (Bacen)" |
| `materia` | String | "Português" |
| `banca` | String | "ESAF" |
| `dificuldade` | String | "Médio" |
| `tipo` | String | "Múltipla Escolha" |
| `enunciado` | String | "Qual é..." |
| `alternativas` | Object | `{"A":"","B":"","C":"","D":""}` |
| `resposta_correta` | String | "C" |
| `explicacao` | String | "Porque..." |
| `pegadinha_banca` | String | "..." |

---

## ⚙️ CAMPOS OPCIONAIS

| Campo | Tipo | Default |
|-------|------|---------|
| `questao_id` | String | Auto-gerado |

---

## 🐛 ERROS COMUNS

| Erro | Causa | Solução |
|------|-------|---------|
| 401 Unauthorized | API-KEY inválida | Usar `elite-concursos-hunter-2024` |
| 422 Validation | Campo obrigatório faltando | Ver [CAMPOS OBRIGATÓRIOS](#campos-obrigatórios) |
| Connection refused | API offline | `docker-compose up -d` |
| "resposta_correta não está" | Gabarito não está em alternativas | Verificar chaves A/B/C/D |
| Timeout | Lote muito grande | Usar `--tamanho-lote 5` |

---

## ⚡ OTIMIZAÇÕES

### Melhor Performance
```
- Tamanho ideal de lote: 10-20 questões
- Timeout recomendado: 30 segundos
- Max alternativas: 5 (A-E)
- Max caracteres enunciado: 5000
```

### Erros Esperados
```
- Duplicata detectada (questao_id já existe): 0 inserido
- Campo inválido: questão descartada
- API-KEY errada: 401 Forbidden
```

---

## 📊 STATUS CODES

| Código | Significado |
|--------|-------------|
| 200 | ✅ Sucesso (pode ter erros parciais) |
| 401 | ❌ API-KEY inválida |
| 422 | ❌ Validação Pydantic falhou |
| 500 | ❌ Erro interno do servidor |

---

## 🔍 VALIDAÇÕES AUTOMÁTICAS

```
✅ concurso: Deve estar na lista de concursos
✅ banca: Deve estar em formato de string
✅ alternativas: Deve ser Object com chaves A-E
✅ resposta_correta: Deve estar em alternativas
✅ campos de texto: Mínimo 10 caracteres
✅ questao_id (se fornecido): Deve ser único
```

---

## 🎯 CASOS DE USO

### Ingerir 1 Questão
```python
# Python
response = requests.post("http://localhost:8000/api/v1/ingest", 
  headers={"X-API-KEY": "elite-concursos-hunter-2024"},
  json={"questoes": [QUESTAO_DICT]})
```

### Ingerir 100 Questões (em lotes)
```python
# Python
for i in range(0, 100, 10):
    lote = questoes[i:i+10]
    response = requests.post(
      "http://localhost:8000/api/v1/ingest",
      headers={"X-API-KEY": "elite-concursos-hunter-2024"},
      json={"questoes": lote}
    )
    print(f"Lote {i//10}: {response.json()['total_inserido']} inseridas")
```

### Usar Agent Bridge (Recomendado)
```bash
python backend/agent_bridge.py --concurso "Banco Central (Bacen)" --modo local
```

---

## 🚀 MODO LOCAL vs SCRAPER

### Modo Local (Padrão)
```bash
python backend/agent_bridge.py --concurso "Banco Central (Bacen)" --modo local
# Usa 2 questões hardcoded de teste
```

### Modo Scraper (Futuro)
```bash
python backend/agent_bridge.py --concurso "Transpetro (Petrobras)" --modo scraper
# Integrado com Crawl4AI (em desenvolvimento)
```

### Modo Hybrid
```bash
python backend/agent_bridge.py --modo hybrid
# Local + Scraper (em desenvolvimento)
```

---

## 📞 SUPORTE

- **Documentação Completa:** [API_INGESTAO.md](API_INGESTAO.md)
- **Exemplos Detalhados:** [API_INGESTAO.md#exemplos-de-uso](API_INGESTAO.md#exemplos-de-uso)
- **Troubleshooting:** [API_INGESTAO.md#troubleshooting](API_INGESTAO.md#troubleshooting)
- **Começar Rápido:** [QUICK_START.md](QUICK_START.md)

---

**V1.0 - Production Ready** ✅  
[← Voltar ao INDEX](INDEX.md)
