#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


data = pd.read_csv('/kaggle/input/videogames-sales-dataset/PS4_GamesSales.csv',encoding = 'windows-1252')


# In[ ]:


data.columns


# In[ ]:


data.info()


# In[ ]:


data.head(10)


# In[ ]:


data.tail(10)


# In[ ]:


data.Publisher.unique()


# In[ ]:


data.Genre.unique()


# In[ ]:


plt.subplots(figsize = (10,7))
plt.hist(data.Year,bins = 30)
plt.show()


# In[ ]:


rockstar = data[data.Publisher == 'Rockstar Games']
activision = data[data.Publisher == 'Activision']
sony = data[data.Publisher == 'Sony Interactive Entertainment']
bethesda = data[data.Publisher == 'Bethesda Softworks']


# In[ ]:


rockstar.head()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.hist(rockstar.Game)
plt.show()


# In[ ]:


plt.scatter(rockstar.Year,rockstar['North America'],color = 'red',alpha = 0.5)
plt.xlabel('Year')
plt.ylabel('North America Sale')
plt.show()


# In[ ]:


activision.head(20)


# In[ ]:


activision.tail()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.hist(activision.Game,bins = 40)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(activision.Year,activision['North America'],color = 'red',alpha = 0.5)
plt.xlabel('Year')
plt.ylabel('North America Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(activision.Year,activision['Europe'],color = 'red',alpha = 0.5)
plt.xlabel('Year')
plt.ylabel('Europe Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(activision.Year,activision.Japan,color = 'red',alpha = 0.5)
plt.xlabel('Year')
plt.ylabel('Japan Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(activision.Year,activision.Global,color = 'red',alpha = 0.5)
plt.xlabel('Year')
plt.ylabel('Global Sale')
plt.show()


# In[ ]:


sony.head(10)


# In[ ]:


sony.tail(10)


# In[ ]:


plt.subplots(figsize = (10,5))
plt.hist(sony.Game,bins = 30)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(sony.Year,sony['North America'],alpha = 0.5,color = 'red')
plt.xlabel('Year')
plt.ylabel('North America Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(sony.Year,sony['Europe'],alpha = 0.5,color = 'red')
plt.xlabel('Year')
plt.ylabel('Europe Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(sony.Year,sony['Japan'],alpha = 0.5,color = 'red')
plt.xlabel('Year')
plt.ylabel('Japan Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(sony.Year,sony['Global'],alpha = 0.5,color = 'red')
plt.xlabel('Year')
plt.ylabel('Global Sale')
plt.show()


# In[ ]:


bethesda.head(10)


# In[ ]:


bethesda.tail(10)


# In[ ]:


plt.subplots(figsize = (10,5))
plt.hist(bethesda.Game,bins = 6)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(bethesda.Year,bethesda['North America'],alpha = 0.5,color = 'red')
plt.xlabel('Year')
plt.ylabel('North America Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(bethesda.Year,bethesda['Europe'],alpha = 0.5,color = 'red')
plt.xlabel('Year')
plt.ylabel('Europe Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(bethesda.Year,bethesda['Japan'],alpha = 0.5,color = 'red')
plt.xlabel('Year')
plt.ylabel('Japan Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.scatter(bethesda.Year,bethesda['Global'],alpha = 0.5,color = 'red')
plt.xlabel('Year')
plt.ylabel('Global Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.plot(rockstar.Global,rockstar['North America'],color = 'red',label = 'North America')
plt.plot(rockstar.Global,rockstar['Europe'],color = 'green',label = 'Europe')
plt.plot(rockstar.Global,rockstar['Japan'],color = 'blue',label = 'Japan')
plt.legend()
plt.xlabel('Global Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.plot(activision.Global,activision['North America'],color = 'red',label = 'North America')
plt.plot(activision.Global,activision['Europe'],color = 'green',label = 'Europe')
plt.plot(activision.Global,activision['Japan'],color = 'blue',label = 'Japan')
plt.legend()
plt.xlabel('Global Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.plot(sony.Global,sony['North America'],color = 'red',label = 'North America')
plt.plot(sony.Global,sony['Europe'],color = 'green',label = 'Europe')
plt.plot(sony.Global,sony['Japan'],color = 'blue',label = 'Japan')
plt.legend()
plt.xlabel('Global Sale')
plt.show()


# In[ ]:


plt.subplots(figsize = (10,5))
plt.plot(bethesda.Global,bethesda['North America'],color = 'red',label = 'North America')
plt.plot(bethesda.Global,bethesda['Europe'],color = 'green',label = 'Europe')
plt.plot(bethesda.Global,bethesda['Japan'],color = 'blue',label = 'Japan')
plt.legend()
plt.xlabel('Global Sale')
plt.show()

