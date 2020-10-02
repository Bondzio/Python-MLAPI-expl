#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 

import os
print(os.listdir("../input"))

import zipfile
with zipfile.ZipFile('../input/platesv2/plates.zip', 'r') as zip_obj:
    zip_obj.extractall('/kaggle/working/')
    
print('After zip extraction:')
print(os.listdir("/kaggle/working/"))


# In[ ]:


import torch.nn as nn
import random

import numpy as np
import torch

def init_random_seed(value=0):
    random.seed(value)
    np.random.seed(value)
    torch.manual_seed(value)
    torch.cuda.manual_seed(value)
    torch.backends.cudnn.deterministic = True

init_random_seed(0)


# In[ ]:


import shutil
from tqdm import tqdm
from IPython.display import FileLink

import torch
import torchvision 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import copy

from torchvision import transforms, models

get_ipython().system('pip install git+https://github.com/aleju/imgaug.git')
from imgaug import augmenters as iaa
import imgaug as ia

import PIL
import matplotlib as mpl

import warnings
warnings.filterwarnings("ignore")


# In[ ]:


data_root = '/kaggle/working/plates/'
print(os.listdir(data_root))


# In[ ]:


train_dir = 'train'
val_dir = 'val'

class_names = ['cleaned', 'dirty']

for dir_name in [train_dir, val_dir]:
    for class_name in class_names:
        os.makedirs(os.path.join(dir_name, class_name), exist_ok=True)

for class_name in class_names:
    source_dir = os.path.join(data_root, 'train', class_name)
    for i, file_name in enumerate(tqdm(os.listdir(source_dir))):
        if i % 6 != 0:
            dest_dir = os.path.join(train_dir, class_name) 
        else:
            dest_dir = os.path.join(val_dir, class_name)
        shutil.copy(os.path.join(source_dir, file_name), os.path.join(dest_dir, file_name))


# In[ ]:


mpl.rcParams['axes.grid'] = False
mpl.rcParams['image.interpolation'] = 'nearest'
mpl.rcParams['figure.figsize'] = 45, 75

mean = np.array([0.485, 0.456, 0.406])
std = np.array([0.229, 0.224, 0.225])

def show_dataset(dataset, n=1):
    img = np.vstack((np.hstack((np.asarray(dataset[i][0].permute(1, 2, 0).numpy() * std + mean )for _ in range(n)))
                   for i in range(len(dataset))))
    
    plt.imshow(img)
    plt.axis('off')


# In[ ]:


class ImgAugTransform: 
    def __init__(self):
        self.aug = iaa.Sequential([
            iaa.AddToHueAndSaturation(value=(-10, 10), per_channel=True),
            iaa.MultiplyHue(mul = (-1,1))
        ])

    def __call__(self, img):
        img = np.array(img)
        return self.aug.augment_image(img)

img_transforms = ImgAugTransform()


# In[ ]:


train_transforms = torchvision.transforms.Compose([
    transforms.RandomChoice(transforms = [transforms.RandomRotation(degrees = 60),transforms.RandomRotation(degrees = 90)]),
    transforms.RandomChoice(transforms = [transforms.CenterCrop((224,224)),transforms.RandomCrop((224,224))]),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

train_transforms_aug = torchvision.transforms.Compose([
    ImgAugTransform(),
    lambda x: PIL.Image.fromarray(x),
    transforms.RandomChoice(transforms = [transforms.RandomRotation(degrees = 60),transforms.RandomRotation(degrees = 90)]),
    transforms.RandomChoice(transforms = [transforms.CenterCrop((224,224)),transforms.RandomCrop((224,224))]),
    transforms.RandomChoice(transforms = [transforms.RandomHorizontalFlip()]),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])



val_transforms = torchvision.transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


# In[ ]:


train_dataset = torchvision.datasets.ImageFolder(train_dir,train_transforms)
show_dataset(train_dataset)


# In[ ]:


train_dataset = torchvision.datasets.ImageFolder(train_dir,train_transforms_aug)
val_dataset = torchvision.datasets.ImageFolder(val_dir,val_transforms)
show_dataset(train_dataset)


# In[ ]:


batch_size = 8
train_dataloader = torch.utils.data.DataLoader(train_dataset,batch_size = batch_size,
                                               num_workers = 0,shuffle = True)
val_dataloader = torch.utils.data.DataLoader(val_dataset,batch_size = batch_size,
                                             num_workers = 0,shuffle = False)


# In[ ]:


def train_model(model, loss, optimizer, scheduler, num_epochs, early_stop=None):
    
    loss_history = []
    acc_history = []
    
    best_acc = 0.
    best_loss = 1000000
    
    best_acc_val = 0.
    best_loss_val = 1000000
    
    improve_count = 0
    for epoch in range(num_epochs):
        print('\nEpoch {}/{}:'.format(epoch, num_epochs - 1), flush=True)
        
        for phase in ['train', 'val']:
            if phase == 'train':
                dataloader = train_dataloader
                scheduler.step()
                model.train()  
            else:
                dataloader = val_dataloader
                model.eval()

            running_loss = 0.
            running_acc = 0.
            running_clean = 0.
            running_recall = 0.

            for inputs, labels in dataloader:
                inputs = inputs.to(device)
                labels = labels.to(device)

                
                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    preds = model(inputs)
                    loss_value = loss(preds, labels)
                    preds_class = preds.argmax(dim=1)

                    if phase == 'train':
                        loss_value.backward()
                        optimizer.step()

                running_loss += loss_value.item()
                running_acc += (preds_class == labels.data).float().mean()
                if sum(labels.data) > 0:
                    running_recall += (preds_class[labels.data == 1] == 1).float().mean()

            epoch_loss = running_loss / len(dataloader)
            epoch_acc = running_acc / len(dataloader)
            epoch_recall = running_recall / len(dataloader)
            
            if phase == 'train':
                
                improve_count+=1 
                loss_history.append(epoch_loss)
                acc_history.append(epoch_acc)
            print('{} Loss: {:.4f} Acc: {:.4f} Recall: {:.4f}'.format(phase, epoch_loss, epoch_acc, epoch_recall), flush=True,end = ' ')
            
            if(phase == 'train' and best_loss>epoch_loss and epoch_recall <0.96):
                
                improve_count = 0
                
                best_loss = epoch_loss    
                best_acc = epoch_acc
                
                best_model_train = copy.deepcopy(model)
                save_epoch_train = epoch
                
                print('| save')
                
            elif(phase == 'val' and best_loss_val>epoch_loss):
                
                best_loss_val = epoch_loss    
                best_acc_val = epoch_acc
                
                best_model_val = copy.deepcopy(model)
                save_epoch_val = epoch
                
                print('| save')
                
            elif (phase == 'val' and best_acc_val == epoch_acc and best_loss_val > epoch_loss):
                
                best_loss_val = epoch_loss    
                best_acc_val = epoch_acc
                
                best_model_val = copy.deepcopy(model)
                save_epoch_val = epoch
                print('| save')
            
            else: print('')
            
            if early_stop is not None:
                if(phase == 'val' and improve_count == early_stop):
                    print('\nLoss does not decrease {} epochs, learning is stopped'.format(early_stop))

                    torch.save(best_model_train.state_dict(), "best_model_train.pth")
                    torch.save(best_model_val.state_dict(), "best_model_val.pth")

                    print('\n Saved model from the {}th epoch with the best loss on train'.format(save_epoch_train))
                    print('\n Saved model from the {}th epoch with the best loss on val'.format(save_epoch_val))

                    return loss_history,acc_history
                
     
    torch.save(best_model_train.state_dict(), "best_model_train.pth")
    torch.save(best_model_val.state_dict(), "model_last_epoch.pth")
    torch.save(model.state_dict(), "best_model_val.pth")
    print('\nSaved model from the {}th epoch with the best loss on train'.format(save_epoch_train))
    print('\nSaved model from the {}th epoch with the best loss on val'.format(save_epoch_val))
    
    return loss_history,acc_history


# In[ ]:


def set_parameter_requires_grad(model):
    for param in model.parameters():
        param.requires_grad = False


# In[ ]:


def init_model(model_name, pretrained, device, num_classes=2):
    # https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html
    if model_name == 'densenet':
        model_ft = models.densenet121(pretrained=pretrained)
        set_parameter_requires_grad(model_ft)
        num_ftrs = model_ft.classifier.in_features
        model_ft.classifier = nn.Linear(num_ftrs, num_classes)      
    elif model_name == 'resnet18':
        model_ft = models.resnet18(pretrained=pretrained)
        set_parameter_requires_grad(model_ft)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, num_classes)
    elif model_name == 'resnet34':
        model_ft = models.resnet34(pretrained=pretrained)
        set_parameter_requires_grad(model_ft)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, num_classes)
    elif model_name == 'resnet152':
        model_ft = models.resnet152(pretrained=pretrained)
        set_parameter_requires_grad(model_ft)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, num_classes)
    elif model_name == 'vgg16':
        model_ft = models.vgg16(pretrained=pretrained)
        set_parameter_requires_grad(model_ft)
        num_ftrs = model_ft.classifier[6].in_features
        model_ft.classifier[6] = nn.Linear(num_ftrs,num_classes)
    else:
        raise ValueError(f'Uknown model name {model_name}')
        
#     print(model_ft) 

    model_ft = model_ft.to(device)
    return model_ft


# In[ ]:


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)


# In[ ]:


loss = torch.nn.CrossEntropyLoss()
model = init_model('resnet152', True, device)
optimizer = torch.optim.Adam(model.parameters(), lr=1.0e-3)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size = 7, gamma=0.01)
train_model(model, loss, optimizer, scheduler, num_epochs=90);


# In[ ]:


model = init_model('resnet152', False, device)
model_keys = torch.load("model_last_epoch.pth")
# model_keys = torch.load("best_model_train.pth")
model.load_state_dict(model_keys)
model = model.to(device)


# In[ ]:


test_dir = 'test'
shutil.copytree(os.path.join(data_root, 'test'), os.path.join(test_dir, 'unknown'))


# In[ ]:


class ImageFolderWithPaths(torchvision.datasets.ImageFolder):
    def __getitem__(self, index):
        original_tuple = super(ImageFolderWithPaths, self).__getitem__(index)
        path = self.imgs[index][0]
        tuple_with_path = (original_tuple + (path,))
        return tuple_with_path
    
test_dataset = ImageFolderWithPaths('/kaggle/working/test', val_transforms)

test_dataloader = torch.utils.data.DataLoader(
    test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)


# In[ ]:


model.eval()
test_predictions = []
test_img_paths = []
for inputs, labels, paths in tqdm(test_dataloader):
    inputs, labels = inputs.to(device), labels.to(device)
    with torch.set_grad_enabled(False):
        preds = model(inputs)
    test_predictions.append(
        torch.nn.functional.softmax(preds, dim=1)[:,1].data.cpu().numpy())
    test_img_paths.extend(paths)
    
test_predictions = np.concatenate(test_predictions)


# In[ ]:


mpl.rcParams['figure.figsize'] = 7, 7
def show_input(input_tensor, title=''):
    image = input_tensor.permute(1, 2, 0).numpy()
    image = std * image + mean
    plt.imshow(image.clip(0, 1))
    plt.title(title)
    plt.show()
    plt.pause(0.001)

inputs, labels, paths = next(iter(test_dataloader))

for img, pred in zip(inputs, test_predictions):
    show_input(img, title=pred)


# In[ ]:


submission_df = pd.DataFrame.from_dict({'id': test_img_paths, 'label': test_predictions})
submission_df['label'] = submission_df['label'].map(lambda pred: 'dirty' if pred > 0.6 else 'cleaned')
submission_df['id'] = submission_df['id'].str.replace('/kaggle/working/test/unknown/', '')
submission_df['id'] = submission_df['id'].str.replace('.jpg', '')
submission_df.set_index('id', inplace=True)
submission_df.to_csv('submission.csv')


# In[ ]:


submission_df.label.map({'dirty':1,'cleaned':0}).mean()


# In[ ]:


from IPython.display import FileLink
FileLink(r'submission.csv')


# In[ ]:


FileLink(r'best_model_train.pth')


# In[ ]:


FileLink(r'best_model_val.pth')


# In[ ]:


FileLink(r'model_last_epoch.pth')

