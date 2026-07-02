# Telco Monthly Charge Prediction

EECE 6544: Assignment #02

## What this project does

Telco's billing and revenue team wants to know: **given which add-on services a
customer subscribes to, what monthly charge should we expect them to pay?**

This project fits a multivariable linear regression that maps ten binary service
indicators (phone service, multiple lines, online security, online backup, device
protection, tech support, streaming TV, streaming movies, and fiber/no-internet
indicators) onto `target`, the customer's monthly charge. It evaluates the model
on a held-out test set, compares it against a single-variable baseline (count of
add-ons), interprets the coefficients as a per-service price list, and answers the
eight business questions the assignment poses.

## Repository contents

| File | Description |
|---|---|
| `telco_regression.ipynb` | The full, already-executed notebook: data inspection, train/test split, model fitting, evaluation, baseline comparison, interpretation, and example predictions. |
| `telco.csv` | The provided dataset (7,043 rows). |
| `FINDINGS.md` | Answers to the eight practical business questions, with two charts. |
| `requirements.txt` | Python packages needed to run the notebook. |
| `charts/` | The exported coefficient bar chart and predicted-vs-actual scatter plot. |

## How to run

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook telco_regression.ipynb
```

Run all cells top to bottom. `telco.csv` must be in the same folder as the
notebook (it already is in this repository).

## Summary of findings

- **Base plan:** about **$24.97/month** with no add-ons (the model's intercept).
- **Per-service prices:** fiber internet (~$24.95) and phone service (~$20.04) are
  the two priciest add-ons; streaming TV and streaming movies are each about
  $10; the five smaller line-item services (multiple lines, online security,
  online backup, device protection, tech support) are each about $5.
- **Model fit:** R² ≈ **0.999**, MAE ≈ **$0.79**, RMSE ≈ **$1.05** on the test set —
  the ten service indicators explain almost all of the variation in monthly
  charge.
- **Vs. baseline:** a single-variable model using only the *count* of add-ons
  reaches R² ≈ 0.70 and MAE ≈ $14.24 on the same split — knowing *which*
  services a customer has is far more informative than knowing *how many*.
- **Example prediction:** fiber internet + both streaming services raises the
  expected bill by about $44.88 over the base plan; phone service + multiple
  lines + tech support comes out to about $55.05/month.

See `FINDINGS.md` for the full write-up with charts and all eight question
answers.
