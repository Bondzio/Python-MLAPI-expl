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


import numpy as np
import pandas as pd
import os
import json
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


train_df = pd.read_csv('../input/data-science-bowl-2019/train.csv')
train_df.head()


# In[ ]:


train_df.shape


# In[ ]:


test_df = pd.read_csv('../input/data-science-bowl-2019/test.csv')
test_df.head()


# In[ ]:


test_df.shape


# In[ ]:


train_labels_df = pd.read_csv('../input/data-science-bowl-2019/train_labels.csv')
train_labels_df.head()


# In[ ]:


train_labels_df.shape


# In[ ]:


specs_df = pd.read_csv('../input/data-science-bowl-2019/specs.csv')
pd.set_option('max_colwidth', 150)
specs_df.head()


# In[ ]:


specs_df.shape


# In[ ]:


sample_submission_df = pd.read_csv('../input/data-science-bowl-2019/sample_submission.csv')
sample_submission_df.head()


# In[ ]:


sample_submission_df.shape


# In[ ]:


print(f"train installation id: {train_df.installation_id.nunique()}")
print(f"test installation id: {test_df.installation_id.nunique()}")
print(f"test & submission installation ids identical: {set(test_df.installation_id.unique()) == set(sample_submission_df.installation_id.unique())}")


# We have 17K different installation_id in train and 1K in test sets

# ## **Missing values**

# In[ ]:


def missing_data(data):
    total = data.isnull().sum()
    percent = (data.isnull().sum()/data.isnull().count()*100)
    tt = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    types = []
    for col in data.columns:
        dtype = str(data[col].dtype)
        types.append(dtype)
    tt['Types'] = types
    return(np.transpose(tt))


# In[ ]:


missing_data(train_df)


# In[ ]:


missing_data(test_df)


# In[ ]:


missing_data(train_labels_df)


# In[ ]:


missing_data(specs_df)


# There are no missing values in the datasets.

# **Train & Test**

# In[ ]:


for column in train_df.columns.values:
    print(f"[train] Unique values of `{column}` : {train_df[column].nunique()}")


# In[ ]:


for column in test_df.columns.values:
    print(f"[test] Unique values of `{column}`: {test_df[column].nunique()}")


# In[ ]:


def plot_count(feature, title, df, size=1):
    f, ax = plt.subplots(1,1, figsize=(4*size,4))
    total = float(len(df))
    g = sns.countplot(df[feature], order = df[feature].value_counts().index[:20], palette='Set3')
    g.set_title("Number and percentage of {}".format(title))
    if(size > 2):
        plt.xticks(rotation=90, size=8)
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x()+p.get_width()/2.,
                height + 3,
                '{:1.2f}%'.format(100*height/total),
                ha="center") 
    plt.show()  


# In[ ]:


plot_count('title', 'title (first most frequent 20 values - train)', train_df, size=4)


# In[ ]:


plot_count('title', 'title (first most frequent 20 values - test)', test_df, size=4)


# In[ ]:


print(f"Title values (train): {train_df.title.nunique()}")
print(f"Title values (test): {test_df.title.nunique()}")


# In[ ]:


plot_count('type', 'type - train', train_df, size=2)


# In[ ]:


plot_count('type', 'type - test', test_df, size=2)


# In[ ]:


plot_count('world', 'world - train', train_df, size=2)


# In[ ]:


plot_count('world', 'world - test', test_df, size=2)


# In[ ]:


plot_count('event_code', 'event_code - test', train_df, size=4)


# In[ ]:


plot_count('event_code', 'event_code - test', test_df, size=4)


# **Train labels**

# In[ ]:


for column in train_labels_df.columns.values:
    print(f"[train_labels] Unique values of {column} : {train_labels_df[column].nunique()}")


# In[ ]:


plot_count('title', 'title - train_labels', train_labels_df, size=3)


# In[ ]:


plot_count('accuracy', 'accuracy - train_labels', train_labels_df, size=4)


# In[ ]:


plot_count('accuracy_group', 'accuracy_group - train_labels', train_labels_df, size=2)


# In[ ]:


plot_count('num_correct', 'num_correct - train_labels', train_labels_df, size=2)


# In[ ]:


plot_count('num_incorrect', 'num_incorrect - train_labels', train_labels_df, size=4)


# **Specs**

# In[ ]:


for column in specs_df.columns.values:
    print(f"[specs] Unique values of `{column}`: {specs_df[column].nunique()}")


# ## **Extract features from train/event_data**
# 
# We will parse a subset of train_df to extract features from event_data. We only extract data from 100K random sampled rows. This should be enough to get a good sample of the content.

# In[ ]:


sample_train_df = train_df.sample(100000)


# In[ ]:


sample_train_df.head()


# In[ ]:


sample_train_df.iloc[0].event_data


# In[ ]:


sample_train_df.iloc[1].event_data


# We use json package to normalize the json; we will create one column for each key; the value in the column will be the value associated to the key in the json. The extracted data columns will be quite sparse.

# In[ ]:


get_ipython().run_cell_magic('time', '', 'extracted_event_data = pd.io.json.json_normalize(sample_train_df.event_data.apply(json.loads))')


# In[ ]:


print(f"Extracted data shape: {extracted_event_data.shape}")


# In[ ]:


extracted_event_data.head(10)


# Let's check the statistics of the missing values in these columns.

# In[ ]:


missing_data(extracted_event_data)


# We modify the missing_data function to order the most frequent encountered event data features (newly created function called existing_data).

# In[ ]:


def existing_data(data):
    total = data.isnull().count() - data.isnull().sum()
    percent = 100 - (data.isnull().sum()/data.isnull().count()*100)
    tt = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    tt = pd.DataFrame(tt.reset_index())
    return(tt.sort_values(['Total'], ascending=False))


# In[ ]:


stat_event_data = existing_data(extracted_event_data)


# In[ ]:


plt.figure(figsize=(10, 10))
sns.set(style='whitegrid')
ax = sns.barplot(x='Percent', y='index', data=stat_event_data.head(40), color='blue')
plt.title('Most frequent features in event data')
plt.ylabel('Features')


# ordered by percent of existing data (descending).

# In[ ]:


stat_event_data[['index', 'Percent']].head(20)


# ## **Extract features from specs/args**

# In[ ]:


specs_df.args[0]


# In[ ]:


specs_args_extracted = pd.DataFrame()
for i in range(0, specs_df.shape[0]): 
    for arg_item in json.loads(specs_df.args[i]) :
        new_df = pd.DataFrame({'event_id': specs_df['event_id'][i],                               'info':specs_df['info'][i],                               'args_name': arg_item['name'],                               'args_type': arg_item['type'],                               'args_info': arg_item['info']}, index=[i])
        specs_args_extracted = specs_args_extracted.append(new_df)


# In[ ]:


print(f"Extracted args from specs: {specs_args_extracted.shape}")


# In[ ]:


specs_args_extracted.head(5)


# Let's see the distribution of the number of arguments for each event_id.

# In[ ]:


tmp = specs_args_extracted.groupby(['event_id'])['info'].count()
df = pd.DataFrame({'event_id':tmp.index, 'count': tmp.values})
plt.figure(figsize=(6,4))
sns.set(style='whitegrid')
ax = sns.distplot(df['count'],kde=True,hist=False, bins=40)
plt.title('Distribution of number of arguments per event_id')
plt.xlabel('Number of arguments'); plt.ylabel('Density'); plt.show()


# In[ ]:


plot_count('args_name', 'args_name (first 20 most frequent values) - specs', specs_args_extracted, size=4)


# In[ ]:


plot_count('args_type', 'args_type - specs', specs_args_extracted, size=3)


# In[ ]:


plot_count('args_info', 'args_info (first 20 most frequent values) - specs', specs_args_extracted, size=4)


# **Merged data distribution**
# 
# Let's merge train and train_labels.
# 
# We define a function to extract time features. We will apply this function for both train and test datasets.

# In[ ]:


def extract_time_features(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['month'] = df['timestamp'].dt.month
    df['hour'] = df['timestamp'].dt.hour
    df['year'] = df['timestamp'].dt.year
    df['dayofweek'] = df['timestamp'].dt.dayofweek
    df['weekofyear'] = df['timestamp'].dt.weekofyear
    df['dayofyear'] = df['timestamp'].dt.dayofyear
    df['quarter'] = df['timestamp'].dt.quarter
    df['is_month_start'] = df['timestamp'].dt.is_month_start
    return df


# In[ ]:


train_df = extract_time_features(train_df)


# In[ ]:


train_df.head()


# In[ ]:


plot_count('year', 'year - year', train_df, size=1)


# In[ ]:


plot_count('month', 'month - train', train_df, size=1)


# In[ ]:


plot_count('hour', 'hour -  train', train_df, size=4)


# In[ ]:


plot_count('dayofweek', 'dayofweek - train', train_df, size=2)


# In[ ]:


plot_count('weekofyear', 'weekofyear - train', train_df, size=2)


# In[ ]:


plot_count('is_month_start', 'is_month_start - train', train_df, size=1)


# Here we define the numerical columns and the categorical columns. We will use these to calculate the aggregated functions for the merge.

# In[ ]:


numerical_columns = ['game_time', 'month', 'dayofweek', 'hour']
categorical_columns = ['type', 'world']

comp_train_df = pd.DataFrame({'installation_id': train_df['installation_id'].unique()})
comp_train_df.set_index('installation_id', inplace = True)


# In[ ]:


def get_numeric_columns(df, column):
    df = df.groupby('installation_id').agg({f'{column}': ['mean', 'sum', 'min', 'max', 'std', 'skew']})
    df[column].fillna(df[column].mean(), inplace = True)
    df.columns = [f'{column}_mean', f'{column}_sum', f'{column}_min', f'{column}_max', f'{column}_std', f'{column}_skew']
    return df


# In[ ]:


for i in numerical_columns:
    comp_train_df = comp_train_df.merge(get_numeric_columns(train_df, i), left_index = True, right_index = True)


# In[ ]:


print(f"comp_train shape: {comp_train_df.shape}")


# In[ ]:


comp_train_df.head()


# In[ ]:


# get the mode of the title
labels_map = dict(train_labels_df.groupby('title')['accuracy_group'].agg(lambda x:x.value_counts().index[0]))
# merge target
labels = train_labels_df[['installation_id', 'title', 'accuracy_group']]
# replace title with the mode
labels['title'] = labels['title'].map(labels_map)
# join train with labels
comp_train_df = labels.merge(comp_train_df, on = 'installation_id', how = 'left')
print('We have {} training rows'.format(comp_train_df.shape[0]))


# In[ ]:


comp_train_df.head()


# In[ ]:


print(f"comp_train_df shape: {comp_train_df.shape}")
for feature in comp_train_df.columns.values[3:20]:
    print(f"{feature} unique values: {comp_train_df[feature].nunique()}")


# In[ ]:


plot_count('title', 'title - compound train', comp_train_df)


# In[ ]:


plot_count('accuracy_group', 'accuracy_group - compound train', comp_train_df, size=2)


# In[ ]:


plt.figure(figsize=(16,6))
_titles = comp_train_df.title.unique()
plt.title("Distribution of log(`game time mean`) values (grouped by title) in the comp train")
for _title in _titles:
    red_comp_train_df = comp_train_df.loc[comp_train_df.title == _title]
    sns.distplot(np.log(red_comp_train_df['game_time_mean']), kde=True, label=f'title: {_title}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_titles = comp_train_df.title.unique()
plt.title("Distribution of log(`game time std`) values (grouped by title) in the comp train")
for _title in _titles:
    red_comp_train_df = comp_train_df.loc[comp_train_df.title == _title]
    sns.distplot(np.log(red_comp_train_df['game_time_std']), kde=True, label=f'title: {_title}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_titles = comp_train_df.title.unique()
plt.title("Distribution of `game time skew` values (grouped by title) in the comp train")
for _title in _titles:
    red_comp_train_df = comp_train_df.loc[comp_train_df.title == _title]
    sns.distplot(red_comp_train_df['game_time_skew'], kde=True, label=f'title: {_title}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_titles = comp_train_df.title.unique()
plt.title("Distribution of `hour mean` values (grouped by title) in the comp train")
for _title in _titles:
    red_comp_train_df = comp_train_df.loc[comp_train_df.title == _title]
    sns.distplot(red_comp_train_df['hour_mean'], kde=True, label=f'title: {_title}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_titles = comp_train_df.title.unique()
plt.title("Distribution of `hour std` values (grouped by title) in the comp train")
for _title in _titles:
    red_comp_train_df = comp_train_df.loc[comp_train_df.title == _title]
    sns.distplot(red_comp_train_df['hour_std'], kde=True, label=f'title: {_title}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_titles = comp_train_df.title.unique()
plt.title("Distribution of `hour skew` values (grouped by title) in the comp train")
for _title in _titles:
    red_comp_train_df = comp_train_df.loc[comp_train_df.title == _title]
    sns.distplot(red_comp_train_df['hour_skew'], kde=True, label=f'title: {_title}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_titles = comp_train_df.title.unique()
plt.title("Distribution of `month mean` values (grouped by title) in the comp train")
for _title in _titles:
    red_comp_train_df = comp_train_df.loc[comp_train_df.title == _title]
    sns.distplot(red_comp_train_df['month_mean'], kde=True, label=f'title: {_title}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_titles = comp_train_df.title.unique()
plt.title("Distribution of `month std` values (grouped by title) in the comp train")
for _title in _titles:
    red_comp_train_df = comp_train_df.loc[comp_train_df.title == _title]
    sns.distplot(red_comp_train_df['month_std'], kde=True, label=f'title: {_title}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_titles = comp_train_df.title.unique()
plt.title("Distribution of `month skew` values (grouped by title) in the comp train")
for _title in _titles:
    red_comp_train_df = comp_train_df.loc[comp_train_df.title == _title]
    sns.distplot(red_comp_train_df['month_skew'], kde=True, label=f'title: {_title}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_accuracy_groups = comp_train_df.accuracy_group.unique()
plt.title("Distribution of log(`game time mean`) values (grouped by accuracy group) in the comp train")
for _accuracy_group in _accuracy_groups:
    red_comp_train_df = comp_train_df.loc[comp_train_df.accuracy_group == _accuracy_group]
    sns.distplot(np.log(red_comp_train_df['game_time_mean']), kde=True, label=f'accuracy group= {_accuracy_group}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_accuracy_groups = comp_train_df.accuracy_group.unique()
plt.title("Distribution of log(`game time std`) values (grouped by accuracy group) in the comp train")
for _accuracy_group in _accuracy_groups:
    red_comp_train_df = comp_train_df.loc[comp_train_df.accuracy_group == _accuracy_group]
    sns.distplot(np.log(red_comp_train_df['game_time_std']), kde=True, label=f'accuracy group= {_accuracy_group}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_accuracy_groups = comp_train_df.accuracy_group.unique()
plt.title("Distribution of `game time skew` values (grouped by accuracy group) in the comp train")
for _accuracy_group in _accuracy_groups:
    red_comp_train_df = comp_train_df.loc[comp_train_df.accuracy_group == _accuracy_group]
    sns.distplot(red_comp_train_df['game_time_skew'], kde=True, label=f'accuracy group= {_accuracy_group}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_accuracy_groups = comp_train_df.accuracy_group.unique()
plt.title("Distribution of `hour mean` values (grouped by accuracy group) in the comp train")
for _accuracy_group in _accuracy_groups:
    red_comp_train_df = comp_train_df.loc[comp_train_df.accuracy_group == _accuracy_group]
    sns.distplot(red_comp_train_df['hour_mean'], kde=True, label=f'accuracy group= {_accuracy_group}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_accuracy_groups = comp_train_df.accuracy_group.unique()
plt.title("Distribution of `hour std` values (grouped by accuracy group) in the comp train")
for _accuracy_group in _accuracy_groups:
    red_comp_train_df = comp_train_df.loc[comp_train_df.accuracy_group == _accuracy_group]
    sns.distplot(red_comp_train_df['hour_std'], kde=True, label=f'accuracy group= {_accuracy_group}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_accuracy_groups = comp_train_df.accuracy_group.unique()
plt.title("Distribution of `hour skew` values (grouped by accuracy group) in the comp train")
for _accuracy_group in _accuracy_groups:
    red_comp_train_df = comp_train_df.loc[comp_train_df.accuracy_group == _accuracy_group]
    sns.distplot(red_comp_train_df['hour_skew'], kde=True, label=f'accuracy group= {_accuracy_group}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_accuracy_groups = comp_train_df.accuracy_group.unique()
plt.title("Distribution of `month mean` values (grouped by accuracy group) in the comp train")
for _accuracy_group in _accuracy_groups:
    red_comp_train_df = comp_train_df.loc[comp_train_df.accuracy_group == _accuracy_group]
    sns.distplot(red_comp_train_df['month_mean'], kde=True, label=f'accuracy group= {_accuracy_group}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_accuracy_groups = comp_train_df.accuracy_group.unique()
plt.title("Distribution of `month std` values (grouped by accuracy group) in the comp train")
for _accuracy_group in _accuracy_groups:
    red_comp_train_df = comp_train_df.loc[comp_train_df.accuracy_group == _accuracy_group]
    sns.distplot(red_comp_train_df['month_std'], kde=True, label=f'accuracy group= {_accuracy_group}')
plt.legend()
plt.show()


# In[ ]:


plt.figure(figsize=(16,6))
_accuracy_groups = comp_train_df.accuracy_group.unique()
plt.title("Distribution of `month skew` values (grouped by accuracy group) in the comp train")
for _accuracy_group in _accuracy_groups:
    red_comp_train_df = comp_train_df.loc[comp_train_df.accuracy_group == _accuracy_group]
    sns.distplot(red_comp_train_df['month_skew'], kde=True, label=f'accuracy group= {_accuracy_group}')
plt.legend()
plt.show()


# In[ ]:


sample_submission_df['accuracy_group'].value_counts(normalize=True)

