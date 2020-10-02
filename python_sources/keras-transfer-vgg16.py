#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from tqdm import tqdm, tqdm_notebook
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.applications import VGG16
from keras.optimizers import Adam


# In[ ]:


train_dir = "../input/train/train/"
test_dir = "../input/test/test/"
train_df = pd.read_csv('../input/train.csv')
train_df.head()


# In[ ]:


im = cv2.imread("../input/train/train/01e30c0ba6e91343a12d2126fcafc0dd.jpg")
plt.imshow(im)


# In[ ]:


vgg16_net = VGG16(weights='imagenet', 
                  include_top=False, 
                  input_shape=(32, 32, 3))


# In[ ]:


vgg16_net.trainable = False
vgg16_net.summary()


# In[ ]:


model = Sequential()
model.add(vgg16_net)
model.add(Flatten())
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))


# In[ ]:


model.compile(loss='binary_crossentropy',
              optimizer=Adam(lr=1e-5), 
              metrics=['accuracy'])


# In[ ]:


X_tr = []
Y_tr = []
imges = train_df['id'].values
for img_id in tqdm_notebook(imges):
    X_tr.append(cv2.imread(train_dir + img_id))    
    Y_tr.append(train_df[train_df['id'] == img_id]['has_cactus'].values[0])  
X_tr = np.asarray(X_tr)
X_tr = X_tr.astype('float32')
X_tr /= 255
Y_tr = np.asarray(Y_tr)


# In[ ]:


batch_size = 32
nb_epoch = 1000


# In[ ]:


get_ipython().run_cell_magic('time', '', '# Train model\nhistory = model.fit(X_tr, Y_tr,\n              batch_size=batch_size,\n              epochs=nb_epoch,\n              validation_split=0.1,\n              shuffle=True,\n              verbose=2)')


# In[ ]:


with open('history.json', 'w') as f:
    json.dump(history.history, f)

history_df = pd.DataFrame(history.history)
history_df[['loss', 'val_loss']].plot()
history_df[['acc', 'val_acc']].plot()


# In[ ]:


get_ipython().run_cell_magic('time', '', "X_tst = []\nTest_imgs = []\nfor img_id in tqdm_notebook(os.listdir(test_dir)):\n    X_tst.append(cv2.imread(test_dir + img_id))     \n    Test_imgs.append(img_id)\nX_tst = np.asarray(X_tst)\nX_tst = X_tst.astype('float32')\nX_tst /= 255")


# In[ ]:


# Prediction
test_predictions = model.predict(X_tst)


# In[ ]:


sub_df = pd.DataFrame(test_predictions, columns=['has_cactus'])
sub_df['has_cactus'] = sub_df['has_cactus'].apply(lambda x: 1 if x > 0.75 else 0)


# In[ ]:


sub_df['id'] = ''
cols = sub_df.columns.tolist()
cols = cols[-1:] + cols[:-1]
sub_df=sub_df[cols]


# In[ ]:


for i, img in enumerate(Test_imgs):
    sub_df.set_value(i,'id',img)


# In[ ]:


sub_df.head()


# In[ ]:


sub_df.to_csv('submission.csv',index=False)

