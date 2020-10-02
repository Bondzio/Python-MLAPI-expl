#!/usr/bin/env python
# coding: utf-8

# https://www.kaggle.com/roche-data-science-coalition/uncover

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # Understanding the Data

# In[ ]:


csv_list = []
for dirname, _, filenames in os.walk('/kaggle/input/uncover/UNCOVER_v4'):
    for filename in filenames:
        input_file = os.path.join(dirname, filename)
        ext = os.path.splitext(input_file)[-1]
        if ext == '.csv':
            csv_list.append(input_file)
            print(input_file)
            df = pd.read_csv(input_file, low_memory=False)
            print(df.columns)


# # Task 1: Which populations are at risk of contracting COVID-19?
# 
# In this task, we want to find out what population could catch COVID-19. We can approach this problem by first looking at the confirmed cases population.
# 
# Dataset with Confirmed Cases and Population Data:
# * /kaggle/input/uncover/UNCOVER_v4/UNCOVER/ontario_government/confirmed-positive-cases-of-covid-19-in-ontario.csv
# * /kaggle/input/uncover/UNCOVER_v4/UNCOVER/worldometer/worldometer-confirmed-cases-and-deaths-by-country-territory-or-conveyance.csv
# * /kaggle/input/uncover/UNCOVER_v4/UNCOVER/our_world_in_data/coronavirus-disease-covid-19-statistics-and-research.csv
# 
# Dataset with Confirmed Cases:
# * /kaggle/input/uncover/UNCOVER_v4/UNCOVER/public_health_england/covid-19-daily-confirmed-cases.csv
# * /kaggle/input/uncover/UNCOVER_v4/UNCOVER/USAFacts/confirmed-covid-19-cases-in-us-by-state-and-county.csv
# * /kaggle/input/uncover/UNCOVER_v4/UNCOVER/worldometer/worldometer-confirmed-cases-and-deaths-by-country-territory-or-conveyance.csv
# 
# 
# 
# 
# 

# Let's look at the Ontario Dataset

# In[ ]:


ont_df = pd.read_csv('/kaggle/input/uncover/UNCOVER_v4/UNCOVER/ontario_government/confirmed-positive-cases-of-covid-19-in-ontario.csv')
print('Number of Cases:', len(ont_df))
print(ont_df.head())


# From the column headers, two columns seem to be population related.
# 1. age_group
# 2. client_gender
# 

# In[ ]:


ont_df['age_group'].value_counts().plot(kind='barh', title='Age')


# In[ ]:


ont_df['client_gender'].value_counts().plot(kind='barh', title='Gender')


# From the plots, 40s and 50s female seems to be high risk population.

# Let's look at the worldometer dataset

# In[ ]:


wor_df = pd.read_csv('/kaggle/input/uncover/UNCOVER_v4/UNCOVER/worldometer/worldometer-confirmed-cases-and-deaths-by-country-territory-or-conveyance.csv')
print('Number of Countries:', len(wor_df))
print(wor_df.head())


# Seems like five columns could be informative.
# 1. total_cases
# 2. new_cases
# 3. active_cases
# 4. total_cases_per_1m_pop
# 5. total_tests_per_1m_pop
# 
# Column sl_no depicts whether each row is a country, so we'll filter by that first.

# In[ ]:


bool_country = wor_df['sl_no'] > 0
print(wor_df[bool_country].head())


# Let's look at the ratio between confirmed cases and tested cases. We'll ignore countries with missing data.

# In[ ]:


bool_tot_cases_1m = wor_df['total_cases_per_1m_pop'] >= 0
bool_tot_test_1m = wor_df['total_tests_per_1m_pop'] >= 0


wor_df['percent_confirmed'] = wor_df['total_cases_per_1m_pop'].div(wor_df['total_tests_per_1m_pop'])
bool_le = wor_df['total_cases_per_1m_pop'].le(wor_df['total_tests_per_1m_pop'])

wor_df[bool_country & bool_tot_cases_1m & bool_tot_test_1m & bool_le].sort_values(by='percent_confirmed',axis=0).plot.barh(x='country', y=['total_cases_per_1m_pop', 'total_tests_per_1m_pop', 'percent_confirmed'],
                                                                      figsize=(10,100), logx=True, title='Total Cases/ Test Cases (1M) (log)').legend(loc='upper right')


# Looks like South America, Africa, and Middle East countries have more confirmed cases.

# Let's look at at the our_world_in_data

# In[ ]:


our_df = pd.read_csv('/kaggle/input/uncover/UNCOVER_v4/UNCOVER/our_world_in_data/coronavirus-disease-covid-19-statistics-and-research (1).csv')
print(our_df.head())
countries = our_df['location'].unique()
print(countries)
print('Number of Countries:', len(countries))


# Let's look at different locations.
# * International: most features are NaN
# * World: features are constant over time
# 
# Let's look at each location at 2020-05-21.
# * Some features are all Nan, let's drop them
# * Some features are NaN, let's replace them with column mean
# 
# 
# 

# In[ ]:


#bool_loc = our_df['location'] == 'World'
#print(our_df[bool_loc])

bool_date = our_df['date'] == '2020-05-21'
#print(our_df[bool_date])

our_df_0521 = our_df[bool_date]

bool_all_nan = our_df_0521.isna().all()
all_nan_features = our_df.columns[bool_all_nan]
our_df_0521 = our_df_0521.drop(labels=all_nan_features, axis=1)

bool_nan = our_df_0521.isna().any()
nan_features = our_df_0521.columns[bool_nan]

for feature in nan_features:
    mean_val = our_df_0521[feature].mean()
    our_df_0521[feature] = our_df_0521[feature].fillna(mean_val)

print(our_df_0521.isna().any())


# If we look at total_cases_per_million as Y, and use country-related features as X, we can build a regression model and find out which features might lead to more cases. Let's use sklearn's tutorial for finding out important fetures.
# 
# https://scikit-learn.org/stable/modules/feature_selection.html

# In[ ]:


from sklearn.feature_selection import VarianceThreshold
from scipy.stats import zscore

features = our_df_0521[['stringency_index', 'population_density', 'median_age', 'aged_65_older', 'aged_70_older',
                        'gdp_per_capita', 'extreme_poverty', 'cvd_death_rate', 'diabetes_prevalence', 'female_smokers',
                        'male_smokers', 'handwashing_facilities', 'hospital_beds_per_100k']]
target = our_df_0521['total_cases_per_million']

features_zscore = pd.DataFrame()
for column in features.columns:
    z = (features[column]-features[column].mean())/features[column].std(ddof=0)
    features_zscore[column] = z
    our_df_0521[column+'_z'] = z
    
target_zscore = (target-target.mean())/target.std(ddof=0)
our_df_0521['total_cases_per_million_z'] = target_zscore
# Variance Threshold
#sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
#sel.fit(features)
#print(features.columns[sel.get_support(indices=True)])

# Univariate
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression

sel = SelectKBest(f_regression, k=5)
sel.fit(features_zscore, target_zscore)
print(features.columns[sel.get_support(indices=True)])

# LASSO
from sklearn.linear_model import LassoCV
clf = LassoCV().fit(features_zscore, target_zscore)
importance = np.abs(clf.coef_)
print(clf.coef_)
print(features.columns[importance>0])

our_df_0521.plot.barh(figsize=(5,100), x='location', y=['aged_65_older_z', 'gdp_per_capita_z', 'total_cases_per_million_z'])


# From univariate, most features are interrelated (age-related). From LASSO we can conclude that high GDP and low <65 old are the two most predictive factors of catching COVID-19. Other factors include,
# 
# Positive Coefficients:
# * stringency_index
# * population_density
# * gdp_per_capita
# * female_smokers
# 
# Negative Coefficients:
# * aged_65_older
# * diabetes_prevalence
# 
# This result does not take into effect the longitudinal trend of num of cases.
# 

# # Summary
# * From the Ontario dataset, we see that females between 40s and 50s are higher risk.
# * From the Worldometer dataset, we see that South America, Africa, and Middle East have higher confirmed percentage.
# * From the Our_world_in_data, higher GDP and not too old population seems to be highly predictive of total_cases_per_million.  
