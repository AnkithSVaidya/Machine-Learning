# Findings: Cobblestone Gifts Sales Review (Dec 2010–Dec 2011)

Based on the clean completed-sales dataset, 522,504 lines, ~£10.2M in
revenue with all figures in GBP. Anything customer-level only covers the ~75% of
sales with a known customer ID; the rest are tagged `GUEST`.

## Seasonality

We looked at roughly £10.2M in total revenue for the year. Trading builds
through the autumn and peaks hard in November 2011, about £1.45M, nearly
double a typical month, right in line with pre-Christmas wholesale
restocking. December looks weak in the chart, but that's just because the
export cuts off on the 9th, not a real drop-off. Whoever's planning Q4 stock
and cash flow should expect that spike. 

## Best sellers

Revenue and unitvolume tell different stories here. By units, it's cheap
stuff moving in bulk, Paper Craft Little Birdie, the Medium Ceramic Top
Storage Jar, Jumbo Bag Red Retrospot. By revenue, pricier items like the
Regency Cakestand 3 Tier and Party Bunting climb the list without needing
anywhere near the same volume. So there isn't one "best seller" story, it's
a mix of high-volume/low-margin lines and lower-volume/higher-value ones, and
pricing or bundling decisions should account for that split rather than
treating every top-10 product the same.

## Markets

Netherlands leads non-UK revenue at ~£284K, then Ireland (~£271K), Germany
(~£205K), and France (~£184K), with Australia not far behind. Zoom out to
region level and Western Europe dominates at ~£774K. Those four countries
already buy at scale and sit close enough for reasonable shipping, they're
the obvious first stop if the company wants to grow internationally.
(`charts/top_markets.png`)

## Customer concentration

This lookss like a wholesale business more than a retail one. The top 1% of
identified customers, about 43 accounts out of roughly 4,300, bring in
close to a third of identified-customer revenue (32%), and the single
biggest account alone is worth about £279K. When a handful of accounts carry
that much weight, retention matters more than acquisition.

## Order value

Average order sits around £518, but that hides a real split: non-UK orders
average £813 against £487 for UK orders. Makes sense, international buyers
are more likely to be wholesalers consolidating into fewer, bigger orders to
make the shipping worthwhile. Another point in favor of leaning into the
international wholesale side of the business.

## Returns and cancellations

Cancelled/returned lines are a small slice of the total row count but punch
above their weight in value, and they cluster around a handful of products
and a few large wholesale accounts, the kind of pattern you'd expect from
big orders getting walked back rather than widespread dissatisfaction. Worth
keeping an eye on those accounts, but it doesn't move the overall revenue
picture much.

## Data-quality memo

We remove 3.6% of raw rows, cancellations, non-product/service codes
(postage, bank charges, Amazon fees, manual adjustments), non-positive
quantities and prices, and exact duplicates. Missing customer IDs (about 25%
of what's left) weren't dropped, we tagged them `GUEST` so real revenue
didn't just disappear from the totals. A few assumptions are baked into
this: a 5-digit code means a real product, zero or negative quantity/price
isn't a valid sale, and `GUEST` rows are genuine revenue that just can't be
tied to a name.

Would this hold up in a board report? For revenue, product, market, and
seasonality, yes, those all come straight from the cleaned completed-sales
data and don't wobble. The one caveat is the customer-level numbers (sections
3 and 4): they only reflect the ~75% of sales we can actually attribute to a
customer, so treat them as representative of the identified base, not the
entire book.
