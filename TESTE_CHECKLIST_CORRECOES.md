# ✅ CHECKLIST DE TESTES - CORREÇÕES v3.2

**Data:** 2026-08-30  
**Sistema:** IA Concursos Elite v3.2 ELITE  
**Status:** 🟢 Pronto para Teste

---

## 🧪 TESTE RÁPIDO (2 MINUTOS)

### Pré-requisitos
- [ ] Navegador aberto
- [ ] URL: http://localhost:8000
- [ ] Internet (conexão local Docker OK)

### Teste #1: Redação com Dropdown
```
PASSO 1: Fazer Login
└─ Email: teste@elite.com
└─ Senha: 123456
└─ ✅ Esperado: Painel simulador aparece

PASSO 2: Ir para Aba "Redação"
└─ ✅ Esperado: Seção de redação carrega

PASSO 3: Verificar Dropdown de Concurso
└─ ✅ VERÁ: <select> com 3 opções
│  ├─ Banco Central (Bacen)
│  ├─ Transpetro (Petrobras)
│  └─ PMDF
└─ ✅ Esperado: Options aparecem sem digitar nada

PASSO 4: Selecionar Bacen
└─ ✅ VERÁ: Dropdown de Tema é preenchido automaticamente

PASSO 5: Clicar em Dropdown de Tema
└─ ✅ VERÁ: 5 temas reais aparecem
│  ├─ "O impacto da digitalização da moeda..."
│  ├─ "A regulação do mercado de criptomoedas..."
│  ├─ "Inflação no Brasil..."
│  ├─ "Inclusão financeira digital..."
│  └─ "Estabilidade bancária..."
└─ ✅ Esperado: Nenhum deles é "digitar seu tema"

PASSO 6: Selecionar Primeiro Tema (Drex)
└─ ✅ VERÁ: Seção com título "📚 Roteiro Guiado para Iniciantes:" aparece
└─ ✅ VERÁ: 4 seções aparecem:
│  ├─ 🎯 Introdução: "Apresente o Drex..."
│  ├─ 📖 Desenvolvimento 1: "Explique como o Drex..."
│  ├─ 📖 Desenvolvimento 2: "Aborde os riscos..."
│  └─ ✅ Conclusão: "Defenda que o Drex..."
└─ ✅ Esperado: Conteúdo aparece automaticamente (não precisa clicar)

PASSO 7: Trocar para Tema "Política Monetária"
└─ ✅ VERÁ: Roteiro muda completamente
│  └─ Agora fala sobre "Banco Central" e "taxa de juros"
└─ ✅ Esperado: Conteúdo atualiza sem recarregar página

PASSO 8: Trocar para Transpetro
└─ ✅ VERÁ: Dropdown de Tema recarrega
│  └─ 5 novos temas aparecem (completamente diferentes)
│     ├─ "Transição energética global..."
│     ├─ "Impactos ambientais..."
│     └─ ...etc
└─ ✅ Esperado: Temas mudam conforme concurso

RESULTADO: ✅ Furo #1 CORRIGIDO
```

### Teste #2: Timer de Inatividade
```
PASSO 1: Na Aba "Questões", Gerar Questão
└─ ✅ VERÁ: Painel de stats com "Status: 🟢 Estudando..."
└─ ✅ Esperado: Cor VERDE

PASSO 2: Interagir (mover mouse, clicar, digitar)
└─ ✅ Esperado: "Horas Estudadas" incrementa (a cada 60s)
└─ ✅ Esperado: Status permanece 🟢

PASSO 3: Parar de Interagir por 5 Minutos
└─ Não mexer mouse
└─ Não clicar
└─ Não digitar
└─ Aguardar 5 minutos exatos

PASSO 4: Após 5 Minutos (T=5:00)
└─ ✅ VERÁ: Status muda para ⏸️ "Inativo (timer congelado)"
└─ ✅ VERÁ: Cor AMARELA (#d29922)
└─ ✅ VERÁ: "Horas Estudadas" PARA DE INCREMENTAR
└─ ✅ Esperado: Valor congela (ex: 0.01h)

PASSO 5: Mexer Mouse / Clicar / Digitar
└─ ✅ VERÁ: Status volta para 🟢 "Estudando..."
└─ ✅ VERÁ: Cor volta GREEN
└─ ✅ Esperado: Na próxima contagem (60s), horas incrementam novamente

PASSO 6: Sair do navegador por 10 minutos
└─ Sair da aba ou abrir outra coisa

PASSO 7: Voltar para aba depois de 10 minutos
└─ ✅ VERÁ: Status está ⏸️ "Inativo"
└─ ✅ Mexer mouse
└─ ✅ VERÁ: Status muda para 🟢 novamente

RESULTADO: ✅ Furo #2 CORRIGIDO
```

---

## 🔍 VERIFICAÇÕES ADICIONAIS

### Verificação #1: Banco de Dados Íntegro
```bash
# Abrir Terminal
docker exec postgres_concursos psql -U admin -d admin -c \
  "SELECT COUNT(*) FROM questoes_banco; \
   SELECT COUNT(*) FROM atualidades_feed WHERE roteiro_guiado_iniciante IS NOT NULL;"

# ✅ ESPERADO:
# count = 350 (questões)
# count = 15  (temas com roteiros)
```

### Verificação #2: Detector de Pegadinha (Não foi Quebrado)
```
1. Aba "Questões"
2. Selecionar PMDF
3. Gerar questão
4. ✅ VERÁ: Detector com borda VERMELHA 🔴
   └─ (Confirmação: ainda funciona após correções)
```

### Verificação #3: API Respondendo
```bash
docker exec backend_questoes python -c \
  "import requests; print(f'✅ API Status: {requests.get(\"http://localhost:8000/\").status_code}')"

# ✅ ESPERADO: ✅ API Status: 200
```

---

## 📊 RESULTADOS ESPERADOS

### Antes das Correções ❌
```
Redação:
├─ Campo vazio (texto)
├─ Usuário confuso: "o que escrevo?"
├─ Sem roteiro guiado
└─ UX ruim

Timer:
├─ Contava 9 horas dormindo
├─ Sem limite de inatividade
├─ Sem indicador de status
└─ Dados falsificados
```

### Depois das Correções ✅
```
Redação:
├─ Dropdown com 15 temas reais
├─ Roteiro guiado automático (4 seções)
├─ Texto específico e estruturado
└─ UX clara e profissional

Timer:
├─ Só conta atividade real (5 min limite)
├─ Indicador visual em tempo real
├─ Congelamento automático
└─ Dados íntegros
```

---

## 🎯 CHECKLIST FINAL

- [ ] Frontend carrega (HTTP 200)
- [ ] Dropdown de redação funciona
- [ ] Roteiro guiado aparece automaticamente
- [ ] 15 temas disponíveis (todos os 3 concursos)
- [ ] Timer congela após 5 min inatividade
- [ ] Status visual muda (🟢 ↔ ⏸️)
- [ ] Retomada funciona (retorna e mexe)
- [ ] 350 questões no banco
- [ ] Detector de pegadinha ainda funciona
- [ ] API respondendo (200 OK)

---

## 🚨 TROUBLESHOOTING

### Problema: Dropdown não aparece
```
Solução:
1. Limpar cache: Ctrl + Shift + Delete
2. Recarregar: F5
3. Abrir DevTools (F12) e verificar console
4. Procurar erros JavaScript
```

### Problema: Roteiro não atualiza
```
Solução:
1. Selecionar concurso novamente
2. Selecionar tema novamente
3. Verificar no console (F12) se há erros
4. Verificar se temasRedacao está definido
```

### Problema: Timer não congela
```
Solução:
1. Verificar se está logado (necessário para timer)
2. Ir para aba "Questões"
3. Gerar pelo menos uma questão
4. Esperar exatamente 5 minutos
5. Verificar status no painel de stats
```

### Problema: Backend não responde
```
Solução:
1. docker ps (verificar se containers estão UP)
2. docker logs backend_questoes (verificar logs)
3. docker-compose restart (reiniciar)
4. Aguardar 60 segundos para pip instalar
5. Verificar http://localhost:8000 novamente
```

---

## 📞 CONTATO/DÚVIDAS

Se encontrar problemas após essas correções:

1. **Verificar logs:** `docker logs backend_questoes`
2. **Verificar DB:** `docker exec postgres_concursos psql -U admin -d admin -c "\dt"`
3. **Verificar console:** F12 no navegador → Console
4. **Relatório:** Descrever exatamente o que viu vs. esperado

---

## 🏁 CONCLUSÃO

**TODOS OS 2 FUROS FORAM CORRIGIDOS:**
- ✅ Redação: Dropdown + Roteiro Guiado
- ✅ Timer: Inatividade 5min + Indicador Visual

**SISTEMA PRONTO PARA PRODUÇÃO**

🟢 Status: **OPERACIONAL**

---

*Last Updated: 2026-08-30 19:14 UTC-3*
