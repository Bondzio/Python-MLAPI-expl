#!/usr/bin/env python
# coding: utf-8

# # Progressive resizing | Deatailed walkthrough of the code | Training the whole architecture
# * Trained only 2 epochs and acheived 90%+ accuracy
# * Have used 64x64 res images and 256x256 res images, feel free to fiddle around this to add more such changes or trying different resolutions

# ### Importing fastai

# In[ ]:


from fastai import *
from fastai.vision import *


# ### Browsing the Dataset Structure

# In[ ]:


get_ipython().system('pwd #current directory')


# In[ ]:


get_ipython().system('ls ../')


# In[ ]:


get_ipython().system('ls ../input')


# In[ ]:


get_ipython().system('ls ../input/train')


# In[ ]:


get_ipython().system('ls ../input/train/train')


# In[ ]:


get_ipython().system('ls ../input/train/train | wc -l #number of classes in train set')


# In[ ]:


get_ipython().system('ls ../input/test')


# In[ ]:


get_ipython().system('ls ../input/test/test | wc -l #number of images in dataset')


# Thus this is the structure of the dataset
# ![struc.jpeg](attachment:struc.jpeg)

# ### Loading the data to fastai 
# * From the last section we know the strcuture of our dataset
# * We shall use the data_block api, you can find about it [here](https://docs.fast.ai/data_block.html) and how they expect the file structure to be if you're using `from_folder`

# In[ ]:


path = Path('../input') #parent path

#low res data
data_64 = (ImageList.from_folder(path/'train') #have specified the train directory as it has a child dir named train which contains all the classes in folders
                .split_by_rand_pct(0.1, seed=33) #since there is no validation set, we are taking 10% of the train set as validation set
                .label_from_folder()#to label the images based on thier folder name/class
                .add_test_folder('..'/path/'test')#came out of the current directory and specified where test set is at, as it doesnt follow the imagenet style of file structure
                .transform(get_transforms(), size=64)#using the default transforms and initial size of 64x64
                .databunch(bs=256)#batch size of 256, be cautious of OOM error when you increase the size of the image decrease the batchsize to be able to fit in the memory
                .normalize(imagenet_stats))#normalizing to the imagenet stats

#high res data
data_256 = (ImageList.from_folder(path/'train')
                .split_by_rand_pct(0.1, seed=33)
                .label_from_folder()
                .add_test_folder('..'/path/'test')
                .transform(get_transforms(), size=256)
                .databunch(bs=64)
                .normalize(imagenet_stats))


# In[ ]:


data_64 #verifying the no. of images, split of different sets and you can observe test has no labels


# In[ ]:


data_64.c #verifying the no. of classes


# ### Model | Trasnfer Learning

# In[ ]:


learn = cnn_learner(data_64, #training on low res first 
                    models.resnet18, #loading the resenet18 arch with pretrained weights
                    metrics=accuracy, 
                    model_dir='/tmp/model/') #specifying a different directory as /input is a read-only directory and will throw an error while using lr_find()


# Finding the best LR to train on is a important step, as it'll help you converge faster without overshooting.
# 
# Choosing 1e-2(10^-2) as the LR as there is a steep drop in loss.

# In[ ]:


learn.lr_find() #finds the change in loss with respect to the learning rate
learn.recorder.plot()#plots that change


# In[ ]:


learn.fit_one_cycle(1, 1e-2)


# ### Unfreezing | Resizing 
# * Considering the model has beem trained on apt amount of epochs we can now unfreeze the initial layers, to update thier weights 
# * Using of high res images now, allowing the model to learn more features

# In[ ]:


learn.data = data_256 #loading the high res images
learn.unfreeze() #unfreezing the inital layers


# In[ ]:


learn.lr_find()
learn.recorder.plot()


# Using slice to provide the initial layers with lower LR so as to not to change much of its weights

# In[ ]:


learn.fit_one_cycle(1, slice(1e-4,1e-3))

