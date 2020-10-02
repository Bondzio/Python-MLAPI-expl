#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


df=pd.read_csv('/kaggle/input/eval-lab-1-f464-v2/train.csv')


# In[ ]:


missing_count=df.isnull().sum(axis = 0)
missing_count[missing_count>0]


# In[ ]:


df['feature3'].fillna(value=df['feature3'].mean(),inplace=True)


# In[ ]:


df['feature4'].fillna(value=df['feature4'].mean(),inplace=True)
df['feature5'].fillna(value=df['feature5'].mean(),inplace=True)
df['feature8'].fillna(value=df['feature8'].mean(),inplace=True)
df['feature9'].fillna(value=df['feature9'].mean(),inplace=True)
df['feature10'].fillna(value=df['feature10'].mean(),inplace=True)
df['feature11'].fillna(value=df['feature11'].mean(),inplace=True)


# In[ ]:


missing_count=df.isnull().sum(axis = 0)
missing_count[missing_count>0]


# In[ ]:


one_hot=pd.get_dummies(df['type'])
df = df.drop('type',axis = 1)
df = df.join(one_hot)
df.head()


# In[ ]:


X=df.copy()
X.drop(columns=['rating','old'],inplace=True)
# X=df[['feature3','feature5','feature6','feature7','new','old']]
y=df['rating']
X.head()


# In[ ]:


fd=pd.read_csv('/kaggle/input/eval-lab-1-f464-v2/test.csv')
fd['feature3'].fillna(value=fd['feature3'].mean(),inplace=True)
fd['feature4'].fillna(value=fd['feature4'].mean(),inplace=True)
fd['feature5'].fillna(value=fd['feature5'].mean(),inplace=True)
fd['feature8'].fillna(value=fd['feature8'].mean(),inplace=True)
fd['feature9'].fillna(value=fd['feature9'].mean(),inplace=True)
fd['feature10'].fillna(value=fd['feature10'].mean(),inplace=True)
fd['feature11'].fillna(value=fd['feature11'].mean(),inplace=True)
one_hot=pd.get_dummies(fd['type'])
fd = fd.drop('type',axis = 1)
fd = fd.join(one_hot)
X_val=fd.copy()
X_val.drop(columns=['old'],inplace=True)
X_val.head()


# In[ ]:





# In[ ]:





# In[ ]:


from sklearn.ensemble import ExtraTreesRegressor
xt = ExtraTreesRegressor(n_estimators=2500,n_jobs=-1)
xt.fit(X,y)


# In[ ]:


predicted_val=xt.predict(X_val)
predicted_val=np.rint(predicted_val)
unique, counts = np.unique(predicted_val, return_counts=True)
np.asarray((unique, counts)).T


# In[ ]:


submission = pd.DataFrame({'id':fd['id'],'rating':predicted_val})
submission.head()


# In[ ]:


filename = 'submission.csv'

submission.to_csv(filename,index=False)

print('Saved file: ' + filename)


# In[ ]:


#second code


# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


df=pd.read_csv('/kaggle/input/eval-lab-1-f464-v2/train.csv')


# In[ ]:


missing_count=df.isnull().sum(axis = 0)
missing_count[missing_count>0]


# In[ ]:


df['feature3'].fillna(value=df['feature3'].mean(),inplace=True)
df['feature4'].fillna(value=df['feature4'].mean(),inplace=True)
df['feature5'].fillna(value=df['feature5'].mean(),inplace=True)
df['feature8'].fillna(value=df['feature8'].mean(),inplace=True)
df['feature9'].fillna(value=df['feature9'].mean(),inplace=True)
df['feature10'].fillna(value=df['feature10'].mean(),inplace=True)
df['feature11'].fillna(value=df['feature11'].mean(),inplace=True)


# In[ ]:


one_hot=pd.get_dummies(df['type'])
df = df.drop('type',axis = 1)
df = df.join(one_hot)
df.head()


# In[ ]:


X=df.copy()
X.drop(columns=['id','rating','old'],inplace=True)
# X=df[['feature3','feature5','feature6','feature7','new','old']]
y=df['rating']
X.head()


# In[ ]:


fd=pd.read_csv('/kaggle/input/eval-lab-1-f464-v2/test.csv')
fd['feature3'].fillna(value=fd['feature3'].mean(),inplace=True)
fd['feature4'].fillna(value=fd['feature4'].mean(),inplace=True)
fd['feature5'].fillna(value=fd['feature5'].mean(),inplace=True)
fd['feature8'].fillna(value=fd['feature8'].mean(),inplace=True)
fd['feature9'].fillna(value=fd['feature9'].mean(),inplace=True)
fd['feature10'].fillna(value=fd['feature10'].mean(),inplace=True)
fd['feature11'].fillna(value=fd['feature11'].mean(),inplace=True)
one_hot=pd.get_dummies(fd['type'])
fd = fd.drop('type',axis = 1)
fd = fd.join(one_hot)
X_val=fd.copy()
X_val.drop(columns=['id','old'],inplace=True)
X_val.head()


# In[ ]:


from sklearn.ensemble import ExtraTreesRegressor
xt = ExtraTreesRegressor(n_estimators=2500,n_jobs=-1)
xt.fit(X,y)


# In[ ]:


predicted_val=xt.predict(X_val)
predicted_val=np.rint(predicted_val)
unique, counts = np.unique(predicted_val, return_counts=True)
np.asarray((unique, counts)).T


# In[ ]:


submission = pd.DataFrame({'id':fd['id'],'rating':predicted_val})
submission.head()


# In[ ]:


filename = 'submission.csv'

submission.to_csv(filename,index=False)

print('Saved file: ' + filename)

