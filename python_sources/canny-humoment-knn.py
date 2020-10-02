#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import math
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler 
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from skimage import io
from skimage import feature

import matplotlib.pyplot as plt

import cv2


# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

#for dirname, _, filenames in os.walk('/kaggle/'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


#LOAD IMAGE DATASET
recurve_path = '/kaggle/input/bow-image/bow/1. traditional Recurve Bow'
longbow_path = '/kaggle/input/bow-image/bow/2. Longbow'
compound_path = '/kaggle/input/bow-image/bow/3. Compound Bow'
crossbow_path = '/kaggle/input/bow-image/bow/4. Crossbow'
kyudo_path = '/kaggle/input/bow-image/bow/5. Kyudo Bow'

recurve = os.listdir(recurve_path)
longbow = os.listdir(longbow_path)
compound = os.listdir(compound_path)
crossbow = os.listdir(crossbow_path)
kyudo = os.listdir(kyudo_path)

print('Done')


# In[ ]:


#VISUALISASI
plt.figure(figsize = (12,12))
for i in range(5):
    plt.subplot(1, 5, i+1)
    img = cv2.imread(recurve_path + "/" + recurve[i])
    img = cv2.GaussianBlur(img,(5,5),0)
    plt.imshow(img,cmap='gray')
    plt.title('actual')
    plt.tight_layout()

plt.figure(figsize = (12,12))
for i in range(5):
    plt.subplot(1, 5, i+1)
    img = cv2.imread(recurve_path + "/" + recurve[i])
    edges = cv2.Canny(img,25,255,L2gradient=False)
    plt.imshow(edges,cmap='gray')
    plt.title('Seg. canny')
    plt.tight_layout()
    
plt.figure(figsize = (12,12))
for i in range(5):
    plt.subplot(1, 5, i+1)
    img = cv2.imread(longbow_path + "/" + longbow[i])
    plt.imshow(img)
    plt.title('actual')
    plt.tight_layout()

plt.figure(figsize = (12,12))
for i in range(5):
    plt.subplot(1, 5, i+1)
    img = cv2.imread(longbow_path + "/" + longbow[i])
    edges = cv2.Canny(img,25,255,L2gradient=False)
    plt.imshow(edges,cmap='gray')
    plt.title('Seg. Canny')
    plt.tight_layout()

plt.figure(figsize = (12,12))
for i in range(5):
    plt.subplot(1, 5, i+1)
    img = cv2.imread(compound_path + "/" + compound[i])
    plt.imshow(img)
    plt.title('Actual')
    plt.tight_layout()

plt.figure(figsize = (12,12))
for i in range(5):
    plt.subplot(1, 5, i+1)
    img = cv2.imread(compound_path + "/" + compound[i])
    edges = cv2.Canny(img,25,255,L2gradient=False)
    plt.imshow(edges,cmap='gray')
    plt.title('Seg. Canny')
    plt.tight_layout()
    
plt.figure(figsize = (12,12))
for i in range(5):
    plt.subplot(1, 5, i+1)
    img = cv2.imread(kyudo_path + "/" + kyudo[i])
    plt.imshow(img)
    plt.title('Actual')
    plt.tight_layout()

plt.figure(figsize = (12,12))
for i in range(5):
    plt.subplot(1, 5, i+1)
    img = cv2.imread(kyudo_path + "/" + kyudo[i])
    edges = cv2.Canny(img,25,255,L2gradient=False)
    plt.imshow(edges,cmap='gray')
    plt.title('Seg. Canny')
    plt.tight_layout()

plt.figure(figsize = (12,12))
for i in range(5):
    plt.subplot(1, 5, i+1)
    img = cv2.imread(crossbow_path + "/" + crossbow[i])
    plt.imshow(img)
    plt.title('Actual')
    plt.tight_layout()

plt.figure(figsize = (12,12))
for i in range(5):
    plt.subplot(1, 5, i+1)
    img = cv2.imread(crossbow_path + "/" + crossbow[i])
    edges = cv2.Canny(img,25,255,L2gradient=False)
    plt.imshow(edges,cmap='gray')
    plt.title('Actual')
    plt.tight_layout()

plt.show()


# In[ ]:


#CANNY DAN HUMOMENT
x= 0
x = np.array([['h1','h2','h3','h4','h5','h6','h7','target']])

for i in range(len(recurve)):
    img = cv2.imread('/kaggle/input/bow-image/bow/1. traditional Recurve Bow' + "/" + recurve[i])
    #img = cv2.GaussianBlur(img,(3,3),0)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    #edges = cv2.Sobel(img,cv2.CV_8U,1,1,ksize=5)
    edges = cv2.Canny(img,25,100)
    a = cv2.HuMoments(cv2.moments(edges)).flatten()
    a = np.append(a,'recurve')
    x = np.vstack((x,a))

for i in range(len(longbow)):
    img = cv2.imread('/kaggle/input/bow-image/bow/2. Longbow' + "/" + longbow[i])
    #img = cv2.GaussianBlur(img,(3,3),0)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #edges = cv2.Sobel(img,cv2.CV_8U,1,1,ksize=5)
    edges = cv2.Canny(img,25,100)
    a = cv2.HuMoments(cv2.moments(edges)).flatten()
    a = np.append(a,'longbow')
    x = np.vstack((x,a))

for i in range(len(compound)):
    img = cv2.imread('/kaggle/input/bow-image/bow/3. Compound Bow' + "/" + compound[i])
    #img = cv2.GaussianBlur(img,(3,3),0)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #edges = cv2.Sobel(img,cv2.CV_8U,1,1,ksize=5)
    edges = cv2.Canny(img,25,100)
    a = cv2.HuMoments(cv2.moments(edges)).flatten()
    a = np.append(a,'compound')
    x = np.vstack((x,a))

for i in range(len(crossbow)):
    img = cv2.imread('/kaggle/input/bow-image/bow/4. Crossbow' + "/" + crossbow[i])
    #img = cv2.GaussianBlur(img,(3,3),0)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #edges = cv2.Sobel(img,cv2.CV_8U,1,1,ksize=5)
    edges = cv2.Canny(img,25,100)
    a = cv2.HuMoments(cv2.moments(edges)).flatten()
    a = np.append(a,'crossbow')
    x = np.vstack((x,a))

#for i in range(len(kyudo)):
#    img = cv2.imread(kyudo_path + "/" + kyudo[i])
    #img = cv2.GaussianBlur(img,(3,3),0)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #edges = cv2.Sobel(img,cv2.CV_8U,1,0,ksize=5)
#    edges = cv2.Canny(img,25,100)
 #   a = cv2.HuMoments(cv2.moments(edges)).flatten()
 #   a = np.append(a,'kyudo')
 #   x = np.vstack((x,a))

print('Done')


# In[ ]:


#EXPORT to CSV
np.savetxt("/kaggle/working/bowcanny.csv", x, fmt='%s',delimiter=',' )
print('Done')


# In[ ]:


#LOAD CSV DATASET
dataset = pd.read_csv('/kaggle/working/bowcanny.csv')
print (len(dataset))
print (dataset)


# In[ ]:


#split target and attribute
x = dataset.iloc[:,1:7]
y = dataset.iloc[:,7]

#split train n test dataset
x_train, x_test, y_train, y_test = train_test_split(x,y, random_state=0, test_size=0.1)
print(len(y_test))
print(len(x_train))
print(len(dataset))


# In[ ]:


#SPLITTING VISUALIZATION
plt.figure(figsize=(10,13))
plt.subplot(2,2,1);y_train.value_counts().plot(kind='bar', color=['C0','C1','C2','C3','C4','C5','C6']);plt.title('training')
plt.subplot(2,2,2);y_test.value_counts().plot(kind='bar', color=['C0','C1','C2','C3','C4','C5','C6']);plt.title('testing')
plt.subplot(2,2,3);y_train.value_counts().plot(kind='pie');plt.title('training')
plt.subplot(2,2,4);y_test.value_counts().plot(kind='pie',);plt.title('testing')


# In[ ]:


#scaling data
sc_x = StandardScaler()
x_train = sc_x.fit_transform(x_train)
x_test = sc_x.transform(x_test)
x_train


# In[ ]:


akurasi = 0
ax = np.array([])
px = np.array([])
rx = np.array([])
fx = np.array([])
for x in range(2,len(x_train)): 
    #choose method and fitting
    classifier = KNeighborsClassifier(n_neighbors=x,p=4,metric='euclidean')
    classifier.fit(x_train, y_train)

    #testing data
    y_pred = classifier.predict(x_test)

    #print result
    cm = confusion_matrix(y_test, y_pred)
    tertinggi = accuracy_score(y_test, y_pred)
    ax = np.append(ax,accuracy_score(y_test, y_pred))
    ppx = precision_score(y_test, y_pred,average=None, zero_division=0)
    rrx = recall_score(y_test, y_pred,average=None, zero_division=0)
    ffx = f1_score(y_test, y_pred,average=None, zero_division=0)
    px = np.append(px,ppx[0])
    rx = np.append(rx,rrx[0])
    fx = np.append(fx,ffx[0])
    if tertinggi >= akurasi:
        akurasi = tertinggi
        cmx = cm
        k = x
        a = accuracy_score(y_test, y_pred)
        p = precision_score(y_test, y_pred,average=None)
        r = recall_score(y_test, y_pred,average=None)
        f = f1_score(y_test, y_pred,average=None)
print("K :" , k)
print(cmx)
print("Akurasi :" , a)
print("presisi :" , p)
print("recall :" , r)
print("F-Score :" , f)
print("--------------------------------------------")
plt.figure(figsize=(20,10))
x = np.arange(start=2, stop=len(x_train))
plt.plot(x, ax, '--')
plt.plot(x, px, '--')
plt.plot(x, rx, '--')
plt.plot(x, fx, '--')
plt.title("grafik result")
plt.xlabel("K Value")
plt.ylabel("performa")
plt.legend(["akurasi","presisi", "recall", "f1-score"])
plt.grid()
plt.show()

