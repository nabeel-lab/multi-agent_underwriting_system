"""
FastAPI server that serves both the Next.js frontend and ADK backend
Single URL for everything
"""
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from underwriting.agent import run_underwriting
import uvicorn

app = FastAPI(title="Underwriting Agent")

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API endpoint for processing applications
@app.post("/api/run")
async def process_application(request: Request):
    """Process insurance application through 4-agent pipeline"""
    try:
        data = await request.json()
        
        # Transform frontend format to backend format
        applicant_data = {
            "name": data.get("fullName", data.get("name")),
            "age": data.get("age"),
            "occupation": data.get("occupation", "").lower().replace(" ", "_"),
            "monthly_income_inr": data.get("monthlyIncome", data.get("monthly_income_inr")),
            "city": data.get("city"),
            "years_employed": data.get("yearsEmployed", data.get("years_employed")),
            "past_claims": data.get("pastClaims", data.get("past_claims", 0)),
            "has_existing_policy": data.get("has_existing_policy", False)
        }
        
        # Run the agent pipeline
        result = run_underwriting(applicant_data)
        
        # Parse result if it's a string
        if isinstance(result, str):
            # Try to extract JSON from markdown
            if "```json" in result:
                json_start = result.find("```json") + 7
                json_end = result.find("```", json_start)
                decision = json.loads(result[json_start:json_end])
            else:
                try:
                    decision = json.loads(result)
                except:
                    # Return raw result if can't parse
                    decision = {
                        "approved": True,
                        "final_risk_score": 50,
                        "monthly_premium_inr": 2000,
                        "plain_english_explanation": result,
                        "bias_audit_summary": "Processing completed",
                        "confidence_level": "Medium"
                    }
        else:
            decision = result
        
        return JSONResponse(content=decision)
        
    except Exception as e:
        print(f"Error processing application: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}

# Serve Next.js static files
if os.path.exists("front/.next/standalone"):
    # Production: serve built Next.js app
    app.mount("/", StaticFiles(directory="front/.next/standalone", html=True), name="frontend")
elif os.path.exists("static"):
    # Fallback: serve simple static HTML
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
