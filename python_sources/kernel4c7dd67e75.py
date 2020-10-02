#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
data = pd.read_csv("../input/musk-dataset/musk_csv.csv")
data.head()


# In[ ]:


data.describe()


# In[ ]:


data.isnull().sum()


# In[ ]:


releation = data.corr().abs()


# In[ ]:


releation


# we can use PCA also for reducing the features which are less  relevant

# In[ ]:


corr_matrix = data.corr().abs()

# upper triangle of correlation matrix
upper_traingle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

# Find index of feature columns with correlation greater than 0.93
drop = [column for column in upper_traingle.columns if any(upper_traingle[column] > 0.92)]


# In[ ]:


df = data.drop(columns = drop)
df.shape


# In[ ]:


def normlize(data):
    for col in data.columns[3:127]:
        data[col] = (data[col]/max(data[col]))
    return data

df_norm = normlize(df)
df_norm.head()


# In[ ]:


datax = df_norm[df_norm.columns[3:127]].to_numpy()
datay = df_norm[df_norm.columns[-1]].to_numpy()
print(datax.shape,datay.shape)


# In[ ]:


from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(datax,datay,test_size = 0.20)


# In[ ]:


print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)


# since data has more features we use cnn to capture the most property of the data
# for balance of data to cnn we have use 114 to 19 by 6

# In[ ]:


x_train = np.reshape(X_train,(X_train.shape[0],19,6,1)).astype('float32')
x_test= np.reshape(X_test,(X_test.shape[0],19,6,1)).astype('float32')


# In[ ]:


print(x_train.shape,x_test.shape)


# In[ ]:


import keras
y_train = keras.utils.to_categorical(y_train,num_classes = 2)
y_test = keras.utils.to_categorical(y_test,num_classes = 2)
print(y_train.shape,y_test.shape)


# In[ ]:


y_train[5000:5005]


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten,Conv2D, MaxPooling2D


# In[ ]:


model=Sequential()
model.add(Conv2D(64,kernel_size=(2,2),activation='relu',input_shape=(19,6,1)))
model.add(Conv2D(64,(2,2),activation='relu'))
model.add(Conv2D(64,(2,2),activation='relu'))
model.add(Conv2D(32,(2,2),activation='relu'))

model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Dropout(0.20))
model.add(Flatten())
model.add(Dense(128,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2,activation='sigmoid'))


# In[ ]:


model.compile(loss='binary_crossentropy',optimizer = 'adam',metrics=['accuracy'])
model.summary()


# In[ ]:


history = model.fit(x_train,y_train,batch_size=128,epochs=20,validation_data=(x_test,y_test))


# In[ ]:


score=model.evaluate(x_test,y_test,verbose=0)
print(score)


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'])
plt.savefig('accuracy.png',dpi = 100)
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'])
plt.savefig('loss.png',dpi = 100)
plt.show()


# In[ ]:


from sklearn.metrics import f1_score, precision_score, recall_score


# In[ ]:


model.predict(x_train[0].reshape(1,19,6,1))
# model is telling 99.9999% musk and 0.0001% is nonMusk


# In[ ]:


x_test.shape


# In[ ]:


yp = model.predict(x_test)
yp.shape


# In[ ]:


def preprocess(m):
    a = np.zeros((1320))
    for i in range(1320):
        if m[i][0]>m[i][1]:
            a[i] = 1
        else:
            a[i] = 0
    return a
y_predict = preprocess(yp)


# In[ ]:


y_test


# In[ ]:


# our y_test is in 2d shape
test = preprocess(y_test)
print(test.shape,y_predict.shape)


# In[ ]:


print("f1_score:",f1_score(test,y_predict))
print("recall:",recall_score(test,y_predict))

print("Validation Loss:",score[0])
print("Validation Accuracy:",score[1])


# In[ ]:


from keras.utils import plot_model
plot_model(model, to_file='model.png')


# In[ ]:




