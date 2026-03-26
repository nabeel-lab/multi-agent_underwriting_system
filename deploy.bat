@echo off
REM Deployment script for Cloud Shell (Windows batch version)
REM Run this in Google Cloud Shell

echo ==========================================
echo UNDERWRITING AGENT - CLOUD RUN DEPLOYMENT
echo ==========================================

set PROJECT_ID=multiml-agent
set REGION=asia-south1
set SERVICE_NAME=underwriting-agent
set API_KEY=AIzaSyA62uqbbMY9yHGL5uMV7Am2IEIkucz02DU

echo.
echo Project: %PROJECT_ID%
echo Region: %REGION%
echo Service: %SERVICE_NAME%
echo.

REM Step 1: Set project
echo Step 1/5: Setting project...
gcloud config set project %PROJECT_ID%

REM Step 2: Enable APIs
echo.
echo Step 2/5: Enabling required APIs (takes 1-2 minutes)...
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com secretmanager.googleapis.com

REM Step 3: Store API key
echo.
echo Step 3/5: Storing Gemini API key as secret...
echo %API_KEY% | gcloud secrets create GOOGLE_API_KEY --data-file=-

REM Step 4: Install ADK
echo.
echo Step 4/5: Installing Google ADK...
pip install google-adk

REM Step 5: Deploy
echo.
echo Step 5/5: Deploying to Cloud Run (takes 5-7 minutes)...
adk deploy cloud_run --project=%PROJECT_ID% --region=%REGION% --service_name=%SERVICE_NAME% .

REM Get service URL
echo.
echo ==========================================
echo DEPLOYMENT COMPLETE!
echo ==========================================
echo.
gcloud run services describe %SERVICE_NAME% --region=%REGION% --format="value(status.url)"
echo.
echo Open the URL above in your browser!
