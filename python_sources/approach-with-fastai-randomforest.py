#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:



from fastai.imports import *
from fastai.structured import *
from pandas_summary import DataFrameSummary
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from IPython.display import display
from sklearn import metrics


# In[ ]:


import os
print(os.listdir("../input"))
PATH = '../input'


# In[ ]:


train = pd.read_csv(f'{PATH}/train.csv', low_memory=False)


# In[ ]:


train


# In[ ]:


building_structure = pd.read_csv(f'{PATH}/Building_Structure.csv', low_memory=False)
building_ownership = pd.read_csv(f'{PATH}/Building_Ownership_Use.csv', low_memory=False)
test = pd.read_csv(f'{PATH}/test.csv', low_memory=False)


# In[ ]:


print(train.shape,'\n',building_ownership.shape,'\n', building_structure.shape)


# Now let's merge training set with building structure and ownership on buildingID (we can see few overlaps which we can drop later)

# In[ ]:


train = train.merge(building_structure, on = 'building_id',how = 'left')
train = train.merge(building_ownership, on = 'building_id', how = 'left')


# In[ ]:


print(train.columns)
print(train.shape)


# In[ ]:


train.drop(['district_id_x', 'district_id_y', 'vdcmun_id_x', 'vdcmun_id_y', 'ward_id_y'], axis=1, inplace=True)


# In[ ]:


print(train.shape,train.columns)


# In[ ]:


test.shape


# Merge the other dataset with test set too !

# In[ ]:


test = test.merge(building_structure, on = 'building_id',how = 'left')
test = test.merge(building_ownership, on = 'building_id', how = 'left')
test.drop(['district_id_x', 'district_id_y', 'vdcmun_id_x', 'vdcmun_id_y', 'ward_id_y'], axis=1, inplace=True)
test.shape


# ### Exploring the Data

# In[ ]:


#function to display all rows and columns
def display_all(df):
    with pd.option_context("display.max_rows", 1000, "display.max_columns", 1000): 
        display(df)


# In[ ]:


display_all(train.tail().T)


# In[ ]:


display_all(train.describe(include='all').T)


# In[ ]:


display_all(train.describe(include='all').T)


# We can see some missing values(has_repair_started / count_families) along with some categorical variable which we'll handle

# ### Preprocessing

# In[ ]:


# Create table for missing data analysis
def draw_missing_data_table(df):
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    return missing_data


# In[ ]:


draw_missing_data_table(train)


# ** Handling Missing Values **

# In[ ]:


#count familes have only 1 missing values we'll fill that
train['count_families'].fillna(train['count_families'].mode()[0],inplace=True)


# In[ ]:


print(train['has_repair_started'].value_counts())
print(test['has_repair_started'].value_counts())


# In[ ]:


train['has_repair_started'].fillna(False,inplace=True)
test['has_repair_started'].fillna(False,inplace=True)


# In[ ]:


print(train.columns.hasnans)
print(test.columns.hasnans)


# has repair started has lot if missing values, we'll first check the importance of that variable and then decide what to do with those missing values(for now set it to false)
# 
# We'll  ** Convert the target variable into numeric format **

# In[ ]:


Y = {'Grade 1': 1, 'Grade 2': 2, 'Grade 3': 3, 'Grade 4': 4, 'Grade 5': 5}
train['damage_grade'].replace(Y, inplace = True)
train['damage_grade'].unique()


# In[ ]:


train.dtypes


# In[ ]:


print(train.select_dtypes('object').nunique())
print(train.select_dtypes('object').nunique())


# **Dropping the ID(not useful) column**

# In[ ]:


#Remove column 'building_id' as it is unique for every row & doesnt have any impact
train_building_id = train['building_id']
test_building_id = test['building_id']
train.drop(['building_id'], axis=1, inplace=True)
test.drop(['building_id'], axis=1, inplace=True)


# In[ ]:


display_all(train)


# **Adding/Extracting features from the existing columns**
# 
# Here we have 
# 
# count_floors_pre_eq|Number of floors that the building had before the earthquake
# 
# count_floors_post_eq|Number of floors that the building had after the earthquake
# 
# height_ft_pre_eq|Height of the building before the earthquake (in feet)
# 
# height_ft_post_eq|Height of the building after the earthquake (in feet)
# 
# We can clearly see that these varaible are not to be used directly but we should extract the meaning from the variable first and then use them.
# We can calculate the changes in floor and height after the earthquake by subtracting first from the 2nd

# In[ ]:


train['count_floors_change'] = (train['count_floors_post_eq']/train['count_floors_pre_eq'])
train['height_ft_change'] = (train['height_ft_post_eq']/train['height_ft_pre_eq'])
test['count_floors_change'] = (test['count_floors_post_eq']/test['count_floors_pre_eq'])
test['height_ft_change'] = (test['height_ft_post_eq']/test['height_ft_pre_eq'])

train.drop(['count_floors_post_eq', 'height_ft_post_eq'], axis=1, inplace=True)
test.drop(['count_floors_post_eq', 'height_ft_post_eq'], axis=1, inplace=True)


# In[ ]:


sns.barplot(train['condition_post_eq'],train['damage_grade']);


# In[ ]:


sns.barplot(train['plan_configuration'],train['damage_grade']);


# **Converting Object/categorical into Dummy variable**
# 
# We'll choose one-hot encoding over numeric codes as here no object/categorical varible is such that it has types like (high medium low) which do indicates (2,1,0) 

# In[ ]:


train_cats(train)
apply_cats(test, train)


# here we'll do one hot encoding on all except plan_configuration and condition_post_eq, as  condition post earthquake can be given codes (1,2,3...) where as plan config doesn't seem much useful now 
# So in proc_df which handles missing values and categorical variable(conversion into codes) we'll set max_n_cat  = 6 so that all the objects having unique values below 6 will be one hot encoded, and the variable above 6 will be given codes

# In[ ]:


df, y, nas = proc_df(train, 'damage_grade', max_n_cat=6)


# In[ ]:


test_df, _, _ = proc_df(test, na_dict=nas, max_n_cat=6)


# In[ ]:


print(test_df.shape, df.shape)


# **Metric F1 **

# In[ ]:


from sklearn.metrics import f1_score

def rmse(x,y): return math.sqrt(((x-y)**2).mean())

def print_score(m):
    res = [m.score(x_train, y_train), m.score(x_test, y_test)]
    if hasattr(m, 'oob_score_'): res.append(m.oob_score_)
    print(res)


# ** Splitting data **

# In[ ]:


from sklearn.model_selection import train_test_split
x = df
x_train, x_test, y_train, y_test = train_test_split(x, y, 
test_size=0.2, random_state=0)


# In[ ]:


print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)


# ### Random Forest ###
# **Base Model**

# In[ ]:


set_rf_samples(100000)


# In[ ]:


m = RandomForestClassifier(n_jobs=-1)
get_ipython().run_line_magic('time', 'm.fit(x_train, y_train)')
print(m.score(x_train, y_train))


# In[ ]:


print_score(m)


# In[ ]:


m = RandomForestRegressor(n_estimators=150, min_samples_leaf=1, max_features=0.6, n_jobs=-1, oob_score=True)
get_ipython().run_line_magic('time', 'm.fit(x_train, y_train)')
print_score(m)


# After trying a lot of combinations of hyperparameters I managed to get 90% on training, 86% on validation (on sampled subset of 100000)
# 
# ### Feature Importance ###

# In[ ]:


fi = rf_feat_importance(m, df); fi[:10]


# In[ ]:


fi.plot('cols', 'imp', figsize=(10,6), legend=False);


# In[ ]:


def plot_fi(fi): return fi.plot('cols', 'imp', 'barh', figsize=(12,7), legend=False)


# In[ ]:


plot_fi(fi[:30]);


# In[ ]:


to_keep = fi[fi.imp>0.001].cols; len(to_keep)


# In[ ]:


to_keep


# In[ ]:


def split_vals(a,n): return a[:n], a[n:]
df_keep = df[to_keep].copy()

from scipy.cluster import hierarchy as hc

corr = np.round(scipy.stats.spearmanr(df_keep).correlation, 4)
corr_condensed = hc.distance.squareform(1-corr)
z = hc.linkage(corr_condensed, method='average')
fig = plt.figure(figsize=(16,10))
dendrogram = hc.dendrogram(z, labels=df_keep.columns, orientation='left', leaf_font_size=16)
plt.show()


# Now looking at the dendogram plot we can remove the varaible which are totaly dependent on each other like ward_id_x and the district_id and also count_floor_change but as we can see above they are important features so dropping them reduces the accuracy drastically.
# 
# Also keeping only the important features is decreasing the accuracy so we keep the same set of earlier chosen features
# 

# In[ ]:


correlations = df.corr()


# In[ ]:


print('Most Positive Correlations:\n', correlations.tail(10))
print('\nMost Negative Correlations:\n', correlations.head(10))


# In[ ]:


imp_features=['height_ft_change', 'condition_post_eq', 'count_floors_change' , 'ward_id_x','age_building', 'plinth_area_sq_ft']
scor = train[imp_features+['damage_grade']]
data_corrs = scor.corr()
data_corrs
plt.figure(figsize = (8, 6))

# Heatmap of correlations
sns.heatmap(data_corrs, cmap = plt.cm.RdYlBu_r, vmin = -0.25, annot = True, vmax = 0.6)
plt.title('Correlation Heatmap');


# In[ ]:


reset_rf_samples()


# In[ ]:


m = RandomForestRegressor(n_estimators=150, min_samples_leaf=1, max_features=0.6, n_jobs=-1, oob_score=True)
get_ipython().run_line_magic('time', 'm.fit(x_train, y_train)')
print_score(m)


# In[ ]:


test_df.head(5)


# In[ ]:


ypreds = m.predict(test_df)


# In[ ]:


ypreds = ypreds.round()


# In[ ]:


prediction=pd.DataFrame({'building_id': test_building_id, 'damage_grade':ypreds})


# In[ ]:


target = {1: 'Grade 1', 2: 'Grade 2', 3: 'Grade 3', 4: 'Grade 4', 5: 'Grade 5'}
prediction.damage_grade.replace(target, inplace=True)
prediction.to_csv('submission.csv', index=False)


# In[ ]:


prediction.head()


# This submission gives a 76.9% accuracy on hackerearth platform.With few variables removed and with xgboost the accuracy can be made to increase to 79+

# In[ ]:


from xgboost import XGBClassifier


# In[ ]:


xgbc = XGBClassifier(n_estimators=100, learning_rate=0.2, max_depth=6, random_state=42) #random state = 42 as for Feature Imp above 0.01 there were 42 cols
xgbc.fit(x_train, y_train)


# In[ ]:


print_score(xgbc)
pred_test_y = pd.Series(list(xgbc.predict(test_df)))
prediction=pd.DataFrame({'building_id': test_building_id, 'damage_grade':pred_test_y})
target = {1: 'Grade 1', 2: 'Grade 2', 3: 'Grade 3', 4: 'Grade 4', 5: 'Grade 5'}
prediction.damage_grade.replace(target, inplace=True)
prediction.to_csv('submission.csv', index=False)


# This gives 75% accuracy on hackerearth

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=5, n_jobs=-1)
knn.fit(x_train, y_train)


# In[ ]:


print_score(knn)


# Getting worst

# At any point of time Ensembling works better than SVM as bags are created and distributed average of predictions of tree are taken.(although sometimes if the data if quite linear or fits perfectly for some poly function then SVM can have a upper hand) The reason here Randomforest gave better accuracy and prediction than xgboost was the data is bit noisy, and in such conditions RF works better than xgb.RFs train each tree independently, using a random sample of the data. This randomness helps to make the model more robust and less likely to overfit on the training data.Also xgb needs more number of enumarators(greater than 250 in this case atleast) for shooting up the accu, i trained on 100(Running on local machine with insuffient memory and above 150 the machine crashed).
