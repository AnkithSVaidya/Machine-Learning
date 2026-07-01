# Cobblestone Gifts: Online Retail Sales Review

EECE 6544, Summer 2026 — Mini-Project #01.

This is our cleaning and analysis of a raw e-commerce export for Cobblestone
Gifts, a UK gift retailer (the public UK Online Retail dataset, 541,909
transaction lines, Dec 2010 through Dec 2011). We profile the raw file, write
down every cleaning decision and why we made it, build a completed-sales
dataset, and use it to answer seven business questions.

## What we did

We loaded the raw export with the right encoding and profiled it first:
shape, missing values, unique counts, summary stats, the usual. From there we
cleaned it up: standardized the country labels, renamed columns to
snake_case, decided what to do about missing customer IDs and blank
descriptions, and stripped out cancellations, non-product lines (postage,
bank fees, Amazon charges, manual adjustments), impossible prices/quantities,
and exact duplicates.

Once the data was trustworthy we engineered a few features, line revenue,
cleaned-up descriptions, a country-to-region lookup, and aggregated by
product, country, customer, and month. The notebook demonstrates all 21
required pandas techniques (3.1–3.21), each one labeled so it's easy to find.
Part 2 answers the seven business questions with code, numbers, and short
write-ups, plus two charts.

## Repo contents

- `online_retail_cleaning.ipynb` -> The notebook. Every technique is labeled by number.
- `clean_online_retail.csv` —> The cleaned, completed-sales dataset.
- `DATA_DICTIONARY.md` —> What every column in the clean dataset means.
- `FINDINGS.md` —> The one-page writeup of the seven business questions.
- `CLEANING_DECISIONS.md` -> The judgment calls, and why we made them.
- `charts/` —> The monthly revenue trend and top non-UK markets charts.
- `requirements.txt` —> What you need to run it.

`data.csv` itself (~50MB) isn't in the repo, will need to grab it from Kaggle and it'll be
ignored by git automatically.

## Getting the dataset

Easiest way: go to
<https://www.kaggle.com/datasets/carrie1/ecommerce-data>, hit Download,
unzip, and drop `data.csv` in the project root.

Or with the Kaggle CLI:
```bash
pip install kaggle                       # kaggle.json goes in ~/.kaggle/
kaggle datasets download -d carrie1/ecommerce-data
unzip ecommerce-data.zip
```

The file isn't UTF-8. The notebook reads it with
`encoding='ISO-8859-1'`, otherwise the £ symbol throws a decode error.

## Running it

```bash
python -m venv .venv
source .venv/bin/activate                # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook online_retail_cleaning.ipynb
```
Run All from top to bottom and it'll regenerate `clean_online_retail.csv` and
everything in `charts/` on its own.

## Findings, short version

Total cleaned revenue comes out to roughly £9.7M for the year. It's a
seasonal business, revenue climbs through the fall and peaks in November
2011 at about £1.43M, nearly double a typical month, right before Christmas.

Best sellers split differently depending on whether you look at revenue or
units sold, cheap items move in bulk, pricier ones don't need volume to
earn more, so pricing and bundling decisions shouldn't treat the two lists
the same way.

Outside the UK, the Netherlands, Ireland, Germany, and France are the biggest
markets, and Western Europe overall is where we'd point any expansion effort.

This is a wholesale-driven business. The top 1% of identified customers
(43 accounts) bring in about 30% of identified-customer revenue, and non-UK
orders average £791 versus £461 for UK orders, bigger, less frequent
purchases, consistent with wholesale buying.

On data quality: we removed about 3.6% of raw rows (cancellations,
non-product lines, bad prices/quantities, duplicates), leaving 522,504 clean
rows. About a quarter of those still have no customer ID, we kept them and
tagged them `GUEST` instead of throwing away real revenue.

Full writeup is in `FINDINGS.md`; the reasoning behind every cleaning call is
in `CLEANING_DECISIONS.md`.

## Known limitations

A few small things came up during review that we're flagging rather than
quietly patching, since none of them change the conclusions above:

- Our `region_map` doesn't include Hong Kong, so those rows end up bucketed
  as `Other` instead of `APAC`.
- About 442 rows have no `country` value. They're counted in totals pulled
  straight from `revenue` (like the £9.7M figure above), but pandas drops
  missing group keys by default, so they quietly disappear from any
  `groupby('country')` or `groupby('region')` table. That's about £4,700,
  roughly 0.05% of total revenue — small, but it means the country/region
  breakdowns won't add up exactly to the headline number.
- The cleaning ledger shows `blank_description: 0`. That's correct, not a
  mistake, those rows had already been caught by the non-product filter
  by the time we checked for blanks.
