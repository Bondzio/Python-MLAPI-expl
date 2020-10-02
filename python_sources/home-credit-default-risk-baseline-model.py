#!/usr/bin/env python
# coding: utf-8

# <h1><center><font size="6">Home Credit Default Risk baseline model</font></center></h1>
# > ****
# 
# Many people struggle to get loans due to insufficient or non-existent credit histories. And, unfortunately, this population is often taken advantage of by untrustworthy lenders.
# 
# Home Credit Group
# 
# Home Credit strives to broaden financial inclusion for the unbanked population by providing a positive and safe borrowing experience. In order to make sure this underserved population has a positive loan experience, Home Credit makes use of a variety of alternative data--including telco and transactional information--to predict their clients' repayment abilities.
# 
# While Home Credit is currently using various statistical and machine learning methods to make these predictions, they're challenging Kagglers to help them unlock the full potential of their data. Doing so will ensure that clients capable of repayment are not rejected and that loans are given with a principal, maturity, and repayment calendar that will empower their clients to be successful.

# The point of this kernel is to show that you can sometimes get an acceptable baseline model without digging deep into the data. I am in no way encouraging this way of doing data science, because it is not half as much fun :)
# I am so impressed by the calibre of people in this community. I just wanted to share something quick and easy. If you like this kernel, please upvote. If you dont like it, then definetely comment, that way I like so many of you can be a better DS tomorrow, than I am today. Cheers to us.

# <img src="https://storage.googleapis.com/kaggle-media/competitions/home-credit/about-us-home-credit.jpg"></img>

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

# Because we only care about errors
import warnings
warnings.filterwarnings('ignore')

# Because thats where they keep the files
import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.
#machine learning libraries
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, average_precision_score, f1_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import scale
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
seed = 42


# In[ ]:


# Load everything because we are crazy like that
previous_application = pd.read_csv('../input/previous_application.csv', sep=',')
POS_CASH_balance = pd.read_csv('../input/POS_CASH_balance.csv', sep=',')
installments_payments = pd.read_csv('../input/installments_payments.csv', sep=',')
credit_card_balance = pd.read_csv('../input/credit_card_balance.csv', sep=',')
bureau_balance = pd.read_csv('../input/bureau_balance.csv', sep=',')
bureau = pd.read_csv('../input/bureau.csv', sep=',')
application_train = pd.read_csv('../input/application_train.csv', sep=',')
application_test = pd.read_csv('../input/application_test.csv', sep=',')


# In[ ]:


#Nothing fancy just grouping by the primary key
bureau_balance_dumm = bureau_balance.groupby(['SK_ID_BUREAU']).sum()
bureau_balance_dumm = bureau_balance_dumm.reset_index('SK_ID_BUREAU')
bureau_balance_dumm.head()


# Drop primary key and get ready for joins post grouping by 'SK_ID_CURR'

# In[ ]:



bureau_merge = pd.merge(bureau, bureau_balance_dumm,  how='left')
bureau_merge_dumm = bureau_merge.drop(['SK_ID_BUREAU'],axis = 1)
bureau_merge_dumm = bureau_merge_dumm.groupby(['SK_ID_CURR']).sum()
bureau_merge_dumm = bureau_merge_dumm.reset_index('SK_ID_CURR')
bureau_merge_dumm.head()


# In[ ]:


POS_CASH_balance_loc = POS_CASH_balance.drop(['SK_ID_PREV'],axis = 1)
POS_CASH_balance_dumm = POS_CASH_balance_loc.groupby(['SK_ID_CURR']).sum()
POS_CASH_balance_dumm = POS_CASH_balance_dumm.reset_index('SK_ID_CURR')
POS_CASH_balance_dumm.head()


# In[ ]:


previous_application_loc = previous_application.drop(['SK_ID_PREV'],axis = 1)
previous_application_dumm = previous_application_loc.groupby(['SK_ID_CURR']).sum()
previous_application_dumm = previous_application_dumm.reset_index('SK_ID_CURR')
previous_application_dumm.head()


# In[ ]:


installments_payments_loc = installments_payments.drop(['SK_ID_PREV'],axis = 1)
installments_payments_dumm = installments_payments_loc.groupby(['SK_ID_CURR']).sum()
installments_payments_dumm = installments_payments_dumm.reset_index('SK_ID_CURR')
installments_payments_dumm.head()


# In[ ]:


credit_card_balance_loc = credit_card_balance.drop(['SK_ID_PREV'],axis = 1)
credit_card_balance_dumm = credit_card_balance_loc.groupby(['SK_ID_CURR']).sum()
credit_card_balance_dumm = credit_card_balance_dumm.reset_index('SK_ID_CURR')
credit_card_balance_dumm.head()


# Merge both train and test files for final prediction

# In[ ]:


merge1 = pd.merge(application_train, bureau_merge_dumm,  how='left')
merge2 = pd.merge(merge1, POS_CASH_balance_dumm,   how='left')
merge3 = pd.merge(merge2, previous_application_dumm,  how='left')
merge4 = pd.merge(merge3, installments_payments_dumm,  how='left')
merge5 = pd.merge(merge4, credit_card_balance_dumm,  how='left')


# In[ ]:


merge1_test = pd.merge(application_test, bureau_merge_dumm, how='left')
merge2_test = pd.merge(merge1_test, POS_CASH_balance_dumm,  how='left')
merge3_test = pd.merge(merge2_test, previous_application_dumm,  how='left')
merge4_test = pd.merge(merge3_test, installments_payments_dumm,  how='left')
merge5_test = pd.merge(merge4_test, credit_card_balance_dumm, how='left')


# This function cleans and does some basic operation to get the model ready for scoring, feel free to improve on it.

# In[ ]:


# Training function
def data_prep_train(data_df):
    
    #how to handle types
    data_df = data_df.set_index('SK_ID_CURR')
    data_df_num = data_df.select_dtypes(exclude=object)
    data_df_obj = data_df.select_dtypes(include=object)

    #how to handle nan in numeric type
    data_df_num_columns = data_df_num.drop(['TARGET'], axis=1).columns
    for column in data_df_num_columns:
        data_df_num[column] = data_df_num[column].fillna(data_df_num[column].mean())
        #data_df_num[column] = scale(data_df_num[column])
    
    #how to handle nan in object type
    data_df_obj_columns = data_df_obj.columns
    for column in data_df_obj_columns:
        data_df_obj[column] = data_df_obj[column].fillna("UNKNOWN")
        data_df_obj[column] = data_df_obj[column].astype('category')
        data_df_obj[column] = data_df_obj[column].cat.codes
    # stage for sampling
    data_stage = pd.DataFrame(pd.concat([data_df_num, data_df_obj],axis=1))
    
    # sample count positive class 
    minority_count = data_stage.TARGET.value_counts().min()
    majority_count = data_stage.TARGET.value_counts().max()
    
    # sampled data (down sampling)
    data_stage0 = data_stage[data_stage['TARGET']==0].sample(majority_count, replace = False)
    data_stage1 = data_stage[data_stage['TARGET']==1].sample(minority_count, replace = False)
    
    return pd.DataFrame(pd.concat([data_stage0, data_stage1],axis=0))


# Testing function
def data_prep_test(data_df):
    
    #how to handle types
    data_df = data_df.set_index('SK_ID_CURR')
    data_df_num = data_df.select_dtypes(exclude=object)
    data_df_obj = data_df.select_dtypes(include=object)

    #how to handle nan in numeric type
    data_df_num_columns = data_df_num.columns
    for column in data_df_num_columns:
        data_df_num[column] = data_df_num[column].fillna(data_df_num[column].mean())
        #data_df_num[column] = scale(data_df_num[column])
    
    #how to handle nan in object type
    data_df_obj_columns = data_df_obj.columns
    
    for column in data_df_obj_columns:
        data_df_obj[column] = data_df_obj[column].fillna("UNKNOWN")#.astype('object')
        data_df_obj[column] = data_df_obj[column].astype('category')
        data_df_obj[column] = data_df_obj[column].cat.codes
    # stage for sampling
    data_stage = pd.DataFrame(pd.concat([data_df_num, data_df_obj],axis=1))
    
    
    return pd.DataFrame(pd.concat([data_df_num, data_df_obj],axis=1))


# In[ ]:


#Train
data_train = data_prep_train(merge5)

#Test
#data_pred = pd.read_csv('application_test.csv', sep=',')
data_pred = data_prep_test(merge5_test)


# In[ ]:


data_train.head()


# In[ ]:


data_pred.head()


# Drop all columns which has NA's, these will be categorical NA's as we have handled numerical NAs already

# In[ ]:


missing_values = ["CNT_INSTALMENT","CNT_INSTALMENT_FUTURE","SK_DPD","SK_DPD_DEF","AMT_APPLICATION",
                  "AMT_DOWN_PAYMENT","NFLAG_LAST_APPL_IN_DAY","RATE_DOWN_PAYMENT","RATE_INTEREST_PRIMARY",
                  "RATE_INTEREST_PRIVILEGED","DAYS_DECISION","SELLERPLACE_AREA","CNT_PAYMENT","DAYS_FIRST_DRAWING",
                  "DAYS_FIRST_DUE","DAYS_LAST_DUE_1ST_VERSION","DAYS_LAST_DUE","DAYS_TERMINATION",
                  "NFLAG_INSURED_ON_APPROVAL","AMT_INST_MIN_REGULARITY","AMT_PAYMENT_CURRENT",
                  "AMT_PAYMENT_TOTAL_CURRENT","AMT_RECEIVABLE_PRINCIPAL","AMT_RECIVABLE","AMT_TOTAL_RECEIVABLE",
                  "CNT_DRAWINGS_ATM_CURRENT","CNT_DRAWINGS_CURRENT","CNT_DRAWINGS_OTHER_CURRENT",
                  "CNT_DRAWINGS_POS_CURRENT","CNT_INSTALMENT_MATURE_CUM","AMT_BALANCE","AMT_CREDIT_LIMIT_ACTUAL",
                  "AMT_DRAWINGS_ATM_CURRENT","AMT_DRAWINGS_CURRENT","AMT_DRAWINGS_OTHER_CURRENT","AMT_DRAWINGS_POS_CURRENT" ]


# In[ ]:


data_train = data_train.drop(missing_values, axis=1)


# In[ ]:


data_pred = data_pred.drop(missing_values, axis = 1 )


# No missing values now :)

# In[ ]:


(data_train.isna().sum()>1).sum(), (data_pred.isna().sum()>1).sum()


# In[ ]:


data_train.shape, data_pred.shape


# In[ ]:


# train test split doesnt actually split
# Will be training on 95% of the data and not 100%, because then i will have to rewrite part of
# this code and i am lazy.
X_train, X_test, y_train, y_test = train_test_split(data_train.drop(['TARGET'],axis = 1),
                                                    data_train['TARGET'], test_size = 0.05,
                                                    random_state = seed)
X_test_final = data_pred


# Using smote to increase the number of under-represented class
sm = SMOTE(random_state = seed, ratio = 'minority')


# In[ ]:


X_train_sm, y_train_sm = sm.fit_sample(X_train, y_train)
X_train_sm.shape, y_train_sm.shape


# In[ ]:


import lightgbm as lgb
def run_lgb(train_X, train_y, val_X, val_y, test_X):
    params = {
        "objective" : "binary",
        "metric" : "auc",
        "num_leaves" : 40,
        "learning_rate" : 0.005,
        #"bagging_fraction" : 0.6,
        "feature_fraction" : 0.6,
        "bagging_frequency" : 6,
        "bagging_seed" : 42,
        "verbosity" : -1,
        "seed": 42
    }
    
    lgtrain = lgb.Dataset(train_X, label=train_y)
    lgval = lgb.Dataset(val_X, label=val_y)
    evals_result = {}
    model = lgb.train(params, lgtrain, 5000, 
                      valid_sets=[lgtrain, lgval], 
                      early_stopping_rounds=100, 
                      verbose_eval=150, 
                      evals_result=evals_result)
    
    pred_test_y = (model.predict(test_X, num_iteration=model.best_iteration))
    return pred_test_y, model, evals_result


# Checking if SMOTE is better than no SMOTE, if you dont know what SMOTE is google it, sometimes for some data sets it is awesome. But then again there is no free meal, you got to try everything. Now that i think of it, i could have also tried downsampling, but personally I dont like throwing away data. But for some data sets down sampling could be the key. But as i have said before, this is the lazy approach ;)

# > Go ahead and check why i didnt use SMOTE in the final model scoring :)

# In[ ]:


# Training LGB with SMOTE
#pred_test_SMOTE, model, evals_result = run_lgb(X_train_sm, y_train_sm, X_test, y_test, data_pred)
#print("LightGBM with SMOTE Training Completed ...")


# In[ ]:


# Training LGB without sampling
pred_test, model, evals_result = run_lgb(X_train, y_train ,X_test, y_test, data_pred)
print("LightGBM Training Completed...")


# In[ ]:


sub = pd.read_csv('../input/sample_submission.csv')

#sub_lgb_SMOTE = pd.DataFrame()
#sub_lgb_SMOTE["TARGET"] = pred_test_SMOTE

sub_lgb = pd.DataFrame()
sub_lgb["TARGET"] = pred_test

# The SMOTE version is overfitting. 
# This is evidenced by the difference in train test you can check it out
#sub["TARGET"] = (sub_lgb_SMOTE["TARGET"])* 0.0 + sub_lgb["TARGET"] * 1.0)

sub["TARGET"] = sub_lgb["TARGET"]


# In[ ]:


print(sub.head())
sub.to_csv('submission_lazy.csv', index=False)


# This model scores about 0.74429 without almost any feature engineering in the public leaderboard

# In[ ]:


0.74429

