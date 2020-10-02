#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[3]:


ds_train = pd.read_csv('../input/train.csv')
ds_test = pd.read_csv('../input/test.csv')


# In[4]:


ds_train.head()


# In[5]:


ds_test.head()


# In[6]:


ds_train.describe()    # checking statistics of data like any outliers 


# In[7]:


ds_test.describe()


# In[8]:


ds_train.info()  # checking null values


# Clearly Embarked, Age and Cabin has Missing Values in train data

# In[9]:


ds_test.info()


# Clearly Age, Fare and Cabin has Missing Values in test data

# #### Finding correlations between features, How they are related to each other
# 

# In[10]:


# Correlation matrix - linear relation among independent attributes and with the Target attribute

sns.set(style="white")

# Compute the correlation matrix
correln = ds_train.corr()

# Generate a mask for the upper triangle
#mask = np.zeros_like(correln, dtype=np.bool)
#mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(correln,  cmap=cmap, vmax=.3, #mask=mask,
            linewidths=.5, cbar_kws={"shrink": .7})


# Fare has highest positive correlation with Survived follwed by Parch and Pclass displayed by color Dark red, light red and light blue

# In[12]:


# Parch and Sex Vs Survived

g = sns.FacetGrid(ds_train, col="Parch",  row="Sex", hue = 'Survived')
g = g.map(plt.hist, "Survived")


# In[13]:


# Passenger class and Sex Vs Survived

g = sns.FacetGrid(ds_train, col="Pclass",  row="Sex", hue = 'Survived')
g = g.map(plt.hist, "Survived")


# Observations:
# 
# 1) Females survival rate is higher
# 
# 2) Pclass 1 and 2 had greater survival rates than class 3 across male and female categories

# In[14]:


print(ds_train.dtypes)


# In[15]:


ds_train["Embarked"].value_counts()


# In[16]:


ds_train['Embarked']=ds_train['Embarked'].replace(np.nan,"S")
ds_test['Embarked']=ds_test['Embarked'].replace(np.nan,"S")


# In[17]:


ds_test[ds_test['Fare'].isna()]['Pclass']


# In[18]:


ds_test['Fare'] = np.where(ds_test['Fare'].isna(), np.nanmedian(ds_test[ds_test['Pclass']==3]['Fare']), ds_test['Fare'])
# imputing fare with respect to pclass with a median value of Fare considering only Pclass of 3 as fare greatly changed with Pclass


# In[19]:


ds_train["Sex"] = ds_train["Sex"].map({"male" : 0, "female" : 1}).astype("category")
ds_train['Pclass'] = ds_train['Pclass'].astype("category")
ds_train['Embarked'] = ds_train['Embarked'].map({'S':0, 'C':1, 'Q':2}).astype("category")

ds_test['Sex'] = ds_test['Sex'].map({'male':0, 'female':1}).astype("category")  
ds_test['Pclass'] = ds_test['Pclass'].astype("category")
ds_test['Embarked'] = ds_test['Embarked'].map({'S':0, 'C':1, 'Q':2}).astype("category")


# In[20]:


# Imputing missing values in Cabin with "Unknown"

ds_train['Cabin']=ds_train['Cabin'].replace(np.nan,"Unknown").astype("category")
ds_test['Cabin']=ds_test['Cabin'].replace(np.nan,"Unknown").astype("category")


# In[21]:


ds_train['title'] = ds_train['Name'].str.split(',').apply(lambda x: x[1])
ds_test['title'] = ds_test['Name'].str.split(',').apply(lambda x: x[1])


# In[22]:


ds_train['title'] = ds_train['title'].str.split('.').apply(lambda x: x[0])
ds_test['title'] = ds_test['title'].str.split('.').apply(lambda x: x[0])


# In[23]:


ds_train['title'].value_counts()


# In[24]:


ds_train['title'] = ds_train['title'].apply(lambda x: x.strip())
ds_test['title'] = ds_test['title'].apply(lambda x: x.strip())


# In[25]:


# Refining Titles in train dataset

ds_train['title'] = np.where(((ds_train['title']== 'Rev') | (ds_train['title']== 'Col') |
                                (ds_train['title']== 'Major') | (ds_train['title']== 'Capt') |
                                (ds_train['title']== 'Don') | (ds_train['title']== 'Sir') |
                                (ds_train['title']== 'Jonkheer') | (ds_train['title']== 'Dr')), 'Mr', ds_train['title'])

ds_train['title'] = np.where(((ds_train['title']== 'Mlle') | (ds_train['title']== 'Lady') | 
                             (ds_train['title']== 'the Countess') | (ds_train['title']== 'Mme') |
                             (ds_train['title']== 'Dona')), 'Mrs', ds_train['title'])

ds_train['title'] = np.where(ds_train['title']=='Ms', 'Miss',ds_train['title'])


# In[26]:


# Refining Titles in test dataset

ds_test['title'] = np.where(((ds_test['title']== 'Rev') | (ds_test['title']== 'Col') |
                                (ds_test['title']== 'Major') | (ds_test['title']== 'Capt') |
                                (ds_test['title']== 'Don') | (ds_test['title']== 'Sir') |
                                (ds_test['title']== 'Jonkheer') | (ds_test['title']== 'Dr')), 'Mr', ds_test['title'])

ds_test['title'] = np.where(((ds_test['title']== 'Mlle') | (ds_test['title']== 'Lady') | 
                             (ds_test['title']== 'the Countess') | (ds_test['title']== 'Mme') |
                             (ds_test['title']== 'Dona')), 'Mrs', ds_test['title'])

ds_test['title'] = np.where(ds_test['title']=='Ms', 'Miss',ds_test['title'])


# In[27]:


ds_train['title'].value_counts()


# In[28]:


# Title encoding

ds_train['title_enc'] = ds_train['title'].map({'Mr':0, 'Miss':1,'Mrs':2,'Master':3}).astype('category')
ds_test['title_enc'] = ds_test['title'].map({'Mr':0, 'Miss':1,'Mrs':2,'Master':3}).astype('category')


# In[29]:


# Imputing with median of the respective group - Train dataset

ds_train['Age'] = np.where(((ds_train['title']=='Mrs') & (ds_train['Age'].isna())), np.nanmedian(ds_train[ds_train['title']=='Mrs']['Age']), ds_train['Age'])
ds_train['Age'] = np.where(((ds_train['title']=='Miss') & (ds_train['Age'].isna())), np.nanmedian(ds_train[ds_train['title']=='Miss']['Age']), ds_train['Age'])
ds_train['Age'] = np.where(((ds_train['title']=='Mr') & (ds_train['Age'].isna())), np.nanmedian(ds_train[ds_train['title']=='Mr']['Age']), ds_train['Age'])
ds_train['Age'] = np.where(((ds_train['title']=='Master') & (ds_train['Age'].isna())), np.nanmedian(ds_train[ds_train['title']=='Master']['Age']), ds_train['Age'])


# In[30]:


# Imputing Age in test datase using the above strategy - Test dataset

ds_test['Age'] = np.where(((ds_test['title']=='Mrs') & (ds_test['Age'].isna())), np.nanmedian(ds_test[ds_test['title']=='Mrs']['Age']), ds_test['Age'])
ds_test['Age'] = np.where(((ds_test['title']=='Miss') & (ds_test['Age'].isna())), np.nanmedian(ds_test[ds_test['title']=='Miss']['Age']), ds_test['Age'])
ds_test['Age'] = np.where(((ds_test['title']=='Mr') & (ds_test['Age'].isna())), np.nanmedian(ds_test[ds_test['title']=='Mr']['Age']), ds_test['Age'])
ds_test['Age'] = np.where(((ds_test['title']=='Master') & (ds_test['Age'].isna())), np.nanmedian(ds_test[ds_test['title']=='Master']['Age']), ds_test['Age'])


# In[31]:


ds_train.isna().sum()


# In[32]:


ds_test.isna().sum()


# In[33]:


ds_train.columns


# In[34]:


ds_test.columns


# In[35]:


tr_ds_reducd = ds_train.drop(['Name','PassengerId','Ticket','Cabin','title'], axis = 1)
test_ds_reducd = ds_test.drop(['Name','PassengerId','Ticket','Cabin','title'], axis = 1)


# In[36]:


test_ds_reducd.columns


# In[37]:


y = tr_ds_reducd['Survived']
x = tr_ds_reducd.drop(['Survived'], axis=1)


# In[38]:


from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(x,y)


# Splitting the train data into train and validation

# In[39]:


# Scaling attributes - Standard Scaler

num_cols = ['Age','Fare']

X_train_scaled = X_train.copy()
X_val_scaled = X_val.copy()
X_test_scaled = test_ds_reducd.copy()

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train[num_cols])
X_train_scaled[num_cols] = scaler.transform(X_train_scaled[num_cols])
X_val_scaled[num_cols] = scaler.transform(X_val_scaled[num_cols])
X_test_scaled[num_cols] = scaler.transform(X_test_scaled[num_cols])


# ### Applying Logistic Regression 
# 

# In[40]:


from sklearn.linear_model import LogisticRegression

log_reg = LogisticRegression()


# In[41]:


log_reg.fit(X_train_scaled,y_train)


# In[42]:


tr_pred = log_reg.predict(X_train_scaled)
val_pred = log_reg.predict(X_val_scaled)
log_test_pred = log_reg.predict(X_test_scaled)


# In[43]:


from sklearn.metrics import accuracy_score


# In[44]:


accuracy_score(y_train, tr_pred)


# In[45]:


accuracy_score(y_val, val_pred)


# In[46]:


print(log_test_pred)


# In[ ]:





# In[ ]:




