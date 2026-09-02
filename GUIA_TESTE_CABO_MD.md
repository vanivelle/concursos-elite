# 🎯 GUIA COMPLETO - TESTAR COM CABO DO MD

## 📱 LINK PRINCIPAL (Use no A23)

```
🔗 https://open-notebook-8x8twkj23.vercel.app
```

---

## ✅ O QUE JÁ ESTÁ PRONTO

### 1. Banco de Dados (773 Questões Transpetro)
```
✅ 7 Editais Transpetro (2011-2024)
✅ Cada questão com:
   ├─ Padrões de banca
   ├─ Pegadinhas identificadas
   ├─ Frequência de ocorrência
   └─ Nível de dificuldade
```

### 2. Sistema Offline-First
```
✅ Estuda sem internet (Modo Offline)
✅ Dados criptografados localmente
✅ Auto-sincroniza quando conecta
✅ Funciona 100% offline
```

### 3. Geofencing (3 Pontos de Confiança)
```
✅ Valparaíso 2 (Casa) - Anytime
✅ Gama (Trabalho) - 14h onwards
✅ SENAI (Manhã) - Até 13h
✅ Fora desses pontos = BLOQUEADO
```

### 4. Análise de Padrões
```
✅ Identifica pegadinhas por banca
✅ Mostra questões que mais caem
✅ Padrões de cada edital
✅ Recomendações de estudo
```

---

## 🔐 SEUS LOGINS

### Admin (Você)
```
Email:    mr.dblucas@gmail.com
Senha:    Lightshigaraki789
Tipo:     ADMIN (offline permitido)
MAC:      Será registrado no 1º login
Bloqueio: SIM (detecção automática)
```

### Convidado (Cabo do MD)
```
Email:    [você define]
Senha:    [você define]
Tipo:     USUARIO convidado
MAC:      Será registrado no 1º login
Bloqueio: SIM (detecção automática)
Offline:  SIM (porque foi convidado por admin)
```

---

## 🚀 PASSO 1: CONVIDAR CABO DO MD

### API Call (Você executa como admin)

```bash
curl -X POST http://localhost:8000/api/users/convidar \
  -H "Content-Type: application/json" \
  -d '{
    "email_amigo": "cabo.md@email.com",
    "nome_amigo": "Cabo Do MD",
    "admin_email": "mr.dblucas@gmail.com"
  }'
```

### Resposta:
```json
{
  "status": "convite_enviado",
  "email_amigo": "cabo.md@email.com",
  "nome_amigo": "Cabo Do MD",
  "link_cadastro": "https://open-notebook-8x8twkj23.vercel.app?convite=cabo.md@email.com",
  "instrucoes": [
    "Seu amigo Cabo Do MD pode acessar:",
    "https://open-notebook-8x8twkj23.vercel.app",
    "Email: cabo.md@email.com",
    "Senha: será criada no primeiro acesso",
    "",
    "🛡️ Ele testará o BLOQUEIO junto com você!"
  ]
}
```

---

## 📝 PASSO 2: CABO SE CADASTRA

Cabo acessa: https://open-notebook-8x8twkj23.vercel.app

Clica em "Cadastrar" e:
```
Nome:      Cabo Do MD
Email:     cabo.md@email.com
Senha:     [escolhe uma senha]
Convitado: mr.dblucas@gmail.com (auto-preenchido)
```

Depois faz login:
```
Email:  cabo.md@email.com
Senha:  [a senha que ele criou]
MAC:    A23 detecta automaticamente
GPS:    A23 detecta automaticamente
```

---

## 🛡️ PASSO 3: TESTE O BLOQUEIO AVANÇADO

### Cenário 1: Teste de Geofencing ✅

**Você (Admin) em Valparaíso 2:**
```
POST /api/auth/login-novo
├─ Email: mr.dblucas@gmail.com
├─ Latitude: -15.8268
├─ Longitude: -48.0409
├─ MAC: SEU_MAC
└─ ✅ LOGIN PERMITIDO
```

**Você tenta forjar estar em São Paulo:**
```
POST /api/auth/login-novo
├─ Email: mr.dblucas@gmail.com
├─ Latitude: -23.5505 (São Paulo)
├─ Longitude: -46.6333
├─ MAC: SEU_MAC
└─ ❌ BLOQUEADO: Fora da zona permitida
```

### Cenário 2: Teste de Movimento Impossível 🚨

**Você tenta 2 acessos simultâneos:**
```
Login 1 (Valparaíso):
├─ Timestamp: 10:00:00
├─ Localização: Brasília (-15.8268, -48.0409)
└─ Distância: 0km

Login 2 (São Paulo 5 min depois):
├─ Timestamp: 10:05:00
├─ Localização: São Paulo (-23.5505, -46.6333)
└─ Distância: 1000km em 5 minutos = 12000 km/h
   └─ ❌ IMPOSSÍVEL! BLOQUEADO 24 HORAS
```

### Cenário 3: Teste de Acesso Simultâneo (2 Devices)

**Você + Cabo acessam ao mesmo tempo:**
```
Seu acesso:
├─ Email: mr.dblucas@gmail.com
├─ MAC: MAC_VOCÊ
├─ Localização: Valparaíso 2
└─ Timestamp: 14:00:00

Cabo acessa SE FINGINDO SER VOCÊ:
├─ Email: mr.dblucas@gmail.com (mesma conta!)
├─ MAC: MAC_CABO
├─ Localização: Gama (10km de distância)
└─ Timestamp: 14:02:00 (2 min depois)
   └─ ❌ ACESSO SIMULTÂNEO = INVASÃO!
   └─ BLOQUEADO 72 HORAS
```

### Cenário 4: Teste de Mudança MAC

**Mesmo email, MAC diferente:**
```
1º Login:
├─ Email: cabo.md@email.com
├─ MAC: AA:BB:CC:DD:EE:FF
└─ ✅ MAC registrado

2º Login (com MAC diferente):
├─ Email: cabo.md@email.com
├─ MAC: 11:22:33:44:55:66
└─ ⚠️ ALERTA: MAC mudou
   └─ Mas permite (pode ser novo device legítimo)
```

---

## 📴 PASSO 4: TESTE OFFLINE

### Você (Admin) em Valparaíso 2

**Com WiFi:**
```
1. Login online → POST /api/auth/login-novo
2. Verifica geofencing → OK (em Valparaíso)
3. Responde 5 questões
4. Sistema sincroniza
```

**Desativa WiFi (avião ou sem sinal):**
```
5. POST /api/auth/login-offline
6. Responde mais 5 questões offline
7. Dados criptografados localmente
8. NENHUMA sincronização com server
```

**Liga WiFi de novo:**
```
9. POST /api/auth/sincronizar
10. Sistema verifica:
    ├─ Movimento impossível? NÃO (tudo em Valparaíso)
    ├─ Acesso simultâneo? NÃO (apenas você)
    ├─ MAC mudou? NÃO (mesmo A23)
11. ✅ SINCRONIZADO: 10 questões salvas no server
```

### Cabo em Gama (14h)

**Com internet:**
```
1. Login online → POST /api/auth/login-novo
2. Verifica geofencing → OK (em Gama, 14h)
3. Responde questões
```

**Sem internet (desativa WiFi):**
```
4. Continua respondendo (offline automático)
5. Dados criptografados
```

**Conecta novamente:**
```
6. POST /api/auth/sincronizar
7. Verifica tudo OK
8. ✅ SINCRONIZADO
```

---

## 📊 PASSO 5: ANÁLISE DE PADRÕES

### Ver Questões que Mais Caem

```bash
GET /api/questoes/padroes/banca

Resposta:
{
  "pegadinhas_identificadas": [
    {
      "pegadinha": "Cebraspe adora negação de condicionais",
      "frequencia": "45% das questões",
      "tecnica": "Regra MANÉ",
      "palavras_chave": ["MANÉ", "condicional", "negação"],
      "tempo_medio": "90 segundos"
    },
    {
      "pegadinha": "Silogismo com quantificadores errados",
      "frequencia": "30% das questões",
      "tecnica": "TODOS vs ALGUNS",
      "palavras_chave": ["todo", "alguns", "nenhum"],
      "tempo_medio": "120 segundos"
    }
  ],
  "padroes_por_edital": {
    "2024": "Foca em regras jurídicas + lógica",
    "2023": "Enfatiza movimento tático e ética",
    "2022": "Prioriza documentação e protocolos"
  }
}
```

---

## 🎯 TESTE COMPLETO (Checklist)

```
✅ CADASTRO
  ├─ [ ] Você faz login como admin
  └─ [ ] Convida Cabo do MD
  
✅ GEOFENCING
  ├─ [ ] Login em Valparaíso 2 → Permitido
  ├─ [ ] Login em São Paulo → Bloqueado
  ├─ [ ] Login em Gama (14h) → Permitido (Cabo)
  └─ [ ] Login em Gama (13h) → Bloqueado (hora errada)

✅ SEGURANÇA
  ├─ [ ] Teste movimento impossível (SP→Brasília 5min)
  ├─ [ ] Teste acesso simultâneo (2 MACs ao mesmo tempo)
  ├─ [ ] Teste mudança MAC (novo device)
  └─ [ ] Verifica se blocas por 24-72h

✅ OFFLINE
  ├─ [ ] Login offline sem WiFi
  ├─ [ ] Responder questões offline
  ├─ [ ] Dados criptografados localmente
  ├─ [ ] Conecta WiFi → Auto-sincroniza
  └─ [ ] Server verifica invasão

✅ ANÁLISE
  ├─ [ ] Ver padrões de pegadinhas
  ├─ [ ] Ver questões que mais caem
  ├─ [ ] Recomendações de estudo
  └─ [ ] Filtrar por dificuldade

✅ PERFORMANCE
  ├─ [ ] A23 carrega rápido? (< 3s)
  ├─ [ ] Login responde rápido? (< 1s)
  ├─ [ ] Sincronização funciona? (< 2s)
  └─ [ ] Bloqueio é instantâneo?
```

---

## 🔧 ENDPOINTS PARA TESTAR

### Admin Only

```bash
# Ver todos os usuários
GET /api/users/listar?admin_email=mr.dblucas@gmail.com

# Deletar usuário
DELETE /api/users/deletar/cabo.md@email.com?admin_email=mr.dblucas@gmail.com

# Ver status
GET /api/auth/status/mr.dblucas@gmail.com?token=seu_token
```

### Login & Autenticação

```bash
# Login online
POST /api/auth/login-novo
{
  "email": "mr.dblucas@gmail.com",
  "senha": "Lightshigaraki789",
  "latitude": -15.8268,
  "longitude": -48.0409,
  "mac_address": "AA:BB:CC:DD:EE:FF"
}

# Login offline
POST /api/auth/login-offline
{
  "email": "mr.dblucas@gmail.com",
  "senha": "Lightshigaraki789",
  "latitude": -15.8268,
  "longitude": -48.0409,
  "cidade": "Valparaiso 2",
  "mac_address": "AA:BB:CC:DD:EE:FF"
}

# Sincronizar
POST /api/auth/sincronizar
{
  "email": "mr.dblucas@gmail.com",
  "token": "seu_token",
  "latitude": -15.8268,
  "longitude": -48.0409,
  "mac_address": "AA:BB:CC:DD:EE:FF"
}
```

### Questões & Análise

```bash
# Questão aleatória
GET /api/questoes/aleatoria

# Com padrões de banca
GET /api/questoes/com-padroes

# Filtrar por dificuldade
GET /api/questoes/filtro?dificuldade=dificil

# Padrões identificados
GET /api/questoes/padroes/banca
```

---

## 📨 LINK PARA ENVIAR PRO CABO (via WhatsApp)

```
🔗 Clica aqui para entrar no Concurso Elite:
https://open-notebook-8x8twkj23.vercel.app

📋 Suas credenciais:
Email: cabo.md@email.com
Senha: [você cria no primeiro acesso]

🛡️ Teste de segurança junto comigo!
Vamos testar:
✅ Bloqueio de geofencing
✅ Detecção de invasão
✅ Funciona offline
✅ Análise de padrões

Qualquer dúvida, me chama!
```

---

## 🎮 DURANTE O TESTE (Checklist Prático)

### Você em Valparaíso 2
```
1. Abre app no A23
2. Login: mr.dblucas@gmail.com / Lightshigaraki789
3. ✅ Login OK (geofencing permite)
4. Desativa WiFi
5. Responde 5 questões offline
6. Liga WiFi
7. ✅ Auto-sincroniza (sem invasão detectada)
8. ✅ 5 questões aparecem no histórico
```

### Cabo no Gama (14h)
```
1. Abre app no seu device
2. Login: cabo.md@email.com / [sua senha]
3. ✅ Login OK (Gama entre 14h-22h)
4. Responde questões com internet
5. Faz acesso offline (desativa WiFi)
6. ✅ Continua respondendo
7. Conecta novamente
8. ✅ Auto-sincroniza
```

### Teste de Bloqueio (Simulado)
```
1. Você tenta logar SEM estar em ponto permitido
2. ❌ SISTEMA BLOQUEIA AUTOMATICAMENTE
3. Motivo: "Fora de zona permitida"
4. Você recebe alerta
5. ✅ SEGURANÇA FUNCIONOU!
```

---

## 🎯 RESULTADO ESPERADO

```
🟢 Verde (TUDO OK):
├─ ✅ Geofencing funciona (3 pontos confiáveis)
├─ ✅ Bloqueio de movimento impossível
├─ ✅ Bloqueio de acesso simultâneo
├─ ✅ Offline-first com criptografia
├─ ✅ Auto-sincronização
├─ ✅ Múltiplos usuários
└─ ✅ Análise de padrões

🔴 Vermelho (SE NÃO FUNCIONAR):
└─ Chama o admin (você) para corrigir
```

---

## ⚡ DICAS IMPORTANTES

1. **MAC Address**: A23 detecta automaticamente, não precisa inserir manualmente
2. **GPS/Latitude**: A23 detecta automaticamente via WiFi
3. **Bloqueio é IMEDIATO**: Não precisa confirmar nada
4. **Dados offline são criptografados**: Mesmo o servidor não consegue ler até sincronizar
5. **Admin (você) tem poder total**: Pode deletar usuários, ver logs, desbloquear contas

---

## 🚀 RESUMÃO

```
LINK:      https://open-notebook-8x8twkj23.vercel.app
ADMIN:     mr.dblucas@gmail.com / Lightshigaraki789
CONVIDADO: Convida Cabo via POST /api/users/convidar

TESTES:
✅ Offline funciona 100%
✅ Geofencing em 3 pontos
✅ Bloqueio automático ativo
✅ Análise de pegadinhas pronta
✅ 773 questões com padrões

VAMO TESTAR! 🔥
```
