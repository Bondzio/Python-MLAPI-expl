#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Libraried
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

import datetime
from time import time
from scipy import stats

from sklearn.model_selection import GroupKFold
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor, CatBoostClassifier
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import os
import glob
import copy

import numpy as np
from scipy.integrate import odeint


# In[ ]:


# x_1 = train_df['Date']
# y_1 = train_df['ConfirmedCases']
# y_2 = train_df['Fatalities']

# fig = make_subplots(rows=1, cols=1)

# fig.add_trace(
#     go.Scatter(x=x_1, mode='lines+markers', y=y_1, marker=dict(color="mediumaquamarine"), showlegend=False,
#                name="Original signal"),
#     row=1, col=1
# )

# fig.add_trace(
#     go.Scatter(x=x_1, mode='lines+markers', y=y_2, marker=dict(color="darkgreen"), showlegend=False,
#                name="Original signal"),
#     row=1, col=1
# )

# fig.update_layout(height=400, width=800, title_text="ConfirmedCases (pale) vs. Fatalities (dark) ")
# fig.show()


# ## Let's get started with the basic SI model (Susceptible Infected)
# 
# First of all let's divide the population into two groups:
# 
# * The susceptibles, who are healthy people, the number of susceptibles is denoted as S.
# * The infected, who have been infected by the virus, the number of infected is denoted as I.
# 
# The number of the total population is denoted as N.
# 
# So N = S + I
# 
# Let's assume each day there will be I[idx] (idx stands for the idx-th day) infected going out and they will meet with r people, and the probability for the contacted people to be infected is B, so we have:
# 
# * S[idx+1] = S[idx] - r*B*I[idx]*S[idx]/N
# * I[idx+1] = I[idx] + r*B*I[idx]*S[idx]/N
# 
# Then we can start programming it:

# In[ ]:


# SI model
N = 2200000          # Total population
I = np.zeros(200)  # Infected
S = np.zeros(200)   # Susceptible

r = 10             # This value defines how quickly the disease spreads
B = 0.01            # Probability of being infected

I[0] = 1           # On day 0, there's only one infected person
S[0] = N-I[0]      # So the suspecptible people is equal = N - I[0]

for idx in range(199):
    S[idx+1] = S[idx] - r*B*I[idx]*S[idx]/N
    I[idx+1] = I[idx] + r*B*I[idx]*S[idx]/N


# In[ ]:


sns.lineplot(x=np.arange(200), y=S, label='Susceptible')
sns.lineplot(x=np.arange(200), y=I, label='Infected')


# What the SI model suggests is that once a people got infected eventually the total population will be infected. But does it sound too simple? How can we improve it?

# ## Introducing SEIR model (Susceptible, Exposed, Infected and Recovered)
# 
# First of all let's divide the population into two groups:
# 
# TO-BE-COMPLETED

# In[ ]:


N = 2200000        # Total population
days = 200          # Period
E = np.zeros(days)  # Exposed          
E[0] = 0            # Day 0 exposed
I = np.zeros(days)  # Infected
I[0] = 1          # Day 0 infected                                                                
S = np.zeros(days)  # Susceptible
S[0] = N - I[0]     # Day 0 susceptible
R = np.zeros(days)  # Recovered
R[0] = 0

r = 20              # Number of susceptible could be contactes by an infected
B = 0.03            # Probability of spread for infected
a = 0.1             # Probability of converted from exposed to infected
r2 = r             # Number of susceptible could be contactes by an exposed
B2 = B          # Probability of spread for exposed
y = 0.1             # Probability of recovered


for idx in range(days-1):
    S[idx+1] = S[idx] - r*B*S[idx]*I[idx]/N - r2*B2*S[idx]*E[idx]/N
    E[idx+1] = E[idx] + r*B*S[idx]*I[idx]/N -a*E[idx] + r2*B2*S[idx]*E[idx]/N
    I[idx+1] = I[idx] + a*E[idx] - y*I[idx]
    R[idx+1] = R[idx] + y*I[idx]
    
plt.figure(figsize=(16,9))
sns.lineplot(x=np.arange(200), y=S, label='Susceptible')
sns.lineplot(x=np.arange(200), y=I, label='Infected')
sns.lineplot(x=np.arange(200), y=E, label='Exposed')
sns.lineplot(x=np.arange(200), y=R, label='Recovered')



I_origin = copy.copy(I)


# ## What if we implement a social-distancing policy?
# 

# In[ ]:


N = 2200000        # Total population
days = 200          # Period
E = np.zeros(days)  # Exposed          
E[0] = 0            # Day 0 exposed
I = np.zeros(days)  # Infected
I[0] = 1            # Day 0 infected                                                                
S = np.zeros(days)  # Susceptible
S[0] = N - I[0]     # Day 0 susceptible
R = np.zeros(days)  # Recovered
R[0] = 0

r = 20              # Number of susceptible could be contactes by an infected
B = 0.03            # Probability of spread for infected
a = 0.1             # Probability of converted from exposed to infected
r2 = r             # Number of susceptible could be contactes by an exposed
B2 = B           # Probability of spread for exposed
y = 0.1             # Probability of recovered


for idx in range(days-1):
    if idx>10:
        r = 5
        r2 = r
    S[idx+1] = S[idx] - r*B*S[idx]*I[idx]/N - r2*B2*S[idx]*E[idx]/N
    E[idx+1] = E[idx] + r*B*S[idx]*I[idx]/N -a*E[idx] + r2*B2*S[idx]*E[idx]/N
    I[idx+1] = I[idx] + a*E[idx] - y*I[idx]
    R[idx+1] = R[idx] + y*I[idx]

plt.figure(figsize=(16,9))
sns.lineplot(x=np.arange(200), y=S, label='Secestible')
sns.lineplot(x=np.arange(200), y=I, label='Infected')
sns.lineplot(x=np.arange(200), y=E, label='Exposed')
sns.lineplot(x=np.arange(200), y=R, label='Recovered')

I_sd = copy.copy(I)


# ### Let's plot them together

# In[ ]:


plt.figure(figsize=(16,9))
sns.lineplot(x=np.arange(200), y=I_origin, label='Infected w/o social distancing')
sns.lineplot(x=np.arange(200), y=I_sd, label='Infected w/ social distancing')


# # Questions:
# 
# 1. Can you tune the parameters used by the model so that it will better fit current status in Alberta?
# 
# Tips: 
# 
# * COVID-19 stats in AB can be found from here webiste:https://covid19stats.alberta.ca/
# 
# * You may want to tweak the parameters such as intitial exposed, 
# 
# 2. As you can see, social distancing is an effective way of "flattening" the infected curve. Can you think of any other methods that can also be used for the same purpose? How can we adjust to model to reflect the effects you may come up with? What reasonable assumptions we can make? Can you also plot it along with the "do nothing" and "social distancing" curves so we can compare them?
# 
# 3. What are your takeawys from dothing these excercises? As an Albertan, what can we do to help our community during this challening time?
# 
