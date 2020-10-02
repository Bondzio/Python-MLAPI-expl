#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
plt.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn import metrics

from sklearn import model_selection

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB


# In[2]:


import os
print(os.listdir("../input"))


# In[3]:


df_train=pd.read_csv('../input/train.csv')
df_train.head()


# In[4]:


df_test=pd.read_csv('../input/test.csv')
print(df_test.shape)
df_test.head()


# In[5]:


df_test.label_bnc.sum()


# In[6]:


# original features
features_orig = ['setting1','setting2','setting3','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14','s15','s16','s17','s18','s19','s20','s21']

# original + extracted fetures
features_extr =[u'setting1', u'setting2', u'setting3', u's1', u's2',
       u's3', u's4', u's5', u's6', u's7', u's8', u's9', u's10', u's11', u's12',
       u's13', u's14', u's15', u's16', u's17', u's18', u's19', u's20', u's21',
       u's1_av', u's1_std', u's2_av',
       u's2_std', u's3_av', u's3_std', u's4_av', u's4_std', u's5_av',
       u's5_std', u's6_av', u's6_std', u's7_av', u's7_std', u's8_av',
       u's8_std', u's9_av', u's9_std', u's10_av', u's10_std', u's11_av',
       u's11_std', u's12_av', u's12_std', u's13_av', u's13_std', u's14_av',
       u's14_std', u's15_av', u's15_std', u's16_av', u's16_std', u's17_av',
       u's17_std', u's18_av', u's18_std', u's19_av', u's19_std', u's20_av',
       u's20_std', u's21_av', u's21_std']

imp_features=['s9_av', 's8_av', 's3_av', 's17_av', 's11_av', 's7_av', 's15_av', 's20_av', 's21_av', 's2_av']

y_train = df_train['label_bnc']
y_test = df_test['label_bnc']


# In[7]:


y_train.sum()


# ## parameter tunning

# In[8]:


def bin_classify(model, clf, features, params=None, score=None):
    
    """Perfor Grid Search hyper parameter tuning on a classifier.
    
    Args:
        model (str): The model name identifier
        clf (clssifier object): The classifier to be tuned
        features (list): The set of input features names
        params (dict): Grid Search parameters
        score (str): Grid Search score
        
    Returns:
        Tuned Clssifier object
        dataframe of model predictions and scores
    
    """
    
    
    X_train = df_train[features]

    X_test = df_test[features] 
    
    grid_search = model_selection.GridSearchCV(estimator=clf, param_grid=params, cv=5, scoring=score, n_jobs=-1)

    grid_search.fit(X_train, y_train)
    y_pred = grid_search.predict(X_test)
    
    if hasattr(grid_search, 'predict_proba'):   
        y_score = grid_search.predict_proba(X_test)[:,1]
    elif hasattr(grid_search, 'decision_function'):
        y_score = grid_search.decision_function(X_test)
    else:
        y_score = y_pred
        
    predictions = {'y_pred' : y_pred, 'y_score' : y_score}
    df_predictions = pd.DataFrame.from_dict(predictions)
    
    return grid_search.best_estimator_, df_predictions


# In[9]:


def bin_class_metrics(model, y_test, y_pred, y_score, print_out=True):
    
    """Calculate main binary classifcation metrics, plot AUC ROC and Precision-Recall curves.
    
    Args:
        model (str): The model name identifier
        y_test (series): Contains the test label values
        y_pred (series): Contains the predicted values
        y_score (series): Contains the predicted scores
        print_out (bool): Print the classification metrics and thresholds values
        plot_out (bool): Plot AUC ROC, Precision-Recall, and Threshold curves
        
    Returns:
        dataframe: The combined metrics in single dataframe
        dataframe: ROC thresholds
        dataframe: Precision-Recall thresholds
        Plot: AUC ROC
        plot: Precision-Recall
        plot: Precision-Recall threshold; also show the number of engines predicted for maintenace per period (queue).
        plot: TPR-FPR threshold
        
    """
      
    binclass_metrics = {
                        'Accuracy' : metrics.accuracy_score(y_test, y_pred),
                        'Precision' : metrics.precision_score(y_test, y_pred),
                        'Recall' : metrics.recall_score(y_test, y_pred),
                        'F1 Score' : metrics.f1_score(y_test, y_pred),
                        'ROC AUC' : metrics.roc_auc_score(y_test, y_score)
                       }

    df_metrics = pd.DataFrame.from_dict(binclass_metrics, orient='index')
    df_metrics.columns = [model]  

    if print_out:
        print('-----------------------------------------------------------')
        print(model, '\n')
        print('Confusion Matrix:')
        print(metrics.confusion_matrix(y_test, y_pred))
        print('\nClassification Report:')
        print(metrics.classification_report(y_test, y_pred))
        print('\nMetrics:')
        print(df_metrics)

    return  df_metrics


# **A** after feature extraction features=features_extr<br>
# **B** original features features=features_orig<br>
# **I** important features=imp_features

# In[10]:



model = 'Logistic Regression B'
clf_lgrb = LogisticRegression(random_state=123)
gs_params = {'C': [.01, 0.1, 1.0, 10], 'solver': ['liblinear', 'lbfgs']}
gs_score = 'roc_auc'

clf_lgrb, pred_lgrb = bin_classify(model, clf_lgrb, features_orig, params=gs_params, score=gs_score)
print('\nBest Parameters:\n',clf_lgrb)

metrics_lgrb= bin_class_metrics(model, y_test, pred_lgrb.y_pred, pred_lgrb.y_score, print_out=True)


# In[11]:


get_ipython().run_cell_magic('time', '', "model = 'Logistic Regression A'\nclf_lgrb = LogisticRegression(random_state=123)\ngs_params = {'C': [.01, 0.1, 1.0, 10], 'solver': ['liblinear', 'lbfgs']}\ngs_score = 'roc_auc'\n\nclf_lgrb, pred_lgrb = bin_classify(model, clf_lgrb, features_extr, params=gs_params, score=gs_score)\nprint ('\\nBest Parameters:\\n',clf_lgrb)\n\nmetrics_lgra= bin_class_metrics(model, y_test, pred_lgrb.y_pred, pred_lgrb.y_score, print_out=True)")


# In[12]:


get_ipython().run_cell_magic('time', '', "model = 'Logistic Regression I'\nclf_lgrb = LogisticRegression(random_state=123)\ngs_params = {'C': [.01, 0.1, 1.0, 10], 'solver': ['liblinear', 'lbfgs']}\ngs_score = 'roc_auc'\n\nclf_lgrb, pred_lgrb = bin_classify(model, clf_lgrb, imp_features, params=gs_params, score=gs_score)\nprint ('\\nBest Parameters:\\n',clf_lgrb)\n\nmetrics_lgri= bin_class_metrics(model, y_test, pred_lgrb.y_pred, pred_lgrb.y_score, print_out=True)")


# In[13]:


metrics_lgr = pd.concat([metrics_lgrb, metrics_lgra,metrics_lgri], axis=1)
metrics_lgr


# In[31]:


get_ipython().run_cell_magic('time', '', "model = 'Decision Tree B'\nclf_dtrb = DecisionTreeClassifier(random_state=123)\ngs_params = {'max_depth': [2, 3, 4, 5, 6], 'criterion': ['gini', 'entropy']}\ngs_score = 'roc_auc'\n\nclf_dtrb, pred_dtrb = bin_classify(model, clf_dtrb, features_orig, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_dtrb)\n\nmetrics_dtrb= bin_class_metrics(model, y_test, pred_dtrb.y_pred, pred_dtrb.y_score, print_out=True)")


# In[32]:


get_ipython().run_cell_magic('time', '', "model = 'Decision Tree A'\nclf_dtrb = DecisionTreeClassifier(random_state=123)\ngs_params = {'max_depth': [2, 3, 4, 5, 6], 'criterion': ['gini', 'entropy']}\ngs_score = 'roc_auc'\n\nclf_dtrb, pred_dtrb = bin_classify(model, clf_dtrb, features_extr, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_dtrb)\n\nmetrics_dtra= bin_class_metrics(model, y_test, pred_dtrb.y_pred, pred_dtrb.y_score, print_out=True)")


# In[33]:


get_ipython().run_cell_magic('time', '', "model = 'Decision Tree I'\nclf_dtrb = DecisionTreeClassifier(random_state=123)\ngs_params = {'max_depth': [2, 3, 4, 5, 6], 'criterion': ['gini', 'entropy']}\ngs_score = 'roc_auc'\n\nclf_dtrb, pred_dtrb = bin_classify(model, clf_dtrb, imp_features, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_dtrb)\n\nmetrics_dtri= bin_class_metrics(model, y_test, pred_dtrb.y_pred, pred_dtrb.y_score, print_out=True)")


# In[17]:


metrics_dtr = pd.concat([metrics_dtrb, metrics_dtra,metrics_dtri], axis=1)
metrics_dtr


# In[18]:


get_ipython().run_cell_magic('time', '', "model = 'Random Forest B'\nclf_rfcb = RandomForestClassifier(n_estimators=50, random_state=123)\ngs_params = {'max_depth': [4, 5, 6, 7, 8], 'criterion': ['gini', 'entropy']}\ngs_score = 'roc_auc'\n\nclf_rfcb, pred_rfcb = bin_classify(model, clf_rfcb, features_orig, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_rfcb)\n\nmetrics_rfcb= bin_class_metrics(model, y_test, pred_rfcb.y_pred, pred_rfcb.y_score, print_out=True)")


# In[34]:


get_ipython().run_cell_magic('time', '', "model = 'Random Forest A'\nclf_rfcb = RandomForestClassifier(n_estimators=50, random_state=123)\ngs_params = {'max_depth': [4, 5, 6, 7, 8], 'criterion': ['gini', 'entropy']}\ngs_score = 'roc_auc'\n\nclf_rfcb, pred_rfcb = bin_classify(model, clf_rfcb, features_extr, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_rfcb)\n\nmetrics_rfca= bin_class_metrics(model, y_test, pred_rfcb.y_pred, pred_rfcb.y_score, print_out=True)")


# In[20]:


get_ipython().run_cell_magic('time', '', "model = 'Random Forest I'\nclf_rfcb = RandomForestClassifier(n_estimators=50, random_state=123)\ngs_params = {'max_depth': [4, 5, 6, 7, 8], 'criterion': ['gini', 'entropy']}\ngs_score = 'roc_auc'\n\nclf_rfcb, pred_rfcb = bin_classify(model, clf_rfcb, imp_features, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_rfcb)\n\nmetrics_rfci= bin_class_metrics(model, y_test, pred_rfcb.y_pred, pred_rfcb.y_score, print_out=True)")


# In[21]:


metrics_rfc = pd.concat([metrics_rfcb, metrics_rfca,metrics_rfci], axis=1)
metrics_rfc


# In[35]:


get_ipython().run_cell_magic('time', '', "model = 'KNN B'\nclf_knnb = KNeighborsClassifier(n_jobs=-1)\ngs_params = {'n_neighbors': [9, 10, 11, 12, 13]}\ngs_score = 'roc_auc'\n\nclf_knnb, pred_knnb = bin_classify(model, clf_knnb, features_orig, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_knnb)\n\nmetrics_knnb= bin_class_metrics(model, y_test, pred_knnb.y_pred, pred_knnb.y_score, print_out=True)")


# In[36]:


get_ipython().run_cell_magic('time', '', "model = 'KNN A'\nclf_knnb = KNeighborsClassifier(n_jobs=-1)\ngs_params = {'n_neighbors': [9, 10, 11, 12, 13]}\ngs_score = 'roc_auc'\n\nclf_knnb, pred_knnb = bin_classify(model, clf_knnb, features_extr, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_knnb)\n\nmetrics_knna= bin_class_metrics(model, y_test, pred_knnb.y_pred, pred_knnb.y_score, print_out=True)")


# In[24]:


get_ipython().run_cell_magic('time', '', "model = 'KNN I'\nclf_knnb = KNeighborsClassifier(n_jobs=-1)\ngs_params = {'n_neighbors': [9, 10, 11, 12, 13]}\ngs_score = 'roc_auc'\n\nclf_knnb, pred_knnb = bin_classify(model, clf_knnb, imp_features, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_knnb)\n\nmetrics_knni= bin_class_metrics(model, y_test, pred_knnb.y_pred, pred_knnb.y_score, print_out=True)")


# In[25]:


metrics_knn = pd.concat([metrics_knnb, metrics_knna,metrics_knni], axis=1)
metrics_knn


# In[26]:


get_ipython().run_cell_magic('time', '', "model = 'Gaussian NB B'\nclf_gnbb = GaussianNB()\ngs_params = {} \ngs_score = 'roc_auc'\n\nclf_gnbb, pred_gnbb = bin_classify(model, clf_gnbb, features_orig, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_gnbb)\n\nmetrics_gnbb= bin_class_metrics(model, y_test, pred_gnbb.y_pred, pred_gnbb.y_score, print_out=True)")


# In[27]:


get_ipython().run_cell_magic('time', '', "model = 'Gaussian NB A'\nclf_gnbb = GaussianNB()\ngs_params = {} \ngs_score = 'roc_auc'\n\nclf_gnbb, pred_gnbb = bin_classify(model, clf_gnbb, features_extr, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_gnbb)\n\nmetrics_gnba= bin_class_metrics(model, y_test, pred_gnbb.y_pred, pred_gnbb.y_score, print_out=True)")


# In[28]:


get_ipython().run_cell_magic('time', '', "model = 'Gaussian NB I'\nclf_gnbb = GaussianNB()\ngs_params = {} \ngs_score = 'roc_auc'\n\nclf_gnbb, pred_gnbb = bin_classify(model, clf_gnbb, imp_features, params=gs_params, score=gs_score)\nprint('\\nBest Parameters:\\n',clf_gnbb)\n\nmetrics_gnbi= bin_class_metrics(model, y_test, pred_gnbb.y_pred, pred_gnbb.y_score, print_out=True)")


# In[29]:


metrics_gnb = pd.concat([metrics_gnbb, metrics_gnba,metrics_gnbi], axis=1)
metrics_gnb


# In[ ]:




