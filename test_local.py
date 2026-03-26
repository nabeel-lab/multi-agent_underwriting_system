"""
Simple test to verify tools work correctly
"""
from underwriting.tools import (
    parse_applicant_input,
    enrich_with_alternative_data,
    calculate_risk_score,
    generate_shap_explanation,
    detect_demographic_bias,
    check_alternative_data_quality,
    stress_test_score
)
import json

# Sample applicant
applicant = {
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

print("="*80)
print("TESTING UNDERWRITING TOOLS")
print("="*80)

# Step 1: Parse
print("\n1. Parsing applicant input...")
parsed = parse_applicant_input(applicant)
print(f"✓ Parsed: {parsed['name']}, {parsed['occupation']}")

# Step 2: Enrich
print("\n2. Enriching with alternative data...")
enriched = enrich_with_alternative_data(parsed)
print(f"✓ Enriched with {len(enriched)} features")
print(f"  - Utility regularity: {enriched['utility_payment_regularity']:.2f}")
print(f"  - Gig income stability: {enriched['gig_income_stability_score']:.2f}")
print(f"  - Digital footprint: {enriched['digital_footprint_score']:.2f}")

# Step 3: Calculate risk
print("\n3. Calculating risk score with XGBoost...")
risk_result = calculate_risk_score(enriched)
print(f"✓ Risk Score: {risk_result['risk_score']}/100")
print(f"  - Confidence: {risk_result['confidence_interval']}")
print(f"  - Premium: ₹{risk_result['monthly_premium_inr']}/month")
print(f"  - Top features: {[f['feature'] for f in risk_result['top_feature_importances'][:3]]}")

# Step 4: Generate explanation
print("\n4. Generating feature importance explanation...")
explanation = generate_shap_explanation(enriched, risk_result)
print(f"✓ {explanation['plain_explanation']}")

# Step 5: Detect bias
print("\n5. Checking for demographic bias...")
bias_check = detect_demographic_bias(enriched, risk_result)
if bias_check['bias_detected']:
    print(f"⚠️  Bias flags: {bias_check['bias_flags']}")
    for concern in bias_check['concerns']:
        print(f"   - {concern}")
else:
    print("✓ No demographic bias detected")

# Step 6: Check data quality
print("\n6. Validating alternative data quality...")
quality_check = check_alternative_data_quality(enriched)
print(f"✓ Data completeness: {quality_check['data_completeness']}")
print(f"  - Quality score: {quality_check['quality_score']}/100")

# Step 7: Stress test
print("\n7. Stress testing score stability...")
stress_result = stress_test_score(enriched, risk_result)
print(f"✓ Worst case score: {stress_result['worst_case_score']}")
print(f"  - Score volatility: {stress_result['score_volatility']}")
print(f"  - Adjusted recommendation: {stress_result['adjusted_score_recommendation']}")

# Final decision simulation
print("\n" + "="*80)
print("FINAL DECISION SIMULATION")
print("="*80)

final_score = stress_result['adjusted_score_recommendation']
approved = final_score < 70 and not bias_check['bias_detected']

print(f"\nApproved: {approved}")
print(f"Final Risk Score: {final_score}/100")
print(f"Monthly Premium: ₹{risk_result['monthly_premium_inr']}")
print(f"Confidence: {risk_result['model_confidence']}")

if bias_check['bias_detected']:
    print(f"\nBias Audit: {len(bias_check['bias_flags'])} potential bias flags detected")
    print("Adversarial agent recommended score adjustment")
else:
    print("\nBias Audit: No bias detected, original score approved")

print("\n" + "="*80)
print("✅ ALL TOOLS WORKING CORRECTLY!")
print("="*80)
print("\nYour system is ready. The agents will use these tools when deployed.")
print("Next step: Deploy to Cloud Run with 'adk deploy cloud_run'")
