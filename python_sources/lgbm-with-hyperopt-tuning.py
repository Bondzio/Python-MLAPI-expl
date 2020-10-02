#!/usr/bin/env python
# coding: utf-8

# # LGBM classifier using HyperOpt tuning
# 
# This is classifier using the LGBM Python sklearn API to predict passenger survival probability. The LGBM hyperparameters are optimized using Hyperopt. The resulting accuracy is around 80%, which seems to be where most models for this dataset are at the best without cheating. Used features are mainly collected from other popular kernels, with a bit of personal tuning.

# In[ ]:


import numpy as np
import pandas as pd
from hyperopt import hp, tpe, Trials
from hyperopt.fmin import fmin
import lightgbm as lgbm
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
import hyperopt
from sklearn.preprocessing import LabelEncoder


# In[ ]:


get_ipython().system('ls ../input')


# In[ ]:


df_train = pd.read_csv("../input/train.csv")
df_test = pd.read_csv("../input/test.csv")
df_train.head()


# The above columns in the data are quite self-explanatory with two exceptions:
# 
# sibsp:	number of siblings / spouses aboard the Titanic	
# parch:	number of parents / children aboard the Titanic
# 

# In[ ]:


df_train.shape


# As the shape shows, the dataset is small. But it is nice to practice and experiment on.

# In[ ]:


df_test.shape


# Combine train and test sets to create new features for both sets at once. Mark them with 1 and 0 to split them back later.

# In[ ]:


df_train["train"] = 1
df_test["train"] = 0
df_all = pd.concat([df_train, df_test], sort=False)
df_all.head()


# In[ ]:


df_all.tail()


# Will be predicting survival. So take that as target:

# In[ ]:


y = df_train["Survived"]
y.head()


# Functions to create features from cabin type, cabin number, and number of cabins a passenger has reserved:

# In[ ]:


def parse_cabin_type(x):
    if pd.isnull(x):
        return None
    #print("X:"+x[0])
    #cabin id consists of letter+numbers. letter is the type/deck, numbers are cabin number on deck
    return x[0]


# In[ ]:


def parse_cabin_number(x):
    if pd.isnull(x):
        return -1
#        return np.nan
    cabs = x.split()
    cab = cabs[0]
    num = cab[1:]
    if len(num) < 2:
        return -1
        #return np.nan
    return num


# In[ ]:


def parse_cabin_count(x):
    if pd.isnull(x):
        return np.nan
    #a typical passenger has a single cabin but some had multiple. in that case they are space separated
    cabs = x.split()
    return len(cabs)


# In[ ]:


df_train.dtypes


# To see what types of cabins there are:

# In[ ]:


cabin_types = df_all["Cabin"].apply(lambda x: parse_cabin_type(x))
cabin_types = cabin_types.unique()
#drop the nan value from list of cabin types
cabin_types = np.delete(cabin_types, np.where(cabin_types == None))
cabin_types


# To create the features for cabin type, cabin number, and number of cabins:

# In[ ]:


df_all["cabin_type"] = df_all["Cabin"].apply(lambda x: parse_cabin_type(x))
df_all["cabin_num"] = df_all["Cabin"].apply(lambda x: parse_cabin_number(x))
df_all["cabin_count"] = df_all["Cabin"].apply(lambda x: parse_cabin_count(x))
df_all["cabin_num"] = df_all["cabin_num"].astype(int)
df_all.head()


# One-hot encode categorical variables (embarked, cabin type, gender):

# In[ ]:


embarked_dummies = pd.get_dummies(df_all["Embarked"], prefix="embarked_", dummy_na=True)
#TODO: see if imputing embardked makes a difference
df_all = pd.concat([df_all, embarked_dummies], axis=1)
df_all.head()


# In[ ]:


cabin_type_dummies = pd.get_dummies(df_all["cabin_type"], prefix="cabin_type_", dummy_na=True)
df_all = pd.concat([df_all, cabin_type_dummies], axis=1)
df_all.head()


# In[ ]:


l_enc = LabelEncoder()
df_all["sex_label"] = l_enc.fit_transform(df_all["Sex"])
df_all.head()


# Create new feature from combined family size:

# In[ ]:


df_all["family_size"] = df_all["SibSp"] + df_all["Parch"] + 1
df_all.head()


# In[ ]:


df_all.columns


# Title parsing and family survival borrowed from this [kernel](https://www.kaggle.com/vincentlugat/200-lines-randomized-search-lgbm-82-3). Don't know if that is the original, but thanks all Kagglers :)

# In[ ]:


# Cleaning name and extracting Title
for name_string in df_all['Name']:
    df_all['Title'] = df_all['Name'].str.extract('([A-Za-z]+)\.', expand=True)
df_all.head()


# In[ ]:


df_all["Title"].unique()


# In[ ]:


# Replacing rare titles 
mapping = {'Mlle': 'Miss', 'Ms': 'Miss', 'Mme': 'Mrs', 'Major': 'Other', 
           'Col': 'Other', 'Dr' : 'Other', 'Rev' : 'Other', 'Capt': 'Other', 
           'Jonkheer': 'Royal', 'Sir': 'Royal', 'Lady': 'Royal', 
           'Don': 'Royal', 'Countess': 'Royal', 'Dona': 'Royal'}
           
df_all.replace({'Title': mapping}, inplace=True)
#titles = ['Miss', 'Mr', 'Mrs', 'Royal', 'Other', 'Master']


# In[ ]:


titles = df_all["Title"].unique()
titles


# In[ ]:


title_dummies = pd.get_dummies(df_all["Title"], prefix="title", dummy_na=True)
df_all = pd.concat([df_all, title_dummies], axis=1)
df_all.head()


# In[ ]:


df_all['Age'].isnull().sum()


# In[ ]:


df_all["Age"].value_counts().count()


# I found the following to be an interesting way to impute age: group by title, use median age per title. Quite often getting good (accuracy) results is not about fitting the most complex model and ensemble but figuring out the data. Like this trick. Again, this is from the kernel I linked above, not my own magic:

# In[ ]:


titles = list(titles)
# Replacing missing age by median age for title 
for title in titles:
    age_to_impute = df_all.groupby('Title')['Age'].median()[titles.index(title)]
    df_all.loc[(df_all['Age'].isnull()) & (df_all['Title'] == title), 'Age'] = age_to_impute


# In[ ]:


df_all['Age'].isnull().sum()


# In[ ]:


df_all["Age"].value_counts().count()


# Find missing fare values (there is just one..):

# In[ ]:


df_all.groupby('Pclass').agg({'Fare': lambda x: x.isnull().sum()})


# In[ ]:


df_all[df_all["Fare"].isnull()]


# Mr Storey above is from the test set, so *survived* is NaN.

# In[ ]:


df_all.loc[152]


# Index 152 repeats twice, from the train set and from the test set. This is visible in *survival*=0 vs *survival*=NaN. And in *train* = 1 vs *train* = 0. Of course, looking back now, just the *survival*=NaN would have been enough to differentiate the two without needing a custom *train* feature.
# 
# Anyway, there is only one missing fare so just impute with median of their passenger class:

# In[ ]:


p3_median_fare = df_all[df_all["Pclass"] == 3]["Fare"].median()
p3_median_fare


# In[ ]:


df_all["Fare"].fillna(p3_median_fare, inplace=True)


# In[ ]:


df_all.loc[152]


# In[ ]:


#name col seems to be in format "last name, first names". 
#so split by comma and take first item in resulting list should give last name..
df_all['Last_Name'] = df_all['Name'].apply(lambda x: str.split(x, ",")[0])


# *Family survival* is another feature I got from the [kernel](https://www.kaggle.com/vincentlugat/200-lines-randomized-search-lgbm-82-3) I linked above. Another good example of a very clever way to look at the data. Group people into families (or any other group travelling together) by matching their last name and fare. Create a feature to indicate if others in this same group survived or not. This turns out to be a very nice predictor feature, as this same model with similar parameters would always score around max 77% accuracy at one point. Adding this upped the accuracy to over 81%. I suppose they are more likely to move and act together.
# 
# In a way, this feels a little like cheating. If I wanted to figure what features on the ship contributed to survival, for cases where the ship has not sunk yet, this kind of information would not be available. Or you would already know the result, since you know who survived or not. But this is Kaggle, and insights such as these are often what really makes a solution rise in the results. And it shows how to think about the data and relations within it in very clever ways. In other cases it could certainly be much more realistic. Cool!
# 
# I guess in other cases, other information could also be useful, such as shared ticket number, or [subsequent ticket numbers](https://www.kaggle.com/c/titanic/discussion/11127), cabins, etc. Anyway..

# In[ ]:


#this would be the default value if no family member is found
DEFAULT_SURVIVAL_VALUE = 0.5
df_all['Family_Survival'] = DEFAULT_SURVIVAL_VALUE
for grp, grp_df in df_all[['Survived','Name', 'Last_Name', 'Fare', 'Ticket', 'PassengerId',
                           'SibSp', 'Parch', 'Age', 'Cabin']].groupby(['Last_Name', 'Fare']):

    if (len(grp_df) != 1):
        # A Family group is found.
        for ind, row in grp_df.iterrows():
            smax = grp_df.drop(ind)['Survived'].max()
            smin = grp_df.drop(ind)['Survived'].min()
            passID = row['PassengerId']
            if (smax == 1.0):
                df_all.loc[df_all['PassengerId'] == passID, 'Family_Survival'] = 1
            elif (smin == 0.0):
                df_all.loc[df_all['PassengerId'] == passID, 'Family_Survival'] = 0
                
for _, grp_df in df_all.groupby('Ticket'):
    if (len(grp_df) != 1):
        for ind, row in grp_df.iterrows():
            if (row['Family_Survival'] == 0) | (row['Family_Survival']== 0.5):
                smax = grp_df.drop(ind)['Survived'].max()
                smin = grp_df.drop(ind)['Survived'].min()
                passID = row['PassengerId']
                if (smax == 1.0):
                    df_all.loc[df_all['PassengerId'] == passID, 'Family_Survival'] = 1
                elif (smin == 0.0):
                    df_all.loc[df_all['PassengerId'] == passID, 'Family_Survival'] = 0


# Now that all the features are created, lets split the data back to train and test sets:

# In[ ]:


df_train = df_all[df_all["train"] == 1]
df_test = df_all[df_all["train"] == 0]


# Select the features to use for prediction. Drop the ones not useful (used for processing earlier):

# In[ ]:


X_cols = set(df_train.columns)

X_cols -= set(['PassengerId', 'Survived', 'Sex', 'Name', 'Ticket', 'Cabin', 
               'Embarked', 'cabin_type', 'Title', 'train', 'Last_Name'])
X_cols = list(X_cols)
X_cols


# In[ ]:


df_train[X_cols].head()


# Following are some functions from my [Github](https://github.com/mukatee/ml-experiments/tree/master/utils), where I have collected some of the code I try to make more generally useful for the times when I need to run this type of models. 
# 
# The following function does an N-way stratified split of the training data, uses these splits to build a cross-validation set, and performs cross-validation N times with different set combinations.
# 
# Example:
# Split training data to 5 parts. Take 4 parts to train on, 1 part to validate. Change these around so each of the 5 parts is used as validation set once. This gives 5 different models, each trained on 80% of the data. Finally, use each of these 5 models to predict the real test-set. Average the results of all 5 predictions. Other applications would include majority voting etc. Maybe later.

# In[ ]:


from sklearn.model_selection import cross_val_score, StratifiedKFold
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

def stratified_test_prediction_avg_vote(clf, X_train, X_test, y, use_eval_set, n_folds, n_classes, 
                                        fit_params, verbosity):
    folds = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=69)
    #N columns, one per target label. each contains probability of that value
    sub_preds = np.zeros((X_test.shape[0], n_classes))
    oof_preds = np.zeros((X_train.shape[0]))
    score = 0
    acc_score = 0
    acc_score_total = 0
    misclassified_indices = []
    misclassified_expected = []
    misclassified_actual = []
    for i, (train_index, test_index) in enumerate(folds.split(X_train, y)):
        print('-' * 20, i, '-' * 20)

        X_val, y_val = X_train.iloc[test_index], y[test_index]
        if use_eval_set:
            clf.fit(X_train.iloc[train_index], y[train_index], eval_set=([(X_val, y_val)]), verbose=verbosity, **fit_params)
        else:
            #random forest does not know parameter "eval_set" or "verbose"
            clf.fit(X_train.iloc[train_index], y[train_index], **fit_params)
        #could directly do predict() here instead of predict_proba() but then mismatch comparison would not be possible
        oof_preds[test_index] = clf.predict_proba(X_train.iloc[test_index])[:,1].flatten()
        #we predict on whole test set, thus split by n_splits, not n_splits - 1
        sub_preds += clf.predict_proba(X_test) / folds.n_splits
#        sub_preds += clf.predict(X_test) / folds.n_splits
#        score += clf.score(X_train.iloc[test_index], y[test_index])
        preds_this_round = oof_preds[test_index] >= 0.5
        acc_score = accuracy_score(y[test_index], preds_this_round)
        acc_score_total += acc_score
        print('accuracy score ', acc_score)
        if hasattr(clf, 'feature_importances_'):
            importances = clf.feature_importances_
            features = X_train.columns

            feat_importances = pd.Series(importances, index=features)
            feat_importances.nlargest(30).sort_values().plot(kind='barh', color='#86bf91', figsize=(10, 8))
            plt.show()
        else:
            print("classifier has no feature importances: skipping feature plot")

        missed = y[test_index] != preds_this_round
        misclassified_indices.extend(test_index[missed])
        m1 = y[test_index][missed]
        misclassified_expected.append(m1)
        m2 = oof_preds[test_index][missed].astype("int")
        misclassified_actual.append(m2)

    print(f"acc_score: {acc_score}")
    sub_sub = sub_preds[:5]
    print(f"sub_preds: {sub_sub}")
    avg_accuracy = acc_score_total / folds.n_splits
    print('Avg Accuracy', avg_accuracy)
    result = {
        "avg_accuracy": avg_accuracy,
        "misclassified_indices": misclassified_indices,
        "misclassified_samples_expected": misclassified_expected,
        "misclassified_samples_actual": misclassified_actual,
        "oof_predictions": oof_preds,
        "predictions": sub_preds,
    }
    return result


# Just some helper functions:

# In[ ]:


#check if given parameter can be interpreted as a numerical value
def is_number(s):
    if s is None:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False

#convert given set of paramaters to integer values
#this at least cuts the excess float decimals if they are there
def convert_int_params(names, params):
    for int_type in names:
        #sometimes the parameters can be choices between options or numerical values. like "log2" vs "1-10"
        raw_val = params[int_type]
        if is_number(raw_val):
            params[int_type] = int(raw_val)
    return params

#convert float parameters to 3 digit precision strings
#just for simpler diplay and all
def convert_float_params(names, params):
    for float_type in names:
        raw_val = params[float_type]
        if is_number(raw_val):
            params[float_type] = '{:.3f}'.format(raw_val)
    return params


# Run hyperopt for *n_trials* iterations to try different hyperparameter combinations. Each iteration consists of *n_folds* cross-validation splits. So *n_folds*=5 results in splitting to 5 folds, using each at a turn as the validation set and the ohter 4 for training:

# In[ ]:


import numpy as np
from sklearn.model_selection import StratifiedKFold
import lightgbm as lgbm
from hyperopt import hp, tpe, Trials
from hyperopt.fmin import fmin
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import hyperopt

# how many CV folds to do on the data
n_folds = 5
# max number of rows to use for X and y. to reduce time and compare options faster
max_n = None
# max number of trials hyperopt runs
n_trials = 500
#verbosity in LGBM is how often progress is printed. with 100=print progress every 100 rounds. 0 is quite?
verbosity = 0
#if true, print summary accuracy/loss after each round
print_summary = False

from sklearn.metrics import accuracy_score, log_loss

all_accuracies = []
all_losses = []
all_params = []

# run n_folds of cross validation on the data
# averages fold results
def fit_cv(X, y, params, fit_params, n_classes):
    # cut the data if max_n is set
    if max_n is not None:
        X = X[:max_n]
        y = y[:max_n]

    score = 0
    acc_score = 0
    folds = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=69)

    if print_summary:
        print(f"Running {n_folds} folds...")
    oof_preds = np.zeros((X.shape[0], n_classes))
    for i, (train_index, test_index) in enumerate(folds.split(X, y)):
        if verbosity > 0:
            print('-' * 20, f"RUNNING FOLD: {i}/{n_folds}", '-' * 20)

        clf = lgbm.LGBMClassifier(**params)
        X_train, y_train = X.iloc[train_index], y[train_index]
        X_test, y_test = X.iloc[test_index], y[test_index]
        # verbose = print loss at every "verbose" rounds.
        #if 100 it prints progress 100,200,300,... iterations
        clf.fit(X_train, y_train, eval_set=(X_test, y_test), verbose=verbosity, **fit_params)
        oof_preds[test_index] = clf.predict_proba(X.iloc[test_index])
        #score += clf.score(X.iloc[test_index], y[test_index])
        acc_score += accuracy_score(y[test_index], oof_preds[test_index][:,1] >= 0.5)
        # print('score ', clf.score(X.iloc[test_index], y[test_index]))
        importances = clf.feature_importances_
        features = X.columns
    #accuracy is calculated each fold so divide by n_folds.
    #not n_folds -1 because it is not sum by row but overall sum of accuracy of all test indices
    total_acc_score = acc_score / n_folds
    all_accuracies.append(total_acc_score)
    logloss = log_loss(y, oof_preds)
    all_losses.append(logloss)
    all_params.append(params)
    if print_summary:
        print(f"total acc: {total_acc_score}, logloss={logloss}")
    return total_acc_score, logloss

def create_fit_params(params):
    using_dart = params['boosting_type'] == "dart"
    if params["objective"] == "binary":
        # https://github.com/Microsoft/LightGBM/blob/master/docs/Parameters.rst
        fit_params = {"eval_metric": ["binary_logloss", "auc"]}
    else:
        fit_params = {"eval_metric": "multi_logloss"}
    if using_dart:
        n_estimators = 2000
    else:
        n_estimators = 15000
        fit_params["early_stopping_rounds"] = 100
    params["n_estimators"] = n_estimators
    return fit_params


# this is the objective function the hyperopt aims to minimize
# i call it objective_sklearn because the lgbm functions called use sklearn API
def objective_sklearn(params):
    int_types = ["num_leaves", "min_child_samples", "subsample_for_bin", "min_data_in_leaf"]
    params = convert_int_params(int_types, params)

    # Extract the boosting type
    params['boosting_type'] = params['boosting_type']['boosting_type']
    #    print("running with params:"+str(params))

    fit_params = create_fit_params(params)
    if params['objective'] == "binary":
        n_classes = 2
    else:
        n_classes = params["num_class"]

    score, logloss = fit_cv(X, y, params, fit_params, n_classes)
    if verbosity == 0:
        if print_summary:
            print("Score {:.3f}".format(score))
    else:
        print("Score {:.3f} params {}".format(score, params))
    #using logloss here for the loss but uncommenting line below calculates it from average accuracy
#    loss = 1 - score
    loss = logloss
    result = {"loss": loss, "score": score, "params": params, 'status': hyperopt.STATUS_OK}
    return result

def optimize_lgbm(n_classes, max_n_search=None):
    # https://github.com/Microsoft/LightGBM/blob/master/docs/Parameters.rst
    # https://indico.cern.ch/event/617754/contributions/2590694/attachments/1459648/2254154/catboost_for_CMS.pdf
    space = {
        #this is just piling on most of the possible parameter values for LGBM
        #some of them apparently don't make sense together, but works for now.. :)
        'class_weight': hp.choice('class_weight', [None, 'balanced']),
        'boosting_type': hp.choice('boosting_type',
                                   [{'boosting_type': 'gbdt',
#                                     'subsample': hp.uniform('dart_subsample', 0.5, 1)
                                     },
                                    {'boosting_type': 'dart',
#                                     'subsample': hp.uniform('dart_subsample', 0.5, 1)
                                     },
                                    {'boosting_type': 'goss'}]),
        'num_leaves': hp.quniform('num_leaves', 30, 150, 1),
        'learning_rate': hp.loguniform('learning_rate', np.log(0.01), np.log(0.2)),
        'subsample_for_bin': hp.quniform('subsample_for_bin', 20000, 300000, 20000),
        'feature_fraction': hp.uniform('feature_fraction', 0.5, 1),
        'bagging_fraction': hp.uniform('bagging_fraction', 0.5, 1), #alias "subsample"
        'min_data_in_leaf': hp.qloguniform('min_data_in_leaf', 0, 6, 1),
        'lambda_l1': hp.choice('lambda_l1', [0, hp.loguniform('lambda_l1_positive', -16, 2)]),
        'lambda_l2': hp.choice('lambda_l2', [0, hp.loguniform('lambda_l2_positive', -16, 2)]),
        'verbose': -1,
        #the LGBM parameters docs list various aliases, and the LGBM implementation seems to complain about
        #the following not being used due to other params, so trying to silence the complaints by setting to None
        'subsample': None, #overridden by bagging_fraction
        'reg_alpha': None, #overridden by lambda_l1
        'reg_lambda': None, #overridden by lambda_l2
        'min_sum_hessian_in_leaf': None, #overrides min_child_weight
        'min_child_samples': None, #overridden by min_data_in_leaf
        'colsample_bytree': None, #overridden by feature_fraction
#        'min_child_samples': hp.quniform('min_child_samples', 20, 500, 5),
        'min_child_weight': hp.loguniform('min_child_weight', -16, 5), #also aliases to min_sum_hessian
#        'reg_alpha': hp.uniform('reg_alpha', 0.0, 1.0),
#        'reg_lambda': hp.uniform('reg_lambda', 0.0, 1.0),
#        'colsample_bytree': hp.uniform('colsample_by_tree', 0.6, 1.0),
    }
    if n_classes > 2:
        space['objective'] = "multiclass"
        space["num_class"] = n_classes
    else:
        space['objective'] = "binary"
        #space["num_class"] = 1

    global max_n
    max_n = max_n_search
    trials = Trials()
    best = fmin(fn=objective_sklearn,
                space=space,
                algo=tpe.suggest,
                max_evals=n_trials,
                trials=trials,
               verbose= 1)

    # find the trial with lowest loss value. this is what we consider the best one
    idx = np.argmin(trials.losses())
    print(idx)

    print(trials.trials[idx])

    # these should be the training parameters to use to achieve the best score in best trial
    params = trials.trials[idx]["result"]["params"]
    max_n = None

    print(params)
    return params

# run a search for binary classification
def classify_binary(X_cols, df_train, df_test, y_param):
    global X
    global y
    y = y_param
    nrows = max_n

    X = df_train[X_cols]
    X_test = df_test[X_cols]

    # use 2 classes as this is a binary classification
    # the second param is the number of rows to use for training
    params = optimize_lgbm(2, 5000)
    print(params)

    clf = lgbm.LGBMClassifier(**params)

    fit_params = create_fit_params(params)

    search_results = stratified_test_prediction_avg_vote(clf, X, X_test, y, use_eval_set=True,
                                                         n_folds=n_folds, n_classes=2, fit_params=fit_params, verbosity=verbosity)
    predictions = search_results["predictions"]
    oof_predictions = search_results["oof_predictions"]
    avg_accuracy = search_results["avg_accuracy"]
    misclassified_indices = search_results["misclassified_indices"]
    misclassified_samples_expected = search_results["misclassified_samples_expected"]
    misclassified_samples_actual = search_results["misclassified_samples_actual"]

    return predictions, oof_predictions, avg_accuracy, misclassified_indices


# In[ ]:


predictions, oof_predictions, _, misclassified_indices = classify_binary(X_cols, df_train, df_test, y)


# The above shows the parameters found for the best iteration (lowest loss) by hyperopt, as well as a plot of the most important features for each of the 5 folds as given by the LGBM classifier.
# 
# Overall, it seems to consistently rank fare, age, family survival, passenger class, and title of Mr as highest features. I guess higher passenger class meant paying a higher fare, and being located at a higher deck. Or perhaps they were given priority to escape? I am sure more internet searches would help but going with this for now..

# Plotting the accuracy vs loss. Generally when loss goes up, accuracy should go down. The plot changes on runs due to not fixing random seed. But almost always there are spots in the plot where loss goes much higher while accuracy stays up. This would be the case where overall accuracy is good but the error in misclassifications is very high. So expect maybe not to generalize so great on unseen instances, rather like overfitting on this data.

# In[ ]:


df_losses = pd.DataFrame()
df_losses["loss"] = all_losses
df_losses["accuracy"] = all_accuracies
df_losses.plot(figsize=(14,8))


# I would expect to start with higher loss and lower accuracy, going towards overall higher average accuracy and lower loss as hyperopt would focus the search on parameters. Well, actually looking at the pic above it does not seem to make such as huge difference. Maybe the problem/data is not complex enough?

# Anyway, to see differences in parameters vs results, print the iterations with highest loss (so "worst"..):

# In[ ]:


df_losses.sort_values(by="loss", ascending=False).head(10)


# So that should show some with high loss but also relatively high accuracy. Meaning accuracy on some of those looks good but loss shows them to be more generally not that good actually.
# 
# And the ones with highest accuracy:

# In[ ]:


df_losses.sort_values(by="accuracy", ascending=False).head(10)


# The above should show how not always having higher accuracy means having lower loss.
# 
# And the final goal of checking the ordered list of smallest losses (so best iterations according to this metric..):

# In[ ]:


df_losses.sort_values(by="loss", ascending=True).head(10)


# All the lowest loss ones have good accuracy as well. Even if a lower loss is not the highest accuracy in all cases.
# 
# So just to make a submission to try out the leaderboard:

# In[ ]:


ss = pd.read_csv('../input/gender_submission.csv')
# predicting only true values, so take column 1 (0 is false column)
np_preds = np.array(predictions)[: ,1]
ss["Survived"] = np.where(np_preds > 0.5, 1, 0)
ss.to_csv('lgbm.csv', index=False)
ss.head(10)


# Now would be a good time to stop, but we can actually have some more fun by looking at the worst misclassifications. That would be the ones where the model makes the biggest mistakes in predicting high confidence of survivor when not surviving and the other way around.
# 
# First a look at the first few misclassifications:

# In[ ]:


len(misclassified_indices)


# In[ ]:


misclassified_indices[:10]


# In[ ]:


oof_predictions[misclassified_indices][:10]


# In[ ]:


oof_series = pd.Series(oof_predictions[misclassified_indices])
oof_series.index = y[misclassified_indices].index
#oof_series


# Raw diff for the negative/positive difference in prediction vs actual label. Absolute diff to order both types of errors in one set. And the prediction just to illustrate where the diff comes from:

# In[ ]:


miss_scale_raw = y[misclassified_indices] - oof_predictions[misclassified_indices]
miss_scale_abs = abs(miss_scale_raw)
df_miss_scale = pd.concat([miss_scale_raw, miss_scale_abs, oof_series, y[misclassified_indices]], axis=1)
df_miss_scale.columns = ["Raw_Diff", "Abs_Diff", "Prediction", "Actual"]
df_miss_scale.head()


# This should show the ones that were misclassified with highest (false) confidense:

# In[ ]:


df_top_misses = df_miss_scale.sort_values(by="Abs_Diff", ascending=False)
df_top_misses.head()


# A look at the actual records that were most misclassified:

# In[ ]:


top10 = df_top_misses.iloc[0:10].index
top10


# In[ ]:


df_train.iloc[top10]


# The list above might change a bit over different runs, so not going to list specific entries there. But as I look at it now, I see a few small children there (age 2-4 or so), some of which had a family member survice, and so on. I guess many of these are actual, reasonable misclassifications, where not every small baby or man in their best of years and health could survive due to many circumstances (e.g., location/state during accident, personal actions, etc.).
# 
# This could use a bit more exploration to see what percentages of men, babies, etc. survived and if there is some explanatory factor to play still.

# What about the ones that were misclassified with the smallest margin?

# In[ ]:


df_bottom_misses = df_miss_scale.sort_values(by="Abs_Diff", ascending=True)
df_bottom_misses.head()


# Since the threshold is 0.5, these are very close to the border of that.

# In[ ]:


bottom10 = df_bottom_misses.iloc[0:10].index
bottom10


# What do these look like?

# In[ ]:


df_train.iloc[bottom10]


# In[ ]:





# In[ ]:




