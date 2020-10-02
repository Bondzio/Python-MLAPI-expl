#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[ ]:


import os
import numpy as np#linear algebra
import pandas as pd#processing dataframes
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
#image processing libraries
import cv2
import glob# for matching the pathnames of the files


# In[ ]:


train_file_path = '../input/landmark-retrieval-2020/train.csv'
df_train = pd.read_csv(train_file_path)


# In[ ]:


df_train.head()


# In[ ]:


df_train.tail()


# In[ ]:


df_train['landmark_id'].describe()


# In[ ]:


print(f'size of the training data is :{df_train.shape}')
print(f'columns present in the dataset :{df_train.columns}')


# # Detect missing information

# In[ ]:


missing= df_train.isnull().sum()
percent = missing/df_train.count()
missing_train_data = pd.concat([missing,percent],axis=1,keys=['Missing','%'])
missing_train_data.head()


# # Visualization

# In[ ]:


sns.set()
print(df_train.nunique)
df_train['landmark_id'].value_counts().plot(kind='hist')


# In[ ]:


plt.title('landmark_id distribution')
sns.distplot(df_train['landmark_id'])


# In[ ]:


# plt.title('Training set: number of images per class')
landmarks_fold_sorted = pd.DataFrame(df_train['landmark_id'].value_counts())
landmarks_fold_sorted.reset_index(inplace=True)
landmarks_fold_sorted.columns = ['landmark_id','count']
landmarks_fold_sorted = landmarks_fold_sorted.sort_values('landmark_id')
ax = landmarks_fold_sorted.plot.scatter(     x='landmark_id',y='count',
     title='Training set: number of images per class(statter plot)')
locs, labels = plt.xticks()
plt.setp(labels, rotation=30)
ax.set(xlabel="Landmarks", ylabel="Number of images")


# In[ ]:


sns.set()
plt.title('Training set : number of images per class(line plot)')
sns.set_color_codes('pastel')
landmarks_folds = pd.DataFrame(df_train['landmark_id'].value_counts())
landmarks_folds.reset_index(inplace=True)
landmarks_folds.columns = ['landmark_id','count']
ax = landmarks_folds['count'].plot(logy=True, grid=True)
locs, labels = plt.xticks()
plt.setp(labels, rotation=30)
ax.set(xlabel="Landmarks", ylabel="Number of images")


# Most frequent landmark ids

# In[ ]:


temp = pd.DataFrame(df_train.landmark_id.value_counts().head(10))
temp.reset_index(inplace=True)
temp.columns = ['landmark_id', 'count']
temp


# In[ ]:


sns.set()
plt.title('Most frequent landmarks')
sns.set_color_codes("pastel")
sns.barplot(x="landmark_id", y="count", data=temp,
            label="Count")
locs, labels = plt.xticks()
plt.setp(labels, rotation=45)
plt.show()


# Least Frequent landmark_ids:
# 

# In[ ]:


temp = pd.DataFrame(df_train.landmark_id.value_counts().tail(10))
temp.reset_index(inplace=True)
temp.columns = ['landmark_id', 'count']
temp


# In[ ]:


sns.set()
plt.figure(figsize=(9, 8))
plt.title('Least frequent landmarks')
sns.set_color_codes("pastel")
sns.barplot(x="landmark_id", y="count", data=temp,
            label="Count")
locs, labels = plt.xticks()
plt.setp(labels, rotation=45)
plt.show()


# # Image retrieval using glob

# In[ ]:


test_list = glob.glob('../input/landmark-retrieval-2020/test/*/*/*/*')
index_list = glob.glob('../input/landmark-retrieval-2020/index/*/*/*/*')


# In[ ]:


print( 'Query', len(test_list), ' test images in ', len(index_list), 'index images')


# In[ ]:


plt.rcParams["axes.grid"] = False
f, axarr = plt.subplots(4, 3, figsize=(24, 22))

curr_row = 0
for i in range(12):
    example = cv2.imread(test_list[i])
    example = example[:,:,::-1]
    
    col = i%4
    axarr[col, curr_row].imshow(example)
    if col == 3:
        curr_row += 1


# # Thank you for reading

# In[ ]:




