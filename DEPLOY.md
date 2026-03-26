# Deployment Guide - Google Cloud Run

This guide walks you through deploying your underwriting agent to Google Cloud Run using a single ADK command.

## Prerequisites Checklist

Before deploying, ensure you have:

- ✅ Google Cloud Project created with Project ID
- ✅ Billing enabled on your project
- ✅ Gemini API key from aistudio.google.com
- ✅ gcloud CLI installed locally OR access to Google Cloud Shell

## Deployment Steps

### Step 1: Upload Project to Cloud Shell

Open Google Cloud Shell (click the terminal icon in Google Cloud Console top-right).

**Option A - Clone from GitHub:**
```bash
git clone https://github.com/YOUR_USERNAME/underwriting_agent.git
cd underwriting_agent
```

**Option B - Upload files directly:**
- Click the 3-dot menu in Cloud Shell → Upload
- Upload your entire project folder
- Navigate: `cd underwriting_agent`

### Step 2: Authenticate and Set Project

```bash
# Login (if not already authenticated)
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Verify it's set correctly
gcloud config get-value project
```

### Step 3: Enable Required APIs

```bash
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com
```

This takes 1-2 minutes. Wait for confirmation.

### Step 4: Store Your Gemini API Key as a Secret

```bash
# Replace YOUR_GEMINI_API_KEY with your actual key from aistudio.google.com
echo -n "YOUR_GEMINI_API_KEY" | \
  gcloud secrets create GOOGLE_API_KEY --data-file=-

# Verify it was created
gcloud secrets list
```

### Step 5: Install ADK in Cloud Shell

```bash
pip install google-adk
```

### Step 6: Deploy with One Command

```bash
adk deploy cloud_run \
  --project=YOUR_PROJECT_ID \
  --region=asia-south1 \
  --service_name=underwriting-agent \
  --with_ui \
  .
```

**What this does:**
- Packages your code into a container
- Builds the image using Cloud Build
- Pushes to Artifact Registry
- Deploys to Cloud Run
- Exposes a public HTTPS endpoint
- Includes ADK's built-in UI

**Deployment time:** 5-7 minutes first time, 2-3 minutes for updates

### Step 7: Get Your Live URL

After deployment completes, you'll see output like:

```
Service [underwriting-agent] deployed successfully.
Service URL: https://underwriting-agent-XXXXX-uc.a.run.app
```

**Copy that URL** - this is your live demo link!

## Testing Your Deployment

### Test with curl:

```bash
curl -X POST https://YOUR_SERVICE_URL/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priya Sharma",
    "age": 28,
    "occupation": "gig_worker",
    "monthly_income_inr": 22000,
    "city": "Hyderabad",
    "years_employed": 1.5,
    "past_claims": 0
  }'
```

### Test with browser:

Open `https://YOUR_SERVICE_URL` in your browser to see the ADK UI.

## Updating Your Deployment

Made changes? Just run the deploy command again:

```bash
adk deploy cloud_run \
  --project=YOUR_PROJECT_ID \
  --region=asia-south1 \
  --service_name=underwriting-agent \
  .
```

ADK handles versioning automatically.

## Troubleshooting

**"Permission denied" errors:**
```bash
gcloud auth application-default login
```

**"API not enabled" errors:**
Re-run Step 3 and wait for all APIs to fully enable.

**"Secret not found" errors:**
Re-run Step 4 and verify with `gcloud secrets list`

**Deployment fails with "root_agent not found":**
Check that `agent.py` has `root_agent = decision_agent` at the bottom.

**Want to see logs:**
```bash
gcloud run services logs read underwriting-agent --region=asia-south1
```

## Cost Estimate

- Cloud Run: Free tier covers 2 million requests/month
- Gemini API: Free tier at aistudio.google.com
- Cloud Build: 120 build-minutes/day free
- Artifact Registry: 0.5 GB free storage

**Expected cost for hackathon demo: $0**

## Cleanup (After Hackathon)

```bash
# Delete the Cloud Run service
gcloud run services delete underwriting-agent --region=asia-south1

# Delete the container images
gcloud artifacts repositories delete cloud-run-source-deploy --location=asia-south1
```

---

## Quick Reference

**Deploy command:**
```bash
adk deploy cloud_run --project=YOUR_PROJECT_ID --region=asia-south1 --service_name=underwriting-agent --with_ui .
```

**View logs:**
```bash
gcloud run services logs read underwriting-agent --region=asia-south1 --limit=50
```

**Get service URL:**
```bash
gcloud run services describe underwriting-agent --region=asia-south1 --format='value(status.url)'
```
