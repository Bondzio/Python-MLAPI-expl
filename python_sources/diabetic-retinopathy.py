#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import cv2
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import os
#for dirname, _, filenames in os.walk('/kaggle/input/'):
    #for filename in filenames:
       #os.path.join(dirname, filename)

# Any results you write to the current directory are saved as output.


# In[ ]:


df = pd.read_csv("/kaggle/input/diabetic-retinopathy-resized/trainLabels_cropped.csv", header=None)
df = df.iloc[1:]
num = len(df)
num


# In[ ]:


data_size= 3000


# In[ ]:


s="/kaggle/input/diabetic-retinopathy-resized/resized_train_cropped/resized_train_cropped/"


# In[ ]:


class_list=[]
img=[]

one_cnt=0
zero_cnt=0
for i in range(0,data_size):
    imgloc = s+df.iloc[i,2]+'.jpeg'
    if(df.iloc[i,3]=='0'):
        zero_cnt=zero_cnt+1
        if(zero_cnt%4==0):
            class_list.append(df.iloc[i,3])
            img1 = cv2.imread(imgloc,1)
            img1 = cv2.resize(img1,(350,350))
            img.append(cv2.cvtColor(img1,cv2.COLOR_BGR2RGB))
    elif(df.iloc[i,3]=='2'):
        one_cnt=one_cnt+1
        if(one_cnt%2==0):    
            class_list.append(df.iloc[i,3])
            img1 = cv2.imread(imgloc,1)
            img1 = cv2.resize(img1,(350,350))
            img.append(cv2.cvtColor(img1,cv2.COLOR_BGR2RGB))
            class_list.append(df.iloc[i,3])
            img1 = cv2.imread(imgloc,1)
            img1 = cv2.resize(img1,(350,350))
            img.append(cv2.cvtColor(img1,cv2.COLOR_BGR2RGB))
    else:
            class_list.append(df.iloc[i,3])
            img1 = cv2.imread(imgloc,1)
            img1 = cv2.resize(img1,(350,350))
            img.append(cv2.cvtColor(img1,cv2.COLOR_BGR2RGB))
            class_list.append(df.iloc[i,3])
            img1 = cv2.imread(imgloc,1)
            img1 = cv2.resize(img1,(350,350))
            img.append(cv2.cvtColor(img1,cv2.COLOR_BGR2RGB))


# In[ ]:


new_data_size=len(class_list)


# In[ ]:


#df[3]=pd.to_numeric(df[3])
zero = 0
one = 0
two = 0
three = 0
four = 0
for i in range(0,len(class_list)):
    if(class_list[i]=='0'): zero= zero+1
    elif(class_list[i]=='1'): one= one+1
    elif(class_list[i]=='2'): two= two+1
    elif(class_list[i]=='3'): three= three+1
    elif(class_list[i]=='4'): four= four+1
print(zero, one, two, three, four)


# In[ ]:


img[0][0][0]


# In[ ]:


area_of_exudate=[]
gre = []
for i in range(0,new_data_size):
    img2 = np.array(img[i])
    #r,img2,b=cv2.split(img2)
    r,greencha,b=cv2.split(img2)
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8,8)) 
    curImg = clahe.apply(greencha)
    gre.append(curImg)
    strEl = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
    curImg = cv2.dilate(curImg, strEl)
    curImg = cv2.medianBlur(curImg,5)
    retValue, curImg = cv2.threshold(curImg, 235, 255, cv2.THRESH_BINARY)
    #curImg= cv2.cvtColor(curImg,cv2.COLOR_BGR2RGB)
    
    count = 0
    for i in range (0,350):
        for j in range(0,350):
            if(curImg[i][j] == 255):
                count=count+1
    area_of_exudate.append(count)
print(area_of_exudate)


# In[ ]:


kernel_for_bv = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

def extract_bv(image):

    contrast_enhanced_green_fundus = image
   
    # applying alternate sequential filtering (3 times closing opening)
    r1 = cv2.morphologyEx(contrast_enhanced_green_fundus, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)), iterations = 1)
    R1 = cv2.morphologyEx(r1, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)), iterations = 1)
    r2 = cv2.morphologyEx(R1, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)), iterations = 1)
   
    R2 = cv2.morphologyEx(r2, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)), iterations = 1)
   
    r3 = cv2.morphologyEx(R2, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(23,23)), iterations = 1)
    
    R3 = cv2.morphologyEx(r3, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(23,23)), iterations = 1)
   # cv2.imshow('contrast_enhanced_green_fundus',contrast_enhanced_green_fundus)
    f4 = cv2.subtract(R3,contrast_enhanced_green_fundus)
    f5 = clahe.apply(f4)
   # cv2.imshow('f5',f5)
# removing very small contours through area parameter noise removal
    ret,f6 = cv2.threshold(f5,15,255,cv2.THRESH_BINARY)
    mask = np.ones(f5.shape[:2], dtype="uint8") * 255
    #print(mask)
   # _, contours, _ = cv2.findContours(f6.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(f6.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    for cnt in contours:
        if cv2.contourArea(cnt) <= 200:
            cv2.drawContours(mask, [cnt], -1, 0, -1)
    im = cv2.bitwise_and(f5, f5, mask=mask)
    ret,fin = cv2.threshold(im,15,255,cv2.THRESH_BINARY_INV)
    newfin = cv2.erode(fin, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)), iterations=1)

    # removing blobs of unwanted bigger chunks taking in consideration they are not straight lines like blood
    #vessels and also in an interval of area
    fundus_eroded = cv2.bitwise_not(newfin)	
    xmask = np.ones(image.shape[:2], dtype="uint8") * 255
    xcontours, xhierarchy = cv2.findContours(fundus_eroded.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    for cnt in xcontours:
        shape = "unidentified"
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * peri, False)
        if len(approx) > 4 and cv2.contourArea(cnt) <= 3000 and cv2.contourArea(cnt) >= 100:
            shape = "circle"
        else:
            shape = "veins"
        if(shape=="circle"):
            cv2.drawContours(xmask, [cnt], -1, 0, -1)

    finimage = cv2.bitwise_and(fundus_eroded,fundus_eroded,mask=xmask)
    blood_vessels = cv2.bitwise_not(finimage)
    return blood_vessels


# In[ ]:


area_of_bloodvessel=[]

for i in range(0,new_data_size):
    bloodvessel = extract_bv(gre[i])
    bloodvessel = cv2.resize(bloodvessel,(350,350))
    count = 0
    bloodvessel =255- bloodvessel
    retValue, bloodvessel = cv2.threshold(bloodvessel, 235, 255, cv2.THRESH_BINARY)
    bloodvessel = cv2.dilate(bloodvessel,kernel_for_bv,iterations = 1)
    bloodvessel= cv2.cvtColor(bloodvessel,cv2.COLOR_BGR2RGB)
    
    for i in range (0,350):
        for j in range(0,350):
            if(bloodvessel[i][j][0] == 255):
                count=count+1
    area_of_bloodvessel.append(count)
print(area_of_bloodvessel)   


# In[ ]:


kernelmicro = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))


# In[ ]:


def extract_ma(image):
     
    median = cv2.medianBlur(image,3)

    erosion_ma =255- cv2.erode(median,kernelmicro,iterations = 1)
    ret3,thresh2 = cv2.threshold(erosion_ma,215,255,cv2.THRESH_BINARY)
    closing_ma = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, kernelmicro)
    mask = np.ones(closing_ma.shape[:2], dtype="uint8") * 255
    contours_mn, hierarchy_mn = cv2.findContours(closing_ma, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
   
    for cnt_mn in contours_mn:
        if cv2.contourArea(cnt_mn) <= 70:
            cv2.drawContours(mask, [cnt_mn], -1, 0, -1)
    final_ma = cv2.bitwise_and(closing_ma, closing_ma, mask=mask)
    sub_ma = cv2.subtract(closing_ma,final_ma)
    sub_ma = cv2.morphologyEx(sub_ma, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)), iterations = 1)
    sub_ma =cv2.erode(sub_ma,kernelmicro,iterations = 1)
    return sub_ma


# In[ ]:


area_of_micro = []
for i in range(0,new_data_size):
    count = 0
    mcran = extract_ma(gre[i])
    for i in range (0,350):
        for j in range(0,350):
            if(mcran[i][j] == 255):
                count=count+1
    area_of_micro.append(count)
#print(area_of_micro)


# In[ ]:


print(area_of_micro)


# In[ ]:


X = list(zip(area_of_exudate,area_of_bloodvessel,area_of_micro))
print(len(X))
y = class_list
#df.iloc[0:new_data_size,3:4].values
#print((y))


# In[ ]:


from sklearn.model_selection import train_test_split

X_train, X_test , y_train, y_test = train_test_split(X,y,test_size = .25 ,random_state =0 )

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
Classifier = RandomForestClassifier(n_estimators = 2500, criterion='gini', max_features = 'auto',  random_state=0, oob_score=True, n_jobs=-1, min_samples_split=5)
Classifier.fit(X_train, y_train)


# In[ ]:


y_pred = Classifier.predict(X_test)


# In[ ]:


#print(y_pred)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)
cm


# In[ ]:


from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)


# In[ ]:


y_pred2 = Classifier.predict(X_train)


# In[ ]:


print(y_pred)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_train,y_pred2)
print(cm)

