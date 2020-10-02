#!/usr/bin/env python
# coding: utf-8

# # Exploring the WHO suicides data
# 
# This notebook employs a few simple techniques for exploring the WHO suicides dataset from Kaggle. 
# ### Table of Contents
# [Data preparation](#preparation)
# <br>
# [Visualizations](#visualizations)
# <br>
# [Transformations](#transformations)
# <br>
# [Predictions](#predictions)

# We'll load a few libraries that we may need in this analysis. 

# In[ ]:


import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
import seaborn as sns; #sns.set()
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, cross_validate, KFold
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
pd.options.mode.chained_assignment = None  # default='warn'
# warnings.filterwarnings('ignore') # disable all warnings
warnings.filterwarnings(action='once') # warn only once


# <a id='preparation'></a>
# # Data preparation

# Let's load the data into a Pandas dataframe.

# In[ ]:


data = pd.read_csv('../input/who_suicide_statistics.csv')


# Take a peek at the first few rows of data, and view some summary statistics to get a high-level understanding of what's going on in the data.

# In[ ]:


data.head()


# In[ ]:


data.describe()


# In[ ]:


data.astype('object').describe()


# We saw some missing values in the first few rows (i.e. the NaNs). Let's find out how many missing values are in the data set. We'll first find how many missing values are in each column, then we'll calculate what proportion of the data points are missing.

# In[ ]:


na_stats = pd.DataFrame([],columns=['count_na','prop_na'])
na_stats['count_na'] = (data.isna().sum())
na_stats['prop_na'] = (data.isna().sum()/data.shape[0])
na_stats


# Ok so about 5% of the suicides_no and 12% of population data are missing. Let's see how this breaks down by country.

# In[ ]:


nan_suicides = data.suicides_no.isnull().groupby([data['country']]).sum().astype(int).reset_index(name='count')
nan_population = data.population.isnull().groupby([data['country']]).sum().astype(int).reset_index(name='count')
count_by_country = pd.DataFrame(data.groupby(data['country'])['suicides_no'].count())
count_by_country = count_by_country.reset_index()

prop = pd.DataFrame([], columns = ['country', 'prop_suicides_nan', 'prop_population_nan'])
prop['prop_suicides_nan'] = nan_suicides['count']/count_by_country['suicides_no']
prop['prop_population_nan'] = nan_population['count']/count_by_country['suicides_no']
prop['country'] = nan_suicides['country']

# Only show countries that have some missing data.
prop[prop['prop_suicides_nan'] > 0].sort_values(by=['prop_suicides_nan'], ascending=False)


# So we can see that Mongolia, Switzerland, Denmark, San Marino, Cuba, and the Phillipines have mostly missing data for suicides, and Bermuda, the Cayman Islands, and Saint Kitts and Nevis have most of the population data missing. I'm not sure why this is, but for my porposes here, I'm OK with dropping entries missing values for now. There are methods for missing data imputation, but I've decided not going to do any imputation in this notebook.
# 
# Let's go ahead and drop the missing value entries, this will make the data easier to work with.

# In[ ]:


data_clean = data.dropna()
data_clean.head()


# <a id='visualizations'></a>
# # Visualizations
# Now that we have the data cleaned up a bit, let's use some visualizations to get a sense of what trends and patterns might exist.

# First we'll set a target country to examine, then we'll plot the number of suicides per year for each age group, and adjust the shape of the data point by gender.

# In[ ]:


target_country = "United States"
fig, ax = plt.subplots(figsize=(12,6))
ax.set_title( 'Suicides by age ({})'.format(target_country))
p = sns.scatterplot(x="year", y="suicides_no", data=data_clean,hue='age',style='sex')


# Now let's take a closer look at the differences in the number of suicides between men and women.

# In[ ]:


target_country = "United States"
fig, ax = plt.subplots(figsize=(12,6))
ax.set_title( 'Suicides by sex ({})'.format(target_country))
sui_by_sex = data_clean[data_clean["country"].str.contains(target_country)].groupby(['sex','year'],as_index=False).sum()
p = sns.scatterplot(x="year", y="suicides_no", data=sui_by_sex,hue='sex')


# <a id='transformations'></a>
# # Transforming the data

# If we want to perform further analysis, it's a good idea to map the ages and genders to values.

# In[ ]:


agemap = {}
i = 0
for x in data.age.unique():
    agemap[x] = i
    i+=1

# since there are only two values here, we can do a mapping for gender. If >2 types listed, we could do a one-hot encoding instead.
gendermap = {}
i = 0
for x in data.sex.unique():
    gendermap[x] = i
    i+=1
    
data_clean['age_id'] = data['age'].map(agemap)
data_clean['sex_id'] = data['sex'].map(gendermap)


# Now we can drop the sex and age columns since we've completed the mapping and added it to the data set.

# In[ ]:


x = data_clean.drop(['sex','age'], axis = 1)
x = pd.get_dummies(x)
y = x[['suicides_no']]
x = x.drop('suicides_no',axis=1)


# Let's get a quick view of how the features of our dataset are correlated with each other.

# In[ ]:


corr = data_clean.corr()
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, vmax=.3, cmap=cmap, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})


# Population and suicides_no are correlated, which makes intuitive sense. sex_id and suicides_no are correlated as men tend to commit more suicides than women. Let's now see if male suicides are correlated with female suicides.

# In[ ]:


# Separate the suicides and population values by gender
data_by_gender = data_clean.loc[data_clean['sex_id'] == 1]
data_by_females = data_clean.loc[data_clean['sex_id'] == 0]
#data_by_gender['f_suicides_no'] = data_by_gender.merge(data_by_females, on=['country', 'year', 'age'])[['suicides_no_y']]
data_by_gender.rename(columns={'suicides_no':'m_suicides_no'}, inplace=True)
data_by_gender.rename(columns={'population':'m_population'}, inplace=True)

# Wrangle the data into the right format without redundant columns
data_by_gender = data_by_gender.merge(data_by_females, on=['country', 'year', 'age'])
data_by_gender = data_by_gender.drop(labels=['age','age_id_y','sex_x','sex_y','sex_id_y','sex_id_x'],axis=1)
data_by_gender.rename(columns={'population':'f_population', 'age_id_x': 'age_id'}, inplace=True)
data_by_gender.rename(columns={'suicides_no':'f_suicides_no'}, inplace=True)


# In[ ]:


data_by_gender.head()


# In[ ]:


x_s = pd.get_dummies(data_by_gender)
y_s = x_s[['f_suicides_no','m_suicides_no']]
x_s = x_s.drop(['f_suicides_no','m_suicides_no'],axis=1)

# Just doing a sanity check to make sure the data looks the way we want it.
x_s.head()


# Looks good! Now that we've separated male and female suicides, let's see if they're correlated with each other.

# In[ ]:


corr_by_gender = data_by_gender.corr()
sns.heatmap(corr_by_gender, vmax=.3, cmap=cmap, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})


# It seems that and female suicides are slightly positively coorelated, whereas age and male suicides are slightly negatively correlated. Interesting! 

# <a id='predictions'></a>
# # Predictions
# Let's use linear regression to try to predict the number of suicides given the rest of the data. We'll first train one model for all countries and age groups.
# 

# First, we'll split the data into training and test sets.

# In[ ]:


# split into train/test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=314)

# and again by gender
x_s_train, x_s_test, y_s_train, y_s_test = train_test_split(x_s, y_s, test_size=0.25, random_state=314)


# Now we can train a linear regression model to predict the number of suicides. 

# In[ ]:


reg = LinearRegression().fit(x_train, y_train)
y_hat = reg.predict(x_test)
y_hat = pd.DataFrame(y_hat,columns=['suicides_no'])

#compute metrics

mse = (metrics.mean_squared_error(y_pred=y_hat, y_true=y_test ))
r2 = metrics.r2_score(y_pred=y_hat, y_true=y_test)
fig, ax = plt.subplots(figsize=(12,6))
sns.scatterplot(x=y_test['suicides_no'],y=y_hat['suicides_no'])
ax.set(xlabel = 'Actual y', ylabel="Predicted y")
plt.show()
print('The r-squared value is: {}, and MSE is: {}'.format(r2, mse))


# Hmm, the plot of predicted y vs actual y looks pretty scattered. The closer the alignment of points along the 45 degree line, would indicate a stronger fit. Let's use k-fold cross-validation to compare our Linear Regression model with other models such as Lasso and kNN.

# In[ ]:


kf = KFold(5,shuffle=True)
reg_cv = LinearRegression()
las_cv = Lasso()
kn_cv = KNeighborsRegressor(n_neighbors=30)
reg_cv_model = cross_validate(reg_cv, X=x, y=y, cv=kf, scoring=('neg_mean_squared_error', 'r2'), return_train_score=False)
las_cv_model = cross_validate(las_cv, X=x, y=y, cv=kf, scoring=('neg_mean_squared_error', 'r2'), return_train_score=False)
kn_cv_model = cross_validate(kn_cv, X=x, y=y, cv=kf, scoring=('neg_mean_squared_error', 'r2'), return_train_score=False)

reg_cv_scores = cross_val_score(reg_cv, X=x, y=y, cv=kf)
las_cv_scores = cross_val_score(las_cv, X=x, y=y, cv=kf)
kn_cv_scores = cross_val_score(kn_cv, X=x, y=y, cv=kf)
print('Linear Regression: The average r-squared value from {}-fold cross-validation is: {}'.format(kf.n_splits, reg_cv_scores.mean()), ('\nLasso: The average r-squared value from {}-fold cross-validation is: {}'.format(kf.n_splits, las_cv_scores.mean())), ('\nk-NN Regressor: The average r-squared value from {}-fold cross-validation is: {}'.format(kf.n_splits, kn_cv_scores.mean())))


# Like the Linear Rergession model, this doesn't look too good. The k-NN modle fit is the worst of the three! Let's see if we can make better predictions by constraining the model by country. We'll pick the USA as an example.

# In[ ]:


x_usa = data_clean.drop(['sex','age'], axis = 1)
x_usa = x_usa[x_usa['country'].str.contains("United States")]
x_usa = x_usa.drop('country',axis=1)
x_usa = pd.get_dummies(x_usa)
y_usa = x_usa[['suicides_no']]
x_usa = x_usa.drop('suicides_no',axis=1);
x_usa_train, x_usa_test, y_usa_train, y_usa_test = train_test_split(x_usa, y_usa, test_size=0.25, random_state=314)


# In[ ]:


reg_usa = LinearRegression().fit(x_usa_train, y_usa_train)
y_usa_hat = reg_usa.predict(x_usa_test)
y_usa_hat = pd.DataFrame(y_usa_hat,columns=['suicides_no'])

#compute metrics
mse_usa = (metrics.mean_squared_error(y_pred=y_usa_hat, y_true=y_usa_test ))
r2_usa = metrics.r2_score(y_pred=y_usa_hat, y_true=y_usa_test)

#fig_usa, ax_usa = plt.subplots(figsize=(12,6))

fig, ax = plt.subplots()
ax.scatter(x=y_usa_test['suicides_no'],y=y_usa_hat['suicides_no'])
plt.xlabel('Actual y')
plt.ylabel('Predicted y')
plt.show()
#ax_usa.set(xlabel = 'Actual y', ylabel="Predicted y")

print('The r-squared value is: {}, and MSE is: {}'.format(r2_usa, mse_usa))


# Let's perform 5-fold cross-validation to compare our country-specific Linear Regression model with the Lasso and a kNN regressor.

# In[ ]:


kf = KFold(5,shuffle=True)
reg_cv = LinearRegression()
las_cv = Lasso()
kn_cv = KNeighborsRegressor(n_neighbors=30)
reg_cv_model = cross_validate(reg_cv, X=x_usa, y=y_usa, cv=kf, scoring=('neg_mean_squared_error', 'r2'), return_train_score=False)
las_cv_model = cross_validate(las_cv, X=x_usa, y=y_usa, cv=kf, scoring=('neg_mean_squared_error', 'r2'), return_train_score=False)
kn_cv_model = cross_validate(kn_cv, X=x_usa, y=y_usa, cv=kf, scoring=('neg_mean_squared_error', 'r2'), return_train_score=False)

reg_cv_scores = cross_val_score(reg_cv, X=x_usa, y=y_usa, cv=kf)
las_cv_scores = cross_val_score(las_cv, X=x_usa, y=y_usa, cv=kf)
kn_cv_scores = cross_val_score(kn_cv, X=x_usa, y=y_usa, cv=kf)
print('Linear Regression: The average r-squared value from {}-fold cross-validation is: {}'.format(kf.n_splits, reg_cv_scores.mean()), ('\nLasso: The average r-squared value from {}-fold cross-validation is: {}'.format(kf.n_splits, las_cv_scores.mean())), ('\nk-NN Regressor: The average r-squared value from {}-fold cross-validation is: {}'.format(kf.n_splits, kn_cv_scores.mean())))


# As we suspected, we see better performance when the model is restricted to a specific country.

# Now let's try to predict by gender only. 

# In[ ]:


# Pick a target gender, m or f
target = 'f_suicides_no'
reg = LinearRegression().fit(x_s_train, y_s_train[target])
y_s_hat = reg.predict(x_s_test)
y_s_hat = pd.DataFrame(y_s_hat,columns=[target])

#compute metrics

mse = (metrics.mean_squared_error(y_pred=y_s_hat[target], y_true=y_s_test[target] ))
r2_s = metrics.r2_score(y_pred=y_s_hat, y_true=y_s_test[target])
fig, ax = plt.subplots(figsize=(12,6))
sns.scatterplot(x=y_s_test[target],y=y_s_hat[target])
ax.set(xlabel = 'Actual y', ylabel="Predicted y")
plt.show()
print('The r-squared value is: {}, and MSE is: {}'.format(r2, mse))


# In[ ]:


kf = KFold(5,shuffle=True)
reg_cv = LinearRegression()
las_cv = Lasso()
kn_cv = KNeighborsRegressor(n_neighbors=30)
reg_cv_model = cross_validate(reg_cv, X=x_s, y=y_s[target], cv=kf, scoring=('neg_mean_squared_error', 'r2'), return_train_score=False)
las_cv_model = cross_validate(las_cv, X=x_s, y=y_s[target], cv=kf, scoring=('neg_mean_squared_error', 'r2'), return_train_score=False)
kn_cv_model = cross_validate(kn_cv, X=x_s, y=y_s[target], cv=kf, scoring=('neg_mean_squared_error', 'r2'), return_train_score=False)

reg_cv_scores_s = cross_val_score(reg_cv, X=x_s, y=y_s[target], cv=kf)
las_cv_scores_s = cross_val_score(las_cv, X=x_s, y=y_s[target], cv=kf)
kn_cv_scores_s = cross_val_score(kn_cv, X=x_s, y=y_s[target], cv=kf)
print('Linear Regression: The average r-squared value from {}-fold cross-validation is: {}'.format(kf.n_splits, reg_cv_scores_s.mean()), ('\nLasso: The average r-squared value from {}-fold cross-validation is: {}'.format(kf.n_splits, las_cv_scores_s.mean())), ('\nk-NN Regressor: The average r-squared value from {}-fold cross-validation is: {}'.format(kf.n_splits, kn_cv_scores_s.mean())))


# In[ ]:


print('The results are much better. We can more accurately predict {} by {} percent over our attempt to predict suicides for both genders.'.format(target, np.round((reg_cv_scores_s.mean()/reg_cv_scores.mean())*100 - 100,2)))


# In[ ]:




