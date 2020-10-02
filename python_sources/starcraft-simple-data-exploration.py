#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv("../input/starcraft.csv")


# In[ ]:


data.head()


# In[ ]:


import matplotlib.pyplot as plt

plt.scatter(data["LeagueIndex"], data["APM"])


# There's clearly a minimum APM trend for people in higher leagues

# In[ ]:


import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

def plot_stat_vs_league(input_stat):
    league_num = []
    avg = []
    min = []
    max = []

    for i in range((data["LeagueIndex"].max())):
        #print(sum(data[data["LeagueIndex"]==1][input_stat])/len(data[data["LeagueIndex"]==1][input_stat]))
        league_num.append(i+1)
        avg.append((data[data["LeagueIndex"]==i+1][input_stat].mean()))
        min.append((data[data["LeagueIndex"]==i+1][input_stat].min()))
        max.append((data[data["LeagueIndex"]==i+1][input_stat].max()))

    plt.plot(league_num, avg, color='b')
    plt.plot(league_num, min, color='g')
    plt.plot(league_num, max, color='r')
    plt.xlabel("League Number")
    plt.ylabel("Average " + str(input_stat))
    plt.title(str(input_stat)+" vs League Number")

    blue_patch = mpatches.Patch(color='blue', label='Average ' + str(input_stat))
    green_patch = mpatches.Patch(color='green', label='Min '+ str(input_stat))
    red_patch = mpatches.Patch(color='red', label='Max '+ str(input_stat))
    plt.legend(handles=[blue_patch, green_patch, red_patch],bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plt.show()


# In[ ]:


plot_stat_vs_league("APM")


# We can see in general the Average and minimum APM is increasing as league increases.  The maximum APM also has a similar trend but seems to peak at leagues 5 and 6.

# In[ ]:


plot_stat_vs_league("Age")


# Looks like only the young people are the top dogs here.

# In[ ]:


plot_stat_vs_league("HoursPerWeek")
plot_stat_vs_league("TotalHours")


# As expected people who spend more time in the game do better.  Note currently there is some outlier in league five.

# In[ ]:


plot_stat_vs_league("SelectByHotkeys")


# Again, as expected, the more hotkey usage the higher the league

# In[ ]:


plot_stat_vs_league("WorkersMade")


# Interesting, average workers made seems to peak around league 7

# In[ ]:




