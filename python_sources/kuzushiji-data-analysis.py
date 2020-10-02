#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
import seaborn as sns
print(os.listdir("../input"))

import matplotlib.pyplot as plt

from PIL import Image, ImageDraw, ImageFont
import tensorflow as tf


# In[ ]:


tf.enable_eager_execution()


# # 1. Load data:

# ## 1.1. Load training data:

# In[ ]:


train_df = pd.read_csv('../input/train.csv')


# In[ ]:


train_df.head()


# In[ ]:


print('Total records of datatframe: ', len(train_df))


# In[ ]:


print('Distinct image id:', len(train_df['image_id'].unique()))


# - So the number of unique image in dataframe is also the number of records, which means each image has 1 label row

# ## 1.2. Load unicode translation:
# - Firstly, you have to download the Japanese font
# - This code is used from https://www.kaggle.com/anokas/kuzushiji-visualisation

# In[ ]:


fontsize = 50

# From https://www.google.com/get/noto/
get_ipython().system('wget -q --show-progress https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip')
get_ipython().system('unzip -p NotoSansCJKjp-hinted.zip NotoSansCJKjp-Regular.otf > NotoSansCJKjp-Regular.otf')
get_ipython().system('rm NotoSansCJKjp-hinted.zip')

font = ImageFont.truetype('./NotoSansCJKjp-Regular.otf', fontsize, encoding='utf-8')


# In[ ]:


unicode_map = {codepoint: char for codepoint, char in pd.read_csv('../input/unicode_translation.csv').values}


# In[ ]:


print('Total unicode character provided:', len(unicode_map))


# 

# # 2. Quick EDA

# - Read the data into tensorflow Dataset

# In[ ]:


def map_name_to_image(image_name):
    img_raw = tf.io.read_file(tf.strings.join(['../input/train_images/', image_name, '.jpg']))
    image = tf.image.decode_jpeg(img_raw)
    return image


# In[ ]:


def map_image_to_width_height(image):
    return tf.shape(image)


# In[ ]:


name_ds = tf.data.Dataset.from_tensor_slices(train_df['image_id'])
image_ds = name_ds.map(map_name_to_image)
image_width_height = image_ds.map(map_image_to_width_height)


# In[ ]:


for img in image_ds:
    print(img.shape)
    break


# In[ ]:


widths = []
heights = []
for width, height, channel in image_width_height:
    widths.append(width.numpy())
    heights.append(height.numpy())


# In[ ]:


# Assign width and height to each image in dataframe
train_df['width'] = pd.Series(widths)
train_df['height'] = pd.Series(heights)


# In[ ]:


train_df.head()


# In[ ]:


sum(train_df['width']==train_df['height'])


# - This visualizing code is used from https://www.kaggle.com/anokas/kuzushiji-visualisation

# In[ ]:


# This function takes in a filename of an image, and the labels in the string format given in train.csv, and returns an image containing the bounding boxes and characters annotated
def visualize_training_data(image_fn, labels):
    # Read image
    imsource = Image.open(image_fn).convert('RGBA')
    bbox_canvas = Image.new('RGBA', imsource.size)
    char_canvas = Image.new('RGBA', imsource.size)
    
    # Convert annotation string to array
    if(labels is not np.nan):
        labels = np.array(labels.split(' ')).reshape(-1, 5)
        bbox_draw = ImageDraw.Draw(bbox_canvas) # Separate canvases for boxes and chars so a box doesn't cut off a character
        char_draw = ImageDraw.Draw(char_canvas)

        for codepoint, x, y, w, h in labels:
            x, y, w, h = int(x), int(y), int(w), int(h)
            char = unicode_map[codepoint] # Convert codepoint to actual unicode character

            # Draw bounding box around character, and unicode character next to it
            bbox_draw.rectangle((x, y, x+w, y+h), fill=(255, 255, 255, 0), outline=(255, 0, 0, 255))
            char_draw.text((x + w + fontsize/4, y + h/2 - fontsize), char, fill=(0, 0, 255, 255), font=font)

        imsource = Image.alpha_composite(Image.alpha_composite(imsource, bbox_canvas), char_canvas)
    imsource = imsource.convert("RGB") # Remove alpha for saving in jpg format.
    return np.asarray(imsource)


# In[ ]:


# plot some image
np.random.seed(1337)

for i in range(10):
    img, labels, w, h = train_df.values[np.random.randint(len(train_df))]
    viz = visualize_training_data('../input/train_images/{}.jpg'.format(img), labels)
    
    plt.figure(figsize=(15, 15))
    plt.title(img)
    plt.imshow(viz, interpolation='lanczos')
    plt.show()


# In[ ]:





# ## 2.1. Image height and width:

# In[ ]:


train_df['aspect_ratio'] = train_df['width'] / train_df['height']


# In[ ]:


train_df.describe()


# - Width and height are not too unequal

# In[ ]:


plt.hist(train_df['width'])
plt.show()


# In[ ]:


plt.hist(train_df['height'])
plt.show()


# ## 2.2. Image labels:
# - First, we are gonna look at some NaN labeled image
# - Then, we will see the distribution of labels (characters) over all training set

# ### 2.2.1. NaN Label:

# In[ ]:


print('Number of image having NaN label:', sum(train_df['labels'].isna()))


# In[ ]:


np.random.seed(2444)

NaN_train_df = train_df[train_df['labels'].isna()]

for i in range(10):
    img, labels, w, h, ar = NaN_train_df.values[np.random.randint(len(NaN_train_df))]
    viz = visualize_training_data('../input/train_images/{}.jpg'.format(img), labels)
    
    plt.figure(figsize=(15, 15))
    plt.title(img)
    plt.imshow(viz, interpolation='lanczos')
    plt.show()


# In[ ]:


NaN_train_df.head()


# ### 2.2.2. Distribution of labels

# In[ ]:


def count_codepoint_freq(labels):
    labels = np.array(labels.split(' ')).reshape(-1, 5)
    code_point = pd.Series(labels[:, 0])
    return code_point.value_counts(sort=False)


# In[ ]:


labels_series = train_df['labels']
all_labels = labels_series.str.cat(sep=' ')
label_counts = count_codepoint_freq(all_labels)


# In[ ]:


print('Number of valid characters in all images: ', len(all_labels))


# In[ ]:


print('Number codepoint appearing in training set: %d, compared to total codepoints in dict: %d'%(len(label_counts), len(unicode_map)))


# - Distribution of 10 different code point in training set

# In[ ]:


plt.figure(figsize=(30, 5))
sns.barplot(label_counts.index[:20], label_counts.values[:20])


# In[ ]:


print('Codepoint that has the most appearance:', np.argmax(label_counts), ' with freq = ', np.max(label_counts))


# In[ ]:


print('Codepoint that has the least appearance:', np.argmin(label_counts), ' with freq = ', np.min(label_counts))


# - We can see that the counts of each code points varies so much compared to each other
# - Below we will see the distribution and histogram of the **value count** of codepoints

# In[ ]:


label_counts.describe()


# In[ ]:


plt.hist(label_counts.values, bins=100)
plt.show()


# - We can see that the mean of characters appearing in training set is 162

# In[ ]:


train_df.to_csv('train_df_plus.csv', index=False)

