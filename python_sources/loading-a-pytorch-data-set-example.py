#!/usr/bin/env python
# coding: utf-8

# ### Importing libraries

# In[ ]:


import torch 
import pandas 
from torch.utils.data import Dataset


# ### How to Load a Dataset

# In[ ]:


class MushroomDataset(Dataset):
    def __init__(self):
        '''Load up the data
        '''
        self.data = pandas.read_csv('../input/mushroom-classification/mushrooms.csv')
        
    def __len__(self):
        '''How much data do we have?
        '''
        return len(self.data)
    
    def __getitem__(self, idx):
        '''Grab one data sample
        
        Args:
            idx {int} -- get the data at this indx
        '''
        if type(idx) is torch.Tensor:
            idx = idex.item()
        return self.data.iloc[idx][1:], self.data.iloc[idx][0:1]


# In[ ]:


mushrooms = MushroomDataset()
len(mushrooms), mushrooms[0]


# ### Separate in a train test

# In[ ]:


num_for_testing = int(len(mushrooms) * 0.05)
number_for_training = len(mushrooms) - num_for_testing
train, test = torch.utils.data.random_split(mushrooms,
                                           [number_for_training, num_for_testing])
len(test), len(train)


# In[ ]:


test[0]

