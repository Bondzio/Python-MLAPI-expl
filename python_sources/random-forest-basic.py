#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from sklearn.datasets import load_digits
digits = load_digits()


# In[ ]:


dir(digits)


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# In[ ]:


plt.gray()
for i in range(4):
    plt.matshow(digits.images[i])  
    '''Display an array as a matrix in a new figure window.The origin is set at the upper left hand corner and rows (first dimension of the array) are displayed horizontally.The aspect ratio of the figure window is that of the array, unless this would make an excessively short or narrow figure.'''


# In[ ]:


df = pd.DataFrame(digits.data)
df.head()


# In[ ]:


df['target'] = digits.target


# In[ ]:


df[0:12]


# In[ ]:


'''Train and the model and prediction'''


# In[ ]:


X = df.drop('target',axis='columns')
y = df.target


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=20)
model.fit(X_train, y_train)


# In[ ]:


model.score(X_test, y_test)


# In[ ]:


y_predicted = model.predict(X_test)


# In[ ]:


'''Confusion Matrix'''


# In[ ]:


from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_predicted)
cm


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sn
plt.figure(figsize=(10,7))
sn.heatmap(cm, annot=True)
plt.xlabel('Predicted')
plt.ylabel('Truth')


# In[ ]:




