#!/usr/bin/env python
# coding: utf-8

# # How to choose a pokemon ?
# 
# In this kernel, I will try to choose the best legendary pokemon according to these combat stats. I just want to try it for fun !!
# So first, I will look at the data, then I will try to create a good combat prediction, which will give me the name of the best pokemon ever !!

# To achieve this goal of choosing a pokemon, I will use 3 steps:
# 1. Look at the dataset
# 2. Create a machine learning algorithm to predict a combat output
# 3. Use this algorithm as a way to mark a pokemon

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os

# Any results you write to the current directory are saved as output.


# In[ ]:


# Settings

pokemon_data = pd.read_csv('../input/pokemon.csv')
combats_data = pd.read_csv('../input/combats.csv')

# Here, we will work only on legendary pokemons
legendary_data = pokemon_data[pokemon_data['Legendary']]
non_legendary_data = pokemon_data[pokemon_data['Legendary'] == False]

pokemon_data.head()


# ## Data description
# 
# Let's look at some statistics on legendary and non legendary pokemons. Legendary have better average stats but they don't have the better pokemon for each stat !!

# In[ ]:


legendary_data.describe()


# In[ ]:


non_legendary_data.describe()


# To normalize combat statistics (attack, defense, ...) in our training data creation, I store the maximum values of each one of these statistics.

# In[ ]:


# storing combat statistics maximum values
atk_max = pokemon_data['Attack'].values.max()
def_max = pokemon_data['Defense'].values.max()
sp_atk_max = pokemon_data['Sp. Atk'].values.max()
sp_def_max = pokemon_data['Sp. Def'].values.max()
speed_max = pokemon_data['Speed'].values.max()


# Now, just for fun, let's find the pokemon which has the most victories in the dataset.

# In[ ]:


winner = combats_data['Winner'].value_counts().idxmax()
pokemon_data.iloc[[winner]].Name


# From the combat data, Mega Mewtwo X is our winner.
# Now, we did not even check for the frequency of this pokemon fights against another so this is clearly not how we want to get a result.
# 
# Let's prepare the data so we can train a classifier on it.

# In[ ]:


# Let's create two classes : the first wins, the second wins
first_winner = combats_data[combats_data['First_pokemon'] == combats_data['Winner']]
second_winner = combats_data[combats_data['First_pokemon'] != combats_data['Winner']]


# In[ ]:


# What are the types of our pokemons ?
pokemon_data['Type 1'].value_counts()


# In[ ]:


# Here, we will create utilitaries to convert data from the pokemon data to usable values
type_dict = {
    'Water' : 0,
    'Normal': 1,
    'Grass': 2,
    'Bug': 3,
    'Psychic': 4,
    'Fire': 5,
    'Rock': 6,
    'Electric': 7,
    'Ground': 8,
    'Dragon': 9,
    'Ghost': 10,
    'Dark': 11,
    'Poison': 12,
    'Fighting': 13,
    'Steel': 14,
    'Ice': 15,
    'Fairy': 16,
    'Flying': 17
}

def create_type_array(type1, type2=''):
    res_arr = [0 for i in range(18)]
    res_arr[type_dict[type1]] = 1
    if type2 in type_dict.keys():
        res_arr[type_dict[type2]] = 1
    res_arr = np.array(res_arr)
    res_arr = res_arr / np.linalg.norm(res_arr)
    return res_arr.tolist()


# Now, we need to create the data we will feed to our machine learning algorithm. I have decided to translate the pokemon types to an array form, to which I will just concatenate the normalized combat statistics.

# In[ ]:


# Creation of a fonction that will generate our input from a match configuration
field_to_keep = ['Type 1', 'Type 2', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
def match_data(id1, id2):
    data = []
    
    # looking at first pokemon data
    first_pokemon = pokemon_data.loc[id1, field_to_keep].values.tolist()
    arr_type = create_type_array(first_pokemon[0], first_pokemon[1])
    atk = first_pokemon[2] / atk_max
    def_ = first_pokemon[3] / def_max
    sp_atk = first_pokemon[4] / sp_atk_max
    sp_def = first_pokemon[5] / sp_def_max
    speed = first_pokemon[6] / speed_max
    data += arr_type + [atk, def_, sp_atk, sp_def, speed]
    
    # looking at second pokemon data
    second_pokemon = pokemon_data.loc[id2, field_to_keep].values.tolist()
    arr_type = create_type_array(second_pokemon[0], second_pokemon[1])
    atk = second_pokemon[2] / atk_max
    def_ = second_pokemon[3] / def_max
    sp_atk = second_pokemon[4] / sp_atk_max
    sp_def = second_pokemon[5] / sp_def_max
    speed = second_pokemon[6] / speed_max
    data += arr_type + [atk, def_, sp_atk, sp_def, speed]
    
    return data


# Now, we will parse the combat data to create our training data, with its labels.

# In[ ]:


x_data = []
y_data = []
for index, row in combats_data.iterrows():
    x_data += [match_data(row['First_pokemon'] - 1, row['Second_pokemon'] - 1)]
    if row['First_pokemon'] == row['Winner']:
        y_data += [1]
    else:
        y_data += [-1]


# ## Prediction

# First, let's create separate our data into a training set and a validation set

# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.25)


# To choose a classifier, we will use a grid search. You don't need to run this grid search as the best classifier is defined in the next cell.

# In[ ]:


from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

# clf = LogisticRegression(penalty='l2', C=25, solver='liblinear')  # Acc: 0.88
# clf = LinearSVC(penalty='l2', loss='hinge', dual=True, tol=0.00001, C=10.0, random_state=42, max_iter=5000)  #Acc: 0.908

clf = RandomForestClassifier(n_estimators=250,
                             criterion='gini',
                             max_depth=None,
                             min_samples_split=2,
                             min_samples_leaf=1,
                             max_features='sqrt')  #Acc: 0.94
param_dict = {
    'n_estimators': [125, 250],
    #'criterion': ['gini', 'entropy'],
    #'max_depth': [None, 5, 8],
    #'min_samples_leaf': [1, 2, 4],
    #'max_features': ['sqrt', 'log2']
}

grid_search = GridSearchCV(clf, param_dict, cv=3, verbose=2, n_jobs=4)

grid_search.fit(x_train, y_train)

print(grid_search.best_score_)    
print(grid_search.best_params_)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(n_estimators=250,
                             criterion='gini',
                             max_depth=None,
                             min_samples_split=2,
                             min_samples_leaf=1,
                             max_features='sqrt')  #Acc: 0.94

clf.fit(x_train, y_train)

print(clf.score(x_val, y_val))


# ## Pokemon choice
# 
# Now, with our algorithm to predict a fight we can find the best fighting pokemon.

# In[ ]:


# First, we will define a function that will test a pokemon during multiple fights to score him
def pokemon_test(pokemon_id, opponent_ids=None):
    # pokemon_id is an id between 0 and 799
    if opponent_ids is None:
        opponents = [i for i in range(800) if i != pokemon_id]
    else:
        opponents = opponent_ids
    
    # We will predict 2*799 fights
    victory_cpt = 0
    for opp in opponents:
        match_1 = match_data(pokemon_id, opp)
        if clf.predict([match_1])[0] == 1:
            victory_cpt += 1
        
        match_2 = match_data(opp, pokemon_id)
        if clf.predict([match_2])[0] == -1:
            victory_cpt += 1
    
    return victory_cpt / (2*799)


# With this new function, let's test Bulbasaur.

# In[ ]:


print(pokemon_test(0))


# Bulbasaur has a 23% winning rate, it won't be our choice...
# 
# Now, let's test only the legendary pokemons, to speed up a bit the calculation

# In[ ]:


def test_pokemon_subset(ids_to_test, verbose=True):
    best_pokemon = ids_to_test[0]
    best_winning_rate = -1
    
    test_cpt = 1
    n_test = len(ids_to_test)
    for pok_id in ids_to_test:
        winning_rate = pokemon_test(pok_id)
        
        if verbose:
            print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
            print("Pokemon {} out of {}".format(test_cpt, n_test))
            print("{} winning rate : {}".format(pokemon_data.loc[pok_id, "Name"], winning_rate))
            print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
        
        if winning_rate > best_winning_rate:
            best_winning_rate = winning_rate
            best_pokemon = pok_id
            
        test_cpt += 1
            
    return best_pokemon, best_winning_rate


# In[ ]:


def test_legendary_pokemons():
    legendary_ids = legendary_data['#'].values - 1
    return test_pokemon_subset(legendary_ids)

b_legendary, win_rate = test_legendary_pokemons()


# AND THE WINNER IS:

# In[ ]:


print("{} with a winning rate of {:.3f}%".format(pokemon_data.loc[b_legendary, "Name"], win_rate * 100.0))


# Now, we could use this to choose the best Water, Fire, Flying, 1st generation, ... pokemon :)

# In[ ]:


# these are just examples
ice_subset = pokemon_data[pokemon_data['Type 1'] == 'Ice']
first_generation = pokemon_data[pokemon_data['Generation'] == 1]

# ['#'].values - 1 to get the ids
best_pokemon, win_rate = test_pokemon_subset(ice_subset['#'].values - 1, verbose=False)
print("Best ice pokemon: {} with a winning rate of {:.3f}%".format(pokemon_data.loc[best_pokemon, "Name"], win_rate * 100.0))

