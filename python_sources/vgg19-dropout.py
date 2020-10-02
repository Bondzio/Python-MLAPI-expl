#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import keras
from keras.applications import VGG19
from keras.layers import Dropout
from keras.models import Model
from keras.preprocessing import image
import matplotlib.pyplot as plt
from keras.optimizers import Adam
from keras import regularizers
from keras.models import Sequential, load_model
from keras.utils.np_utils import to_categorical
from keras.layers import Dense,Activation,Flatten,MaxPool2D,Conv2D,Dropout
from keras.layers.normalization import BatchNormalization
import keras.backend as K
import itertools
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


from keras.datasets import cifar10
(X_train,y_train),(X_test, y_test) = cifar10.load_data()


# In[ ]:


y_train = to_categorical(y_train,10)
y_test = to_categorical(y_test,10)


# In[ ]:


model = VGG19(
    weights=None,
    classes=10,
    input_shape=[32,32,3]
)

# Store the fully connected layers
fc1 = model.layers[-3]
fc2 = model.layers[-2]
predictions = model.layers[-1]

# Create the dropout layers
dropout1 = Dropout(0.3)
dropout2 = Dropout(0.5)

# Reconnect the layers
x = dropout1(fc1.output)
x = fc2(x)
x = dropout2(x)
predictors = predictions(x)

# Create a new model
model2 = Model(inputs=model.input, outputs=predictors)


# In[ ]:


model = model2
model.summary()


# In[ ]:


model.compile(
    loss='categorical_crossentropy',
    optimizer='sgd',
    metrics=['accuracy']
)


# In[ ]:


import os

# Prepare model model saving directory.
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'VGG19'
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
filepath = os.path.join(save_dir, model_name)


# In[ ]:


from tensorflow.keras.callbacks import ModelCheckpoint

# Prepare callbacks for model saving and for learning rate adjustment.
checkpoint = ModelCheckpoint(filepath=filepath,
                             monitor='val_acc',
                             verbose=1,
                             save_best_only=True)

callbacks = [checkpoint]


# In[ ]:


# Train the model
h = model.fit(
    x=X_train,
    y=y_train,
    validation_split=0.1,
    batch_size=32,
    epochs=40,
    callbacks=callbacks
)


# In[ ]:


model.save('VGG19.h5')


# In[ ]:


model.save_weights('VGG19_w.hdf5')


# In[ ]:


import pickle

f=open('VGG19_h.pckl','wb')
pickle.dump(h.history,f)
f.close()


# In[ ]:


import matplotlib.pyplot as plt
epoch_nums = range(1, 41)
training_loss = h.history["loss"]
validation_loss = h.history["val_loss"]
plt.plot(epoch_nums , training_loss)
plt.plot(epoch_nums , validation_loss)
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(['training','validation'], loc='upper right')
plt.show()


# In[ ]:


scores = model.evaluate(X_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])


# In[ ]:


def testimage(result):
    print(result) 
    if result[0][0]==1: 
        print("Airplane") 
    elif result[0][1]==1: 
        print('Automobile') 
    elif result[0][2]==1: 
        print('Bird') 
    elif result[0][3]==1: 
        print('Cat') 
    elif result[0][4]==1: 
        print('Deer') 
    elif result[0][5]==1: 
        print('Dog') 
    elif result[0][6]==1: 
        print('Frog') 
    elif result[0][7]==1: 
        print('Horse') 
    elif result[0][8]==1: 
        print('Ship') 
    elif result[0][9]==1: 
        print('Truck') 
    else:
        print('Error')


# In[ ]:


import numpy as np
test_image1 =image.load_img("../input/imagetest/Image/horse1.jpg",target_size =(32,32,3))
test_image =image.img_to_array(test_image1)
test_image =np.expand_dims(test_image, axis =0) 
result = model.predict(test_image)
result = result.astype(int)
#result = result.astype(int)
plt.imshow(test_image1)
testimage(result)


# In[ ]:


import numpy as np
test_image1 =image.load_img("../input/imagetest/Image/dog1.jpg",target_size =(32,32,3))
test_image =image.img_to_array(test_image1)
test_image =np.expand_dims(test_image, axis =0) 
result = model.predict(test_image)
result = result.astype(int)
#result = result.astype(int)
plt.imshow(test_image1)
testimage(result)


# In[ ]:


import numpy as np
test_image1 =image.load_img("../input/imagetest/Image/truck1.jpg",target_size =(32,32,3))
test_image =image.img_to_array(test_image1)
test_image =np.expand_dims(test_image, axis =0) 
result = model.predict(test_image)
result = result.astype(int)
#result = result.astype(int)
plt.imshow(test_image1)
testimage(result)


# In[ ]:


import numpy as np
test_image1 =image.load_img("../input/imagetest/Image/airp1.jpg",target_size =(32,32,3))
test_image =image.img_to_array(test_image1)
test_image =np.expand_dims(test_image, axis =0) 
result = model.predict(test_image)
result = result.astype(int)
#result = result.astype(int)
plt.imshow(test_image1)
testimage(result)


# In[ ]:


import numpy as np
test_image1 =image.load_img("../input/imagetest/Image/airp2.jpg",target_size =(32,32,3))
test_image =image.img_to_array(test_image1)
test_image =np.expand_dims(test_image, axis =0) 
result = model.predict(test_image)
result = result.astype(int)
#result = result.astype(int)
plt.imshow(test_image1)
testimage(result)


# In[ ]:


y_pred_test = model.predict(X_test)
y_pred_test_classes = np.argmax(y_pred_test, axis=1)
y_pred_test_max_probas = np.max(y_pred_test, axis=1)


# In[ ]:


cols = 8
rows = 2
NUM_CLASSES = 10
# load data
(x_train2, y_train2), (x_test2, y_test2) = cifar10.load_data()
cifar10_classes = ["airplane", "automobile", "bird", "cat", "deer", 
                   "dog", "frog", "horse", "ship", "truck"]
fig = plt.figure(figsize=(2 * cols - 1, 3 * rows - 1))
for i in range(cols):
    for j in range(rows):
        random_index = np.random.randint(0, len(y_test2))
        ax = fig.add_subplot(rows, cols, i * rows + j + 1)
        ax.grid('off')
        ax.axis('off')
        ax.imshow(x_test2[random_index, :])
        pred_label =  cifar10_classes[y_pred_test_classes[random_index]]
        pred_proba = y_pred_test_max_probas[random_index]
        true_label = cifar10_classes[y_test2[random_index, 0]]
        ax.set_title("pred: {}\nscore: {:.3}\ntrue: {}".format(
               pred_label, pred_proba, true_label
        ))
plt.show()
 

