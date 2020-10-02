#!/usr/bin/env python
# coding: utf-8

# <h1 style='color:slategray; font-family:Akronim; font-Size:200%;' class='font-effect-fire-animation'> &#x1F310; &nbsp; Python Modules, Styling, Helpful Functions, and Links</h1>
# #### [Github Version](https://github.com/OlgaBelitskaya/deep_learning_projects/blob/master/DL_PP4) & [Colaboratory Version](https://colab.research.google.com/drive/1r5yRD-3tQwN6lSql_VRoVuwQ8DaY5zUt)

# In[ ]:


get_ipython().run_cell_magic('html', '', "<style> \n@import url('https://fonts.googleapis.com/css?family=Akronim|Roboto&effect=3d|fire-animation');\nbody {background-color: gainsboro;} \na,h4 {color:#37c9e1; font-family:Roboto;} \nspan {color:black; text-shadow:4px 4px 4px #aaa;}\ndiv.output_prompt,div.output_area pre {color:slategray;}\ndiv.input_prompt,div.output_subarea {color:#37c9e1;}      \ndiv.output_stderr pre {background-color:gainsboro;}  \ndiv.output_stderr {background-color:slategrey;}       \n</style>")


# In[ ]:


import warnings; warnings.filterwarnings('ignore')
import h5py,cv2,keras as ks,tensorflow as tf
import pandas as pd,numpy as np,pylab as pl
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.callbacks import ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential,load_model,Model
from keras.layers import Input,Activation,Dense,LSTM
from keras.layers import Flatten,Dropout,BatchNormalization
from keras.layers import Conv2D,MaxPooling2D,GlobalMaxPooling2D
from keras.layers import GlobalAveragePooling2D
from keras.layers.advanced_activations import PReLU,LeakyReLU
np.set_printoptions(precision=6)
fw='weights.style.hdf5'
dr2,dr25,dr3,dr5=.2,.25,.3,.5
fr2,fr5,fr8,al=.2,.5,.8,.02
from keras import __version__
print('keras version:', __version__)
print('tensorflow version:', tf.__version__)


# In[ ]:


def ohe(x): 
    return OneHotEncoder(categories='auto')           .fit(x.reshape(-1,1)).transform(x.reshape(-1,1))           .toarray().astype('int64')
def tts(X,y): 
    x_train,x_test,y_train,y_test=    train_test_split(X,y,test_size=.2,random_state=1)
    n=int(len(x_test)/2)
    x_valid,y_valid=x_test[:n],y_test[:n]
    x_test,y_test=x_test[n:],y_test[n:]
    return x_train,x_valid,x_test,y_train,y_valid,y_test
def history_plot(fit_history):
    keys=list(fit_history.history.keys())[6:]
    pl.figure(figsize=(12,10)); pl.subplot(211)
    pl.plot(fit_history.history[keys[0]],
            color='slategray',label='valid 1')
    pl.plot(fit_history.history[keys[1]],
            color='#37c9e1',label='valid 2')
    pl.xlabel("Epochs"); pl.ylabel("Loss")
    pl.legend(); pl.grid(); pl.title('Loss Function')     
    pl.subplot(212)
    pl.plot(fit_history.history[keys[2]],
            color='slategray',label='valid 1')
    pl.plot(fit_history.history[keys[3]],
            color='#37c9e1',label='valid 2')
    pl.xlabel("Epochs"); pl.ylabel("Accuracy")    
    pl.legend(); pl.grid(); pl.title('Accuracy'); pl.show()


# In[ ]:


tpu=tf.distribute.cluster_resolver.TPUClusterResolver()
tf.config.experimental_connect_to_cluster(tpu)
tf.tpu.experimental.initialize_tpu_system(tpu)
tpu_strategy=tf.distribute.experimental.TPUStrategy(tpu)


# <h1 style='color:slategray; font-family:Akronim; font-Size:200%;' class='font-effect-fire-animation'> &#x1F310; &nbsp; Loading and Preprocessing the Data</h1>

# In[ ]:


data=pd.read_csv("../input/style/style.csv")
data.tail()


# In[ ]:


def display_images(img_path,ax):
    img=cv2.imread("../input/style/"+img_path)
    ax.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))    
fig=pl.figure(figsize=(16,4))
for i in range(10):
    ax=fig.add_subplot(2,5,i+1,xticks=[],yticks=[], 
                       title=data['brand_name'][i*218]+\
                       ' || '+data['product_name'][i*218])
    display_images(data['file'][i*218],ax)


# In[ ]:


f=h5py.File('../input/StyleColorImages.h5','r')
keys=list(f.keys())
brands=np.array(f[keys[0]])
images=np.array(f[keys[1]])/255 # normalization
products=np.array(f[keys[2]])


# In[ ]:


gray_images=np.dot(images[...,:3],[.299,.587,.114])
print('Product: ',data['product_name'][100])
print('Brand: ',data['brand_name'][100])
pl.figure(figsize=(3,3))
pl.imshow(gray_images[100],cmap=pl.cm.bone); pl.show()
gray_images=gray_images.reshape(-1,150,150,1)


# In[ ]:


cbrands,cproducts=ohe(brands),ohe(products)
ctargets=np.concatenate((cbrands,cproducts),axis=1)
pd.DataFrame([images.shape,gray_images.shape,
              cbrands.shape,cproducts.shape,ctargets.shape])


# In[ ]:


# Color Images / Multi-Label Target
x_train5,x_valid5,x_test5,y_train5,y_valid5,y_test5=tts(images,ctargets)
# Grayscaled Images / Multi-Label Target 
x_train6,x_valid6,x_test6,y_train6,y_valid6,y_test6=tts(gray_images,ctargets)
y_train5_list=[y_train5[:,:7],y_train5[:,7:]]
y_test5_list=[y_test5[:,:7],y_test5[:,7:]]
y_valid5_list=[y_valid5[:,:7],y_valid5[:,7:]]
y_train6_list=[y_train6[:,:7],y_train6[:,7:]]
y_test6_list=[y_test6[:,:7],y_test6[:,7:]]
y_valid6_list=[y_valid6[:,:7],y_valid6[:,7:]]
sh=[el.shape for el in [x_train5,y_train5,x_valid5,y_valid5,x_test5,y_test5,
 x_train6,y_train6,x_valid6,y_valid6,x_test6,y_test6]]
pd.DataFrame(sh)


# <h1 style='color:slategray; font-family:Akronim; font-Size:200%;' class='font-effect-fire-animation'> &#x1F310; &nbsp;Multi-Label Classification Models</h1>
# We should have an accuracy 
# 
# - greater than 14.3% for the first target (`brand`) and 
# 
# - greater than 10% for the second target (`product`).

# In[ ]:


# Color Images
def mmodel():    
    model_input=Input(shape=(150,150,3))
    x=BatchNormalization()(model_input)
    x=Conv2D(32,(5,5),padding='same')(model_input)
    x=LeakyReLU(alpha=al)(x)
    x=MaxPooling2D(pool_size=(2,2))(x)    
    x=Dropout(dr25)(x)   
    x=Conv2D(256,(5,5),padding='same')(x)       
    x=MaxPooling2D(pool_size=(2,2))(x)    
    x=Dropout(dr25)(x)              
    x=GlobalMaxPooling2D()(x)   
    x=Dense(512)(x)
    x=LeakyReLU(alpha=al)(x)    
    x=Dropout(dr25)(x)     
    y1=Dense(7,activation='softmax')(x)
    y2=Dense(10,activation='softmax')(x)   
    model=Model(inputs=model_input,outputs=[y1,y2])    
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    return model
with tpu_strategy.scope():
    mmodel=mmodel()


# In[ ]:


checkpointer=ModelCheckpoint(filepath=fw,verbose=2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=5,
                               verbose=2,factor=fr8)
estopping=EarlyStopping(monitor='val_loss',patience=25,verbose=2)
history=mmodel.fit(x_train5,y_train5_list,
                   validation_data=(x_valid5,y_valid5_list),
                   epochs=150,batch_size=128,verbose=2,
                   callbacks=[checkpointer,lr_reduction,estopping])


# In[ ]:


history_plot(history)


# In[ ]:


mmodel.load_weights(fw)
scores=mmodel.evaluate(x_test5,y_test5_list)
print("Scores: \n",(scores))
print("The Brand Label. Accuracy: %.2f%%"%(scores[3]*100))
print("The Product Label. Accuracy: %.2f%%"%(scores[4]*100))


# In[ ]:


# Grayscaled Images
def gray_mmodel():    
    model_input=Input(shape=(150,150,1))
    x=BatchNormalization()(model_input)
    x=Conv2D(32,(5,5),padding='same')(model_input)
    x=LeakyReLU(alpha=al)(x)
    x=MaxPooling2D(pool_size=(2,2))(x)    
    x=Dropout(dr25)(x)    
    x=Conv2D(256,(5,5),padding='same')(x)
    x=LeakyReLU(alpha=al)(x)       
    x=MaxPooling2D(pool_size=(2,2))(x)    
    x=Dropout(dr25)(x)             
    x=GlobalMaxPooling2D()(x)    
    x=Dense(1024)(x)
    x=LeakyReLU(alpha=al)(x)   
    x=Dropout(dr25)(x)   
    x=Dense(256)(x)
    x=LeakyReLU(alpha=al)(x)    
    x=Dropout(dr25)(x)    
    y1=Dense(7,activation='softmax')(x)
    y2=Dense(10,activation='softmax')(x)       
    model=Model(inputs=model_input,outputs=[y1,y2])
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',metrics=['accuracy'])   
    return model
with tpu_strategy.scope():
    gray_mmodel=gray_mmodel()


# In[ ]:


checkpointer=ModelCheckpoint(filepath=fw,verbose=2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=5,
                               verbose=2,factor=fr5)
estopping=EarlyStopping(monitor='val_loss',patience=25,verbose=2)
history=gray_mmodel.fit(x_train6,y_train6_list,
                        validation_data=(x_valid6,y_valid6_list),
                        epochs=150,batch_size=128,verbose=2,
                        callbacks=[checkpointer,lr_reduction,estopping])


# In[ ]:


history_plot(history)


# In[ ]:


gray_mmodel.load_weights(fw)
scores=gray_mmodel.evaluate(x_test6,y_test6_list)
print("Scores: \n",(scores))
print("The Brand Label. Accuracy: %.2f%%"%(scores[3]*100))
print("The Product Label. Accuracy: %.2f%%"%(scores[4]*100))

