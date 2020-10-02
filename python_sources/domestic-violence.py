#!/usr/bin/env python
# coding: utf-8

# My Inspiration
# ***Maria da Penha Maia Fernandes is a Brazilian biopharmacist and women human rights defender. She advocates for women rights, particularly against domestic violence. Maria da Penha was a victim of domestic violence by her husband. In 1983, her husband, attempted to kill her twice. The first time he shot her in her sleep, but she survived, the second time he tried to electrocute her while she showered. Penha was left paraplegic due to these attacks. The husband was jailed for two years and was released in 2002.

# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpAIaLwMGELoTuQbFyVrTNeuNITWMHsFoYoFWcEC_UwPu3lLnM&s',width=400,height=400)


# Image plenarinho.leg.br

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsKXsN8fQuv4HyH9Plys9aeZopK9uoDbHjNngB3lBLo6MaYMRkjg&s',width=400,height=400)


# Image marlborough-ma.gov

# In[ ]:


nRowsRead = 1000 # specify 'None' if want to read whole file
df = pd.read_csv('../input/cusersmarildownloadsdomviolcsv/domviol.csv', delimiter=';', encoding = "ISO-8859-1", nrows = nRowsRead)
df.dataframeName = 'domviol.csv'
nRow, nCol = df.shape
print(f'There are {nRow} rows and {nCol} columns')


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuSgOo2oDgYvee6-OuHL_s-cK3ZNEmRz4UnfUe3ilkKZMjgrEmvg&s',width=400,height=400)


# Image hdnbc.org

# In[ ]:


df.head()


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQY7_JDGRvUv9UBBBBW8rLXRlwbSdpeqsNLWaI43b3FMLMXbIDM&s',width=400,height=400)


# Image focusforhealth.org

# In[ ]:


df.info()


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUzfiUghiBsUEaMqyMRxEYhmwUq1IHtlmnGyhT4ME8RZY3Waf0vw&s',width=400,height=400)


# These are the names of the 999 female victims of domestic violence  
# * Image euronews.com

# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwm6V9HkfxOC71zjinmjFrqwoO13KMQBpaSZmtliXZsLESveEs&s',width=400,height=400)


# Image dvfree.org.nz

# In[ ]:


df.describe()


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJXkXvnXuW16N63VAw0qDaCcukOHpdjCvtXyKhJbJt51StJbx4&s',width=400,height=400)


# Image chicagopolicyreview.org

# In[ ]:


categorical_cols = [cname for cname in df.columns if
                    df[cname].nunique() < 10 and 
                    df[cname].dtype == "object"]


# Select numerical columns
numerical_cols = [cname for cname in df.columns if 
                df[cname].dtype in ['int64', 'float64']]


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQE5szB1NSHwUvb_kbAncoOH7ZdHqu_YdY1t0UlcoUBTFVAVFeF&s',width=400,height=400)


# Image theadvocate.com

# In[ ]:


print(numerical_cols)


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7hk4kiNtpSAs66o9nE6LeHzeE-gMubtvnPt9TX83tKyz-aC8y&s',width=400,height=400)


# Image istockphoto.com

# In[ ]:


#Missing values. Codes from my friend Caesar Lupum @caesarlupum
total = df.isnull().sum().sort_values(ascending = False)
percent = (df.isnull().sum()/df.isnull().count()*100).sort_values(ascending = False)
missing_data  = pd.concat([total, percent], axis=1, keys=['value', 'period'])
missing_data.head(8)


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbsXsrnrIDUL2VxSkgQ6RLJ8VvKUY7y8mqv2l1W5D2k0STc6s2&s',width=400,height=400)


# Image ncdsv.org

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIF_qvx4S8-X_5k-0jvUrDzKiKfg4RtLisBWeoBnogZjNKDpYpnw&s',width=400,height=400)


# Men can be victims of domestic violence 
# * Image dallasnews.com

# In[ ]:


import plotly.offline as pyo
import plotly.graph_objs as go
lowerdf = df.groupby('value').size()/df['period'].count()*100
labels = lowerdf.index
values = lowerdf.values

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])
fig.show()


# In[ ]:


sns.scatterplot(x='value',y='period',data=df)


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpogRtCE5GmcSZgaO5eMAovxZuKUGsNOV5UBa5c8dPlU5OAi89dA&s',width=400,height=400)


# Image dfsv.aventedge.com

# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwQsFLi7_BWBB9AJPCWAcjVo6QkNnPfgtasOVTisK9Bm4DsBcz&s',width=400,height=400)


# Image pendleton.marines.mil

# In[ ]:


plt.figure(figsize=(8, 5))
pd.value_counts(df['value']).plot.bar()
plt.show()


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0HTGXleV0MZkGU-cFgc2_fCnP20Jqc7kA7AIRO_XNqjZnbXO-&s',width=400,height=400)


# Image intermountainhealthcare.org

# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSA2_FOPT7x8dxjHNJJwVTgAP4KnrU9eGDfHnJzvoEBgsF054QI&s',width=400,height=400)


# Image siumed.org

# In[ ]:


sns.countplot(df["value"])


# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWszYeHQ7ANMwpJNKsMZRMdrhS4MgH7kMnWp0iEh9KKaUKhrSxvw&s',width=400,height=400)


# Image kjct8.com

# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTt8jE36cCpCcyGjNZMsYxKQaLG2x4Ycp-9RLQmkhPqpYxyorfFiQ&s',width=400,height=400)


# Image intervalhousect.org
