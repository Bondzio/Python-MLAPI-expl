#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


Yogurt = pd.read_csv("../input/Yogurt.csv").drop("Unnamed: 0",axis=1)
brands = ['dannon', 'hiland', 'weight', 'yoplait']
brands_ordered = [x[0] for x in sorted([[brand,Yogurt["price." + brand].mean()] 
                                        for brand in brands],key = lambda x : x[1])]


# In[ ]:


def filter_id(n,df): return df[df["id"] == n]
def filter_choice(yogurt,df): return df[df["choice"] == yogurt]
def filter_feature(yogurt,feature,df): return df[df["feat." + yogurt] == feature]


# In[ ]:


def yogurt_filter_id_choice_feature(n,yogurt,feature):
    return filter_feature(yogurt,feature,filter_choice(yogurt,filter_id(n,Yogurt)))
def yogurt_filter_id_choice_feature_bar(n,feature):
    return np.array([yogurt_filter_id_choice_feature(n,yogurt,feature).shape[0] for yogurt in brands_ordered])


# In[ ]:


#the random 0.0000001 is to deal with customers who don't purchase any units of a specific brand
def emperical_entropy(purchase_freq):
    x = ((purchase_freq / purchase_freq.sum()) + 0.0000001)
    return - (x * np.log2(x)).sum()


# In[ ]:


entropy_id_pairs = [(emperical_entropy(yogurt_filter_id_choice_feature_bar(n+1,0) + 
                                       yogurt_filter_id_choice_feature_bar(n+1,1)),n+1) 
                    for n in range(100)]


# In[ ]:


entropy_id_pairs_sorted = sorted(entropy_id_pairs, key = lambda x: x[0])
def ids_ordered(n): return entropy_id_pairs_sorted[n][1]


# In[ ]:


def customer_to_grid(n): return [(i,j) for i in range(10) for j in range(10)][n]


# In[ ]:


xticks = [0,1,2,3]
feat_colors = sns.color_palette("pastel")
not_feat_colors = sns.color_palette()

f, ax = plt.subplots(10,10,figsize=(20, 15))
f.tight_layout()

for n in range(100):
    i = customer_to_grid(n)[0]
    j = customer_to_grid(n)[1]
    ax[i,j].bar(xticks,yogurt_filter_id_choice_feature_bar(ids_ordered(n),0),align='center',color=not_feat_colors)
    ax[i,j].bar(xticks,yogurt_filter_id_choice_feature_bar(ids_ordered(n),1),align='center',
                bottom=yogurt_filter_id_choice_feature_bar(ids_ordered(n),0),color=feat_colors)
    ax[i,j].set_xticks([])
    ax[i,j].set_yticks([])
plt.show()


# These bar plots show the number of times each customer puchases each type of yogurt. The barplots are normalized. This is necessary because some customers purchase a lot more yogurt than others. The customers are ordered by the entropy of there emperical purchasing distrubution. The colors are
# 
# - blue = hiland.    average price = 5.36
# - green = weight.   average price = 7.95
# - red = dannon.     average price = 8.16
# - purple = yoplait. average price = 10.68
# 
# the light colors are the are the purchases where the yogurt was featured.

# In[ ]:




