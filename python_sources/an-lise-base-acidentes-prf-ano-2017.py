#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[ ]:


df_acidentes = pd.read_csv('../input/datatran2017.csv', parse_dates=['data_inversa'])


# In[ ]:


df_acidentes.shape


# In[ ]:


df_acidentes.head


# In[ ]:


df_acidentes.info()


# In[ ]:


df_acidentes.nunique()


# In[ ]:


del_columns = [
 'data_inversa',
 'id',
 'latitude',
 'longitude',
 'ignorados',
 'veiculos',
 'km',
 'municipio',
 'horario']


# In[ ]:


for col in del_columns:
    del df_acidentes[col]


# In[ ]:


df_acidentes.nunique()


# In[ ]:


list(df_acidentes.columns)


# In[ ]:


dummies_columns = [
 'dia_semana',
 'uf',
 'br',
 'causa_acidente',
 'tipo_acidente',
 'classificacao_acidente',
 'fase_dia',
 'sentido_via',
 'condicao_metereologica',
 'tipo_pista',
 'tracado_via',
 'uso_solo']


# In[ ]:


for col in dummies_columns:
    df_acidentes = pd.concat([df_acidentes, pd.get_dummies(df_acidentes[col], prefix=col).iloc[:,:-1]], axis=1)
    del df_acidentes[col]


# In[ ]:


df_acidentes.shape


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


train, valid = train_test_split(df_acidentes, random_state=42)


# In[ ]:


print(train.shape,valid.shape)


# In[ ]:


from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR


# In[ ]:


models = {'RandomForest': RandomForestRegressor(random_state=42), 
          'ExtraTrees': ExtraTreesRegressor(random_state=42), 
          'GBM': GradientBoostingRegressor(random_state=42), 
          'DecisionTree' : DecisionTreeRegressor(random_state=42),
          'AdaBoost': AdaBoostRegressor(random_state=42), 
          'KNN 1': KNeighborsRegressor(n_neighbors=1), 
          'KNN 3': KNeighborsRegressor(n_neighbors=3), 
          'KNN 11':  KNeighborsRegressor(n_neighbors=11), 
          'SVR': SVR(), 
          'Linear Regression': LinearRegression()}


# In[ ]:


models = {'RandomForest': RandomForestRegressor(random_state=42)}


# In[ ]:


removed_cols = ['pessoas',
 'mortos',
 'feridos_leves',
 'feridos_graves',
 'feridos',
 'ilesos']


# In[ ]:


feats = [c for c in df_acidentes.columns if c not in removed_cols]


# In[ ]:


from sklearn.metrics import mean_squared_error


# In[ ]:


def run_model(model, train, valid, feats, y_name):
    model.fit(train[feats], train[y_name])
    preds = model.predict(valid[feats])
    return mean_squared_error(valid['mortos'], preds)**(1/2)


# In[ ]:


import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[ ]:


scores = []
for name, model in models.items():
    score = run_model(model, train, valid, feats, 'mortos')
    scores.append(score)
    print(name+':', score)


# In[ ]:


pd.Series(scores, index=models.keys()).sort_values(ascending=False).plot.barh()


# In[ ]:


scores.pop()


# In[ ]:


index = list(models.keys())


# In[ ]:


index.pop()


# In[ ]:


index


# In[ ]:


pd.Series(scores, index=index).sort_values(ascending=False).plot.barh()

