# ⚡ CHECKLIST DE TESTES RÁPIDOS - V3.3 ELITE

**Tempo Total de Testes:** 15 minutos  
**URL:** http://localhost:8000  
**Login Demo:** teste@elite.com / 123456

---

## 🎯 TESTE #1: STT EXÉRCITO NO DROPDOWN (2 min)

```
PASSO 1: Abrir http://localhost:8000
└─ ✅ Esperado: Painel de login aparece

PASSO 2: Login com teste@elite.com / 123456
└─ ✅ Esperado: Simulador carrega, painel com abas aparece

PASSO 3: Aba "Questões" → Olhar dropdown "🏢 Concurso Elite"
└─ ✅ VERÁ: 4 opções aparecem:
   ├─ Banco Central (Bacen)
   ├─ Transpetro (Petrobras)
   ├─ PMDF
   └─ STT Exército (Sargento Técnico) ← NOVO! 🎯

PASSO 4: Selecionar "STT Exército"
└─ ✅ Esperado: Dropdown de matérias atualiza

PASSO 5: Olhar dropdown "📖 Matéria"
└─ ✅ VERÁ: 8 opções STT:
   ├─ Português
   ├─ Matemática
   ├─ Raciocínio Lógico (RLM)
   ├─ Direito Administrativo
   ├─ Regulamento de Continências (RCONT)
   ├─ Regulamento Interno e Disciplinar (RID)
   ├─ Conhecimentos Gerais
   └─ Conhecimentos Práticos e Atribuições do Cargo ← NOVO! 🎯

RESULTADO: ✅ STT adicionado corretamente
```

---

## 🎯 TESTE #2: QUESTÃO DE PRÁTICA DO CARGO (3 min)

```
PASSO 1: Concurso: STT Exército (já selecionado)

PASSO 2: Matéria: "Conhecimentos Práticos e Atribuições do Cargo" ← NOVO
└─ Selecionar essa opção

PASSO 3: Dificuldade: Médio

PASSO 4: Clique "⚡ Gerar Questão Instantânea"
└─ ⏳ Aguarde 1-2 segundos

PASSO 5: Questão aparece
└─ ✅ VERÁ conteúdo sobre:
   - Ronda de quartel (RID)
   - Livro de Ordens
   - Sindicância
   - Documentação militar
   - Direitos de militar
   └─ Exemplo: "Um Sargento Técnico Temporário (STT) é designado..."

PASSO 6: Ler alternativas (A, B, C, D)
└─ ✅ Esperado: Resposta é sobre procedimento correto

PASSO 7: Clicar em alternativa (ex: B)
└─ ✅ VERÁ:
   - 🔴 "Por Que Você Errou" (se errar)
   - 🟢 "Por Que Você Acertou" (se acertar)
   - Conteúdo específico sobre tema

RESULTADO: ✅ Questão de prática carregou com sucesso
```

---

## 🎯 TESTE #3: CRONOGRAMA CRONOGRÁFICO (2 min)

```
PASSO 1: Estar no painel simulador (qualquer aba)

PASSO 2: ROLAR PARA CIMA no painel
└─ Após "Bem-vindo", antes das abas de questões

PASSO 3: Procurar seção com fundo AZUL com título:
"📅 Cronograma Crítico de Inscrições (2026/2027)"
└─ ✅ VERÁ: Fundo diferente (azul-escuro), visível

PASSO 4: Dentro dessa seção, procurar 4 "cards" lado a lado
└─ ✅ VERÁ:
   
   Card 1 (Borda VERDE):
   ├─ Concurso: Transpetro (Cesgranrio)
   ├─ Badge: 🟢 Aberto
   ├─ Inscrições: 25/08/2026 até 14/09/2026
   └─ Prova: 29/11/2026
   
   Card 2 (Borda AMARELA):
   ├─ Concurso: STT Exército (Regiões Militares)
   ├─ Badge: 🟡 Iminente
   ├─ Inscrições: 01/09/2026 até 30/10/2026
   └─ Prova: Fevereiro 2027
   
   Card 3 (Borda AZUL):
   ├─ Concurso: Banco Central Técnico
   ├─ Badge: 🔵 Previsto
   ├─ Inscrições: Dezembro 2026 até Janeiro 2027
   └─ Prova: Março 2027
   
   Card 4 (Borda AZUL):
   ├─ Concurso: PMDF Soldado (Cebraspe)
   ├─ Badge: 🔵 Previsto
   ├─ Inscrições: Janeiro 2027 até Fevereiro 2027
   └─ Prova: Abril 2027

RESULTADO: ✅ Cronograma visível e completo
```

---

## 🎯 TESTE #4: REDAÇÃO COM STT (4 min)

```
PASSO 1: Aba "✍️ Redação"
└─ ✅ Esperado: Seção de redação carrega

PASSO 2: Dropdown "🏢 Concurso para Redação"
└─ ✅ VERÁ: 4 concursos
   ├─ Banco Central (Bacen)
   ├─ Transpetro (Petrobras)
   ├─ PMDF
   └─ STT Exército ← NOVO! 🎯

PASSO 3: Selecionar "STT Exército"
└─ ✅ Esperado: Dropdown "📝 Tema da Redação" atualiza

PASSO 4: Clique em dropdown "📝 Tema da Redação"
└─ ✅ VERÁ: 5 temas STT aparecem:
   ├─ "A importância da disciplina hierárquica..."
   ├─ "O papel do Sargento Técnico..."
   ├─ "Gestão de pessoal e atribuições administrativas..."
   ├─ "Sindicância administrativa..."
   └─ "Estatuto dos Militares e direitos sociais..."

PASSO 5: Selecionar QUALQUER tema (ex: primeiro)
└─ ✅ VERÁ: Seção "📚 Roteiro Guiado para Iniciantes" aparece com:
   
   ✅ Introdução: "Explique o conceito de hierarquia militar..."
   📖 Desenvolvimento 1: "Cite exemplos reais: em uma ronda..."
   📖 Desenvolvimento 2: "Na gestão de estoque..."
   ✅ Conclusão: "Defenda que sargento técnico..."

PASSO 6: Ler cada seção
└─ ✅ Esperado: Conteúdo é ESPECÍFICO e estruturado (não genérico)

PASSO 7: Trocar para tema diferente (ex: "Sindicância")
└─ ✅ VERÁ: Roteiro muda completamente (agora fala sobre direitos militares)

RESULTADO: ✅ STT redação com 5 temas + roteiros funcionando
```

---

## 🎯 TESTE #5: "CONHECIMENTOS PRÁTICOS" EM TODOS (2 min)

```
PASSO 1: Aba "Questões"

PASSO 2: Selecionar CADA concurso e verificar matérias:
   └─ Bacen → Matérias
   └─ Transpetro → Matérias
   └─ PMDF → Matérias
   └─ STT Exército → Matérias

PASSO 3: Em TODOS, procurar:
"Conhecimentos Práticos e Atribuições do Cargo"
└─ ✅ DEVE APARECER em todos os 4 concursos

RESULTADO: ✅ Matéria "Prática" disponível universalmente
```

---

## 🎯 TESTE #6: BANCO DE DADOS - 377 QUESTÕES (1 min)

```
PASSO 1: Abrir Terminal PowerShell

PASSO 2: Executar:
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT COUNT(*) as total FROM questoes_banco;"

PASSO 3: Verificar resultado
└─ ✅ ESPERADO: total = 377 (350 anterior + 27 prática)

PASSO 4: Verificar prática do cargo:
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT COUNT(*) as prativa FROM questoes_banco 
   WHERE materia = 'Conhecimentos Práticos e Atribuições do Cargo';"

PASSO 5: Verificar resultado
└─ ✅ ESPERADO: prativa = 27-30

RESULTADO: ✅ Banco tem 377 questões com prática do cargo
```

---

## 🎯 TESTE #7: BACKEND RESPONDENDO (1 min)

```
PASSO 1: Terminal PowerShell

PASSO 2: Executar:
docker exec backend_questoes python -c \
  "import requests; \
   r = requests.get('http://localhost:8000/'); \
   print(f'Backend: HTTP {r.status_code}')"

PASSO 3: Verificar resultado
└─ ✅ ESPERADO: Backend: HTTP 200

RESULTADO: ✅ Backend operacional
```

---

## 🎯 TESTE #8: TIMER INATIVIDADE (5 min - opcional)

```
PASSO 1: Aba "Questões" → Gerar questão

PASSO 2: Olhar painel de stats (direita)
└─ ✅ VERÁ: Status: "🟢 Estudando..."

PASSO 3: Não mexer por 5 minutos (mouse, teclado, clique)
└─ Deixar browser aberto
└─ Esperar exatamente 5 minutos

PASSO 4: Após 5 minutos, status deve mudar
└─ ✅ VERÁ: "⏸️ Inativo (timer congelado)" ← AMARELO
└─ ✅ "Horas Estudadas" CONGELA

PASSO 5: Mover mouse / clicar
└─ ✅ VERÁ: Status volta "🟢 Estudando..." ← VERDE
└─ ✅ "Horas" voltam a incrementar no próximo heartbeat (60s)

RESULTADO: ✅ Timer funciona com inatividade
```

---

## ✅ CHECKLIST FINAL (Marque conforme valida)

- [ ] STT Exército aparece no dropdown de concursos
- [ ] STT tem 8 matérias (incluindo Prática)
- [ ] Questão de prática do cargo carrega
- [ ] Cronograma visível com 4 concursos
- [ ] Cronograma tem datas reais e cores
- [ ] Redação STT com 5 temas
- [ ] Cada tema redação STT tem roteiro 4 seções
- [ ] Todos os concursos têm "Conhecimentos Práticos"
- [ ] Banco tem 377 questões
- [ ] Backend respondendo HTTP 200
- [ ] Timer inatividade funciona (opcional)

**TOTAL CHECKLIST:** ___/11 ✅

---

## 🎉 SE TODOS PASSAREM

Sistema v3.3 Elite está **100% OPERACIONAL** e pronto para:
- ✅ Alunos PMDF
- ✅ Alunos STT Exército (NOVO!)
- ✅ Alunos Transpetro
- ✅ Alunos Bacen
- ✅ Qualquer concurso de nível médio 2026/2027

**Abra http://localhost:8000 AGORA e teste!**

---

*Testes Gerados: 2026-08-30*  
*Versão: v3.3 Elite - Prática do Cargo + Cronograma*
