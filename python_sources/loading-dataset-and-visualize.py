#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import plotly.graph_objects as go
import numpy as np
import os


# Load price data

# In[ ]:


prices = np.loadtxt('../input/binance-bitcoin-futures-price-10s-intervals/prices_btc_Jan_11_2020_to_May_22_2020.txt', dtype=float)


# In[ ]:


len(prices)


# In[ ]:


fig = go.Figure(data=go.Scatter(y=prices[-10000:]))
fig.show()


# In[ ]:




