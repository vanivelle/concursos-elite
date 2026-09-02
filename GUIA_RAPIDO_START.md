# 🚀 GUIA RÁPIDO - COMEÇAR 24/7 OPENHANDS HOJE MESMO

## ⚡ 5 MINUTOS PARA INICIAR TUDO

### Passo 1: Preparar Ambiente (2 min)

```bash
# Navegar para projeto
cd "e:\Downloado D\games\fotos da vovo\IA\claude\protocolos\open-notebook"

# Criar arquivo .env
cat > .env << 'EOF'
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=Lightshigaraki789
SUPABASE_URL=https://db.lnnwefppeaaqhpjqpdvz.supabase.co
SUPABASE_KEY=seu_chave_supabase_aqui
JWT_SECRET=sua_chave_secreta_super_segura_2024
OPENHANDS_LLM_MODEL=gpt-4
ENVIRONMENT=production
GRAFANA_PASSWORD=admin
EOF
```

### Passo 2: Iniciar Docker (1 min)

```bash
# Iniciar todos os serviços
docker-compose up -d

# Verificar status
docker-compose ps

# Esperado:
# postgres       - Up ✅
# redis          - Up ✅
# backend        - Up ✅
# openhands      - Up ✅
# langflow       - Up ✅
# crawl4ai       - Up ✅
# celery_worker  - Up ✅
# celery_beat    - Up ✅
```

### Passo 3: Verificar Tudo Rodando (1 min)

```bash
# Backend health
curl http://localhost:8000/health

# Resposta esperada:
# {"status":"online","timestamp":"2024-09-02T..."}

# OpenHands ready
curl http://localhost:3001/api/health

# Resposta esperada:
# {"status":"ok","version":"0.14.0"}
```

### Passo 4: Acessar Interfaces (1 min)

Abra estes links no navegador:

```
📊 Grafana (Dashboard)
   http://localhost:3000
   User: admin
   Password: admin

🤖 OpenHands (Agente)
   http://localhost:3001

🌊 Langflow (Workflows)
   http://localhost:7860

💾 Adminer (Banco Dados)
   http://localhost:8080
   Server: postgres
   User: postgres
   Password: Lightshigaraki789
   BD: postgres

📈 Prometheus (Métricas)
   http://localhost:9090

🌐 Backend Docs (API)
   http://localhost:8000/docs
```

## ✅ VERIFICAR SE FUNCIONANDO

### 1. Testar Backend

```bash
# Listar questões
curl -X GET "http://localhost:8000/api/questoes?limit=5"

# Resultado esperado: Array com questões
```

### 2. Monitorar Celery

```bash
# Terminal 1: Ver logs do worker
docker logs -f celery_worker

# Terminal 2: Ver logs do beat
docker logs -f celery-beat-concurso

# Esperado:
# [INFO/Worker-1] Ready to accept tasks
# [INFO/Beat] Scheduler: Adjusting
```

### 3. Flower - Dashboard Celery

```bash
# Instalar (se não tiver)
pip install flower

# Rodar
flower -A backend.tasks

# Acessar
http://localhost:5555
```

## 📅 VERIFICAR PRÓXIMA EXECUÇÃO

OpenHands vai executar em:

```
HOJE 05:00 - Atualizar Questões
HOJE 07:00 - Atualizar Atualidades
HOJE 12:00 - Analisar Padrões
HOJE 19:00 - Atualizar Redação
HOJE 22:00 - Sincronizar GitHub
HOJE 23:00 - Backup e Limpeza
```

Para forçar execução agora (teste):

```bash
# SSH no container
docker exec celery_worker python -c "
from backend.tasks import atualizar_questoes
resultado = atualizar_questoes()
print(resultado)
"
```

## 🐛 TROUBLESHOOTING RÁPIDO

### Backend não responde
```bash
docker logs backend
# Verifique DB_PASSWORD e DATABASE_URL
```

### OpenHands não conecta
```bash
docker logs openhands-concurso
# Verifique se PostgreSQL está rodando
docker logs postgres
```

### Celery não agenda
```bash
docker logs celery-beat-concurso
# Verifique se Redis está rodando
docker logs redis
```

### Supabase erro
```bash
# Teste conexão
psql postgresql://postgres:Lightshigaraki789@localhost:5432/postgres
```

## 📊 MONITORAR EM TEMPO REAL

### Opção 1: Logs em tempo real
```bash
# Ver tudo acontecendo
docker-compose logs -f

# Ou serviço específico
docker-compose logs -f backend
docker-compose logs -f openhands
docker-compose logs -f celery_worker
```

### Opção 2: Prometheus
```bash
# Acessar http://localhost:9090
# Query: rate(http_requests_total[1m])
```

### Opção 3: Grafana
```bash
# Acessar http://localhost:3000
# Dashboard: Sistema em tempo real
```

## 🎯 PRÓXIMAS AÇÕES

### 1. Hoje (Hoje)
- ✅ Docker-compose up -d
- ✅ Verificar status
- ✅ Testar endpoints
- ✅ Acessar dashboards

### 2. Amanhã
- Verificar se tasks rodaram
- Contar novas questões inseridas
- Analisar logs de execução
- Ajustar horários se necessário

### 3. Esta Semana
- Treinar OpenHands com tarefas reais
- Configurar alertas Telegram/Email
- Testar escalabilidade (mais workers)
- Deploy em produção (Railway/Coolify)

## 🔧 COMANDOS ÚTEIS

```bash
# Ver status
docker-compose ps

# Parar tudo
docker-compose down

# Remover volumes (CUIDADO!)
docker-compose down -v

# Ver logs de um serviço
docker logs -f [nome_servico]

# Executar comando em container
docker exec [nome_container] [comando]

# Reiniciar um serviço
docker-compose restart [nome_servico]

# Escalar workers
docker-compose up -d --scale celery_worker=3

# Backup BD
docker exec postgres pg_dump -U postgres postgres > backup.sql
```

## 📞 SUPORTE

Se algo não funcionar:

1. **Cheque os logs:** docker logs [serviço]
2. **Verifique conexão:** docker-compose ps
3. **Teste endpoint:** curl http://localhost:8000/health
4. **Reinicie:** docker-compose restart [serviço]
5. **Last resort:** docker-compose down -v && docker-compose up -d

## ✨ RESULTADO ESPERADO

Após 5 minutos:

```
┌─────────────────────────────────────────────────────┐
│  ✅ SISTEMA RODANDO 24/7                            │
│                                                     │
│  ✅ Backend respondendo                             │
│  ✅ Banco de dados online                           │
│  ✅ OpenHands pronto para trabalhar                │
│  ✅ Celery agendando tarefas                        │
│  ✅ Langflow orquestrando                           │
│  ✅ Crawl4AI pronto para raspar                    │
│  ✅ Dashboards acessíveis                           │
│                                                     │
│  05:00 → Atualizar questões                        │
│  12:00 → Analisar padrões                          │
│  19:00 → Atualizar redação                         │
│  23:00 → Backup                                    │
│                                                     │
│  🤖 OPENHANDS TRABALHANDO... 🤖                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🎉 SUCESSO!

Você agora tem um **sistema autônomo 24/7** que:

- ✅ Mantém dados sempre atualizados
- ✅ Raspa questões automaticamente
- ✅ Analisa padrões em background
- ✅ Gera relatórios semanais
- ✅ Faz backups automáticos
- ✅ Sincroniza com GitHub
- ✅ Monitora saúde 24/7
- ✅ Escala conforme necessário

**Você estuda. OpenHands trabalha. Win-win!** 🚀

---

**Criado em:** 2024-09-02
**Versão:** 4.0 (OpenHands + Automação Completa)
**Status:** ✅ PRONTO PARA DEPLOY
