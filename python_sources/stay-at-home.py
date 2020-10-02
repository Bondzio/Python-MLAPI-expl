#!/usr/bin/env python
# coding: utf-8

# ## Task : Which populations assessed should stay home and which should see an HCP?
# 
# In this notebook I try to find the effect of age and certain illnesses when looking at the number deaths and hospitalized people. 

# In[ ]:


# Library import
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns # plot library for statistics
import matplotlib.pyplot as plt # plot library
from scipy.stats import norm # normal distribution statistics tools


# First, we look at data in Ontario where we have the number of ventilators used in hospital for covid-19 patients. Serious cases of Covid-19 may not require a ventilator but those that require a ventilator are most definitely serious cases.
# The dataset is not so big hence to get a good idea, we estimate the proportion of patients that needed ventilator as well as a confidence interval around this estimated value (normal asymptotic confidence interval).

# In[ ]:


df_icu = pd.read_csv('/kaggle/input/uncover/UNCOVER/howsmyflattening/ontario-icu-capacity.csv')
n=len(df_icu)
# There are two classes of covid-patients : the patients tested positive and the patients suspected for covid.
p_vent = np.mean(df_icu['confirmed_positive_ventilator']/df_icu['confirmed_positive'])
sd_vent = np.std(df_icu['confirmed_positive_ventilator']/df_icu['confirmed_positive'])
IC=[p_vent-norm.ppf(0.975)*sd_vent/np.sqrt(n),p_vent+norm.ppf(0.975)*sd_vent/np.sqrt(n)]

print('There is a mean proportion of patient that needed ventilator among tested positive of  %4.2f,'
     ' with 95 percent confidence interval of [%4.2f, %4.2f]' % (p_vent, IC[0], IC[1]) )

# Same for patients with suspected covid
p_vent = np.mean(df_icu['suspected_covid_ventilator']/df_icu['suspected_covid'])
sd_vent = np.std(df_icu['suspected_covid_ventilator']/df_icu['suspected_covid'])

IC=[p_vent-norm.ppf(0.975)*sd_vent/np.sqrt(n),p_vent+norm.ppf(0.975)*sd_vent/np.sqrt(n)]

print('There is a mean proportion of patient that needed ventilator among suspected covid of  %4.2f,'
     ' with 95 percent confidence interval of [%4.2f, %4.2f]' % (p_vent, IC[0], IC[1]) )


# As expected the number of ventilator needed for suspected covid is smaller than for those tested positive most probably because the suspected covid can either not have covid or have mild case of covid that did not warrent a test at places where we lack testing capacity.
# Next, let us study the effect of different factors (illnesses and age) for this question.

# In[ ]:


# dictionary of abbreviations for us-states as different database use abbreviation.
dict_states={'AL': 'ALABAMA','AK': 'ALASKA','AZ': 'ARIZONA','AR': 'ARKANSAS','CA': 'CALIFORNIA','CO': 'COLORADO','CT': 'CONNECTICUT',
             'DE': 'DELAWARE','FL': 'FLORIDA','GA': 'GEORGIA','HI': 'HAWAII','ID': 'IDAHO','IL': 'ILLINOIS','IN': 'INDIANA','IA': 'IOWA',
             'KS': 'KANSAS','KY': 'KENTUCKY','LA': 'LOUISIANA','ME': 'MAINE','MD': 'MARYLAND','MA': 'MASSACHUSETTS','MI': 'MICHIGAN',
             'MN': 'MINNESOTA','MS': 'MISSISSIPPI','MO': 'MISSOURI','MT': 'MONTANA','NE': 'NEBRASKA','NV': 'NEVADA','NH': 'NEW HAMPSHIRE',
             'NJ': 'NEW JERSEY','NM': 'NEW MEXICO','NY': 'NEW YORK','NC': 'NORTH CAROLINA','ND': 'NORTH DAKOTA','OH': 'OHIO','OK': 'OKLAHOMA',
             'OR': 'OREGON', 'PA': 'PENNSYLVANIA','RI': 'RHODE ISLAND','SC': 'SOUTH CAROLINA','SD': 'SOUTH DAKOTA','TN': 'TENNESSEE','TX': 'TEXAS',
             'UT': 'UTAH','VT': 'VERMONT','VA': 'VIRGINIA','WA': 'WASHINGTON','WV': 'WEST VIRGINIA','WI': 'WISCONSIN','WY': 'WYOMING','DC': 'COLUMBIA'}


# We use three different datasets, all giving statistics for US states. 
# * The dataset from "covid_tracking_project" gives us the number of death and hospitalized people.
# * The dataset from "esri_covid-19" give us information about age in each state.
# * The dataset from "us_cdc" give us information about illnesses in each state.

# In[ ]:


# Import the dataset.
df_statistics = pd.read_csv('/kaggle/input/uncover/UNCOVER/covid_tracking_project/covid-statistics-by-us-states-totals.csv')
# Replace state abbreviation with the name of the state.
df_statistics = df_statistics.replace({"state": dict_states})
# Select features in the dataset.
df_statistics = df_statistics[['state','positive','hospitalized','death']]
df_statistics= df_statistics.set_index('state').sort_index()

# Import the dataset. Dataset taken from https://worldpopulationreview.com/states/median-age-by-state/ giving median age and population by state in the us.
df_age = pd.read_csv("/kaggle/input/median-age-and-pop-us-by-state/median_age.csv", index_col=0)
df_age= df_age.set_index('state').sort_index()

# Import the dataset.
df_illness = pd.read_csv('/kaggle/input/uncover/UNCOVER/us_cdc/us_cdc/500-cities-census-tract-level-data-gis-friendly-format-2019-release.csv')
# Select features in the dataset.
illnesses=['bphigh_crudeprev',"bpmed_crudeprev", "cancer_crudeprev" ,"csmoking_crudeprev",
                         "diabetes_crudeprev","stroke_crudeprev","kidney_crudeprev","obesity_crudeprev"]
df_illness = df_illness[["stateabbr"]+illnesses]
# Replace states abbreviation with the name of the state.
df_illness = df_illness.replace({"stateabbr": dict_states})
# aggregate the statistics for each states as is tract-level.
df_illness = df_illness.groupby(['stateabbr']).sum()

# Concatenate the three datasets in one.
df=pd.concat([df_statistics,df_illness,df_age], axis=1)


# ### Preprocessing of the data

# In[ ]:


#drop states with missing data.
df = df.dropna(axis=0)
# display the beginning of the dataset
df.head()


# We want to compare states and as such we have to take into account the difference in population. 

# In[ ]:


# Change the data into proportions.

df[['hospitalized','death']] = df[['hospitalized','death']].div(df['positive'], axis=0)
df=df.drop(['positive'], axis=1)

df[illnesses] = df[illnesses].div(df['Population'], axis=0)
df=df.drop(['Population'], axis=1)


# In[ ]:


# Visualization of the correlations
df.corr().style.background_gradient()


# Finally, we plot the couple (hospitalized,death) with a color depending on the feature for the features that can be the age or illnesses. 

# In[ ]:


f, axes = plt.subplots(3, 3, figsize=(18, 11), sharex=True, sharey=True)
cmap = sns.cubehelix_palette(dark=.2, light=.7, as_cmap=True)

for f in range(9):
    sns.scatterplot(x="hospitalized", y="death",size=df.columns[f+2],
                    hue=df.columns[f+2], data=df,ax=axes.ravel()[f],sizes=(50, 200),palette=cmap, legend=False)
    axes.ravel()[f].set_title('plot for '+df.columns[f+2])
plt.tight_layout()


# As expected the number of hospitalized people is correlated with the number of death.

# In[ ]:




