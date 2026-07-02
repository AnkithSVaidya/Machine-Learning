# Findings: Cobblestone Gifts Sales Review (Dec 2010–Dec 2011)

Based on the clean completed-sales dataset, 515,601 lines, ~£9.66M in
revenue with all figures in GBP. Anything customer-level only covers the ~75% of
sales with a known customer ID; the rest are tagged `GUEST`.

## Seasonality
We looked at roughly £9.67M in total revenue for the year. Trading builds
through the autumn and peaks hard in November 2011, about £1.43M, more than
double a typical month, right in line with pre-Christmas wholesale
restocking. December looks weak in the chart, but that's just because the
export cuts off on the 9th, not a real drop-off. Whoever's planning Q4 stock
and cash flow should expect that spike. 
<img width="1080" height="540" alt="image" src="https://github.com/user-attachments/assets/084507b1-307b-4387-96a7-9e12b841c2bc" />

## Best sellers
Revenue and unit volume tell different stories here. By units, it's cheap
stuff moving in bulk, World War 2 Gliders Asstd Designs, Jumbo Bag Red
Retrospot, and Assorted Colour Bird Ornament lead the list. By revenue,
pricier items like the Regency Cakestand 3 Tier and Party Bunting climb the
list without needing anywhere near the same volume. Only 4 of the top 10
products by revenue also appear in the top 10 by units, so there isn't one
"best seller" story, it's a mix of high-volume/low-margin lines and
lower-volume/higher-value ones, and pricing or bundling decisions should
account for that split rather than treating every top-10 product the same.

## Markets
Netherlands leads non-UK revenue at ~£283K, then Ireland (~£258K), Germany
(~£191K), and France (~£181K), with Australia not far behind. Zoom out to
region level and Western Europe dominates at ~£753K. Those four countries
already buy at scale and sit close enough for reasonable shipping, they're
the obvious first stop if the company wants to grow internationally.
<img width="1080" height="540" alt="image" src="https://github.com/user-attachments/assets/6abd066b-f8f5-40fb-881b-2a990e16da54" />

## Customer concentration
This lookss like a wholesale business more than a retail one. The top 1% of
identified customers, about 43 accounts out of roughly 4,300, bring in
close to a third of identified-customer revenue (30%), and the single
biggest account alone is worth about £279K. When a handful of accounts carry
that much weight, retention matters more than acquisition.

## Order value
Average order sits around £492, but that hides a real split: non-UK orders
average £791 against £461 for UK orders. Makes sense, international buyers
are more likely to be wholesalers consolidating into fewer, bigger orders to
make the shipping worthwhile. Another point in favor of leaning into the
international wholesale side of the business.

## Returns and cancellations
Cancelled/returned lines are a small slice of the total row count but punch
above their weight in value, and they cluster around a handful of products
and a few large wholesale accounts, the kind of pattern you'd expect from
big orders getting walked back rather than widespread dissatisfaction. Beyond
removing the cancellation lines themselves, we also traced each cancellation
back to the original order it reversed (matching on customer, product, and
price) and removed that original line too, so a purchase that was later
fully or partially cancelled doesn't inflate revenue. That step alone
accounts for 6,944 additional rows removed. Worth keeping an eye on the
accounts behind these reversals, but it doesn't move the overall revenue
picture much beyond what's already reflected in the £9.66M total above.

## Data-quality memo
We removed 3.6% of raw rows for cancellations, non-product/service codes
(postage, bank charges, Amazon fees, manual adjustments), non-positive
quantities and prices, and exact duplicates. On top of that, we removed a
further 6,944 rows that were the original, since-cancelled orders behind
those cancellation lines, matched by customer, product, and price, so revenue
isn't inflated by purchases that were later reversed. Counting both steps
together, about 4.9% of raw rows were removed, leaving 515,601 clean rows.
Missing customer IDs (about 25% of what's left) weren't dropped, we tagged
them `GUEST` so real revenue didn't just disappear from the totals. A few
assumptions are baked into this: a 5-digit code means a real product, zero or
negative quantity/price isn't a valid sale, `GUEST` rows are genuine revenue
that just can't be tied to a name, and the cancellation-matching relies on a
known customer ID, so cancellations tied to a `GUEST` checkout can't be
traced back to their original order.

Would this hold up in a board report? For revenue, product, market, and
seasonality, yes, those all come straight from the cleaned completed-sales
data and don't wobble. The one caveat is the customer-level numbers (sections
3 and 4): they only reflect the ~75% of sales we can actually attribute to a
customer, so treat them as representative of the identified base, not the
entire book.
