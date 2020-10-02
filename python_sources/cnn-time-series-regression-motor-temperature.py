#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data

from sklearn.preprocessing import MinMaxScaler

torch.manual_seed(2)
np.random.seed(2)


# In[ ]:


df = pd.read_csv("../input/electric-motor-temperature/pmsm_temperature_data.csv")


# In[ ]:


df.head()


# In[ ]:


col_list = df.columns.tolist()
profile_id = ['profile_id']
target_list = ['pm', 'torque', 'stator_yoke', 'stator_tooth', 'stator_winding']
feature_list = [col for col in col_list if col not in target_list and col not in profile_id]


# ##### As explained in the description the profile_id column in the data set corresponds to different measurement sessions. The most interesting target features given in description are rotor temperature('pm), stator temperatures('stator_*) and torque. 
# ##### All the other features are considered to be inputs features

# In[ ]:


col_list = df.columns.tolist()
profile_id = ['profile_id']
target_list = ['pm', 'torque', 'stator_yoke', 'stator_tooth', 'stator_winding']
feature_list = [col for col in col_list if col not in target_list and col not in profile_id]


# In[ ]:


df.info()


# ##### As profile id just indicates which measurement session the data belongs to, it can be treated as categorical variable, and also to make select data that is relevant to the session

# In[ ]:


df['profile_id'] = df.profile_id.astype('category', inplace=True)
df.profile_id.unique()


# Dividing the data based on the profile id

# In[ ]:


df_dict = {}
for id_ in df.profile_id.unique():
    df_dict[id_] = df[df['profile_id']==id_].reset_index(drop = True)


# ### Since all the variables/features are measured over time and are time dependant. The later analysis is done assuming the data to be time series data.
# 
# #### For this reason, the data is split into number of time sequences. The target value for a given sequence will be the value which is just after a given sequence.

# In[ ]:


def build_sequences(features_df, target_df, sequence_length = 10):
    """Builds sequences from data and converts them into pytorch tensors
        sequence_length - represents the number of samples to be considered in a sequence
    """
    data_ = []
    target_ = []
    
    for i in range(int(features_df.shape[0]/sequence_length)):
        
        data = torch.from_numpy(features_df.iloc[i:i+sequence_length].values)
        target = torch.from_numpy(target_df.iloc[i+sequence_length+1].values)
        
        data_.append(data)
        target_.append(target)
        
    data = torch.stack(data_)
    target = torch.stack(target_)
    
    return data, target


# In[ ]:


prof_ids = list(df_dict.keys())
df_dict.keys()


# ###### Slecting a measurement profile to prepare the data

# In[ ]:


# Randomly selecting
# idx = np.random.randint(len(list(df_dict.keys())))

# prof_id = prof_ids[idx]
# print('Selected profile -',prof_id)

### OR ###
# Manual Selection
prof_id = 6

curr_df = df_dict[prof_id]

curr_df = curr_df.drop('profile_id', axis = 1)
columns = curr_df.columns.tolist()


# In[ ]:


scaler = MinMaxScaler()

curr_df = pd.DataFrame(scaler.fit_transform(curr_df), columns= columns)
curr_df.head()


# ### Sequence length has to be selected prior to the model initialization
# 
# ##### As the sampling is done at 2 Hz, the sequence size can be >= 2. But, keeping in view the importance of speed of operation as the values are needed for other operations or control, it should be as small as possible to reduce the delay.
# 
# ##### Also, another point to be noted here is, if the sequence length is higher the prediction error is less. So there must be a trade off between the required error rate and speed (in this case the initial prediction). 
# 
# ##### The delay in responce will be only at the beginning and the later predictions will not have the delay if real time operation is considered.

# In[ ]:


sequence_length = 3

features = curr_df[feature_list]
target = curr_df[target_list][['pm']]

data, target = build_sequences(features, target, sequence_length=sequence_length)


# ##### Dividing the generated sequences into training and testing set

# In[ ]:


# Test size the percentage of data to be used for testing
test_size = 0.05

indices = torch.randperm(data.shape[0])

train_indices = indices[:int(indices.shape[0] * (1-test_size))]
test_indices = indices[int(indices.shape[0] * (1-test_size)):]

X_train, y_train = data[train_indices], target[train_indices]
X_test, y_test = data[test_indices], target[test_indices]


# ##### A Dataset class is needed for the data inorder to use the dataloader of Pytorch

# In[ ]:


class PMSMDataset(torch.utils.data.dataset.Dataset):
    """Dataset with Rotor Temperature as Target"""
    def __init__(self, data, target):
        
        self.data = data
        self.target = target
        
    def __len__(self):
        return self.data.shape[0]
    
    def __getitem__(self, idx):
        return self.data[idx].unsqueeze(0), self.target[idx]


# In[ ]:


batch_size = 10

pm_train_dataset = PMSMDataset(X_train, y_train)
pm_train_loader = torch.utils.data.dataloader.DataLoader(pm_train_dataset, batch_size= batch_size)

pm_test_dataset = PMSMDataset(X_test, y_test)
pm_test_loader = torch.utils.data.dataloader.DataLoader(pm_test_dataset, batch_size= 1)


# ##### The network 

# In[ ]:


class Network(nn.Module):
    def __init__(self, sequence_length, n_features):
        super(Network, self).__init__()
        
        
        self.conv1 = nn.Conv1d(1, 3, kernel_size=(sequence_length, n_features))
        
        self.lin_in_size = self.conv1.out_channels * int(((sequence_length - (self.conv1.kernel_size[0]-1) -1)/self.conv1.stride[0] +1))
        
#         print(self.lin_in_size)
        
        self.fc1 = nn.Linear(self.lin_in_size,30)
        self.fc2 = nn.Linear(30, 1)
        
    def forward(self, x):
        
        x = F.relu(self.conv1(x))
        x = x.view(-1, self.lin_in_size)
        
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        
        return x


# ##### Note that the same sequence length used to generate the data should be used to create the network

# In[ ]:


n_features = X_train.shape[-1]

net = Network(sequence_length, n_features).double()
net


# In[ ]:


lr = 0.001

criterion = nn.MSELoss()
optimizer = optim.Adam(net.parameters(), lr=lr)


# ### Training

# In[ ]:


training_losses = []
for epoch in range(50):
    running_loss = 0.0
    batch_losses = []
    for i, (data, target) in enumerate(pm_train_loader):

        optimizer.zero_grad()

        out = net(data)

        loss = criterion(out, target)
        batch_losses.append(loss.item())

        loss.backward()
        optimizer.step()            
    training_losses.append(np.mean(batch_losses))
    print("Epoch {}, loss {:.6f}".format(epoch+1, training_losses[-1]))


# In[ ]:


plt.plot(training_losses)


# ### Testing

# In[ ]:


losses = []
batch_losses = []
targets = []
outputs = []
with torch.no_grad():
    for i, (data, target) in enumerate(pm_test_loader):
        out = net(data)
        loss = criterion(out, target)
#         print('Target : {:.4f}, Predicted Output : {:.4f}'.format(target.item(), out.item()))
        
        targets.append(target.item())
        outputs.append(out.item())
        
        batch_losses.append(loss.item())
    losses.append(np.mean(batch_losses))
print("Testing loss {:.6f}".format(losses[-1]))


# In[ ]:


plt.figure(figsize=(13,7))
# plt.scatter(np.arange(len(outputs)),outputs, c = 'b', s = 15, marker='*', label = 'predicted')
plt.plot(np.arange(len(outputs)),outputs, alpha = 0.8, marker = '.',label = 'predicted' )
plt.scatter(np.arange(len(targets)),targets, c = 'r', s = 15, label = 'true')
plt.legend(loc='best')


# In[ ]:




