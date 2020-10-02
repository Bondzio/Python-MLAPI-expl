#!/usr/bin/env python
# coding: utf-8

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


# Disclaimer: I completely made up these numbers.
# 
# The idea is to simulate a "smart" football club; who rarely calls the same type of play (I considered "pass" plays, "run" plays and "RPO"-run pass option- plays) twice in a row. I created a state diagram (see image) which represents the probability of calling each type of play. For reference; like coloured lines are considered outward arrows. 
# 
# ![Screen%20Shot%202020-06-05%20at%201.11.08%20AM.png](attachment:Screen%20Shot%202020-06-05%20at%201.11.08%20AM.png)

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random as rm


# The idea is to similate the probabilities in the above state diagram using Markov chains. 

# In[ ]:


##P: Pass, R: Run, O: Option, i.e RPO play
states = ["P","R","O"]

# Possible sequences 
transitionName = [["PP","PR","PO"],["RP","RR","RO"],["OP","OR","OO"]]

# Probabilities matrix (transition matrix)
transitionMatrix = [[0.35,0.25,0.4],[0.4,0.3,0.3],[0.45,0.35,0.2]]


# Next we define the forecast function to simulate these events (plays)

# In[ ]:


def forecast(downs):
    play = "P"
    playbook = [play]
    i = 0
    prob = 1
    while i != downs:
        if play == "P":
            change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
            if change == "PP":
                prob = prob * 0.35
                playbook.append("P")
                pass
            elif change == "PR":
                prob = prob * 0.25
                play = "R"
                playbook.append("R")
            elif change == "PO":
                prob = prob * 0.4
                play = "O"
                playbook.append("O")
        elif play == "R":
            change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
            if change == "RR":
                prob = prob * 0.4
                playbook.append("R")
                pass
            elif change == "RP":
                prob = prob * 0.3
                play = "P"
                playbook.append("P")
            elif change == "RO":
                prob = prob * 0.3
                play = "O"
                playbook.append("O")
        elif play == "O":
            change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
            if change == "OO":
                prob = prob * 0.45
                playbook.append("O")
                pass
            elif change == "OP":
                prob = prob * 0.35
                play = "P"
                playbook.append("P")
            elif change == "OR":
                prob = prob * 0.2
                play = "R"
                playbook.append("R")
        i += 1       
    return playbook

full_playbook = []
count = 0


# Next, preform many simulations

# In[ ]:


##simulate 4 downs
for iterations in range(1,10000):
        full_playbook.append(forecast(3))

#See all plays called in a particular set of 4 downs
##print(full_playbook)

#Counts; so we can predict the probability of a given play 
##for example, in this case, the probability we call an RPO on 4th down

for plays in full_playbook:
    if(plays[3] == "O"):
        count += 1


# Calculate different probabilities

# In[ ]:


percentage = (count/10000) * 100
print("The probability of starting at state:'P' and ending at state:'O'= " + str(percentage))


# In[ ]:


def forecast(downs):
    play = "R"
    playbook = [play]
    i = 0
    prob = 1
    while i != downs:
        if play == "P":
            change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
            if change == "PP":
                prob = prob * 0.35
                playbook.append("P")
                pass
            elif change == "PR":
                prob = prob * 0.25
                play = "R"
                playbook.append("R")
            elif change == "PO":
                prob = prob * 0.4
                play = "O"
                playbook.append("O")
        elif play == "R":
            change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
            if change == "RR":
                prob = prob * 0.4
                playbook.append("R")
                pass
            elif change == "RP":
                prob = prob * 0.3
                play = "P"
                playbook.append("P")
            elif change == "RO":
                prob = prob * 0.3
                play = "O"
                playbook.append("O")
        elif play == "O":
            change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
            if change == "OO":
                prob = prob * 0.45
                playbook.append("O")
                pass
            elif change == "OP":
                prob = prob * 0.35
                play = "P"
                playbook.append("P")
            elif change == "OR":
                prob = prob * 0.2
                play = "R"
                playbook.append("R")
        i += 1       
    return playbook

full_playbook = []
count = 0


for iterations in range(1,10000):
        full_playbook.append(forecast(3))

#See all plays called in a particular set of 4 downs
##print(full_playbook)

#Counts; so we can predict the probability of a given play 
##for example, in this case, the probability we call an RPO on 4th down
for plays in full_playbook:
    if(plays[1] == "P"):
        count += 1


# In[ ]:


percentage2 = (count/10000) * 100
print("The probability of starting at state:'R' and running a passing play on 2nd down 'P'= " + str(percentage2))


# And so on; we could easily choose different probabilities to explore which I may add later (probability of running on first down? How about passing on 4th down?)
# 
# I hope you learned a bit about Markov chains and how to implement them in python!
