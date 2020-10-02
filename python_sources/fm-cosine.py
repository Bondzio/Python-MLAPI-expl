# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import pandas as pd
from keras.layers import * #Input, Embedding, Dense,Flatten, merge,Activation
from keras.models import Model
from keras.regularizers import l2 as l2_reg
import itertools
import keras
from keras.optimizers import *
from keras.regularizers import l2
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory


train_data = pd.read_csv("../input/rating.csv")

print(train_data.columns)
train_data = train_data.sample(frac=1.0)
train_data['rating'] = train_data['rating']/5.0
feat_cols = []
cat_cols = []
from sklearn import preprocessing
ule = preprocessing.LabelEncoder()
vle = preprocessing.LabelEncoder()
for feat in train_data.columns:
        if feat in ['userId','movieId']:
                if feat == 'userId':
                        le = ule
                else:
                        le = vle
                feat_cols.append(feat)
                le.fit(train_data[feat])
                train_data["new_%s"%feat] = le.transform(train_data[feat])
                cat_cols.append("new_%s"%feat)
print(feat_cols)
print(cat_cols)

from keras.utils import plot_model
def KerasFM(max_features,K=10,solver=Adam(lr=0.01),l2=0.00,l2_fm = 0.00):
    inputs = []
    flatten_layers=[]
    columns = range(len(max_features))
    fm_layers = []
    #for c in columns:
    for c in max_features.keys():
        inputs_c = Input(shape=(1,), dtype='int32',name = 'input_%s'%c)
        num_c = max_features[c]
        embed_c = Embedding(
                        num_c,
                        K,
                        input_length=1,
                        name = 'embed_%s'%c,
                        embeddings_regularizer=keras.regularizers.l2(1e-5)
                        )(inputs_c)

        flatten_c = Flatten()(embed_c)

        inputs.append(inputs_c)
        flatten_layers.append(flatten_c)
    for emb1,emb2 in itertools.combinations(flatten_layers, 2):
        dot_layer = dot([emb1,emb2],axes=-1,normalize=True)
        fm_layers.append(dot_layer)

    #flatten = BatchNormalization(axis=1)(add((fm_layers)))
    flatten = dot_layer
    outputs = Dense(1,activation='linear',name='outputs')(flatten)
    model = Model(input=inputs, output=outputs)
    model.compile(optimizer=solver,loss= 'mae')
    plot_model(model, to_file='fm_cosine_model.png',show_shapes=True)
    #model.summary()
    return model


max_features = train_data[cat_cols].max() + 1

train_len = int(len(train_data)*0.95)
X_train, X_valid = train_data[cat_cols][:train_len], train_data[cat_cols][train_len:]
y_train, y_valid = train_data['rating'][:train_len], train_data['rating'][train_len:]

train_input = []
valid_input = []
#test_input = []
#print(test_data)
for col in cat_cols:
    train_input.append(X_train[col])
    valid_input.append(X_valid[col])
#    test_input.append(test_data[col])
ck = keras.callbacks.ModelCheckpoint("best.model", monitor='val_loss', verbose=0, save_best_only=True, save_weights_only=True, mode='auto', period=1)
es = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=2, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
model = KerasFM(max_features)
model.fit(train_input, y_train, batch_size=100000,nb_epoch=100,verbose=2,validation_data=(valid_input,y_valid),callbacks=[ck,es])

from sklearn.metrics import roc_auc_score
p_valid = model.predict(valid_input)
auc = roc_auc_score(y_valid>=0.5,p_valid)
print("valid auc is %0.6f"%auc)
p_valid = p_valid*5
from sklearn.metrics import *
mse = mean_absolute_error(y_valid*5.0,p_valid)
print("valid mae is %0.6f"%mse)
valid_df = train_data[feat_cols][train_len:]
valid_df['rating'] = 5.0*train_data['rating'][train_len:]

valid_df['pred_rating'] = p_valid
valid_df.to_csv('cosine_valid.csv',index=False)


# Any results you write to the current directory are saved as output.