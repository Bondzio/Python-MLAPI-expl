#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import re
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import plotly.express as px
import plotly.graph_objects as go
import tensorflow as tf
from sklearn.model_selection import train_test_split


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

pd.set_option('display.max_columns', None)


# ## Data Analysis

# In[ ]:


train_df = pd.read_csv('/kaggle/input/titanic/train.csv')
test_df = pd.read_csv('/kaggle/input/titanic/test.csv')

# Storing the passenger_ids for submission
passenger_ids = test_df['PassengerId']


# **Exploring train data**

# In[ ]:


train_df.head()


# **Exploring test data**

# In[ ]:


test_df.head()


# **Getting the counts of survived and dead**

# In[ ]:


train_df['Survived'].value_counts()


# **Getting the count of missing values of each feature in train data**

# In[ ]:


train_df.info()


# **Getting the count of missing values of each feature in test data**

# In[ ]:


test_df.info()


# **Applying some statistical functions on train data**

# In[ ]:


train_df.describe()


# **Applying some statistical functions on test data**

# In[ ]:


test_df.describe()


# ## Visualization

# **Creating an histogram for Survived with respect to Passenger class **

# In[ ]:


def hist_survived_vs_feature(feature, df=train_df, labels={}):

    survived_mapping = df['Survived'].map({0: 'Dead', 1: 'Survived'})

    fig = px.histogram(df, x=survived_mapping, width=800, color=feature, labels=labels)
    fig.update_layout(
        bargap=0.2,
        xaxis_title_text='Survived',
        yaxis_title_text='Survived count'
    )
    
    return fig

hist_survived_vs_feature('Pclass')


# **Creating an histogram for Survived with respect to Sex**

# In[ ]:


hist_survived_vs_feature('Sex')


# **Creating an histogram for Survived with respect to Age**

# In[ ]:


fig = px.histogram(train_df, x='Age', color='Survived', barmode='overlay')
fig


# **Creating an histogram for Survived with respect to Sibling and Spouse count**

# In[ ]:


hist_survived_vs_feature('SibSp')


# **Creating an histogram for Survived with respect to Parent and Children count**

# In[ ]:


hist_survived_vs_feature('Parch')


# **Creating an histogram for Survived with respect to Fare**

# In[ ]:


fig = px.histogram(train_df, x='Fare', color='Survived', barmode='overlay')
fig


# **Creating an histogram for Survived with respect to Cabin**

# In[ ]:


df = train_df[train_df['Cabin'].notnull()]
cabin_initials = df['Cabin'].map(lambda x: x[0])

hist_survived_vs_feature(cabin_initials, df=df, labels={'color': 'cabin'})


# **Creating an histogram for Survived with respect to Embarked station**

# In[ ]:


df = train_df[train_df['Embarked'].notnull()]
hist_survived_vs_feature('Embarked', df=df)


# ## Feature Engineering

# In[ ]:


train_df.columns


# **Extracting the titles from passenger names and one-hot encoding them**

# In[ ]:


# Combining the train and test data into a single dataset
dataset = [train_df, test_df]

# Preprocessing feature 'Name'

for df in dataset:
    # Extracting title
    df['Title'] = df['Name'].map(lambda x: re.search(r' ([A-Za-z]+)\.', x).group().strip().replace('.', ''))

# Unique titles in train data
train_df['Title'].value_counts().index


# In[ ]:


# # Unique titles in test data

test_df['Title'].value_counts().index


# In[ ]:


# Mapping Mr, Miss, Mrs, Master and rest to numerical values
title_mapping = {'Mr': 1, 'Miss': 2, 'Mrs': 3, 'Master': 4, 'Dr': 5, 'Rev': 5, 'Col': 5,
                 'Major': 5, 'Mlle': 5, 'Ms': 5, 'Countess': 5, 'Lady': 5, 'Capt': 5,
                 'Jonkheer': 5, 'Don': 5, 'Sir': 5, 'Mme': 5}

for df in dataset:
    df['Title'] = df['Title'].map(title_mapping)

train_df.head()


# In[ ]:


def concat_dummies(feature_name):
    global dataset
    
    new_train_df = pd.concat([train_df, pd.get_dummies(train_df[feature_name], prefix=feature_name)], axis=1)
    new_test_df = pd.concat([test_df, pd.get_dummies(test_df[feature_name], prefix=feature_name)], axis=1)
    dataset = [new_train_df, new_test_df]
    
    return new_train_df, new_test_df


# In[ ]:


# Concatenating the one-hot encoded values with the train and test dataframes
train_df, test_df = concat_dummies('Title')

train_df.head()


# **Encoding the passenger gender to numerical values**

# In[ ]:


# Preprocessing feature 'Sex'

sex_mapping = {'male': 0, 'female': 1}

for df in dataset:
    df['Sex'] = df['Sex'].map(sex_mapping)
    
train_df.head()


# **Binning Age feature based on the trend in histogram and one-hot encoding them**
# 
# * 0 - 5: Age Group 1
# * 6 - 11: Age Group 2
# * 12 - 17: Age Group 3
# * 18 - 25: Age Group 4
# * 26 - 47: Age Group 5
# * 48 - 61: Age Group 6
# * 61 - 80: Age Group 7

# In[ ]:


# Preprocessing feature 'Age'

age_bins = [0, 5.99, 11.9, 17.9, 25.9, 47.9, 61.9, 80]
age_labels = [i for i in range(1, 8)]

for df in dataset:
    # Filling the missing values in each dataset with median of corresponding 'Title' feature
    df['Age'] = df['Age'].fillna(df.groupby('Title')['Age'].transform('median'))
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)

train_df.head()


# In[ ]:


# Concatenating the one-hot encoded values with the train and test dataframes
train_df, test_df = concat_dummies('AgeGroup')

train_df.head()


# **Scaling the parent/children count and sibling/spouse count to 0 - 1**

# In[ ]:


# Preprocessing features 'Parch' and 'SipSp'

def scale_feature(feature):
    result = []
    
    # Applying min-max scaling to the 'Parch' and 'SipSp' features
    for df in dataset:
        feature_val = df[feature]
        max_val = feature_val.max()
        min_val = feature_val.min()
        scaled_feature = (feature_val - min_val) / (max_val - min_val)
        result.append(scaled_feature)
        
    return result

train_df['SibSp'], test_df['SibSp'] = scale_feature('SibSp')
train_df['Parch'], test_df['Parch'] = scale_feature('Parch')

train_df.head()


# **Scaling the passenger fare to 0 - 1**

# In[ ]:


# Preprocessing feature 'Fare'

# Filling the missing values with the median of the corresponding passenger class
test_df['Fare'] = test_df['Fare'].fillna(test_df.groupby('Pclass')['Fare'].transform('median'))
train_df['Fare'], test_df['Fare'] = scale_feature('Fare')

train_df.head()


# **One-hot encoding the embarked station**

# In[ ]:


# Preprocessing feature 'Embarked'

# Visualizing the count of passenger's embarkment across different passenger classes using bar chart
df = train_df[train_df['Embarked'].notnull()]
class_count = df.groupby(['Pclass', 'Embarked'])['Embarked'].count()
C_count = class_count.loc[([1, 2, 3], 'C')]
Q_count = class_count.loc[([1, 2, 3], 'Q')]
S_count = class_count.loc[([1, 2, 3], 'S')]

p_class = [1, 2, 3]
fig = go.Figure()
fig.add_trace(go.Bar(x=p_class, y=C_count.tolist(), name='C'))
fig.add_trace(go.Bar(x=p_class, y=Q_count.tolist(), name='Q'))
fig.add_trace(go.Bar(x=p_class, y=S_count.tolist(), name='S'))
fig.update_layout(
    barmode='stack',
    xaxis_title_text='Passenger class',
    yaxis_title_text='Embarked station count'
)
fig.show()

# Getting the same figure using histogram
fig = px.histogram(df, x='Pclass', color='Embarked')
fig.update_layout(
    bargap=0.2,
    xaxis_title_text='Passenger class',
    yaxis_title_text='Embarked station count'
)


# In[ ]:


# Filling the missing values with 'S' station as it covers 50% of the count on each class
train_df['Embarked'] = train_df['Embarked'].fillna('S')
# Concatenating the one-hot encoded values with the train and test dataframes
train_df, test_df = concat_dummies('Embarked')

train_df.head()


# In[ ]:


# Dropping unwanted columns
train_df = train_df.drop(['PassengerId', 'Name', 'Age', 'Ticket', 'Cabin', 'Embarked',
                          'Title', 'AgeGroup'], axis=1)
test_df = test_df.drop(['PassengerId', 'Name', 'Age', 'Ticket', 'Cabin', 'Embarked',
                          'Title', 'AgeGroup'], axis=1)

train_df.head()


# In[ ]:


test_df.head()


# **Note: Passenger class is not one-hot encoded to maintain the ordinality of the feature**

# ## Modelling

# In[ ]:


X = train_df.iloc[:, 1:].values
y = train_df['Survived'].values

# Splitting the train data into train and validation sets 
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=1)
X_test = test_df.values


# In[ ]:


print(f'Shape of X_train: {X_train.shape}')
print(f'Shape of X_test: {X_val.shape}')
print(f'Shape of y_train: {y_train.shape}')
print(f'Shape of y_test: {y_val.shape}')


# In[ ]:


# Building a Keras sequential model for the binary classification problem
model = tf.keras.Sequential()
# Adding dropout layer to avoid overfitting the train data
model.add(tf.keras.layers.Dropout(0.25, input_shape=[20]))
model.add(tf.keras.layers.Dense(25, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

# Using Adam optimizer with custom learning rate
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
model.summary()


# In[ ]:


# Training the model for 10 epochs
history = model.fit(
    x=X_train,
    y=y_train,
    epochs=10,
    batch_size=1,
    validation_data=(X_val, y_val)
)


# In[ ]:


# Predicting 'Survived' for test data
prediction = model.predict(X_test)
# Rounding the predictions to either 0 or 1
rounded_prediction = np.where(prediction >= 0.5, 1, 0).flatten()

# Creating a dataframe for submission
submission_df = pd.DataFrame({
    'PassengerId': passenger_ids,
    'Survived': rounded_prediction
})

submission_df.head()


# In[ ]:


# Outputting the dataframe as a CSV file for submission
submission_df.to_csv('submission.csv', index=False)

