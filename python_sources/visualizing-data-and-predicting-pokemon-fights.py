#!/usr/bin/env python
# coding: utf-8

# I was pretty excited when I found this dataset, I remembered when I fought with my Blaziken back then in 2nd grade, it was fun. I stopped playing after emerald, and haven't touched pokemon since, and I'm curious of the new generation of pokemons, and I'm going to visualize things. And in the end, I will try to predict the pokemon battles.
# 
# Let's get started.
# 
# ![](https://i.imgur.com/nEwECJa.gif)
# 
# **Contents**
# 1. Data visualization  
#     -Basic data analysis  
#     -Exploring pokemon based on stats  
#     -Exploring pokemons based on generations  
#     -Exploring pokemon based on battles
# 
# 2. Data cleaning & prediction  
#     -Deal with emtpy data  
#     -Calculate stats differences  
#     -Calculate types effectiveness  
#     -Train and test the model  

# In[ ]:


import pandas as pd #data processing
import numpy as np #calculate stuff
import seaborn as sns #visualization
import matplotlib.pyplot as plt #visualization


# In[ ]:


pokemon_df = pd.read_csv('../input/pokemon.csv')
combats_df = pd.read_csv('../input/combats.csv')
test_df = pd.read_csv('../input/tests.csv')
prediction_df = test_df.copy()


# **Visualization**  
# Let's start with seeing what the data looks like.

# In[ ]:


print(pokemon_df.head())


# Hmm, okay we got name, some stats and the types.  
# Let's count the pokemon types.

# In[ ]:


sns.countplot(x='Type 1', data=pokemon_df, order=pokemon_df['Type 1'].value_counts().index)
plt.xticks(rotation=90)
plt.show()


# In[ ]:


sns.countplot(x='Type 2', data=pokemon_df, order=pokemon_df['Type 2'].value_counts().index)
plt.xticks(rotation=90)
plt.show()


# **Exploring pokemon by stats**  
# Let's see the total status distribution.

# In[ ]:


pokemon_df['Total_stats'] = pokemon_df['HP'] + pokemon_df['Attack'] + pokemon_df['Defense'] + pokemon_df['Sp. Atk'] + pokemon_df['Sp. Def'] + pokemon_df['Speed']
print(pokemon_df.iloc[:, [1, -1]].head())


# In[ ]:


sns.distplot(pokemon_df.Total_stats)
plt.show()


# In[ ]:


#average stats
mean_stats = pokemon_df['Total_stats'].mean()
print(mean_stats)


# In[ ]:


#closest value from near_stats
average_pokemon = min(pokemon_df['Total_stats'], key=lambda x: abs(x-mean_stats))
print(pokemon_df.loc[((pokemon_df['Total_stats'] >= average_pokemon-5) & (pokemon_df['Total_stats'] <= average_pokemon+5)), ['Name', 'Total_stats']])


# Here are some name of average pokemon, which has the stats from ranging from 430 to 440. You can meet most of these pokemons at early to mid game of your pokemon journey.
# 
# Anyways, do you know what pokemon has the highest stats and lowest stats? Let's find out.

# In[ ]:


sorted_pokemon_df = pokemon_df.sort_values(by='Total_stats')
#pokemon with 10 lowest stats
print(sorted_pokemon_df[['Name', 'Total_stats']].head(10))


# This is the typical pokemon you will find at the start of your journey after acquiring your first pokemon.
# 
# By the way, even though Magikarp is on this list, it has a big potential. Later on it will evolve to Gyarados, which in my experience, is pretty strong.
# 
# ![](https://i.imgur.com/MtOzK86.jpg)

# In[ ]:


#pokemon with 10 highest stats
print(sorted_pokemon_df[['Name', 'Total_stats', 'Legendary']].tail(10))


# I personally haven't met with any of these. Have you ever caught these pokemons?
# The interesting thing for me that not all the strongest pokemon are legendary.
# 
# Now I am curious, what are the *weakest* legendary pokemon?

# In[ ]:


legendary_pokemon = pokemon_df.loc[pokemon_df['Legendary'] == True]
legendary_pokemon = legendary_pokemon.sort_values(by='Total_stats')
print(legendary_pokemon[['Name', 'Total_stats']].head(20))


# I've only met and several of these pokemons, namely Zapdos, and Moltres. There are many legendary pokemons that I don't know, and this is starting to get interesting.

# **Exploring pokemon by generations**

# In[ ]:


#new pokemon introduced on each generation, sort ascendingly
print(pokemon_df['Generation'].value_counts())

sns.countplot(x='Generation', data=pokemon_df, order=pokemon_df['Generation'].value_counts().index)
plt.show()


# Hmm, I wonder how the total stats correlates to each generation. Is the pokemon becoming stronger on each generation? Let's find out.

# In[ ]:


#group data by generation
group_df = pokemon_df.drop(['#', 'Legendary'], axis=1)
pokemon_groups = group_df.groupby('Generation')
pokemon_groups_mean = pokemon_groups.mean()

sns.pointplot(x=pokemon_groups_mean.index.values, y=pokemon_groups_mean['Total_stats'])
plt.show()


# Hmm, okay. Newer pokemon doesn't mean that they're stronger. How about other stats? Are they tankier? Or faster?

# In[ ]:


fig, axes = plt.subplots(ncols=2, nrows=3, figsize=(15, 10))
sns.pointplot(x=pokemon_groups_mean.index.values, y=pokemon_groups_mean['Attack'], color='red', ax=axes[0][0])
sns.pointplot(x=pokemon_groups_mean.index.values, y=pokemon_groups_mean['Defense'], color='blue', ax=axes[0][1])
sns.pointplot(x=pokemon_groups_mean.index.values, y=pokemon_groups_mean['HP'], color='black', ax=axes[1][0])
sns.pointplot(x=pokemon_groups_mean.index.values, y=pokemon_groups_mean['Speed'], color='green', ax=axes[1][1])
sns.pointplot(x=pokemon_groups_mean.index.values, y=pokemon_groups_mean['Sp. Atk'], color='orange', ax=axes[2][0])
sns.pointplot(x=pokemon_groups_mean.index.values, y=pokemon_groups_mean['Sp. Def'], color='purple', ax=axes[2][1])

plt.show()


# There are 3 stats that are low in gen 2, attack, speed, and sp. atk. Maybe that's the reason the gen 2 pokemons has the lowest average of total stats.  
# 
# Meanwhile, the gen 4 pokemons have the highest stats from all generation, except for speed which is the second highest.

# **Exploring pokemon based on battles**

# 

# In[ ]:


#creating battles dataframe
name_dict = dict(zip(pokemon_df['#'], pokemon_df['Name']))
combats_name_df = combats_df[['First_pokemon', 'Second_pokemon', 'Winner']].replace(name_dict)
print(combats_name_df.head())


# In[ ]:


first_battle = combats_name_df['First_pokemon'].value_counts()
second_battle = combats_name_df['Second_pokemon'].value_counts()
win_counts = combats_name_df['Winner'].value_counts()
total_battle = first_battle + second_battle
win_percentage = win_counts / total_battle

win_percentage = win_percentage.sort_values()


# In[ ]:


#lowest win rate
print(win_percentage.head(10))


# Heh, not a surprise. Most of these pokemons can be found in the wild at the early stage of the game. Pokemon trainers must be beating the shit out of them.

# In[ ]:


print(win_percentage.tail(10))


# Wait, something is wrong here, why is there a Shuckle?

# In[ ]:


print('Total battles of Shuckle:', total_battle['Shuckle'])
# print('Total wins of Shuckle', win_counts['Shuckle'])
# this code produces an error, this is because shuckle lost all the battles, thus not getting counted
print('Total win of Shuckle: 0')
print(':(')


# Poor shuckle, lost all his battles. At least you tried.
# 
# ![](https://i.imgur.com/JXYMX5y.gif)

# In[ ]:


win_percentage.dropna(inplace=True)
print(win_percentage.tail(10))


# Hmm, highest stats doesn't imply highest win rate. Maybe this has to do with the effectiveness of the pokemon against it's enemy.

# **Data cleaning**  
# Alright, before processing the data, it needs to be cleaned.

# In[ ]:


pokemon_df.info()


# Type 2 nulls are pretty understandable, because not all pokemon have 2 types. There is something strange though, which is a null name.

# In[ ]:


pokemon_df.loc[pokemon_df['Name'].isnull()==True]


# With the help of [pokemondb](https://pokemondb.net/pokedex/all), I found out that the missing name was 'Primeape', let's insert that into our data.

# In[ ]:


pokemon_df['Type 2'] = pokemon_df['Type 2'].fillna('None')
pokemon_df['Name'] = pokemon_df['Name'].fillna('Primeape')

#some type is named 'Fight', and some named 'Fighting'. This code is to clean it up.
pokemon_df['Type 1'] = pokemon_df['Type 1'].replace('Fighting', 'Fight')
pokemon_df['Type 2'] = pokemon_df['Type 2'].replace('Fighting', 'Fight')

#changing true/false to 1/0 in Legendary column
pokemon_df['Legendary'] = pokemon_df['Legendary'].map({False: 0, True:1})


# In[ ]:


#creating dictionaries
type_df = pokemon_df.iloc[:, 0:4]
type_df = type_df.drop('Name', axis=1)
stats_df = pokemon_df.drop(['Type 1', 'Type 2', 'Name', 'Generation', 'Total_stats'], axis=1)

type_dict = type_df.set_index('#').T.to_dict('list')
stats_dict = stats_df.set_index('#').T.to_dict('list')


# In[ ]:


#changing winner to 0 and 1, each corresponds to first and second pokemon respectively
combats_df.Winner[combats_df.Winner == combats_df.First_pokemon] = 0
combats_df.Winner[combats_df.Winner == combats_df.Second_pokemon] = 1

print(combats_df.head(5))


# In[ ]:


def replace_things(data):
    #map each battles to pokemon data
    
    data['First_pokemon_stats'] = data.First_pokemon.map(stats_dict)
    data['Second_pokemon_stats'] = data.Second_pokemon.map(stats_dict)

    data['First_pokemon'] = data.First_pokemon.map(type_dict)
    data['Second_pokemon'] = data.Second_pokemon.map(type_dict)

    return data


# In[ ]:


def calculate_stats(data):
    #calculate stats difference
    
    stats_col = ['HP_diff', 'Attack_diff', 'Defense_diff', 'Sp.Atk_diff', 'Sp.Def_diff', 'Speed_diff', 'Legendary_diff']
    diff_list = []

    for row in data.itertuples():
        diff_list.append(np.array(row.First_pokemon_stats) - np.array(row.Second_pokemon_stats))

    stats_df = pd.DataFrame(diff_list, columns=stats_col)
    data = pd.concat([data, stats_df], axis=1)
    data.drop(['First_pokemon_stats', 'Second_pokemon_stats'], axis=1, inplace=True)

    return data


# In[ ]:


def calculate_effectiveness(data):

    '''
        this function creates a new column of each pokemon's effectiveness against it's enemy.
        every effectiveness starts with 1, if an effective type is found on enemy's type, effectiveness * 2
        if not very effective is found on enemy's type, effectiveness / 2
        if not effective is found on enemy's type, effectiveness * 0
        
        This function creates 4 new columns
            1. P1_type1, pokemon 1 first type effectiveness against the enemy's type
            2. P1_type2, pokemon 1 second type effectiveness against the enemy's type
            3. P2_type1, pokemon 2 first type effectiveness against the enemy's type
            4. P2_type2, pokemon 2 second type effectiveness against the enemy's type
    '''
    
    very_effective_dict = {'Normal': [],
                           'Fight': ['Normal', 'Rock', 'Steel', 'Ice', 'Dark'],
                           'Flying': ['Fight', 'Bug', 'Grass'],
                           'Poison': ['Grass', 'Fairy'],
                           'Ground': ['Poison', 'Rock', 'Steel', 'Fire', 'Electric'],
                           'Rock': ['Flying', 'Bug', 'Fire', 'Ice'],
                           'Bug': ['Grass', 'Psychic', 'Dark'],
                           'Ghost': ['Ghost', 'Psychic'],
                           'Steel': ['Rock', 'Ice', 'Fairy'],
                           'Fire': ['Bug', 'Steel', 'Grass', 'Ice'],
                           'Water': ['Ground', 'Rock', 'Fire'],
                           'Grass': ['Ground', 'Rock', 'Water'],
                           'Electric': ['Flying', 'Water'],
                           'Psychic': ['Fight', 'Poison'],
                           'Ice': ['Flying', 'Ground', 'Grass', 'Dragon'],
                           'Dragon': ['Dragon'],
                           'Dark': ['Ghost', 'Psychic'],
                           'Fairy': ['Fight', 'Dragon', 'Dark'],
                           'None': []}

    not_very_effective_dict = {'Normal': ['Rock', 'Steel'],
                               'Fight': ['Flying', 'Poison', 'Bug', 'Psychic', 'Fairy'],
                               'Flying': ['Rock', 'Steel', 'Electric'],
                               'Poison': ['Poison', 'Rock', 'Ground', 'Ghost'],
                               'Ground': ['Bug', 'Grass'],
                               'Rock': ['Fight', 'Ground', 'Steel'],
                               'Bug': ['Fight', 'Flying', 'Poison', 'Ghost', 'Steel', 'Fire', 'Fairy'],
                               'Ghost': ['Dark'],
                               'Steel': ['Steel', 'Fire', 'Water', 'Electric'],
                               'Fire': ['Rock', 'Fire', 'Water', 'Dragon'],
                               'Water': ['Water', 'Grass', 'Dragon'],
                               'Grass': ['Flying', 'Poison', 'Bug', 'Steel', 'Fire', 'Grass', 'Dragon'],
                               'Electric': ['Grass', 'Electric', 'Dragon'],
                               'Psychic': ['Steel', 'Psychic'],
                               'Ice': ['Steel', 'Fire', 'Water', 'Psychic'],
                               'Dragon': ['Steel'],
                               'Dark': ['Fight', 'Dark', 'Fairy'],
                               'Fairy': ['Posion', 'Steel', 'Fire'],
                               'None': []}

    not_effective_dict = {'Normal': ['Ghost'],
                          'Fight': ['Ghost'],
                          'Flying': [],
                          'Poison': ['Steel'],
                          'Ground': ['Flying'],
                          'Rock': [],
                          'Bug': [],
                          'Ghost': ['Normal'],
                          'Steel': [],
                          'Fire': [],
                          'Water': [],
                          'Grass': [],
                          'Electric': ['Ground'],
                          'Psychic': ['Dark'],
                          'Ice': [],
                          'Dragon': ['Fairy'],
                          'Dark': [],
                          'Fairy': [],
                          'None': []}

    p1_type1_list = []
    p1_type2_list = []
    p2_type1_list = []
    p2_type2_list = []

    for row in data.itertuples():
        nested_type = [[1, 1], [1, 1]]

        #manipulating values if found on dictionary
        for i in range(0,2):
            for j in range(0,2):
                if row.Second_pokemon[j] in very_effective_dict.get(row.First_pokemon[i]):
                    nested_type[0][i] *= 2
                if row.Second_pokemon[j] in not_very_effective_dict.get(row.First_pokemon[i]):
                    nested_type[0][i] /= 2
                if row.Second_pokemon[j] in not_effective_dict.get(row.First_pokemon[i]):
                    nested_type[0][i] *= 0

                if row.First_pokemon[j] in very_effective_dict.get(row.Second_pokemon[i]):
                    nested_type[1][i] *= 2
                if row.First_pokemon[j] in not_very_effective_dict.get(row.Second_pokemon[i]):
                    nested_type[1][i] /= 2
                if row.First_pokemon[j] in not_effective_dict.get(row.Second_pokemon[i]):
                    nested_type[1][i] *= 0

        p1_type1_list.append(nested_type[0][0])
        p1_type2_list.append(nested_type[0][1])
        p2_type1_list.append(nested_type[1][0])
        p2_type2_list.append(nested_type[1][1])

    data = data.assign(P1_type1=p1_type1_list, P1_type2=p1_type2_list, P2_type1=p2_type1_list, P2_type2=p2_type2_list)
    data = data.drop(['First_pokemon', 'Second_pokemon'], axis=1)

    return data


# In[ ]:


#map the battle to pokemon's data
train_df = replace_things(combats_df)
print(train_df.head(5))
print('Each value on the list corresponds to HP, atk, def, sp.atk, sp.def, speed and legendary')


# In[ ]:


#calculate the stats difference
train_df = calculate_stats(train_df)
print(train_df.head(5))
print('Each first pokemon\'s stats are then subtracted by the second pokemon\'s stats')
print('Positive values implies the first pokemon has higher stats and vice versa.')


# In[ ]:


#calculate pokemon types' effectiveness
train_df = calculate_effectiveness(train_df)
print(train_df.head())


# In[ ]:


y_train_full = train_df['Winner']
x_train_full = train_df.drop('Winner', axis=1)

from sklearn.model_selection import train_test_split
x_train, x_cv, y_train, y_cv = train_test_split(x_train_full, y_train_full, test_size=0.25, random_state=42)


# Let's train the model.
# 
# **Training**

# In[ ]:


from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

clf_dict = {'log reg': LogisticRegression(), 
            'naive bayes': GaussianNB(), 
            'random forest': RandomForestClassifier(n_estimators=100),
            'knn': KNeighborsClassifier(),
            'linear svc': LinearSVC(),
            'ada boost': AdaBoostClassifier(n_estimators=100),
            'gradient boosting': GradientBoostingClassifier(n_estimators=100),
            'CART': DecisionTreeClassifier()}

for name, clf in clf_dict.items():
    model = clf.fit(x_train, y_train)
    pred = model.predict(x_cv)
    print('Accuracy of {}:'.format(name), accuracy_score(pred, y_cv))


# Hmm, seems like the random forest model is the best right here. Let's use that model to predict our test set.
# 
# **Prediction**

# In[ ]:


test_df = replace_things(test_df)
test_df = calculate_stats(test_df)
test_df = calculate_effectiveness(test_df)
print(test_df.head())


# In[ ]:


classifier = RandomForestClassifier(n_estimators=100)
model = classifier.fit(x_train_full, y_train_full)
prediction = model.predict(test_df)

#prediction_df is created at the very beginning, it's the same thing as test_df before it's changed.
prediction_df['Winner'] = prediction
prediction_df['Winner'][prediction_df['Winner'] == 0] = prediction_df['First_pokemon']
prediction_df['Winner'][prediction_df['Winner'] == 1] = prediction_df['Second_pokemon']
print(prediction_df)


# **Conclusion**  
# I find this dataset pretty interesting. It was a really fun journey to play with this data.
# 
# I believe there are still many things that can be improved from this code. If you spot any mistakes, feel free to leave a comment below.
# 
# Cheers,  
# Vincent
