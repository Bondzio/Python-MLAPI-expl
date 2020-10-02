#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# # Load helper method

# In[ ]:


get_ipython().system('wget https://raw.githubusercontent.com/Iamsdt/60daysofudacity/master/day22/Helper.py')


# In[ ]:


os.listdir("../input/seefood")


# # see sample Image

# In[ ]:


from PIL import Image
data_dir = "../input/seefood"
path = data_dir + "/train/hot_dog/1000288.jpg"
Image.open(path)


# # Prepare Data

# In[ ]:


import Helper
import torch
from torchvision import datasets, transforms,models
from torch.utils.data import DataLoader

mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

train_transform = transforms.Compose([
                                transforms.Resize(255),
                                transforms.RandomResizedCrop(224),
                                transforms.CenterCrop(224),
                                transforms.RandomHorizontalFlip(),
                                transforms.ColorJitter(),
                                transforms.ToTensor(),
                                transforms.Normalize(mean, std)])
test_transform = transforms.Compose([
                                transforms.Resize(255),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize(mean, std)])

train_data = datasets.ImageFolder(data_dir+"/train", transform=train_transform)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=64,shuffle=True)

test_data = datasets.ImageFolder(data_dir+"/test", transform=test_transform)
test_loader = torch.utils.data.DataLoader(test_data, batch_size=64)

print(len(train_loader))
print(len(test_loader))


# In[ ]:


classes = os.listdir(data_dir+"/train")
classes


# # Visualize

# In[ ]:


Helper.visualize(test_loader, classes)


# # Load model

# In[ ]:


model = models.densenet161(pretrained=True)
model.classifier


# In[ ]:


model = Helper.freeze_parameters(model)


# In[ ]:


import torch.nn as nn
from collections import OrderedDict

classifier = nn.Sequential(
  nn.Linear(in_features=2208, out_features=2208),
  nn.ReLU(),
  nn.Dropout(p=0.4),
  nn.Linear(in_features=2208, out_features=1024),
  nn.ReLU(),
  nn.Dropout(p=0.3),
  nn.Linear(in_features=1024, out_features=8),
  nn.LogSoftmax(dim=1)  
)
    
model.classifier = classifier
model.classifier


# In[ ]:


import torch.optim as optim
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

criterion = nn.NLLLoss()
optimizer = optim.Adam(model.classifier.parameters(), lr=0.003)


# # Training

# In[ ]:


epoch = 5+5


# In[ ]:


model, train_loss, test_loss = Helper.train(model, train_loader, test_loader, epoch, optimizer, criterion)


# In[ ]:


model = Helper.load_latest_model(model)


# In[ ]:


Helper.check_overfitted(train_loss, test_loss)


# #  Testing

# In[ ]:


Helper.test(model, test_loader)


# In[ ]:


Helper.test_per_class(model, test_loader, criterion, classes)


# # Test single image

# In[ ]:


from PIL import Image

def test(file):
  ids = train_loader.dataset.class_to_idx

  with Image.open(file) as f:
      img = test_transform(f).unsqueeze(0)
      with torch.no_grad():
          out = model(img.to(device)).cpu().numpy()
          for key, value in ids.items():
              if value == np.argmax(out):
                    #name = classes[int(key)]
                    print(f"Predicted Label: {key} and value {value}")
          plt.imshow(np.array(f))
          plt.show()


# In[ ]:


from PIL import Image
from matplotlib import pyplot as plt
name = os.listdir(data_dir+"/test/hot_dog")[6]
file = data_dir+'/test/hot_dog/'+name
print(file)

test(file)


# In[ ]:


name = os.listdir(data_dir+"/test/not_hot_dog")[6]
file = data_dir+'/test/not_hot_dog/'+name
print(file)

test(file)

