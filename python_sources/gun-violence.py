#!/usr/bin/env python
# coding: utf-8

# ### Gun-Violence incidents and few insights

# In[ ]:


# Import all the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from plotly.offline  import download_plotlyjs,init_notebook_mode,plot, iplot
import cufflinks as cf
init_notebook_mode(connected = True)
cf.go_offline()


# In[ ]:


# Read the file into a dataframe
df = pd.read_csv('..//input//gun-violence-data_01-2013_03-2018.csv')


# In[ ]:


df.columns


# In[ ]:


df.state.value_counts().iplot(kind = 'bar', theme = 'solar', title = 'STATES AND NUMBER OF INCIDENTS')


# In[ ]:


df.city_or_county.value_counts().head(10).iplot(kind = 'bar', theme = 'solar', title = 'TOP 10 Cities highest incidents happend')


# In[ ]:


temp = df[['state', 'n_killed']].reset_index(drop=True)
temp = temp.groupby('state').sum()
temp.iplot(kind = 'bar',  theme = 'solar', title = 'States and Number of persons killed')


# In[ ]:


#Maximum number of people killed in a single incident 
df[df.n_killed> 20][['state','n_killed']].reset_index(drop =True)


# In[ ]:


df[df['n_killed'] == max(df['n_killed'])]


# In[ ]:


df[df['n_injured'] == max(df['n_injured'])]


# #### Get the number of people involved in each incident. 

# In[ ]:


def truncate(a):
    a = a.split('||')
    a  = [x.replace('::','-') for x in a]
    a =  [(x.split('-')) for x in a]
    y = []
    for  i in range (0, len(a)):
        y.append(a[i][-1])
    return(y)  
change = lambda x: truncate(x)
df['participant_gender'] = df['participant_gender'].fillna("0::Zero")
df['People'] = df['participant_gender'].apply(change)


# ####  Make Males, Females count

# In[ ]:


def count_male (a):
    return(a.count('Male'))
def count_female (a):
    return(a.count('Female'))
check_male = lambda x: count_male(x)
check_female = lambda y: count_female(y)
df['Males'] = df['People'].apply(check_male)
df['Females'] = df['People'].apply(check_female)
df['People_count'] = df['Males'] + df['Females']


# In[ ]:


df[['state', 'Males', 'Females']].groupby('state').sum().iplot(kind = 'line' )


# #### Age and the Crime relationship.

# In[ ]:





# In[ ]:


def modify(x):
    x = str(x)
    x = x.replace("::", ":")
    x = x.replace('||', '|')
    x = x.split('|')
    x  = [t.replace(':','-') for t in x]
    a =  [(t.split('-')) for t in x]
    y = []
    for  i in range (0, len(a)):
        y.append(int(max(a[i])))
    return y
def min_age(x):
    return(min(x))
def max_age(x):
    return(max(x))
simplify = lambda x: modify(x)    
df['participant_age'] = df['participant_age'].fillna("0::0")
df['Ages'] = df['participant_age'].apply(simplify)
df['Ages']
df['Min_Age'] = df['Ages'].apply(lambda x: min_age(x))
df['Max_Age'] = df['Ages'].apply(lambda x: max_age(x))
incident_age = df[['incident_id', 'Max_Age', 'Min_Age']]
incident_age ['Max_Age'] > 0


# In[ ]:


import seaborn as sns
x = incident_age.Min_Age
sns.distplot(x)


# ## Observations : 
# 1.  Illinoise State had the highest  Incidents.  17556 incidents.
# 2. Chicago City had the highest Incidents . 10814 incident
# 3. California and Texas States are highest in number of people killed in the incidents. ( 5562, 5046)
# 4. Top Two single incidents where highest number of people  killed, occured in  Florida( 50 killed) ,  Texas(27 killed)
# 5.  One single Incident ID = 577157 where maximum number of people injured (53 ) and maximum number people killed(50) -- This need further exploration
# 6.  Every Incident More number of Males involved compared to Females. 

# In[ ]:





# In[ ]:




