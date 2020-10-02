#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


# reading the data into a dataframe
df=pd.read_csv('../input/insurance/insurance.csv')
df.head()


# In[ ]:


# looking into the dataframe for any missing values , getting an idea about the different data types
df.info()

# As can be seen there are no missing columns , also sex, smoker and region are categorical varibales


# In[ ]:


df.describe()


# We have two choices we can spend some time cleaning our data ie. converting the categorical variables into
# numeric values using Label Encoder , get_dummies , to_categorical or other methods but
# instead we will take a new approach and try to build a working model ASAP and then spend some time fine tuning the model and we will see if Data preprocessing gives us any better results

# In[ ]:


# lets take a look at our dataset
df.shape
# our dataset has 1338 rows and 7 cols 


# In[ ]:


# lets look at some random rows in our dataset
df.sample(6)


# In[ ]:


# our target feature/columns is charges ( the columns we want our model to predict)
y=df.charges.to_frame()
y


# In[ ]:


# let's separate our remaining data and get in our x variable ( kind of convention for better readability)
x=df.iloc[:,:-1]
x


# In[ ]:


from xgboost import XGBRegressor

# we will use xgbregressor which a boosting approach ( which will disucss later )


# In[ ]:


# let's split our data into train and test sets 
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.2,random_state=2)


# In[ ]:


# let's create our model now which is fairly simple one line code
model=XGBRegressor(reg_aplha=.5)
# our model is created ( with default parameters , you can check my other 
#notebooks if you want to learn more about these parameters)


# In[ ]:


# now remember our data has categorical variables so let's convert them to numeric 
from sklearn.preprocessing import LabelEncoder

#let's look at categorical varibales one by one

df.sex.value_counts()

# there are only different values for sex so label Encoder can be used ( if there are more than 15 different values
# for the categorical column then we should not use label Encoder)


# In[ ]:


# let's create an instance of our labelEncoder 
encoder=LabelEncoder()
# fit the encoder to the train and test data for feature sex
x_train.sex=encoder.fit_transform(x_train.sex)
x_test.sex=encoder.transform(x_test.sex)


# In[ ]:


# As you can see the sex column now has numberic value 0/1
x_train


# In[ ]:


# lets apply the same procedure to smoker and region features 
# lets use get_dummies this time

x_train.smoker=pd.get_dummies(x_train.smoker,drop_first=True)
x_test.smoker=pd.get_dummies(x_test.smoker,drop_first=True)
x_train

# we get similar result from get_dummies function (be careful of the dummy trap but let's leave that for another day  )


# In[ ]:


# let's encode region using LabelEncoder again , we can use get dummies as well 
encoder1=LabelEncoder()
x_train.region=encoder1.fit_transform(x_train.region)
x_test.region=encoder1.transform(x_test.region)
x_test


# In[ ]:


# now that all are columns / features are in numeric let's try and fit our model 
model.fit(x_train,y_train)
# the model has default paramters for now


# In[ ]:


# let's check our training accuracy 
model.score(x_train,y_train)


# In[ ]:


# model has training accuracy of 99% 
# let's see how our model does on test data 

model.score(x_test,y_test)


# # That a simple machine learning model for a simple dataset with not many feature and a small number of records.
# 
# # If you are intrested in optimizing this model to increase it's test accuracy plz check my other notebook,
