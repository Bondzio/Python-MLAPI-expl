#!/usr/bin/env python
# coding: utf-8

# # Freesound Kaggle Presentation
# 
# ### Matt Potma
# 
# ### May 3, 2018
# 
# This notebook has been written for a presentation happening at approximately 6:30pm PDT today, May 3rd. A link to the livestream will be posted here shortly before it begins, so anyone can view it. Without watching the presentation, and even with, the flow of the notebook may be a bit awkward, but the presentation will be left up on YouTube to be viewed at any time. At some point, I may edit this notebook to provide more context, but will be left as-is for now.
# 
# Unfortunately, despite the notebook running from scratch on my laptop in about 2 hours, trying to Commit & Run the notebook ran out of time. I've added two flags at the beginning of the second code cell, `cache` and `run_full_notebook`. Both are set to `False` in this notebook, hoping that it can fully execute on this kernel. The `cache` flag saves intermediate results and calculates spectral features on audio files with silence trimmed off, and `run_full_notebook` trains a couple of extra LGBM models. By setting both of those flags to `True` and running the notebook locally, the last submission file is good for 0.836 on the Public Leaderboard, with lots that can be improved upon.
# 
# A link to my presentation where I go through this notebook can be seen here https://www.youtube.com/watch?v=3CtPuwok7Nw
# 
# 

# ### Miscellaneous imports

# In[61]:


import os, random, math

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import lightgbm as lgb

import librosa
import librosa.display

from scipy.stats import skew, kurtosis
from sklearn.model_selection import train_test_split

from prettytable import PrettyTable
from tqdm import tqdm_notebook, tqdm_pandas
tqdm_notebook().pandas(smoothing=0.7)

import IPython
import IPython.display as ipd

import matplotlib as mpl
mpl.rcParams['font.size'] = 14


# ### Setting up directories
# 
# If `cache` is set to `True`, calculated features will be saved to disk for use later. In addition, the spectral features will be calculated on trimmed audio files, instead of the original files.

# In[62]:


cache = False
run_full_notebook = False

train_root = '../input/audio_train/'
test_root = '../input/audio_test/'

if cache:
    train_root_trimmed = '../input/audio_train_trimmed/'
    test_root_trimmed = '../input/audio_test_trimmed/'

    os.makedirs('../input/audio_train_trimmed', exist_ok=True)
    os.makedirs('../input/audio_test_trimmed', exist_ok=True)
    
    os.makedirs('../cache', exist_ok=True)
    os.makedirs('../output', exist_ok=True)

else:
    train_root_trimmed = train_root
    test_root_trimmed = test_root


# ### Load and view data

# In[63]:


test_df = pd.read_csv("../input/sample_submission.csv")
train_df = pd.read_csv("../input/train.csv")

train_df.head()


# ### Data counts

# In[64]:


n_test = test_df.shape[0]
n_training = train_df.shape[0]
n_categories = len(train_df.label.unique())

print("Number of training examples: {}".format(n_training))
print("Number of testing examples: {}".format(n_test))
print("Number of unique categories: {}".format(n_categories))


# In[65]:


# Plot a pie chart
mpl.rcParams['font.size'] = 16
plt.figure(figsize=(10, 10))
plt.pie([n_training - train_df.manually_verified.sum(), train_df.manually_verified.sum()],
        labels=["Not Verified ({:.0f}%)".format(100*(n_training - train_df.manually_verified.sum())/n_training),
                "Verified ({:.0f}%)".format(100*train_df.manually_verified.sum()/n_training)])

# Turn the pie chart into a donut chart
p = plt.gcf()
p.gca().add_artist(plt.Circle((0, 0), 0.6, color='white'))
plt.axis('equal')

plt.show()


# In[66]:


def play_audio(wavfile, dset='train'):
    print(wavfile)
    fname = '../input/audio_{}/{}'.format(dset, wavfile)
    IPython.display.display(ipd.Audio(fname))
    
    x, sr = librosa.load(fname)
    
    plt.figure(figsize=(14, 5))
    librosa.display.waveplot(x, sr=sr)
    
    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')


# In[67]:


random_int = random.randint(0, n_training)
random_wavfile = train_df.fname.iloc[random_int]
print(train_df.label.iloc[random_int])

play_audio(random_wavfile)


# ## List of categories
# 
# | Instruments   | Instruments Continued | Human        | Actions | Other |
# | :------------ | :-------              | :------      | :----   | :---  |
# | Hi-hat        | Bass_drum             | Laughter     | Knock   | Gunshot_or_gunfire |
# | Saxophone     | Harmonica             | Finger_snapping | Drawer_open_or_close  | Bus |
# | Trumpet       | Gong                  | Fart         | Computer_keyboard | Telephone |
# | Glockenspiel  | Double_bass           | Cough        | Tearing | Squeak |
# | Cello         | Tambourine            | Applause     | Shatter | Scissors |
# | Clarinet      | Cowbell               | Burping_or_eructation  | Keys_jangling | Microwave_oven |
# | Snare_drum    | Electric_piano        |              | Writing | Bark |
# | Oboe          | Acoustic_guitar       |  |  | Meow |
# | Flute         | Voilin_or_fiddle      |              | | Fireworks |
# | Chime         |  | |  | |
# 
# 

# ### Label Distributions

# In[68]:


def plot_label_distributions():
    plot = train_df.groupby(['label', 'manually_verified'])['label'].count().unstack('label').transpose()
    plot['total'] = plot[0] + plot[1]
    plot.sort_values(['total', 1], ascending=[0, 1], inplace=True)
    plot.drop('total', axis=1, inplace=True)
    plot.plot(kind='bar', stacked=True, figsize=(22, 7), fontsize=18)

plot_label_distributions()


# ### First attempt at basic feature engineering
# From the data, derive simple statistical features, such as mean, min, max, standard deviation, length, rms, skewness and kurtosis.

# In[69]:


def wavfile_stats(fname, root):
    try:
        data, fs = librosa.core.load(root + fname, sr=None)
        mean = np.mean(data)
        minimum = np.min(data)
        maximum = np.max(data)
        std = np.std(data)
        length = len(data)
        rms = np.sqrt(np.mean(data**2))
        skewness = skew(data)
        kurt = kurtosis(data)

        return pd.Series([length, mean, minimum, maximum, std, rms, skewness, kurt])
    except ValueError:
        print("Bad file at {}".format(fname))
        return pd.Series([0, 0, 0, 0, 0, 0, 0, 0])


# ### Apply to the DataFrame
# 
# Use pandas' progress apply to calculate the simple statistical features.
# 
# If possible, load features from a cached csv file.

# In[70]:


if os.path.isfile('../cache/train_1.csv') and cache:
    train_df = pd.read_csv('../cache/train_1.csv')
    test_df = pd.read_csv('../cache/test_1.csv')
    assert len(train_df.index) == n_training
    assert len(test_df.index) == n_test
    print("Files loaded from cache")

else:
    train_df[['length', 'data_mean', 'data_min', 'data_max', 'data_std', 'data_rms', 'skewness', 'kurtosis']] =         train_df['fname'].progress_apply(wavfile_stats, root=train_root)
    test_df[['length', 'data_mean', 'data_min', 'data_max', 'data_std', 'data_rms', 'skewness', 'kurtosis']] =         test_df['fname'].progress_apply(wavfile_stats, root=test_root)
    
    if cache:
        train_df.to_csv('../cache/train_1.csv', index=False)
        test_df.to_csv('../cache/test_1.csv', index=False)


# ### A couple of other miscellaneous features

# In[71]:


train_df['rms_std'] = train_df['data_rms'] / train_df['data_std']
test_df['rms_std'] = test_df['data_rms'] / test_df['data_std']

train_df['max_min'] = train_df['data_max'] / train_df['data_min']
test_df['max_min'] = test_df['data_max'] / test_df['data_min']


# ### Make it easy to view your data
# 
# Here are two simple functions for producing either a histogram or boxplot of any variable in the DataFrame

# In[72]:


def plot_hist(feature_name, bins=50, log=False):
    """Plot feature histogram with pandas."""
    data = train_df[feature_name].values
    plt.hist(data, bins=bins, log=log)
    plt.grid()
    plt.show()

def plot_box(feature_name):
    """Plot boxplot of variable with pandas."""
    props = dict(linewidth=3)
    train_df.boxplot(column=feature_name, by='label', rot=90, figsize=(20, 7), sym='', grid=False, boxprops=props)
    plt.title('{} boxplot'.format(feature_name))
    plt.suptitle('')


# In[73]:


feature = 'kurtosis'

# plot_hist(feature, log=True)
plot_box(feature)


# ### Removal of NaNs, etc

# In[74]:


test_df[pd.isnull(test_df).any(axis=1)].head()


# In[75]:


test_df.fillna(0, inplace=True)


# ### Split data into training, validation, and testing sets

# In[76]:


def data_split(train_df, test_df, shuffle=True, test_size=0.25, random_state=0, verbose=True):
    # Get numpy array of X data
    X_train = train_df.drop(['fname', 'label', 'manually_verified'], axis=1).values
    X_test = test_df.drop(['fname', 'label'], axis=1).values
    feature_names = list(test_df.drop(['fname', 'label'], axis=1).columns.values)

    # Get numpy array of y data
    y_train = pd.get_dummies(train_df.label)
    labels = y_train.columns.values
    y_train = y_train.values

    y_train = [np.argmax(row) for row in y_train]
    X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=test_size,
                                                          random_state=random_state, shuffle=shuffle)
    if verbose:
        print("Train X shape = {}\nTrain y shape = {}".format(X_train.shape, len(y_train)))
        print("\nValid X shape = {}\nValid y shape = {}".format(X_valid.shape, len(y_valid)))

    assert X_train.shape[1] == X_valid.shape[1] == X_test.shape[1]
    assert len(y_train) == X_train.shape[0]
    assert len(y_valid) == X_valid.shape[0]
    
    return X_train, X_valid, y_train, y_valid, X_test, feature_names, labels


# In[77]:


X_train, X_valid, y_train, y_valid, X_test, feature_names, labels = data_split(train_df, test_df)


# ### Prepare dataset for LightGBM

# In[78]:


def lgb_dset(X_train, X_valid, y_train, y_valid, feature_names):
    
    d_train = lgb.Dataset(X_train, label=y_train, feature_name=feature_names)
    d_valid = lgb.Dataset(X_valid, label=y_valid, feature_name=feature_names)

    params = {
        'boosting_type': 'gbdt',
        'objective': 'multiclass',
        'metric': 'multi_logloss',
        'max_depth': 5,
        'num_leaves': 31,
        'learning_rate': 0.025,
        'feature_fraction': 0.85,
        'bagging_fraction': 0.85,
        'bagging_freq': 5,
        'num_threads': os.cpu_count(),
        'lambda_l2': 1.0,
        'min_gain_to_split': 0,
        'num_class': n_categories,
    }
    
    return d_train, d_valid, params


# ### Train our first model

# In[79]:


d_train, d_valid, params = lgb_dset(X_train, X_valid, y_train, y_valid, feature_names)
clf = lgb.train(params, d_train, num_boost_round=500, valid_sets=d_valid, verbose_eval=100, early_stopping_rounds=100)


# ### Calculation of MAP@3
# Demo available here https://www.kaggle.com/wendykan/map-k-demo

# In[80]:


def apk(actual, predicted, k=10):
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 0.0

    return score / min(len(actual), k)

def mapk(actual, predicted, k=10):
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])


# ### Predict and score validation set

# In[81]:


p = clf.predict(X_valid, num_iteration=clf.best_iteration)

predictions = [list(np.argsort(p[i])[::-1][:3]) for i in range(len(p))]
actual = [[i] for i in y_valid]

valid_score = mapk(actual, predictions, k=3)

print("Score = {:.4f}".format(valid_score))


# ### LightGBM feature importances

# In[82]:


ax = lgb.plot_importance(clf, max_num_features=10, grid=False, height=0.8, figsize=(20, 6))
plt.show()


# ### View some sample predictions

# In[83]:


def preds_to_labels(p, labels):
    predictions = [list(np.argsort(p[i])[::-1][:3]) for i in range(len(p))]
    prediction_labels = []
    
    for pred in predictions:
        label_list = []
        for output in pred:
            label_list.append(labels[output])
        prediction_labels.append(label_list)
    return prediction_labels

lab = preds_to_labels(p, labels)

t = PrettyTable(['Truth', 'Prediction'])
[t.add_row([labels[l[1][0]], l[0]]) for l in zip(lab[:10], actual[:10])]
print(t)


# ### Predict test set

# In[84]:


preds = clf.predict(X_test, num_iteration=clf.best_iteration)
lab = preds_to_labels(preds, labels)


# ### Spot check test set

# In[85]:


random_int = random.randint(0, n_test)
random_wavfile = test_df.fname.iloc[random_int]
print(lab[random_int])
play_audio(test_df.fname.iloc[random_int], dset='test')


# ### Create submission

# In[86]:


def create_submission(predictions, name='submission.csv'):
    predictions = ['{} {} {}'.format(x[0], x[1], x[2]) for x in predictions]
    submission = pd.read_csv('../input/sample_submission.csv')
    submission.label = predictions
    submission.to_csv('{}'.format(name), index=False)
    print("Submission saved to '{}'".format(name))

# LB score = 0.445, CV score = 0.4500
if run_full_notebook:
    create_submission(lab, 'submission-{:.4f}.csv'.format(valid_score))


# ### Trim silence from files

# In[87]:


def trim_silence(fname, root, window_length=0.5):
    try:
        trimmed_ends = 0
        trimmed_int = 0
        
        data, fs = librosa.core.load(root + fname, sr=None)
        length = len(data)
        
        # Trim silence from ends
        data, _ = librosa.effects.trim(data, top_db=40)
        length_int = len(data)
        ratio_int = length_int/length
        
        # Split file into non-silent chunks and recombine
        splits = librosa.effects.split(data, top_db=40)
        if len(splits) > 1:
            data = np.concatenate([data[x[0]:x[1]] for x in splits])    
        
        length_final = len(data)
        ratio_final = length_final/length_int     

        if cache:
            # Save file and return new features
            librosa.output.write_wav('{}_trimmed/{}'.format(root[:-1], fname), data, fs)
        return pd.Series([length_int, length_final, ratio_int, ratio_final])
       
    except ValueError:
        print("Bad file at {}".format(fname))
        return pd.Series([0, 0, 0, 0])  


# ### Apply silence trimming to DataFrame

# In[88]:


if os.path.isfile('../cache/train_2.csv') and cache:
    train_df = pd.read_csv('../cache/train_2.csv')
    test_df = pd.read_csv('../cache/test_2.csv')
    assert len(train_df.index) == n_training
    assert len(test_df.index) == n_test
    print("Files loaded from cache")

else:
    train_df[['length_int', 'length_final', 'ratio_int', 'ratio_final']] =         train_df['fname'].progress_apply(trim_silence, root=train_root)
    test_df[['length_int', 'length_final', 'ratio_int', 'ratio_final']] =         test_df['fname'].progress_apply(trim_silence, root=test_root)

    if cache:
        train_df.to_csv('../cache/train_2.csv', index=False)
        test_df.to_csv('../cache/test_2.csv', index=False)


# In[89]:


trimmed_ends = 100*train_df.ratio_final[train_df.ratio_final < 1.0].count()/len(train_df.index)
trimmed_int = 100*train_df.ratio_int[train_df.ratio_int < 1.0].count()/len(train_df.index)

trimmed_ends_test = 100*test_df.ratio_final[test_df.ratio_final < 1.0].count()/len(test_df.index)
trimmed_int_test = 100*test_df.ratio_int[test_df.ratio_int < 1.0].count()/len(test_df.index)

t = PrettyTable(['Dataset', 'Ends Trimmed', 'Intermediate Trimmed'])
t.add_row(['Training', '{:.1f}%'.format(trimmed_ends), '{:.1f}%'.format(trimmed_int)])
t.add_row(['Testing', '{:.1f}%'.format(trimmed_ends_test), '{:.1f}%'.format(trimmed_int_test)])
print(t)


# ### Create dataset with new features and train

# In[90]:


if run_full_notebook:
    X_train, X_valid, y_train, y_valid, X_test, feature_names, labels = data_split(train_df, test_df)

    d_train, d_valid, params = lgb_dset(X_train, X_valid, y_train, y_valid, feature_names)
    clf = lgb.train(params, d_train, num_boost_round=1000, valid_sets=d_valid, verbose_eval=100, early_stopping_rounds=100)


# ### Check our new validation score

# In[91]:


if run_full_notebook:    
    p = clf.predict(X_valid, num_iteration=clf.best_iteration)

    predictions = [list(np.argsort(p[i])[::-1][:3]) for i in range(len(p))]
    actual = [[i] for i in y_valid]

    valid_score = mapk(actual, predictions, k=3)

    print("Score = {:.4f}".format(valid_score))


# ### Check new feature importances

# In[92]:


if run_full_notebook:
    ax = lgb.plot_importance(clf, max_num_features=10, grid=False, height=0.8, figsize=(20, 6))
    plt.show()


# ### MFCC
# 
# - Similar to log-magnitude spectrograms
# - Use non-linaer Mel scale frequencies, $M(f) = 1125*ln(1+f/700)$
# - Use discrete cosine transformation, retaining only the lower coefficients

# In[93]:


def spectral_features(fname=None, root=None, n_mfcc=20, return_fnames=False):
    feature_names = []
    for i in ['mean', 'std', 'min', 'max', 'skew', 'kurt']:
        for j in range(n_mfcc):
            feature_names.append('mfcc_{}_{}'.format(j, i))
        feature_names.append('centroid_{}'.format(i))
        feature_names.append('bandwidth_{}'.format(i))
        feature_names.append('contrast_{}'.format(i))
        feature_names.append('rolloff_{}'.format(i))
        feature_names.append('flatness_{}'.format(i))
        feature_names.append('zcr_{}'.format(i))
    
    if return_fnames:
        return feature_names

    spectral_features = [
        librosa.feature.spectral_centroid,
        librosa.feature.spectral_bandwidth,
        librosa.feature.spectral_contrast,
        librosa.feature.spectral_rolloff,
        librosa.feature.spectral_flatness,
        librosa.feature.zero_crossing_rate]
     
    try:
        data, fs = librosa.core.load(root + fname, sr=None)
        M = librosa.feature.mfcc(data, sr=fs, n_mfcc=n_mfcc)
        data_row = np.hstack((np.mean(M, axis=1), np.std(M, axis=1), np.min(M, axis=1),
                              np.max(M, axis=1), skew(M, axis=1), kurtosis(M, axis=1)))
        
        for feat in spectral_features:
            S = feat(data)[0]
            data_row = np.hstack((data_row, np.mean(S), np.std(S), np.min(S),
                                  np.max(S), skew(S), kurtosis(S)))

        return pd.Series(data_row)
        
    except (ValueError, RuntimeError):
        print("Bad file at {}".format(fname))
        return pd.Series([0]*len(feature_names))  


# ### Apply spectral features to DataFrame

# In[94]:


if os.path.isfile('../cache/train_spectral.csv') and cache:
    train_df = pd.read_csv('../cache/train_spectral.csv')
    test_df = pd.read_csv('../cache/test_spectral.csv')
    assert len(train_df.index) == n_training
    assert len(test_df.index) == n_test
    print("Files loaded from cache")

else:
    feature_names = spectral_features(return_fnames=True)
    train_df[feature_names] = train_df['fname'].progress_apply(spectral_features, root=train_root_trimmed)
    test_df[feature_names] = test_df['fname'].progress_apply(spectral_features, root=test_root_trimmed)
    if cache:
        train_df.to_csv('../cache/train_spectral.csv', index=False)
        test_df.to_csv('../cache/test_spectral.csv', index=False)


# ### Train with spectral features

# In[95]:


# Create dataset
X_train, X_valid, y_train, y_valid, X_test, feature_names, labels = data_split(train_df, test_df, verbose=False)
d_train, d_valid, params = lgb_dset(X_train, X_valid, y_train, y_valid, feature_names)

# Train and predict
clf = lgb.train(params, d_train, num_boost_round=2000, valid_sets=d_valid, verbose_eval=200, early_stopping_rounds=100)
p = clf.predict(X_valid, num_iteration=clf.best_iteration)

# Score
predictions = [list(np.argsort(p[i])[::-1][:3]) for i in range(len(p))]
actual = [[i] for i in y_valid]
valid_score = mapk(actual, predictions, k=3)
print("\nScore = {:.4f}".format(valid_score))


# ### Feature importance with spectral features

# In[96]:


# Plot importances
ax = lgb.plot_importance(clf, max_num_features=10, grid=False, height=0.8, figsize=(16, 8))
plt.show()


# ### Create submission with spectral features

# In[97]:


# CV = 0.7854, LB = 0.835
p = clf.predict(X_test, num_iteration=clf.best_iteration)
lab = preds_to_labels(p, labels)
create_submission(lab, 'submission-{:.4f}.csv'.format(valid_score))


# ### Prepare to train on full dataset

# In[98]:


if run_full_notebook:
    params = {
        'boosting_type': 'gbdt',
        'objective': 'multiclass',
        'metric': 'multi_logloss',
        'max_depth': 5,
        'num_leaves': 31,
        'learning_rate': 0.025,
        'feature_fraction': 0.85,
        'bagging_fraction': 0.85,
        'bagging_freq': 5,
        'num_threads': os.cpu_count(),
        'lambda_l2': 1.0,
        'min_gain_to_split': 0,
        'num_class': n_categories,
    }

    # Create dataset
    X_train, X_valid, y_train, y_valid, X_test, feature_names, labels =         data_split(train_df, test_df, test_size=0)
    d_train = lgb.Dataset(X_train, label=y_train, feature_name=feature_names)


# ### Train, predict, create submission

# In[99]:


if run_full_notebook:
    # Train and predict
    print("Begin training...")
    clf = lgb.train(params, d_train, num_boost_round=1135)

    print("Begin test predictions...")
    p = clf.predict(X_test)
    lab = preds_to_labels(p, labels)

    create_submission(lab, 'submission-test.csv')
    print("Submission created.")

    # 0.836 LB


# ## Next steps beginner
# - Run this notebook yourself and submit the predictions
# - Kaggle user Zafar has a great notebook, based on neural networks
#     - https://www.kaggle.com/fizzbuzz/beginner-s-guide-to-audio-data
#     - Run his notebook and combine the predictions
#     - How do different methods of combing results effect your score? (mean, geometric mean, voting, ??)
#         - This could net you a top-5 place right now
# - Identify and modify any hyperparameters in this notebook

# ## Next steps intermediate
# - Try different algorithms
# - Normalization of MFCC coefficients
# - New/more/less features
# - Add more data
#     - Either external datasets or by adding noise
# - Add test data with high confidence predictions to training data

# ## Next steps advanced
# - Apply a sliding window to augment data
#     - Can assume label is characterized by entire signal and average outputs
#     - Can also assume label is characterized best by single frame and use highest output
# - Build a neural network on MFCC's or spectrograms and either
#     - A) Append calculated features to dense layer of neural network
#     - B) Use low dimension bottleneck of neural network as features in other models
# - Ignore me and do something better

# In[ ]:




