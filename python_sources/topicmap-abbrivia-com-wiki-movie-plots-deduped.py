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


nRowsRead = None # specify 'None' if want to read whole file
# Names-from-35k-WikipediaMoviePlots-Abbrivia.com-CC-BY-SA-4.0.csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df = pd.read_csv('/kaggle/input/wikipedia-movie-plots/wiki_movie_plots_deduped.csv', delimiter=',', nrows = nRowsRead, low_memory=False)
#df.dataframeName = 'Names-from-35k-WikipediaMoviePlots-Abbrivia.com-CC-BY-SA-4.0.csv'
nRow, nCol = df.shape
print(f'There are {nRow} rows and {nCol} columns')


# In[ ]:


print(df.columns)


# In[ ]:


dataset_name='wiki_movie_plots_deduped'
writer = pd.ExcelWriter('Abbrivia.com-'+dataset_name+'.xlsx', engine='xlsxwriter')
df[['Title', 'Plot']].to_excel(writer, sheet_name=('Abbrivia.com-'+dataset_name)[0:30], index = True)
writer.save()

