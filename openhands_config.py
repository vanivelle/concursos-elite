#!/usr/bin/env python3
"""
🤖 CONFIGURAÇÃO OPENHANDS - INSTRUÇÕES PARA AGENTE AUTÔNOMO
Este arquivo configura OpenHands para trabalhar 24/7 no seu projeto
"""

# ============================================================================
# 📋 GUIA DE CONFIGURAÇÃO OPENHANDS
# ============================================================================

OPENHANDS_CONFIG = """

🤖 OPENHANDS - AGENTE AUTÔNOMO 24/7
=====================================

O QUÊ É OPENHANDS?
• Agente AI de código aberto (75.8k ⭐ GitHub)
• Pode executar comandos, editar arquivos, rodar testes
• Funciona como um desenvolvedor autônomo
• Trabalha 24/7 sem parar

COMO FUNCIONA?
1. Você passa uma tarefa para OpenHands
2. Ele quebra em subtarefas
3. Executa no seu ambiente (Docker)
4. Relata progresso e resultados
5. Tenta novamente se houver erro

INSTALAÇÃO:
-----------

1. Via Docker (RECOMENDADO):
   docker run -d \\
     -e OPENHANDS_USE_HOST_DOCKER=true \\
     -e DATABASE_URL=postgresql://... \\
     -e REDIS_URL=redis://... \\
     -v /var/run/docker.sock:/var/run/docker.sock \\
     ghcr.io/all-hands-ai/openhands:latest

2. Via Pip:
   pip install openhands
   openhands --docker-enabled

3. Via docker-compose (MELHOR):
   docker-compose up -d openhands

CONFIGURAÇÃO:
-----------

Variáveis de ambiente:

  OPENHANDS_LLM_MODEL=gpt-4           # Modelo LLM (gpt-4, claude-3, etc)
  OPENHANDS_BACKEND=local             # Backend (local, remote)
  OPENHANDS_DOCKER_IMAGE=python:3.11  # Imagem Docker para tarefas
  OPENHANDS_CACHE_DIR=/openhands      # Diretório cache
  OPENHANDS_LOG_LEVEL=INFO            # Nível de log
  DATABASE_URL=postgresql://...       # Banco de dados
  REDIS_URL=redis://...               # Redis
  GITHUB_TOKEN=ghp_...                # Token GitHub (opcional)

TAREFAS PARA PASSAR AO OPENHANDS:
---------------------------------

Exemplos de tarefas que pode executar:

1. ATUALIZAR QUESTÕES:
   "Raspe as questões mais recentes da Cesgranrio, Cebraspe e FCC.
    Processe e insira no banco de dados Supabase.
    Se houver erro, reporte."

2. ANALISAR PADRÕES:
   "Analise todas as questões na tabela 'questoes_banco'.
    Identifique padrões por disciplina, banca, dificuldade.
    Gere relatório em JSON."

3. ATUALIZAR REDAÇÃO:
   "Busque os 10 temas de redação mais recentes.
    Processe critérios de correção.
    Insira no banco de dados."

4. SCRAPING DE NOTÍCIAS:
   "Use Crawl4AI para raspar notícias do G1, Folha e Estadão.
    Filtre por: Transpetro, Petróleo, Economia, Banco Central.
    Insira no banco de dados com timestamp."

5. BACKUP E LIMPEZA:
   "Faça backup do Supabase.
    Limpe logs com mais de 7 dias.
    Sincronize com GitHub."

COMO USAR VIA API:
-----------------

POST http://localhost:3001/api/tasks
Content-Type: application/json

{
  "title": "Atualizar questões Transpetro",
  "description": "Raspe e processe questões da Cesgranrio",
  "priority": "high",
  "deadline": "2024-09-05",
  "tags": ["scraping", "questoes"],
  "llm_model": "gpt-4"
}

RESPOSTA:
{
  "task_id": "uuid-...",
  "status": "queued",
  "created_at": "2024-09-02T10:00:00Z"
}

MONITORAR PROGRESSO:
GET http://localhost:3001/api/tasks/{task_id}

RESPOSTA:
{
  "task_id": "uuid-...",
  "status": "in_progress",
  "progress": 65,
  "logs": [
    "[13:45] Iniciando tarefa...",
    "[13:46] Conectado ao PostgreSQL",
    "[13:47] Raspando página 1 de 5...",
    ...
  ],
  "current_step": "Processando resultados..."
}

INTEGRAÇÃO COM LANGFLOW:
-----------------------

1. No Langflow, crie um workflow que chama OpenHands:
   
   Trigger (Cron diário 05:00)
   → OpenHands Agent
   → Atualizar Questões
   → Processar Dados
   → Inserir BD
   → Notificar via Telegram/Email
   → Logs

2. Configure no Langflow:
   - Tipo de tarefa: "Scraping e Atualização"
   - Modelo: GPT-4
   - Timeout: 3600 segundos
   - Retries: 3
   - Notificação: Email/Telegram

3. Execute via:
   curl -X POST http://localhost:7860/api/flows/run \\
     -H "Content-Type: application/json" \\
     -d '{
       "flow_id": "seu_flow_id",
       "inputs": {"tarefa": "atualizar_questoes"}
     }'

INTEGRAÇÃO COM COOLIFY:
-----------------------

Se usar Coolify (56.4k ⭐) para hosting:

1. Deploy OpenHands em Coolify:
   • New Service → Docker Image
   • Image: ghcr.io/all-hands-ai/openhands:latest
   • Portas: 3001:3001
   • Environment Variables (acima)
   • Enable Auto-Deploy

2. Configurar webhook GitHub:
   • GitHub Repo → Settings → Webhooks
   • Payload URL: https://seu-coolify.com/api/webhooks/github
   • Trigger: push, pull_request

3. Agora quando commit, Coolify auto-deploy

MONITORAMENTO:
--------------

1. Logs em tempo real:
   docker logs -f openhands-concurso

2. Dashboard Flower (Celery):
   pip install flower
   flower -A tasks
   # Acesse http://localhost:5555

3. Prometheus + Grafana:
   # Já incluído em docker-compose.yml
   http://localhost:3000

4. Health Check:
   curl http://localhost:3001/api/health

TROUBLESHOOTING:
----------------

Problema: OpenHands não consegue raspar
Solução: Verifique se Crawl4AI está rodando
  docker logs crawl4ai-concurso

Problema: Erro de conexão com Supabase
Solução: Verifique DATABASE_URL
  docker exec openhands-concurso printenv | grep DATABASE_URL

Problema: Tarefas não agendadas
Solução: Verifique Celery Beat
  docker logs celery-beat-concurso

Problema: Fila de tarefas acumulando
Solução: Aumentar workers
  docker-compose up -d --scale celery_worker=3

EXEMPLOS DE SCRIPTS:
-------------------

1. Tarefa via CLI:
   
   openhands-cli \\
     --task "Raspe questões Cesgranrio e insira em Supabase" \\
     --model gpt-4 \\
     --max-steps 50 \\
     --timeout 3600

2. Enviar tarefa via Python:
   
   from openhands_sdk import OpenHandsClient
   
   client = OpenHandsClient(url="http://localhost:3001")
   
   task = client.create_task(
       title="Atualizar questões",
       description="Raspe e processe questões Cesgranrio",
       tags=["scraping", "questoes"],
       priority="high"
   )
   
   print(f"Task ID: {task['task_id']}")
   
   # Monitorar
   result = client.wait_for_task(task['task_id'])
   print(f"Status: {result['status']}")
   print(f"Output: {result['output']}")

3. Webhook para receber notificações:
   
   @app.post("/webhooks/openhands")
   async def openhands_webhook(data: dict):
       task_id = data['task_id']
       status = data['status']
       output = data['output']
       
       if status == "completed":
           send_notification(f"✅ Tarefa {task_id} concluída")
       elif status == "failed":
           send_notification(f"❌ Tarefa {task_id} falhou: {output}")

CUSTO ESTIMADO:
---------------

Considerando uso com GPT-4 (mais caro):

• 10 tarefas/dia × 30 dias = 300 tarefas/mês
• ~500 tokens por tarefa = 150k tokens
• GPT-4: $0.03/1k input, $0.06/1k output
• Custo estimado: $9-15/mês (MUITO BARATO!)

Sem usar LLM (local):
• Totalmente GRÁTIS

PRÓXIMOS PASSOS:
----------------

1. Docker-compose up -d openhands
2. Acessar http://localhost:3001
3. Criar primeira tarefa
4. Monitorar andamento
5. Integrar com Langflow
6. Agendar com Celery Beat
7. Configurar notificações
8. Monitorar com Prometheus/Grafana

COMUNIDADE:
-----------

• GitHub: github.com/All-Hands-AI/OpenHands
• Discord: discord.gg/openhands
• Docs: docs.openhands.ai
• Issues: github.com/All-Hands-AI/OpenHands/issues

"""

# ============================================================================
# 🎯 TAREFAS PRONTAS PARA OPENHANDS
# ============================================================================

TAREFAS_PRONTAS = [
    {
        "id": "task_001",
        "nome": "Atualizar Questões Transpetro",
        "descricao": """
        Raspe questões da Cesgranrio (Transpetro 2024):
        1. Acesse https://cesgranrio.org.br
        2. Procure provas Transpetro
        3. Extraia questões (texto, opções, gabarito)
        4. Conecte ao Supabase
        5. Insira na tabela 'questoes_banco'
        6. Se houver erro, reporte
        """,
        "tags": ["scraping", "questoes", "transpetro"],
        "prioridade": "alta",
        "intervalo": "diário",
        "horario": "05:00"
    },
    
    {
        "id": "task_002",
        "nome": "Analisar Padrões de Questões",
        "descricao": """
        Analise questões no Supabase:
        1. Conecte ao banco
        2. Busque 'SELECT * FROM questoes_banco'
        3. Agrupe por: banca, disciplina, dificuldade
        4. Identifique padrões (tópicos mais cobrados)
        5. Crie relatório em JSON
        6. Salve em 'relatorios/padroes.json'
        """,
        "tags": ["análise", "relatório"],
        "prioridade": "média",
        "intervalo": "diário",
        "horario": "12:00"
    },
    
    {
        "id": "task_003",
        "nome": "Atualizar Notícias e Atualidades",
        "descricao": """
        Raspe notícias relevantes:
        1. Use Crawl4AI para raspar G1, Folha, Estadão
        2. Filtre por: Transpetro, Petróleo, Economia, BC
        3. Processe e prepare
        4. Insira em 'atualidades' com timestamp
        5. Deduplicar se existir
        """,
        "tags": ["scraping", "notícias"],
        "prioridade": "alta",
        "intervalo": "a cada 2h"
    },
    
    {
        "id": "task_004",
        "nome": "Atualizar Temas de Redação",
        "descricao": """
        Raspe dados de redação:
        1. Procure temas ENEM 2024
        2. Procure critérios de correção
        3. Procure redações nota 1000
        4. Processe e normalize
        5. Insira em BD com referências
        """,
        "tags": ["redação", "temas"],
        "prioridade": "média",
        "intervalo": "semanal",
        "horario": "19:00"
    },
    
    {
        "id": "task_005",
        "nome": "Backup e Limpeza",
        "descricao": """
        Manutencão do sistema:
        1. Faça backup do Supabase
        2. Limpe logs com mais de 7 dias
        3. Otimize índices BD
        4. Gere relatório de limpeza
        5. Sincronize com GitHub
        """,
        "tags": ["backup", "manutenção"],
        "prioridade": "alta",
        "intervalo": "diário",
        "horario": "23:00"
    },
]

# ============================================================================
# 🚀 INSTRUÇÕES PARA OPENHANDS NO GITHUB
# ============================================================================

OPENHANDS_INSTRUCTIONS = """
# OpenHands - Instruções para o Agente Autônomo

Você é um agente autônomo especializado em atualizar dados de concursos.
Você trabalha 24/7 em tarefas de scraping, análise e atualização.

## Seu Objetivo Principal
Manter a base de dados do Concurso Elite atualizada com:
- Questões das principais bancas (Cesgranrio, Cebraspe, FCC)
- Temas e critérios de redação
- Notícias e atualidades relevantes
- Padrões e insights

## Ferramentas Disponíveis

1. **Crawl4AI** - Web scraping
   - Raspe questões de sites
   - Extraia estruturado
   - Trate erros

2. **Supabase** - Banco de dados
   - Conecte e consulte
   - Insira/atualize dados
   - Faça backups

3. **Docker** - Executar comandos
   - Rode scripts Python
   - Processe dados
   - Execute testes

4. **GitHub** - Controle de versão
   - Commit mudanças
   - Sincronize alterações
   - Reporte issues

## Fluxo de Trabalho

1. **Receba tarefa**
   - Analise os requisitos
   - Planeje os passos
   - Estime duração

2. **Execute**
   - Raspe dados (Crawl4AI)
   - Processe/normalize
   - Insira em BD (Supabase)
   - Se erro, tente novamente

3. **Valide**
   - Verifique dados inseridos
   - Compare com esperado
   - Teste integridade

4. **Reporte**
   - Logs detalhados
   - Quantidade de itens
   - Qualquer problema
   - Próxima execução

## Regras Importantes

- ✅ SEMPRE use try/except para erros
- ✅ SEMPRE registre logs detalhados
- ✅ SEMPRE verifique dados antes de inserir
- ✅ SEMPRE respeite rate limits de sites
- ✅ NÃO raspe dados protegidos por copyright
- ✅ NÃO sobrecarregue o Supabase
- ✅ NÃO faça alterações não solicitadas

## Exemplo de Tarefa

Tarefa: "Raspe questões Cesgranrio e atualize BD"

Passos que vai executar:
1. Conectar ao Supabase
2. Usar Crawl4AI em cesgranrio.org.br
3. Extrair questões (JSON)
4. Validar formato
5. Inserir em 'questoes_banco'
6. Registrar timestamp
7. Reportar: "✅ 47 questões inseridas"

## Agendamento

Tarefas que vai executar automaticamente:

- 05:00 - Atualizar questões
- A cada 2h - Atualizar atualidades
- 12:00 - Analisar padrões
- 19:00 - Atualizar redação
- 23:00 - Backup e limpeza
- Domingo 08:00 - Relatório semanal

## Contato com Usuário

Se precisar de clarificação:
1. Reporte via logs
2. Pause a tarefa
3. Aguarde comando

Se concluir com sucesso:
1. Salve resultado em JSON
2. Commit no GitHub
3. Aguarde próxima tarefa

---

Você é o motor de automação do Concurso Elite.
Trabalhe bem e o usuário terá sempre os dados mais atualizados! 🤖
"""

# ============================================================================
# 📝 ARQUIVO DE INSTRUÇÕES OPENHANDS (SALVAR COMO .instructions.md)
# ============================================================================

if __name__ == "__main__":
    print(OPENHANDS_CONFIG)
    print("\n" + "="*80 + "\n")
    print(f"Total de tarefas prontas: {len(TAREFAS_PRONTAS)}")
    for tarefa in TAREFAS_PRONTAS:
        print(f"  ✓ {tarefa['nome']}")
