#!/usr/bin/env python
# coding: utf-8

# ### Content
# &#8544;. Read Data in<br>
# &#8545;. Fetch Audio Features for Tracks from Spotify Web API<br>
# &#8546;. Split Data into Train-Valid-Test sets<br>
# &#8547;. Preprocess Data for Train-Valid sets<br>
# &#8548;. Build Models with Random Forests & Neural Networks<br>
# &#8549;. Test out Models on Test set<br>

# # Prediction on Streams of Spotify's Worldwide Daily Most Listened Songs
# <b>* Github for Complete Running:</b> 
# <i><a href='https://github.com/Xiaobin-Gao/INFO6105_FinalProject-Prediction_on_Streams_of_Spotify_Daily_Most_Listened_Songs'>https://github.com/XiaobinGao/INFO6105_FinalProjectPrediction_on_Streams_of_Spotify_Daily_Most_Listened_Songs</a></i>

# <b>Goal:</b>
# To build a random forests model and a neural networts model respectively to predict 'Streams' of Spotify's worldwide daily most listened songs.<br>
# <b>Dataset:</b>
# The daily 200 most listened songs in 53 countries from 2017 to 2018 by Spotify users. More descriptions of the dataset can be found <a href='https://www.kaggle.com/edumucelli/spotifys-worldwide-daily-song-ranking'>here</a>.<br>
# <b>Basic Ideas:</b>
# Explore & Preprocess data -> Build a random forests model for prediction & Update dataset by dropping columns of little importance with the help of variable importance scores -> Build a deep neural networks model for prediction with the updated datasets<br>
# <b>Measures to Evaluate Models:</b>
# R-Squared, Mean Squared Error<br>

# In[ ]:


"""Import necessary packages"""

import pandas as pd
import numpy as np
import spotipy
import spotipy.util as util
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import r2_score, mean_squared_error
# from keras.wrappers.scikit_learn import KerasRegressor
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# ## &#8544;. Read Data in

# In[ ]:


df_data = pd.read_csv('../input/spotifys-worldwide-daily-song-ranking/data.csv', parse_dates=['Date'])

print(df_data.shape)
df_data.head()


# In[ ]:


df_data.info()


# <i>From the outputs, we know that we are going to deal with a giant dataset, which contains more than 3 million rows of data. Even with such a giant dataset, however, it would still be hard to build a good machine learning model, since there are only 6 variables there for prediction and some variables like 'URL' actually have nothing to do with 'Streams'. As we all know, audio features of a song are what really matters when it comes to helping the song get popular and gain more streams. Therefore, instead of directly throwing 'URL' into our feature models, we could use 'URL' in a more meaningful way- to expend data features by fetching audio features for all the tracks from Spotify Web API.</i>

# ## &#8545;.  Fetch Audio Features for Tracks from Spotify Web API

# <b>* This step shows every detail of how I fetched audio features for tracks from Spotify Web API. It would take hours to run through this step since Spotify allows us to fetch data for at most 50 tracks at a time. Data obtained from this step has been saved. We could move forward to step &#8546; directly if we do not want to get stuck here too long.</b>

# In[ ]:


"""
In order to use Spotify API to fetch data, we need to set our Spotify API credentials, 
which means to register an app on Spotify website first. I have done that outside the 
notebook, so now we have the needed environment variables, as below: 
    SPOTIPY_CLIENT_ID='9b89bceb41094be298505c3970a11bcc'
    SPOTIPY_CLIENT_SECRET='bbfd5570092b4e09b88e83e744f7e848'
    SPOTIPY_REDIRECT_URI='http://google.com/'
"""

"""
Spotify would give their users instant IDs when requested. Remember that those IDs will 
be valid only for an hour. To request your instant ID: 
    go to Spotify player-> log in your Spotify account-> click on your profile image
    -> get an ID by clicking 'Copy Profile Link' under '...'
"""

# Here's my instant profile link: 
# https://open.spotify.com/user/31z2m2i3pqszfsroulu63g7bc3hu?si=c_eLRG0qT3STuJEFN1tylQ
user_id = '31z2m2i3pqszfsroulu63g7bc3hu?si=c_eLRG0qT3STuJEFN1tylQ'
token = util.prompt_for_user_token(user_id, 
                                   client_id='9b89bceb41094be298505c3970a11bcc', 
                                   client_secret='bbfd5570092b4e09b88e83e744f7e848',
                                   redirect_uri='http://google.com/')
spotify_obj = spotipy.Spotify(auth=token)


# In[ ]:


"""Fetch audio features for a track with its url and have a
general picture of what audio features there are"""

# Get url of the first track
url = df_data['URL'][0]

# Fetch audio features of the first track
spotify_obj.audio_features(url)


# <i>For more information of what these audio feature names stand for, check <a href='https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/'>this</a> out.</i>

# In[ ]:


# Check how many NaNs there are
df_data.isnull().sum()


# <i>From the output, we know that there are 8 NaNs in the 'URL' column. If we try to use these NaNs as URLs to fetch data with Spotify API, errors would be thrown. We thus have to deal with NaNs for the 'URL' column first.</i>

# In[ ]:


# Replace NaNs with ''
df_data_2 = df_data.fillna(value={'URL': ''})

df_data_2.isnull().sum()


# In[ ]:


"""Fetch audio features for all tracks"""

audio_features = []
for i in range(0, len(df_data), 50):
    if i == 0:
        print("Fetching audio features...")
        print()
    while True:
        try:
            # Spotify API allows at most 50 tracks to fetch audio features at a time
            audio_features += spotify_obj.audio_features(df_data_2['URL'][i:i+50].values.tolist())
            if i % 300000 == 0 and i != 0:
                print(f"Done for {i} tracks!")
            break
        except:
            print()
            # Get user ID renewed when it's expired in a hour
            user_id = input("Enter new user ID to get access token refreshed: ")
            token = util.prompt_for_user_token(user_id, 
                                            client_id='9b89bceb41094be298505c3970a11bcc', 
                                            client_secret='bbfd5570092b4e09b88e83e744f7e848',
                                            redirect_uri='http://google.com/')
            spotify_obj = spotipy.Spotify(auth=token)
print()
print("Done for all tracks!")


# In[ ]:


"""We got None objects in audio_feature when URLs were invalid. 
Those Nones would be big trouble if we constructed a DataFrame 
object with audio_feature directly. So replace them first"""

# Replace None in audio_features with {}
audio_features_2 = [{} if item is None else item for item in audio_features]


# In[ ]:


# Construct a DataFrame object with audio_feature_2
df_audio_features = pd.DataFrame(audio_features_2)

print(df_audio_features.shape)
df_audio_features.head()


# In[ ]:


"""Save audio features as CSV to current path"""  

# c_path = DirextoryToSaveAudioFeatures
df_audio_features.to_csv(f'{c_path}/audio_features.csv')


# ## &#8546;. Split Data into Train-Valid-Test Sets

# In[ ]:


"""Read data in again & Integrate audio features into the original dataset. 
we will be only using the integrated dataset from here throughout to the end"""

df_af = pd.read_csv(f'../input/audio-featurescsv/audio_features.csv', index_col=0)
df_data_with_af = pd.concat([df_data, df_af], axis=1)
df_data_with_af.sort_values(by=['Date', 'Region'], inplace=True)

print(df_data_with_af.shape)
df_data_with_af.head(3)


# In[ ]:


"""In order to go through every step needed to build machine learning models, 
we will be using a subset of df_data_with_af. This is totally out of consideration
of running speed. Comment codes in this box if we want to see what would be like 
with the whole dataset."""

df_data_with_af = df_data_with_af[:441197]

print(df_data_with_af.shape)


# In[ ]:


"""Seperate out X and y"""

y_data_with_af = df_data_with_af['Streams']
X_data_with_af = df_data_with_af.drop(['Streams'], axis=1)

print(X_data_with_af.shape, y_data_with_af.shape)


# In[ ]:


"""Split data into train-valid set and test set"""

(X_train_valid, X_test, y_train_valid, y_test) = train_test_split(X_data_with_af, 
                                                                  y_data_with_af, 
                                                                  test_size=0.12, 
                                                                  shuffle=False)

print('Shape:')
print('Train-Valid Set -', X_train_valid.shape, y_train_valid.shape)
print('Test Set -', X_test.shape, y_test.shape)


# ## &#8547;. Preprocess Data for Train-Valid Sets

# In[ ]:


"""Define some functions for data preprocessing for later use"""

def split_date(df, date_column):
    """Function to split df[date_column] into four other date relevant columns
       df: a DataFrame object
       data_column: name of the column with datetime64 dtype - str
    """
    df = df.copy()
    date_df = pd.DataFrame({"year": df[date_column].dt.year,
                            "month": df[date_column].dt.month,
                            "day": df[date_column].dt.day,
                            "dayofweek": df[date_column].dt.dayofweek,
             })
    df = df.drop(date_column, axis=1)
    df = pd.concat([df, date_df], axis=1)
    return df

def convert_cat_to_num(df, feature, mapping=None):
    """Function to convert object dtype data in df[feature] to numerical values
       df: a DateFrame object
       feature: a feature of the df - str
       mapping: categories and their mapping values - None/dict 
    """
    df = df.copy()
    cats_list = df[feature].astype('category').cat.categories.tolist()
    if mapping is None:
        mapping = {k: v for k, v in zip(cats_list, list(range(1, len(cats_list) + 1)))}
        
    else:
        new_cats_list = []
        for c in cats_list:
            if c not in mapping:
                new_cats_list.append(c)
        start = len(mapping) + 1
        mapping.update({k: v for k, v in zip(new_cats_list, list(range(start, len(new_cats_list) + start)))})
                                    
    df[feature] = df[feature].map(mapping)
    return df, mapping   


# In[ ]:


"""Drop columns that intuitively have nothing to do with Streams- We also throw 
the 'Position' column since 'Position' is the ranking of tracks, which won't be 
known until 'Streams' is available"""

X_train_valid_2 = X_train_valid.drop(['Position', 'URL', 'analysis_url', 'id', 'track_href', 'type', 'uri'], axis=1)


# In[ ]:


"""Split 'Data' column"""

X_train_valid_3 = split_date(X_train_valid_2, 'Date')

X_train_valid_3.tail(3)


# In[ ]:


X_train_valid_3.info()


# In[ ]:


"""Convert data of object dtype to numerical values"""

X_train_valid_4, track_name_map = convert_cat_to_num(X_train_valid_3, 'Track Name')
X_train_valid_4, artist_map = convert_cat_to_num(X_train_valid_4, 'Artist')
X_train_valid_4, region_map = convert_cat_to_num(X_train_valid_4, 'Region')

X_train_valid_4.info()


# In[ ]:


X_train_valid_4.isnull().sum()


# In[ ]:


"""Deal with NaNs"""

X_train_valid_5 = X_train_valid_4.fillna(0)


# In[ ]:


"""Standardize continuous variables"""

# scaler = MinMaxScaler()
scaler = StandardScaler()

con_cols = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness',
       'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']
X_train_valid_5[con_cols] = scaler.fit_transform(X_train_valid_5[con_cols])

X_train_valid_5.head()


# In[ ]:


"""Split train-valid set into training set and validation set"""

X_train, X_valid, y_train, y_valid = train_test_split(X_train_valid_5, 
                                                      y_train_valid, 
                                                      train_size=0.85, 
                                                      shuffle=False)

print('Shape:')
print('Train Set -', X_train.shape, y_train.shape)
print('Validation Set -', X_valid.shape, y_valid.shape)


# ## &#8548;. Build Models with Random Forests & Neural Networks

# ### - Random Forests Model(Hyper-parameter Tuning Included)

# In[ ]:


"""Tune parameters with multiple for-loops"""

max_features = ["auto", "sqrt", "log2", None]
n_estimators = [50, 100, 250]

combination_rf = []
r2_result_rf = []

for m in max_features:
    for n in n_estimators:
        combination_rf.append(str(m)+"/"+str(n))
        rfr = RandomForestRegressor(n_jobs=-1, max_features=m, n_estimators=n)
        rfr.fit(X_train, y_train)
        r2_result_rf.append(rfr.score(X_valid, y_valid))
        
r2_result_rf_df = pd.DataFrame({"combination": combination_rf, "vld_r2_rf": r2_result_rf})

r2_result_rf_df


# In[ ]:


"""Plot max_features/n_estimators vs r2 score on validation set"""

plt.figure(figsize=(8, 3), dpi=80)
axes = plt.gca()
axes.set_ylim([0.94, 1.0])
# axes.set_xlim([0, 12])
plt.stem(r2_result_rf_df.index, r2_result_rf_df["vld_r2_rf"])
plt.xticks(np.arange(12))
plt.xlabel('combination')
plt.ylabel('r2')
plt.show()


# In[ ]:


"""Find the best max_features/n_estimators combination"""

rsq_max = max(r2_result_rf)
index = r2_result_rf.index(rsq_max)

print('vld_rsq maximum:', rsq_max, 'index:', index)
print('Best max_features/n_estimators:', combination_rf[index])


# In[ ]:


"""Build a random forests model with the best max_features/n_estimators combination"""

rf_model = RandomForestRegressor(n_jobs=-1, max_features='auto', n_estimators=250)
rf_model.fit(X_train, y_train)


# In[ ]:


'''Plot importance scores of data features'''

plt.figure(figsize=(10, 5))
rf_model.feature_importances_
feat_imps = pd.DataFrame(rf_model.feature_importances_, index = X_train.columns,
            columns=['Importance score']).sort_values('Importance score', ascending=False)

feat_imps = feat_imps.reset_index()
feat_imps.columns = ["Feature", "Importance Score"]
sns.barplot(x="Importance Score", y="Feature", data=feat_imps, orient="h")


# In[ ]:


"""Drop those columns with little importance"""

X_train_final = X_train.drop(['year', 'time_signature', 'dayofweek', 'mode', 'month'], axis=1)
X_valid_final = X_valid.drop(['year', 'time_signature', 'dayofweek', 'mode', 'month'], axis=1)

print(X_train_final.shape, X_valid_final.shape)


# In[ ]:


"""Retrain the random forests model with ultimate training dataset"""

rf_model.fit(X_train_final, y_train)


# ### - Neural Networks Model

# In[ ]:


"""Build a deep neural networks model"""

dnn_model = Sequential()
dnn_model.add(Dense(23, input_dim=15, kernel_initializer='normal', activation='relu'))
dnn_model.add(Dense(15, kernel_initializer='normal', activation='relu'))
dnn_model.add(Dense(9, kernel_initializer='normal', activation='relu'))
# dnn_model.add(Dense(4, kernel_initializer='normal', activation='relu'))
dnn_model.add(Dense(1, kernel_initializer='normal'))

dnn_model.compile(loss='mse', optimizer='Adam', metrics=['mse'])
history = dnn_model.fit(X_train_final, y_train, validation_data=(X_valid_final, y_valid), 
                        nb_epoch=100, batch_size=2000)


# In[ ]:


"""Plot epoch vs training set mse & epoch vs validation set mse"""

plt.figure(figsize=(10, 4), dpi=80)
plt.plot(history.history['mean_squared_error'])
plt.plot(history.history['val_mean_squared_error'])
plt.title('Model Mean Squared Error')
plt.ylabel('MSE')
plt.xlabel('Epoch')
plt.legend(['train', 'valid'], loc='upper left')
plt.show()


# ## &#8549;. Test out Models on Test Set

# In[ ]:


print(X_test.shape)
X_test.head()


# <i>Next, we should preprocess test set data exactly the same way we did for training set data and 
# validation set data, except that we use those maps we got earlier when converting object dtype data to numerical values.</i>

# In[ ]:


"""Preprocess test set data"""

# Drop columns that intuitively wouldn't be helpful 
X_test_2 = X_test.drop(['Position', 'URL', 'analysis_url', 'id', 'track_href', 'type', 'uri'], axis=1)

# Split the 'Data' column
X_test_3 = split_date(X_test_2, 'Date')

# Convert object dtype data to numerical values with those maps we got earlier
X_test_4, _ = convert_cat_to_num(X_test_3, 'Track Name', track_name_map)
X_test_4, _ = convert_cat_to_num(X_test_4, 'Artist', artist_map)
X_test_4, _ = convert_cat_to_num(X_test_4, 'Region', region_map)

# Deal with NaNs
X_test_5 = X_test_4.fillna(0)

# Standardize continuous variables
X_test_5[con_cols] = scaler.transform(X_test_5[con_cols])

# Drop columns with little importance
X_test_final = X_test_5.drop(['year', 'time_signature', 'dayofweek', 'mode', 'month'], axis=1)

X_test_final.head()


# <b>Testing...</b>

# In[ ]:


"""Test the random forests model"""

y_vld_pre_rf = rf_model.predict(X_valid_final)
r2_trn_rf = r2_score(y_valid, y_vld_pre_rf)
mse_trn_rf = mean_squared_error(y_valid, y_vld_pre_rf)

y_tst_pre_rf = rf_model.predict(X_test_final)
r2_tst_rf = r2_score(y_test, y_tst_pre_rf)
mse_tst_rf = mean_squared_error(y_test, y_tst_pre_rf)

print('Random Forests Model:')
print('r2 on training set:', r2_trn_rf)
print('mse on training set:', mse_trn_rf)
print('r2 on test set:', r2_tst_rf)
print('mse on test set:', mse_tst_rf)


# In[ ]:


"""Test the neural networks model"""

y_vld_pre_dnn = dnn_model.predict(X_valid_final)
r2_trn_dnn = r2_score(y_valid, y_vld_pre_dnn)
mse_trn_dnn = mean_squared_error(y_valid, y_vld_pre_dnn)

y_tst_pre_dnn = dnn_model.predict(X_test_final)
r2_tst_dnn = r2_score(y_test, y_tst_pre_dnn)
mse_tst_dnn = mean_squared_error(y_test, y_tst_pre_dnn)

print('Neural Networks Model:')
print('r2 on training set:', r2_trn_dnn)
print('mse on training set:', mse_trn_dnn)
print('r2 on test set:', r2_tst_dnn)
print('mse on test set:', mse_tst_dnn)

