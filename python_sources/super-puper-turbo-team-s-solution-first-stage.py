#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import cross_val_score, GroupKFold, TimeSeriesSplit, GridSearchCV
from sklearn.metrics import fbeta_score, confusion_matrix, make_scorer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from matplotlib import pyplot as plt
from lightgbm import LGBMClassifier

get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")


# In[ ]:


employees_data = pd.read_csv('../input/softserve-ds-hackathon-2020/employees.csv', parse_dates=['HiringDate', 'DismissalDate'])
history_data = pd.read_csv('../input/softserve-ds-hackathon-2020/history.csv', parse_dates=['Date'])
submission_data = pd.read_csv('../input/softserve-ds-hackathon-2020/submission.csv')

print(employees_data.shape, history_data.shape, submission_data.shape)
print(employees_data['EmployeeID'].nunique(), history_data['EmployeeID'].nunique(), submission_data['EmployeeID'].nunique())


# ## Feature engineering

# In[ ]:


# PREDICT_MONTHS = 3
PREDICT_MONTHS = 5


# In[ ]:


df = history_data.merge(employees_data, how='outer', on='EmployeeID')
df['months_to_dissmiss'] = (df['DismissalDate'].sub(df['Date']) / np.timedelta64(1, 'M')).round()
df['target'] = (df['months_to_dissmiss'] <= PREDICT_MONTHS).astype(int)
df['experience_months'] = (df['Date'].sub(df['HiringDate']) / np.timedelta64(1, 'M')).round()
df['experience_years'] = (df['Date'].sub(df['HiringDate']) / np.timedelta64(1, 'Y')).round()

df['ProjectID'] = df['ProjectID'].fillna(0)

df.shape


# In[ ]:


# clean data
guys_who_word_after_dissmissal = df[df['Date'] > df['DismissalDate']]['EmployeeID'].unique()
df.drop(df[df['EmployeeID'].isin(guys_who_word_after_dissmissal)].index, inplace=True)


# Additional data source - https://jobs.dou.ua/trends/ (2 charts)

# In[ ]:


applications = pd.read_csv('../input/trends-data-from-dou/applications.csv', parse_dates=['Date'])
vacancies = pd.read_csv('../input/trends-data-from-dou/vacancies.csv', parse_dates=['Date'])
df = df.merge(applications, on='Date', how='outer')
df = df.merge(vacancies, on='Date', how='outer')
df.shape


# In[ ]:


cols_categorical = ['DevCenterID', 'SBUID', 'PositionID', 'CustomerID', 'ProjectID', 
               'CompetenceGroupID', 'FunctionalOfficeID', 'PaymentTypeId']
cols_numerical = ['PositionLevel', 
              'LanguageLevelID', 'IsTrainee', 'IsInternalProject', 'OnSite', 'Utilization', 'HourVacation', 
                'HourMobileReserve', 'HourLockedReserve', 'BonusOneTime', 'APM', 
                'WageGross', 
                  'MonthOnPosition', 'MonthOnSalary', 
                  'experience_months', 
                  'experience_years', 
#                   'experience_yearmonths',
                  'times_wage_changed', 'times_posit_lvl_changed', 'times_lang_lvl_changed',
#               'times_wage_inc', 'times_wage_dec', 'times_posit_lvl_inc', 
#                   'times_posit_lvl_dec', 'times_lang_lvl_inc', 'times_lang_lvl_dec',
                  'times_project_changed', 'times_customer_changed', 'times_position_changed',
                  'times_dev_center_changed', 'times_sbuid_changed', 'times_compet_group_changed',
                  'times_funct_office_changed', 'times_payment_type_changed',
#                   'num_unique_projects', 'num_unique_customers', 'num_unique_positions',
#                   'num_unique_position_lvls', 'num_unique_lang_lvls', 
#                   'num_unique_dev_centers', 'num_unique_sbuids', 'num_unique_compet_groups', 
#                   'num_unique_funct_offices', 'num_unique_payment_types', 
                  'cumulative_hour_mobile_reserve', 'cumulative_hour_locked_reserve', 'cumulative_hour_vacation',
                  'cumulative_bonus', 'cumulative_wage', 'cumulative_apm',
#                   'mean_hour_vacation', 'mean_bonus', 'mean_wage', 'mean_apm', 'mean_utilization',
                  'max_hour_vacation', 'max_bonus', 
#                   'max_wage', 
                  'max_apm', 
#                   'min_wage', 
                  'min_apm', 
                  'months_on_internal_proj', 'months_on_site',
                  'was_trainee',
#                  'wage_normalized_for_position_id', 'wage_normalized_for_position_lvl',
#                   'cumulative_wage_6months', 'cumulative_wage_3months',
                  'wage_back_1month', 'wage_back_2months', 
                  'wage_back_3months', 'wage_back_4months', 
                  'wage_back_5months',
#                   'wage_back_6months', 
#                   'wage_back_7months', 'wage_back_8months',
                  'lang_lvl_back_1month', 'lang_lvl_back_2months', 'lang_lvl_back_3months', 
                  'lang_lvl_back_4months', 'lang_lvl_back_5months',
                  'Vacancies', 'Applications'
                 ]

print(len(cols_categorical), len(cols_numerical))


# In[ ]:


get_ipython().run_cell_magic('time', '', "changes = df.groupby('EmployeeID').apply(lambda x: pd.concat((x['EmployeeID'], \n#     (x['WageGross'].diff() > 0).cumsum().rename('times_wage_inc'),\n#     (x['WageGross'].diff() < 0).cumsum().rename('times_wage_dec'),\n    (x['WageGross'].diff() != 0).cumsum().rename('times_wage_changed'),\n#     (x['PositionLevel'].diff() > 0).cumsum().rename('times_posit_lvl_inc'),\n#     (x['PositionLevel'].diff() < 0).cumsum().rename('times_posit_lvl_dec'),\n    (x['PositionLevel'].diff() != 0).cumsum().rename('times_posit_lvl_changed'),\n#     (~x['PositionLevel'].duplicated()).cumsum().rename('num_unique_position_lvls'),\n#     (x['LanguageLevelID'].diff() > 0).cumsum().rename('times_lang_lvl_inc'),\n#     (x['LanguageLevelID'].diff() < 0).cumsum().rename('times_lang_lvl_dec'),\n    (x['LanguageLevelID'].diff() != 0).cumsum().rename('times_lang_lvl_changed'),\n    x['LanguageLevelID'].shift(periods=1, fill_value=0).rename('lang_lvl_back_1month'),\n    x['LanguageLevelID'].shift(periods=2, fill_value=0).rename('lang_lvl_back_2months'),\n    x['LanguageLevelID'].shift(periods=3, fill_value=0).rename('lang_lvl_back_3months'),\n    x['LanguageLevelID'].shift(periods=4, fill_value=0).rename('lang_lvl_back_4months'),\n    x['LanguageLevelID'].shift(periods=5, fill_value=0).rename('lang_lvl_back_5months'),\n#     (~x['LanguageLevelID'].duplicated()).cumsum().rename('num_unique_lang_lvls'),\n#     (~x['ProjectID'].duplicated()).cumsum().rename('num_unique_projects'),\n#     (~x['CustomerID'].duplicated()).cumsum().rename('num_unique_customers'),\n#     (~x['PositionID'].duplicated()).cumsum().rename('num_unique_positions'),\n#     (~x['DevCenterID'].duplicated()).cumsum().rename('num_unique_dev_centers'),\n#     (~x['SBUID'].duplicated()).cumsum().rename('num_unique_sbuids'),\n#     (~x['CompetenceGroupID'].duplicated()).cumsum().rename('num_unique_compet_groups'),\n#     (~x['FunctionalOfficeID'].duplicated()).cumsum().rename('num_unique_funct_offices'),\n#     (~x['PaymentTypeId'].duplicated()).cumsum().rename('num_unique_payment_types'),\n    x['ProjectID'].ne(x['ProjectID'].shift(1).bfill()).cumsum().rename('times_project_changed'),\n    x['CustomerID'].ne(x['CustomerID'].shift(1).bfill()).cumsum().rename('times_customer_changed'),\n    x['PositionID'].ne(x['PositionID'].shift(1).bfill()).cumsum().rename('times_position_changed'),\n    x['DevCenterID'].ne(x['DevCenterID'].shift(1).bfill()).cumsum().rename('times_dev_center_changed'),\n    x['SBUID'].ne(x['SBUID'].shift(1).bfill()).cumsum().rename('times_sbuid_changed'),\n    x['CompetenceGroupID'].ne(x['CompetenceGroupID'].shift(1).bfill()).cumsum().rename('times_compet_group_changed'),\n    x['FunctionalOfficeID'].ne(x['FunctionalOfficeID'].shift(1).bfill()).cumsum().rename('times_funct_office_changed'),\n    x['PaymentTypeId'].ne(x['PaymentTypeId'].shift(1).bfill()).cumsum().rename('times_payment_type_changed'),\n    x['HourMobileReserve'].cumsum().rename('cumulative_hour_mobile_reserve'),\n    x['HourLockedReserve'].cumsum().rename('cumulative_hour_locked_reserve'),\n    x['HourVacation'].cumsum().rename('cumulative_hour_vacation'),\n    x['HourVacation'].cummax().rename('max_hour_vacation'),\n#     x['HourVacation'].expanding().mean().rename('mean_hour_vacation'),\n    x['BonusOneTime'].cumsum().rename('cumulative_bonus'),\n    x['BonusOneTime'].cummax().rename('max_bonus'),\n#     x['BonusOneTime'].expanding().mean().rename('mean_bonus'),\n    x['WageGross'].cumsum().rename('cumulative_wage'),\n#     x['WageGross'].cummax().rename('max_wage'),\n#     x['WageGross'].cummin().rename('min_wage'),\n#     x['WageGross'].rolling(min_periods=1, window=6).sum().rename('cumulative_wage_6months'),\n#     x['WageGross'].rolling(min_periods=1, window=3).sum().rename('cumulative_wage_3months'),\n    x['WageGross'].shift(periods=1, fill_value=0).rename('wage_back_1month'),\n    x['WageGross'].shift(periods=2, fill_value=0).rename('wage_back_2months'),\n    x['WageGross'].shift(periods=3, fill_value=0).rename('wage_back_3months'),\n    x['WageGross'].shift(periods=4, fill_value=0).rename('wage_back_4months'),\n    x['WageGross'].shift(periods=5, fill_value=0).rename('wage_back_5months'),\n#     x['WageGross'].shift(periods=6, fill_value=0).rename('wage_back_6months'),\n#     x['WageGross'].shift(periods=7, fill_value=0).rename('wage_back_7months'),\n#     x['WageGross'].shift(periods=8, fill_value=0).rename('wage_back_8months'),\n#     x['WageGross'].expanding().mean().rename('mean_wage'),\n    x['APM'].cumsum().rename('cumulative_apm'),\n    x['APM'].cummax().rename('max_apm'),  \n    x['APM'].cummin().rename('min_apm'),\n#     x['APM'].expanding().mean().rename('mean_apm'),\n#     x['Utilization'].expanding().mean().rename('mean_utilization'),\n    x['IsInternalProject'].cumsum().rename('months_on_internal_proj'),\n    x['OnSite'].cumsum().rename('months_on_site'),                                                          \n    x['Date']), axis=1))\n\ndf_with_feats = df.merge(changes, on=['EmployeeID', 'Date'], how='outer')\n# changes")


# In[ ]:


was_trainee = df_with_feats.groupby('EmployeeID')['IsTrainee'].max().rename('was_trainee')
df_with_feats = df_with_feats.merge(was_trainee, on='EmployeeID', how='outer')


# In[ ]:


df_with_feats[cols_categorical] = df_with_feats[cols_categorical].astype(str)
df_with_feats[cols_numerical] = df_with_feats[cols_numerical].astype(float)

train_raw = df_with_feats[~(df_with_feats['DismissalDate'].isna())].copy()
test_raw = df_with_feats[df_with_feats['DismissalDate'].isna()].copy()

print(train_raw.shape, test_raw.shape)


# ## Composing train df, CV scheme

# 1) Take "target 1" samples from "train", and "target 0" samples from "test without last 3 months" (thus we are sure employee will not dissmiss in next 3 month, while also maintaining data variance)

# 2) Make sure all 3 "target 1" samples for one person go entirely to train or test fold - to prevent data leak - use GroupKFold, where groups are EmployeeIDs

# In[ ]:


train_ones = train_raw[train_raw['target'] == 1]

# select rows exept last 3 rows, per employee
train_zeros = test_raw.groupby('EmployeeID').apply(lambda df: df[df['Date'] <= 
                                                             (df['Date'].max() - np.timedelta64(3, 'M'))]) \
    .reset_index(level=0, drop=True)
# select random row per employee
train_zeros = train_zeros.groupby('EmployeeID')     .apply(lambda df: df.sample(1, random_state=(abs(hash(df.iloc[0]['EmployeeID'])) % (10 ** 9))))     .reset_index(drop=True)

# train_zeros = pd.concat((train_zeros, train_zeros_1))
train_zeros['target'] = 0

train = pd.concat((train_zeros, train_ones))

# shuffle (to mix 1s and 0s) and sort by date
train = train.sample(frac=1, random_state=1)
train = train.sort_values(by='Date')

print(train.shape)
train['target'].value_counts()


# In[ ]:


X_train = train.drop('target', axis=1)
y_train = train['target']

# test on last month from "test_raw" dataframe
test_date = test_raw.groupby('EmployeeID')['Date'].max()
X_test = test_raw.drop('target', axis=1)
X_test = X_test.merge(test_date, on=['EmployeeID', 'Date'], how='inner')

# remove redundant 200 employees
X_test = X_test.merge(submission_data, on='EmployeeID', how='inner')
X_test = X_test.drop('target', axis=1)

print(X_train.shape, y_train.shape, X_test.shape)


# In[ ]:


# cv = GroupKFold(n_splits=10)
cv = TimeSeriesSplit(n_splits=10)
scorer = make_scorer(fbeta_score, beta=1.7)


# ## Pipeline

# In[ ]:


class ThresholdRandomForestClassifier(RandomForestClassifier):
    def __init__(self, n_estimators=100,
                        criterion='gini',
                        max_depth=None,
                        min_samples_split=2,
                        min_samples_leaf=1,
                        min_weight_fraction_leaf=0.0,
                        max_features='auto',
                        max_leaf_nodes=None,
                        min_impurity_decrease=0.0,
                        min_impurity_split=None,
                        bootstrap=True,
                        oob_score=False,
                        n_jobs=None,
                        random_state=None,
                        verbose=0,
                        warm_start=False,
                        class_weight=None,
                        ccp_alpha=0.0,
                        max_samples=None,
                        threshold=0.5):
        super().__init__(n_estimators, criterion, max_depth, min_samples_split, min_samples_leaf, 
                         min_weight_fraction_leaf, max_features, max_leaf_nodes, min_impurity_decrease,
                        min_impurity_split, bootstrap, oob_score, n_jobs, random_state, verbose, warm_start,
                        class_weight, ccp_alpha, max_samples)
        self.threshold = threshold
        
    def predict(self, X):
        return (RandomForestClassifier.predict_proba(self, X)[:, 1] > self.threshold).astype(int)


# In[ ]:


class ItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]

# clf = LGBMClassifier(max_depth=64, n_estimators=1000, random_state=1)
clf = ThresholdRandomForestClassifier(threshold=0.5, n_estimators=2000, random_state=1, class_weight='balanced')
# clf = ExtraTreeClassifier(random_state=1, class_weight='balanced')
    
pipe = Pipeline([
    ('union', FeatureUnion([
        ('column_transformer', ColumnTransformer([
            ('ohe', OneHotEncoder(handle_unknown='ignore'), cols_categorical),
#             ('scaler', StandardScaler(), cols_need_scaling)
        ])),
        ('item_selector', ItemSelector(cols_numerical))
    ])),
    ('clf', clf)
])


# In[ ]:


def make_submission(model, X_train, y_train, X_test, submission_file_name='submission.csv'):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    submission = pd.DataFrame({'EmployeeID': X_test['EmployeeID'], 'target': y_pred})
    submission.to_csv(submission_file_name, index=False)
    
    return submission


# ## Testing

# ### Random forest

# In[ ]:


score = cross_val_score(pipe, X_train, y_train, cv=cv, groups=X_train['EmployeeID'], 
                        n_jobs=-1, scoring=scorer)
score, score.mean(), score.std()


# In[ ]:


submission = make_submission(pipe, X_train, y_train, X_test, 'submission.csv')
submission['target'].value_counts()


# In[ ]:




