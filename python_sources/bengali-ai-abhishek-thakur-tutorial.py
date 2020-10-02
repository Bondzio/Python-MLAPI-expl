#!/usr/bin/env python
# coding: utf-8

# Ref: https://www.youtube.com/watch?v=8J5Q4mEzRtY&list=PL98nY_tJQXZntH5WUtKB0bghZeKVIJHJc

# * First build a good cross validation system

# # Create folds
# Multilabel classification problem, we can have multiple model, or a single model can do the job
# For multilabel classification, we are using Multilabel Stratified KFold

# In[ ]:


get_ipython().system('pip install iterative-stratification')


# In[ ]:


import pandas as pd
from iterstrat.ml_stratifiers import MultilabelStratifiedKFold

import numpy as np
import joblib
import glob
from tqdm import tqdm

from zipfile import ZipFile


# In[ ]:


if __name__ == "__main__":
    df = pd.read_csv("../input/bengaliai-cv19/train.csv")
    print(df.head())
    df.loc[:, 'kfold'] = -1
    
    #shuffling dataset
    #frac = ?
    df = df.sample(frac = 1).reset_index(drop = True)
    
    x = df.image_id.values
    y = df[["grapheme_root", "vowel_diacritic", "consonant_diacritic"]].values
    
    mskf = MultilabelStratifiedKFold(n_splits = 5)
    
    for fold, (trn_, val_) in enumerate(mskf.split(x, y)):
        print("TRAIN: ", trn_, "VAL: ",  val_)
        df.loc[val_, "kfold"] = fold
        
    print(df.kfold.value_counts())
    


# In[ ]:


df.head()


# In[ ]:


df_1 = pd.read_parquet("../input/bengaliai-cv19/train_image_data_0.parquet")


# In[ ]:


df_1.head()


# # Pickles

# In[ ]:


get_ipython().system('mkdir image_pickles.zip')


# In[ ]:



if __name__ == "__main__":
    files = glob.glob("../input/bengaliai-cv19/train_*.parquet")
    folder = "..output/kaggle/working/image_pickles.zip"
    zipObj = ZipFile(folder, "w")
    for f in files:
        df = pd.read_parquet(f)
        image_ids = df.image_id.values
        df = df.drop("image_id", axis = 1)
        image_array = df.values
        for j, image_id in tqdm(enumerate(image_ids), total = len(image_ids)):
            label = "image_pickles" + image_id + ".pkl"
            joblib.dump(image_array[j, :], label)
            zipObj.write(label)
    zipObj.close()


# Yeah Kaggle :/ whatever

# # Model
# * three different model
# * one model
# 
# First create a dataset class

# In[ ]:


df.head()


# In[ ]:


class BengaliDatasetTrain:
    def __init__(self, folds, img_height, img_width, mean, std):
        df = df
        df = df[["image_id", "grapheme_root", "vowel_diacritic", "consonent_diacritic", "kfold"]]
        
        df = df[df.kfold.isin(folds)].reset_index(drop = True)
        self.image_ids = df.image_id.values
        self.grapheme_root = df.grapheme_root.values
        self.vowel_diacritic = df.vowel_diacritic.values
        self.consonent_diacritic = df.consonent_diacritic.values
        
    def __len__(self):
        return len(self.image_ids)
    
    def __getitem__(self, item):
        image = joblib.load("..input/image_pickles/{self.image_ids[item]}.pkl")
        #image is vector
        image = image.reshape(137, 236).astype(float)
        
    
    

