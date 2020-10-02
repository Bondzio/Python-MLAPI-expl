#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.set(style="whitegrid", palette="Paired")
plt.rcParams['figure.dpi'] = 130
import warnings
warnings.filterwarnings('ignore')

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


cardio = pd.read_csv('../input/cardiogoodfitness/CardioGoodFitness.csv')
cardio


# In[ ]:


cardio.info()


# In[ ]:


cardio.describe()


# In[ ]:


pr_cnt = cardio.Product.value_counts()
pr_pie = plt.pie(pr_cnt, labels = [f'{pr_cnt.index[0]}: {pr_cnt[0]}',
                                          f'{pr_cnt.index[1]}: {pr_cnt[1]}',
                                          f'{pr_cnt.index[2]}: {pr_cnt[2]}'], autopct='%1.1f%%')
pr_pie_circle = plt.Circle((0,0), 0.8, color='black', fc='white', linewidth=0)
p=plt.gcf()
p.gca().add_artist(pr_pie_circle)
plt.show()


# In[ ]:


cardio['Age_group'] = cardio.Age
cardio.Age_group = cardio.Age_group.map(lambda age: int(age//10+1))
cardio.Age_group.value_counts()


# In[ ]:


age_group_pie_set = cardio.Age_group.value_counts()
explode = (0,0,0,0,0.3)
labels_group_age = [f'{x*10-10} - {x*10-1} y/o' for x in age_group_pie_set.index]
age_group_pie = plt.pie(age_group_pie_set, explode=explode, labels=labels_group_age, autopct='%1.1f%%')


# In[ ]:


pd.crosstab(cardio['Product'],cardio['Age_group'])


# In[ ]:


pr_cp = sns.countplot(x="Product", hue="Gender", data=cardio)
for p in pr_cp.patches:
    pr_cp.annotate(p.get_height(), 
                        (p.get_x() + p.get_width() / 2.0, 
                         p.get_height()), 
                         ha = 'center', 
                         va = 'center', 
                         xytext = (0, 4),
                         textcoords = 'offset points')
plt.legend(bbox_to_anchor=(1.0, 0.7))


# In[ ]:


pr_cp = sns.countplot(x="Product", hue="MaritalStatus", data=cardio)
for p in pr_cp.patches:
    pr_cp.annotate(p.get_height(), 
                        (p.get_x() + p.get_width() / 2.0, 
                         p.get_height()), 
                         ha = 'center', 
                         va = 'center', 
                         xytext = (0, 3),
                         textcoords = 'offset points')


# In[ ]:


cardio.Usage.value_counts()


# In[ ]:


sns.factorplot(x='Usage', data=cardio , kind='count')


# In[ ]:


pd.crosstab(cardio['Product'],cardio['Usage'])


# In[ ]:


sns.kdeplot(cardio.Education[cardio.Product == 'TM195'], shade=True, color="r", label = 'TM195')
sns.kdeplot(cardio.Education[cardio.Product == 'TM498'], shade=True, color="b", label = 'TM498')
sns.kdeplot(cardio.Education[cardio.Product == 'TM798'], shade=True, color="gray", label = 'TM798')
plt.xlabel('Education (in years)')


# In[ ]:


sns.factorplot(x='Fitness', data=cardio , kind='count')


# In[ ]:


sns.countplot(x="Product", hue="Fitness", data=cardio)


# In[ ]:


pd.crosstab(cardio['Product'],cardio['Fitness'])


# In[ ]:


gr_inc = cardio.groupby('Product').Income.mean().plot(kind='bar', color=['skyblue', 'steelblue', 'darkseagreen'])
for p in gr_inc.patches:
    gr_inc.annotate(f'{int(p.get_height())}', 
                        (p.get_x() + p.get_width() / 2.0, 
                         p.get_height()), 
                         ha = 'center', 
                         va = 'center', 
                         xytext = (0, 4),
                         textcoords = 'offset points')
plt.xticks(rotation=0)


# In[ ]:


gr_inc = cardio.groupby('Product').Miles.mean().plot(kind='bar', color=['skyblue', 'steelblue', 'darkseagreen'])
for p in gr_inc.patches:
    gr_inc.annotate(f'{int(p.get_height())}', 
                        (p.get_x() + p.get_width() / 2.0, 
                         p.get_height()), 
                         ha = 'center', 
                         va = 'center', 
                         xytext = (0, 4),
                         textcoords = 'offset points')
plt.xticks(rotation=0)

