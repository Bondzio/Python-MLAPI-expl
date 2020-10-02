#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.plotly as py 
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

import os
import sys
print(os.listdir("../input"))


# In[ ]:


veriler = pd.read_csv('../input/2017.csv')


# In[ ]:


veriler.columns


# In[ ]:


veriler.head(20)


# In[ ]:


veriler.describe()


# In[ ]:


country = list(veriler['Country'])
hpns = list(veriler['Happiness.Score'])
frdm = list(veriler['Freedom'])
economy = list(veriler['Economy..GDP.per.Capita.'])


# In[ ]:


veriler.isnull().values.any() #null values test


# In[ ]:


plt.figure(figsize=(20,10))
ax= sns.barplot(x=country[:20], y=hpns[:20],palette = sns.cubehelix_palette(len(country[:20])))
plt.xlabel('Top 20 of Most Happy Countries')
plt.xticks(rotation='vertical')
plt.ylabel('Happiness Score')
plt.title('Most Happy Countries')
plt.show()


# In[ ]:


plt.figure(figsize=(20,10))
ax= sns.barplot(x=country[135:], y=hpns[135:],palette = sns.cubehelix_palette(len(country[:20])))
plt.xlabel('Top 20 of Most Unhappy Countries')
plt.xticks(rotation='vertical')
plt.ylabel('Happiness Score')
plt.title('Most UnHappy Countries')
plt.show()


# In[ ]:


print('Most Happy Country is: ',veriler.iloc[0,0])
print('Most UnHappy Country is: ',veriler.iloc[154,0])


# In[ ]:


hsnx = veriler.iloc[:,2:3].values
frdmy = veriler.iloc[:,8:9].values


# In[ ]:



from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(frdmy,hsnx)
hsnxpred = lr.predict(frdmy)


# In[ ]:


plt.figure(figsize=(20,10))
plt.ylabel('Happiness Score')
plt.xlabel('Freedom')
plt.scatter(frdm,hpns,color='red')
plt.plot(frdmy,hsnxpred, linewidth=4)
plt.show()


# In[ ]:


veriler.head()


# In[ ]:


verilercor = veriler.drop(columns=['Happiness.Rank','Country','Whisker.high','Whisker.low'])


# In[ ]:


plt.figure(figsize=(20,10))
sns.heatmap(verilercor.corr(),annot=True, fmt=".2f")
plt.show()


# In[ ]:


print('Number of Countries:',veriler['Country'].count())


# In[ ]:


print('Maximum Happines Score:',max(hpns))
print('Minimum Happines Score:',min(hpns))


# In[ ]:


veriler2 = veriler.copy()


# In[ ]:


veriler2['Happiness.Score'] = veriler['Happiness.Score']/max(hpns)
veriler2['Economy..GDP.per.Capita.'] = veriler['Economy..GDP.per.Capita.']/max(economy)


# In[ ]:


f,ax1 = plt.subplots(figsize =(20,10))
sns.pointplot(x='Country',y='Happiness.Score',data=veriler2,color='green',alpha=1)
sns.pointplot(x='Country',y='Economy..GDP.per.Capita.',data=veriler2,color='red',alpha=1)
plt.text(10,0.1,'Economy(GDP)',color='red',fontsize = 17,style = 'italic')
plt.text(130,0.90,'Happiness Score',color='green',fontsize = 18,style = 'italic')
plt.xlabel('Countries (1-155)',fontsize = 15,color='blue')
plt.ylabel('Values',fontsize = 15,color='blue')
plt.title('Happiness Score  VS  Economy(GDP)',fontsize = 20,color='blue')
plt.grid()


# In[ ]:


turkey = veriler['Country'] == 'Turkey'
Turkey = veriler[turkey]
Turkey


# In[ ]:


filterh = sum(hpns) / float(len(hpns))
print(filterh)
if Turkey['Happiness.Score'].values >= filterh:
    print('Turkey is a Happy Country')
else:
    print('Turkey is an Unhappy Country')


# In[ ]:


data = dict(type = 'choropleth', 
           locations = veriler['Country'],
           locationmode = 'country names',
           z = veriler['Happiness.Score'], 
           text = veriler['Country'],
           colorbar = {'title':'Happiness'})
layout = dict(title = 'Happiness 2017', 
             geo = dict(showframe = False, 
                       projection = {'type': 'equirectangular'}))
choromap3 = go.Figure(data = [data], layout=layout)
iplot(choromap3)


# In[ ]:


print('X = Freedom')
print('Y = Economy (GDP)')
print('Z = Happiness Score')
trace1 = go.Scatter3d(
    x=veriler.Freedom,
    y=veriler['Economy..GDP.per.Capita.'],
    z=veriler['Happiness.Score'],
    mode='markers',
    marker=dict(
        size=5,
        color='rgb(255,0,0)',                  
    )
)

data = [trace1]
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0  
    )
    
)
fig = go.Figure(data=data, layout=layout)
iplot(fig)


# **What we learned from this data analysis:**
# * There is linear relationship between Economy and Happiness.
# * There is linear relationship between Freedom and Happiness.
# * Most Happy Country is:  Norway
# * Most UnHappy Country is:  Central African Republic

# In[ ]:




