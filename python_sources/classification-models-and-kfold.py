#!/usr/bin/env python
# coding: utf-8

# **This notebook covers:**
# * Visualization of Dataset
# * Impute Null Values
# * Check Coorelation
# * Scale Data
# * All Classification Models
# * KFold
# * Evaluate Models

# In[ ]:


import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore") 

get_ipython().run_line_magic('matplotlib', 'inline')


# # 1.1 Import Dataset

# In[ ]:


# Read Dataset
data = pd.read_csv('../input/pima-indians-diabetes-database/diabetes.csv')
data.sample(n = 10, random_state = 0)


# # ** 1.2 Summary of Dataset**

# In[ ]:


data.info(verbose = True)


# # **1.3 Evalute Dataset by Descriptive Statistics**

# In[ ]:


data.describe().transpose()


# # **1.4 Pairwise Relationships in the Dataset**

# In[ ]:


import seaborn as sns
sns.pairplot(data, hue = 'Outcome', diag_kind='kde')
plt.show()


# **Columns Glucose, BloodPressure, SkinThickness, Insulin, BMI have invalid zero. Create a deep copy of dataset so that changes doesn't affect our original dataset
# **

# In[ ]:


data_copy = data.copy(deep = True)
data_copy.loc[:, ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']] = data_copy.loc[:, ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']].replace(0, np.NaN)


# # **1.5 Visualizaion of Null Values**

# In[ ]:


data_copy.isnull().sum()
import missingno as msno
msno.matrix(data_copy, figsize = (20, 10), labels = True, color = (0.502, 0.0, 0.0)) 
plt.show()


# # **1.6 Boxplot**

# In[ ]:


import plotly.graph_objects as go
column_names = data_copy.columns
no_of_boxes = len(column_names)
colors = [ 'hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, no_of_boxes)]

fig = go.Figure(data = [go.Box(y = data_copy.loc[:, column_names[i]], marker_color = colors[i], name = column_names[i], boxmean = True, showlegend = True) for i in range(no_of_boxes)])

fig.update_layout(
    xaxis=dict(showgrid = True, zeroline = True, showticklabels = True),
    yaxis=dict(zeroline = True, gridcolor = 'white'),
    paper_bgcolor = 'rgb(233,233,233)',
    plot_bgcolor = 'rgb(233,233,233)')

fig.show()


# # **1.7 Replace Null Values**

# In[ ]:


from sklearn.impute import SimpleImputer
imputer_mean = SimpleImputer(missing_values = np.NaN, strategy = 'mean')
imputer_median = SimpleImputer(missing_values = np.NaN, strategy = 'median')

glucose_fit = imputer_mean.fit(data_copy[['Glucose']])
data_copy[['Glucose']] = glucose_fit.transform(data_copy[['Glucose']])

bp_fit = imputer_median.fit(data_copy[['BloodPressure']])
data_copy[['BloodPressure']] = bp_fit.transform(data_copy[['BloodPressure']])

bp_fit = imputer_median.fit(data_copy[['SkinThickness']])
data_copy[['SkinThickness']] = bp_fit.transform(data_copy[['SkinThickness']])

bp_fit = imputer_median.fit(data_copy[['Insulin']])
data_copy[['Insulin']] = bp_fit.transform(data_copy[['Insulin']])

bp_fit = imputer_median.fit(data_copy[['BMI']])
data_copy[['BMI']] = bp_fit.transform(data_copy[['BMI']])


# # **1.8 Coorelation of Clean Dataset**

# In[ ]:


plt.figure(figsize = (14, 10))
sns.heatmap(data_copy.corr(), annot = True, cmap = 'Blues', linecolor = 'tab:cyan', linewidths = 2)
plt.title("Clean dataset")
plt.show()


# # **1.9 Scale Dataset**

# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
data_scaled = pd.DataFrame(scaler.fit_transform(data_copy.drop(labels = ['Outcome'], axis = 1)), columns = column_names[:-1])
data_scaled.sample(n = 10)


# # **1.10 Target Class Ratio**

# In[ ]:


count_0 = data_copy[data_copy[['Outcome']] == 0]['Outcome']
count_1 = data_copy[data_copy[['Outcome']] == 1]['Outcome']

trace1 = go.Histogram(x = count_0, name = 'Non-Diabetic')
trace2 = go.Histogram(x = count_1, name = 'Diabetic')

plot_data = [trace1, trace2]
layout = go.Layout(title = "Total Outcomes", xaxis = dict(title = "Outcome"),yaxis = dict(title = "Count") ) 

fig = go.Figure(data = plot_data, layout = layout)
fig.show()


# # **2.1 Split Dataset**

# In[ ]:


from sklearn.model_selection import train_test_split
x = data_scaled
y = data[['Outcome']]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, stratify = data[['Outcome']])
x_train.shape, x_test.shape, y_train.shape, y_test.shape


# **Function to store every model's metrics**

# In[ ]:


from sklearn import metrics
from sklearn.model_selection import cross_val_score
accuracy = []
precision = []
recall = []
f1_score = []
def calculate_metrics(y_test, y_pred):
    acc = metrics.accuracy_score(y_true = y_test, y_pred = y_pred)
    pre = metrics.precision_score(y_true = y_test, y_pred = y_pred)
    rec = metrics.recall_score(y_true = y_test, y_pred = y_pred)
    f1 = metrics.f1_score(y_true = y_test, y_pred = y_pred)
    accuracy.append(acc)
    precision.append(pre)
    recall.append(rec)
    f1_score.append(f1)

    
kfold_min = []
kfold_mean = []
kfold_max = []
def calculate_kfold(estimator):
    accuracies = cross_val_score(estimator, x, y, cv = 10)
    kfold_min.append(accuracies.min())
    kfold_mean.append(accuracies.mean())
    kfold_max.append(accuracies.max())


# # **2.2 Logistic Regression**

# In[ ]:


from sklearn.linear_model import LogisticRegression
logisticRegression = LogisticRegression()
logisticRegression.fit(x_train, y_train)
logisticRegression_prediction = logisticRegression.predict(x_test)
calculate_metrics(y_test, logisticRegression_prediction)
calculate_kfold(logisticRegression)


# # **2.3 Decision Tree**

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
decisionTree = DecisionTreeClassifier(criterion = 'entropy')
decisionTree.fit(x_train, y_train)
decisionTree_prediction = decisionTree.predict(x_test)
calculate_metrics(y_test, decisionTree_prediction)
calculate_kfold(decisionTree)


# # **2.4 Random Forest**

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
randomForest = RandomForestClassifier(n_estimators = 1000)
randomForest.fit(x_train, y_train)
randomForest_prediction = randomForest.predict(x_test)
calculate_metrics(y_test, randomForest_prediction)
calculate_kfold(randomForest)


# # **2.5 Linear Support Vector Classifier**

# In[ ]:


from sklearn.svm import LinearSVC
linearSVC = LinearSVC()
linearSVC.fit(x_train, y_train)
linearSVC_prediction = linearSVC.predict(x_test)
calculate_metrics(y_test, linearSVC_prediction)
calculate_kfold(linearSVC)


# # **2.6 XGB Classifier**

# In[ ]:


from xgboost import XGBClassifier
xgbClassifier = XGBClassifier()
xgbClassifier.fit(x_train, y_train)
xgbClassifier_prediction = xgbClassifier.predict(x_test)
calculate_metrics(y_test, xgbClassifier_prediction)
calculate_kfold(xgbClassifier)


# # **2.7 KNeighbors**

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
knnClassifier = KNeighborsClassifier()
knnClassifier.fit(x_train, y_train)
knnClassifier_prediction = knnClassifier.predict(x_test)
calculate_metrics(y_test, knnClassifier_prediction)
calculate_kfold(knnClassifier)


# # **2.8 Bernoulli Naive Bayes**

# In[ ]:


from sklearn.naive_bayes import BernoulliNB
bernoulliNB = BernoulliNB(binarize = True)
bernoulliNB.fit(x_train, y_train)
bernoulliNB_prediction = bernoulliNB.predict(x_test)
calculate_metrics(y_test, bernoulliNB_prediction)
calculate_kfold(bernoulliNB)


# # **3.0 Combine All Metrics**

# In[ ]:


column = pd.MultiIndex.from_arrays([['First Train', 'First Train', 'First Train', 'First Train', 'KFold', 'KFold', 'KFold'], ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'Min', 'Mean', 'Max']])

results = pd.DataFrame(data = [accuracy, precision , recall, f1_score, kfold_min, kfold_mean, kfold_max], columns = column, index = ['Logistic Regression', 'Decision Tree', 'Random Forest', 'Linear SVC', 'XGBoost', 'K Neighbors', 'Bernoulli NB'])
results


# # Please give your suggestions in the comment box.
# # If you found it useful, UPVOTE.
