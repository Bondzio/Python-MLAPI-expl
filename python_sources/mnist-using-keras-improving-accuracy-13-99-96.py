#!/usr/bin/env python
# coding: utf-8

# # Introduction to Computer Vision: MNIST Challenge
# Hi!
# 
# This is a following kernel  my first kernel: https://www.kaggle.com/shaygu/fast-cnn-for-beginners-0-9923
# I tried to push a little bit to get better results. 
# 
# And architecture was inspired by: https://www.kaggle.com/josh24990/recognising-digits-with-keras-top-8-score
# 
# Few conclusions from this attempt:
# 
# From observing the predicted data and reading other discussions\kernels i've learned that some of the data isnt labeled currectly (confusion between labels 1-7, 9-4 or 3-8) so a result of 99.97-99.98 is probably the limit accuracy. The limit can be pushed using the complete data set which is available.
# 
# In my solution I use a lot of parameters (~1 million) and heavy regularization (Dropout,augmantation) one can probably come up with a better solution using less parameters and less regularization. I think its reasonable that a function that takes 28^2 positive values (pixels) and classifies it to 10 classes needs less parameters than that. 
# Using so many parameters I did have to fight overfitting. Alongside regularization I choose to predict on the network that did the best on the evaluation, usually taken from epoch num ~40 from 100 epochs, before the network begin overfitting. Thus, the evaluation size has to be large enough. 
# 
# Other hyper-parameters that were significant are the learning rate decay (or learning rate function) and the batch size. Inreasing the batch size and controlling the learning rate decay changed the graph of loss as a function of epochs. For relative small learning rate decay and batch size of 64 the loss variance was big even for high epoch number. Using large batch size improved the variance a lot and the schedualed learning rate improved the performance. 
# 
# 
# #### Author: Shay Guterman, Hebrew University of Jerusalem: shaygu62@gmail.com
# 

# ## Starting with Kaggle - imporing data 
# 
# Important: Switch settings to GPU

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import tensorflow as tf


# Input data files are available in the "../input/" directory.
import os
print(os.listdir("../input"))
# Any results you write to the current directory are saved as output.

# This is a bit of magic to make matplotlib figures appear inline in the notebook
# rather than in a new window.
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


# ## Importing the data the data

# In[ ]:


from tensorflow.python.keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split

# Import Data
train = pd.read_csv("../input/train.csv")
test= pd.read_csv("../input/test.csv")
print("Train size:{}\nTest size:{}".format(train.shape, test.shape))

# Transform Train and Test into images\labels.
x_train = train.drop(['label'], axis=1).values.astype('float32') # all pixel values
y_train = train['label'].values.astype('int32') # only labels i.e targets digits
x_test = test.values.astype('float32')
x_train = x_train.reshape(x_train.shape[0], 28, 28) / 255.0
x_test = x_test.reshape(x_test.shape[0], 28, 28) / 255.0

x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size = 0.11, random_state=42)

print(x_train.shape)
print(x_val.shape)
print(y_train.shape)
print(x_test.shape)


# ## Visualize some examples from the dataset.
# Showing some example per class

# In[ ]:


# classes for title
# num classes for amount of examples
classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
print(x_train.shape)
num_classes = len(classes)
samples_per_class = 7
plt.figure(0)
for y, cls in enumerate(classes):
    idxs = np.flatnonzero(y_train == y)
    idxs = np.random.choice(idxs, samples_per_class, replace=False)
    for i, idx in enumerate(idxs):
        plt_idx = i * num_classes + y + 1
        plt.subplot(samples_per_class, num_classes, plt_idx)
        # plt.imshow(x_train[idx].astype('uint8'))
        plt.imshow(x_train[idx])
        plt.axis('off')
        if i == 0:
            plt.title(cls)
plt.show()


# ## Adding dimensions for keras

# In[ ]:


x_train = x_train.reshape(x_train.shape[0], 28, 28,1)  
x_val = x_val.reshape(x_val.shape[0], 28, 28,1)  
x_test = x_test.reshape(x_test.shape[0], 28, 28,1) 
print("Train size:{}\nvalidation size:{}\nTest size:{}".format(x_train.shape,x_val.shape, x_test.shape))

mean_px = x_train.mean().astype(np.float32)
std_px = x_train.std().astype(np.float32)


# ## Defining the architecture
# 
# ### Option 1:
# Light architecture with approximately 25K parameters. 
# <br>Dropout for avoiding overfitting
# <br>BatchNormalization for faster convergence time

# In[ ]:


from tensorflow.python.keras.layers import Input , Dense , Conv2D , Activation , Add,ReLU,MaxPool2D,Flatten,Dropout,BatchNormalization
from tensorflow.python.keras.models import Model



input = Input(shape=[28, 28, 1])
x = Conv2D(32, (5, 5), strides=1, padding='same')(input)
# x = BatchNormalization(momentum=0.1, epsilon=1e-5, gamma_initializer='uniform')(x)
x = Activation('relu')(x)
x = Conv2D(32, (5, 5), strides=1, padding='same')(x)
# x = BatchNormalization(momentum=0.1, epsilon=1e-5, gamma_initializer='uniform')(x)
x = Activation('relu')(x)
x = MaxPool2D(pool_size=2, strides=2, padding='same')(x)
x = Dropout (0.3)(x)

x = Conv2D(64, (3, 3), strides=1, padding='same')(x)
# x = BatchNormalization(momentum=0.1, epsilon=1e-5, gamma_initializer='uniform')(x)
x = Activation('relu')(x)
# x = Dropout (0.5)(x)
x = Conv2D(64, (3, 3), strides=1, padding='same')(x)
# x = BatchNormalization(momentum=0.1, epsilon=1e-5, gamma_initializer='uniform')(x)
x = Activation('relu')(x)
x = Conv2D(64, (3, 3), strides=1, padding='same')(x)
# x = BatchNormalization(momentum=0.1, epsilon=1e-5, gamma_initializer='uniform')(x)
x = Activation('relu')(x)

x = MaxPool2D(pool_size=2, strides=2, padding='same')(x)
x = Dropout (0.3)(x)
x = Flatten()(x)
x = Dense(256)(x)
x = Activation('relu')(x)
x = BatchNormalization()(x)
x = Dense(10)(x)
x = Activation('softmax')(x)

model = Model(inputs = input, outputs =x)
print(model.summary())


# ### Defining a class to get access about information after each update

# In[ ]:


class CollectBatchStats(tf.keras.callbacks.Callback):
    def __init__(self):
        self.batch_losses = []
        self.batch_acc = []

    def on_batch_end(self, batch, logs=None):
        self.batch_losses.append(logs['loss'])
        self.batch_acc.append(logs['acc'])

batch_stats = CollectBatchStats()


# ## Train the model using data augmentation

# In[ ]:


from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
from tensorflow.python.keras.optimizers import Adam ,RMSprop


# optimizer = RMSprop(lr=0.001, rho=0.95, epsilon=1e-08, decay=0.0)
epochs = 60
Learning_rate = 0.001
decay= 5 * Learning_rate / epochs
# optimizer = Adam(lr=Learning_rate, decay= 3 * Learning_rate / epochs)
optimizer = RMSprop(lr=Learning_rate, rho=0.9, epsilon=1e-08, decay= 0)


model.compile(optimizer=optimizer,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

#               loss='sparse_categorical_crossentropy',

# Set a learning rate annealer
learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc', 
                                            patience=3, 
                                            verbose=1, 
                                            factor=0.5, 
                                            min_lr=0.0001)

# Data augmentation

aug_num = 12 
datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range= aug_num,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range = aug_num / 100, # Randomly zoom image 
        width_shift_range= aug_num / 100,  # randomly shift images horizontally (fraction of total width)
        height_shift_range= aug_num / 100,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=False,  # randomly flip images horizontally
        vertical_flip=False)  # randomly flip images vertically


datagen.fit(x_train)
# batch_size = 64
batch_size = 256
# Max value lr_min = 0.000125
checkpoint = ModelCheckpoint("best_weights.hdf5", monitor='val_acc', verbose=1, save_best_only=True, mode='max')

history = model.fit_generator(datagen.flow(x_train,y_train, batch_size=batch_size),
                              epochs = epochs, validation_data = (x_val,y_val),
                              verbose = 1, steps_per_epoch=x_train.shape[0] // batch_size,callbacks=[checkpoint,learning_rate_reduction])
model.load_weights("best_weights.hdf5") 


# ## Visualizations

# In[ ]:


plt.figure(1)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Complexity Graph:  Training vs. Validation Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validate'], loc='upper right')

plt.figure(2)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model Accuracy Graph:  Training vs. Validation accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validate'], loc='upper right')
plt.show()


# ## Plotting prediction
# Stright forward taking some images and plotting predictions

# In[ ]:


# predicted class
num_rows = 6
num_cols = 15
sample_size = num_rows * num_cols
indices = np.arange(sample_size)
x_pred = x_test[indices,:,:]
predictions = model.predict(x_pred)
x_pred = np.squeeze(x_test[indices,:,:])
y_pred = np.argmax(predictions,axis=1)

num_images = num_rows*num_cols
plt.figure(figsize=(num_cols*2, num_rows*2))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.6)
for i in range(num_images):
  plt.subplot(num_rows, num_cols, i+1)
  plt.imshow(x_pred[i])
  plt.title(classes[y_pred[i]])
  # plt.subplot(num_rows, 2*num_cols, 2*i+2)
  # plot_value_array(i, predictions, test_labels)
plt.show()


# ## Confusion matrix

# In[ ]:


from sklearn.metrics import confusion_matrix

y_vecs = model.predict(x_val)
y_pred = np.argmax(y_vecs, axis=1)
y_true = y_val
cm = confusion_matrix(y_true, y_pred)
# print(cm)

# plt.imshow(cm, cmap = 'ocean')
# plt.colorbar

min_val, max_val = 0, 15

# intersection_matrix = np.random.randint(0, 10, size=(max_val, max_val))
plt.figure(11)
fig, ax = plt.subplots()
ax.matshow(cm, cmap=plt.cm.Blues)
# ax.matshow(cm, cmap=plt.cm.magma_r)

for i in range(10):
    for j in range(10):
        c = cm[j,i]
        ax.text(i, j, str(c), va='center', ha='center')


plt.xticks(range(10))
plt.yticks(range(10))
plt.title('Confusion matrix',size = 28)
plt.xlabel('True labeling',size = 20)
plt.ylabel('Predicted labeling',size = 20)
plt.rcParams.update({'font.size': 22})


# ## Miss-labeled data

# In[ ]:


# Display some error results 
# y_vecs = model.predict(x_test)
# y_pred = np.argmax(y_vecs, axis=1)
Y_true = y_val
Y_pred_classes =  y_pred
Y_pred = y_vecs
X_val = x_val
# Errors are difference between predicted labels and true labels
errors = (Y_pred_classes - Y_true != 0)

Y_pred_classes_errors = Y_pred_classes[errors]
Y_pred_errors = Y_pred[errors]
Y_true_errors = Y_true[errors]
X_val_errors = X_val[errors]

def display_errors(errors_index,img_errors,pred_errors, obs_errors):
    """ This function shows 6 images with their predicted and real labels"""
    n = 0
    nrows = 2
    ncols = 2
    fig, ax = plt.subplots(nrows,ncols,sharex=True,sharey=True)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=1)
    plt.figure(figsize=(num_cols, num_rows))

    for row in range(nrows):
        for col in range(ncols):
            error = errors_index[n]
            ax[row,col].imshow((img_errors[error]).reshape((28,28)))
            ax[row,col].set_title("Predicted  :{}\nTrue  :{}".format(pred_errors[error],obs_errors[error]), fontsize=14)
            n += 1

# Probabilities of the wrong predicted numbers
Y_pred_errors_prob = np.max(Y_pred_errors,axis = 1)

# Predicted probabilities of the true values in the error set
true_prob_errors = np.diagonal(np.take(Y_pred_errors, Y_true_errors, axis=1))

# Difference between the probability of the predicted label and the true label
delta_pred_true_errors = Y_pred_errors_prob - true_prob_errors

# Sorted list of the delta prob errors
sorted_dela_errors = np.argsort(delta_pred_true_errors)

# Top 6 errors 
most_important_errors = sorted_dela_errors[-25:]

# Show the top 6 errors
display_errors(most_important_errors, X_val_errors, Y_pred_classes_errors, Y_true_errors)


# ## Submission

# In[ ]:


# predict results
results = model.predict(x_test)

# select the indix with the maximum probability
results = np.argmax(results,axis = 1)

results = pd.Series(results,name="Label")

submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),results],axis = 1)

submission.to_csv("MNIST-CNN-ENSEMBLE.csv",index=False)


# ## Save model

# In[ ]:


# model.save('gdrive/My Drive/DL-ML/mnist/2203 995 percent.h5')


# ### Option 2:
# Very Heavy architecture ~300k params per net with ensamble averaging over 15 nets
# Taken Directly from: https://www.kaggle.com/cdeotte/25-million-images-0-99757-mnist

# In[ ]:


# from tensorflow.python.keras.layers import Input , Dense , Conv2D , Activation , Add,ReLU,MaxPool2D,Flatten,Dropout,BatchNormalization
# from tensorflow.python.keras.models import Model
# from tensorflow.python.keras.optimizers import Adam
# from tensorflow.python.keras.callbacks import ReduceLROnPlateau, LearningRateScheduler

# nets = 15; 
# model = [0] *nets
# for j in range(nets):
#     input = Input(shape=[28, 28, 1])
#     x = Conv2D(16, (3, 3), strides=1, padding='same', name='conv1')(input)
#     x = Conv2D(32, kernel_size = 3, activation='relu', input_shape = (28, 28, 1))(x)
#     x = BatchNormalization()(x)
#     x = Conv2D(32, kernel_size = 3, activation='relu')(x)
#     x = BatchNormalization()(x)
#     x = Conv2D(32, kernel_size = 5, strides=2, padding='same', activation='relu')(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.4)(x)

#     x = Conv2D(64, kernel_size = 3, activation='relu')(x)
#     x = BatchNormalization()(x)
#     x = Conv2D(64, kernel_size = 3, activation='relu')(x)
#     x = BatchNormalization()(x)
#     x = Conv2D(64, kernel_size = 5, strides=2, padding='same', activation='relu')(x)
#     x = BatchNormalization()(x)
#     x = Dropout(0.4)(x)

#     x = Conv2D(128, kernel_size = 4, activation='relu')(x)
#     x = BatchNormalization()(x)
#     x = Flatten()(x)
#     x = Dropout(0.4)(x)
#     x = Dense(10, activation='softmax')(x)
    
#     model[j] = Model(inputs = input, outputs =x)
#     # COMPILE WITH ADAM OPTIMIZER AND CROSS ENTROPY COST
#     model[j].compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
# #     print(model[j].summary())
    
# # DECREASE LEARNING RATE EACH EPOCH
# annealer = LearningRateScheduler(lambda x: 1e-3 * 0.95 ** x)
# # TRAIN NETWORKS
# history = [0] * nets
# epochs = 45
# y_binary = to_categorical(y_train)

# for j in range(nets):
#     X_train2, X_val2, Y_train2, Y_val2 = train_test_split(x_train, y_binary, test_size = 0.1)
#     history[j] = model[j].fit_generator(datagen.flow(X_train2,Y_train2, batch_size=64),
#         epochs = epochs, steps_per_epoch = X_train2.shape[0]//64,  
#         validation_data = (X_val2,Y_val2), callbacks=[annealer], verbose=0)
#     print("CNN {0:d}: Epochs={1:d}, Train accuracy={2:.5f}, Validation accuracy={3:.5f}".format(
#         j+1,epochs,max(history[j].history['acc']),max(history[j].history['val_acc']) ))

# # ENSEMBLE PREDICTIONS AND SUBMIT
# results = np.zeros( (X_test.shape[0],10) ) 
# for j in range(nets):
#     results = results + model[j].predict(X_test)
# results = np.argmax(results,axis = 1)
# results = pd.Series(results,name="Label")
# submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),results],axis = 1)
# submission.to_csv("MNIST-CNN-ENSEMBLE.csv",index=False)

