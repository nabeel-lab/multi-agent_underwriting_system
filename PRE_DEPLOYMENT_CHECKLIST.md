# ✅ Pre-Deployment Checklist

Use this checklist to verify everything is ready before deploying to Cloud Run.

---

## 📋 PREREQUISITES

### Google Cloud Account
- [ ] Google Cloud account created
- [ ] Billing enabled
- [ ] Credits loaded (if applicable)
- [ ] Project created
- [ ] Project ID written down: `_______________________`

### API Keys
- [ ] Gemini API key obtained from aistudio.google.com
- [ ] API key saved securely
- [ ] API key copied to clipboard for deployment

### Local Tools
- [ ] Python 3.11+ installed (`python --version`)
- [ ] pip installed (`pip --version`)
- [ ] gcloud CLI installed (`gcloud --version`)
- [ ] Code editor available (VS Code, Cursor, Kiro, etc.)

---

## 🧪 LOCAL TESTING

### Environment Setup
- [ ] Project downloaded/cloned to local machine
- [ ] Navigated to project directory: `cd underwriting_agent`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created: `cp underwriting/.env.example underwriting/.env`
- [ ] `.env` file edited with Gemini API key
- [ ] `.env` file saved

### Verify File Structure
- [ ] `underwriting/agent.py` exists
- [ ] `underwriting/tools.py` exists
- [ ] `underwriting/__init__.py` exists
- [ ] `requirements.txt` exists
- [ ] `demo.py` exists
- [ ] `static/index.html` exists

### Run Local Demo
- [ ] Executed: `python demo.py`
- [ ] Saw "Starting 4-agent pipeline..." message
- [ ] Agent 1 (Data Harvesting) executed
- [ ] Agent 2 (Risk Modelling) executed
- [ ] Agent 3 (Adversarial) executed
- [ ] Agent 4 (Decision) executed
- [ ] Final decision JSON printed
- [ ] "Demo completed successfully!" message shown
- [ ] No errors in output

### Verify Code Quality
- [ ] `root_agent` variable exists in `agent.py` (line ~145)
- [ ] All imports work (no ModuleNotFoundError)
- [ ] .env file is in `underwriting/` folder (not root)
- [ ] API key has no extra spaces or quotes

---

## ☁️ CLOUD DEPLOYMENT PREP

### Google Cloud Console
- [ ] Logged into console.cloud.google.com
- [ ] Correct project selected (check top bar)
- [ ] Cloud Shell accessible (terminal icon works)

### Information Ready
- [ ] Project ID ready to paste: `_______________________`
- [ ] Gemini API key ready to paste: `_______________________`
- [ ] Region decided (default: asia-south1)
- [ ] Service name decided (default: underwriting-agent)

### Upload Method Chosen
- [ ] **Option A:** GitHub repo URL ready: `_______________________`
- [ ] **Option B:** Files ready to upload via Cloud Shell

---

## 🚀 DEPLOYMENT COMMANDS READY

Copy these commands and fill in YOUR_PROJECT_ID and YOUR_GEMINI_API_KEY:

```bash
# 1. Set project
gcloud config set project YOUR_PROJECT_ID

# 2. Enable APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com secretmanager.googleapis.com

# 3. Store API key
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets create GOOGLE_API_KEY --data-file=-

# 4. Install ADK
pip install google-adk

# 5. Deploy
adk deploy cloud_run --project=YOUR_PROJECT_ID --region=asia-south1 --service_name=underwriting-agent --with_ui .
```

- [ ] Commands copied to notepad/text editor
- [ ] YOUR_PROJECT_ID replaced with actual project ID
- [ ] YOUR_GEMINI_API_KEY replaced with actual API key
- [ ] Commands ready to paste into Cloud Shell

---

## 🎯 POST-DEPLOYMENT VERIFICATION

After deployment completes:

- [ ] Deployment succeeded (no errors)
- [ ] Service URL received: `_______________________`
- [ ] URL copied to clipboard
- [ ] URL opened in browser
- [ ] Web UI loads correctly
- [ ] Sample form is visible
- [ ] "Process Application" button works
- [ ] All 4 agents animate
- [ ] Final decision card displays
- [ ] Risk score shows
- [ ] Premium amount shows
- [ ] Bias audit summary shows

---

## 🧪 TEST SCENARIOS

Test these applicant profiles to verify different outcomes:

### Test 1: Low Risk (Should Approve)
- [ ] Name: Raj Kumar
- [ ] Age: 35
- [ ] Occupation: salaried
- [ ] Income: 45000
- [ ] City: Bangalore
- [ ] Years: 5
- [ ] Result: Approved with low risk score (<50)

### Test 2: Medium Risk (Should Approve with Higher Premium)
- [ ] Name: Priya Sharma
- [ ] Age: 28
- [ ] Occupation: gig_worker
- [ ] Income: 22000
- [ ] City: Hyderabad
- [ ] Years: 1.5
- [ ] Result: Approved with medium risk score (50-65)

### Test 3: Bias Detection (Should Flag and Adjust)
- [ ] Name: Amit Singh
- [ ] Age: 24
- [ ] Occupation: gig_worker
- [ ] Income: 18000
- [ ] City: Indore
- [ ] Years: 1
- [ ] Result: Adversarial agent flags bias, adjusts score

### Test 4: API Test (Optional)
- [ ] curl command executed successfully
- [ ] JSON response received
- [ ] Response contains all required fields

---

## 📊 DEMO PREPARATION

### Talking Points Ready
- [ ] Opening statement prepared
- [ ] Agent 1 explanation ready
- [ ] Agent 2 explanation ready
- [ ] Agent 3 explanation ready (emphasize adversarial pattern)
- [ ] Agent 4 explanation ready
- [ ] Key differentiators memorized
- [ ] SHAP explanation prepared
- [ ] Alternative data explanation prepared
- [ ] Bias detection explanation prepared

### Demo Flow Practiced
- [ ] Can navigate to URL quickly
- [ ] Can fill form smoothly
- [ ] Can explain each agent as it animates
- [ ] Can interpret final decision
- [ ] Can answer "Why 4 agents?"
- [ ] Can answer "What is adversarial pattern?"
- [ ] Can answer "Why alternative data?"
- [ ] Can answer "How does bias detection work?"

### Backup Plans
- [ ] Screenshots of working demo saved
- [ ] Video recording of demo made (optional)
- [ ] Local demo ready as backup (`python demo.py`)
- [ ] Presentation slides prepared (if required)

---

## 🔧 TROUBLESHOOTING PREP

### Common Issues Reviewed
- [ ] Know how to check Cloud Run logs
- [ ] Know how to restart service if needed
- [ ] Know how to verify API key in Secret Manager
- [ ] Know how to check enabled APIs
- [ ] Have TROUBLESHOOTING section bookmarked

### Emergency Contacts
- [ ] Hackathon support contact: `_______________________`
- [ ] Team member contact: `_______________________`
- [ ] Backup person who can help: `_______________________`

---

## 📚 DOCUMENTATION REVIEWED

- [ ] Read QUICKSTART.md
- [ ] Read YOUR_ACTION_ITEMS.md
- [ ] Skimmed ARCHITECTURE.md (for technical questions)
- [ ] Bookmarked DEPLOY.md (for reference)
- [ ] Know where to find TROUBLESHOOTING section

---

## 🎯 FINAL GO/NO-GO

### All Systems Green?
- [ ] Local demo works perfectly
- [ ] Cloud deployment successful
- [ ] Live URL accessible
- [ ] All test scenarios pass
- [ ] Demo practiced and ready
- [ ] Talking points memorized
- [ ] Backup plans in place

### Ready to Deploy?
- [ ] **YES** - All checkboxes above are checked
- [ ] **NO** - Review unchecked items and complete them

---

## 🚀 DEPLOYMENT DAY

### Morning Of
- [ ] Test local demo one more time
- [ ] Verify live URL still works
- [ ] Check Cloud Run service status
- [ ] Test with fresh browser (clear cache)
- [ ] Charge laptop fully
- [ ] Have backup internet (mobile hotspot)

### During Demo
- [ ] Speak clearly and confidently
- [ ] Emphasize adversarial pattern (your USP)
- [ ] Show bias detection in action
- [ ] Explain SHAP values
- [ ] Mention production readiness
- [ ] Answer questions calmly
- [ ] Have fun!

---

## 📝 NOTES SECTION

Use this space for any additional notes or reminders:

```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

---

**When all checkboxes are complete, you're ready to deploy! 🚀**

**Estimated time to complete checklist: 30-45 minutes**

**Good luck with your hackathon!**
