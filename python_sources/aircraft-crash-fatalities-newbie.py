#!/usr/bin/env python
# coding: utf-8

# ## Introduction

# This is my very first notebook in Kaggle, so my main motivation is to learn how Kaggle works. But at the same time, I have been learning Python for data science and machine learning for just a few months, so if you are looking for expert analysis, look elsewhere :-)
# 
# But hey, don't go just yet. The dataset used is the commonly available *"Airplane_Crashes_and_Fatalities_Since_1908.csv"* which I have improved by adding new accident data up to Feb 2020, and by visually analysing and improving it with a spreadsheet. This has uncovered evidence that was otherwise hidden under errors and misspellings. So given you will go through it in less than 3 minutes, I reckon it will be worth browsing it.

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
import datetime

# Pretty display for notebooks
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# Upload data file into dataframe df
df = pd.read_csv("../input/Airplane_Crashes_and_Fatalities_Since_1908_DV_03032020.csv")


# ## Data preparation

# In[ ]:


df.head()


# In[ ]:


df.info()


# In[ ]:


# Convert DATE column to datetime format
df['DATE'] = pd.to_datetime(df['DATE'])
df.info()


# In[ ]:


df.describe()


# In[ ]:


df.describe(include='object')


# In[ ]:


df.isnull().sum() # missing data


# ## Descriptive stats
# Some basic stats about the most accidented aircraft types and operators. Note how after revising the data some key players such as the UK Royal Air Force have come to light.
# 
# The plot of ground casualties reminds us right away of the mad times we live in.

# In[ ]:


# Nbr of accident per aircraft type (top 25)

acc_per_ac_type = df['AIRCRAFT_TYPE'].value_counts().head(25)
acc_per_ac_type.plot(kind='barh', figsize=(12,8), title='Nbr of accidenteds per aircraft type (top 25)', grid=True)
acc_per_ac_type.head(25)


# In[ ]:


# Nbr of accidents per airline / operator (top 25)

acc_per_operator = df['OPERATOR'].value_counts().head(25)
acc_per_operator.plot(kind='barh', figsize=(12,8), title='Nbr of fatal accidentes per operator (top 25)', grid=True)
acc_per_operator.head(25)


# In[ ]:


# Nbr of aviation accidents per year since 1908
df['DATE'].groupby(df.DATE.dt.year).agg('count').plot(figsize=(12,8), title='Nbr of aviation fatal accidents per year since 1908', grid=True)


# In[ ]:


# Nbr of aviation fatalities per year since 1908
df['TOTAL_FATALITIES'].groupby(df.DATE.dt.year).agg('sum').plot(figsize=(12,8), title='Nbr of aviation fatalities per year since 1908', grid=True)


# In[ ]:


# Nbr of aviation ground fatalities per year since 1908 - note the sharp peak in 2001, rest in peace those who died on Sept 11 2001 
df['GROUND_CASUALTIES'].groupby(df.DATE.dt.year).agg('sum').plot(figsize=(12,8), title='Nbr of aviation ground fatalities per year since 1908', grid=True)


# In[ ]:


# Accidents per year of the top 10 accidented operators

top10_acc_operator = acc_per_operator.head(10)

plt.figure(figsize=(32,12))
plt.xlabel ('YEAR')
plt.ylabel('NUMBER OF ACCIDENTS')

df_accidents = df[['DATE', 'OPERATOR']]

for op in top10_acc_operator.index:
  
  df_accidents_py = df_accidents[df_accidents.OPERATOR == op].groupby(df.DATE.dt.year).agg('count')
  plt.plot(df_accidents_py.index, df_accidents_py.DATE, linewidth=0.5, marker='*')

plt.legend(top10_acc_operator.index, loc='upper left')
plt.show()


# ## So what now??

# From here, time and inspiration permiting, I have some ideas to dig deeper:
# 
#     - combine the dataset with new aircraft accident data with no casualties (the dataset this analysis is based on includes only accidents with casualties) - from there a model to predict survivors is a must.
# 
#     - further work can be done to refine the data so that things like 737-xyz are aggregated as a single 737 aircraft type  (whether that has any scientific interest I am not sure).
#     
#     - whilst there is already plenty of work out there on causes of accidents and the like, applying some NLP processing to the SUMMARY_OF_EVENTS column of the dataset and drafting some charts from the results will surely yield some interesting insights too.

# ## Analysis of the SUMMARY_OF_EVENTS column with NLP spaCy
# 
# There is valuable information in the summary column about the circumstances surrounding the accident, including the phase of the flight when the accident occurred, the weahter conditions, or if the aircraft was shot down by a missile. So here is a first attempt at processing this information and drawing some conclusions.

# In[ ]:


df_summary = df['SUMMARY_OF_EVENTS']
df_summary


# In[ ]:


import spacy
import string
#from spacy.lang.en.stop_words import STOP_WORDS
#from spacy.lang.en import English

nlp = spacy.load("en_core_web_sm")
stop_words = spacy.lang.en.stop_words.STOP_WORDS
print("Nbr. of stop words: %d" %len(stop_words))


# In[ ]:


punctuation = string.punctuation
punctuation


# In[ ]:


# Create a tokenizer function for pre-processing each accident summary

def spacy_tokenizer(sentence):
    # Create token object
    mytokens = nlp(sentence)
    #mytokens = parser(sentence)

    # Lemmatize each token and convert it into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]

    # Remove stop words and punctuations
    mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuation ]

    # return preprocessed list of tokens
    return mytokens


# In[ ]:


test_sentence = "While attempting to land in rain and fog, the aircraft ran out of fuel, stalled and crashed at Lunghwa field."
tokens = spacy_tokenizer(test_sentence)
tokens


# In[ ]:


# Create a new column in the dataframe and assign the tokens for each accident

tokens = []

for x in df.SUMMARY_OF_EVENTS:
  tokens.append(spacy_tokenizer(str(x)))
  
df['TOKENS'] = tokens


# In[ ]:


df['TOKENS'].head(20)


# In[ ]:


# Create a dictionary with pairs of words and their frequencies
# to count how relevant each of these words are

hash_map = {}

for tokens in df['TOKENS']:
  for word in tokens:
    if word in hash_map:
      hash_map[word] = hash_map[word] + 1
    else:
      hash_map[word] = 1

# Order the dictionary by highest values first
#hash_map = {k: v for k, v in sorted(hash_map.items(), key=lambda item: item[1], reverse=True)}

# Search for the frequency of specific relevant words
words_list = ['rain', 'fog', 'wind', 'snow', 'turbulence', 'storm', 'clear', 
              'midair', 'sea', 'ocean', 'mountain', 'hill', 'building', 
              'residential', 'hijack', 'missile', 'failure', 'malfunction', 
              'explosion', 'collision', 'overload', 'takeoff', 'climb',
              'cruise', 'descend', 'landing']

for w in words_list:
  print(w + " : " + str(hash_map[w]))


# ## Some more descriptive stats
# ### Weather conditions

# In[ ]:


# Create a mini-dataframe with weather conditions stats
weather_words = {'rain', 'fog', 'wind', 'snow', 'turbulence', 'storm', 'clear'}
weather_df = []

for w in weather_words:
  print(w + " : " + str(hash_map[w]))
  weather_df.append([w, hash_map[w]])

weather_df = pd.DataFrame(weather_df, columns=['WEATHER_CONDITION', 'NBR_ACCIDENTS'])
weather_df


# In[ ]:


# Plot a pie chart with % values
from pylab import rcParams
rcParams['figure.figsize'] = 8,8

fig1, ax1 = plt.subplots()
ax1.pie(weather_df.NBR_ACCIDENTS, labels=weather_df.WEATHER_CONDITION, autopct='%1.1f%%', startangle=180)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('Percentage of accidents in specific weather conditions')
plt.show()


# ### Phase of flight

# In[ ]:


# Create a mini-dataframe with phase of the flight stats
flight_phase_words = {'takeoff', 'climb', 'cruise', 'descend', 'landing'}
flight_phase_df = []

for f in flight_phase_words:
  print(f + " : " + str(hash_map[f]))
  flight_phase_df.append([f, hash_map[f]])
  
flight_phase_df = pd.DataFrame(flight_phase_df, columns=['FLIGHT_PHASE', 'NBR_ACCIDENTS'])
flight_phase_df


# In[ ]:


# Plot a pie chart with % values

fig2, ax2 = plt.subplots()
ax2.pie(flight_phase_df.NBR_ACCIDENTS, labels=flight_phase_df.FLIGHT_PHASE, autopct='%1.1f%%', startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('Percentage of accidents in each phase of the flight')
plt.show()


# ### Crash zone

# In[ ]:


# Create a mini-dataframe with crash zone stats
# Some words are counted together: 
#   sea & ocean --> sea
#   montain & hill --> mountain
#   building & residential --> residential

crash_zone_words = {'midair', 'sea', 'mountain', 'residential'}
crash_zone_df = []

for z in crash_zone_words:
  print(z + " : " + str(hash_map[z]))
  if (z == 'sea'):
    crash_zone_df.append([z, hash_map[z] + hash_map['ocean']])
  elif (z == 'mountain'):
    crash_zone_df.append([z, hash_map[z] + hash_map['hill']])
  elif (z == 'residential'):
    crash_zone_df.append([z, hash_map[z] + hash_map['building']])
  else:
    crash_zone_df.append([z, hash_map[z]])

  
crash_zone_df = pd.DataFrame(crash_zone_df, columns=['CRASH_ZONE', 'NBR_ACCIDENTS'])
crash_zone_df


# In[ ]:


# Plot a pie chart with % values

fig3, ax3 = plt.subplots()
ax3.pie(crash_zone_df.NBR_ACCIDENTS, labels=crash_zone_df.CRASH_ZONE, autopct='%1.1f%%', startangle=0)
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('Percentage of accidents per crash zone')
plt.show()


# ### Crash reason

# In[ ]:


# Create a mini-dataframe with crash reason stats
crash_reason_words = {'hijack', 'missile', 'failure', 'malfunction', 'explosion', 'overload'}
crash_reason_df = []

for r in crash_reason_words:
  print(r + " : " + str(hash_map[r]))
  crash_reason_df.append([r, hash_map[r]])
  
crash_reason_df = pd.DataFrame(crash_reason_df, columns=['CRASH_REASON', 'NBR_ACCIDENTS'])
crash_reason_df


# In[ ]:


# Pie chart with % values

fig4, ax4 = plt.subplots()
ax4.pie(crash_reason_df.NBR_ACCIDENTS, labels=crash_reason_df.CRASH_REASON, autopct='%1.1f%%')
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('Percentage of accidents per crash reason')
plt.show()


# Naturally, the language is way more complicated than this and the current analysis is veeeery basic, not accounting for example for composed words such as 'emergency landing', 'shot down', 'midair collision', or 'en route', nor differentiating betweeen 'engine failure' and 'structural failure', let alone some more specialized words such as 'nosedive' and 'stall.
# 
# But all that for the next day.
