#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC


# In[ ]:


df=pd.read_csv("/kaggle/input/eval-lab-1-f464-v2/train.csv")


df2=pd.read_csv("/kaggle/input/eval-lab-1-f464-v2/test.csv")


# In[ ]:


y_train=df['rating']
x_train=df.copy()

df.isnull().any()


# In[ ]:


x_train=x_train.drop(['rating','id','type'],axis=1)
x_train.fillna(x_train.mean(),inplace=True)


# In[ ]:


df2=df2.drop(['id'],axis=1)
x_test=df2.copy()


# In[ ]:



x_test.fillna(x_test.mean(),inplace=True)
x_test.drop(['type'],axis=1)


# In[ ]:


#from sklearn import preprocessing as pp


# In[ ]:


#normalizer=pp.Normalizer()
#x_train_norm=normalizer.fit_transform(x_train)


# In[ ]:



#x_train_new=pd.DataFrame(x_train_norm,columns=list(x_train.columns))

#normalizer2=pp.Normalizer()

#x_test_norm=normalizer2.fit_transform(x_test)
#x_test_new=pd.DataFrame(x_test_norm,columns=list(x_test.columns))
#x_test_new


# In[ ]:


#Y_pred=reg.predict(df2)
#x_train1=pd.concat([x_train1,(df['type'])])l
x_train1=x_train
x_train1["type"]=df["type"]
x_train1['type']=x_train1['type'].map({'new':1,'old':0})


x_test1=x_test
x_test1['type']=df2["type"]
x_test1['type']=x_test1['type'].map({'new':1,'old':0})

######################################################################################################################



# In[ ]:


clf=RandomForestClassifier(n_estimators=45,max_depth=14)
clf.fit(x_train1,y_train)


# In[ ]:


plt.plot(y_train,clf.predict(x_train1))


# In[ ]:


accuracy_score(y_train,clf.predict(x_train1))


# In[ ]:


y_actpredicted=clf.predict(x_test1)


# In[ ]:


test2=pd.read_csv("/kaggle/input/eval-lab-1-f464-v2/test.csv")


# In[ ]:


dfpd=pd.DataFrame({'id':test2['id'],'rating':y_actpredicted})


# In[ ]:


dfpd.to_csv("submission.csv",header=True,index=False)


# In[ ]:


dfpd.head()

