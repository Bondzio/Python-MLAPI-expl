#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from sklearn import preprocessing
import tensorflow as tf
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split


# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


import warnings
warnings.filterwarnings('ignore')


# In[ ]:


physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)
print(physical_devices)


# # Read dataset

# In[ ]:


df = pd.read_csv('/kaggle/input/kc-house/kc_house_data.csv')
df.head()


# In[ ]:


print('Number of entries {}'.format(len(df)))
print('Column names in our dataset ->\n', list(df.columns))


# Correlation Matrix

# In[ ]:


corr = df.corr()
sns.set(font_scale = .7)
plt.figure(figsize=(15,8))
sns.heatmap(
    corr,
    annot= True,
    fmt='.2f',
    cmap='BuGn',
)


# In[ ]:


# dropping high correlation columns, unused columns and target column
data = df.drop(['id','lat','long','price'],axis=1)
data.head()


# In[ ]:


y = df[['price']]
y.head()


# # Feature Engineering
#     Use Sale Date, Year Built and Renovation data to create more features

# In[ ]:


data['date'] = data['date'].map(lambda x : int(x[:4]))
data[['date']].head()


# In[ ]:


data['selling_age'] = data['date'] - data['yr_built']
data['was_renovated'] = (data['yr_renovated'] != 0).astype(int)
data[['date','yr_built','yr_renovated','was_renovated','selling_age']].head()


# In[ ]:


data['bedrooms/bathrooms'] = data['bedrooms'] + data['bathrooms']
data[['bedrooms','bathrooms','bedrooms/bathrooms']].head()


# In[ ]:


data = data.drop(['date','yr_built','yr_renovated','bedrooms','bathrooms'],axis=1)
data.head()


# # Feature vs Target Plots
#     Plotting every feature against house price to find relations/patterns

# In[ ]:


boxplot_columns = [
'bedrooms/bathrooms',
'condition',
'grade',
'view',
'floors',
]
continous_columns = [x for x in data.columns if x not in boxplot_columns]
continous_columns


#  Boxplot for categorical features and Scatter plot for continous features

# In[ ]:


i = 0
for col in boxplot_columns:
    i += 1
    if(i % 2 == 1):
        plt.figure(figsize=(16,15))
    plt.subplot(int(len(boxplot_columns) / 2) + 1,2,i)
    plt.title('{} vs price boxplot'.format(col))
    plt.xlabel(col)
    sns.boxplot(data[col],y['price'])
    plt.xticks(
        rotation=45, 
        horizontalalignment='right',
        fontweight='light',  
    )
i = 0
for col in continous_columns:
    i += 1
    if(i % 2 == 1):
        plt.figure(figsize=(16,15))
    plt.subplot(int(len(continous_columns) / 2) + 1,2,i)
    plt.title('{} vs price'.format(col))
    plt.xlabel(col)
    plt.ylabel('price')
    sns.scatterplot(data[col],y['price'])
    plt.xticks(
        rotation=45, 
        horizontalalignment='right',
        fontweight='light',  
    )
plt.show()


# # Creating Train and Test Data by preprocessing the data

# In[ ]:


categorical = [
'waterfront',
'was_renovated',
'zipcode',
'view',
'condition'
]
continous = [ col for col in data.columns if col not in categorical]
continous


# In[ ]:


ss = preprocessing.StandardScaler()
conti_array = ss.fit_transform(data[continous])
conti_df = pd.DataFrame(conti_array,columns=continous)
conti_df.head()


# In[ ]:


zipcode = pd.get_dummies(data['zipcode'])
zipcode.columns = ['Zip_'+str(i) for i in zipcode.columns]
zipcode.head()


# In[ ]:


view = pd.get_dummies(data['view'])
view.columns = ['View_'+ str(i+1) for i in range(len(view.columns))]
view.head()


# In[ ]:


condition = pd.get_dummies(data['condition'])
condition.columns = ['Condition_' + str(i) for i in condition.columns]
condition.head()


# In[ ]:


X = pd.concat([
    conti_df,
    data[['waterfront','was_renovated']],
    view,
    condition,
    zipcode
],axis=1)
X.head()


# In[ ]:


X.columns


# In[ ]:


y.head()


# In[ ]:


train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state = 69)
print('Training dataset shape {}'.format(train_x.shape))
print('Testing dataset shape {}'.format(test_x.shape))


# # Linear Regression using Classic ML (sklearn)

# In[ ]:


# first linear regression using classic ML
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(train_x, train_y)


# In[ ]:


print('Training score -> {}'.format(lr.score(train_x, train_y)))
print('Testing score -> {}'.format(lr.score(test_x, test_y)))


# In[ ]:


pred_train = lr.predict(train_x)
pred_test = lr.predict(test_x)

print('Training r2 score -> {}'.format(r2_score(train_y, pred_train)))
print('Testing r2 score -> {}'.format(r2_score(test_y, pred_test)))


# # Linear regression using Neuron Network (Single Neuron)

# In[ ]:


# using keras
model = Sequential()
model


# In[ ]:


model.add(
    Dense(
        # one neuron will be used for this linear regression
        1,
        input_shape = (1,),
        # linear regression
        activation = 'linear'
    )
)


# In[ ]:


optimizer = tf.keras.optimizers.Adam(0.05)
model.compile(loss='mse',optimizer=optimizer,metrics=['mae'])


# In[ ]:


model.summary()


# In[ ]:


weights = model.layers[0].get_weights()
print('bias ->\n',weights[1])
print('weights ->\n',weights[0])


# In[ ]:


history = model.fit(train_x['sqft_living15'],train_y, validation_split=0.2, epochs=300, verbose=1)


# In[ ]:


# to visualize
def plot_history(history):
    plt.figure(figsize=(15,15))
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error')
    plt.plot(history.epoch, np.array(history.history['mae']),label='train_loss')
    plt.plot(history.epoch, np.array(history.history['val_mae']),label='val_loss')
    plt.legend()
    plt.show()


# In[ ]:


plot_history(history)


# In[ ]:


result = model.predict(train_x['sqft_living15'])
test_result = model.predict(test_x['sqft_living15']).flatten()

print('R2 score for train data using 1 neuron -> ',r2_score(train_y, result))
print('R2 score for test data using 1 neuron-> ',r2_score(test_y, test_result))


# # Linear Regression using Neural Network (Hidden layer using Keras)

# In[ ]:


# using keras
nn_model = Sequential()
nn_model


# In[ ]:


# input layer
nn_model.add(
    Dense(
        # 64 neurons will be used for this linear regression
        64,
        # input shape
        input_shape = (X.shape[1],),
        activation = tf.nn.relu
    )
)
# hidden layer
nn_model.add(
    Dense(
        # 64 neurons for hidden layer
        64,
        activation = tf.nn.relu
    )
)
# output layer
nn_model.add(
    Dense(
        # 1 neurons as output neuron
        1
    )
)


# In[ ]:


optimizer = tf.keras.optimizers.Adam(0.01)
nn_model.compile(loss='mse',optimizer=optimizer,metrics=['mae'])


# In[ ]:


nn_model.summary()


# In[ ]:


weights = nn_model.layers[0].get_weights()
print('bias ->\n',weights[1])
print('weights ->\n',weights[0])


# In[ ]:


nn_history = nn_model.fit(train_x, train_y, validation_split=0.2, epochs=100, verbose=1)


# In[ ]:


plot_history(nn_history)


# In[ ]:


nn_result = nn_model.predict(train_x)
nn_test_result = nn_model.predict(test_x).flatten()

print('R2 score for train data using hidden layer -> ',r2_score(train_y, nn_result))
print('R2 score for test data using hidden layer -> ',r2_score(test_y, nn_test_result))


# # Comparing predictions results
#     -> for three different implementations of linear regression

# In[ ]:


plt.figure(figsize=(24,8))
plt.subplot(131)
plt.title('Linear Regression using classic ML')
plt.xlabel('predictions')
plt.ylabel('true labels')
plt.scatter(train_y,pred_train)
plt.subplot(132)
plt.xlabel('predictions')
plt.ylabel('true labels')
plt.title('Linear Regression using Single Neuron Networks')
plt.scatter(train_y,result)
plt.subplot(133)
plt.xlabel('predictions')
plt.ylabel('true labels')
plt.title('Linear Regression using Neural Network with Hidden layer')
plt.scatter(train_y,nn_result)
plt.show()


# In[ ]:


plt.figure(figsize=(24,8))
plt.subplot(131)
plt.title('Linear Regression using classic ML')
plt.xlabel('predictions')
plt.ylabel('true labels')
plt.scatter(test_y,pred_test,color='blue',label='Classic ML')
plt.legend()
plt.subplot(132)
plt.xlabel('predictions')
plt.ylabel('true labels')
plt.title('Linear Regression using Single Neuron Networks')
plt.scatter(test_y,test_result,color='grey',label='Neural Network with single neuron')
plt.legend()
plt.subplot(133)
plt.title('Linear Regression using Neural Network with Hidden layer')
plt.xlabel('predictions')
plt.ylabel('true labels')
plt.scatter(test_y,nn_test_result,color='green', label='Neural network with hidden layer')
plt.legend()
plt.show()

