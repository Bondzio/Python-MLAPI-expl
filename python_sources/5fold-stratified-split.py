#!/usr/bin/env python
# coding: utf-8

# In this kernel, I want to show how to do stratified 5fold split of data. This is inspired by this [kernel](https://www.kaggle.com/lightforever/severstal-mlcomp-catalyst-train-0-90672-offline) from the recently concluded Steel Competition. Then we will build a dataloader in Pytorch showing how to do 5-fold training.  

# Fist we will need to install `mlcomp` since this library has nice inbuilt `stratified_group_k_fold` module for stratified K-folding. 

# In[ ]:


get_ipython().system('pip install mlcomp')


# In[ ]:


import os
import cv2
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torchvision
import torch.nn.functional as F
import torch.utils.data as data
from collections import Counter
import albumentations
from albumentations.pytorch import ToTensor
from mlcomp.contrib.split import stratified_group_k_fold


# In[ ]:


get_ipython().system('ls ../input/understanding_cloud_organization')


# In[ ]:


train = pd.read_csv('../input/understanding_cloud_organization/train.csv')


# In[ ]:


train.head()


# > First let's create a column called `exists` which will indicate whether the image has mask(s) or not.

# In[ ]:


train['exists'] = train['EncodedPixels'].notnull().astype(int)
train.head()


# > Now let's split the `Image_Label` to get the `image_name` and the corresponding `class_name`. Since the `Label` is a class name(`string`), we will map the `string` to `int` indicating the corresponding class labels; this will be our `class_id` 

# In[ ]:


train['image_name'] = train['Image_Label'].map(lambda x: x.split('_')[0].strip())
train['class_name'] = train['Image_Label'].map(lambda x: x.split('_')[-1])
class_names_dict = {'Fish':1, 'Flower':2, 'Gravel':3, 'Sugar':4}
train['class_id'] = train['class_name'].map(class_names_dict)
train.head()


# > We will now zeroing out the corresponding values in `class_id` for which there exists no mask(s) i.e. `exists == 0`

# In[ ]:


train['class_id'] = [row.class_id if row.exists else 0 for row in train.itertuples()]
train.head()


# Finally we will do stratified 5-fold split based on `class_id` such that in each fold there are enough images from each class. This is where we will use the `stratified_group_k_fold` from `mlcomp`

# In[ ]:


# You can change n_splits to any number you like. 5-fold split is the most common
train['fold'] = stratified_group_k_fold(label='class_id', group_column='image_name', df=train, n_splits=5)
train.head()


# Let's check how many images are there in each from different classes

# In[ ]:


for fold in range(5):
    print('-'*10, f'fold: {fold}', '-'*10)
    df_fold = train[train['fold']==fold]
    print('Images per class: ', Counter(df_fold['class_id']))


# > It looks pretty OK to me. What do you think? Let's save it then!!

# In[ ]:


train.to_csv('df_5fold.csv', index=False)


# > Now, we will use this `train` dataframe to build our fold data-loader in `pytorch`. First we will need some-helper function from this  [kernel](https://www.kaggle.com/ryches/turbo-charging-andrew-s-pytorch/notebook#Setting-up-data-for-training-in-Catalyst).

# In[ ]:


def make_mask(df: pd.DataFrame, image_name: str='img.jpg', shape: tuple = (350, 525)):
    """
    Create mask based on df, image name and shape.
    """
    masks = np.zeros((shape[0], shape[1], 4), dtype=np.float32)
    df = df[df["image_name"] == image_name]
    for idx, im_name in enumerate(df["image_name"].values):
        for classidx, classid in enumerate(["Fish", "Flower", "Gravel", "Sugar"]):
            mask = cv2.imread("../input/understanding-clouds-resized/train_masks_525/train_masks_525/" + classid + im_name)
            if mask is None:
                continue
            if mask[:,:,0].shape != (350,525):
                mask = cv2.resize(mask, (525,350))
            masks[:, :, classidx] = mask[:,:,0]
    masks = masks/255
    return masks


# In[ ]:


get_ipython().system('ls ../input/understanding_cloud_organization')


# In[ ]:


class Cloud_Dataset(data.Dataset):
    def __init__(self, df, mode, transform=None, fold_index=None):
        
        self.df = df
        self.transform = transform
        self.mode = mode
        
        # change to your path
        self.train_image_path = r'../input/understanding-clouds-resized/train_images_525/train_images_525/'
        self.test_image_path = r'../input/understanding_cloud_organization/test_images'

        self.fold_index = None
        self.set_mode(mode, fold_index)

    def set_mode(self, mode, fold_index):
        self.mode = mode
        self.fold_index = fold_index

        if self.mode == 'train':
            self.df_fold = self.df[self.df.fold != fold_index]
            
            self.img_ids = self.df_fold.image_name.values.tolist()
            self.defects = self.df_fold.class_id.values.tolist()
            self.exist_labels = self.df_fold.exists.astype(bool).values

            self.num_data = len(self.df_fold)

        elif self.mode == 'valid':
            self.df_fold = self.df[self.df.fold == fold_index]
            
            self.img_ids = self.df_fold.image_name.values.tolist()
            self.defects = self.df_fold.class_id.values.tolist()
            self.exist_labels = self.df_fold.exists.astype(bool).values

            self.num_data = len(self.df_fold)

        elif self.mode == 'test':
            self.test_list = sorted(os.listdir(self.test_image_path))
            self.num_data = len(self.test_list)

    def __getitem__(self, index):
        if self.fold_index is None and self.mode != 'test':
            print('WRONG!!!!!!! fold index is NONE!!!!!!!!!!!!!!!!!')
            return
        
        if self.mode == 'test':
            image = cv2.imread(os.path.join(self.test_image_path, self.test_list[index]), 1)
            if self.transform:
                sample = {"image": image}
                sample = self.transform(**sample)
                image = sample['image']
            image_id = self.test_list[index].replace('.png', '')
            return image_id, image
        
        elif self.mode != 'test':
            image_id = self.img_ids[index]
            mask = make_mask(self.df_fold, image_id)
            image = cv2.imread(os.path.join(self.train_image_path, image_id), 1)
            
        if self.transform:
            augmented = self.transform(image=image, mask=mask)
            image = augmented['image']
            mask = augmented['mask'] # 1x320x320x4
            mask = mask[0].permute(2, 0, 1) # 1x4x320x320
            
        return image, mask
             
    def __len__(self):
        return self.num_data


# > We will also need a function for generating our `transformation` for `train`, `valid` and `test` loaders.

# In[ ]:



def generate_transforms(mode):
    # MAX_SIZE = 448
    IMAGE_SIZE = [320,320]

    train_transform = albumentations.Compose([
        
        albumentations.HorizontalFlip(p=1),
        albumentations.ElasticTransform(p=1, alpha=120, sigma=120 * 0.05, alpha_affine=120 * 0.03),
        albumentations.Resize(IMAGE_SIZE[0], IMAGE_SIZE[1]),
        albumentations.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, p=1.0),
        ToTensor()
    
    ])


    val_transform = albumentations.Compose([
        albumentations.Resize(IMAGE_SIZE[0], IMAGE_SIZE[1]),
        albumentations.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, p=1.0),
        ToTensor()
    
    ])

    test_transform = albumentations.Compose([
        #albumentations.Resize(IMAGE_SIZE[0], IMAGE_SIZE[1]),
        albumentations.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, p=1.0),
        ToTensor()
    
    ])
    
    
    if mode == 'train':
        return train_transform
    elif mode == 'valid':
        return val_transform
    else:
        return test_transform


# In[ ]:




def get_fold_dataloader(fold_index, mode, batch_size = 16):
    df = pd.read_csv('df_5fold.csv')
    
    dataset = Cloud_Dataset(df, mode, generate_transforms(mode), fold_index) # df, mode, transform=None, fold_index=None
    
    dataloader = torch.utils.data.DataLoader(dataset,
                            batch_size=batch_size,
                            num_workers=0,
                            pin_memory=True,
                            shuffle=mode == 'train',
                            )
    
    return dataloader


# > Let's get our `train_loader`, `valid_loader` and `test_loader`

# In[ ]:


train_loader = get_fold_dataloader(fold_index=0, mode='train')
valid_loader = get_fold_dataloader(fold_index=0, mode='valid')
test_loader = get_fold_dataloader(fold_index=0, mode='test')


# > Time to check if they are working propely as expected or not!

# In[ ]:


for image, mask in train_loader:
    print(image.shape, mask.shape)
    break


# In[ ]:


for image, mask in valid_loader:
    print(image.shape, mask.shape)
    break


# In[ ]:


for image_id, image in test_loader:
    print(image.shape)
    break


# >I guess our loader are working fine as expected. This is my way of creating loaders. Let me know your way?

# Below a pseudo-code for how to do 5-fold training!
# ```python
# for fold in range(num_folds=5):
#     train_loader = get_fold_dataloader(fold_index=fold, mode='train')
#     valid_loader = get_fold_dataloader(fold_index=fold, mode='valid')
#     test_loader = get_fold_dataloader(fold_index=fold, mode='test')
#     
#     train_model(model, train_loader)
#     validate_model(model, valid_loader)
#     test_model(model, test_loader)
#     save_model(model, fold)
# ```
# 
# 

# > I hope this kernel was useful to you in someway. If you have any suggestions/queries, please let me know in the comments.
