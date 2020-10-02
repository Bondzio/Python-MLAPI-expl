#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('ggplot')
import seaborn as sns


import plotly
import os, json, time, datetime
import lightgbm as lgb
import xgboost as xgb
from PIL import Image
from wordcloud import WordCloud

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.metrics import mean_squared_error, roc_auc_score
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
import gc
from catboost import CatBoostClassifier
from tqdm import tqdm_notebook
import plotly.offline as py
py.init_notebook_mode(connected = True)
import plotly.graph_objs as go
import plotly.tools as tls
import random, warnings
warnings.filterwarnings("ignore")

from functools import partial
pd.set_option('max_colwidth',500)
pd.set_option('max_columns',500)
pd.set_option('max_rows', 100)

import scipy as sp
from math import sqrt
from collections import Counter
from sklearn.metrics import confusion_matrix as sk_cmatrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.tokenize import TweetTokenizer

import langdetect, eli5
from IPython.display import display

from sklearn.metrics import cohen_kappa_score
def kappa(y_true, y_pred):
    return cohen_kappa_score(y_true, y_pred,weights ='quadratic')


# In[ ]:


get_ipython().system('ls ../input/petfinder-adoption-prediction/')
#or
print(os.listdir("../input/petfinder-adoption-prediction/train"))


# In[ ]:


breeds = pd.read_csv("../input/petfinder-adoption-prediction/breed_labels.csv")
color = pd.read_csv("../input/petfinder-adoption-prediction/color_labels.csv")
state = pd.read_csv("../input/petfinder-adoption-prediction/state_labels.csv")

train = pd.read_csv("../input/petfinder-adoption-prediction/train/train.csv")
test = pd.read_csv("../input/petfinder-adoption-prediction/test/test.csv")
sub = pd.read_csv("../input/petfinder-adoption-prediction/test/sample_submission.csv")

train['dataset_type']='train'
test['dataset_type'] = 'test'
all_data = pd.concat([train, test])


# In[ ]:


train.drop('Description', axis=1).head(5)


# In[ ]:


train.info()


# In[ ]:


train.shape


# In[ ]:


# target column is AdoptionSpeed

train['AdoptionSpeed'].value_counts().sort_index().plot('barh',color = 'teal');
plt.title('Adoption Speed class counts')


# In[ ]:


plt.figure(figsize= (14,5))
g = sns.countplot(x ='AdoptionSpeed', data = all_data.loc[all_data['dataset_type']=='train'])
plt.title('Adoption Speed classes rate')
ax = g.axes


# In[ ]:


ax


# In[ ]:


ax.patches


# In[ ]:


ax.patches[2].get_width()


# In[ ]:


plt.figure(figsize=(14,7))
g = sns.countplot(x='AdoptionSpeed', data = all_data.loc[all_data['dataset_type']=='train'])
plt.title('Adoption Speed classes rates')
ax = g.axes
for p in ax.patches:
    ax.annotate(f"{p.get_height() * 100 / train.shape[0]:.2f}%", 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha ='center', va='center', fontsize = 11, color = 'gray', rotation = 0, 
                xytext = (0,10),
                textcoords = 'offset points'
               )
    


# In[ ]:


for p in ax.patches:
    print(f"{p.get_height() * 100 / train.shape[0]:.2f}%", 
                (p.get_x() + p.get_width()/2., p.get_height()))


# In[ ]:


# Type
all_data['Type'].value_counts()


# In[ ]:


all_data['Type'] = all_data['Type'].apply(lambda x : 'Dog' if x==1 else 'Cat')


# In[ ]:


plt.figure(figsize = (10,5))
sns.countplot(x = 'dataset_type', data = all_data, hue ='Type')
plt.title('Distribution of Dogs and Cats in training and test set')


# In[ ]:


all_data.loc[(all_data['Type']=='Cat') &  (all_data['dataset_type']=='train')].shape


# In[ ]:


all_data.loc[(all_data['Type']=='Cat') &  (all_data['dataset_type']=='train') &
            (all_data['AdoptionSpeed']==0)].shape


# In[ ]:


main_count = train['AdoptionSpeed'].value_counts(normalize=True).sort_index()


# In[ ]:


def prepare_plot_dict(df, col, main_count):
    main_count = dict(main_count)
    plot_dict = {}
    for i in df[col].unique():
        val_count = dict(df.loc[df[col]==i,'AdoptionSpeed'].value_counts().sort_index())
        
        for k, v in main_count.items():
            if k in val_count:
                plot_dict[val_count[k]] = ((val_count[k] / sum(val_count.values())) / main_count[k]) *100 -100
            else:
                plot_dict[0] = 0
    return plot_dict


# In[ ]:


def make_count_plot(df, x, hue ='AdoptionSpeed', title ='', main_count = main_count):
    g = sns.countplot(x = x, data = df, hue = hue)
    plt.title(f"AdoptionSpeed {title}")
    ax = g.axes
    
    plot_dict = prepare_plot_dict(df, x, main_count)
    
    for p in ax.patches:
        h = p.get_height() if str(p.get_height()) != 'nan' else 0
        text = f"{plot_dict[h]:.0f}%" if plot_dict[h] <0 else f"+{plot_dict[h]:.0f}%"
        ax.annotate(text, (p.get_x() + p.get_width()/2., h),
                    ha ='center', va='center', fontsize = 11, color ='green' if plot_dict[h]>0 else 'red',
                    rotation =0, xytext =(0,10),
                    textcoords = 'offset points'
                   )


# In[ ]:


plt.figure(figsize =(10,5))
make_count_plot(df = all_data.loc[all_data['dataset_type']=='train'], x = 'Type', title ='By pet type')


# In[ ]:


## Cat and dog names wordcloud

fig, ax = plt.subplots(figsize = (16,12))
plt.subplot(1,2,1)
text_cat = ' '.join(all_data.loc[all_data['Type']=='Cat','Name'].fillna('').values)
wordcloud = WordCloud(max_font_size = None, background_color= 'black', width = 1200, height = 1000).generate(text_cat)
plt.imshow(wordcloud)
plt.title('Cat Names')
plt.axis('off')

plt.subplot(1,2,2)
text_dog = ' '.join(all_data.loc[all_data['Type']=='Dog','Name'].fillna('').values)
wordcloud = WordCloud(max_font_size=None, background_color='black', width =1200, height =1000).generate(text_dog)
plt.imshow(wordcloud)
plt.title('Dog Names')
plt.axis('off')

plt.show()


# In[ ]:


print("Most popular pet names and Adoption speed")
for n in train['Name'].value_counts().index[:5]:
    print(n)
    print(train.loc[train['Name']==n,'AdoptionSpeed'].value_counts().sort_index())
    print("")
    


# In[ ]:


##unnamed pets
train['Name'] = train['Name'].fillna('unnamed')
test['Name'] = test['Name'].fillna('unnamed')
all_data['Name'] = all_data['Name'].fillna('unnamed')

train['No_name'] = 0
train.loc[train['Name']=='unnamed','No_name'] = 1
test['No_name'] =0
test.loc[test['Name']=='unnamed','No_name'] = 1
all_data['No_name'] = 0
all_data.loc[all_data['Name']=='unnamed','No_name'] = 1

print(f"Rate of unnamed pets in training dataset : {train['No_name'].sum()*100 / train['No_name'].shape[0]:.2f}%")
print(f"Rate of unnamed pets in test dataset : {test['No_name'].sum() *100 / test['No_name'].shape[0]:.2f}%")
      


# In[ ]:


pd.crosstab(train['No_name'], train['AdoptionSpeed'], normalize = 'index')


# In[ ]:


plt.figure(figsize = (10,5))
make_count_plot(df = all_data.loc[all_data['dataset_type']=='train'], x = 'No_name', title='and having a name')


# In[ ]:


# short character names

all_data[all_data['Name'].apply(lambda x: len(str(x))==3)]['Name'].value_counts().tail()


# In[ ]:


# less than 3 character names

all_data[all_data['Name'].apply(lambda x : len(str(x))<3)]['Name'].unique()


# In[ ]:


# Age plot

fig, ax = plt.subplots(figsize = (16,6))
plt.subplot(1,2,1)
plt.title('Distribution of pets age')
train['Age'].plot('hist', label = 'train')
test['Age'].plot('hist', label='test')
plt.legend()

plt.subplot(1,2,2)
plt.title('Distribution of pets age(log)')
np.log1p(train['Age']).plot('hist', label='train')
np.log1p(test['Age']).plot('hist', label = 'test')
plt.legend()


# In[ ]:


train['Age'].value_counts().head()


# In[ ]:


plt.figure(figsize = (10,5))
sns.violinplot(x = 'AdoptionSpeed', y='Age', hue='Type', data= train)
plt.title('Adoptionspeed by age and type')


# In[ ]:


data = []
for a in range(5):
    df = train.loc[train['AdoptionSpeed'] == a]

    data.append(go.Scatter(
        x = df['Age'].value_counts().sort_index().index,
        y = df['Age'].value_counts().sort_index().values,
        name = str(a)
    ))
    
layout = go.Layout(dict(title = "AdoptionSpeed trends by Age",
                  xaxis = dict(title = 'Age (months)'),
                  yaxis = dict(title = 'Counts'),
                  )
                  )
py.iplot(dict(data=data, layout=layout), filename='basic-line')


# In[ ]:


# Breeds

train['Pure_breed'] =0 
train.loc[train['Breed2']==0,'Pure_breed'] = 1
test['Pure_breed']=0
test.loc[test['Breed2']==0, 'Pure_breed']=1
all_data['Pure_breed']=0
all_data.loc[all_data['Breed2']==0, 'Pure_breed'] = 1

print(f"Rate of pure breed pets in training set : {train['Pure_breed'].sum() *100 / train['Pure_breed'].shape[0]:.2f}%")
print(f"Rate of pure breed pets in training set : {test['Pure_breed'].sum() *100 / test['Pure_breed'].shape[0]:.2f}%")


# In[ ]:


def plot_four_graphs(col='', main_title='', dataset_title=''):
    """
    Plotting four graphs:
    - adoption speed by variable;
    - counts of categories in the variable in train and test;
    - adoption speed by variable for dogs;
    - adoption speed by variable for cats;    
    """
    plt.figure(figsize=(20, 12));
    plt.subplot(2, 2, 1)
    make_count_plot(df=train, x=col, title=f'and {main_title}')

    plt.subplot(2, 2, 2)
    sns.countplot(x='dataset_type', data=all_data, hue=col);
    plt.title(dataset_title);

    plt.subplot(2, 2, 3)
    make_count_plot(df=train.loc[train['Type'] == 1], x=col, title=f'and {main_title} for dogs')

    plt.subplot(2, 2, 4)
    make_count_plot(df=train.loc[train['Type'] == 2], x=col, title=f'and {main_title} for cats')
    
plot_four_graphs(col='Pure_breed', main_title='having pure breed', dataset_title='Number of pets by pure/not-pure breed in train and test data')


# In[ ]:


breeds_dict = {k:v for k,v in zip(breeds['BreedID'], breeds['BreedName'])}


# In[ ]:


train['Breed1_name'] = train['Breed1'].apply(lambda x : '_'.join(breeds_dict[x].split()) 
                                             if x in breeds_dict else ' Unknown')
train['Breed2_name'] = train['Breed2'].apply(lambda x : '_'.join(breeds_dict[x].split()) 
                                             if x in breeds_dict else '-')

test['Breed1_name'] = test['Breed1'].apply(lambda x : '_'.join(breeds_dict[x].split()) 
                                           if x in breeds_dict else 'Unknown')
test['Breed2_name'] = test['Breed2'].apply(lambda x : '_'.join(breeds_dict[x].split()) 
                                           if x in breeds_dict else '-')

all_data['Breed1_name'] = all_data['Breed1'].apply(lambda x : '_'.join(breeds_dict[x].split())
                                                  if x in breeds_dict else 'Unknown')
all_data['Breed2_name'] = all_data['Breed2'].apply(lambda x : '_'.join(breeds_dict[x].split())
                                                  if x in breeds_dict else '-')


# In[ ]:


fig, ax = plt.subplots(figsize = (20,12))
plt.subplot(2,2,1)
plt.title('Top cat breed1')
text_cat1 = ' '.join(all_data.loc[all_data['Type']=='Cat','Breed1_name'].fillna('').values)
wordcloud = WordCloud(max_font_size=None, background_color='White', collocations=False, width =1200, 
                     height = 1000).generate(text_cat1)
plt.imshow(wordcloud)
plt.axis('off')

plt.subplot(2,2,2)
plt.title('Top cat breed2')
text_cat2 = ' '.join(all_data.loc[all_data['Type']=='Cat', 'Breed2_name'].fillna('').values)
wordcloud = WordCloud(max_font_size=None, background_color='White', collocations=False,
                     width = 1200, height =1000).generate(text_cat2)
plt.imshow(wordcloud)
plt.axis('off')

plt.subplot(2,2,3)
plt.title('Top dog breed1')
text_dog1 = ' '.join(all_data.loc[all_data['Type']=='Dog', 'Breed1_name'].fillna('').values)
wordcloud = WordCloud(max_font_size=None, background_color='White', collocations=False,
                     width = 1200, height = 1000).generate(text_dog1)
plt.imshow(wordcloud)
plt.axis('off')

plt.subplot(2,2,4)
plt.title('Top dog breed2')
text_dog2 = ' '.join(all_data.loc[all_data['Type']=='Dog','Breed2_name'].fillna('').values)
wordcloud = WordCloud(max_font_size=None, background_color='White', collocations=False,
                     width = 1200, height = 1000).generate(text_dog2)
plt.imshow(wordcloud)
plt.axis('off')


# In[ ]:


(all_data['Breed1_name']+ "__" + all_data["Breed2_name"]).value_counts().head(15)


# In[ ]:


# Gender
#1 = Male, 2 =Female, 3 = group of pets

plt.figure(figsize = (18,6))
plt.subplot(1,2,1)
make_count_plot(df = train, x ='Gender', title= 'and gender')

plt.subplot(1,2,2)
sns.countplot(x = 'dataset_type', data = all_data, hue ='Gender')
plt.title('Number of pets by gender and type')


# In[ ]:


sns.factorplot(x='Type', hue = 'Gender', data = all_data, kind ='count', col ='dataset_type')
plt.subplots_adjust(top=0.8)
plt.suptitle("Count of cats and dogs by Gender and type")


# In[ ]:


# Colors
colors_dict = { k: v for k, v in zip(color['ColorID'], color['ColorName'])}

train['Color1_name'] = train['Color1'].apply(lambda x : colors_dict[x] if x in colors_dict else '')
train['Color2_name'] = train['Color2'].apply(lambda x : colors_dict[x] if x in colors_dict else '')
train['Color3_name'] = train['Color3'].apply(lambda x : colors_dict[x] if x in colors_dict else '') 

test['Color1_name'] = test['Color1'].apply(lambda x : colors_dict[x] if x in colors_dict else '')
test['Color2_name'] = test['Color2'].apply(lambda x : colors_dict[x] if x in colors_dict else '')
test['Color3_name'] = test['Color3'].apply(lambda x : colors_dict[x] if x in colors_dict else '') 

all_data['Color1_name'] = all_data['Color1'].apply(lambda x : colors_dict[x] if x in colors_dict else '')
all_data['Color2_name'] = all_data['Color2'].apply(lambda x : colors_dict[x] if x in colors_dict else '')
all_data['Color3_name'] = all_data['Color3'].apply(lambda x : colors_dict[x] if x in colors_dict else '') 


# In[ ]:


def make_factor_plot(df, x, col, title, main_count=main_count, hue=None, ann=True, col_wrap=4):
    if hue:
        g = sns.factorplot(col, col = x, data = df, kind ='count', hue = hue, col_wrap = col_wrap)
    else:
        g = sns.factorplot(col, col=x, data = df, kind ='count', col_wrap = col_wrap)
        
    plt.subplots_adjust(top = 0.8)
    plt.suptitle(title)
    ax = g.axes
    plot_dict = prepare_plot_dict(df, x, main_count)
    if ann:
        for a in ax:
            for p in a.patches:
                text = f"{plot_dict[p.get_height()]:.0f}%" if plot_dict[p.get_height()] < 0 else f"+{plot_dict[p.get_height()]:.0f}%"
                a.annotate(text, (p.get_x() +p.get_width()/2., p.get_height()),ha='center',
                           va='center', fontsize = 11, rotation=0, color ='green' if plot_dict[p.get_height()] >0
                           else 'red' , xytext = (0,10), textcoords ='offset points')
                
                
                                


# In[ ]:


sns.factorplot('dataset_type',col = 'Type',data = all_data, kind ='count',  hue = 'Color1_name',
               palette = ['Black', 'Brown', '#FFFDD0', 'Gray', 'Gold', 'White', 'Yellow'])
plt.subplots_adjust(top=0.9)
plt.suptitle('Count of pets by main color')


# In[ ]:


make_factor_plot(df = train, x ='Color1_name', col='AdoptionSpeed', title ='Count of pet colors by adoption speed')


# In[ ]:


train['fullcolor'] = (train['Color1_name']+"__"+train['Color2_name']+"__"+train['Color3_name']).str.replace("__","")
test['fullcolor'] = (test['Color1_name']+"__"+test['Color2_name']+"__"+test['Color3_name']).str.replace("__","")
all_data['fullcolor'] = (all_data['Color1_name']+"__"+all_data['Color2_name']+"__"+all_data['Color3_name']).str.replace("__","")


# In[ ]:


make_factor_plot(df = train.loc[train['fullcolor'].isin(list(train['fullcolor'].value_counts().index)[:12])],
                 x='fullcolor', col ='AdoptionSpeed', title='Counts of pets by color and Adoption speed')


# In[ ]:


gender_dict = {1:'Male',2 :'Female',3:'Mixed'}
for i in all_data['Type'].unique():
    for j in all_data['Gender'].unique():
        df = all_data.loc[(all_data['Type']==i) & (all_data['Gender']==j)]
        top_colors = list(df['fullcolor'].value_counts().index)[:5]
        j = gender_dict[j]
        print(f"Most popular colors in {j} {i}s: {' '.join(top_colors)}")


# MaturitySize
# 
# 1. Size at maturity (1 = Small, 2 = Medium, 3 = Large, 4 = Extra Large, 0 = Not Specified)

# In[ ]:


plot_four_graphs(col='MaturitySize', main_title='MaturitySize', dataset_title='Number of pets by MaturitySize in train and test data')


# In[ ]:


make_factor_plot(df=all_data, x='MaturitySize', col='Type', title='Count of cats and dogs in train and test set by MaturitySize', hue='dataset_type', ann=False)


# In[ ]:


images =  [i.split('-')[0] for i in os.listdir('../input/petfinder-adoption-prediction/train_images/')]


# In[ ]:


images = [i.split('-')[0] for i in os.listdir('../input/petfinder-adoption-prediction/train_images/')]
size_dict = {1: 'Small', 2: 'Medium', 3: 'Large', 4: 'Extra Large'}
for t in all_data['Type'].unique():
    for m in all_data['MaturitySize'].unique():
        df = all_data.loc[(all_data['Type'] == t) & (all_data['MaturitySize'] == m)]
        top_breeds = list(df['Breed1_name'].value_counts().index)[:5]
        m = size_dict[m]
        print(f"Most common Breeds of {m} {t}s:")
        
        fig = plt.figure(figsize=(25, 4))
        
        for i, breed in enumerate(top_breeds):
            # excluding pets without pictures
            b_df = df.loc[(df['Breed1_name'] == breed) & (df['PetID'].isin(images)), 'PetID']
            if len(b_df) > 1:
                pet_id = b_df.values[1]
            #else:
             #   pet_id = b_df.values[0]
            ax = fig.add_subplot(1, 5, i+1, xticks=[], yticks=[])

            im = Image.open("../input/petfinder-adoption-prediction/train_images/" + pet_id + '-1.jpg')
            plt.imshow(im)
            ax.set_title(f'Breed: {breed}')
        plt.show();


# In[ ]:


# Furlength
#(1 = Short, 2 = Medium, 3 = Long, 0 = Not Specified)
plot_four_graphs(col='FurLength', main_title='FurLength', dataset_title='Number of pets by FurLength in train and test data')


# In[ ]:


fig,ax = plt.subplots(figsize = (20,12))
plt.subplot(2,2,1)
text_cat1 = ' '.join(all_data.loc[(all_data['FurLength']==1) & (all_data['Type']=='Cat'),'Breed1_name'].fillna('').values)
wordcloud = WordCloud(max_font_size=None, background_color ='Black', width = 1200, height=1000).generate(text_cat1)
plt.imshow(wordcloud)
plt.title('Top cat breed1 with short fur')
plt.axis('off')

plt.subplot(2,2,2)
text_dog1 = ' '.join(all_data.loc[(all_data['FurLength']==1) &(all_data['Type']=='Dog'),'Breed1_name'].fillna('').values)
wordcloud = WordCloud(max_font_size=None, background_color ='Black', width = 1200, height=1000).generate(text_cat1)
plt.imshow(wordcloud)
plt.title('Top dog breed1 with short fur')
plt.axis('off')

plt.subplot(2,2,3)
text_cat1 = ' '.join(all_data.loc[(all_data['FurLength']==2) & (all_data['Type']=='Cat'),'Breed1_name'].fillna('').values)
wordcloud = WordCloud(max_font_size=None, background_color ='Black', width = 1200, height=1000).generate(text_cat1)
plt.imshow(wordcloud)
plt.title('Top cat breed1 with medium fur')
plt.axis('off')

plt.subplot(2,2,4)
text_dog1 = ' '.join(all_data.loc[(all_data['FurLength']==2) &(all_data['Type']=='Dog'),'Breed1_name'].fillna('').values)
wordcloud = WordCloud(max_font_size=None, background_color ='Black', width = 1200, height=1000).generate(text_cat1)
plt.imshow(wordcloud)
plt.title('Top dog breed1 with medium fur')
plt.axis('off')

plt.show()


# In[ ]:


## strange pets

c= 0 
strange_pets= []

for i, row in all_data[all_data['Breed1_name'].str.contains('air')].iterrows():
    if 'Short' in row['Breed1_name'] and row['FurLength'] == 1:
        pass
    elif 'Medium' in row['Breed1_name'] and row['FurLength'] == 2:
        pass
    elif 'High' in row['Breed1_name'] and row['FurLength'] == 3:
        pass
    else:
        c+=1
        strange_pets.append((row['PetID'], row['Breed1_name'], row['FurLength']))
    
print(f"There are {c} pets whose breed and fur length is not matched")
                                                                   
                    


# In[ ]:



strange_pets = [p for p in strange_pets if p[0] in images]
fig = plt.figure(figsize = (25,12))
fur_dict = {1:'Short',2:'Medium',3:'Long'}
for i,s in enumerate(random.sample(strange_pets, 12)):
    ax = fig.add_subplot(3,4,i+1, xticks=[], yticks =[])
    im = Image.open("../input/petfinder-adoption-prediction/train_images/"+s[0]+'-1.jpg')
    plt.imshow(im)
    ax.set_title(f'Breed:{s[1]}\n FurLength:{fur_dict[s[2]]}')

plt.show()


# In[ ]:


plt.figure(figsize=(20,10))
plt.subplot(2,2,1)
make_count_plot(df = train,x ='Vaccinated', title='Vaccinated' )
plt.xticks([0,1,2],['Yes','No','Not sure'])
plt.title('AdoptionSpeed and Vaccinated')

plt.subplot(2,2,2)
make_count_plot(df= train, x ='Dewormed',title = 'Dewormed')
plt.xticks([0,1,2],['Yes','No','Not sure'])
plt.title('AdoptionSpeed and Dewormed')

plt.subplot(2,2,3)
make_count_plot(df= train, x ='Sterilized',title = 'Sterilized')
plt.xticks([0,1,2],['Yes','No','Not sure'])
plt.title('AdoptionSpeed and Sterilized')

plt.subplot(2,2,4)
make_count_plot(df= train, x ='Health',title = 'Health')
plt.xticks([0,1,2],['Healthy', 'Minor Injury', 'Serious Injury'])
plt.title('AdoptionSpeed and Healthy')

plt.suptitle('Adoption Speed and health conditions')


# In[ ]:


train['health'] = train['Vaccinated'].astype('str')+'_'+train['Dewormed'].astype('str')+'_'+train['Sterilized'].astype('str')+'_'+train['Health'].astype('str')
test['health'] = train['Vaccinated'].astype('str')+'_'+train['Dewormed'].astype('str')+'_'+train['Sterilized'].astype('str')+'_'+train['Health'].astype('str')
    
make_factor_plot(df=train.loc[train['health'].isin(list(train.health.value_counts().index[:5]))], x='health', col='AdoptionSpeed', title='Counts of pets by main health conditions and Adoption Speed')


# In[ ]:


plt.figure(figsize =(15,10))
plt.subplot(3,2,1)
sns.violinplot(x='AdoptionSpeed', y='Age',data = train)
plt.title('Adoption speed distribution by age')

plt.subplot(3,2,2)
sns.violinplot(x= 'AdoptionSpeed', y='Age', hue ='Vaccinated', data= train)
plt.title('Adoption speed distribution by age and vaccinated')

plt.subplot(3,2,3)
sns.violinplot(x= 'AdoptionSpeed', y='Age', hue ='Dewormed', data= train)
plt.title('Adoption speed distribution by age and Dewormed')

plt.subplot(3,2,4)
sns.violinplot(x= 'AdoptionSpeed', y='Age', hue ='Sterilized', data= train)
plt.title('Adoption speed distribution by age and Sterilized')

plt.subplot(3,2,5)
sns.violinplot(x= 'AdoptionSpeed', y='Age', hue ='Health', data= train)
plt.title('Adoption speed distribution by age and Health')


# In[ ]:


train.loc[train['Quantity']>11][['Name','Description', 'Quantity','AdoptionSpeed']].head(10)


# In[ ]:


train['Quantity'].value_counts().head(10)


# In[ ]:


train['Quantity_short'] = train['Quantity'].apply(lambda x : x if x<=5 else 6)
test['Quantity_short'] = test['Quantity'].apply(lambda x:x if x<=5 else 6)
all_data['Quantity_short'] = test['Quantity'].apply(lambda x: x if x<=5 else 6)

plot_four_graphs(col='Quantity_short', main_title='Quantity_short', dataset_title ='Number of pets by quantity short in train and test set')


# In[ ]:


# fee
train['Free'] = train['Fee'].apply(lambda x: 'Free' if x == 0 else 'Not Free')
test['Free'] = test['Fee'].apply(lambda x: 'Free' if x == 0 else 'Not Free')
all_data['Free'] = all_data['Fee'].apply(lambda x: 'Free' if x == 0 else 'Not Free')
plot_four_graphs(col='Free', main_title='Free', dataset_title='Number of pets by Free in train and test data')


# In[ ]:


all_data.sort_values('Fee', ascending = False)[['Name','Description','Fee','AdoptionSpeed','dataset_type']].head(10)


# In[ ]:


plt.figure(figsize=(16, 6));
plt.subplot(1, 2, 1)
plt.hist(train.loc[train['Fee'] < 400, 'Fee']);
plt.title('Distribution of fees lower than 400');

plt.subplot(1, 2, 2)
sns.violinplot(x="AdoptionSpeed", y="Fee", hue="Type", data=train);
plt.title('AdoptionSpeed by Type and Fee');


# In[ ]:


plt.figure(figsize=(16, 10));
sns.scatterplot(x="Fee", y="Quantity", hue="Type",data=all_data);
plt.title('Quantity of pets and Fee');


# In[ ]:


#state
states_dict = {k: v for k, v in zip(state['StateID'], state['StateName'])}
train['State_name'] = train['State'].apply(lambda x: '_'.join(states_dict[x].split()) if x in states_dict else 'Unknown')
test['State_name'] = test['State'].apply(lambda x: '_'.join(states_dict[x].split()) if x in states_dict else 'Unknown')
all_data['State_name'] = all_data['State'].apply(lambda x: '_'.join(states_dict[x].split()) if x in states_dict else 'Unknown')


# In[ ]:


all_data['State_name'].value_counts(normalize=True).head()


# In[ ]:


make_factor_plot(df=train.loc[train['State_name'].isin(list(train.State_name.value_counts().index[:3]))], x='State_name', col='AdoptionSpeed', title='Counts of pets by states and Adoption Speed')


# In[ ]:


#rescuer
all_data['RescuerID'].value_counts().head()


# In[ ]:


make_factor_plot(df=train.loc[train['RescuerID'].isin(list(train.RescuerID.value_counts().index[:5]))], x='RescuerID', col='AdoptionSpeed', title='Counts of pets by rescuers and Adoption Speed', col_wrap=5)


# In[ ]:


train['VideoAmt'].value_counts()


# In[ ]:


print(F'Maximum amount of photos in {train["PhotoAmt"].max()}')
train['PhotoAmt'].value_counts().head()


# In[ ]:


make_factor_plot(df=train.loc[train['PhotoAmt'].isin(list(train.PhotoAmt.value_counts().index[:5]))], x='PhotoAmt', col='AdoptionSpeed', title='Counts of pets by PhotoAmt and Adoption Speed', col_wrap=5)


# In[ ]:


plt.figure(figsize=(16, 6));
plt.subplot(1, 2, 1)
plt.hist(train['PhotoAmt']);
plt.title('Distribution of PhotoAmt');

plt.subplot(1, 2, 2)
sns.violinplot(x="AdoptionSpeed", y="PhotoAmt", hue="Type", data=train);
plt.title('AdoptionSpeed by Type and PhotoAmt');


# In[ ]:


#Description
fig, ax = plt.subplots(figsize = (12, 8))
text_cat = ' '.join(all_data['Description'].fillna('').values)
wordcloud = WordCloud(max_font_size=None, background_color='white',
                      width=1200, height=1000).generate(text_cat)
plt.imshow(wordcloud)
plt.title('Top words in description');
plt.axis("off");


# In[ ]:


tokenizer = TweetTokenizer()
vectorizer = TfidfVectorizer(ngram_range=(1, 2), tokenizer=tokenizer.tokenize)

vectorizer.fit(all_data['Description'].fillna('').values)
X_train = vectorizer.transform(train['Description'].fillna(''))

rf = RandomForestClassifier(n_estimators=20)
rf.fit(X_train, train['AdoptionSpeed'])


# In[ ]:


for i in range(5):
    print(f'Example of Adoption speed {i}')
    text = train.loc[train['AdoptionSpeed'] == i, 'Description'].values[0]
    print(text)
    display(eli5.show_prediction(rf, doc=text, vec=vectorizer, top=10))


# In[ ]:


train['Description'] = train['Description'].fillna('')
test['Description'] = test['Description'].fillna('')
all_data['Description'] = all_data['Description'].fillna('')

train['desc_length'] = train['Description'].apply(lambda x: len(x))
train['desc_words'] = train['Description'].apply(lambda x: len(x.split()))

test['desc_length'] = test['Description'].apply(lambda x: len(x))
test['desc_words'] = test['Description'].apply(lambda x: len(x.split()))

all_data['desc_length'] = all_data['Description'].apply(lambda x: len(x))
all_data['desc_words'] = all_data['Description'].apply(lambda x: len(x.split()))

train['averate_word_length'] = train['desc_length'] / train['desc_words']
test['averate_word_length'] = test['desc_length'] / test['desc_words']
all_data['averate_word_length'] = all_data['desc_length'] / all_data['desc_words']


# In[ ]:


plt.figure(figsize=(16, 6));
plt.subplot(1, 2, 1)
sns.violinplot(x="AdoptionSpeed", y="desc_length", hue="Type", data=train);
plt.title('AdoptionSpeed by Type and description length');

plt.subplot(1, 2, 2)
sns.violinplot(x="AdoptionSpeed", y="desc_words", hue="Type", data=train);
plt.title('AdoptionSpeed by Type and count of words in description');


# In[ ]:


# Sentiment
sentiment_dict = {}
for filename in os.listdir('../input/petfinder-adoption-prediction/train_sentiment/'):
    with open('../input/petfinder-adoption-prediction/train_sentiment/' + filename, 'r') as f:
        sentiment = json.load(f)
    pet_id = filename.split('.')[0]
    sentiment_dict[pet_id] = {}
    sentiment_dict[pet_id]['magnitude'] = sentiment['documentSentiment']['magnitude']
    sentiment_dict[pet_id]['score'] = sentiment['documentSentiment']['score']
    sentiment_dict[pet_id]['language'] = sentiment['language']

for filename in os.listdir('../input/petfinder-adoption-prediction/test_sentiment/'):
    with open('../input/petfinder-adoption-prediction/test_sentiment/' + filename, 'r') as f:
        sentiment = json.load(f)
    pet_id = filename.split('.')[0]
    sentiment_dict[pet_id] = {}
    sentiment_dict[pet_id]['magnitude'] = sentiment['documentSentiment']['magnitude']
    sentiment_dict[pet_id]['score'] = sentiment['documentSentiment']['score']
    sentiment_dict[pet_id]['language'] = sentiment['language']


# In[ ]:


train['lang'] = train['PetID'].apply(lambda x : sentiment_dict[x]['language'] if x in sentiment_dict else 'no')
train['magnitude'] = train['PetID'].apply(lambda x : sentiment_dict[x]['magnitude'] if x in sentiment_dict else 0)
train['score'] = train['PetID'].apply(lambda x : sentiment_dict[x]['score'] if x in sentiment_dict else 0)


test['lang'] = test['PetID'].apply(lambda x : sentiment_dict[x]['language'] if x in sentiment_dict else 'no')
test['magnitude'] = test['PetID'].apply(lambda x : sentiment_dict[x]['magnitude'] if x in sentiment_dict else 0)
test['score'] = test['PetID'].apply(lambda x : sentiment_dict[x]['score'] if x in sentiment_dict else 0)

all_data['lang'] = all_data['PetID'].apply(lambda x : sentiment_dict[x]['language'] if x in sentiment_dict else 'no')
all_data['magnitude'] = all_data['PetID'].apply(lambda x : sentiment_dict[x]['magnitude'] if x in sentiment_dict else 0)
all_data['score'] = all_data['PetID'].apply(lambda x : sentiment_dict[x]['score'] if x in sentiment_dict else 0)


# In[ ]:


plot_four_graphs(col='lang', main_title='lang', dataset_title='Number of pets by lang in train and test data')


# In[ ]:


plt.figure(figsize = (15,6))
plt.subplot(1,2,1)
sns.violinplot(x ='AdoptionSpeed', y='score', hue='Type',data=train)
plt.title('Adoption speed distribuiton by sentiment score and type')

plt.subplot(1,2,2)
sns.violinplot(x ='AdoptionSpeed', y='magnitude', hue='Type',data=train)
plt.title('Adoption speed distribuiton by sentiment magnitude and type')


# In[ ]:


# Baseline model

cols_to_use = ['Type', 'Age', 'Breed1', 'Breed2', 'Gender', 'Color1', 'Color2',
       'Color3', 'MaturitySize', 'FurLength', 'Vaccinated', 'Dewormed',
       'Sterilized', 'Health', 'Quantity', 'Fee', 'State', 'RescuerID', 'health', 'Free', 'score',
       'VideoAmt', 'PhotoAmt', 'AdoptionSpeed', 'No_name', 'Pure_breed', 'desc_length', 'desc_words', 'averate_word_length', 'magnitude']

train = train[[cols for cols in cols_to_use if cols in train.columns]]
test = test[[cols for cols in cols_to_use if cols in test.columns]]


# In[ ]:


cat_cols = ['Type', 'Breed1', 'Breed2', 'Gender', 'Color1', 'Color2',
       'Color3', 'MaturitySize', 'FurLength', 'Vaccinated', 'Dewormed',
       'Sterilized', 'Health', 'State', 'RescuerID',
       'No_name', 'Pure_breed', 'health', 'Free']


# In[ ]:


##Adding more cols
more_cols =[]
for col1 in cat_cols:
    for col2 in cat_cols:
        if col1 != col2 and col1 not in ['RescuerID','State'] and col2 not in ['RescuerID','State']:
            train[col1 +'_'+col2] = train[col1].astype(str)+'_'+train[col2].astype(str)
            test[col1 +'_'+col2] = test[col1].astype(str)+'_'+test[col2].astype(str)
            more_cols.append(col1+'_'+col2)

cat_cols = cat_cols + more_cols


# In[ ]:


get_ipython().run_cell_magic('time', '', 'indexer = {}\nfor col in cat_cols:\n    _,indexer[col] = pd.factorize(train[col].astype(str))\n\nfor col in tqdm_notebook(cat_cols):\n    train[col] = indexer[col].get_indexer(train[col].astype(str))\n    test[col] = indexer[col].get_indexer(test[col].astype(str))')


# In[ ]:


y = train['AdoptionSpeed']
train = train.drop(['AdoptionSpeed'], axis = 1)


# # Naive Multiclass LGB

# In[ ]:


n_fold = 5
folds = StratifiedKFold(n_splits = n_fold, shuffle = True, random_state = 15)


# In[ ]:


def train_model(X = train, X_test = test, y= y, params = None, folds = folds, model_type ='lgb',
               plot_feature_importance = False, averaging ='usual',make_oof = False):
    result_dict = {}
    if make_oof:
        oof = np.zeros((len(X),5))
    prediction = np.zeros((len(X_test),5))
    scores = []
    feature_importance = pd.DataFrame()
    
    for fold_n,(train_index, valid_index)  in  enumerate(folds.split(X,y)):
        gc.collect()
        print('Fold :',fold_n+1, 'Starting at ', time.ctime())
        X_train, X_valid = X.iloc[train_index], X.iloc[valid_index]
        y_train, y_valid = y.iloc[train_index], y.iloc[valid_index]
        
        if model_type =='lgb':
            train_data = lgb.Dataset(X_train, label = y_train, categorical_feature = cat_cols)
            valid_data = lgb.Dataset(X_valid, label = y_valid, categorical_feature = cat_cols)
            
            model = lgb.train(params, train_data,
                             num_boost_round = 20000,
                              valid_sets=[train_data, valid_data],
                             verbose_eval = 500,
                             early_stopping_rounds = 200)
            
            del train_data, valid_data
            gc.collect()
            
            y_pred_valid = model.predict(X_valid, num_iteration = model.best_iteration)
            del X_valid
            gc.collect()
            y_pred = model.predict(X_test, num_iteration = model.best_iteration)
        
        if model_type =='xgb':
            train_data = xgb.DMatrix(data = X_train, label = y_train)
            valid_data = xgb.DMatrix(data = X_valid, label = y_valid)
            
            watchlist = [(train_data,'train'),(valid_data,'valid_data')]
            
            model = xgb.train(dtrain = train_data, num_boost_round = 20000,evals = watchlist, 
                             early_stopping_rounds = 200, verbose_eval = 500, params = params)
            
            y_pred_valid = model.predict(xgb.DMatrix(X_valid), ntree_limit = model.best_ntree_limit)
            y_pred = model.predict(xgb.DMatrix(X_test),ntree_limit = model.best_ntree_limit)
            
        
        if make_oof:
            oof[valid_index] = y_pred_valid
        
        scores.append(kappa(y_valid, y_pred_valid.argmax(1)))
        print("Fold kappa: ", kappa(y_valid, y_pred_valid.argmax(1)))
        print('')
        
        if averaging=='usual':
            prediction += y_pred
        elif averaging =='rank':
            prediction +=pd.Series(y_pred).rank().values
        
        if model_type =='lgb':
            fold_importance = pd.DataFrame()
            fold_importance['feature'] = X.columns
            fold_importance['importance']= model.feature_importance()
            fold_importance['fold'] = fold_n+1
            feature_importance = pd.concat([feature_importance, fold_importance], axis= 0)
            
    prediction /=n_fold
    
    print("CV mean score: {0:.4f}, std:{1:.4f}".format(np.mean(scores), np.std(scores)))
    
    if model_type=='lgb':
        if plot_feature_importance:
            feature_importance['importance'] /= n_fold
            cols = feature_importance[['feature','importance']].groupby('feature').mean().sort_values(by='importance', ascending = False)[:50].index
            best_features = feature_importance.loc[feature_importance['feature'].isin(cols)]
            
            plt.figure(figsize = (16,12))
            sns.barplot(x='importance',y='feature',data = best_features.sort_values(by='importance', ascending = False))
            plt.title("LGB Features - avg over folds")
    
            result_dict['feature_importance'] = feature_importance

    result_dict['prediction'] = prediction
    if make_oof:
        result_dict['oof'] = oof
        
    return result_dict
    
    
    


# In[ ]:


params = {'num_leaves' : 512,
         'objective' : 'multiclass',
          'max_depth' : -1,
          'learning_rate':0.01,
          'boosting':'gbdt',
          'feature_fraction': 0.9,
          'bagging_freq': 3,
          'bagging_fraction': 0.9,
          'bagging_seed':11,
          'random_state':42,
          'verbosity':-1,
          'num_class':5
         }


# In[ ]:


result_dict_lgb = train_model(X = train, X_test = test, y = y, params = params, model_type='lgb',
                             plot_feature_importance = True, make_oof = True)


# In[ ]:


xgb_params = {'eta':0.01, 
             'max_depth': 9,
              'subsample' : 0.9, #Bagging ratio
              'colsample_bytree': 0.9, # number of features by tree
              'objective':'multi:softprob',
              'eval_metric':'merror', #multiclass classification error
              'silent' : True,
              'nthread' : 4,
              'num_class':5
              
             }
result_dict_xgb = train_model(params = xgb_params, model_type ='xgb',make_oof = True)


# In[ ]:


prediction = (result_dict_lgb['prediction'] + result_dict_xgb['prediction']).argmax(1)
submission = pd.DataFrame({'PetID': sub.PetID, 'AdoptionSpeed':[int(i) for i in prediction]})
submission.head()


# In[ ]:


submission.to_csv('submission.csv',index = False)


# Reference:
#     https://www.kaggle.com/artgor/exploration-of-data-step-by-step

# In[ ]:




