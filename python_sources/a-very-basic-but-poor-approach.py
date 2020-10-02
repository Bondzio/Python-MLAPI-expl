#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
labels=pd.read_csv("D:/data science/toon emotions detection/Dataset/Train.csv")
labels.head()


# In[ ]:


r=labels.iloc[:,1].values
label=np.delete(r,-1)
label1=np.delete(r,-1)


# In[ ]:


emotions=np.unique(label)
emotions


# In[ ]:


o=np.where(emotions=="angry")
o[0][0]


# In[ ]:


import glob
import cv2
from PIL import Image
import numpy as np
image_array=[]
l=[]
for img in glob.glob("D:/data science/toon emotions detection/Dataset/data/*.jpg"):
    image= cv2.imread(img)
    image_from_array = Image.fromarray(image, 'RGB')
    size_image = image_from_array.resize((50,50))
    image_array.append(np.array(size_image))
    p_label=np.where(emotions==label1[0])
    l.append(p_label[0][0])
    label1=np.delete(label1,0)
    
    
len(image_array)


# In[ ]:


data=np.array(image_array)
labels=np.array(l)


# In[ ]:


import matplotlib.pyplot as plt
figure=plt.figure(figsize=(15,10))
ax=figure.add_subplot(121)
ax.imshow(data[0])
bx=figure.add_subplot(122)
bx.imshow(data[60])


# In[ ]:


np.save("Cells",data)
np.save("labels",l)


# In[ ]:


Cells=np.load("Cells.npy")
labels=np.load("labels.npy")


# In[ ]:


s=np.arange(Cells.shape[0])
np.random.shuffle(s)
Cells=Cells[s]
labels=labels[s]


# In[ ]:


num_classes=len(np.unique(labels))
len_data=len(Cells)


# In[ ]:


emotions=np.unique(labels)
emotions


# In[ ]:


x_train,x_test=Cells[(int)(0.1*len_data):],Cells[:(int)(0.1*len_data)]
x_train = x_train.astype('float32')/255
x_test = x_test.astype('float32')/255
train_len=len(x_train)
test_len=len(x_test)


# In[ ]:


y_train,y_test=labels[(int)(0.1*len_data):],labels[:(int)(0.1*len_data)]


# In[ ]:


import keras
y_train=keras.utils.to_categorical(y_train,num_classes)
y_test=keras.utils.to_categorical(y_test,num_classes)


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Dropout,Flatten
from keras.optimizers import RMSprop


# In[ ]:


model=Sequential()
model.add(Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(50,50,3)))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32,kernel_size=2,padding="same",activation="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64,kernel_size=2,padding="same",activation="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(500,activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(5,activation="softmax"))
model.summary()


# In[ ]:


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[ ]:


model.fit(x_train,y_train,batch_size=50,epochs=250,verbose=1)


# In[ ]:


accuracy = model.evaluate(x_test, y_test,verbose=1)
print('\n', 'Test_Accuracy=>', accuracy[1])


# In[ ]:


from keras.models import load_model
model.save('cells.h5')


# # test

# In[ ]:


import glob
import cv2
from PIL import Image
import numpy as np
image_array1=[]
for img in glob.glob("D:/data science/toon emotions detection/Dataset/image_extract/*.jpg"):
    image= cv2.imread(img)
    image_from_array = Image.fromarray(image, 'RGB')
    size_image = image_from_array.resize((50,50))
    image_array1.append(np.array(size_image))
    
    
len(image_array1)


# In[ ]:


data1=np.array(image_array1)
np.save("Cells1",data1)
Cells1=np.load("Cells1.npy")


# In[ ]:


a=model.predict(Cells1)
l=[]
a=list(a)
for i in a:
    l.append(np.argmax(i))


# In[ ]:


b=pd.DataFrame(a)
c=pd.DataFrame(l)
c=pd.concat([b,c],axis=1)


# In[ ]:


c.columns=[1,2,3,4,5,6]


# In[ ]:


c


# In[ ]:


def emo(l):
    if l==0:
        return 'Unknown'
    if l==1:
        return 'angry'
    if l==2:
        return 'happy'
    if l==3:
        return 'sad'
    if l==4:
        return 'surprised'
c[6]=c[6].apply(emo)


# In[ ]:


import numpy as np
import pandas as pd
labels=pd.read_csv("D:/data science/toon emotions detection/Dataset/Test.csv")
labels.head()


# In[ ]:


gen=c[6]
labels=pd.concat([labels,gen],axis=1)
labels


# In[ ]:


labels.columns=["Frame_ID","Emotion"]


# In[ ]:


labels


# In[ ]:


labels.to_csv('D:/data science/toon emotions detection/Dataset/submission1-.csv',columns=["Frame_ID","Emotion"],index=False)

