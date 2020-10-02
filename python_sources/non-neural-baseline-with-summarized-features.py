#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# for hyper parameter search
get_ipython().system('pip install optuna')


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


import pyarrow.parquet as pq


# In[ ]:


from pathlib import Path


# In[ ]:


class DataPaths(object):
    TRAIN_PARQUET_PATH = Path('../input/train.parquet')
    TRAIN_METADATA_PATH = Path('../input/metadata_train.csv')
    TEST_PARQUET_PATH = Path('../input/test.parquet')
    TEST_MATADATA_PATH = Path('../input/metadata_test.csv')


# In[ ]:


train_meta_df = pd.read_csv('../input/metadata_train.csv')


# In[ ]:


train_meta_df[:10]


# In[ ]:


# for debug
# train_meta_df = train_meta_df.iloc[:600]


# In[ ]:


train_meta_df.info()


# In[ ]:


train_meta_df.describe()


# 

# # feature extraction

# In[ ]:


from scipy import signal


# In[ ]:


import pywt


# In[ ]:


WAVELET_WIDTH = 30


# In[ ]:


from sklearn.preprocessing import FunctionTransformer


# In[ ]:


subset_train = pq


# In[ ]:


class SummaryTransformer(FunctionTransformer):
    def __init__(self, 
                 kw_args=None, inv_kw_args=None):
        validate = False
        inverse_func = None
        accept_sparse = False
        pass_y = 'deprecated'
        super().__init__(self.f, inverse_func, validate, accept_sparse, pass_y, kw_args, inv_kw_args)
    
    def f(self, X):
        avgs = np.mean(X)
        stds = np.std(X)
        maxs = np.max(X)
        mins = np.min(X)
        medians = np.median(X)
        return np.array([avgs, stds, maxs, mins, medians])


# In[ ]:


class WaevletSummaryTransformer(FunctionTransformer):
    def __init__(self, wavelet_width,
                 kw_args=None, inv_kw_args=None):
        validate = False
        inverse_func = None
        accept_sparse = False
        pass_y = 'deprecated'
        self.wavelet_width = wavelet_width
        super().__init__(self.f, inverse_func, validate, accept_sparse, pass_y, kw_args, inv_kw_args)
    
    def f(self, X):
#         wavelets = signal.cwt(X, signal.ricker, np.arange(1, self.wavelet_width + 1))
        wavelets, _ = pywt.cwt(X, np.arange(1, self.wavelet_width + 1), 'mexh')
        avgs = np.mean(wavelets, axis=1)
        stds = np.std(wavelets, axis=1)
        maxs = np.max(wavelets, axis=1)
        mins = np.min(wavelets, axis=1)
        medians = np.median(wavelets, axis=1)
        return np.concatenate([avgs, stds, maxs, mins, medians])


# In[ ]:


class SpectrogramSummaryTransformer(FunctionTransformer):
    def __init__(self, sample_rate, fft_length, stride_length,
                 kw_args=None, inv_kw_args=None):
        validate = False
        inverse_func = None
        accept_sparse = False
        pass_y = 'deprecated'
        self.sample_rate = sample_rate
        self.fft_length = fft_length
        self.stride_length = stride_length
        super().__init__(self.f, inverse_func, validate, accept_sparse, pass_y, kw_args, inv_kw_args)
    
    def f(self, X):
        X = self.to_spectrogram(X)
        avgs = np.mean(X, axis=1)
        stds = np.std(X, axis=1)
        maxs = np.max(X, axis=1)
        mins = np.min(X, axis=1)
        medians = np.median(X, axis=1)
        return np.concatenate([avgs, stds, maxs, mins, medians])

    def to_spectrogram(self, series):
        f, t, Sxx = signal.spectrogram(series, fs=self.sample_rate, nperseg=self.fft_length,
                                   noverlap=self.fft_length - self.stride_length, window="hanning", axis=0,
                                   return_onesided=True, mode="magnitude", scaling="density")
        return Sxx


# In[ ]:


from typing import List


# In[ ]:


from sklearn.base import TransformerMixin


# In[ ]:


train_meta_df.columns


# In[ ]:


def read_column(parquet_path, column_id):
    return pq.read_pandas(parquet_path, columns=[str(column_id)]).to_pandas()[str(column_id)]


# In[ ]:


import itertools


# In[ ]:


from tqdm import tqdm_notebook


# In[ ]:


from multiprocessing.pool import Pool


# In[ ]:


class FeatureExtractor(object):
    def __init__(self, transformers):
        self.transformers: List[TransformerMixin] = transformers
        self._parquet_path = None
        self._meta_df = None
    
    def fit(self, parquet_path, meta_df):
        pass
    
    def from_signal(self, parquet_path, signal_id):
        return [ transformer.transform(read_column(parquet_path, signal_id).values)  
                                          for transformer in self.transformers]
    
    def from_measurement(self, measure_id):
        temp = np.concatenate(
            list(itertools.chain.from_iterable(
                [ self.from_signal(self._parquet_path, signal_id) for signal_id 
                 in self._meta_df[self._meta_df["id_measurement"] == measure_id].signal_id
                ]
            ))
        )
        return temp
    
    def transform(self, parquet_path, meta_df, n_jobs=2):
        self._parquet_path = parquet_path
        self._meta_df = meta_df
        with Pool(n_jobs) as pool:
            rows = pool.map(self.from_measurement, self._meta_df.id_measurement.unique())
        return np.vstack(rows)


# In[ ]:


N_MEASUREMENTS = 800000


# In[ ]:


TOTAL_DURATION = 20e-3


# In[ ]:


sample_rate = N_MEASUREMENTS / TOTAL_DURATION


# In[ ]:


# wavelet transform takes too much time
# extractor = FeatureExtractor([SummaryTransformer(), WaevletSummaryTransformer(WAVELET_WIDTH), SpectrogramSummaryTransformer(
#     sample_rate= sample_rate, fft_length=200, stride_length=100)])


# In[ ]:


extractor = FeatureExtractor([SummaryTransformer(), SpectrogramSummaryTransformer(
    sample_rate= sample_rate, fft_length=200, stride_length=100)])


# In[ ]:


X = extractor.transform(DataPaths.TRAIN_PARQUET_PATH, train_meta_df, n_jobs=4)


# In[ ]:


X.shape


# ## train model

# In[ ]:


from sklearn.metrics import matthews_corrcoef


# In[ ]:


from lightgbm import LGBMClassifier


# In[ ]:


import optuna


# In[ ]:


y = train_meta_df.target[list(range(train_meta_df.signal_id.values[0], 
                                        train_meta_df.signal_id.values[-1], 3))]


# In[ ]:


RANDOM_STATE=10


# In[ ]:


from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer


# In[ ]:


def objective(trial:optuna.trial.Trial):
    boosting_type = trial.suggest_categorical("boosting_type", ['gbdt', 'dart'])
    num_leaves = trial.suggest_int('num_leaves', 30, 80)
    min_data_in_leaf = trial.suggest_int('min_data_in_leaf', 10, 100)
#     max_depth = trial.suggest_int('max_depth', )
    lambda_l1 = trial.suggest_loguniform('lambda_l1', 1e-5, 1e-2)
    lambda_l2 = trial.suggest_loguniform('lambda_l2', 1e-5, 1e-2)
#     num_iterations = trial.suggest_int("num_iterations", 100, 500)
    learning_rate = trial.suggest_loguniform('learning_rate', 1e-4, 1e-1)
    
    clf = LGBMClassifier(boosting_type=boosting_type, num_leaves=num_leaves, 
                        learning_rate=learning_rate, reg_alpha=lambda_l1, 
                        min_child_samples=min_data_in_leaf,
                         reg_lambda=lambda_l2, random_state=RANDOM_STATE)
#     fit_params = {"early_stopping_rounds":20, 
#                  "eval_metric": matthews_corrcoef}
    scores = cross_validate(clf, X, y, verbose=1,  
                  n_jobs=-1, scoring=make_scorer(matthews_corrcoef), cv=5)
    return - scores["test_score"].mean()
    


# In[ ]:


study = optuna.create_study()


# In[ ]:


study.optimize(objective, n_trials=10)


# In[ ]:


study.best_params


# In[ ]:


study.best_value


# In[ ]:


best_params = study.best_params


# In[ ]:


best_params["random_state"] = RANDOM_STATE


# In[ ]:


clf = LGBMClassifier(**best_params)


# In[ ]:


clf.fit(X, y, eval_metric=matthews_corrcoef, 
       verbose=1)


# ## predict

# In[ ]:


test_meta_df = pd.read_csv(DataPaths.TEST_MATADATA_PATH)


# In[ ]:


# test_meta_df = test_meta_df.iloc[:15]


# In[ ]:


test_meta_df.shape


# In[ ]:


X = extractor.transform(DataPaths.TEST_PARQUET_PATH, test_meta_df, n_jobs=4)


# In[ ]:


predictions = clf.predict(X)


# In[ ]:


submit_df = pd.DataFrame()


# In[ ]:


submit_df["signal_id"] = test_meta_df.signal_id


# In[ ]:


submit_df["target"] = np.repeat(predictions, 3)


# In[ ]:


submit_df[:10]


# In[ ]:


submit_df.to_csv("submission.csv", index=None)


# In[ ]:




