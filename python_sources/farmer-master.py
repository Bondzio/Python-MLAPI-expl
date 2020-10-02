#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_columns', 200)

pd.set_option('display.max_rows', 200)
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


farmer_df = pd.read_csv('/kaggle/input/farmermasterdb/farmer_db2.csv')


# In[ ]:


mas_villages = pd.read_csv('/kaggle/input/farmermasterdb/mas_villages.csv')


# In[ ]:


farmer_df.head(1)


# In[ ]:


farmer_df.shape


# In[ ]:


print("Total enter farmer {}".format(farmer_df.shape[0]))


# In[ ]:


farmer_df = farmer_df[['farmer_id','relation','gender','village_code', 'category']]


# In[ ]:


farmer_df.head(2)


# In[ ]:


farmer_df['category'] = farmer_df['category'].map({1.0:'SC',2.0:'ST',3.0:'OBC',4.0:'General',5.0:'General'})


# In[ ]:


farmer_df.head(5)


# In[ ]:


mas_villages.head(3)


# In[ ]:


farmer_df = farmer_df.merge(mas_villages, left_on='village_code', right_on='village_code')


# In[ ]:


farmer_df.head(3)


# In[ ]:


plt.figure(figsize=(10, 6))
g = sns.countplot(farmer_df['category'])
for p in g.patches:
    height = p.get_height()
    g.text(p.get_x()+p.get_width()/2.,
            height + 3, '{:1.2f}%'.format(height/farmer_df.shape[0]*100),
            ha="center",fontsize=14) 
plt.show()


# In[ ]:


print(pd.crosstab(farmer_df['district_name'],farmer_df['category'], normalize='index'))


# In[ ]:


plt.figure(figsize=(19, 6))
g = sns.countplot(x='district_name', hue='category', data=farmer_df)

plt.xticks(rotation=45)
plt.show()


# In[ ]:



props = farmer_df.groupby("district_name")['category'].value_counts(normalize=True).unstack()
props.plot(kind='bar', stacked='True', rot=45,figsize=(16,6))
plt.show()


# In[ ]:


'''plt.figure(figsize=(10, 6))
sns.boxenplot(x='district_name', y='cons.price.idx', hue='category', data=farmer_df )
plt.xticks(rotation=45)
plt.show()'''


# In[ ]:


plt.figure(figsize=(10, 9))
sns.heatmap(pd.crosstab(farmer_df['district_name'],farmer_df['category'],  normalize='index'),  annot=True,cmap="YlGnBu")
plt.show()


# In[ ]:


farmer_df.groupby(['district_name', 'category'])['category'].count()

