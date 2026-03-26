# 🚀 DEPLOY NOW - Copy These Commands

Your GitHub repo: https://github.com/nabeel-lab/multi-agent_underwriting_system.git

---

## OPEN CLOUD SHELL

1. Go to: https://console.cloud.google.com
2. Make sure "multiml-agent" is selected (top bar)
3. Click terminal icon (>_) in top-right
4. Copy-paste the commands below

---

## COPY-PASTE THESE COMMANDS (One block at a time)

### Block 1: Clone and Setup (2 minutes)
```bash
# Clone your repo
git clone https://github.com/nabeel-lab/multi-agent_underwriting_system.git
cd multi-agent_underwriting_system

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > underwriting/.env << 'EOF'
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=AIzaSyA62uqbbMY9yHGL5uMV7Am2IEIkucz02DU
MODEL_NAME=gemini-2.0-flash
EOF

# Test tools
python test_local.py
```

**✅ Wait for:** "ALL TOOLS WORKING CORRECTLY!" message

---

### Block 2: Enable APIs (2 minutes)
```bash
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com
```

**✅ Wait for:** "Operation finished successfully"

---

### Block 3: Store API Key (30 seconds)
```bash
echo -n "AIzaSyA62uqbbMY9yHGL5uMV7Am2IEIkucz02DU" | \
  gcloud secrets create GOOGLE_API_KEY --data-file=-
```

**If error "already exists":**
```bash
gcloud secrets delete GOOGLE_API_KEY
# Then run the create command again
```

---

### Block 4: Deploy (7 minutes)
```bash
adk deploy cloud_run \
  --project=multiml-agent \
  --region=asia-south1 \
  --service_name=underwriting-agent \
  .
```

**✅ Wait for:** "Service [underwriting-agent] deployed successfully"

---

### Block 5: Get Your URL
```bash
gcloud run services describe underwriting-agent \
  --region=asia-south1 \
  --format='value(status.url)'
```

**Copy the URL and open it in your browser!**

---

## 🎉 DONE!

You should see:
- Beautiful web UI
- Application form
- "Process Application" button

Click the button and watch:
1. 🔵 Data Harvesting Agent
2. 🟢 Risk Modelling Agent
3. 🟠 Adversarial Agent (bias detection)
4. 🟣 Decision Agent
5. Final decision card with risk score and premium

---

## Test API (Optional)

```bash
# Replace YOUR_URL with your actual service URL
curl -X POST https://YOUR_URL/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "age": 30,
    "occupation": "salaried",
    "monthly_income_inr": 35000,
    "city": "Mumbai",
    "years_employed": 3,
    "past_claims": 0
  }'
```

---

## View Logs

```bash
gcloud run services logs read underwriting-agent --region=asia-south1 --limit=50
```

---

## Redeploy (After Code Changes)

```bash
cd multi-agent_underwriting_system
git pull
adk deploy cloud_run --project=multiml-agent --region=asia-south1 --service_name=underwriting-agent .
```

---

## 🎯 Timeline

- Clone & test: 3 minutes
- Enable APIs: 2 minutes
- Deploy: 7 minutes
- **Total: 12 minutes**

---

**That's it! Just copy-paste the blocks above in Cloud Shell and you're live! 🚀**
