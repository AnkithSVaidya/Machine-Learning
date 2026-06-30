# Cleaning Decisions Log

The judgment calls made while turning the raw export into the clean
completed-sales dataset, and the reasoning behind each one. The raw DataFrame is
kept separate and untouched, and all cleaning builds new objects.

| # | Decision | What was done | Why |
|---|----------|---------------|-----|
| 1 | Encoding | Read with `encoding='ISO-8859-1'`. | The file is not UTF-8, and the pound symbol raises a decode error under UTF-8. |
| 2 | Cancellations | Dropped all lines whose `InvoiceNo` starts with C (about 9,300 lines). | They are reversals and returns, not completed sales. They are analysed separately for Q6. |
| 3 | Non-product lines | Dropped rows whose `StockCode` is not a 5-digit product code (optionally with a letter). | This catches POST, DOT, M, BANK CHARGES, AMAZONFEE, gift cards, and manual adjustments, which are services and fees rather than product sales. |
| 4 | Non-positive quantity | Dropped rows with `quantity <= 0`. | A sale moves at least one unit, so a value of zero or less indicates a return or adjustment. |
| 5 | Non-positive price | Dropped rows with `unit_price <= 0`. | A valid sale has a positive price, so zero or negative lines are adjustments or bad data. |
| 6 | Blank descriptions | Dropped rows with a missing `description` (about 1,500). | These overwhelmingly coincide with zero-price and non-product lines and carry no sale information. |
| 7 | Exact duplicates | Dropped fully identical rows (about 5,300) with `drop_duplicates()`. | Repeated identical lines would double-count revenue and units. |
| 8 | Missing CustomerID (about 25%) | Kept the rows and filled the blank id with the value GUEST. | These are genuine completed sales (real product, positive quantity and price). Dropping a quarter of the data would understate total revenue, best-sellers, and market size. Tagging GUEST keeps revenue correct while making the unknown explicit. |
| 9 | Customer-level analysis | Excluded GUEST from Q3 (distinct customers) and Q4 (concentration). | Those questions need named customers, and an undifferentiated GUEST bucket would distort counts and concentration. |
| 10 | Country labels | Mapped EIRE to Ireland, RSA to South Africa, and Unspecified to missing. | Standardise inconsistent labels so country and region aggregates are correct. |
| 11 | Column names | Renamed all columns to snake_case. | A consistent, query-friendly schema. |
| 12 | Dropped column | Dropped the `invoice_initial` helper. | It was only a scratch flag for detecting cancellations and can be recreated from `invoice_no`, so it adds nothing to the final analysis. |
| 13 | Region join | Used a left join (not inner) for the region lookup, with unmatched countries set to Other. | A left join keeps every sale even when a country has no region entry, whereas an inner join would drop those sales and understate revenue. |
| 14 | Description cleaning | Applied strip() and title(). | Normalises inconsistent spacing and casing so product groupings do not fragment. |

## Net effect
* Raw rows: 541,909.
* Removed (cancellations, non-products, bad quantity and price, blank
  descriptions, duplicates): about one in five lines.
* Repaired (missing `customer_id` set to GUEST): about 25% of the clean rows.
* Final clean completed-sales rows: 522,504.

The exact per-step counts are printed in the notebook's data-quality ledger
(Question 7).
