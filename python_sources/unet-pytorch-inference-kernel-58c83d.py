#!/usr/bin/env python
# coding: utf-8

# ### UNet Inference kernel
# 
# 

# In[ ]:


# What this is doing? please refer to my above linked kernel
get_ipython().system('pip install ../input/pretrainedmodels/pretrainedmodels-0.7.4/pretrainedmodels-0.7.4/ > /dev/null')
package_path = '../input/unetmodelscript'
import sys
sys.path.append(package_path)


# In[ ]:


import pdb
import os
import cv2
import torch
import pandas as pd
import numpy as np
from tqdm import tqdm
import torch.backends.cudnn as cudnn
from torch.utils.data import DataLoader, Dataset
from albumentations import (Normalize, Compose)
from albumentations.torch import ToTensor
import torch.utils.data as data
from model import Unet


# In[ ]:


#https://www.kaggle.com/paulorzp/rle-functions-run-lenght-encode-decode
def mask2rle(img):
    '''
    img: numpy array, 1 - mask, 0 - background
    Returns run length as string formated
    '''
    pixels= img.T.flatten()
    pixels = np.concatenate([[0], pixels, [0]])
    runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
    runs[1::2] -= runs[::2]
    return ' '.join(str(x) for x in runs)


# In[ ]:


class TestDataset(Dataset):
    '''Dataset for test prediction'''
    def __init__(self, root, df, mean, std):
        self.root = root
        #df['ImageId'] = df['ImageId_ClassId'].apply(lambda x: x.split('_')[0])
        self.fnames = df['ImageId'].unique().tolist()
        self.num_samples = len(self.fnames)
        self.transform = Compose(
            [
                Normalize(mean=mean, std=std, p=1),
                ToTensor(),
            ]
        )

    def __getitem__(self, idx):
        fname = self.fnames[idx]
        path = os.path.join(self.root, fname)
        image = cv2.imread(path)
        images = self.transform(image=image)["image"]
        return fname, images

    def __len__(self):
        return self.num_samples


# In[ ]:


def post_process(probability, threshold, min_size):
    '''Post processing of each predicted mask, components with lesser number of pixels
    than `min_size` are ignored'''
    mask = cv2.threshold(probability, threshold, 1, cv2.THRESH_BINARY)[1]
    num_component, component = cv2.connectedComponents(mask.astype(np.uint8))
    predictions = np.zeros((256, 1600), np.float32)
    num = 0
    for c in range(1, num_component):
        p = (component == c)
        if p.sum() > min_size:
            predictions[p] = 1
            num += 1
    return predictions, num


# In[ ]:


get_ipython().system('ls ../input/unetstartermodelfile/')


# In[ ]:


sample_submission_path = '../input/severstal-steel-defect-detection/sample_submission.csv'
test_data_folder = "../input/severstal-steel-defect-detection/test_images"


# In[ ]:


# initialize test dataloader
best_threshold = 0.5
num_workers = 2
batch_size = 4
print('best_threshold', best_threshold)
min_size = 3500
mean = (0.485, 0.456, 0.406)
std = (0.229, 0.224, 0.225)
df = pd.read_csv(sample_submission_path)
testset = DataLoader(
    TestDataset(test_data_folder, df, mean, std),
    batch_size=batch_size,
    shuffle=False,
    num_workers=num_workers,
    pin_memory=True
)


# In[ ]:


# Initialize mode and load trained weights
ckpt_path = "../input/unetstartermodelfile/model.pth"
device = torch.device("cuda")
model = Unet("resnet18", encoder_weights=None, classes=4, activation=None)
model.to(device)
model.eval()
state = torch.load(ckpt_path, map_location=lambda storage, loc: storage)
model.load_state_dict(state["state_dict"])


# In[ ]:


# start prediction
predictions = []
for i, batch in enumerate(tqdm(testset)):
    fnames, images = batch
    batch_preds = torch.sigmoid(model(images.to(device)))
    batch_preds = batch_preds.detach().cpu().numpy()
    for fname, preds in zip(fnames, batch_preds):
        for cls, pred in enumerate(preds):
            pred, num = post_process(pred, best_threshold, min_size)
            rle = mask2rle(pred)
            #name = fname + f"_{cls+1}"
            name = fname
            cls  = cls + 1
            predictions.append([name,rle,cls])


# In[ ]:


# save predictions to submission.csv
#df = pd.DataFrame(predictions, columns=['ImageId_ClassId', 'EncodedPixels'])
df = pd.DataFrame(predictions, columns=['ImageId', 'EncodedPixels','ClassId'])
print(df.info())


# In[ ]:


df['ImageId_ClassId'] = [(str(df['ImageId'][i])+'_'+str(df['ClassId'][i])) for i in range(len(df))]
df.head()


# In[ ]:


df_submit = df[['ImageId_ClassId','EncodedPixels']]


# In[ ]:


df = pd.read_csv('../input/severstal-steel-defect-detection/sample_submission.csv')
df['EncodedPixels']=['' for i in range(len(df))]


if df.columns[0]=='ImageId_ClassId':
    df.set_index('ImageId_ClassId', inplace=True)
    df_submit.set_index('ImageId_ClassId', inplace=True)

    for name, row in df_submit.iterrows():
        df.loc[name] = row

    df.reset_index(inplace=True)

df.to_csv('submission.csv', index=False)
df.head()

