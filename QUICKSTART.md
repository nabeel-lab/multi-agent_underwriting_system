# ⚡ Quick Start - 5 Minutes to Deploy

## Prerequisites (Do These First)

1. **Google Cloud Project** → console.cloud.google.com → Create Project → Note the Project ID
2. **Gemini API Key** → aistudio.google.com → Get API Key → Copy it
3. **Enable Billing** → Add payment method in Google Cloud Console

## Local Test (2 minutes)

```bash
# Install
pip install -r requirements.txt

# Configure
cp underwriting/.env.example underwriting/.env
# Edit .env and paste your Gemini API key

# Test
python demo.py
```

✅ If you see a final decision printed, you're ready to deploy!

## Deploy to Cloud (3 minutes)

**Open Google Cloud Shell** (terminal icon in console.cloud.google.com)

```bash
# Upload your project (or git clone it)
# Then run these commands:

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

**Wait 5-7 minutes** → Get your live URL → Open in browser → Done!

## Test Your Live Service

```bash
curl -X POST https://YOUR_SERVICE_URL/run \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","age":30,"occupation":"salaried","monthly_income_inr":35000,"city":"Mumbai","years_employed":3,"past_claims":0}'
```

## What Makes This Hackathon-Worthy

1. **4-Agent Architecture** - Not just one LLM call, but orchestrated specialists
2. **Adversarial Pattern** - Agent 3 actively challenges Agent 2 for bias
3. **Real ML Model** - XGBoost trained on synthetic credit data
4. **Explainable AI** - SHAP values show feature contributions
5. **Alternative Data** - APAC-relevant signals (utility, mobile, gig income)
6. **Production Ready** - One command deploys to Cloud Run with public URL
7. **Bias Detection** - Checks age, location, occupation discrimination

## Demo Script for Judges

"This is a multi-agent insurance underwriting system. Watch as 4 specialized agents process this application:

1. Data Harvesting enriches the profile with alternative data
2. Risk Modelling scores with XGBoost and explains with SHAP
3. Adversarial Agent challenges the score for bias - this is key
4. Decision Agent synthesizes everything into a final call

The adversarial debate ensures fairness. Let me show you a gig worker application..."

[Show the UI with animated agent steps]

## Files You Need to Know

- `underwriting/agent.py` - All 4 agents defined here
- `underwriting/tools.py` - All tool functions (data enrichment, ML scoring, bias detection)
- `demo.py` - Local testing script
- `DEPLOY.md` - Detailed deployment guide
- `static/index.html` - Web UI

## Troubleshooting

**Error: "root_agent not found"**
→ Check line 145 in agent.py has: `root_agent = decision_agent`

**Error: "GOOGLE_API_KEY not set"**
→ Check .env file exists and has your key

**Deployment hangs:**
→ Check all APIs are enabled (Step 2)

**Want to see logs:**
```bash
gcloud run services logs read underwriting-agent --region=asia-south1
```

---

**You're ready to deploy! Follow the steps above and you'll have a live demo in under 10 minutes.**
