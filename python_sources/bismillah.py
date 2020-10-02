#!/usr/bin/env python
# coding: utf-8

# "Ingin mengetahui bagaimana pengaruh tingkat rata-rata harga barang per penjual (avg. price) terhadap tanggal penjualan (date)?"

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


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# In[ ]:


plt.rcParams["figure.figsize"] = (10,6) # define figure size of pyplot


# In[ ]:


pd.set_option("display.max_columns", 100) # set max columns when displaying pandas DataFrame
pd.set_option("display.max_rows", 200) # set max rows when displaying pandas DataFrame


# In[ ]:


df = pd.read_csv('/kaggle/input/uisummerschool/Online_sales.csv')


# In[ ]:


df['Date']=pd.to_datetime(df['Date'],format='%Y%m%d')


# In[ ]:


df


# In[ ]:


df.describe() 


# In[ ]:


df.info()


# In[ ]:


df2=df.groupby('Date')['Avg. Price'].sum().reset_index(name='Avg_Price')


# In[ ]:


df2.sort_values('Avg_Price',ascending=False).head()


# Berdasarkan hasil tersebut, diketahui bahwa tingginya tingkat rata-rata harga barang per penjual (avg. price) tertinggi terjadi pada 27 November 2017, yaitu sebesar 34748.40. Grafik dibawah ini merepresentasikan tingkat rata-rata harga barang per penjual (avg. price) terhadap tanggal transaksi(date).

# In[ ]:


df2.set_index('Date').plot()


# Lebih lanjut, akan lebih baik apabila dapat dilihat pula keterkaitan antara rata-rata harga barang per penjual (avg.price), tanggal transaksi (date), banyaknya barang yang dapat dijual pada waktu tersebut (quantity) serta jenis barang (product) apa yang memiliki pengaruh terhadap hasil tersebut.
