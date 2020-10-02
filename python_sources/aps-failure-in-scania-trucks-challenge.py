#!/usr/bin/env python
# coding: utf-8

# ### Imports

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

import plotly
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=False)

from sklearn.feature_selection import chi2, f_classif, mutual_info_classif, GenericUnivariateSelect
from sklearn.preprocessing import Imputer, StandardScaler
# from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, fbeta_score, make_scorer, f1_score
# from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.base import TransformerMixin, BaseEstimator

from keras.wrappers.scikit_learn import KerasClassifier

from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline, make_pipeline
from imblearn.ensemble import BalancedBaggingClassifier, EasyEnsembleClassifier

import lightgbm as lgb
from lightgbm.sklearn import LGBMClassifier


# In[ ]:


def challenge_metric(y_true, y_pred):
    """
     Predicted class |      True class       |
                     |    pos    |    neg    |
     -----------------------------------------
      pos            |     -     |  Cost_1   |
     -----------------------------------------
      neg            |  Cost_2   |     -     |
     -----------------------------------------
     Cost_1 = 10 and cost_2 = 500

     Total_cost = Cost_1*No_Instances + Cost_2*No_Instances.
    """

    Cost_1 = 10
    Cost_2 = 500

    tn, fp, fn, tp = confusion_matrix(y_true=y_true, y_pred=y_pred).ravel()
    return Cost_1 * fp + Cost_2 * fn


def negative_challenge_metric(y_true, y_pred):
    return -challenge_metric(y_true=y_true, y_pred=y_pred)


def impute_target_class(df, strategy="mean"):
    """
    Impute a pandas dataframe by the statistic (mean/median/mode) of the target class
    """

    if strategy != "mean" and strategy != "median" and strategy != "mode":
        raise Exception("Invalid strategy: {}".format(strategy))

    df1 = df.copy()  # Make a copy of the original df

    df_groupby = df1.groupby("class")

    df_groups = []
    for group, df_group in df_groupby:
        if strategy == "mean":
            df_group.fillna(df_group.mean(), inplace=True)
        elif strategy == "median":
            df_group.fillna(df_group.median(), inplace=True)
        elif strategy == "mode":
            df_group.fillna(df_group.mode(), inplace=True)

        df_groups.append(df_group)

    df1 = pd.concat(df_groups, axis=0)
    return df1.iloc[np.argsort(df1.index)]


# In[ ]:


class PandasColumnsSelector(BaseEstimator, TransformerMixin):
    """
    Select a pandas dataframe using columns.
    """

    def __init__(self, columns="all"):
        if isinstance(columns, str) and columns != "all":
            raise ValueError("Invalid columns: {}".format(columns))

        self.columns = columns

    def fit(self, *_):
        return self

    def transform(self, X, *_):
        if isinstance(self.columns, str) and self.columns == "all":
            self.columns = X.columns

        return X[self.columns]


class PandasCorrelatedFeaturesDropper(BaseEstimator, TransformerMixin):
    """
    Drop highly correlated features from a pandas dataframe.
    """

    def __init__(self, corr_threshold=0.95):
        self.corr_threshold = corr_threshold

    def fit(self, X, *_):
        corr_matrix = X.corr().abs()
        upper = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        to_drop = [col for col in upper.columns if any(
            upper[col] >= self.corr_threshold)]
        self.to_drop = to_drop
        return self

    def transform(self, X, *_):
        return X.drop(self.to_drop, axis=1)


class PandasHighNullRatioFeaturesDropper(BaseEstimator, TransformerMixin):
    """
    Drop high null ratio features from a dataframe.
    """

    def __init__(self, null_ratio_threshold=0.4):
        self.null_ratio_threshold = null_ratio_threshold

    def fit(self, X, *_):
        drop_mask = ((X.isnull().sum() / len(X)) >= self.null_ratio_threshold)
        self.drop_columns = X.columns[drop_mask]
        return self

    def transform(self, X, *_):
        return X.drop(self.drop_columns, axis=1)


class PandasNullMarkerFeaturesCreator(BaseEstimator, TransformerMixin):
    """
    Create new features by marking null values in a pandas dataframe.
    """

    def __init__(self, columns="all", null_threshold=None):
        if isinstance(columns, str) and columns != "all":
            raise ValueError("Invalid columns: {}".format(columns))

        self.columns = columns
        self.null_threshold = null_threshold

    def fit(self, X, *_):
        if self.null_threshold is None:
            self.null_threshold = 0

        over_threshold = (X.isnull().sum() / len(X)) >= self.null_threshold
        self.cols_over_threhold = over_threshold[over_threshold].index

        return self

    def transform(self, X, *_):
        if isinstance(self.columns, str) and self.columns == "all":
            self.columns = X.columns

        null_markers_df = X[self.columns][self.cols_over_threhold].isnull().astype(
            "int")
        null_markers_df.columns = ["{}_is_null".format(
            col) for col in null_markers_df.columns]
        return pd.concat([X, null_markers_df], axis=1)


# ### Configurations

# In[ ]:


USE_LGB = False # Whether to fit the lightgbm model


# ### Data Loading
# <hr>
# Load data from the csv files located in the "<b>input</b>" directory.

# In[ ]:


# df_train = pd.read_csv("../input/aps_failure_training_set.csv", skiprows=20, na_values=["na"])
# df_test = pd.read_csv("../input/aps_failure_test_set.csv", skiprows=20, na_values=["na"])

df_train = pd.read_csv("../input/aps_failure_training_set.csv", na_values=["na"])
df_test = pd.read_csv("../input/aps_failure_test_set.csv", na_values=["na"])


# In[ ]:


df_train.shape


# In[ ]:


df_test.shape


# In[ ]:


df_train.columns


# In[ ]:


df_test.columns


# Convert "<b>class</b>" column to binary

# In[ ]:


df_train["class"] = (df_train["class"] == "pos").astype("int")
df_test["class"] = (df_test["class"] == "pos").astype("int")


# ### Exploration
# <hr>
# We will be using mostly plotly for visualizations due to its interactivity.

# First, let's have a look at some statistics.

# In[ ]:


df_train.describe()


# #### Target Class Distribution
# Let's have a look at the target class distribution.

# In[ ]:


class_value_counts = df_train["class"].value_counts()

trace = go.Pie(labels=class_value_counts.index, 
               values=class_value_counts.values,
               marker={
                   "colors": ["blue", "red"]
               })

data = [trace]
layout = go.Layout(title="Target Class Distribution for Training Set")

fig = go.Figure(data=data, layout=layout)
plotly.offline.iplot(fig)


# Seems like we have a highly <b>imbalanced</b> dataset! We will be using ensembles of classifiers with random under/over sampling to handle this directly in the cross-validation grid search later.
# <br>
# <br>
# An ensemble of classifiers is required to avoid sampling the wrong stuffs if we do resampling only once.

# #### Null Ratio
# Lets have a look at the null ratio of the features.

# In[ ]:


NULL_RATIO_TRHESHOLD = 0 # Set the null ratio threshold required


null_ratios = (df_train.isnull().sum() / df_train.shape[0])
null_ratios_over_threshold = null_ratios[null_ratios > NULL_RATIO_TRHESHOLD].sort_values(ascending=False)

data = [
    go.Bar(
        x=null_ratios_over_threshold.index,
        y=null_ratios_over_threshold
    )
]

fig = go.Figure(data=data, layout={
    "title": "Null Ratio for Features with Null Ratio Exceeding {}".format(NULL_RATIO_TRHESHOLD)
})

plotly.offline.iplot(fig)


# We have quite a few features over <b>70%</b> null ratio! We will be integrating dropping of high null ratio features into cross-validation grid search later.

# #### Correlation
# Let's have a look at the feature correlations.

# In[ ]:


def plot_plotly_scatter_matrix(df, features):
    """
    Plot plotly scatter matrix given pandas dataframe and list of required features.
    Assumes dataframe has a binary valued column called "class".
    """
    
    rows = len(features)
    cols = rows

    fig = plotly.tools.make_subplots(rows=rows, cols=cols)

    neg_class = df[df["class"] == 0]
    pos_class = df[df["class"] == 1]

    for i, f1 in enumerate(features):
        for j, f2 in enumerate(features):
#             print(f1, f2)

            trace0 = go.Scattergl(
                x = neg_class[f2],
                y = neg_class[f1],
                name = '0',
                mode = 'markers',
                marker = dict(
                    size = 2,
                    color = 'blue'
                ),
            )

            trace1 = go.Scattergl(
                x = pos_class[f2],
                y = pos_class[f1],
                name = '1',
                mode = 'markers',
                marker = dict(
                    size = 2,
                    color = 'red'
                ),
            )

            fig.append_trace(trace0, i+1, j+1)
            fig.append_trace(trace1, i+1, j+1)

            fig['layout']['xaxis{}'.format(i * cols + j+1)].update(title=f2)
            fig['layout']['yaxis{}'.format(i * cols + j+1)].update(title=f1)

    fig["layout"]["showlegend"] = False

    plotly.offline.iplot(fig)


# Compute the feature correlation matrix.

# In[ ]:


corr = df_train[df_train.columns.difference(["class"])].corr()
corr.shape


# In[ ]:


trace = go.Heatmap(z=corr.values,
                   x=corr.columns,
                   y=corr.index)

fig = go.Figure([trace], layout={
    "title": "Feature Correlations"
})
plotly.offline.iplot(fig)


# We can see some blocks of highly correlated features, we will try using cross-validation grid search to see if removing highly correlated features helps.

# #### Feature Importances

# Let's fit a random forest and see what it thinks are the importance features.

# In[ ]:


tree = RandomForestClassifier(class_weight="balanced")
tree.fit(Imputer(strategy="median").fit_transform(df_train[df_train.columns.difference(["class"])]), 
         df_train["class"])

feature_importances = pd.DataFrame([ [feature, importance] for feature, importance in zip(df_train.columns.difference(["class"]), tree.feature_importances_) ], columns=["feature", "importance"])
feature_importances = feature_importances.sort_values("importance", ascending=False)
feature_importances.reset_index(inplace=True)
print(feature_importances)


# Let's plot a scatter matrix of the top 5 most important features according to the model.

# In[ ]:


# plot_plotly_scatter_matrix(df_train, list(feature_importances[:5].feature))


# Here are the top five important features according to the model.

# In[ ]:


feature_importances[:5]["feature"]


# Let's see what univariate feature selection says regarding feature importances.

# In[ ]:


def get_univariate_feature_importances(df, score_func=chi2):
    """
    Get feature importances dataframe.
    """
    
    feature_selector = GenericUnivariateSelect(score_func, mode="percentile", param=100) # Select all features
    feature_selector.fit(Imputer(strategy="median").fit_transform(df[df.columns.difference(["class"])]), 
                         df_train["class"])
    score_df = pd.DataFrame([ [ feature, importance ] for feature, importance in zip(df.columns[1:], feature_selector.scores_) ], 
                            columns=["feature", "importance"])
    score_df = score_df.sort_values("importance", ascending=False)
    score_df.reset_index(drop=True, inplace=True)
    return score_df


# In[ ]:


score_chi2 = get_univariate_feature_importances(df_train)
print(score_chi2.head())


# In[ ]:


score_f_classif = get_univariate_feature_importances(df_train, score_func=f_classif)
print(score_f_classif.head())


# In[ ]:


df_train[df_train.columns.difference(["class"])[89]].describe()


# Thanks for letting us know feature "<b>cd_000</b>" is useless. Useless as it does not help to discriminate the target class.

# In[ ]:


score_mutual_info_classif = get_univariate_feature_importances(df_train, score_func=mutual_info_classif)
print(score_mutual_info_classif.head())


# In[ ]:


score_chi2["rank"] = score_chi2["importance"].rank(ascending=False)
score_f_classif["rank"] = score_f_classif["importance"].rank(ascending=False)
score_mutual_info_classif["rank"] = score_mutual_info_classif["importance"].rank(ascending=False)


# Feature importances according to chi2, ANOVA F-value, and mutual information

# In[ ]:


df_feature_scores = pd.merge(pd.merge(score_chi2, score_f_classif, how="left", on="feature", suffixes=["_chi2", "_f_classif"]), score_mutual_info_classif, how="left", on="feature")
df_feature_scores.columns = [
    "feature",
    
    "score_chi2",
    "rank_chi2",
    
    "score_f_classif",
    "rank_f_classif",

    "score_mutual_info_classif",
    "rank_mutual_info_classif"
]
df_feature_scores["mean_rank"] = (df_feature_scores["rank_chi2"] + df_feature_scores["rank_f_classif"] + df_feature_scores["rank_mutual_info_classif"]) / 3
df_feature_scores = df_feature_scores.sort_values("mean_rank", ascending=True)
df_feature_scores["mean_rank1"] = df_feature_scores["mean_rank"].rank(ascending=True)
df_feature_scores.reset_index(drop=True, inplace=True)
df_feature_scores


# ### Model Development
# <hr>
# We will be integrating the following functions into cross-validation grid search to find the best model:
# <ol>
#     <li><b>Pre-processing</b> (dropping of high null ratio features, imputation, etc)</li>
#     <li><b>Feature engineering</b> (creating new features by marking null values, etc)</li>
#     <li><b>Feature selection</b> (select best features based on univariate statistical tests, dimensionality reduction techniques (PCA) etc)</li>
#     <li><b>Handling target class imbalance</b> (ensembles of balanced random sampling, etc)</li>
#     <li><b>Model hyperparameter tuning</b></li>
# </ol>
# The reason for putting everything in the cross-validation grid search is so we can collectlively optimize all the parameters, e.g, what feature null ratio before dropping feature, what imputation strategy, etc.
# <br>
# <br>
# We will be saving trained models in the following format "<b>searcher_model-{TRAIN_SCORE}-{TEST_SCORE}.joblib</b>".
# I have put trained models in the "<b>models</b>" directory.
# To load a particular model, do: <b>model = joblib.load("{MODEL_JOBLIB_FILE}")</b>
# <br>
# <br>
# Due to extremely long computation time, I have splitted model training codes into separate jupyter notebooks to allow for parallel computation.
# <br>
# <br>
# I will be focusing the following models:
# <ul>
#     <li><b>xgboost</b>: Winners of many Kaggle challanges</li>
#     <li><b>lightgbm</b>: Same as above</li>
#     <li><b>Random Forest</b></li>
#     <li><b>Neural Network</b></li>
# </ul>
# I will not be using the following models:
# <ul>
#     <li>K Nearest Neighbors: too slow for grid search</li>
#     <li>Support Vector Machine: too slow for grid search</li>
# </ul>

# Load trained model

# In[ ]:


# model = joblib.load("models/searcher_lgb-23830-9050.joblib")


# Best model parameters after a grid search

# In[ ]:


# model.best_params_


# In[ ]:


# test_score = model.score(df_test, df_test["class"])
# print("challenge metric (test set):", test_score)


# Confusion matrix

# In[ ]:


# confusion_matrix(model.predict(df_test), df_test["class"])


# #### Grid Search
# Here this is the code for cross-validation grid search for the model Lightgbm.

# We will be using the negative challenge metric as the scorer in sklearn cross-validation grid search instead of the usual accuracy.

# In[ ]:


scorer = make_scorer(negative_challenge_metric)


# #### Lightgbm

# In[ ]:


pipeline_lgb = make_pipeline(
    PandasColumnsSelector(columns=df_train.columns.difference(["class"])),
    
    PandasHighNullRatioFeaturesDropper(), # We can either drop high null ratio features
#     PandasNullMarkerFeaturesCreator() # ...or we keep them, but create new features indicating null locations
    
    PandasCorrelatedFeaturesDropper(), # Drop highly correlated features
    
    Imputer(), # Replace null values, will put this step as low as possible to avoid any distortion to data
    
    GenericUnivariateSelect(chi2), # Feature selection based on univariate statistical testing

#     RandomUnderSampler(),
    BalancedBaggingClassifier(base_estimator=LGBMClassifier(num_threads=8), n_jobs=-1) # Ensembles of resampling LGBMClassifiers 
)
pipeline_lgb


# List model parameters

# In[ ]:


list(pipeline_lgb.get_params().keys())


# In[ ]:


searcher_lgb = GridSearchCV(estimator=pipeline_lgb, 
                            param_grid=[
                                {
#                                     "simpleimputer__strategy": ["median"],
                                    "imputer__strategy": ["median"],
                                    
#                                     "pandashighnullratiofeaturesdropper__null_ratio_threshold": [0.7, 1],
                                    "pandashighnullratiofeaturesdropper__null_ratio_threshold": [0.3, 0.5, 0.7],
#                                     "pandascorrelatedfeaturesdropper__corr_threshold": [0.9, 1],
                                    "pandascorrelatedfeaturesdropper__corr_threshold": [0.85, 0.9, 0.95],
                                    
                                    "genericunivariateselect__mode": ["percentile",],
#                                     "genericunivariateselect__param": [75, 100],
                                    "genericunivariateselect__param": [25, 50, 75],
                                    
#                                     "lgbmclassifier__boosting": ["gbdt", "dart", "goss"],
#                                     "lgbmclassifier__num_iterations": [100, 200, 500, 1000],
#                                     "balancedbaggingclassifier__base_estimator__boosting": ["gbdt", "dart", "goss"],
                                    "balancedbaggingclassifier__base_estimator__boosting": ["gbdt"],
                                    "balancedbaggingclassifier__base_estimator__num_iterations": [200, 300, 400],
#                                     "balancedbaggingclassifier__base_estimator__max_depth": [5, 7, -1],
                                    "balancedbaggingclassifier__base_estimator__max_depth": [6, 7, 8],
#                                     "balancedbaggingclassifier__base_estimator__min_data_in_leaf": [10, 20, 30],
                                    "balancedbaggingclassifier__base_estimator__min_data_in_leaf": [30, 40, 50],
#                                     "balancedbaggingclassifier__base_estimator__early_stopping_round": [0, 50],
#                                     "balancedbaggingclassifier__base_estimator__eval_metric": ["binary_logloss"],
#                                     "balancedbaggingclassifier__base_estimator__feature_fraction": [0.8, 0.9, 1],
                                    "balancedbaggingclassifier__base_estimator__feature_fraction": [1],
#                                     "balancedbaggingclassifier__base_estimator__bagging_fraction": [0.8, 0.9, 1],
                                    "balancedbaggingclassifier__base_estimator__bagging_fraction": [1],
                                    
                                    "balancedbaggingclassifier__n_estimators": [20,]
                                },
#                                 {
#                                     "simpleimputer__strategy": ["mean", "median"],
                                    
#                                     "pandashighnullratiofeaturesdropper__null_ratio_threshold": [0.25, 0.5, 0.75],
#                                     "pandascorrelatedfeaturesdropper__corr_threshold": [0.8, 0.9, 1],
                                    
#                                     "genericunivariateselect__mode": ["fdr", "fwe"],
#                                     "genericunivariateselect__param": [0.05, 0.01, 0.1],
                                    
# #                                     "lgbmclassifier__boosting": ["gbdt", "dart", "goss"],
# #                                     "lgbmclassifier__num_iterations": [100, 200, 500, 1000],
#                                     "balancedbaggingclassifier__base_estimator__boosting": ["gbdt", "dart", "goss"],
#                                     "balancedbaggingclassifier__base_estimator__num_iterations": [100, 200, 500, 1000],
#                                 }
                            ],
                            cv=3,
                            scoring=scorer)


# In[ ]:


if USE_LGB:
    searcher_lgb.fit(df_train, df_train["class"])


# In[ ]:


if USE_LGB:
    print(searcher_lgb.best_params_)


# In[ ]:


if USE_LGB:
    print(searcher_lgb.score(df_train, df_train["class"]))


# In[ ]:


if USE_LGB:
    print(searcher_lgb.score(df_test, df_test["class"]))


# In[ ]:


if USE_LGB:
    score_train = challenge_metric(y_pred=searcher_lgb.predict(df_train),
                                   y_true=df_train["class"])
    print("competition score (train set):", score_train)
    score_test = challenge_metric(y_pred=searcher_lgb.predict(df_test),
                                  y_true=df_test["class"])
    print("competition score (test set) :", score_test)
    
    # Save model
    joblib.dump(searcher_lgb, 'searcher_lgb-{}-{}.joblib'.format(score_train, score_test))

