#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 


# In[ ]:


# Notebook reference
# https://www.kaggle.com/mayer79/m5-forecast-attack-of-the-data-table
# @mayer79


# In[ ]:


submission = pd.read_csv('../input/m5-forecast-attack-of-the-data-table/submission.csv')

for i in range(1,29):
    submission['F'+str(i)] *= 1.04
    
submission.to_csv('submission.csv', index=False)    

