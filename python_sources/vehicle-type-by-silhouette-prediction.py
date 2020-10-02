#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


# Dataset Load
url = '../input/prediction-of-vehicle-type-by-silhouette/vehicle.csv'
data = pd.read_csv(url, header='infer')


# **Exploration**

# In[ ]:


data.shape


# In[ ]:


data.isna().sum()


# In[ ]:


#Dropping the records with null / missing values

data = data.dropna()


# In[ ]:


data.head()


# In[ ]:


data.groupby('class').size()


# **Modeling & Prediction**
# 
# Under modeling & prediction, I shall compare multiple Classifier Models from SKLEARN library and try to find the model with highest accuracy. The model that gives the higest accuracy will then be used for making predictions on unseen data

# In[ ]:


# --- Importing ML libraries ---
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder 

#Metrics Libraries
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

#ML Classifier Algorithm Libraries
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


# In[ ]:


data.columns


# In[ ]:


#Feature & Target Selection
features = ['compactness', 'circularity', 'distance_circularity', 'radius_ratio',
       'pr.axis_aspect_ratio', 'max.length_aspect_ratio', 'scatter_ratio',
       'elongatedness', 'pr.axis_rectangularity', 'max.length_rectangularity',
       'scaled_variance', 'scaled_variance.1', 'scaled_radius_of_gyration',
       'scaled_radius_of_gyration.1', 'skewness_about', 'skewness_about.1',
       'skewness_about.2', 'hollows_ratio']
target = ['class']

# Feature& Target  Dataset
X = data[features]
y = data[target]


# In[ ]:


#Dataset Split  [train = 90%, test = 10%]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0) 

#Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# **Model Creation & Evaluation**

# In[ ]:


# -- Building Model List --
models = []
models.append(('CART', DecisionTreeClassifier()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
models.append(('RFC', RandomForestClassifier()))


# In[ ]:


# -- Model Evaluation --
model_results = []
model_names = []

for name, model in models:
    kfold = KFold(n_splits=10, random_state=None, shuffle=False)
    cross_val_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
    model.verbose = False
    model_results.append(cross_val_results)
    model_names.append(name)
    print(name, ":--", "Mean Accuracy =", '{:.2%}'.format(cross_val_results.mean()), 
                       "Standard Deviation Accuracy =", '{:.2%}'.format(cross_val_results.std())
         )


# In[ ]:


# boxplot algorithm comparison
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(model_results)
ax.set_xticklabels(model_names)
plt.show()


# **As observed, SVM Model has provided the highest accuracy of 96.17% .**

# **Making Predictions - SVM Model**

# In[ ]:


#Instantiating Model
svm = SVC(kernel = 'linear', random_state=0)


# In[ ]:


#Training the Model
svm.fit(X_train, y_train)


# In[ ]:


#Making a prediction
y_pred = svm.predict(X_test)

# -- Calculating Metrics 
print("Trained Model Accuracy Score - SVM Model: ",'{:.2%}'.format(accuracy_score(y_test,y_pred)) )


# In[ ]:


#Converting the Test Sample to DataFrame
X_test_df = pd.DataFrame(list(X_test), columns=features)


# In[ ]:


#Appending the Prediction to the Test Sample

X_test_df['Predictions'] = y_pred


# In[ ]:


X_test_df.head()


# **Classification Report**

# In[ ]:


print(classification_report(y_test, y_pred))


# **Confusion Matrix**

# In[ ]:


conf_matrix = pd.DataFrame(confusion_matrix(y_test, y_pred), columns=['bus','car','van'], index= ['bus','car','van'])
conf_matrix.index.name = "Actual"
conf_matrix.columns.name = "Predicted"
plt.figure(figsize=(10,7))
sns.set(font_scale=1.4)
ax = sns.heatmap(conf_matrix, annot=True, cmap='Blues', annot_kws={"size":12}, cbar=False)

