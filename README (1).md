# Cobblestone Gifts - Online Retail Sales Review

EECE 6544, Summer 2026 - Mini-Project 01.

Cobblestone Gifts is a UK gift retailer, and this is a cleanup and analysis of a
raw export from their order system (the public UK Online Retail dataset, 541,909
transaction lines running Dec 2010 through Dec 2011). The export had never been
touched. It mixed real sales with cancellations, was missing a customer ID on
about a quarter of the rows, and was full of postage charges, bank fees and
manual adjustments. The job was to make it trustworthy first, then answer seven
questions off the back of it.

## What's in here

The work splits into three parts. First we profile the raw file: encoding, shape,
missing values, the usual quality read. Then we clean it, so we standardise the
country labels, rename columns to snake_case, decide what to do about the missing
customer IDs and blank descriptions, and strip out the cancellations, non-product
lines, impossible prices and quantities, and the exact duplicates. Finally we
engineer a few features (line revenue, a country to region lookup, cleaned
descriptions), aggregate by product, country, customer and month, and answer the
business questions.

The notebook goes through all 21 required pandas techniques (3.1 to 3.21), and
each one has a numbered header so it is easy to find. Part 2 answers the seven
questions with code, numbers and a short writeup each, plus two charts.

## Files

| File | What it is |
|------|-----------|
| `online_retail_cleaning.ipynb` | The notebook. Techniques labelled by number. |
| `clean_online_retail.csv` | The cleaned, completed-sales dataset. |
| `DATA_DICTIONARY.md` | What each column in the clean dataset means. |
| `FINDINGS.md` | One-page writeup of the seven questions. |
| `CLEANING_DECISIONS.md` | The judgment calls, and the reasoning behind them. |
| `charts/` | Monthly revenue trend and top non-UK markets. |
| `requirements.txt` | What you need to run it. |

`data.csv` (about 50 MB) is not committed, you grab it from Kaggle (below) and git
ignores it.

## Getting the data

Quickest way is to open <https://www.kaggle.com/datasets/carrie1/ecommerce-data>,
hit Download, unzip, and drop `data.csv` in the project root.

Or with the CLI:

```bash
pip install kaggle                       # kaggle.json goes in ~/.kaggle/
kaggle datasets download -d carrie1/ecommerce-data
unzip ecommerce-data.zip
```

The file is not UTF-8. The notebook reads it with `encoding='ISO-8859-1'`, and
without that the pound sign throws a decode error.

## Running it

```bash
python -m venv .venv
source .venv/bin/activate                # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook online_retail_cleaning.ipynb
```

Run All from top to bottom and it will regenerate `clean_online_retail.csv` and
everything under `charts/`.

## The findings, short version

Cleaned revenue comes out to roughly 10.2M pounds for the year. It is a seasonal
business, sales build through the autumn and peak in November 2011 at about 1.45M,
nearly double a normal month, right before Christmas.

The best seller picture depends on how you look at it. By units, cheap items move
in bulk. By revenue, the pricier products earn their keep without needing the
volume. So the two lists don't match, and pricing and bundling shouldn't treat
them like they do.

Outside the UK, the Netherlands, Ireland, Germany and France are the biggest
markets, and Western Europe is where any expansion effort should go.

This reads like a wholesale business. The top 1% of identified customers (about 43
accounts) bring in roughly 32% of identified-customer revenue, and non-UK orders
average about 813 pounds against 487 for UK ones, so bigger and less frequent
baskets, which is what wholesale buying looks like.

On data quality, about 3.6% of the raw rows came out (cancellations, non-product
lines, bad prices and quantities, duplicates), which leaves 522,504 clean rows.
About a quarter of those still have no customer ID, and we kept them and tagged
them `GUEST` instead of throwing away real revenue.

Full writeup is in `FINDINGS.md`, and the reasoning behind every cleaning call is
in `CLEANING_DECISIONS.md`.

## Known limitations

A couple of small things we are flagging rather than hiding, since neither one
changes the conclusions:

- About 442 rows have no `country`. They still count toward totals pulled straight
  off `revenue` (like the 10.2M headline), but pandas drops missing group keys by
  default, so they quietly fall out of any `groupby('country')` or
  `groupby('region')` table. That is roughly 4,700 pounds, about 0.05% of revenue,
  so the country and region breakdowns won't add up to the headline exactly.
- The cleaning ledger shows `blank_description: 0`, and that is correct, not a
  miss. Those rows had already been caught by the non-product and bad-price filters
  by the time the blank-description check ran.
