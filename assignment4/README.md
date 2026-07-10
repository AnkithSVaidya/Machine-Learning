### Assignment 4: Decision Tree
This program runs a decision tree on the Titanic data to predict surviveability. Both gini and entropy criterions were used.

For both criterions, the sex of the person was the most important feature but it had a higher effect with gini. Gini was slightly more accurate than entropy (79% vs 77%), but this difference was slight. Both criterions identify very similar features at similar importances, but for gini sex is a little bit higher.

Comparing the trees, the first few nodes of both trees are the same. However, as the tree goes down gini and entropy choose different features or thresholds. This makes sense, as the criterions agree on the high-impact features but disagree on the more marginal ones.