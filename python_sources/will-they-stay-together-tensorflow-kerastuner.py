#!/usr/bin/env python
# coding: utf-8

# Can we use machine learning to predict if a couple on *Married at First Sight* will stay together? Let's find out.

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


# In[ ]:


import tensorflow as tf
import matplotlib.pyplot as plt


# In[ ]:


raw_data= pd.read_csv("../input/married-at-first-sight/mafs.csv")
raw_data.head()


# What proportion of the couples are still married?

# In[ ]:


print("% stay together: ", len(raw_data[raw_data.Status == 'Married']) * 100/ len(raw_data))


# I'm going to make a new dataframe that makes the most sense to me, with one row per couple. 

# In[ ]:


man = (raw_data.Gender == 'M')
woman = (raw_data.Gender == 'F')

data = pd.DataFrame()
data['couple'] = np.unique(raw_data.Couple)
data['location'] = raw_data.Location.values[::2]
data['man_name'] = raw_data.Name[man].values
data['woman_name'] = raw_data.Name[woman].values
data['man_occupation'] = raw_data.Occupation[man].values
data['woman_occupation'] = raw_data.Occupation[woman].values
data['man_age'] = raw_data.Age[man].values
data['woman_age'] = raw_data.Age[woman].values
data['man_decision'] = raw_data.Decision[man].values
data['woman_decision'] = raw_data.Decision[woman].values
data['status'] = raw_data.Status.values[::2]


# In[ ]:


data.head()


# In[ ]:


still_together = (data.status == 'Married')


# Let's make some visualizations to get a better idea of who goes on the show.

# In[ ]:


import seaborn as sns

sns.catplot("Gender", "Age", data = raw_data, kind = 'violin')
plt.title("Age of contestants on Married at First Sight")


# In[ ]:


plt.plot(np.subtract(data.man_age.values, data.woman_age.values), 'o')
plt.plot(data.couple[still_together] - 1,
         np.subtract(data.man_age.values, data.woman_age.values)[still_together], 'o',
        label = 'still together')
plt.xlabel("Couple")
plt.ylabel("Age difference (man - woman)")
plt.axhline(0, c='k')
plt.title("Couple Age Differences")
plt.legend()
plt.show()


# In[ ]:


avg_age = [(i+j)/2 for i,j in zip(data.man_age.values, data.woman_age.values)]
plt.plot(avg_age, 'o')
plt.plot(data.couple.values[still_together] - 1,
         np.array(avg_age)[still_together], 'o', label = 'still together')
plt.xlabel("Couple")
plt.ylabel("Average Couple Age")
plt.title("Average Couple Age")
plt.legend()
plt.show()


# It doesn't seem that age difference or average age influences whether the couples stay together in the long term. 

# I'm going to assign each of their professions a number (by hand) based on the category:
# 
# 
# | Category | Type                                                                         |
# |----------|------------------------------------------------------------------------------|
# | 0        | Finance/Business/Sales (financial analyst, business owner, salesperson, etc) |
# | 1        | Athletics (coach, athlete, etc)                                              |
# | 2        | Health/Medicine (nurse, doctor, etc)                                         |
# | 3        | Public Service (teacher, non-profits, firefighter, etc)                      |
# | 4        | STEM (engineer, scientist, etc)                                              |
# | 5        | Customer Service (real estate agent, flight attendant, etc)                  |

# In[ ]:


data.man_occupation.values


# In[ ]:


data['man_job_cat'] = np.zeros(len(data))
data['woman_job_cat'] = np.zeros(len(data))
data['man_job_cat'] = [0, 3, 4, 5, 2, 0, 0, 0, 0, 5, 0, 5, 1, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 4, 2, 1, 0, 0, 1, 4, 4, 0, 3, 1]


# In[ ]:


data.woman_occupation.values


# In[ ]:


data['woman_job_cat'] = [2, 5, 0, 0, 0, 5, 5, 2, 0, 3, 5, 5, 2, 3, 0, 5, 0, 0, 0, 0, 0,0,0,0,5,3,0,0,3,3,2,4,0,1]


# In[ ]:


labels = "Finance/Business/Sales", "Athletics", "Health/Medicine", "Public Service", "STEM", "Customer Service"

_, woman_counts = np.unique(data.woman_job_cat.values, return_counts = True)
fig, ax = plt.subplots()
ax.pie(woman_counts, labels = labels)
ax.axis("equal")
plt.title("Woman Occupations")
plt.show()

_, man_counts = np.unique(data.man_job_cat.values, return_counts = True)
fig, ax = plt.subplots()
ax.pie(man_counts, labels = labels)
ax.axis("equal")
plt.title("Man Occupations")
plt.show()


# In[ ]:


labels = ["Finance\nBusiness\nSales", "Athletics", "Health\nMedicine", "Public Service", "STEM", "Customer\nService"]
g = sns.violinplot(data.man_job_cat.values, data.man_age.values)
plt.xlabel("Man's Job Category")
plt.ylabel("Man's age")
plt.title("Men's job category and age")
g.set_xticklabels(labels)
plt.show()

h = sns.violinplot(data.woman_job_cat.values, data.woman_age.values)
plt.xlabel("Woman's Job Category")
plt.ylabel("Woman's age")
plt.title("Women's job category and age")
h.set_xticklabels(labels)
plt.show()


# Which jobs are combined with which?

# In[ ]:


job_combos = np.histogram2d(data.man_job_cat.values, data.woman_job_cat.values, bins = 6)
sns.heatmap(job_combos[0], annot = True, xticklabels = labels, yticklabels = labels, cbar_kws={'label': 'Frequency'})
plt.xlabel("Man's job category")
plt.ylabel("Woman's job category")
plt.title("Job combinations of couples on Married at First Sight")


# In[ ]:


job_combos = np.histogram2d(data.man_job_cat.values[still_together], data.woman_job_cat.values[still_together], bins = 6)
sns.heatmap(job_combos[0], annot = True, xticklabels = labels, yticklabels = labels, cbar_kws={'label': 'Frequency'})
plt.xlabel("Man's job category")
plt.ylabel("Woman's job category")
plt.title("Job combinations of couples on Married at First Sight that stay together")


# Does the location influence whether they stay together?

# In[ ]:


data['loc_index'] = np.zeros(len(data))
data['loc_index'] = [list(np.unique(data.location)).index(i) for i in data.location.values]
data


# In[ ]:


data.location[still_together]


# I'm going to create a model that will predict if the couples will stay together in the long-term. The inputs will be the normalized ages, job categories, and location category.

# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

train, test = train_test_split(shuffle(data), test_size = 0.15)


# In[ ]:


def normalized_value(value, array):
    mean = np.average(array)
    stdev = np.std(array)
    return (value - mean)/stdev


# In[ ]:


train_inputs = []
for index, row in train.iterrows():
    train_inputs.append([normalized_value(row.man_age, data.man_age.values),
                         normalized_value(row.woman_age, data.woman_age.values),
                        row.man_job_cat, row.woman_job_cat, row.loc_index])
    
test_inputs = []
for index, row in test.iterrows():
    test_inputs.append([normalized_value(row.man_age, data.man_age.values),
                         normalized_value(row.woman_age, data.woman_age.values),
                      row.man_job_cat, row.woman_job_cat, row.loc_index])


# In[ ]:


train_outputs = [1 if i == 'Married' else 0 for i in train.status.values]
test_outputs = [1 if i == 'Married' else 0 for i in test.status.values]


# KerasTuner is a great tool for hyperparameter tuning (finding the best parameters for the model). For more information: https://www.tensorflow.org/tutorials/keras/keras_tuner

# In[ ]:


get_ipython().system('pip install keras-tuner')


# In[ ]:


import kerastuner as kt
def build_model(hp):
    model = tf.keras.Sequential()
    hp_units = hp.Int('units', min_value = 16, max_value = 512, step = 16)
    
    model.add(tf.keras.layers.Dense(hp_units,activation = 'relu', input_shape = (5,)))
    model.add(tf.keras.layers.Dense(16, activation = 'relu'))
    model.add(tf.keras.layers.Dense(2, kernel_initializer = 'uniform',activation = 'softmax'))
    
    hp_learning_rate = hp.Choice('learning_rate', values = [1e-3, 1e-4, 1e-5]) 
    
    model.compile(loss = 'sparse_categorical_crossentropy', optimizer = tf.keras.optimizers.Adam(hp_learning_rate),
                  metrics = ['accuracy'])
    return model


# In[ ]:


tuner = kt.Hyperband(build_model,
                     objective = 'val_accuracy', 
                     max_epochs = 10,
                     factor = 3)     


# In[ ]:


tuner.search(train_inputs, train_outputs, epochs = 100, verbose = 1,
          validation_data = (test_inputs, test_outputs))


# In[ ]:


tuner.results_summary()


# Now, we can grab the best model and train it.

# In[ ]:


best_hps = tuner.get_best_hyperparameters(num_trials = 1)[0]
model = tuner.hypermodel.build(best_hps)
model.fit(train_inputs, train_outputs, epochs = 100, verbose = 1,
          validation_data = (test_inputs, test_outputs),
         callbacks = tf.keras.callbacks.EarlyStopping(patience = 10))


# Let's see how accurate it is.

# In[ ]:


model.evaluate(test_inputs, test_outputs)[1]


# The model's not that great, but it would be fun to predict what couples stay together when the next season comes out! In the meantime, I'll save the dataframe I created as a CSV in case anyone else wants to play around with it.

# In[ ]:


data.to_csv("MAFS_by_couple.csv", index = False)


# In[ ]:




