#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torch.utils.data as data_util
from tqdm import tqdm_notebook, tqdm
from copy import deepcopy
import matplotlib.pyplot as plt

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


train_df = pd.read_csv('/kaggle/input/Kannada-MNIST/train.csv')
val_df = pd.read_csv('/kaggle/input/Kannada-MNIST/Dig-MNIST.csv')


# In[ ]:


train_df.head()


# In[ ]:


def df_to_image(df):
    imgs = []
    labels = []
    for idx in tqdm_notebook(range(len(df))):
        row = df.iloc[idx].values
        label, img = row[0], row[1:]
        labels.append(label)
        imgs.append(img.reshape(1, 28, 28).astype('uint8'))
    
    imgs = np.concatenate(imgs, axis=0)
    labels = np.array(labels)
    
    return imgs, labels


# In[ ]:


train_img, train_label = df_to_image(train_df)
val_img, val_label = df_to_image(val_df)


# In[ ]:


def random_plot(images, labels):
    num = len(images)
    idxs = np.random.choice(range(num), 9, replace=False)
    fig, axes = plt.subplots(3, 3)
    for plot_idx, arch in enumerate(idxs):
        i = plot_idx % 3 # Get subplot row
        j = plot_idx // 3 # Get subplot column
        img = images[arch]
#         axes[i, j].imshow(img, cmap='gray')
        axes[i, j].imshow(img,)
        axes[i, j].axis('off')
        axes[i, j].set_title(f'{labels[arch]}')
    plt.subplots_adjust(wspace=0.1, hspace=0.3)
    plt.show()


# In[ ]:


random_plot(train_img, train_label)


# #### Build model

# In[ ]:


model = torchvision.models.resnet34()
model.fc


# In[ ]:


model.fc = nn.Linear(512, 10)


# In[ ]:


model.conv1 = nn.Conv2d(1, 64, kernel_size=(3), stride=1, padding=1) # stride=2


# In[ ]:


class DigDataset(data_util.Dataset):
    def __init__(self, imgs, labels):
        super(DigDataset, self).__init__()
        self.imgs = imgs.reshape(-1, 28, 28, 1)
        self.labels = labels
        self.trans = torchvision.transforms.ToTensor()
        
    
        
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        img = self.imgs[idx]
        label = self.labels[idx]
        
        return self.trans(img), torch.tensor(label)


# In[ ]:


# batch_size = 50 # ORIG
batch_size = 40
train_set = DigDataset(train_img, train_label)
val_set = DigDataset(val_img, val_label)

train_loader = data_util.DataLoader(train_set, batch_size=batch_size, num_workers=2, pin_memory=True, shuffle=True)
val_loader = data_util.DataLoader(val_set, batch_size=batch_size, num_workers=2, pin_memory=True, shuffle=False)


# In[ ]:


cuda = torch.cuda.is_available()


# In[ ]:


cuda


# In[ ]:


def generate_matrix(gt, pre, num_class=10):
        mask = (gt >= 0) & (gt < num_class)
        label = num_class * gt[mask].astype('int') + pre[mask]
        count = np.bincount(label, minlength=num_class**2)
        confusion_matrix = count.reshape(num_class, num_class)
        return confusion_matrix


# In[ ]:


def do_train(model, optim, data_loader, epoch):
    model.train()
    confusion_matrix = np.zeros((10, 10))
    tbar = tqdm_notebook(train_loader)
    for img, label in tbar:
        if cuda:
            img, label = img.cuda(), label.cuda()
        
        optim.zero_grad()
        logit = model(img)
        loss = F.cross_entropy(logit, label)
        loss.backward()
        optim.step()
        
        pred = torch.argmax(logit, dim=1)
        batch_acc = (pred == label).sum() / len(pred)
        tbar.set_description(f'Train loss: {loss.item():.4f} acc: {batch_acc}')
        confusion_matrix += generate_matrix(label.cpu().numpy(), pred.cpu().numpy())
    
    acc = np.diag(confusion_matrix).sum() / confusion_matrix.sum()
    print(f'Epoch: {epoch_idx} acc: {acc}')
    
def do_eval(model, data_loader, epoch):
    model.eval()
    confusion_matrix = np.zeros((10, 10))
    tbar = tqdm_notebook(train_loader)
    for img, label in tbar:
        if cuda:
            img, label = img.cuda(), label.cuda()
        
        with torch.no_grad():
            logit = model(img)
        loss = F.cross_entropy(logit, label)
        
        pred = torch.argmax(logit, dim=1)
        batch_acc = (pred == label).sum() / len(pred)
        tbar.set_description(f'Val loss: {loss.item():.4f} acc: {batch_acc}')
        confusion_matrix += generate_matrix(label.cpu().numpy(), pred.cpu().numpy())
    
    acc = np.diag(confusion_matrix).sum() / confusion_matrix.sum()
    print(f'Epoch: {epoch_idx} val acc: {acc}')
    return acc


# In[ ]:


epoch = 20
if cuda:
    model = model.cuda()
    
optim = torch.optim.Adam(params=model.parameters())
bst_model = None
bst_acc = 0.
for epoch_idx in range(epoch):
    do_train(model, optim, train_loader, epoch_idx)
    
    val_acc = do_eval(model, val_loader, epoch_idx)
    
    if bst_acc < val_acc:
        bst_model = deepcopy(model)
        bst_acc = val_acc


# ## Test

# In[ ]:


test_df = pd.read_csv('/kaggle/input/Kannada-MNIST/test.csv')


# In[ ]:


test_df.head()


# In[ ]:


test_img, ids = df_to_image(test_df)


# In[ ]:


test_set = DigDataset(test_img, ids)
test_loader = data_util.DataLoader(test_set, batch_size=batch_size, num_workers=2, shuffle=False)


# In[ ]:


submit = {
    'id': [],
    'label': []
}
if cuda:
    bst_model = bst_model.cuda()
for b_imgs, b_ids in tqdm_notebook(test_loader):
    if cuda:
        b_imgs = b_imgs.cuda()
        
    with torch.no_grad():
        logit = bst_model(b_imgs)
        
    pred = torch.argmax(logit, dim=1)
    pred = pred.cpu().numpy()
    submit['label'].extend(pred.tolist())
    submit['id'].extend(b_ids.cpu().numpy().tolist())
    


# In[ ]:


submit_df = pd.DataFrame(submit)
submit_df.head()


# In[ ]:


submit_df.to_csv('submission.csv', index=False)


# In[ ]:


get_ipython().system('head submission.csv')

