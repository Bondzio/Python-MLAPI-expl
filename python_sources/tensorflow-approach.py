#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix 
from sklearn.model_selection import train_test_split


# # 1. Import Data

# In[ ]:


df_sky = pd.read_csv("../input/Skyserver_SQL2_27_2018 6_51_39 PM.csv", dtype={'class':'category'})
df_sky.head()


# Here we initialize the database and remove two columns that will not make a difference to our classification, the column 'objid' and 'specobjid' which are object identifiers.

# In[ ]:


df_sky.drop(['objid','specobjid'],axis =1,inplace=True)
df_sky.head()


# # 2. Data Exploration
# ## Analyzing data
# Number of samples per class. We notice that the quantity of Quasar is much smaller than the other classses.

# In[ ]:


counts = df_sky.groupby(['class'])['class'].count().plot(kind='bar')


# ## Correlation Study

# In[ ]:


import seaborn as sns
corr = df_sky.corr()
plt.figure(figsize=(10,10))
sns.heatmap(corr, xticklabels=corr.columns,yticklabels=corr.columns)


# ## Density graph
# Plots density graphs, in which you can verify the distribution of the data.

# In[ ]:


plt.figure(figsize=(20,20))
x = 0
for column in df_sky.columns:
    if column not in ['rerun','class']:
        x = x + 1
        plt.subplot(4,4,x)
        df_sky.groupby('class')[column].plot.kde()
        plt.title(column)
        plt.legend()


# # 3. Data Preprocess
# It separates the DataFrame into training and test pieces, in which the 'class' column is taken from the DataFrame. y is the class corresponding to the DataFrame X.
# ## Label Encoding

# In[ ]:


col = [i for i in df_sky.columns if i not in ['class']]
from sklearn.preprocessing import LabelEncoder
X_train = df_sky[col].apply(LabelEncoder().fit_transform)
X_train.head()


# In[ ]:


col = ['class']
from sklearn.preprocessing import LabelEncoder
Y_train = df_sky[col].apply(LabelEncoder().fit_transform)
Y_train.head()


# In[ ]:


Y_train.shape


# In[ ]:


X_train=df_sky.drop('class',axis=1).values


# In[ ]:


print("X_train shape:", X_train.shape)
print("Y_train shape:", Y_train.shape)


# In[ ]:


import keras
Y_train = keras.utils.to_categorical(Y_train, 3)
print("Y_train shape:", Y_train.shape)


# In[ ]:


#X_train=train.drop('class',axis=1).values

#Y_train=train['class'].values
#Y_train=Y_train.reshape((10000,1))

#print("X_train shape:", X_train.shape)
#print("Y_train shape:", Y_train.shape)


# Now the data format of feature & label are suitable for MLP model.
# 
# ## Data split to training & testing sets

# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X_train,Y_train, test_size=0.2, random_state=42)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)


# # 4. Model Training

# In[ ]:


import tensorflow as tf
def layer(output_dim,input_dim,inputs,activation=None):
    W = tf.Variable(tf.random_normal([input_dim, output_dim]))
    b = tf.Variable(tf.random_normal([1, output_dim]))
    XWb = tf.matmul(inputs, W)+b
    if activation is None:
        outputs = XWb
    else:
        outputs = activation(XWb)
    return outputs


# In[ ]:


X = tf.placeholder("float", [None, 15])
h1 = layer(300,15,X,activation=tf.nn.relu)
y_predict = layer(3, 300, h1, activation=None)
y_label = tf.placeholder("float", [None, 3]) 


# In[ ]:


loss_function = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=y_predict,labels=y_label))


# In[ ]:


optimizer = tf.train.AdamOptimizer(learning_rate = 0.001).minimize(loss_function)


# In[ ]:


correct_prediction = tf.equal(tf.argmax(y_label,1),tf.argmax(y_predict,1))


# In[ ]:


accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))


# In[ ]:


import math
def batches(batch_size, features,labels):
    sample_size = len(features)
    for start_i in range(0, sample_size, batch_size):
        end_i = start_i + batch_size
        batch1 = features[start_i:end_i]
        batch2 = labels[start_i:end_i]
    return batch1,batch2


# In[ ]:


trainEpochs = 20
batchSizes = 100
totalBatchs = int(10000/batchSizes)

epoch_list = []
loss_list = []
acc_list = []
from time import time
startTime = time()

sess = tf.Session()
sess.run(tf.global_variables_initializer())


# In[ ]:


for epoch in range(trainEpochs):
    for i in range(totalBatchs):
        batch_x, batch_y = batches(batchSizes, x_train, y_train)
        sess.run(optimizer,feed_dict={X: batch_x, y_label: batch_y})
    loss,acc = sess.run([loss_function,accuracy],feed_dict={X: x_test,y_label: y_test})
    epoch_list.append(epoch)
    loss_list.append(loss)
    acc_list.append(acc)
    print("Train Epoch:", '%02d' % (epoch+1), "Loss=", "{:.9f}".format(loss), "Acc=", acc)
duration = time() - startTime
print("Train Finished takes:", duration)


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
fig = plt.gcf()
fig.set_size_inches(10,6)
plt.plot(epoch_list, acc_list, label='MES')
plt.ylabel('acc')
plt.xlabel('epoch')
plt.legend(['acc'], loc='upper left')


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
fig = plt.gcf()
fig.set_size_inches(10,6)
plt.plot(epoch_list, loss_list, label='MES')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['loss'], loc='upper left')

