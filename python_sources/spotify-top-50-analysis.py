#!/usr/bin/env python
# coding: utf-8

# Import plugin/library python yang akan digunakan

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# Baca file top50.csv diatas dengan menggunakan pandas dan buat dataframe baru.

# In[ ]:


file = '/kaggle/input/top50spotify2019/top50.csv'
df = pd.read_csv(file,encoding='ISO-8859-1')
df
df.head()


# In[ ]:


df.groupby(['Genre','Popularity']).sum()


# # Energy vs Danceability
# Visualisasi data antara Energy dengan Danceability, Enery adalah indikator bahwa lagu tersebut energetik atau tidak, sedangkan Daceability adalah indikator bahwa lagu tersebut mudah untuk ditarikan atau tidak.

# In[ ]:


sns.set_style('whitegrid')
g = sns.relplot(x='Energy', y='Danceability', data=df, kind='line', ci=None)
g.fig.suptitle('Energy vs Danceability', y=1.03)
plt.show()


# # Liveness & Track Length
# Liveness merupakan indikator yang menandakan apakah lagu tersebut direkam secara langsung atau tidak, sedangkan Length adalah panjang lagu dalam satuan detik.

# In[ ]:


print(df.groupby('Liveness')['Length.'].sum())
plt.figure(figsize=(10,10))
sns.catplot(x='Liveness', y='Length.', kind='bar', data=df, ci=None)
sns.catplot(x='Liveness', y='Length.', kind='box', data=df, whis=[0, 100])
plt.show()


# In[ ]:


plt.figure(figsize=(10,10))
sns.relplot(x="Energy",y="Popularity",data=df, hue="Genre", kind='line', ci=None)
plt.show()

