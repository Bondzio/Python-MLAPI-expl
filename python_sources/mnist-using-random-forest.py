#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


mnist_train_data= pd.read_csv('/kaggle/input/mnist-in-csv/mnist_train.csv')
mnist_train= mnist_train_data.drop("label", axis=1)
mnist_label= mnist_train_data["label"].copy()

mnist_test_data= pd.read_csv('/kaggle/input/mnist-in-csv/mnist_test.csv')
mnist_test= mnist_test_data.drop("label", axis=1)
mnist_test_label= mnist_test_data["label"].copy()


# In[ ]:


X_train, y_train = mnist_train.values, mnist_label.values
X_test, y_test = mnist_test.values, mnist_test_label

X_train.shape, y_train.shape, X_test.shape, y_test.shape


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as plt

some_digit = X_train[40000]
some_digit_image= some_digit.reshape(28,28)

plt.imshow(some_digit_image, cmap= matplotlib.cm.binary, interpolation= "nearest")
plt.axis("off")
plt.show()

print("actual output: " + str(y_train[40000]))


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
forest_clf= RandomForestClassifier(random_state= 42)
forest_clf.fit(X_train, y_train)


# In[ ]:


forest_clf.predict([some_digit])


# In[ ]:


forest_clf.predict_proba([some_digit])


# In[ ]:


from sklearn.model_selection import cross_val_score, cross_val_predict
cross_val_score(forest_clf, X_train, y_train, cv=3, scoring='accuracy')


# In[ ]:


y_train_pred= cross_val_predict(forest_clf,X_train, y_train, cv=3)
from sklearn.metrics import confusion_matrix as cm
cm(y_train, y_train_pred)


# In[ ]:


y_predictions= forest_clf.predict(X_test)


# In[ ]:


from sklearn.metrics import accuracy_score, precision_score, recall_score


# In[ ]:


precision_score(y_test, y_predictions, average= None)


# In[ ]:


recall_score(y_test, y_predictions, average= None)


# In[ ]:


accuracy_score(y_test, y_predictions)


# In[ ]:


Final_predictions= pd.DataFrame(y_predictions, columns=['Predicted Digit'])
Final_predictions= Final_predictions.to_csv(header= 'Predicted Digit', index= False)


# In[ ]:


from joblib import dump
dump(forest_clf, "Random Forest model trained")
dump(Final_predictions, 'Final_predictions.csv')

