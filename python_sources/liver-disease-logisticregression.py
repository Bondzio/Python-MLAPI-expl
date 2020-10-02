#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[ ]:


data = pd.read_csv("../input/indian-liver-patient-records/indian_liver_patient.csv")


# ### Data analysis ###

# In[ ]:


data.isnull().sum()


# In[ ]:


data = data.dropna()
data.isnull().any()


# In[ ]:


fig, ax = plt.subplots(figsize=(7,7))
sns.heatmap(abs(data.corr()), annot=True, square=True, cbar=False, ax=ax, linewidths=0.25);


# In[ ]:


data = data.drop(columns= ['Direct_Bilirubin', 'Alamine_Aminotransferase', 'Total_Protiens'])


# As we can see there are correlation: 'Total_Bilirubin'-'Direct_Bilirubin', 'Alamine_Aminotransferase'-'Aspartate_Aminotransferase', 'Total_Protiens'-'Albumin'.
# I drop from data: 'Direct_Bilirubin', 'Alamine_Aminotransferase', 'Total_Protiens'.
# 
# And data look like:
# 
# Categorical:
# - Gender
# 
# Continuous data:
# - Age
# - Total_Bilirubin
# - Alkaline_Phosphotase
# - Aspartate_Aminotransferase
# - Albumin
# - Albumin_and_Globulin_Ratio

# In[ ]:


data['Dataset'] = data['Dataset'].replace(1,0)
data['Dataset'] = data['Dataset'].replace(2,1)


# In[ ]:


print('How many people to have disease:', '\n', data.groupby('Gender')[['Dataset']].sum(), '\n')
print('How many people participated in the research:', '\n', data.groupby('Gender')[['Dataset']].count())


# In[ ]:


print('Percentage of people with the disease depending on gender:')
data.groupby('Gender')[['Dataset']].sum()/ data.groupby('Gender')[['Dataset']].count()


# Women have a higher percentage of the disease.

# In[ ]:


age=pd.cut(data['Age'], [0,18,91])
print('Distribution of the disease by gender and age')
data.pivot_table('Dataset', ['Gender', age])


# Among men with the disease at risk young people under 18 years of age.

# ### Train model ###

# In[ ]:


from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve


# In[ ]:


X = data[['Age', 'Gender', 'Total_Bilirubin','Alkaline_Phosphotase','Aspartate_Aminotransferase','Albumin','Albumin_and_Globulin_Ratio']]
y = pd.Series(data['Dataset'])


# In[ ]:


from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
X['Gender'] = labelencoder.fit_transform(X['Gender'])


# We need that column 'Gender' should be type of numbers. For it we to use LabelEncoder

# In[ ]:


x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(x_train)
X_test = scaler.transform(x_test)


# In[ ]:


model = LogisticRegression()
model.fit(X_train, y_train);


# Because it is a Logistic Regression, we as researchers can choose a threshold by which we can adjust the result of model predictions.
# Look at results of predictions with different threshold:

# In[ ]:


acc = np.array([])
for i in range(0, 100, 10):
    y_pred_new_threshold = (model.predict_proba(X_test)[:, 1]>= i/100).astype(int)
    newscore = accuracy_score(y_test, y_pred_new_threshold)
    acc = np.append(acc, [y_pred_new_threshold])
acc = acc.astype(int)
acc = acc.reshape(10,-1)


# In[ ]:


i=0
for l in acc:
    print('***', i, '***')
    matrix = confusion_matrix(y_test, l)
    print('\n', matrix.T, '\n')
    print('accuracy_score= ', accuracy_score(y_test, l), '\n')
    i+=1


# I would prefer that threshold = 0.3
# With this value, most people with the disease and no disease will be determined correctly. And *** accuracy score = 67% ***

# In[ ]:


labels = (model.predict_proba(X_test)[:, 1]>=0.3).astype(int)
accuracy_score(y_test, labels)


# In[ ]:


matrix = confusion_matrix(y_test, labels)
sns.heatmap(matrix.T, square=True, annot=True, fmt='d', cbar=False)
plt.xlabel('true label')
plt.ylabel('predicted label');


# In[ ]:


logit_roc_auc = roc_auc_score(y_test, labels)
fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()


# Area under Roc curve = 0.68
# More people with desease will be predict right.
