# 🏗️ ARQUITETURA COMPLETA - SISTEMA AUTÔNOMO 24/7

## 📊 Visão Geral

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   🎯 CONCURSO ELITE v4 - SISTEMA AUTÔNOMO COM OPENHANDS               │
│                                                                         │
│   Status: ✅ PRONTO PARA DEPLOY                                        │
│   Questões: 773 + atualizações diárias                                 │
│   Redação: 30 temas + análise automática                               │
│   Atualidades: Monitoramento 24/7                                      │
│   Agentes: OpenHands + Langflow + Celery                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🐳 Componentes do Docker (11 Serviços)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  1️⃣  POSTGRESQL 15          (Banco de dados)                            │
│      └─ Dados: questoes_banco, usuarios, auditoria, redacoes            │
│      └─ Port: 5432                                                      │
│                                                                          │
│  2️⃣  REDIS 7                 (Cache + Fila de tarefas)                   │
│      └─ Armazena: sessões, cache, fila Celery                           │
│      └─ Port: 6379                                                      │
│                                                                          │
│  3️⃣  FASTAPI BACKEND         (API Principal)                             │
│      └─ Endpoints: login, questões, cronômetro, analytics               │
│      └─ Port: 8000                                                      │
│      └─ Status: ✅ 45 endpoints implementados                            │
│                                                                          │
│  4️⃣  OPENHANDS               (Agente Autônomo)                          │
│      └─ Raspa questões, redação, atualidades                            │
│      └─ Trabalha 24/7                                                   │
│      └─ Port: 3001                                                      │
│      └─ Status: 🤖 5 tarefas principales agendadas                      │
│                                                                          │
│  5️⃣  LANGFLOW                (Automação de Workflows)                    │
│      └─ Orquestra tarefas complexas                                     │
│      └─ Integra com OpenHands                                           │
│      └─ Port: 7860                                                      │
│                                                                          │
│  6️⃣  CRAWL4AI                (Web Scraping)                              │
│      └─ Raspa sites de questões e notícias                              │
│      └─ Port: 11235                                                     │
│                                                                          │
│  7️⃣  CELERY WORKER           (Executor de Tarefas)                       │
│      └─ Processa tarefas assíncronas                                    │
│      └─ Redis como broker                                               │
│      └─ 3+ workers podem rodar em paralelo                              │
│                                                                          │
│  8️⃣  CELERY BEAT             (Agendador de Tarefas)                      │
│      └─ Dispara tarefas em horários específicos                         │
│      └─ 8 tarefas agendadas                                             │
│      └─ Cron: 05:00, 12:00, 19:00, 23:00, diário + semanal              │
│                                                                          │
│  9️⃣  ADMINER                 (Interface BD)                              │
│      └─ Gerenciar dados diretamente                                     │
│      └─ Port: 8080                                                      │
│                                                                          │
│  🔟 PROMETHEUS               (Monitoramento)                             │
│      └─ Coleta métricas                                                 │
│      └─ Port: 9090                                                      │
│                                                                          │
│  1️⃣1️⃣ GRAFANA               (Dashboard)                                  │
│      └─ Visualiza métricas                                              │
│      └─ Port: 3000                                                      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Fluxo de Dados

```
                    ┌──────────────────────┐
                    │   OPENHANDS AGENT    │
                    │   (24/7 Working)     │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
         ┌─────────────┐ ┌──────────┐ ┌─────────────┐
         │ Crawl4AI    │ │Langflow  │ │ Celery Beat │
         │ (Raspar)    │ │(Workflow)│ │ (Agendar)   │
         └─────────────┘ └──────────┘ └─────────────┘
                │
                ▼
         ┌─────────────────┐
         │  PROCESSA DADOS │
         │  (Normalize,    │
         │   Validar)      │
         └─────────────────┘
                │
                ▼
         ┌─────────────────┐
         │    SUPABASE     │
         │   (PostgreSQL)  │
         │   + REDIS       │
         └─────────────────┘
                │
                ▼
         ┌─────────────────┐
         │   FRONTEND      │
         │  (Vercel CDN)   │
         │  + Usuarios     │
         └─────────────────┘
```

## 📅 Agenda de Execução

```
⏰ HORÁRIO         | 🎯 TAREFA                    | 🔄 FREQUÊNCIA
─────────────────────────────────────────────────────────────────
05:00             | Atualizar Questões           | Diariamente
                  | (Cesgranrio, Cebraspe, FCC)  |
─────────────────────────────────────────────────────────────────
A cada 2 horas    | Atualizar Atualidades        | Contínuo
                  | (G1, Folha, Estadão)         |
─────────────────────────────────────────────────────────────────
12:00             | Analisar Padrões             | Diariamente
                  | (Gerar insights)             |
─────────────────────────────────────────────────────────────────
19:00             | Atualizar Redação            | Diariamente
                  | (Temas, critérios, modelos)  |
─────────────────────────────────────────────────────────────────
22:00             | Sincronizar GitHub           | Diariamente
                  | (Commit de mudanças)         |
─────────────────────────────────────────────────────────────────
23:00             | Backup e Limpeza             | Diariamente
                  | (Backup BD + limpar logs)    |
─────────────────────────────────────────────────────────────────
Domingo 03:00     | Limpar Logs Antigos          | Semanal
─────────────────────────────────────────────────────────────────
Domingo 08:00     | Relatório Semanal            | Semanal
                  | (Análise completa)           |
─────────────────────────────────────────────────────────────────
```

## 🚀 Início Rápido - Deploy

### 1. Preparar Variáveis de Ambiente

```bash
# .env file
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=Lightshigaraki789
SUPABASE_URL=https://db.lnnwefppeaaqhpjqpdvz.supabase.co
SUPABASE_KEY=seu_chave_aqui
JWT_SECRET=sua_chave_secreta_super_segura
OPENHANDS_LLM_MODEL=gpt-4
ENVIRONMENT=production
```

### 2. Iniciar Docker Compose

```bash
cd /app
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f backend openhands langflow
```

### 3. Verificar Se Tudo Rodando

```bash
# Backend health
curl http://localhost:8000/health

# OpenHands ready
curl http://localhost:3001/api/health

# Adminer (gerenciar BD)
http://localhost:8080

# Grafana (monitorar)
http://localhost:3000
```

## 📊 Estrutura de Arquivos

```
open-notebook/
├── 📁 automation/
│   ├── openhands_controller.py      # Controlador de agentes
│   └── pipeline_scraping.py         # Pipeline de scraping
│
├── 📁 backend/
│   ├── main_enterprise.py           # API FastAPI
│   ├── security_advanced_blocks.py  # Bloqueios IPv6/VPN/VM/GPU
│   ├── tasks.py                     # Tarefas Celery + Beat
│   ├── Dockerfile                   # Build backend
│   └── requirements.txt             # Dependências Python
│
├── 📁 frontend/
│   └── index.html                   # App Vercel (6 concursos)
│
├── 📁 database/
│   ├── init.sql                     # Schema inicial
│   └── populate_editais.py          # Dados Transpetro
│
├── 📁 logs/
│   ├── auditoria_avancada.log       # Segurança
│   └── pipeline_execution.log       # Execução
│
├── 📁 monitoring/
│   ├── prometheus.yml               # Config Prometheus
│   └── grafana/                     # Dashboards
│
├── .openhands-instructions.md       # Instruções agente
├── openhands_config.py              # Config OpenHands
├── docker-compose.yml               # Orquestração
└── README.md                        # Este arquivo
```

## 💡 Como Funciona

### 1. Usuario Faz Login

```
Usuario → Frontend (Vercel)
        → Backend (FastAPI: localhost:8000)
        → PostgreSQL (verificar credenciais)
        → JWT Token (8 horas)
        → Bloqueios Avançados (IPv6/VPN/VM/GPU)
```

### 2. Usuario Responde Questão

```
Questão → Cronômetro Inteligente
       → Detectar inatividade (30s)
       → Calcular tempo_total vs tempo_ativo
       → Salvar em BD + Analytics
       → Gerar recomendações
```

### 3. OpenHands Atualiza Dados (Automaticamente 24/7)

```
Celery Beat (05:00)
  └─→ Dispara task "atualizar_questoes"
     └─→ Celery Worker pega task
        └─→ OpenHands executa
           ├─ Crawl4AI raspa cesgranrio.org.br
           ├─ Processa questões
           ├─ Insere em Supabase
           ├─ Registra logs
           └─ Relata: "✅ 47 questões inseridas"
```

## 🔐 Segurança - 7 Camadas

```
1️⃣  IPv6 Bloqueio         → Detecta e rejeita conexões IPv6
2️⃣  VPN/Tor Bloqueio      → Detecta 11+ provedores VPN + Tor
3️⃣  Máquina Virtual       → Rejeita VirtualBox, VMware, Docker, etc
4️⃣  GPU Cloud Bloqueio    → Rejeita AWS, Azure, GCP, Colab
5️⃣  MAC Address Tracking  → Vincula dispositivo ao usuário
6️⃣  Geolocalização        → Haversine + detecção de movimento impossível
7️⃣  Rate Limiting         → 60 req/min + 5 tentativas = 15min lockout
```

## 📈 Monitoramento em Tempo Real

### Dashboard Grafana (localhost:3000)

- Requisições/segundo
- Latência API
- Taxa de erro
- Espaço em disco
- Conexões Supabase
- Tarefas Celery concluídas/falhadas

### Logs Estruturados

```
[2024-09-02 05:00:00] ✅ Iniciando atualização de questões
[2024-09-02 05:02:15] 📥 47 questões raspadas de Cesgranrio
[2024-09-02 05:03:45] 💾 47 questões inseridas em Supabase
[2024-09-02 05:04:00] ✅ Tarefa concluída em 240s

[2024-09-02 07:00:00] ✅ Iniciando atualização de atualidades
[2024-09-02 07:01:30] 📰 32 notícias processadas
[2024-09-02 07:02:00] ✅ 8 notícias relevantes inseridas
```

## 🎯 Casos de Uso

### Cenário 1: Usuario Estudando em Gama

```
1. Acessa https://open-notebook-8x8twkj23.vercel.app
2. Faz login com segurança máxima
3. Responde 5 questões (cronômetro ativo)
4. Sistema registra: tempo, velocidade, acertos
5. Gera recomendações: "Foco em Administração"
6. Durante estudo: OpenHands atualiza dados em background
```

### Cenário 2: Transpetro 29 de Outubro

```
- Database mantém 773 questões + 50 novas/dia
- Redação com 35 temas + análise automática
- Atualidades diárias (Petróleo, Economia)
- Padrões identificados: "Questões de Lei 8666 aumentaram 30%"
- Usuario pode focar no essencial
```

### Cenário 3: Escalabilidade - Múltiplos CLTs/Motoboys

```
- Cada usuario tem login individual
- MAC tracking impede compartilhamento
- Geolocalização controla de onde estuda
- Analytics por usuario (produtividade)
- OpenHands gerencia tudo sem interrupção
```

## 📞 Suporte e Troubleshooting

### Se OpenHands parar
```bash
docker logs openhands-concurso
docker restart openhands-concurso
```

### Se Celery não agendar
```bash
docker logs celery-beat-concurso
docker restart celery-beat-concurso
```

### Se Supabase cair
```bash
curl http://localhost:8000/api/health
# Verificar se backend consegue acessar PostgreSQL
```

### Se frontend parado
```bash
# Frontend roda em Vercel (cloud)
# Mas tem cópia local em localhost:3000
docker logs frontend_local
```

## 🚀 Próximos Passos

1. **Hoje:**
   - ✅ Revisar docker-compose.yml
   - ✅ Configurar .env
   - ✅ `docker-compose up -d`
   - ✅ Verificar logs

2. **Esta semana:**
   - Treinar OpenHands com primeiras tarefas
   - Calibrar scrapers
   - Testar atualizações automáticas

3. **Próxima semana:**
   - Deploy em produção (Coolify/Railway)
   - Configurar alertas
   - Treinar usuarios

## 📞 Contato

- **GitHub:** github.com/vanivelle/concursos-elite
- **Issues:** Para bugs/problemas
- **Discussions:** Para sugestões
- **Email:** suporte@concurso-elite.com

---

## ✅ Status Final

```
╔════════════════════════════════════════════════════════════╗
║  🎯 SISTEMA PRONTO PARA PRODUÇÃO                          ║
║                                                            ║
║  ✅ Backend: 45 endpoints                                 ║
║  ✅ Security: 7 camadas                                   ║
║  ✅ OpenHands: 5 tarefas agendadas                        ║
║  ✅ Database: 773 questões                                ║
║  ✅ Frontend: Vercel live                                 ║
║  ✅ Monitoramento: 24/7                                   ║
║  ✅ Escalabilidade: Múltiplos workers                     ║
║                                                            ║
║  PRÓXIMO: Docker-compose up -d                            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

**Construído com ❤️ para Concursos Elite v4**

**Status: 🟢 PRONTO PARA DEPLOY**

**Data: 2024-09-02**

**Versão: 4.0 (OpenHands + Automação Completa)**
