#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler  # for normalizing input vectors mean and variance


# In[7]:


# Read Data
train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')

print(train.shape)
print(test.shape)


# In[12]:


train_x = train.drop("label",axis=1)
train_y = train['label']

print(train_x.shape)
print(train_y.shape)

scaler = StandardScaler().fit(train_x)
print(len(scaler.mean_))

train_x_standard = scaler.transform(train_x.astype(float))

print(train_x_standard.shape)

test_x_standard = scaler.transform(test.astype(float))

print(test_x_standard.shape)


# In[4]:


# Multinomial Logistic Regression
model = LogisticRegression(multi_class='multinomial', penalty='l1', solver='saga', tol=0.0001)
model.fit(train_x_standard, train_y)


# In[5]:


test_y = model.predict(test_x_standard)

submission = pd.DataFrame({"ImageId": range(1, test_y.shape[0]+1), "label": test_y})
submission.to_csv("submission.csv", index=False)


# In[6]:


test_y[:10]

