#!/usr/bin/env python
# coding: utf-8

# # Extracts Meta-Features from JPG Images and Dicom Images
# 
# This notebook extracts some features for all train and test images and stores them in CSV files for later analysis:
# 
# * Dicom metadata (Study Time, SOP Instance UID, ...)
# * JPG ImageSizes in Bytes, width in pixel, height in pixels
# * mean pixel value
# * mean pixel value for red, green, blue channel
# * histograms for red/green/blue channel with 32 bins
# 
# I use dask for fast parallel processing. To reduce communication overhead to the workers, the workload is batched.

# In[ ]:


from tqdm import tqdm
import os
import pandas as pd 
import numpy as np

import PIL
from PIL import Image

get_ipython().system('pip install pydicom')
import pydicom

from dask.distributed import Client, progress
from dask.distributed import fire_and_forget
from dask.distributed import as_completed

from tlz import partition_all


# In[ ]:


client = Client(threads_per_worker=8, n_workers=1)
client


# In[ ]:


BASEPATH = '../input'
COMPPATH = os.path.join(BASEPATH, 'siim-isic-melanoma-classification')
df_train = pd.read_csv(os.path.join(COMPPATH, 'train.csv'))
df_test = pd.read_csv(os.path.join(COMPPATH, 'test.csv'))
df_sub = pd.read_csv(os.path.join(COMPPATH, 'sample_submission.csv'))


# In[ ]:


#df_train_features = pd.DataFrame(df_train['image_name']).set_index('image_name')
#df_test_features = pd.DataFrame(df_test['image_name']).set_index('image_name')


# In[ ]:


def map_parallel_chunked(lst, func):
    CHUNKSIZE = 16
    
    f_many = lambda chunk: [func(x) for x in chunk]
    chunks = list(partition_all(CHUNKSIZE, lst))
    futures = client.map(f_many, chunks)
    for _ in tqdm(as_completed(futures), total=len(futures), unit='chunks', smoothing=0.2): None

    lst_result = []    
    for chunk in futures:
        for res in chunk.result():
            lst_result.append(res)
            
    return lst_result


# In[ ]:


def get_features_from_jpg(typ, image_name):
    f = os.path.join(COMPPATH, f'jpeg/{typ}/{image_name}.jpg')
    img = Image.open(f)
    
    features = dict()    
    features['image_size_bytes'] = os.path.getsize(f)    
    features['image_size_pixels_x'] = img.size[0]
    features['image_size_pixels_y'] = img.size[1]
    
    if img.width < img.height:
        x = 256
        y = int(img.height * (256/img.width))
    else:
        x = int(img.width * (256/img.height))
        y = 256        
        
    img = img.resize((x,y), resample=PIL.Image.NEAREST)
    
    img = np.array(img)
    
    features['image_mean'] = np.mean(img)
    
    channel_means = np.mean(img, axis=(0,1))
    features['image_mean_r'] = channel_means[0]
    features['image_mean_g'] = channel_means[1]
    features['image_mean_b'] = channel_means[2]
    
    bins = np.array(list(range(33)))*8
    features['image_hist_r'] = np.histogram(img[:,:,0].flatten(), bins=bins)[0]
    features['image_hist_g'] = np.histogram(img[:,:,1].flatten(), bins=bins)[0]
    features['image_hist_b'] = np.histogram(img[:,:,2].flatten(), bins=bins)[0]
    
    return features


# In[ ]:


def get_dataframe_from_jpg_features(features):

    df = pd.DataFrame(features)

    df_r = pd.DataFrame(df["image_hist_r"].to_list(), columns=[f'image_hist_r_{i}' for i in range(32)])
    df_g = pd.DataFrame(df["image_hist_g"].to_list(), columns=[f'image_hist_g_{i}' for i in range(32)])
    df_b = pd.DataFrame(df["image_hist_b"].to_list(), columns=[f'image_hist_b_{i}' for i in range(32)])

    df = df.join([df_r, df_g, df_b])

    del df['image_hist_r']
    del df['image_hist_g']
    del df['image_hist_b']
    
    return  df


# In[ ]:


feat = map_parallel_chunked(df_train["image_name"].values, lambda x: get_features_from_jpg('train', x))
df_train_features_jpg = get_dataframe_from_jpg_features(feat)
df_train_features_jpg["image_name"] = df_train["image_name"]

feat = map_parallel_chunked(df_test["image_name"].values, lambda x: get_features_from_jpg('test', x))
df_test_features_jpg = get_dataframe_from_jpg_features(feat)
df_test_features_jpg["image_name"] = df_test["image_name"]


# In[ ]:


df_train_features_jpg


# In[ ]:


def get_features_from_dicom(typ, image_name):
    f = os.path.join(COMPPATH, f'{typ}/{image_name}.dcm')
    ds = pydicom.read_file(f)
    features = dict()
    for elem in ds:
        desc = pydicom.datadict.dictionary_description(elem.tag)
        if not desc == 'Pixel Data':
            features[desc] = str(elem.value)            
    return features


# In[ ]:


feat = map_parallel_chunked(df_train["image_name"].values, lambda x: get_features_from_dicom('train', x))
df_train_features_dicom = pd.DataFrame(feat)
df_train_features_dicom["image_name"] = df_train["image_name"]

feat = map_parallel_chunked(df_test["image_name"].values, lambda x: get_features_from_dicom('test', x))
df_test_features_dicom = pd.DataFrame(feat)
df_test_features_dicom["image_name"] = df_test["image_name"]


# In[ ]:


df_train_features_dicom


# In[ ]:


df_train_features_jpg.to_csv("train_features_jpg.csv", index=False)
df_test_features_jpg.to_csv("test_features_jpg.csv", index=False)

df_train_features_dicom.to_csv("train_features_dicom.csv", index=False)
df_test_features_dicom.to_csv("test_features_dicom.csv", index=False)


# In[ ]:


get_ipython().system('ls -l ')


# You can split the "SOP Instance UID" into the individual parts with following snippet.

# In[ ]:


df_splitted = df_train_features_dicom["SOP Instance UID"].apply(lambda x: pd.Series(x.split('.')))
df_splitted


# Using DataFrame.describe() we can see that most parts of the ID are constant, but not all.

# In[ ]:


df_splitted.describe(include='all')


# Column 9, 10 and 11 are not always constant. Do they contain useful information?
# 
# Part 9 - could be
# Part 10 - could be
# Part 11 - dont think so. Every entry is unique like the 'image_name'
# 
# 
# Please upvote if you like this notebook. Thank you :-)
