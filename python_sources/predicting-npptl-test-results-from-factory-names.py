#!/usr/bin/env python
# coding: utf-8

# This is just a fun exploration of a tiny set of test results performed by the National PPE Testing Lab. The tests are being conducted on non-NIOSH approved facemask type respirators, most commonly, the KN95. Iniitally the FDA issued an emergency blanket approval allowing the import of non-approved models. Unfortunately there are many outright fake or low quality versions of this PPE being produced and sold. As can be seen if you follow along, some of the worst test results show a complete lack of efficacy. 
# 
# Since the information provided by the dataset was very sparse, and the initial models were barely beating baseline, I pulled a few tricks out of the feature engineer's magic hat. 
# 
# First, after realizing that many of the manufacturer names contained a city and or province name, I crudely parsed these out by extracting the first 3 terms in the name. You can probably guess that I suspected that some places might be better than others. This was not initially the case, but it as interesting to note that the longer factory names were associated more strongly with a minimum filtration efficiency below the 95% standard.
# 
# 

# In[ ]:


import pandas as pd

dfs= pd.read_html('https://www.cdc.gov/niosh/npptl/respirators/testing/NonNIOSHresults.html')
import matplotlib.pyplot as plt

places = pd.read_csv("../input/china-city-names-with-province/city_names_lat_long.csv")


# grabbed a list of city and province names from the web, minimally processed to separate province
# this is clearly a subset of all chinese cities.

# In[ ]:


places.head() 


# In[ ]:


prov_names= places.Province.value_counts().index
places.set_index('Province', inplace=True)


# In[ ]:


df= dfs[0] 
df[df.columns[3]].median

df.columns=['Manufacturer', 'Model', 'Standard',
       'max_fe', 'min_fe',
       'Test Report']
df['name_len'] =  df.Manufacturer.str.split().str.len()
df['name1'] = df.Manufacturer.str.split().str.get(0)
df['name2'] =  df.Manufacturer.str.split().str.get(1)
df['name3'] =  df.Manufacturer.str.split().str.get(2)
df['ispname'] = df.name1.isin(prov_names)
df['mod_len'] = df.Model.str.split().str.len()      #model number of words
df.drop(index=df.index[(df.Manufacturer == '3M')])  #no prejudice


df['pass'] = df.min_fe >= 95 
df['mfg_ntests']=  df[['Manufacturer','Test Report']].groupby('Manufacturer')['Test Report'].transform(pd.Series.count)
#df[['Manufacturer','Test Report']].groupby(by='Manufacturer').count().sort_values(by='Test Report', ascending=False)
target='pass'


# In[ ]:


means = df[['Manufacturer','name1','max_fe','min_fe']].groupby(by='name1').mean().sort_values(by='min_fe', ascending=False)
ax = means.plot(figsize=(10,5))
ax.set_title('Min, Max FE ranges')
ax.hlines(y=95, xmin=df.name1[0], xmax='Yufing', color='red')


# In[ ]:


df = df.join(places, on='name1', how='left')

df.Latitude.fillna(value=df.Latitude.mean(),inplace=True)
df.Longitude.fillna(value=df.Longitude.mean(),inplace=True)


# In[ ]:


features = [ 'mod_len','ispname',
         'name_len', 'name1', 'name2',
       'name3', 'mfg_ntests','Latitude','Longitude','city']


# In[ ]:


import matplotlib.colors
cmap = 'RdPu'
c= df.min_fe

ax= df.plot.scatter(x='Latitude',y='Longitude', c=c,cmap='RdBu', alpha= .6,figsize=(6,6))
ax.set_xlabel('latitude')


# In[ ]:


import seaborn as sns
ax = sns.heatmap(
    df.corr(), 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)


# In[ ]:


fi_feat = ['mfg_ntests','ispname','mod_len'] # by feature importance lr
#features = fi_feat


# In[ ]:


from sklearn.model_selection import train_test_val_split

train,test,val = train_test_val_split(df,val_size=.2,test_size= .2,random_state =3)
train.shape,test.shape,val.shape

X_train= train[features]
y_train= train[target]
X_val=   val[features]
y_val  = val[target]
X_test = test[features]
y_test = test[target]

baseline= df[target].value_counts(normalize=True).values[0] #baseline
print( df[target].value_counts(normalize=True)) #predict false= FAIL  


# In[ ]:


import category_encoders as ce
from sklearn.linear_model import LogisticRegression, RidgeClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from xgboost import XGBClassifier
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest

models = [RidgeClassifierCV(),LogisticRegression(),XGBClassifier() , RandomForestClassifier(),DecisionTreeClassifier() ]

for model in models:
    pipe = make_pipeline( ce.OrdinalEncoder(),SimpleImputer(), model)
    pipe.fit(X_train,y_train)
    print(list(pipe.named_steps.keys())[-1])
    print('Training Accuracy:', pipe.score(X_train, y_train))
    print('Validation Accuracy:', pipe.score(X_val, y_val))
    print('Test Accuracy:', pipe.score(X_test, y_test))
    print('baseline Accuracy:', baseline,'\n')


# In[ ]:


pipe.named_steps['simpleimputer']


# In[ ]:


import eli5
from eli5.sklearn  import PermutationImportance
print('logreg')
perm = PermutationImportance(pipe, random_state=887).fit(pipe.named_steps['ordinalencoder'].transform(X_test),y_test)
eli5.show_weights(perm, feature_names = pipe.named_steps['ordinalencoder'].get_feature_names())


# In[ ]:


from pdpbox import pdp, get_dataset, info_plots

feature  = 'Latitude'
mfg_name_length=  pdp.pdp_isolate(model=pipe, dataset=X_test,
                              model_features= pipe.named_steps['ordinalencoder'].get_feature_names(),
                                  feature =feature)
pdp.pdp_plot(mfg_name_length, feature)
plt.show()
#so we conclude the more words the manufacturer name contains, the more likely they are to fail

