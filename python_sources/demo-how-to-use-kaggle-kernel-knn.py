#!/usr/bin/env python
# coding: utf-8

# This demo is intended to demostrate a very straight way to our fellow engineers about how to use Kaggle Kernel.
# Notice: The content is not well polished.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.
train_file = "../input/train.csv"
drData = pd.read_csv(train_file, header = 0)


# In[ ]:


drData.info()
drData.head()


# In[ ]:


import matplotlib.pyplot as plt

images_sel = drData.iloc[0:50,1:]
labels_sel = drData.iloc[0:50,:1]

for i in range(2,8):
    plt.subplot(330 + (i+1))
    img = images_sel.iloc[i].as_matrix()
    img = img.reshape((28,28))
    plt.imshow(img,cmap='gray')
    plt.title(labels_sel.iloc[i,0])


# In[ ]:


vData = drData.copy()
images_sel = vData.iloc[0:50,1:]
images_sel[images_sel > 140] = 255

for i in range(2,8):
    plt.subplot(330 + (i+1))
    img = images_sel.iloc[i].as_matrix()
    img = img.reshape((28,28))
    plt.imshow(img,cmap='gray')
    plt.title(labels_sel.iloc[i,0])


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split

images = drData.iloc[0:10000,1:]
labels = drData.iloc[0:10000,:1]
images = images / 255

X_train, X_test, y_train, y_test = train_test_split(images, labels)


# Check which KNN n_neighbors has best result. In most runs, the n_neighbors=5 has the best results.
# You can also replace 255 with 1 to see how everything goes.

# In[ ]:


def tryKnnBestNeighborParam(nbList):
    for idx, val in enumerate(nbList):
        knn = KNeighborsClassifier(n_neighbors=val, n_jobs=-1)

        knn.fit(X_train, y_train.values.ravel())
        X_test_predict = knn.predict(X_test)

        print(knn)
        print("Score of neighbor %s: %s\n" % (val, knn.score(X_test, y_test)))


# In[ ]:


nbList = [4,5,6,7,8]

tryKnnBestNeighborParam(nbList)


# Let's check which pixel filter (0, 35, 70, 105, 140, 175, 210, 245) has best result. In most runs, filter=0 has the best results.

# In[ ]:


def tryBestFilterParam(fltList):
    for idx, val in enumerate(fltList):
        drData = pd.read_csv(train_file, header = 0)
        images = drData.iloc[0:10000,1:]
        labels = drData.iloc[0:10000,:1]
        # Nomalize daat between 0..1
        images = images / 255

        X_train, X_test, y_train, y_test = train_test_split(images, labels)

        knn = KNeighborsClassifier(n_neighbors=5, n_jobs=-1)

        knn.fit(X_train, y_train.values.ravel())
        X_test_predict = knn.predict(X_test)

        print(knn)
        print("Score of filter %s: %s\n" % (val, knn.score(X_test, y_test)))


# In[ ]:


fltList = [0,35,70,105,140,175,210,245]

tryBestFilterParam(fltList)


# Let's check how algorithm affect the training.

# In[ ]:


def tryBestAlgorithmParam(algList):
    drData = pd.read_csv(train_file, header = 0)
    images = drData.iloc[0:10000,1:]
    labels = drData.iloc[0:10000,:1]
    images = images / 255
    X_train, X_test, y_train, y_test = train_test_split(images, labels)
    
    for idx, val in enumerate(algList):
        knn = KNeighborsClassifier(n_neighbors=5, n_jobs=-1, algorithm=val)

        knn.fit(X_train, y_train.values.ravel())
        X_test_predict = knn.predict(X_test)

        print(knn)
        print("Score of algorithm %s: %s\n" % (val, knn.score(X_test, y_test)))


# In[ ]:


algList = ['auto','ball_tree','kd_tree','brute']

tryBestAlgorithmParam(algList)


# Let's check how the tarining scale affects results.

# In[ ]:


def tryScaleAffection(scaleList):
    for idx, val in enumerate(scaleList):
        drData = pd.read_csv(train_file, header = 0)
        images = drData.iloc[0:val,1:]
        labels = drData.iloc[0:val,:1]
        images = images / 255  
        X_train, X_test, y_train, y_test = train_test_split(images, labels)
    
        knn = KNeighborsClassifier(n_neighbors=5, n_jobs=-1)

        knn.fit(X_train, y_train.values.ravel())
        X_test_predict = knn.predict(X_test)

        print(knn)
        print("Score of scale %s: %s\n" % (val, knn.score(X_test, y_test)))


# In[ ]:


scaleList = [20000,30000,41999]

tryScaleAffection(scaleList)


# Now, let's generate the final training model.

# In[ ]:


drData = pd.read_csv(train_file, header = 0)
images = drData.iloc[0:41999,1:]
labels = drData.iloc[0:41999,:1]
images = images / 255 

X_train, X_test, y_train, y_test = train_test_split(images, labels)

knn = KNeighborsClassifier(n_neighbors=5, n_jobs=-1)

knn.fit(X_train, y_train.values.ravel())
X_test_predict = knn.predict(X_test)

print(knn)
print("Score: %s\n" % (knn.score(X_test, y_test)))


# In[ ]:


test_file = "../input/test.csv"
drTest = pd.read_csv(test_file, header = 0)

drTest.info()
drTest.head()


# In[ ]:


drTest_predict = knn.predict(drTest)


# In[ ]:


submission = pd.DataFrame(
    {
        'ImageId': list(range(1,len(drTest_predict)+1)), 
        'Label': drTest_predict
    })

submission.to_csv('submission_knn_demo.csv', index=False, header=True)

