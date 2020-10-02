#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
print(os.listdir("../input"))


# In[4]:


import warnings
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import pyplot as plt
import seaborn as sns
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
import calendar


# ## Read data

# In[5]:


train_df = pd.read_csv('../input/train_sessions.csv', index_col='session_id')


# In[6]:


times = ['time%s' % i for i in range(1, 11)]

train_df[times] = train_df[times].apply(pd.to_datetime)

train_df = train_df.sort_values(by='time1')


# In[7]:


y = train_df['target']


# In[8]:


train_df.head()


# In[9]:


y.head()


# ## Create time features

# In[10]:


unique_years = list(train_df['time1'].apply(lambda ts: ts.year).unique())
unique_years


# In[11]:


train_times = pd.DataFrame(index=train_df.index)

train_times['start_year'] = train_df['time1'].apply(lambda ts: unique_years.index(ts.year))

train_times['start_month'] = train_df['time1'].apply(lambda ts: ts.month)

train_times['start_day_of_week'] = train_df['time1'].apply(lambda ts: ts.weekday())

train_times['start_hour'] = train_df['time1'].apply(lambda ts: ts.hour)

train_times.head()


# ## OneHotEncoding

# In[12]:


ohe_times = OneHotEncoder([2, 12 + 1, 7, 24])

ohe_times.fit(train_times)


# In[13]:


ohe_train_times = ohe_times.transform(train_times)
ohe_train_times.shape


# ## Logistic regression feature importance

# In[14]:


logit = LogisticRegression(random_state=17)

logit.fit(ohe_train_times, y)


# In[15]:


def visualize_coefficients(classifier, feature_names, n_top_features=15):
    
    coef = classifier.coef_.ravel()
    positive_coefficients = np.argsort(coef)[-n_top_features:]
    negative_coefficients = np.argsort(coef)[:n_top_features]
    
    interesting_coefficients = np.hstack([negative_coefficients, positive_coefficients])
    
    plt.figure(figsize=(15, 5))
    
    colors = ["red" if c < 0 else "blue" for c in coef[interesting_coefficients]]
    
    plt.bar(np.arange(2 * n_top_features), coef[interesting_coefficients], color=colors)
    
    feature_names = np.array(feature_names)
    plt.xticks(np.arange(2 * n_top_features), feature_names[interesting_coefficients], rotation=90, ha="right")


# In[16]:


feature_values = {'start_year': unique_years,
                  'start_month': calendar.month_name,
                  'start_day_of_week': calendar.day_name,
                  'start_hour': [str(h) + 'h' for h in range(0, 24)]}

feature_names = []

for i,feature in enumerate(train_times.columns):
    a = ohe_times.feature_indices_[i]
    b = ohe_times.feature_indices_[i + 1]
    for j in range(a, b):
        k = j - a
        feature_names.append(feature_values[feature][k])


# In[17]:


visualize_coefficients(logit, feature_names, len(feature_names) // 2)


# ## Boruta Feature Selection

# To install Boruta using `pip` type:
# 
# ```
# pip3 install --user Boruta
# ```
# 
# or
# 
# ```
# sudo pip3 install Boruta
# ```

# In[1]:


from sklearn.ensemble import RandomForestClassifier
from boruta import BorutaPy


# In[2]:


random_forest = RandomForestClassifier(class_weight='balanced', max_depth=5, n_jobs=-1)


# In[18]:


feature_selector = BorutaPy(random_forest, n_estimators='auto', verbose=2, random_state=1)


# In[19]:


feature_selector.fit(ohe_train_times.toarray(), y)


# In[20]:


print('Total features:', ohe_train_times.shape[1])
print('Number of selected features:', feature_selector.n_features_)


# In[21]:


selected_features_names = [feature for i,feature in enumerate(feature_names) if feature_selector.support_[i]]
selected_features_names


# In[22]:


def visualize_coefficients_with_mask(classifier, feature_names, mask, n_top_features=15):
    
    coef = classifier.coef_.ravel()
    positive_coefficients = np.argsort(coef)[-n_top_features:]
    negative_coefficients = np.argsort(coef)[:n_top_features]
    
    interesting_coefficients = np.hstack([negative_coefficients, positive_coefficients])
    
    plt.figure(figsize=(15, 5))
    
    colors = ["black" if not m else "red" if c < 0 else "blue" for c,m in zip(coef[interesting_coefficients], mask[interesting_coefficients])]
    
    plt.bar(np.arange(2 * n_top_features), coef[interesting_coefficients], color=colors)
    
    feature_names = np.array(feature_names)
    plt.xticks(np.arange(2 * n_top_features), feature_names[interesting_coefficients], rotation=90, ha="right")


# In[23]:


visualize_coefficients_with_mask(logit, feature_names, feature_selector.support_, len(feature_names) // 2)


# On plot above features not selected by Boruta are black colored.

# In[ ]:




