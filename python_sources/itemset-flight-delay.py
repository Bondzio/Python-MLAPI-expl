#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
pd.set_option('display.max_columns', None)  
pd.set_option('display.max_rows', None)  
# pd.set_option('display.', None)  
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import collections
import operator
import itertools
from functools import reduce
import re
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


airports_df = pd.read_csv('/kaggle/input/flight-delays/airports.csv')
airports_df.head()


# In[ ]:


flights_df = pd.read_csv('/kaggle/input/flight-delays/flights.csv')


# In[ ]:


flights_df.shape


# In[ ]:


flights_df.tail()


# ## Preprocessing

# ### Step 1) Relevant columns are filtered

# In[ ]:


my_flights_df = flights_df[['YEAR','MONTH','DAY','DAY_OF_WEEK','AIRLINE','FLIGHT_NUMBER','ORIGIN_AIRPORT','DESTINATION_AIRPORT',
                          'DEPARTURE_DELAY','ARRIVAL_DELAY','CANCELLED','DIVERTED']]
my_flights_df.tail()


# ### Step 2) Cancelled flights are removed

# In[ ]:


my_flights_df = my_flights_df[my_flights_df['CANCELLED']==0]


# In[ ]:


my_flights_df.shape


# ### Step 3) Diverted flights are removed

# In[ ]:


my_flights_df = my_flights_df[my_flights_df['DIVERTED']==0]


# ### Step 4) Less-than-zero delays are converted to zero

# In[ ]:


# we don't consider negative delay as delay, so we replace 0 for delays < 0.
my_flights_df['ARRIVAL_DELAY'][my_flights_df['ARRIVAL_DELAY']<0] = 0
my_flights_df['DEPARTURE_DELAY'][my_flights_df['DEPARTURE_DELAY']<0] = 0


# ### Step 5) Arrival delays and departure delays are combined

# In[ ]:


my_flights_df['DELAY'] = my_flights_df['ARRIVAL_DELAY'] + my_flights_df['DEPARTURE_DELAY']


# ### Step 6) Flights with no delay are removed

# In[ ]:


my_flights_df = my_flights_df[my_flights_df['DELAY']!=0]


# ### Step 7) 'Cancelled' and 'Diverted' columns are removed

# In[ ]:


# we see that these two columns are always zero in this resulting dataframe, so we drop them
my_flights_df = my_flights_df.drop(['CANCELLED','DIVERTED'], axis=1)


# ### Step 8) Destination and origin city and state of the flight is added

# In[ ]:


my_flights_df = my_flights_df.merge(airports_df, how='left',left_on='ORIGIN_AIRPORT', 
                                    right_on='IATA_CODE').drop(['IATA_CODE','AIRPORT','COUNTRY','LATITUDE','LONGITUDE'], axis=1)
my_flights_df = my_flights_df.rename({'CITY':'ORIGIN_CITY','STATE':'ORIGIN_STATE'}, axis=1)
my_flights_df = my_flights_df.merge(airports_df, how='left',left_on='DESTINATION_AIRPORT', 
                                    right_on='IATA_CODE').drop(['IATA_CODE','AIRPORT','COUNTRY','LATITUDE','LONGITUDE'], axis=1)
my_flights_df = my_flights_df.rename({'CITY':'DESTINATION_CITY','STATE':'DESTINATION_STATE'}, axis=1)
my_flights_df.head()


# ### Step 9) Null values are checked

# In[ ]:


my_flights_df.isnull().sum()


# ### Step 10) Flights with no origin/departure city are removed

# In[ ]:


# There are some airports that their city is not provided, we remove these rows too
my_flights_df = my_flights_df[~(my_flights_df['ORIGIN_CITY'].isnull() | my_flights_df['DESTINATION_CITY'].isnull())]


# ### Step 11) Interstate flights are removed

# In[ ]:


# to reduce the size of the dataset, only intrastate flights are condidered
my_flights_df = my_flights_df[my_flights_df['ORIGIN_STATE']!=my_flights_df['DESTINATION_STATE']]


# ### Step 12) "O_D" column is added

# In[ ]:


my_flights_df['O_D']= my_flights_df['ORIGIN_STATE']+'_'+my_flights_df['DESTINATION_STATE']


# In[ ]:


my_flights_df.shape


# In[ ]:





# ### Step 13) The size of the dataset is reduced

# In[ ]:


np.random.seed(10)
before_size = my_flights_df.shape[0]
# del_rate = 0.99
# remove_n = int(del_rate * my_flights_df.shape[0])
# remove_n = 10000
remainder = 4000
remove_n = before_size - remainder
drop_indices = np.random.choice(my_flights_df.index, remove_n, replace=False)
truncated_flights_df = my_flights_df.drop(drop_indices)
after_size = truncated_flights_df.shape[0]
print('size changed from {} to {}'.format(before_size, after_size))


# In[ ]:


truncated_flights_df.head()


# ## Some Plots

# In[ ]:


(my_flights_df['DESTINATION_STATE'].value_counts()+my_flights_df['ORIGIN_STATE'].value_counts()).sort_values(ascending=False).shape


# In[ ]:


(my_flights_df['DESTINATION_CITY'].value_counts()+my_flights_df['ORIGIN_CITY'].value_counts()).sort_values(ascending=False)[:100]


# In[ ]:


(my_flights_df['ORIGIN_STATE'].value_counts()+my_flights_df['DESTINATION_STATE'].value_counts()).plot(kind='bar', figsize=(15, 4), title='Origin State of the Flights')


# In[ ]:


my_flights_df['DESTINATION_STATE'].value_counts().plot(kind='bar', figsize=(15, 4), title='Destination State of the Flights')


# In[ ]:


my_flights_df['DESTINATION_CITY'].value_counts()[:50].plot(kind='bar', figsize=(15, 4), title='Destination City of the Flights (top 50)')


# In[ ]:


my_flights_df['ORIGIN_CITY'].value_counts()[:50].plot(kind='bar', figsize=(15, 4), title='Origin City of the Flights (top 50)')


# In[ ]:


(my_flights_df['DESTINATION_CITY'].value_counts()+my_flights_df['DESTINATION_CITY'].value_counts())[:50].plot(kind='bar', figsize=(15, 4), title='Involved Cities of the Delayed Flights (top 50)')
plt.ylabel('# of delayed flights')


# In[ ]:


my_flights_df.groupby('MONTH').count()['YEAR'].plot(kind='bar')
plt.ylabel('# delayed flights')
plt.title('# of delayed flights each month')


# In[ ]:


my_flights_df.groupby('DAY_OF_WEEK').count()['YEAR'].plot(kind='bar')
plt.ylabel('# delayed flights')
plt.title('# of delayed flights in different days of week')


# In[ ]:


my_flights_df.groupby('DAY').count()['YEAR'].plot(kind='bar')
plt.ylabel('# delayed flights')
plt.title('# of delayed flights in different days of month')


# In[ ]:


my_flights_df.head()


# In[ ]:


print('Here is top ten destination-origin pair flights')
print(my_flights_df['O_D'].value_counts()[:5])


# ## Saving the dataset

# In[ ]:


import os
os.chdir(r'/kaggle/working')
my_flights_df.to_csv(r'flights.csv')


# In[ ]:


from IPython.display import FileLink
FileLink(r'flights.csv')


# In[ ]:


my_flights_df.to_csv(r'flights_4000.csv')
FileLink(r'flights_4000.csv')


# ## Frequent itemset mining for the truncated dataset

# ### Making the dataset

# In[ ]:


# making the dataset
gp = truncated_flights_df.groupby('MONTH')
dataset = []
for i in list(truncated_flights_df['MONTH'].value_counts().sort_index().index):
    lst = (gp.get_group(i)['O_D']).tolist()
    dataset.append(lst)


# In[ ]:


# !pip install mlxtend


# In[ ]:


# from mlxtend.preprocessing import TransactionEncoder
# from mlxtend.frequent_patterns import fpgrowth
# from mlxtend.frequent_patterns import association_rules

# te = TransactionEncoder()
# te_ary = te.fit(dataset).transform(dataset)
# df = pd.DataFrame(te_ary, columns=te.columns_)
# res = fpgrowth(df, min_support=1, use_colnames=True)


# In[ ]:


# association_rules(res, metric="confidence", min_threshold=1)


# ### Extracting frequent itemsets and association rules

# In[ ]:


get_ipython().system('pip install efficient-apriori')


# In[ ]:


from efficient_apriori import apriori
itemsets, rules = apriori(dataset, min_support=1,  min_confidence=1)


# note that itemsets is in the format of:  
# {1: {('a',): 3, ('b',): 2, ('c',): 1},  
#     ...             2: {('a', 'b'): 2, ('a', 'c'): 1}}  

# ### Putting all itemsets in a list

# In[ ]:


my_itemsets_dicts = []
for i in range(1, len(itemsets)):
  my_itemsets_dicts.append(itemsets[i])


# In[ ]:


my_itemsets = []
for d in my_itemsets_dicts:
  my_itemsets.append(list(d.keys()))
# flattening the list
my_itemsets = [item for sublist in my_itemsets for item in sublist]
print('There are {} frequent itemsets'.format(len(my_itemsets)))
print('There are {} rules'.format(len(rules)))


# ### Mining Maximal Itemsets

# In[ ]:


def is_power_of_two(n):
    """Returns True iff n is a power of two.  Assumes n > 0."""
    return (n & (n - 1)) == 0

def get_maximal_subsets(sequence_of_sets):
    """Return a list of the elements of `sequence_of_sets`, removing all
    elements that are subsets of other elements.  Assumes that each
    element is a set or frozenset and that no element is repeated."""
    # The code below does not handle the case of a sequence containing
    # only the empty set, so let's just handle all easy cases now.
    if len(sequence_of_sets) <= 1:
        return list(sequence_of_sets)
    # We need an indexable sequence so that we can use a bitmap to
    # represent each set.
    if not isinstance(sequence_of_sets, collections.Sequence):
        sequence_of_sets = list(sequence_of_sets)
    # For each element, construct the list of all sets containing that
    # element.
    sets_containing_element = {}
    for i, s in enumerate(sequence_of_sets):
        for element in s:
            try:
                sets_containing_element[element] |= 1 << i
            except KeyError:
                sets_containing_element[element] = 1 << i
    # For each set, if the intersection of all of the lists in which it is
    # contained has length != 1, this set can be eliminated.
    out = [s for s in sequence_of_sets
           if s and is_power_of_two(reduce(
               operator.and_, (sets_containing_element[x] for x in s)))]
    return out


# In[ ]:


maximal_itemsets = get_maximal_subsets(my_itemsets)
print('There are {} maximal frequent itemsets'.format(len(maximal_itemsets)))


# In[ ]:


maximal_itemsets[-10:]


# In[ ]:


maximal_itemsets[0]


# ## Bootstrap Sampling for Confidence Interval

# In[ ]:


def get_sample(data_df, size):
    """
    provides a bootstrap sample of the dataset

    Parameters
    ----------
    data_df : DataFrame
        dataset that the sample is drawn from
    size : Integer
        size of the sample
    """
    chosen_indices = np.random.choice(data_df.index, size, replace=True)
    sample_flights_df = my_flights_df.loc[chosen_indices]
    return sample_flights_df


# In[ ]:


def convert_df_to_dataset(data_df):
    """
    Converts a DataFrame to a list of baskets, the baskets are months and the items are the fligths

    Parameters
    ----------
    data_df : DataFrame
        dataframe to be converted to the dataset
    """
    gp = data_df.groupby('MONTH')
    dataset = []
    for i in list(data_df['MONTH'].value_counts().sort_index().index):
        lst = (gp.get_group(i)['O_D']).tolist()
        dataset.append(lst)
    return dataset


# In[ ]:


def compute_rsupport(sample_dataset, pattern):
    """
    computes the support of a pattern in the given dataset

    Parameters
    ----------
    sample_df : List
        sample dataset that is a list of baskets
    pattern : Tuple
        pattern to be found
    """
    support = 0
    for item in sample_dataset:
        if set(pattern).issubset(item):
            support = support + 1
    return support/len(sample_dataset)


# In[ ]:


def get_lower_bound(cumlative_dist, lower_bound_index):
    lower_bound = 0
    for item in cumlative_dist:
        if item < lower_bound_index:
            continue
        lower_bound = cumlative_dist[cumlative_dist == item].index[0]
        break
    return lower_bound


# In[ ]:


def get_upper_bound(cumlative_dist, upper_bound_index):
    upper_bound = 0
    for item in cumlative_dist.sort_values(ascending=False):
        if item > upper_bound_index:
            continue
        upper_bound = cumlative_dist[cumlative_dist == item].index[0]
        break
    return upper_bound


# In[ ]:


def get_rsupport_bound(dataset_df, pattern, k=50, n =2000, alpha=0.99):
    lower_bound_index = (1-alpha)/2
    upper_bound_index = (1+alpha)/2
    rsupport = []
    for i in range(k):
        sample_df = get_sample(dataset_df, n)
        sample_dataset = convert_df_to_dataset(sample_df)  
        rsupport.append(compute_rsupport(sample_dataset, pattern))

    cumlative_dist = (1/k) * np.cumsum(pd.Series(rsupport).value_counts().sort_index())
    rsup_bound = get_lower_bound(cumlative_dist, lower_bound_index), get_upper_bound(cumlative_dist, upper_bound_index)
    return rsup_bound


# In[ ]:


get_rsupport_bound(my_flights_df, maximal_itemsets[0], k=500, n=2000)


# In[ ]:


bounds = []
for itemset in maximal_itemsets[:20]:
    bounds.append((itemset,get_rsupport_bound(my_flights_df, itemset, n=5000)))


# In[ ]:


# taking itemsets with the highest mean bounds
item_mean_bound = {}
for item in bounds:
    item_mean_bound.update({item[0]: 0.5*(item[1][0]+ item[1][1])})
# sorting the dictionary
item_mean_bound = {k: v for k, v in sorted(item_mean_bound.items(), key=lambda item: item[1], reverse=True)}
dict(itertools.islice(item_mean_bound.items(), 10))


# # Finding Influential Flights
# flights that appear alone at the right side of frequent association rules and the left side has the maximum (7) number of flights

# In[ ]:


rhs_lens = []
for rule in rules:
    rhs_lens.append(len(rule.rhs))
max_consequent = np.max(rhs_lens)


# In[ ]:


influential_rules = []
for rule in rules:
    if len(rule.lhs) == 1 and len(rule.rhs) == max_consequent:
        influential_rules.append(rule)
print('There are {} influential rules'.format(len(influential_rules)))
influential_rules[:10]


# In[ ]:


influential_flights = []
for rule in influential_rules:
    influential_flights.append(rule.rhs)
influential_flights = np.unique(influential_flights)
print('There are {} influential flights'.format(len(influential_flights)))
influential_flights


# ## Influential States
# the most common states in the influential flights are influential states

# In[ ]:


influential_states = []
states = []
flatten = lambda l: [item for sublist in l for item in sublist]
for flight in influential_flights:
    states.append(re.split("_", flight))
states = flatten(states)
# finding top 5 
pd.Series(states).value_counts()[:5]


# In[ ]:


pd.Series(states).value_counts()[:5].index

