#!/usr/bin/env python
# coding: utf-8

# # Introduction
# After feature selection, we will find a model that shows the highest accuracy through modeling techniques such as DecisionTree, MLP, and Ensemble, using the Linear regression model as the baseline.

# ## 1) Feature selection
#     If there are a large number of features, the complexity increases with the number of samples, so the probability of overfitting is high. Therefore, the Irrelevant feature and the Redundant Feature will be removed to see the difference from the original feature.

# #Import training dataset, test dataset into Pandas

# In[ ]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as matplot
import numpy as np

import re
import sklearn

import warnings
warnings.filterwarnings("ignore")

get_ipython().run_line_magic('matplotlib', 'inline')

df_train = pd.read_csv('../input/Train_data.csv')
df_test = pd.read_csv('../input/test_data.csv')
df_test = df_test.drop('Unnamed: 0',axis=1)


# In[ ]:


df_train.head()


# In[ ]:


df_test.head()


# ##Save training dataset and test dateaset to each df and split X and Y (xAttack, analysis features)

# In[ ]:


X_train = df_train.drop('xAttack', axis=1)
Y_train = df_train.loc[:,['xAttack']]
X_test = df_test.drop('xAttack', axis=1)
Y_test = df_test.loc[:,['xAttack']]


# #Preprocessing and one hot encoding, X is onehotencoder, Y is LabelBinarizer****

# In[ ]:


from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder


# In[ ]:


le = preprocessing.LabelEncoder()
enc = OneHotEncoder()
lb = preprocessing.LabelBinarizer()


# - X OneHotEncoding

# In[ ]:


X_train['protocol_type'] = le.fit_transform(X_train['protocol_type'])
# enc.fit_transform(X_train['protocol_type'])

X_test['protocol_type'] = le.fit_transform(X_test['protocol_type'])
# enc.fit_transform(X_test['protocol_type'])

X_train.head()


# - Y LabelBinarizer

# In[ ]:


Y_train['xAttack'] = le.fit_transform(Y_train['xAttack'])
lb.fit_transform(Y_train['xAttack'])

Y_test['xAttack'] = le.fit_transform(Y_test['xAttack'])
lb.fit_transform(Y_test['xAttack'])

Y_train.describe()


# ### 1. Standard deviation
# We have applied a method to exclude features with small standard deviation (small deviation). However, when the feature type is discrete, the deviation is small.

# In[ ]:


#except continuous feature
con_list = ['protocol_type', 'service', 'flag', 'land', 'logged_in', 'su_attempted', 'is_host_login', 'is_guest_login']
con_train = X_train.drop(con_list, axis=1)

#drop n smallest std features
stdtrain = con_train.std(axis=0)
std_X_train = stdtrain.to_frame()
std_X_train.nsmallest(10, columns=0).head(10)


# num_outbound_cmds is removed from the first because the standard deviation is zero.

# In[ ]:


X_train = X_train.drop(['num_outbound_cmds'], axis=1)
X_test = X_test.drop(['num_outbound_cmds'], axis=1)

df_train = pd.concat([X_train, Y_train], axis=1)
df_train.head()

X_train.head()


# Std picks the 10 low and stores the features in drop -> X_train_stdrop. (Will be used after ensemble feature selection)

# In[ ]:


stdrop_list = ['urgent', 'num_shells', 'root_shell',
        'num_failed_logins', 'num_access_files', 'dst_host_srv_diff_host_rate',
        'diff_srv_rate', 'dst_host_diff_srv_rate', 'wrong_fragment']

X_test_stdrop = X_test.drop(stdrop_list, axis=1)

X_train_stdrop = X_train.drop(stdrop_list, axis=1)

df_train_stdrop = pd.concat([X_train_stdrop, Y_train], axis=1)

df_train_stdrop.head()


# Baseline - Learn about performance with linear regression

# - Linear regression

# In[ ]:


from sklearn import linear_model


# In[ ]:


LR = linear_model.LinearRegression()


# In[ ]:


LR.fit(X_train, Y_train)


# In[ ]:


lr_score = LR.score(X_test, Y_test)
print('Linear regression processing ,,,')
print('Linear regression Score: %.2f %%' % lr_score)


# The linear regression yields only 33% probability.

# ### 2. Ensemble feature selection
# Ensemble Modeling can see how the feature affected each model. Therefore, we tried feature selection around those features (attempt to remove Irrelevant feature).

# In[ ]:


from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.tree import DecisionTreeClassifier


# In[ ]:


AB = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(), n_estimators=100, learning_rate=1.0)
RF = RandomForestClassifier(n_estimators=10, criterion='entropy', max_features='auto', bootstrap=True)
ET = ExtraTreesClassifier(n_estimators=10, criterion='gini', max_features='auto', bootstrap=False)
GB = GradientBoostingClassifier(loss='deviance', learning_rate=0.1, n_estimators=200, max_features='auto')


# In[ ]:


y_train = Y_train['xAttack'].ravel()
x_train = X_train.values
x_test = X_test.values


# Check the feature importances to see how accurate the basic features are.

# In[ ]:


AB.fit(X_train, Y_train)


# In[ ]:


AB_feature = AB.feature_importances_
AB_feature

ab_score = AB.score(X_test, Y_test)

print('AdaBoostClassifier processing ,,,')
print('AdaBoostClassifier Score: %.3f %%' % ab_score)


# In[ ]:


RF.fit(X_train, Y_train)


# In[ ]:


RF_feature = RF.feature_importances_
RF_feature

rf_score = RF.score(X_test, Y_test)

print('RandomForestClassifier processing ,,,')
print('RandomForestClassifier Score: %.3f %%' % rf_score)


# In[ ]:


ET.fit(X_train, Y_train)


# In[ ]:


ET_feature = ET.feature_importances_
ET_feature

et_score = ET.score(X_test, Y_test)

print('ExtraTreesClassifier processing ,,,')
print('ExtraTreeClassifier: %.3f %%' % et_score)


# In[ ]:


GB.fit(X_train, Y_train)


# In[ ]:


GB_feature = GB.feature_importances_
GB_feature

gb_score = GB.score(X_test, Y_test)

print('GradientBoostingClassifier processing ,,,')
print('GradientBoostingClassifier Score: %.3f %%' % gb_score)


# Let's look at how the features affect each other through Ensemble

# In[ ]:


cols = X_train.columns.values

feature_df = pd.DataFrame({'features': cols,
                           'AdaBoost' : AB_feature,
                           'RandomForest' : RF_feature,
                           'ExtraTree' : ET_feature,
                           'GradientBoost' : GB_feature
                          })
feature_df.head(8)


# Graphs showing the influence of features

# In[ ]:


from matplotlib.ticker import MaxNLocator
from collections import namedtuple

graph = feature_df.plot.bar(figsize = (18, 10), title = 'Feature distribution', grid=True, legend=True, fontsize = 15, 
                            xticks=feature_df.index)
graph.set_xticklabels(feature_df.features, rotation = 80)


# #### Extract twelve features from each Ensemble model

# In[ ]:


a_f = feature_df.nlargest(12, 'AdaBoost')
e_f = feature_df.nlargest(12, 'ExtraTree')
g_f = feature_df.nlargest(12, 'GradientBoost')
r_f = feature_df.nlargest(12, 'RandomForest')


# #### Delete Duplicates

# In[ ]:


result = pd.concat([a_f, e_f, g_f, r_f])
result = result.drop_duplicates() # delete duplicate feature
result


# In[ ]:


selected_features = result['features'].values.tolist()
selected_features


# #### Below are the results of training with the exception of the features with small standard deviations.

# In[ ]:


AB.fit(X_train_stdrop, Y_train)


# In[ ]:


ab2_score = AB.score(X_test_stdrop, Y_test)

print('AdaBoostClassifier_stdrop processing ,,,')
print('AdaBoostClasifier Score: %.3f %%' % ab2_score)


# In[ ]:


RF.fit(X_train_stdrop, Y_train)


# In[ ]:


rf2_score = RF.score(X_test_stdrop, Y_test)

print('RandomForestClassifier_stdrop processing ,,,')
print('RandomForestClassifier Score: %.3f %%' % rf2_score)


# In[ ]:


ET.fit(X_train_stdrop, Y_train)


# In[ ]:


et2_score = ET.score(X_test_stdrop, Y_test)

print('ExtraTreesClassifier_stdrop processing ,,,')
print('ExtraTreesClassifier Score: %.3f %%' % et2_score)


# In[ ]:


GB.fit(X_train_stdrop, Y_train)


# In[ ]:


gb2_score = GB.score(X_test_stdrop, Y_test)

print('GradientBoostingClassifier_stdrop processing ,,,')
print('GradientBoostingClassifier Score: %.2f %%' % gb2_score)


# #### Only features obtained through ensemble

# In[ ]:


X_train_ens = X_train[selected_features]
X_train_ens.head()

X_test_ens = X_test[selected_features]
X_test_ens.head()


# ### 3. Correlation
# Features that have high correlation among multiple features (redundant features) 
# are merged or deleted. This is because if there is a large correlation between these features, 
# there is no need to increase the number of features.

# In[ ]:


sample = X_train_ens[:10000]

colormap = plt.cm.viridis
plt.figure(figsize=(20, 20))
sns.heatmap(sample.astype(float).corr(), linewidths=0.1, vmax=1.0, square=True, cmap=colormap, annot=True)


# #### The above graph analysis shows that the dependency is high in the following features

# In[ ]:


selected2 = ['flag', 'dst_host_serror_rate', 'serror_rate']
X_train_cordrop = X_train_ens.drop(selected2, axis=1)
X_train_cordrop.describe()

X_test_cordrop = X_test_ens.drop(selected2, axis=1)
X_test_cordrop.describe()


# ## 2) Modeling

# #### Modeling after completion of the feature selection process (elimination of low deviation, high correlation)
# #### Comparing final modeling results with features that affect ensemble modeling

# ### Ensemble Modeling results with final modeling impact

# In[ ]:


AB.fit(X_train_cordrop, Y_train)


# In[ ]:


ab_finalscore = AB.score(X_test_cordrop, Y_test)

print('AdaBoostClassifier_final processing ,,,')
print('AdaBoostClassifier_final Score: %.3f %%' % ab_finalscore)


# In[ ]:


RF.fit(X_train_cordrop, Y_train)


# In[ ]:


rf_finalscore = RF.score(X_test_cordrop, Y_test)

print('RandomForestClassifier_final processing ,,,')
print('RandomForestClassifier_final Score: %.3f %%' % rf_finalscore)


# In[ ]:


ET.fit(X_train_cordrop, Y_train)


# In[ ]:


et_finalscore = ET.score(X_test_cordrop, Y_test)

print('ExtraTreesClassifier_final processing ,,,')
print('ExtraTreesClassifier_final Score: %.3f %%' % et_finalscore)


# In[ ]:


GB.fit(X_train_cordrop, Y_train)


# In[ ]:


gb_finalscore = GB.score(X_test_cordrop, Y_test)

print('GradientBoostClassifier_final processing ,,,')
print('GradientBoostClassifier_final Score: %.3f %%' % gb_finalscore)


# In[ ]:


LR.fit(X_train_cordrop, Y_train)


# In[ ]:


lr_finalscore = LR.score(X_test_cordrop, Y_test)

print('LinearRegression_final processing ,,,')
print('LinearRegression_final Score: %.3f %%' % lr_finalscore)


# In[ ]:


from sklearn.neural_network import MLPClassifier


# In[ ]:


MLP = MLPClassifier(hidden_layer_sizes=(1000, 300, 300), solver='adam', shuffle=False, tol = 0.0001)


# In[ ]:


MLP.fit(X_train_cordrop, Y_train)


# In[ ]:


mlp_finalscore = MLP.score(X_test_cordrop, Y_test)

print('MLP_final processing ,,,')
print('MLP_final Score: %.3f %%' % mlp_finalscore)


# ## 3) Result

# As a result, feature selection and extraction did not result in high probability. I have seen 1-2% increase in accuracy, but I think the feature will be reduced and it will be able to operate a little faster and will prevent overfitting when new data comes in.
# 
# Comparing the score of each model
# 
# - first models

# In[ ]:


first_model = {'Model': ['Linear Regression', 'Adaboost', 'RandomForest', 'ExtraTrees', 'GradientBoost'],
               'accuracy' : [lr_score, ab_score, rf_score, et_score, gb_score]}

result_df = pd.DataFrame(data = first_model)
result_df


# In[ ]:


r1 = result_df.plot(x='Model', y='accuracy', kind='bar', figsize=(8, 8), grid=True, title='FIRST MODEL ACCURACY', colormap=plt.cm.viridis,
               sort_columns=True)
r1.set_xticklabels(result_df.Model, rotation = 45)


# - second models

# In[ ]:


second_model = {'Model': ['Adaboost', 'RandomForest', 'ExtraTrees', 'GradientBoost'],
               'accuracy' : [ab2_score, rf2_score, et2_score, gb2_score]}

result_df = pd.DataFrame(data = second_model)
result_df


# In[ ]:


r2 = result_df.plot(x='Model', y='accuracy', kind='bar', figsize=(8, 8), grid=True, title='SECOND MODEL ACCURACY', colormap=plt.cm.viridis,
               sort_columns=True)
r2.set_xticklabels(result_df.Model, rotation = 45)


# - final models

# In[ ]:


final_model = {'Model': ['Linear Regression', 'Adaboost', 'RandomForest', 'ExtraTrees', 'GradientBoost', 'MLP'],
               'accuracy' : [lr_finalscore, ab_finalscore, rf_finalscore, et_finalscore, gb_finalscore, mlp_finalscore]}

result_df = pd.DataFrame(data = final_model)
result_df


# In[ ]:


r3 = result_df.plot(x='Model', y='accuracy', kind='bar', figsize=(8, 8), grid=True, title='FINAL MODEL ACCURACY', colormap=plt.cm.viridis,
               sort_columns=True)
r3.set_xticklabels(result_df.Model, rotation = 45)


# ## FASTEST AND ACCURATE MODEL - ExtraTrees of the final model (76.4%)
# ## STRONGEST AND THE MOST ACCURATE MODEL - GradientBoost of the final model (77.1%)
# 
# Gradient boost has a 77 percent chance, but the speed is significantly faster with ExtraTress.

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




