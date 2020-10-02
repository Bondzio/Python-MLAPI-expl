#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from matplotlib import pyplot


# In[ ]:


df=pd.read_csv("../input/indian-women-in-defense/WomenInDefense.csv")
print(df.shape)


# In[ ]:


df.plot(kind ='box', subplots=True, layout=(3,3), sharex=False, sharey=False)
pyplot.show()


# In[ ]:


df.hist()
pyplot.show()


# In[ ]:


scatter_matrix(df)
pyplot.show()

