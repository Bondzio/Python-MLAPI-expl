#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import datetime
from sklearn import datasets, metrics, neighbors
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns

df_placement = pd.read_csv('../input/factors-affecting-campus-placement/Placement_Data_Full_Class.csv') #Importamos el dataset
dataset = pd.DataFrame(df_placement)

dataset['gender'] = dataset['gender'].replace(["M"], 1) #Remplazamos los hombres por 1
dataset['gender'] = dataset['gender'].replace(["F"], 0) #Remplazamos las mujeres por 2
dataset['ssc_b'] = dataset['ssc_b'].replace(["Others"], 0) #Remplazamos others por 0
dataset['ssc_b'] = dataset['ssc_b'].replace(["Central"], 1) #Remplazamos central por 1
dataset['hsc_b'] = dataset['hsc_b'].replace(["Others"], 0) #Remplazamos others por 0
dataset['hsc_b'] = dataset['hsc_b'].replace(["Central"], 1) #Remplazamos central por 1
dataset['workex'] = dataset['workex'].replace(["Yes"], 1) #Remplazamos Yes por 1
dataset['workex'] = dataset['workex'].replace(["No"], 0) #Remplazamos central por 0
dataset['status'] = dataset['status'].replace(["Placed"], 1) #Remplazamos placed por 1
dataset['status'] = dataset['status'].replace(["Not Placed"], 0) #Remplazamos Not PLaced por 0
dataset['specialisation'] = dataset['specialisation'].replace(["Mkt&HR"], 1) #Remplazamos Mkt&HR por 1
dataset['specialisation'] = dataset['specialisation'].replace(["Mkt&Fin"], 0) #Remplazamos Mkt&Fin por 0
dataset['degree_t'] = dataset['degree_t'].replace(["Sci&Tech"], 1) #Remplazamos Sci&Tech por 1
dataset['degree_t'] = dataset['degree_t'].replace(["Comm&Mgmt"], 0) #Remplazamos Comm&Mgmt por 0
dataset['degree_t'] = dataset['degree_t'].replace(["Others"], 2) #Remplazamos Others por 2
dataset['hsc_s'] = dataset['hsc_s'].replace(["Commerce"], 0) #Remplazamos Commerce por 0
dataset['hsc_s'] = dataset['hsc_s'].replace(["Science"], 1) #Remplazamos Sciencie por 1
dataset['hsc_s'] = dataset['hsc_s'].replace(["Arts"], 2) #Remplazamos Arts por 2

#Definimos los features en X y el target en Y
X = np.array(dataset.drop(['sl_no','status','salary'], 1))
y = np.array(dataset['status'])

X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=80, test_size=0.3)

k_range = range(1, 20)
scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors = k)
    knn.fit(X_train, y_train)
    scores.append(knn.score(X_test, y_test))
plt.figure()
plt.xlabel('k')
plt.ylabel('accuracy')
plt.scatter(k_range, scores)
plt.xticks([0,5,10,15,20])

knn = KNeighborsClassifier(n_neighbors=2, metric='euclidean') 
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
print('Porcentaje de aciertos: {} %'.format((knn.score(X_test, y_test))*100))


# In[ ]:




