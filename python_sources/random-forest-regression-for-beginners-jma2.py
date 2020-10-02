#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


df=pd.read_csv("../input/car-speeding-and-warning-signs/amis.csv")
df.head()


# In[ ]:


x=df.speed.values.reshape(-1,1)
y=df.warning.values.reshape(-1,1)


# In[ ]:


from sklearn.ensemble import RandomForestRegressor
rf=RandomForestRegressor(n_estimators=100,random_state=42)
rf.fit(x,y)


# In[ ]:


rf.predict([[7.5]])


# In[ ]:


x_=np.arange(min(x),max(x),0.01).reshape(-1,1)


# In[ ]:


y_head=rf.predict(x_)


# In[ ]:


plt.figure(figsize=(18,6))
plt.scatter(x,y,color="r")
plt.plot(x_,y_head,color="g")
plt.xlabel("Cost")
plt.ylabel("q")
plt.show()

