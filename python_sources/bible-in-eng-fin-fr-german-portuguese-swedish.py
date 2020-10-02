#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
import math
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)


from wordcloud import WordCloud, STOPWORDS

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np # linear algebra
import matplotlib 
import matplotlib.pyplot as plt
import sklearn
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt 
plt.rcParams["figure.figsize"] = [16, 12]
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input/genesis/"]).decode("utf8"))

# Any results you write to the current directory are saved as output.
filenames = check_output(["ls", "../input/genesis/"]).decode("utf8").strip()
# helpful character encoding module
import chardet

# set seed for reproducibility
np.random.seed(0)


# In[ ]:


for filename in filenames.split('\n'):
    if filename[-4:] == '.txt':
        print(filename)
        with open("../input/genesis/" + filename, 'rb') as rawdata:
            print(rawdata.readlines(200))


# In[ ]:


for filename in filenames.split('\n'):
    if filename[-4:] == '.txt':
        print(filename)
        with open("../input/genesis/" + filename, 'rb') as rawdata:
            for size in range(1,7):
                length = 10 ** size
                with open("../input/genesis/" + filename, 'rb') as rawdata:
                    result = chardet.detect(rawdata.read(length))

                # check what the character encoding might be
                print(size, length, result)


# In[ ]:


lang2bible = dict()
for filename in filenames.split('\n'):
    if filename[-4:] == '.txt':
        print(filename)
        with open("../input/genesis/" + filename, 'rb') as rawdata:
            lang2bible[filename[:-4]] = pd.Series(list(map(lambda l: l.strip(), rawdata.readlines())))
            


# In[ ]:


df = pd.DataFrame(lang2bible)


# In[ ]:


df.sample(10)


# In[ ]:


for filename in filenames.split('\n'):
    if filename[-4:] == '.txt':
        print(filename)
        with open("../input/genesis/" + filename, 'rb') as rawdata:
            for size in range(1,9):
                length = 10 ** size
                with open("../input/genesis/" + filename, 'rb') as rawdata:
                    result = chardet.detect(rawdata.read(length))

                # check what the character encoding might be
                print(size, length, result)


# In[ ]:




