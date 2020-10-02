#!/usr/bin/env python
# coding: utf-8

# # Your first submission on Kaggle for the Global Wheat Detection challenge !
# 
# > If it is your first Kaggle competition, it is the right place to start your journey toward counting wheat head like a jedi !
# 
# You can find way better notebook to get an insight to the data. An important part is that the origin is available is the train.csv. In the hidden test set, the images comes from different origins. It still wheat head but the data are "out of distribution" (o.o.d), when usually the test set is usually independantly and identically distributed. (a very nice introduction on the difference between the two concepts are described here: https://arxiv.org/abs/2004.07780
# 
# The code for training the baseline Faster-RCNN comes from https://www.kaggle.com/pestipeti/pytorch-starter-fasterrcnn-train 
# 
# First difficulty: for the moment, access to internet is disabled so you need to save your model in a dataset and let your submission notebook access it. Dataset can be private. You just have to click on "File" then "Add Data". To run this tutorial, don't forget to add: https://www.kaggle.com/bendvd/torchvisionfasterrcnn
# 
# The submission file needs a prediction string. When there is more than one box to predict, just join the different box string with a space ("confidence_1 x_min_1 y_min_1 x_max_1 y_max_1 confidence_2 x_min_2 y_min_2 x_max_2 y_max_2 etc...")
# 
# I hope it's clear ! Don't hesitate to ask more question below !
# 
# (If you think it was easy for me to create the tutorial... I took me 12 attempts to get it right ! )

# 
# 
# ![alt text](http://www.global-wheat.com/wp-content/uploads/2020/04/ILLU_01_EN-1024x982.jpg "Welcome to the dark side of the force !")
# 

# In[ ]:


import pandas as pd
import numpy as np
import cv2
import os
import re

from PIL import Image

import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2

import torch
import torchvision

from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator

from torch.utils.data import DataLoader, Dataset
from torch.utils.data.sampler import SequentialSampler

from matplotlib import pyplot as plt


DIR_INPUT = '../input/global-wheat-detection'
DIR_TRAIN = f'{DIR_INPUT}/train'
DIR_TEST = f'{DIR_INPUT}/test'


def expand_bbox(x):
    r = np.array(re.findall("([0-9]+[.]?[0-9]*)", x))
    if len(r) == 0:
        r = [-1, -1, -1, -1]
    return r

class WheatDataset(Dataset):

    def __init__(self, dataframe, image_dir, transforms=None):
        super().__init__()

        self.image_ids = dataframe['image_id'].unique()
        self.df = dataframe
        self.image_dir = image_dir
        self.transforms = transforms

    def __getitem__(self, index: int):

        image_id = self.image_ids[index]
        records = self.df[self.df['image_id'] == image_id]

        image = cv2.imread(f'{self.image_dir}/{image_id}.jpg', cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
        image /= 255.0

        boxes = records[['x', 'y', 'w', 'h']].values
        boxes[:, 2] = boxes[:, 0] + boxes[:, 2]
        boxes[:, 3] = boxes[:, 1] + boxes[:, 3]
        
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        area = torch.as_tensor(area, dtype=torch.float32)

        # there is only one class
        labels = torch.ones((records.shape[0],), dtype=torch.int64)
        
        # suppose all instances are not crowd
        iscrowd = torch.zeros((records.shape[0],), dtype=torch.int64)
        
        target = {}
        target['boxes'] = boxes
        target['labels'] = labels
        # target['masks'] = None
        target['image_id'] = torch.tensor([index])
        target['area'] = area
        target['iscrowd'] = iscrowd

        if self.transforms:
            sample = {
                'image': image,
                'bboxes': target['boxes'],
                'labels': labels
            }
            sample = self.transforms(**sample)
            image = sample['image']
            
            target['boxes'] = torch.stack(tuple(map(torch.tensor, zip(*sample['bboxes'])))).permute(1, 0)

        return image, target, image_id

    def __len__(self) -> int:
        return self.image_ids.shape[0]

class Averager:
    def __init__(self):
        self.current_total = 0.0
        self.iterations = 0.0

    def send(self, value):
        self.current_total += value
        self.iterations += 1

    @property
    def value(self):
        if self.iterations == 0:
            return 0
        else:
            return 1.0 * self.current_total / self.iterations

    def reset(self):
        self.current_total = 0.0
        self.iterations = 0.0


# In[ ]:


train_img_number = -1 # I set here a very low number of image for faster training

train_df = pd.read_csv(f'{DIR_INPUT}/train.csv')
train_df.shape
train_df['x'] = -1
train_df['y'] = -1
train_df['w'] = -1
train_df['h'] = -1

train_df[['x', 'y', 'w', 'h']] = np.stack(train_df['bbox'].apply(lambda x: expand_bbox(x)))
train_df.drop(columns=['bbox'], inplace=True)
train_df['x'] = train_df['x'].astype(np.float)
train_df['y'] = train_df['y'].astype(np.float)
train_df['w'] = train_df['w'].astype(np.float)
train_df['h'] = train_df['h'].astype(np.float)
image_ids = train_df['image_id'].unique()
valid_ids = image_ids[train_img_number:]
train_ids = image_ids[:train_img_number]
valid_df = train_df[train_df['image_id'].isin(valid_ids)]
train_df = train_df[train_df['image_id'].isin(train_ids)]
valid_df.shape, train_df.shape


# As you can notice, the train dataset contains very few annotations ! If you want to win, you will have to change that !

# In[ ]:


# load a model; pre-trained on COCO
# Internet is currently disabled so you have to create a dataset to save weight before submitting ! 

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained_backbone=False)
model.load_state_dict(torch.load("../input/torchvisionfasterrcnn/fasterrcnn_resnet50_fpn.pth"))
#torch.save(model.state_dict(),"fasterrcnn_resnet50_fpn.pth")


num_classes = 2  # 1 class (wheat) + background
# get number of input features for the classifier
in_features = model.roi_heads.box_predictor.cls_score.in_features

# replace the pre-trained head with a new one
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)


# In[ ]:


# Albumentations
def get_train_transform():
    return A.Compose([
        A.Flip(0.5),
        ToTensorV2(p=1.0)
    ], bbox_params={'format': 'pascal_voc', 'label_fields': ['labels']})

def get_valid_transform():
    return A.Compose([
        ToTensorV2(p=1.0)
    ], bbox_params={'format': 'pascal_voc', 'label_fields': ['labels']})


# ### Train
# 
# Here you have the code for training. In some papers, instead of putting the whole image, random patches of 512 px X 512 px are sampled from the original images. for prediction, one image is converted to a set of overlapping images and the prediction are merged afterwards

# In[ ]:


def collate_fn(batch):
    return tuple(zip(*batch))

train_dataset = WheatDataset(train_df, DIR_TRAIN, get_train_transform())
valid_dataset = WheatDataset(valid_df, DIR_TRAIN, get_valid_transform())


# split the dataset in train and test set
indices = torch.randperm(len(train_dataset)).tolist()

train_data_loader = DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=False,
    num_workers=4,
    collate_fn=collate_fn
)

valid_data_loader = DataLoader(
    valid_dataset,
    batch_size=8,
    shuffle=False,
    num_workers=4,
    collate_fn=collate_fn
)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

model.to(device)
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
# lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)
lr_scheduler = None

num_epochs = 10

loss_hist = Averager()
itr = 1000

for epoch in range(num_epochs):
    loss_hist.reset()
    
    for images, targets, image_ids in train_data_loader:
        
        images = list(image.to(device) for image in images)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        loss_dict = model(images, targets)

        losses = sum(loss for loss in loss_dict.values())
        loss_value = losses.item()

        loss_hist.send(loss_value)

        optimizer.zero_grad()
        losses.backward()
        optimizer.step()

        if itr % 25 == 0:
            print(f"Iteration #{itr} loss: {loss_value}")

        itr += 1
    
    # update the learning rate
    if lr_scheduler is not None:
        lr_scheduler.step()

    print(f"Epoch #{epoch} loss: {loss_hist.value}")


# ### 4- Make your submission

# i like to have a function that describes well how the prediction is done. It would be way faster if done per batch. Test Time Augmentation would be a very nice idea to test !

# In[ ]:



def model_prediction(image_path,model,device):
    model.eval()
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image /= 255.0
    images = torch.from_numpy(image).float().permute(2,0,1).unsqueeze(0).to(device)
    outputs = model(images)


    outputs = [{k: v.detach().cpu().numpy() for k, v in t.items()} for t in outputs]
    boxes = outputs[0]["boxes"]
    scores = outputs[0]["scores"]
    valid_boxes = boxes[scores > 0.5]
    valid_scores = scores[scores > 0.5]
    return valid_boxes, valid_scores


# In[ ]:


submission = pd.read_csv("/kaggle/input/global-wheat-detection/sample_submission.csv")
submission.head()


# The expected output is then a two columns csv. The first column contains the image_id related to the prediction. PredictionString follow the format "{confidence} {x} {y} {h} {w}" where confidence is a float, and x,y,h and w are integer.

# In[ ]:


from tqdm import tqdm
from pathlib import Path
data_dir = '../input/global-wheat-detection/test'

submission = pd.read_csv(f'{DIR_INPUT}/sample_submission.csv')



root_image = Path("../input/global-wheat-detection/test")
test_images = [root_image / f"{img}.jpg" for img in submission.image_id]


submission = []
model.eval()

for image in tqdm(test_images):
    boxes, scores = model_prediction(str(image),model,device)
    prediction_string = []
    for (x_min,y_min,x_max,y_max),s in zip(boxes,scores):
        x = round(x_min)
        y = round(y_min)
        h = round(x_max-x_min)
        w = round(y_max-y_min)
        prediction_string.append(f"{s} {x} {y} {h} {w}")
    prediction_string = " ".join(prediction_string)
    
    submission.append([image.name[:-4],prediction_string])

sample_submission = pd.DataFrame(submission, columns=["image_id","PredictionString"])
sample_submission.to_csv('submission.csv', index=False)


# 1- When your notebook or script is done, please commit it
# 
# 2- Then go on https://www.kaggle.com/your-name/your-notebook (remove edit/run)
# 
# 3- There is an output tab, you can click on it after committing
# 
# 4- You will find a "submit to competition" button :) 
# 
# 5- Grab a coffee...
# 
# 6- You're on the leaderboard ! 

# In[ ]:




