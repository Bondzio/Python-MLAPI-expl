#!/usr/bin/env python
# coding: utf-8

# **Importing packages**

# In[ ]:


import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
import torch.nn.functional as F


# **Inputs & Targets**

# In[ ]:


inputs = np.array([[73, 67, 43], [91, 88, 64], [87, 34, 58], 
                   [20, 43, 37], [69, 96, 70], [73, 67, 43], 
                   [91, 88, 64], [87, 34, 58], [12, 43, 37], 
                   [69, 96, 70], [73, 67, 43], [91, 88, 64], 
                   [87, 14, 58], [12, 43, 37], [69, 96, 70]], 
                  dtype='float32')
targets = np.array([[0.0], [1.0], [0.0], 
                    [0.0], [1.0], [0.0], 
                    [1.0], [0.0], [1.0], 
                    [1.0], [0.0], [1.0], 
                    [0.0], [0.0], [1.0]], 
                   dtype='float32')
targets = torch.from_numpy(targets)
inputs = torch.from_numpy(inputs)


# **Defining a model**

# In[ ]:


model = nn.Linear(3, 1)
print(model.weight)
print(model.bias)


# In[ ]:


preds = model(inputs)
print(preds)


# In[ ]:


loss_fn = F.mse_loss
loss = loss_fn(model(inputs), targets)
print(loss)


# In[ ]:


opt = torch.optim.SGD(model.parameters(), lr=0.00001)


# In[ ]:


def fit(num_epochs, model, loss_fn, opt):
    
    # Repeat for given number of epochs
    for epoch in range(num_epochs):
        # 1. Generate predictions
        pred = model(inputs)
            
            # 2. Calculate loss
        loss = loss_fn(pred, targets)
            
            # 3. Compute gradients
        loss.backward()
            
            # 4. Update parameters using gradients
        opt.step()
            
            # 5. Reset the gradients to zero
        opt.zero_grad()
        
        # Print the progress
        if (epoch+1) % 10 == 0:
            
            print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss.item()))


# *Calculating the loss***

# In[ ]:


fit(900000, model, loss_fn, opt)


# In[ ]:


preds=model(inputs)


# **Lets check the predicted values**

# In[ ]:


print(targets)#/to be predicted
print(preds) #predicted


# **Since the input is a small dataset the predicted values are nearly equal to the target values, but not excatly the same. **
