#!/usr/bin/env python
# coding: utf-8

# Train a convolutional network that classifies the data in the provided dataset. Feel free to experiment with the layer architectures as long as it meets the requirements below. Perform the following after the training.
# 
# Architecture requirements 
# a)	If your first name starts with A-M, all pooling must be max pooling, else they must be average pooling
# b)	A convolutional layer with NxN filter must exist (at least 1) where N is the number of vowels in your surname + 1.
# c)	Overall, the network should use at least 2 dense layers
# 
# Task Activities
# a)	Submit the notebook used to train the network
# b)	Perform evaluation on the specified testing set and report the accuracy, recall, precision, and the confusion matrix. Make sure they are reported in the notebook clearly.
# c)	The network should at least perform better than random guess.

# In[ ]:


#import needed library
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import tensorflow.keras.optimizers as Optimizer
import tensorflow.keras.metrics as Metrics
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#Data Input folders
from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))


# In[ ]:


data = pd.read_csv('../input/utensils/utensils_test.csv')

#number of rows and columns
print('data({0[0]},{0[1]})'.format(data.shape))


# In[ ]:


#added another csv file for the labels of utensils
#read labels from CSV file
labels_csv = pd.read_csv('../input/labels/utensils_labels.csv')
labels = {}
for index, row in labels_csv.iterrows():
    labels[row['Label']] = row['Name']

for k, v in labels.items():
    print(k, v)


# In[ ]:


FILE_PATH = '../input/utensils/utensils_test.csv'


# In[ ]:


df = pd.read_csv(FILE_PATH)
df.head()


# In[ ]:


#convert labels to one-hot encoding
y = df['Label'].values
y[:5]


# In[ ]:


z = list(labels_csv['Name'].values)
z[:5]


# In[ ]:


y_encoder = OneHotEncoder(sparse=False)
y_encoded = y_encoder.fit_transform(y.reshape(-1, 1))
y_encoded[:5]


# In[ ]:


y_encoder.categories_


# In[ ]:


images = data.iloc[:,1:].values
images = images.astype(np.float)

# convert from [0:255] => [0.0:1.0]
images = np.multiply(images, 1.0 / 255.0)

#no of rows and columns
print('images({0[0]},{0[1]})'.format(images.shape))


# In[ ]:


image_size = images.shape[1]
print ('image_size => {0}'.format(image_size))

# in this case all images are square
image_width = image_height = np.ceil(np.sqrt(image_size)).astype(np.uint8)

print ('image_width => {0}\nimage_height => {1}'.format(image_width,image_height))


# In[ ]:


#Remove the labels in the set of our input features
#using above information, we will use width and height of 28 to get a square image
X = df.drop('Label', axis=1).values
X = X.reshape(-1, 28, 28, 1)


# In[ ]:


X.shape


# In[ ]:


# display images
def display(data, num_per_group):
    
    rows = data.sample(frac=1).groupby('Label', sort=False).head(num_per_group)
    
    figure_width = figure_height = np.ceil(np.sqrt(rows.shape[0])).astype(np.uint8)
    
    fig = plt.figure(figsize=(8, 8))
    
    i = 1
    for index, row in rows.iterrows():
        one_image = row[1:].values.reshape(image_width,image_height)
        label = labels[row[0]]
        sub = fig.add_subplot(figure_height, figure_width, i)
        sub.axis('off')
        sub.set_title(label)
        sub.imshow(one_image, cmap=cm.binary)
        i += 1

# output image     
display(data, 4)


# In[ ]:


#verifying the images

for i in range(10):
    plt.imshow(X[i].reshape(28, 28))
    plt.show()
    print('Label:', z[y[i]])


# ### Create a Keras model for training

# In[ ]:


input_ = tf.keras.Input((28, 28, 1))
conv1 = tf.keras.layers.Conv2D(8, (3, 3), activation='relu')(input_)
conv2 = tf.keras.layers.Conv2D(8, (3, 3), activation='relu')(conv1)
mp1 = tf.keras.layers.MaxPool2D((2,2))(conv2)
conv3 = tf.keras.layers.Conv2D(8, (3, 3), activation='relu')(mp1)
conv4 = tf.keras.layers.Conv2D(8, (3, 3), activation='relu')(conv3)
conv5 = tf.keras.layers.Conv2D(8, (3, 3), activation='relu')(conv4)
conv6 = tf.keras.layers.Conv2D(8, (3, 3), activation='relu')(conv5)
conv7 = tf.keras.layers.Conv2D(8, (3, 3), activation='relu')(conv6)
mp2 = tf.keras.layers.MaxPool2D((2,2))(conv7)
fl = tf.keras.layers.Flatten()(mp2)
dense1 = tf.keras.layers.Dense(8, activation='relu')(fl)
dense2 = tf.keras.layers.Dense(8, activation='relu')(dense1)
dense3 = tf.keras.layers.Dense(8, activation='relu')(dense2)
output = tf.keras.layers.Dense(3, activation='softmax')(dense3)

model = tf.keras.Model(inputs=input_, outputs=output)
model.summary()


# In[ ]:


#model.compile('adam', 'categorical_crossentropy')
model.compile(optimizer=Optimizer.Adam(lr=0.0001),loss='categorical_crossentropy',metrics=['accuracy'])


# In[ ]:


tf.keras.utils.plot_model(model)


# ### Fit the model using the training data

# In[ ]:


hst = model.fit(X, y_encoded, batch_size=25000, epochs=750, validation_split=0.35)


# ### Predictions to validate training operation

# In[ ]:


predictions = model.predict(X)


# In[ ]:


for i in range(10):
    plt.imshow(X[i].reshape(28, 28))
    plt.show()
    print('Prediction:', predictions[i])


# ### Convert the probabilities to labels

# In[ ]:


for i in range(10):
    plt.imshow(X[i].reshape(28, 28))
    plt.show()
    print('Prediction:', z[np.argmax(predictions[i])])
    print('Actual:', z[y[i]])


# Confusion Matrix, Precision, Recall and Accuracy 

# In[ ]:


# actual values
actual = np.argmax(y_encoded, axis=1)
# predicted values
predicted = np.argmax(predictions, axis=1)

# confusion matrix
matrix = confusion_matrix(actual,predicted, labels=[1,0])
print('Confusion matrix : \n',matrix)

# outcome values order in sklearn
tp, fn, fp, tn = confusion_matrix(actual,predicted,labels=[1,0]).reshape(-1)
print('Outcome values : \n',"TP FN FP TN \n", tp, fn, fp, tn)

# classification report for precision, recall f1-score and accuracy
matrix = classification_report(actual,predicted,labels=[1,0])
print('Classification report : \n',matrix)

