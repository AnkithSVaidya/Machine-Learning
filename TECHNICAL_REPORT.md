# Technical Report — HealthGuard Insurance Pricing Models

**EECE 6544 · Summer 2026 · MiniProject #02**
**Stakeholder:** Ms. Sarah Nabil, Head of Pricing, HealthGuard Insurance
**Companion notebook:** `HealthGuard_Insurance_Analysis.ipynb` (all numbers below are reproduced by it, `random_state = 42`)

---

## 1. Problem statement

HealthGuard prices plans from outdated actuarial tables, underpricing high-risk customers and overpricing low-risk ones. Using 1,338 historical customer records (`age`, `sex`, `bmi`, `children`, `smoker`, `region`, `charges`), the stakeholder's three requirements translate into three ML tasks:

| Requirement | ML task | Target |
|---|---|---|
| "Understand our customers first" | Exploratory data analysis | — |
| "Predict the medical charges" | Regression | `charges` (USD/year) |
| "Flag the expensive customers" | Binary classification | `charges` > median ($9,386.16) |

## 2. Data cleaning — decisions and rationale

The raw dataframe is treated as **immutable**: all cleaning happens on a copy, and the result is saved to a separate file (`data/insurance_clean.csv`), so raw and clean data never mix.

| Issue | Finding | Decision | Rationale |
|---|---|---|---|
| Encoding / loading | Reads cleanly as UTF-8 | Explicit `encoding="utf-8"` | Reproducibility on any machine |
| Missing values | 0 in all 7 columns | Nothing to impute | Contingency documented: median for numerics, mode for categoricals, and *drop* rows missing the target (never impute what you are predicting) |
| Duplicate rows | 1 exact duplicate (19-year-old male non-smoker, northwest, $1,639.56) | Drop, keep first → **1,337 rows** | No customer ID exists to prove they are two people; an identical row adds no information and double-weights one observation |
| Inconsistent categories | None found | Defensive `str.strip().str.lower()` on all text columns | Cheap insurance against future data refreshes ("Male ", "YES") |
| Invalid values | None — age 18–64, BMI 15.96–53.13, children 0–5, charges $1,122–$63,770 | Keep all rows | All ranges pass documented sanity checks |
| Extreme charges | Strong right skew (skewness 1.52), max $63,770 | **Keep** — not errors | The tail concentrates in older/obese smokers — exactly the customers being mispriced; deleting them defeats the project |
| Types | Text columns as strings | Cast `sex`/`smoker`/`region` to `category` | Correct semantics, smaller memory |
| Feature engineering | — | Add `bmi_category` (WHO bins via `pd.cut`), `age_group`, `obese_smoker` flag | Used for EDA interpretation; **excluded from models** (derived from existing features) |

## 3. Exploratory analysis — key insights

Seven visualizations in the notebook (all saved under `charts/`). Headlines:

1. **Charges are right-skewed.** Median $9,386 vs mean $13,279; a long tail past $60k. Flat table pricing must misprice the tail. *(charges_distribution.png)*
2. **Smoking is the dominant driver** (r = 0.79 with charges). Smokers average **$32,050** vs **$8,441** for non-smokers (3.8×); the two distributions barely overlap. *(charges_by_smoker.png)*
3. **The surprising pattern — risk multiplies, it doesn't add.** For non-smokers, BMI moves the average bill only $5,485 → $8,866 (underweight → obese). For smokers it explodes: **obese smokers average $41,693**, ~4.7× obese non-smokers and more than double non-obese smokers. *(bmi_vs_charges.png, bmi_smoker_interaction.png)*
4. **Age adds a steady ~$250–280 per year** for everyone (group means: 18–29 = $9,201, 30–44 = $12,491, 45–64 = $17,070); the age scatter shows three parallel cost bands with smoking shifting the whole curve up. *(age_vs_charges.png)*
5. **Region, children, and sex are second-order** (all |r| < 0.08). The southeast's higher mean ($14,735 vs $12,347 southwest) mostly reflects its smoker/BMI mix, not geography. *(region_children.png, correlation_heatmap.png)*

**Pricing implication:** premiums should be driven by smoking status, age, and BMI-given-smoking; a model must capture the smoking×BMI *interaction* to price the expensive segment correctly.

## 4. Model development and evaluation

### 4.1 Protocol

- One-hot encoding (`drop_first=True`) → 8 features; engineered EDA helpers excluded (derived/collinear).
- One fixed **80/20 train/test split** (`random_state=42`) shared by all regression models; the classification split is additionally **stratified**.
- All hyperparameters tuned with **5-fold cross-validation on the training set only**; scalers live inside sklearn `Pipeline`s so no test information leaks into preprocessing (including during CV).
- Regression metrics (test set): MAE, MSE, RMSE, R². Classification metrics: accuracy, precision, recall, F1, ROC-AUC.

### 4.2 Regression — "Predict the medical charges"

| Rank | Model | Tuning | MAE | MSE | RMSE | R² (test) | R² (train) |
|---|---|---|---|---|---|---|---|
| 1 | **Decision Tree (depth 4)** | max_depth=4, min_samples_leaf=5 (CV) | **$2,621** | 18.89M | **$4,346** | **0.897** | 0.855 |
| 2 | Polynomial (degree 2) | scaled pipeline | $2,867 | 21.59M | $4,646 | 0.883 | 0.834 |
| 3 | SVR (RBF kernel) | C=1, γ=0.1; features **and target** scaled | $2,541 | 22.02M | $4,692 | 0.880 | 0.839 |
| 4 | Polynomial (degree 3) | scaled pipeline | $3,049 | 23.72M | $4,870 | 0.871 | 0.847 |
| 5 | Multiple Linear (all features) | — | $4,177 | 35.48M | $5,956 | 0.807 | 0.730 |
| 6 | Ridge (α = 5.62) | α via CV over 10⁻³–10³ | $4,191 | 35.67M | $5,973 | 0.806 | 0.730 |
| 7 | Lasso (α = 46.4) | α via CV; **eliminated `sex_male`** | $4,186 | 35.85M | $5,988 | 0.805 | 0.730 |
| 8 | Polynomial (degree 4) | scaled pipeline | $3,756 | 36.70M | $6,058 | 0.800 | **0.867** |
| 9 | SVR (linear kernel) | C=0.1 | $3,431 | 37.12M | $6,092 | 0.798 | 0.702 |
| 10 | Simple Linear (`smoker` only) | best single predictor from EDA | $5,831 | 60.04M | $7,749 | 0.673 | 0.599 |

Notable findings:

- **Simple linear regression** on the single best EDA predictor (`smoker`) already explains 67% of test variance: predict $8,498, add $22,637 if the customer smokes.
- **Overfitting demonstrated with polynomials:** train R² climbs monotonically with degree (0.73 → 0.834 → 0.847 → 0.867) while test R² peaks at degree 2 and then falls (0.883 → 0.871 → 0.800). Degree 2 wins because its interaction terms (notably `bmi × smoker_yes`) capture the multiplicative risk EDA found; higher degrees memorize noise.
- **Ridge/Lasso match plain linear regression** — with 8 well-behaved features there is little variance to shrink. Lasso's value here is feature selection: it zeroed out `sex_male` and nearly zeroed the region dummies, independently confirming the EDA importance ranking.
- **SVR needs both features and the target scaled** (via `TransformedTargetRegressor`); the RBF kernel then achieves the lowest MAE of any model ($2,541).
- **The decision tree's CV-chosen depth of 4** is the bias/variance sweet spot; its feature importances (smoker 0.70, BMI 0.17, age 0.12, all else ≈ 0) again match the EDA.

**Recommended model: Decision Tree (depth 4).**
(1) Best RMSE and R² — and RMSE penalizes exactly the large mispricings on expensive customers that motivated the project; (2) it is a human-readable pricing rulebook (first split: *do you smoke?* → BMI ≥ 30? → age bracket) that a pricing team and a regulator can audit, unlike SVR; (3) it captures the smoking×obesity interaction natively. Runner-up if smooth (non-banded) quotes are required: Polynomial degree 2.

### 4.3 Classification — "Flag the expensive customers"

*Expensive* = annual charges above the median (**$9,386.16**, a fixed business threshold set by finance, computed once on the cleaned data). Classes are balanced by construction (669 / 668). `charges` is excluded from the features.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| **Random Forest** | **0.937** | 0.961 | **0.910** | **0.935** | 0.944 |
| Decision Tree (depth 5) | 0.937 | 0.983 | 0.888 | 0.933 | 0.944 |
| SVM (RBF) | 0.929 | 0.946 | 0.910 | 0.928 | **0.959** |
| SVM (linear) | 0.925 | 0.932 | 0.918 | 0.925 | 0.954 |
| Logistic Regression | 0.907 | 0.898 | 0.918 | 0.908 | 0.953 |
| K-Nearest Neighbors (k=7) | 0.903 | 0.929 | 0.873 | 0.900 | 0.938 |
| Gaussian Naive Bayes | 0.757 | 1.000 | 0.515 | 0.680 | 0.952 |

**Recommended model: Random Forest** — best F1 with the strongest precision/recall balance. For HealthGuard the costly error is the **false negative** (an expensive customer priced as cheap = direct loss), which favors the Forest's 0.910 recall over the single tree's 0.888 at identical accuracy. If a wider net is wanted, lowering the Forest's probability threshold below 0.5 trades precision for recall with no retraining. Gaussian Naive Bayes is the cautionary tale: perfect precision but it misses half the expensive customers — the exact failure mode the company already suffers.

## 5. Final recommendation to the stakeholder

1. **Deploy the depth-4 Decision Tree** as the premium-estimation tool (R² 0.897, typical error ≈ $2,600) — it doubles as an auditable pricing rulebook.
2. **Deploy the Random Forest** as the expensive-customer triage flag (93.7% accuracy, 91% of expensive customers caught).
3. **Price on smoking, age, and BMI-given-smoking.** Sex, region, and children add almost nothing (Lasso discarded sex entirely) — dropping sex also sidesteps jurisdictions that restrict its use in pricing.

**Limitations to state honestly:**

- 1,337 records is modest; retrain and validate on HealthGuard's own book before production use.
- No claims history, chronic conditions, or medications — the strongest actuarial signals are still untapped.
- Self-reported smoking is under-reported in practice; consider verification for large policies.
- Charges are a single-year snapshot; longitudinal data would allow multi-year risk pricing.

## 6. Reproducibility

- Deterministic: `random_state = 42` for every split, model, and search.
- Raw data never mutated; cleaned data written to `data/insurance_clean.csv`.
- Pinned dependencies in `requirements.txt`; run instructions in `README.md`.
- Executing the notebook top-to-bottom regenerates every number, table, and chart in this report.
