#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import sklearn


# In[ ]:


df=pd.read_csv(r"C:\Users\SHIVANSH SINGH\Downloads\USA_cars_datasets.csv")


# In[ ]:


df.head()


# In[ ]:


df=df.drop(columns=["model","color","vin","lot","state","country","condition"],axis=1)


# In[ ]:


df=df.drop(columns=["Unnamed: 0"])


# In[ ]:


df.head()


# In[ ]:


df.title_status.value_counts().plot(kind="bar")


# In[ ]:



pd.get_dummies(df.title_status)


# In[ ]:


df["brand"].value_counts()
#df.brand.value_counts().plot(kind="bar")


# In[ ]:


dict={"audi":"neo","maserati":"neo","ram":"neo","harley-davidson":"neo", "toyota":"neo" ,"lexus":"neo" ,"acura":"neo" ,"lincoln":"neo", "mazda":"neo", "heartland":"neo", "peterbilt":"neo","land":"neo"}
df=df.replace({"brand":dict})


# In[ ]:


df


# In[ ]:


df=pd.get_dummies(df,columns=['brand','title_status'])
df


# In[ ]:


df.drop(columns=["brand_nissan","title_status_salvage insurance"])


# In[ ]:


df


# In[ ]:


x=df.iloc[:,1:].values
y=df.iloc[:,[0]].values


# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.05)



# In[ ]:


from sklearn import linear_model
regr = linear_model.LinearRegression()
regr.fit(x_train, y_train)

y_predict=regr.predict(x_test)
len(y_predict)


# In[ ]:


from sklearn.metrics import r2_score
r2_score(y_test,y_predict)


# In[ ]:


from sklearn import svm


# In[ ]:


svr=svm.SVR(gamma='auto')
svr.fit(x_train, y_train.ravel())


# In[ ]:


y_predict=svr.predict(x_test)


# In[ ]:


y_predict.shape


# In[ ]:


r2_score(y_test,y_predict)


# In[ ]:


from sklearn import tree

clf = tree.DecisionTreeRegressor()
clf = clf.fit(x_train,y_train)
r2_score(clf.predict(x_test),y_test)


# In[ ]:




