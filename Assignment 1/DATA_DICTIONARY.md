# Data Dictionary: `clean_online_retail.csv`

The clean, completed-sales dataset. One row is one valid sale line (a single
product on a single non-cancelled invoice). 522,504 rows and 10 columns.

| Column | Type | Description |
|--------|------|-------------|
| `invoice_no` | string | Transaction (order) ID. All cancellation invoices (leading C) have been removed, so every value here is a completed sale. |
| `stock_code` | string | Product code, restricted to genuine 5-digit product codes (optionally with a letter suffix, for example 85123A). Service and adjustment codes (POST, DOT, M, BANK CHARGES, AMAZONFEE, and similar) were removed. |
| `description` | string | Product name, cleaned with strip() and title() so spacing and casing are consistent. Blank descriptions were removed. |
| `quantity` | integer | Units sold on the line. Always greater than 0, since returns and negative quantities were removed. |
| `unit_price` | float | Price per unit in pounds (GBP). Always greater than 0, since zero and negative prices were removed. |
| `revenue` | float | Line revenue, equal to quantity times unit_price, in pounds (GBP). |
| `invoice_date` | datetime | Timestamp of the transaction, parsed from the raw text date. |
| `customer_id` | string | Customer identifier. Known customers are integer-like strings (for example 17850). Sales with no customer ID in the raw export are tagged GUEST (kept as real revenue but excluded from customer-level metrics). |
| `country` | string | Customer country, with labels standardised (EIRE to Ireland, RSA to South Africa, Unspecified to missing). |
| `region` | string | Region grouping merged from the country-to-region lookup (for example UK&IE, Western Europe, APAC). Countries not in the lookup are labelled Other. |

Notes:
* Currency is GBP throughout.
* `revenue` is derived and equals quantity times unit_price for every row.
* The raw export (`data.csv`) is kept separate and untouched. This file is the
  cleaned output only.
