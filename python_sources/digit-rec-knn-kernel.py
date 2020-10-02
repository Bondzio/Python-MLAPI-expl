#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Read data and use shape function to check if the data is complete.

# In[8]:


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')
train_set = train.values[:5000,1:]
train_label = train.values[:5000,0]
test_set = test.values
print(train.shape)
print(test.shape)
train.head()


# Check how does train set picture looks like.

# In[9]:


plt.imshow(train_set[10].reshape((28, 28)))
plt.show()


# In[10]:


classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
for y in range (9):
    index = np.nonzero([i == y for i in train_set])
    samples = np.random.choice(index[0], 4)
    
    for i, idx in enumerate(samples):
        plt_idx = i * len(classes) + y + 1
        plt.subplot(4, len(classes), plt_idx)
        plt.imshow(train_set[idx].reshape((28, 28)))
        plt.axis("off")
        if i == 0:
            plt.title(y)
plt.show()


# In[11]:


from sklearn.model_selection import train_test_split
train_train, train_vali, label_train, label_vali = train_test_split(train_set, train_label,test_size = 0.2, random_state = 14)
print(train_train.shape, train_vali.shape, label_train.shape, label_vali.shape)


# In[12]:


import time
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from sklearn.neighbors import KNeighborsClassifier

# cross validation to find the optimal k
scores = []
for k in range(1, 10):
    print("k = " + str(k))
    start = time.time()
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(train_train,label_train)
    y_pred = knn.predict(train_vali)
    accuracy = accuracy_score(label_vali,y_pred)
    scores.append(accuracy)
    end = time.time()
    print(classification_report(label_vali, y_pred))  
    print(confusion_matrix(label_vali, y_pred))  
    
    print("Complete time: " + str(end-start) + " Secs.")
print(scores)


# In[13]:


plt.plot([i+1 for i in np.arange(9)],scores)
plt.xlabel('Value of k')
plt.ylabel('Accuracy score')
plt.show()


# In[14]:


k = 5
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(train_set,train_label)
y_pred = knn.predict(test_set[:1000])


# In[15]:


print (y_pred[200])
plt.imshow(test_set[200].reshape((28, 28)))
plt.show()


# In[16]:


print(len(y_pred))
# save submission to csv
pd.DataFrame({"ImageId": list(range(1,len(y_pred)+1)),"Label": y_pred}).to_csv('Digit_Recogniser_Result.csv', index=False,header=True)


# In[ ]:




