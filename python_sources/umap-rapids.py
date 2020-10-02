#!/usr/bin/env python
# coding: utf-8

# ## Data Link
# https://www.kaggle.com/c/trends-assessment-prediction/data

# In[ ]:


import sys
get_ipython().system('cp ../input/rapids/rapids.0.13.0 /opt/conda/envs/rapids.tar.gz')
get_ipython().system('cd /opt/conda/envs/ && tar -xzvf rapids.tar.gz > /dev/null')
sys.path = ["/opt/conda/envs/rapids/lib/python3.6/site-packages"] + sys.path
sys.path = ["/opt/conda/envs/rapids/lib/python3.6"] + sys.path
sys.path = ["/opt/conda/envs/rapids/lib"] + sys.path
get_ipython().system('cp /opt/conda/envs/rapids/lib/libxgboost.so /opt/conda/lib/')


# In[ ]:


import numpy as np
import pandas as pd
import cudf
import cupy as cp
import warnings
from cuml.neighbors import KNeighborsRegressor
from cuml import SVR
from cuml.linear_model import Ridge, Lasso, ElasticNet

import cuml

from sklearn.model_selection import KFold
from sklearn.ensemble import BaggingRegressor

#from cuml.ensemble import RandomForestRegressor
#from sklearn.ensemble import RandomForestRegressor
#from cuml.neighbors import KNeighborsRegressor



import requests
import pandas as pd
import numpy as np
import datashader as ds
import datashader.utils as utils
import datashader.transfer_functions as tf
import matplotlib.pyplot as plt




def metric(y_true, y_pred):
    return np.mean(np.sum(np.abs(y_true - y_pred), axis=0)/np.sum(y_true, axis=0))


# In[ ]:


'''
I began this work in version 0.61 of cudf where the performance of cudf super differing from pandas, 
so I have to convert it to pandas to show samples of data.
''' 

fnc_df = cudf.read_csv("../input/trends-assessment-prediction/fnc.csv")
loading_df = cudf.read_csv("../input/trends-assessment-prediction/loading.csv")

#pd_fnc_df = fnc_df.to_pandas()
#pd_loading_df = loading_df.to_pandas()

labels_df = cudf.read_csv("../input/trends-assessment-prediction/train_scores.csv")

labels_df["is_train"] = True # label the train set as well as test set;


# In[ ]:


df = fnc_df.merge(loading_df, on="Id")
df = df.merge(labels_df, on="Id", how="left")

test_df = df[df["is_train"]!=True]
df = df[df["is_train"]==True]

# Take Id of train set:
id_df = cudf.DataFrame()
id_df["Id"] = df["Id"]

# Take Id of test set:
id_test_df = cudf.DataFrame()
id_test_df["Id"] = test_df["Id"]


df.shape, test_df.shape, id_df.shape, id_test_df.shape


# In[ ]:


fnc_df.shape, loading_df.shape, labels_df.shape, test_df.shape


# ## Uniform Manifold Approximation(UMAP) For Train Set

# In[ ]:


data_fnc = df.loc[:, df.columns[1:1378]]
data_loading = df.loc[:, df.columns[1379:1405]]


# In[ ]:


get_ipython().run_cell_magic('time', '', 'n_components_fnc = 30\n\nreducer_fnc = cuml.UMAP(\n    n_neighbors=15,\n    n_components=n_components_fnc,\n    n_epochs=500,\n    min_dist=0.1\n)\nemb_fnc = reducer_fnc.fit_transform(data_fnc)')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'n_components_loading = 20\n\nreducer_loading = cuml.UMAP(\n    n_neighbors=15,\n    n_components=n_components_loading,\n    n_epochs=500,\n    min_dist=0.1\n)\nemb_loading = reducer_loading.fit_transform(data_loading)')


# In[ ]:





# In[ ]:


plt_df = emb_fnc.to_pandas()
plt_df.columns.astype(str)
plt_df = plt_df.rename(columns={0:"x", 1:"y"})


# In[ ]:


#df.columns = ["x", "y"]


cvs = ds.Canvas(plot_width=400, plot_height=400)
#agg = cvs.points(df, "x", 'y')
agg = cvs.points(plt_df, 'x', 'y')
img = tf.shade(agg, how='eq_hist')

utils.export_image(img, filename='dfdf', background='black')

image = plt.imread('dfdf.png')
fig, ax = plt.subplots(figsize=(12, 12))
plt.imshow(image)
plt.setp(ax, xticks=[], yticks=[])
plt.title("TReNDS Center Train fnc Data\n"
          "into two dimensions by UMAP\n"
          "visualised with Datashader",
          fontsize=12)

plt.show()


# In[ ]:


id_df["key"] = emb_fnc["key"]= emb_loading["key"] = [x for x in range(len(emb_fnc))]
df = id_df.merge(emb_fnc, on="key")
df = df.merge(emb_loading, on="key")

df = df.drop("key")
df = df.merge(labels_df, on="Id")


# In[ ]:


df.shape


# In[ ]:


df.head(5)


# ## UMAP For test set

# In[ ]:


data_fnc = test_df.loc[:, test_df.columns[1:1378]]
data_loading = test_df.loc[:, test_df.columns[1379:1405]]

emb_fnc = reducer_fnc.transform(data_fnc)
emb_loading = reducer_loading.transform(data_loading)


# In[ ]:


plt_df = emb_fnc.to_pandas()
plt_df.columns.astype(str)
plt_df = plt_df.rename(columns={0:"x", 1:"y"})


# In[ ]:



#df['class'] = pd.Series([str(x) for x in target.to_array()], dtype="category")

cvs = ds.Canvas(plot_width=400, plot_height=400)
agg = cvs.points(plt_df, 'x', 'y')
img = tf.shade(agg, how='eq_hist')

utils.export_image(img, filename='dfdf', background='black')

image = plt.imread('dfdf.png')
fig, ax = plt.subplots(figsize=(12, 12))
plt.imshow(image)
plt.setp(ax, xticks=[], yticks=[])
plt.title("TReNDS Center Test Data\n"
          "into two dimensions by UMAP\n"
          "visualised with Datashader",
          fontsize=12)

plt.show()


# In[ ]:



id_test_df["key"] = emb_fnc["key"] = emb_loading["key"] = [x for x in range(len(test_df))]
test_df = id_test_df.merge(emb_fnc, on="key")
test_df = test_df.merge(emb_loading, on="key")
test_df = test_df.drop("key")


# In[ ]:


test_df.head(10)


# In[ ]:





# In[ ]:


# Giving less importance to FNC features since they are easier to overfit due to high dimensionality.
#FNC_SCALE = 1/485

#df[fnc_features] *= FNC_SCALE
#test_df[fnc_features] *= FNC_SCALE

df = df.astype("float32").copy()
test_df = test_df.astype("float32").copy()

df["Id"] = df["Id"].astype(int)
test_df["Id"] = test_df["Id"].astype(int)


# ## ensemble of models
# 
# \begin{equation}
# model = \sum_{i=1}^4 bw_i\cdot model_i
# \end{equation}
# 
# where $\sum bw_i=1$ and:
# 1. $model_1$ is the `SVR`
# 2. $model_2$ is the Ridge Regressor
# 3. $model_3$ is the BaggingRegressor based on Ridge Regressor
# 4. $model_4$ is the knn
# 5. $model_5$ is the Lasso Regressor
# 
# The convex hull of those above may perform better than any of them with appropriate blend weights $[bw_i]$. Note that $[bw_{ji}]$ is indeed a matrix associated with each target $j$ the $model_i$ to learn with.

# ## TRAIN MODEL

# In[ ]:


get_ipython().run_cell_magic('time', '', '\n# To suppress the "Expected column (\'F\') major order, but got the opposite." warnings from cudf. It should be fixed properly,\n# although as the only impact is additional memory usage, I\'ll supress it for now.\nwarnings.filterwarnings("ignore", message="Expected column")\n\n# Take a copy of the main dataframe, to report on per-target scores for each model.\n# TODO Copy less to make this more efficient.\ndf_model1 = df.copy() # model1 is SVR\ndf_model2 = df.copy() # model2 is Ridge regressor\ndf_model3 = df.copy() # model3 is BaggingRegressor based on Ridge regressor\ndf_model4 = df.copy() # model4 is knn;\ndf_model5 = df.copy() # Elastic\n\nNUM_FOLDS = 7\nkf = KFold(n_splits=NUM_FOLDS, shuffle=True, random_state=0)\n\nfeatures = [col for col in df.columns[1:-6]]\n\n# Blending weights between the three models are specified separately for the 5 targets. \n#                                SVR,  Ridge, BaggingRegressor, knn, Elastic;\nblend_weights = {"age":          [0.8,  0.1,  0.05,            0.025, 0.025],\n                 "domain1_var1": [0.8, 0.05,  0.05,             0.05, 0.05],\n                 "domain1_var2": [0.5, 0.0,   0.25,            0.125, 0.125],\n                 "domain2_var1": [0.55, 0.1,  0.3,             0.025, 0.025],\n                 "domain2_var2": [0.5,  0.05,  0.4,            0.025, 0.025]}\n\noverall_score = 0\n\n# Iteration for targets, together with parameters for SVR, weights of total scores;\nfor target, c, w in [("age", 60, 0.3), ("domain1_var1", 12, 0.175), ("domain1_var2", 8, 0.175), ("domain2_var1", 9, 0.175), ("domain2_var2", 12, 0.175)]:    \n    # initiate the target for each model with numpy, by which to reduce the overhead of GPU memories;\n    y_oof = np.zeros(df.shape[0])\n    y_oof_model_1 = np.zeros(df.shape[0])\n    y_oof_model_2 = np.zeros(df.shape[0])\n    y_oof_model_3 = np.zeros(df.shape[0])\n    y_oof_model_4 = np.zeros(df.shape[0])\n    y_oof_model_5 = np.zeros(df.shape[0])\n    \n    \n    y_test = np.zeros((test_df.shape[0], NUM_FOLDS))\n    \n    # Iteration for folds, in each fold, the validation set only 1/NUM_FOLDS;\n    for f, (train_ind, val_ind) in enumerate(kf.split(df, df)):\n        train_df, val_df = df.iloc[train_ind], df.iloc[val_ind]\n        train_df = train_df[train_df[target].notnull()]\n        \n        # train SVR, Ridge by cuml directly;\n        model_1 = SVR(C=c, cache_size=3000.0)\n        model_1.fit(train_df[features].values, train_df[target].values)\n        model_2 = Ridge(alpha = 0.0001)\n        model_2.fit(train_df[features].values, train_df[target].values)\n        \n        ### The BaggingRegressor, using the Ridge regression method as a base, is added here. The BaggingRegressor\n        # is from sklearn, not RAPIDS, so dataframes need converting to Pandas.\n        model_3 = BaggingRegressor(Ridge(alpha = 0.0001), n_estimators=30, random_state=42, max_samples=0.3, max_features=0.3)\n        model_3.fit(train_df.to_pandas()[features].values, train_df.to_pandas()[target].values)\n                \n        \n        #model_4 = RandomForestRegressor(n_estimators = 150, max_depth=13)\n        #model_4.fit(train_df.to_pandas()[features].values, train_df.to_pandas()[target].values)\n        \n        model_4 = Lasso(alpha=0.15)\n        model_4.fit(train_df[features].values, train_df[target].values)\n        \n        model_5 = ElasticNet(alpha = 0.1, l1_ratio=0.5)\n        model_5.fit(train_df[features].values, train_df[target].values)\n        \n        # The target to predict here is determined by the [target] choosed in above training\n        # The prediction of validation just working on the validation set in this fold\n        # The output should be embeded in y_oof_model_i\n        val_pred_1 = model_1.predict(val_df[features])\n        val_pred_2 = model_2.predict(val_df[features])\n        val_pred_3 = model_3.predict(val_df.to_pandas()[features])\n        val_pred_3 = cudf.from_pandas(pd.Series(val_pred_3))\n        \n        #val_pred_4 = model_4.predict(val_df.to_pandas()[features])\n        #val_pred_4 = cudf.from_pandas(pd.Series(val_pred_4))\n        \n        val_pred_4 = model_4.predict(val_df[features])\n        val_pred_5 = model_5.predict(val_df[features])\n        \n        # The prediction of test set working on the total test set with the fold number as features;\n        test_pred_1 = model_1.predict(test_df[features])\n        test_pred_2 = model_2.predict(test_df[features])\n        test_pred_3 = model_3.predict(test_df.to_pandas()[features])\n        test_pred_3 = cudf.from_pandas(pd.Series(test_pred_3))\n        \n        #test_pred_4 = model_4.predict(test_df.to_pandas()[features])\n        #test_pred_4 = cudf.from_pandas(pd.Series(test_pred_4))\n        \n        test_pred_4 = model_4.predict(test_df[features])\n        test_pred_5 = model_5.predict(test_df[features])\n        \n        val_pred = blend_weights[target][0]*val_pred_1+blend_weights[target][1]*val_pred_2+blend_weights[target][2]*val_pred_3+blend_weights[target][3]*val_pred_4+blend_weights[target][4]*val_pred_5\n        val_pred = cp.asnumpy(val_pred.values.flatten())\n        \n        test_pred = blend_weights[target][0]*test_pred_1+blend_weights[target][1]*test_pred_2+blend_weights[target][2]*test_pred_3+blend_weights[target][3]*test_pred_4+blend_weights[target][4]*test_pred_5\n        test_pred = cp.asnumpy(test_pred.values.flatten())\n        \n        y_oof[val_ind] = val_pred # predicted score with total blend weights\n        \n        # prediction for single model:\n        y_oof_model_1[val_ind] = val_pred_1 # validation just 1/NUM_FOLDS of df, in each fold, it just part of df;\n        y_oof_model_2[val_ind] = val_pred_2\n        y_oof_model_3[val_ind] = val_pred_3\n        y_oof_model_4[val_ind] = val_pred_4\n        y_oof_model_5[val_ind] = val_pred_5\n        \n        y_test[:, f] = test_pred # Add fold number f as a feature for predicted target of total test set;\n    \n    # add pred_{} column\n    df["pred_{}".format(target)] = y_oof \n    df_model1["pred_{}".format(target)] = y_oof_model_1\n    df_model2["pred_{}".format(target)] = y_oof_model_2\n    df_model3["pred_{}".format(target)] = y_oof_model_3\n    df_model4["pred_{}".format(target)] = y_oof_model_4\n    df_model5["pred_{}".format(target)] = y_oof_model_5\n    \n    test_df[target] = y_test.mean(axis=1) # Averaging on folds;\n    \n    # compute the total score\n    score = metric(df[df[target].notnull()][target].values, df[df[target].notnull()]["pred_{}".format(target)].values)\n    overall_score += w*score\n    \n    score_model1 = metric(df_model1[df_model1[target].notnull()][target].values, df_model1[df_model1[target].notnull()]["pred_{}".format(target)].values)\n    score_model2 = metric(df_model2[df_model2[target].notnull()][target].values, df_model2[df_model1[target].notnull()]["pred_{}".format(target)].values)\n    score_model3 = metric(df_model3[df_model3[target].notnull()][target].values, df_model3[df_model1[target].notnull()]["pred_{}".format(target)].values)\n    score_model4 = metric(df_model4[df_model4[target].notnull()][target].values, df_model4[df_model1[target].notnull()]["pred_{}".format(target)].values)\n    score_model5 = metric(df_model5[df_model5[target].notnull()][target].values, df_model5[df_model1[target].notnull()]["pred_{}".format(target)].values)\n\n    \n    print(f"For {target}:")\n    print("SVR:", np.round(score_model1, 6))\n    print("Ridge:", np.round(score_model2, 6))\n    print("BaggingRegressor:", np.round(score_model3, 6))\n    print("Lasso", np.round(score_model4, 6))\n    print("Elastic", np.round(score_model5, 6))\n    print("Ensemble:", np.round(score, 6))\n    print()\n    \nprint("Overall score:", np.round(overall_score, 6))')


# In[ ]:


test_df.shape


# In[ ]:


# Preparing the submission dataframe:

sub_df = cudf.melt(test_df[["Id", "age", "domain1_var1", "domain1_var2", "domain2_var1", "domain2_var2"]], id_vars=["Id"], value_name="Predicted")
# Unpivots a DataFrame from wide format to long format, optionally leaving identifier variables set.
# It generates a new list with repeat "Id" corresponding the other 5 features;


# The following column "variable" is auto-generated by .melt attribute;
sub_df["Id"] = sub_df["Id"].astype("str") + "_" +  sub_df["variable"].astype("str")

sub_df = sub_df.drop("variable", axis=1).sort_values("Id") # sorting by new "Id"
assert sub_df.shape[0] == test_df.shape[0]*5 # To check whether the sub_df has five times more rows than test_df, since the prediction has five: age, domain{x_var{y
sub_df.tail(10)


# In[ ]:


#sub_df = sub_df.astype(int)
sub_df.to_csv("submission_UMAP.csv", index=False)

