#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Basic Libs
import os
from glob import glob

#For basic operations
import pandas as pd
import numpy as np
from random import randint

#Used for training
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, ReLU, BatchNormalization, MaxPool2D, Dense, Dropout, Flatten
import math
import cv2
from sklearn.utils import shuffle
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix, recall_score, precision_score, f1_score, auc, accuracy_score

#used for visual representation
from tqdm import tqdm
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


# In[ ]:


class ImageClassifier(tf.keras.Model):
    def __init__(self, image_size=[80, 80], dataset_path=None,l_rate=0.00001):
        super(ImageClassifier, self).__init__()
        self.image_size = image_size
        self.dataset_path = dataset_path
        self.classes = sorted(os.listdir(self.dataset_path))
        self.l_rate = l_rate
        self.data_x = []
        self.data_y = []
    
    def preprocess_data(self):
        w, h = 80, 80

        center = (w / 2, h / 2)

        angle90 = 90
        angle180 = 180
        angle270 = 270

        scale = 1.0
        #Basic Preprocession
        for c in tqdm(self.classes):
            _list = glob(self.dataset_path+c+"/*.jpg")
            for name in _list:
                img = cv2.resize(plt.imread(name), (w, h))/255
                self.data_x.append(img)
                self.data_y.append(c)

                M = cv2.getRotationMatrix2D(center, angle90, scale)
                rotated90 = cv2.warpAffine(img, M, (h, w))
                self.data_x.append(img)
                self.data_y.append(c)

                M = cv2.getRotationMatrix2D(center, angle180, scale)
                rotated180 = cv2.warpAffine(img, M, (w, h))
                self.data_x.append(img)
                self.data_y.append(c)

                M = cv2.getRotationMatrix2D(center, angle270, scale)
                rotated270 = cv2.warpAffine(img, M, (w, h))
                self.data_x.append(img)
                self.data_y.append(c)
        return self.data_x, self.data_y
    
    @tf.function
    def model(self):
        self.conv_1 = Conv2D(32, (3,3), 
                             input_shape=[self.image_size[0], 
                                          self.image_size[1], 3],
                             name="input_conv_1")
        self.bn_1 = BatchNormalization(name="bn_1")
        self.relu_1 = ReLU(name="relu_1")
        
        self.conv_2 = Conv2D(64, (3,3), name="conv_2")
        self.bn_2 = BatchNormalization(name="bn_2")
        self.relu_2 = ReLU(name="relu_2")
        
        self.conv_3 = Conv2D(128, (3,3), name="conv_3")
        self.max_pool_3 = MaxPool2D(name="max_pool_3")
        self.bn_3 = BatchNormalization(name="bn_3")
        self.relu_3 = ReLU(name="relu_3")
        
        self.conv_4 = Conv2D(128, (3,3), name="conv_4")
        self.bn_4 = BatchNormalization(name="bn_4")
        self.relu_4 = ReLU(name="relu_4")

        self.conv_5 = Conv2D(64, (3,3), name="conv_5")
        self.max_pool_5 = MaxPool2D(name="max_pool_5")
        self.bn_5 = BatchNormalization(name="bn_5")
        self.relu_5 = ReLU(name="relu_5")
        
        self.conv_6 = Conv2D(32, (3,3), name="conv_6")
        self.bn_6 = BatchNormalization(name="bn_6")
        self.relu_6 = ReLU(name="relu_6")
        
        self.flatten = Flatten(name="flat")
        self.dense_1 = Dense(4096, activation=tf.nn.relu, name="dense_1")
        self.droput_1 = Dropout(0.2, name="dropout_1")
        
        self.dense_2 = Dense(1024, activation=tf.nn.relu, name="dense_2")
        self.droput_2 = Dropout(0.2, name="dropout_2")
        
        self.output_dense_3 = Dense(len(self.classes), activation=None, name="output_dense_3")
        
        self.opt = tf.keras.optimizers.Adam(learning_rate=self.l_rate)
        
    @tf.function
    def call(self, input_tensor, training=True):
        x = self.conv_1(input_tensor)
        x = self.bn_1(x, training=training)
        x = self.relu_1(x)
        
        x = self.conv_2(x)
        x = self.bn_2(x, training=training)
        x = self.relu_2(x)
        
        x = self.conv_3(x)
        x = self.max_pool_3(x)
        x = self.bn_3(x, training=training)
        x = self.relu_3(x)
        
        x = self.conv_4(x)
        x = self.bn_4(x, training=training)
        x = self.relu_4(x)
        
        x = self.conv_5(x)
        x = self.max_pool_5(x)
        x = self.bn_5(x, training=training)
        x = self.relu_5(x)
        
        x = self.conv_6(x)
        x = self.bn_6(x, training=training)
        x = self.relu_6(x)
        
        x = self.flatten(x)
        
        x = self.dense_1(x)
        x = self.droput_1(x, training=training)
        
        x = self.dense_2(x)
        x = self.droput_2(x, training=training)
        
        x = self.output_dense_3(x)
        
        return x
    
    def step(self, _real_x, _real_y, training=False):
        with tf.GradientTape() as tape:
            _input = np.reshape(_real_x, newshape=[-1, 
                                                    self.image_size[0],
                                                    self.image_size[1],
                                                    3])
            pred_y = self.call(_input, training=training)
            loss = tf.nn.softmax_cross_entropy_with_logits(_real_y, pred_y)
        model_grad = tape.gradient(loss, self.trainable_variables)
        self.opt.apply_gradients(zip(model_grad, self.trainable_variables))
        return loss
    
    def calc_metrics(self, pred, test_y):
        _test_y, _pred = np.argmax(test_y.values, axis=1), tf.math.argmax(pred, axis=1).numpy()
        _f1 = f1_score(_test_y,_pred ,  average="weighted")
        _recall = recall_score(_test_y,_pred ,  average="weighted")
        _precision = precision_score(_test_y,_pred ,  average="weighted")
        _acc = accuracy_score(_test_y,_pred)
        return _f1, _recall, _precision, _acc
    
    def show_metrics(self, test_x, test_y):
        batch_size=32
        bat_per_epoch = math.floor(len(test_x) / batch_size)
        f1_list = []
        pre_list = []
        rec_list = []
        acc_list = []
        for i in range(bat_per_epoch):
            pred = tf.nn.softmax(self.call(np.array(test_x)[i:i+batch_size], training=False))
            f1,rec,pre,acc = self.calc_metrics(pred, test_y.iloc[i:i+batch_size])
            f1_list.append(f1)
            rec_list.append(rec)
            pre_list.append(pre)
            acc_list.append(acc)
        return round(np.mean(f1_list), 4), round(np.mean(pre_list), 4), round(np.mean(rec_list), 4), round(np.mean(acc_list), 4)
    
    def return_pred_target_probabs(self, test_x, test_y):
        batch_size=32
        bat_per_epoch = math.floor(len(test_x) / batch_size)
        pred_list = []
        target_list = []
        for i in range(bat_per_epoch):
            pred = tf.nn.softmax(self.call(np.array(test_x)[i:i+batch_size], training=False))
            target_list+=list(test_y.values[i:i+batch_size])
            pred_list+=list(pred)
        return np.array(target_list), np.array(pred_list)


# In[ ]:


DATASET_PATH="/kaggle/input/flowers-recognition/flowers/" #Path where dataset stored
classes = sorted(['daisy', 'rose', 'dandelion', 'sunflower', 'tulip'] )
imageClassifier = ImageClassifier(image_size=[80, 80], dataset_path=DATASET_PATH,l_rate=0.00001)
imageClassifier.classes = classes
imageClassifier.model()


# In[ ]:


data_x, data_y = imageClassifier.preprocess_data()


# In[ ]:


train_x, train_y = shuffle(data_x, data_y)
train_x, train_y, test_x, test_y = (train_x[0:int(len(train_x)*0.9)], pd.get_dummies(train_y[0:int(len(train_x)*0.9)]), 
                                    train_x[int(len(train_x)*0.9):], pd.get_dummies(train_y[int(len(train_x)*0.9):]))


# In[ ]:


# train_x, train_y = shuffle(data_x, data_y)
# train_x, train_y, test_x, test_y = (train_x[0:100], pd.get_dummies(train_y[0:100]), 
#                                     train_x[100:150], pd.get_dummies(train_y[100:150]))


# In[ ]:


print("Train Data len: ", len(train_x))
print("Test Data len: ", len(test_x))


# In[ ]:


batch_size=32
bat_per_epoch = math.floor(len(train_x) / batch_size)
# _train_y = pd.get_dummies(np.array(train_y))
epochs = 6
for epoch in range(epochs):
    train_x, train_y = shuffle(train_x, train_y)
    _loss_list = []
    for i in range(bat_per_epoch):
        n = i*batch_size
        _loss = imageClassifier.step(np.array(train_x[n:n+batch_size]), np.array(train_y[n:n+batch_size]))
        _loss_list.append(_loss.numpy().mean())
        
    print("Epoch: ", epoch+1, " loss: ", np.mean(_loss_list))
    train_x_data, train_y_data = shuffle(train_x, train_y)
    train_f1,train_pre,train_rec,train_acc = imageClassifier.show_metrics(train_x_data[:1000], train_y_data.iloc[:1000])
    print(" \t Train: f1_score:", train_f1, " precision:", train_pre, " recall:",train_rec, " Accuracy:", train_acc)
    
    test_f1,test_pre,test_rec,test_acc = imageClassifier.show_metrics(test_x, test_y)
    print(" \t Test: f1_score:", test_f1, " precision:", test_pre, " recall:",test_rec, " Accuracy:", test_acc)
    
    print()


# In[ ]:


plt.figure(figsize=[15,15])
for i in range(16):
    idx=randint(0, len(test_x))
    pred = tf.nn.softmax(imageClassifier.call(np.array(test_x)[idx:idx+1], training=False))
    test_label, pred_label = test_y.columns[np.argmax(test_y.values[idx])], test_y.columns[tf.math.argmax(pred[0]).numpy()]
    plt.subplot(4,4,i+1)
    plt.imshow(test_x[idx])
    _=plt.title("True: "+test_label+" | pred:"+pred_label)


# In[ ]:


fpr_list = []
tpr_list = []
n_classes = len(classes)
classes = test_y.columns.values


# In[ ]:


target_prob, pred_prob = imageClassifier.return_pred_target_probabs(test_x, test_y)
train_infer_x, train_infer_y = shuffle(train_x[:1000], train_y.iloc[:1000])
train_target_prob, train_pred_prob = imageClassifier.return_pred_target_probabs(train_infer_x, train_infer_y)
plt.figure(figsize=(20, 20))
for i in range(n_classes):
    plt.subplot(np.ceil(n_classes/2),2,i+1)
    
    test_fpr, test_tpr, _ = roc_curve(target_prob[:,i], pred_prob[:,i])
    test_roc_auc_score = auc(test_fpr, test_tpr)
    plt.plot(test_fpr, test_tpr, label="Test roc_auc_score: "+str(round(test_roc_auc_score, 4)))
    
    train_fpr, train_tpr, _ = roc_curve(train_target_prob[:,i], train_pred_prob[:,i])
    train_roc_auc_score = auc(train_fpr, train_tpr)
    plt.plot(train_fpr, train_tpr, label="Train roc_auc_score: "+str(round(train_roc_auc_score, 4)))
    
    plt.plot([0,1], [0,1], "--k")
    plt.legend()
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Classes: "+classes[i])


# In[ ]:




