#!/usr/bin/env python
# coding: utf-8

# In[2]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[4]:


#Import the dataset
df = pd.read_csv("../input/data.csv")


# In[6]:


#Lets check the dataset
df.info()


# In[7]:


#Lets check the null value of the dataset
df.isnull().sum()


# In[8]:


#There's an additional column 'unnamed' with no data. delete as well
df.drop('Unnamed: 32',axis=1,inplace=True)


# In[10]:


#Lets check the statistical inference of the dataset
df.describe()


# In[12]:


#Visualising the Data
#Check the Radius mean first
import matplotlib.pyplot as plt
import seaborn as sns
plt.hist(df.radius_mean, 10, facecolor='red', alpha=0.5, label="radius_mean")
plt.subplots_adjust(left=0, right=1, bottom=0, top=0.5, hspace=0.05, wspace=1)
plt.xlabel('radius mean')
plt.ylabel('Frequency')
plt.title('Distribution of radius mean')
plt.show()


# In[14]:



#Lets check the correlation and heat map
corr = df.corr()
colormap = sns.diverging_palette(220, 10, as_cmap = True)
plt.figure(figsize = (20,18))
sns.heatmap(corr,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values,
            annot=True,fmt='.2f',linewidths=0.30,
            cmap = colormap, linecolor='white')
plt.title('Correlation of df Features', y = 1.05, size=15)


# In[16]:


#Lets create the ML model
#Lets take our matrix of features 
x = df.iloc[:, 2:32].values


# In[18]:


#Lets check the diagnosis column, which is our target variable
sns.countplot(df['diagnosis'],label="Count")
y = df.iloc[:,1].values


# In[19]:


# Encoding the Categorical data (For Malignant: M =1, Benign: B = 0)
from sklearn.preprocessing import LabelEncoder
labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)


# In[20]:


#Spliting the dataset into training set and test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)


# In[21]:


#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)


# In[22]:


#Importing the Libraries for ANN
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout


# In[23]:


#Initilasing the ANN
classifier = Sequential()


# In[24]:


# Adding the input layer and 1st hidden layers
classifier.add(Dense(units = 16, kernel_initializer = 'uniform', activation ='relu', input_dim = 30))
classifier.add(Dropout(p = 0.1))


# In[25]:


# Adding 2nd hidden layers
classifier.add(Dense(units = 16, kernel_initializer = 'uniform', activation ='relu'))
classifier.add(Dropout(p = 0.1))


# In[26]:


# Adding 3rd hidden layers
classifier.add(Dense(units = 16, kernel_initializer = 'uniform', activation ='relu'))
classifier.add(Dropout(p = 0.1))


# In[27]:


#Adding output layers
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation ='sigmoid'))


# In[28]:


#Compile the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


# In[29]:


#Fitting ANN to the Traning set
classifier.fit(x_train, y_train, batch_size = 10, epochs = 200)


# In[30]:


#Evaluted the Classifier
score = classifier.evaluate(x_test, y_test,verbose=1)
print(score)


# In[31]:


#Predicting the Test set result
y_pred = classifier.predict(x_test)
y_pred = (y_pred > 0.5)


# In[32]:


#Making the Confusion Matrix, and Accuracy Score
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
print(cm)
print("Accuracy = ", accuracy)


# In[ ]:




