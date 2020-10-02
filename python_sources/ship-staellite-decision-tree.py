#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import json
from matplotlib import pyplot as plt
from skimage import color
from skimage.feature import hog
from sklearn import tree
from sklearn.metrics import classification_report,accuracy_score

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


f = open(r'../input/shipsnet.json')
dataset = json.load(f)
f.close()

dataset.keys()


# In[ ]:


data = np.array(dataset['data']).astype('uint8')


# In[ ]:


data.shape
img_length = 80
data = data.reshape(-1,3,img_length,img_length).transpose([0,2,3,1])
data.shape
plt.imshow(data[5])


# In[ ]:


data_gray = [ color.rgb2gray(i) for i in data]
plt.imshow(data_gray[5])


# In[ ]:


ppc = 16
hog_images = []
hog_features = []
for image in data_gray:
    fd,hog_image = hog(image, orientations=8, pixels_per_cell=(ppc,ppc),cells_per_block=(4, 4),block_norm= 'L2',visualise=True)
    hog_images.append(hog_image)
    hog_features.append(fd)


# In[ ]:


plt.imshow(hog_images[51])


# In[ ]:


labels =  np.array(dataset['labels']).reshape(len(dataset['labels']),1)
print("sdfsdf")


# In[ ]:



clf = tree.DecisionTreeClassifier(random_state=17)


hog_features = np.array(hog_features)
data_frame = np.hstack((hog_features,labels))
np.random.shuffle(data_frame)
print("sdfsdf")


# In[ ]:


percentage = 80
partition = int(len(hog_features)*percentage/100)
print("sdfsdf")


# In[ ]:


x_train, x_test = data_frame[:partition,:-1],  data_frame[partition:,:-1]
y_train, y_test = data_frame[:partition,-1:].ravel() , data_frame[partition:,-1:].ravel()

clf.fit(x_train,y_train)
print("sdfsdf")


# In[ ]:



y_pred = clf.predict(x_test)


# In[ ]:


print("Accuracy: "+str(accuracy_score(y_test, y_pred)))
print('\n')
print(classification_report(y_test, y_pred))

