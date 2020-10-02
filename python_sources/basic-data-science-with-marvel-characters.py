#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv('../input/marvel-wikia-data.csv')
data.head(10)


# In[ ]:


data.info()


# In[ ]:


data.describe()


# In[ ]:


data.corr()


# In[ ]:


#correlation map
f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(data.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


# Line Plot
#data.APPEARANCES.plot(kind = 'line', color = 'g',label = 'Appearances',linewidth=1,alpha = 0.5,grid = True,linestyle = ':')
#data.Year.plot(color = 'r',label = 'Year',linewidth=1, alpha = 0.5,grid = True,linestyle = '-.')
#plt.legend(loc='upper right')    
#plt.xlabel('x axis')             
#plt.ylabel('y axis')
#plt.title('Line Plot')           
#plt.show()


# In[ ]:


# Scatter Plot 
data.plot(kind='scatter', x='APPEARANCES', y='Year',alpha = 0.5,color = 'red')
plt.xlabel('Appearance')             
plt.ylabel('Year')
plt.title('Appearance Year Scatter Plot')  


# In[ ]:


# Histogram
data.APPEARANCES.plot(kind = 'hist',bins = 50,figsize = (12,12))
plt.show()


# In[ ]:


#'normed' keyword is changed with 'density'.
data.plot(kind='hist', y='APPEARANCES', bins=25, range = (0,170), density=True)
plt.show()


# In[ ]:


#subplot
data.plot(subplots=True)
plt.show()


# In[ ]:


data1 = data.loc[:,['APPEARANCES','Year']]
data1.plot()
plt.show()


# In[ ]:


#filtering
x = data['Year']>1984
print(x)


# In[ ]:


data[np.logical_and(data['Year']>2000,data['APPEARANCES']>100)]


# In[ ]:


filter_data = data[np.logical_and(data['Year']>2000,data['ALIGN']=='Good Characters')]
filter_data


# In[ ]:


data.name[data.APPEARANCES>500] 


# In[ ]:


fltr_data2 = data[np.logical_and(data['APPEARANCES']>500,data['ALIGN']=='Bad Characters')]
fltr_data2


# In[ ]:


#tidy data
melt_data = pd.melt(frame=filter_data,id_vars='name',value_vars=['Year','ALIGN'])
melt_data


# In[ ]:


#pivoting data
#reverse of melting
melt_data.pivot(index='name',columns='variable',values='value')


# In[ ]:


#frequency of characters align
print(data['ALIGN'].value_counts(dropna=False))


# In[ ]:


data.boxplot(column='APPEARANCES',by ='Year')


# In[ ]:


new_data = data.head(10)
new_data


# In[ ]:


melted = pd.melt(frame=new_data,id_vars='name',value_vars=['ID','Year'])
melted


# In[ ]:


melted.pivot(index='name',columns='variable',values='value')


# In[ ]:


#concatenating data
#vertical concatenating
data1 = data.head(10)
data2 = data.tail(10)
conc_data = pd.concat([data1,data2],axis=0,ignore_index=True)
conc_data


# In[ ]:


#horizontal concatenating
data3=data['name'].head(10)
data4 = data['SEX'].head(10)
data5 = data['ID'].head(10)
conc_data2 = pd.concat([data3,data4,data5],axis=1)
conc_data2


# In[ ]:


data_name = data['name']
data_sex = (data[['SEX']]=='Female Characters')
data_align = (data[['ALIGN']]=='Bad Characters')
data_id = (data[['ID']]=='Public Identity')
conc_fml = pd.concat([data_name,data_sex,data_align,data_id],axis=1)
conc_fml


# In[ ]:





# In[ ]:


data_year = data['Year']>2000
data[data_year]


# In[ ]:


data.info()


# In[ ]:


data['Year'].value_counts(dropna = False)


# In[ ]:


#drop the nan values from Year
#assert data['Year'].dropna(inplace = True)


# In[ ]:


#plain python function 
def div(n):
    return n/1000
data.APPEARANCES.head(10).apply(div)


# In[ ]:


#plain python function with lambda
data.APPEARANCES.head(10).apply(lambda n : n/1000)


# In[ ]:


data2 = data.copy()
data2.head()


# In[ ]:


df = pd.DataFrame(data2)
df


# In[ ]:


#stacking dataframe
#sex and align are our new index.
#sex is outer index.
#align is inner index.
df1 = df.set_index(['SEX','ALIGN'])
df1


# In[ ]:


#change inner and outer index position.
df2 = df1.swaplevel(0,1)
df2


# In[ ]:


#groupby - according to sex, calculate the mean
df.groupby('SEX').mean()


# In[ ]:


#grouping data according the sex and find the max values.
df.groupby('SEX').page_id.max()


# In[ ]:


#grouping with multiple features.
#as we can see,the first characters came up in the 1939.
df.groupby('ALIGN')['page_id','Year'].min()

