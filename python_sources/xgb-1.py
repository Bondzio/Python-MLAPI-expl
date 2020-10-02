import numpy as np
import pandas as pd
from scipy import sparse
import xgboost as xgb
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import log_loss
from sklearn.feature_extraction.text import CountVectorizer
import datetime as dt

train_df = pd.read_json("../input/train.json")
test_df = pd.read_json("../input/test.json")

def runXGB(train_X, train_y, test_X, test_y=None, feature_names=None, seed_val=321, num_rounds=2000):
    param = {}
    param['objective'] = 'multi:softprob'
    param['eta'] = 0.02
    param['max_depth'] = 6
    param['silent'] = 1
    param['num_class'] = 3
    param['eval_metric'] = "mlogloss"
    param['min_child_weight'] = 1
    param['subsample'] = 0.7
    param['colsample_bytree'] = 0.7
    param['seed'] = seed_val
    num_rounds = num_rounds

    plst = list(param.items())
    xgtrain = xgb.DMatrix(train_X, label=train_y)

    if test_y is not None:
        xgtest = xgb.DMatrix(test_X, label=test_y)
        watchlist = [ (xgtrain,'train'), (xgtest, 'test') ]
        model = xgb.train(plst, xgtrain, num_rounds, watchlist, early_stopping_rounds=20)
    else:
        xgtest = xgb.DMatrix(test_X)
        model = xgb.train(plst, xgtrain, num_rounds)

    pred_test_y = model.predict(xgtest)
    return pred_test_y, model

print (" feature enginnering ....")

test_df["bathrooms"].loc[19671] = 1.5
test_df["bathrooms"].loc[22977] = 2.0
test_df["bathrooms"].loc[63719] = 2.0
train_df["price"] = train_df["price"].clip(upper=13000)

train_df["logprice"] = np.log(train_df["price"])
test_df["logprice"] = np.log(test_df["price"])

train_df["price_t"] = train_df["price"]/train_df["bedrooms"]
test_df["price_t"] = test_df["price"]/test_df["bedrooms"] 

train_df["room_sum"] = train_df["bedrooms"]+train_df["bathrooms"] 
test_df["room_sum"] = test_df["bedrooms"]+test_df["bathrooms"] 

train_df['price_per_room'] = train_df['price']/train_df['room_sum']
test_df['price_per_room'] = test_df['price']/test_df['room_sum']

train_df["num_photos"] = train_df["photos"].apply(len)
test_df["num_photos"] = test_df["photos"].apply(len)

train_df["num_features"] = train_df["features"].apply(len)
test_df["num_features"] = test_df["features"].apply(len)

train_df["num_description_words"] = train_df["description"].apply(lambda x: len(x.split(" ")))
test_df["num_description_words"] = test_df["description"].apply(lambda x: len(x.split(" ")))

train_df["created"] = pd.to_datetime(train_df["created"])
test_df["created"] = pd.to_datetime(test_df["created"])
train_df["created_year"] = train_df["created"].dt.year
test_df["created_year"] = test_df["created"].dt.year
train_df["created_month"] = train_df["created"].dt.month
test_df["created_month"] = test_df["created"].dt.month
train_df["created_day"] = train_df["created"].dt.day
test_df["created_day"] = test_df["created"].dt.day
train_df['created_weekday'] = train_df['created'].dt.weekday
test_df['created_weekday'] = test_df['created'].dt.weekday
train_df['created_quarter'] = train_df['created'].dt.quarter
test_df['created_quarter'] = test_df['created'].dt.quarter
train_df['created_week'] = train_df['created'].dt.week
test_df['created_week'] = test_df['created'].dt.week
train_df['is_weekend'] = (train_df['created_weekday'] == 5) & (train_df['created_weekday'] == 6)
test_df['is_weekend'] = (test_df['created_weekday'] == 5) & (test_df['created_weekday'] == 6)
train_df['is_weekday'] = (train_df['created_weekday'] != 5) & (train_df['created_weekday'] != 6)
test_df['is_weekday'] = (test_df['created_weekday'] != 5) & (test_df['created_weekday'] == 6)
train_df["created_hour"] = train_df["created"].dt.hour
test_df["created_hour"] = test_df["created"].dt.hour
train_df['created_min'] = train_df['created'].dt.minute
test_df['created_min'] = test_df['created'].dt.minute
train_df['created_sec'] = train_df['created'].dt.second
test_df['created_sec'] = test_df['created'].dt.second
train_df['created'] = train_df['created'].map(lambda x : (x - dt.datetime(1899,12,30)).days)
test_df['created'] = test_df['created'].map(lambda x : (x - dt.datetime(1899,12,30)).days)
train_df['x2'] = train_df['latitude'].map(lambda x : round(x,2))
test_df['x2'] = test_df['latitude'].map(lambda x : round(x,2))
train_df['y2'] = train_df['longitude'].map(lambda x : round(x,2))
test_df['y2'] = test_df['longitude'].map(lambda x : round(x,2))
train_df['x3'] = train_df['latitude'].map(lambda x : round(x,3))
test_df['x3'] = test_df['latitude'].map(lambda x : round(x,3))
train_df['y3'] = train_df['longitude'].map(lambda x : round(x,3))
test_df['y3'] = test_df['longitude'].map(lambda x : round(x,3))
train_df['dist_to_center'] = np.sqrt((train_df['latitude'] - train_df['latitude'].median())**2 + (train_df['longitude'] - train_df['longitude'].median())**2)
test_df['dist_to_center'] = np.sqrt((test_df['latitude'] - test_df['latitude'].median())**2 + (test_df['longitude'] - test_df['longitude'].median())**2)

train_df["pos"] = train_df.longitude.round(3).astype(str) + '_' + train_df.latitude.round(3).astype(str)
test_df["pos"] = test_df.longitude.round(3).astype(str) + '_' + test_df.latitude.round(3).astype(str)

vals = train_df['pos'].value_counts()
dvals = vals.to_dict()
train_df["density"] = train_df['pos'].apply(lambda x: dvals.get(x, vals.min()))
test_df["density"] = test_df['pos'].apply(lambda x: dvals.get(x, vals.min()))

# features_to_use=["bathrooms", "bedrooms", "latitude", "longitude", "price","price_t","price_per_room", "logprice", "density",
# "num_photos", "num_features", "num_description_words","listing_id", "created_year", "created_month", "created_day", "created_hour"]

features_to_use=["bathrooms", "bedrooms", "latitude", "longitude", "price","price_t",
"price_per_room", "logprice", "density","num_photos", "num_features", "num_description_words",
"listing_id", 'created',"created_year", "created_month", "created_day", 'created_weekday',
'created_quarter','created_week',"created_hour",'created_min','created_sec',"x2","y2","x3","y3","dist_to_center"]

print (" feature engineering end ....")

index=list(range(train_df.shape[0]))
random.shuffle(index)
a=[np.nan]*len(train_df)
b=[np.nan]*len(train_df)
c=[np.nan]*len(train_df)

for i in range(5):
    building_level={}
    for j in train_df['manager_id'].values:
        building_level[j]=[0,0,0]
    
    test_index=index[int((i*train_df.shape[0])/5):int(((i+1)*train_df.shape[0])/5)]
    train_index=list(set(index).difference(test_index))
    
    for j in train_index:
        temp=train_df.iloc[j]
        if temp['interest_level']=='low':
            building_level[temp['manager_id']][0]+=1
        if temp['interest_level']=='medium':
            building_level[temp['manager_id']][1]+=1
        if temp['interest_level']=='high':
            building_level[temp['manager_id']][2]+=1
            
    for j in test_index:
        temp=train_df.iloc[j]
        if sum(building_level[temp['manager_id']])!=0:
            a[j]=building_level[temp['manager_id']][0]*1.0/sum(building_level[temp['manager_id']])
            b[j]=building_level[temp['manager_id']][1]*1.0/sum(building_level[temp['manager_id']])
            c[j]=building_level[temp['manager_id']][2]*1.0/sum(building_level[temp['manager_id']])
            
train_df['manager_level_low']=a
train_df['manager_level_medium']=b
train_df['manager_level_high']=c

a=[]
b=[]
c=[]
building_level={}
for j in train_df['manager_id'].values:
    building_level[j]=[0,0,0]

for j in range(train_df.shape[0]):
    temp=train_df.iloc[j]
    if temp['interest_level']=='low':
        building_level[temp['manager_id']][0]+=1
    if temp['interest_level']=='medium':
        building_level[temp['manager_id']][1]+=1
    if temp['interest_level']=='high':
        building_level[temp['manager_id']][2]+=1

for i in test_df['manager_id'].values:
    if i not in building_level.keys():
        a.append(np.nan)
        b.append(np.nan)
        c.append(np.nan)
    else:
        a.append(building_level[i][0]*1.0/sum(building_level[i]))
        b.append(building_level[i][1]*1.0/sum(building_level[i]))
        c.append(building_level[i][2]*1.0/sum(building_level[i]))
test_df['manager_level_low']=a
test_df['manager_level_medium']=b
test_df['manager_level_high']=c

features_to_use.append('manager_level_low') 
features_to_use.append('manager_level_medium') 
features_to_use.append('manager_level_high')

categorical = ["display_address", "manager_id", "building_id"]
for f in categorical:
        if train_df[f].dtype=='object':
            lbl = LabelEncoder()
            lbl.fit(list(train_df[f].values) + list(test_df[f].values))
            train_df[f] = lbl.transform(list(train_df[f].values))
            test_df[f] = lbl.transform(list(test_df[f].values))
            features_to_use.append(f)

train_df['features'] = train_df["features"].apply(lambda x: " ".join(["_".join(i.split(" ")) for i in x]))
test_df['features'] = test_df["features"].apply(lambda x: " ".join(["_".join(i.split(" ")) for i in x]))

tfidf = CountVectorizer(stop_words='english', max_features=200)
tr_sparse = tfidf.fit_transform(train_df["features"])
te_sparse = tfidf.transform(test_df["features"])

train_X = sparse.hstack([train_df[features_to_use], tr_sparse]).tocsr()
test_X = sparse.hstack([test_df[features_to_use], te_sparse]).tocsr()

target_num_map = {'high':0, 'medium':1, 'low':2}
train_y = np.array(train_df['interest_level'].apply(lambda x: target_num_map[x]))

print(train_X.shape, test_X.shape)
print (" start training model...... ")

preds, model = runXGB(train_X, train_y, test_X, num_rounds=500)
out_df = pd.DataFrame(preds)
out_df.columns = ["high", "medium", "low"]
out_df["listing_id"] = test_df.listing_id.values
out_df.to_csv("submission.csv", index=False)
