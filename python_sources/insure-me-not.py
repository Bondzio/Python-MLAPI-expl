#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns


from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

csv_chunks = pd.read_csv("../input/Rate.csv",iterator=True,chunksize = 1000)
rates = pd.concat(chunk for chunk in csv_chunks)
get_ipython().run_line_magic('matplotlib', 'inline')


# Code is a bit slow, will need to fix... later
# 
# 
# 

# In[ ]:





# In[ ]:


plans = pd.read_csv('../input/PlanAttributes.csv')


# In[ ]:


rates = rates[np.isfinite(rates['PrimarySubscriberAndOneDependent'])]
rates = rates[rates.IndividualRate <9000]


rates.head(n=5)


# In[ ]:


print(rates.describe())


# In[ ]:


import matplotlib.pyplot as plt

##Individual histograme
plt.hist(rates.IndividualRate.values)


# In[ ]:




