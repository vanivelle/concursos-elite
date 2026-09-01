# 🚀 DEPLOYMENT BACKEND EM RAILWAY

## STATUS
- ✅ Frontend: https://open-notebook-8x8twkj23.vercel.app (LIVE)
- ⏳ Backend: Pronto para Railway
- ⏳ Database: Pronto para Supabase

## PASSO 1: Criar Supabase Database (5 MIN)

### 1.1 Criar Database
1. Acesse: https://supabase.com
2. Signup com GitHub
3. "Create new project"
4. Escolha:
   - Project Name: "concurso-elite"
   - Region: "Brasil" (mais rápido)
   - Password: salve bem!
5. Espere criar (2-3 min)

### 1.2 Copiar Connection String
1. Projeto criado → "Settings" → "Database"
2. Procure por "Connection string"
3. Copie a URL que começa com: `postgresql://postgres:...@db.xxxx.supabase.co:5432/postgres`
4. **Salve essa URL** - vamos usar em Railway

### 1.3 Migrar Dados
1. No seu computador, faça backup do banco local:
```powershell
# Exportar banco local
pg_dump -U admin -h localhost -d admin > backup.sql 2>&1
```

2. Restaure em Supabase:
```powershell
# Conectar ao Supabase e executar backup
psql "<SUPABASE_CONNECTION_STRING>" < backup.sql
```

3. Verificar se 377 questões foram migradas:
```powershell
psql "<SUPABASE_CONNECTION_STRING>" -c "SELECT COUNT(*) as total FROM questoes_banco;"
```

✅ Deve retornar: 377

---

## PASSO 2: Deploy Backend em Railway (5 MIN)

### 2.1 Criar Account Railway
1. Acesse: https://railway.app
2. Signup → "Sign up with GitHub"
3. Conecte seu GitHub (vanivelle/concursos-elite)

### 2.2 Criar Novo Projeto
1. Dashboard → "New Project"
2. Selecione: "Deploy from GitHub repo"
3. Escolha: `vanivelle/concursos-elite`
4. Clique "Deploy"

### 2.3 Configurar Variáveis
Railway deve auto-detectar Dockerfile. Configurar:

1. Projeto → "Variables"
2. Adicione:
```
DATABASE_URL=postgresql://postgres:SENHA@db.xxxx.supabase.co:5432/postgres
ENVIRONMENT=production
DEBUG=false
FRONTEND_URL=https://open-notebook-8x8twkj23.vercel.app
```

3. Clique "Deploy"

### 2.4 Obter URL Backend
1. Railway Dashboard → seu projeto
2. Procure por: "Domains"
3. URL ficará como: `https://concurso-elite-backend.railway.app` (você pode customizar)

✅ Copie essa URL!

---

## PASSO 3: Testar Backend (2 MIN)

### Teste Health Check
```powershell
curl -i https://concurso-elite-backend.railway.app/docs
```

Deve retornar: **HTTP 200 OK**

### Teste Gerar Questão
```powershell
$response = Invoke-RestMethod -Uri "https://concurso-elite-backend.railway.app/gerar-questao" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"concurso":"Banco Central (Bacen)","materia":"Português","dificuldade":"Fácil"}'

$response
```

Deve retornar objeto com questão

### Teste Registrar Tempo
```powershell
$response = Invoke-RestMethod -Uri "https://concurso-elite-backend.railway.app/registrar-tempo" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"usuario_id":"teste123","minutos":1}'

$response
```

Deve retornar: `{"status":"ok"}`

---

## PASSO 4: Verificar Integração (1 MIN)

1. Abra: https://open-notebook-8x8twkj23.vercel.app
2. Abra DevTools (F12) → aba "Network"
3. Clique em "Gerar Questão"
4. Procure por requisição para `concurso-elite-backend.railway.app`
5. Deve retornar questão com 200 OK

✅ Frontend + Backend integrados!

---

## 🚨 Troubleshooting

### Backend retorna 502 Bad Gateway
- Verificar DATABASE_URL está correto em Railway
- Verificar se Supabase está online
- Logs: Railway → seu projeto → "Logs"

### Questões não carregam
- Verificar se 377 questões foram migradas para Supabase
- Logs do backend: `SELECT COUNT(*) FROM questoes_banco;`

### Erro de CORS
- Frontend não consegue chamar backend
- Verificar FRONTEND_URL em Railway está correto
- Backend deve ter CORS habilitado no main.py

### Banco de dados vazio
- Backup não foi restaurado
- Fazer `pg_restore` do arquivo SQL

---

## ✅ Checklist Final

- [ ] Supabase database criado
- [ ] 377 questões migradas
- [ ] Backend deployado em Railway
- [ ] Variáveis de ambiente configuradas
- [ ] URL Railway funciona (GET /docs → 200)
- [ ] Frontend conecta ao backend
- [ ] Questões carregam no frontend
- [ ] Timer registra tempo

---

## 📊 URLs Finais

| Componente | URL | Status |
|---|---|---|
| Frontend | https://open-notebook-8x8twkj23.vercel.app | ✅ LIVE |
| Backend | https://concurso-elite-backend.railway.app | ⏳ Deploy |
| Database | Supabase PostgreSQL | ⏳ Configurar |
| Admin | https://vercel.com/vanivelle/concursos-elite | ✅ Dashboard |

---

**Próximo passo**: Cole sua DATABASE_URL do Supabase quando tiver!
