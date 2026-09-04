---
agentName: OpenHands-Backend
description: "Autonomous backend analysis and refactoring for Concurso Elite FastAPI system"
keywords: [backend, analysis, refactoring, deployment, architecture]
applyTo: 
  - "backend/**/*.py"
  - "requirements.txt"
  - "Procfile"
  - "render.yaml"
---

# OpenHands - Backend Architect

## Purpose
Autonomous codebase analysis and refactoring for FastAPI + Supabase + Geofencing system. Replaces 20-30 manual code reads with 1 agent call.

## When to Use

### ✅ Perfect For
- "Analyze entire backend folder and list all endpoints"
- "Why does main_enterprise.py fail to start?"
- "Refactor authentication to use JWT"
- "Find all database queries and optimize them"
- "What's missing from requirements.txt?"
- "Is the backend production-ready?"

### ❌ Not For
- Quick syntax fixes (use direct edit)
- Single file questions (use Explore)
- Runtime debugging (use Python skill)

## How It Works

### Step 1: Initial Diagnosis (5 min)
```
USER: "Analyze backend structure"

OPENHANDS:
1. Reads all Python files in backend/
2. Extracts: endpoints, imports, dependencies
3. Checks requirements.txt vs imports
4. Reports: ✅ working / ❌ missing / ⚠️ issues
5. Token cost: ~150 tokens
```

### Step 2: Deep Analysis (10 min)
```
USER: "Why does main_enterprise.py fail?"

OPENHANDS:
1. Reads main_enterprise.py line by line
2. Traces import errors
3. Checks if geoip2, security_advanced_blocks exist
4. Reports exact failure point
5. Suggests fix (install vs create module)
6. Token cost: ~200 tokens
```

### Step 3: Autonomous Fixes (15 min)
```
USER: "Refactor authentication to JWT"

OPENHANDS:
1. Analyzes current auth flow
2. Proposes JWT implementation
3. Generates modified code
4. Tests changes (if able)
5. Reports token changes & security impact
6. Token cost: ~400 tokens (but replaces 10 manual edits)
```

## Integration with Other Tools

| Tool | When OpenHands Helps |
|------|---------------------|
| **Explore** | After finding "what files exist", use OpenHands for "why it fails" |
| **DSPy** | Use DSPy to validate OpenHands suggestions against test cases |
| **LiteLLM** | OpenHands finds work, LiteLLM codes it cheaper |
| **Direct Edits** | Use OpenHands for >3 file changes, direct edit for <3 |

## Cost Breakdown

| Task | Manual | OpenHands | Savings |
|------|--------|-----------|---------|
| Analyze endpoint list | 200 tokens | 50 tokens | 75% ✅ |
| Find import errors | 300 tokens | 150 tokens | 50% ✅ |
| Refactor auth | 800 tokens | 400 tokens | 50% ✅ |
| Design database schema | 1000 tokens | 600 tokens | 40% ✅ |
| **TOTAL/month** | 8000 tokens | 3000 tokens | **63% ✅** |

## Example Invocations

### Example 1: Quick Endpoint List
```
openhands: "List all endpoints in backend/main_supabase.py with their HTTP methods"

Result:
GET  /health
POST /api/auth/login-novo
POST /api/auth/login-offline
GET  /api/auth/status/{email}

Cost: 40 tokens (vs 200 manual grep searches)
```

### Example 2: Dependency Check
```
openhands: "Cross-reference all Python imports against requirements.txt and report missing packages"

Result:
✅ fastapi==0.110.0
✅ sqlalchemy==2.0.28
✅ psycopg2-binary==2.9.9
❌ geoip2 (imported but NOT in requirements.txt)
❌ security_advanced_blocks (imported but FILE MISSING)

Recommendations:
1. Add to requirements.txt: geoip2==4.7.0
2. Create file: backend/security_advanced_blocks.py
3. OR remove imports from main_enterprise.py

Cost: 120 tokens (vs 500+ manual investigation)
```

### Example 3: Production Readiness
```
openhands: "Full production readiness audit of backend"

Result:
🟢 API Layer: Ready
  - 4 endpoints functional
  - Error handling present
  - CORS configured

🟡 Authentication: Partial
  - Hardcoded users (OK for MVP)
  - No JWT (needs 2 hours)

🔴 Testing: Missing
  - No test files
  - No CI/CD pipeline

💡 Recommendations:
1. Add pytest tests (2 hours)
2. Implement JWT (1 hour)
3. Set up GitHub Actions (1 hour)
4. Deploy to Railway (30 min)

Total: 4 hours → Production-ready
Cost: 250 tokens (vs 1000+ manual audit)
```

## Monthly Token Budget

```
Backend work: 2000 tokens/month
- OpenHands analysis: 400 tokens (20%)
- DSPy validation: 300 tokens (15%)
- LiteLLM coding: 600 tokens (30%)
- Direct edits/config: 700 tokens (35%)

Savings vs no agents: ~5000 tokens/month (71% reduction)
```

## Repos This Agent References

- **OpenHands** (github.com/All-Hands-AI/OpenHands) - Main logic
- **Langflow** (github.com/langflow-ai/langflow) - FastAPI patterns
- **Supabase** (github.com/supabase/supabase) - Database best practices
- **FastAPI docs** - API design validation

## Important Notes

⚠️ **OpenHands is autonomous** - it can run bash, modify files, install packages. Always review its suggestions before applying.

✅ **Use with Explore first** - Get file list from Explore, send to OpenHands for deep analysis.

💡 **Combine with DSPy** - OpenHands proposes, DSPy validates against your business logic.

---

**Status**: Ready to use  
**Last Updated**: 04/09/2026  
**Token Efficiency**: 60-70% savings vs manual work
