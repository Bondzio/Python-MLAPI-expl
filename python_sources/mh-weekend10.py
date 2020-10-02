#!/usr/bin/env python
# coding: utf-8

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


import pandas_profiling 


# In[ ]:


raw_data = pd.read_csv("/kaggle/input/vg-sales-pred/Data/Train.csv")
test_data = pd.read_csv("/kaggle/input/vg-sales-pred/Data/Test.csv")


# In[ ]:


raw_data.head()


# In[ ]:


import catboost


# In[ ]:


CReg = catboost.CatBoostRegressor(cat_features=['CONSOLE', 'CATEGORY', 'PUBLISHER', 'RATING'], n_estimators=100. )#learning_rate=0.001, iterations=1200)


# In[ ]:


raw_data.sh


# In[ ]:


CReg.fit(raw_data.drop(['SalesInMillions','ID'], axis=1), 
         raw_data['SalesInMillions'], verbose=0)


# In[ ]:


print(CReg.best_score_)


# In[ ]:


print(CReg.eval_metrics)


# In[ ]:


CReg.predict(test_data.drop(['ID'], axis=1))


# In[ ]:


sub_file = pd.read_csv("/kaggle/input/vg-sales-pred/Data/Sample_Submission.csv")


# In[ ]:


sub_file['SalesInMillions'] = CReg.predict(test_data)


# In[ ]:


# sub = pd.read_excel("/kaggle/input/mh-financial-risk/Financial_Risk_Participants_Data/Sample_Submission.xlsx")

# submit_df = pd.DataFrame(test_prediction,  columns=['0','1'])

from IPython.display import FileLink
sub_name = "cat_baseline4"
sub_file.to_csv(sub_name+'.csv', index=False)
FileLink(sub_name+'.csv')


# In[ ]:


print(pd.read_csv("/kaggle/input/vg-sales-pred/Data/Sample_Submission.csv").head())


# In[ ]:


import lightgbm


# In[ ]:


LGB = lightgbm.LGBMRegressor()


# In[ ]:


LGB.fit(raw_data.drop(['SalesInMillions','ID','CONSOLE', 'CATEGORY', 'PUBLISHER', 'RATING'], axis=1), 
         raw_data['SalesInMillions'], verbose=2)


# In[ ]:


print(LGB.n_estimators)


# In[ ]:


LGB.predict(test_data.drop(['ID','CONSOLE', 'CATEGORY', 'PUBLISHER', 'RATING'], axis=1))


# In[ ]:


sub_file2 = pd.read_csv("/kaggle/input/vg-sales-pred/Data/Sample_Submission.csv")
sub_file2['SalesInMillions'] = LGB.predict(test_data.drop(['ID','CONSOLE', 'CATEGORY', 'PUBLISHER', 'RATING'], axis=1))

from IPython.display import FileLink
sub_name = "lgb_baseline1"
sub_file2.to_csv(sub_name+'.csv', index=False)
FileLink(sub_name+'.csv')


# In[ ]:


sub3 = (sub_file + sub_file2)/2

sub_name = "lgb_cat_baseline1"
sub3.to_csv(sub_name+'.csv', index=False)
FileLink(sub_name+'.csv')


# In[ ]:


sub3


# In[ ]:


import xgboost


# In[ ]:


XGB = xgboost.XGBRegressor()


# In[ ]:


XGB.fit(raw_data.drop(['SalesInMillions','ID','CONSOLE', 'CATEGORY', 'PUBLISHER', 'RATING'], axis=1), 
         raw_data['SalesInMillions'], verbose=2)


# In[ ]:


sub_file4 = pd.read_csv("/kaggle/input/vg-sales-pred/Data/Sample_Submission.csv")
sub_file4['SalesInMillions'] = XGB.predict(test_data.drop(['ID','CONSOLE', 'CATEGORY', 'PUBLISHER', 'RATING'], axis=1))

from IPython.display import FileLink
sub_name = "xgb_baseline1"
sub_file4.to_csv(sub_name+'.csv', index=False)
FileLink(sub_name+'.csv')


# In[ ]:


sub4 = (sub_file + sub_file2 + sub_file4)/3

sub_name = "lgb_cat__xgb_baseline1"
sub3.to_csv(sub_name+'.csv', index=False)
FileLink(sub_name+'.csv')


# In[ ]:


sub3.head()


# In[ ]:


sub4.head()


# In[ ]:


CReg2 = catboost.CatBoostRegressor()#learning_rate=0.001, iterations=1200)


# In[ ]:


CReg2.fit(raw_data.drop(['SalesInMillions','ID','CONSOLE', 'CATEGORY', 'PUBLISHER', 'RATING'], axis=1), 
         raw_data['SalesInMillions'], verbose=2)


# In[ ]:


sub_file5 = pd.read_csv("/kaggle/input/vg-sales-pred/Data/Sample_Submission.csv")
sub_file5['SalesInMillions'] = CReg2.predict(test_data.drop(['ID','CONSOLE', 'CATEGORY', 'PUBLISHER', 'RATING'], axis=1))

from IPython.display import FileLink
sub_name = "final_mh10"
sub_file5.to_csv(sub_name+'.csv', index=False)
FileLink(sub_name+'.csv')


# In[ ]:




