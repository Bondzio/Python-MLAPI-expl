#!/usr/bin/env python
# coding: utf-8

# # This notebook calculates shape and aggreagation landscape metrics for melanomas.... only 46 here but over 130 extras features are available..

# # it could capture additional tabular information to use to enhance predictions with NNs.

# In[ ]:


get_ipython().system('conda install -c conda-forge -y pylandstats')
import numpy as np
from pylandstats import *
import matplotlib.pyplot as plt


# In[ ]:


train = np.load("../input/siimisic-melanoma-resized-images/x_train_32.npy", mmap_mode="r")
test = np.load("../input/siimisic-melanoma-resized-images/x_test_32.npy", mmap_mode="r")


# In[ ]:


row=np.random.choice(range(train.shape[0]))
array=train[row,:,:,:]
ch=2
barray=np.where(array[:,:,ch] > np.quantile(array[:,:,ch],0.15), 2, 1)

plt.figure(figsize=(10,5)) 

plt.subplot(1, 2, 1)
plt.imshow(array, cmap=plt.cm.binary)
plt.axis('off')
plt.subplot(1, 2, 2)
plt.imshow(barray, cmap=plt.cm.binary)
plt.axis('off')
plt.subplots_adjust(wspace=-0.1, hspace=-0.1)
plt.show()


# In[ ]:


parray=Landscape(barray, res=(1,1))
LSMetrics=parray.compute_landscape_metrics_df()
parray.plot_landscape()
LSMetrics.head()


# In[ ]:


TrainFeatures=np.zeros((train.shape[0],46,3))

for j in range(train.shape[0]):
  for ch in range(3):
    array=train[j,:,:,ch]
    barray=np.where(array > np.quantile(array,0.15), 2, 1)
    parray=Landscape(barray, res=(1,1))
    LSMetrics=parray.compute_landscape_metrics_df()
    TrainFeatures[j,:,ch]=LSMetrics[0:].values

TestFeatures=np.zeros((test.shape[0],46,3))

for j in range(test.shape[0]):
  for ch in range(3):
    array=test[j,:,:,ch]
    barray=np.where(array > np.quantile(array,0.15), 2, 1)
    parray=Landscape(barray, res=(1,1))
    LSMetrics=parray.compute_landscape_metrics_df()
    TestFeatures[j,:,ch]=LSMetrics[0:].values


# In[ ]:


np.save("trainFeatures.npy", TrainFeatures)
np.save("testFeatures.npy", TestFeatures)

