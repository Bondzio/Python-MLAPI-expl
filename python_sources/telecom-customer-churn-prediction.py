#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ### Importing required libraries

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# ### Loading the dataset

# In[ ]:


df = pd.read_csv('/kaggle/input/telco-customer-churn/WA_Fn-UseC_-Telco-Customer-Churn.csv')
df.head()


# ### Exploratory Data Analysis (EDA)

# In[ ]:


df.shape


# In[ ]:


sns.heatmap(df.isnull())


# In[ ]:


df.dtypes


# ### Encoding Churn column with LabelEncoder

# In[ ]:


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df['Churn'] = le.fit_transform(df['Churn'])
df['Churn'].unique()


# ### Splitting the data set into training and testing data

# In[ ]:


df0 = df.drop(columns='Churn')
test = df['Churn']
df1 = pd.get_dummies(df0)
df2 = pd.concat([df0,df1], axis=1)

train = df2.drop(columns=['customerID','gender','Partner','Dependents','PhoneService','MultipleLines','InternetService',
                 'OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies',
                 'Contract','PaperlessBilling','PaymentMethod','TotalCharges'], axis=1)
print(train.shape)
print(test.shape)


# In[ ]:


from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(train,test, train_size=0.25, random_state=0)


# In[ ]:


print(x_train.shape)
print(x_test.shape)


# ### Applying Support Vector Machine (SVM) model

# In[ ]:


from sklearn.svm import SVC

model = SVC(C=0.1, gamma=0.001, kernel='rbf')
model.fit(x_train,y_train)


# ### Prediction using testing set

# In[ ]:


y_pred = model.predict(x_test)


# ### Evaluation

# In[ ]:


from sklearn import metrics

print('Accuracy Score:  ', metrics.accuracy_score(y_test,y_pred))
print('Confusion Matrix:  ', metrics.confusion_matrix(y_test,y_pred))


# ### Applying Random Forest Model

# In[ ]:


from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor()
rf.fit(x_train,y_train)


# In[ ]:


y_predrf = rf.predict(x_test).astype(int)


# In[ ]:


print('Accuracy Score:  ', metrics.accuracy_score(y_test,y_predrf))
print('Confusion Matrix:  ', metrics.confusion_matrix(y_test,y_predrf))


# ## Accuracy Score comparison

# In[ ]:


scores = [['Support Vector Machine', 78.23],['Random Forest', 75.18]]

acc_score = pd.DataFrame(scores, columns=['Algorithm','Accuracy Score'])

acc_score


# ### Hyperparameter tuning

# In[ ]:


from sklearn.model_selection import GridSearchCV

param_grid = {'kernel':['poly','rbf'],
              'C':[0.1,1,10],
              'gamma':[1,0.1,0.01,0.001,0.0001]}

grid = GridSearchCV(model,param_grid)
grid.fit(x_train,y_train)


# In[ ]:


grid.best_params_


# In[ ]:




