#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import ast
from collections import Counter

pd.set_option('max_columns', None)


# In[ ]:


import os
os.listdir("../input")


# In[ ]:


train = pd.read_csv('../input/tmdb-box-office-prediction/train.csv')
test = pd.read_csv('../input/tmdb-box-office-prediction/test.csv')


# Now that the data has been loaded in, we can perform some basic EDA to get a better understanding of the data that has been provided. 
# 

# In[ ]:


print("Training data shape: ",train.shape)
print("Testing data shape:  ",test.shape)


# In[ ]:


train.iloc[0]


# Since a majority of the datatypes of the columns are objects, we'll have to process and convert them into relavent datatypes.

# Converting all json responses to dictionaries:
# 
# 

# In[ ]:


dict_columns = ['belongs_to_collection', 'genres', 'production_companies',
                'production_countries', 'spoken_languages', 'Keywords', 'cast', 'crew']

def text_to_dict(df):
    for column in dict_columns:
        df[column] = df[column].apply(lambda x: {} if pd.isna(x) else ast.literal_eval(x) )
    return df

if type(train[dict_columns[0]][0]) == str:
    train = text_to_dict(train)
    test = text_to_dict(test)
else:
    print("Already in Dict format")


# # Columnar Analysis:
# ### 1. Belongs_to_collection :
# 

# In[ ]:


print("Number of null cells in this column: ", sum(train.belongs_to_collection == {}))
print("Which amounts to {:.2f} % missing from the 3000 rows present.".format(sum(train.belongs_to_collection == {})/30))


# So this column seems to be of a standard json response format, consisting a variety of details. 
# 

# This column holds details of the ID, name and poster paths which can be accessed by appending the path in the column to [https://image.tmdb.org/t/p/original](https://image.tmdb.org/t/p/original) this link, for example we can get the original poster for the picture by visiting [https://image.tmdb.org/t/p/original/wt5AMbxPTS4Kfjx7Fgm149qPfZl.jpg](https://image.tmdb.org/t/p/original/wt5AMbxPTS4Kfjx7Fgm149qPfZl.jpg)

# Since none of the fields of this JSON response seem to be corelated to the budget or revenue of the movie, we can ignore it for now.

# In[ ]:


train = train.drop(['belongs_to_collection'], axis=1)
test = test.drop(['belongs_to_collection'], axis=1)


# ### 2. Budget: 
# The [budget](https://en.wikipedia.org/wiki/Film_budgeting) of a film defines how much has been spent to make the movie, and the movie can be a success only if the revenue earned it higher than the budget spent. 

# In[ ]:


plt.plot(train.budget)


# In[ ]:


plt.scatter(train.budget,train.revenue)


# In[ ]:


ids = []
genre_list = []
d = []
for i in train.genres:
    for j in i:
        if j['name'] == 'TV Movie':
            j['name'] = 'TV_Movie'
        if j['name'] not in genre_list:
            ids.append(j['id'])
            genre_list.append(j['name'])
            d.append(j)
print(genre_list)


# In[ ]:


count = {}
for name in genre_list:
    count[name] = 0
for i in train.genres:
    for j in i:
        val = j['name']
        count[val]+=1


# In[ ]:


print("{0: <18}|  {1: <5}\n".format('Genres','Count'))
for i in count.keys():
    print("{0: <18}|  {1: <5}".format(i,count[i]))


# In[ ]:


train['num_genres'] = train['genres'].apply(lambda x: len(x) if x != {} else 0)
train['all_genres'] = train['genres'].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')

test['num_genres'] = test['genres'].apply(lambda x: len(x) if x != {} else 0)
test['all_genres'] = test['genres'].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')

for g in genre_list:
    train['genre_' + g] = train['all_genres'].apply(lambda x: 1 if g in x else 0)
    test['genre_' + g] = test['all_genres'].apply(lambda x: 1 if g in x else 0)

test['num_genres'] = test['genres'].apply(lambda x: len(x) if x != {} else 0)
test['all_genres'] = test['genres'].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')


train = train.drop(['genres'], axis=1)
test = test.drop(['genres'], axis=1)


# In[ ]:


languages = train.original_language.unique()
print(languages)


# In[ ]:


for g in languages:
    train['language_' + g] = train['original_language'].apply(lambda x: 1 if g == x else 0)
for g in languages:
    test['language_' + g] = train['original_language'].apply(lambda x: 1 if g == x else 0)


# In[ ]:


from matplotlib import pyplot as plt
plt.scatter(train.runtime, train.revenue)


# In[ ]:


for i, e in enumerate(train['production_companies'][:5]):
    print(e)


# In[ ]:


#no of productions companies in a movie - eg 775 movies have only 1 prod company
x = train['production_companies'].apply(lambda x: len(x) if x != {} else 0).value_counts()
x


# In[ ]:


x = train['production_companies'].apply(lambda x: len(x) if x != {} else 0)
y = (train['revenue'])
z = train['production_companies'].apply(lambda x: len(x) if x != {} else 0).value_counts()
d = {}
for i in train.index:
    if x[i] in d.keys():
        d[x[i]] += y[i]
    else:
        d[x[i]] = y[i]
for i in d.keys():
    d[i]/=z[i]


# In[ ]:


list_of_companies = list(train['production_companies'].apply(lambda x: [i['name'] for i in x] if x != {} else []).values)


# In[ ]:



print(8 in d.keys())
plt.scatter(d.keys(),d.values())


# No absolute relation between the number of production companies, thus it cannot be considered as a feature for the final dataset

# In[ ]:


print('Number of production countries in films')
train['production_countries'].apply(lambda x: len(x) if x != {} else 0).value_counts()


# In[ ]:


file = open('../input/production-companies-and-countries/production_countries.txt','r')
lines = file.read().split('\n')
len(lines)
#last 27 - 1 group: 140 left, split to 14 groups
i = 0
country_group = []
inc = 1
total = 0
for i in range(0,10):
    country_group.append(lines[total:total+inc])
    total+=inc
    if i <=3:
        inc+=1
    if i > 3:
        inc+=5
country_group.append(lines[total:])


# In[ ]:


def f(x,group):
    for elem in x:
        #print(elem,group)
        if elem in group:
            return True
    return False


# In[ ]:


def f2(x,group):
    for elem in x:
        #print(elem,group)
        if any(elem in s for s in group):
            return True
    return False


# In[ ]:


train['all_countries'] = train['production_countries'].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')
test['all_countries'] = test['production_countries'].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')
for i in range(len(country_group)):
    #train['country_group_' + str(i)] = train['all_countries'].apply(lambda x: 1 if x in country_group[i] else 0)
    train['country_group_' + str(i)] = train['production_countries'].apply(lambda x: 1 if f([j['name'] for j in x],country_group[i]) else 0)
    test['country_group_' + str(i)] = test['production_countries'].apply(lambda x: 1 if f([j['name'] for j in x],country_group[i]) else 0)


# In[ ]:


for i in range(len(country_group)):
    plt.scatter(train['country_group_'+str(i)].value_counts()[1],i)


# The countries were sorted based on the revenue generated by them. This sorted list were grouped based on the number of movies they had produced together, and after a few tries, it was found that apart from USA, which has produced slightly over 76%, the next 2 countries produced about 400 of the movies, and the next 3 movies after them produced another 450 movies and so on, so we group the countries in increasing number, starting from the first group being only USA, the second group being United Kingdom and China combined, and the 3rd group being France, Japan, Germany. Similarly, 10 groups were formed with the intention to group up countries with similar revenues generated.

# In[ ]:


file = open('../input/production-companies-and-countries/production_companies.txt','r')
lines = file.read().split('\n')
len(lines)
#last 27 - 1 group: 140 left, split to 14 groups
i = 0
print(len(lines))
company_group = []
inc = 4
total = 0
for i in range(0,8):
    company_group.append(lines[total:total+inc])
    total+=inc
    inc+=25
    if i >2:
        inc+=150
    if i >4:
        inc+=200
    if i >6:
        inc+=1500
company_group.append(lines[total:])
train['all_production_companies'] = train['production_companies'].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')
test['all_production_companies'] = test['production_companies'].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')


# In[ ]:


for i in range(len(company_group)):
    train['company_group_' + str(i)] = train['production_companies'].apply(lambda x: 1 if f([j['name'] for j in x],company_group[i]) else 0)
    test['company_group_' + str(i)] = test['production_companies'].apply(lambda x: 1 if f([j['name'] for j in x],company_group[i]) else 0)


# In[ ]:


for i in range(len(company_group)):
    plt.scatter(train['company_group_'+str(i)].value_counts()[1],i)


# Similarly, for production countries, we sorted the countries based on their revenue earned, and grouped them to have equal distributions of revenue per group.

# In[ ]:


train["release_date"]= pd.to_datetime(train["release_date"]) 
train['year'] = train['release_date'].apply(lambda x: x.year)
train['month'] = train['release_date'].apply(lambda x: x.month)
train['date'] = train['release_date'].apply(lambda x: x.day)
test["release_date"]= pd.to_datetime(test["release_date"]) 
test['year'] = test['release_date'].apply(lambda x: x.year)
test['month'] = test['release_date'].apply(lambda x: x.month)
test['date'] = test['release_date'].apply(lambda x: x.day)


# In[ ]:


train['all_languages'] = train['spoken_languages'].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')
for g in languages:
    train['language_' + g] = train['all_languages'].apply(lambda x: 1 if g in x else 0)
    
test['all_languages'] = test['spoken_languages'].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')
for g in languages:
    test['language_' + g] = test['all_languages'].apply(lambda x: 1 if g in x else 0)


# ### Date format is m/d/yy

# Status has only 2 types and only 4 examples for rumored. has minimal meaning. removing

# In[ ]:


train.status.unique()


# In[ ]:


temp = train[train['status'] == 'Rumored']


# In[ ]:


temp


# ## Status
# 
# It can either be Released or Rumored, with rumored being a part of only 4 of the rows, and having no difference wrt the other attributes. maybe dropping it.

# In[ ]:


print('Number of Cast members in films')
train['crew'].apply(lambda x: len(x) if x != {} else 0).value_counts()


# Too many casts to consider them all. We can only consider the most common casts among them all. For example, the 30 most commonly occuring names were:
# 

# In[ ]:


list_of_cast_names = list(train['cast'].apply(lambda x: [i['name'] for i in x] if x != {} else []).values)
Counter([i for j in list_of_cast_names for i in j]).most_common(30)


# In[ ]:



def transform_most_common(column):
    entire_list = list(train[column].apply(lambda x: [i['name'] for i in x] if x != {} else []).values)
    top_30 = [m[0] for m in Counter([i for j in entire_list for i in j]).most_common(30)]
    test['all_'+column] = test[column].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')
    train['all_'+column] = train[column].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')
    for g in top_30:
        train[column+'_'+ g] = train['all_'+column].apply(lambda x: 1 if g in x else 0)
        test[column+'_'+ g] = test['all_'+column].apply(lambda x: 1 if g in x else 0)
transform_most_common('Keywords')
transform_most_common('cast')
transform_most_common('crew')


# In[ ]:





# In[ ]:


train['cast_count'] = train['cast'].apply(lambda x: len(x) if x != {} else 0)
train['crew_count'] = train['crew'].apply(lambda x: len(x) if x != {} else 0)
train['spoken_languages_count'] = train['spoken_languages'].apply(lambda x: len(x) if x != {} else 0)

test['cast_count'] = test['cast'].apply(lambda x: len(x) if x != {} else 0)
test['crew_count'] = test['crew'].apply(lambda x: len(x) if x != {} else 0)
test['spoken_languages_count'] = test['spoken_languages'].apply(lambda x: len(x) if x != {} else 0)


# In[ ]:


train['crew_count'] = train['crew'].apply(lambda x: len(x) if x != {} else 0)


# In[ ]:


train['spoken_languages_count'] = train['spoken_languages'].apply(lambda x: len(x) if x != {} else 0)


# In[ ]:





# In[ ]:


# data fixes from https://www.kaggle.com/somang1418/happy-valentines-day-and-keep-kaggling-3
train.loc[train['id'] == 16,'revenue'] = 192864          # Skinning
train.loc[train['id'] == 90,'budget'] = 30000000         # Sommersby          
train.loc[train['id'] == 118,'budget'] = 60000000        # Wild Hogs
train.loc[train['id'] == 149,'budget'] = 18000000        # Beethoven
train.loc[train['id'] == 313,'revenue'] = 12000000       # The Cookout 
train.loc[train['id'] == 451,'revenue'] = 12000000       # Chasing Liberty
train.loc[train['id'] == 464,'budget'] = 20000000        # Parenthood
train.loc[train['id'] == 470,'budget'] = 13000000        # The Karate Kid, Part II
train.loc[train['id'] == 513,'budget'] = 930000          # From Prada to Nada
train.loc[train['id'] == 797,'budget'] = 8000000         # Welcome to Dongmakgol
train.loc[train['id'] == 819,'budget'] = 90000000        # Alvin and the Chipmunks: The Road Chip
train.loc[train['id'] == 850,'budget'] = 90000000        # Modern Times
train.loc[train['id'] == 1112,'budget'] = 7500000        # An Officer and a Gentleman
train.loc[train['id'] == 1131,'budget'] = 4300000        # Smokey and the Bandit   
train.loc[train['id'] == 1359,'budget'] = 10000000       # Stir Crazy 
train.loc[train['id'] == 1542,'budget'] = 1              # All at Once
train.loc[train['id'] == 1570,'budget'] = 15800000       # Crocodile Dundee II
train.loc[train['id'] == 1571,'budget'] = 4000000        # Lady and the Tramp
train.loc[train['id'] == 1714,'budget'] = 46000000       # The Recruit
train.loc[train['id'] == 1721,'budget'] = 17500000       # Cocoon
train.loc[train['id'] == 1865,'revenue'] = 25000000      # Scooby-Doo 2: Monsters Unleashed
train.loc[train['id'] == 2268,'budget'] = 17500000       # Madea Goes to Jail budget
train.loc[train['id'] == 2491,'revenue'] = 6800000       # Never Talk to Strangers
train.loc[train['id'] == 2602,'budget'] = 31000000       # Mr. Holland's Opus
train.loc[train['id'] == 2612,'budget'] = 15000000       # Field of Dreams
train.loc[train['id'] == 2696,'budget'] = 10000000       # Nurse 3-D
train.loc[train['id'] == 2801,'budget'] = 10000000       # Fracture
test.loc[test['id'] == 3889,'budget'] = 15000000       # Colossal
test.loc[test['id'] == 6733,'budget'] = 5000000        # The Big Sick
test.loc[test['id'] == 3197,'budget'] = 8000000        # High-Rise
test.loc[test['id'] == 6683,'budget'] = 50000000       # The Pink Panther 2
test.loc[test['id'] == 5704,'budget'] = 4300000        # French Connection II
test.loc[test['id'] == 6109,'budget'] = 281756         # Dogtooth
test.loc[test['id'] == 7242,'budget'] = 10000000       # Addams Family Values
test.loc[test['id'] == 7021,'budget'] = 17540562       #  Two Is a Family
test.loc[test['id'] == 5591,'budget'] = 4000000        # The Orphanage
test.loc[test['id'] == 4282,'budget'] = 20000000       # Big Top Pee-wee

power_six = train.id[train.budget > 1000][train.revenue < 100]

for k in power_six :
    train.loc[train['id'] == k,'revenue'] =  train.loc[train['id'] == k,'revenue'] * 1000000


# In[ ]:


train['log_budget'] = np.log1p(train['budget'])
test['log_budget'] = np.log1p(test['budget'])


# In[ ]:


col = ['id','all_genres','homepage',
       'imdb_id', 'original_language', 'original_title', 'overview',
       'poster_path', 'production_companies',
       'production_countries', 'release_date', 'spoken_languages',
       'status', 'tagline', 'title', 'Keywords', 'cast', 'crew','all_crew','all_cast','all_Keywords','all_languages','all_production_companies','all_countries']


# In[ ]:





# In[ ]:


X = train.drop(col, axis = 1)
X = X.drop(['revenue','budget'],axis = 1)
y = np.log1p(train['revenue'])


# In[ ]:


X =X.fillna(0)
X.head()


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


y=y.astype('int')
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=0)


# In[ ]:


import xgboost as xgb


# In[ ]:


params =  {'eta': 0.005,
              'objective': 'reg:linear',
              'max_depth': 10,
              'subsample': 0.8,
              'colsample_bytree': 0.5,
              'eval_metric': 'rmse',
              'seed': 11,
              'silent': True}


# In[ ]:


train_data = xgb.DMatrix(data=X_train.values, label=y_train)
valid_data = xgb.DMatrix(data=X_valid.values, label=y_valid)

watchlist = [(train_data, 'train'), (valid_data, 'valid_data')]
model = xgb.train(dtrain=train_data, num_boost_round=20000, evals=watchlist, early_stopping_rounds=200, verbose_eval=500, params=params)
y_pred_valid = model.predict(xgb.DMatrix(X_valid.values), ntree_limit=model.best_ntree_limit)


# In[ ]:


X_test = test.drop(col,axis = 1,inplace = True)
X_test = test.drop('budget', axis = 1)
X_test = X_test.fillna(0)
X_test.head()


# In[ ]:


y_final = model.predict(xgb.DMatrix(X_test.values), ntree_limit=model.best_ntree_limit)


# In[ ]:


sub = pd.read_csv('../input/tmdb-box-office-prediction/sample_submission.csv')


# In[ ]:


sub['revenue'] = np.expm1(y_final)


# In[ ]:


sub.to_csv("final.csv", index=False)

