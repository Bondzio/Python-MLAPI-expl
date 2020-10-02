#!/usr/bin/env python
# coding: utf-8

# **If you like my notebook, please upvote my work!**
# 
# **If you use parts of this notebook in your scripts/notebooks, giving some kind of credit for instance link back to this notebook would be very much appreciated. Thanks in advance! :)**
# 
# Thankyou! :) Hope you like my work!

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


# # Importing important libraries.

# In[ ]:


import keras
import plotly.express as px
from keras import backend as K
from keras.optimizers import Adam
import plotly.graph_objects as go
import plotly.figure_factory as ff
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense,Flatten
from keras.metrics import categorical_crossentropy
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator


# # Loading the Dataset.

# In[ ]:


df_train = pd.read_csv('/kaggle/input/digit-recognizer/train.csv')
df_train.describe()


# # Splitting the target and predictor variables.

# In[ ]:


df_train_x = df_train.drop('label',axis =1)
df_train_y = df_train[['label']]


# # Machine Learning Model.

# ## Splitting data into train and test set 

# In[ ]:


np_train_x = df_train_x.to_numpy().reshape(-1,28,28,1)
np_train_y = df_train_y.to_numpy()
x_train,x_test,y_train,y_test = train_test_split(np_train_x, np_train_y,test_size=0.10,random_state=42)


# ## Defining the Image generator function

# In[ ]:


datagen = ImageDataGenerator(
    featurewise_center=False,
    featurewise_std_normalization=False,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=False,
    vertical_flip=False,
    brightness_range = [0.8,1.])
datagen.fit(x_train)


# ## Defining the layers and metrics for the Neural Network

# In[ ]:


model  = Sequential()
model.add(Flatten(input_shape = (28,28,1)))
model.add(Dense(1000,activation = 'relu'))
model.add(Dense(10,activation = 'softmax'))
model.compile(Adam(lr = 0.0001),loss = 'sparse_categorical_crossentropy',
              metrics = ['accuracy'])
keras.utils.plot_model(model, "Neural_Network.png", show_shapes=True)


# In[ ]:


model.summary()


# ## Training the Neural Network

# In[ ]:


model.fit_generator(datagen.flow(x_train,y_train,batch_size = 30),
                    steps_per_epoch = 1000,validation_data = (x_test,y_test),
                    epochs = 50,verbose = 2)


# ## Plotting the training vs testing accuracy

# In[ ]:


plot = pd.DataFrame()
plot['Validation Accuracy'] = model.history.history['val_accuracy']
plot['Training Accuracy'] = model.history.history['accuracy']
plot['Validation Loss'] = model.history.history['val_loss']
plot['Training Loss'] = model.history.history['loss']
plot['Epoch'] = plot.reset_index()['index']+1
plot


# In[ ]:


fig = go.Figure()
fig.add_trace(go.Scatter(x = plot['Epoch'],
                         y = plot['Training Accuracy'].to_numpy()//.0001/100,
                         mode = 'lines+markers',name = 'Training Accuracy',
                         hovertemplate='The Training Accuracy is: %{y}%<br>'+
                                   'The Epochs run are: %{x}<extra></extra>'))
fig.add_trace(go.Scatter(x = plot['Epoch'],
                         y = plot['Validation Accuracy']//.0001/100,
                         mode = 'lines+markers',name = 'Validation Accuracy',
                         hovertemplate='The Validation Accuracy is: %{y}%'+
                               '<br>The Epochs run are: %{x}<extra></extra>'))
fig.update_layout(title  = 'Change in validation and training accuracy over the epochs',
                  xaxis_title = 'Epochs run',yaxis_range = [70,100],
                  yaxis_title = 'Acuuracy (In percentage)')
fig.show()


# ## Plotting the confusion matrix

# In[ ]:


predictions = model.predict_classes(x_test)
y_test = y_test
classes = [0,1,2,3,4,5,6,7,8,9]


confusion_mat = np.zeros((len(classes),len(classes)))
for i in range(len(predictions)):
    confusion_mat[classes.index(predictions[i])][classes.index(y_test[i])]+=1
confusion_mat = confusion_mat.T
confusion_mat_norm = confusion_mat/len(y_test)
confusion_mat_norm = (confusion_mat_norm//0.0001)/10000

fig = ff.create_annotated_heatmap(confusion_mat_norm, x=classes, y=classes, 
              annotation_text=confusion_mat_norm,
              colorscale='Viridis',text = confusion_mat,
              hovertemplate='Expected Value: %{y}<br>Predicted Value: %{x}'
                            +'<br>No. of datapoints in this category are:'
                            +' %{text}<extra></extra>')
fig.update_layout(title_text='<b>Confusion Matrix for the dataset:</b>',
                  xaxis = {'title':'Predicted Values'},width = 900,
                  yaxis = {'title':'Expected Values','autorange':'reversed'})
fig.update_traces(showscale = True)
fig.show()


# We can see that the confusion matrix shows higher values for digits that look similar and might be confusiong to distinguish between and lower values for the digits that are easy to distinguish between.

# # Predicting output over the testset.

# ## Reading test file

# In[ ]:


df_test = pd.read_csv('/kaggle/input/digit-recognizer/test.csv')
df_test.describe()


# ## Processing of the test file 

# In[ ]:


np_test = df_test.to_numpy().reshape(-1,28,28,1)


# ## Predicting over test set

# In[ ]:


df_test['label'] = model.predict_classes(np_test)


# In[ ]:


a = []
for i in range(28000):
    a.append(i+1)
df_test['ImageId'] = a
df_test.describe()


# ## Exporting output to csv

# In[ ]:


df_test[['ImageId','label']].to_csv('submission.csv',index=False)

