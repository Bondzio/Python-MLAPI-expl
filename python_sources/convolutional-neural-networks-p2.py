#!/usr/bin/env python
# coding: utf-8

# # Importando Librerias

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns 
get_ipython().run_line_magic('matplotlib', 'inline')

np.random.seed(2)

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import itertools

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau
from keras.utils.np_utils import to_categorical # convertir a one-hot-encoding  

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# Cargando la data 

# In[ ]:


train = pd.read_csv("../input/train.csv")
test = pd.read_csv("../input/test.csv")


# In[ ]:


# Guardamos la columna 'label' y la guardamos en la variable Y_train
Y_train = train["label"]

# Le hacemos drop a la columna 'label'
X_train = train.drop(labels = ['label'], axis = 1)

# Liberamos algo de espacio
del train

# Hacemos una grafica donde mostramos la cantidad de observaciones que hay en cada categoria 

g = sns.countplot(Y_train)

Y_train.value_counts()


# Chequeamos la data

# In[ ]:


X_train.isnull().any().describe()


# In[ ]:


test.isnull().any().describe()


# # Normalizacion y Reshape

# In[ ]:


# Normalizamos la data 
X_train = X_train / 255.0
test = test / 255.0


# In[ ]:


# Hacemos Reshape de la imagen en 3 dimensiones (height = 28px, width = 28px, canal = 1)
X_train = X_train.values.reshape(-1, 28, 28, 1)
test = test.values.reshape(-1, 28, 28, 1)


# Encode labels a vectores one hot (ejemplo: 2 -> [0,0,1,0,0,0,0,0,0,0])

# In[ ]:


Y_train = to_categorical(Y_train, num_classes = 10)


# In[ ]:


random_seed = 2


# Dividimos el set de entrenamiento y de validacion para hacer el fit

# In[ ]:


X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size = 0.05, random_state = random_seed)


# Ejemplo:

# In[ ]:


g = plt.imshow(X_train[2][:,:,0])


# # Configuracion de la Red Neuronal Convolucional

# La arquitectura del modelo que vamos a utilizar es: Index -> [[Conv2D -> ReLU]x2 -> MaxPool2D -> Dropout]x2 -> Flatten -> Dense -> Dropout -> Output

# In[ ]:


model = Sequential()

model.add(Conv2D(filters = 32, kernel_size = (5, 5), padding = 'Same', activation = 'relu', input_shape = (28, 28, 1)))
model.add(BatchNormalization())
model.add(Conv2D(filters = 32, kernel_size = (5, 5), padding = 'Same', activation = 'relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(filters = 64, kernel_size = (3, 3), padding = 'Same', activation = 'relu'))
model.add(BatchNormalization())
model.add(Conv2D(filters = 64, kernel_size = (3, 3), padding = 'Same', activation = 'relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size = (2, 2), strides = (2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation = 'relu'))
model.add(Dropout(0.25))
model.add(Dense(10, activation = 'softmax'))


# Definimos el optimizador 

# In[ ]:


optimizer = RMSprop(lr = 0.001, rho = 0.9, epsilon = 1e-08, decay = 0.0)


# Resumen del modelo

# In[ ]:


model.summary()
model.compile(optimizer = optimizer, loss = 'categorical_crossentropy', metrics = ['accuracy'])


# In[ ]:


learning_rate_reduction = ReduceLROnPlateau(monitor = 'val_acc', patience = 3, verbose = 1, factor = 0.5, min_lr = 0.00001)


# In[ ]:


epochs = 30 
batch_size = 86


# In[ ]:


# Creamos mas imagenes con data augmentation para prevenir el overfitting 

datagen = ImageDataGenerator(
        featurewise_center = False,  # set input mean to 0 over the dataset
        samplewise_center = False,  # set each sample mean to 0
        featurewise_std_normalization = False,  # divide inputs by std of the dataset
        samplewise_std_normalization = False,  # divide each input by its std
        zca_whitening = False,  # apply ZCA whitening
        rotation_range = 10,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range = 0.1, # Randomly zoom image 
        width_shift_range = 0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range = 0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip = False,  # randomly flip images
        vertical_flip = False)  # randomly flip images

datagen.fit(X_train)


# Entrenamos el modelo

# In[ ]:


history = model.fit_generator(datagen.flow(X_train, Y_train, batch_size = batch_size), epochs = epochs, validation_data = (X_val, Y_val), 
                              verbose = 2, steps_per_epoch = X_train.shape[0] // batch_size, callbacks = [learning_rate_reduction])


# Graficamos las curvas de perdida y precision para training y validacion

# In[ ]:


fig, ax = plt.subplots(2,1)
ax[0].plot(history.history['loss'], color = 'b', label = "Training loss")
ax[0].plot(history.history['val_loss'], color = 'r', label = "validation loss", axes =ax[0])
legend = ax[0].legend(loc = 'best', shadow = True)

ax[1].plot(history.history['acc'], color = 'b', label = "Training accuracy")
ax[1].plot(history.history['val_acc'], color = 'r',label = "Validation accuracy")
legend = ax[1].legend(loc = 'best', shadow = True)


# Viendo la matriz de confusion

# In[ ]:


def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation = 45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis = 1)[:, np.newaxis]

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# Predecimos los valores desde el set de validacion
Y_pred = model.predict(X_val)
# Convertimos las clases de prediccion a vectores one hot 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convertimos las observaciones de validacion a vectores one hot 
Y_true = np.argmax(Y_val,axis = 1) 
# Computamos la matriz de confusion
confusion_mtx = confusion_matrix(Y_true, Y_pred_classes) 
# Trazamos la matriz de confusion
plot_confusion_matrix(confusion_mtx, classes = range(10)) 


# Predecimos los resultados

# In[ ]:


results = model.predict(test)

# Selecciona el indice con la maxima probabilidad 
results = np.argmax(results,axis = 1)

results = pd.Series(results,name="Label")


# # Hacemos submit de los resultados obtenidos

# In[ ]:


submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),results],axis = 1)

submission.to_csv("submission.csv",index=False)

