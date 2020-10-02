#!/usr/bin/env python
# coding: utf-8

# This is a Fork of my [Densenet169](https://www.kaggle.com/guntherthepenguin/fastai-v1-densenet169/) kernel. The only thing new is I included the [WSI ids](https://www.kaggle.com/tywangty/histopathologiccancerwsi) from this [discussion](https://www.kaggle.com/c/histopathologic-cancer-detection/discussion/83760) to reduce overfitting and correlations between validation and training set.
# Thanks to [SM](https://www.kaggle.com/sermakarevich) for the WSI set and Idea and [Taylor](https://www.kaggle.com/tywangty) for uploading it on kaggle

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import os
from sklearn.metrics import f1_score

from fastai import *
from fastai.vision import *

import torch
import torch.nn as nn
import torchvision
import cv2

from tqdm import tqdm
from skmultilearn.model_selection import iterative_train_test_split
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import roc_auc_score
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '')


# In[ ]:


from torchvision.models import *


# Defining a metric so after epoch I get the validation ROC-AUC score

# In[ ]:


model_path='.'
path='../input/histopathologic-cancer-detection/'
train_folder=f'{path}train'
test_folder=f'{path}test'
train_lbl=f'{path}train_labels.csv'
ORG_SIZE=96

bs=64
num_workers=None # Apprently 2 cpus per kaggle node, so 4 threads I think
sz=96


# In Case I want to run quick tests use a subsample:

# In[ ]:


from pathlib import Path
test_fnames=[str(file) for file in Path(test_folder).iterdir()]


# In[ ]:


df_trn=pd.read_csv(train_lbl)


# In[ ]:


df_WSI=pd.read_csv('../input/histopathologiccancerwsi/patch_id_wsi.csv')


# In[ ]:


tfms = get_transforms(do_flip=True, flip_vert=True, max_rotate=0.0, max_zoom=.15,
                      max_lighting=0.1, max_warp=0.15)


# # Count per WSI id

# ## Take only Ids of which we know the WSI

# ## extract all images we dont know the WSI id of (will go into validation set)

# In[ ]:


df_notinWSI=df_trn.set_index('id').drop(df_WSI.id)


# ## Get 20% of the WSIs as validation set (maybe later make sure its stratified)

# In[ ]:


valWSI=df_WSI.groupby(by='wsi')['id'].count().sample(frac=0.23).index


# In[ ]:


trnWSI=[i[0] for i in df_WSI.groupby(by='wsi')['id'] if i[0] not in valWSI]


# In[ ]:


len(trnWSI),len(valWSI)


# 
# ## get the integer index for all the images with WSIs of the validation set

# In[ ]:


val_idx=np.hstack([df_WSI.groupby(by='wsi')['id'].indices[WSI] for WSI in valWSI])


# In[ ]:


val_idx=np.append(df_notinWSI.index.values,df_WSI.id[val_idx])


# In[ ]:


trn_idx=np.hstack([df_WSI.groupby(by='wsi')['id'].indices[WSI] for WSI in trnWSI])
trn_idx=df_WSI.id[trn_idx]


# In[ ]:


val_idx=df_trn.reset_index().set_index('id').loc[val_idx,'index'].values
trn_idx=df_trn.reset_index().set_index('id').loc[trn_idx,'index'].values


# In[ ]:


np.random.shuffle(val_idx)
np.random.shuffle(trn_idx)


# In[ ]:


src = (ImageList.from_df(df_trn, path=path, suffix='.tif',folder='train')                
                .split_by_idxs(trn_idx,val_idx)
                .label_from_df(label_delim=' '))
src.add_test(test_fnames);


# In[ ]:


data=ImageDataBunch.create_from_ll(src, ds_tfms=tfms, size=sz,bs=bs)
stats=data.batch_stats()        
data.normalize(stats);


# In[ ]:


def auc_score(y_pred,y_true,tens=True):
    score=roc_auc_score(y_true[:,1],torch.sigmoid(y_pred)[:,1])
    if tens:
        score=tensor(score)
    else:
        score=score
    return score



class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2, logits=False, reduce=True):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.logits = logits
        self.reduce = reduce
    def forward(self, inputs, targets):
        if self.logits:
            BCE_loss = F.binary_cross_entropy_with_logits(inputs, targets, reduce=False)
        else:
            BCE_loss = F.binary_cross_entropy(inputs, targets, reduce=False)
        pt = torch.exp(-BCE_loss)
        F_loss = self.alpha * (1-pt)**self.gamma * BCE_loss

        if self.reduce:
            return torch.mean(F_loss)
        else:
            return F_loss
        


# In[ ]:


learn = create_cnn(
    data,
    densenet169,
    path='.',    
    metrics=[auc_score], 
    #loss_func=FocalLoss(logits=True,gamma=1),
    ps=0.5
)


# In[ ]:


x,y=learn.get_preds()


# In[ ]:


auc_score(x,y)


# In[ ]:


learn.lr_find()
learn.recorder.plot()


# In[ ]:


learn.fit_one_cycle(1,1e-2)
learn.recorder.plot()
learn.recorder.plot_losses()


# In[ ]:


learn.unfreeze()
learn.lr_find()


# In[ ]:


learn.recorder.plot()


# ### Warm up with frozen weight is done on a subset so we dont have to waste an entire epoch

# In[ ]:


learn.fit_one_cycle(10,slice(1e-4,1e-3))


# In[ ]:


learn.recorder.plot()


# In[ ]:


learn.recorder.plot_losses()


# In[ ]:


preds,y,losses = learn.get_preds(with_loss=True)
interp = ClassificationInterpretation(learn, preds, y.long(), losses)


# ### Predit the validation data using TTA
# Here for every image we want to predict on, n_augs images are augmented form the original image.
# We can then compare the predictions on for example the image and the image flipped / roated / slightly different crop/ lighting/stretched etc. 
# For now only the diherdral and rotations are used. THis gives a nice extra percent or two when compared to the auc above after training where not TTA is used. 
# I also test if mean or max is better to use on the image and its augments but it can't conclude anything yet.

# In[ ]:


preds,y=learn.get_preds()
pred_score=auc_score(preds,y)
pred_score


# In[ ]:


preds,y=learn.TTA()
pred_score_tta=auc_score(preds,y)
pred_score_tta


# ### Now predict on test set

# In[ ]:


preds_test,y_test=learn.get_preds(ds_type=DatasetType.Test)


# In[ ]:


preds_test_tta,y_test_tta=learn.TTA(ds_type=DatasetType.Test)


# ### prepare submission
# I now load in the sample submission and put my predictions in the label column and save to a new file.

# Sometimes its important in which order the ids in the submissions are so to make sure I don't mess up I put them in the same order. My first submission had a 50% score so I somewhere messed up the order oder the matching of id to label.
# since fname_clean is the id we can just use that as index when adding the correct label in our dataframe. 

# In[ ]:


sub=pd.read_csv(f'{path}/sample_submission.csv').set_index('id')
sub.head()


# In[ ]:


clean_fname=np.vectorize(lambda fname: str(fname).split('/')[-1].split('.')[0])
fname_cleaned=clean_fname(data.test_ds.items)
fname_cleaned=fname_cleaned.astype(str)


# ## I add the score to the name of the file so I can later plot the leaderboard score versus my validation score
# In the fastai course Jeremy mentions that if you have a monotonic relation between validation and LB score the way you set up your validation set matches what the test set consists of.

# In[ ]:


sub.loc[fname_cleaned,'label']=to_np(preds_test[:,1])
sub.to_csv(f'submission_{pred_score}.csv')


# In[ ]:


sub.loc[fname_cleaned,'label']=to_np(preds_test_tta[:,1])
sub.to_csv(f'submission_{pred_score_tta}.csv')


# In[ ]:





# In[ ]:




