#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from fastai import *
from fastai.vision import *
import os
print(os.listdir("../input/"))
os.getcwd()


# In[2]:


def decode(num):
    if(num == 0):
        return 9
    elif(num == 1):
        return 0
    elif(num == 2):
        return 7
    elif(num == 3):
        return 6
    elif(num == 4):
        return 1
    elif(num == 5):
        return 8
    elif(num == 6):
        return 4
    elif(num == 7):
        return 3
    elif(num == 8):
        return 2
    elif(num == 9):
        return 5


# In[3]:


path = Path("../input/sign-language-digits-dataset/Sign-language-digits-dataset")
path.ls()


# In[4]:


data = np.load(path/'X.npy')
labels = np.load(path/'Y.npy')
print(data.shape,labels.shape)


# In[5]:


import matplotlib.pyplot as plt
import random
n = random.randint(1, 2000)
plt.imshow(data[n])
print(decode(np.argmax(labels[n])))
print(labels[n])


# In[6]:


import imageio
from skimage import img_as_uint

for i in range(data.shape[0]):
    img = img_as_uint(data[i])
    file_path = "./data/{}/test".format(decode(np.argmax(labels[i])))
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        #print("Made new directory")
    imageio.imwrite('./data/{}/{}.jpg'.format(decode(np.argmax(labels[i])), i), img)


# In[7]:


path = Path("../working/data")
data = ImageDataBunch.from_folder(path, 
                                  train='.',
                                  valid_pct=0.2,
                                  ds_tfms=get_transforms(), size=224, num_workers=6).normalize(imagenet_stats)


# In[8]:


path_m = Path("../input/aslsignmodel")
letter = "K"
learn_tmp = load_learner(path_m)
img = open_image(Path("../input/asl-alphabet-test/asl-alphabet-test/"+letter).ls()
                             [random.randint(1, 5)])
print(learn_tmp.predict(img)[0])
img


# In[9]:


learn = create_cnn(data,models.resnet50, metrics=[accuracy,error_rate])
learn.model[0].load_state_dict(learn_tmp.model[0].state_dict())


# In[10]:


learn.lr_find()
learn.recorder.plot()


# In[11]:


learn.fit_one_cycle(3, slice(1e-3,1e-2))


# In[14]:


learn.save("stage-1")


# In[15]:


path_v = Path("./data/")
num = "2"
img = open_image(Path("./data/"+num).ls()[random.randint(1, 10)])
print(learn.predict(img)[0])
img


# In[16]:


learn.unfreeze()
learn.lr_find()
learn.recorder.plot()


# In[17]:


learn.fit_one_cycle(2, slice(5e-5,9e-5))


# In[18]:


learn.save("stage-2")


# In[19]:


learn.path = Path("/kaggle/working")
learn.export()


# In[27]:


import shutil
print(os.listdir("/kaggle/working/"))
shutil.rmtree("/kaggle/working/data")
print(os.listdir("/kaggle/working/"))


# In[ ]:




