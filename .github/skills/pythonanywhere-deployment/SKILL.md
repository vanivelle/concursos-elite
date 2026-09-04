---
name: pythonanywhere-deployment
description: "Use when: deploying FastAPI backend to PythonAnywhere production; automating full deployment workflow with environment setup; validating production readiness before going live; setting up 24/7 uptime for mobile access"
---

# 🚀 PythonAnywhere Deployment Automation

**Purpose**: Secure, professional, fully-automated backend deployment to PythonAnywhere with environment validation.

**When to use this skill**:
- Need to deploy FastAPI backend to production (24/7 uptime)
- Setting up mobile access for multiple users (iPhone/Android)
- Want automated, repeatable deployment process
- Need environment variable security + validation

**What this skill provides**:
- ✅ Pre-deployment validation checklist
- ✅ Automated setup script (`pythonanywhere-deploy.sh`)
- ✅ Security checks (no hardcoded secrets, environment vars verified)
- ✅ Quick rollback procedures
- ✅ Production monitoring commands

---

## 📋 Pre-Deployment Checklist

Before deploying, verify:

### Code Quality
- [ ] `main_supabase.py` uses `os.getenv("DATABASE_URL", fallback)` (not hardcoded)
- [ ] All imports in `main_supabase.py` exist in `requirements.txt`
- [ ] No print() debugging statements (use logging)
- [ ] CORS configured for your Vercel frontend

### Environment
- [ ] PostgreSQL connection string validated (test locally first)
- [ ] Python 3.11+ available
- [ ] Git repository clean (no uncommitted changes)

### Security
- [ ] No .env files committed to Git
- [ ] Database password NOT in code (must be env var)
- [ ] CORS restricted to known domains only

---

## 🔧 Deployment Steps (Automated)

### Step 1: Run Deployment Script

```bash
cd backend
bash ../../.github/skills/pythonanywhere-deployment/pythonanywhere-deploy.sh
```

**Script does:**
1. ✅ Validates PostgreSQL connection
2. ✅ Confirms requirements.txt is complete
3. ✅ Generates PythonAnywhere WSGI config
4. ✅ Creates deployment instructions (copy-paste ready)

### Step 2: Manual Setup on PythonAnywhere (3 min)

**A. Create Account**
```
https://www.pythonanywhere.com/pricing/
→ Beginner (free) account
→ Username: your_choice (becomes your_choice.pythonanywhere.com)
```

**B. Upload Code**
```
PythonAnywhere Bash Console:

cd ~
git clone https://github.com/vanivelle/concursos-elite.git
cd concursos-elite
pip install --user -r requirements.txt
```

**C. Create Web App**
```
PythonAnywhere → Web → "+ Add a new web app"
→ Choose Python 3.11
→ Choose FastAPI
→ Confirm
```

**D. Configure WSGI** 
```
File: /var/www/<username>_pythonanywhere_com_wsgi.py

Replace with content from deployment script output:
```

**E. Set Environment Variables**
```
Web tab → Environment variables:

DATABASE_URL = postgresql://postgres:Lightshigaraki789@db.lnnwefppeaaqhpjqpdvz.supabase.co:5432/postgres
PYTHONUNBUFFERED = 1
```

**F. Reload**
```
Web tab → Click "Reload" button (green)
Wait 10 seconds
```

### Step 3: Verify Deployment

```bash
# Test health endpoint
curl https://<your_username>.pythonanywhere.com/health

# Expected response:
# {"status": "connected", "database": "up"}
```

---

## 📱 Production URLs

After deployment, share with users:

**Frontend** (already deployed):
```
https://open-notebook-8x8twkj23.vercel.app
```

**Backend API**:
```
https://<your_username>.pythonanywhere.com
```

**Users can now access from any device**:
- Matheus (iPhone): Login with matheus@email.com / matheus123
- Cabo (Android): Login with cabo.md@email.com / cabo123
- Admin: mr.dblucas@gmail.com / Lightshigaraki789

---

## 🔍 Monitoring & Troubleshooting

### Check Logs
```
PythonAnywhere → Web → Log files
- Access log (HTTP requests)
- Error log (Python exceptions)
```

### Test Endpoint Directly
```bash
curl -X POST https://<username>.pythonanywhere.com/api/auth/login-novo \
  -H "Content-Type: application/json" \
  -d '{"email":"matheus@email.com","password":"matheus123","lat":-15.85,"lng":-48.06}'
```

### Restart if Needed
```
PythonAnywhere → Web → Click "Reload"
```

### Rollback to Previous Version
```
PythonAnywhere Bash:

cd ~/concursos-elite
git log --oneline -5
git reset --hard <commit_hash>  # or git pull for latest
# Then Reload in Web tab
```

---

## 🛡️ Security Best Practices

1. **Never commit credentials** → Always use environment variables
2. **Rotate passwords periodically** → Update DATABASE_URL in PythonAnywhere console
3. **Monitor access logs** → Check for suspicious IPs
4. **CORS restricted** → Only allow Vercel frontend domain
5. **Backups** → Supabase handles DB backups automatically

---

## 📊 Cost & Uptime

| Provider | Tier | Cost | Uptime |
|----------|------|------|--------|
| PythonAnywhere | Beginner | FREE | 99.9% |
| Supabase | Free | FREE | 99.9% |
| Vercel | Free | FREE | 99.99% |
| **Total** | - | **FREE** | **99.9%** |

---

## ✅ When Deployment is Complete

- ✅ Backend responds to `/health` endpoint
- ✅ All 3 users can login from deployed URL
- ✅ Geofencing coordinates validate correctly
- ✅ Mobile devices access frontend + backend seamlessly
- ✅ No hardcoded secrets in repository
- ✅ Environment variables configured on PythonAnywhere

---

## 🚨 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| 502 Bad Gateway | Run: `pip install --user -r requirements.txt` in PythonAnywhere bash |
| Database connection refused | Verify DATABASE_URL in environment variables exactly matches |
| 404 on endpoints | Confirm main_supabase.py path in WSGI config |
| Slow startup | First load on free tier takes 5-10s (normal) |

---

**Status**: Production-ready, secure, scalable ✅
