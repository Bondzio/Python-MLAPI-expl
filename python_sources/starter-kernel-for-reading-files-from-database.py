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


# **Line list of public cases (COVID-19) out of Canada**
# 
# Citation:
# COVID-19 Canada Open Data Working Group. Epidemiological Data from the COVID-19 Outbreak in Canada. https://github.com/ishaberry/Covid19Canada.
# 

# In[ ]:


covid19_canada = pd.ExcelFile('/kaggle/input/coronawhy/Public_COVID-19_Canada.xlsx')


# In[ ]:


print("No. of tables in file: ", len(covid19_canada.sheet_names))
print("Table Names(Sheets): ", covid19_canada.sheet_names)


# In[ ]:


cases = pd.read_excel(covid19_canada, sheet_name='Cases')
print(cases.shape)
cases.head()


# In[ ]:


mortality = pd.read_excel(covid19_canada, sheet_name='Mortality')
print(mortality.shape)
mortality.head()


# In[ ]:


recovered = pd.read_excel(covid19_canada, sheet_name='Recovered')
print(recovered.shape)
recovered.columns


# In[ ]:


# Read each of the files & display details
UN_population = pd.read_csv('/kaggle/input/coronawhy/UN-population-projection-medium-variant.csv')
print(UN_population.shape)
UN_population.head()


# In[ ]:


covid_title_abstract = pd.read_csv('/kaggle/input/coronawhy/covid_TitleAbstract_processed-20200325.csv')
print(covid_title_abstract.shape)
covid_title_abstract.head()


# In[ ]:


contact_Info = pd.read_excel('/kaggle/input/coronawhy/CleanedEmails_v2.xlsx')
print(contact_Info.shape)
contact_Info.head()

