#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 
import torch
from torch.utils.data import Dataset, random_split, DataLoader
from PIL import Image
import torchvision.models as models
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import torchvision.transforms as T
from sklearn.metrics import f1_score
import torch.nn.functional as F
import torch.nn as nn
from torchvision.utils import make_grid


# Now we will load the training and the testing data. When you start a notebook in a Kaggle Competition, the data is automotically loaded in the /input folder.

# In[ ]:


DATA_DIR = '../input/jovian-pytorch-z2g/Human protein atlas'

TRAIN_DIR = DATA_DIR + '/train'                           # Contains training images
TEST_DIR = DATA_DIR + '/test'                             # Contains test images

TRAIN_CSV = DATA_DIR + '/train.csv'                       # Contains real labels for training images
TEST_CSV = '../input/jovian-pytorch-z2g/submission.csv'   # Contains dummy labels for test image


# In[ ]:


train = pd.read_csv(TRAIN_CSV)
test = pd.read_csv(TEST_CSV)


# In[ ]:


train.head()


# In[ ]:


test.head()


# For our understanding and for later use we will create a dictionary of labels with their corresponding protein names.

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


# Now we will encode the labels as vectors of 1's and 0's. For example is the label is `'2 4 5'` then we will encode it as `([0 0 1 0 1 1 0 0 0 0])`

# In[ ]:


# Encoding the labels to vectors
def encode_label(label):
    target = torch.zeros(10)
    for l in str(label).split(' '):
        target[int(l)] = 1.
    return target

# Decoding the vectors back to their original labels
def decode_target(target, text_labels=False, threshold=0.5):
    result = []
    for i, x in enumerate(target):
        if (x >= threshold):
            if text_labels:
                result.append(labels[i] + "(" + str(i) + ")")
            else:
                result.append(str(i))
    return ' '.join(result)


# Let's see if the code works and gives us correct results what we expect....

# In[ ]:


encode_label('2 4 5')


# Okay.... This is correct. Now let's check if we get the original label using the decoding code...

# In[ ]:


decode_target(torch.tensor([0., 0., 1., 0., 1., 1., 0., 0., 0., 0.]))


# Yay! Its giving correct results. Now, lets get the protein names corresponding to the labels. This is the reason we created a dictionary of labels and their corresponding protein names.

# In[ ]:


decode_target(torch.tensor([0., 0., 1., 0., 1., 1., 0., 0., 0., 0.]),text_labels=True)


# ## Let's create Datasets and Dataloaders

# In[ ]:


class HumanProteinDataset(Dataset):
    def __init__(self, df, root_dir, transform=None):
        self.df = df
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


# Now we will do some transformation on the data using the `transfoms` method.

# In[ ]:


train_transform = T.Compose([T.RandomHorizontalFlip(), 
                       T.RandomRotation(10), 
                       T.ColorJitter(brightness=0.1, contrast=0.05, hue=0.1), 
                       T.ToTensor()])
val_transform = T.Compose([T.ToTensor()])


# ## Training and Validation datasets

# In[ ]:


np.random.seed(42)
len_df = np.random.rand(len(train)) < 0.8

train_df = train[len_df].reset_index()
val_df = train[~len_df].reset_index()


# In[ ]:


len(len_df)


# In[ ]:


train_ds = HumanProteinDataset(train_df, TRAIN_DIR, transform=train_transform)
val_ds = HumanProteinDataset(val_df, TRAIN_DIR, transform=val_transform)
len(train_df), len(val_df)


# Let's have a look at how the image of a sample protiein looks like in our dataset.

# In[ ]:


def show_sample(img, target, invert=True):
    if invert:
        plt.imshow(1 - img.permute((1, 2, 0)))
    else:
        plt.imshow(img.permute(1, 2, 0))
    print('Labels:', decode_target(target, text_labels=True))


# In[ ]:


show_sample(*train_ds[0], invert=False)


# Without `invert`

# In[ ]:


show_sample(*train_ds[0])


# You might be wondering what `invert` does? Well, some of the images in our dataset are dark, so in order to make them lighter we use the `invert` function.

# ### Now its time to create DataLoaders:

# In[ ]:


# First we will set a batch size
batch_size = 64


# In[ ]:


# Then we will create training and validation data loaders
train_dl = DataLoader(train_ds, batch_size, shuffle=True, num_workers=2, pin_memory=True)
val_dl = DataLoader(val_ds, batch_size*2, num_workers=2, pin_memory=True)


# In[ ]:


def show_batch(dl, invert=True):
    for images, labels in dl:
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.set_xticks([]); ax.set_yticks([])
        data = 1-images if invert else images
        ax.imshow(make_grid(data, nrow=16).permute(1, 2, 0))
        break


# ## Let's start creating our model:

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
        # Use a pretrained model
        self.network = models.resnet34(pretrained=True)
        # Replace last layer
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Linear(num_ftrs, 10)
    
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


model = ProteinCnnModel()
model


# In[ ]:


# Setting the default device to 'cuda'
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


# ## It's time to train our model:

# In[ ]:


from tqdm.notebook import tqdm


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
        model.epoch_end(epoch, result)
        history.append(result)
    return history


# In[ ]:


model = to_device(ProteinCnnModel(), device)


# In[ ]:


history = [evaluate(model, val_dl)]
history


# First, freeze the ResNet layers and train some epochs. This only trains the final layer to start classifying the images.

# In[ ]:


model.freeze()


# In[ ]:


epochs = 5
max_lr = 0.01
grad_clip = 0.1
weight_decay = 1e-4
opt_func = torch.optim.Adam


# In[ ]:


get_ipython().run_cell_magic('time', '', 'history += fit_one_cycle(epochs, max_lr, model, train_dl, val_dl, \n                         grad_clip=grad_clip, \n                         weight_decay=weight_decay, \n                         opt_func=opt_func)')


# In[ ]:


model.unfreeze()


# In[ ]:


get_ipython().run_cell_magic('time', '', 'history += fit_one_cycle(epochs, 0.001, model, train_dl, val_dl, \n                         grad_clip=grad_clip, \n                         weight_decay=weight_decay, \n                         opt_func=opt_func)')


# In[ ]:


def plot_scores(history):
    scores = [x['val_score'] for x in history]
    plt.plot(scores, '-x')
    plt.xlabel('epoch')
    plt.ylabel('score')
    plt.title('F1 score vs. No. of epochs');


# In[ ]:


plot_scores(history)


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


plot_losses(history)


# In[ ]:


def plot_lrs(history):
    lrs = np.concatenate([x.get('lrs', []) for x in history])
    plt.plot(lrs)
    plt.xlabel('Batch no.')
    plt.ylabel('Learning rate')
    plt.title('Learning Rate vs. Batch no.');


# In[ ]:


plot_lrs(history)


# ## Let's make predictions now:

# In[ ]:


def predict_single(image):
    xb = image.unsqueeze(0)
    xb = to_device(xb, device)
    preds = model(xb)
    prediction = preds[0]
    print("Prediction: ", prediction)
    show_sample(image, prediction)


# In[ ]:


test_dataset = HumanProteinDataset(test, TEST_DIR, transform=train_transform)


# In[ ]:


img, target = test_dataset[0]
img.shape


# In[ ]:


predict_single(test_dataset[100][0])


# In[ ]:


predict_single(test_dataset[74][0])


# In[ ]:


predict_single(test_dataset[105][0])


# In[ ]:


predict_single(test_dataset[0][0])


# In[ ]:


predict_single(test_dataset[2000][0])


# In[ ]:


predict_single(test_dataset[1994][0])


# ## We have to submit it, so let's create a submission file:

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


sub_fname = 'submission.csv'


# In[ ]:


submission_df.to_csv(sub_fname, index=False)


# In[ ]:


get_ipython().system('pip install jovian --upgrade')


# In[ ]:


import jovian


# In[ ]:


jovian.commit(project='zerogans-protein-competition')


# In[ ]:




