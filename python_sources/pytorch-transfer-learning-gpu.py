#!/usr/bin/env python
# coding: utf-8

# thanks to @abhishek brother and @xhlulu as i borrowed a lot of code from them,without kaggler like them i am nothing in kaggle. have been learning a lot from them since last 1+ year. 

# # ChangeLog
# * v1. Training for 7 epochs because i have ~6 hours gpu quota left now (model resnet101 of torchvision)
# * v2. MSELoss - 10 epoch (forcefully stopped training because of version 3 attempt)
# * v3. Adding sigmoid during inference
# * v4. inferencing by solving inference issue of v3
# 
# 
# 
# * Fork - changed to use pretrained model + more image augmentation

# # Import libraries and utility scripts

# In[ ]:


import os


import torch

import warnings

import pandas as pd
import numpy as np
import torch.nn as nn

from sklearn.model_selection import train_test_split

from sklearn import metrics
from transformers import AdamW
from transformers import get_linear_schedule_with_warmup

import time
import torchvision
import torch.nn as nn
from tqdm import tqdm_notebook as tqdm

from PIL import Image, ImageFile
from torch.utils.data import Dataset
import torch
import torch.optim as optim
from torchvision import transforms
from torch.optim import lr_scheduler
import os
warnings.filterwarnings("ignore")


# In[ ]:


BASE_PATH = "/kaggle/input/alaska2-image-steganalysis"
train_imageids = pd.Series(os.listdir(BASE_PATH + '/Cover')).sort_values(ascending=True).reset_index(drop=True)
test_imageids = pd.Series(os.listdir(BASE_PATH + '/Test')).sort_values(ascending=True).reset_index(drop=True)
sub = pd.read_csv('/kaggle/input/alaska2-image-steganalysis/sample_submission.csv')


# In[ ]:


#https://www.kaggle.com/xhlulu/alaska2-efficientnet-on-tpus
def append_path(pre):
    return np.vectorize(lambda file: os.path.join(BASE_PATH, pre, file))


# In[ ]:


train_filenames = np.array(os.listdir("/kaggle/input/alaska2-image-steganalysis/Cover/"))
len(train_filenames)


# In[ ]:


#https://www.kaggle.com/xhlulu/alaska2-efficientnet-on-tpus
np.random.seed(0)
positives = train_filenames.copy()
negatives = train_filenames.copy()
np.random.shuffle(positives)
np.random.shuffle(negatives)

jmipod = append_path('JMiPOD')(positives[:10000])
juniward = append_path('JUNIWARD')(positives[10000:20000])
uerd = append_path('UERD')(positives[20000:30000])

pos_paths = np.concatenate([jmipod, juniward, uerd])


# In[ ]:


#https://www.kaggle.com/xhlulu/alaska2-efficientnet-on-tpus
test_paths = append_path('Test')(sub.Id.values)
neg_paths = append_path('Cover')(negatives[:30000])


# In[ ]:


train_paths = np.concatenate([pos_paths, neg_paths])
train_labels = np.array([1] * len(pos_paths) + [0] * len(neg_paths))


# In[ ]:


#https://www.kaggle.com/xhlulu/alaska2-efficientnet-on-tpus
train_paths, valid_paths, train_labels, valid_labels = train_test_split(
    train_paths, train_labels, test_size=0.15, random_state=2020)


# In[ ]:


len(valid_labels)


# In[ ]:


l=np.array([train_paths,train_labels])
traindataset = pd.DataFrame({ 'images': list(train_paths), 'label': train_labels},columns=['images','label'])


# In[ ]:


val_l=np.array([valid_paths,valid_labels])
validdataset=dataset = pd.DataFrame({ 'images': list(valid_paths), 'label': valid_labels},columns=['images','label'])


# **For now just using the train set only training**

# In[ ]:


#traindataset = pd.concat([traindataset,validdataset])
len(traindataset)


# In[ ]:


traindataset.head(2)


# In[ ]:


len(traindataset)


# In[ ]:


#i use this line of code for debugging
#traindataset = traindataset.head(100)
len(traindataset)


# In[ ]:


image = Image.open(train_paths[50] )
image


# In[ ]:


# add image augmen tation
class train_images(Dataset):

    def __init__(self, csv_file):

        self.data = csv_file

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        #print(idx)
        img_name =  self.data.loc[idx][0]
        image = Image.open(img_name)
        image = image.resize((512, 512), resample=Image.BILINEAR)
        label = self.data.loc[idx][1] #torch.tensor(self.data.loc[idx, 'label'])

# ## https://pytorch.org/docs/stable/torchvision/transforms.html
# transforms.Compose([
# transforms.CenterCrop(10),
# transforms.ToTensor(),
# ])
        
#         return {'image': transforms.ToTensor()(image), # ORIG
        return {'image': transforms.Compose([transforms.RandomVerticalFlip(),
                                             transforms.RandomHorizontalFlip(),
                                             transforms.ColorJitter(),
                                             transforms.ToTensor()])(image),
            'label': label
            }


# In[ ]:


train_dataset = train_images(traindataset)
valid_dataset = train_images(validdataset)


# In[ ]:


model = torchvision.models.resnet101(pretrained=True)
#model.load_state_dict(torch.load("../input/pytorch-pretrained-models/resnet101-5d3b4d8f.pth"))

num_features = model.fc.in_features
model.fc = nn.Linear(2048, 1)
model.load_state_dict(torch.load("../input/pytorch-transfer-learning-baseline/model.bin"))
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 
print(device)
model = model.to(device)
model.eval()


# In[ ]:


data_loader = torch.utils.data.DataLoader(train_dataset, batch_size = 16, shuffle=True, num_workers=4)
'''valid_loader = torch.utils.data.DataLoader(validdataset, batch_size=64, shuffle=True, num_workers=4)
valid_loader'''


plist = [
         {'params': model.layer4.parameters(), 'lr': 1e-4, 'weight': 0.001},
         {'params': model.fc.parameters(), 'lr': 1e-3}
         ]

optimizer = optim.Adam(plist, lr=0.001)
scheduler = lr_scheduler.StepLR(optimizer, step_size=10)


# In[ ]:


#https://www.kaggle.com/abhishek/very-simple-pytorch-training-0-59/data
since = time.time()
criterion = torch.nn.MSELoss() # BCEWithLogitsLoss

num_epochs = 6 # train for longer for better results

for epoch in range(num_epochs):
    print('Epoch {}/{}'.format(epoch, num_epochs - 1))
    print('-' * 10)
    scheduler.step()
    model.train()
    running_loss = 0.0
    tk0 = tqdm(data_loader, total=int(len(data_loader)))
    counter = 0
    for bi, d in enumerate(tk0):
        inputs = d["image"]
        labels = d["label"].view(-1, 1)
        inputs = inputs.to(device, dtype=torch.float)
        labels = labels.to(device, dtype=torch.float)
        optimizer.zero_grad()
        with torch.set_grad_enabled(True):
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            #loss = criterion(outputs, torch.max(labels, 1)[1])
            loss.backward()
            optimizer.step()
        running_loss += loss.item() * inputs.size(0)
        #print(running_loss)
        counter += 1
        tk0.set_postfix(loss=(running_loss / (counter * data_loader.batch_size)))
    epoch_loss = running_loss / len(data_loader)
    print('Training Loss: {:.4f}'.format(epoch_loss))

time_elapsed = time.time() - since
print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
torch.save(model.state_dict(), "model.bin")


# # Inference

# In[ ]:


class test_images(Dataset):

    def __init__(self, csv_file):

        self.data = csv_file

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_name =  self.data.loc[idx][0]
        image = Image.open(img_name)
        image = image.resize((512, 512), resample=Image.BILINEAR)
        #label = self.data.loc[idx][1] #torch.tensor(self.data.loc[idx, 'label'])
        #image = self.transform(image)
        return {'image': transforms.ToTensor()(image)}


# In[ ]:


testdataset = pd.DataFrame({ 'images': list(test_paths)},columns=['images'])
testdataset.head(2)


# In[ ]:


testdataset = test_images(testdataset)


# In[ ]:


sub["Label"] = pd.to_numeric(sub["Label"].astype(float))


# In[ ]:


get_ipython().run_cell_magic('time', '', 'test_loader = torch.utils.data.DataLoader(testdataset, batch_size=1, shuffle=False) # test_set contains only images directory\n\nfor param in model.parameters():\n    param.requires_grad = False\n\nprediction_list = []\ntk0 = tqdm(test_loader)\nfor i, x_batch in enumerate(tk0):\n    #print(i)\n    \n    x_batch = x_batch["image"]\n    #print(x_batch)\n    pred =  model(x_batch.to(device))\n    #prediction_list.append(pred.cpu())\n    #print( type(pred.item()))\n    #print("\\n")\n    sub.Label[i] = pred.item()\n    #print(sub.Label[i])')


# In[ ]:


sub.to_csv('submission.csv', index=False)
sub.head(110)


# # TakeAways : 
# * [very simple pytorch training](https://www.kaggle.com/abhishek/very-simple-pytorch-training-0-59/data)
# 
# * [Alaska2: EfficientNet on TPUs](https://www.kaggle.com/xhlulu/alaska2-efficientnet-on-tpus)
# 
# 
# 

# In[ ]:




