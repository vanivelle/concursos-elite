# 🚀 QUICK START - API de Ingestão

## 30 Segundos para Começar

### 1️⃣ Verificar Sistema
```bash
curl http://localhost:8000/health
```
Esperado: `{"status":"OK"}`

### 2️⃣ Testar Ingestão (Bacen)
```bash
python backend/agent_bridge.py --concurso "Banco Central (Bacen)" --modo local
```
Esperado: `✅ 2 questões inseridas` | Total: 17

### 3️⃣ Verificar Banco
```bash
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT COUNT(*) FROM questoes_banco;"
```
Esperado: `17`

---

## Todos os Comandos Úteis

### Sistema
| Comando | Resultado |
|---------|-----------|
| `docker-compose up -d` | Iniciar tudo |
| `docker-compose down` | Parar tudo |
| `docker logs backend_questoes -f` | Ver logs (Ctrl+C para sair) |
| `curl http://localhost:8000/info` | Ver estatísticas |

### Agent Bridge
```bash
# Bacen
python backend/agent_bridge.py --concurso "Banco Central (Bacen)" --modo local

# Transpetro  
python backend/agent_bridge.py --concurso "Transpetro (Petrobras)" --modo local

# PMDF
python backend/agent_bridge.py --concurso "PMDF" --modo local

# Com arquivo JSON
python backend/agent_bridge.py --arquivo meu_arquivo.json --tamanho-lote 10
```

### Banco de Dados
```bash
# Total de questões
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT COUNT(*) FROM questoes_banco;"

# Por concurso
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT concurso, COUNT(*) FROM questoes_banco GROUP BY concurso;"

# Últimas 5
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT questao_id, materia, banca FROM questoes_banco ORDER BY data_criacao DESC LIMIT 5;"
```

### API (cURL)
```bash
# Health check
curl http://localhost:8000/health

# Estatísticas
curl http://localhost:8000/info

# Ingerir 1 questão
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "X-API-KEY: elite-concursos-hunter-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "questoes": [{
      "concurso": "Banco Central (Bacen)",
      "materia": "Português",
      "banca": "ESAF",
      "dificuldade": "Médio",
      "tipo": "Múltipla Escolha",
      "enunciado": "Qual é a questão?",
      "alternativas": {"A": "Opção A", "B": "Opção B", "C": "Opção C", "D": "Opção D"},
      "resposta_correta": "B",
      "explicacao": "Porque...",
      "pegadinha_banca": "A banca tenta..."
    }]
  }'
```

---

## 📊 Status Atual

| Item | Status |
|------|--------|
| API | ✅ Online |
| PostgreSQL | ✅ 17 questões |
| Agent Bridge | ✅ Funcional |
| Documentação | ✅ Completa |
| Testes E2E | ✅ Passando |

---

## 📚 Documentação Completa

- **[API_INGESTAO.md](API_INGESTAO.md)** - Guia técnico completo (350+ linhas)
- **[IMPLEMENTACAO_INGESTAO.md](IMPLEMENTACAO_INGESTAO.md)** - Resumo de implementação
- **[ARQUITETURA.md](ARQUITETURA.md)** - Visão geral técnica
- **[GUIA_DE_USO.md](GUIA_DE_USO.md)** - Manual operacional

---

## ⚡ Próximo Passo?

**Integrar Crawl4AI**
```bash
pip install crawl4ai

# Modificar agent_bridge.py para modo scraper real
# Depois: python backend/agent_bridge.py --modo scraper
```

**Ou usar com OpenHands**
- Copiar agent_bridge.py para agente OpenHands
- Usar `ClienteIngestao` como importação
- Executar 24/7 em background

---

**V1.0 - Ready for Production** ✅
