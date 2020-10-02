#!/usr/bin/env python
# coding: utf-8

# ### Quick and dirty stock diversity analysis 1 - Find opposite groups the unsupervised way
# 
# A step-by-step guide to cluster stocks and identify interesting stock trends! So simple, a caveman can do it! All transformation done to the data are explained, if not, shout at me.
# 
# **Questions**
# 1. How to cluster stock trends?
# 2. How to find very different stock clusters and visualize their differences?
# 
# **We will transform, optimize, cluster, plot!**
# 
# We will use the **history_60d.csv** files in the https://www.kaggle.com/qks1lver/amex-nyse-nasdaq-stock-histories dataset, which has about 41 trading days of around 7800 stocks.
# 
# 2019.4.14 edit: I really didn't like the way I previously calculate the 2 most apart clusters (too lazy and too tired), so I updated it to a slightly more complex but more correct one.

# In[12]:


import os
print(os.listdir("../input"))

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn import decomposition
from sklearn.preprocessing import scale, minmax_scale
from sklearn import cluster
from scipy.optimize import minimize
from scipy.spatial.distance import euclidean


# In[2]:


# Load data and preview a bit
p_history = '../input/history_60d.csv'
df = pd.read_csv(p_history)
display(df.head())


# ### Question 1: How to cluster stock trends?
# 
# Let's first define trend as **relative day-to-day movement.** This means we want data on changes made during each trading day and we want to focus on the ratio of change (hint: relative data usually means taking the ratio). So, if we ask: **How has the stock changed over the course of a trading day?** One of the most straigh-forward responses would be **end-of-day price divide by start-of-day price**. Let's also **-1** that so \$110/\$ 100-1 = 0.10 and \$90/\$100-1 = -0.10. Then we try to cluster and see what we get and further analyze from there!

# In[3]:


# Transform data and save that as a new data frame
# Hint: when possible (i.e. if memory permits), refrain from changing the original data frame... this can save you hours of troubleshooting when analysis gets long!

# Number of unique stock symbols in the data
ntickers0 = len(df['symbol'].unique())

# [.assign()] df get a new "diff" column with adjusted close price / open price - 1
# [.pivot_table()] Then we "pivot" data frame, so we have a new table-like data frame with unique stock symbol for each row, dates analyzing as columns, and "diff" as the values
# [.dropna()] Then to simplify this basic analysis, let's get rid of all the stocks that for some reason have fewer days of data
dfx = df.assign(diff=df['adjclose']/df['open']-1).pivot_table(index='symbol', columns='date', values='diff', aggfunc=np.max).dropna()
display(dfx.head())

# Let's see how many stocks we still have left
ntickers1 = len(dfx)
print('Number of symbols: %d (%.2f)' % (ntickers1, ntickers1/ntickers0))

# Let's scale the data row-wise (i.e. independently for each stock) and save to another data frame so we can use dfx to plot later
# Important: This is a very critical step here for better clustering.
# Primarily because stock prices are so diverse (from a dollar to thousands) and the movement pattern could be the identical between 2 stocks,
# but because prices are different, the volumes become very different thus the ratios of change are different as a result.
# i.e. Stock-A: 0.5, -0.2, 0.4 and Stock-B: 0.25, -0.1, 0.2
# It would be challenging to mine out trend groups without some sort of scaling or normalization.
# Try removing the scaled() transformation part and run the rest and see what would happen. Doesn't cluster very well, does it?
dfscaled = pd.DataFrame(scale(dfx, axis=1), index=dfx.index, columns=dfx.columns)
display(dfscaled.head())

# After scaling, the mean of each row would be very very close to zero. You can check this with np.mean(dfscaled.values, axis=1)
# The previous example of Stock-A: 0.5, -0.2, 0.4 and Stock-B: 0.25, -0.1, 0.2
# would become Stock-A: 0.86, -1.40,  0.54 and Stock-B: 0.86, -1.40,  0.54
# Now, arguably this may not be what you want, but for this analysis on trends, this is an effective transformation


# ### Clustering! This is the cool part!
# DBSCAN is a pretty good clustering method, and I'll let this scikit-learn article do all the talking:
# https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html#sphx-glr-auto-examples-cluster-plot-cluster-comparison-py
# The tricky part is using the right epsilon (**eps**), and there's really no "right" way to do it since we don't know what clusters we want to see, or else we wouldn't be doing this. So, we can either try different eps manually **or** we can decide on **an assumption** and **an objective** and automate a search for the best eps that fits our goal.
# 
# **Assumption:** Stock trends are messy, the possibilitie are endless, so there could be as many clusters as the number of stocks out there.
# 
# **Objective function:** Find an eps that maximizes the number of clusters

# In[4]:


# Find the optimal eps and generate the clusters, this can take a while.

def clust_func(i, data):
    """
    This performs DBSCAN
    Each cluster is required to have at least 5 samples, this is arbitrary but it can significantly change the result.
    Play around with the min_samples to see what happens.
    n_jobs let's you specify how many CPUs to use, I don't know how many Kaggle let me use, so just set as -1 to use as many as allowed.
    """
    return cluster.DBSCAN(eps=i, min_samples=5, n_jobs=-1).fit_predict(data.values)

def clust_min_func(i, data):
    """
    This calculates the objective function with the DBSCAN result
    i.e. count the number of clusters
    Optimization here search for the minimal objective value, thus we negate the count to get it to maximize
    """
    if i <= 0:
        return np.Inf
    return -len(np.unique(clust_func(i, data)))

# This is Scipy's minimization function, we use COBYLA to solve so we don't have to bother with figuring out a gradient function
# The initial (first test) eps is set to 1, then the minimize() function will test this first and try to find a better one from there.
res = minimize(fun=clust_min_func, x0=1, args=dfscaled, method='cobyla')

# Store cluster label of each sample to "y" (thus y is an 1-by-n_samples array)
print('Optimal epsilon: ', res.x)
y = clust_func(res.x, dfscaled)
print('Clusters:')
print(np.unique(y))


# ### Question 2: How to find very different stock clusters and visualize their differences?
# Cluster with **-1** are outliers, ones that this round of DBSCAN cannot identify good clusters for, and there are likely a lot of them. For this analysis, let's just focus on the ones that got clustered. Seeing is believing. Plotting with the original data or scaled data may help us see the separations, but since clustering is done with around 40 days of data, it's likely that we'll have to plot a lot of dimensions to appreciate the separations of clusters. Instead, we can perform dimensionality **reduction techniques** (i.e. principle component analysis) to determine some of the best ways to separate the samples and return the new coordinates of the separated samples. By doing this, hopefully, we can plot fewer dimensions with the new coordinates and still see clear separations. We can also use these coordinates to automatically identify clusters that are polar opposites of each others.
# 
# Let's keep things simple. Let's just use the coordinates on the first 3 components of the PCA to identify the opposite clusters. The 1st component is always the one that can explain the highest variance in the data. But because it's stock, quite random, don't expect **comp1** to explain a lot of variance (probably around 10%), so let's take a bit more and see what happens. You can change **n_comps** to a higher value to account for more components from the PCA in calculating the opposite clusters. The following code simply compute the Euclidean distance from the lowest point of each component for each sample.

# In[16]:


# Do PCA to get transformed coordinates
n_comps = 3
m = decomposition.PCA()
X = m.fit_transform(dfscaled.values)
print('Explained variance ratio of %d components: %.2f' % (n_comps, np.sum(m.explained_variance_ratio_[:n_comps])))

# Generate PCA plot of first 2 components, also store the PCA coordinates of the clustered samples to "xs"
# Not all samples are clustered, many are considered outliers (-1), let's not plot outliers
xs = [[] for _ in range(np.max(y) + 1)]
_,g = plt.subplots(figsize=(10,10))
g = sns.scatterplot(x=X[:,0], y=X[:,1], ax=g, alpha=0.1)
for idx,(i,j,k) in enumerate(zip(X[:,0], X[:,1], y)):
    if k > -1:
        g.text(x=i, y=j, s=str(k))
        xs[k].append(X[idx, :n_comps])
g.set_xlabel('Component 1 ( %.1f%% of variance )' % (m.explained_variance_ratio_[0]*100))
g.set_ylabel('Component 2 ( %.1f%% of variance )' % (m.explained_variance_ratio_[1]*100))
plt.draw()
plt.show()

# Use "xs" to determine the average position of the clusters and store to "xm"
# Scale the average positions of each cluster to their min and max along each component so they can then be weighed by
# the amount of variance explainable by each component (i.e. how userful each is) - this attempts to position the clusters more fairly,
# since we will just use 1 metric (their Euclidean distances) to determine the clusters' similarities
# Then calculate the Euclidean distances of clusters to each other
# Then identify the clusters with the largest distance from each other
xm = minmax_scale(np.array([np.mean(x, axis=0) for x in xs]), axis=0) * m.explained_variance_ratio_[:n_comps]
xdist = []   # distances
xpairs = []  # cluster pairs
for i, a in enumerate(xm[:-2]):
    for j, b in enumerate(xm):
        if j > i:
            xpairs.append((i,j))
            xdist.append(euclidean(a,b))
clusters = xpairs[np.argmax(xdist)]
print('Clusters: %d and %d' % clusters)


# Each dot is a stock symbol. All the ones without a cluster ID next to them are outliers.... quite a bit, huh?

# In[6]:


# Plot the scaled trends of the selected 2 clusters to see why they are separated

# Compile the data frame for plotting
# Since the cluster label of each sample is stored in "y", we can use y to get the index of the samples we want to focus on
# [pd.melt()] Transform the "dfscaled" data frame so it's just 3 columns: stock symbols (symbols), dates (date), and the scaled values (value)
# [df.reset_index()] to convert the symbol index in dfscaled to just numerical row number indices
# [df.assign()] Give each cluster a name (i.e. g1)
dfy = pd.DataFrame()
for i in clusters:
    dtmp = pd.melt(dfscaled[y==i].reset_index(), id_vars='symbol', value_vars=dfscaled.columns)
    dfy = dfy.append(dtmp.assign(g='g%d'%i), ignore_index=True)
display(dfy.head())

# Plot with Seaborn's line plot so we can see the changes in adjusted close price / open price - 1 over the 40ish days
fig,g = plt.subplots(figsize=(16,5))
g = sns.lineplot(data=dfy, x='date', y='value', hue='g', ax=g, alpha=.1)
g.set_xlabel('')
g.set_ylabel('Relative movement')
plt.setp(g.get_xticklabels(), rotation=35, ha='right', va='top', rotation_mode='anchor')
g.axhline(y=0.)
sns.despine()
plt.draw()
plt.show()
fig.tight_layout()


# The 2 patterns should look **almost** like opposites of each other.

# In[7]:


# Now, what does the closing prices (untransformed) look like for these selected clusters?

# Compile the data frame for plotting
# Use the first data frame (df), but only if the symbols are the ones within the clusters
dfy = pd.DataFrame()
for i in clusters:
    dtmp = df[df['symbol'].isin(dfx[y==i].index)].reset_index()
    dfy = dfy.append(dtmp.assign(g='g%d'%i), ignore_index=True)
display(dfy.head())

# But! Because prices of stocks vary so much, we will unlikely see clear patterns (i.e. stock prices of the same cluster overlaying)
# So we much scale the prices of each stock, so the stocks are comparable
yscaled = []
for s in dfy['symbol'].unique():
    yscaled.append(dfy[dfy['symbol']==s]['adjclose'].values)
yscaled = scale(yscaled, axis=1)
dfy = dfy.assign(y=np.concatenate(yscaled))

# Plotting with line plot as we did before
fig,g = plt.subplots(figsize=(16,5))
g = sns.lineplot(data=dfy, x='date', y='y', hue='g', ax=g)
g = sns.scatterplot(data=dfy, x='date', y='y', hue='g', ax=g, alpha=0.1)
g.set_ylabel('Scaled closing price')
fig.autofmt_xdate()
plt.setp(g.get_xticklabels(), rotation=35, ha='right', va='top', rotation_mode='anchor')
sns.despine()
plt.draw()
plt.show()
fig.tight_layout()


# Whenever one cluster goes up, the other should go down. Each dot in a column (a day) represents a stock symbol of that cluster (color-coded).

# In[8]:


# What are the stocks in these clusters?
print('Cluster 1: ', ', '.join(dfx[y==clusters[0]].index.values))
print('\nCluster 2: ', ', '.join(dfx[y==clusters[1]].index.values))


# ### Conclusions
# It is possible to cluster and identify stocks with opposite trends with fairly simple statistical methods. Here we performed **DBSCAN to find the clusters**, used **PCA to reduce data dimensions** so we can visualize the clusters, used the PCA coordinates to **find the clusters with polar opposite stock movements**, proved that we actually found clusters with opposite movements, and listed what they are!
# 
# ### What's next?
# Notice how we didn't get to cluster everything and a lot of good stocks are left out in the dark (outliers). Next time, we'll explore ways to get them all and optimize your portfolio so it is diverse enough to withstand any unforeseeable economical disaster... sorta! No stock gets left behind!
# 
# ### Also...
# Let me know if you have questions about this kernel or find a mistake or disagree with something. Thanks!
# 
# Happy mining!
# 
# Jiun
