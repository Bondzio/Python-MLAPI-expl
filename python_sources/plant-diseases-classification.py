#!/usr/bin/env python
# coding: utf-8

# # We will use resnet9 architecture to design and train a model for the prediction of disease in plants.
# 

# Let's import required modules

# In[ ]:


import os # for working with files
import torch # Pytorch module 
import matplotlib.pyplot as plt # for plotting informations on graph and images using tensors
import torch.nn as nn # for creating  neural networks
from torch.utils.data import DataLoader # for dataloaders 
from PIL import Image # for checking images
import torch.nn.functional as F # for functions for calculating loss
import torchvision.transforms as transforms # for transforming images into tensors 
from torchvision.utils import make_grid # for data checking
from torchvision.datasets import ImageFolder # for working with classes and images
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


project_name = "Plant-Disease-Classification" # used by jovian


# In[ ]:


Data_Dir = "../input/new-plant-diseases-dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"
Train_Dir = Data_Dir + "/train"
Valid_Dir = Data_Dir + "/valid"
Diseases = os.listdir(Train_Dir)
print(Diseases)
print(len(Diseases))


# In[ ]:


plants = []
NumberOfDiseases = 0
for plant in Diseases:
    if plant.split('___')[0] not in plants:
        plants.append(plant.split('___')[0])
    if plant.split('___')[1] != 'healthy':
        NumberOfDiseases += 1
print(plants)
print(len(plants))
print(NumberOfDiseases)


# So we have images of leaves of 14 plants and while excluding healthy leaves, we have 26 types of images that show a particular disease in a particular plant.

# In[ ]:


# Number of images for each disease
nums = {}
for disease in Diseases:
    nums[disease] = len(os.listdir(Train_Dir + '/' + disease))
print(nums)


# While visualizing above information on graph

# In[ ]:


index = [n for n in range(38)]
plt.bar(index, [n for n in nums.values()], width=0.3)
plt.xlabel('Plants/Diseases', fontsize=10)
plt.ylabel('No of images available', fontsize=10)
plt.xticks(index, Diseases, fontsize=5, rotation=90)
plt.title('Images per each class of plant disease')


# In[ ]:


add = 0
for val in nums.values():
    add += val
print(add)


# So there are 70295 images available for training.

# In[ ]:


# datasets for validation and training
train_ds = ImageFolder(Train_Dir, transform=transforms.ToTensor())
val_ds = ImageFolder(Valid_Dir, transform=transforms.ToTensor()) 


# 

# In[ ]:


img, label = train_ds[0]
print(img.shape, label)


# In[ ]:


train_ds.classes


# In[ ]:


# for checking some images from training dataset
def show_image(image, label):
    print("Label :" + train_ds.classes[label] + "(" + str(label) + ")")
    plt.imshow(image.permute(1, 2, 0))


# ### Images from training dataset

# In[ ]:


show_image(*train_ds[0])


# In[ ]:


show_image(*train_ds[70000])


# In[ ]:


show_image(*train_ds[30000])


# In[ ]:


random_seed = 7
torch.manual_seed(random_seed)


# In[ ]:


batch_size = 32


# In[ ]:


# DataLoaders for training and validation
train_dl = DataLoader(train_ds, batch_size, shuffle=True, num_workers=2, pin_memory=True)
val_dl = DataLoader(val_ds, batch_size, num_workers=2, pin_memory=True)


# In[ ]:


def show_batch(dl):
    for images, labels in dl:
        fig, ax = plt.subplots(figsize=(30, 30))
        ax.set_xticks([]); ax.set_yticks([])
        ax.imshow(make_grid(images, nrow=8).permute(1, 2, 0))
        break


# In[ ]:


show_batch(train_dl) # Images for first batch of training


# In[ ]:


# for moving data into GPU
def get_default_device():
    if torch.cuda.is_available:
        return torch.device("cuda")
    else:
        return torch.device("cpu")
    
def to_device(data, device):
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)


class DeviceDataLoader:
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device
        
    def __iter__(self):
        for b in self.dl:
            yield to_device(b, self.device)
        
    def __len__(self):
        return len(self.dl)


# In[ ]:


device = get_default_device()
device


# In[ ]:


# Moving data into GPU
train_dl = DeviceDataLoader(train_dl, device)
val_dl = DeviceDataLoader(val_dl, device)


# In[ ]:


def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))
    

class DiseaseClassificationBase(nn.Module):
    
    def training_step(self, batch):
        images, labels = batch
        out = self(images)
        loss = F.cross_entropy(out, labels)
        return loss
    
    def validation_step(self, batch):
        images, labels = batch
        out = self(images)
        loss = F.cross_entropy(out, labels)
        accur = accuracy(out, labels)
        return {"val_loss": loss.detach(), "val_accuracy": accur}
    
    def validation_epoch_end(self, outputs):
        batch_losses = [x["val_loss"] for x in outputs]
        batch_accuracy = [x["val_accuracy"] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()
        epoch_accuracy = torch.stack(batch_accuracy).mean()
        return {"val_loss": epoch_loss, "val_accuracy": epoch_accuracy}
    
    def epoch_end(self, epoch, result):
        print("Epoch [{}], last_lr: {:.5f}, train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
            epoch, result['lrs'][-1], result['train_loss'], result['val_loss'], result['val_accuracy']))
        


# In[ ]:


# Architecture for training
def ConvBlock(in_channels, out_channels, pool=False):
    layers = [nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
             nn.BatchNorm2d(out_channels),
             nn.ReLU(inplace=True)]
    if pool:
        layers.append(nn.MaxPool2d(4))
    return nn.Sequential(*layers)


class ResNet9(DiseaseClassificationBase):
    def __init__(self, in_channels, num_diseases):
        super().__init__()
        
        self.conv1 = ConvBlock(in_channels, 64)
        self.conv2 = ConvBlock(64, 128, pool=True) # out_dim : 128 x 64 x 64 
        self.res1 = nn.Sequential(ConvBlock(128, 128), ConvBlock(128, 128))
        
        self.conv3 = ConvBlock(128, 256, pool=True) # out_dim : 256 x 16 x 16
        self.conv4 = ConvBlock(256, 512, pool=True) # out_dim : 512 x 4 x 44
        self.res2 = nn.Sequential(ConvBlock(512, 512), ConvBlock(512, 512))
        
        self.classifier = nn.Sequential(nn.MaxPool2d(4),
                                       nn.Flatten(),
                                       nn.Linear(512, num_diseases))
        
    def forward(self, xb): # xb is the loaded batch
        out = self.conv1(xb)
        out = self.conv2(out)
        out = self.res1(out) + out
        out = self.conv3(out)
        out = self.conv4(out)
        out = self.res2(out) + out
        out = self.classifier(out)
        return out
            
        


# In[ ]:


model = to_device(ResNet9(3, len(train_ds.classes)), device) # defining the model and moving it to the GPU
model


# In[ ]:


# for training
@torch.no_grad()
def evaluate(model, val_loader):
    model.eval()
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)


def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']
    

def fit_OneCycle(epochs, max_lr, model, train_loader, val_loader, weight_decay=0,
                grad_clip=None, opt_func=torch.optim.SGD):
    torch.cuda.empty_cache()
    history = []
    
    optimizer = opt_func(model.parameters(), max_lr, weight_decay=weight_decay)
    # scheduler for one cycle learniing rate
    sched = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr, epochs=epochs, steps_per_epoch=len(train_loader))
    
    
    for epoch in range(epochs):
        # Training
        model.train()
        train_losses = []
        lrs = []
        for batch in train_loader:
            loss = model.training_step(batch)
            train_losses.append(loss)
            loss.backward()
            
            # gradient clipping
            if grad_clip: 
                nn.utils.clip_grad_value_(model.parameters(), grad_clip)
                
            optimizer.step()
            optimizer.zero_grad()
            
            # recording and updating learning rates
            lrs.append(get_lr(optimizer))
            sched.step()
            
    
        # validation
        result = evaluate(model, val_loader)
        result['train_loss'] = torch.stack(train_losses).mean().item()
        result['lrs'] = lrs
        model.epoch_end(epoch, result)
        history.append(result)
        
    return history
    


# In[ ]:


get_ipython().run_cell_magic('time', '', 'history = [evaluate(model, val_dl)]\nhistory')


# In[ ]:


epochs = 2
max_lr = 0.01
grad_clip = 0.1
weight_decay = 1e-4
opt_func = torch.optim.Adam


# In[ ]:


get_ipython().run_cell_magic('time', '', 'history += fit_OneCycle(epochs, max_lr, model, train_dl, val_dl, \n                             grad_clip=grad_clip, \n                             weight_decay=1e-4, \n                             opt_func=opt_func)')


# ## So it says, we got 99.21% accuracy. Let's test it.

# In[ ]:


def predict_image(img, model):
    # Convert to a batch of 1
    xb = to_device(img.unsqueeze(0), device)
    # Get predictions from model
    yb = model(xb)
    # Pick index with highest probability
    _, preds  = torch.max(yb, dim=1)
    # Retrieve the class label
    return train_ds.classes[preds[0].item()]


# In[ ]:


test_dir = "../input/new-plant-diseases-dataset/test"
test_ds = ImageFolder(test_dir, transform=transforms.ToTensor())


# In[ ]:


test_ds.classes


# In[ ]:


test_images = sorted(os.listdir(test_dir + '/test')) # since images in test folder are in alphabetical order
test_images


# In[ ]:


def predict_image(img, model):
    # Convert to a batch of 1
    xb = to_device(img.unsqueeze(0), device)
    # Get predictions from model
    yb = model(xb)
    # Pick index with highest probability
    _, preds  = torch.max(yb, dim=1)
    # Retrieve the class label
    return train_ds.classes[preds[0].item()]


# In[ ]:


Image.open('../input/new-plant-diseases-dataset/test/test/AppleCedarRust1.JPG')


# In[ ]:


img, label = test_ds[0]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[0], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[1]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[1], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[2]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[2], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[3]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[3], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[4]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[4], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[5]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[5], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[6]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[6], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[7]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[7], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[8]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[8], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[9]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[9], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[10]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[10], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[11]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[11], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[12]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[12], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[13]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[13], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[14]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[14], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[15]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[15], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[16]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[16], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[17]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[17], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[18]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[18], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[19]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[19], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[20]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[20], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[21]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[21], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[22]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[22], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[23]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[23], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[24]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[24], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[25]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[25], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[26]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[26], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[27]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[27], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[28]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[28], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[29]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[29], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[30]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[30], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[31]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[31], ', Predicted:', predict_image(img, model))


# In[ ]:


img, label = test_ds[32]
plt.imshow(img.permute(1, 2, 0))
print('Label:', test_images[32], ', Predicted:', predict_image(img, model))


# In[ ]:


torch.save(model.state_dict(), 'plantdiseaseclassification.pth')


# SO it is able to predict every image from the test data correctly

# In[ ]:





# In[ ]:





# In[ ]:




