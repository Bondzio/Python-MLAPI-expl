#!/usr/bin/env python
# coding: utf-8

# ##References
# FASTAI Course Videos and notes
# https://course.fast.ai
# 
# 
# Starter kernels - 
# https://www.kaggle.com/demonplus/fast-ai-starter-with-resnet-50
# https://www.kaggle.com/lhohoz/aptos-fastai-resnet50-with-previous-data
# 
# All custom functions are from public kernels, if I missed any credits please remind me. Will also welcome any suggestion as I am still newbie to this field.
# 
# Please upvote if you find useful.

# Version history - 
# * V7-8 -  Metrics for understanding loss and QWK
# * V8-10 - Tried using Kappascore from fastai but it did not work. 
# * V 11-12 - split train/test using Stratified KFold. Changing Batch size
# * V13 - Using TTA
# 
# Todo - Kfold CV 

# In[ ]:


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import fastai
from fastai import *
from fastai.vision import *
from fastai.callbacks import *
import cv2

import pandas as pd
import matplotlib.pyplot as plt


# In[ ]:


# Making pretrained weights work without needing to find the default filename
if not os.path.exists('/tmp/.cache/torch/checkpoints/'):
        os.makedirs('/tmp/.cache/torch/checkpoints/')
get_ipython().system("cp '../input/resnet50/resnet50.pth' '/tmp/.cache/torch/checkpoints/resnet50-19c8e357.pth'")
get_ipython().system("cp '../input/densenet161/densenet161.pth' '/tmp/.cache/torch/checkpoints/densenet161-8d451a50.pth'")


# In[ ]:


import os
os.listdir('../input/')


# In[ ]:


print('Make sure cudnn is enabled:', torch.backends.cudnn.enabled)


# In[ ]:


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

SEED = 1667
seed_everything(SEED)


# In[ ]:


base_image_dir = os.path.join('..', 'input/aptos2019-blindness-detection/')
train_dir = os.path.join(base_image_dir,'train_images/')
df = pd.read_csv(os.path.join(base_image_dir, 'train.csv'))
df['path'] = df['id_code'].map(lambda x: os.path.join(train_dir,'{}.png'.format(x)))
df = df.drop(columns=['id_code'])
df = df.sample(frac=1).reset_index(drop=True) #shuffle dataframe
df.head(10)


# ## EDA

# Checking the distribution of labels and basic EDA..
# 
# Todo: Training with old competition data, data imbalance etc.

# In[ ]:


len_df = len(df)
print(f"There are {len_df} images")


# In[ ]:


df['diagnosis'].hist(figsize = (10, 5))


# In[ ]:


IMG_SIZE = 256 #512

def crop_image1(img,tol=7):
    # img is image data
    # tol  is tolerance
        
    mask = img>tol
    return img[np.ix_(mask.any(1),mask.any(0))]

def crop_image_from_gray(img,tol=7):
    if img.ndim ==2:
        mask = img>tol
        return img[np.ix_(mask.any(1),mask.any(0))]
    elif img.ndim==3:
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mask = gray_img>tol
        
        check_shape = img[:,:,0][np.ix_(mask.any(1),mask.any(0))].shape[0]
        if (check_shape == 0): # image is too dark so that we crop out everything,
            return img # return original image
        else:
            img1=img[:,:,0][np.ix_(mask.any(1),mask.any(0))]
            img2=img[:,:,1][np.ix_(mask.any(1),mask.any(0))]
            img3=img[:,:,2][np.ix_(mask.any(1),mask.any(0))]
    #         print(img1.shape,img2.shape,img3.shape)
            img = np.stack([img1,img2,img3],axis=-1)
    #         print(img.shape)
        return img

def load_ben_color(path, sigmaX=10):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = crop_image_from_gray(image)
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    image=cv2.addWeighted ( image,4, cv2.GaussianBlur( image , (0,0) , sigmaX) ,-4 ,128)
        
    return image

def _load_format(path, convert_mode, after_open)->Image:
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = crop_image_from_gray(image)
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    image=cv2.addWeighted ( image,4, cv2.GaussianBlur( image , (0,0), 10) ,-4 ,128)
                    
    return Image(pil2tensor(image, np.float32).div_(255)) #return fastai Image format

vision.data.open_image = _load_format


# ## Fast AI Data Block API for Regression

# In[ ]:


# create Stratified validation split (20%)
from sklearn.model_selection import StratifiedKFold
cv = StratifiedKFold(n_splits=5, random_state=42)
tr_ids, val_ids = next(cv.split(df.path, df.diagnosis))
print(len(tr_ids), len(val_ids))
_ = df.loc[val_ids].hist()


# For regression use Floatlist as label class, default CategoryList for classification

# In[ ]:


bs=32   
src = (ImageList.from_df(df=df,path='./',cols='path') #get dataset from dataset
        #.split_by_rand_pct(0.2, seed=42) #Splitting the dataset
       .split_by_idx(val_ids)
        .label_from_df(cols='diagnosis',label_cls=FloatList) #obtain labels from the level column
      )
src


# In[ ]:


tfms = get_transforms(do_flip=True, flip_vert=True, max_rotate=0.10, max_zoom=1.3, max_warp=0.0, max_lighting=0.2)
data = (
    src.transform(tfms,size=128)
    .databunch(bs=bs)
    .normalize(imagenet_stats)
)


# ## Training (Transfer learning)

# The Kaggle competition used the Cohen's quadratically weighted kappa so I have that here to compare. This is a better metric when dealing with imbalanced datasets like this one, and for measuring inter-rater agreement for categorical classification (the raters being the human-labeled dataset and the neural network predictions). Here is an implementation based on the scikit-learn's implementation, but converted to a pytorch tensor, as that is what fastai uses.

# In[ ]:


from sklearn.metrics import cohen_kappa_score
def quadratic_kappa(y_hat, y):
    return torch.tensor(cohen_kappa_score(torch.round(y_hat), y, weights='quadratic'),device='cuda:0')


# In[ ]:


#update1 - kappa from fastai
#kappa = KappaScore()
#kappa.weights = "quadratic"

#update2 - kappa from fastai did not work, I get errors during training, switching to sklearn, need to debug later


# **Training:**
# 
# We use transfer learning, where we retrain the last layers of a pretrained neural network. I use the ResNet and Densenet architectures trained on the ImageNet dataset, which has been commonly used for pre-training applications in computer vision. Fastai makes it quite simple to create a model and train.
# * Pretrained Weights have to be from publicly available datasets from Kaggle and not from internet.
# * resnet slightly better than densenet here

# default loss is cross entropy, we can try some custom loss function 
# 
# learn.loss_func = NewLoss()
# 
# Weight decay during training is another thing needs to be researched

# In[ ]:


learn = cnn_learner(data, base_arch=models.densenet161 ,metrics=[quadratic_kappa], #densenet161
                    callback_fns=[partial(EarlyStoppingCallback, monitor='quadratic_kappa',
                                          min_delta=0.01, patience=3)],
                    model_dir='/kaggle',pretrained=True)
#todo: callback best kappa score or mse for regression
#partial(SaveModel, monitor='quadratic_kappa')


# In[ ]:


learn.lr_find()
learn.recorder.plot(suggestion=True)


# In[ ]:


learn.fit_one_cycle(5, 2e-2)


# Here we are training the last layer, save the weights and next we unfreeze all layers and train

# In[ ]:


learn.recorder.plot_losses()
learn.recorder.plot_metrics()


# In[ ]:


#learn.save('stage-1_dn161')


# In[ ]:


learn.unfreeze()
learn.lr_find()
learn.recorder.plot()


# we will be using a variable learning rate for the various layers. Using 'slice'  takes a start value and a stop value and train the very first layers at a learning rate of 1e-6, and the very last layers at a rate of 1e-4, and distribute all the other layers across that (i.e. between those two values equally).

# In[ ]:


learn.fit_one_cycle(10, max_lr=slice(1e-5,1e-3))


# In[ ]:


learn.export()
learn.save('stage2')
learn.recorder.plot_losses()


# ## Inference

# In[ ]:


learn.show_results(ds_type=DatasetType.Train, rows=4, figsize=(8,10))


# ## Optimize the Metric
# 
# Optimizing the quadratic kappa metric was an important part of the top solutions in the previous competition. Thankfully, @abhishek has already provided code to do this for us. We will use this to improve the score.

# In[ ]:


valid_preds = learn.get_preds(ds_type=DatasetType.Valid)


# In[ ]:


import numpy as np
import pandas as pd
import os
import scipy as sp
from functools import partial
from sklearn import metrics
from collections import Counter
import json


# In[ ]:


class OptimizedRounder(object):
    def __init__(self):
        self.coef_ = 0

    def _kappa_loss(self, coef, X, y):
        X_p = np.copy(X)
        for i, pred in enumerate(X_p):
            if pred < coef[0]:
                X_p[i] = 0
            elif pred >= coef[0] and pred < coef[1]:
                X_p[i] = 1
            elif pred >= coef[1] and pred < coef[2]:
                X_p[i] = 2
            elif pred >= coef[2] and pred < coef[3]:
                X_p[i] = 3
            else:
                X_p[i] = 4

        ll = metrics.cohen_kappa_score(y, X_p, weights='quadratic')
        return -ll

    def fit(self, X, y):
        loss_partial = partial(self._kappa_loss, X=X, y=y)
        initial_coef = [0.5, 1.5, 2.5, 3.5]
        self.coef_ = sp.optimize.minimize(loss_partial, initial_coef, method='nelder-mead')
        print(-loss_partial(self.coef_['x']))

    def predict(self, X, coef):
        X_p = np.copy(X)
        for i, pred in enumerate(X_p):
            if pred < coef[0]:
                X_p[i] = 0
            elif pred >= coef[0] and pred < coef[1]:
                X_p[i] = 1
            elif pred >= coef[1] and pred < coef[2]:
                X_p[i] = 2
            elif pred >= coef[2] and pred < coef[3]:
                X_p[i] = 3
            else:
                X_p[i] = 4
        return X_p

    def coefficients(self):
        return self.coef_['x']


# In[ ]:


optR = OptimizedRounder()
optR.fit(valid_preds[0],valid_preds[1])


# In[ ]:


coefficients = optR.coefficients()
print(coefficients)


# ## TTA
# 
# Test-time augmentation, or TTA, is a commonly-used technique to provide a boost in your score, and is very simple to implement. 
# * Below is custom TTA implementation from one of the public kernels. 
# 

# In[ ]:


from fastai.core import *
from fastai.basic_data import *
from fastai.basic_train import *
from fastai.torch_core import *
def _tta_only(learn:Learner, ds_type:DatasetType=DatasetType.Valid, num_pred:int=10) -> Iterator[List[Tensor]]:
    "Computes the outputs for several augmented inputs for TTA"
    dl = learn.dl(ds_type)
    ds = dl.dataset
    old = ds.tfms
    aug_tfms = [o for o in learn.data.train_ds.tfms]
    try:
        pbar = master_bar(range(num_pred))
        for i in pbar:
            ds.tfms = aug_tfms
            yield get_preds(learn.model, dl, pbar=pbar)[0]
    finally: ds.tfms = old

Learner.tta_only = _tta_only

def _TTA(learn:Learner, beta:float=0, ds_type:DatasetType=DatasetType.Valid, num_pred:int=10, with_loss:bool=False) -> Tensors:
    "Applies TTA to predict on `ds_type` dataset."
    preds,y = learn.get_preds(ds_type)
    all_preds = list(learn.tta_only(ds_type=ds_type, num_pred=num_pred))
    avg_preds = torch.stack(all_preds).mean(0)
    if beta is None: return preds,avg_preds,y
    else:            
        final_preds = preds*beta + avg_preds*(1-beta)
        if with_loss: 
            with NoneReduceOnCPU(learn.loss_func) as lf: loss = lf(final_preds, y)
            return final_preds, y, loss
        return final_preds, y

Learner.TTA = _TTA


# In[ ]:


# remove zoom from FastAI TTA
#tta_params = {'beta':0.12, 'scale':1.0}


# ## Submission
# Let's now create a submission

# In[ ]:


sample_df = pd.read_csv('../input/aptos2019-blindness-detection/sample_submission.csv')
sample_df.head()


# In[ ]:


learn.data.add_test(ImageList.from_df(sample_df,'../input/aptos2019-blindness-detection',folder='test_images',suffix='.png'))
#preds,y = learn.get_preds(ds_type=DatasetType.Test)


# 
# TTA wraps get_preds with augmentation
# TTA parameters I need to research

# In[ ]:



preds,y = learn.TTA(ds_type=DatasetType.Test)
#, **tta_params)


# In[ ]:


test_predictions = optR.predict(preds, coefficients)
sample_df.diagnosis = test_predictions.astype(int)
sample_df.head()
sample_df.to_csv('submission.csv',index=False)


# ## Ensemble - Todo
