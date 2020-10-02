"""
"""
## Imports
from ashrae_utils import reduce_mem_usage, CyclicLR, LRFinder
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math
import tqdm
import gc
from sklearn.linear_model import RidgeCV, LassoCV
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import keras.backend as K
from keras.callbacks import ModelCheckpoint
import seaborn as sns


## Parameters
BENCHMARK_SUBS=True
PRINT_CORR_HEATMAP=False
REPLACE_LEAK=True # Replace leak data or not
DEBUG=False
PRINT_WEIGHTS = True
RIDGE_ALPHAS = (0.1, 1.0, 10.0) #(0.01, 0.1, 0.3, 0.5, 1.0, 2.0, 6.0, 10.0)
TYPE_PREDICTION = 'ridgecv' # Mean, Median, keras, ridgecv, errorinversionnormalized
ADD_METER_COLS = False
submission_paths = [
                    #'/kaggle/input/ashrae-half-and-half/submission.csv', #1.108 --> 0.9451
                    '/kaggle/input/half-half-drop-rows-stratify-weekday/submission.csv', #1.105 --> 0.9446
                    #'/kaggle/input/ashrae-simple-data-cleanup-lb-1-08-no-leaks/submission.csv',
                    '/kaggle/input/simple-data-cleanup-3-models/submission.csv',# 1.072
                    '/kaggle/input/ashrae-kfold-lightgbm-without-leak-1-08/submission.csv',
                    '/kaggle/input/another-1-08-lb-no-leak/fe2_lgbm.csv',
                    '/kaggle/input/ashrae-kfold-lightgbm-without-building-id/submission.csv', #1.098
                    '/kaggle/input/ashrae-energy-prediction-using-stratified-kfold/fe2_lgbm.csv', #1.074
                    '/kaggle/input/ashrae-lightgbm-without-leak/submission.csv', #1.082
                    '/kaggle/input/ashrae-stratified-kfold-lightgbm/submission.csv', #1.075
                    '/kaggle/input/ashrae-2-lightgbm-without-leak-data/submission.csv',
                    #'/kaggle/input/avg-models-keras-embedding-read-k-folds/submission.csv', 
                   ]

## Functions
def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true-y_pred)**2))

def rmsle(y_true, y_pred):
    return np.sqrt(np.mean((np.log1p(y_true)-np.log1p(y_pred))**2))

def read_submissions():
    print('## Reading submissions')
    subs = []
    for i, path in enumerate(submission_paths):
        print(f'Reading {path}')
        sub = pd.read_csv(path)
        sub.columns = ['row_id', f'meter_reading_{i}']
        subs.append(sub[f'meter_reading_{i}']) 
    subs = pd.concat(subs, axis=1)
    subs['row_id'] = sub.row_id
    subs = reduce_mem_usage(subs)
    sub = reduce_mem_usage(sub)
    sub.columns = ['row_id', 'meter_reading']
    return sub, subs

def read_leak():
    y_test = pd.read_csv('/kaggle/input/leak-test-set/y_test.csv', names=['meter_reading'], index_col=0)
    y_test['meter_reading'] = np.clip(y_test['meter_reading'], 0, None)
    return y_test

def leak_benchmark(sub):
    print("## Comparing predictions against leak data")
    y_test = read_leak()
    rmsle_error = rmsle(y_test.values.T[0], sub['meter_reading'][y_test.index].values)
    print(f'RMSLE in the leak data is {rmsle_error}')
    if REPLACE_LEAK:
        print("## Replacing predictions with leak data")
        sub['meter_reading'][y_test.index] = y_test['meter_reading']
    return sub

def keras_model(X):
    model = Sequential([
            Dense(units=1, input_shape=(X.shape[1],))
        ])
    return model

def train_keras(X, y, run_lr_finder=False, epochs=5):
    print("train_keras")
    # Parameters
    VAL_SPLIT = 0.5
    BS = 1024
    
    # Prepare data
    y = np.log1p(y)
    X = prepare_X(X)
    
    # Loss Function
    def root_mean_squared_error(y_true, y_pred):
        return K.sqrt(K.mean(K.square(y_pred-y_true)))
        
    # 1. Define your base model here
    model = keras_model(X)

    model.compile(optimizer=Adam(lr=0.001), # Default of adam is 0.001. Check large and small values, use a value slighly lower than a diverging lr
                 loss=root_mean_squared_error)

    clr = CyclicLR(base_lr=1e-3, 
                   max_lr=1e-1,
                   step_size=2*int(len(y)/BS), # 2 times the number of iterations
                   mode='exp_range',
                   gamma=0.99994
                  )

    checkpointer=ModelCheckpoint('best_val.hdf5', monitor='val_loss', verbose=1, save_best_only=True,mode='min', period=1)

    # LRFINDER
    if run_lr_finder:
        model.fit(X, y, epochs=1, batch_size=BS, validation_split=VAL_SPLIT, callbacks=[LRFinder(min_lr=1e-4, max_lr=10)])
    else:
        print("Fitting Keras Model")
        model.fit(X, y, epochs=epochs, batch_size=BS, validation_split=0.5, callbacks=[checkpointer], verbose=0)
        model.load_weights('best_val.hdf5')
        return model

def read_X_test():
    X_test = pd.read_feather('/kaggle/input/ashrae-feather-format-for-fast-loading/test.feather')
    X_test = X_test.set_index('row_id')
    return X_test
    
def prepare_X(X):
    X = np.log1p(X)
    if ADD_METER_COLS:
        X_test = read_X_test()
        X_test = reduce_mem_usage(X_test)
        X['meter']=X_test.iloc[X.index]['meter']
        
        if sum(X['meter']==2)==0:
            X.loc[0,'meter']=2
        
        buffer = []  
        for c in X.columns[:-1]:
            df = pd.get_dummies(X.meter, prefix='pred_'+c.split('_')[2]+'_meter')
            buffer.append(df.multiply(X[c], axis="index"))

        X = pd.concat(buffer, axis=1)
        
    return X    

def benchmark_subs(X, y):
    for i, col in enumerate(X.columns):
        print(f"Benchmarking {submission_paths[i].split('/')[-2]}")
        score = rmse(X[col].values, y['meter_reading'].values)
        print(f"RMSLE is {score}")

def ridgecv_predict(subs):
    #X, y = get_X_y(subs)
    y = read_leak()
    X = subs.iloc[y.index, :len(submission_paths)]
    X = prepare_X(X)
    y = np.log1p(y)
    
    if BENCHMARK_SUBS:
        benchmark_subs(X, y)
    
    if PRINT_CORR_HEATMAP:
        sns_plot = sns.heatmap(pd.concat([X, y], axis=1).corr(), annot=True)
        sns_plot.savefig("corr_w_gt.png")

    reg = RidgeCV(alphas = RIDGE_ALPHAS).fit(X, y)
    if PRINT_WEIGHTS:
        print("## Ridge Coefficients")
        print(f'Sum of coefficients: {sum(reg.coef_[0])}')
        for ww, ss in zip(reg.coef_[0], submission_paths):
            print(f'{ss.split("/")[-2]} has weight {ww:.2f}')
    X = subs.iloc[:, :len(submission_paths)]
    X = prepare_X(X)
    y_pred = reg.predict(X)
    y_pred = y_pred.T[0]
    y_pred = np.clip(y_pred, 0, None)
    y_pred = np.expm1(y_pred)
    return y_pred

def lasso_predict(subs):
    #X, y = get_X_y(subs)
    y = read_leak()
    X = subs.iloc[y.index, :len(submission_paths)]
    X = prepare_X(X)
    y = np.log1p(y)
    
    if BENCHMARK_SUBS:
        benchmark_subs(X, y)
    
    if PRINT_CORR_HEATMAP:
        sns_plot = sns.heatmap(pd.concat([X, y], axis=1).corr(), annot=True)
        sns_plot.savefig("corr_w_gt.png")

    reg = LassoCV().fit(X, y)
    if PRINT_WEIGHTS:
        print("## Lasso Coefficients")
        print(f'Sum of coefficients: {sum(reg.coef_[0])}')
        for ww, ss in zip(reg.coef_[0], submission_paths):
            print(f'{ss.split("/")[-2]} has weight {ww:.2f}')
    X = subs.iloc[:, :len(submission_paths)]
    X = prepare_X(X)
    y_pred = reg.predict(X)
    y_pred = y_pred.T[0]
    y_pred = np.clip(y_pred, 0, None)
    y_pred = np.expm1(y_pred)
    return y_pred

def get_X_y(subs):
    y = read_leak()
    X = subs.iloc[y.index, :len(submission_paths)]
    return X, y

def keras_predict(subs):
    print("Keras predict")
    X, y = get_X_y(subs) # y is from leak
    #train_keras(X, y, run_lr_finder=True)
    model = train_keras(X, y, epochs=5)
    
    w=model.weights[0].numpy()
    if len(w==len(submission_paths)):
        for ww, ss in zip(w, submission_paths):
            print(f'{ss.split("/")[-2]} has weight {ww[0]:.2f}')
            
    X = subs.iloc[:, :len(submission_paths)]
    X = prepare_X(X)
    y_pred = model.predict(X, batch_size=5000, verbose=1)
    y_pred = y_pred.T[0]
    y_pred = np.expm1(y_pred)
    return y_pred

def nie_predict(subs):
    y = read_leak()
    X = subs.iloc[y.index, :len(submission_paths)]
    #X = prepare_X(X)
    weights = []
    for c, s in zip(X.columns, submission_paths):
        e = rmsle(y['meter_reading'].values, X[c].values)
        print(f'RMSLE of {s.split("/")[-2]} is {e:.4f}')
        weights.append(1/e**100)
    print(f'Weights are {weights}')
    weights = weights/np.sum(weights)
    print(f'Normalized weights are {weights}')

    X = subs.iloc[:, :len(submission_paths)]
    y_pred = np.sum(X * weights, axis=1).values
    y_pred = np.clip(y_pred, 0, None)
    return y_pred


def predict(subs, **kwargs):
    
    if PRINT_CORR_HEATMAP:
        sns_plot = sns.heatmap(subs.iloc[:, :len(submission_paths)].corr(), annot=True)
        sns_plot.savefig("corr_subs.png")
    
    if TYPE_PREDICTION=='mean':
        return subs.iloc[:, :len(submission_paths)].mean(axis=1)
    elif TYPE_PREDICTION=='median':
        return subs.iloc[:, :len(submission_paths)].median(axis=1)
    elif TYPE_PREDICTION=='keras':
        return keras_predict(subs)
    elif TYPE_PREDICTION=='lassocv':
        return lassocv_predict(subs)
    elif TYPE_PREDICTION=='ridgecv':
        return ridgecv_predict(subs)
    elif TYPE_PREDICTION=='normalizedinvertederror':
        return nie_predict(subs)

def export(sub):
    if not DEBUG:
        print('## Saving to CSV')
        sub.to_csv('submission.csv', index=False, float_format='%g')

## Main Function
if __name__=='__main__':
    
    # 1. Reading Data
    sub, subs = read_submissions()
    
    # 2. Predicting
    sub['meter_reading'] = predict(subs)
    
    # 3. Leak correction
    sub = leak_benchmark(sub)
    
    # 4. Export Submission
    export(sub)