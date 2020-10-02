# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.

from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

cwd = os.getcwd()

data_train = pd.read_csv("../input/train.csv")
data_test = pd.read_csv("../input/test.csv")

data_train.info()
data_test.info()

data_train.head()
data_test.head()


# Analyse des prix des maisons


# On analyse le fichier train, qui contient toutes les informations relatives aux maisons.


# Pour avoir une vision globale, on utilise la fonction describe :

data_train.describe()

# On peut observer notamment que la moyenne du prix des maisons est de $180921, avec un �cart type de $79442. Cela signigie qu'il y a une grande disparit� des prix.

# Recherchons maintenant la corr�lation entre le prix et les autres �l�ments du data frame.

tabcorr = data_train.corr()
correlation_prix = tabcorr.SalePrice
print(correlation_prix)

# Remarque : on peut suprrimer la ligne SalePrice puisqu'elle n'est pas pertinente. Une valeur est toujours corr�l�e � elle-m�me.

correlation_prix = correlation_prix.drop(['SalePrice'], axis=0)
print(correlation_prix)

# On peut aussi la trier par ordre d�croissant.

correlation_prix = correlation_prix.sort_values(ascending=False)    
print(correlation_prix)

# Ainsi, on observe que le prix d�pend principalement des facteurs suivants : "OverallQual" (qualit� des mat�riaux et finitions de la maison), et du GrLivArea (surface habitable de la maison).
# De plus, la corr�lation est positive, donc plus ces valeurs augmentent, et plus le prix de la maison augemente (cela aurait eu un effet contraire si le signe �tait n�gatif).

# Pour avoir une id�e plus g�n�rale, et mieux visualiser les donn�es, on trace ces deux valeurs en fonction du prix des maisons.

plt.figure(figsize=(8,8))
plt.scatter(data_train.OverallQual, data_train.SalePrice)
plt.xlabel('Qualit� de la maison')                  
plt.ylabel('Valeur')                        
plt.title('Valeur par la qualit� de la maison')        
plt.show

# On a bien un r�sultat logique : plus la qualit� de la maison augmente, plus la maison est ch�re. 

plt.figure(figsize=(8,8))
plt.scatter(data_train.GrLivArea, data_train.SalePrice)
plt.xlabel('Surface habitable hors sol')                  
plt.ylabel('Valeur')                        
plt.title('Valeur en fonction de la surface habitable hors sol')        
plt.show

# De m�me, on a un r�sultat globalement logique : plus cette surface augmente, et plus le prix de la maison en question augmente.
# De plus, on observe deux valeurs aberrantes que l'on supprime pour avoir un mod�le pertinent.

max(data_train.GrLivArea)
data_train = data_train[data_train.GrLivArea != 5642]
max(data_train.GrLivArea)
data_train = data_train[data_train.GrLivArea != 4676]


# Pr�diction du prix


# Comme les corr�lations ne sont pertinentes que pour les colonnes suivantes : OverallQual et GrLivArea. On pr�dira donc le prix de la maison � partir de ces valeurs. De plus, ce ne sont que des valeurs num�riques, ce qui simplifie grandement la pr�diction.

Y_train = data_train['SalePrice']
X_train = data_train[['OverallQual','GrLivArea']] 
X_test = data_test[['OverallQual','GrLivArea']] 

X_train.head()

# On v�rifie si les dataframes ont des valeurs NaN.

X_train.isnull().values.any()
X_test.isnull().values.any()

#Ce n'est pas le cas, on peut donc �tablir une pr�diction.


# Pr�diction par r�gression lin�aire :

lm = LinearRegression()
lm.fit(X_train, Y_train)            
Y_pred = lm.predict(X_test)


# Pr�diction par for�ts al�atoires :

from sklearn import ensemble
rf = ensemble.RandomForestRegressor()
rf.fit(X_train, Y_train)
Y_rf = rf.predict(X_test)


# Pour comparer les mod�les utilis�es, on les v�rifie en les appliquant sur des donn�es que l'on connait en "cachant" les prix.
# Ainsi, on utilise le dataframe Train.csv. On le s�pare en deux : un train et un test.

data_train_train = data_train.sample(frac=0.8)          
data_train_test = data_train.drop(data_train_train.index)

Y2_train = data_train_train['SalePrice']
X2_train = data_train_train[['OverallQual','GrLivArea']]
Y2_test = data_train_test['SalePrice']
X2_test = data_train_test[['OverallQual','GrLivArea']]


# On teste le mod�le de la r�gression lin�raire.

lm.fit(X2_train, Y2_train)            
Y2_pred = lm.predict(X2_test)         

plt.scatter(Y2_test, Y2_pred)
plt.plot([Y2_test.min(),Y2_test.max()],[Y2_test.min(),Y2_test.max()], color='red', linewidth=3)
plt.xlabel("Prix")
plt.ylabel("Prediction de prix")
plt.title("Prix reels vs predictions")

# On peut visualiser l'erreur : 

plt.plot(Y2_test-Y2_pred)

# Calculons la avec l'erreur sur les moindres carr�s.

from sklearn import metrics
print(metrics.mean_squared_error(Y2_test, Y2_pred))

# Faisons de m�me avec la m�thode des for�ts al�atoires.

rf.fit(X2_train, Y2_train)
Y2_rf = rf.predict(X2_test)

plt.scatter(Y2_test, Y2_rf)
plt.plot([Y2_test.min(),Y2_test.max()],[Y2_test.min(),Y2_test.max()], color='red', linewidth=3)
plt.xlabel("Prix")
plt.ylabel("Prediction de prix")
plt.title("Prix reels vs predictions")

# On observe que ce mod�le est plus pr�cis. V�rifions le en calculant l'erreur.

plt.plot(Y2_test-Y2_rf)
print(metrics.mean_squared_error(Y2_test, Y2_rf))

# On observe bien que la m�thode des for�ts al�atoires est plus pr�cise que la m�thode de la r�gression lin�aire.