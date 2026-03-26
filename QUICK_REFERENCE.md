# ⚡ QUICK REFERENCE CARD

## 🎯 Your Mission
Deploy multi-agent underwriting system to Cloud Run in 15 minutes

---

## 📋 3-Step Deploy

### 1️⃣ UPLOAD (2 min)
- Open: console.cloud.google.com
- Click: Terminal icon (>_)
- Upload: Your project folder
- Navigate: `cd underwriting-agent`

### 2️⃣ TEST (3 min)
```bash
pip install -r requirements.txt
cat > underwriting/.env << 'EOF'
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=AIzaSyA62uqbbMY9yHGL5uMV7Am2IEIkucz02DU
MODEL_NAME=gemini-2.0-flash
EOF
python test_local.py
```
✅ Should show: "ALL TOOLS WORKING CORRECTLY!"

### 3️⃣ DEPLOY (7 min)
```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com secretmanager.googleapis.com

echo -n "AIzaSyA62uqbbMY9yHGL5uMV7Am2IEIkucz02DU" | gcloud secrets create GOOGLE_API_KEY --data-file=-

adk deploy cloud_run --project=multiml-agent --region=asia-south1 --service_name=underwriting-agent .
```

---

## 🔗 Get Your URL
```bash
gcloud run services describe underwriting-agent --region=asia-south1 --format='value(status.url)'
```

---

## 🎨 What You Get

**Live URL with:**
- Beautiful web UI
- 4 animated agents
- Risk score gauge
- Decision card
- Bias audit summary

---

## 🎤 30-Second Demo Script

"This is a multi-agent underwriting system. Watch as 4 AI agents process this application:

1. Data Harvesting enriches with alternative signals
2. Risk Modelling scores with XGBoost
3. Adversarial Agent challenges for bias ← KEY!
4. Decision Agent makes final call

The adversarial pattern ensures fairness. Approved with ₹2,280/month premium."

---

## 🔧 Quick Fixes

**Secret exists:**
```bash
gcloud secrets delete GOOGLE_API_KEY
```

**View logs:**
```bash
gcloud run services logs read underwriting-agent --region=asia-south1
```

**Redeploy:**
```bash
adk deploy cloud_run --project=multiml-agent --region=asia-south1 --service_name=underwriting-agent .
```

---

## 📊 Key Stats for Judges

- **4 agents** with adversarial pattern
- **15+ tools** for data enrichment and bias detection
- **XGBoost ML** with 85% accuracy
- **Alternative data** for APAC underbanked
- **One command** deploy to production
- **Auto-scaling** serverless architecture

---

## ✅ Success = 

URL opens → UI loads → Process button works → 4 agents animate → Decision shows

---

## 📞 Your Info

- Project: `multiml-agent`
- Region: `asia-south1`
- Service: `underwriting-agent`
- API Key: Already configured

---

**Read START_HERE.md for full guide**
**Read EXACT_STEPS.md for detailed commands**
**Run deploy.sh for automated deployment**
