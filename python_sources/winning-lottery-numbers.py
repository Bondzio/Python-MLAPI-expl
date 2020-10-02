#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import the data, specify data types
import pandas as pd
df = pd.read_csv('../input/Lottery_NY_Lotto_Winning_Numbers__Beginning_2001.csv')
df.head()


# ## Data manipulation
# 
# Let's split up those numbers so that we each number in a winning combination has its own row.

# In[ ]:


df.columns = ['Date', 'Numbers', 'Bonus','Extra']
df["AllNumbers"] = df["Numbers"].map(str) + " " + df["Bonus"].map(str)
df2 = df.copy()
del df2['Bonus']
del df2['Extra']
del df2['Numbers']


# In[ ]:


df3 = pd.DataFrame(df2['AllNumbers'].str.split(" ").apply(pd.Series, 0).stack())
df3.index = df3.index.droplevel(-1)
df3.head(20)


# In[ ]:


merged = pd.merge(df, df3,  how='inner', left_index=True, right_index=True)
del merged['Numbers']
del merged['AllNumbers']
del merged['Extra']
del merged['Bonus']
merged.columns = ['Date','Number']
merged.reset_index(inplace=True)
merged.head(20)


# In[ ]:


dothis = lambda x: pd.Series([i for i in reversed(x.split('/'))])
dates = merged['Date'].apply(dothis)
merged2 = pd.merge(merged, dates,  how='inner', left_index=True, right_index=True)
del merged2['index']
merged2.columns = ['Date','Number','Year','Day','Month']
merged2.head(20)


# In[ ]:


merged2.info()


# In[ ]:


merged2['Number'] = merged2['Number'].astype(int)
merged2.info()


# ## Frequency of numbers in winning combinations
# 
# You could try to see which numbers had not been called in a while (like No. 6 in the plot below) and consider adding those to your selection.

# In[ ]:


import seaborn as sns
import matplotlib as mpl
mpl.rc("figure", figsize=(12, 20))
ax = sns.countplot(y="Number", data=merged2)


# ## Combining Numbers
# 
# Another way you could try to get an edge is add up your selected numbers. Does their total fall in the distribution where most winning combination sums fall (about 175 to 250 based on the histogram below).

# In[ ]:


sumtotal = merged2.groupby(['Date']).sum() # total up the winning combination numbers 
sumtotal.describe()


# In[ ]:


# show the distribution of winning combinations' totals
mpl.rc("figure", figsize=(12, 6))
ax = sns.distplot(sumtotal['Number'])

