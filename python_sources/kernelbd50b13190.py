#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing Libraries############

get_ipython().run_line_magic('reset', '-f')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost.sklearn import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
 
from sklearn.preprocessing import StandardScaler as ss
from sklearn.decomposition import PCA
#from sklearn.decomposition import PCA, KernelPCA
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score
from sklearn.metrics import auc, roc_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import auc, roc_curve
from sklearn.metrics import confusion_matrix

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from bayes_opt import BayesianOptimization

import matplotlib.pyplot as plt
from xgboost import plot_importance
import seaborn as sns


from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from bayes_opt import BayesianOptimization
from xgboost.sklearn import XGBClassifier
from sklearn.model_selection import cross_val_score
import eli5
from eli5.sklearn import PermutationImportance

import eli5
from eli5.sklearn import PermutationImportance

import time
import os
import gc
import random
from scipy.stats import uniform


# In[ ]:


#Reading data

os.chdir("../input")
os.listdir()

tr_f = "winequalityN.csv"

total_lines = 250000
num_lines = 0.99 * total_lines    # 99% of data

data = pd.read_csv(
         tr_f,
         header=0)

p = num_lines/total_lines  


# In[ ]:


#Any null values,then drop

data.dropna(axis=0, inplace=True)


# In[ ]:


data.isnull().any


# In[ ]:


#iii) Segregate dataset into predictors (X) and target (y)

X=data.iloc[: , 1 : 14]
X 
y = data.iloc[:, 0]
y


# In[ ]:


#iv) Map values in ' y ' (target) from 'M' and 'B' to 1 and 0

di= {'white':1,'red':0}
y =y.map(di)
y
           


# In[ ]:


#Explore data         
data.shape 


# In[ ]:


data.columns.values       


# In[ ]:


data.head(3)
data.describe()


# In[ ]:


# Store column names somewhere
#     for use in feature importance

colnames = X.columns.tolist()


# In[ ]:


#  Split dataset into train and validation parts
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.35,
                                                    shuffle = True
                                                    )
y_test


# In[ ]:


X_train.shape 


# In[ ]:


X_test.shape


# In[ ]:


y_train.shape 


# In[ ]:


y_test.shape


# In[ ]:


#create pipe Line

steps_xg = [('sts', ss() ),
            ('pca', PCA()),
            ('xg',  XGBClassifier(silent = False,
                                  n_jobs=2)        # Specify other parameters here
            )
            ]


# In[ ]:


#Instantiate Pipeline object
pipe_xg = Pipeline(steps_xg)


# In[ ]:


#Performance Tuning Parameters with models


# In[ ]:


###########Grid Search#######

#Specify xgboost parameter-range

parameters = {'xg__learning_rate':  [0.2, 0.5], 
              'xg__n_estimators':   [50, 100],
              'xg__max_depth':      [3,5],
              'pca__n_components' : [5,7]
              }                   


# In[ ]:


clf = GridSearchCV(pipe_xg,           
                   parameters,         
                   n_jobs = 2,         
                   cv =2 ,            
                   verbose =2,        
                   scoring = ['accuracy', 'roc_auc'], 
                   refit = 'roc_auc'  
                                      
                   )


# In[ ]:


data.isnull().sum()


# In[ ]:


start = time.time()
clf.fit(X_train, y_train)
end = time.time()
(end - start)/60


# In[ ]:


f"Best score: {clf.best_score_} "


# In[ ]:


f"Best parameter set {clf.best_params_}"


# In[ ]:


#Make predictions
y_pred = clf.predict(X_test)
y_pred


# In[ ]:


# 7.5 Accuracy
accuracy = accuracy_score(y_test, y_pred)
f"Accuracy: {accuracy * 100.0}"


# In[ ]:


#  Find feature importance of any BLACK Box model

perm = PermutationImportance(
                            clf,
                            random_state=1
                            )

#fit data & learn
#        Takes sometime

start = time.time()
perm.fit(X_test, y_test)
end = time.time()
(end - start)/60


# In[ ]:


eli5.show_weights(
                  perm,
                  feature_names = colnames      # X_test.columns.tolist()
                  )


# In[ ]:


fw = eli5.explain_weights_df(
                  perm,
                  feature_names = colnames      # X_test.columns.tolist()
                  )


# In[ ]:


fw


# In[ ]:


##################### EE. Randomized Search #################


# In[ ]:


parameters = {'xg__learning_rate':  uniform(0, 1),
              'xg__n_estimators':   range(50,100),
              'xg__max_depth':      range(3,5),
              'pca__n_components' : range(5,7)}


# In[ ]:


# Tune parameters using random search
#     Create the object first
rs = RandomizedSearchCV(pipe_xg,
                        param_distributions=parameters,
                        scoring= ['roc_auc', 'accuracy'],
                        n_iter=10,          # Max combination of
                                            # parameter to try. Default = 10
                        verbose = 3,
                        refit = 'roc_auc',
                        n_jobs = 2,          # Use parallel cpu threads
                        cv = 2               # No of folds.
                                             # So n_iter * cv combinations
                        )


# In[ ]:


# Run random search for 25 iterations. 21 minutes
start = time.time()
rs.fit(X_train, y_train)
end = time.time()
(end - start)/60


# In[ ]:


#  Evaluate
f"Best score: {rs.best_score_} "


# In[ ]:


f"Best parameter set: {rs.best_params_} "


# In[ ]:


#  Make predictions
y_pred = rs.predict(X_test)


# In[ ]:


#Accuracy

accuracy = accuracy_score(y_test, y_pred)
f"Accuracy: {accuracy * 100.0}"


# In[ ]:


######################### Bayes Optimization

parameter_bo = {
           'learning_rate':  (0, 1),            
           'n_estimators':   (60,120),         
           'max_depth':      (4,7),            
           'n_components' :  (5,7)
            }


# In[ ]:


def xg_eval(learning_rate,n_estimators, max_depth,n_components):
    #Make Pipeling for BO
    pipe_xg1 = make_pipeline (ss(),
                              PCA(n_components=int(round(n_components))),
                              XGBClassifier(
                                           silent = False,
                                           n_jobs=2,
                                           learning_rate=learning_rate,
                                           max_depth=int(round(max_depth)),
                                           n_estimators=int(round(n_estimators))
                                           )
                             )
    #Fitting into pipeline 
    cv_result = cross_val_score(estimator = pipe_xg1,
                                X= X_train,
                                y = y_train,
                                cv = 2,
                                n_jobs = 2,
                                scoring = 'f1'
                                ).mean()             # taking mean of all results

    return cv_result


# In[ ]:


bayesian_opt = BayesianOptimization(
                             xg_eval,     
                             parameter_bo   
                             )


# In[ ]:


start = time.time()


# In[ ]:


bayesian_opt.maximize(init_points=5,
               n_iter=15,        
               )


# In[ ]:


f"Best parameter set: {bayesian_opt.max} "


# In[ ]:


###############    Model Importance   #################

#Model with parameters of grid search
model_gs = XGBClassifier(
                    learning_rate = clf.best_params_['xg__learning_rate'],
                    max_depth = clf.best_params_['xg__max_depth'],
                    n_estimators=clf.best_params_['xg__max_depth']
                    )


# In[ ]:


# Model with parameters of random search
model_rs = XGBClassifier(
                    learning_rate = rs.best_params_['xg__learning_rate'],
                    max_depth = rs.best_params_['xg__max_depth'],
                    n_estimators=rs.best_params_['xg__max_depth']
                    )


# In[ ]:


# Model with parameters of random search
model_bo = XGBClassifier(
              
    learning_rate = bayesian_opt.max['params']['learning_rate'],
                    max_depth = int(bayesian_opt.max['params']['max_depth']),
                    n_estimators= int(bayesian_opt.max['params']['n_estimators'])
                    )


# In[ ]:


#  Modeling with both parameters
start = time.time()
model_gs.fit(X_train, y_train)
model_rs.fit(X_train, y_train)
model_bo.fit(X_train, y_train)
end = time.time()
(end - start)/60


# In[ ]:


#  Predictions with both models
y_pred_gs = model_gs.predict(X_test)
y_pred_rs = model_rs.predict(X_test)
y_pred_bo = model_bo.predict(X_test)


# In[ ]:


#  Accuracy from both models
accuracy_gs = accuracy_score(y_test, y_pred_gs)
accuracy_rs = accuracy_score(y_test, y_pred_rs)
accuracy_bo = accuracy_score(y_test, y_pred_bo)
print ("Grid Search Accuracy " ,accuracy_gs)
print ("Random Search Accuracy ", accuracy_rs)
print ("Bayes OPt Accuracy ", accuracy_bo)


# In[ ]:


# Get feature importances from both models
get_ipython().run_line_magic('matplotlib', 'qt5')
model_gs.feature_importances_
model_rs.feature_importances_
model_bo.feature_importances_
plot_importance(model_gs)
plot_importance(model_rs)
plt.show()


# In[ ]:


#Confusion Matrix
confusion_matrix(y_test,y_pred_gs)
confusion_matrix(y_test,y_pred_rs)
confusion_matrix(y_test,y_pred_bo)
tn,fp,fn,tp= confusion_matrix(y_test,y_pred_gs).flatten()
tn,fp,fn,tp= confusion_matrix(y_test,y_pred_rs).flatten()
tn,fp,fn,tp= confusion_matrix(y_test,y_pred_bo).flatten()


# In[ ]:


#precision and recall

p_gs,r_gs,f_gs,_ = precision_recall_fscore_support(y_test,y_pred_gs)
p_rs,r_rs,f_rs,_ = precision_recall_fscore_support(y_test,y_pred_rs)
p_rs,r_rs,f_rs,_ = precision_recall_fscore_support(y_test,y_pred_bo)


# In[ ]:


#Get probability values
y_pred_gs_prob = model_gs.predict_proba(X_test)
y_pred_rs_prob = model_rs.predict_proba(X_test)
y_pred_bo_prob = model_bo.predict_proba(X_test)


# In[ ]:


y_pred_gs_prob


# In[ ]:


tn,fp,fn,tp


# In[ ]:


fpr_gs, tpr_gs, thresholds = roc_curve(y_test,
                                 y_pred_gs_prob[: ,0],
                                 pos_label=0
                                 )


# In[ ]:


fpr_rs, tpr_rs, thresholds = roc_curve(y_test,
                                 y_pred_rs_prob[: ,0],
                                 pos_label= 0
                                 )


# In[ ]:


fpr_bo, tpr_bo, thresholds = roc_curve(y_test,
                                 y_pred_bo_prob[: ,0],
                                 pos_label= 0
                                 )


# In[ ]:


#  AUC  of Grid Search
auc(fpr_gs, tpr_gs)


# In[ ]:


#  AUC of Random Search
auc(fpr_rs, tpr_rs)


# In[ ]:


#  AUC of Bayes OPtimization
auc(fpr_bo, tpr_bo)


# In[ ]:


#Data Explore with few GRaphs
sns.countplot(x = data.quality, data=data, hue='type', palette="husl")


# In[ ]:




