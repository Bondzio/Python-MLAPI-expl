#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Basic packages
import pandas as pd
import numpy as np
import warnings
import time
import random
import glob
import sys
import os
import gc

# ML packages
from scipy.stats import spearmanr
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from IPython.display import display
import matplotlib.patches as patch
import matplotlib.pyplot as plt
from sklearn.svm import NuSVR
from scipy.stats import norm
import lightgbm as lgb
import eli5
from eli5.sklearn import PermutationImportance
from scipy.stats import kurtosis, skew

from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader

# visualization packages
import seaborn as sns
import matplotlib.pyplot as plt

# execution progress bar
from tqdm import tqdm_notebook, tnrange
from tqdm.auto import tqdm
tqdm.pandas()


# In[ ]:


# System Setup
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('precision', '4')
warnings.filterwarnings('ignore')
plt.style.use('ggplot')
np.set_printoptions(suppress=True)
pd.set_option("display.precision", 15)


# ## Load Data

# In[ ]:


print(os.listdir("../input/"))


# In[ ]:


# import Dataset to play with it
train= pd.read_csv("../input/train.csv")
test = pd.read_csv('../input/test.csv')
sample_submission = pd.read_csv('../input/sample_submission.csv')


# In[ ]:


train.shape, test.shape, sample_submission.shape


# In[ ]:


train.head(5)


# In[ ]:


#Temporary tiny sample df for code development
#random.seed(4444)
#train = train.sample(n=5000)
#train.shape


# ##   Data Exploration

# In[ ]:


train.columns


# In[ ]:


print(len(train.columns))


# In[ ]:


print(train.info())


# In[ ]:


train.describe()


# In[ ]:


# distribution of targets
colors = ['darkseagreen','lightcoral']
plt.figure(figsize=(6,6))
plt.pie(train["target"].value_counts(), explode=(0, 0.25), labels= ["0", "1"], startangle=45, autopct='%1.1f%%', colors=colors)
plt.axis('equal')
plt.show()


# In[ ]:


# correlation with target
labels = []
values = []

for col in train.columns:
    if col not in ['ID_code', 'target']:
        labels.append(col)
        values.append(spearmanr(train[col].values, train['target'].values)[0])

corr_df = pd.DataFrame({'col_labels': labels, 'corr_values' : values})
corr_df = corr_df.sort_values(by='corr_values')

corr_df = corr_df[(corr_df['corr_values']>0.03) | (corr_df['corr_values']<-0.03)]

ind = np.arange(corr_df.shape[0])
width = 0.9
fig, ax = plt.subplots(figsize=(12,12))
rects = ax.barh(ind, np.array(corr_df.corr_values.values), color='darkseagreen')
ax.set_yticks(ind)
ax.set_yticklabels(corr_df.col_labels.values, rotation='horizontal')
ax.set_xlabel("Correlation coefficient")
ax.set_title("Variable correlation to Target")
plt.show()


# In[ ]:


# check covariance among importance variables
cols_to_use = corr_df[(corr_df['corr_values']>0.05) | (corr_df['corr_values']<-0.05)].col_labels.tolist()

temp_df = train[cols_to_use]
corrmat = temp_df.corr(method='spearman')
f, ax = plt.subplots(figsize=(18, 18))

#Draw the heatmap using seaborn
sns.heatmap(corrmat, vmax=1., square=True, cmap="Blues", annot=True)
plt.title("Important variables correlation map", fontsize=15)
plt.show()


# ## Data Preprocessing

# In[ ]:


# Check missing data for test & train
def check_missing_data(df):
    flag=df.isna().sum().any()
    if flag==True:
        total = df.isnull().sum()
        percent = (df.isnull().sum())/(df.isnull().count()*100)
        output = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
        data_type = []
        # written by MJ Bahmani
        for col in df.columns:
            dtype = str(df[col].dtype)
            data_type.append(dtype)
        output['Types'] = data_type
        return(np.transpose(output))
    else:
        return(False)


# In[ ]:


print('missing in train: ',check_missing_data(train))
print('missing in test: ',check_missing_data(test))


# In[ ]:


train.head()


# ## Variable Engineering

# #### PCA

# In[ ]:


'''pca_df = preprocessing.normalize(train.drop(['ID_code','target'],axis=1))
pca_test_df = preprocessing.normalize(test.drop(['ID_code'],axis=1))

def _get_number_components(model, threshold):
    component_variance = model.explained_variance_ratio_
    explained_variance = 0.0
    components = 0

    for var in component_variance:
        explained_variance += var
        components += 1
        if(explained_variance >= threshold):
            break
    return components

### Get the optimal number of components
pca = PCA()
train_pca = pca.fit_transform(pca_df)
test_pca = pca.fit_transform(pca_test_df)
components = _get_number_components(pca, threshold=0.9)
components'''


# In[ ]:


# Implement PCA 
'''obj_pca = model = PCA(n_components = components)
X_pca = obj_pca.fit_transform(pca_df)
X_t_pca = obj_pca.fit_transform(pca_test_df)'''


# In[ ]:


# add the decomposed features in the train dataset
'''def _add_decomposition(df, decomp, ncomp, flag):
    for i in range(1, ncomp+1):
        df[flag+"_"+str(i)] = decomp[:, i - 1]'''


# In[ ]:


#pca_train = train[['ID_code','target']]
#pca_test = test[['ID_code']]

'''_add_decomposition(train, X_pca, 90, 'pca')
_add_decomposition(test, X_t_pca, 90, 'pca')'''


# #### Summary Stats

# In[ ]:


idx = features = train.columns.values[2:202]
for df in [train, test]:
    df['sum'] = df[idx].sum(axis=1)  
    df['min'] = df[idx].min(axis=1)
    df['max'] = df[idx].max(axis=1)
    df['mean'] = df[idx].mean(axis=1)
    df['std'] = df[idx].std(axis=1)
    df['skew'] = df[idx].skew(axis=1)
    df['kurt'] = df[idx].kurtosis(axis=1)
    df['med'] = df[idx].median(axis=1)


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


train.shape


# ## Feature importance

# In[ ]:


cols=["target","ID_code"]
X = train.drop(cols,axis=1)
y = train["target"]
test_ID = test["ID_code"]
#cols=["target","ID_code"]
#X = pca_train.drop(cols,axis=1)
#y = pca_train["target"]


# In[ ]:


X_test  = test.drop("ID_code",axis=1)
#X_test  = pca_test.drop("ID_code",axis=1)


# In[ ]:


train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)


# In[ ]:


# rfc_model = RandomForestClassifier(random_state=0).fit(train_X, train_y)


# ### Permutation Importance

# In[ ]:


'''perm = PermutationImportance(rfc_model, random_state=1).fit(val_X, val_y)
eli5.show_weights(perm, feature_names = val_X.columns.tolist())'''


# In[ ]:


# features = [c for c in train.columns if c not in ['ID_code', 'target']]


#  ## Model Development

# ### lightgbm

# In[ ]:


# for get better result chage fold_n to 5
fold_n=5
folds = StratifiedKFold(n_splits=fold_n, shuffle=True, random_state=10)


# In[ ]:


params = {
        'bagging_freq': 5,
        'bagging_fraction': 0.4,
        'boost_from_average':'false',
        'boost': 'gbdt',
        'feature_fraction': 0.05,
        'learning_rate': 0.01,
        'max_depth': -1,
        'metric':'auc',
        'min_data_in_leaf': 80,
        'min_sum_hessian_in_leaf': 10.0,
        'num_leaves': 13,
        'num_threads': 8,
        'tree_learner': 'serial',
        'objective': 'binary', 
        'verbosity': -1,
        #'is_unbalance': True,
        'reg_alpha': 0.1,
        'reg_lambda': 8
}


# In[ ]:


get_ipython().run_cell_magic('time', '', "y_pred_lgb = np.zeros(len(X_test))\nfor fold_n, (train_index, valid_index) in enumerate(folds.split(X,y)):\n    print('Fold', fold_n, 'started at', time.ctime())\n    X_train, X_valid = X.iloc[train_index], X.iloc[valid_index]\n    y_train, y_valid = y.iloc[train_index], y.iloc[valid_index]\n    \n    train_data = lgb.Dataset(X_train, label=y_train)\n    valid_data = lgb.Dataset(X_valid, label=y_valid)\n        \n    lgb_model = lgb.train(params,train_data,num_boost_round=100000,\n                    valid_sets = [train_data, valid_data],verbose_eval=1000,early_stopping_rounds = 3000)\n            \n    y_pred_lgb += lgb_model.predict(X_test, num_iteration=lgb_model.best_iteration)/5")


# In[ ]:





# In[ ]:


train_preds_lgb = np.zeros(len(X))
train_preds_lgb = lgb_model.predict(X, num_iteration=lgb_model.best_iteration)/5
auc_lgb  = round(roc_auc_score(train['target'], train_preds_lgb), 4) 


# ### Neural Net

# In[ ]:


train_features = train.drop(['target','ID_code'], axis = 1)
test_features = test.drop(['ID_code'],axis = 1)
train_target = train['target']

sc = StandardScaler()
train_features = sc.fit_transform(train_features)
test_features = sc.transform(test_features)

n_splits = 5 # Number of K-fold Splits
splits = list(StratifiedKFold(n_splits=n_splits, shuffle=True).split(train_features, train_target))


# In[ ]:


class CyclicLR(object):
    def __init__(self, optimizer, base_lr=1e-3, max_lr=6e-3,
                 step_size=2000, mode='triangular', gamma=1.,
                 scale_fn=None, scale_mode='cycle', last_batch_iteration=-1):

        if not isinstance(optimizer, Optimizer):
            raise TypeError('{} is not an Optimizer'.format(
                type(optimizer).__name__))
        self.optimizer = optimizer

        if isinstance(base_lr, list) or isinstance(base_lr, tuple):
            if len(base_lr) != len(optimizer.param_groups):
                raise ValueError("expected {} base_lr, got {}".format(
                    len(optimizer.param_groups), len(base_lr)))
            self.base_lrs = list(base_lr)
        else:
            self.base_lrs = [base_lr] * len(optimizer.param_groups)

        if isinstance(max_lr, list) or isinstance(max_lr, tuple):
            if len(max_lr) != len(optimizer.param_groups):
                raise ValueError("expected {} max_lr, got {}".format(
                    len(optimizer.param_groups), len(max_lr)))
            self.max_lrs = list(max_lr)
        else:
            self.max_lrs = [max_lr] * len(optimizer.param_groups)

        self.step_size = step_size

        if mode not in ['triangular', 'triangular2', 'exp_range']                 and scale_fn is None:
            raise ValueError('mode is invalid and scale_fn is None')

        self.mode = mode
        self.gamma = gamma

        if scale_fn is None:
            if self.mode == 'triangular':
                self.scale_fn = self._triangular_scale_fn
                self.scale_mode = 'cycle'
            elif self.mode == 'triangular2':
                self.scale_fn = self._triangular2_scale_fn
                self.scale_mode = 'cycle'
            elif self.mode == 'exp_range':
                self.scale_fn = self._exp_range_scale_fn
                self.scale_mode = 'iterations'
        else:
            self.scale_fn = scale_fn
            self.scale_mode = scale_mode

        self.batch_step(last_batch_iteration + 1)
        self.last_batch_iteration = last_batch_iteration

    def batch_step(self, batch_iteration=None):
        if batch_iteration is None:
            batch_iteration = self.last_batch_iteration + 1
        self.last_batch_iteration = batch_iteration
        for param_group, lr in zip(self.optimizer.param_groups, self.get_lr()):
            param_group['lr'] = lr

    def _triangular_scale_fn(self, x):
        return 1.

    def _triangular2_scale_fn(self, x):
        return 1 / (2. ** (x - 1))

    def _exp_range_scale_fn(self, x):
        return self.gamma**(x)

    def get_lr(self):
        step_size = float(self.step_size)
        cycle = np.floor(1 + self.last_batch_iteration / (2 * step_size))
        x = np.abs(self.last_batch_iteration / step_size - 2 * cycle + 1)

        lrs = []
        param_lrs = zip(self.optimizer.param_groups, self.base_lrs, self.max_lrs)
        for param_group, base_lr, max_lr in param_lrs:
            base_height = (max_lr - base_lr) * np.maximum(0, (1 - x))
            if self.scale_mode == 'cycle':
                lr = base_lr + base_height * self.scale_fn(cycle)
            else:
                lr = base_lr + base_height * self.scale_fn(self.last_batch_iteration)
            lrs.append(lr)
        return lrs


# In[ ]:


class Simple_NN(nn.Module):
    def __init__(self ,input_dim ,hidden_dim, dropout = 0.1):
        super(Simple_NN, self).__init__()
        
        self.inpt_dim = input_dim
        self.hidden_dim = hidden_dim
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, int(hidden_dim/2))
        self.fc3 = nn.Linear(int(hidden_dim/2), int(hidden_dim/4))
        self.fc4 = nn.Linear(int(hidden_dim/4), int(hidden_dim/8))
        self.fc5 = nn.Linear(int(hidden_dim/8), 1)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.bn2 = nn.BatchNorm1d(int(hidden_dim/2))
        self.bn3 = nn.BatchNorm1d(int(hidden_dim/4))
        self.bn4 = nn.BatchNorm1d(int(hidden_dim/8))
    
    def forward(self, x):
        y = self.fc1(x)
        y = self.relu(y)
        #y = self.bn1(y)
        y = self.dropout(y)
        
        y = self.fc2(y)
        y = self.relu(y)
        #y = self.bn2(y)
        y = self.dropout(y)
        
        y = self.fc3(y)
        y = self.relu(y)
        #y = self.bn3(y)
        y = self.dropout(y)
        
        y = self.fc4(y)
        y = self.relu(y)
        #y = self.bn4(y)
        y = self.dropout(y)
        
        out= self.fc5(y)
        
        return out


# In[ ]:


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# In[ ]:


model = Simple_NN(208,512)
model.cuda()
optimizer = torch.optim.Adam(model.parameters(), lr = 0.0002) # Using Adam optimizer


# In[ ]:


from torch.optim.optimizer import Optimizer
n_epochs = 40
batch_size = 512

train_preds = np.zeros((len(train_features)))
test_preds = np.zeros((len(test_features)))

x_test = np.array(test_features)
x_test_cuda = torch.tensor(x_test, dtype=torch.float).cuda()
test = torch.utils.data.TensorDataset(x_test_cuda)
test_loader = torch.utils.data.DataLoader(test, batch_size=batch_size, shuffle=False)

avg_losses_f = []
avg_val_losses_f = []

for i, (train_idx, valid_idx) in enumerate(splits):  
    x_train = np.array(train_features)
    y_train = np.array(train_target)
    
    x_train_fold = torch.tensor(x_train[train_idx.astype(int)], dtype=torch.float).cuda()
    y_train_fold = torch.tensor(y_train[train_idx.astype(int), np.newaxis], dtype=torch.float32).cuda()
    
    x_val_fold = torch.tensor(x_train[valid_idx.astype(int)], dtype=torch.float).cuda()
    y_val_fold = torch.tensor(y_train[valid_idx.astype(int), np.newaxis], dtype=torch.float32).cuda()
    
    loss_fn = torch.nn.BCEWithLogitsLoss()
    
    step_size = 2000
    base_lr, max_lr = 0.0001, 0.005  
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), 
                             lr=max_lr)
    
    ################################################################################################
    scheduler = CyclicLR(optimizer, base_lr=base_lr, max_lr=max_lr,
               step_size=step_size, mode='exp_range',
               gamma=0.99994)
    ###############################################################################################

    train = torch.utils.data.TensorDataset(x_train_fold, y_train_fold)
    valid = torch.utils.data.TensorDataset(x_val_fold, y_val_fold)
    
    train_loader = torch.utils.data.DataLoader(train, batch_size=batch_size, shuffle=True)
    valid_loader = torch.utils.data.DataLoader(valid, batch_size=batch_size, shuffle=False)
    
    print(f'Fold {i + 1}')
    for epoch in range(n_epochs):
        start_time = time.time()
        model.train()
        avg_loss = 0.
        #avg_auc = 0.
        for i, (x_batch, y_batch) in enumerate(train_loader):
            y_pred = model(x_batch)
            #########################
            if scheduler:
                #print('cycle_LR')
                scheduler.batch_step()
            ########################
            loss = loss_fn(y_pred, y_batch)

            optimizer.zero_grad()
            loss.backward()

            optimizer.step()
            avg_loss += loss.item()/len(train_loader)
            #avg_auc += round(roc_auc_score(y_batch.cpu(),y_pred.detach().cpu()),4) / len(train_loader)
        model.eval()
        
        valid_preds_fold = np.zeros((x_val_fold.size(0)))
        test_preds_fold = np.zeros((len(test_features)))
        
        avg_val_loss = 0.
        #avg_val_auc = 0.
        for i, (x_batch, y_batch) in enumerate(valid_loader):
            y_pred = model(x_batch).detach()
            
            #avg_val_auc += round(roc_auc_score(y_batch.cpu(),sigmoid(y_pred.cpu().numpy())[:, 0]),4) / len(valid_loader)
            avg_val_loss += loss_fn(y_pred, y_batch).item() / len(valid_loader)
            valid_preds_fold[i * batch_size:(i+1) * batch_size] = sigmoid(y_pred.cpu().numpy())[:, 0]
            
        elapsed_time = time.time() - start_time 
        print('Epoch {}/{} \t loss={:.4f} \t val_loss={:.4f} \t time={:.2f}s'.format(
            epoch + 1, n_epochs, avg_loss, avg_val_loss, elapsed_time))
        
    avg_losses_f.append(avg_loss)
    avg_val_losses_f.append(avg_val_loss) 
    
    for i, (x_batch,) in enumerate(test_loader):
        y_pred = model(x_batch).detach()

        test_preds_fold[i * batch_size:(i+1) * batch_size] = sigmoid(y_pred.cpu().numpy())[:, 0]
        
    train_preds[valid_idx] = valid_preds_fold
    test_preds += test_preds_fold / len(splits)

auc_nn  =  round(roc_auc_score(train_target,train_preds),4)      
print('All \t loss={:.4f} \t val_loss={:.4f} \t auc={:.4f}'.format(np.average(avg_losses_f),np.average(avg_val_losses_f),auc_nn))


# In[ ]:


ensemble = 0.5*train_preds_lgb + 0.5* train_preds
ensemble_test = 0.5* y_pred_lgb + 0.5* test_preds


# In[ ]:


print('LightBGM auc = {:<8.5f}'.format(auc_lgb))
print('NN auc = {:<8.5f}'.format(auc_nn))
print('NN+LightBGM auc = {:<8.5f}'.format(roc_auc_score(train_target, ensemble)))


# ## Submission Files

# In[ ]:


submission_lgb = pd.DataFrame({
        "ID_code": test_ID,
        "target": y_pred_lgb
    })
submission_lgb.to_csv('submission_lgb.csv', index=False)


# In[ ]:


submission_nn = pd.DataFrame({
        "ID_code": test_ID,
        "target": test_preds
    })
submission_nn.to_csv('submission_nn.csv', index=False)


# In[ ]:


submission_ens = pd.DataFrame({
        "ID_code": test_ID,
        "target": ensemble_test
    })
submission_ens.to_csv('submission_ens.csv', index=False)


#  <a id="55"></a> <br>
# ## Stacking

# In[ ]:


'''submission_rfc_cat = pd.DataFrame({
        "ID_code": test["ID_code"],
        "target": (y_pred_rfc +y_pred_cat)/2
    })
submission_rfc_cat.to_csv('submission_rfc_cat.csv', index=False)'''


# # References & credits
# Thanks fo following kernels that help me to create this kernel.

# 1. [https://www.kaggle.com/mjbahmani/santander-ml-explainability](https://www.kaggle.com/mjbahmani/santander-ml-explainability)  
# 1. [https://www.kaggle.com/super13579/pytorch-nn-cyclelr-k-fold-0-897-lightgbm-0-899](https://www.kaggle.com/super13579/pytorch-nn-cyclelr-k-fold-0-897-lightgbm-0-899)  
# 1. [https://www.kaggle.com/dansbecker/permutation-importance](https://www.kaggle.com/dansbecker/permutation-importance)
# 1. [https://www.kaggle.com/dansbecker/partial-plots](https://www.kaggle.com/dansbecker/partial-plots)
# 1. [https://www.kaggle.com/miklgr500/catboost-with-gridsearch-cv](https://www.kaggle.com/miklgr500/catboost-with-gridsearch-cv)
# 1. [https://www.kaggle.com/dromosys/sctp-working-lgb](https://www.kaggle.com/dromosys/sctp-working-lgb)
# 1. [https://www.kaggle.com/gpreda/santander-eda-and-prediction](https://www.kaggle.com/gpreda/santander-eda-and-prediction)
# 1. [permutation-importance](https://www.kaggle.com/dansbecker/permutation-importance)
# 1. [partial-plots](https://www.kaggle.com/dansbecker/partial-plots)
# 1. [https://www.kaggle.com/dansbecker/shap-values](https://www.kaggle.com/dansbecker/shap-values)
# 1. [algorithm-choice](https://docs.microsoft.com/en-us/azure/machine-learning/studio/algorithm-choice)

# # Not Completed yet!!!
