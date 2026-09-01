# 🚀 Concurso Elite v3.3 - Guia de Deployment

## Status Atual
- ✅ **Frontend**: Pronto para Vercel (HTML/JS estático)
- ✅ **Backend**: Pronto para Railway/Render (FastAPI + Docker)
- ✅ **Database**: 377 questões (350 originais + 27 práticas)
- ✅ **Código**: Commitado em GitHub (vanivelle/concursos-elite)

## 🔧 Deployment Automático (3 PASSOS)

### PASSO 1: Token Vercel
1. Vá para: https://vercel.com/account/tokens
2. Crie novo token chamado "concurso-elite-ci"
3. Copie o token e cole aqui ⬇️

**Seu Token**: [AGUARDANDO INPUT]

### PASSO 2: Deploy Frontend no Vercel
```powershell
cd "e:\Downloado D\games\fotos da vovo\IA\claude\protocolos\open-notebook"
.\deploy.ps1 -VercelToken "seu_token_aqui"
```

✅ Resultado: `https://concursos-elite.vercel.app`

### PASSO 3: Deploy Backend em Railway
1. Acesse: https://railway.app (signup com GitHub)
2. Crie novo projeto → "Deploy from GitHub repo"
3. Selecione: `vanivelle/concursos-elite`
4. Configure variáveis de ambiente:
   ```
   DATABASE_URL=postgresql://user:pass@db-host:5432/concursos
   ENVIRONMENT=production
   ```
5. Clique "Deploy"

✅ Resultado: `https://concurso-elite-backend.railway.app`

### PASSO 4: Database em Supabase
1. Acesse: https://supabase.com (signup)
2. Crie novo projeto PostgreSQL
3. Copie connection string
4. No Railway, defina: `DATABASE_URL=<supabase-connection-string>`
5. Execute migrations:
   ```sql
   -- Backup local
   pg_dump postgresql://admin:senha_segura_123@localhost:5432/admin > backup.sql
   
   -- Restore em Supabase
   psql <SUPABASE_CONNECTION_STRING> < backup.sql
   ```

## ✅ Verificação Pós-Deploy

### Frontend
- [ ] Acessa `https://concursos-elite.vercel.app`
- [ ] Dropdown de concourses carrega (6 opções)
- [ ] Tema de redação carrega
- [ ] Timer começa automaticamente

### Backend
- [ ] Acessa `https://concurso-elite-backend.railway.app/docs`
- [ ] Endpoint `/gerar-questao` retorna questão
- [ ] Database tem 377 questões
- [ ] POST `/registrar-tempo` funciona

### Integração
- [ ] Frontend conecta ao backend (verificar aba Network no DevTools)
- [ ] API_URL no frontend atualizado para Railway URL
- [ ] Questões carregam do backend
- [ ] Timer registra tempo corretamente

## 📋 Checklist Final
- [ ] GitHub repo linkado (vanivelle/concursos-elite)
- [ ] Frontend deployado em Vercel
- [ ] Backend deployado em Railway
- [ ] Database migrado para Supabase
- [ ] Variáveis de ambiente configuradas
- [ ] Frontend conectado ao backend
- [ ] 377 questões carregadas no banco
- [ ] Todos endpoints testados e funcionando

## 🆘 Troubleshooting

**Frontend não carrega?**
- Verificar: https://vercel.com/vanivelle/concursos-elite/deployments
- Logs: Aba "Deployments" → Ver logs do build

**Backend 502 Bad Gateway?**
- Verificar DATABASE_URL em Railway
- Logs: Railway Dashboard → Logs
- Testar: `curl https://concurso-elite-backend.railway.app/docs`

**Database conexão recusada?**
- Verificar credentials Supabase
- Permitir conexão externa em Supabase → Settings
- Migrar dados com `pg_restore` se backup disponível

## 📞 Suporte
Sistema totalmente automatizado. Se erro:
1. Verificar logs no Vercel/Railway/Supabase
2. Revisar arquivo `.env` (variáveis de ambiente)
3. Testar endpoints localmente antes de deploy
