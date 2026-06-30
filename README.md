# Cobblestone Gifts: Online Retail Sales Review

EECE 6544: Introduction to Machine Learning and Pattern Recognition, Summer 2026,
Mini-Project #01.

Cleaning and analysis of a raw e-commerce export for a UK-based online gift
retailer (the public UK Online Retail dataset, about 541,909 transaction lines
from December 2010 to December 2011). The project profiles the raw export,
documents the cleaning decisions, builds a completed-sales dataset, and answers
seven business questions.

## What the project does
1. Loads and profiles the raw export (correct ISO-8859-1 encoding, shape,
   missingness, unique values, summary statistics).
2. Cleans and fixes the data: standardises country labels, renames columns to
   snake_case, handles missing values, and removes cancellations, non-product
   lines (postage, bank charges, Amazon fees, adjustments), impossible prices and
   quantities, and exact duplicate rows.
3. Engineers features (line revenue, cleaned descriptions, a region lookup) and
   aggregates by product, country, customer, and time.
4. Answers seven business questions with code, numbers, short interpretations, and
   two charts.

All 21 required pandas techniques (3.1 to 3.21) are demonstrated and labelled by
number in the notebook.

## Repository contents
| File | Description |
|------|-------------|
| `online_retail_cleaning.ipynb` | The cleaning and analysis notebook, with each technique labelled by number. |
| `clean_online_retail.csv` | The exported clean completed-sales dataset. |
| `DATA_DICTIONARY.md` | Definition of every column in the clean dataset. |
| `FINDINGS.md` | One-page summary answering the seven business questions. |
| `CLEANING_DECISIONS.md` | Log of the judgment calls made and the reasoning. |
| `charts/` | Saved charts (monthly revenue trend, top non-UK markets). |
| `requirements.txt` | Python libraries and versions needed to reproduce the work. |

The raw input `data.csv` (about 50 MB) is not committed. Download it from Kaggle
(see below). It is listed in `.gitignore`.

## Get the dataset
Option A, Kaggle website: open
<https://www.kaggle.com/datasets/carrie1/ecommerce-data>, click Download, unzip,
and place `data.csv` in the project root.

Option B, Kaggle API:
```bash
pip install kaggle                       # put kaggle.json in ~/.kaggle/
kaggle datasets download -d carrie1/ecommerce-data
unzip ecommerce-data.zip                 # produces data.csv
```

The file is not UTF-8, so the notebook reads it with
`pd.read_csv('data.csv', encoding='ISO-8859-1')` to handle the pound symbol.

## How to run
```bash
python -m venv .venv
source .venv/bin/activate                # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook online_retail_cleaning.ipynb     # then Run All
```
Running the notebook top to bottom regenerates `clean_online_retail.csv` and the
files in `charts/`.

## Findings at a glance
* Total cleaned revenue is about 10.2 million pounds for the year. Sales are
  seasonal and peak in November 2011 at about 1.45 million pounds (about +98% over
  a typical month) ahead of Christmas.
* Best sellers differ by revenue against units (high-volume cheap lines against
  higher-value items), so pricing and bundling should treat them differently.
* The top non-UK markets are the Netherlands, Ireland, Germany, and France;
  Western Europe is the strongest region and the natural place to expand.
* The business is wholesale-driven: the top 1% of identified customers (about 43
  accounts) generate about 32% of identified-customer revenue, and non-UK orders
  (about 813 pounds) are much larger than UK orders (about 487 pounds).
* On data quality, about one in five raw lines was removed (cancellations,
  non-products, bad prices and quantities, duplicates), and missing customer IDs
  (about 25%) were kept and tagged GUEST rather than discarded.

See `FINDINGS.md` for the full summary and `CLEANING_DECISIONS.md` for the
reasoning behind every cleaning choice.
