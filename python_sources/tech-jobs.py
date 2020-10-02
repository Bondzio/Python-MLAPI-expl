#!/usr/bin/env python
# coding: utf-8

# 

# In[ ]:


import pandas as pd
import numpy as np
import datetime


import warnings
warnings.filterwarnings("ignore")
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="white", color_codes=True)



# Read data 
d=pd.read_csv("../input/h1b_kaggle.csv")


# In[ ]:


d['EMPLOYER_NAME'].value_counts().head(15)


# In[ ]:


t=d[d['WORKSITE']=='PHILADELPHIA, PENNSYLVANIA']
t['EMPLOYER_NAME'].value_counts().head(25)


# In[ ]:


t=d[d['EMPLOYER_NAME']=='COMCAST CABLE COMMUNICATIONS, LLC']
t['PREVAILING_WAGE'].value_counts().tolist
#sns.distplot(t['PREVAILING_WAGE']);
t=t[t['PREVAILING_WAGE']<500000]
sns.distplot(t['PREVAILING_WAGE']);
#t['PREVAILING_WAGE'].describe()


# In[ ]:


t[(t['SOC_NAME']=='COMPUTER AND INFORMATION SYSTEMS MANAGERS') & (t['PREVAILING_WAGE'] < 90000)]


# In[ ]:


tt=t[ (t['PREVAILING_WAGE'] < 95000)]
tt['SOC_NAME'].value_counts().head(20)


# In[ ]:


tt=t[ (t['PREVAILING_WAGE'] >= 95000)]
tt['SOC_NAME'].value_counts().head(20)


# In[ ]:



d['title']=d['SOC_NAME'].str.upper()
d['title'].head()


# In[ ]:


# SOFTWARE ALL
t=d[d.title.str.match(r'.*SOFTWARE.*', na=False)]
t = t[(t['PREVAILING_WAGE']>= 0) & (t['PREVAILING_WAGE']<=150000)]
sns.distplot(t['PREVAILING_WAGE']);

