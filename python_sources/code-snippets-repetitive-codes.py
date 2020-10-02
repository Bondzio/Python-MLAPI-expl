#!/usr/bin/env python
# coding: utf-8

# # some of the most needed code snippets 
# I'm will put some usefull and most repetitive code snippets in this notebook.<br>
# feel free to fork this notebook and complete it:)

# In[ ]:


import numpy as np 
import pandas as pd


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# <font color='red'>you can skip this part of the notebook. it's only for creating some dummy data</font>

# In[ ]:


# creating a sample csv file 
size = 150
y = np.random.choice(['L1', 'L2', 'L3'], size=size, p=[0.1, 0.6, 0.3]) # labels for our dummy data
cat1 = np.random.choice(['a','b','c','d', np.nan], size=size, p=[0.2,0.1,0.2,0.45, 0.05])
cat2 = np.random.choice([0,1, np.nan], size=size, p=[0.5,0.45, 0.05])

df = pd.DataFrame({'x1': np.random.randn(size), 'x2' : np.random.randn(size),'cat1': cat1, 'cat2':cat2, 'y': y})

df.to_csv('sample.csv', index=False)


# # Reading Dataset

# ### CSV File

# In[ ]:


csv_path = 'sample.csv'
df = pd.read_csv(csv_path)
df.head()


# ### opening Image Files from Zip
# 
# not recommended for large image datasets

# In[ ]:


zip_file_path = 'zip.zip' # or 'your_npz.npz'
# uncomment the line below
# images = np.load(zip_file_path) 


# ### Extracting Zip file

# In[ ]:


import zipfile
# uncomment the folowing lines
# with zipfile.ZipFile(zip_file_path) as z:
#     z.extractall()


# # Visualization

# In[ ]:


import seaborn as sns
from matplotlib import pyplot as plt

# set the figure sizes
plt.figure(figsize=(10,5))
sns.set(rc={'figure.figsize':(10,5)})


# ### histogram

# In[ ]:


sns.distplot(df['x1'])


# ### bar chart
# for label y

# In[ ]:


sns.countplot(df.y)


# ### boxplot

# In[ ]:


sns.boxplot(df.x2, df.y)


# ### pie chart

# In[ ]:


labels, counts = np.unique(df.y,return_counts=True)
plt.pie(counts, labels=labels)


# # Preprocessing

# In[ ]:


from sklearn import preprocessing


# ## Handling <font color='blue'> Nan</font> Vaules

# In[ ]:


from sklearn.impute import SimpleImputer
# here I changed the missing value to 'nan' but most of the times default is good
imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent') 
df[['cat1', 'cat2']] = imputer.fit_transform(df[['cat1','cat2']])


# <font color='red'>Note: if your feature is 1-D array you shall use reshape(1,-1) before using it with imputer</font>

# ## Normalizing

# ### MinMax

# In[ ]:


minmax = preprocessing.MinMaxScaler((0,1))
df[['x1','x2']] = minmax.fit_transform(df[['x1','x2']])
df.head()


# ### Label Encoder

# In[ ]:


categorical_features = df.select_dtypes('object').columns


le = preprocessing.LabelEncoder()
for col in categorical_features:
    df[col] = le.fit_transform(df[col])
    
df.head()


# ### One Hot Encoder

# In[ ]:


# adding another dummy categorical feature
gender = np.random.choice(['Male', 'Female', 'another'], size=size, p=[0.4, 0.4, 0.2])
df['gender'] = gender


# In[ ]:


from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(handle_unknown='ignore', sparse=False)


oht = pd.DataFrame(ohe.fit_transform(df[['gender']]))

oht.index = df.index

num_df = df.drop(['gender'], axis=1)

df = pd.concat([num_df, oht],axis=1)


# ## Train-Test Split

# In[ ]:


from sklearn.model_selection import train_test_split

y = df.y
X = df.drop(['y'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print('train shape: {}\ntest shape: {}'.format(X_train.shape, X_test.shape))


# # Baseline Models

# In[ ]:


# using mean squared error
from sklearn.metrics import mean_squared_error

def calculate_error(y_pred, y_true):
    print(mean_squared_error(y_pred, y_true))


# ## Linear Models

# ### RidgeClassifier

# In[ ]:


from sklearn.linear_model import RidgeClassifier

model = RidgeClassifier(random_state=0)
model.fit(X_train, y_train)
preds = model.predict(X_test)
calculate_error(preds, y_test)


# ### SGDClassifier

# In[ ]:


from sklearn.linear_model import SGDClassifier

model = SGDClassifier(random_state=0)
model.fit(X_train, y_train)
preds = model.predict(X_test)
calculate_error(preds, y_test)


# ## Ensemble

# ### Random forrest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=0)
model.fit(X_train, y_train)
preds = model.predict(X_test)
calculate_error(preds, y_test)


# ### AdaBoost

# In[ ]:


from sklearn.ensemble import AdaBoostClassifier

model = AdaBoostClassifier(random_state=0)
model.fit(X_train, y_train)
preds = model.predict(X_test)
calculate_error(preds, y_test)


# ### GradientBoosting

# In[ ]:


from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(random_state=0)
model.fit(X_train, y_train)
preds = model.predict(X_test)
calculate_error(preds, y_test)


# ## Decision Tree

# In[ ]:


from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_leaf_nodes=200, random_state=0)
model.fit(X_train, y_train)
preds = model.predict(X_test)
calculate_error(preds, y_test)


# # create submission csv

# In[ ]:


def save_submission(test_path, preds, path='submission.csv'):    
    '''
    test_path: test csv file
    preds    : predicted label from your model
    path     : where you want to save the csv file
    '''
    test_df = pd.read_csv(test_path)
    test_df['label_column'] = preds
    test_df.to_csv(path, index=False)

