#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


train = pd.read_csv("/kaggle/input/eval-lab-1-f464-v2/train.csv")
test = pd.read_csv("/kaggle/input/eval-lab-1-f464-v2/test.csv")
test.head()
missing_count = test.isnull().sum()
missing_count[missing_count>0].sort_index()

test.fillna(value=test.mean(),inplace=True)
test = pd.get_dummies(test,columns=['type'],drop_first = True)
test.head()
y1 = test.drop(['id'],axis = 1)
y1


# In[ ]:


train.head()


# In[ ]:


plt.style.use(style = 'ggplot')
plt.rcParams['figure.figsize'] = (10,6)


# In[ ]:


train.rating.describe()


# In[ ]:


plt.hist(train.rating,color = 'red')
plt.show()


# In[ ]:


numeric_features = train.select_dtypes(include=[np.number])
corr = numeric_features.corr()
corr['feature11'].sort_values(ascending= False)


# In[ ]:


tg = np.log(train.id)
plt.scatter(x = train['feature2'],y = tg)


# In[ ]:


train.feature1.describe()


# In[ ]:


missing_count = train.isnull().sum()
missing_count[missing_count>0].sort_index()


# In[ ]:


train[train['feature10'].isnull()]
train.dtypes
train.head()


# In[ ]:


train['type'].describe()


# In[ ]:


train.fillna(value=train.mean(),inplace=True)


# In[ ]:


sns.distplot(train['feature4'],kde = False)


# In[ ]:


tr1 = train.copy()


# In[ ]:


train = pd.get_dummies(train,columns=['type'],drop_first = True)


# In[ ]:


train.type_old.dtype


# In[ ]:


X = train.drop(['id','rating'],axis = 1)
y = train.rating
X.head()
y.head()


# In[ ]:


from sklearn.model_selection import train_test_split

X_train,X_val,y_train,y_val = train_test_split(X,y,test_size=0.33,random_state=42)
X_val


# In[ ]:


from sklearn.linear_model import LinearRegression
from sklearn import linear_model
# clf = linear_model.SGDRegressor()

reg_lr = LinearRegression().fit(X_train,y_train)
# reg_lr = clf.fit(X_train,y_train)


# print(reg_lr.score(X_val, y_val))


# In[ ]:


from sklearn.metrics import mean_squared_error
from math import sqrt
predictions = reg_lr.predict(X_val)
predictions = np.ceil(predictions)
predictions = predictions.astype(int)
print(predictions)
print(sqrt(mean_squared_error(y_val,predictions)))


# In[ ]:


print(reg_lr.predict(X_val))


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 160,leaf_size=5,algorithm='auto',n_jobs=-1,p=30,weights='distance',metric = 'euclidean')
knn.fit(X_train,y_train)
predictions = knn.predict(X_val)
print(sqrt(mean_squared_error(y_val,predictions)))
print(predictions)


# In[ ]:


pred = knn.predict(y1)
#y1['rating'] = pred
y1.shape


# In[ ]:


pred


# In[ ]:


y1.head()
x11 = pd.read_csv("/kaggle/input/eval-lab-1-f464-v2/test.csv")
y1['id'] = x11['id']
y1['rating'] = pred


# In[ ]:


y1.head()


# In[ ]:


cols = ['feature1']
y1.drop(y1.cols,inplace = True)
y1.head(15)
(y1.columns.values)


# In[ ]:


y1.shape


# In[ ]:


newdf = y1.drop(['feature1'], axis=1)
newdf


# In[ ]:


y1


# In[ ]:


newdf['rating']  = y1['rating'] 


# In[ ]:


y1.drop(['rating'], axis=1,inplace=True)


# In[ ]:


y1['rating'] = newdf['rating']


# In[ ]:


y1.drop(['feature1'], axis=1,inplace=True)


# In[ ]:


y1


# In[ ]:


y1.to_csv("ans1.csv",index=False)

