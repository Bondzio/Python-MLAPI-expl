#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#importing necessary modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, roc_curve, auc


# In[ ]:


#importing data
data = pd.read_csv("../input/creditcard.csv")
data.head()


# In[ ]:


#checking Unbalanced Data
count_classes = pd.value_counts(data['Class'])
count_classes_log = np.log10(count_classes)
count_classes.plot(kind = "bar")
plt.xlabel("Class")
plt.ylabel("Frequency")
plt.show()


#  **This Shows Imabalanced Classes. As you can see Class 1 i.e frauds is almost 0. To get a better view of this we will take a look at Log of values**

# In[ ]:


# Log graph
count_classes_log.plot(kind = 'bar')
plt.xlabel("Class")
plt.ylabel("log_Frequency")
plt.show()


# **This gives us a better view of how imbalanced classes are.**

# **As we can see values in various columns are not scaled and using such unscaled values can cause our classifiers to give inaccurate results.**

# In[ ]:


#Scaling data
data['normAmount'] = StandardScaler().fit_transform(data['Amount'].values.reshape(-1, 1))
data =  data.drop(["Time", "Amount"], axis = 1)
data.head()


# In[ ]:


#Splitting into Feature and label data
x = data.drop(["Class"], axis = 1)
y = data["Class"]


# In[ ]:


#performing SMOTE to solve Unbalanced Classes
smote = SMOTE(random_state= 42)
x_new, y_new = smote.fit_sample(x, y)
print(len(y_new[y_new == 1]))


# In[ ]:


#splitting into train-test data
x_train, x_test, y_train, y_test = train_test_split(x_new, y_new, random_state = 42, test_size = 0.2 )


# In[ ]:


#fitting RandomForestClassifier Model
rf =  RandomForestClassifier()
rf.fit(x_train, y_train)


# In[ ]:


#Predicting labels
y_pred = rf.predict(x_test)


# In[ ]:


#measuring Accuracy Score
accuracy_score(y_test, y_pred)


# In[ ]:


#Measuring Roc_Auc score
roc_auc_score(y_test, y_pred)


# In[ ]:


#Preparing ROC curve
false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
roc_auc = auc(false_positive_rate, true_positive_rate)


# In[ ]:


#Plotting ROC Curve
plt.title('ROC CURVE')
plt.plot(false_positive_rate, true_positive_rate, 'b',
label='AUC = %0.2f'% roc_auc)
plt.legend(loc='lower right')
plt.plot([0,1],[0,1],'r--')
plt.xlim([-0.1,1.2])
plt.ylim([-0.1,1.2])
plt.ylabel('True_Positive_Rate')
plt.xlabel('False_Positive_Rate')
plt.show()


# In[ ]:




