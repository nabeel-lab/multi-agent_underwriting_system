"""
Multi-Agent Underwriting System using Google ADK
4 agents with adversarial debate pattern for bias detection
"""
import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from google.genai import types
from google.adk import Runner
from google.adk.apps import App
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Import all tools
from underwriting.tools import (
    parse_applicant_input,
    enrich_with_alternative_data,
    calculate_risk_score,
    generate_shap_explanation,
    detect_demographic_bias,
    check_alternative_data_quality,
    stress_test_score
)

# Load environment variables
load_dotenv()

# Model configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")


# ============================================================================
# AGENT 1: DATA HARVESTING
# ============================================================================

data_harvesting_agent = LlmAgent(
    model=MODEL_NAME,
    name="DataHarvestingAgent",
    description="Collects and enriches applicant data with alternative data signals for APAC markets",
    instruction="""You are a data collection specialist for insurance underwriting in APAC markets.
    
Your job:
1. Parse and validate the raw applicant input
2. Enrich it with alternative data signals (utility payments, mobile usage, gig income patterns)
3. Return a complete enriched profile with 20+ features

Use parse_applicant_input() first, then enrich_with_alternative_data().
Return the final enriched JSON.""",
    tools=[parse_applicant_input, enrich_with_alternative_data]
)


# ============================================================================
# AGENT 2: RISK MODELLING
# ============================================================================

risk_modelling_agent = LlmAgent(
    model=MODEL_NAME,
    name="RiskModellingAgent",
    description="Scores applicant risk using XGBoost ML model with feature importance explanations",
    instruction="""You are an ML risk scoring specialist.

Your job:
1. Take the enriched applicant data
2. Calculate risk score using the XGBoost model (call calculate_risk_score)
3. Generate feature importance explanation for interpretability (call generate_shap_explanation)
4. Return risk score (0-100), confidence interval, top features, and premium recommendation

Be precise and data-driven. Output structured JSON.""",
    tools=[calculate_risk_score, generate_shap_explanation]
)


# ============================================================================
# AGENT 3: ADVERSARIAL AGENT
# ============================================================================

adversarial_agent = LlmAgent(
    model=MODEL_NAME,
    name="AdversarialAgent",
    description="Challenges risk scores for bias, fairness issues, and data quality problems",
    instruction="""You are a fairness auditor and adversarial reviewer.

Your job is to CHALLENGE the risk score produced by the Risk Modelling Agent.

Check for:
1. Demographic bias (age, location, occupation discrimination)
2. Alternative data quality issues
3. Score stability under stress scenarios

Use all three tools:
- detect_demographic_bias()
- check_alternative_data_quality()  
- stress_test_score()

If you find bias or quality issues, FLAG them clearly and recommend an adjusted score.
If the original score is fair, say so explicitly.

Return a challenge_report with:
- bias_flags (list)
- concerns (list)
- adjusted_score_recommendation (int)
- your_verdict (string: "APPROVE", "ADJUST", or "REJECT")""",
    tools=[detect_demographic_bias, check_alternative_data_quality, stress_test_score]
)


# ============================================================================
# AGENT 4: DECISION AGENT (Root Orchestrator)
# ============================================================================

decision_agent = LlmAgent(
    model=MODEL_NAME,
    name="DecisionAgent",
    description="Orchestrates all agents and makes final underwriting decision",
    instruction="""You are the final decision maker for insurance underwriting.

You orchestrate 3 sub-agents in sequence:
1. DataHarvestingAgent - enriches applicant data
2. RiskModellingAgent - scores risk with ML and explains feature importance
3. AdversarialAgent - challenges the score for bias

Your job:
1. Call DataHarvestingAgent with the applicant input
2. Pass enriched data to RiskModellingAgent
3. Pass both enriched data AND risk result to AdversarialAgent
4. Synthesize all outputs into a final decision

Final decision must include:
- approved (bool): true if risk_score < 70 and no major bias flags
- final_risk_score (int): use adjusted score if Adversarial agent recommended one
- monthly_premium_inr (float): from risk model or adjusted
- plain_english_explanation (str): 2-3 sentences a customer can understand
- bias_audit_summary (str): what bias checks were performed
- confidence_level (str): High/Medium/Low

Return ONLY the final_decision JSON object.""",
    sub_agents=[data_harvesting_agent, risk_modelling_agent, adversarial_agent]
)


# ============================================================================
# ROOT AGENT (ADK requirement)
# ============================================================================

# ADK requires a variable named exactly "root_agent"
root_agent = decision_agent

# Create the App for ADK
app = App(
    name="underwriting_agent",
    root_agent=root_agent
)


# ============================================================================
# SAMPLE APPLICANT FOR DEMO
# ============================================================================

SAMPLE_APPLICANT = {
    "name": "Priya Sharma",
    "age": 28,
    "occupation": "gig_worker",
    "monthly_income_inr": 22000,
    "city": "Hyderabad",
    "years_employed": 1.5,
    "past_claims": 0,
    "has_existing_policy": False,
    "mobile_recharge_frequency": "weekly",
    "utility_payment_regularity": 0.85
}


def run_underwriting(applicant_data: Dict[str, Any] = None) -> str:
    """
    Run the complete underwriting pipeline.
    
    Args:
        applicant_data: Applicant information dict (uses SAMPLE_APPLICANT if None)
    
    Returns:
        Final underwriting decision as string
    """
    if applicant_data is None:
        applicant_data = SAMPLE_APPLICANT
    
    # Create session service and session
    session_service = InMemorySessionService()
    user_id = "demo_user"
    session_id = "demo_session"
    
    # Create session
    session_service.create_session(
        app_name="underwriting_agent",
        user_id=user_id,
        session_id=session_id
    )
    
    runner = Runner(app=app, session_service=session_service)
    
    prompt_text = f"""Process this insurance application and make a final underwriting decision:

{json.dumps(applicant_data, indent=2)}

Follow the complete pipeline: data enrichment → risk scoring → adversarial review → final decision."""
    
    # Create message content
    message = Content(
        role="user",
        parts=[Part(text=prompt_text)]
    )
    
    # Run and collect events
    result_text = ""
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=message
    ):
        if hasattr(event, 'content') and event.content:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    result_text += part.text
    
    return result_text
