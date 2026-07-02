# Findings - Cobblestone Gifts Sales Review (Dec 2010 to Dec 2011)

From the clean completed-sales dataset (522,504 lines, about 10.2M pounds in
revenue). Everything is in GBP. The customer-level figures cover the roughly 75%
of sales that carry a known customer ID.

### 1. Seasonality

Total revenue is about 10.2M pounds. Sales climb through the autumn and peak in
November 2011 at roughly 1.45M, which is close to double a normal month (about
+98%), and that lines up with the pre-Christmas wholesale restock. December 2011
only looks weak because the export stops on the 9th. Stock and cash should be
planned for a heavy fourth quarter. See `charts/monthly_revenue.png`.

### 2. Best sellers

The top-10-by-revenue and top-10-by-units lists only partly overlap. The high-unit
sellers are cheap, high-volume items, things like Paper Craft Little Birdie, Medium
Ceramic Top Storage Jar and Jumbo Bag Red Retrospot. The revenue list also brings
in higher-priced items such as the Regency Cakestand 3 Tier and Party Bunting. So
revenue comes from a mix of volume lines and value lines, and they are worth
pricing and bundling differently.

### 3. Markets

Outside the UK, the most valuable countries by revenue are the Netherlands (about
284,000 pounds), Ireland (about 271,000), Germany (about 205,000) and France
(about 184,000), with Australia close behind. By region, Western Europe is far and
away the strongest (about 774,000). These are the natural expansion targets, since
they already buy at scale and are close for shipping. See `charts/top_markets.png`.

### 4. Customer concentration

The top 1% of identified customers (about 43 of roughly 4,300 accounts) account
for about 32% of identified-customer revenue, and the single largest account
spends around 279,000 pounds. That is the shape you would expect from a wholesale
business, where a handful of large buyers dominate, so holding onto the key
accounts matters more than chasing lots of small ones.

### 5. Order value

The average order is worth about 518 pounds. Non-UK orders (about 817) run
considerably larger than UK ones (about 487). Overseas buyers tend to be
wholesalers ordering in bigger batches to spread the shipping cost, which again
points toward international wholesale accounts.

### 6. Returns and cancellations

Cancellations and returns are a small share of the line count but a bigger share
of value, and they cluster in a few products and a handful of large wholesale
accounts where bulk orders got reversed. Those accounts are worth watching, but
they don't shift the overall revenue picture.

### 7. Data-quality memo

About one raw line in five was removed or repaired: cancellations, non-product and
service codes (postage, bank charges, Amazon fees, manual adjustments),
non-positive quantities and prices, blank descriptions, and exact duplicates. The
missing customer IDs (about 25%) were repaired to GUEST rather than discarded. The
assumptions were that a 5-digit code identifies a real product, that zero or
negative quantity and price lines are not valid sales, and that GUEST rows are real
revenue that just can't be tied to a named customer.

Would I trust this for a board report? Yes on revenue, products, markets and
seasonality, since those rest on the clean completed-sales lines and hold up. One
caveat: the customer-level metrics (Q3 and Q4) only cover the roughly 75% of sales
with a known ID, so they should be read as indicative of the identified-customer
base rather than the whole book.
