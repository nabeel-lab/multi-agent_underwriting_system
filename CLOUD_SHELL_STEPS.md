# Exact Steps for Cloud Shell Testing & Deployment

## PART 1: Push Code to GitHub (On Your Windows Machine)

### Option A: If you have Git installed
```bash
# Initialize git repo
git init
git add .
git commit -m "Initial commit - underwriting agent"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/underwriting-agent.git
git push -u origin main
```

### Option B: Manual Upload to GitHub
1. Go to github.com
2. Click "New repository"
3. Name it "underwriting-agent"
4. Click "uploading an existing file"
5. Drag and drop your entire project folder
6. Commit

---

## PART 2: Test in Cloud Shell (Before Deploying)

### Step 1: Open Cloud Shell
1. Go to https://console.cloud.google.com
2. Make sure "multiml-agent" project is selected (top bar)
3. Click the terminal icon (>_) in top-right
4. Cloud Shell opens in browser

### Step 2: Clone Your Project
```bash
# Clone from GitHub
git clone https://github.com/YOUR_USERNAME/underwriting-agent.git
cd underwriting-agent

# OR if you don't have GitHub, upload files:
# Click 3-dot menu → Upload → Select your folder
# Then: cd underwriting-agent
```

### Step 3: Install Dependencies in Cloud Shell
```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 4: Create .env File in Cloud Shell
```bash
# Create the .env file
cat > underwriting/.env << 'EOF'
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=AIzaSyA62uqbbMY9yHGL5uMV7Am2IEIkucz02DU
MODEL_NAME=gemini-2.0-flash
EOF
```

### Step 5: Test Tools in Cloud Shell
```bash
# Run the tool test
python test_local.py
```

**Expected output:**
- All 7 tools execute successfully
- Risk score calculated
- Bias checks completed
- "✅ ALL TOOLS WORKING CORRECTLY!" message

**If this works, you're ready to deploy!**

---

## PART 3: Deploy to Cloud Run (After Testing)

### Step 1: Enable Required APIs
```bash
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com
```

Wait 1-2 minutes for APIs to enable.

### Step 2: Store API Key as Secret
```bash
echo -n "AIzaSyA62uqbbMY9yHGL5uMV7Am2IEIkucz02DU" | \
  gcloud secrets create GOOGLE_API_KEY --data-file=-
```

**If you get "already exists" error:**
```bash
gcloud secrets delete GOOGLE_API_KEY
# Then run the create command again
```

### Step 3: Deploy with ADK
```bash
adk deploy cloud_run \
  --project=multiml-agent \
  --region=asia-south1 \
  --service_name=underwriting-agent \
  .
```

**This takes 5-7 minutes.** You'll see:
- Building container image
- Pushing to Artifact Registry
- Deploying to Cloud Run
- Service URL at the end

### Step 4: Get Your Live URL
After deployment completes, run:
```bash
gcloud run services describe underwriting-agent \
  --region=asia-south1 \
  --format='value(status.url)'
```

Copy that URL - this is your live service!

---

## PART 4: Test Your Deployed Service

### Test with curl in Cloud Shell:
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

### Test in Browser:
Open the URL in your browser - you should see the web UI!

---

## Quick Reference Commands

**View logs:**
```bash
gcloud run services logs read underwriting-agent --region=asia-south1 --limit=50
```

**Update deployment (after code changes):**
```bash
# Pull latest code
git pull

# Redeploy
adk deploy cloud_run --project=multiml-agent --region=asia-south1 --service_name=underwriting-agent .
```

**Delete service (cleanup):**
```bash
gcloud run services delete underwriting-agent --region=asia-south1
```

---

## Troubleshooting

**"Permission denied":**
```bash
gcloud auth application-default login
```

**"API not enabled":**
Wait 2 minutes after enabling APIs, then retry

**"Secret already exists":**
```bash
gcloud secrets delete GOOGLE_API_KEY
# Then create again
```

**Deployment fails:**
```bash
# Check build logs
gcloud builds list --limit=5

# Check specific build
gcloud builds log BUILD_ID
```

---

## Summary

1. **On Windows:** Push code to GitHub
2. **In Cloud Shell:** Clone → Install deps → Test tools
3. **In Cloud Shell:** Enable APIs → Store secret → Deploy
4. **Get URL:** Test in browser

**Total time: ~15 minutes**
