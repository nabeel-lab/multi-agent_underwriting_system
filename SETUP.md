# Complete Setup Guide

## What You Need to Do (Prerequisites)

### 1. Google Cloud Account Setup

**Create a Google Cloud Project:**
1. Go to console.cloud.google.com
2. Click "Select a project" → "New Project"
3. Name it (e.g., "underwriting-agent")
4. Note down your **Project ID** (not the name - the ID shown below the name)

**Enable Billing:**
1. Go to Billing in the left menu
2. Link a billing account
3. Add credits if you have a promo code

**Get Gemini API Key:**
1. Go to aistudio.google.com
2. Click "Get API Key"
3. Create a new key or use existing
4. Copy the key - you'll need it in Step 4 of deployment

### 2. Install Local Tools

**Python 3.11+:**
```bash
python --version  # Should show 3.11 or higher
```
If not installed, download from python.org

**Google Cloud SDK (gcloud CLI):**
- Download from cloud.google.com/sdk
- Run the installer
- Verify: `gcloud --version`

**Install ADK:**
```bash
pip install google-adk
```

### 3. Local Testing (Before Cloud Deployment)

```bash
# Clone or download this project
cd underwriting_agent

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp underwriting/.env.example underwriting/.env

# Edit .env and add your Gemini API key
# On Windows: notepad underwriting/.env
# Add: GOOGLE_API_KEY=your_actual_key_here

# Test locally
python demo.py
```

If `demo.py` runs successfully and prints a final decision, you're ready to deploy!

### 4. Deploy to Cloud Run

**Open Google Cloud Shell:**
- Go to console.cloud.google.com
- Click the terminal icon (top-right, looks like `>_`)
- A terminal opens in your browser

**Upload your project:**

Option A - From GitHub:
```bash
git clone https://github.com/YOUR_USERNAME/underwriting_agent.git
cd underwriting_agent
```

Option B - Upload directly:
- Click 3-dot menu in Cloud Shell → Upload
- Select your project folder
- Navigate: `cd underwriting_agent`

**Run deployment commands:**

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs (takes 1-2 minutes)
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com

# Store your Gemini API key as a secret
echo -n "YOUR_GEMINI_API_KEY" | \
  gcloud secrets create GOOGLE_API_KEY --data-file=-

# Install ADK in Cloud Shell
pip install google-adk

# Deploy (takes 5-7 minutes first time)
adk deploy cloud_run \
  --project=YOUR_PROJECT_ID \
  --region=asia-south1 \
  --service_name=underwriting-agent \
  --with_ui \
  .
```

**Get your live URL:**
After deployment completes, you'll see:
```
Service URL: https://underwriting-agent-XXXXX-uc.a.run.app
```

Open that URL in your browser - your agent is live!

## What I Can't Do (You Must Handle)

1. **Create your Google Cloud Project** - I can't access your Google account
2. **Enable billing** - Requires your payment method
3. **Get Gemini API key** - You need to sign in to aistudio.google.com
4. **Run gcloud commands** - I can't execute commands in your Cloud Shell
5. **Download datasets** - The code uses synthetic data, but if you want real datasets from Kaggle/UCI, you need to download them manually

## What I Built for You

✅ Complete 4-agent system with adversarial pattern
✅ XGBoost risk model with SHAP explanations
✅ Alternative data enrichment for APAC markets
✅ All tools with full implementations (no placeholders)
✅ Local demo script for testing
✅ Web UI with animated agent pipeline
✅ Deployment guide for Cloud Run
✅ Proper ADK structure with root_agent

## Testing Checklist

Before deploying, verify:

- [ ] `python demo.py` runs without errors
- [ ] You see output from all 4 agents
- [ ] Final decision JSON is printed
- [ ] .env file exists with your GOOGLE_API_KEY
- [ ] `root_agent` variable exists in agent.py (line 145)

## Deployment Checklist

- [ ] Google Cloud Project created
- [ ] Project ID noted down
- [ ] Billing enabled
- [ ] Gemini API key obtained
- [ ] APIs enabled in Cloud Shell
- [ ] API key stored as secret
- [ ] Deploy command executed
- [ ] Service URL received

## Cost Estimate

For a hackathon demo with moderate usage:
- **Cloud Run**: Free tier (2M requests/month)
- **Gemini API**: Free tier at aistudio.google.com
- **Cloud Build**: 120 build-minutes/day free
- **Total expected cost: $0**

## Troubleshooting

**"ModuleNotFoundError: No module named 'google_adk'"**
```bash
pip install google-adk
```

**"GOOGLE_API_KEY not found"**
- Check that .env file exists in underwriting/ folder
- Verify the key is on the line: GOOGLE_API_KEY=your_key_here
- No quotes needed around the key

**"root_agent not found" during deployment**
- Check line 145 in agent.py
- Must have: `root_agent = decision_agent`

**Deployment fails with permission errors**
```bash
gcloud auth application-default login
```

## Next Steps After Deployment

1. Test your live URL with curl or browser
2. Prepare your hackathon presentation
3. Highlight the adversarial bias detection (this is your USP)
4. Show the SHAP explanations (explainable AI)
5. Demo with different applicant profiles

## Support

- ADK Docs: github.com/google/genai-adk
- Cloud Run Docs: cloud.google.com/run/docs
- Gemini API: ai.google.dev
