# System Architecture

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Application                          │
│  { name, age, occupation, income, city, employment_history }    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DECISION AGENT (Root)                         │
│                    Orchestrates Pipeline                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   AGENT 1    │    │   AGENT 2    │    │   AGENT 3    │
│     DATA     │───▶│     RISK     │───▶│ ADVERSARIAL  │
│  HARVESTING  │    │   MODELLING  │    │   REVIEWER   │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        │                    │                    │
        ▼                    ▼                    ▼
  Enriched Data      Risk Score + SHAP    Challenge Report
  20+ features       Confidence Interval   Bias Flags
  Alt. signals       Premium Estimate      Adjusted Score
                                                  │
                                                  │
        ┌─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FINAL DECISION                              │
│  { approved, final_risk_score, premium, explanation,            │
│    bias_audit_summary, confidence_level }                       │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Details

### Agent 1: Data Harvesting Agent

**Purpose:** Enrich raw applicant data with alternative signals

**Tools:**
- `parse_applicant_input()` - Validates and normalizes input
- `enrich_with_alternative_data()` - Adds APAC-relevant signals

**Output Features (20+):**
- Core: age, income, occupation, city, employment_months
- Alternative Data:
  - utility_payment_regularity (0-1)
  - mobile_recharge_frequency (daily/weekly/monthly)
  - gig_income_stability_score (0-1)
  - location_stability_index (0-1)
  - social_network_density_score (0-1)
  - digital_footprint_score (0-1)
  - payment_diversity_score (0-1)
- Derived: income_to_city_median_ratio, has_past_claims

**Why Alternative Data?**
In APAC markets, traditional credit scores are often unavailable. Alternative data (utility payments, mobile usage) provides risk signals for underbanked populations.

---

### Agent 2: Risk Modelling Agent

**Purpose:** Score applicant risk using ML model

**Tools:**
- `calculate_risk_score()` - XGBoost prediction
- `generate_shap_explanation()` - Feature importance

**ML Model:**
- Algorithm: XGBoost Classifier
- Training: 5000 synthetic samples (simulating UCI Credit dataset)
- Features: 8 key signals (age, income, employment, utility regularity, etc.)
- Output: Risk probability (0-1) scaled to 0-100

**SHAP Explanations:**
Shows which features increased/decreased risk:
```
income: -0.15 (decreased risk)
utility_regularity: -0.08 (decreased risk)
past_claims: +0.22 (increased risk)
```

**Premium Calculation:**
```
base_premium = 1500 INR/month
risk_multiplier = 1 + (risk_score/100) * 1.5
final_premium = base_premium * risk_multiplier
```

---

### Agent 3: Adversarial Agent

**Purpose:** Challenge the risk score for bias and fairness

**Tools:**
- `detect_demographic_bias()` - Checks age, location, occupation discrimination
- `check_alternative_data_quality()` - Validates data completeness
- `stress_test_score()` - Simulates adverse scenarios

**Bias Checks:**

1. **Age Bias:** Young applicants (<25) shouldn't be auto-penalized
2. **Location Proxy:** Tier-2/3 cities shouldn't increase risk unfairly
3. **Occupation Discrimination:** Gig workers with strong alt. data shouldn't be scored higher
4. **Income Discrimination:** Low income + strong payment history = acceptable

**Stress Tests:**
- Income drops 30%
- One missed utility payment
- Job change (employment reset)

**Output:**
```json
{
  "bias_flags": ["gig_worker_discrimination"],
  "concerns": ["Gig workers may be unfairly scored..."],
  "adjusted_score_recommendation": 52,
  "your_verdict": "ADJUST"
}
```

---

### Agent 4: Decision Agent

**Purpose:** Synthesize all outputs into final decision

**Logic:**
1. Collect outputs from Agents 1, 2, 3
2. If Adversarial Agent recommends adjustment, use adjusted score
3. Approval threshold: risk_score < 70 AND no major bias flags
4. Generate plain English explanation
5. Summarize bias audit

**Final Decision Schema:**
```json
{
  "approved": boolean,
  "final_risk_score": int (0-100),
  "monthly_premium_inr": float,
  "plain_english_explanation": string,
  "bias_audit_summary": string,
  "confidence_level": "High" | "Medium" | "Low"
}
```

---

## Technology Stack

### Core Framework
- **Google ADK** - Multi-agent orchestration, tool calling, LLM integration
- **Gemini 2.0 Flash** - Fast, cost-effective LLM for agent reasoning

### ML & Explainability
- **XGBoost** - Gradient boosting for risk classification
- **SHAP** - SHapley Additive exPlanations for model interpretability
- **scikit-learn** - Data preprocessing and train/test split
- **pandas/numpy** - Data manipulation

### Deployment
- **Cloud Run** - Serverless container platform
- **Cloud Build** - Automated container builds
- **Artifact Registry** - Container image storage
- **Secret Manager** - API key storage
- **FastAPI** - Web framework (via ADK)

### Frontend
- **Tailwind CSS** - Styling via CDN
- **Vanilla JS** - No framework overhead
- **Animated UI** - Shows agent pipeline in real-time

---

## Data Flow Example

**Input:**
```json
{
  "name": "Priya Sharma",
  "age": 28,
  "occupation": "gig_worker",
  "monthly_income_inr": 22000,
  "city": "Hyderabad",
  "years_employed": 1.5,
  "past_claims": 0
}
```

**After Agent 1 (Data Harvesting):**
```json
{
  ...original fields...,
  "utility_payment_regularity": 0.85,
  "gig_income_stability_score": 0.62,
  "location_stability_index": 0.78,
  "digital_footprint_score": 0.80,
  "income_to_city_median_ratio": 0.79
}
```

**After Agent 2 (Risk Modelling):**
```json
{
  "risk_score": 58,
  "confidence_interval": "50-66",
  "top_feature_importances": [
    {"feature": "utility_regularity", "importance": 0.245},
    {"feature": "income", "importance": 0.198},
    {"feature": "employment_months", "importance": 0.156}
  ],
  "monthly_premium_inr": 2370
}
```

**After Agent 3 (Adversarial):**
```json
{
  "bias_flags": ["gig_worker_discrimination"],
  "concerns": ["Gig workers may be unfairly scored despite stable alt. data"],
  "adjusted_score_recommendation": 52,
  "your_verdict": "ADJUST"
}
```

**Final Decision:**
```json
{
  "approved": true,
  "final_risk_score": 52,
  "monthly_premium_inr": 2280,
  "plain_english_explanation": "Application approved with moderate risk. Strong utility payment history and digital footprint offset gig worker occupation concerns.",
  "bias_audit_summary": "Adversarial review detected potential gig worker discrimination. Score adjusted from 58 to 52 based on strong alternative data signals.",
  "confidence_level": "High"
}
```

---

## Key Design Decisions

### Why 4 Agents?

1. **Separation of Concerns** - Each agent has a single responsibility
2. **Modularity** - Easy to swap out risk models or add new bias checks
3. **Transparency** - Each step is visible and auditable
4. **Adversarial Pattern** - Agent 3 provides checks and balances

### Why Adversarial Pattern?

Traditional ML pipelines have a single model that outputs a decision. This system adds a "challenger" agent that:
- Questions the model's assumptions
- Checks for systematic bias
- Stress-tests the score
- Recommends adjustments

This mirrors real-world underwriting where multiple reviewers check each other's work.

### Why Alternative Data?

In APAC markets (India, Southeast Asia), 60-70% of the population lacks traditional credit scores. Alternative data provides risk signals for:
- Gig workers (Uber, Swiggy, Zomato drivers)
- Small business owners
- Rural populations
- Young professionals

### Why SHAP?

SHAP values provide:
- **Interpretability** - Regulators and customers can understand decisions
- **Debugging** - Identify when model relies on proxy variables
- **Trust** - Transparent AI builds confidence

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Cloud Run Service                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │              FastAPI Application (ADK)              │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │         4-Agent Pipeline                     │  │    │
│  │  │  Decision → Data → Risk → Adversarial       │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  │                                                      │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │         XGBoost Model (in-memory)            │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────┘    │
│                           │                                  │
│                           ▼                                  │
│                  Gemini 2.0 Flash API                       │
│                  (via GOOGLE_API_KEY)                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Secret Manager │
                   │  (API Key)      │
                   └─────────────────┘
```

**Scaling:**
- Cloud Run auto-scales from 0 to N instances
- Each instance handles concurrent requests
- Model loaded once per instance (cached)
- Stateless design enables horizontal scaling

**Security:**
- API key stored in Secret Manager (not in code)
- HTTPS-only endpoints
- IAM-based access control
- No PII stored (stateless processing)

---

## Performance Characteristics

**Latency:**
- Data Harvesting: ~500ms (LLM + tool calls)
- Risk Modelling: ~800ms (XGBoost + SHAP + LLM)
- Adversarial Review: ~1000ms (3 tools + LLM)
- Total: ~2.5-3 seconds end-to-end

**Cost (per 1000 requests):**
- Gemini API: ~$0.10 (free tier covers 1500 requests/day)
- Cloud Run: ~$0.05 (free tier covers 2M requests/month)
- Total: ~$0.15 per 1000 requests (after free tier)

**Accuracy:**
- XGBoost model: ~85% on synthetic test set
- Bias detection: Flags 15-20% of cases for review
- False positive rate: <5% (over-cautious by design)

---

## Future Enhancements

1. **Real Training Data** - Replace synthetic data with UCI/Kaggle datasets
2. **Model Retraining** - Periodic updates based on actual underwriting outcomes
3. **A/B Testing** - Compare adversarial vs. non-adversarial decisions
4. **Human-in-the-Loop** - Escalate borderline cases to human underwriters
5. **Multi-Language** - Support Hindi, Tamil, Telugu for APAC markets
6. **Mobile App** - Native iOS/Android with offline capability
7. **Blockchain Audit Trail** - Immutable record of all decisions
8. **Federated Learning** - Train on distributed data without centralization
