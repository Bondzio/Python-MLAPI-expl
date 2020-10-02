#!/usr/bin/env python
# coding: utf-8

# This was obtained by extracting the face of the first frame of the videos, the putting reals and fakes side by side.

# In[ ]:


import pandas as pd

metadata = pd.read_csv('../input/deepfake-faces/metadata.csv')
metadata = metadata.replace({'.mp4$': '.jpg'}, regex=True)
metadata


# ## Reals on the left, fakes on the right

# In[ ]:


import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
                                                                                                  
path = '../input/deepfake-faces/faces_155/'

for row in metadata.head(100).itertuples():
    if row.label == 'REAL':
        continue
    
    f, axarr = plt.subplots(1,2, figsize=(6,3))
    
    try:
        real = plt.imread(path + row.original)
        axarr[0].imshow(real)
    except:
        pass
    
    fake = plt.imread(path + row.videoname) 
    axarr[1].imshow(fake)
    
    

