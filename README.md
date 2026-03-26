# Predictive Insurance Underwriting - Multi-Agent System

A production-ready insurance underwriting system using Google ADK with 4 specialized agents and adversarial bias detection.

## 🎯 What This Does

This system processes insurance applications through a 4-agent pipeline:

1. **Data Harvesting Agent** - Enriches applicant data with alternative signals (utility payments, mobile usage, gig income patterns)
2. **Risk Modelling Agent** - Scores risk using XGBoost ML model with SHAP explanations
3. **Adversarial Agent** - Challenges the score for demographic bias and fairness issues
4. **Decision Agent** - Synthesizes all outputs into final approval decision

The adversarial pattern is the key innovation - Agent 3 actively challenges Agent 2's scoring for bias before the final decision is made.

## 🚀 Quick Start (Local Testing)

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp underwriting/.env.example underwriting/.env
# Edit .env and add your GOOGLE_API_KEY from aistudio.google.com

# Run demo
python demo.py
```

You should see all 4 agents execute and output a final decision.

## ☁️ Deploy to Google Cloud Run

See [DEPLOY.md](DEPLOY.md) for complete deployment instructions.

**TL;DR:**
```bash
adk deploy cloud_run \
  --project=YOUR_PROJECT_ID \
  --region=asia-south1 \
  --service_name=underwriting-agent \
  --with_ui \
  .
```

## 📊 Sample Output

```json
{
  "approved": true,
  "final_risk_score": 45,
  "monthly_premium_inr": 2175,
  "plain_english_explanation": "Application approved with moderate risk. Strong alternative data signals offset gig worker occupation concerns.",
  "bias_audit_summary": "No demographic bias detected. Alternative data quality verified. Score stable under stress tests.",
  "confidence_level": "High"
}
```

## 🏗️ Architecture

```
User Input
    ↓
Decision Agent (Orchestrator)
    ↓
    ├─→ Data Harvesting Agent
    │       ↓ (enriched data)
    ├─→ Risk Modelling Agent
    │       ↓ (risk score + SHAP)
    ├─→ Adversarial Agent ⚔️
    │       ↓ (challenge report)
    └─→ Final Decision
```

## 🔧 Tech Stack

- **Google ADK** - Multi-agent orchestration
- **Gemini 2.0 Flash** - LLM reasoning
- **XGBoost** - Risk scoring ML model
- **SHAP** - Model explainability
- **Cloud Run** - Serverless deployment
- **FastAPI** - API framework (via ADK)

## 📁 Project Structure

```
underwriting_agent/
├── requirements.txt
├── demo.py                    ← Local testing script
├── DEPLOY.md                  ← Deployment guide
├── static/
│   └── index.html            ← Web UI
└── underwriting/
    ├── __init__.py
    ├── agent.py              ← 4 agents defined here
    ├── tools.py              ← All tool functions
    └── .env.example          ← Config template
```

## 🎓 Hackathon Highlights

- **Real ML Model**: XGBoost trained on synthetic credit data
- **Explainable AI**: SHAP values show which features drove the score
- **Bias Detection**: Adversarial agent checks for age, location, occupation discrimination
- **Alternative Data**: Uses APAC-relevant signals (utility payments, mobile recharge, gig income)
- **Production Ready**: One-command deploy to Cloud Run with public HTTPS endpoint
- **Adversarial Debate**: Agent 3 actively challenges Agent 2 - visible in output

## 🔑 Environment Variables

Create `underwriting/.env`:

```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_key_from_aistudio
MODEL_NAME=gemini-2.0-flash
```

## 📝 License

MIT
