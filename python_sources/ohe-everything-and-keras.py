#!/usr/bin/env python
# coding: utf-8

# from other kernel....
# 
# https://www.kaggle.com/rspadim/humm-float-integer-why-not-categorical

# In[ ]:


#reading data :)
import numpy as np
import pandas as pd
train=pd.read_csv('../input/train.csv')
test =pd.read_csv('../input/test.csv')
test['target']=-1 # just to match columns
both=test.copy()
both=both.append(train.copy())
del test  #bye!
del train #bye!
cols=both.columns.drop(['id','target']).tolist()
print('columns: ',both.columns.tolist())
print('target values: ',both['target'].unique())


# In[ ]:


noncat=[]
cats=[]
cats_prefix={}
for i in cols:
    unique_train=both[both['target']!=-1][i].unique()
    unique_both =both[i].unique()
    equal=(sorted(unique_train) == sorted(unique_both))
    length_train=len(unique_train)
    length_both=len(unique_both)
    print('Column: ',i,'\t unique values at train/both=',
          length_train,' / ',length_both,
          '\t <- categorical?!' if equal else ''
         )
    if(not equal):
        noncat.append(i)
    if(equal and length_both>2):
        cats.append(i)
        cats_prefix[i]="OHE_"+i
print("these variables should be categorical, or not?! =) ",cats)


# In[ ]:


#i will OHE to you :)
both=pd.get_dummies(both,prefix=cats_prefix,columns=cats)
both[both['target']!=-1].to_csv('train.cat.ohe.csv.gzip',index=False,compression='gzip')
both[both['target']==-1].to_csv('test.cat.ohe.csv.gzip' ,index=False,compression='gzip')

print('features:',len(both.columns.drop(['target','id']).tolist()))


# In[ ]:


del both
import gc
gc.collect()


# --------------
# keras
# 
# from: https://www.kaggle.com/tilii7/keras-averaging-runs-gini-early-stopping

# In[ ]:


from datetime import datetime
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from keras.models import Sequential, Model
from keras.layers import Input, Dense, Dropout, Activation
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint, CSVLogger, Callback
from keras.wrappers.scikit_learn import KerasClassifier


# In[ ]:


class roc_auc_callback(Callback):
    def __init__(self,training_data,validation_data):
        self.x = training_data[0]
        self.y = training_data[1]
        self.x_val = validation_data[0]
        self.y_val = validation_data[1]

    def on_train_begin(self, logs={}):
        return

    def on_train_end(self, logs={}):
        return

    def on_epoch_begin(self, epoch, logs={}):
        return

    def on_epoch_end(self, epoch, logs={}):
        y_pred = self.model.predict_proba(self.x, verbose=0)
        roc = roc_auc_score(self.y, y_pred)
        logs['roc_auc'] = roc_auc_score(self.y, y_pred)
        logs['norm_gini'] = ( roc_auc_score(self.y, y_pred) * 2 ) - 1

        y_pred_val = self.model.predict_proba(self.x_val, verbose=0)
        roc_val = roc_auc_score(self.y_val, y_pred_val)
        logs['roc_auc_val'] = roc_auc_score(self.y_val, y_pred_val)
        logs['norm_gini_val'] = ( roc_auc_score(self.y_val, y_pred_val) * 2 ) - 1

        print('\rroc_auc: %s - roc_auc_val: %s - norm_gini: %s - norm_gini_val: %s' % (str(round(roc,5)),str(round(roc_val,5)),str(round((roc*2-1),5)),str(round((roc_val*2-1),5))), end=10*' '+'\n')
        return

    def on_batch_begin(self, batch, logs={}):
        return

    def on_batch_end(self, batch, logs={}):
        return


# In[ ]:


def timer(start_time=None):
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod(
            (datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        print('\n Time taken: %i hours %i minutes and %s seconds.' %
              (thour, tmin, round(tsec, 2)))

def scale_data(X, scaler=None):
    if not scaler:
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaler.fit(X)
    X = scaler.transform(X)
    return X, scaler


# In[ ]:


# train and test data path
DATA_TRAIN_PATH = 'train.cat.ohe.csv.gzip'
DATA_TEST_PATH = 'test.cat.ohe.csv.gzip'

def load_data(path_train=DATA_TRAIN_PATH, path_test=DATA_TEST_PATH):
    train_loader = pd.read_csv(path_train, compression='gzip', 
                               dtype={'target': np.int8, 'id': np.int32})
    train = train_loader.drop(['target', 'id'], axis=1)
    train_labels = train_loader['target'].values
    train_ids = train_loader['id'].values
    print('\n Shape of raw train data:', train.shape)

    test_loader = pd.read_csv(path_test, compression='gzip', dtype={'id': np.int32})
    
    test = test_loader.drop(['id','target'], axis=1)
    test_ids = test_loader['id'].values
    print(' Shape of raw test data:', test.shape)

    return train, train_labels, test, train_ids, test_ids


# In[ ]:


folds = 4
runs = 2

cv_LL = 0
cv_AUC = 0
cv_gini = 0
fpred = []
avpred = []
avreal = []
avids = []


# In[ ]:


# Load data set and target values
train, target, test, tr_ids, te_ids = load_data()
n_train = train.shape[0]
train_test = pd.concat((train, test)).reset_index(drop=True)
train_test_scaled, scaler = scale_data(train_test)
train = train_test_scaled[:n_train, :]
test = train_test_scaled[n_train:, :]
print('\n Shape of processed train data:', train.shape)
print(' Shape of processed test data:', test.shape)


# In[ ]:


patience = 10
batchsize = 128


# In[ ]:


# Let's split the data into folds. I always use the same random number for reproducibility, 
# and suggest that you do the same (you certainly don't have to use 1001).

skf = StratifiedKFold(n_splits=folds, random_state=1001)
starttime = timer(None)
for i, (train_index, test_index) in enumerate(skf.split(train, target)):
    start_time = timer(None)
    X_train, X_val = train[train_index], train[test_index]
    y_train, y_val = target[train_index], target[test_index]
    train_ids, val_ids = tr_ids[train_index], tr_ids[test_index]
    
# This is where we define and compile the model. These parameters are not optimal, as they were chosen 
# to get a notebook to complete in 60 minutes. Other than leaving BatchNormalization and last sigmoid 
# activation alone, virtually everything else can be optimized: number of neurons, types of initializers, 
# activation functions, dropout values. The same goes for the optimizer at the end.

#########
# Never move this model definition to the beginning of the file or anywhere else outside of this loop. 
# The model needs to be initialized anew every time you run a different fold. If not, it will continue 
# the training from a previous model, and that is not what you want.
#########

    # This definition must be within the for loop or else it will continue training previous model
    def baseline_model():
        model = Sequential()
        model.add(
            Dense(
                200,
                input_dim=X_train.shape[1],
                kernel_initializer='glorot_normal',
                ))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))
        model.add(Dense(100, kernel_initializer='glorot_normal'))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.25))
        model.add(Dense(50, kernel_initializer='glorot_normal'))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.15))
        model.add(Dense(25, kernel_initializer='glorot_normal'))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.1))
        model.add(Dense(1, activation='sigmoid'))

        # Compile model
        model.compile(optimizer='adam', metrics = ['accuracy'], loss='binary_crossentropy')

        return model

# This is where we repeat the runs for each fold. If you choose runs=1 above, it will run a 
# regular N-fold procedure.

#########
# It is important to leave the call to random seed here, so each run starts with a different seed.
#########

    for run in range(runs):
        print('\n Fold %d - Run %d\n' % ((i + 1), (run + 1)))
        np.random.seed()

# Lots to unpack here.

# The first callback prints out roc_auc and gini values at the end of each epoch. It must be listed 
# before the EarlyStopping callback, which monitors gini values saved in the previous callback. Make 
# sure to set the mode to "max" because the default value ("auto") will not handle gini properly 
# (it will act as if the model is not improving even when roc/gini go up).

# CSVLogger creates a record of all iterations. Not really needed but it doesn't hurt to have it.

# ModelCheckpoint saves a model each time gini improves. Its mode also must be set to "max" for reasons 
# explained above.

        callbacks = [
            roc_auc_callback(training_data=(X_train, y_train),validation_data=(X_val, y_val)),  # call this before EarlyStopping
            EarlyStopping(monitor='norm_gini_val', patience=patience, mode='max', verbose=1),
            CSVLogger('keras-5fold-run-01-v1-epochs.log', separator=',', append=False),
            ModelCheckpoint(
                    'keras-5fold-run-01-v1-fold-' + str('%02d' % (i + 1)) + '-run-' + str('%02d' % (run + 1)) + '.check',
                    monitor='norm_gini_val', mode='max', # mode must be set to max or Keras will be confused
                    save_best_only=True,
                    verbose=1)
        ]

# The classifier is defined here. Epochs should be be set to a very large number (not 3 like below) which 
# will never be reached anyway because of early stopping. I usually put 5000 there. Because why not.

        nnet = KerasClassifier(
            build_fn=baseline_model,
# Epoch needs to be set to a very large number ; early stopping will prevent it from reaching
#            epochs=5000,
            epochs=3,
            batch_size=batchsize,
            validation_data=(X_val, y_val),
            verbose=2,
            shuffle=True,
            callbacks=callbacks)

        fit = nnet.fit(X_train, y_train)
        
# We want the best saved model - not the last one where the training stopped. So we delete the old 
# model instance and load the model from the last saved checkpoint. Next we predict values both for 
# validation and test data, and create a summary of parameters for each run.

        del nnet
        nnet = load_model('keras-5fold-run-01-v1-fold-' + str('%02d' % (i + 1)) + '-run-' + str('%02d' % (run + 1)) + '.check')
        scores_val_run = nnet.predict_proba(X_val, verbose=0)
        LL_run = log_loss(y_val, scores_val_run)
        print('\n Fold %d Run %d Log-loss: %.5f' % ((i + 1), (run + 1), LL_run))
        AUC_run = roc_auc_score(y_val, scores_val_run)
        print(' Fold %d Run %d AUC: %.5f' % ((i + 1), (run + 1), AUC_run))
        print(' Fold %d Run %d normalized gini: %.5f' % ((i + 1), (run + 1), AUC_run*2-1))
        y_pred_run = nnet.predict_proba(test, verbose=0)
        if run > 0:
            scores_val = scores_val + scores_val_run
            y_pred = y_pred + y_pred_run
        else:
            scores_val = scores_val_run
            y_pred = y_pred_run
            
# We average all runs from the same fold and provide a parameter summary for each fold. Unless something 
# is wrong, the numbers printed here should be better than any of the individual runs.

    scores_val = scores_val / runs
    y_pred = y_pred / runs
    LL = log_loss(y_val, scores_val)
    print('\n Fold %d Log-loss: %.5f' % ((i + 1), LL))
    AUC = roc_auc_score(y_val, scores_val)
    print(' Fold %d AUC: %.5f' % ((i + 1), AUC))
    print(' Fold %d normalized gini: %.5f' % ((i + 1), AUC*2-1))
    timer(start_time)
    
# We add up predictions on the test data for each fold. Create out-of-fold predictions for validation data.

    if i > 0:
        fpred = pred + y_pred
        avreal = np.concatenate((avreal, y_val), axis=0)
        avpred = np.concatenate((avpred, scores_val), axis=0)
        avids = np.concatenate((avids, val_ids), axis=0)
    else:
        fpred = y_pred
        avreal = y_val
        avpred = scores_val
        avids = val_ids
    pred = fpred
    cv_LL = cv_LL + LL
    cv_AUC = cv_AUC + AUC
    cv_gini = cv_gini + (AUC*2-1)


# In[ ]:


LL_oof = log_loss(avreal, avpred)
print('\n Average Log-loss: %.5f' % (cv_LL/folds))
print(' Out-of-fold Log-loss: %.5f' % LL_oof)
AUC_oof = roc_auc_score(avreal, avpred)
print('\n Average AUC: %.5f' % (cv_AUC/folds))
print(' Out-of-fold AUC: %.5f' % AUC_oof)
print('\n Average normalized gini: %.5f' % (cv_gini/folds))
print(' Out-of-fold normalized gini: %.5f' % (AUC_oof*2-1))
score = str(round((AUC_oof*2-1), 5))
timer(starttime)
mpred = pred / folds


# In[ ]:


print('#\n Writing results')
now = datetime.now()
oof_result = pd.DataFrame(avreal, columns=['target'])
oof_result['prediction'] = avpred
oof_result['id'] = avids
oof_result.sort_values('id', ascending=True, inplace=True)
oof_result = oof_result.set_index('id')
sub_file = 'train_5fold-keras-run-01-v1-oof_' + str(score) + '_' + str(now.strftime('%Y-%m-%d-%H-%M')) + '.csv'
print('\n Writing out-of-fold file:  %s' % sub_file)
oof_result.to_csv(sub_file, index=True, index_label='id')


# In[ ]:


result = pd.DataFrame(mpred, columns=['target'])
result['id'] = te_ids
result = result.set_index('id')
print('\n First 10 lines of your 5-fold average prediction:\n')
print(result.head(10))
sub_file = 'submission_5fold-average-keras-run-01-v1_' + str(score) + '_' + str(now.strftime('%Y-%m-%d-%H-%M')) + '.csv'
print('\n Writing submission:  %s' % sub_file)
result.to_csv(sub_file, index=True, index_label='id')

