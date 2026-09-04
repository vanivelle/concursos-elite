# Concurso Elite - Agent Instructions

**Context**: FastAPI backend + Supabase + geofencing + 3 users. Token-efficient workflow using external agents.

---

## Agent Ecosystem

### 🤖 Primary Agents (Use These)

#### 1. **OpenHands** (Architecture Lead)
- **Purpose**: Autonomous codebase analysis, refactoring, schema updates
- **Repo**: github.com/All-Hands-AI/OpenHands (75.8K stars)
- **Trigger**: `@openhands analyze backend`
- **Skills**: Read all files, propose changes, execute bash
- **Cost**: Saves 60% tokens vs manual exploration

#### 2. **Explore** (Fast Diagnostics)
- **Purpose**: Quick codebase Q&A without deep changes
- **Built-in**: VS Code
- **Trigger**: Use for "what files exist", "find function X", "list endpoints"
- **Cost**: 2-3 token burst vs 50+ for manual grep

#### 3. **DSPy** (Structured Prompting)
- **Purpose**: Cache repeated patterns, validate LLM outputs
- **Repo**: github.com/stanfordnlp/dspy (11K stars)
- **Use for**: "Login validation", "Geofencing checks", "User status"
- **Cost**: 80% token reduction for repeated tasks

#### 4. **LiteLLM** (Model Router)
- **Purpose**: Use cheaper models for simple tasks (e.g., "check syntax")
- **Repo**: github.com/BerriAI/litellm (56K stars)
- **Routing**:
  - Cheap (gpt-3.5/claude-haiku): Syntax checks, summaries
  - Normal (claude-3): Code review, refactoring
  - Expensive (gpt-4): Architecture decisions

---

## Workflow Rules (TOKEN EFFICIENT)

### ❌ DON'T DO
- Run manual `grep_search` > 1 time per task
- Read files sequentially (batch 3-5 parallel reads)
- Run CLI commands without checking if tool exists
- Ask questions about imports/syntax (use Explore agent)

### ✅ DO THIS
1. **Diagnose**: Call Explore agent (30s)
2. **Validate**: Use LiteLLM + cached prompts (DSPy)
3. **Execute**: Use OpenHands for big changes OR direct edits for small ones
4. **Test**: Use existing test files, don't create new

---

## Repos Mapped to Tasks

| Task | Repo | Stars | Use Case |
|------|------|-------|----------|
| **Backend Architecture** | OpenHands | 75.8K | Analyze main.py, propose optimizations |
| **FastAPI Patterns** | Langflow | 194K | Reference for FastAPI best practices |
| **Async/Queue** | Celery (in LangFlow) | - | Task queueing for logins |
| **DB Schema** | Supabase | 102K | PostgreSQL patterns, migrations |
| **Vector Search** | LLMLingua | 6K | If adding semantic search to questions |
| **Caching** | GPTCache | 7K | Cache login tokens, geofencing results |
| **Agent Framework** | DSPy | 11K | Structure login validation logic |
| **LLM Routing** | LiteLLM | 56K | Choose model cost-effectively |
| **CLI Tools** | n8n/Dify | 143K+ | Automation templates (ignore, internal use) |
| **PDF/Web** | Stirling PDF / Crawl4AI | 80K/67K | If adding document parsing |

---

## Token Budget Strategy

**Monthly budget**: 200K tokens
**Daily**: ~6.5K tokens

### Allocation
- 40% = Develop + Test (backend, API, logins)
- 30% = Explore + Diagnostics (agents handling this)
- 20% = Documentation + Explanations
- 10% = Buffer for emergencies

### How Agents Save
- **Explore**: 1 call = 5-10 manual searches
- **OpenHands**: 1 analysis = 20-30 manual code reads
- **DSPy**: Cached logic = 80% reduction on repeated tasks
- **LiteLLM**: Route to cheap models = 60% cost reduction

---

## When to Call Each Agent

| Scenario | Agent | Cost |
|----------|-------|------|
| "What endpoints exist?" | Explore | 50 tokens |
| "Refactor authentication" | OpenHands | 200 tokens |
| "Check if login valid?" | DSPy (cached) | 20 tokens |
| "Write new middleware" | Me (direct) | 100 tokens |
| "Analyze 5 files for patterns" | OpenHands | 150 tokens |
| "Quick syntax question" | LiteLLM (cheap model) | 10 tokens |

---

## Auto-Activation Rules

1. **If** task involves >3 files → Use OpenHands
2. **If** task is "what is X in codebase" → Use Explore
3. **If** task is repeated (login, geofencing) → Use DSPy cache
4. **If** task is "optimize costs" → Use LiteLLM routing
5. **If** task is simple edit → Direct file edit (fastest)

---

## Files This Applies To

```
applyTo:
  - "backend/*.py"
  - "frontend/*.html"
  - "*.md"
  - ".github/**"
```

**Except**:
- `.env` (never auto-analyze)
- `node_modules/`, `venv/` (ignore)
- `*.log`, `*.tmp` (ignore)
