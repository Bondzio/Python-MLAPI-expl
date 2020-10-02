#!/usr/bin/env python
# coding: utf-8

# # Overview

# The purpose of this kernel is to draw the relationship between train data and test data and make assumptions about hypothesis construction.
# Thanks to the kernel author for reference.<br>
# There is a negative correlation between training data and test data.
# Therefore, I think that CV score is low in the part where the number of test data is small.
# There is little time left, but I'm thinking of doing the following.
# <br>Please comment if I said something off target.
# 1. Change the threshold according to the number of training data when giving pseudo labels
# 2. Change the threshold according to the number of training data when flipping training data labels
# 3. Focus and tune on the set with few training data

# In[ ]:


import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
from sklearn.pipeline import Pipeline
from tqdm import tqdm_notebook
import warnings
import multiprocessing
from scipy.optimize import minimize  
import time
warnings.filterwarnings('ignore')


# In[ ]:


# LOAD DATA
train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')
cols = [c for c in train.columns if c not in ['id', 'target', 'wheezy-copper-turtle-magic']]
print(f"train shape is {train.shape}, test shape is {test.shape}")


# # Predict with the QDA using original training data.

# In[ ]:


# SET THE MAGIC NUBER(512)
magic_num = len(train['wheezy-copper-turtle-magic'].unique())
print(f'wheezy-copper-turtle-magic has {magic_num} unique values.')

# INITIALIZE VARIABLES
oof = np.zeros(len(train))
preds = np.zeros(len(test))

train_set = []
test_set = []
total_set = []
for i in tqdm_notebook(range(magic_num)):
# for i in tqdm_notebook(range(2)):
    # ONLY TRAIN WITH DATA WHERE WHEEZY EQUALS I
    train2 = train[train['wheezy-copper-turtle-magic']==i]
    test2 = test[test['wheezy-copper-turtle-magic']==i]
    idx1 = train2.index; idx2 = test2.index
    train2.reset_index(drop=True,inplace=True)
 
    #NUMBER OF DATA INCLUDED DATA WHERE WHEEZY EQUALS I
    train_set.append(train2.shape[0])
    test_set.append(test2.shape[0])
    total_set.append(train2.shape[0]+test2.shape[0])

    # FEATURE SELECTION (USE APPROX 40 OF 255 FEATURES)
    sel = VarianceThreshold(threshold=1.5).fit(train2[cols])
    train3 = sel.transform(train2[cols])
    test3 = sel.transform(test2[cols])
    
    # STRATIFIED K-FOLD
    skf = StratifiedKFold(n_splits=11, random_state=42, shuffle=True)
    for train_index, test_index in skf.split(train3, train2['target']):
        # MODEL AND PREDICT WITH QDA
        clf = QuadraticDiscriminantAnalysis(reg_param=0.5)
        clf.fit(train3[train_index,:],train2.loc[train_index]['target'])
        oof[idx1[test_index]] = clf.predict_proba(train3[test_index,:])[:,1]
        preds[idx2] += clf.predict_proba(test3)[:,1] / skf.n_splits
    
#PRINT CV AUC
auc = roc_auc_score(train['target'], oof)
print(f'AUC: {auc:.5}')


# # The relationship between train data and test data.

# ## Histogram of the number of data. 
# Although the number of train data is 262144 = 512 * 512, the number of actual train data varies.

# In[ ]:


import matplotlib.pyplot as plt
plt.hist(train_set,bins=120)
plt.title('train_data')
plt.show()

plt.hist(test_set,bins=120)
plt.title('test_data')
plt.show()

plt.hist(total_set,bins=120)
plt.title('train + test')
plt.show()


# In[ ]:


pd_train = pd.DataFrame(train_set,columns={"train"})
pd_test = pd.DataFrame(test_set,columns={"test"})
pd_total = pd.DataFrame(total_set,columns={"total"})
pd_set = pd.concat([pd_train,pd_test,pd_total],axis=1)
pd_set.head()


# ## Scatter plot of training data and test data

# In[ ]:


pd_set.plot(kind="scatter",x="train",y="test")


# In[ ]:


pd_set.corr()


# # Conclusion

# There is a negative correlation between training data and test data.
# Therefore, I think that CV score is low in the part where the number of test data is small.
# There is little time left, but I'm thinking of doing the following.
# <br>Please comment if I said something off target.
# 1. Change the threshold according to the number of training data when giving pseudo labels
# 2. Change the threshold according to the number of training data when flipping training data labels
# 3. Focus and tune on the set with few training data

# In[ ]:


sub = pd.read_csv('../input/sample_submission.csv')
sub['target'] = preds
sub.to_csv('submission.csv',index=False)


# In[ ]:




