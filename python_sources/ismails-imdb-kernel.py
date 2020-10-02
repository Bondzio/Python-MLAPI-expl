#!/usr/bin/env python
# coding: utf-8

# In[118]:


import pandas as pd
import sklearn as sk
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab


# In[119]:


#hapim datasetin (fajlli .csv) dhe e ruajme ne variablen data
data = open("C:\\Users\\Albina\\Desktop\\Semestri 6\\G�rmimi i t� dh�nave\\Projekti\\Projekti\\IMDB-Movie-Data.csv")


# In[120]:


#me ane te librarise pandas e lexojme fajllin .csv dhe e ruajme ne variablen traindata
traindata = pd.read_csv(data)


# In[73]:


traindata


# In[74]:


#shohim sa rreshta dhe atribute ka dataseti
traindata.shape


# In[75]:


traindata.head()


# In[76]:


traindata.head(10)


# In[77]:


traindata.tail()


# In[78]:


traindata.tail(10)


# In[79]:


traindata.describe(include = "all")


# In[80]:


traindata.describe()


# In[81]:


traindata.dtypes


# In[82]:


# Nderlidhjet mes kolonave
traindata.corr()


# In[121]:


traindata = traindata.rename(columns = {'Revenue (Millions)':'Revenue_Millions'})


# In[122]:


traindata = traindata.rename(columns = {'Runtime (Minutes)':'Runtime_Minutes'})


# In[85]:


traindata['Genre'].value_counts()


# In[86]:


zhanret_ndara = 'Action','Adventure','Animation','Biography','Comedy','Crime','Drama','Fantasy','Family','History','Horror','Music','Musical','Mystery','Romance','Sci-Fi','Sport','Thriller','War','Western'
for zhanri in zhanret_ndara:
    df = traindata['Genre'].str.contains(zhanri).fillna(False)
    print('Numri total i filmave me zhanrin: ',zhanri,'=',len(traindata[df]))
    f, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x = 'Year', data = traindata[df], palette = "Greens_d");
    plt.title(zhanri)
    krahasimi_vleresimit_filmave = ['Runtime_Minutes', 'Votes','Revenue_Millions', 'Metascore']
    for krahasimi in krahasimi_vleresimit_filmave:
        sns.jointplot(x='Rating', y = krahasimi, data = traindata[df], alpha = 0.7, color = 'b', height = 8)
        plt.title(zhanri)


# In[87]:


traindata.Director.value_counts()[:10].plot.pie(autopct='%1.1f%%',figsize=(10,10))
plt.title('TOP 10 Direktoret e filmave')


# In[88]:


traindata.Actors.value_counts()[:10].plot.pie(autopct='%1.1f%%',figsize=(10,10))
plt.title('TOP 10 Aktoret e filmave')


# In[89]:


traindata["Year"].value_counts()


# In[90]:


# Vizualizimi i numrit te filmave te bere gjate viteve 2006 - 2016.
sns.countplot(traindata['Year']);
plt.xlabel('Vitet');
plt.ylabel('Numri i filmave');
plt.show()


# In[118]:


# Vizualizimi i njejte por i paraqitur ne nje forme tjeter
pylab.rcParams['figure.figsize'] = (14.0, 8.0)

with plt.style.context('fivethirtyeight'):
    ax1 = plt.subplot2grid((3,3), (0,0), colspan=3)
    ax1.plot(traindata.groupby('Year').size(), 'ro-')
    ax1.set_title ('Te gjithe filmat')
    start, end = ax1.get_xlim()
    ax1.xaxis.set_ticks(np.arange(start, end, 1))
    
    pylab.gcf().text(0.5, 1.03, 
                    'Grupimi i filmave sipas viteve',
                     horizontalalignment='center',
                     verticalalignment='top', 
                     fontsize = 28)
    plt.tight_layout(2)
plt.show()


# In[91]:


# Vizualizimi i vlersimit te filmave
sns.countplot(traindata['Rating']);
plt.xlabel('Vleresimi nga 1 - 10');
plt.ylabel('Numri i filmave');
plt.show()


# In[121]:


# Vizualizimi i njejte por i paraqitur ne nje forme tjeter
pylab.rcParams['figure.figsize'] = (14.0, 8.0)

with plt.style.context('fivethirtyeight'):
    ax1 = plt.subplot2grid((3,3), (0,0), colspan=3)
    ax1.plot(traindata.groupby('Rating').size(), 'ro-')
    ax1.set_title ('Te gjithe filmat')
    start, end = ax1.get_xlim()
    ax1.xaxis.set_ticks(np.arange(start, end, 1))
    
    pylab.gcf().text(0.5, 1.03, 
                    'Grupimi i filmave sipas viteve',
                     horizontalalignment='center',
                     verticalalignment='top', 
                     fontsize = 28)
    plt.tight_layout(2)
plt.show()


# In[94]:


sns.stripplot(x="Year", y="Rating", data = traindata, jitter=True);
print('Vleresimi i bazuar ne vite')


# In[92]:


sns.swarmplot(x="Year", y="Votes", data = traindata);
print('Votat bazuar ne vite')


# In[98]:


sns.stripplot(x="Year", y="Revenue_Millions", data = traindata, jitter=True);
print('Te ardhurat (te shprehura ne milione) bazuar ne vite')


# In[96]:


sns.swarmplot(x="Year", y="Metascore", data = traindata);
print('Metascore bazuar ne vite')


# In[99]:


traindata["Runtime_Minutes"].value_counts()


# In[100]:


traindata.Runtime_Minutes.value_counts()[:10].plot.pie(autopct='%1.1f%%',figsize=(10,10))
plt.title('TOP 10 kohezgjatjet (runtime) me te medhaja te filmave')


# In[101]:


traindata["Rating"].value_counts()


# In[103]:


# Top 10 filmat me rating me te larte 
vlera = traindata.sort_values(['Rating'], ascending=False)
vlera.head(10)


# In[105]:


# 10 filmat me rating me te ulte 
vlera = traindata.sort_values(['Rating'], ascending=True)
vlera.head(10)


# In[107]:


# Filmat me rating me te ulte se 3.0
filmatedobet= traindata.query('(Rating > 0) & (Rating < 3.0)')
filmatedobet.head()


# In[111]:


# Top 5 filmat me te votuar 
votat = traindata.sort_values(['Votes'], ascending=False)
votat.head()


# In[113]:


f = votat.query('(Votes > 1000000)')
print('Numri i filmave te votuar me shume se 1 milion:')
len(f)


# In[114]:


print('Titujt dhe rangjet e filmave te votuara me shume se 1 milion:')
votat["Title"].head(6)


# In[115]:


print('Ratingu i  filmave te votuara me shume se 1 milion:')
votat["Rating"].head(6)


# In[116]:


# Renditja e bazuar ne te ardhurat
teardhurat = traindata.sort_values(['Revenue_Millions'], ascending=False)


# In[117]:


# Top 5 filmat me m� se shumti te ardhura
teardhurat.head()


# In[123]:


# Shohim se cilat atribute kane vlera null
traindata.isnull().sum().sort_values(ascending = False)


# In[145]:


traindata['Revenue_Millions'].value_counts()


# In[124]:


# fshijme vlerat null vetem te kolones Revenue_Millions
traindata.dropna(subset=['Revenue_Millions'], inplace=True)


# In[124]:


traindata['Metascore'].value_counts()


# In[125]:


# fshijme vlerat null vetem te kolones Metascore
traindata.dropna(subset=['Metascore'], inplace=True)


# In[126]:


traindata.shape


# In[127]:


features = ["Votes", "Revenue_Millions", "Metascore"]
X = traindata[features]
Y = traindata["Rating"]


# In[144]:


from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.7, test_size=0.3, random_state=42, shuffle=True)


# In[154]:


# Modeli I: Decision Tree

regressor =  DecisionTreeRegressor(random_state=42)
regressor.fit(X_train, Y_train)

dt = regressor.score(X_test, Y_test)

y_pred = regressor.predict(X_test)
print("Koeficienti i percaktimit te parashikimit: ", dt)
print("Perqindja e saktesise se parashikimmit me Decision Tree: ", round(dt * 100, 2), "%")
print("Mean squared error: %.2f"% mean_squared_error(Y_test, y_pred))


# In[155]:


# Modeli II: K Nearest Neighbors (KNN)

from sklearn.neighbors import KNeighborsRegressor
knn = KNeighborsRegressor()
knn.fit(X_train, Y_train)
y_pred = knn.predict(X_test)
n = knn.score(X_test, Y_test)
print("Koeficienti i percaktimit te parashikimit: ", n)
print("Perqindja e saktesise se parashikimmit me KNN: ", round(n * 100, 2), "%")
print("Mean squared error: %.2f"% mean_squared_error(Y_test, y_pred))


# In[482]:


# Modeli III: Random Forest

from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


randomforest = RandomForestRegressor()
randomforest.fit(X_train, Y_train)
y_pred = randomforest.predict(X_test)
rf = randomforest.score(X_test, Y_test)
print("Koeficienti i percaktimit te parashikimit: ", rf)
print("Perqindja e saktesise se parashikimmit me Random Forest: ", round(rf * 100, 2), "%")
print("Mean squared error: %.2f"% mean_squared_error(Y_test, y_pred))


# In[422]:


# Modeli IV: Extra Trees

from sklearn.ensemble import ExtraTreesRegressor
et = ExtraTreesRegressor()
et.fit(X_train, Y_train)
y_pred = et.predict(X_test)
etr = et.score(X_test, Y_test)
print("Koeficienti i percaktimit te parashikimit: ", etr)
print("Perqindja e saktesise se parashikimmit me Extra Trees Regression: ", round(etr * 100, 2), "%")
print("Mean squared error: %.2f"% mean_squared_error(Y_test, y_pred))


# In[483]:


modelet = pd.DataFrame({
    'Modeli': ['KNN','Random Forest','Decision Tree','Extra Trees'],
    'Perqindja': [  
              n * 100, rf * 100, dt * 100, etr * 100]})
modelet.sort_values(by='Perqindja', ascending=False)

