#!/usr/bin/env python
# coding: utf-8

# <h1><center><font size="6">LANL Earthquake EDA and Ensemble Prediction</font></center></h1>
# 
# <h2><center><font size="4">Dataset used: LANL Earthquake Prediction</font></center></h2>
# 
# <img src="https://storage.googleapis.com/kaggle-media/competitions/LANL/nik-shuliahin-585307-unsplash.jpg" width="600"></img>
# 
# <br>
# 
# # <a id='0'>Content</a>
# 
# - <a href='#1'>Introduction</a>  
# - <a href='#2'>Prepare the data analysis</a>  
# - <a href='#3'>Data exploration</a>   
# - <a href='#4'>Feature engineering</a>
# - <a href='#5'>Model</a>
# - <a href='#6'>Submission</a>  
# - <a href='#7'>References</a>

# # <a id='1'>Introduction</a>  
# 
# My goal with this kernel is to have an end-to-end model which encorporates:
# 
# * Extensible feature engineering
# * Ability to try and measure many regression models
# * Fexlibility of both a blended and stacked model production to produce testable ensemble models
# 
# This kernel is based on a fork from Gabriel Preda's excellent kernel, 'LANLEarthquake EDA and Prediction." I have left most of his EDA and feature engineering in place, while adding a few features of my own. The modeling portion is based partially on his models. In addition, I use ensembling approaches from Serigne's excellent model in the House Price Advanced Regression Techniques competition, https://www.kaggle.com/serigne/stacked-regressions-top-4-on-leaderboard.
# 
# This model produces 1.488 leader board entry with the averaged model, using RF, lgb, cat, and lasso.
# 
# 
# ## Simulated earthquake experiment
# 
# This introduction is from Gabrial Prada's kernel:
# 
# "The data are from an experiment conducted on rock in a double direct shear geometry subjected to bi-axial loading, a classic laboratory earthquake model.
# 
# Two fault gouge layers are sheared simultaneously while subjected to a constant normal load and a prescribed shear velocity. The laboratory faults fail in repetitive cycles of stick and slip that is meant to mimic the cycle of loading and failure on tectonic faults. While the experiment is considerably simpler than a fault in Earth, it shares many physical characteristics. 
# 
# Los Alamos' initial work showed that the prediction of laboratory earthquakes from continuous seismic data is possible in the case of quasi-periodic laboratory seismic cycles."   
# 
# ## Competition 
# 
# In this competition, the team has provided a much more challenging dataset with considerably more aperiodic earthquake failures.  
# Objective of the competition is to predict the failures for each test set.  
# 
# ## Kernel
# 
# This solution is based on a fork from Gabriel Preda's excellent kernel, 'LANLEarthquake EDA and Prediction." His solution uses  Andrew's Data Munging plus some inspiration from Scirpus's [Kernel](https://www.kaggle.com/scirpus/andrews-script-plus-a-genetic-program-model/).
# 
# It also includes the elegant stacking model from Serigne's regression model (see reference above.)
# 
# This kernel extends the existing model by
# 
# * normalizing the values to a mean of zero
# * using log values to remove outliers
# * removal of segments in training which contain the quake
# * additional prediction models
# * combining results from multiple models through various ensemble techniques
# 
# 

# # <a id='1'>Prepare the data analysis</a>
# 
# ## Load packages
# 
# Here we define the packages for data manipulation, feature engineering and model training.

# In[ ]:


import gc
import os
import time
import logging
import datetime
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import xgboost as xgb
import lightgbm as lgb
from scipy import stats
from scipy.signal import hann
from tqdm import tqdm_notebook
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from scipy.signal import convolve
from sklearn.svm import NuSVR, SVR
from catboost import CatBoostRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.linear_model import ElasticNet, Lasso,  BayesianRidge, LassoLarsIC
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor,  GradientBoostingRegressor
from sklearn.model_selection import KFold,StratifiedKFold, RepeatedKFold
from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone


warnings.filterwarnings("ignore")


# ## Load the data
# 
# Let's see first what files we have in input directory.

# In[ ]:





# In[ ]:


IS_LOCAL = False
if(IS_LOCAL):
    PATH="../input/LANL/"
else:
    PATH="../input/"
os.listdir(PATH)


# We have two files in the **input** directory and another directory, with the **test** data.  
# 
# Let's see how many files are in **test** folder.

# In[ ]:


print("There are {} files in test folder".format(len(os.listdir(os.path.join(PATH, 'test' )))))


# 
# 
# Let's load the train file.

# In[ ]:


get_ipython().run_cell_magic('time', '', "train_df = pd.read_csv(os.path.join(PATH,'train.csv'), \n                       dtype={'acoustic_data': np.int16, 'time_to_failure': np.float32})")


# In[ ]:


train_df_save = train_df.copy


# * Let's check the data imported. We normalize the data to a 0 mean value.

# In[ ]:


mean_acoustic = np.mean(train_df.acoustic_data)
train_df.acoustic_data = train_df.acoustic_data - mean_acoustic
print(mean_acoustic)
print (round(np.mean(train_df.acoustic_data),2))


# In[ ]:


print("Train: rows:{} cols:{}".format(train_df.shape[0], train_df.shape[1]))


# In[ ]:


pd.options.display.precision = 15
train_df.head(10)


# # <a id='3'>Data exploration</a>  
# 
# The dimmension of the data is large, in excess of 600 millions rows of data.  
# The two columns in the train dataset have the following meaning:   
# *  accoustic_data: is the accoustic signal measured in the laboratory experiment;  
# * time to failure: this gives the time until a failure will occurs.
# 
# Let's plot 2% of the data. For this we will sample every 50 points of data.  

# In[ ]:


train_ad_sample_df = train_df['acoustic_data'].values[::50]
train_ttf_sample_df = train_df['time_to_failure'].values[::50]

def plot_acc_ttf_data(train_ad_sample_df, train_ttf_sample_df, title="Acoustic data and time to failure: 1% sampled data"):
    fig, ax1 = plt.subplots(figsize=(12, 8))
    plt.title(title)
    plt.plot(train_ad_sample_df, color='r')
    ax1.set_ylabel('acoustic data', color='r')
    plt.legend(['acoustic data'], loc=(0.01, 0.95))
    ax2 = ax1.twinx()
    plt.plot(train_ttf_sample_df, color='b')
    ax2.set_ylabel('time to failure', color='b')
    plt.legend(['time to failure'], loc=(0.01, 0.9))
    plt.grid(True)

plot_acc_ttf_data(train_ad_sample_df, train_ttf_sample_df)
del train_ad_sample_df
del train_ttf_sample_df


# The plot shows only 2% of the full data. 
# The acoustic data shows complex oscilations with variable amplitude. Just before each failure there is an increase in the amplitude of the acoustic data. Because the data is all positive and log, the peaks are not as severe.
# 
# We see that large amplitudes are also obtained at different moments in time (for example about the mid-time between two succesive failures).  
# 
# Let's plot as well the first two earthquakes of the data.

# In[ ]:





# In[ ]:


gc.collect()
#train_ad_sample_df = train_df['acoustic_data'].values[:6291455]
#train_ttf_sample_df = (train_df['time_to_failure'].values[:6291455])
train_ad_sample_df = train_df['acoustic_data'].values[:50580000]
train_ttf_sample_df = (train_df['time_to_failure'].values[:50580000])

plot_acc_ttf_data(train_ad_sample_df, train_ttf_sample_df, title="Acoustic data and time to failure: 1st 2 quakes")
del train_ad_sample_df
del train_ttf_sample_df


# On this zoomed-in-time plot we can see that actually the large oscilation before the failure is not quite in the last moment. There are also trains of intense oscilations preceeding the large one and also some oscilations with smaller peaks after the large one. Then, after some minor oscilations, the failure occurs.

# # <a id='4'>Features engineering</a>  
# 
# The test segments are 150,000 each.   
# We split the train data in segments of the same dimmension with the test sets.
# 
# We will create additional aggregation features, calculated on the segments. 
# 

# In[ ]:


rows = 150000
segments = int(np.floor(train_df.shape[0] / rows))
print("Number of segments: ", segments)


# Let's define some computation helper functions.

# In[ ]:


def add_trend_feature(arr, abs_values=False):
    idx = np.array(range(len(arr)))
    if abs_values:
        arr = np.abs(arr)
    lr = LinearRegression()
    lr.fit(idx.reshape(-1, 1), arr)
    return lr.coef_[0]

def classic_sta_lta(x, length_sta, length_lta):
    sta = np.cumsum(x ** 2)
    # Convert to float
    sta = np.require(sta, dtype=np.float)
    # Copy for LTA
    lta = sta.copy()
    # Compute the STA and the LTA
    sta[length_sta:] = sta[length_sta:] - sta[:-length_sta]
    sta /= length_sta
    lta[length_lta:] = lta[length_lta:] - lta[:-length_lta]
    lta /= length_lta
    # Pad zeros
    sta[:length_lta - 1] = 0
    # Avoid division by zero by setting zero values to tiny float
    dtiny = np.finfo(0.0).tiny
    idx = lta < dtiny
    lta[idx] = dtiny
    return sta / lta


# ## Process train file
# 
# Now let's calculate the aggregated functions for train set.

# In[ ]:


gc.collect()


# In[ ]:


train_X = pd.DataFrame(index=range(segments), dtype=np.float64)

train_y = pd.DataFrame(index=range(segments), dtype=np.float64, columns=['time_to_failure'])
# These may be needed later
need_aggregated_features = False
if need_aggregated_features:
    total_mean = train_df['acoustic_data'].mean()
    total_std = train_df['acoustic_data'].std()
    total_max = train_df['acoustic_data'].max()
    total_min = train_df['acoustic_data'].min()
    total_sum = train_df['acoustic_data'].sum()
    total_abs_sum = np.abs(train_df['acoustic_data']).sum()


# In[ ]:


train_X.shape, train_y.shape


# In[ ]:


def create_features(seg_id, seg, X):
    xc = pd.Series(seg['acoustic_data'].values)
    zc = np.fft.fft(xc)
    X.loc[seg_id, 'mean'] = xc.mean()
    X.loc[seg_id, 'std'] = xc.std()
    X.loc[seg_id, 'max'] = xc.max()
    
    #FFT transform values
    realFFT = np.real(zc)
    imagFFT = np.imag(zc)
    
    X.loc[seg_id, 'Rmean'] = realFFT.mean()
    X.loc[seg_id, 'Rstd'] = realFFT.std()
    X.loc[seg_id, 'Rmax'] = realFFT.max()
    X.loc[seg_id, 'Rmin'] = realFFT.min()
    X.loc[seg_id, 'Imean'] = imagFFT.mean()
    X.loc[seg_id, 'Istd'] = imagFFT.std()
    X.loc[seg_id, 'Imax'] = imagFFT.max()
    X.loc[seg_id, 'Imin'] = imagFFT.min()
    X.loc[seg_id, 'Rmean_last_5000'] = realFFT[-5000:].mean()
    X.loc[seg_id, 'Rstd__last_5000'] = realFFT[-5000:].std()
    X.loc[seg_id, 'Rmax_last_5000'] = realFFT[-5000:].max()
    X.loc[seg_id, 'Rmin_last_5000'] = realFFT[-5000:].min()
    X.loc[seg_id, 'Rmean_last_15000'] = realFFT[-15000:].mean()
    X.loc[seg_id, 'Rstd_last_15000'] = realFFT[-15000:].std()
    X.loc[seg_id, 'Rmax_last_15000'] = realFFT[-15000:].max()
    X.loc[seg_id, 'Rmin_last_15000'] = realFFT[-15000:].min()
    X.loc[seg_id, 'mean_change_abs'] = np.mean(np.diff(xc))
    X.loc[seg_id, 'mean_change_rate'] = np.mean(np.nonzero((np.diff(xc) / xc[:-1]))[0])
    
    X.loc[seg_id, 'abs_max'] = np.abs(xc).max()
    X.loc[seg_id, 'abs_min'] = np.abs(xc).min()
    X.loc[seg_id, 'std_first_50000'] = xc[:50000].std()
    X.loc[seg_id, 'std_last_50000'] = xc[-50000:].std()
    X.loc[seg_id, 'std_first_10000'] = xc[:10000].std()
    X.loc[seg_id, 'std_last_10000'] = xc[-10000:].std()

    X.loc[seg_id, 'avg_first_50000'] = xc[:50000].mean()
    X.loc[seg_id, 'avg_last_50000'] = xc[-50000:].mean()
    X.loc[seg_id, 'avg_first_10000'] = xc[:10000].mean()
    X.loc[seg_id, 'avg_last_10000'] = xc[-10000:].mean()
   
    X.loc[seg_id, 'min_first_50000'] = xc[:50000].min()
    X.loc[seg_id, 'min_last_50000'] = xc[-50000:].min()
    X.loc[seg_id, 'min_first_10000'] = xc[:10000].min()
    X.loc[seg_id, 'min_last_10000'] = xc[-10000:].min()
    
    X.loc[seg_id, 'max_first_50000'] = xc[:50000].max()
    X.loc[seg_id, 'max_last_50000'] = xc[-50000:].max()
    X.loc[seg_id, 'max_first_10000'] = xc[:10000].max()
    X.loc[seg_id, 'max_last_10000'] = xc[-10000:].max()

    #X.loc[seg_id, 'max_to_min'] = xc.max() / np.abs(xc.min())
    X.loc[seg_id, 'max_to_min_diff'] = xc.max() - np.abs(xc.min())
    
    X.loc[seg_id, 'count_big'] = len(xc[np.abs(xc) > 500])
    X.loc[seg_id, 'sum'] = xc.sum()
    
    X.loc[seg_id, 'mean_change_rate_first_50000'] = np.mean(np.nonzero((np.diff(xc[:50000]) / xc[:50000][:-1]))[0])
    X.loc[seg_id, 'mean_change_rate_last_50000'] = np.mean(np.nonzero((np.diff(xc[-50000:]) / xc[-50000:][:-1]))[0])
    X.loc[seg_id, 'mean_change_rate_first_10000'] = np.mean(np.nonzero((np.diff(xc[:10000]) / xc[:10000][:-1]))[0])
    X.loc[seg_id, 'mean_change_rate_last_10000'] = np.mean(np.nonzero((np.diff(xc[-10000:]) / xc[-10000:][:-1]))[0])
    
    X.loc[seg_id, 'q95'] = np.quantile(xc, 0.95)
    X.loc[seg_id, 'q99'] = np.quantile(xc, 0.99)
    X.loc[seg_id, 'q05'] = np.quantile(xc, 0.05)
    X.loc[seg_id, 'q01'] = np.quantile(xc, 0.01)

    X.loc[seg_id, 'abs_q95'] = np.quantile(np.abs(xc), 0.95)
    X.loc[seg_id, 'abs_q99'] = np.quantile(np.abs(xc), 0.99)
    X.loc[seg_id, 'abs_q05'] = np.quantile(np.abs(xc), 0.05)
    X.loc[seg_id, 'abs_q01'] = np.quantile(np.abs(xc), 0.01)
    
    X.loc[seg_id, 'trend'] = add_trend_feature(xc)
    X.loc[seg_id, 'abs_trend'] = add_trend_feature(xc, abs_values=True)
    X.loc[seg_id, 'abs_mean'] = np.abs(xc).mean()
    X.loc[seg_id, 'abs_std'] = np.abs(xc).std()
    
    X.loc[seg_id, 'mad'] = xc.mad()
    
    X.loc[seg_id, 'Moving_average_700_mean'] = xc.rolling(window=700).mean().mean(skipna=True)
    X.loc[seg_id, 'Moving_average_1500_mean'] = xc.rolling(window=1500).mean().mean(skipna=True)
    X.loc[seg_id, 'Moving_average_3000_mean'] = xc.rolling(window=3000).mean().mean(skipna=True)
    X.loc[seg_id, 'Moving_average_6000_mean'] = xc.rolling(window=6000).mean().mean(skipna=True)
    ewma = pd.Series.ewm
    X.loc[seg_id, 'exp_Moving_average_300_mean'] = (ewma(xc, span=300).mean()).mean(skipna=True)
    X.loc[seg_id, 'exp_Moving_average_3000_mean'] = ewma(xc, span=3000).mean().mean(skipna=True)
    X.loc[seg_id, 'exp_Moving_average_30000_mean'] = ewma(xc, span=6000).mean().mean(skipna=True)
    no_of_std = 2
    X.loc[seg_id, 'MA_700MA_std_mean'] = xc.rolling(window=700).std().mean()
    X.loc[seg_id,'MA_700MA_BB_high_mean'] = (X.loc[seg_id, 'Moving_average_700_mean'] + no_of_std * X.loc[seg_id, 'MA_700MA_std_mean']).mean()
    X.loc[seg_id,'MA_700MA_BB_low_mean'] = (X.loc[seg_id, 'Moving_average_700_mean'] - no_of_std * X.loc[seg_id, 'MA_700MA_std_mean']).mean()
    X.loc[seg_id, 'MA_400MA_std_mean'] = xc.rolling(window=400).std().mean()
    X.loc[seg_id,'MA_400MA_BB_high_mean'] = (X.loc[seg_id, 'Moving_average_700_mean'] + no_of_std * X.loc[seg_id, 'MA_400MA_std_mean']).mean()
    X.loc[seg_id,'MA_400MA_BB_low_mean'] = (X.loc[seg_id, 'Moving_average_700_mean'] - no_of_std * X.loc[seg_id, 'MA_400MA_std_mean']).mean()
    X.loc[seg_id, 'MA_1000MA_std_mean'] = xc.rolling(window=1000).std().mean()
    
    X.loc[seg_id, 'iqr'] = np.subtract(*np.percentile(xc, [75, 25]))
    X.loc[seg_id, 'q999'] = np.quantile(xc,0.999)
    X.loc[seg_id, 'q001'] = np.quantile(xc,0.001)
    X.loc[seg_id, 'ave10'] = stats.trim_mean(xc, 0.1)

    for windows in [5, 10, 50, 100, 500, 1000, 5000, 10000]:
    
        x_roll_std = xc.rolling(windows).std().dropna().values
        x_roll_mean = xc.rolling(windows).mean().dropna().values
        X.loc[seg_id, 'ave_roll_std_' + str(windows)] = x_roll_std.mean()
        X.loc[seg_id, 'std_roll_std_' + str(windows)] = x_roll_std.std()
        X.loc[seg_id, 'max_roll_std_' + str(windows)] = x_roll_std.max()
        X.loc[seg_id, 'min_roll_std_' + str(windows)] = x_roll_std.min()
        X.loc[seg_id, 'q01_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.01)
        X.loc[seg_id, 'q05_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.05)
        X.loc[seg_id, 'q95_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.95)
        X.loc[seg_id, 'q99_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.99)
        X.loc[seg_id, 'av_change_abs_roll_std_' + str(windows)] = np.mean(np.diff(x_roll_std))
        X.loc[seg_id, 'av_change_rate_roll_std_' + str(windows)] = np.mean(np.nonzero((np.diff(x_roll_std) / x_roll_std[:-1]))[0])
        X.loc[seg_id, 'abs_max_roll_std_' + str(windows)] = np.abs(x_roll_std).max()
        
        X.loc[seg_id, 'ave_roll_mean_' + str(windows)] = x_roll_mean.mean()
        X.loc[seg_id, 'std_roll_mean_' + str(windows)] = x_roll_mean.std()
        X.loc[seg_id, 'max_roll_mean_' + str(windows)] = x_roll_mean.max()
        X.loc[seg_id, 'min_roll_mean_' + str(windows)] = x_roll_mean.min()
        X.loc[seg_id, 'q01_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.01)
        X.loc[seg_id, 'q05_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.05)
        X.loc[seg_id, 'q95_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.95)
        X.loc[seg_id, 'q99_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.99)
        X.loc[seg_id, 'av_change_abs_roll_mean_' + str(windows)] = np.mean(np.diff(x_roll_mean))
        X.loc[seg_id, 'av_change_rate_roll_mean_' + str(windows)] = np.mean(np.nonzero((np.diff(x_roll_mean) / x_roll_mean[:-1]))[0])
        X.loc[seg_id, 'abs_max_roll_mean_' + str(windows)] = np.abs(x_roll_mean).max()  
    


# In[ ]:


# iterate over all segments
for seg_id in tqdm_notebook(range(segments)):
    seg = train_df.iloc[seg_id*rows:seg_id*rows+rows]
    create_features(seg_id, seg, train_X)
    # the y value is the last entry in the time to failure in the segment
    train_y.loc[seg_id, 'time_to_failure'] = seg['time_to_failure'].values[-1]


# Let's check the result. We plot the shape and the head of train_X and train_y.

# In[ ]:


train_X_save = train_X.copy
train_y_save = train_y.copy
train_y.head(5)


# In[ ]:


# We will not train on the segments with a quake, because there are likely outliers
train_y_quake = np.nonzero(np.diff(train_y.time_to_failure) > 0)[0] + 1
print(len(train_y_quake))
print (len(train_y))

for idx in train_y_quake: 
    train_y.drop([idx],inplace=True)
    train_X.drop([idx],inplace = True)
#np.abs(train_X.corrwith(train_y)).sort_values(ascending=False).head(12)
train_X.to_csv('train_features.csv', index=False)
train_y.to_csv('train_y.csv', index=False)


# In[ ]:





# In[ ]:


train_X.shape, train_y.shape


# In[ ]:


train_X.head(), train_y.head()


# We scale the data.

# In[ ]:


scaler = StandardScaler()
scaler.fit(train_X)
scaled_train_X = pd.DataFrame(scaler.transform(train_X), columns=train_X.columns)
#scaled_train_X = train_X


# Let's check the obtained dataframe.

# In[ ]:


scaled_train_X.head(10)


# ## Process test data
# 
# We apply the same processing done for the training data to the test data.
# 
# We read the submission file and prepare the test file.

# In[ ]:


submission = pd.read_csv('../input/sample_submission.csv', index_col='seg_id')
test_X = pd.DataFrame(columns=train_X.columns, dtype=np.float64, index=submission.index)


# Let's check the shape of the submission and test_X datasets.

# In[ ]:


submission.shape, test_X.shape


# In[ ]:


for seg_id in tqdm_notebook(test_X.index):
    seg = pd.read_csv('../input/test/' + seg_id + '.csv')
    # convert to mean 0 of the training dataset 
    # seg_mean = np.mean(seg.acoustic_data)
    seg.acoustic_data = seg.acoustic_data - mean_acoustic
    create_features(seg_id, seg, test_X)


# In[ ]:


# save before scaling
test_X.to_csv('test_features.csv', index=False)


# We scale the test data.

# In[ ]:


scaled_test_X = pd.DataFrame(scaler.transform(test_X), columns=test_X.columns)
#scaled_test_X = test_X
scaled_test_X.values[1117]


# In[ ]:


scaled_test_X.shape


# In[ ]:


scaled_test_X.tail(10)


# 
# # <a id='5'>Model</a>  
# 
# Let's prepare the model. First we define a validation function to evaluate model performance.
# 
# We next define a set of models which can later be blended and stacked.
# 
# 
# ## Define Validation
# 
# First define a cross validation measurement routine.

# In[ ]:


n_fold = 5
def mae_cv (model):
    folds = KFold(n_splits=n_fold, shuffle=True, random_state=42).get_n_splits(scaled_train_X.values)
    mae = -cross_val_score (model, scaled_train_X.values, train_y, scoring="neg_mean_absolute_error",
                           verbose=0,
                           cv=folds)
    return mae


# ### LGB Model
# We define the model parameters and the definition for the first model, an LGB regression.

# In[ ]:


get_ipython().run_cell_magic('time', '', '\nlgb_params = {\'num_leaves\': 51,\n         \'min_data_in_leaf\': 10, \n         \'objective\':\'regression\',\n         \'max_depth\': -1,\n         \'learning_rate\': 0.001,\n         "boosting": "gbdt",\n         "feature_fraction": 0.91,\n         "bagging_freq": 1,\n         "bagging_fraction": 0.91,\n         "bagging_seed": 42,\n         "metric": \'mae\',\n         "lambda_l1": 0.1,\n         "verbosity": -1,\n         "nthread": -1,\n         "random_state": 42}\n\n\nlgb_model = lgb.LGBMRegressor(objective=\'regression\',num_leaves=5,\n                              learning_rate=0.01, n_estimators=720,\n                              bagging_freq = 5, feature_fraction = 0.2319,\n                              feature_fraction_seed=9, bagging_seed=9,\n                              min_data_in_leaf =6, min_sum_hessian_in_leaf = 11, n_jobs = -1)\n\nscore = mae_cv(lgb_model)\nprint("LGBM score: {:.4f} ({:.4f})\\n" .format(score.mean(), score.std()))\nlgb_model')


# In[ ]:


lgb_gamma_model = lgb.LGBMRegressor(objective='gamma',num_leaves=5,
                              learning_rate=0.01, n_estimators=720,
                              bagging_freq = 5, feature_fraction = 0.2319,
                              feature_fraction_seed=9, bagging_seed=9,
                              min_data_in_leaf =6, min_sum_hessian_in_leaf = 11, n_jobs = -1)

score = mae_cv(lgb_gamma_model)
print("LGBM - gamma score: {:.4f} ({:.4f})\n" .format(score.mean(), score.std()))
lgb_gamma_model


# ### XGB Model

# In[ ]:


get_ipython().run_cell_magic('time', '', 'xgb_params = {\'eta\': 0.03,\n              \'max_depth\': 9,\n              \'subsample\': 0.85,\n              \'objective\': \'reg:linear\',\n              \'eval_metric\': \'mae\',\n              \'silent\': True,\n              \'nthread\': 4}\n    \nxgb_model = xgb.XGBRegressor(colsample_bytree=0.4603, gamma=0.0468, \n                             learning_rate=0.05, max_depth=3, \n                             min_child_weight=1.7817, n_estimators=2200,\n                             reg_alpha=0.4640, reg_lambda=0.8571,\n                             subsample=0.5213, silent=1,\n                             random_state =7, nthread = -1, eval_metric = \'mae\',)\n\nscore = mae_cv(xgb_model)\nprint("XGB score: {:.4f} ({:.4f})\\n" .format(score.mean(), score.std()))\nxgb_model\n\n#    xgb.train(dtrain=train_data, num_boost_round=20000, evals=watchlist, early_stopping_rounds=200, \n#                          verbose_eval=500, params=xgb_params)')


# ### Random Forest

# In[ ]:


get_ipython().run_cell_magic('time', '', 'rf_model = RandomForestRegressor(n_estimators=120, n_jobs=-1, min_samples_leaf=1, \n                           max_features = "auto",max_depth=15, )\nscore = mae_cv(rf_model)\nprint("Random Forest score: {:.4f} ({:.4f})\\n" .format(score.mean(), score.std()))\nrf_model')


# ### Cat Boost
# 
# 

# In[ ]:


get_ipython().run_cell_magic('time', '', 'params = {\'loss_function\':\'MAE\',}\ncat_model = CatBoostRegressor(iterations=1000,  eval_metric=\'MAE\', verbose=False, **params)\n\nscore = mae_cv(cat_model)\nprint("Cat Boost score: {:.4f} ({:.4f})\\n" .format(score.mean(), score.std()))\ncat_model')


# ### Kernel Ridge

# In[ ]:


get_ipython().run_cell_magic('time', '', 'KRR_model = KernelRidge(alpha=0.6, kernel=\'polynomial\', degree=2, coef0=2.5)\nscore = mae_cv(KRR_model)\nprint("Kernel Ridge score: {:.4f} ({:.4f})\\n" .format(score.mean(), score.std()))\nprint (score)\nKRR_model')


# ### Elastic Net
# 

# In[ ]:


get_ipython().run_cell_magic('time', '', '#ENet_model = make_pipeline(RobustScaler(), ElasticNet(alpha=0.0005, l1_ratio=0.9, random_state=3,max_iter=5000))\nENet_model = ElasticNet(alpha=0.0005, l1_ratio=0.9, random_state=3,max_iter=5000)\nscore = mae_cv(ENet_model)\nprint("Elastic Net score: {:.4f} ({:.4f})\\n" .format(score.mean(), score.std()))\nENet_model')


# ### Lasso

# In[ ]:


get_ipython().run_cell_magic('time', '', 'lasso_model = Lasso(alpha =0.0005, random_state=1)\nscore = mae_cv(lasso_model)\nprint("Lasso score: {:.4f} ({:.4f})\\n" .format(score.mean(), score.std()))\nlasso_model')


# In[ ]:


class AveragingModels(BaseEstimator, RegressorMixin, TransformerMixin):
    def __init__(self, models):
        self.models = models
        
    # we define clones of the original models to fit the data in
    def fit(self, X, y):
        self.models_ = [clone(x) for x in self.models]
        
        # Train cloned base models
        for model in self.models_:
            model.fit(X, y)

        return self
    
    #Now we do the predictions for cloned models and average them
    def predict(self, X):
        
        predictions = np.column_stack([
            model.predict(X) for model in self.models_
        ])
        return np.mean(predictions, axis=1)   


# In[ ]:


class StackingAveragedModels(BaseEstimator, RegressorMixin, TransformerMixin):
    def __init__(self, base_models, meta_model, n_folds=5):
        self.base_models = base_models
        self.meta_model = meta_model
        self.n_folds = n_folds
   
    # We again fit the data on clones of the original models
    def fit(self, X, y):
        print (type(X))
        self.base_models_ = [list() for x in self.base_models]
        self.meta_model_ = clone(self.meta_model)
        kfold = KFold(n_splits=self.n_folds, shuffle=True, random_state=156)
        print (KFold)
        # Train cloned base models then create out-of-fold predictions
        # that are needed to train the cloned meta-model
        out_of_fold_predictions = np.zeros((X.shape[0], len(self.base_models)))
        for i, model in enumerate(self.base_models):
            for train_index, holdout_index in kfold.split(X, y):
                instance = clone(model)
                self.base_models_[i].append(instance)
                instance.fit(X.iloc[train_index], y.iloc[train_index])
                y_pred = instance.predict(X.iloc[holdout_index])
                out_of_fold_predictions[holdout_index, i] = y_pred
                
        # Now train the cloned  meta-model using the out-of-fold predictions as new feature
        self.meta_model_.fit(out_of_fold_predictions, y)
        return self
   
    #Do the predictions of all base models on the test data and use the averaged predictions as 
    #meta-features for the final prediction which is done by the meta-model
    def predict(self, X):
        meta_features = np.column_stack([
            np.column_stack([model.predict(X) for model in base_models]).mean(axis=1)
            for base_models in self.base_models_ ])
        return self.meta_model_.predict(meta_features)


# In[ ]:


class StackingCVRegressorRetrained(BaseEstimator, RegressorMixin, TransformerMixin):
    def __init__(self, regressors, meta_regressor, n_folds=5, use_features_in_secondary=False):
        self.regressors = regressors
        self.meta_regressor = meta_regressor
        self.n_folds = n_folds
        self.use_features_in_secondary = use_features_in_secondary

    def fit(self, X, y):
        self.regr_ = [clone(x) for x in self.regressors]
        self.meta_regr_ = clone(self.meta_regressor)

        kfold = KFold(n_splits=self.n_folds, shuffle=True)

        out_of_fold_predictions = np.zeros((X.shape[0], len(self.regressors)))

        # Create out-of-fold predictions for training meta-model
        for i, regr in enumerate(self.regr_):
            for train_idx, holdout_idx in kfold.split(X, y):
                instance = clone(regr)
                instance.fit(X[train_idx], y[train_idx])
                out_of_fold_predictions[holdout_idx, i] = instance.predict(X[holdout_idx])

        # Train meta-model
        if self.use_features_in_secondary:
            self.meta_regr_.fit(np.hstack((X, out_of_fold_predictions)), y)
        else:
            self.meta_regr_.fit(out_of_fold_predictions, y)
        
        # Retrain base models on all data
        for regr in self.regr_:
            regr.fit(X, y)

        return self

    def predict(self, X):
        meta_features = np.column_stack([
            regr.predict(X) for regr in self.regr_
        ])

        if self.use_features_in_secondary:
            return self.meta_regr_.predict(np.hstack((X, meta_features)))
        else:
            return self.meta_regr_.predict(meta_features)


# In[ ]:


get_ipython().run_cell_magic('time', '', '#averaged_models = AveragingModels(models = (rf_model, xgb_model, KRR_model, lgb_model, ENet_model, cat_model, lasso_model))\n#averaged_models = AveragingModels(models = (rf_model, lgb_model,  cat_model, lasso_model))\naveraged_models = AveragingModels(models = (rf_model,cat_model))\n\nscore =mae_cv(averaged_models)\nprint(" Averaged base models score: {:.4f} ({:.4f})\\n".format(score.mean(), score.std()))\n#averaged_models.fit (scaled_train_X.values, train_y)')


# In[ ]:


averaged_models.fit (scaled_train_X.values, train_y)
averaged2_train_predict = averaged_models.predict(scaled_train_X.values)
print(mean_absolute_error(train_y, averaged2_train_predict))


# In[ ]:




averaged_prediction = np.zeros(len(scaled_test_X))
averaged_prediction += averaged_models.predict(scaled_test_X.values)
averaged_prediction


# In[ ]:


get_ipython().run_cell_magic('time', '', 'stacked_predict = StackingAveragedModels(base_models =(rf_model, xgb_model, lgb_model, cat_model,ENet_model), \n                                          meta_model =lasso_model) \nstacked_predict.fit(scaled_train_X, train_y)')


# In[ ]:


stacked_train_pred = stacked_predict.predict(scaled_train_X)

print(mean_absolute_error(train_y, stacked_train_pred))

stacked_prediction = np.zeros(len(scaled_test_X))
stacked_prediction += stacked_predict.predict(scaled_test_X)**1.0
stacked_prediction[0:4]


# # <a id='6'>Submission</a>  
# 
# We set the predicted time to failure in the submission file.

# In[ ]:


submission.time_to_failure = averaged_prediction
submission.to_csv('submissionV30_averaged_cat_rf.csv',index=True)
submission.time_to_failure = stacked_prediction
submission.to_csv('submissionV30_stacked.csv',index=True)


# # <a id='7'>References</a>  
# 
# [1] Fast Fourier Transform, https://en.wikipedia.org/wiki/Fast_Fourier_transform   
# [2] Shifting aperture, in Neural network for inverse mapping in eddy current testing, https://www.researchgate.net/publication/3839126_Neural_network_for_inverse_mapping_in_eddy_current_testing   
# [3] Andrews Script plus a Genetic Program Model, https://www.kaggle.com/scirpus/andrews-script-plus-a-genetic-program-model/
