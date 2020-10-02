# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import pyplot as plt
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input/movie_metadata.csv"]).decode("utf8"))

# Any results you write to the current directory are saved as output.
data = pd.read_csv("../input/movie_metadata.csv")
data = data.dropna(subset=['budget'])
med = data.groupby(['genres'])['budget'].median()
plt.figure()
ax = med.nlargest(20).plot(kind='barh',title="Genres vs Median Budget - Top 20",color=['red','yellow','maroon','orange','green','cyan'])
ax.set_xlabel("Budget")
ax.set_ylabel("Genres")
plt.savefig("ensemble.png", dpi=200)

data = data[data['language']=='English']
#data['genres']=data['genres'].str.replace('|','\n')                                                                                                                                
med = data.groupby(['title_year'])['duration'].median()

plt.figure()
ax = med.plot(title="Median Duration of English movies over the years",color="Red")
ax.set_xlabel("Year")
ax.set_ylabel("Median Duration (Minutes)")
plt.savefig("duration_english.png",dpi=400)