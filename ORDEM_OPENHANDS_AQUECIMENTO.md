# 🤖 ORDEM AUTÔNOMA PARA OPENHANDS - OPERAÇÃO AQUECIMENTO
**Data:** 2026/08/29 | **Alvo:** 300 Questões de Elite | **Status:** ATIVO

---

## 📋 MISSÃO EXECUTIVA (Copie e Cole no OpenHands UI)

```
OpenHands, atue como um Engenheiro de Dados Sênior e Especialista em Web Scraping.

MISSÃO PRIMÁRIA: Aquecer o banco PostgreSQL local com dados reais de concursos públicos.

PARÂMETROS:
- Alvo Total: 300 questões gabaritadas
- Distribuição: 100 (Bacen/ESAF) + 100 (Transpetro/Cesgranrio) + 100 (PMDF/Cebraspe)
- API Local: http://docker.internal:8000/api/v1/ingest (autenticação: X-API-KEY=elite-concursos-hunter-2024)
- Banco PostgreSQL: postgres_concursos via Docker local
- Ollama: http://docker.internal:11434 (modelo gemma2:2b)

PROTOCOLO DE EXECUÇÃO:

1. **ETAPA 1: Setup de Ferramentas**
   - Instale localmente: pip install crawl4ai requests beautifulsoup4 selenium
   - Verifique conectividade: curl http://docker.internal:8000/health
   - Confirme Ollama online: curl http://docker.internal:11434/api/tags

2. **ETAPA 2: Extração de Dados Reais (Crawl4AI)**
   Use estes portais públicos como fonte:
   
   a) **Banco Central (Bacen):**
      - Fonte: qconcursos.com (filtro: Bacen, banca ESAF)
      - Formato: HTML tables com questões gabaritadas
      - Extrator: Selênio + BeautifulSoup para capturar <tr> com questão/alternativas/gabarito
      - Target: 100 questões de Direito Administrativo + Português + Conhecimentos Gerais
   
   b) **Transpetro (Cesgranrio):**
      - Fonte: cesgranrio.org.br/concursos (seção Transpetro histórico)
      - Formato: PDF scanneado → OCR com pytesseract
      - Extrator: Pypdf2 + tesseract para extrair texto de provas antigas
      - Target: 100 questões de Português técnico + Logística + Conhecimentos Gerais
   
   c) **PMDF (Cebraspe):**
      - Fonte: cebraspe.org.br/concursos (PMDF histórico)
      - Formato: HTML estruturado com itens Certo/Errado
      - Extrator: Crawl4AI async para página por página
      - Target: 100 questões de Direito Penal + Direito Administrativo

3. **ETAPA 3: Normalização de Dados**
   Para cada questão extraída, normalize:
   ```python
   {
     "concurso": "Banco Central (Bacen)",
     "materia": "Direito Administrativo",
     "banca": "ESAF",
     "dificuldade": "Médio",  # Inferir de tags ou contexto
     "tipo": "Múltipla Escolha",
     "enunciado": "Texto completo da questão",
     "alternativas": {
       "A": "Opção A completa",
       "B": "Opção B completa",
       "C": "Opção C completa (GABARITO)",
       "D": "Opção D completa"
     },
     "resposta_correta": "C",
     "explicacao": "Texto da explicação oficial (se disponível)",
     "pegadinha_banca": "Padrão de erro comum nesta banca"
   }
   ```

4. **ETAPA 4: Enriquecimento com Ollama (Opcional)**
   Para cada questão normalizada, chame Ollama para gerar:
   ```bash
   curl -X POST http://docker.internal:11434/api/generate \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gemma2:2b",
       "prompt": "Analise a questão: [QUESTÃO]. Retorne JSON com diagnostico_erro e nucleo_acerto",
       "stream": false
     }'
   ```
   Extraia e injete os campos `diagnostico_erro` e `nucleo_acerto` na questão.

5. **ETAPA 5: Ingestão em Lote (Bulk Insert)**
   Agrupe questões em lotes de 50-100 e execute:
   ```bash
   curl -X POST http://docker.internal:8000/api/v1/ingest \
     -H "X-API-KEY: elite-concursos-hunter-2024" \
     -H "Content-Type: application/json" \
     -d '{
       "questoes": [
         {questão 1 normalizada},
         {questão 2 normalizada},
         ...
       ]
     }'
   ```
   Monitore retorno: "total_inserido" deve ser igual ao tamanho do lote.
   Se houver erros, log-os e continue com próximo lote.

6. **ETAPA 6: Validação Pós-Ingestão**
   Confirme: curl http://docker.internal:8000/info | grep questoes_banco
   Alvo: questoes_banco >= 300

TIMELINE:
- Extração de dados: ~10-15min (paralelo com 3 fontes)
- Enriquecimento IA: ~5-8min (opcional, pode pular se muito lento)
- Ingestão lote: ~2-3min (1000 Q/s com bulk_insert_mappings)
- **Total estimado: 20-30 minutos**

CONFIGURAÇÕES DE RETRY:
- Timeout conexão: 30s
- Retry automático: 3 tentativas por lote
- Backoff exponencial: 2s, 4s, 8s

OUTPUTS ESPERADOS:
- ✅ stdout: Logs de progresso (uma linha por 50 questões)
- ✅ stderr: Erros específicos (questões que falharam)
- ✅ Exit code 0: Sucesso (>=300 questões no banco)
- ❌ Exit code 1: Falha (menos de 300 questões)

STOP CONDITION:
Parar automaticamente quando:
- tabela questoes_banco.count() >= 300, OU
- Fila de extração vazia + ingestão completada

Após conclusão, reporte:
- Total questões inseridas
- Distribuição por concurso
- Tempo total de execução
- Taxa de sucesso (%)
```

---

## 🔧 Alternativa: Script Python Local

Se OpenHands estiver lento, execute diretamente no seu PowerShell:

```powershell
cd "e:\Downloado D\games\fotos da vovo\IA\claude\protocolos\open-notebook"
python openhands_ingestao_protocolo.py
```

Este script já é uma implementação funcional (com questões mockup). Para ativar Crawl4AI real:

1. Descomente as linhas de `enriquecer_questao_com_ia()`
2. Substitua `gerar_questoes_mockup()` com chamadas de Crawl4AI real
3. Execute novamente

---

## 📊 Métricas Esperadas Após Conclusão

```
✅ Performance:
- Velocidade ingestão: 300 Q em <3min (100 Q/min = 1.67 Q/s)
- Latência query: <57ms (indexado por questao_id, concurso)
- Espaço disco: ~30-50MB (300 questões + índices)

✅ Distribuição no Banco:
- Bacen: 100 (33%)
- Transpetro: 100 (33%)
- PMDF: 100 (33%)

✅ Rota GET /gerar-questao:
- Antes: Retorna 15 questões (mockup)
- Depois: Sorteia de pool de 300 reais
- Latência: <100ms ✅

✅ Testes Validação:
- 7/7 testes ainda passando
- Database test: questoes_banco.count() = 300 ✅
```

---

## ⚠️ Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| `Connection refused: API` | Backend offline | `docker ps` e `docker-compose up -d` |
| `401 Unauthorized` | X-API-KEY incorreta | Verificar env var `API_KEY_INGESTAO` |
| `UNIQUE constraint failed` | Questão duplicada | Usar `questao_id` único com timestamp |
| `Timeout 30s` | Ollama muito lento | Pular enriquecimento IA (etapa 4) |
| `PostgreSQL connection error` | Banco desligado | Reiniciar container: `docker restart postgres_concursos` |

---

## 🎖️ Autorização para Execução

**Soldado, esta missão é CRÍTICA.**

Você tem carta branca para:
- ✅ Extrair dados de portais públicos (QConcursos, Cesgranrio, Cebraspe)
- ✅ Modificar scripts de ingestão conforme necessário
- ✅ Ativar Ollama 24/7 durante raspagem
- ✅ Aumentar pool de conexões PostgreSQL se necessário

**Limitações:**
- ❌ Não extrair dados de plataformas pagas (Estratégia Concursos, etc)
- ❌ Respeitar robots.txt dos portais
- ❌ Não paralelizar mais de 3 conexões simultâneas (não sobrecarregar servidores)

---

**ORDEM APROVADA:** 2026/08/29 | **PRIORIDADE:** MÁXIMA | **CUSTOIA:** $0
**Assinado:** Claude Haiku 4.5 (Agent Tier 1)
