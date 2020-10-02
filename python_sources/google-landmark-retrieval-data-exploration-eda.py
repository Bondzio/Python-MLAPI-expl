#!/usr/bin/env python
# coding: utf-8

# ![](https://www.usnews.com/dims4/USNEWS/cf1a1c4/2147483647/resize/1200x%3E/quality/85/?url=http%3A%2F%2Fmedia.beam.usnews.com%2F9d%2F9b%2Fd8dc8f3747b9b147d5c0a7fa1888%2F2-angkor-wat-getty.jpg)
# Angkor: Siem Reap, Cambodia

# # Exploration of the Dataset

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import cv2
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


train_data = pd.read_csv('../input/landmark-retrieval-2020/train.csv')

print("Training data size:",train_data.shape)


# In[ ]:


test_list = glob.glob('../input/landmark-retrieval-2020/test/*/*/*/*')
index_list = glob.glob('../input/landmark-retrieval-2020/index/*/*/*/*')
train_list= glob.glob('../input/landmark-retrieval-2020/train/*/*/*/*')


# In[ ]:


print( 'Query', len(test_list), ' test images in ', len(index_list), 'index images')


# In[ ]:


train_data.info()


# In[ ]:


train_data.head()


# In[ ]:


sns.set()
plt.title('Training set: number of images per class(line plot)')
landmarks_fold = pd.DataFrame(train_data['landmark_id'].value_counts())
landmarks_fold.reset_index(inplace=True)
landmarks_fold.columns = ['landmark_id','count']
ax = landmarks_fold['count'].plot(logy=True, grid=True)
locs, labels = plt.xticks()
plt.setp(labels, rotation=30)
ax.set(xlabel="Landmarks", ylabel="Number of images")


# In[ ]:


sns.set()
landmarks_fold_sorted = pd.DataFrame(train_data['landmark_id'].value_counts())
landmarks_fold_sorted.reset_index(inplace=True)
landmarks_fold_sorted.columns = ['landmark_id','count']
landmarks_fold_sorted = landmarks_fold_sorted.sort_values('landmark_id')
ax = landmarks_fold_sorted.plot.scatter(     x='landmark_id',y='count',
     title='Training set: number of images per class(statter plot)')
locs, labels = plt.xticks()
plt.setp(labels, rotation=30)
ax.set(xlabel="Landmarks", ylabel="Number of images")


# In[ ]:


plt.figure(figsize = (8, 2))
plt.title('Landmark id density plot')
sns.kdeplot(train_data['landmark_id'], color="tomato", shade=True)
plt.show()


# # Test Images Display

# In[ ]:


plt.rcParams["axes.grid"] = True
f, axarr = plt.subplots(6, 5, figsize=(24, 22))

curr_row = 0
for i in range(30):
    example = cv2.imread(test_list[i])
    example = example[:,:,::-1]
    
    col = i%6
    axarr[col, curr_row].imshow(example)
    if col == 5:
        curr_row += 1


# # Index Images Display

# In[ ]:


plt.rcParams["axes.grid"] = True
f, axarr = plt.subplots(6, 5, figsize=(24, 22))

curr_row = 0
for i in range(30):
    example = cv2.imread(index_list[i])
    example = example[:,:,::-1]
    
    col = i%6
    axarr[col, curr_row].imshow(example)
    if col == 5:
        curr_row += 1


# # Train Images Display

# In[ ]:


plt.rcParams["axes.grid"] = True
f, axarr = plt.subplots(6, 5, figsize=(24, 22))

curr_row = 0
for i in range(30):
    example = cv2.imread(train_list[i])
    example = example[:,:,::-1]
    
    col = i%6
    axarr[col, curr_row].imshow(example)
    if col == 5:
        curr_row += 1


# # Train data

# In[ ]:


train_data['landmark_id'].describe()


# In[ ]:


sns.set()
print(train_data.nunique())
train_data['landmark_id'].value_counts().hist()


# In[ ]:


from scipy import stats
sns.set()
res = stats.probplot(train_data['landmark_id'], plot=plt)


# Most frequent landmark ID

# In[ ]:


temp = pd.DataFrame(train_data.landmark_id.value_counts().head(10))
temp.reset_index(inplace=True)
temp.columns = ['landmark_id', 'count']
temp


# In[ ]:


sns.set()
# plt.figure(figsize=(9, 8))
plt.title('Most frequent landmarks')
sns.set_color_codes("pastel")
sns.barplot(x="landmark_id", y="count", data=temp,
            label="Count")
locs, labels = plt.xticks()
plt.setp(labels, rotation=45)
plt.show()


# Least frequent landmark ID

# In[ ]:


temp = pd.DataFrame(train_data.landmark_id.value_counts().tail(10))
temp.reset_index(inplace=True)
temp.columns = ['landmark_id', 'count']
temp


# In[ ]:


sns.set()
# plt.figure(figsize=(9, 8))
plt.title('Least frequent landmarks')
sns.set_color_codes("pastel")
sns.barplot(x="landmark_id", y="count", data=temp,
            label="Count")
locs, labels = plt.xticks()
plt.setp(labels, rotation=45)
plt.show()


# # Feature Extraction

# In[ ]:


dataset_path = '../input/google-image-recognition-tutorial'
img_building = cv2.imread(os.path.join(dataset_path, 'building_1.jpg'))
img_building = cv2.cvtColor(img_building, cv2.COLOR_BGR2RGB)  # Convert from cv's BRG default color order to RGB

orb = cv2.ORB_create()  # OpenCV 3 backward incompatibility: Do not create a detector with `cv2.ORB()`.
key_points, description = orb.detectAndCompute(img_building, None)
img_building_keypoints = cv2.drawKeypoints(img_building, 
                                           key_points, 
                                           img_building, 
                                           flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) # Draw circles.
plt.figure(figsize=(16, 16))
plt.title('ORB Interest Points')
plt.imshow(img_building_keypoints); plt.show()


# The found interest points/features are circled in the image above. As we can see, some of these points are unique to this scene/building like the points near the top of the two towers. However, others like the ones at the top of the tree may not be distinctive.

# In[ ]:


def image_detect_and_compute(detector, img_name):
    """Detect and compute interest points and their descriptors."""
    img = cv2.imread(os.path.join(dataset_path, img_name))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp, des = detector.detectAndCompute(img, None)
    return img, kp, des
    

def draw_image_matches(detector, img1_name, img2_name, nmatches=50):
    """Draw ORB feature matches of the given two images."""
    img1, kp1, des1 = image_detect_and_compute(detector, img1_name)
    img2, kp2, des2 = image_detect_and_compute(detector, img2_name)
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key = lambda x: x.distance) # Sort matches by distance.  Best come first.
    
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:nmatches], img2, flags=2) # Show top 50 matches
    plt.figure(figsize=(16, 16))
    plt.title(type(detector))
    plt.imshow(img_matches); plt.show()
    

orb = cv2.ORB_create()
draw_image_matches(orb, 'building_1.jpg', 'building_2.jpg')


# # Stay Tuned! More to come!

# REFERANCES: 
# * https://www.kaggle.com/seriousran/google-landmark-retrieval-2020-eda
# * https://www.kaggle.com/codename007/a-very-extensive-landmark-exploratory-analysis
# * https://www.kaggle.com/wesamelshamy/image-feature-extraction-and-matching-for-newbies
