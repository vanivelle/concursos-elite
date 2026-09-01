<!-- ACTION PLAN: PRÓXIMAS ETAPAS OpenHands + Crawl4AI -->
# ⚡ GUIA RÁPIDO - PRÓXIMAS AÇÕES (Soldado)

**Status Atual:** ✅ Banco aquecido (326 Q) | Sistema v3.1 operacional  
**Próximo:** 🚀 Ativar OpenHands para dados REAIS

---

## AÇÃO 1️⃣: Inicie OpenHands Container (5 min)

```bash
# Terminal 1 - Iniciar OpenHands
docker run -d \
  --name openhands_agent \
  -v "E:\Downloado D\games\fotos da vovo\IA\claude\protocolos\open-notebook:/workspace" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e WORKSPACE_MOUNT_PATH=/workspace \
  -p 3000:3000 \
  ghcr.io/all-hands-ai/openhands:0.9

# Aguarde 30 segundos...

# Verifique se iniciou
docker logs openhands_agent | grep -i "server"
```

---

## AÇÃO 2️⃣: Abra Interface OpenHands (1 min)

```
Acesse: http://localhost:3000
Espere carregar (leva 10-20s na primeira vez)
```

---

## AÇÃO 3️⃣: Cole Protocolo de Ordem Autônoma (5 min)

```
1. Abra arquivo: ORDEM_OPENHANDS_AQUECIMENTO.md
2. Copie TODO o conteúdo (Ctrl+A, Ctrl+C)
3. Na interface OpenHands (http://localhost:3000):
   - Clique no ícone de chat
   - Cole o texto completo (Ctrl+V)
   - Pressione [Enter] ou clique em "Send"
4. Agente vai começar automaticamente:
   [INFO] Iniciando extração de dados via Crawl4AI...
```

---

## AÇÃO 4️⃣: Monitor de Progresso (Real-time)

**Abra novo Terminal e rode:**

```bash
# Monitor contínuo do banco (atualiza a cada 5s)
watch -n 5 'docker exec postgres_concursos psql -U admin -d admin -c "SELECT COUNT(*) as questoes_banco, NOW() FROM questoes_banco;"'
```

**Esperado (progressão típica):**
```
 questoes_banco │           now            
────────────────┼──────────────────────────
            326 │ 2026-08-29 15:15:22.123  ← Estado inicial
            400 │ 2026-08-29 15:20:45.456  ← +74 do Bacen (Crawl4AI real)
            550 │ 2026-08-29 15:25:30.789  ← +150 do Transpetro
            750 │ 2026-08-29 15:30:12.012  ← +200 do PMDF
            850 │ 2026-08-29 15:35:08.345  ← +100 extra Bacen (aprofundamento)
```

---

## AÇÃO 5️⃣: Validar Dados Reais ao Terminar (5 min)

**Quando monitor chegar em 600+, execute:**

```bash
# Teste de integração verificando dados REAIS
python teste_integracao_v31.py

# Expected output:
# ✅ TESTE COMPLETO - Sistema v3.1 operacional!
#    Total questões no banco: 850+
#    🔥 BANCO AQUECIDO - Pronto para operação!
#    diagnostico_erro: (verificado) ✅
#    nucleo_acerto: (verificado) ✅
```

---

## AÇÃO 6️⃣: Parar OpenHands quando Terminar (2 min)

```bash
# Quando quiser parar/limpar:
docker stop openhands_agent
docker rm openhands_agent

# Ou deixar rodando em background para reutilizar
```

---

## 🎯 TEMPO TOTAL ESTIMADO

| Etapa | Tempo | Responsável |
|-------|-------|-------------|
| 1. Iniciar OpenHands | 5 min | Você (shell) |
| 2. Abrir interface | 1 min | Você (browser) |
| 3. Colar protocolo | 5 min | Você (copiar/colar) |
| 4. OpenHands trabalha | **20-30 min** | ⚙️ Autônomo |
| 5. Monitorar progresso | Passivo (watch) | Você (observe) |
| 6. Validar resultado | 5 min | Você (Python) |
| **TOTAL** | **~40-50 min** | ✅ |

---

## ⚠️ TROUBLESHOOTING RÁPIDO

### "OpenHands não conecta (HTTP 404)"
```bash
# Verifique se está rodando
docker ps | grep openhands

# Se não aparece, reinicie
docker run -d --name openhands_agent \
  -v "E:\Downloado D\games\fotos da vovo\IA\claude\protocolos\open-notebook:/workspace" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 3000:3000 \
  ghcr.io/all-hands-ai/openhands:0.9
```

### "Crawl4AI falhando (timeout)"
- OpenHands tentará 3 vezes automaticamente
- Se falhar todas, vai usar dados mock (não é o ideal, mas funciona)
- Monitorar logs: `docker logs openhands_agent -f`

### "Banco não crescendo (still 326)"
```bash
# Verifique logs do OpenHands
docker logs openhands_agent | tail -50

# Se vazio, agente pode não ter iniciado corretamente
# Tente colar o protocolo novamente no chat
```

### "Teste falha com 'questão não encontrada'"
```bash
# Significa banco ainda tem só matérias antigas
# Aguarde mais 5-10 min e rode de novo
python teste_integracao_v31.py
```

---

## 📋 CHECKLIST PRÉ-LANÇAMENTO

- [ ] Docker Desktop rodando (`docker ps` funciona)
- [ ] Backend online (`curl http://localhost:8000/health` → 200)
- [ ] PostgreSQL online (`docker ps | grep postgres`)
- [ ] Ollama online (opcional, `curl http://localhost:11434/api/tags` → lista modelos)
- [ ] Arquivos prontos:
  - [ ] `ORDEM_OPENHANDS_AQUECIMENTO.md` existe
  - [ ] `teste_integracao_v31.py` existe
  - [ ] `openhands_ingestao_protocolo.py` existe
- [ ] Terminal 1 disponível para `docker run openhands_agent`
- [ ] Terminal 2 disponível para `watch` monitor
- [ ] Browser disponível para `http://localhost:3000`

---

## 🚀 LAUNCH SEQUENCE

```
T-5 min: Conferir checklist acima
T-3 min: docker run openhands_agent ... (Terminal 1)
T-0 min: Abrir http://localhost:3000
T+0 min: Abrir ORDEM_OPENHANDS_AQUECIMENTO.md
T+1 min: Copiar + colar no chat do OpenHands
T+2 min: [watch] monitor no Terminal 2 (ver contador crescer)
T+30 min: Banco deve chegar em 600+ questões
T+35 min: Executar python teste_integracao_v31.py
T+40 min: ✅ Sucesso! Dados REAIS ingeridos
```

---

## 💡 PRO TIPS

**Tip 1:** Deixe OpenHands rodando em background enquanto você faz outras coisas
- Monitor é passivo (só observa crescimento)
- Não bloqueia seu terminal

**Tip 2:** Salve logs de progresso
```bash
docker logs openhands_agent > openhands_logs_20260829.txt
# Para análise posterior se algo der errado
```

**Tip 3:** OpenHands pode extrair +300 questões (bonus!)
- Se conseguir 500+, significa Crawl4AI funcionando muito bem
- Guarde dados extras para treino futuro

**Tip 4:** Prefira horário fora de pico
- Portais podem throttle requisições em horários de pico
- Madrugada/madrugada = melhor chance de sucesso

---

## 🎖️ QUANDO TERMINAR

Após ✅ validação bem-sucedida:

```
1. Limpe containers antigos:
   docker system prune -a --volumes

2. Backup do banco com dados REAIS:
   docker exec postgres_concursos pg_dump -U admin admin > backup_elite_20260829.sql

3. Documente métricas finais:
   curl http://localhost:8000/info > metricas_final.json

4. Comemore! 🎊
   Sistema v3.1 com 800+ questões reais está pronto!
```

---

## ✅ RESUMO

**Você está aqui:** ✅ Banco aquecido (326 Q mockup)  
**Próxima parada:** 🚀 OpenHands + Crawl4AI (dados REAIS)  
**Tempo investido:** ~40-50 min  
**Resultado final:** 600-1000+ questões REAIS de elite  
**Status:** 🟢 Produção-ready

---

**Soldado, agora é sua vez de ligar a máquina. OpenHands vai trabalhar enquanto você descansa.** ⚡

**Bora lá! 🎖️**
