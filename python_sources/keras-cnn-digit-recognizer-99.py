#!/usr/bin/env python
# coding: utf-8

# # Loading dataset and Libs

# In[ ]:


from sklearn.model_selection import train_test_split
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from keras.utils.np_utils import to_categorical
get_ipython().run_line_magic('matplotlib', 'inline')

train = pd.read_csv("../input/digit-recognizer/train.csv")
test = pd.read_csv("../input/digit-recognizer/test.csv")


# # Examine dataset and normalize data

# In[ ]:


Y_train = train["label"]
X_train = train.drop(labels = ["label"],axis = 1)


# In[ ]:


X_train.isnull().any().describe()


# In[ ]:


test.isnull().any().describe()


# In[ ]:


X_train = X_train / 255.0
test = test / 255.0


# In[ ]:


X_train = X_train.values.reshape(-1,28,28,1)
test = test.values.reshape(-1,28,28,1)


# In[ ]:


Y_train = to_categorical(Y_train, num_classes = 10)


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X_train, Y_train, test_size = 0.1, random_state=2)


# # Examine the size and image dimensions
# 
# 

# In[ ]:


# printing the number of samples in X_train, X_test, y_train, y_test
print("Initial shape of dimensions of X_train", str(X_train.shape))

print("Number of samples in our training data: "+ str(len(X_train)))
print("Number of labels in out training data: "+ str(len(y_train)))
print("Number of samples in our test data: "+ str(len(X_test)))
print("Number of labels in out test data: "+ str(len(y_test)))
print()
print("Dimensions of x_train:" + str(X_train[0].shape))
print("Labels in x_train:" + str(y_train.shape))
print()
print("Dimensions of X_test:" + str(X_test[0].shape))
print("Labels in X_test:" + str(y_test.shape))


# # Let's take a look at some of images in this dataset
# 

# In[ ]:


g = plt.imshow(X_train[0][:,:,0])


# # Create Our Model
# - We're constructing a simple but effective CNN that uses 32 filters of size 3x3
# - We've added a 2nd CONV layer of 64 filters of the same size 3x2
# - We then downsample out data to 2x2, hete he apply a dropout where p is set to 0.2
# - We then flatten out Max Pool output that is connected to a Dense/FC layer has an output size of 128
# - How we apply a dropout where P is set to 0.5
# - Thus 128 output is connected to another FC/Dense layer that outputs to the 10 categorical units

# In[ ]:


num_classes = y_test.shape[1]
num_pixels = X_train.shape[1] * X_train.shape[2]
import keras
from tensorflow.keras.utils import plot_model
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.optimizers import SGD

optimizer=keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
dropout=0.2

model = Sequential()

model.add(Conv2D(32, (3,3),
                     activation='relu',
                     input_shape=(28,28,1)))
model.add(Conv2D(64, 
                     (3,3),
                     activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(dropout))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(dropout))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss = 'categorical_crossentropy',
                 optimizer = optimizer,
                 metrics = ['accuracy'])


print(model.summary())
plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)


# # Train our Model
# 

# In[ ]:


batch_size = 64
epochs = 100

history = model.fit(X_train,
                    y_train,
                    batch_size = batch_size,
                    epochs = epochs,
                    verbose = 1,
                    validation_data = (X_test, y_test))

score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


# # Plotting out Loss and Accuracy Charts
# 

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

history_dict = history.history

loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
epochs = range(1, len(loss_values) + 1)

line1 = plt.plot(epochs, val_loss_values, label='Validation/Test Loss')
line2 = plt.plot(epochs, loss_values, label='Training Loss')
plt.setp(line1, linewidth=1.0, marker = '+', markersize=1.0)
plt.setp(line2, linewidth=1.0, marker = '4', markersize=1.0)
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.grid(True)
plt.legend()
plt.show()


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

history_dict = history.history

acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']
epochs = range(1, len(loss_values) + 1)

line1 = plt.plot(epochs, val_acc_values, label='Validation/Test Accuracy')
line2 = plt.plot(epochs, acc_values, label='Training Accuracy')
plt.setp(line1, linewidth=1.0, marker = '+', markersize=1.0)
plt.setp(line2, linewidth=1.0, marker = '4', markersize=1.0)
plt.xlabel('Epochs') 
plt.ylabel('Accuracy')
plt.grid(True)
plt.legend()
plt.show()


# # Saving our Model
# 

# In[ ]:


model.save("/mnist_simple_cnn_10_epochs.h5")
print("Model save")


# # Loading our Model

# In[ ]:


from keras.models import load_model
classifier = load_model("/mnist_simple_cnn_10_epochs.h5")
print("Model loaded")


# In[ ]:



results = model.predict(test)


results = np.argmax(results,axis = 1)

results = pd.Series(results,name="Label")
submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),results],axis = 1)

submission.to_csv("submission.csv",index=False)


# ##  If you like, please upvote!
