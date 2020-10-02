#!/usr/bin/env python
# coding: utf-8

#  # Overview 

# I used progressive resizing and transfer-learning (ofc). My learning pipeline is very minimalistic: 1) create two databunches (with default transformations, except for flip_vert) one of size 224 and second of size 448, 2) train model on 224, then unfreeze and train a little bit more, then freeze and train on 448 and then unfreeze and fine tune. So the interesting part of my work was experementing with hyperparametrs, so here are my results
# 
# Here i would just list training times on my best attempts
# 
# * resnet50 public score 0.969 training time on gpu 3 hours 
# * efficientnet-b3 public score 0.964 training time on gpu 1.18 hours (71 minutes)
# * densenet121 public score 0.958 training time on gpu 1.43 hours (86 minutes)
# * efficientnet-b4 public score 0.955 training time on gpu 1.93 hours (115 minutes)
# 
# My best ensemble solution got 0.970
# 

# # Ways to imporve my result 
# Couple of ideas that you can implement:
# 1. Create third databunch of size 768 and fine tune models on it
# 2. densenet161 is really underfitted, so you might train it a few extra epochs and/or increase lr
# 3. Adding one more split in efficientnets will help them train better

# In[ ]:


get_ipython().system('pip install -q efficientnet_pytorch')


# In[ ]:


import numpy as np 
import pandas as pd 
from pathlib import Path

from fastai.imports import *
from fastai import *
from fastai.vision import *

from tqdm import tqdm_notebook as tqdm

base_path = Path('/kaggle/input/plant-pathology-2020-fgvc7/')


# # Get tags from train.csv

# In[ ]:


def get_tag(row):
    if row.healthy:
        return "healthy"
    if row.multiple_diseases:
        return "multiple_diseases"
    if row.rust:
        return "rust"
    if row.scab:
        return "scab"


# In[ ]:


def transform_data(train_labels):
    train_labels.image_id = [image_id+'.jpg' for image_id in train_labels.image_id]
    train_labels['tag'] = [get_tag(train_labels.iloc[idx]) for idx in train_labels.index]
    train_labels.drop(columns=['healthy', 'multiple_diseases', 'rust', 'scab'], inplace=True)


# In[ ]:


train_labels = pd.read_csv(base_path/"train.csv")
path = base_path/"images"


# In[ ]:


transform_data(train_labels)
train_labels = train_labels.set_index("image_id")


# In[ ]:


train_labels.head()


# # Create DataBunches 

# I want first to train my models on small resolution images and then using transfer learning fine-tune them on high resolution images. This approach speeds up learning dramatically and reduces amount of data needet for training. 

# In[ ]:


tfms = get_transforms(max_rotate=30.,flip_vert=True) # all default except for fliping images vertically since these images of leaves, they have no top or bottom


# In[ ]:


src = (ImageList.from_folder(path)
      .filter_by_func(lambda fname: "Train" in fname.name) 
      .split_by_rand_pct()
      .label_from_func(lambda o: train_labels.loc[o.name]['tag']))


# Next two cells actually needs to become single function that takes size and bs as arguments. Since for different models we need different batchsizes

# In[ ]:


def get_data(size, bs):
    data = (src.transform(tfms, size=size)
       .databunch(bs=bs) 
       .normalize())
    return data


# # Training

# I trained 4 models (densenet121, resnet50, efficientnet-b3, efficientnet-b4) and then combined results. Also i used half-precision floating-point format (learner.to_fp16), more info here https://www.quora.com/What-is-the-difference-between-FP16-and-FP32-when-doing-deep-learning

# In[ ]:


from efficientnet_pytorch import EfficientNet

def getModelEff(model_name = 'efficientnet-b4'):
    model = EfficientNet.from_pretrained(model_name)
    if model_name == 'efficientnet-b4':
        model._fc = nn.Linear(1792,4)
    elif model_name == 'efficientnet-b3':
        model._fc = nn.Linear(1536,4)
    return model


# Here are hyperparamentrs that i found out work best, but you should read comments 

# In[ ]:


archs = {
    "resnet50": {
        "model": models.resnet50,
        "epochs_1": 10,
        "epochs_2": 10,
        "epochs_3": 10,
        "epochs_4": 10,
        "max_lr_s1": 0.003,
        "max_lr_s2": slice(1e-5, 3e-4),
        "max_lr_s1_448": 0.003,
        "max_lr_s2_448":slice(1e-5, 3e-4)
    }, 
    "dense121": {
        "model": models.densenet121,
        "epochs_1": 6,
        "epochs_2": 5,
        "epochs_3": 6,
        "epochs_4": 3,
        "max_lr_s1": 0.003,
        "max_lr_s2": slice(1e-5, 3e-4),
        "max_lr_s1_448": 0.003,
        "max_lr_s2_448":slice(1e-5, 1e-4)
    }, 
    "dense161": { # it really underfits, so i need to try more epochs/higher lr
        "model": models.densenet161,
        "epochs_1": 8,
        "epochs_2": 5,
        "epochs_3": 7,
        "epochs_4": 4,
        "max_lr_s1": 1e-3,
        "max_lr_s2": slice(1e-5, 1e-4),
        "max_lr_s1_448": 0.003,
        "max_lr_s2_448":slice(1e-5, 3e-4)
    },  
    "eff-b3": {
        "model": getModelEff('efficientnet-b3'),
        "epochs_1": 7,
        "epochs_2": 3,
        "epochs_3": 5,
        "epochs_4": 2,
        "max_lr_s1": 1e-3,
        "max_lr_s2": slice(1e-5, 1e-4),
        "max_lr_s1_448": 1e-3,
        "max_lr_s2_448":slice(1e-5, 3e-4)
    },
    "eff-b4": {
        "model": getModelEff('efficientnet-b4'),
        "epochs_1": 10,
        "epochs_2": 5,
        "epochs_3": 8,
        "epochs_4": 5,
        "max_lr_s1": 3e-3,
        "max_lr_s2": slice(1e-5, 3e-4),
        "max_lr_s1_448": 1e-3,
        "max_lr_s2_448":slice(1e-5, 1e-4)
    }
}


# In[ ]:


archs = {
    "resnet152": {
        "model_name": "resnet152",
        "model": models.resnet152,
        "stages": [{
            "name_s1": "stage-1_lr",
            "epochs_s1": 10,
            "max_lr_s1": 1e-3,
            "name_s2": "stage-2_lr",
            "epochs_s2": 10,
            "max_lr_s2": slice(1e-5, 1e-4),
            "size": 224,
            "bs": 20
        },
        {
            "name_s1": "stage-1_mr",
            "epochs_s1": 10,
            "max_lr_s1": 1e-3,
            "name_s2": "stage-2_mr",
            "epochs_s2": 10,
            "max_lr_s2": slice(1e-5, 1e-4),
            "size": 448,
            "bs": 10
        },
        {
            "name_s1": "stage-1_hr",
            "epochs_s1": 10,
            "max_lr_s1": 1e-3,
            "name_s2": "stage-2_hr",
            "epochs_s2": 10,
            "max_lr_s2": slice(1e-5, 1e-4),
            "size": 896,
            "bs": 5
        }]
    }
}


# In[ ]:


import gc

def train_model(arch): 
    model_name = arch["model_name"]
    
    print(arch)
    for i, stage in enumerate(arch["stages"]):
        print(f"traing {model_name} on {stage['name_s1']}")
        data = get_data(size=stage["size"], bs=stage["bs"])
        if model_name.startswith("eff"):
            learner = Learner(data, arch["model"], metrics=error_rate).to_fp16() # if we create learner from pytorch model we can't use cnn_learner
            learner.split( lambda m: (arch._conv_head,) ) # we need to tell fastai where to split model to use different lr (from slice)
        else:
            learner = cnn_learner(data, arch["model"], metrics=error_rate).to_fp16()
        learner.model_dir = "/kaggle/working"
        if i != 0:
            learner.load(f"{arch['stages'][i-1]['name_s2']}_{model_name}")
                                             
        print(f"lr for {model_name} {stage['name_s1']}")
        learner.lr_find()
        learner.recorder.plot(suggestion=True)

        learner.fit_one_cycle(stage['epochs_s1'], max_lr=stage['max_lr_s1'])
        learner.save(f"{stage['name_s1']}_{model_name}")
                                             
        print(f"lr for {model_name} {stage['name_s2']}")
        learner.unfreeze()

        learner.lr_find()
        learner.recorder.plot(suggestion=True)

        learner.fit_one_cycle(stage['epochs_s2'], max_lr=stage['max_lr_s2'])
        learner.save(f"{stage['name_s2']}_{model_name}")
        del data
        gc.collect()
        if i == len(arch["stages"])-1:
                return learner
        learner.destroy()
        torch.cuda.empty_cache()


# # Results

# create_results will train model with specified hyper-parametrs and save predictions in csv files, which you can combine how you like

# In[ ]:


def create_results():
    test_images = ImageList.from_folder(base_path/"images")
    test_images.filter_by_func(lambda x: x.name.startswith("Test"))
    
    for model_name in archs:
        arch = archs[model_name]
        learner = train_model(arch)
        
        test_df = pd.read_csv(base_path/"test.csv")
        test_df['healthy'] = [0.0 for _ in test_df.index]
        test_df['multiple_diseases'] = [0.0 for _ in test_df.index]
        test_df['rust'] = [0.0 for _ in test_df.index]
        test_df['scab'] = [0.0 for _ in test_df.index]
        test_df = test_df.set_index('image_id')
        
        for item in tqdm(test_images.items):
            name = item.name[:-4]
            img = open_image(item)
            preds = learner.predict(img)[2]

            test_df.loc[name]['healthy'] = preds[0]
            test_df.loc[name]['multiple_diseases'] = preds[1]
            test_df.loc[name]['rust'] = preds[2]
            test_df.loc[name]['scab'] = preds[3]
            
        test_df.to_csv(f"/kaggle/working/{model_name}_result.csv")
        
        learner.destroy()
        torch.cuda.empty_cache()


# In[ ]:


create_results()


# In[ ]:




