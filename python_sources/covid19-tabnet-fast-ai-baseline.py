#!/usr/bin/env python
# coding: utf-8

# # [#masks4all](https://masks4all.co/why-we-need-mandatory-mask-laws-masks4all/)
# 
# # Introduction
# 
# The goal of this notebook is to provide some basic [fast.ai](https://www.fast.ai/), [TabNet (paper here)](https://arxiv.org/abs/1908.07442) model for COVID-19 dataset.
# 
# The solution utilizes mostly [fast.ai](https://www.fast.ai/) library with [fast_tabnet](https://github.com/mgrankin/fast_tabnet) and stuff included in [this course](https://course.fast.ai/)
# 
# Although it is not the best approach here (doesn't have an RNN part, for instance), it requires reasonably small amount of code and obviously no feature engineering.

# In[ ]:


get_ipython().system('pip install fastai2')
get_ipython().system('pip install fast_tabnet')


# In[ ]:


from fastai2.basics import *
from fastai2.tabular.all import *
from fast_tabnet.core import *

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# # Load input data

# In[ ]:


PATH = '/kaggle/input/covid19-global-forecasting-week-4/'
train_df = pd.read_csv(PATH + 'train.csv', parse_dates=['Date'])
test_df = pd.read_csv(PATH + 'test.csv', parse_dates=['Date'])

add_datepart(train_df, 'Date', drop=False)
add_datepart(test_df, 'Date', drop=False)


# # Metadata (continent, population, tests per million etc.)

# In[ ]:


PATH1 = '/kaggle/input/covid19-country-data-wk3-release/'

meta_convert_fun = lambda x: np.float32(x) if x not in ['N.A.', '#N/A', '#NULL!'] else np.nan

meta_df = pd.read_csv(PATH1 + 'Data Join - RELEASE.csv', thousands=",",
                     converters={
                         ' TFR ': meta_convert_fun,
                         'Personality_uai': meta_convert_fun,
                     }).rename(columns=lambda x: x.strip())

PATH2 = '/kaggle/input/countryinfo/'
countryinfo = pd.read_csv(PATH2 + 'covid19countryinfo.csv', thousands=",", parse_dates=['quarantine', 'schools', 'publicplace', 'gathering', 'nonessential'])
testinfo = pd.read_csv(PATH2 + 'covid19tests.csv', thousands=",")

countryinfo.rename(columns={'region': 'Province_State', 'country': 'Country_Region'}, inplace=True)
testinfo.rename(columns={'region': 'Province_State', 'country': 'Country_Region'}, inplace=True)
testinfo = testinfo.drop(['alpha3code', 'alpha2code', 'date'], axis=1)

PATH3 = '/kaggle/input/covid19-forecasting-metadata/'
continent_meta = pd.read_csv(PATH3 + 'region_metadata.csv')
continent_meta = continent_meta[['Country_Region' ,'Province_State', 'continent']]

recoveries_meta = pd.read_csv(PATH3 + 'region_date_metadata.csv', parse_dates=['Date'])

def fill_unknown_state(df):
    df.fillna({'Province_State': 'Unknown'}, inplace=True)
    
for d in [train_df, test_df, meta_df, countryinfo, testinfo, continent_meta, recoveries_meta]:
    fill_unknown_state(d)


# # Add external features to input dataframes
# For each country, we want to extract the first day when it reached at least 1 and 50 cases.
# 
# Average fatality rate will be calculated from last data available, simply taking deaths / cases.

# In[ ]:


idx_group = ['Country_Region', 'Province_State']

def day_reached_cases(df, name, no_cases=1):
    """For each country/province get first day of year with at least given number of cases."""
    gb = df[df['ConfirmedCases'] >= no_cases].groupby(idx_group)
    return gb.Dayofyear.first().reset_index().rename(columns={'Dayofyear': name})

def area_fatality_rate(df):
    """Get average fatality rate for last known entry, for each country/province."""
    gb = df[df['Fatalities'] >= 22].groupby(idx_group)
    res_df = (gb.Fatalities.last() / gb.ConfirmedCases.last()).reset_index()
    return res_df.rename(columns={0 : 'FatalityRate'})


# In[ ]:


def joined_data(df):
    res = df.copy()
    
    fatality = area_fatality_rate(train_df)
    first_nonzero = day_reached_cases(train_df, 'FirstCaseDay', 1)
    first_fifty = day_reached_cases(train_df, 'First50CasesDay', 50)
    
    # Add external features
    res = pd.merge(res, continent_meta, how='left')
    res = pd.merge(res, recoveries_meta, how='left')
    res = pd.merge(res, meta_df, how='left')
    res = pd.merge(res, countryinfo, how='left')
    res = pd.merge(res, testinfo, how='left', left_on=idx_group, right_on=idx_group)
    
    # Add calculated features
    res = pd.merge(res, fatality, how='left')
    res = pd.merge(res, first_nonzero, how='left')
    res = pd.merge(res, first_fifty, how='left')
    return res

train_df = joined_data(train_df)
test_df = joined_data(test_df)


# In[ ]:


# It turns out any country in train dataset has at least one case.
train_df.FirstCaseDay.isna().sum()


# # Add temporal features
# 
# Some basic features like number of days since the first case in each country/province with analogous feature for 50 days may be worth adding,
# including containment measures such as closed schools and quarantine.

# In[ ]:


def with_new_features(df, train=True):
    res = df.copy()
    add_datepart(res, 'quarantine', prefix='qua')
    add_datepart(res, 'schools', prefix='sql')
    
    res['DaysSinceFirst'] = res['Dayofyear'] - res['FirstCaseDay']
    res['DaysSince50'] = res['Dayofyear'] - res['First50CasesDay']
    res['DaysQua'] = res['Dayofyear'] - res['quaDayofyear']
    res['DaysSql'] = res['Dayofyear'] - res['sqlDayofyear']
    
    # Since we will take log of dependent variable, we won't make it nonzero.
    if train:
        res['ConfirmedCases'] += 1
    return res
    
train_df = with_new_features(train_df)
test_df = with_new_features(test_df, train=False)


# In[ ]:


train_df.shape


# # Feature selection
# In fast.ai we can easily select categorical and continuous variables for training.
# 
# I decided not to choose any external data in baseline model. Adding numerical values from country data provided in this notebook doesn't seem to improve the validation score much.

# In[ ]:


# Categorical variables - only basic identifiers, some features like continent will be worth adding.
cat_vars = ['Country_Region', 'Province_State',
            'continent'
#             'publicplace', 'gathering', 'nonessential'
           ]

# Continuous variables - just ones directly connected with time.
cont_vars = ['DaysSinceFirst', 'DaysSince50', 'Dayofyear',
            'DaysQua', 'DaysSql',
            'latitude', 'longitude',
            'TRUE POPULATION', 'TFR', 'Personality_uai',
            'testper1m', 'positiveper1m',
            'casediv1m', 'deathdiv1m', 
            'FatalityRate',
#             'density', 'urbanpop', 'medianage', 'hospibed','healthperpop', 'fertility',
            'smokers', 'lung', 
#             'continent_gdp_pc', 'continent_happiness', 'continent_Life_expectancy','GDP_region', 
#            'abs_latitude', 'temperature', 'humidity',
            ]

# We will predict only confirmed cases. 
# For fatalities, one could train another model but we won't do it - multiplying by average fatality in each area is enough for a sample submission.
dep_var = ['ConfirmedCases', 'Fatalities']

df = train_df[cont_vars + cat_vars + dep_var +['Date']].copy().sort_values('Date')


# # Avoid leakage - take only non-overlapping values for training
# 
# For now, the only available data to validate our model is in training set. 
# 
# As our test set starts on **02.04.2020**, we should take only rows before that date for training to avoid leakage.

# In[ ]:


print(test_df.Date.min())
MAX_TRAIN_IDX = df[df['Date'] < test_df.Date.min()].shape[0]


# # Preparing training set
# 
# In fast.ai v2, we have to manually take log of dependent variables. Preprocessing setup is vanilla fast.ai stuff,
# we utilize our training index to make a unleaky train/valid split. 
# 
# An important thing is also picking the right batch size in our DataLoader, I've chosen value 512 which is pretty big but doesn't seem to affect the training negatively.

# In[ ]:


df1 = df.copy()
df1['ConfirmedCases'] = np.log(df1['ConfirmedCases'])
df1['Fatalities'] = np.log(df1['Fatalities'] + 1)


# In[ ]:


path = '/kaggle/working/'

procs=[FillMissing, Categorify, Normalize]

splits = list(range(MAX_TRAIN_IDX)), (list(range(MAX_TRAIN_IDX, len(df))))

get_ipython().run_line_magic('time', 'to = TabularPandas(df1, procs, cat_vars.copy(), cont_vars.copy(), dep_var, y_block=TransformBlock(), splits=splits)')


# In[ ]:


dls = to.dataloaders(bs=512, path=path)
dls.show_batch()


# # Processed test set

# In[ ]:


to_tst = to.new(test_df)
to_tst.process()
to_tst.all_cols.head()


# In[ ]:


emb_szs = get_emb_sz(to); print(emb_szs)


# # Model
# 
# The model provided here is a simple baseline from [fast_tabnet](https://github.com/mgrankin/fast_tabnet) documentation, without any fine tuning.
# 
# [Here](https://github.com/mgrankin/fast_tabnet#how-to-use) you can find **how to tune hyperparameters**.
# 
# In contrary to fast.ai tabular learner, this network accepts **multivariable output** like here - (Cases, Fatalities)
# is what we are going to predict.

# In[ ]:


dls.c = 2 # Number of outputs we expect from our network - in this case 2.
model = TabNetModel(emb_szs, len(to.cont_names), dls.c, n_d=16, n_a=8, n_steps=3)
opt_func = partial(Adam, wd=0.01, eps=1e-5)
learn = Learner(dls, model, MSELossFlat(), opt_func=opt_func, lr=3e-2, metrics=[rmse])


# In[ ]:


learn.lr_find()


# In[ ]:


cb = SaveModelCallback()
learn.fit_one_cycle(200, cbs=cb)


# # Preparing submission

# In[ ]:


# Load the best model so far (based on validation score)
learn.load('model')


# In[ ]:


tst_dl = dls.valid.new(to_tst)
tst_dl.show_batch()


# In[ ]:


learn.metrics = []
tst_preds,_ = learn.get_preds(dl=tst_dl)


# In[ ]:


res1 = np.expm1(tst_preds)
res2 = list(map(lambda x: x[0], res1.numpy()))
res3 = list(map(lambda x: x[1], res1.numpy()))
submit = pd.DataFrame({'ConfirmedCases': res2, 'Fatalities': res3})
submit.index = test_df.ForecastId


# In[ ]:


submit.to_csv('submission.csv')


# # Example predictions on our validation set.
# 
# Display some interesting countries to see if our model performs any good.

# In[ ]:


import seaborn as sns

min_date = test_df.Date.min()
max_date = train_df.Date.max()

f, axes = plt.subplots(10, 1, figsize=(16, 60))

def plot_preds(country, ax):
    targets = train_df[(train_df['Country_Region'] == country) & (train_df['Date'] >= min_date)].ConfirmedCases
    subset = test_df[(test_df['Country_Region'] == country) & (test_df['Date'] <= max_date)]
    
    idx = subset.index
    dates = subset.Date
    predicted = submit.iloc[idx].ConfirmedCases
    
    targets.index = dates
    predicted.index = dates
    
    combined = pd.DataFrame({'real' : targets, 'pred': predicted})
    
    sns.lineplot(data=combined, ax=axes[ax]).set_title(country)

plot_preds('Italy', 0)
plot_preds('Spain', 1)
plot_preds('Germany', 2)
plot_preds('Poland', 3)
plot_preds('Czechia', 4)
plot_preds('Russia', 5)
plot_preds('Iran', 6)
plot_preds('Sweden', 7)
plot_preds('Japan', 8)
plot_preds('Belgium', 9)


# # Conclusion
# 
# As neural networks are thought not to perform well on tabular data, which is true especially for some trivial architectures like MLP used in fast.ai tabular v1.
# 
# There is quite a lot to explore in this TabNet, in terms of hyperparameters and feature selection, so I would expect a much better performance with tuning.
# 
# # [#masks4all](https://masks4all.co/why-we-need-mandatory-mask-laws-masks4all/)
