#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


train_data = pd.read_csv("/kaggle/input/santander-customer-transaction-prediction/train.csv")
test_data = pd.read_csv("/kaggle/input/santander-customer-transaction-prediction/test.csv")
train_data.head()


# In[ ]:


test_data.head()


# In[ ]:


from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# In[ ]:


train_data.isnull().any().sum()


# In[ ]:


from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

scaled = StandardScaler()

X = train_data.iloc[:,2:]

y = train_data.iloc[:,1]
                      
X = scaled.fit_transform(X)
                      
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)


# In[ ]:


final_test = test_data.iloc[:,1:]
final_label = test_data.iloc[:,0]


# In[ ]:


final_test = scaled.fit_transform(final_test)


# In[ ]:


#from sklearn.decomposition import PCA
#pca  = PCA(n_components=6)

#pca.fit(X)
#pca_samples = pca.transform(X) 


# In[ ]:


#principal_df = pd.DataFrame(data = pca_samples)


# In[ ]:


#principal_df.tail()


# In[ ]:


#print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_.cumsum()))


# In[ ]:


from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
gb_model = GaussianNB()
gb_model.fit(X_train,y_train)

y_pred = gb_model.predict_proba(X_test)[:,1]

#print('Accuracy:',accuracy_score(y_test,y_pred))


# In[ ]:


y_pred


# In[ ]:


final_pred = gb_model.predict_proba(final_test)[:,1]

submission = pd.DataFrame({'ID_code': final_label,'target':final_pred})

submission.to_csv("my_submission_gb.csv",index=False)


# In[ ]:


final_pred

