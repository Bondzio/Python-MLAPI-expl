#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# All the required imports

import pandas as pd
import numpy as np
import os
import torch
import torchvision
from torchvision import transforms
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
from torch import nn
import torch.nn.functional as F
from torch import optim
from skimage import io, transform
from torchvision import models
from PIL import Image
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#Dataset class

class ImageDataset(Dataset):
    

    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with labels.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.data_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, self.data_frame['Id'][idx])         # getting path of image
        image = Image.open(img_name).convert('RGB')                                # reading image and converting to rgb if it is grayscale
        label = np.array(self.data_frame['Category'][idx])                         # reading label of the image
        
        if self.transform:            
            image = self.transform(image)                                          # applying transforms, if any
        
        sample = (image, label)        
        return sample


# In[ ]:


# Transforms to be applied to each image (you can add more transforms), resizing every image to 3 x 224 x 224 size and converting to Tensor
transform = transforms.Compose([transforms.RandomResizedCrop(224),
                                transforms.RandomHorizontalFlip(),
                                transforms.RandomRotation(10),
                                transforms.ToTensor()])

trainset = ImageDataset(csv_file = '../input/train.csv', root_dir = '../input/data/data', transform=transform)     #Training Dataset
trainloader = torch.utils.data.DataLoader(trainset, batch_size=16, shuffle=True, num_workers=0)                     #Train loader, can change the batch_size to your own choice


# In[ ]:


model=models.densenet201(pretrained=True)
model.classifier=nn.Linear(1920,67,bias=True)


# In[ ]:


criterion = nn.CrossEntropyLoss()   # You can change this if needed

# Optimizer to be used, replace "your_model" with the name of your model and enter your learning rate in lr=0.001
optimizer = optim.SGD(model.parameters(), lr=0.001)


# In[ ]:


model = model.to('cuda')
model.train()
n_epochs = 10
#number of epochs, change this accordingly
for epoch in range(1, n_epochs+1):
    for inputs, labels in trainloader:
         # Move input and label tensors to the default device
        inputs, labels = inputs.cuda(), labels.cuda()
        optimizer.zero_grad()
        logps = model(inputs)
        loss = criterion(logps, labels)
        loss.backward()
        optimizer.step()
    print(loss)
    print(epoch)


# In[ ]:


model.eval() # eval mode
# Reading sample_submission file to get the test image names
submission = pd.read_csv('../input/sample_sub.csv')


# In[ ]:


#Loading test data to make predictions

testset = ImageDataset(csv_file = '../input/sample_sub.csv', root_dir = '../input/data/data/', transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=16, shuffle=False, num_workers=0)


# In[ ]:


predictions=[]
for data, target in testloader:
    # move tensors to GPU if CUDA is available
    data, target = data.cuda(), target.cuda()
    # forward pass: compute predicted outputs by passing inputs to the model
    output = model(data)
    _, pred = torch.max(output, 1)
    for i in range(len(pred)):
        predictions.append(int(pred[i]))
submission['Category'] = predictions             #Attaching predictions to submission file
#saving submission file
submission.to_csv('submission.csv', index=False, encoding='utf-8')


# In[ ]:


os.environ['KAGGLE_USERNAME']="kananarora"
os.environ['KAGGLE_KEY']="2011c447658fb23f4517f0f36f75a817"
get_ipython().system('pip install kaggle')
get_ipython().system('kaggle competitions submit -c qstp-deep-learning-2019 -f submission.csv -m "4d"')


# In[ ]:




