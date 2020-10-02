#!/usr/bin/env python
# coding: utf-8

# Thank you to inversion, whose [code](https://www.kaggle.com/inversion/processing-bson-files) I have modified for importing BSON files.
# 
# This kernel is to understand how one could structure their data to run it through Tensor Flow. I have only used the train_example.bson data and have not bothered to split the data into train/dev sets as there are only 82 images in this data. This produces very bad results but hopefully you will find it useful!
# 
# PS: This is my first post.
# 
# 

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import io, bson
import matplotlib.pyplot as plt
from skimage.data import imread   # or, whatever image library you prefer

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# The code below will read the BSON files into a pandas dataframe, and then read the category_id that we are trying to predict into a numpy matrix Y, the images that we are using to predict into a matrix X, and the unique ID's into a matrix X_ids.

# In[ ]:


# Simple data processing
data = bson.decode_file_iter(open('../input/train_example.bson', 'rb'))
# read bson file into pandas DataFrame
with open('../input/train_example.bson','rb') as b:
    df = pd.DataFrame(bson.decode_all(b.read()))

#Get shape of first image 
for e, pic in enumerate(df['imgs'][0]):
        picture = imread(io.BytesIO(pic['picture']))
        pix_x,pix_y,rgb = picture.shape

n = len(df.index) #cols of data in train set
X_ids = np.zeros((n,1)).astype(int)
Y = np.zeros((n,1)).astype(int) #category_id for each row
X_images = np.zeros((n,pix_x,pix_y,rgb)) #m images are 180 by 180 by 3

print("Examples:", n)
print("Dimensions of Y: ",Y.shape)
print("Dimensions of X_images: ",X_images.shape)

# prod_to_category = dict()
i = 0
for c, d in enumerate(data):
    X_ids[i] = d['_id'] 
    Y[i] = d['category_id'] 
    for e, pic in enumerate(d['imgs']):
        picture = imread(io.BytesIO(pic['picture']))
    X_images[i] = picture #add only the last image 
    i+=1


# In[ ]:


#Lets take a look at the category names supplied to us:
df_categories = pd.read_csv('../input/category_names.csv', index_col='category_id')

count_unique_cats = len(df_categories.index)

print("There are ", count_unique_cats, " unique categories to predict. E.g.")
print("")
print(df_categories.head())


# There are 5270 unique categories. You can use the code below to take a look at some of the images and their respective categories.

# In[ ]:


#Function to return the category description from df_categories
def get_category(category_id,level):
    if(level in range(1,4)):
        try:
            return df_categories.iloc[df_categories.index == category_id[0],level-1].values[0]
        except:
            print("Error - category_id does not exist")
    else:
        print("Error - level must be between 1 - 3")

#Play around with the index and cat levels to explore the images in the test data set
index = 3
cat_desc_level = 1 # level 1 - 3
print("ID: ",X_ids[index][0], "category_id: ",Y[index][0], "category_description: ",get_category(Y[index],cat_desc_level))
plt.imshow(X_images[index])


# We will now encode the category_id labels into "one-hot vectors". A one hot vector is 0 in all except one dimension where it is 1. For example in the [MNST](https://www.tensorflow.org/get_started/mnist/beginners) data set a value of 3 would be [0,0,0,1,0,0,0,0,0,0].

# In[ ]:


from sklearn import preprocessing
import warnings

warnings.filterwarnings("ignore") 

#full list of classes
category_classes = df_categories.index.values
category_classes = category_classes.reshape(category_classes.shape[0],1)

#using a label encoder, and binarizer to convert all unique category_ids to have a column for each class 
le = preprocessing.LabelEncoder() 
lb = preprocessing.LabelBinarizer()

le.fit(df_categories.index.values)
y_encoded = le.transform(Y)

lb.fit(y_encoded)
Y_flat = lb.transform(y_encoded)

#redimension X for our model
X_flat = X_images.reshape(X_images.shape[0], -1)
Y_flat = Y_flat
m = X_flat.shape[1]
n = Y_flat.shape[1]

#Scale RGB data for learning
X_flat = X_flat/255
#print results
print("X Shape =", X_flat.shape, "Y Shape =",Y_flat.shape, "m = ",m, "n classes found in test data=", n)


# Below is a simple implementation of logistic regression on the small training set data using tensor flow. For those who are not familiar with tensor flow, their [documentaion](https://www.tensorflow.org/get_started/mnist/beginners) is a good place to start. The results of this is not meant to be meaningful - it is just illustrative of how one might get started with Tensor Flow.

# In[ ]:


import tensorflow as tf

#set up params
sess = tf.Session()
seed = 2
tf.set_random_seed(2)
batch_size = 100
LEARNING_RATE = 1e-4

##nn with one layer
#set up some placeholders which we will feed data into
x = tf.placeholder(tf.float32, [None, m])
y_ = tf.placeholder(tf.float32, [None, n])

#set up a simple network - make sure the dimensions for W and b match
W = tf.Variable(tf.zeros([m, n]))
b = tf.Variable(tf.zeros([n]))
#let Y = Wx + b with a softmax activiation function
y = tf.nn.softmax(tf.matmul(x, W) + b)

#setup the minimisation pronlem with gradient descent
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

#Start a session and run
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
sess.run(train_step, feed_dict={x: X_flat, y_: Y_flat})

#have a look at the results
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

#print results
print(sess.run(accuracy, feed_dict={x: X_flat, y_: Y_flat}))


# Hope that helps! Leave comments below. I am still learning so I will answer them if I know.
