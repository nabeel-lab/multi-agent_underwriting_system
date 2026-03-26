#!/bin/bash
# Deployment script for Cloud Shell
# Run this in Google Cloud Shell after uploading your project

set -e  # Exit on error

echo "=========================================="
echo "UNDERWRITING AGENT - CLOUD RUN DEPLOYMENT"
echo "=========================================="

PROJECT_ID="multiml-agent"
REGION="asia-south1"
SERVICE_NAME="underwriting-agent"
API_KEY="AIzaSyA62uqbbMY9yHGL5uMV7Am2IEIkucz02DU"

echo ""
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo ""

# Step 1: Set project
echo "Step 1/5: Setting project..."
gcloud config set project $PROJECT_ID

# Step 2: Enable APIs
echo ""
echo "Step 2/5: Enabling required APIs (takes 1-2 minutes)..."
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com

# Step 3: Store API key
echo ""
echo "Step 3/5: Storing Gemini API key as secret..."
# Check if secret exists
if gcloud secrets describe GOOGLE_API_KEY &>/dev/null; then
    echo "Secret already exists, deleting old one..."
    gcloud secrets delete GOOGLE_API_KEY --quiet
fi
echo -n "$API_KEY" | gcloud secrets create GOOGLE_API_KEY --data-file=-
echo "✓ API key stored securely"

# Step 4: Install ADK
echo ""
echo "Step 4/5: Installing Google ADK..."
pip install google-adk --quiet

# Step 5: Deploy
echo ""
echo "Step 5/5: Deploying to Cloud Run (takes 5-7 minutes)..."
echo "Building container and deploying..."
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=$REGION \
  --service_name=$SERVICE_NAME \
  .

# Get service URL
echo ""
echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')
echo "Your live service URL:"
echo "$SERVICE_URL"
echo ""
echo "Test it with:"
echo "curl -X POST $SERVICE_URL/run -H 'Content-Type: application/json' -d '{\"name\":\"Test\",\"age\":30,\"occupation\":\"salaried\",\"monthly_income_inr\":35000,\"city\":\"Mumbai\",\"years_employed\":3,\"past_claims\":0}'"
echo ""
echo "Or open in browser: $SERVICE_URL"
