#!/usr/bin/env python
# coding: utf-8

# ### Imports

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Read Data

# In[ ]:


df_train = pd.read_csv('../input/X_train.csv', encoding='cp949')
df_test = pd.read_csv('../input/X_test.csv', encoding='cp949')
y_train = pd.read_csv('../input/y_train.csv').gender
IDtest = df_test.custid.unique()

df_train.head()


# ### Transform Data with One-hot Encoding

# In[ ]:


level = 'corner_nm'
df_train[level].nunique()


# In[ ]:


df_all = pd.concat([df_train, df_test])
X_train = pd.pivot_table(df_all, index='custid', columns=level, values='tot_amt',
                         aggfunc=lambda x: np.where(len(x) >=1, 1, 0), fill_value=0). \
                         reset_index(). \
                         query('custid not in @IDtest'). \
                         drop(columns=['custid']).values
X_test = pd.pivot_table(df_all, index='custid', columns=level, values='tot_amt',
                         aggfunc=lambda x: np.where(len(x) >=1, 1, 0), fill_value=0). \
                         reset_index(). \
                         query('custid in @IDtest'). \
                         drop(columns=['custid']).values

max_features = X_train.shape[1]


# ### Build Models

# In[ ]:


# Learn XGB
from xgboost import XGBClassifier
import sys, warnings
if not sys.warnoptions: warnings.simplefilter("ignore")

model = XGBClassifier(random_state=0, n_jobs=-1)
model.fit(X_train, y_train)


# ### Make Submissions

# In[ ]:


pred = model.predict_proba(X_test)[:,1]
fname = 'submissions_OHE.csv'
submissions = pd.concat([pd.Series(IDtest, name="custid"), pd.Series(pred, name="gender")] ,axis=1)
submissions.to_csv(fname, index=False)
print("'{}' is ready to submit." .format(fname))


# ## End
