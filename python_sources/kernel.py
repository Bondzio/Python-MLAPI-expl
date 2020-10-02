#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# In[ ]:


data = pd.read_csv('../input/train.csv')
data.head()


# In[ ]:


data.visits = data.visits.apply(lambda s: list(map(int, s.split())))
data['visits_day_of_week'] = data.visits.apply(lambda s: [(x - 1) % 7 + 1 for x in s])
data['diff'] = data.visits.apply(lambda l: [l[i] - l[i-1] for i in range(1, len(l))])
data.head()


# In[ ]:


def create_weights(seq):
    weights = np.cumsum(seq)
    return weights / np.linalg.norm(weights)

def predict(features):
    counts = [0] * 7
    weights = create_weights(features[3])
    for w, day in zip(weights, features[2]):
        counts[day - 1] += w
        
    counts = np.exp(counts) / np.exp(counts).sum()
    
    prediction = [counts[i] * np.prod(1-counts[:i]) for i in range(counts.size)]
    return np.argmax(prediction) + 1


# In[ ]:


ans = data.apply(predict, axis=1)


# In[ ]:


pd.DataFrame(data={'id': data.id.values, 'nextvisit': ans.values}).to_csv('solution.csv', index=False)

