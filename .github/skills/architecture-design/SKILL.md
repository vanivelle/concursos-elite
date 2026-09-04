# Concurso Elite Architecture Skill

## Description
Autonomous analysis and optimization of FastAPI + Supabase + Geofencing system. Uses OpenHands + DSPy + LiteLLM to reduce token waste and provide production-ready suggestions.

**When to use**: Architecture decisions, backend refactoring, deployment planning, database schema optimization.

---

## Quick Start

```
User: "Is the backend production-ready?"
Agent: Runs OpenHands → analyzes main_supabase.py + requirements.txt + backend folder
Returns: ✅/❌ checklist + token cost breakdown
```

---

## Available Commands

### 1. **Diagnose Backend Health**
```
@architecture-skill diagnose
```
Returns:
- ✅ Working components
- ❌ Missing pieces
- ⚠️ Risk areas
- 💡 Optimizations
- 📊 Token cost

### 2. **Check Deployment Ready**
```
@architecture-skill production-readiness
```
Returns:
- Database connectivity
- API endpoints validated
- Environment variables needed
- Security checks
- Performance baselines

### 3. **Optimize Token Usage**
```
@architecture-skill analyze-tokens
```
Returns:
- Current usage breakdown
- Waste identification
- Agent swap recommendations
- Cached prompt suggestions

### 4. **Suggest Architecture Changes**
```
@architecture-skill recommend {component}
```
Examples:
- `@architecture-skill recommend authentication` 
- `@architecture-skill recommend database`
- `@architecture-skill recommend API-design`

Returns:
- Pros/cons of each pattern
- Implementation effort
- Token savings potential
- Recommended path

---

## Behind the Scenes

### Agents Used
1. **OpenHands** - Full codebase analysis
2. **DSPy** - Structured validation (login checks, geofencing logic)
3. **LiteLLM** - Cost-efficient model routing
4. **Explore** - Quick file/endpoint discovery

### Repos Consulted
- OpenHands (75.8K) - Codebase patterns
- Langflow (194K) - FastAPI best practices
- Supabase (102K) - PostgreSQL patterns
- DSPy (11K) - Validation logic caching
- LiteLLM (56K) - Model routing

### Token Budget
- Single diagnosis: ~100-200 tokens (vs 500+ manual)
- Production check: ~150-300 tokens
- Recommendations: ~200-400 tokens
- **Savings**: 60-70% vs manual approach

---

## Example Outputs

### ✅ Production Readiness Report
```
Backend Health: 🟢 PRODUCTION-READY

✅ API Layer (main_supabase.py)
  - 4 endpoints implemented
  - Health check working
  - CORS configured
  - Error handling present

✅ Database (Supabase PostgreSQL)
  - Connected to db.lnnwefppeaaqhpjqpdvz.supabase.co
  - Credentials in environment
  - 773 questions loaded

⚠️ Geofencing (Partial)
  - Logic in code but not fully integrated
  - Recommendation: Activate in login endpoint

❌ User Authentication
  - Hardcoded users (OK for MVP, not for prod)
  - JWT not implemented
  - Fix: Switch to python-jose (1 hour)

📊 Token Cost: 180 tokens for this full analysis
```

### 💡 Architecture Recommendation
```
Current: main_supabase.py (4 endpoints, works)
Goal: Production backend with 15+ endpoints

Path A (Fast - 8 hours):
  Use main.py (v2.0), add JWT, deploy to Railway
  Token cost: ~400 tokens (design + validation)
  Time: Same-day

Path B (Robust - 24 hours):
  Full OpenHands refactoring, test suite, CI/CD
  Token cost: ~800 tokens
  Time: 1 day

RECOMMENDATION: Path A (you need it today)
```

---

## Cost Tracking

Every `@architecture-skill` call logs:
- Tokens used
- Agents invoked
- Files analyzed
- Recommendations count

Monthly dashboard shows:
- Architecture work tokens
- vs manual exploration
- Savings realized

---

## Files This Covers

```yaml
applyTo:
  - "backend/**/*.py"
  - "requirements.txt"
  - "Procfile"
  - "render.yaml"
  - ".github/copilot-instructions.md"
```

---

## Not Recommended For
- Debugging runtime errors (use Python skill)
- Database migrations (use direct SQL)
- Frontend UI changes (not architecture)
- Dependency version conflicts (use pip directly)

Use this skill for ARCHITECTURE decisions only.
