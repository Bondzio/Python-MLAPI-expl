#!/usr/bin/env python
# coding: utf-8

# # Overview
# This kernel demonstrates how to test a flower classifier (trained elsewhere, loaded from a saved checkpoint file) for the final project of the Udacity's PyTorch FB Challenge.
# 
# The data originally comes from http://www.robots.ox.ac.uk/~vgg/data/flowers/102/. There are 102 flower categories, and the test dataset contains 819 test images. For this competition the labels of the test dataset are not provided.
# 
# Submitted to: https://www.kaggle.com/c/oxford-102-flower-pytorch

# # Imports
# Import all the required modules.

# In[ ]:


import torch
import torch.nn as nn
import torchvision
from torchvision import datasets, transforms, models
from torch.utils import data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from PIL import Image

print(os.listdir("../input"))
print(f'\nPyTorch version {torch.__version__}\n')
print('cuda' if torch.cuda.is_available() else 'cpu')


# In[ ]:


print(os.listdir('../input/oxford-102-flower-pytorch/flower_data/flower_data/'))


# # Load the data
# Here we create the data loaders for the validation and test datasets. We will use the validation dataset to check if our model works by computing the total accuracy on this dataset (for which the labels are provided). Then, we make the predictions on the unlabelled data from the test dataset, which will be submited for the competition.
# 
# The validation dataloader is created with [ImageFolder](https://pytorch.org/docs/stable/_modules/torchvision/datasets/folder.html#ImageFolder) class. This is possible because the folder 'valid' has the required structure: category subfolders containing images of the corresponding category. However, for the test dataset we cannot use ImageFolder because the 'test' folder contains images from different categories, not categorized in subfolders. If we try it, it will throw the error 'RuntimeError: Found 0 files in subfolders of...'. Therefore, to create the test dataloader, we will use a custom dataset class which inherits from the data.Dataset.

# 

# In[ ]:


#try data_dir = '../input/flower_data/flower_data/'
data_dir = '../input/oxford-102-flower-pytorch/flower_data/flower_data/'

class TestDataset(data.Dataset):
    '''
    Custom dataset class for test dataset which contains uncategorized images.
    The category index is set to 0 for all images (we don't need it).
    It also returns the filename of each image.
    '''
    def __init__(self, path, transform=None):
        self.path = path
        self.files = []
        for (dirpath, _, filenames) in os.walk(self.path):
            for f in filenames:
                if f.endswith('.jpg'):
                    p = {}
                    p['img_path'] = dirpath + '/' + f
                    self.files.append(p)
        self.transform = transform

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        img_path = self.files[idx]['img_path']
        img_name = img_path.split('/')[-1]
        image = pil_loader(img_path)
        if self.transform:
            image = self.transform(image)
        return image, 0, img_name
    
    
def pil_loader(path):
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')
    
    
# Image transformations
data_transforms = transforms.Compose([transforms.Resize(256),
                                      transforms.CenterCrop(224),
                                      transforms.ToTensor(),
                                      transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                            std=[0.229, 0.224, 0.225])])

# Validation dataset
val_dataset = datasets.ImageFolder(data_dir + 'valid', transform=data_transforms)

# Test dataset
test_dataset = TestDataset(data_dir + 'test', transform=data_transforms)

# Create the dataloaders
batch_size = 32
val_loader = data.DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False)


# Let's plot a batch of test images to check if the test dataloader works properly.

# In[ ]:


def imshow(image):
    if isinstance(image, torch.Tensor):
        image = image.numpy().transpose((1, 2, 0))
    else:
        image = np.array(image).transpose((1, 2, 0))
    # Unnormalize
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    image = std * image + mean
    image = np.clip(image, 0, 1)
    # Plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    plt.imshow(image)
    ax.axis('off') 
        
    # Make a grid from batch
images, _, _ = next(iter(test_loader))
out = torchvision.utils.make_grid(images, nrow=8)
imshow(out)


# # Load the model from a checkpoint
# Here we load our pretrained model (the state dict) from a checkpoint file which should be first uploaded to the 'input' folder by clicking on **+Add Data** (Draft Environment tab on the right). 
# Note that in the following code there are 4 things that you may need to change:
# * the pretrained model (in my case densenet161)
# * the classifier
# * the checkpoint's key to the state dict
# * the checkpoint's path and filename.

# In[ ]:


# Change the classifier to the one you used.
def classifier(n_ftrs):
    return nn.Sequential(nn.Linear(n_ftrs, 102),                           
                         nn.LogSoftmax(dim=1))


# In[ ]:


def load_checkpoint(checkpoint_path):
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
    # Here put the pretrained model that you used (in my case it's densenet161).
    model = models.densenet161(pretrained=False)
    
    # We freeze all the layers since we are not training the model here.
    for param in model.parameters():
        param.requires_grad = False
    
    try:
        n_ftrs = model.classifier.in_features
        model.classifier = classifier(n_ftrs)
    except AttributeError:
        n_ftrs = model.fc.in_features
        model.fc = classifier(n_ftrs)
                              
    model.load_state_dict(checkpoint['model_state_dict'])  # your checkpoint's key may differ (e.g.'state_dict')
    model.eval()
    
    return model

model = load_checkpoint('../input/checkpoint/checkpoint_ft_0_.pth')  # use your path to checkpoint file
print(model.classifier)


# ---------------------------------------
# Now that we have loaded our trained model, let's check its performance on the validation dataset.

# In[ ]:


def comp_accuracy(model, dataloader):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    model.to(device)
    model.eval()
    
    with torch.no_grad():
        running_acc = 0.0
        for ii, (images, labels) in enumerate(dataloader, start=1):
            if ii % 5 == 0:
                print('Batch {}/{}'.format(ii, len(dataloader)))
            images, labels = images.to(device), labels.to(device)
            logps = model(images)
            ps = torch.exp(logps)  # in my case the outputs are logits so I take the exp()
            equals = ps.topk(1)[1].view(labels.shape) == labels          
            running_acc += equals.sum().item()
        acc = running_acc/len(dataloader.dataset) 
        print(f'\nAccuracy: {acc:.5f}') 
        
    return acc


# In[ ]:


comp_accuracy(model, val_loader)


# Finally. let's get the predictions on the test dataset flower images and write them to the csv file ready for the submission.
# The submission csv file has two columns, one with the image filenames and one with the id's of the predicted flower category.

# In[ ]:


# The prediction of our model is an index which we need to convert back to the class label.
# For this, we will use the following mapping
idx_to_class = {val: key for key, val in val_dataset.class_to_idx.items()}
print(idx_to_class)


# In[ ]:


def predict(model, dataloader):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    model.to(device)
    model.eval()
    
    predictions = {}   
    with torch.no_grad():
        for ii, (images, _, img_names) in enumerate(dataloader, start=1):
            if ii % 5 == 0:
                print('Batch {}/{}'.format(ii, len(dataloader)))
            images = images.to(device)
            logps = model(images)
            ps = torch.exp(logps)
            
            # Top indices
            _, top_indices = ps.topk(1)
            top_indices = top_indices.detach().cpu().numpy().tolist()
    
            # Convert indices to classes
            top_classes = [idx_to_class[idx[0]] for idx in top_indices]
            
            for i, img_name in enumerate(img_names):
                predictions[img_name] = top_classes[i]
            
        print('\nCompleted')

    return predictions


# In[ ]:


predictions = predict(model, test_loader)


# In[ ]:


submission = pd.DataFrame(list(predictions.items()), columns=['file_name', 'id'])
submission.to_csv('submission.csv', index=False)
print(submission)


# # Submit your predictions
# Run the notebook (after first forking the kernel) and commit. The submition.csv will be stored on the Output folder (if you go back by pressing << on the upper-left corner, you will see the Output tab is on the left sidebar). Press the Output tab and then "Submit to Competition" button.
# 
# ![](https://storage.googleapis.com/kagglesdsdata/datasets/102106/242233/subm.png?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1547190677&Signature=alcL%2FMz1z2TqAtZR9lHe%2FrhKeA4PJRqJg4yEW4nmL2%2FEVmUT%2FQ2CD7mWzH7dyzRnE39eNKIfK%2BVHES8CbPCvO7vy%2FD5g7nYNrZj475SRwCg7W9XoqPrBT5Kk0CWlgA2Y0GqRhxUE0O5kuH9v24q1CUn7jrk3Iov%2FUa3jVR3z%2BsGLv70ZU4griFZ6V7JJbvSjdToiLuHW3GhpuYmCG67DoTrpQ9tI42B3SO7IVxC9y5z0I5yKzc4NfcVr4ZohpxCVEMbvRR44rqg79I7WDhNtviyTl%2BC8p1%2B3QQIGbm%2FESAfYxjBVm7z2P0xX0Dihu13AwMIb5PDuFP2dtPtj2kqfYA%3D%3D)
# 
# 

# In[ ]:




