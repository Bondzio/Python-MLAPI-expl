#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


dataset=pd.read_csv("../input/churn-predictions-personal/Churn_Predictions.csv")


# In[ ]:


dataset.head(5)


# In[ ]:


import seaborn as sns
sns.pairplot(dataset)


# In[ ]:


sns.catplot(x="IsActiveMember", y="Balance", col="Exited",
                data=dataset, kind="box",height=4, aspect=.7,hue="NumOfProducts")


# **Drop unnecessary columns**

# In[ ]:


X = dataset.drop(["RowNumber","CustomerId","Surname","Exited"], axis=1)


# In[ ]:


X.head(5)


# Encoding the Gender column

# In[ ]:


from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
X["Gender"]= le.fit_transform(X["Gender"])


# One Hot encoding the Geography column 

# In[ ]:


from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder',OneHotEncoder(),[1])], remainder="passthrough")
X=np.array(ct.fit_transform(X))


# In[ ]:


y= dataset[("Exited")]
y.head(5)


# In[ ]:


y=y.values.reshape(-1,1)


# **Feature Scaling**

# In[ ]:


from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_scaled = sc.fit_transform(X)


# **Splitting the dataset into train and test**

# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X_scaled,y,test_size=0.2,random_state=0)


# **Build the ANN Model**

# In[ ]:


import tensorflow.keras
from keras.models import Sequential
from keras.layers import Dense


# In[ ]:


# Initiate the sequential model
model = Sequential()
# add input layers
model.add(Dense(units=25,activation="relu"))
model.add(Dense(units=25,activation="relu"))
model.add(Dense(units=1,activation="sigmoid"))


# In[ ]:


model.compile(optimizer="adam",loss="binary_crossentropy", metrics=['accuracy'])


# In[ ]:


epochs_hist= model.fit(X_train,y_train,epochs=100,batch_size=25)


# In[ ]:


epochs_hist.history.keys()


# In[ ]:


import matplotlib.pyplot as plt
plt.plot(epochs_hist.history["loss"])
plt.title('Model Loss Progression During Training')
plt.ylabel('Training Loss')
plt.xlabel('Epoch Number')
plt.legend(['Training Loss'])


# In[ ]:


plt.plot(epochs_hist.history["accuracy"])
plt.title('Model Accuracy plot')
plt.ylabel('Accuracy')
plt.xlabel('Epoch Number')
plt.legend(['Training Accuracy'])


# In[ ]:


y_pred=model.predict(X_test)


# In[ ]:


y_pred


# In[ ]:


# Converting y_pred to binary
y_pred = (y_pred > 0.5)


# In[ ]:


from sklearn.metrics import confusion_matrix,accuracy_score

cm=confusion_matrix(y_pred,y_test)
print(cm)


# In[ ]:


accuracy_score(y_pred,y_test)

