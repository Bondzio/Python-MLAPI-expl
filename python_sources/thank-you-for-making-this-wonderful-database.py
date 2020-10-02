#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model, preprocessing, svm
from sklearn.preprocessing import StandardScaler, Normalizer
import math
import matplotlib
import seaborn as sns
import os
from textwrap import wrap
#import ML packages
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress


get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


print(os.listdir('../input/'))


# In[ ]:


df1 = pd.read_csv('../input/tc20171021.csv', error_bad_lines = False)#, sep=',', header=0)#, encoding='cp1252')


# In[ ]:


df1.sample(10)


# In[ ]:


df1.describe()


# In[ ]:


df1.Make.value_counts()


# In[ ]:


df1['YearsOld'] = 2018-df1.Year


# # I'm not going to buy a car less than five years old. Those data points will just skew the delcine rate 

# In[ ]:


#df1 = df1[df1.YearsOld >= 5]


# # I'll only consider Models with atleast 5 data points

# In[ ]:


groupped = df1.groupby('Model').size().reset_index().rename(columns={0: 'count'})
few = groupped[groupped['count'] < 5]
#df1 = df1[~df1.Model.isin(few.Model)]


# In[ ]:


(groupped['count'] < 5).value_counts()


# # They also must have been in production for at least 5 years

# In[ ]:


groupped = df1.groupby('Model')
groupped = groupped.apply(lambda x: x.YearsOld.max() - x.YearsOld.min()).reset_index().rename(columns={0: 'Span'})
few = groupped[groupped['Span'] < 5]
#df1 = df1[~df1.Model.isin(few.Model)]


# In[ ]:


(groupped['Span'] < 5).value_counts()


# # I want to buy a car less than 10 years old so I'll remove models with no production in last decade

# In[ ]:


groupped = df1.groupby('Model')
groupped = groupped.apply(lambda x: x.YearsOld.min()).reset_index().rename(columns={0: 'Youngest'})
few = groupped[groupped['Youngest'] > 10]
#df1 = df1[~df1.Model.isin(few.Model)]


# In[ ]:


(groupped['Youngest'] > 10).value_counts()


# In[ ]:


df1.isnull().sum()


# In[ ]:


df1[df1.Make == "Jeep"].Model.value_counts()


# In[ ]:


def fit(df): 
    GrpYr = plotme.groupby('YearsOld')
    Quint50 = GrpYr.quantile(0.5).reset_index()#GrpYr.median().reset_index()
    Quint10 = GrpYr.quantile(0.1).reset_index()
    Quint90 = GrpYr.quantile(0.90).reset_index()
    
    Y = Quint50[['Price']].values#df[['Price']].values
    X = Quint50[['YearsOld']].values#df[['YearsOld']].values
    
    return ((X*Y).mean(axis=1) - X.mean()*Y.mean(axis=1)) / ((X**2).mean() - (X.mean())**2)


# In[ ]:


def model(df):
    GrpYr = plotme.groupby('YearsOld')
    Quint50 = GrpYr.quantile(0.5).reset_index()#GrpYr.median().reset_index()
    Quint10 = GrpYr.quantile(0.1).reset_index()
    Quint90 = GrpYr.quantile(0.90).reset_index()
    
    y = Quint50[['Price']].values#df[['Price']].values
    X = Quint50[['YearsOld']].values#df[['YearsOld']].values
    
    fit = LinearRegression(fit_intercept=False).fit(X, y)
    
    return [np.squeeze(fit.coef_)]#,fit.predict(0)]

def group_predictions(df, date):
    date = pd.to_datetime(date)
    df.date = pd.to_datetime(df.date)

    day = np.timedelta64(1, 'D')
    mn = df.date.min()
    df['date_delta'] = df.date.sub(mn).div(day)

    dd = (date - mn) / day

    return df.groupby('group').apply(model, delta=dd)


# GrpYr = plotme.groupby('YearsOld')
# Quint50 = GrpYr.quantile(0.5).reset_index()#GrpYr.median().reset_index()
# Quint10 = GrpYr.quantile(0.1).reset_index()
# Quint90 = GrpYr.quantile(0.90).reset_index()
# 
# Y = np.squeeze(Quint50[['Price']].values)#df[['Price']].values
# X = np.squeeze(Quint50[['YearsOld']].values)#df[['YearsOld']].values

# linregress(X, Y)

# In[ ]:


df = pd.DataFrame({'A': 'a a b'.split(), 'B': [1,2,3], 'C': [4,6, 5], 'D': [21,22,23]})
print(df.head())
g = df.groupby('A')
g.apply(lambda x: [x.C.max() - x.B.min(),4])


# In[ ]:


df = pd.DataFrame(np.random.rand(5,5), columns=list('ABCDE'))
print(df.head())
f = {'B':['prod'], 'D': lambda g: df.loc[g.index].E.sum()}

df.groupby('A').agg(f)


# In[ ]:


df = pd.DataFrame({'A': 'a a b'.split(), 'B': [1,2,3], 'C': [4,20, 5], 'D' : ['1','1','3']})
print(df.head())
g = df.groupby(['D','A'])
g.apply(lambda x: linregress(x.C.values,x.B.values).slope)


# In[ ]:


df1.head()


# In[ ]:


MMGrp = df1.groupby(['Make','Model'])

#f = {'B':['prod'], 'D': lambda g: df.loc[g.index].E.sum()}
f = {'Price': [lambda x: linregress(df1.loc[x.index].YearsOld,x).slope,'count'], 'YearsOld' : ['min']}

MMdf = MMGrp.agg(f)

#MMdf = MMGrp.apply(lambda x: linregress(x.YearsOld.values,x.Price.values).slope).reset_index().rename(columns={0: 'dpdy'})
MMdf.head()


# In[ ]:


bm = MMdf['YearsOld']['min']<=10
bm.value_counts()


# In[ ]:


MMdf['Price']['<lambda>']


# In[ ]:


MMdf.dropna(inplace = True)

#MMdf.rename(columns={0: 'd$/d(year)'})

print('Gain Value Over Time: %d' % (len(MMdf.index) - len(MMdf[MMdf['Price']['<lambda>'] < 0].index)))

MMdf = MMdf[MMdf['Price']['<lambda>'] < 0]

MMdf.head()


# In[ ]:


MMdf.sort_values(by = ('Price','<lambda>'),ascending = False).head(500)


# In[ ]:


MMdf.reset_index(inplace = True)


# In[ ]:


MMdf[MMdf['Make']=='Jeep']


# In[ ]:


out = MMdf.to_csv('MMdf.csv')
print(out)


# In[ ]:


def plotQuints(plotme, ShowAll = False):
    plt.figure(figsize=(20,10),facecolor='white')
    
    
    GrpYr = plotme.groupby('YearsOld')
    Quint50 = GrpYr.quantile(0.5).reset_index()#GrpYr.median().reset_index()
    Quint10 = GrpYr.quantile(0.1).reset_index()
    Quint90 = GrpYr.quantile(0.90).reset_index()
    
    if ShowAll: plt.plot(plotme.Year,plotme.Price,'.k', label = 'All Data')

    plt.plot(Quint50.Year,Quint50.Price,'or', label = 'Median')
    plt.plot(Quint10.Year,Quint10.Price,'-g', label = '10th quintile')
    plt.plot(Quint90.Year,Quint90.Price,'-y', label = '90th quintile')
    
    wrapLength = 200
    
    plt.title('Make(s): ' + "\n".join(wrap(", ".join(plotme.Make.unique()),wrapLength)) + "\n Model(s): " + "\n".join(wrap(", ".join(plotme.Model.unique()),wrapLength)))
    plt.xlabel('Year')
    plt.ylabel('Price ($)')
    plt.legend()
    
    plt.grid(True)
    
    plt.xlim(plotme.Year.max()+1, plotme.Year.min()-1)
    
    plt.show()


# In[ ]:


def plotQuintsMileage(plotme, ShowAll = False):
    plt.figure(figsize=(20,10),facecolor='white')
    
    GrpYr = plotme.groupby('YearsOld')
    Quint50 = GrpYr.quantile(0.5).reset_index()#GrpYr.median().reset_index()
    Quint10 = GrpYr.quantile(0.1).reset_index()
    Quint90 = GrpYr.quantile(0.90).reset_index()
    
    if ShowAll: plt.plot(plotme.Mileage,plotme.Price,'.k', label = 'All Data')

    plt.plot(Quint50.Mileage,Quint50.Price,'or', label = 'Median')
    plt.plot(Quint10.Mileage,Quint10.Price,'-g', label = '10th quintile')
    plt.plot(Quint90.Mileage,Quint90.Price,'-y', label = '90th quintile')
    
    wrapLength = 200
    
    sTitle = 'Make(s): ' + "\n".join(wrap(", ".join(plotme.Make.unique()),wrapLength))
    sTitle = sTitle + "\n Model(s): " + "\n".join(wrap(", ".join(plotme.Model.unique()),wrapLength))
    sTitle = sTitle + "\n Year(s): " + "\n".join(wrap(", ".join(plotme.Year.sort_values().apply(str).unique()),wrapLength))
    
    plt.title(sTitle)
    plt.xlabel('Mileage')
    plt.ylabel('Price ($)')
    plt.legend()
    
    plt.grid(True)
    
    plt.show()


# In[ ]:


df1.head()


# In[ ]:


df1.head()


# In[ ]:


plotme = df1[df1.Make == 'Honda']
#plotme = df1[df1.Model == 'LibertyRenegade']
#plotme =df1[df1.Model.str.startswith('Forester2.5i')]
plotme =plotme[plotme.Model.str.startswith('CR-VEX-L')]

#plotme = plotme[plotme.YearsOld <= 20]#.sample(1000)
#plotme = plotme[plotme.YearsOld > 3]

plotQuints(plotme,True)





plotme =plotme[plotme.Year == 2014]
plotQuintsMileage(plotme,True)


# In[ ]:





# plotMedian.head()

# In[ ]:


df1[df1.Model.str.startswith('Escape')].count()


# In[ ]:





# In[ ]:




