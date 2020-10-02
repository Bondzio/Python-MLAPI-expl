#!/usr/bin/env python
# coding: utf-8

# This is the version using Keras to learn and predict the result, for data analysis, pls. refer to another version:
# 
# [https://www.kaggle.com/sunixliu/bank-customer-churn-model](http://)

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


#Load all data in
all_data = pd.read_csv("../input/Churn_Modelling.csv")


# In[3]:


#One-encoding Gender, Geography and NumOfProducts
dummy_gender = pd.get_dummies(all_data['Gender'], prefix='Gender')
dummy_geo = pd.get_dummies(all_data['Geography'],prefix = 'Geo')
dummy_NoOfProducts=pd.get_dummies(all_data['NumOfProducts'],prefix='NOP')


# In[4]:


#Dealing with Age,catogorized it into 7 sections
bins = [18,22,34,40,60,80,100]
labels = ['18-22','23-34','35-40','41-60','61-80','81-100']
dummy_age_labels=pd.cut(all_data['Age'],bins,labels=labels,right=False)


# In[5]:


all_data['Age_labeled']= dummy_age_labels


# In[6]:


dummy_age=pd.get_dummies(all_data['Age_labeled'],prefix='Age')


# In[7]:


# Dealing with creditscore, catogorizing it into 5 catogories
bins =[300,579,669,739,799,850]
labels =['Very Poor','Fair','Good','Very Good','Exceptional']
dummy_crdscore_labels=pd.cut(all_data['CreditScore'],bins,labels=labels)
all_data['CreditScore_labled']= dummy_crdscore_labels
dummy_creditscore = pd.get_dummies(all_data['CreditScore_labled'], prefix = 'CreditLevel')


# In[8]:


#Tenure catogorized into 4 sections
bins = [0,1,5,8,11]
labels = ['0-1','1-5','5-8','8-11']
dummy_tenure_labels=pd.cut(all_data['Tenure'],bins,labels=labels,right=False)
all_data['Tenure_labeled']= dummy_tenure_labels
dummy_tenure = pd.get_dummies(all_data['Tenure_labeled'],prefix = 'Tenure')


# In[9]:


# Get Balance and EstimatedSalary standard
from sklearn.preprocessing import StandardScaler
all_data['Balance'] = StandardScaler().fit_transform(all_data.filter(['Balance']))
all_data['EstimatedSalary'] = StandardScaler().fit_transform(all_data.filter(['EstimatedSalary']))


# In[10]:


data_combined = pd.concat([all_data,dummy_age,dummy_tenure,dummy_creditscore,dummy_geo,dummy_gender,dummy_NoOfProducts],axis =1)


# In[11]:


data_combined.drop(['Gender', 'Age', 'CreditScore','Geography','NumOfProducts','Tenure'], axis=1, inplace=True)


# In[12]:


data_combined.drop(['Surname','CustomerId','Age_labeled','CreditScore_labled','Tenure_labeled'],
                   axis=1,inplace = True)


# In[13]:


y_data=data_combined['Exited']
data_combined.drop(['Exited'],axis=1, inplace = True)
X_data = data_combined

X_data.set_index('RowNumber')
X_data.reset_index(drop = True, inplace = True)
X_data.drop('RowNumber',axis =1, inplace = True)


# In[14]:


#split data into train and test dataset
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(X_data,y_data,test_size=0.2,random_state=2)


# In[15]:


import tensorflow as tf

model = tf.keras.models.Sequential()


# In[16]:


model.add(tf.keras.layers.Dense(units = 128,
                                input_dim = 28, #totally 28 features as input
                                use_bias = True,
                                kernel_initializer ='uniform',
                                activation ='relu',
                                bias_initializer ='zeros'
                                ))
#add 2 hidden layers
for i in range(0,2):
    model.add(tf.keras.layers.Dense(units=128, kernel_initializer='normal',
                     bias_initializer='zeros',activation='relu'))
    model.add(tf.keras.layers.Dropout(.40)) # dropout some data to avoid overfitting


#output layer
model.add(tf.keras.layers.Dense(units =2,
                               activation ='softmax'))


# In[17]:


optimizer = tf.keras.optimizers.Adam(0.00001) #use Adam as optimizer and the learning rate is 0.00001
loss_function = "sparse_categorical_crossentropy"

model.compile(optimizer = optimizer, loss = loss_function, metrics=['accuracy'])


# In[18]:


model.summary()


# In[19]:


train_history = model.fit(x = x_train,
                          y = y_train,
                          validation_split = 0.2, #use 20% of train data as validation data
                          epochs = 200,
                          batch_size = 50,
                          verbose =1
                         )    


# In[20]:


def v_train_history(trainhist, train_metrics, valid_metrics):
    plt.plot(trainhist.history[train_metrics])
    plt.plot(trainhist.history[valid_metrics])
    plt.title('Training metrics')
    plt.ylabel(train_metrics)
    plt.xlabel('Epochs')
    plt.legend(['train','validation'],loc='upper left')
    plt.show()


# In[21]:


v_train_history(train_history,'acc','val_acc')


# In[22]:


v_train_history(train_history,'loss','val_loss')


# In[23]:


evaluate_result = model.evaluate(x=x_test,
                               y=y_test)


# In[ ]:




