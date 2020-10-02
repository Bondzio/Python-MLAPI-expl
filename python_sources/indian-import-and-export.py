#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
y=[]
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        y.append(os.path.join(dirname, filename))
    print(y)
    

# Any results you write to the current directory are saved as output.


# In[ ]:


exp=pd.read_csv(y[0])
imp.head()
imp=pd.read_csv(y[1])
exp.head()


# In[ ]:


exp.describe()


# In[ ]:


imp.describe()


# In[ ]:


exp.info()


# In[ ]:


imp.info()


# In[ ]:


imp.isnull().sum()


# In[ ]:


exp.isnull().sum()


# ## Import ##

# In[ ]:


len(imp[imp.country=='UNSPECIFIED'])


#     Drop where value is not present.

# In[ ]:


imp = imp[imp.value!=0]
imp.dropna(inplace=True)


# In[ ]:


imp.head()


# In[ ]:


len(imp)


# In[ ]:


imp.isnull().sum()


# In[ ]:


print("Import Commodity Count : "+str(len(imp['Commodity'].unique())))
print("Export Commodity Count : "+str(len(exp['Commodity'].unique())))


# In[ ]:


print("No of Country were we are importing Comodities are "+str(len(imp['country'].unique())))
print("No of Country were we are Exporting Comodities are "+str(len(exp['country'].unique())))


# In[ ]:



df1=imp.groupby('year').agg({'value':'sum'})
df1['Import']=imp.groupby('year').agg({'value':'sum'})
df1['Export']=exp.groupby('year').agg({'value':'sum'})
del df1['value']
df1['Defecit']= df1['Export']- df1['Import'] 
#df1.reset_index(drop = False)
df1=df1.reset_index()
df1


# In[ ]:



import matplotlib.pyplot as plt
df1.plot(x="year", y=["Import", "Export", "Defecit"], kind="bar",color=["g",'b',"r"])
plt.show()


# Import is increasing but export is almost constant.
# Bad sign for economy growth

# In[ ]:


df2=imp.groupby('country').agg({'value':'sum'})
df2['Import']=imp.groupby('country').agg({'value':'sum'})
df2['Export']=exp.groupby('country').agg({'value':'sum'})
del df2['value']
#df2['Defecit']= df2['Export']- df2['Import'] 
#df1.reset_index(drop = False)
df2=df2.reset_index()
df2.head()
topimp=df2.set_index('Import')
topimp=topimp.sort_index(axis=0,ascending=False).head(10)

topexp=df2.set_index('Export')
topexp=topexp.sort_index(axis=0,ascending=False).head(10)


# In[ ]:


topimp=topimp.reset_index()
topexp=topexp.reset_index()


# In[ ]:


topimp.plot(x="country", y=["Import"], kind="bar",color=["r"])
topexp.plot(x="country", y=["Export"], kind="bar",color=["g"])
plt.show()


# In[ ]:


df3=imp.groupby('Commodity').agg({'value':'sum'})
df3['Import']=imp.groupby('Commodity').agg({'value':'sum'})
df3['Export']=exp.groupby('Commodity').agg({'value':'sum'})
del df3['value']
#df2['Defecit']= df2['Export']- df2['Import'] 
#df1.reset_index(drop = False)
df3=df3.reset_index()
df3.head()


# In[ ]:


topimp=df3.set_index('Import')
topimp=topimp.sort_index(axis=0,ascending=False).head(10)

topexp=df3.set_index('Export')
topexp=topexp.sort_index(axis=0,ascending=False).head(10)


# In[ ]:


topimpc=df3.set_index('Import')
topimpc=topimp.sort_index(axis=0,ascending=False).head(10)

topexpc=df3.set_index('Export')
topexpc=topexp.sort_index(axis=0,ascending=False).head(10)


# In[ ]:


topimpc=topimpc.reset_index()
topexpc=topexpc.reset_index()


# In[ ]:


topexpc


# In[ ]:


topexpc


# In[ ]:


topimpc.plot(x="Commodity", y=["Import"], kind="bar",color=["r"])
topexpc.plot(x="Commodity", y=["Export"], kind="bar",color=["g"])
plt.show()


# In[ ]:




