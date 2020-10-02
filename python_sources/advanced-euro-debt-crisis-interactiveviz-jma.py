#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots
get_ipython().run_line_magic('matplotlib', 'inline')


import plotly.tools as tls
import cufflinks as cf
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)

print(__version__) # requires version >= 1.9.0
cf.go_offline()


# In[ ]:


df = pd.read_csv('../input/euro-debt-crisis/P6-EuroDebtCrisis.csv')
df.head()


# In[ ]:


df_reg=df.groupby(['Creditor']).agg({'Amount':'sum'}).sort_values(["Amount"],ascending=False).reset_index()
df_reg.head(10)


# In[ ]:


fig = go.Figure(data=[go.Table(
    columnwidth = [50],
    header=dict(values=('Creditor', 'Amount'),
                fill_color='#104E8B',
                align='center',
                font_size=14,
                font_color='white',
                height=40),
    cells=dict(values=[df_reg['Creditor'].head(10), df_reg['Amount'].head(10)],
               fill=dict(color=['#509EEA', '#A4CEF8',]),
               align='right',
               font_size=12,
               height=30))
])

fig.show()


# In[ ]:


df_reg.iplot(kind='box')


# In[ ]:


fig = px.pie(df_reg.head(10),
             values="Amount",
             names="Creditor",
             title="Amount",
             template="seaborn")
fig.update_traces(rotation=90, pull=0.05, textinfo='value+label')
fig.show()

