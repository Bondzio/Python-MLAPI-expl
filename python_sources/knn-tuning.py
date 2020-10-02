#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from itertools import product, combinations
import gc

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from sklearn.ensemble import (RandomForestClassifier
                              , RandomForestRegressor
                              , ExtraTreesClassifier
                             )
from sklearn.neighbors import KNeighborsClassifier
from mlxtend.classifier import StackingCVClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

rand_state = 719


# # Load Data

# In[ ]:


data_path = '/kaggle/input/learn-together/'
def reload(x):
    return pd.read_csv(data_path + x, index_col = 'Id')

train = reload('train.csv')
n_train = len(train)
test = reload('test.csv')
n_test = len(test)

index_test = test.index.copy()
y_train = train.Cover_Type.copy()

all_data = train.iloc[:,train.columns != 'Cover_Type'].append(test)
all_data['train'] = [1]*n_train + [0]*n_test

del train
del test


# # Impute "Fake" 0s

# In[ ]:


questionable_0 = ['Hillshade_9am', 'Hillshade_3pm']

corr_cols = {'Hillshade_9am': ['Hillshade_3pm', 'Aspect', 'Slope', 'Soil_Type10', 'Wilderness_Area1'
                               ,'Wilderness_Area4', 'Vertical_Distance_To_Hydrology']
            , 'Hillshade_3pm': ['Hillshade_9am', 'Hillshade_Noon', 'Slope', 'Aspect']
            }


# In[ ]:


rfr = RandomForestRegressor(n_estimators = 100, random_state = rand_state, verbose = 1, n_jobs = -1)

# for col in questionable_0: 
#     print('='*20)
#     scores = cross_val_score(rfr,
#                              all_data_non0[corr_cols[col]], 
#                              all_data_non0[col],
#                              n_jobs = -1)
#     print(col + ': {0:.4} (+/- {1:.4}) ## [{2}]'.format(scores.mean(), scores.std()*2, ', '.join(map(str, np.round(scores,4)))))

# ====================
# Hillshade_9am: 1.0 (+/- 0.00056) ## [0.9995, 0.9993, 0.9988]
# ====================
# Hillshade_3pm: 1.0 (+/- 0.0029) ## [0.9981, 0.9971, 0.9947]

## NEAR PERFECT SCORES FOR ALL => no need further feature engineering for questionable_0 predictions


# In[ ]:


for col in questionable_0:
    print('='*20)
    print(col)
    all_data_0 = all_data[all_data[col] == 0].copy()
    all_data_non0 = all_data[all_data[col] != 0].copy()
    rfr.fit(all_data_non0[corr_cols[col]], all_data_non0[col])
    pred = rfr.predict(all_data_0[corr_cols[col]])
    pred_col = 'predicted_{}'.format(col)
    
    all_data[pred_col] = all_data[col].copy()
    all_data.loc[all_data_0.index, pred_col] = pred

for col in questionable_0:
    all_data['predicted_{}'.format(col)] = all_data['predicted_{}'.format(col)].apply(int)


# # Other Features
# ### Aspect, Slope & Shadow

# In[ ]:


def aspect_slope(df):
    df['AspectSin'] = np.sin(np.radians(df.Aspect))
    df['AspectCos'] = np.cos(np.radians(df.Aspect))
    df['AspectSin_Slope'] = df.AspectSin * df.Slope
    df['AspectCos_Slope'] = df.AspectCos * df.Slope
    df['AspectSin_Slope_Abs'] = np.abs(df.AspectSin_Slope)
    df['AspectCos_Slope_Abs'] = np.abs(df.AspectCos_Slope)
    df['Hillshade_Mean'] = df[['Hillshade_9am',
                              'Hillshade_Noon',
                              'Hillshade_3pm']].apply(np.mean, axis = 1)
    return df


# ### Distances & Elevation

# In[ ]:


def distances(df):
    horizontal = ['Horizontal_Distance_To_Fire_Points', 
                  'Horizontal_Distance_To_Roadways',
                  'Horizontal_Distance_To_Hydrology']
    
    df['Euclidean_to_Hydrology'] = np.sqrt(df['Horizontal_Distance_To_Hydrology']**2 + df['Vertical_Distance_To_Hydrology']**2)
    df['EuclidHydro_Slope'] = df.Euclidean_to_Hydrology * df.Slope
    df['Elevation_VDH_sum'] = df.Elevation + df.Vertical_Distance_To_Hydrology
    df['Elevation_VDH_diff'] = df.Elevation - df.Vertical_Distance_To_Hydrology
    df['Elevation_2'] = df.Elevation**2
    df['Elevation_3'] = df.Elevation**3
    df['Elevation_log1p'] = np.log1p(df.Elevation) # credit: https://www.kaggle.com/evimarp/top-6-roosevelt-national-forest-competition/notebook
    
    for col1, col2 in combinations(zip(horizontal, ['HDFP', 'HDR', 'HDH']), 2):
        df['{0}_{1}_diff'.format(col1[1], col2[1])] = df[col1[0]] - df[col2[0]]
        df['{0}_{1}_sum'.format(col1[1], col2[1])] = df[col1[0]] + df[col2[0]]
    
    df['Horizontal_sum'] = df[horizontal].sum(axis = 1)
    return df


# ### Categorical

# In[ ]:


def OHE_to_cat(df, colname, data_range): # data_range = [min_index, max_index+1]
    df[colname] = sum([i * df[colname + '{}'.format(i)] for i in range(data_range[0], data_range[1])])
    return df


# ### Rockiness

# In[ ]:


soils = [
    [7, 15, 8, 14, 16, 17,
     19, 20, 21, 23], #unknow and complex 
    [3, 4, 5, 10, 11, 13],   # rubbly
    [6, 12],    # stony
    [2, 9, 18, 26],      # very stony
    [1, 24, 25, 27, 28, 29, 30,
     31, 32, 33, 34, 36, 37, 38, 
     39, 40, 22, 35], # extremely stony and bouldery
]
soil_dict = {}
for index, soil_group in enumerate(soils):
    for soil in soil_group:
        soil_dict[soil] = index

def rocky(df):
    df['Rocky'] = sum(i * df['Soil_Type' + str(i)] for i in range(1,41))
    df['Rocky'] = df['Rocky'].map(soil_dict)
    return df


# ## Summary and Output

# In[ ]:


all_data = aspect_slope(all_data)
all_data = distances(all_data)
all_data = OHE_to_cat(all_data, 'Wilderness_Area', [1,5])
all_data = OHE_to_cat(all_data, 'Soil_Type', [1,41])
all_data = rocky(all_data)
all_data.drop(['Soil_Type7', 'Soil_Type15', 'train'] + questionable_0, axis = 1, inplace = True)


# In[ ]:


X_train = all_data.iloc[:n_train,:].copy()
X_test = all_data.iloc[n_train:, :].copy()
del all_data

def mem_reduce(df):
    # credit: https://www.kaggle.com/arateris/2-layer-k-fold-learning-forest-cover
    start_mem = df.memory_usage().sum() / 1024.0**2
    for col in df.columns:
        if df[col].dtype=='float64': 
            df[col] = df[col].astype('float32')
        if df[col].dtype=='int64': 
            if df[col].max()<1: df[col] = df[col].astype(bool)
            elif df[col].max()<128: df[col] = df[col].astype('int8')
            elif df[col].max()<32768: df[col] = df[col].astype('int16')
            else: df[col] = df[col].astype('int32')
    end_mem = df.memory_usage().sum() / 1024**2
    print('Reduce from {0:.3f} MB to {1:.3f} MB (decrease by {2:.2f}%)'.format(start_mem, end_mem, 
                                                                (start_mem - end_mem)/start_mem*100))
    return df

X_train = mem_reduce(X_train)
print('='*10)
X_test=mem_reduce(X_test)
gc.collect()


# In[ ]:


# Important columns: https://www.kaggle.com/hoangnguyen719/beginner-eda-and-feature-engineering
important_cols = ['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology'
                  , 'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways'
                  , 'Hillshade_Noon', 'Horizontal_Distance_To_Fire_Points', 'Wilderness_Area1'
                  , 'Wilderness_Area3', 'Wilderness_Area4', 'Soil_Type3', 'Soil_Type4', 'Soil_Type10'
                  , 'predicted_Hillshade_9am', 'predicted_Hillshade_3pm', 'AspectSin', 'AspectCos'
                  , 'AspectSin_Slope', 'AspectCos_Slope', 'AspectSin_Slope_Abs', 'AspectCos_Slope_Abs'
                  , 'Hillshade_Mean', 'Euclidean_to_Hydrology', 'EuclidHydro_Slope'
                  , 'Elevation_VDH_sum', 'Elevation_VDH_diff', 'Elevation_2', 'Elevation_3'
                  , 'Elevation_log1p', 'HDFP_HDR_diff', 'HDFP_HDR_sum', 'HDFP_HDH_diff'
                  , 'HDFP_HDH_sum', 'HDR_HDH_diff', 'HDR_HDH_sum', 'Horizontal_sum'
                  , 'Wilderness_Area', 'Soil_Type', 'Rocky'
                 ]


# ### Search params

# In[ ]:


# params = {'n_neighbors':[1,3,5,10,15,20]
#           , 'algorithm': ['ball_tree', 'kd_tree', 'brute']
#           , 'leaf_size': [1, 3, 5, 10, 15, 30]
#           , 'weights': ['uniform', 'distance']
#           , 'p': [1,2]
#          }
# knn = KNeighborsClassifier()
# grid_imp = GridSearchCV(estimator=knn
#                    , param_grid = params
#                    , scoring = 'accuracy'
#                    , n_jobs = -1
#                    , cv = 3
#                    , verbose = 0
#                    )
# grid_imp.fit(X_train[important_cols], y_train)

# grid_all = GridSearchCV(estimator=knn
#                    , param_grid = params
#                    , scoring = 'accuracy'
#                    , n_jobs = -1
#                    , cv = 3
#                    , verbose = 0
#                    )
# grid_all.fit(X_train, y_train)


# #### Important cols

# In[ ]:


# def extract_params(output, params_dict):
#     for key in params_dict.keys():
#         output[key] = output.params.apply(lambda x: x[key])
#     return output

# for cols, model in [('Important_cols', grid_imp)
#                    , ('All_cols', grid_all)
#                    ]:
#     print('='*10 + cols + '='*10)
#     print('Best hyper-parameters found:')
#     print(model.best_params_)
#     print('\nFitting time:')
#     print(model.refit_time_)
#     print('\Best score:')
#     print(round(model.best_score_,3))
#     results = pd.DataFrame(model.cv_results_)
#     results = results.sort_values(by=['rank_test_score'])


#     results = extract_params(results, params)
#     print(results[list(params.keys()) + ['mean_test_score']].head(10))
#     print('='*30)
    
# ##### OUTPUT #######
# ==========Important_cols==========
# Best hyper-parameters found:
# {'algorithm': 'ball_tree', 'leaf_size': 1, 'n_neighbors': 15, 'p': 2, 'weights': 'distance'}

# Fitting time:
# 0.05556893348693848
# \Best score:
# 0.521
#      n_neighbors  algorithm  leaf_size   weights  p  mean_test_score
# 235           15    kd_tree         10  distance  2         0.520833
# 187           15    kd_tree          3  distance  2         0.520833
# 331           15      brute          3  distance  2         0.520833
# 43            15  ball_tree          3  distance  2         0.520833
# 163           15    kd_tree          1  distance  2         0.520833
# 259           15    kd_tree         15  distance  2         0.520833
# 355           15      brute          5  distance  2         0.520833
# 307           15      brute          1  distance  2         0.520833
# 211           15    kd_tree          5  distance  2         0.520833
# 379           15      brute         10  distance  2         0.520833
# ==============================
# ==========All_cols==========
# Best hyper-parameters found:
# {'algorithm': 'ball_tree', 'leaf_size': 1, 'n_neighbors': 15, 'p': 2, 'weights': 'distance'}

# Fitting time:
# 0.10615134239196777
# \Best score:
# 0.521
#      n_neighbors  algorithm  leaf_size   weights  p  mean_test_score
# 67            15  ball_tree          5  distance  2         0.520833
# 355           15      brute          5  distance  2         0.520833
# 163           15    kd_tree          1  distance  2         0.520833
# 307           15      brute          1  distance  2         0.520833
# 91            15  ball_tree         10  distance  2         0.520833
# 19            15  ball_tree          1  distance  2         0.520833
# 43            15  ball_tree          3  distance  2         0.520833
# 379           15      brute         10  distance  2         0.520833
# 187           15    kd_tree          3  distance  2         0.520833
# 139           15  ball_tree         30  distance  2         0.520833
# ==============================


# In[ ]:


knn = KNeighborsClassifier(n_neighbors = 15
                          , algorithm = 'ball_tree'
                          , leaf_size = 1
                          , p = 2
                          , weights = 'distance'
                          )
knn.fit(X_train[important_cols], y_train)


# ### Output for submission

# In[ ]:


predict = knn.predict(X_test[important_cols])


# In[ ]:


output = pd.DataFrame({'Id': index_test
                       ,'Cover_Type': predict
                      })
output.to_csv('Submission.csv', index=False)

