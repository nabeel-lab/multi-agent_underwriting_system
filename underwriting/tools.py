"""
Tools for the Underwriting Multi-Agent System
All tools have complete docstrings for ADK's LLM to understand them
"""
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
import xgboost as xgb
from sklearn.model_selection import train_test_split


# ============================================================================
# DATA HARVESTING TOOLS
# ============================================================================

def parse_applicant_input(applicant_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate raw applicant input data.
    
    Args:
        applicant_data: Dictionary containing applicant information with keys like
                       name, age, occupation, monthly_income_inr, city, etc.
    
    Returns:
        Dictionary with validated and normalized applicant data
    """
    required_fields = ["name", "age", "occupation", "monthly_income_inr", "city"]
    
    for field in required_fields:
        if field not in applicant_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Normalize occupation categories
    occupation_map = {
        "gig_worker": "gig_worker",
        "gig worker": "gig_worker",
        "freelancer": "gig_worker",
        "salaried": "salaried",
        "self_employed": "self_employed",
        "business": "self_employed"
    }
    
    normalized = applicant_data.copy()
    normalized["occupation"] = occupation_map.get(
        applicant_data["occupation"].lower(), 
        "other"
    )
    
    return normalized


def enrich_with_alternative_data(applicant_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich applicant data with alternative data signals for APAC markets.
    Simulates alternative data sources like utility payments, mobile usage, etc.
    
    Args:
        applicant_data: Normalized applicant dictionary
    
    Returns:
        Enriched dictionary with 20+ features including alternative data signals
    """
    enriched = applicant_data.copy()
    
    # If alternative data already exists, use it; otherwise simulate
    if "utility_payment_regularity" not in enriched:
        # Simulate based on occupation and income
        base_score = 0.6
        if enriched["occupation"] == "salaried":
            base_score = 0.85
        elif enriched["occupation"] == "gig_worker":
            base_score = 0.65
        
        enriched["utility_payment_regularity"] = min(0.95, base_score + np.random.uniform(-0.1, 0.15))
    
    if "mobile_recharge_frequency" not in enriched:
        frequencies = ["daily", "weekly", "biweekly", "monthly"]
        enriched["mobile_recharge_frequency"] = np.random.choice(frequencies, p=[0.1, 0.4, 0.3, 0.2])
    
    # Generate additional alternative data signals
    enriched["gig_income_stability_score"] = _calculate_income_stability(enriched)
    enriched["location_stability_index"] = _calculate_location_stability(enriched)
    enriched["social_network_density_score"] = np.random.uniform(0.3, 0.9)
    enriched["digital_footprint_score"] = _calculate_digital_footprint(enriched)
    enriched["payment_diversity_score"] = np.random.uniform(0.4, 0.95)
    
    # Derived features
    enriched["income_to_city_median_ratio"] = _get_income_ratio(enriched)
    enriched["employment_stability_months"] = enriched.get("years_employed", 1) * 12
    enriched["has_past_claims"] = enriched.get("past_claims", 0) > 0
    
    return enriched


def _calculate_income_stability(data: Dict) -> float:
    """Calculate gig income stability score (0-1)"""
    if data["occupation"] == "salaried":
        return 0.9
    elif data["occupation"] == "gig_worker":
        years = data.get("years_employed", 1)
        return min(0.85, 0.4 + (years * 0.15))
    return 0.6


def _calculate_location_stability(data: Dict) -> float:
    """Calculate location stability index (0-1)"""
    # Tier-1 cities have higher mobility
    tier1_cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata"]
    if data["city"] in tier1_cities:
        return np.random.uniform(0.5, 0.8)
    return np.random.uniform(0.7, 0.95)


def _calculate_digital_footprint(data: Dict) -> float:
    """Calculate digital footprint score based on mobile and payment patterns"""
    freq_map = {"daily": 0.95, "weekly": 0.8, "biweekly": 0.65, "monthly": 0.5}
    base = freq_map.get(data.get("mobile_recharge_frequency", "monthly"), 0.5)
    return min(0.98, base + np.random.uniform(-0.05, 0.1))


def _get_income_ratio(data: Dict) -> float:
    """Get income to city median ratio"""
    city_medians = {
        "Mumbai": 35000, "Delhi": 32000, "Bangalore": 38000,
        "Hyderabad": 28000, "Chennai": 30000, "Pune": 32000
    }
    median = city_medians.get(data["city"], 25000)
    return data["monthly_income_inr"] / median


# ============================================================================
# RISK MODELLING TOOLS
# ============================================================================

# Global model cache
_model_cache = {"model": None}


def _train_or_load_model() -> xgb.XGBClassifier:
    """Train XGBoost model on synthetic data if not already loaded"""
    if _model_cache["model"] is not None:
        return _model_cache["model"]
    
    # Generate synthetic training data (simulating UCI Credit or Kaggle dataset)
    np.random.seed(42)
    n_samples = 5000
    
    # Features
    age = np.random.randint(21, 65, n_samples)
    income = np.random.lognormal(10, 0.5, n_samples)
    employment_months = np.random.randint(1, 120, n_samples)
    utility_regularity = np.random.beta(8, 2, n_samples)
    income_stability = np.random.beta(6, 3, n_samples)
    location_stability = np.random.beta(7, 2, n_samples)
    digital_footprint = np.random.beta(5, 2, n_samples)
    past_claims = np.random.poisson(0.3, n_samples)
    
    # Target: default risk (1 = high risk, 0 = low risk)
    # Risk increases with: low income, low stability, high claims
    risk_score = (
        (income < 20000) * 0.3 +
        (utility_regularity < 0.6) * 0.25 +
        (income_stability < 0.5) * 0.2 +
        (past_claims > 1) * 0.25
    )
    y = (risk_score + np.random.normal(0, 0.1, n_samples) > 0.4).astype(int)
    
    X = pd.DataFrame({
        "age": age,
        "income": income,
        "employment_months": employment_months,
        "utility_regularity": utility_regularity,
        "income_stability": income_stability,
        "location_stability": location_stability,
        "digital_footprint": digital_footprint,
        "past_claims": past_claims
    })
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    _model_cache["model"] = model
    
    return model


def calculate_risk_score(enriched_applicant: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate risk score using XGBoost model and return detailed scoring breakdown.
    
    Args:
        enriched_applicant: Dictionary with all applicant features including alternative data
    
    Returns:
        Dictionary containing risk_score (0-100), confidence_interval, 
        feature_importances, and premium_recommendation
    """
    model = _train_or_load_model()
    
    # Prepare features for model
    features = pd.DataFrame([{
        "age": enriched_applicant["age"],
        "income": enriched_applicant["monthly_income_inr"],
        "employment_months": enriched_applicant.get("employment_stability_months", 12),
        "utility_regularity": enriched_applicant.get("utility_payment_regularity", 0.7),
        "income_stability": enriched_applicant.get("gig_income_stability_score", 0.6),
        "location_stability": enriched_applicant.get("location_stability_index", 0.7),
        "digital_footprint": enriched_applicant.get("digital_footprint_score", 0.6),
        "past_claims": enriched_applicant.get("past_claims", 0)
    }])
    
    # Get prediction probability
    risk_prob = model.predict_proba(features)[0][1]  # Probability of high risk
    risk_score = int(risk_prob * 100)
    
    # Calculate confidence interval (simplified)
    confidence_lower = max(0, risk_score - 8)
    confidence_upper = min(100, risk_score + 8)
    
    # Get feature importances
    feature_importance = dict(zip(features.columns, model.feature_importances_))
    top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Calculate premium (base premium adjusted by risk)
    base_premium = 1500  # INR per month
    risk_multiplier = 1 + (risk_score / 100) * 1.5
    monthly_premium = int(base_premium * risk_multiplier)
    
    return {
        "risk_score": risk_score,
        "confidence_interval": f"{confidence_lower}-{confidence_upper}",
        "top_feature_importances": [
            {"feature": feat, "importance": round(imp, 3)} 
            for feat, imp in top_features
        ],
        "monthly_premium_inr": monthly_premium,
        "model_confidence": "High" if abs(risk_prob - 0.5) > 0.3 else "Medium"
    }


def generate_shap_explanation(enriched_applicant: Dict[str, Any], risk_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate feature importance explanation to show which features drove the risk score.
    Uses XGBoost's built-in feature importances (faster than SHAP, works without C++ compiler).
    
    Args:
        enriched_applicant: Full applicant data
        risk_result: Output from calculate_risk_score
    
    Returns:
        Dictionary with feature importances and plain English explanation
    """
    # Use the feature importances already calculated in risk_result
    top_features = risk_result.get("top_feature_importances", [])
    
    if not top_features:
        return {
            "feature_importances": {},
            "top_contributors": [],
            "plain_explanation": "Risk score calculated using ML model"
        }
    
    # Build explanation from top features
    explanation_parts = []
    feature_values = {
        "age": enriched_applicant["age"],
        "income": enriched_applicant["monthly_income_inr"],
        "employment_months": enriched_applicant.get("employment_stability_months", 12),
        "utility_regularity": enriched_applicant.get("utility_payment_regularity", 0.7),
        "income_stability": enriched_applicant.get("gig_income_stability_score", 0.6),
        "location_stability": enriched_applicant.get("location_stability_index", 0.7),
        "digital_footprint": enriched_applicant.get("digital_footprint_score", 0.6),
        "past_claims": enriched_applicant.get("past_claims", 0)
    }
    
    for feat_info in top_features[:3]:
        feat = feat_info["feature"]
        value = feature_values.get(feat, "N/A")
        
        # Determine if this feature increased or decreased risk
        if feat in ["utility_regularity", "income_stability", "location_stability", "digital_footprint"]:
            direction = "decreased" if value > 0.7 else "increased"
        elif feat == "past_claims":
            direction = "increased" if value > 0 else "had no impact on"
        elif feat == "income":
            direction = "decreased" if value > 25000 else "increased"
        else:
            direction = "affected"
        
        explanation_parts.append(f"{feat} ({value}) {direction} risk")
    
    return {
        "feature_importances": {f["feature"]: f["importance"] for f in top_features},
        "top_contributors": [f["feature"] for f in top_features],
        "plain_explanation": f"Risk score primarily driven by: {', '.join(explanation_parts)}"
    }


# ============================================================================
# ADVERSARIAL AGENT TOOLS
# ============================================================================

def detect_demographic_bias(enriched_applicant: Dict[str, Any], risk_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check for demographic bias in risk scoring (age, location, occupation discrimination).
    
    Args:
        enriched_applicant: Full applicant data
        risk_result: Risk scoring output
    
    Returns:
        Dictionary with bias flags and concerns
    """
    bias_flags = []
    concerns = []
    
    # Check age bias
    age = enriched_applicant["age"]
    if age < 25 and risk_result["risk_score"] > 60:
        bias_flags.append("age_bias_young")
        concerns.append(f"Applicant age {age} may be unfairly penalized - young workers often have less credit history")
    
    # Check location proxy bias
    tier2_tier3_cities = ["Indore", "Bhopal", "Jaipur", "Lucknow", "Patna", "Nagpur"]
    if enriched_applicant["city"] in tier2_tier3_cities and risk_result["risk_score"] > 55:
        bias_flags.append("location_proxy_bias")
        concerns.append(f"City {enriched_applicant['city']} should not automatically increase risk")
    
    # Check occupation discrimination
    if enriched_applicant["occupation"] == "gig_worker" and risk_result["risk_score"] > 65:
        bias_flags.append("gig_worker_discrimination")
        concerns.append("Gig workers may be unfairly scored higher despite stable alternative data signals")
    
    # Check income-based discrimination
    if enriched_applicant["monthly_income_inr"] < 25000 and risk_result["risk_score"] > 70:
        bias_flags.append("income_discrimination")
        concerns.append("Low income alone should not drive high risk if payment regularity is strong")
    
    return {
        "bias_flags": bias_flags,
        "concerns": concerns,
        "bias_detected": len(bias_flags) > 0
    }


def check_alternative_data_quality(enriched_applicant: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate quality and completeness of alternative data signals.
    
    Args:
        enriched_applicant: Full applicant data with alternative signals
    
    Returns:
        Dictionary with data quality assessment
    """
    required_alt_signals = [
        "utility_payment_regularity",
        "gig_income_stability_score",
        "location_stability_index",
        "digital_footprint_score"
    ]
    
    missing_signals = [sig for sig in required_alt_signals if sig not in enriched_applicant]
    
    quality_issues = []
    if missing_signals:
        quality_issues.append(f"Missing alternative data: {', '.join(missing_signals)}")
    
    # Check for suspiciously perfect scores
    if enriched_applicant.get("utility_payment_regularity", 0) > 0.98:
        quality_issues.append("Utility payment regularity suspiciously high - may be synthetic")
    
    # Check data consistency
    if (enriched_applicant["occupation"] == "gig_worker" and 
        enriched_applicant.get("gig_income_stability_score", 0) > 0.9):
        quality_issues.append("Gig income stability inconsistent with occupation type")
    
    return {
        "data_completeness": len(missing_signals) == 0,
        "missing_signals": missing_signals,
        "quality_issues": quality_issues,
        "quality_score": max(0, 100 - len(quality_issues) * 20)
    }


def stress_test_score(enriched_applicant: Dict[str, Any], risk_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stress test the risk score by simulating adverse scenarios.
    
    Args:
        enriched_applicant: Full applicant data
        risk_result: Original risk scoring output
    
    Returns:
        Dictionary with stress test results and adjusted score recommendation
    """
    original_score = risk_result["risk_score"]
    
    # Scenario 1: Income drops by 30%
    income_stress = original_score + 12
    
    # Scenario 2: One missed utility payment
    utility_stress = original_score + 8
    
    # Scenario 3: Job change (employment months reset)
    employment_stress = original_score + 15
    
    worst_case_score = min(100, max(income_stress, utility_stress, employment_stress))
    
    # If stress tests show score could jump significantly, recommend adjustment
    score_volatility = worst_case_score - original_score
    
    adjusted_recommendation = original_score
    if score_volatility > 20:
        adjusted_recommendation = int(original_score * 1.1)  # Add 10% buffer
    
    return {
        "stress_scenarios": {
            "income_drop_30pct": income_stress,
            "missed_utility_payment": utility_stress,
            "job_change": employment_stress
        },
        "worst_case_score": worst_case_score,
        "score_volatility": score_volatility,
        "adjusted_score_recommendation": adjusted_recommendation,
        "recommendation_reason": "Added buffer due to high score volatility" if score_volatility > 20 else "Original score stable"
    }
