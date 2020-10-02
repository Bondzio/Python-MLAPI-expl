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


df=pd.read_csv("/kaggle/input/insurance-premium-prediction/insurance.csv")


# In[ ]:


df.head(5)


# In[ ]:


#to find if data is having null values
df.isnull().any()


# In[ ]:


#to find if data is having any duplicate values
df.duplicated().sum()


# In[ ]:


#dropping duplicated values
df.drop_duplicates(inplace=True)


# In[ ]:


df.duplicated().sum()


# In[ ]:


df.shape


# In[ ]:


df.info()


# In[ ]:


# we have 3 categorical variables, sex, smoker and region,
# sex and smoker can be label encoded. since thr are only 2 possibility for each
df['sex'].value_counts()


# In[ ]:


df['smoker'].value_counts()


# In[ ]:


#label encoding sex and smoker columns
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
df[['sex','smoker']]=df[['sex','smoker']].apply(le.fit_transform)


# In[ ]:


df.head(5)


# In[ ]:


#Since region is having 4 different values we can one hot encode region
dummy=pd.get_dummies(df['region'])


# In[ ]:


dummy.head(5)


# In[ ]:


#In order to fall into dummy trap we will remove a variable southwest, we can do it all together after concatinating with original set
df=pd.concat((df,dummy),axis=1)


# In[ ]:


df.head(5)


# In[ ]:


#dropping region and south west region
df=df.drop(['region','southwest'],axis=1)


# In[ ]:


df.head(5)


# In[ ]:


#now we have all numerical data, we shaal see how each variable is effecting expenses 
import seaborn as sb
import matplotlib.pyplot as plt
sb.scatterplot(x="age",y="expenses",hue='smoker',data=df)

From above scatter chart it is clear that smokers are having high expenses.This feature is significant
# In[ ]:


sb.scatterplot(x="age",y="expenses",hue='bmi',data=df)

It is likely that ppl with high bmi are having most expenses as well
# In[ ]:


sb.scatterplot(x="age",y="expenses",hue='children',data=df)


# In[ ]:


# Finding if their is any relation b/w region and expenses
print(df.groupby('northeast')['expenses'].mean())
print(df.groupby('northwest')['expenses'].mean())
print(df.groupby('southeast')['expenses'].mean())


# We will consider only with 1. We can see that people in southeast region are spending more on an average of 14,735 followed by northeast and northwest

# In[ ]:


df.head(5)


# In[ ]:


#We can scale down the data but since sklearn Linear Regression can handle we car directly going to use it
from sklearn.model_selection import train_test_split
x=df[['age','sex','bmi','children','smoker','northeast','northwest','southeast']]
y=df['expenses']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)


# In[ ]:


print("Size of x_train : {}".format(x_train.shape))
print("Size of x_train : {}".format(x_test.shape))
print("Size of y_train : {}".format(y_train.shape))
print("Size of y_test : {}".format(y_test.shape))


# In[ ]:


from sklearn.linear_model import LinearRegression
le=LinearRegression()
le.fit(x_train,y_train)


# In[ ]:


#predicting using x_test data
y_pred=le.predict(x_test)


# In[ ]:


#we can get accuracy/score of the predicted model
le.score(x_test,y_test)


# In[ ]:


#r2 or accuracy of the model
from sklearn.metrics import r2_score
acc=r2_score(y_test,y_pred)
print("Accuracy of the model is : {}".format(acc))

