#!/usr/bin/env python
# coding: utf-8

# ### Detecting the boneage from X-Ray images 

# This is my first ever Public kernal in Kaggle Community and I referred these great kernals. 
# https://www.kaggle.com/kmader/attention-on-pretrained-vgg16-for-bone-age
# 
# https://www.kaggle.com/jackbyte/predict-age-from-x-rays-selfmade-cnn

# ### Thanks to DanB for his deep learning kaggle tutorials, they helped me a lot.**

# The Boneage prediction is a regressive model, I tried with many pre-trained models like VGG, MobileNet, InceptionNet. Batchsize plays a major role and my 8GB RAM is crashing when i use batchsize 512in train test split. 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
#for dirname, _, filenames in os.walk('../input'):
    #for filename in filenames:
        #print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow import keras

rsna_df = pd.read_csv("../input/rsna-bone-age/boneage-training-dataset.csv")


# In[ ]:


base_bone_dir = '../input/rsna-bone-age/'
rsna_df['path'] = rsna_df['id'].map(lambda x: os.path.join(base_bone_dir,
                                                         'boneage-training-dataset', 
                                                         'boneage-training-dataset', 
                                                          '{}.png'))
#rsna_df['imagepath'] = [f'{pid}.png' for pid in rsna_df.id]
rsna_df['imagepath'] = rsna_df['id'].map(lambda x: '{}.png'.format(x))
rsna_df.head()
bone_age_mean = rsna_df['boneage'].mean()
bone_age_dev = 2 * rsna_df['boneage'].std()
bone_age_std = rsna_df['boneage'].std()
rsna_df['bone_age_zscore'] = rsna_df.boneage.map(lambda x: (x - bone_age_mean)/bone_age_dev)
# we take the mean , dev as 0 and 1
#bone_age_mean = 0
#bone_age_dev = 1.0
rsna_df['bone_age_float'] = rsna_df.boneage.map(lambda x: (x - 0.)/1.)
rsna_df.dropna(inplace = True)
rsna_df.head(5)


# In[ ]:


rsna_df['gender'] = rsna_df['male'].map(lambda x: 'male' if x else 'female')
rsna_df.head()
import seaborn as sns
gender = sns.countplot(rsna_df['gender'])
rsna_df['sex'] = rsna_df['gender'].map(lambda x: 1 if x=='male' else 0)
rsna_df.head()


# In[ ]:


X = pd.DataFrame(rsna_df[['id','bone_age_float','imagepath','bone_age_zscore']])


# In[ ]:


Y = pd.DataFrame(X['bone_age_zscore'])


# In[ ]:


from pathlib import Path
train_img_path = Path('../input/rsna-bone-age/boneage-training-dataset/boneage-training-dataset/')
#test_img_path = Path('../input/rsna-bone-age/boneage-test-dataset/boneage-test-dataset/')


# **BUILD MODEL**

# In[ ]:


from sklearn.model_selection import train_test_split
x_train,    x_test,  y_train, y_test = train_test_split(X,Y, 
                                   test_size = 0.2, 
                                   random_state = 2020,
                                   )
print(' x train', x_train.shape[0], 'x validation', x_test.shape[0])
print('y train', y_train.shape[0], 'y validation', y_test.shape[0])


# In[ ]:


#For training  i have taken only these records
#x_train = x_train.head(9600)
#x_test = x_train.tail(3000)
#y_train = y_train.head(9600)
#y_test = y_train.tail(3000)


# ***mobile net V2***

# In[ ]:


import matplotlib.pyplot as plt
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
import tensorflow as tf


# In[ ]:


tf.keras.backend.clear_session()


# In[ ]:


img_rows = 224
img_cols = 224

datagen=ImageDataGenerator(rescale=1./255, rotation_range=20, zoom_range=0.15,
                           width_shift_range=0.2, height_shift_range=0.2, shear_range=0.15,
                           horizontal_flip=True, vertical_flip = False, fill_mode="nearest"
                           )

train_gen_mnet=datagen.flow_from_dataframe(dataframe=x_train,
                                            #directory=train_img_path,
                                            directory="../input/rsna-bone-age/boneage-training-dataset/boneage-training-dataset/", 
                                            x_col='imagepath', 
                                            y_col= 'bone_age_zscore', 
                                            class_mode = 'raw',
                                            color_mode = 'rgb',
                                            target_size = (img_rows, img_cols), 
                                            batch_size=64)
valid_gen_mnet=datagen.flow_from_dataframe(dataframe=x_test,
                                            #directory=train_img_path,
                                            directory="../input/rsna-bone-age/boneage-training-dataset/boneage-training-dataset/", 
                                            x_col='imagepath', 
                                            y_col= 'bone_age_zscore', 
                                            class_mode = 'raw',
                                            color_mode = 'rgb',
                                            target_size = (img_rows, img_cols), 
                                            batch_size=64)


# In[ ]:


STEP_SIZE_TRAIN=np.ceil(train_gen_mnet.n//train_gen_mnet.batch_size)
STEP_SIZE_VALID=np.ceil(valid_gen_mnet.n//valid_gen_mnet.batch_size)


# In[ ]:


print (STEP_SIZE_TRAIN, STEP_SIZE_VALID)


# In[ ]:


train_img_mnet, train_lbl_mnet = next(train_gen_mnet)
valid_img_mnet, valid_lbl_mnet = next(valid_gen_mnet)


# In[ ]:


train_img_mnet.shape


# In[ ]:


train_X, train_Y = next(datagen.flow_from_dataframe(dataframe=x_train, 
                                            directory="../input/rsna-bone-age/boneage-training-dataset/boneage-training-dataset/", 
                                            #directory=train_img_path,
                                            x_col='imagepath', 
                                            y_col='bone_age_zscore', 
                                            class_mode = 'raw',
                                            color_mode = 'rgb',
                                            target_size=(224, 224), 
                                            batch_size=1024))


# In[ ]:


train_X.shape


# In[ ]:


base_model=MobileNet(input_shape =  train_img_mnet.shape[1:],weights='imagenet',include_top=False) #imports the mobilenet model and discards the last 1000 neuron layer.

base_mobilenet_model=base_model.output
base_mobilenet_model=GlobalAveragePooling2D()(base_mobilenet_model)
base_mobilenet_model=Dense(1024,activation='relu')(base_mobilenet_model) #we add dense layers so that the model can learn more complex functions and classify for better results.
base_mobilenet_model=Dense(1024,activation='relu')(base_mobilenet_model) #dense layer 2
base_mobilenet_model=Dense(512,activation='relu')(base_mobilenet_model) #dense layer 3
output1=Dense(1,activation='linear')(base_mobilenet_model) #final layer with linear activation


# In[ ]:


rsna_mobilenet=Model(inputs=base_model.input,outputs=output1)
#specify the inputs
#specify the outputs
#now a model has been created based on our architecture
for i,layer in enumerate(rsna_mobilenet.layers):
  print(i,layer.name)
for layer in rsna_mobilenet.layers:
    layer.trainable=False
# or if we want to set the first 20 layers of the network to be non-trainable
for layer in rsna_mobilenet.layers[:20]:
    layer.trainable=False
for layer in rsna_mobilenet.layers[20:]:
    layer.trainable=True


# In[ ]:


rsna_mobilenet.compile(optimizer = 'adam', loss = 'mse',
                           metrics = ['mae'])

rsna_mobilenet.summary()


# ****Set Hyperparameter and Start training
# 
# #### Adam optimizer
# #### Using mse as loss function****

# In[ ]:


from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau
weight_path="{}_mnet_weights.h5".format('bone_age')
checkpoint = ModelCheckpoint(weight_path, monitor='val_loss', verbose=1, 
                             save_best_only=True, mode='min', save_weights_only = True)


reduceLROnPlat = ReduceLROnPlateau(monitor='val_loss', factor=0.8, patience=2, verbose=1, mode='auto', min_delta=0.01, cooldown=3, min_lr=0.01)
early = EarlyStopping(monitor="val_loss", 
                      mode="min", 
                      patience=3) # probably needs to be more patient
callbacks_list = [checkpoint, early, reduceLROnPlat]


# In[ ]:


history_mobilenet = rsna_mobilenet.fit_generator( generator=train_gen_mnet,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_gen_mnet,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=10
                    ,callbacks = callbacks_list)


# ### Learning / Inferences
# 1. Try with different test-train split ratio.(90:10, 80:20,70:30 etc)
# 2. Image pre-processing plays a vital role, try with different augmentation types like flipping , rotating, reducing the size of the image
# 3. Train with different batch sizes
# 4. While using transfer learning , always use pre-trained weights
# 5. Play with learning rate
# 6. Try Changing the output layer activation function from sigmoid to linear for regression problems
# 7. Use early stopping to save training time
# 8. Use batch normalization, drop-outs during model building to avoid overfitting or underfitting issue
# 9. Play with Epochs, train-valid batch sizes for better model learning
# 10. Adam is the mostly used optimizer, SGD and AdaGrad, RAdam are other better options.
# 11. Relu/TanH is the activation function used in other layers
# 12. mse, mae ,rmse are used for regressive models wheras acc is measured for classification problems
# 13. In model compile, other than std metrics, userdefined metrics can be used.
# 14. It is always better to mormalize the x values, ((x-mean(x))/std(x))
# 15. Complex problems , ensampling techniques are preferred
# * Split data into Grp A, B
# * Feed data to Models X and Y
# * Take the combined result of X and Y and feed to model Z

# * **Validation loss went down to 0.06031, when lr=0.01 and 'linear' function used at the output layer with batch size of 64 and train data split at 9:1 ratio

# In[ ]:


mae = history_mobilenet.history['mae']
val_mae = history_mobilenet.history['val_mae']

loss = history_mobilenet.history['loss']
val_loss = history_mobilenet.history['val_loss']
epochs = 6
epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, mae, label='Training MAE ')
plt.plot(epochs_range, val_mae, label='Validation MAE ')
plt.legend(loc='lower right')
plt.title('Training and Validation MAE')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()


# ![image.png](attachment:image.png)
# 
# 
# val_loss improved from 0.13853 to 0.06031, saving model to bone_age_mnet_weights.h5

# **val_pred_Y - Prediction by model
# 
# val_Y_months - Actual Y from df converted to months since our model takes zscore of Y**

# In[ ]:


#print ( (rsna_mobilenet.evaluate(valid_gen_mnet, verbose = 0))*100)


# In[ ]:


from keras.models import Model
import keras.backend as K


# In[ ]:


rsna_mobilenet.load_weights(weight_path)


# In[ ]:


val_pred_Y = (bone_age_dev*rsna_mobilenet.predict(train_X, batch_size = 64, verbose = True))+bone_age_mean
val_Y_months = (bone_age_dev*train_Y)+bone_age_mean


# In[ ]:


rand_idx = np.random.choice(range(train_X.shape[0]), 80)
fig, m_axs = plt.subplots(20, 4, figsize = (14, 30))
for (idx, c_ax) in zip(rand_idx, m_axs.flatten()):
    c_ax.imshow(train_X[idx, :,:,0], cmap = 'bone')
    c_ax.set_title('\n\nActual (Prediction) : %2.1f (%2.1f)' % (val_Y_months[idx], val_pred_Y[idx]))
    c_ax.axis('off')


# In[ ]:


fig, ax1 = plt.subplots(1,1, figsize = (10,10))
ax1.plot(val_Y_months, val_pred_Y, 'r.', label = 'predictions')
ax1.plot(val_Y_months, val_Y_months, 'b-', label = 'actual')
ax1.legend()
ax1.set_xlabel('Actual Age (Months)')
ax1.set_ylabel('Predicted Age (Months)')


# ![image.png](attachment:image.png)

# ### Let's change the batchsize from 256 to 64 , the prediction improves 
# 
# 
# ![image.png](attachment:image.png)

# In[ ]:


# evaluate the model
_, train_acc = rsna_mobilenet.evaluate(train_gen_mnet)
_, valid_acc = rsna_mobilenet.evaluate(valid_gen_mnet)
print('Train: %.3f, Validation: %.3f' % (train_acc, valid_acc))


# **Mobile net with 5 epochs, BS 64 resulted in val loss of 0.06 and acc of 0.254, 0.256 **

# ***TEST / PREDICT the model*

# In[ ]:


test_df = pd.read_csv("../input/rsna-bone-age/boneage-test-dataset.csv")


# In[ ]:


test_df.head()


# In[ ]:


test_df.shape


# In[ ]:


test_img_path = ('../input/rsna-bone-age/boneage-test-dataset/')


# In[ ]:


test_images = os.listdir(test_img_path)
#print(len(test_images), 'test images found')


# ### Use the below snippet to preprocess image of test dataset to be predicted

# In[ ]:


pred_datagen = ImageDataGenerator(rescale=1./255)
pred_generator = pred_datagen.flow_from_directory(
        str(test_img_path),#"../input/rsna-bone-age/boneage-test-dataset/boneage-test-dataset/",
        target_size=(224, 224),
        batch_size=10,
        class_mode='sparse',
        color_mode ='rgb',
        shuffle=False)


# In[ ]:


_, pred_acc = rsna_mobilenet.evaluate(pred_generator)


# In[ ]:


print('Test: %.3f' % (pred_acc))


# In[ ]:


img_batch = next(pred_generator)


# In[ ]:


pred=rsna_mobilenet.predict_generator(pred_generator, steps=len(pred_generator), verbose=1)


# In[ ]:


# Get classes by np.round
cl = np.round(pred)
# Get filenames (set shuffle=false in generator is important)
filenames=pred_generator.filenames


# ## Since I used bone_age_mean and bone_age_std to find zscore, the following code must be applied to return the bone age in months

# In[ ]:


y_months = (pred[:,0]*41.18 + 127.32).astype(int)


# In[ ]:


y_months


# In[ ]:


# Data frame
results=pd.DataFrame({"file":filenames,"prediction":y_months})


# In[ ]:


results.head(20)


# In[ ]:


results.to_csv("boneage_testdata_predict.csv")


# In[ ]:


test_df.insert(2, "Boneage",y_months, True)


# In[ ]:


test_df.head()


# ### Please upvote if you like the kernal, Thank you.
