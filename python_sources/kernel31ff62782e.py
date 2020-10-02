#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


data = pd.read_csv('/kaggle/input/ufcdata/preprocessed_data.csv')
raw = pd.read_csv('/kaggle/input/ufcdata/data.csv')


# In[ ]:


data.head()


# In[ ]:


raw.head()


# In[ ]:


raw.describe()


# In[ ]:


data.describe()


# In[ ]:


data_num = data.select_dtypes(include=[np.float, np.int])

scaler = StandardScaler()
data[list(data_num.columns)] = scaler.fit_transform(data[list(data_num.columns)])


# In[ ]:


y = data['Winner']
X = data.drop(columns = 'Winner')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)


# In[ ]:


model = SVC()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
# evaluate predictions
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

