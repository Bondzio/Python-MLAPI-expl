#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


import json

import scipy as sp
import pandas as pd
import numpy as np

from functools import partial
from math import sqrt

from sklearn.metrics import cohen_kappa_score, mean_squared_error
from sklearn.metrics import confusion_matrix as sk_cmatrix
from sklearn.model_selection import StratifiedKFold

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

from collections import Counter

import lightgbm as lgb


# In[ ]:


# The following 3 functions have been taken from Ben Hamner's github repository
# https://github.com/benhamner/Metrics
def confusion_matrix(rater_a, rater_b, min_rating=None, max_rating=None):
    """
    Returns the confusion matrix between rater's ratings
    """
    assert(len(rater_a) == len(rater_b))
    if min_rating is None:
        min_rating = min(rater_a + rater_b)
    if max_rating is None:
        max_rating = max(rater_a + rater_b)
    num_ratings = int(max_rating - min_rating + 1)
    conf_mat = [[0 for i in range(num_ratings)]
                for j in range(num_ratings)]
    for a, b in zip(rater_a, rater_b):
        conf_mat[a - min_rating][b - min_rating] += 1
    return conf_mat


def histogram(ratings, min_rating=None, max_rating=None):
    """
    Returns the counts of each type of rating that a rater made
    """
    if min_rating is None:
        min_rating = min(ratings)
    if max_rating is None:
        max_rating = max(ratings)
    num_ratings = int(max_rating - min_rating + 1)
    hist_ratings = [0 for x in range(num_ratings)]
    for r in ratings:
        hist_ratings[r - min_rating] += 1
    return hist_ratings


def quadratic_weighted_kappa(y, y_pred):
    """
    Calculates the quadratic weighted kappa
    axquadratic_weighted_kappa calculates the quadratic weighted kappa
    value, which is a measure of inter-rater agreement between two raters
    that provide discrete numeric ratings.  Potential values range from -1
    (representing complete disagreement) to 1 (representing complete
    agreement).  A kappa value of 0 is expected if all agreement is due to
    chance.
    quadratic_weighted_kappa(rater_a, rater_b), where rater_a and rater_b
    each correspond to a list of integer ratings.  These lists must have the
    same length.
    The ratings should be integers, and it is assumed that they contain
    the complete range of possible ratings.
    quadratic_weighted_kappa(X, min_rating, max_rating), where min_rating
    is the minimum possible rating, and max_rating is the maximum possible
    rating
    """
    rater_a = y
    rater_b = y_pred
    min_rating=None
    max_rating=None
    rater_a = np.array(rater_a, dtype=int)
    rater_b = np.array(rater_b, dtype=int)
    assert(len(rater_a) == len(rater_b))
    if min_rating is None:
        min_rating = min(min(rater_a), min(rater_b))
    if max_rating is None:
        max_rating = max(max(rater_a), max(rater_b))
    conf_mat = confusion_matrix(rater_a, rater_b,
                                min_rating, max_rating)
    num_ratings = len(conf_mat)
    num_scored_items = float(len(rater_a))

    hist_rater_a = histogram(rater_a, min_rating, max_rating)
    hist_rater_b = histogram(rater_b, min_rating, max_rating)

    numerator = 0.0
    denominator = 0.0

    for i in range(num_ratings):
        for j in range(num_ratings):
            expected_count = (hist_rater_a[i] * hist_rater_b[j]
                              / num_scored_items)
            d = pow(i - j, 2.0) / pow(num_ratings - 1, 2.0)
            numerator += d * conf_mat[i][j] / num_scored_items
            denominator += d * expected_count / num_scored_items

    return (1.0 - numerator / denominator)


# In[ ]:


class OptimizedRounder(object):
    def __init__(self):
        self.coef_ = 0

    def _kappa_loss(self, coef, X, y):
        X_p = np.copy(X)
        for i, pred in enumerate(X_p):
            if pred < coef[0]:
                X_p[i] = 0
            elif pred >= coef[0] and pred < coef[1]:
                X_p[i] = 1
            elif pred >= coef[1] and pred < coef[2]:
                X_p[i] = 2
            elif pred >= coef[2] and pred < coef[3]:
                X_p[i] = 3
            else:
                X_p[i] = 4

        ll = quadratic_weighted_kappa(y, X_p)
        return -ll

    def fit(self, X, y):
        loss_partial = partial(self._kappa_loss, X=X, y=y)
        initial_coef = [0.5, 1.5, 2.5, 3.5]
        self.coef_ = sp.optimize.minimize(loss_partial, initial_coef, method='nelder-mead')

    def predict(self, X, coef):
        X_p = np.copy(X)
        for i, pred in enumerate(X_p):
            if pred < coef[0]:
                X_p[i] = 0
            elif pred >= coef[0] and pred < coef[1]:
                X_p[i] = 1
            elif pred >= coef[1] and pred < coef[2]:
                X_p[i] = 2
            elif pred >= coef[2] and pred < coef[3]:
                X_p[i] = 3
            else:
                X_p[i] = 4
        return X_p

    def coefficients(self):
        return self.coef_['x']


# In[ ]:


def rmse(actual, predicted):
    return sqrt(mean_squared_error(actual, predicted))


# In[ ]:


get_ipython().run_cell_magic('time', '', 'print(\'Train\')\ntrain = pd.read_csv("../input/train/train.csv")\nprint(train.shape)\n\nprint(\'Test\')\ntest = pd.read_csv("../input/test/test.csv")\nprint(test.shape)\n\nprint(\'Breeds\')\nbreeds = pd.read_csv("../input/breed_labels.csv")\nprint(breeds.shape)\n\nprint(\'Colors\')\ncolors = pd.read_csv("../input/color_labels.csv")\nprint(colors.shape)\n\nprint(\'States\')\nstates = pd.read_csv("../input/state_labels.csv")\nprint(states.shape)')


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


breeds.head()


# In[ ]:


colors.head()


# In[ ]:


states.head()


# In[ ]:


target = train['AdoptionSpeed']
train_id = train['PetID']
test_id = test['PetID']
train.drop(['AdoptionSpeed', 'PetID'], axis=1, inplace=True)
test.drop(['PetID'], axis=1, inplace=True)


# In[ ]:


get_ipython().run_cell_magic('time', '', "doc_sent_mag = []\ndoc_sent_score = []\nnf_count = 0\nfor pet in train_id:\n    try:\n        with open('../input/train_sentiment/' + pet + '.json', 'r') as f:\n            sentiment = json.load(f)\n        doc_sent_mag.append(sentiment['documentSentiment']['magnitude'])\n        doc_sent_score.append(sentiment['documentSentiment']['score'])\n    except FileNotFoundError:\n        nf_count += 1\n        doc_sent_mag.append(-1)\n        doc_sent_score.append(-1)\n\ntrain.loc[:, 'doc_sent_mag'] = doc_sent_mag\ntrain.loc[:, 'doc_sent_score'] = doc_sent_score\n\ndoc_sent_mag = []\ndoc_sent_score = []\nnf_count = 0\nfor pet in test_id:\n    try:\n        with open('../input/test_sentiment/' + pet + '.json', 'r') as f:\n            sentiment = json.load(f)\n        doc_sent_mag.append(sentiment['documentSentiment']['magnitude'])\n        doc_sent_score.append(sentiment['documentSentiment']['score'])\n    except FileNotFoundError:\n        nf_count += 1\n        doc_sent_mag.append(-1)\n        doc_sent_score.append(-1)\n\ntest.loc[:, 'doc_sent_mag'] = doc_sent_mag\ntest.loc[:, 'doc_sent_score'] = doc_sent_score")


# In[ ]:


get_ipython().run_cell_magic('time', '', 'train_desc = train.Description.fillna("none").values\ntest_desc = test.Description.fillna("none").values\n\ntfv = TfidfVectorizer(min_df=3,  max_features=10000,\n        strip_accents=\'unicode\', analyzer=\'word\', token_pattern=r\'\\w{1,}\',\n        ngram_range=(1, 3), use_idf=1, smooth_idf=1, sublinear_tf=1,\n        stop_words = \'english\')\n    \n# Fit TFIDF\ntfv.fit(list(train_desc))\nX =  tfv.transform(train_desc)\nX_test = tfv.transform(test_desc)\n\nsvd = TruncatedSVD(n_components=120)\nsvd.fit(X)\nprint(svd.explained_variance_ratio_.sum())\nprint(svd.explained_variance_ratio_)\nX = svd.transform(X)\nX = pd.DataFrame(X, columns=[\'svd_{}\'.format(i) for i in range(120)])\ntrain = pd.concat((train, X), axis=1)\nX_test = svd.transform(X_test)\nX_test = pd.DataFrame(X_test, columns=[\'svd_{}\'.format(i) for i in range(120)])\ntest = pd.concat((test, X_test), axis=1)')


# In[ ]:


get_ipython().run_cell_magic('time', '', "vertex_xs = []\nvertex_ys = []\nbounding_confidences = []\nbounding_importance_fracs = []\ndominant_blues = []\ndominant_greens = []\ndominant_reds = []\ndominant_pixel_fracs = []\ndominant_scores = []\nlabel_descriptions = []\nlabel_scores = []\nnf_count = 0\nnl_count = 0\nfor pet in train_id:\n    try:\n        with open('../input/train_metadata/' + pet + '-1.json', 'r') as f:\n            data = json.load(f)\n        vertex_x = data['cropHintsAnnotation']['cropHints'][0]['boundingPoly']['vertices'][2]['x']\n        vertex_xs.append(vertex_x)\n        vertex_y = data['cropHintsAnnotation']['cropHints'][0]['boundingPoly']['vertices'][2]['y']\n        vertex_ys.append(vertex_y)\n        bounding_confidence = data['cropHintsAnnotation']['cropHints'][0]['confidence']\n        bounding_confidences.append(bounding_confidence)\n        bounding_importance_frac = data['cropHintsAnnotation']['cropHints'][0].get('importanceFraction', -1)\n        bounding_importance_fracs.append(bounding_importance_frac)\n        dominant_blue = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['color']['blue']\n        dominant_blues.append(dominant_blue)\n        dominant_green = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['color']['green']\n        dominant_greens.append(dominant_green)\n        dominant_red = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['color']['red']\n        dominant_reds.append(dominant_red)\n        dominant_pixel_frac = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['pixelFraction']\n        dominant_pixel_fracs.append(dominant_pixel_frac)\n        dominant_score = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['score']\n        dominant_scores.append(dominant_score)\n        if data.get('labelAnnotations'):\n            label_description = data['labelAnnotations'][0]['description']\n            label_descriptions.append(label_description)\n            label_score = data['labelAnnotations'][0]['score']\n            label_scores.append(label_score)\n        else:\n            nl_count += 1\n            label_descriptions.append('nothing')\n            label_scores.append(-1)\n    except FileNotFoundError:\n        nf_count += 1\n        vertex_xs.append(-1)\n        vertex_ys.append(-1)\n        bounding_confidences.append(-1)\n        bounding_importance_fracs.append(-1)\n        dominant_blues.append(-1)\n        dominant_greens.append(-1)\n        dominant_reds.append(-1)\n        dominant_pixel_fracs.append(-1)\n        dominant_scores.append(-1)\n        label_descriptions.append('nothing')\n        label_scores.append(-1)\n\nprint(nf_count)\nprint(nl_count)\ntrain.loc[:, 'vertex_x'] = vertex_xs\ntrain.loc[:, 'vertex_y'] = vertex_ys\ntrain.loc[:, 'bounding_confidence'] = bounding_confidences\ntrain.loc[:, 'bounding_importance'] = bounding_importance_fracs\ntrain.loc[:, 'dominant_blue'] = dominant_blues\ntrain.loc[:, 'dominant_green'] = dominant_greens\ntrain.loc[:, 'dominant_red'] = dominant_reds\ntrain.loc[:, 'dominant_pixel_frac'] = dominant_pixel_fracs\ntrain.loc[:, 'dominant_score'] = dominant_scores\ntrain.loc[:, 'label_description'] = label_descriptions\ntrain.loc[:, 'label_score'] = label_scores\n\n\nvertex_xs = []\nvertex_ys = []\nbounding_confidences = []\nbounding_importance_fracs = []\ndominant_blues = []\ndominant_greens = []\ndominant_reds = []\ndominant_pixel_fracs = []\ndominant_scores = []\nlabel_descriptions = []\nlabel_scores = []\nnf_count = 0\nnl_count = 0\nfor pet in test_id:\n    try:\n        with open('../input/test_metadata/' + pet + '-1.json', 'r') as f:\n            data = json.load(f)\n        vertex_x = data['cropHintsAnnotation']['cropHints'][0]['boundingPoly']['vertices'][2]['x']\n        vertex_xs.append(vertex_x)\n        vertex_y = data['cropHintsAnnotation']['cropHints'][0]['boundingPoly']['vertices'][2]['y']\n        vertex_ys.append(vertex_y)\n        bounding_confidence = data['cropHintsAnnotation']['cropHints'][0]['confidence']\n        bounding_confidences.append(bounding_confidence)\n        bounding_importance_frac = data['cropHintsAnnotation']['cropHints'][0].get('importanceFraction', -1)\n        bounding_importance_fracs.append(bounding_importance_frac)\n        dominant_blue = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['color']['blue']\n        dominant_blues.append(dominant_blue)\n        dominant_green = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['color']['green']\n        dominant_greens.append(dominant_green)\n        dominant_red = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['color']['red']\n        dominant_reds.append(dominant_red)\n        dominant_pixel_frac = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['pixelFraction']\n        dominant_pixel_fracs.append(dominant_pixel_frac)\n        dominant_score = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['score']\n        dominant_scores.append(dominant_score)\n        if data.get('labelAnnotations'):\n            label_description = data['labelAnnotations'][0]['description']\n            label_descriptions.append(label_description)\n            label_score = data['labelAnnotations'][0]['score']\n            label_scores.append(label_score)\n        else:\n            nl_count += 1\n            label_descriptions.append('nothing')\n            label_scores.append(-1)\n    except FileNotFoundError:\n        nf_count += 1\n        vertex_xs.append(-1)\n        vertex_ys.append(-1)\n        bounding_confidences.append(-1)\n        bounding_importance_fracs.append(-1)\n        dominant_blues.append(-1)\n        dominant_greens.append(-1)\n        dominant_reds.append(-1)\n        dominant_pixel_fracs.append(-1)\n        dominant_scores.append(-1)\n        label_descriptions.append('nothing')\n        label_scores.append(-1)\n\nprint(nf_count)\ntest.loc[:, 'vertex_x'] = vertex_xs\ntest.loc[:, 'vertex_y'] = vertex_ys\ntest.loc[:, 'bounding_confidence'] = bounding_confidences\ntest.loc[:, 'bounding_importance'] = bounding_importance_fracs\ntest.loc[:, 'dominant_blue'] = dominant_blues\ntest.loc[:, 'dominant_green'] = dominant_greens\ntest.loc[:, 'dominant_red'] = dominant_reds\ntest.loc[:, 'dominant_pixel_frac'] = dominant_pixel_fracs\ntest.loc[:, 'dominant_score'] = dominant_scores\ntest.loc[:, 'label_description'] = label_descriptions\ntest.loc[:, 'label_score'] = label_scores")


# In[ ]:


train.head()


# In[ ]:


get_ipython().run_cell_magic('time', '', "train.drop(['Name', 'RescuerID', 'Description'], axis=1, inplace=True)\ntest.drop(['Name', 'RescuerID', 'Description'], axis=1, inplace=True)")


# In[ ]:


numeric_cols = ['Age', 'Quantity', 'Fee', 'VideoAmt', 'PhotoAmt', 'AdoptionSpeed', 'doc_sent_mag', 'doc_sent_score', 'dominant_score', 'dominant_pixel_frac', 'dominant_red', 'dominant_green', 'dominant_blue', 'bounding_importance', 'bounding_confidence', 'vertex_x', 'vertex_y', 'label_score'] + ['svd_{}'.format(i) for i in range(120)]
cat_cols = list(set(train.columns) - set(numeric_cols))
train.loc[:, cat_cols] = train[cat_cols].astype('category')
test.loc[:, cat_cols] = test[cat_cols].astype('category')
print(train.shape)
print(test.shape)
train.head()


# In[ ]:


def run_cv_model(train, test, target, model_fn, params={}, eval_fn=None, label='model'):
    kf = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
    fold_splits = kf.split(train, target)
    cv_scores = []
    qwk_scores = []
    pred_full_test = 0
    pred_train = np.zeros((train.shape[0], 5))
    all_coefficients = np.zeros((5, 4))
    feature_importance_df = pd.DataFrame()
    i = 1
    for dev_index, val_index in fold_splits:
        print('Started ' + label + ' fold ' + str(i) + '/5')
        if isinstance(train, pd.DataFrame):
            dev_X, val_X = train.iloc[dev_index], train.iloc[val_index]
            dev_y, val_y = target[dev_index], target[val_index]
        else:
            dev_X, val_X = train[dev_index], train[val_index]
            dev_y, val_y = target[dev_index], target[val_index]
        params2 = params.copy()
        pred_val_y, pred_test_y, importances, coefficients, qwk = model_fn(dev_X, dev_y, val_X, val_y, test, params2)
        pred_full_test = pred_full_test + pred_test_y
        pred_train[val_index] = pred_val_y
        all_coefficients[i-1, :] = coefficients
        if eval_fn is not None:
            cv_score = eval_fn(val_y, pred_val_y)
            cv_scores.append(cv_score)
            qwk_scores.append(qwk)
            print(label + ' cv score {}: RMSE {} QWK {}'.format(i, cv_score, qwk))
        fold_importance_df = pd.DataFrame()
        fold_importance_df['feature'] = train.columns.values
        fold_importance_df['importance'] = importances
        fold_importance_df['fold'] = i
        feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)        
        i += 1
    print('{} cv RMSE scores : {}'.format(label, cv_scores))
    print('{} cv mean RMSE score : {}'.format(label, np.mean(cv_scores)))
    print('{} cv std RMSE score : {}'.format(label, np.mean(cv_scores)))
    print('{} cv QWK scores : {}'.format(label, qwk_scores))
    print('{} cv mean QWK score : {}'.format(label, np.mean(qwk_scores)))
    print('{} cv std QWK score : {}'.format(label, np.std(qwk_scores)))
    pred_full_test = pred_full_test / 5.0
    results = {'label': label,
               'train': pred_train, 'test': pred_full_test,
                'cv': cv_scores, 'qwk': qwk_scores,
               'importance': feature_importance_df,
               'coefficients': all_coefficients}
    return results

params = {'application': 'regression',
          'boosting': 'gbdt',
          'metric': 'rmse',
          'num_leaves': 80,
          'max_depth': 11,
          'learning_rate': 0.01,
          'bagging_fraction': 0.9,
          'feature_fraction': 0.8,
          'min_split_gain': 0.01,
          'min_child_samples': 150,
          'min_child_weight': 0.1,
          'verbosity': -1,
          'data_random_seed': 3,
          'early_stop': 100,
          'verbose_eval': 100,
          'num_rounds': 10000}

def runLGB(train_X, train_y, test_X, test_y, test_X2, params):
    print('Prep LGB')
    d_train = lgb.Dataset(train_X, label=train_y)
    d_valid = lgb.Dataset(test_X, label=test_y)
    watchlist = [d_train, d_valid]
    print('Train LGB')
    num_rounds = params.pop('num_rounds')
    verbose_eval = params.pop('verbose_eval')
    early_stop = None
    if params.get('early_stop'):
        early_stop = params.pop('early_stop')
    model = lgb.train(params,
                      train_set=d_train,
                      num_boost_round=num_rounds,
                      valid_sets=watchlist,
                      verbose_eval=verbose_eval,
                      early_stopping_rounds=early_stop)
    print('Predict 1/2')
    pred_test_y = model.predict(test_X, num_iteration=model.best_iteration)
    optR = OptimizedRounder()
    optR.fit(pred_test_y, test_y)
    coefficients = optR.coefficients()
    pred_test_y_k = optR.predict(pred_test_y, coefficients)
    print("Valid Counts = ", Counter(test_y))
    print("Predicted Counts = ", Counter(pred_test_y_k))
    print("Coefficients = ", coefficients)
    qwk = quadratic_weighted_kappa(test_y, pred_test_y_k)
    print("QWK = ", qwk)
    print('Predict 2/2')
    pred_test_y2 = model.predict(test_X2, num_iteration=model.best_iteration)
    return pred_test_y.reshape(-1, 1), pred_test_y2.reshape(-1, 1), model.feature_importance(), coefficients, qwk

results = run_cv_model(train, test, target, runLGB, params, rmse, 'lgb')


# In[ ]:


imports = results['importance'].groupby('feature')['feature', 'importance'].mean().reset_index()
imports.sort_values('importance', ascending=False)


# In[ ]:


optR = OptimizedRounder()
coefficients_ = np.mean(results['coefficients'], axis=0)
print(coefficients_)
train_predictions = [r[0] for r in results['train']]
train_predictions = optR.predict(train_predictions, coefficients_).astype(int)
Counter(train_predictions)


# In[ ]:


optR = OptimizedRounder()
test_predictions = [r[0] for r in results['test']]
test_predictions = optR.predict(test_predictions, coefficients_).astype(int)
Counter(test_predictions)


# In[ ]:


pd.DataFrame(sk_cmatrix(target, train_predictions), index=list(range(5)), columns=list(range(5)))


# In[ ]:


quadratic_weighted_kappa(target, train_predictions)


# In[ ]:


rmse(target, [r[0] for r in results['train']])


# In[ ]:


submission = pd.DataFrame({'PetID': test_id, 'AdoptionSpeed': test_predictions})
submission.head()


# In[ ]:


submission.to_csv('submission.csv', index=False)


# In[ ]:




