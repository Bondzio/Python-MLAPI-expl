#!/usr/bin/env python
# coding: utf-8

# >**Import the libraies**

# In[ ]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import warnings
warnings.filterwarnings('ignore')
from sklearn.metrics import make_scorer,mean_squared_error
from sklearn.model_selection import cross_val_score
import xgboost as xgb
from catboost import Pool, CatBoostRegressor
import random
random.seed(42)
import os
print(os.listdir("../input"))


# > **Pre-processing**

# 
# > Load the data

# In[ ]:



pot_energy=pd.read_csv('../input/potential_energy.csv')
mulliken_charges=pd.read_csv('../input/mulliken_charges.csv')
train_df=pd.read_csv('../input/train.csv')
scalar_coupling_cont=pd.read_csv('../input/scalar_coupling_contributions.csv')
test_df=pd.read_csv('../input/test.csv')
magnetic_shield_tensor=pd.read_csv('../input/magnetic_shielding_tensors.csv')
dipole_moment=pd.read_csv('../input/dipole_moments.csv')
structures=pd.read_csv('../input/structures.csv')


# 
# > Let's see the shapes of our datasets

# In[ ]:


print('Shape of potential energy dataset:',pot_energy.shape)
print('Shape of mulliken_charges dataset:',mulliken_charges.shape)
print('Shape of train dataset:',train_df.shape)
print('Shape of scalar coupling contributions dataset:',scalar_coupling_cont.shape)
print('Shape of test dataset:',test_df.shape)
print('Shape of magnetic shielding tensors dataset:',magnetic_shield_tensor.shape)
print('Shape of dipole moments dataset:',dipole_moment.shape)
print('Shape of structures dataset:',structures.shape)


# > Let's explore our datasetes

# In[ ]:


#data types in dataset
print('Data Types:\n',pot_energy.dtypes)
#Descriptive statistics
print('Descriptive statistics:\n',np.round(pot_energy.describe(),3))
#Top few rows of dataset
pot_energy.head(6)


# > molecule_name - Name of the molecule,  
# >potential_energy - Potential energy of the molecule

# In[ ]:


#data types in dataset
print('Data Types:\n',mulliken_charges.dtypes)
#Descriptive statistics
print('Descriptive statistics:\n',np.round(mulliken_charges.describe(),3))
#Top few rows of dataset
mulliken_charges.head(6)


# > atom_index - Index of the atom in molecule,  
# > mulliken_charge- Mulliken charge of the atom

# In[ ]:


#data types in dataset
print('Data Types:\n',train_df.dtypes)
#Descriptive statistics
print('Descriptive statistics:\n',np.round(train_df.describe(),3))
#Top few rows of dataset
train_df.head(6)


# > atom_index_1 - atom indices of the atom-pair creating coupling,  
# > type - scalar coupling type,  
# > scalar_coupling_constant- scalar coupling constant that we want to predict (target variable)

# In[ ]:


#data types in dataset
print('Data Types:\n',scalar_coupling_cont.dtypes)
#Descriptive statistics
print('Descriptive statistics:\n',np.round(scalar_coupling_cont.describe(),3))
#Top few rows of dataset
scalar_coupling_cont.head(6)


# > fc  - Fermi contact contribution,  
# > sc  - Spin-dipolar contribution,  
# > pso - Paramagnetic spin-orbit contribution,  
# > dso - Diemagnetic spin-orbit contribution

# In[ ]:


#data types in dataset
print('Data Types:\n',test_df.dtypes)
#Descriptive statistics
print('Descriptive statistics:\n',np.round(test_df.describe(),3))
#Top few rows of dataset
test_df.head(6)


# In[ ]:



#data types in dataset
print('Data Types:\n',magnetic_shield_tensor.dtypes)
#Descriptive statistics
print('Descriptive statistics:\n',np.round(magnetic_shield_tensor.describe(),3))
#Top few rows of dataset
magnetic_shield_tensor.head(6)


# > XX, YX, ZX, XY, YY, ZY, XZ, YZ, ZZ- Elements of tensor/ matrix

# > X, Y, Z - X, Y, & Z componets of dipole moments

# In[ ]:


#data types in dataset
print('Data Types:\n',structures.dtypes)
#Descriptive statistics
print('Descriptive statistics:\n',np.round(structures.describe(),3))
#Top few rows of dataset
structures.head(6)


# > x, y, & z - Cartesian co-oridnates of the atom

# In[ ]:


#Map the atom structure data into train & test datasets

def map_atom_data(df,atom_idx):
    df=pd.merge(df,structures,how='left',
               left_on=['molecule_name',f'atom_index_{atom_idx}'],
               right_on=['molecule_name','atom_index'])
    df=df.drop('atom_index',axis=1)
    df=df.rename(columns={'atom':f'atom_{atom_idx}',
                         'x':f'x_{atom_idx}',
                         'y':f'y_{atom_idx}',
                         'z':f'z_{atom_idx}'})
    return df
#train dataset
train_df=map_atom_data(train_df,0)
train_df=map_atom_data(train_df,1)
#test dataset
test_df=map_atom_data(test_df,0)
test_df=map_atom_data(test_df,1)


# In[ ]:


get_ipython().run_cell_magic('time', '', "#Engineer a single feature: distance vector between atoms\n# for train dataset\ntrain_m_0=train_df[['x_0','y_0','z_0']].values\ntrain_m_1=train_df[['x_1','y_1','z_1']].values\n#for test dataset\ntest_m_0=test_df[['x_0','y_0','z_0']].values\ntest_m_1=test_df[['x_0','y_0','z_0']].values\n\n#distance vector between atoms for train dataset\ntrain_df['dist_vector']=np.linalg.norm(train_m_0-train_m_1,axis=1)\ntrain_df['dist_X']=(train_df['x_0']-train_df['x_1'])**2\ntrain_df['dist_Y']=(train_df['y_0']-train_df['y_1'])**2\ntrain_df['dist_Z']=(train_df['z_0']-train_df['z_1'])**2\n\n#distance vector between atoms for test dataset\ntest_df['dist_vector']=np.linalg.norm(test_m_0-test_m_1,axis=1)\ntest_df['dist_X']=(test_df['x_0']-test_df['x_1'])**2\ntest_df['dist_Y']=(test_df['y_0']-test_df['y_1'])**2\ntest_df['dist_Z']=(test_df['z_0']-test_df['z_1'])**2")


# > > **References:-**     
# > 1. https://www.kaggle.com/abhishek/competition-metric,   
# > 2. https://www.kaggle.com/seriousran/just-speed-up-calculate-distance-from-benchmark,  
# > 3. https://www.kaggle.com/inversion/atomic-distance-benchmark,    
# > 4. https://www.kaggle.com/robikscube/exploring-molecular-properties-data

# > Now let's check our train & test dataset

# In[ ]:


#train_df['type_0']=train_df['type'].apply(lambda x:x)
#test_df['type_0']=test_df['type'].apply(lambda x : x)


# In[ ]:


train_df=train_df.drop(columns=['molecule_name'],axis=1)
display(train_df.head(6))


# In[ ]:


test_df=test_df.drop(columns=['molecule_name'],axis=1)
display(test_df.head(10))


# Attributes like **atom_0**, & **atom_1** requires type converson from **obejcet** to **categorical** for proper understanding

# In[ ]:


#Type casting

# for train data
#train_df['type_0']=train_df.type_0.astype('category')
train_df['type']=train_df.type.astype('category')
train_df['atom_0']=train_df.atom_0.astype('category')
train_df['atom_1']=train_df.atom_1.astype('category')

#for test data
#test_df['type_0']=test_df.type_0.astype('category')
test_df['type']=test_df.type.astype('category')
test_df['atom_0']=test_df.atom_0.astype('category')
test_df['atom_1']=test_df.atom_1.astype('category')


# > **Histograms for Data Visualization**

# In[ ]:


plt.hist(train_df['scalar_coupling_constant'])
plt.ylabel('No of times')
plt.xlabel('scalar copling constant')
plt.show()


# In[ ]:


plt.hist(train_df['dist_vector'])
plt.ylabel('No of times')
plt.xlabel('Distance vector')
plt.show()


# In[ ]:


plt.hist(train_df['dist_X'])
plt.ylabel('No of times')
plt.xlabel('X distance vector')
plt.show()


# In[ ]:


plt.hist(train_df['dist_Y'])
plt.ylabel('No of times')
plt.xlabel('Y distance vector')
plt.show()


# In[ ]:


plt.hist(train_df['dist_Z'])
plt.ylabel('No of times')
plt.xlabel('Z distance vector')
plt.show()


# >** Box plots to detect outliers**

# In[ ]:


train=train_df[['scalar_coupling_constant','dist_vector','dist_X','dist_Y','dist_Z']]
plt.figure(figsize=(20,16))
sn.boxplot(data=train)


# In[ ]:


test=test_df[['dist_vector','dist_X','dist_Y','dist_Z']]
plt.figure(figsize=(15,8))
sn.boxplot(data=test)


# > Replace & impute the outliers

# In[ ]:


#Dataframe for outliers
trainDf=pd.DataFrame(train,columns=['scalar_coupling_constant','dist_X','dist_Y','dist_Z'])
testDf=pd.DataFrame(test,columns=['dist_X','dist_Y','dist_Z'])
train_labels=['scalar_coupling_constant','dist_X','dist_Y','dist_Z']
test_labels=['dist_X','dist_Y','dist_Z']
for i in train_labels:
    # Divide the data into 75% quantile & 25% quantile                               
    q75,q25=np.percentile(trainDf.loc[:,i],[75,25]) 
    #Inter quantile range
    iqr=q75-q25
    #Inner fence
    min=q25-(iqr*1.5)
    #outer fence
    max=q75+(iqr*1.5)
    #Replace outliers with NA
    trainDf.loc[trainDf.loc[:,i]<min,:i]=np.NaN
    trainDf.loc[trainDf.loc[:,i]>max,:i]=np.NaN
        
        
for j in test_labels:
    # Divide the data into 75% quantile & 25% quantile                               
    q75,q25=np.percentile(testDf.loc[:,j],[75,25]) 
    #Inter quantile range
    iqr=q75-q25
    #Inner fence
    min=q25-(iqr*1.5)
    #outer fence
    max=q75+(iqr*1.5)
    #Replace outliers with NA
    testDf.loc[testDf.loc[:,j]<min,:j]=np.NaN
    testDf.loc[testDf.loc[:,j]>max,:j]=np.NaN
                                  


# In[ ]:


print(trainDf.isnull().sum())


# In[ ]:


print(testDf.isnull().sum())


# In[ ]:


#Imputing the outliers by mean imputation
#For train data
trainDf['scalar_coupling_constant']=trainDf['scalar_coupling_constant'].fillna(trainDf['scalar_coupling_constant'].mean())
trainDf['dist_X']=trainDf['dist_X'].fillna(trainDf['dist_X'].mean())
trainDf['dist_Y']=trainDf['dist_Y'].fillna(trainDf['dist_Y'].mean())
trainDf['dist_Z']=trainDf['dist_Z'].fillna(trainDf['dist_Z'].mean())
#For test data
testDf['dist_X']=testDf['dist_X'].fillna(testDf['dist_X'].mean())
testDf['dist_Y']=testDf['dist_Y'].fillna(testDf['dist_Y'].mean())
testDf['dist_Z']=testDf['dist_Z'].fillna(testDf['dist_Z'].mean())


# In[ ]:


print(trainDf.isnull().sum())


# In[ ]:


print(testDf.isnull().sum())


# > Replace the features in original dataset with imputed data

# In[ ]:


train_df=train_df.drop(columns=['scalar_coupling_constant','dist_X','dist_Y','dist_Z'],axis=1)
test_df=test_df.drop(columns=['dist_X','dist_Y','dist_Z'],axis=1)


# In[ ]:


#For tran dataset
train_df['scalar_coupling_constant']=trainDf['scalar_coupling_constant']
train_df['dist_X']=trainDf['dist_X']
train_df['dist_Y']=trainDf['dist_Y']
train_df['dist_Z']=trainDf['dist_Z']
#For test dataset
test_df['dist_X']=testDf['dist_X']
test_df['dist_Y']=testDf['dist_Y']
test_df['dist_Z']=testDf['dist_Z']


# > **Histogram plots after outliers imputation**

# In[ ]:


plt.hist(train_df['scalar_coupling_constant'])
plt.ylabel('No of times')
plt.xlabel('scalar coupling constant')
plt.show()


# In[ ]:


plt.hist(train_df['dist_vector'])
plt.ylabel('No of times')
plt.xlabel('distance vector')
plt.show()


# In[ ]:


plt.hist(train_df['dist_X'])
plt.ylabel('No of times')
plt.xlabel('X distance vector')
plt.show()


# In[ ]:


plt.hist(train_df['dist_Y'])
plt.ylabel('No of times')
plt.xlabel('Y distance vector')
plt.show()


# In[ ]:


plt.hist(train_df['dist_Z'])
plt.ylabel('No of times')
plt.xlabel('Z distance vector')
plt.show()


# **Feature selection**

# In[ ]:


#Threshold for removing correalated values
#threshold=0.95
#Absolute value correlation matrix
#corr_matrix=train_df.corr().abs()

#Gettng the upper traingle of correlations
#upper=corr_matrix.where(np.triu(np.ones(corr_matrix.shape),k=1).astype(np.bool))


# In[ ]:


#select columns with correlations above threshold
#to_drop=[column for column in upper.columns if any(upper[column]>threshold)]
#print('There are are %d columns to remove.'%(len(to_drop)))


# In[ ]:


#train_df=train_df.drop(columns=to_drop)
#test_df=test_df.drop(columns=to_drop)
#print('Training data shape',train_df.shape)
#print('Testing data shape',test_df.shape)


# In[ ]:


Attributes=['atom_index_0','atom_index_1','type','x_0','y_0','z_0','atom_0',
            'atom_1','x_1','y_1','z_1','dist_vector','dist_X','dist_Y','dist_Z']
#categorical attributes
cat_attributes=['type','atom_0','atom_1']
target_label=['scalar_coupling_constant']
# split the data into X_train,X_test,& y_target

X_train=train_df[Attributes]
X_test=test_df[Attributes]
y_target=train_df[target_label]
            


# In[ ]:




#Transform categorical variables
#X_train=pd.get_dummies(X_train,columns=cat_attributes)
#X_test=pd.get_dummies(X_test,columns=cat_attributes)


# In[ ]:


print(X_train.shape,X_test.shape)


# In[ ]:


display(y_target.shape)


# In[ ]:


#Enocode the categorigal variables
from sklearn.preprocessing import LabelEncoder
for f in ['type','atom_index_0','atom_index_1','atom_0','atom_1']:
    #if f in good_columns:
        lbl=LabelEncoder()
        lbl.fit(list(X_train[f].values)+list(X_test[f].values))
        X_train[f]=lbl.transform(list(X_train[f].values))
        X_test[f]=lbl.transform(list(X_test[f].values))


# > Let's look at our transformed data

# In[ ]:



X_train.head(6)


# In[ ]:


X_test.head(6)


# **Linear Regression model**

# In[ ]:



from sklearn import linear_model
#linear_reg=linear_model.LinearRegression()
#n_folds=3
#Cross validation
#lin_reg_score=cross_val_score(linear_reg,X_train,y_target,
                          #scoring=make_scorer(mean_squared_error),
                          #cv=n_folds)
#lin_score=sum(lin_reg_score)/n_folds
#print('rgf_score:',lin_score)


# In[ ]:


#lr_model=linear_reg.fit(X_train,y_target)
#score=np.round(lr_model.score(X_train,y_target),3)
#print('Accuracy of trained model:',score)
#model_coeff=np.round(lr_model.coef_,3)
#print('Model coefficients:',model_coeff)
#model_intercept=np.round(lr_model.intercept_,3)
#print('Model intercept value:',model_intercept)


# In[ ]:


#model prediction
#from sklearn.metrics import r2_score
#y_pred=lr_model.predict(X_test)
#SCC=pd.read_csv('../input/sample_submission.csv')
#SCC['scalar_coupling_constant']= y_pred
#SCC.to_csv('Linear_Regression_model.csv',index=False)


# > **Lasso Regression model**

# In[ ]:


#%%time
#from sklearn import linear_model
#lasso=linear_model.Lasso(alpha=0.001)
#n_folds=10
#Cross validation
#lasso_score=cross_val_score(lasso,X_train,y_target,
                          #scoring=make_scorer(mean_squared_error),
                          #cv=n_folds)
#lasso_score=sum(lasso_score)/n_folds
#print('lasso_score:',lasso_score)
#print(lasso)


# In[ ]:


#lasso_model=lasso.fit(X_train,y_target)
#score=np.round(lasso_model.score(X_train,y_target),3)
#print('Accuracy of trained model:',score)


# In[ ]:


#model prediction
#y_pred=lasso_model.predict(X_test)
#SCC=pd.read_csv('../input/sample_submission.csv')
#SCC['scalar_coupling_constant']= y_pred
#SCC.to_csv('Lasso_Regression_model.csv',index=False)
#y_pred


# In[ ]:


#from sklearn import linear_model
#linear_reg=linear_model.ElasticNet(alpha=0.008)
#ElasticNet_model=linear_reg.fit(X_train,y_target)
#score=np.round(ElasticNet_model.score(X_train,y_target),3)
#print('Accuracy of trained model:',score)


# In[ ]:


#model prediction
#y_pred=ElasticNet_model.predict(X_test)
#SCC=pd.read_csv('../input/sample_submission.csv')
#SCC['scalar_coupling_constant']= y_pred
#SCC.to_csv('ElasticNet_Regression_model.csv',index=False)
#y_pred


# 
# 
# **Light Gradient Boostng Machine**

# > Hyperopt for Hyperparameter tuning (Bayesian optimization)

# In[ ]:


#Define hyper space
#from hyperopt import fmin,hp,tpe,Trials,space_eval,STATUS_OK,STATUS_RUNNING
#hyper_space={'objective':'regression',
            # 'metric':'mape',
             #'boosting':'gbdt',
             #'n_estimators':hp.choice('n_estimators',[100,250,450,600,850,1000,2000,3000,4000,5000]),
            # 'max_depth':hp.choice('max_depth',[5,10,15,20,25,30,35]),
             #'num_leaves':hp.choice('num_leaves',[45,60,95,125,145,200]),
             #'subsample':hp.choice('subsample',[.1,.2,.3,.4,0.5,0.6,0.7,0.8,0.9,1]),
             #'colsample_bytree': hp.choice('colsample_bytree',[.1,.2,.3,.4,.5,0.6,0.7,0.8,0.9,1.0]),
             #'learning_rate': hp.choice('learning_rate',[0.1,0.2,0.3,0.35,0.4,0.5]),
             #'reg_lambda': hp.choice('reg_lambda',[.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]),
            # 'reg_alpha': hp.choice('reg_alpha',[.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]),
            # 'min_child_samples':hp.choice('min_child_samples',[3,6,8,12,15])
           # }


# In[ ]:


#Defining the metric to score our optimizer
#def metric(df,pred):
    #df['diff']=(df['scalar_coupling_constant']-pred).abs()
    #return np.log(df.groupby([['type']])['diff'].mean().map(lambda x:max(x,1e-9))).mean()


# In[ ]:


#Split the train data into train(70%) & valid dataset(30%)
from sklearn.model_selection import train_test_split
X_train,X_valid,y_train,y_valid=train_test_split(X_train,y_target,
                                               test_size=0.2, random_state=42)
print(X_train.shape,X_valid.shape)
print(y_train.shape,y_valid.shape)


# In[ ]:


#from lightgbm import LGBMRegressor
#import lightgbm as lgb
#Create a function for Hyper parameters optimization
#train_data=lgb.Dataset(X_train,label=y_train)
#valid_data=lgb.Dataset(X_valid,label=y_valid)
#def evaluate_metric(params):
    #lgbm_model=lgb.train(params,train_data,500,
                             # valid_sets=[train_data,valid_data],
                            # early_stopping_rounds=20,verbose_eval=500)
   # pred=lgbm_model.predict(X_valid)
   # score=metric(df_valid,pred)
   # print(score)
   # return {
        #'loss':score,
        #'status':STATUS_OK,
       # 'staus running':STATUS_RUNNING
    #}
    


# > **Initalzing the optimizer**

# In[ ]:


#from functools import partial
#Trial
#trials=Trials()
#set algorithm parameters
#algo=partial(tpe.suggest,n_startup_jobs=-1)
#set the no.of evaluations
#Max_evals=20
#Fit the Tree parzen estimator
#best_vals=fmin(evaluate_metric,space=hyper_space,verbose=1,
             # algo=algo,max_evals=Max_evals,trials=trials)


# In[ ]:


#print the best parameters
#best_params=space_eval(hyper_space,best_vals)
#print('Best Parameters from Hyperopt:\n'+str(best_params))


# In[ ]:


#params={'objective':'regression',
       # 'boosting':'dart',
        #'colsample_bytree':1.0,
        #'learning_rate':0.35,
        #'max_depth':30,
        #'metric':'mse',
        #'min_child_samples':120,
        #'n_estimators':5000,
        #'num_leaves':2000,
        #'reg_alpha':0.005,
       #}

#lgb_model=lgb.train(params,train_data,valid_sets=[train_data,valid_data],verbose_eval=100,
                 #  early_stopping_rounds=100)


# In[ ]:


#y_pred=lgb_model.predict(X_test)
#SCC=pd.read_csv('../input/sample_submission.csv')
#SCC['scalar_coupling_constant']= y_pred
#SCC.to_csv('LGBM_dart_model.csv',index=False)


# > **XGBOOST**

# In[ ]:


get_ipython().run_cell_magic('time', '', '#training dataset\nxg_train=xgb.DMatrix(data=X_train,label=y_train)\nxg_valid=xgb.DMatrix(data=X_valid,label=y_valid)\nxg_test=xgb.DMatrix(X_test)')


# In[ ]:


#Setting parameters
xgb_params={'booster':'gbtree',
            'eval_metric':'rmse',
            'eta':0.8,
            'gamma':100,
            'max_depth':50,
           }


# In[ ]:


get_ipython().run_cell_magic('time', '', "num_rounds=2000\nevallist=[(xg_train,'train'),(xg_valid,'eval')]\nxgb=xgb.train(xgb_params,xg_train,num_rounds,evallist,verbose_eval=100,early_stopping_rounds=500)")


# In[ ]:


get_ipython().run_cell_magic('time', '', "xgb_predict=xgb.predict(xg_test,ntree_limit=xgb.best_ntree_limit)\n\nSCC=pd.read_csv('../input/sample_submission.csv')\nSCC['scalar_coupling_constant']= xgb_predict\nSCC.to_csv('xgboost_model.csv',index=False)")


# In[ ]:





# **Regurized Greedy Forest (RGF) algorithm**

# In[ ]:


from rgf.sklearn import RGFRegressor,FastRGFRegressor
from sklearn.metrics import make_scorer,mean_squared_error
from sklearn.model_selection import cross_val_score


# In[ ]:


#%%time
#rgf=RGFRegressor(max_leaf=500,algorithm='RGF_Sib',test_interval=100,
               # loss='LS',verbose=False)
#n_folds=3
#rgf_scores = cross_val_score(rgf,
                             #X_train,
                            # y_target,
                             #scoring=make_scorer(mean_squared_error,greater_is_better=False),
                             #cv=n_folds)
#rgf_score=sum(rgf_scores)/n_folds
#print('rgf_score:',rgf_score)


# In[ ]:


#%%time
#Tran the model
#rgf_model=rgf.fit(X_train,y_target)


# In[ ]:


#%%time
#model prediction
#y_pred=rgf_model.predict(X_test)
#SCC=pd.read_csv('../input/sample_submission.csv')
#SCC['scalar_coupling_constant']= y_pred
#SCC.to_csv('RGF_model.csv',index=False)
#y_pred


# **Fast Regurized Greedy Forest (RGF) algorithm**

# In[ ]:


get_ipython().run_cell_magic('time', '', "#Frgf=FastRGFRegressor( opt_algorithm='rgf',\n                     #l2=2000.0,\n                     #min_child_weight=5.0,\n                     #sparse_max_features=80000,\n                    # sparse_min_occurences=5\n                     #)\n#Frgf=FastRGFRegressor(n_estimators=1000)\n#n_folds=3\n#Frgf_scores=cross_val_score(Frgf,X_train,y_target,\n                         # scoring=make_scorer(mean_squared_error),\n                          #cv=n_folds)\n#Frgf_score=sum(Frgf_scores)/n_folds\n#print('Frgf_score:',Frgf_score)\n#print(Frgf)")


# In[ ]:


#Train the model
#Frgf_model=Frgf.fit(X_train,y_target)


# In[ ]:


#model prediction
#y_pred=Frgf_model.predict(X_test)
#SCC=pd.read_csv('../input/sample_submission.csv')
#SCC['scalar_coupling_constant']= y_pred
#SCC.to_csv('FRGF_model.csv',index=False)
#y_pred

