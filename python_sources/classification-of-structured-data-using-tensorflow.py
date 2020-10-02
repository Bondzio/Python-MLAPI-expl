#!/usr/bin/env python
# coding: utf-8

# # Importing dataset and libraries

# In[ ]:


#importing libararies
import pandas as pd
import numpy as np 
import tensorflow as tf

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split


# In[ ]:


#create dataframe
#load dataset

df=pd.read_csv("diabetic_data.csv")
df.head()


# # Data analysis
# Analyzing the data 

# In[ ]:


df.shape


# In[ ]:


df.dtypes


# In[ ]:


df.keys()


# In[ ]:


df.info()


# In[ ]:


df.describe()


# In[ ]:


df.select_dtypes(include=['object']).shape


# # Feature Engineering

# Numeric columns have no NULL values
# 
# Missing information is represented by '?' in few columns of dtype 'object'
# 
# Counting number of rows with missing information i.e., '?' in each column

# In[ ]:


for column in df.columns:
    if df[column].dtype == object:
        print(column,df[column][df[column]== '?'].count())


# Dropping columns 'encounter_id', 'patient_nbr' ,'payer_code' that are unnecessary for the model
# Dropping columns 'weight','medical_specialty' whose values are '?' above 90% and 40% respectively

# In[ ]:


df.drop(['encounter_id', 'patient_nbr', 'weight','medical_specialty', 'payer_code','admission_source_id' ], axis=1, inplace= True)


# In[ ]:


df['gender'].value_counts()


# In[ ]:


# Removing 3 rows with gender values 'Unknown/Invalid

df = df[df.gender != 'Unknown/Invalid']


# In[ ]:


#Removing rows with missing information in all 3 diagnosis

df = df[(df.diag_1 != '?') | (df.diag_2 != '?') | (df.diag_3 != '?')]


# Dropping all columns related to medicines except insulin,metformin,glimepiride,repaglinide,pioglitazone,acarbose,glipizide, glyburide ,nateglinide (which is widely used diabetic medicine) as there is a column "diabetesMed" which tells if a patient is using diabetes medicine or not

# In[ ]:


df.drop(['chlorpropamide','acetohexamide', 'tolbutamide', 'rosiglitazone', 'miglitol', 'troglitazone', 'tolazamide', 'examide', 'citoglipton',
       'glyburide-metformin', 'glipizide-metformin','glimepiride-pioglitazone', 'metformin-rosiglitazone','metformin-pioglitazone','diag_1','diag_2','diag_3'],axis=1, inplace= True)


# In[ ]:


def fn(x):
    if x =='NO' or x=='>30':
        return 0
    else :
        return 1
df['readmit']= df['readmitted'].map(fn)
df.drop(['readmitted'], axis=1, inplace= True)


# In[ ]:


df.head()


# In[ ]:


def fun(z):
    if z =='None' or z=='Norm':
        return 1
    else :
        return 0
df['A1C']= df['A1Cresult'].map(fun)
df.drop(['A1Cresult'], axis=1, inplace= True)


# In[ ]:


#Dividing age groups in to three categories 'young','mid','old
def gt_ag(a):
    if a =='[0-10)' or a=='[10-20)' or a=='[20-30)':
        return 'young'
    elif a =='[30-40)' or a=='[40-50)' or a=='[50-60)':
        return 'mid'
    else:
        return'old'
df['Age']= df['age'].map(gt_ag)
df.drop(['age'], axis=1, inplace= True)


# In[ ]:


df['Age'].value_counts()


# # Splitting the Dataset into Train,Test and Validation

# In[ ]:


train, test = train_test_split(df, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)
print(len(train), 'train examples')
print(len(val), 'validation examples')
print(len(test), 'test examples')


# In[ ]:


labels = df.pop('readmit')


# In[ ]:


# A utility method to create a tf.data dataset from a Pandas Dataframe
def df_to_dataset(df, shuffle=True, batch_size=32):
  df = df.copy()
  labels = df.pop('readmit')
  ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(df))
  ds = ds.batch(batch_size)
  return ds


# In[ ]:


batch_size = 50 # A small batch sized is used for demonstration purposes
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)


# In[ ]:


for feature_batch, label_batch in train_ds.take(1):
  print('Every feature:', list(feature_batch.keys()))
  print('A batch of ages:', feature_batch)
  print('A batch of targets:', label_batch )


# In[ ]:


# We will use this batch to demonstrate several types of feature columns
example_batch = next(iter(train_ds))[0]


# 
# # Creating feature layer and adding features 

# In[ ]:


# A utility method to create a feature column
# and to transform a batch of data
def demo(feature_column):
  feature_layer = layers.DenseFeatures(feature_column)
  print(feature_layer(example_batch).numpy())


# In[ ]:


##

feature_columns = []

num_lab_procedures=feature_column.numeric_column("num_lab_procedures")
#demo(num_lab_procedures)

# numeric cols
for header in ['num_lab_procedures', 'num_medications', 'number_inpatient', 'number_diagnoses', 'number_emergency','A1C']:
  feature_columns.append(feature_column.numeric_column(header))

#categorical cols

insulin = feature_column.categorical_column_with_vocabulary_list(
      'insulin', ['No', 'Steady','Up','Down'])

insulin = feature_column.indicator_column(insulin)
feature_columns.append(insulin)


metformin = feature_column.categorical_column_with_vocabulary_list(
      'metformin', ['No', 'Steady','Up','Down'])

metformin = feature_column.indicator_column(metformin)
feature_columns.append(metformin)

age = feature_column.categorical_column_with_vocabulary_list(
      'Age', ['old', 'mid','young'])

age = feature_column.indicator_column(age)
feature_columns.append(age)




# In[ ]:


feature_layer = tf.keras.layers.DenseFeatures(feature_columns)


# # Converting the target using LabelEncoder

# In[ ]:


from sklearn.preprocessing import LabelEncoder
# creating instance of labelencoder
labelencoder = LabelEncoder()
# Assigning numerical values and storing in another column
train['readmit'] = labelencoder.fit_transform(train['readmit'])
train['readmit'].head()
test['readmit'] = labelencoder.fit_transform(test['readmit'])
test['readmit'].head()
val['readmit'] = labelencoder.fit_transform(val['readmit'])
val['readmit'].head()


# # Splitting dataset into for Evaluation

# In[ ]:


batch_size = 32
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)


# # Model

# In[ ]:


model = tf.keras.Sequential([
 
  feature_layer,
  layers.Dense(128, activation='relu'),
  layers.Dense(128, activation='relu'),
  layers.Dense(1)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_ds,
          validation_data=val_ds,
          epochs=10)


# # Accuracy

# In[ ]:


loss, accuracy = model.evaluate(test_ds)
print(" Test Accuracy", accuracy)
loss, accuracy = model.evaluate(val_ds)
print(" Validation Accuracy", accuracy)


# In[ ]:




