#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import os
get_ipython().system('pip install mtcnn')
from mtcnn import MTCNN
import cv2
import json

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


lr = 1e-4
bs = 32
epochs = 20


# In[ ]:


annotations_dir='../input/face-mask-detection-dataset/Medical mask/Medical mask/Medical Mask/annotations/'
images_dir='../input/face-mask-detection-dataset/Medical mask/Medical mask/Medical Mask/images/'


# In[ ]:




images=[]
labels=[]
for filename in os.listdir(images_dir):
    num = filename.split('.')[ 0 ]
    if int(num) > 1800:
        class_name = None
        anno = filename + ".json"
        with open(os.path.join(annotations_dir, anno)) as json_file:
            json_data = json.load(json_file)
            no_anno = json_data["NumOfAnno"]
            k = 0
            for i in range(0, no_anno):
                class_nam = json_data['Annotations'][i]['classname']
                if class_nam == 'face_with_mask':
                    class_name = 'face_with_mask'
                    k = i
                    break
                elif class_nam == 'face_no_mask':
                    class_name = 'face_no_mask'
                    k = i
                    break
                else:
                    if class_nam in ['hijab_niqab', 'face_other_covering', "face_with_mask_incorrect", "scarf_bandana", "balaclava_ski_mask", "other" ]:
                        class_name = 'face_no_mask'
                    elif class_nam in ["gas_mask", "face_shield", "mask_surgical", "mask_colorful"]:
                        class_name = 'face_with_mask'
            box = json_data[ 'Annotations' ][k][ 'BoundingBox' ]
            (x1, x2, y1, y2) = box
        if class_name is not None:
            image = cv2.imread(os.path.join(images_dir, filename))
            img = image[x2:y2, x1:y1]
            img = cv2.resize(img, (224, 224))
            img = img[...,::-1].astype(np.float32)
            img = preprocess_input(img)
            images.append(img)
            labels.append(class_name)  
   
images = np.array(images, dtype="float32")
labels = np.array(labels)
print(len(images))
print(len(labels))


# In[ ]:


labels.shape


# In[ ]:


lb = LabelEncoder()
labels = lb.fit_transform(labels)
print(labels[:10])
labels = to_categorical(labels)
print(labels[:10])


# In[ ]:


(trainX, testX, trainY, testY) = train_test_split(images, labels,
                                test_size=0.20, stratify=labels, random_state=42)
print(len(trainX))
print(len(trainY))
print(len(testX))
print(len(testY))


# In[ ]:


from tensorflow.keras.preprocessing.image import ImageDataGenerator

imageData = ImageDataGenerator(rotation_range=20,
                              zoom_range=0.15,
                              width_shift_range=0.2,
                              height_shift_range=0.2,
                              shear_range=0.15,
                              fill_mode='nearest')


# In[ ]:


Model1 = MobileNetV2(weights='imagenet',
                    include_top=False,
                    input_tensor=
                    Input(shape=(224,224,3)))
Model2 = Model1.output
Model2 = AveragePooling2D(pool_size=(7,7))(Model2)
Model2 = Flatten(name='flatten')(Model2)
Model2 = Dense(128, activation='relu')(Model2)
Model2 = Dropout(0.5)(Model2)
Model2 = Dense(2, activation='softmax')(Model2)
model = Model(inputs=Model1.input, outputs=Model2)
for layer in Model1.layers:
    layer.trainable = False
optimizer = Adam(lr=lr, decay=lr/epochs)
model.compile(loss='binary_crossentropy', 
              optimizer=optimizer,
             metrics=['accuracy'])


# In[ ]:


model.summary()


# In[ ]:


his = model.fit(imageData.flow(trainX, trainY, batch_size=bs),
               steps_per_epoch=len(trainX)//bs,
               validation_data=(testX, testY),
               validation_steps=len(testX)//bs,
               epochs=epochs)


# In[ ]:


plt.plot(his.history['accuracy'])
plt.plot(his.history['val_accuracy'])
plt.title('Model Accuracy')
plt.xlabel('Accuracy')
plt.ylabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.plot(his.history['loss'])
plt.plot(his.history['val_loss'])
plt.title('Model Loss')
plt.xlabel('Loss')
plt.ylabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()


# In[ ]:


print(model.predict(testX, batch_size=bs))


# In[ ]:


pred = model.predict(testX, batch_size=bs)
pred = np.argmax(pred, axis=1)
print(classification_report(testY.argmax(axis=1), pred, target_names=lb.classes_))


# In[ ]:


img = cv2.imread(os.path.join(images_dir, '1800.jpg'))
x = cv2.rectangle(img, (956,460),(246,326), (0,55,155), 10)


# In[ ]:


plt.imshow(x)


# In[ ]:


detector = MTCNN()
img = plt.imread(os.path.join(images_dir, '1795.jpg'))
face = detector.detect_faces(img)
for face in face:
    bounding_box = face['box']
    x=cv2.rectangle(img,
                   (bounding_box[0], bounding_box[1]),
                   (bounding_box[0]+bounding_box[2], 
                   bounding_box[1]+bounding_box[3]),
                   (0, 155, 255),
                   4)
    plt.imshow(x)
    


# In[ ]:


a = os.listdir(images_dir)
a.sort()
print((a))


# In[ ]:


test_images = a[:1698]


# In[ ]:


detector = MTCNN()
test_df = []
for image in test_images:
    img = plt.imread(os.path.join(images_dir, image))
    faces = detector.detect_faces(img)
    test = []
    for face in faces:
        bounding_box = face['box']
        test.append([image, bounding_box])
    test_df.append(test)


# In[ ]:


test = []
for i in test_df:
    if len(i)>0:
        if len(i)==1:
            test.append(i[0])
        else:
            for j in i:
                test.append(j)


# In[ ]:


sub=[]
rest_image=[]
for i in test:
    sub.append(i[0])
for image in test_images:
    if image not in sub:
        rest_image.append(image) 


# In[ ]:


detector=MTCNN()
test_df_=[]
for image in rest_image:
    img=cv2.imread(os.path.join(images_dir,image))
    faces=detector.detect_faces(img)
    test_=[]
    for face in faces:
        bounding_box=face['box']
        test_.append([image,bounding_box])
    test_df_.append(test_)


# In[ ]:


for i in test_df_:
    if len(i)>0:
        if len(i)==1:
            test.append(i[0])
        else:
            for j in i:
                test.append(j) 


# In[ ]:


negative = []
for i in test:
    for j in i[1]:
        if j<0:
            negative.append(i)


# In[ ]:


test_data = []
def create_test_data():
    for j in test:
        if j not in negative:
            img = cv2.imread(os.path.join(images_dir, j[0]))
            img = img[j[1][1]:j[1][1]+j[1][3],
                      j[1][0]:j[1][0]+j[1][2]]
            img = cv2.resize(img, (224, 224))
            img = img.reshape(-1,224,224,3)
            img = preprocess_input(img)
            predict = model.predict(img)
            test_data.append([j, predict])
    
create_test_data()


# In[ ]:


image = []
classname = []
for i,j in test_data:
    classname.append(np.argmax(j))
    image.append(i)
df = pd.DataFrame(columns=['image', 'classname'])
df['image']=image
df['classname']=classname
df['classname']= lb.inverse_transform(df['classname'])

image=[]
x1=[]
x2=[]
y1=[]
y2=[]
for i in df['image']:
    image.append(i[0])
    x1.append(i[1][0])
    x2.append(i[1][1])
    y1.append(i[1][2])
    y2.append(i[1][3])
df['name'] = image
df['x1'] = x1
df['x2'] = x2
df['y1'] = y1
df['y2'] = y2
df.drop(['image'], axis=1, inplace=True)
df.sort_values('name', axis=0, inplace=True, ascending=False)
cols = ['name', 'x1', 'x2', 'y1', 'y2', 'classname']
df = df[cols]
df.to_csv('submission.csv', index=False)


# In[ ]:




