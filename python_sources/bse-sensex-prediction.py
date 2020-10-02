#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import os
print(os.listdir("../input"))
df=pd.read_csv("../input/CSVForDate.csv",parse_dates=["Date"])
df.head()


# In[ ]:


#data columns
df.columns


# In[ ]:


#check for missing values
df.isnull().sum()


# In[ ]:


#lets see if date is a date time series
type(df.Date[0])


# In[ ]:


#lets make Date as index
df.set_index("Date",inplace=True)


# In[ ]:


df.index


# In[ ]:


df.head()


# In[ ]:


#lets see date for the month of January and february
df["2009-01":"2009-02"]


# In[ ]:


#lets see data of January only
df["2009-01"]


# In[ ]:


df.sort_index(inplace=True)
df_jan=df["2009-01"] #January data in sorted way


# In[ ]:


df_jan #january dataset created for see the trend in January


# In[ ]:


sns.distplot(df_jan["Open"])


# In[ ]:


#resmapling data on a monthly frequency with avg close price every month end
df.Close.resample("M").mean()


# In[ ]:


#plotting the above data to see the trend
plt.figure(figsize=(10,10))
plt.subplot(2,2,1)
df.Close.resample("M").mean().plot()
plt.subplot(2,2,2)
#lets plot data quarterly
df.Close.resample("Q").mean().plot()


# In[ ]:


plt.scatter(df["Open"],df["Close"],data=df)
plt.xlabel("Open price")
plt.ylabel("close Price")


# In[ ]:


sns.lineplot(df["Open"],df["Close"],data=df,color="r")


# Lets look at the datato predict the close point of the same 

# In[ ]:


df.head()


# In[ ]:


#feature correlation
df1=df[["Open","High","Low"]]
df1.corr()


# In[ ]:


#Data is highly correlated hence it will give us a bad model so use only 1 feature
X=df["Open"].values.reshape(-1,1)


# In[ ]:


#Label
y=df["Close"]


# In[ ]:


#train test and split
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.2,random_state=1)


# In[ ]:


#lets  do the feature scaling for an acurate model
#from sklearn.preprocessing import MinMaxScaler
#mm=MinMaxScaler()
#mm.fit(X_train,y_train)


# In[ ]:


from sklearn.linear_model import LinearRegression
lreg=LinearRegression()
lreg.fit(X_train,y_train)


# In[ ]:


y_pred=lreg.predict(X_test)
y_pred


# In[ ]:


sns.lineplot(y_test,y_pred)


# Score of the Linear regression model

# In[ ]:


lreg.score(X_test,y_test)  #this High score suspects overfitting of data

