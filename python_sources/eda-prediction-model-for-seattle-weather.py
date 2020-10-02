#!/usr/bin/env python
# coding: utf-8

# Motive behind this kernel is to analyse the variables with effective use of EDA and build a model to predict Seattle weather condition
#        ---
#   You will find different models built to predict <br>
#   1) Rain <br>
#   2) Max Temperature <br>
#   3) Min Temperature <br>
#   4) Precipitation in incches

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

import plotly.graph_objs as go
plt.style.use('bmh')
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
init_notebook_mode(connected=True)
from collections import Counter

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, learning_curve

sns.set(style='white', context='notebook', palette='deep')
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))
Weather =pd.read_csv("../input/seattleWeather_1948-2017.csv")

# Any results you write to the current directory are saved as output.


# Quick look at the Weather dataframe
#      ---

# In[ ]:


Weather.head()


# We have a task here to predict whether it will rain in Seattle . Lets check Column Rain . We have only two categories here.

# In[ ]:


Weather['RAIN'].value_counts()


# Lets express True and False in binary for building our model

# In[ ]:


Weather['RAIN'] = Weather["RAIN"].map(lambda i: 1 if i==True else 0)
Weather['RAIN'].value_counts()


# Lets take help of 3D plot to visualize the weather condition
#        ----

# In[ ]:


Weather_plot = Weather[['PRCP','TMAX','TMIN','RAIN']]
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(18, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('TMAX')
ax.set_ylabel('TMIN')
ax.set_zlabel('PRCP')
ax.scatter(Weather_plot[Weather_plot.RAIN == 0]['TMAX'],
           Weather_plot[Weather_plot.RAIN == 0]['TMIN'],
           Weather_plot[Weather_plot.RAIN == 0]['PRCP'],marker="o",color="Red")
ax.scatter(Weather_plot[Weather_plot.RAIN == 1]['TMAX'],
           Weather_plot[Weather_plot.RAIN == 1]['TMIN'],
           Weather_plot[Weather_plot.RAIN == 1]['PRCP'],marker="o",color="Blue");


# There is a clear sepration line in the plot which distinguish Rain condition in Seattle .
#        ----
#   **Blue dots = It rained when the amount precipitation in inches increased <br>
#    Red dots = It Didnt rain when the amount precipitation in inches is at lower level**

# Lets take help of Plotly to check the set of variables interactively 
#       ---

# In[ ]:


trace0 = go.Scatter3d(
    x=Weather_plot[Weather_plot.RAIN == 1]['TMAX'],
    y=Weather_plot[Weather_plot.RAIN == 1]['TMIN'],
    z=Weather_plot[Weather_plot.RAIN == 1]['PRCP'],
    mode='markers',
    name='Rain = Yes',
    marker=dict(
        size=2,
        line=dict(
            color='blue',
            width=0.5
        ),
        
    )
)
trace1 = go.Scatter3d(
    x=Weather_plot[Weather_plot.RAIN == 0]['TMAX'],
    y=Weather_plot[Weather_plot.RAIN == 0]['TMIN'],
    z=Weather_plot[Weather_plot.RAIN == 0]['PRCP'],
    mode='markers',
    name='Rain = No',
    marker=dict(
        size=2,
        line=dict(
            color='red',
            width=0.5
        ),
        
    )
)
data = [trace0, trace1]
layout = go.Layout(
      xaxis=dict(title='year'),
      yaxis=dict(title='Median listing PricePerSqft$$'),
      title=('Rain condition in Seattle, hover over the points'))
fig = go.Figure(data=data, layout=layout)
iplot(fig)


# Lets check the correlation between the variables. 
#       ---

# In[ ]:


g = sns.heatmap(Weather_plot[["PRCP","TMAX","TMIN","RAIN"]].corr(),annot=True, fmt = ".2f", cmap = "coolwarm")


# **Only PRCP(precipitation in inches) has a significative correlation with the Rain variable.**

# Feature Importance : To Predict Rain
#        ----

# In[ ]:


Weather = Weather.dropna()

rnd_clf = RandomForestClassifier(n_estimators = 100 , criterion = 'entropy',random_state = 0)
rnd_clf.fit(Weather.iloc[:,1:4],Weather.iloc[:,4])
for name, importance in zip(Weather.iloc[:,1:4].columns, rnd_clf.feature_importances_):
    print(name, "=", importance)

g = sns.barplot(y=Weather.iloc[:,1:4].columns,x = rnd_clf.feature_importances_, orient='h')


# Feature Importance : To Predict Max Temperature
#        ----

# In[ ]:


rnd_reg = RandomForestRegressor(n_estimators = 100 , random_state = 0)
rnd_reg.fit(Weather.iloc[:,[1,3,4]],Weather.iloc[:,2])
for name, importance in zip(Weather.iloc[:,[1,3,4]].columns, rnd_reg.feature_importances_):
    print(name, "=", importance)

g = sns.barplot(y=Weather.iloc[:,[1,3,4]].columns,x = rnd_reg.feature_importances_, orient='h')


# Feature Importance : To Predict Min Temperature
#        ----

# In[ ]:


rnd_reg = RandomForestRegressor(n_estimators = 100 ,random_state = 0)
rnd_reg.fit(Weather.iloc[:,[1,2,4]],Weather.iloc[:,3])
for name, importance in zip(Weather.iloc[:,[1,2,4]].columns, rnd_reg.feature_importances_):
    print(name, "=", importance)

g = sns.barplot(y=Weather.iloc[:,[1,2,4]].columns,x = rnd_reg.feature_importances_, orient='h')


# Feature Importance : To Predict Precipitation in inches
#        ----

# In[ ]:


rnd_reg = RandomForestRegressor(n_estimators = 100 ,random_state = 0)
rnd_reg.fit(Weather.iloc[:,[2,3,4]],Weather.iloc[:,1])
for name, importance in zip(Weather.iloc[:,[2,3,4]].columns, rnd_reg.feature_importances_):
    print(name, "=", importance)

g = sns.barplot(y=Weather.iloc[:,[2,3,4]].columns,x = rnd_reg.feature_importances_, orient='h')


# 1) Lets first Build model to predict Rain
#        ---
# We have enough evidence that Precipitation in inches is the most crucial variable in deciding the Rain condition in Seattle.
#         ---

# In[ ]:


X = Weather.iloc[:, [1, 2,3]].values
y = Weather.iloc[:, 4].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

classifier = RandomForestClassifier(n_estimators = 100 , criterion = 'entropy',random_state = 0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)
labels = [1, 0]
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(cm)
plt.title('Confusion matrix of the classifier')
fig.colorbar(cax)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()


# **Above model was able to predict Rain condition perfectly . In this case it is 100% accurate **
#       ----
# 

# 2) Model to predict Max Temperature
#        ---
# 

# In[ ]:


X = Weather.iloc[:, [1,3,4]]
y = Weather.iloc[:, 2]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

from sklearn.ensemble import RandomForestRegressor
RF_regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
RF_regressor.fit(X_train, y_train)
y_pred = RF_regressor.predict(X_test)

plt.scatter(X_test['TMIN'],y_test,color='red')
plt.scatter(X_test['TMIN'],RF_regressor.predict(X_test),color='blue')
plt.title('Random Forest regression Model built to predict Max Temperature')
plt.xlabel('Min Temperature')
plt.ylabel('Predicted Max Temperature blue');


# 3) Model to predict Min Temperature
#        ---
# 

# In[ ]:


X = Weather.iloc[:, [1,2,4]]
y = Weather.iloc[:, 3]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

from sklearn.ensemble import RandomForestRegressor
RF_regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
RF_regressor.fit(X_train, y_train)
y_pred = RF_regressor.predict(X_test)

plt.scatter(X_test['TMAX'],y_test,color='red')
plt.scatter(X_test['TMAX'],RF_regressor.predict(X_test),color='blue')
plt.title('Random Forest regression Model built to predict Min Temperature')
plt.xlabel('Max Temperature')
plt.ylabel('Predicted Min Temperature blue');


# 4) Model to predict Precipitation
#        ---
# 

# In[ ]:


X = Weather.iloc[:, [2,3,4]]
y = Weather.iloc[:,1]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

from sklearn.ensemble import RandomForestRegressor
RF_regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
RF_regressor.fit(X_train, y_train)
y_pred = RF_regressor.predict(X_test)

plt.scatter(X_test['TMAX'],y_test,color='red')
plt.scatter(X_test['TMAX'],RF_regressor.predict(X_test),color='blue')
plt.title('Random Forest regression Model built to predict Precipitation in inches')
plt.xlabel('Max Temperature')
plt.ylabel('Predicted Precipitation in inches in blue');


# In[ ]:


'''
from mpl_toolkits.basemap import Basemap
from matplotlib import animation, rc
from IPython.display import HTML

import warnings
warnings.filterwarnings('ignore')

import base64
from IPython.display import HTML, display
import warnings
warnings.filterwarnings('ignore')
from scipy.misc import imread
import codecs
'''


# In[ ]:


'''
import folium 
from folium import plugins
from folium.plugins import HeatMap

m = folium.Map(location=[47,-122],zoom_start=5)
folium.Marker((47,-122), popup='Seattle').add_to(m)
''';

