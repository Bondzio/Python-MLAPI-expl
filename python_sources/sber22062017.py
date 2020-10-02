import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
import datetime
from sklearn import model_selection, preprocessing

train = pd.read_csv('../input/train.csv', parse_dates=['timestamp'])
test = pd.read_csv('../input/test.csv', parse_dates=['timestamp'])
macro = pd.read_csv('../input/macro.csv', parse_dates=['timestamp'])


rng = np.random.RandomState(1)

bad_index = train[train.life_sq > train.full_sq].index
train.ix[bad_index, "life_sq"] = np.NaN

equal_index = [601,1896,2791]
test.ix[equal_index, "life_sq"] = test.ix[equal_index, "full_sq"]

bad_index = test[test.life_sq > test.full_sq].index
test.ix[bad_index, "life_sq"] = np.NaN

bad_index = train[train.life_sq < 5].index
train.ix[bad_index, "life_sq"] = np.NaN

bad_index = test[test.life_sq < 5].index
test.ix[bad_index, "life_sq"] = np.NaN

bad_index = train[train.full_sq < 5].index
train.ix[bad_index, "full_sq"] = np.NaN

bad_index = test[test.full_sq < 5].index
test.ix[bad_index, "full_sq"] = np.NaN

kitch_is_build_year = [13117]
train.ix[kitch_is_build_year, "build_year"] = train.ix[kitch_is_build_year, "kitch_sq"]

bad_index = train[train.kitch_sq >= train.life_sq].index
train.ix[bad_index, "kitch_sq"] = np.NaN

bad_index = test[test.kitch_sq >= test.life_sq].index
test.ix[bad_index, "kitch_sq"] = np.NaN

bad_index = train[(train.kitch_sq == 0).values + (train.kitch_sq == 1).values].index
train.ix[bad_index, "kitch_sq"] = np.NaN

bad_index = test[(test.kitch_sq == 0).values + (test.kitch_sq == 1).values].index
test.ix[bad_index, "kitch_sq"] = np.NaN

bad_index = train[(train.full_sq > 210) * (train.life_sq / train.full_sq < 0.3)].index
train.ix[bad_index, "full_sq"] = np.NaN

bad_index = test[(test.full_sq > 150) * (test.life_sq / test.full_sq < 0.3)].index
test.ix[bad_index, "full_sq"] = np.NaN

bad_index = train[train.life_sq > 300].index
train.ix[bad_index, ["life_sq", "full_sq"]] = np.NaN

bad_index = test[test.life_sq > 200].index
test.ix[bad_index, ["life_sq", "full_sq"]] = np.NaN

bad_index = train[train.build_year < 1500].index
train.ix[bad_index, "build_year"] = np.NaN

bad_index = test[test.build_year < 1500].index
test.ix[bad_index, "build_year"] = np.NaN

bad_index = train[train.num_room == 0].index 
train.ix[bad_index, "num_room"] = np.NaN

bad_index = test[test.num_room == 0].index 
test.ix[bad_index, "num_room"] = np.NaN

bad_index = [10076, 11621, 17764, 19390, 24007, 26713, 29172]
train.ix[bad_index, "num_room"] = np.NaN

bad_index = [3174, 7313]
test.ix[bad_index, "num_room"] = np.NaN

bad_index = train[(train.floor == 0).values * (train.max_floor == 0).values].index
train.ix[bad_index, ["max_floor", "floor"]] = np.NaN

bad_index = train[train.floor == 0].index
train.ix[bad_index, "floor"] = np.NaN

bad_index = train[train.max_floor == 0].index
train.ix[bad_index, "max_floor"] = np.NaN

bad_index = test[test.max_floor == 0].index
test.ix[bad_index, "max_floor"] = np.NaN

bad_index = train[train.floor > train.max_floor].index
train.ix[bad_index, "max_floor"] = np.NaN

bad_index = test[test.floor > test.max_floor].index
test.ix[bad_index, "max_floor"] = np.NaN

bad_index = [23584]
train.ix[bad_index, "floor"] = np.NaN

bad_index = train[train.state == 33].index
train.ix[bad_index, "state"] = np.NaN

train.loc[train.full_sq == 0, 'full_sq'] = 50
train = train[train.price_doc/train.full_sq <= 600000]
train = train[train.price_doc/train.full_sq >= 10000]

# Add month-year
month_year = (train.timestamp.dt.month + train.timestamp.dt.year * 100)
month_year_cnt_map = month_year.value_counts().to_dict()
train['month_year_cnt'] = month_year.map(month_year_cnt_map)

month_year = (test.timestamp.dt.month + test.timestamp.dt.year * 100)
month_year_cnt_map = month_year.value_counts().to_dict()
test['month_year_cnt'] = month_year.map(month_year_cnt_map)

# Add week-year count
week_year = (train.timestamp.dt.weekofyear + train.timestamp.dt.year * 100)
week_year_cnt_map = week_year.value_counts().to_dict()
train['week_year_cnt'] = week_year.map(week_year_cnt_map)

week_year = (test.timestamp.dt.weekofyear + test.timestamp.dt.year * 100)
week_year_cnt_map = week_year.value_counts().to_dict()
test['week_year_cnt'] = week_year.map(week_year_cnt_map)

# Add month and day-of-week
train['month'] = train.timestamp.dt.month
train['dow'] = train.timestamp.dt.dayofweek

test['month'] = test.timestamp.dt.month
test['dow'] = test.timestamp.dt.dayofweek

# Other feature engineering
train['rel_floor'] = train['floor'] / train['max_floor'].astype(float)
train['rel_kitch_sq'] = train['kitch_sq'] / train['full_sq'].astype(float)

test['rel_floor'] = test['floor'] / test['max_floor'].astype(float)
test['rel_kitch_sq'] = test['kitch_sq'] / test['full_sq'].astype(float)

train.apartment_name=train.sub_area + train['metro_km_avto'].astype(str)
test.apartment_name=test.sub_area + train['metro_km_avto'].astype(str)

train['room_size'] = train['life_sq'] / train['num_room'].astype(float)
test['room_size'] = test['life_sq'] / test['num_room'].astype(float)


#x_train = train.drop(["id", "timestamp", "price_doc"], axis=1)
#x_test = test.drop(["id", "timestamp"], axis=1)

my_macro=macro[[]]
my_train=train.join(my_macro,on='timestamp')
my_test=test.join(my_macro,on='timestamp')


id_test=my_test.id
y_train=my_train.price_doc
train_df = my_train.drop(["id", "timestamp", "price_doc"], axis=1)
test_df = my_test.drop(["id", "timestamp"], axis=1)


num_train = len(train_df)
x_all = pd.concat([train_df, test_df])

for c in x_all.columns:
    if x_all[c].dtype == 'object':
        lbl = preprocessing.LabelEncoder()
        lbl.fit(list(x_all[c].values))
        x_all[c] = lbl.transform(list(x_all[c].values))
        #x_train.drop(c,axis=1,inplace=True)

x_train = x_all[:num_train]
x_test = x_all[num_train:]




regr_2 = DecisionTreeRegressor()

x_train.fillna(x_train.median(),inplace=True)
x_test.fillna(x_test.median(),inplace=True)

regr_2.fit(x_train,y_train)


y_predict2 = regr_2.predict(x_test)

y_predict2= np.round(y_predict2)

output2 = pd.DataFrame(y_predict2)

output2.to_csv('y.csv')

