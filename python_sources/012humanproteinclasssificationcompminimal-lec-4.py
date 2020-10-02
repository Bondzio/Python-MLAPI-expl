#!/usr/bin/env python
# coding: utf-8

# * ***User***: [@manishshah120](https://www.kaggle.com/manishshah120)
# * ***LinkedIn***: https://www.linkedin.com/in/manishshah120/
# * ***GitHub***: https://github.com/ManishShah120
# * ***Twitter***: https://twitter.com/ManishShah120
# 
# > *This Notebook was created while undergoing a course "[Deep Learning with PyTorch: Zero to GANs](https://jovian.ml/forum/t/start-here-welcome-to-deep-learning-with-pytorch-zero-to-gans/1622)" from "jovian.ml" in collaboratoin with "freecodecamp.org"*

# # Human Protein Multi Label Image Classification

# ## Imports

# In[ ]:


import os
import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, random_split, DataLoader
from PIL import Image
import torchvision.models as models
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from sklearn.metrics import f1_score
import torch.nn.functional as F
import torch.nn as nn
from torchvision.utils import make_grid
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Exploring the Data

# The Dataset is not linked with this notebook. This notebook is just a minimal notebook or clone of the actual starter notebook provided by Aakash.

# In[ ]:


DATA_DIR = '../input/jovian-pytorch-z2g/Human protein atlas'

TRAIN_DIR = DATA_DIR + '/train'                           # Contains training images
TEST_DIR = DATA_DIR + '/test'                             # Contains test images

TRAIN_CSV = DATA_DIR + '/train.csv'                       # Contains real labels for training images
TEST_CSV = '../input/jovian-pytorch-z2g/submission.csv'   # Contains dummy labels for test image


# In[ ]:


get_ipython().system('head "{TRAIN_CSV}"')


# In[ ]:


get_ipython().system('head "{TEST_CSV}"')


# In[ ]:


get_ipython().system('ls "{TRAIN_DIR}" | head')


# In[ ]:


train_df = pd.read_csv(TRAIN_CSV)
train_df.head()


# In[ ]:


train_df.info()


# In[ ]:


labels = {
    0: 'Mitochondria',
    1: 'Nuclear bodies',
    2: 'Nucleoli',
    3: 'Golgi apparatus',
    4: 'Nucleoplasm',
    5: 'Nucleoli fibrillar center',
    6: 'Cytosol',
    7: 'Plasma membrane',
    8: 'Centrosome',
    9: 'Nuclear speckles'
}


# In[ ]:


def encode_label(label):
    target = torch.zeros(10)
    for l in str(label).split(' '):
        target[int(l)] = 1.
    return target

def decode_target(target, text_labels=False, threshold=0.5):
    result = []
    for i, x in enumerate(target):
        if (x >= threshold):
            if text_labels:
                result.append(labels[i] + "(" + str(i) + ")")
            else:
                result.append(str(i))
    return ' '.join(result)


# In[ ]:


encode_label('2 4 5')


# In[ ]:


decode_target(torch.tensor([0, 0, 1, 0, 1, 1, 0, 0, 0, 0.]))


# In[ ]:


decode_target(torch.tensor([0, 0, 1, 0, 1, 1, 0, 0, 0, 0.]), text_labels=True)


# ## Creating Datasets & Data Loaders

# In[ ]:


class HumanProteinDataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        self.df = pd.read_csv(csv_file)
        self.transform = transform
        self.root_dir = root_dir
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        row = self.df.loc[idx]
        img_id, img_label = row['Image'], row['Label']
        img_fname = self.root_dir + "/" + str(img_id) + ".png"
        img = Image.open(img_fname)
        if self.transform:
            img = self.transform(img)
        return img, encode_label(img_label)


# In[ ]:


transform = transforms.Compose([transforms.ToTensor()])
dataset = HumanProteinDataset(TRAIN_CSV, TRAIN_DIR, transform=transform)


# In[ ]:


len(dataset)


# In[ ]:


dataset


# In[ ]:


def show_sample(img, target, invert=True):
    if invert:
        plt.imshow(1 - img.permute((1, 2, 0)))
    else:
        plt.imshow(img.permute(1, 2, 0))
    print('Labels:', decode_target(target, text_labels=True))


# In[ ]:


show_sample(*dataset[0], invert=False)


# In[ ]:


show_sample(*dataset[0])


# ## Training & Validation sets

# In[ ]:


torch.manual_seed(10)


# In[ ]:


val_pct = 0.1
val_size = int(val_pct * len(dataset))
train_size = len(dataset) - val_size


# In[ ]:


train_ds, val_ds = random_split(dataset, [train_size, val_size])
len(train_ds), len(val_ds)


# ### Data Loaders

# In[ ]:


batch_size = 32


# In[ ]:


train_dl = DataLoader(
                      train_ds, 
                      batch_size, 
                      shuffle=True, 
                      num_workers=2, 
                      pin_memory=True
                     )
val_dl = DataLoader(
                    val_ds, 
                    batch_size*2, 
                    num_workers=2, 
                    pin_memory=True
                   )


# In[ ]:


def show_batch(dl, invert=True):
    for images, labels in dl:
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.set_xticks([]); ax.set_yticks([])
        data = 1-images if invert else images
        ax.imshow(make_grid(data, nrow=16).permute(1, 2, 0))
        break


# In[ ]:


show_batch(train_dl)


# ## Model

# In[ ]:


def F_score(output, label, threshold=0.5, beta=1):
    prob = output > threshold
    label = label > threshold

    TP = (prob & label).sum(1).float()
    TN = ((~prob) & (~label)).sum(1).float()
    FP = (prob & (~label)).sum(1).float()
    FN = ((~prob) & label).sum(1).float()

    precision = torch.mean(TP / (TP + FP + 1e-12))
    recall = torch.mean(TP / (TP + FN + 1e-12))
    F2 = (1 + beta**2) * precision * recall / (beta**2 * precision + recall + 1e-12)
    return F2.mean(0)


# In[ ]:


class MultilabelImageClassificationBase(nn.Module):
    def training_step(self, batch):
        images, targets = batch 
        out = self(images)                      
        loss = F.binary_cross_entropy(out, targets)      
        return loss
    
    def validation_step(self, batch):
        images, targets = batch 
        out = self(images)                           # Generate predictions
        loss = F.binary_cross_entropy(out, targets)  # Calculate loss
        score = F_score(out, targets)
        return {'val_loss': loss.detach(), 'val_score': score.detach() }
        
    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()   # Combine losses
        batch_scores = [x['val_score'] for x in outputs]
        epoch_score = torch.stack(batch_scores).mean()      # Combine accuracies
        return {'val_loss': epoch_loss.item(), 'val_score': epoch_score.item()}
    
    def epoch_end(self, epoch, result):
        print("Epoch [{}], train_loss: {:.4f}, val_loss: {:.4f}, val_score: {:.4f}".format(
            epoch, result['train_loss'], result['val_loss'], result['val_score']))


# In[ ]:


class ProteinCnnModel(MultilabelImageClassificationBase):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),


            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),


            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),


            nn.Flatten(), 
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 10),
            nn.Sigmoid()
        )
        
    def forward(self, xb):
        return self.network(xb)


# In[ ]:


class ProteinCnnModel2(MultilabelImageClassificationBase):
    def __init__(self):
        super().__init__()
        # Use a pretrained model
        self.network = models.resnet34(pretrained=True)
        # Replace last layer
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Linear(num_ftrs, 10)
    
    def forward(self, xb):
        return torch.sigmoid(self.network(xb))


# In[ ]:


model = ProteinCnnModel2()
model


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


train_dl = DeviceDataLoader(train_dl, device)
val_dl = DeviceDataLoader(val_dl, device)
to_device(model, device);


# In[ ]:


def try_batch(dl):
    for images, labels in dl:
        print('images.shape:', images.shape)
        out = model(images)
        print('out.shape:', out.shape)
        print('out[0]:', out[0])
        break

try_batch(train_dl)


# ## Training the model

# In[ ]:


from tqdm.notebook import tqdm


# In[ ]:


@torch.no_grad()
def evaluate(model, val_loader):
    model.eval()
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)

def fit(epochs, lr, model, train_loader, val_loader, opt_func=torch.optim.SGD):
    torch.cuda.empty_cache()
    history = []
    optimizer = opt_func(model.parameters(), lr)
    for epoch in range(epochs):
        # Training Phase 
        model.train()
        train_losses = []
        for batch in tqdm(train_loader):
            loss = model.training_step(batch)
            train_losses.append(loss)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        # Validation phase
        result = evaluate(model, val_loader)
        result['train_loss'] = torch.stack(train_losses).mean().item()
        model.epoch_end(epoch, result)
        history.append(result)
    return history


# In[ ]:


model = to_device(ProteinCnnModel2(), device)


# In[ ]:


evaluate(model, val_dl)


# In[ ]:


num_epochs = 5
opt_func = torch.optim.Adam
lr = 0.1


# In[ ]:


history += fit(num_epochs, lr, model, train_dl, val_dl, opt_func)


# In[ ]:


num_epochs = 5
opt_func = torch.optim.Adam
lr = 0.01


# In[ ]:


history += fit(num_epochs, lr, model, train_dl, val_dl, opt_func)


# In[ ]:


num_epochs = 5
opt_func = torch.optim.Adam
lr = 0.01


# In[ ]:


history += fit(num_epochs, lr, model, train_dl, val_dl, opt_func)


# ## Plotting Functions

# In[ ]:


def plot_accuracies(history):
    accuracies = [x['val_score'] for x in history]
    plt.plot(accuracies, '-x')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.title('Accuracy vs. No. of epochs');

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


history


# In[ ]:


plot_accuracies(history)


# In[ ]:


plot_losses(history)


# ### Let's save our work at Jovian

# In[ ]:


get_ipython().system('pip install jovian --upgrade')
import jovian


# In[ ]:


jovian.log_dataset(val_size=val_size, val_pct=val_pct, train_size=train_size)


# In[ ]:


jovian.reset()
jovian.log_hyperparams({
    'num_epochs': num_epochs,
    'opt_func': opt_func.__name__,
    'batch_size': batch_size,
    'lr': lr,
})


# In[ ]:


jovian.log_metrics(train_loss=history[-1]['train_loss'], 
                   val_loss=history[-1]['val_loss'], 
                   val_score=history[-1]['val_score'])


# In[ ]:


jovian.commit(project="zerogans-protein-competition", message="3rd Commit")


# ## Making predictions & submission

# In[ ]:


def predict_single(image):
    xb = image.unsqueeze(0)
    xb = to_device(xb, device)
    preds = model(xb)
    prediction = preds[0]
    print("Prediction: ", prediction)
    show_sample(image, prediction)


# In[ ]:


test_dataset = HumanProteinDataset(TEST_CSV, TEST_DIR, transform=transform)


# In[ ]:


img, target = test_dataset[0]
img.shape


# In[ ]:


predict_single(test_dataset[100][0])


# In[ ]:


predict_single(test_dataset[74][0])


# ## Creating a submission file

# In[ ]:


test_dl = DeviceDataLoader(DataLoader(test_dataset, batch_size, num_workers=2, pin_memory=True), device)


# In[ ]:


@torch.no_grad()
def predict_dl(dl, model):
    torch.cuda.empty_cache()
    batch_probs = []
    for xb, _ in tqdm(dl):
        probs = model(xb)
        batch_probs.append(probs.cpu().detach())
    batch_probs = torch.cat(batch_probs)
    return [decode_target(x) for x in batch_probs]


# In[ ]:


test_preds = predict_dl(test_dl, model)


# In[ ]:


submission_df = pd.read_csv(TEST_CSV)
submission_df.Label = test_preds
submission_df.head()


# In[ ]:


submission_df.head(20)


# We can now save it batck to CSV, and download the file from the sidebar (check the output folder)

# In[ ]:


sub_fname = 'resnet3rd_submission.csv'


# In[ ]:


submission_df.to_csv(sub_fname, index=False)


# ## Save to Jovian

# In[ ]:


get_ipython().system('pip install jovian --upgrade')


# In[ ]:


import jovian


# In[ ]:


jovian.commit(project='zerogans-protein-competition',message='3rd submission default notebook')


# # **THE END**
