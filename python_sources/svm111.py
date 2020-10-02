#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


get_ipython().system('pip install keras==2.2.4')


# In[ ]:


from __future__ import print_function
import numpy as np
import os
import sys
from sklearn.model_selection import KFold, StratifiedKFold, train_test_split
from sklearn.utils import shuffle
import keras
from keras.models import Model, load_model
import tensorflow as tf
from time import time
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Input
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization, GlobalAveragePooling2D, Lambda
from keras.layers import Conv2D, Conv3D, GlobalAveragePooling3D, Reshape
from keras.callbacks import ModelCheckpoint, TensorBoard, ReduceLROnPlateau
from keras.applications import MobileNetV2, MobileNet, Xception
from sklearn.datasets import make_circles
from sklearn.svm import SVC
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.metrics import confusion_matrix
import keras.backend as K
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt


# In[ ]:


ids = ["MED_LYMPH_001",
"MED_LYMPH_002",
"MED_LYMPH_003",
"MED_LYMPH_004",
"MED_LYMPH_005",
"MED_LYMPH_006",
"MED_LYMPH_007",
"MED_LYMPH_008",
"MED_LYMPH_009",
"MED_LYMPH_010",
"MED_LYMPH_011",
"MED_LYMPH_012",
"MED_LYMPH_013",
"MED_LYMPH_014",
"MED_LYMPH_015",
"MED_LYMPH_016",
"MED_LYMPH_017",
"MED_LYMPH_018",
"MED_LYMPH_019",
"MED_LYMPH_020",
"MED_LYMPH_021",
"MED_LYMPH_022",
"MED_LYMPH_023",
"MED_LYMPH_024",
"MED_LYMPH_025",
"MED_LYMPH_026",
"MED_LYMPH_027",
"MED_LYMPH_028",
"MED_LYMPH_029",
"MED_LYMPH_030",
"MED_LYMPH_031",
"MED_LYMPH_032",
"MED_LYMPH_033",
"MED_LYMPH_034",
"MED_LYMPH_035",
"MED_LYMPH_036",
"MED_LYMPH_037",
"MED_LYMPH_038",
"MED_LYMPH_039",
"MED_LYMPH_040",
"MED_LYMPH_041",
"MED_LYMPH_042",
"MED_LYMPH_043",
"MED_LYMPH_044",
"MED_LYMPH_045",
"MED_LYMPH_046",
"MED_LYMPH_047",
"MED_LYMPH_048",
"MED_LYMPH_049",
"MED_LYMPH_050",
"MED_LYMPH_051",
"MED_LYMPH_052",
"MED_LYMPH_053",
"MED_LYMPH_054",
"MED_LYMPH_055",
"MED_LYMPH_056",
"MED_LYMPH_057",
"MED_LYMPH_058",
"MED_LYMPH_059",
"MED_LYMPH_060",
"MED_LYMPH_061",
"MED_LYMPH_062",
"MED_LYMPH_063",
"MED_LYMPH_064",
"MED_LYMPH_065",
"MED_LYMPH_066",
"MED_LYMPH_067",
"MED_LYMPH_068",
"MED_LYMPH_069",
"MED_LYMPH_070",
"MED_LYMPH_071",
"MED_LYMPH_072",
"MED_LYMPH_073",
"MED_LYMPH_074",
"MED_LYMPH_075",
"MED_LYMPH_076",
"MED_LYMPH_077",
"MED_LYMPH_078",
"MED_LYMPH_079",
"MED_LYMPH_080",
"MED_LYMPH_081",
"MED_LYMPH_082",
"MED_LYMPH_083",
"MED_LYMPH_084",
"MED_LYMPH_085",
"MED_LYMPH_086",
"MED_LYMPH_087",
"MED_LYMPH_088",
"MED_LYMPH_089",
"MED_LYMPH_090"]
ids.sort()
ids=np.array(ids)


# In[ ]:


plt.figure(0).clf()

np.set_printoptions(threshold=sys.maxsize)
seed=5
np.random.seed(seed)

train_path="/kaggle/input/25dii/2.5D-II/train/"
test_path="/kaggle/input/25dii/2.5D-II/test/"


# In[ ]:


def check_units(y_true, y_pred):
    if y_pred.shape[1] != 1:
      y_pred = y_pred[:,1:2]
      y_true = y_true[:,1:2]
    return y_true, y_pred

def precision(y_true, y_pred):
    y_true, y_pred = check_units(y_true, y_pred)
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def recall(y_true, y_pred):
    y_true, y_pred = check_units(y_true, y_pred)
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def f1(y_true, y_pred):
    def recall(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    y_true, y_pred = check_units(y_true, y_pred)
    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def acc1(y_true, y_pred):
    acc1 = K.mean(K.equal(K.argmax(y_true, axis=-1), K.argmax(y_pred, axis=-1)))
    return acc1

def acc_rec(y_true, y_pred):
    def recall(y_true, y_pred):
        y_true, y_pred = check_units(y_true, y_pred)
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall
    
    def acc1(y_true, y_pred):
        acc1 = K.mean(K.equal(K.argmax(y_true, axis=-1), K.argmax(y_pred, axis=-1)))
        return acc1

    acc1 = acc1(y_true, y_pred)
    recall1 = recall(y_true, y_pred)
    alpha = 0.5
    return (alpha*acc1+(1-alpha)*recall1)

def f1_rec(y_true, y_pred):
    def recall(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    y_true, y_pred = check_units(y_true, y_pred)
    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    f1 = 2*((precision*recall)/(precision+recall+K.epsilon()))
    return (f1+recall)/2


# In[ ]:


kfold = KFold(n_splits=5, shuffle=True, random_state=seed)

accuracy_list = []
precision_list = []
recall_list = []
f1_score_list = []
cohens_kappa_list = []
ROC_AUC_list = []
true_negative = []
false_negative = []
false_positive = []
true_positive = []
cnt=0

for train, test in kfold.split(ids):
    cnt=cnt+1
    train_ids=ids[train]
    test_ids=ids[test]
    training_data=np.load(train_path+train_ids[0]+".npy", allow_pickle=True)
    X=np.array([i[0] for i in training_data]).reshape(-1,32,32,12)
    Y=np.array([i[1] for i in training_data])

    training_data=np.load(test_path+test_ids[0]+".npy", allow_pickle=True)
    x_test=np.array([i[0] for i in training_data]).reshape(-1,32,32,12)
    y_test=np.array([i[1] for i in training_data])


    for i in range(1, len(train_ids)):
        training_data=np.load(train_path+train_ids[i]+".npy", allow_pickle=True)
        X_temp=np.array([i[0] for i in training_data]).reshape(-1,32,32,12)
        Y_temp=np.array([i[1] for i in training_data])
        X=np.concatenate((X, X_temp))
        Y=np.concatenate((Y, Y_temp))

    for i in range(1, len(test_ids)):
        training_data=np.load(test_path+test_ids[i]+".npy", allow_pickle=True)
        x_test_temp=np.array([i[0] for i in training_data]).reshape(-1,32,32,12)
        y_test_temp=np.array([i[1] for i in training_data])
        x_test=np.concatenate((x_test, x_test_temp))
        y_test=np.concatenate((y_test, y_test_temp))

    X, Y=shuffle(X, Y, random_state=seed)
    x_test, x_val, y_test, y_val=train_test_split(x_test, y_test, test_size=0.3, random_state=seed)

    print()
    print(X.shape, Y.shape)
    print(x_val.shape, y_val.shape)
    print(x_test.shape, y_test.shape)
    print()

    opt = keras.optimizers.Adam(lr=0.0001)
    inp = Input(shape=(32, 32, 12))
    x = Conv2D(3, 3, padding='same')(inp)
    x = Lambda(lambda x: K.tf.image.resize_images(x, (224, 224)), input_shape=(32, 32, 3))(x)
    base_model=MobileNetV2(weights='imagenet',include_top=False,input_shape=(224,224,3))(x) #imports the mobilenet model and discards the last 1000 neuron layer.

    x=base_model
    x=GlobalAveragePooling2D()(x)
    x=Dense(1024,activation='relu')(x) #we add dense layers so that the model can learn more complex functions and classify for better results.
    x=Dropout(0.2)(x)
    x=Dense(1024,activation='relu', name="SVM")(x) #dense layer 2
    x=Dropout(0.3)(x)
    preds=Dense(2,activation='softmax')(x) #final layer with softmax activation

    model=Model(inputs=inp,outputs=preds)
    model.summary()

    model_name = "m1.h5"
    model_checkpoint = ModelCheckpoint(model_name, monitor='val_acc', verbose=1, save_best_only=True)
    
    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
    model.fit(X, Y, batch_size=32, epochs=15, callbacks=[model_checkpoint], validation_data=(x_val, y_val), shuffle=True)
    
    print()
    print("#######################################################")
    print()

    model_1 = load_model('m1.h5')
    
    yhat_probs=model_1.predict(x_test, verbose=1)
    yhats=yhat_probs.argmax(axis=-1)
    probs=yhat_probs[:, 1]
    testy=y_test[:, 1]

    # accuracy: (tp + tn) / (p + n)
    accuracy = accuracy_score(testy, yhats)
    print('Accuracy: %f' % accuracy)

    # precision tp / (tp + fp)
    precision = precision_score(testy, yhats)
    print('Precision: %f' % precision)

    # recall: tp / (tp + fn)
    recall = recall_score(testy, yhats)
    print('Recall: %f' % recall)

    # f1: 2 tp / (2 tp + fp + fn)
    f1 = f1_score(testy, yhats)
    print('F1 score: %f' % f1)
 
    # kappa
    kappa = cohen_kappa_score(testy, yhats)
    print('Cohens kappa: %f' % kappa)

    # ROC AUC
    auc = roc_auc_score(testy, probs)
    print('ROC AUC: %f' % auc)

    # confusion matrix
    matrix = confusion_matrix(testy, yhats)
    print(matrix)

    fpr, tpr, thresh = roc_curve(testy, probs)
    plt.plot(fpr, tpr, label="fold "+str(cnt)+", auc="+str(auc), linestyle='dashed')

    true_negative.append(matrix[0][0])
    false_negative.append(matrix[1][0])
    false_positive.append(matrix[0][1])
    true_positive.append(matrix[1][1])
    precision_list.append(precision)
    recall_list.append(recall)
    f1_score_list.append(f1)
    cohens_kappa_list.append(kappa)
    ROC_AUC_list.append(auc)
    accuracy_list.append(accuracy * 100)

    print()
    print("#######################################################")
    print()
    
    svm_training=[]
    svm_testing=[]
    intermediate_layer_model=Model(inputs=model.input, outputs=model.get_layer("SVM").output)

    intermediate_output1=intermediate_layer_model.predict(X)
    for i in range(intermediate_output1.shape[0]):
        svm_training.append([np.array(intermediate_output1[i]), np.array(Y[i])])

    intermediate_output1=intermediate_layer_model.predict(x_test)
    for i in range(intermediate_output1.shape[0]):
        svm_testing.append([np.array(intermediate_output1[i]), np.array(y_test[i])])

    np.save("training_"+str(cnt)+".npy", svm_training)
    np.save("testing_"+str(cnt)+".npy", svm_testing)

plt.legend(loc=0)
plt.savefig("m1")
plt.close()


print("%.2f%% (+/- %.2f%%)" % (np.mean(accuracy_list), np.std(accuracy_list)))
print("%.2f (+/- %.2f)" % (np.mean(precision_list), np.std(precision_list)))
print("%.2f (+/- %.2f)" % (np.mean(recall_list), np.std(recall_list)))
print("%.2f (+/- %.2f)" % (np.mean(f1_score_list), np.std(f1_score_list)))
print("%.2f (+/- %.2f)" % (np.mean(cohens_kappa_list), np.std(cohens_kappa_list)))
print("%.2f (+/- %.2f)" % (np.mean(ROC_AUC_list), np.std(ROC_AUC_list)))
print("%.2f (+/- %.2f)" % (np.mean(true_negative), np.std(true_negative)))
print("%.2f (+/- %.2f)" % (np.mean(false_negative), np.std(false_negative)))
print("%.2f (+/- %.2f)" % (np.mean(false_positive), np.std(false_positive)))
print("%.2f (+/- %.2f)" % (np.mean(true_positive), np.std(true_positive)))


# In[ ]:





# In[ ]:




