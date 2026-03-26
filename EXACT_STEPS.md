# EXACT STEPS - What to Do Right Now

## ✅ Your Code is Ready and Tested!

All tools are working. Now follow these exact steps to deploy.

---

## STEP 1: Upload to Cloud Shell (2 minutes)

### Option A: Via GitHub (Recommended)

**On your Windows machine:**
1. Open terminal in your project folder
2. Run these commands:
```bash
git init
git add .
git commit -m "Underwriting agent ready"
```

3. Go to github.com → New repository → Name it "underwriting-agent"
4. Copy the commands GitHub shows you, something like:
```bash
git remote add origin https://github.com/YOUR_USERNAME/underwriting-agent.git
git branch -M main
git push -u origin main
```

**In Cloud Shell:**
1. Go to console.cloud.google.com
2. Click terminal icon (>_) top-right
3. Run:
```bash
git clone https://github.com/YOUR_USERNAME/underwriting-agent.git
cd underwriting-agent
```

### Option B: Direct Upload (Easier but slower)

**In Cloud Shell:**
1. Go to console.cloud.google.com
2. Click terminal icon (>_) top-right
3. Click 3-dot menu → Upload
4. Select your entire `underwriting_agent` folder (or zip it first)
5. Wait for upload
6. Run:
```bash
cd underwriting-agent
```

---

## STEP 2: Test in Cloud Shell (3 minutes)

**In Cloud Shell, run these commands:**

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > underwriting/.env << 'EOF'
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=AIzaSyA62uqbbMY9yHGL5uMV7Am2IEIkucz02DU
MODEL_NAME=gemini-2.0-flash
EOF

# Test the tools
python test_local.py
```

**Expected output:**
```
================================================================================
TESTING UNDERWRITING TOOLS
================================================================================

1. Parsing applicant input...
✓ Parsed: Priya Sharma, gig_worker

2. Enriching with alternative data...
✓ Enriched with 18 features
...
✅ ALL TOOLS WORKING CORRECTLY!
```

**If you see this, continue to Step 3!**

---

## STEP 3: Deploy to Cloud Run (7 minutes)

**Still in Cloud Shell, run these commands one by one:**

### Command 1: Enable APIs
```bash
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com
```

Wait for "Operation finished successfully" message.

### Command 2: Store API Key
```bash
echo -n "AIzaSyA62uqbbMY9yHGL5uMV7Am2IEIkucz02DU" | \
  gcloud secrets create GOOGLE_API_KEY --data-file=-
```

**If you get "already exists" error:**
```bash
gcloud secrets delete GOOGLE_API_KEY
# Then run the create command again
```

### Command 3: Deploy
```bash
adk deploy cloud_run \
  --project=multiml-agent \
  --region=asia-south1 \
  --service_name=underwriting-agent \
  .
```

**This takes 5-7 minutes. You'll see:**
- "Building container image..."
- "Pushing to Artifact Registry..."
- "Deploying to Cloud Run..."
- "Service [underwriting-agent] deployed successfully"

### Command 4: Get Your URL
```bash
gcloud run services describe underwriting-agent \
  --region=asia-south1 \
  --format='value(status.url)'
```

**Copy the URL that appears!**

---

## STEP 4: Test Your Live Service (2 minutes)

### Test 1: API Test in Cloud Shell
```bash
# Replace YOUR_SERVICE_URL with the URL from Step 3
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

You should see JSON output with the decision.

### Test 2: Browser Test
1. Copy your service URL
2. Open it in a new browser tab
3. You should see the web UI with the form
4. Click "Process Application"
5. Watch the 4 agents animate
6. See the final decision card

---

## ALTERNATIVE: Use the Automated Script

I created `deploy.sh` for you. In Cloud Shell, just run:

```bash
# Make it executable
chmod +x deploy.sh

# Run it
./deploy.sh
```

This runs all the commands automatically!

---

## What Each File Does

- `test_local.py` - Tests all tools work (run this in Cloud Shell first)
- `deploy.sh` - Automated deployment script (Linux/Cloud Shell)
- `deploy.bat` - Automated deployment script (Windows, but use .sh in Cloud Shell)
- `underwriting/agent.py` - Your 4 agents
- `underwriting/tools.py` - All 15+ tools
- `static/index.html` - Web UI

---

## Timeline

- Upload to Cloud Shell: 2 minutes
- Test tools: 3 minutes
- Enable APIs: 2 minutes
- Deploy: 7 minutes
- **Total: ~15 minutes**

---

## After Deployment

You'll have:
- ✅ Live public HTTPS URL
- ✅ Web UI with animated agent pipeline
- ✅ API endpoint for programmatic access
- ✅ Auto-scaling serverless deployment
- ✅ Ready for hackathon demo

---

## Next Steps for Hackathon

1. **Practice your demo** with different applicant profiles
2. **Prepare talking points** about the adversarial pattern
3. **Test different scenarios:**
   - Low risk (salaried, high income)
   - Medium risk (gig worker, moderate income)
   - High risk (young, low income, short employment)
4. **Highlight the bias detection** - this is your USP!

---

## Need Help?

**Check logs:**
```bash
gcloud run services logs read underwriting-agent --region=asia-south1
```

**Verify APIs are enabled:**
```bash
gcloud services list --enabled
```

**Check secret exists:**
```bash
gcloud secrets list
```

---

**You're ready! Follow the steps above and you'll have a live demo in 15 minutes.**
