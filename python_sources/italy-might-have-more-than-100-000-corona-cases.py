#!/usr/bin/env python
# coding: utf-8

# ## Italy might have more than 100.000 corona cases
# 
# ### Italy might have a large number of unreported corona virus cases assuming the death rate in all countries is the same and observed differences stem in false negative cases. 
# 
# This script plots the countries with at least 100 validated cases of corona virus over time. Only dates are plotted with 30 cases or more. Further down the script compares the reported death rate between South Korea and Italy. While Italy currently reports death rates of around 6% South Korea reported a constant death rate below 1%. South Korea is testing vigorously and it can be assumed that it has a much lower false negative rate than Italy.
# 
# The resulting corrected case numbers for Italy are potentially 8 times higher than reported. This is making several assumptions that if not met would alter the result of this analysis.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


vtime = pd.read_csv("/kaggle/input/novel-corona-virus-2019-dataset/time_series_covid_19_confirmed.csv")
vtime


# In[ ]:


dtime = pd.read_csv("/kaggle/input/novel-corona-virus-2019-dataset/time_series_covid_19_deaths.csv")
dtime


# In[ ]:


ww = vtime.iloc[:,1]
ww[np.where(ww == "Iran (Islamic Republic of)")[0]] = "Iran"
ww[np.where(ww == "Republic of Korea")[0]] = "South Korea"
ww[np.where(ww == "Korea, South")[0]] = "South Korea"
ww[np.where(ww == "China")[0]] = "Mainland China"
ww[np.where(ww == "UK")[0]] = "United Kingdom"
ww[np.where(ww == "Viet Nam")[0]] = "Vietnam"
ww[np.where(ww == "Republic of Moldova")[0]] = "Moldova"
ww[np.where(ww == "Russian Federation")[0]] = "Russia"
uc = ww.unique()
uc.sort()


# In[ ]:


counter = 0

plt.figure(figsize=(20,45))
plt.tight_layout(pad=4.0, w_pad=4.0)

for country in uc:
    ma = np.where(ww == country)[0]
    country_count = vtime.iloc[ma, 4:].sum(axis=0)
    
    if np.max(country_count) > 100:
        sig_cases = np.where(country_count > 30)[0]
        counter = counter + 1
        plt.subplot(10,4,counter)
        plt.plot(country_count[sig_cases], 'r.-')
        #plt.plot(np.log(country_count))
        
        plt.xticks(rotation=90)
        plt.title(country)
        plt.ylabel("cases")

plt.subplots_adjust(left=0, right=1.3, top=1.3, bottom=0, hspace=0.5)
plt.show()


# In[ ]:


ma = np.where(ww == "Mainland China")[0]
china_count = vtime.iloc[ma, 4:].sum(axis=0)

country_count = vtime.iloc[:, 4:].sum(axis=0)
plt.figure(figsize=(20,10))
res1, = plt.plot(country_count, 'b.-', label="Global")
res2, = plt.plot(china_count, 'r.-', label="Mainland China")
plt.title("Global Infections")
plt.ylabel("cases")
plt.xticks(rotation=90)
plt.legend(handles=[res1, res2])
plt.show()


# In[ ]:



country = "Italy"
ma = np.where(ww == country)[0]
country_count = vtime.iloc[ma, 4:].sum(axis=0)
country_deaths = dtime.iloc[ma, 4:].sum(axis=0)


sig_cases = np.where(country_count > 30)[0]

fig, ax1 = plt.subplots(figsize=(10,6))

plt.xticks(rotation=90)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'black'
ax1.set_xlabel('date')
ax1.set_ylabel('cases', color=color)
ax1.plot(country_count[sig_cases], 'b^-', label="Cases (Italy)")
ax2.plot(country_deaths[sig_cases], 'b^--', label="Deaths (Italy)")

ax1.tick_params(axis='y', labelcolor=color)


country = "South Korea"
ma = np.where(ww == country)[0]
country_count = vtime.iloc[ma, 4:].sum(axis=0)
country_deaths = dtime.iloc[ma, 4:].sum(axis=0)

color = 'green'
ax2.set_ylabel('deaths', color=color)  # we already handled the x-label with ax1
ax1.plot(country_count[sig_cases], 'ro-', label="Cases (South Korea)")
ax2.plot(country_deaths[sig_cases], 'ro--', label="Deaths (South Korea)")
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax1.legend(loc='upper left')
ax2.legend(loc='upper center')
plt.show()


# In[ ]:


country = "Italy"
ma = np.where(ww == country)[0]
country_count = vtime.iloc[ma, 4:].sum(axis=0)
country_deaths = dtime.iloc[ma, 4:].sum(axis=0)
dr_italy = country_deaths / country_count

d_cases = np.where(country_deaths > 3)[0]

country = "South Korea"
ma = np.where(ww == country)[0]
country_count = vtime.iloc[ma, 4:].sum(axis=0)
country_deaths = dtime.iloc[ma, 4:].sum(axis=0)
dr_korea = country_deaths / country_count

plt.figure(figsize=(10,6))
res1, = plt.plot(dr_italy[d_cases], 'b.-', label="Death rate (Italy)")
res2, = plt.plot(dr_korea[d_cases], 'r.-', label="Death rae (South Korea)")
plt.title("Death rates")
plt.ylabel("death rate")
plt.xticks(rotation=90)
plt.legend(handles=[res1, res2])
plt.show()


# ### Assuming that the death rate reported in South Korea is correct and we assume similar death rates in all countries we can correct the reported number of cases for Italy by using the observed differences in death rates
# 
# ### Assumptions
# 1. Death rates should be the same in all countries
# 2. Cases are generally under reported (there is a large number of false negative cases, this number depends on how thourougly the population is tested and there is no false positives)
# 3. The number of deaths attributed to corona virus have low false negative rates and no false positives
# 
# With these assumptions if there are significant differences in death rates it means there is a difference in false negative cases between countries. 

# In[ ]:


scaling_factor = dr_italy[d_cases] / dr_korea[d_cases]
country = "Italy"
ma = np.where(ww == country)[0]

country_count = vtime.iloc[ma, 4:].sum(axis=0)
country_deaths = dtime.iloc[ma, 4:].sum(axis=0)

potential_cases = country_count[d_cases] * scaling_factor

plt.figure(figsize=(10,6))
res1, = plt.plot(country_count[d_cases], 'bo-', label="Cases (Italy)")
res2, = plt.plot(potential_cases, 'ro-', label="Correct Cases (Italy)")
plt.title("Corrected case count by death rate")
plt.ylabel("cases")
plt.xticks(rotation=90)
plt.legend(handles=[res1, res2])
plt.show()

