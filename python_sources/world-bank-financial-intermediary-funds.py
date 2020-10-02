#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


df_funds = pd.read_csv('/kaggle/input/financial-intermediary-funds-funding-decisions/financial-intermediary-funds-funding-decisions.csv')


# In[ ]:


df_funds.info()


# In[ ]:


df_funds.nunique()


# In[ ]:


_=df_funds[['Calendar Year', 'Amount in USD']].plot(kind='scatter', x='Calendar Year', y='Amount in USD')


# In[ ]:


plt.subplots(figsize=(16, 10))
_=sns.scatterplot(x='Calendar Year', y='Amount in USD',data=df_funds, hue="Sector/Theme", alpha=0.7,palette="Set2")


# In[ ]:


#https://seaborn.pydata.org/tutorial/axis_grids.html
g = sns.FacetGrid(df_funds, row="Sector/Theme", aspect=3, height=7)
#hue="Approval Quarter",
#g.map(plt.scatter, "Calendar Year", "Amount in USD", alpha=.7,  cmap="coolwarm")
_=g.map(sns.regplot, "Calendar Year", "Amount in USD", fit_reg=False, x_jitter=.1)
_=g.add_legend()
#col="smoker",


# In[ ]:


_=df_funds["Amount in USD"].plot(kind='hist', logy=True, bins=20)


# In[ ]:


_=df_funds["Amount in USD"].plot(kind='box', logy=True)


# In[ ]:


import plotly.express as px
fig = px.scatter(df_funds, x="Calendar Year", y="Amount in USD", facet_row="Use Code",
                width=1000, height=1300)
# color="Approval Quarter",
fig.show()


# In[ ]:


fig = px.scatter(df_funds, x="Calendar Year", y="Amount in USD", facet_row="Approval Quarter",
                width=1000, height=1300)
fig.show()


# In[ ]:


fig = px.scatter(df_funds, x="Calendar Year", y="Amount in USD", facet_row="Sector/Theme",
                width=1000, height=1600)
fig.show()


# In[ ]:


plt.subplots(figsize=(16, 7))
ax = sns.boxplot(x="Sector/Theme", y="Amount in USD", data=df_funds)
ax.set_yscale('log')


# In[ ]:


plt.subplots(figsize=(16, 7))
ax = sns.boxplot(x="Sector/Theme", y="Amount in USD",hue="Approval Quarter", data=df_funds)
ax.set_yscale('log')


# In[ ]:


plt.subplots(figsize=(7, 16))
ax = sns.boxplot(y="Financial Product", x="Amount in USD", data=df_funds)
ax.set_xscale('log')


# In[ ]:


plt.subplots(figsize=(7, 16))
ax = sns.boxplot(y="Fund Name", x="Amount in USD", data=df_funds)
ax.set_xscale('log')


# In[ ]:


df_funds['Fund Name+Sub Account'] = df_funds['Fund Name']+'-'+df_funds['Sub Account']


# In[ ]:


plt.subplots(figsize=(7, 16))
ax = sns.boxplot(y='Fund Name+Sub Account', x="Amount in USD", data=df_funds)
ax.set_xscale('log')


# In[ ]:


plt.subplots(figsize=(10, 7))
ax = sns.boxplot(x="Approval Quarter", y="Amount in USD", data=df_funds)
ax.set_yscale('log')


# In[ ]:


plt.subplots(figsize=(10, 7))
ax = sns.boxplot(x="Use Code", y="Amount in USD", data=df_funds)
ax.set_yscale('log')


# In[ ]:


plt.subplots(figsize=(10, 7))
ax = sns.boxplot(x="Use Code", y="Amount in USD",hue="Approval Quarter", data=df_funds)
ax.set_yscale('log')


# In[ ]:


# ax = sns.stripplot(y="Calendar Year", x="Amount in USD", hue="Use Code",
#                    data=df_funds, jitter=True)


# In[ ]:


ax = sns.catplot(x="Use Code", y="Amount in USD",
                row='Fund Name', 
                data=df_funds, kind="box",
                aspect=2);

