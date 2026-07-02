# Data Dictionary - `clean_online_retail.csv`

The cleaned, completed-sales dataset. One row is one valid sale line, so a single
product on a single non-cancelled invoice. 522,504 rows and 10 columns.

| Column | Type | What it holds |
|--------|------|---------------|
| `invoice_no` | string | Order ID. Every cancellation invoice (the ones with a leading C) has been removed, so each value here is a completed sale. |
| `stock_code` | string | Product code, a genuine 5-digit code with an optional single trailing letter (like 85123A). Service and adjustment codes (POST, DOT, M, BANK CHARGES, AMAZONFEE and the like) are gone. |
| `description` | string | Product name, run through strip() and title() so the spacing and casing line up. Blanks were removed. |
| `quantity` | integer | Units on the line. Always positive, since returns and negative quantities were dropped. |
| `unit_price` | float | Price per unit in pounds (GBP). Always positive, since zero and negative prices were dropped. |
| `revenue` | float | Line revenue, so quantity times unit_price, in pounds. |
| `invoice_date` | datetime | Transaction timestamp, parsed from the raw text date. |
| `customer_id` | string | Customer identifier. Known customers are integer-like strings (like 17850). Sales with no ID in the raw export are tagged GUEST, so they are kept as real revenue but left out of customer-level metrics. |
| `country` | string | Customer country, with the labels tidied up (EIRE to Ireland, RSA to South Africa, Unspecified to missing). |
| `region` | string | Region grouping merged in from the country to region lookup (UK&IE, Western Europe, APAC and so on). Countries not in the lookup are labelled Other. |

A few notes:

- Everything is in GBP.
- `revenue` is derived, it is always quantity times unit_price.
- The raw export (`data.csv`) is left untouched and kept separate. This file is
  the cleaned output only.
