#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup as bs
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


frame = pd.read_csv('../input/celebrity_deaths_4.csv',encoding='latin1')


# In[ ]:


frame.fame_score.fillna(0)


# In[ ]:


sns.countplot(frame.death_year)


# Filter to only the 'natural causes of death'

# In[ ]:


frame['natural_causes'] = False


# In[ ]:


frame.loc[(
frame['cause_of_death'].str.contains('cancer'))|
(frame['cause_of_death'].str.contains('cardiac'))|
(frame['cause_of_death'].str.contains('diabetes'))|
(frame['cause_of_death'].str.contains('cerebral'))|
(frame['cause_of_death'].str.contains('failure'))|
(frame['cause_of_death'].str.contains('sudden'))|
(frame['cause_of_death'].str.contains('disease'))|
(frame['cause_of_death'].str.contains('old'))|
(frame['cause_of_death'].str.contains('infection'))|                 
(frame['cause_of_death'].str.contains('cardiovascular'))|
(frame['cause_of_death'].str.contains('complications'))|
(frame['cause_of_death'].str.contains('pulmonary')), 'natural_causes'] = True


# In[ ]:


sns.set_style('dark',{"axes.facecolor": "1"})
sns.countplot(frame[frame.natural_causes ==False].death_year,palette=sns.color_palette("Greys_d",n_colors=1),label='Other')
sns.countplot(frame[frame.natural_causes ==True].death_year,palette=sns.color_palette("Reds_d",n_colors=1),label='Natural causes')
plt.legend(loc=2)
plt.xlabel('Year of death')
plt.ylabel('')
plt.yticks([])
plt.title('Celebrity deaths per year')


# Check to see if the age distribution of celebrities who died in 2016 from natural causes resembles the expected distribution of deaths for people born in the average year of a dead celebrity in 2016 (1945).

# In[ ]:


nat = frame_nc[frame_nc.death_year == 2016].age
male_n = np.random.normal(72,nat.std(),10000)
female_n = np.random.normal(77,nat.std(),10000)


# In[ ]:


sns.distplot(nat,hist=False, kde_kws={'label':'Dead Celebrity'})
sns.distplot(male_n,hist=False, kde_kws={'label':'Expected Male'})
sns.distplot(female_n,hist=False, kde_kws={'label':'Expected Female'})
plt.yticks([])


# control for seemingly exponentially divergent relationship between fame score and frame b

# In[ ]:


frame['log_fame_score'] = np.log(frame.fame_score)


# In[ ]:


#sns.lmplot('age','log_fame_score',frame[frame.natural_causes==True])


# In[ ]:


frame.age.corr(frame.log_fame_score)


# We can therefore safely disgard the correlation between fame score and age

# Go on the attack and drop the missing causes of death

# In[ ]:


frame_cleaned = frame.dropna()


# In[ ]:


frame.head()


# In[ ]:


sns.distplot(frame.log_fame_score)
sns.distplot(frame_cleaned.log_fame_score)

