#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


df_train = pd.read_csv('/kaggle/input/ods-mlclass-dubai-2019-03-lecture3-hw/train.csv')
print(df_train.shape)

df_test = pd.read_csv('/kaggle/input/ods-mlclass-dubai-2019-03-lecture3-hw/test.csv')
print(df_test.shape)


# In[ ]:


df_train.head()


# In[ ]:


df_test['target'] = np.nan

df = pd.concat([df_train, df_test])

print(df.shape)


# In[ ]:


df.head()


# In[ ]:


df.tail()


# In[ ]:


df.dtypes


# In[ ]:


cats = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']

nums = ['age', 'fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']


# In[ ]:


import itertools as it


# In[ ]:


for i in range(1, 4):
    print(i)
    for g in it.combinations(cats, i):
        df = pd.concat(
            [
                df, 
                df.groupby(list(g))[nums].transform('mean').rename(
                    columns=dict([(s, ':'.join(g) + '__' + s + '__mean') for s in nums])
                )
            ], 
            axis=1
        )


# In[ ]:


df.drop(columns=cats, inplace=True)
df.shape


# In[ ]:


cols = [c for c in df.columns if c != 'uid' and c != 'target']


# In[ ]:


from sklearn.preprocessing import StandardScaler

df[cols] = StandardScaler().fit_transform(df[cols])


# In[ ]:


df_m = df[cols].corr()


# In[ ]:


cor = {}
for c in cols:
    cor[c] = set(df_m.loc[c][df_m.loc[c] > 0.5].index) - {c}
    
len(cor)


# In[ ]:


for c in cols:
    if c not in cor:
        continue
    for s in cor[c]:
        if s in cor:
            cor.pop(s)


# In[ ]:


cols = list(cor.keys())

len(cols)


# In[ ]:


cols


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier


# In[ ]:


model = KNeighborsClassifier(
    n_neighbors=100,
    weights='distance',
    algorithm='auto',
    leaf_size=30,
    p=2,
    metric='minkowski',
    n_jobs=-1
)

model = model.fit(df.loc[df['target'].notna()][cols], df.loc[df['target'].notna()]['target'])


# In[ ]:


p = model.predict_proba(df.loc[df['target'].isna()][cols])


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("dark")


# In[ ]:


sns.distplot(p[:, 1])


# In[ ]:


df_submit = pd.DataFrame({
    'uid': df.loc[df['target'].isna()]['uid'],
    'target': p[:, 1]
})


# In[ ]:


df_submit.to_csv('/kaggle/working/submit.csv', index=False)


# In[ ]:


get_ipython().system('head /kaggle/working/submit.csv')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




