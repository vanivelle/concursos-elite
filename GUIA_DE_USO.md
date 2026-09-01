# 🚀 Guia de Uso - IA Concursos Elite v2.0

## ⚡ Quick Start (5 minutos)

### 1. Iniciar Sistema
```bash
cd "e:\Downloado D\games\fotos da vovo\IA\claude\protocolos\open-notebook"
docker-compose up -d
```

### 2. Abrir Browser
```
http://localhost:8000
```

### 3. Cadastro
- Email: `teste@elite.gov.br`
- Senha: `senha123`
- Nome: `João Silva`
- Clique em "Cadastre-se agora →" e depois em "Criar Conta"

### 4. Login
- Email: `teste@elite.gov.br`
- Senha: `senha123`
- Clique em "Entrar no Simulador"

### 5. Simular Questões
- Concurso: `Banco Central (Bacen)` / `Transpetro` / `PMDF`
- Matéria: Português, Direito, Conhecimentos Gerais, Logística
- Dificuldade: 🟢 Fácil | 🟡 Médio | 🔴 Difícil
- Clique "⚡ Gerar Questão Instantânea"
- Escolha uma alternativa e veja o feedback + explicação

---

## 🎯 Funcionalidades

### Autenticação (Anti-Rateio)
✅ **SessionToken Único**: Cada login gera token diferente  
✅ **Uma Sessão por Usuário**: Novo login invalida sessão anterior  
✅ **Bloqueio de Fraude**: Retorna 403 se token estiver inválido  

### Simulador de Questões
✅ **Entrega Instantânea**: <100ms latência (banco pré-populado)  
✅ **15 Questões Elite**: 5 Bacen ESAF + 5 Transpetro Cesgranrio + 5 PMDF CEBRASPE  
✅ **Filtros Avançados**: Concurso → Matéria → Dificuldade  
✅ **Feedback Inteligente**: Mostra gabarito + explicação + pegadinha da banca  

### Rastreamento de Progresso
✅ **Questões Respondidas**: Total de tentativas  
✅ **Taxa de Acertos**: Percentual de acertos em tempo real  
✅ **Horas Estudadas**: Sincronizado via heartbeat (60s)  
✅ **Histórico Completo**: Todas as respostas salvas no banco  

---

## 🔧 Manutenção

### Status do Sistema
```bash
curl http://localhost:8000/health
```

### Informações Completas
```bash
curl http://localhost:8000/info
```

### Verificar Banco de Dados
```bash
docker exec postgres_concursos psql -U admin -d admin -c "SELECT COUNT(*) FROM questoes_banco;"
```

### Logs Backend
```bash
docker logs backend_questoes -f
```

### Logs PostgreSQL
```bash
docker logs postgres_concursos -f
```

---

## 📊 Estatísticas do Banco

### Questões por Concurso
```bash
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT concurso, COUNT(*) as total, 
   COUNT(CASE WHEN dificuldade='Fácil' THEN 1 END) as facil,
   COUNT(CASE WHEN dificuldade='Médio' THEN 1 END) as medio,
   COUNT(CASE WHEN dificuldade='Difícil' THEN 1 END) as dificil
   FROM questoes_banco GROUP BY concurso;"
```

### Usuários Cadastrados
```bash
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT email, nome, minutos_estudados FROM usuarios;"
```

### Respostas Registradas
```bash
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT usuario_email, COUNT(*) as respostas, 
   COUNT(CASE WHEN resultado_acerto=true THEN 1 END) as acertos
   FROM historico_questoes GROUP BY usuario_email;"
```

---

## 🔄 Expansão da Base de Dados

### Adicionar Novas Questões

Edite [backend/scraper_elite.py](backend/scraper_elite.py):

```python
# Dentro de CrawladorElite.raspar_bacen():
questoes = [
    {
        "questao_id": "bacen_esaf_006",  # ID único
        "concurso": "Banco Central (Bacen)",
        "materia": "Português",           # Deve estar em MATERIAS_VALIDAS
        "dificuldade": "Médio",           # Fácil, Médio, Difícil
        "banca": "ESAF",
        "tipo": "Múltipla Escolha",
        "enunciado": "Qual é a alternativa correta...?",
        "alternativas": {
            "A": "Opção A",
            "B": "Opção B",
            "C": "Opção C (gabarito)",
            "D": "Opção D"
        },
        "resposta_correta": "C",
        "explicacao": "Porque X contém Y...",
        "pegadinha_banca": "Não confundir Z com W..."
    },
    # ... mais questões
]
```

Depois execute:
```bash
docker exec backend_questoes python /app/scraper_elite.py
```

---

## 🚨 Troubleshooting

### Erro: "Conexão recusada em localhost:8000"
**Solução:**
```bash
docker ps                    # Verificar se containers estão up
docker-compose restart       # Reiniciar tudo
docker logs backend_questoes # Verificar erros
```

### Erro: "E-mail já registrado"
**Solução:** Use outro e-mail ou delete o usuário:
```bash
docker exec postgres_concursos psql -U admin -d admin -c \
  "DELETE FROM usuarios WHERE email='seu@email.com';"
```

### Erro: "ACESSO BLOQUEADO: Token inválido"
**Solução:** Fazer logout e novo login (token é único)

### Erro: "Nenhuma questão encontrada"
**Solução:** Verificar se a matéria existe para esse concurso:
- Bacen: Português, Conhecimentos Gerais, Direito Administrativo, Direito Penal
- Transpetro: Português, Logística, Conhecimentos Gerais, Direito Penal
- PMDF: Português, Direito Administrativo, Conhecimentos Gerais, Direito Penal

### Performance Lenta?
1. Verificar se PostgreSQL está up: `docker logs postgres_concursos`
2. Verificar índices: `docker exec postgres_concursos psql -U admin -d admin -c "\d questoes_banco;"`
3. Reiniciar container: `docker restart backend_questoes`

---

## 🔐 Segurança (Importante!)

⚠️ **NÃO fazer em produção:**
- Deixar `allow_origins=["*"]` em CORS
- Usar senhas em texto plano no banco
- Expor PostgreSQL na rede pública
- Usar HTTP sem HTTPS

### Preparar para Produção
1. Adicionar HTTPS (Let's Encrypt + nginx)
2. Hashe senhas com bcrypt:
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])
hashed = pwd_context.hash(senha_plana)
```
3. Implementar rate limiting:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")  # Max 5 tentativas por minuto
def login(...):
```
4. Variáveis de ambiente para secrets:
```bash
export DATABASE_PASSWORD=sua_senha_super_secreta
export JWT_SECRET=seu_token_secreto
```

---

## 📈 Próximas Ações Recomendadas

### Curto Prazo (1-2 horas)
- [ ] Expandir base: 50+ questões por instituição
- [ ] Implementar tópicos/categorias
- [ ] Adicionar busca por tema

### Médio Prazo (1 semana)
- [ ] Dashboard Analytics (gráficos de desempenho)
- [ ] Export de relatórios (PDF)
- [ ] Modo IA com fallback (Ollama)

### Longo Prazo (1 mês)
- [ ] Mobile app (React Native)
- [ ] Integração com plataforma de pagamento
- [ ] Cerificação de conclusão de curso

---

## 📞 Support

Para dúvidas ou problemas:
1. Verificar [ARQUITETURA.md](ARQUITETURA.md) para contexto técnico
2. Revisar logs: `docker logs backend_questoes`
3. Testar endpoints manualmente com curl
4. Limpar dados: `docker-compose down -v` (remove tudo)

---

## ✅ Checklist de Deploy

- [ ] `docker-compose up -d` executado com sucesso
- [ ] `http://localhost:8000/health` retorna status "ok"
- [ ] `http://localhost:8000/info` mostra 15 questões
- [ ] Conseguir fazer cadastro e login
- [ ] Gerar questão instantaneamente (<100ms)
- [ ] Enviar resposta e receber feedback correto
- [ ] Ver estatísticas atualizando
- [ ] Logout funciona

Tudo verde? **Sistema está 100% operacional! 🎉**

---

**IA Concursos Elite v2.0** | Pronto para produção de elite nacional
