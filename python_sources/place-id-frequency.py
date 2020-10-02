#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:


df = pd.read_csv('../input/train.csv')


# In[ ]:


place_counts = Counter(df.place_id.values)


# In[ ]:


fig = plt.figure(figsize=(10,5))
bins = np.arange(0.5, max(list(place_counts.values()))+1, 1)
plt.hist(list(place_counts.values()),
         bins=bins, alpha=0.5)
plt.xlabel('Number of place_id occurrences')
plt.ylabel('Frequency')
plt.show()


# In[ ]:


print("Total number of place_id's:    {}".format(len(df)))
print("Unique place_id's:             {}".format(len(place_counts)))
print('Average number of occurrences: {:.0f}'.format(np.mean(list(place_counts.values()))))

