#!/usr/bin/env python
# coding: utf-8

# ## Simple classification using pytorch
# 
# In this notebook I will try to demonstate usage of pytorch for simple image classfication task. We will create a simple CNN and then try transfer learning using a pretrained model(ResNet18)
# 
# 

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import sys
import time
import copy
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim import lr_scheduler
import torchvision
import torchvision.transforms as transforms
from torchvision import models
from torch.utils.data import Dataset, random_split, DataLoader


# In[ ]:


batch_size = 64
n_iters = 30
epochs  = 10#int( n_iters / (len(train_dl) / batch_size))
input_dim = 784
output_dim = 10
lr_rate  = 0.001


# In[ ]:


def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')
    
def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

class DeviceDataLoader():
    """Wrap a dataloader to move data to a device"""
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device
        
    def __iter__(self):
        """Yield a batch of data after moving it to device"""
        for b in self.dl: 
            yield to_device(b, self.device)

    def __len__(self):
        """Number of batches"""
        return len(self.dl)


# In[ ]:


device = get_default_device()
device


# In[ ]:


from torchvision.utils import make_grid

def show_batch(dl):
    for images, labels in dl:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xticks([]); ax.set_yticks([])
        ax.imshow(make_grid(images, nrow=16).permute(1, 2, 0))
        break


# In[ ]:


transform = transforms.Compose(
    [transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)


trainset = torchvision.datasets.ImageFolder(root="/kaggle/input/100-bird-species/train/", transform=transform)
train_dl = DataLoader(trainset, batch_size=batch_size, num_workers=3, shuffle=True)

testset = torchvision.datasets.ImageFolder(root="/kaggle/input/100-bird-species/test/", transform=transform)
val_dl = DataLoader(testset, batch_size=batch_size, num_workers=3, shuffle=False)

dataloaders = {
    "train": train_dl,
    "test": val_dl
}
datasizes = {
    "train": len(trainset),
    "test": len(testset)
}
CLASSES = list(trainset.class_to_idx.keys())


# In[ ]:


##we are creating the dataset without transform

transform = transforms.Compose(
    [transforms.ToTensor(),
#     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ]
)


trainset_no_t = torchvision.datasets.ImageFolder(root="/kaggle/input/100-bird-species/train/", transform=transform) 
train_dl_no_t = DataLoader(trainset_no_t, batch_size=batch_size, num_workers=3, shuffle=True)

testset_no_t = torchvision.datasets.ImageFolder(root="/kaggle/input/100-bird-species/test/", transform=transform)
val_dl_no_t = DataLoader(testset_no_t, batch_size=batch_size, num_workers=3, shuffle=False)

dataloaders_no_t = {
    "train": trainset_no_t,
    "test": val_dl_no_t
}
datasizes_no_t = {
    "train": len(trainset_no_t),
    "test": len(train_dl_no_t)
}
CLASSES = list(trainset.class_to_idx.keys())


# In[ ]:


def plot_accuracies(history):
    accuracies = [x['val_acc'] for x in history]
    plt.plot(accuracies, '-x')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.title('Accuracy vs. No. of epochs');


# In[ ]:


def plot_losses(history):
    train_losses = [x.get('train_loss') for x in history]
    val_losses = [x['val_loss'] for x in history]
    plt.plot(train_losses, '-bx')
    plt.plot(val_losses, '-rx')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend(['Training', 'Validation'])
    plt.title('Loss vs. No. of epochs');


# In[ ]:


def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))

class ImageClassificationBase(nn.Module):
    def training_step(self, batch):
        images, labels = batch 
        out = self(images)                  # Generate predictions
        loss = F.cross_entropy(out, labels) # Calculate loss
        return loss
    
    def validation_step(self, batch):
        images, labels = batch 
        out = self(images)                    # Generate predictions
        loss = F.cross_entropy(out, labels)   # Calculate loss
        acc = accuracy(out, labels)           # Calculate accuracy
        return {'val_loss': loss.detach(), 'val_acc': acc}
        
    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()   # Combine losses
        batch_accs = [x['val_acc'] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()      # Combine accuracies
        return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}
    
    def epoch_end(self, epoch, result):
        print("Epoch [{}], train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
            epoch, result['train_loss'], result['val_loss'], result['val_acc']))


# In[ ]:


class BirdClassifierCnnModel(ImageClassificationBase):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 12, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(12, 32, 5)
        self.fc1 = nn.Linear(32*53*53, 512)
        self.fc3 = nn.Linear(512, len(CLASSES))
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 32*53*53)
        x = F.relu(self.fc1(x))
        x = self.fc3(x)
        return x


# In[ ]:


##data without normalization
show_batch(train_dl_no_t)


# In[ ]:


##data with normalization
show_batch(train_dl)


# In[ ]:


model = BirdClassifierCnnModel()
model


# In[ ]:


@torch.no_grad()
def evaluate(model, val_loader):
    model.eval()
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)

def fit(epochs, lr, model, train_loader, val_loader, opt_func=torch.optim.SGD):
    history = []
    optimizer = opt_func(model.parameters(), lr)
    for epoch in tqdm(range(epochs)):
        # Training Phase 
        model.train()
        train_losses = []
        for batch in train_loader:
            loss = model.training_step(batch)
            train_losses.append(loss)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        # Validation phase
        result = evaluate(model, val_loader)
        result['train_loss'] = torch.stack(train_losses).mean().item()
        result['model'] = 'CNN-model'
        model.epoch_end(epoch, result)
        history.append(result)
    return history


# In[ ]:


opt_func = torch.optim.Adam
lr = 0.001


# ## Train the data without data transform

# In[ ]:


train_dl_no_t = DeviceDataLoader(train_dl_no_t, device)
val_dl_no_t = DeviceDataLoader(val_dl_no_t, device)
to_device(model, device);


# In[ ]:


evaluate(model, val_dl_no_t)


# In[ ]:


get_ipython().run_cell_magic('time', '', 'history = fit(epochs, lr, model, train_dl_no_t, val_dl_no_t, opt_func)')


# In[ ]:


plot_accuracies(history)


# In[ ]:


plot_losses(history)


# ### log the results to jovian

# In[ ]:


get_ipython().system('pip install jovian --upgrade --quiet')


# In[ ]:


import jovian


# In[ ]:


hyperparams = {
    'arch_name': 'cnn',
    'Wall time': '11 min',
    'lr': lr,
    'batch_size' : 64,
    'n_iters': 30,
    'epochs' : 10,#int( n_iters / (len(train_dl) / batch_size))
    'input_dim' : 784,
    'output_dim' : 10
}
jovian.log_hyperparams(hyperparams)


# In[ ]:


##save the metrics
# epoch_count = 0
# for h in history:
#     h['epoch'] = epoch_count
#     jovian.log_metrics(h)
#     epoch_count+=1


# In[ ]:


h = history[-1]
print(h)


# In[ ]:


jovian.log_metrics(h)


# In[ ]:


jovian.commit(project='bird-classifier', environment=None)


# ## Train the data with transform

# In[ ]:


train_dl = DeviceDataLoader(train_dl, device)
val_dl = DeviceDataLoader(val_dl, device)
to_device(model, device);


# In[ ]:


evaluate(model, val_dl)


# In[ ]:


get_ipython().run_cell_magic('time', '', 'history = fit(epochs, lr, model, train_dl, val_dl, opt_func)')


# In[ ]:


plot_accuracies(history)


# In[ ]:


plot_losses(history)


# ### log the results to jovian

# In[ ]:


hyperparams = {
    'arch_name': 'cnn_with_data_normalization',
    'Wall time': '12min',
    'lr': lr,
    'batch_size' : 64,
    'epochs' : 10,#int( n_iters / (len(train_dl) / batch_size))
    'input_dim' : 784,
    'output_dim' : 10
}
jovian.log_hyperparams(hyperparams)


# In[ ]:


##save the metrics
# epoch_count = 0
# for h in history:
#     h['epoch'] = epoch_count
#     h['model'] = 'cnn_with_data_normalization'
#     jovian.log_metrics(h)
#     epoch_count+=1


# In[ ]:


h = history[-1]
h['model'] = 'cnn_with_data_normalization'
print(h)


# In[ ]:


jovian.log_metrics(h)


# In[ ]:


jovian.commit(project='bird-classifier', environment=None)


# As we can see, we did not get a good accuracy at all and will not get a good one from this model, because model is not upto the mark to do classification of 200 classes.
# 
# So we will use a pretrained model and edit its last fully connected layer and train ONLY that last layer.
# We will use generic model training function form pytorch documentation (because its all we need, no changes at all)

# ## Use Pre-trained model

# In[ ]:


class PreTrainedClassifier(ImageClassificationBase):
    def __init__(self):
        super().__init__()
        # Use a pretrained model
        self.network = models.resnet34(pretrained=True)
        # Replace last layer
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Linear(num_ftrs, len(CLASSES))
    
    def forward(self, xb):
        return torch.sigmoid(self.network(xb))
    
    def freeze(self):
        # To freeze the residual layers
        for param in self.network.parameters():
            param.require_grad = False
        for param in self.network.fc.parameters():
            param.require_grad = True
    
    def unfreeze(self):
        # Unfreeze all layers
        for param in self.network.parameters():
            param.require_grad = True


# In[ ]:


@torch.no_grad()
def evaluate(model, val_loader):
    model.eval()
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)

def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

def fit_one_cycle(epochs, max_lr, model, train_loader, val_loader, 
                  weight_decay=0, grad_clip=None, opt_func=torch.optim.SGD):
    torch.cuda.empty_cache()
    history = []
    
    # Set up cutom optimizer with weight decay
    optimizer = opt_func(model.parameters(), max_lr, weight_decay=weight_decay)
    # Set up one-cycle learning rate scheduler
    sched = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr, epochs=epochs, 
                                                steps_per_epoch=len(train_loader))
    
    for epoch in range(epochs):
        # Training Phase 
        model.train()
        train_losses = []
        lrs = []
        for batch in tqdm(train_loader):
            loss = model.training_step(batch)
            train_losses.append(loss)
            loss.backward()
            
            # Gradient clipping
            if grad_clip: 
                nn.utils.clip_grad_value_(model.parameters(), grad_clip)
            
            optimizer.step()
            optimizer.zero_grad()
            
            # Record & update learning rate
            lrs.append(get_lr(optimizer))
            sched.step()
        
        # Validation phase
        result = evaluate(model, val_loader)
        result['train_loss'] = torch.stack(train_losses).mean().item()
        result['lrs'] = lrs
        result['model'] = 'pre-trained-model'
        model.epoch_end(epoch, result)
        history.append(result)
    return history


# In[ ]:


model = to_device(PreTrainedClassifier(), device)


# In[ ]:


history = [evaluate(model, val_dl)]
history


# In[ ]:


model.freeze()


# In[ ]:


max_lr = 0.01
grad_clip = 0.1
weight_decay = 1e-4
opt_func = torch.optim.Adam


# In[ ]:


get_ipython().run_cell_magic('time', '', 'history += fit_one_cycle(int(epochs/2), max_lr, model, train_dl, val_dl, \n                         grad_clip=grad_clip, \n                         weight_decay=weight_decay, \n                         opt_func=opt_func)')


# In[ ]:


model.unfreeze()


# In[ ]:


get_ipython().run_cell_magic('time', '', 'history += fit_one_cycle(int(epochs/2), 0.001, model, train_dl, val_dl, \n                         grad_clip=grad_clip, \n                         weight_decay=weight_decay, \n                         opt_func=opt_func)')


# In[ ]:


plot_accuracies(history)


# In[ ]:


plot_losses(history)


# ### Pretrained Results
# 
# In only 4-5 epochs we crossed 94% accuracy , without even breaking a sweat.
# We can improve it further by 
# 1. More data augmentation and transformation while loading like Rotating image randomly, or Cropped selection and Scaled to make model more scale and rotate invariant
# 2. Fine tune model by playing with learning rate, and number of epochs
# etc

# In[ ]:


hyperparams = {
    'arch_name': 'cnn_with_pre_trained_models_and_varying_lr',
    'Wall time': '15min',
    'lr': lr,
    'batch_size' : 64,
    'epochs' : 10,#int( n_iters / (len(train_dl) / batch_size))
    'input_dim' : 784,
    'output_dim' : 10
}
jovian.log_hyperparams(hyperparams)


# In[ ]:


h = history[-1]
h['model'] = 'cnn_with_pre_trained_models_and_varying_lr'
# print(h)


# In[ ]:


jovian.log_metrics(h)


# In[ ]:


# ##save the metrics
# epoch_count = 0
# for h in history:
#     h['model'] = 'cnn_with_pre_trained_models_and_varying_lr'
#     jovian.log_metrics(h)
#     epoch_count+=1


# ### Save the notebook

# In[ ]:


jovian.commit(project='bird-classifier', environment=None)


# ### Lets try with 20 epoch

# In[ ]:


epochs = 20


# No Transformation

# In[ ]:


get_ipython().run_cell_magic('time', '', 'history = fit(epochs, lr, model, train_dl_no_t, val_dl_no_t, opt_func)')


# In[ ]:


plot_accuracies(history)


# In[ ]:


plot_losses(history)


# In[ ]:


hyperparams = {
    'arch_name': 'cnn',
    'Wall time': '20min',
    'lr': lr,
    'batch_size' : 64,
    'epochs' : 20,#int( n_iters / (len(train_dl) / batch_size))
    'input_dim' : 784,
    'output_dim' : 10
}
jovian.log_hyperparams(hyperparams)


# In[ ]:


h = history[-1]
h['model'] = 'cnn'
print(h)


# In[ ]:


jovian.log_metrics(h)


# In[ ]:


jovian.commit(project='bird-classifier', environment=None)


# Data with Transformation

# In[ ]:


get_ipython().run_cell_magic('time', '', 'history = fit(epochs, lr, model, train_dl, val_dl, opt_func)')


# In[ ]:


plot_accuracies(history)


# In[ ]:


plot_losses(history)


# In[ ]:


hyperparams = {
    'arch_name': 'cnn_with_data_normalization',
    'Wall time': '17min',
    'lr': lr,
    'batch_size' : 64,
    'epochs' : 20,#int( n_iters / (len(train_dl) / batch_size))
    'input_dim' : 784,
    'output_dim' : 10
}
jovian.log_hyperparams(hyperparams)


# In[ ]:


h = history[-1]
h['model'] = 'cnn_with_data_normalization'
print(h)


# In[ ]:


jovian.log_metrics(h)


# In[ ]:


jovian.commit(project='bird-classifier', environment=None)


# Pre-trained models

# In[ ]:


model.freeze()


# In[ ]:


max_lr = 0.01
grad_clip = 0.1
weight_decay = 1e-4
opt_func = torch.optim.Adam


# In[ ]:


get_ipython().run_cell_magic('time', '', 'history += fit_one_cycle(int(epochs/2), max_lr, model, train_dl, val_dl, \n                         grad_clip=grad_clip, \n                         weight_decay=weight_decay, \n                         opt_func=opt_func)')


# In[ ]:


model.unfreeze()


# In[ ]:


get_ipython().run_cell_magic('time', '', 'history += fit_one_cycle(int(epochs/2), 0.001, model, train_dl, val_dl, \n                         grad_clip=grad_clip, \n                         weight_decay=weight_decay, \n                         opt_func=opt_func)')


# In[ ]:


plot_accuracies(history)


# In[ ]:


plot_losses(history)


# In[ ]:


hyperparams = {
    'arch_name': 'cnn_with_pre_trained_models_and_varying_lr',
    'Wall time': '15min',
    'lr': lr,
    'batch_size' : 64,
    'epochs' : 20,#int( n_iters / (len(train_dl) / batch_size))
    'input_dim' : 784,
    'output_dim' : 10
}
jovian.log_hyperparams(hyperparams)


# In[ ]:


h = history[-1]
h['model'] = 'cnn_with_pre_trained_models_and_varying_lr'
# print(h)


# In[ ]:


jovian.log_metrics(h)


# In[ ]:


jovian.commit(project='bird-classifier', environment=None)


# In[ ]:




