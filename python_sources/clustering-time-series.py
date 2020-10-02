#!/usr/bin/env python
# coding: utf-8

# This is my first kernel, I still got a lot to learn and hope this helps. You also might want to check this kernel here since I too learned from him.
# https://www.kaggle.com/darshanadiga/time-series-data-exploration

# In[ ]:


import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
from math import sqrt
import sys
from scipy import spatial


# In[ ]:


df = pd.read_csv('../input/train.csv')


# After we load the data, we now plot the store based on the item sales

# In[ ]:


sales_across_store_df = df.copy()
sales_across_store_df = pd.pivot_table(sales_across_store_df, index='store', 
                                       values=['sales','date'], columns='item', aggfunc=np.mean)
sales_across_store_df['avg_sale'] = sales_across_store_df.apply(lambda r: r.mean(), axis=1)

sales_store_data = go.Scatter(
    y = sales_across_store_df.avg_sale.values,
    mode='markers',
    marker=dict(
        size = sales_across_store_df.avg_sale.values,
        color = sales_across_store_df.avg_sale.values,
        colorscale='Viridis',
        showscale=True
    ),
    text = sales_across_store_df.index.values
)
data = [sales_store_data]

sales_store_layout = go.Layout(
    autosize= True,
    title= 'Scatter plot of avg sales per store',
    hovermode= 'closest',
    xaxis= dict(
        title= 'Stores',
        ticklen= 10,
        zeroline= False,
        gridwidth= 1,
    ),
    yaxis=dict(
        title= 'Avg Sales',
        ticklen= 10,
        zeroline= False,
        gridwidth= 1,
    ),
    showlegend= False
)
fig = go.Figure(data=data, layout=sales_store_layout)
py.iplot(fig,filename='scatter_sales_store')


# In[ ]:


store_clusters = []
store_clusters.append([2, 3, 4, 8, 9, 10])
store_clusters.append([1])
store_clusters.append([5, 6, 7])


# As we can see, in terms of average sales, store 2, 3, 4, 8, 9, and 10 seems to be in  one cluster while 5, 6, and 7 in another cluster and store 1 in also another cluster. So we have 3 clusters. The following code will dig down to more detail into peritem. (index in the picture starts from 0)

# In[ ]:


sales_across_item_df = df.copy()
sales_across_item_df = pd.pivot_table(sales_across_item_df, index='store', 
                                       values=['sales','date'], columns='item', aggfunc=np.mean)
sales_across_item_df.loc[11] = sales_across_item_df.apply(lambda r: r.mean(), axis=0)
avg_sales_per_item_across_stores_df = pd.DataFrame(data=[[i+1,a] for i,a in enumerate(sales_across_item_df.loc[11:].values[0])], columns=['item', 'avg_sale'])

# Scatter plot of average sales per item
sales_item_data = go.Bar(
    x=[i for i in range(0, 50)],
    y=avg_sales_per_item_across_stores_df.avg_sale.values,
    marker=dict(
        color=avg_sales_per_item_across_stores_df.avg_sale.values,
        colorscale='Blackbody',
        showscale=True
    ),
    text = avg_sales_per_item_across_stores_df.item.values
)
data = [sales_item_data]

sales_item_layout = go.Layout(
    autosize= True,
    title= 'Scatter plot of avg sales per item',
    hovermode= 'closest',
    xaxis= dict(
        title= 'Items',
        ticklen= 55,
        zeroline= False,
        gridwidth= 1,
    ),
    yaxis=dict(
        title= 'Avg Sales',
        ticklen= 10,
        zeroline= False,
        gridwidth= 1,
    ),
    showlegend= False
)
fig = go.Figure(data=data, layout=sales_item_layout)
py.iplot(fig,filename='scatter_sales_item')


# Now we see that items sales are vary among others, some have very high sales while the other don't. Now we will plot per item per store

# In[ ]:


def plot_sales(item_ids, store_ids):
    stores_items_df = df.copy()    
    multi_store_item_ts_data = []
    for st,it in zip(store_ids, item_ids):
        flt = stores_items_df[stores_items_df.store == st]
        flt = flt[flt.item == it]
        multi_store_item_ts_data.append(go.Scatter(x=flt.date, y=flt.sales, name = "Store:" + str(st) + ",Item:" + str(it)))
    py.iplot(multi_store_item_ts_data)


# In[ ]:


plot_sales([1], [1])


# That sales plot really shows us that there is seasonal pattern in it.

# In[ ]:


plot_sales([1 for _ in range(10)], [x+1 for x in range(10)])


# Those are plots on item 1 in all stores. They seem to follow the same pattern.

# In[ ]:


for store_cluster in store_clusters:
    plot_sales([1 for _ in range(len(store_cluster))], store_cluster)


# Well I don't think split the data in to cluster based on the store make any difference. So next I will item on item in the same and different store.

# In[ ]:


plot_sales([1, 1, 15, 15, 42, 42], [2, 7, 2, 7, 2, 7])


# Now we see each of the sales data react differently to the seasonal pattern. So next I will try to cluster them for each item per store using K means.

# In[ ]:


def euclid_dist(t1, t2):
    return np.sqrt(((t1-t2)**2).sum(axis = 1))


# In[ ]:


def init_centroids(data, num_clust):
    centroids = np.zeros([num_clust, data.shape[1]]) 
    centroids[0,:] = data[np.random.randint(0, data.shape[0], 1)]

    for i in range(1, num_clust):
        D2 = np.min([np.linalg.norm(data - c, axis = 1)**2 for c in centroids[0:i, :]], axis = 0) 
        probs = D2/D2.sum()
        cumprobs = probs.cumsum()
        ind = np.where(cumprobs >= np.random.random())[0][0]
        centroids[i, :] = np.expand_dims(data[ind], axis = 0)

    return centroids


# In[ ]:


def calc_centroids(data, centroids):
    dist = np.zeros([data.shape[0], centroids.shape[0]])

    for idx, centroid in enumerate(centroids):
        dist[:, idx] = euclid_dist(centroid, data)

    return np.array(dist)


# In[ ]:


def closest_centroids(data, centroids): 
    dist = calc_centroids(data, centroids) 
    return np.argmin(dist, axis = 1)


# In[ ]:


def move_centroids(data, closest, centroids):
    k = centroids.shape[0]
    new_centroids = np.array([data[closest == c].mean(axis = 0) for c in np.unique(closest)])

    if k - new_centroids.shape[0] > 0:
        print("adding {} centroid(s)".format(k - new_centroids.shape[0]))
        additional_centroids = data[np.random.randint(0, data.shape[0], k - new_centroids.shape[0])] 
        new_centroids = np.append(new_centroids, additional_centroids, axis = 0)

    return new_centroids


# In[ ]:


def k_means(data, num_clust, num_iter): 
    centroids = init_centroids(data, num_clust)
    last_centroids = centroids

    for n in range(num_iter):
        closest = closest_centroids(data, centroids)
        centroids = move_centroids(data, closest, centroids)
        if not np.any(last_centroids != centroids):
            break
        last_centroids = centroids

    return centroids


# In[ ]:


def cosine_similarity(t1, t2):
    return 1 - spatial.distance.cosine(t1, t2)


# In[ ]:


store_ids = [s for s in range(1, 11)]
item_ids = [i for i in range(1, 51)]

multi_store_item_df = df.copy()
series_sales = []

for it in item_ids:
#     sales = []
    for st in store_ids:
        flt = multi_store_item_df[multi_store_item_df.store == st]
        flt = flt[flt.item == it]
        series_sales.append(list(flt.sales.values))
    
series_sales = np.reshape(series_sales, (len(series_sales), len(series_sales[0])))
series_sales.shape


# In[ ]:


num_cluster = 25
centroids = k_means(series_sales, num_cluster, 100)

sales_clusters = [[] for _ in range(num_cluster)]
for i in range(len(series_sales)):
    clostest_dist = 0
    clust = 0
    for c in range(num_cluster):
        dist = cosine_similarity(centroids[c], series_sales[i])
        if dist > clostest_dist:
            clostest_dist = dist
            clust = c
    sales_clusters[clust].append({
        'store': (i%10) + 1,
        'item': int(i/10) + 1
    })

for sales_cluster in sales_clusters:
    print(len(sales_cluster))


# I tried to make 10 cluster and see the number of member on each cluster

# In[ ]:


item_ids = []
store_ids = []
for sales_dict in sales_clusters[5]:
    item_ids.append(sales_dict['item'])
    store_ids.append(sales_dict['store'])
plot_sales(item_ids, store_ids)

item_ids = []
store_ids = []    
for sales_dict in sales_clusters[10]:
    item_ids.append(sales_dict['item'])
    store_ids.append(sales_dict['store'])
plot_sales(item_ids, store_ids)

item_ids = []
store_ids = []
for sales_dict in sales_clusters[15]:
    item_ids.append(sales_dict['item'])
    store_ids.append(sales_dict['store'])
plot_sales(item_ids, store_ids)


# The member of the same cluster seems to have the very similiar pattern

# I think maybe if we use these clusters to train the model, it might help to improve the accuracy. Hope this helps, thank you.

# In[ ]:





# In[ ]:




