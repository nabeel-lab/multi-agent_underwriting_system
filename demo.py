"""
Local demo script to test the underwriting agent pipeline
Run this before deploying to Cloud Run
"""
import json
from underwriting.agent import run_underwriting, SAMPLE_APPLICANT


def print_section(title: str, content: str):
    """Pretty print a section"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)
    print(content)


def main():
    print("\n🚀 PREDICTIVE INSURANCE UNDERWRITING - MULTI-AGENT DEMO")
    print("="*80)
    
    print("\n📋 APPLICANT PROFILE:")
    print(json.dumps(SAMPLE_APPLICANT, indent=2))
    
    print("\n⚙️  Starting 4-agent pipeline...")
    print("   Agent 1: Data Harvesting")
    print("   Agent 2: Risk Modelling (XGBoost + SHAP)")
    print("   Agent 3: Adversarial Review (Bias Detection)")
    print("   Agent 4: Final Decision")
    
    try:
        result = run_underwriting()
        
        print_section("✅ PIPELINE COMPLETE", "")
        print_section("📊 FINAL DECISION", result)
        
        # Try to extract structured decision if present
        try:
            if "```json" in result:
                json_start = result.find("```json") + 7
                json_end = result.find("```", json_start)
                decision_json = json.loads(result[json_start:json_end])
                
                print("\n" + "="*80)
                print("  DECISION SUMMARY")
                print("="*80)
                print(f"  Approved: {decision_json.get('approved', 'N/A')}")
                print(f"  Risk Score: {decision_json.get('final_risk_score', 'N/A')}")
                print(f"  Monthly Premium: ₹{decision_json.get('monthly_premium_inr', 'N/A')}")
                print(f"  Confidence: {decision_json.get('confidence_level', 'N/A')}")
                print(f"\n  Explanation: {decision_json.get('plain_english_explanation', 'N/A')}")
                print(f"\n  Bias Audit: {decision_json.get('bias_audit_summary', 'N/A')}")
        except:
            pass
        
        print("\n" + "="*80)
        print("✅ Demo completed successfully!")
        print("="*80)
        print("\nNext steps:")
        print("1. Copy this project to Google Cloud Shell")
        print("2. Run: adk deploy cloud_run --project=YOUR_PROJECT_ID --region=asia-south1")
        print("3. Get your live URL and demo it!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check that .env file exists with GOOGLE_API_KEY")
        print("2. Verify all dependencies are installed: pip install -r requirements.txt")
        print("3. Ensure Python 3.11+ is being used")
        raise


if __name__ == "__main__":
    main()
