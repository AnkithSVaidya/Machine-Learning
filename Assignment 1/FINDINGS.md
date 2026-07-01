# Findings Summary: Cobblestone Gifts Sales Review (Dec 2010 to Dec 2011)

Based on the clean completed-sales dataset (522,504 lines, about 10.2 million
pounds in revenue). All figures are in pounds (GBP). Customer-level figures cover
the roughly 75% of sales that have a known customer ID.

### 1. Seasonality
Total revenue is about 10.2 million pounds. Sales rise steadily through the autumn
and peak in November 2011 at about 1.45 million pounds, which is roughly double a
typical month (about +98%) and matches the pre-Christmas wholesale restocking
period. December 2011 looks low only because the export ends on 9 December. Stock
and cash should be planned for a large fourth-quarter peak.
See `charts/monthly_revenue.png`.

### 2. Best sellers
The top-10-by-revenue and top-10-by-units lists overlap only partly. The
high-unit sellers are cheap, high-volume items such as Paper Craft Little Birdie,
Medium Ceramic Top Storage Jar, and Jumbo Bag Red Retrospot. The top-revenue list
also includes higher-priced items such as the Regency Cakestand 3 Tier and Party
Bunting. Revenue therefore comes from a mix of volume lines and value lines, which
should be priced and bundled differently.

### 3. Markets
Outside the UK, the most valuable countries by revenue are the Netherlands (about
284,000 pounds), Ireland (about 271,000 pounds), Germany (about 205,000 pounds),
and France (about 184,000 pounds), followed by Australia. By region, Western Europe
is the strongest (about 774,000 pounds). These are the natural targets for
expansion because they already buy at scale and are close for shipping.
See `charts/top_markets.png`.

### 4. Customer concentration
The top 1% of identified customers (about 43 of roughly 4,300 accounts) account for
about 32% of identified-customer revenue, and the single largest account spends
about 279,000 pounds. This is typical of a wholesale business in which a small set
of large buyers dominates, so retaining the key accounts matters more than chasing
many small ones.

### 5. Order value
The average order is worth about 518 pounds. Non-UK orders (about 813 pounds) are
considerably larger than UK orders (about 487 pounds). Overseas buyers tend to be
wholesalers who order in bigger batches to spread shipping costs, which again
supports focusing on international wholesale accounts.

### 6. Returns and cancellations
Cancellation and return lines are a small share of the total line count but a
larger share of value, and they are concentrated in a handful of products and a few
large wholesale accounts where big bulk orders were reversed. These accounts are
worth monitoring, but they do not change the overall revenue picture.

### 7. Data-quality memo
About one in five raw lines was removed: cancellations, non-product and service
codes (postage, bank charges, Amazon fees, and manual adjustments), non-positive
quantities and prices, blank descriptions, and exact duplicates. Missing customer
IDs (about 25%) were repaired by setting them to GUEST rather than discarding
genuine sales. The assumptions were that a 5-digit code identifies a real product,
that zero or negative quantity and price lines are not valid sales, and that GUEST
rows are real revenue that cannot be attributed to a named customer.

Would I trust this for a board report? Yes for the revenue, product, market, and
seasonality questions, because those rest on the cleaned completed-sales lines and
are stable. One caveat: the customer-level metrics (Q3 and Q4) cover only the
roughly 75% of sales with a known ID, so they should be read as indicative of the
identified-customer base rather than the whole book.
