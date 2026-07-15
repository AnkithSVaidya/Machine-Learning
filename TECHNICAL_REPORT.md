# Technical Report: HealthGuard Insurance Pricing Models

EECE 6544, Summer 2026, MiniProject #02

Stakeholder: Ms. Sarah Nabil, Head of Pricing, HealthGuard Insurance

Companion notebook: `HealthGuard_Insurance_Analysis.ipynb`. Every number in this report is produced by the notebook, which is fully deterministic (`random_state = 42`).

---

## 1. Problem statement

HealthGuard prices its plans from outdated actuarial tables. As a result the company underprices high risk customers and overprices low risk ones. Using 1,338 historical customer records (`age`, `sex`, `bmi`, `children`, `smoker`, `region`, `charges`), we translated the stakeholder's three requirements into three tasks:

| Requirement | Task | Target |
|---|---|---|
| "Understand our customers first" | Exploratory data analysis | none |
| "Predict the medical charges" | Regression | `charges` (USD per year) |
| "Flag the expensive customers" | Binary classification | `charges` above the median ($9,386.16) |

## 2. Data cleaning decisions and rationale

We treated the raw dataframe as read-only. All cleaning was done on a copy, and the result was saved to a separate file (`data/insurance_clean.csv`), so the raw and cleaned data never mix.

| Issue | Finding | Decision | Rationale |
|---|---|---|---|
| Encoding and loading | Reads cleanly as UTF-8 | Pass `encoding="utf-8"` explicitly | Reproducible on any machine |
| Missing values | 0 in all 7 columns | Nothing to impute | We still documented a plan: median for numeric columns, mode for categorical ones, and drop any row missing the target (it makes no sense to impute the value we are predicting) |
| Duplicate rows | 1 exact duplicate (19 year old male non-smoker, northwest, $1,639.56) | Drop it, keep the first. 1,337 rows remain | There is no customer ID to prove these are two different people, and an identical row double counts one observation |
| Inconsistent categories | None found | Strip whitespace and lowercase all text columns anyway | Cheap protection in case a future data refresh contains values like "Male " or "YES" |
| Invalid values | None. Age 18-64, BMI 15.96-53.13, children 0-5, charges $1,122 to $63,770 | Keep all rows | Every value passes the documented sanity checks |
| Extreme charges | Strong right skew (skewness 1.52), max $63,770 | Keep them, they are not errors | The tail sits with older and obese smokers, exactly the customers being mispriced. Deleting them would defeat the project |
| Types | Text columns stored as strings | Cast `sex`, `smoker`, `region` to category | Correct semantics and smaller memory |
| Feature engineering | | Added `bmi_category` (WHO bins), `age_group`, an `obese_smoker` flag and a `risk_label` built with a row-wise `apply` | Used for interpretation in the EDA. Excluded from the models because they are derived from existing features |

## 3. Exploratory analysis and key insights

The notebook contains seven visualizations (all saved under `charts/`). The main findings:

1. **Charges are heavily right skewed.** The median is $9,386 but the mean is $13,279, and the tail runs past $60,000. Flat table pricing has to misprice that tail. (charges_distribution.png)
2. **Smoking is the dominant driver** (correlation 0.79 with charges). Smokers average $32,050 per year against $8,441 for non-smokers, roughly a 3.8x gap, and the two distributions barely overlap. (charges_by_smoker.png)
3. **The most surprising pattern: risk multiplies instead of adding.** For non-smokers, going from underweight to obese only moves the average bill from $5,485 to $8,866. For smokers the same change is dramatic: obese smokers average $41,693, about 4.7 times obese non-smokers and more than double non-obese smokers. (bmi_vs_charges.png, bmi_smoker_interaction.png)
4. **Age adds roughly $250 to $280 per extra year** for everyone (group means: 18-29 at $9,201, 30-44 at $12,491, 45-64 at $17,070). The age scatter shows three parallel cost bands, with smoking lifting the whole curve. (age_vs_charges.png)
5. **Region, children and sex are second order factors** (every correlation below 0.08 in absolute value). The southeast's higher mean ($14,735 against $12,347 in the southwest) mostly reflects its smoker and BMI mix rather than geography. (region_children.png, correlation_heatmap.png)

For pricing, this means premiums should be driven by smoking status, age, and BMI in combination with smoking, and models should be judged on how well they handle the expensive tail.

## 4. Model development and evaluation

### 4.1 Protocol

- One-hot encoding with `drop_first=True`, giving 8 features. The engineered EDA helpers were excluded because they duplicate information.
- One fixed 80/20 train/test split (`random_state=42`) shared by every regression model. The classification split is also stratified.
- All hyperparameters tuned with 5-fold cross validation on the training set only. Scalers sit inside sklearn pipelines, so no test set information leaks into preprocessing, including during cross validation.
- Regression metrics on the test set: MAE, MSE, RMSE, R2. Classification metrics: accuracy, precision, recall, F1, ROC-AUC.

### 4.2 Regression ("Predict the medical charges")

| Rank | Model | Tuning | MAE | MSE | RMSE | R2 (test) | R2 (train) |
|---|---|---|---|---|---|---|---|
| 1 | Decision Tree (depth 4) | max_depth=4, min_samples_leaf=5 by CV | $2,621 | 18.89M | $4,346 | 0.897 | 0.855 |
| 2 | Polynomial (degree 2) | scaled pipeline | $2,867 | 21.59M | $4,646 | 0.883 | 0.834 |
| 3 | SVR (RBF kernel) | C=1, gamma=0.1, features and target scaled | $2,541 | 22.02M | $4,692 | 0.880 | 0.839 |
| 4 | Polynomial (degree 3) | scaled pipeline | $3,049 | 23.72M | $4,870 | 0.871 | 0.847 |
| 5 | Multiple Linear (all features) | none | $4,177 | 35.48M | $5,956 | 0.807 | 0.730 |
| 6 | Ridge (alpha = 5.62) | alpha by CV over 0.001 to 1000 | $4,191 | 35.67M | $5,973 | 0.806 | 0.730 |
| 7 | Lasso (alpha = 46.4) | alpha by CV, eliminated `sex_male` | $4,186 | 35.85M | $5,988 | 0.805 | 0.730 |
| 8 | Polynomial (degree 4) | scaled pipeline | $3,756 | 36.70M | $6,058 | 0.800 | 0.867 |
| 9 | SVR (linear kernel) | C=0.1 | $3,431 | 37.12M | $6,092 | 0.798 | 0.702 |
| 10 | Simple Linear (`smoker` only) | best single predictor from the EDA | $5,831 | 60.04M | $7,749 | 0.673 | 0.599 |

Observations worth noting:

- The simple linear model on the single best EDA predictor (`smoker`) already explains 67% of test variance: predict $8,498, and add $22,637 if the customer smokes.
- The polynomial models demonstrate overfitting clearly. Training R2 climbs with degree (0.730, 0.834, 0.847, 0.867) while test R2 peaks at degree 2 and then falls (0.883, 0.871, 0.800). Degree 2 works because its interaction terms (mainly `bmi` times `smoker_yes`) capture the multiplicative risk pattern from the EDA. Higher degrees just memorize noise.
- Ridge and Lasso match plain linear regression. With 8 well behaved features there is little variance to shrink. Lasso was still useful for feature selection: it removed `sex_male` entirely and nearly zeroed the region dummies, confirming the EDA ranking.
- SVR needs the target scaled as well as the features (we used `TransformedTargetRegressor`). Once scaled, the RBF kernel reaches the lowest MAE of any model ($2,541).
- The tree's cross validated depth of 4 balances bias and variance, and its feature importances (smoker 0.70, bmi 0.17, age 0.12) agree with the EDA.

**Recommended model: the depth 4 Decision Tree.** It has the best RMSE and R2, and RMSE penalizes exactly the large mispricings on expensive customers that motivated the project. Just as important for an insurer, the tree can be read as a set of pricing rules (first split: does the customer smoke, then BMI at least 30, then age bracket), which a pricing team and a regulator can audit. The SVR is slightly better on MAE but is much harder to explain in a rate filing. If the business needs smooth quotes instead of the tree's roughly 16 price bands, the degree 2 polynomial is a solid alternative.

### 4.3 Classification ("Flag the expensive customers")

"Expensive" means annual charges above the median ($9,386.16). This is a fixed business threshold set by the finance team, computed once on the cleaned data, so the classes are balanced by construction (669 against 668). `charges` was excluded from the features.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Random Forest | 0.937 | 0.961 | 0.910 | 0.935 | 0.944 |
| Decision Tree (depth 5) | 0.937 | 0.983 | 0.888 | 0.933 | 0.944 |
| SVM (RBF) | 0.929 | 0.946 | 0.910 | 0.928 | 0.959 |
| SVM (linear) | 0.925 | 0.932 | 0.918 | 0.925 | 0.954 |
| Logistic Regression | 0.907 | 0.898 | 0.918 | 0.908 | 0.953 |
| K-Nearest Neighbors (k=7) | 0.903 | 0.929 | 0.873 | 0.900 | 0.938 |
| Gaussian Naive Bayes | 0.757 | 1.000 | 0.515 | 0.680 | 0.952 |

**Recommended model: Random Forest**, with the best F1 and the best balance of precision and recall. For HealthGuard the costly error is the false negative (an expensive customer priced as cheap is a direct loss, while a false positive only risks a slightly high quote), which favors the Forest's 0.910 recall over the single tree's 0.888 at the same accuracy. If a wider net is wanted, the Forest's probability threshold can be lowered below 0.5 without retraining. Gaussian Naive Bayes illustrates why accuracy alone is misleading: perfect precision, but it misses about half of the expensive customers, which is the failure the company already has.

## 5. Final recommendation to the stakeholder

1. Deploy the depth 4 decision tree as the premium estimation tool (R2 of 0.897, typical error around $2,600). It doubles as an auditable set of pricing rules.
2. Deploy the random forest as the expensive customer flag (93.7% accuracy, catching 91% of the expensive customers).
3. Price on smoking, age, and BMI in combination with smoking. Sex, region and children add almost nothing, and Lasso discarded sex on its own, so dropping it also avoids trouble in jurisdictions that restrict its use.

Limitations we want to be upfront about:

- 1,337 records is a modest sample. The models should be retrained and validated on HealthGuard's own book before going live.
- The data has no claims history, chronic conditions or medications, which are the strongest signals an insurer usually has.
- Smoking is self reported and tends to be under reported. Verification may be worth it on large policies.
- Charges are a single year snapshot, so multi year risk cannot be priced from this data yet.

## 6. Reproducibility

- Every split, model and grid search uses `random_state = 42`, so a re-run gives identical numbers.
- The raw data is never modified. The cleaned data lives in its own file.
- Dependencies are pinned in `requirements.txt`, and run instructions are in `README.md`.
- Executing the notebook top to bottom regenerates every number, table and chart in this report.
