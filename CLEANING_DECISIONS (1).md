# Cleaning Decisions

The judgment calls made turning the raw export into the clean completed-sales
dataset, and why each one went the way it did. The raw DataFrame stays separate
and untouched the whole time, so every cleaning step builds a new object.

| # | Decision | What I did | Why |
|---|----------|-----------|-----|
| 1 | Encoding | Read with `encoding='ISO-8859-1'`. | The file is not UTF-8, and the pound sign throws a decode error otherwise. |
| 2 | Cancellations | Dropped every line whose `InvoiceNo` starts with C (about 9,300). | They are reversals and returns, not completed sales. Analysed separately for Q6. |
| 3 | Non-product lines | Dropped rows whose `StockCode` is not a 5-digit product code (with an optional single trailing letter). | Catches POST, DOT, M, BANK CHARGES, AMAZONFEE, gift cards and manual adjustments, which are services and fees, not products. |
| 4 | Non-positive quantity | Dropped rows with `quantity <= 0`. | A sale moves at least one unit, so zero or less means a return or an adjustment. |
| 5 | Non-positive price | Dropped rows with `unit_price <= 0`. | A real sale has a positive price, so zero or negative lines are adjustments or bad data. |
| 6 | Blank descriptions | Handled after the filters above, and by then none were left. | Blank descriptions almost entirely overlap the non-product and zero-price lines already removed in steps 3 to 5, so no separate drop was needed. |
| 7 | Exact duplicates | Dropped fully identical rows (about 5,300) with `drop_duplicates()`. | Repeated identical lines would double-count revenue and units. |
| 8 | Missing CustomerID (about 25%) | Kept the rows and filled the blank id with GUEST. | These are real completed sales, so real product, positive quantity and price. Dropping a quarter of the data would understate revenue, best-sellers and market size. Tagging GUEST keeps revenue right while keeping the unknown honest. |
| 9 | Customer-level analysis | Left GUEST out of Q3 (distinct customers) and Q4 (concentration). | Those questions need named customers, and an undifferentiated GUEST bucket would throw off the counts and concentration. |
| 10 | Country labels | Mapped EIRE to Ireland, RSA to South Africa, and Unspecified to missing. | Standardise the inconsistent labels so country and region totals come out right. |
| 11 | Column names | Renamed everything to snake_case. | A consistent, query-friendly schema. |
| 12 | Dropped column | Dropped the `invoice_initial` helper. | It was only a scratch flag for spotting cancellations, and it can be rebuilt from `invoice_no`, so it adds nothing to the final table. |
| 13 | Region join | Used a left join for the region lookup, not inner, with unmatched countries set to Other. | A left join keeps every sale even when a country has no region entry, while an inner join would drop those sales and understate revenue. |
| 14 | Description cleaning | Applied strip() and title(). | Normalises the spacing and casing so product groupings don't fragment. |

## Net effect

- Raw rows: 541,909.
- Removed (cancellations, non-products, bad quantity and price, duplicates): about
  3.6% of raw lines, roughly 19,400 rows.
- Repaired (missing `customer_id` set to GUEST): about 25% of the clean rows.
- Final clean completed-sales rows: 522,504.

The per-step counts are printed in the notebook's data-quality ledger (Question 7).

## A note on the product-code filter

The product-code check anchors on both ends, so `\d{5}[A-Za-z]?` as a full match,
not just a prefix. An earlier prefix-only version let codes like `15056BL` slip
through, because they happen to start with five digits, and that contradicted the
rule this filter is meant to enforce. If you are re-running from a version that
used the prefix-only check, expect the clean row count to drop by a few hundred
rows once the anchored version clears those leftovers.
