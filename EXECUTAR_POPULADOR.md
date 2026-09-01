# 🚀 SOLUÇÃO DO ERRO DE ENCODING

**Problema**: O path tem caracteres especiais (`ç`, `á`, `ó`) que o psycopg2 não decodifica bem

**Solução**: Rodar o populador **DENTRO do container Docker** (sem encoding issues)

---

## ⚡ COMANDO RÁPIDO (1 linha)

```bash
docker exec -it backend_questoes python /app/populate.py
```

---

## Passo a Passo

### 1. Verificar se Docker está rodando
```bash
docker ps
```

Deve listar `backend_questoes` e `postgres_concursos` com status UP

### 2. Se não estiverem rodando
```bash
docker-compose up -d
docker ps  # Verificar novamente
```

### 3. Popular o banco (DENTRO do container)
```bash
docker exec -it backend_questoes python /app/populate.py
```

### Resultado
```
================================================================================
🏛️  POPULADOR ELITE v2 - VERSÃO DOCKER
================================================================================

🔢 Injetando questões de exatas...
   ✅ 9 questões de exatas inseridas!

📝 Injetando temas de redação...
   ✅ 15 temas de redação inseridos!

================================================================================
✅ POPULAÇÃO COMPLETA!
   📊 Questões de exatas + Temas de redação no banco
================================================================================
```

---

## ✅ Pronto!

Agora testa:
1. Abra `http://localhost:8000`
2. Login
3. Selecione "Bacen" + "Raciocínio Lógico (RLM)"
4. Clique "Gerar Questão"

Deve gerar questão de lógica com detector em **RED** 🔴
