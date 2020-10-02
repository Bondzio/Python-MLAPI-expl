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
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


investments = pd.read_csv("/kaggle/input/startup-investments-crunchbase/investments_VC.csv",encoding = 'unicode_escape')
investments.head(10)


# In[ ]:


investments.shape


# In[ ]:


investments.columns


# ### Startup Statistics
# Country and Market

# In[ ]:


investments["country_code"].value_counts(sort=True).iloc[:15].plot.bar(figsize=(15,7), width=.9)
plt.xticks(rotation=60)
plt.ylabel("#Startups")
plt.show()


# In[ ]:


investments[" market "].value_counts(sort=True).iloc[:15].plot.bar(figsize=(15,7), width=.9)
plt.xticks(rotation=60)
plt.ylabel("#Startups")
plt.show()


# ### Funding Statistics
# Country and Market

# In[ ]:


list(investments.columns[18:])


# In[ ]:


investments["procurement_total"] = investments[investments.columns[18:]].sum(axis=1)
investments[["name", " funding_total_usd ", "procurement_total"]].head(10)


# In[ ]:


investments["funding_total_usd"] = investments[" funding_total_usd "].str.replace(",", "").dropna(0)
investments["funding_total_usd"] = investments["funding_total_usd"].str.strip().replace("-", "0").fillna("0").astype(int)


# In[ ]:


funding_total_ctry = investments.groupby("country_code")["funding_total_usd"].sum()
funding_total_mrkt = investments.groupby(" market ")["funding_total_usd"].sum()
funding_mean_ctry = investments.groupby("country_code")["funding_total_usd"].mean()
funding_mean_mrkt = investments.groupby(" market ")["funding_total_usd"].mean()


# In[ ]:


funding_ctry = pd.merge(funding_mean_ctry, funding_total_ctry, on="country_code")
funding_ctry.columns = ["mean", "total"]


# In[ ]:


funding_mrkt = pd.merge(funding_mean_mrkt, funding_total_mrkt, on=" market ")
funding_mrkt.columns = ["mean", "total"]


# In[ ]:


def show_bar(df, title=""):
    df.plot.bar(figsize=(15,7), width=.9)
    plt.xticks(rotation=60)
    plt.ylabel(title)
    plt.show()


# In[ ]:


def show_top10(df, title=""):
    df_top10 = df.sort_values(ascending=False)[:10]
    show_bar(df_top10, title)


# In[ ]:


show_top10(funding_total_ctry, "funding total [USD]")


# In[ ]:


show_top10(funding_total_mrkt, "funding total [USD]")


# In[ ]:


show_top10(funding_mean_ctry, "funding mean [USD]")


# In[ ]:


show_top10(funding_mean_mrkt, "funding mean [USD]")


# In[ ]:




