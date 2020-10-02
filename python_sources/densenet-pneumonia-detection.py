#!/usr/bin/env python
# coding: utf-8

# # Basline GPU DenseNet Model
# 
# Trying out a densenet201 architecture for Xray Pneumonia Detection. This model shall serve as a baseline for a TPU accelerated model.

# In[ ]:


import numpy as np
import pandas as pd
import os
from glob import glob
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix, roc_curve, auc, precision_recall_curve, average_precision_score
import tensorflow as tf
from tensorflow import keras


# ## Early processing of metadata for easier model training:

# In[ ]:


## Below is some helper code to read all of your full image filepaths into a dataframe for easier manipulation
## Load the NIH data to all_xray_df
all_xray_df = pd.read_csv('../input/data/Data_Entry_2017.csv')
all_image_paths = {os.path.basename(x): x for x in 
                   glob(os.path.join('../input/data','images*', '*', '*.png'))}
print('Scans found:', len(all_image_paths), ', Total Headers', all_xray_df.shape[0])
all_xray_df['path'] = all_xray_df['Image Index'].map(all_image_paths.get)
all_xray_df.sample(3)


# In[ ]:


# Using only PA images
pa_xray_df = all_xray_df.drop(all_xray_df.loc[all_xray_df['View Position']=='AP'].index)


# In[ ]:


## Splitting finding lables into individual rows
cleaned = pa_xray_df.rename(columns={'Finding Labels': 'labels'})
cleaned = cleaned.set_index('Image Index').labels.str.split('|', expand=True).stack().reset_index(level=1, drop=True).to_frame('lables')
cleaned.head()


# In[ ]:


# getting dummy variables for the lables and grouping by the index.
cleaned = pd.get_dummies(cleaned, columns=['lables']).groupby(level=0).sum()


# In[ ]:


cleaned.head()


# In[ ]:


# ensuring both data frames use the same index
pa_xray_df.set_index('Image Index', inplace=True)


# In[ ]:


# merging dummy variable columns with the data frame containing the image paths.
prepared_df = pa_xray_df.merge(cleaned, left_index = True, right_index=True)


# In[ ]:


prepared_df.head()


# In[ ]:


## Renamiong dummy column to 'pneumonia_class' that will allow us to look at 
## images with or without pneumonia for binary classification

prepared_df.rename(columns={'lables_Pneumonia': 'pneumonia_class'}, inplace=True)


# In[ ]:


# Checking that class is binary
prepared_df.pneumonia_class.unique()


# In[ ]:


prepared_df.to_csv("prepared_df.csv")


# ## Train-Validation Split:

# In[ ]:


prepared_df = pd.read_csv("prepared_df.csv", index_col="Image Index")


# In[ ]:


# checking class imbalance
prepared_df['pneumonia_class'].value_counts()


# In[ ]:


train_data, val_data = train_test_split(prepared_df, test_size=0.2, stratify = prepared_df['pneumonia_class'], random_state=42)


# # Data Preprocessing:

# #### First suggestion: perform some image augmentation on your data

# In[ ]:


train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    featurewise_center=False,
    featurewise_std_normalization=False,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True)

val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    featurewise_center=False,
    featurewise_std_normalization=False)

train_generator = train_datagen.flow_from_dataframe(
    train_data, directory=None, x_col='path', y_col='pneumonia_class', weight_col=None,
    target_size=(224, 224), color_mode='rgb', classes=None,
    class_mode='raw', batch_size=32, shuffle=True, seed=42,
    save_to_dir=None, save_prefix='', save_format='png', subset=None,
    interpolation='nearest', validate_filenames=True
)
validation_generator = val_datagen.flow_from_dataframe(
    val_data, directory=None, x_col='path', y_col='pneumonia_class', weight_col=None,
    target_size=(224, 224), color_mode='rgb', classes=None,
    class_mode='raw', batch_size=32, shuffle=True, seed=42,
    save_to_dir=None, save_prefix='', save_format='png', subset=None,
    interpolation='nearest', validate_filenames=True
)


# In[ ]:


## May want to look at some examples of our augmented training data. 
## This is helpful for understanding the extent to which data is being manipulated prior to training, 
## and can be compared with how the raw data look prior to augmentation

t_x, t_y = next(train_generator)
fig, m_axs = plt.subplots(4, 4, figsize = (16, 16))
for (c_x, c_y, c_ax) in zip(t_x, t_y, m_axs.flatten()):
    c_ax.imshow(c_x[:,:,0], cmap = 'bone')
    if c_y == 1: 
        c_ax.set_title('Pneumonia')
    else:
        c_ax.set_title('No Pneumonia')
    c_ax.axis('off')


# ## Building model: 

# In[ ]:


METRICS = [
          keras.metrics.TruePositives(name='tp'),
          keras.metrics.FalsePositives(name='fp'),
          keras.metrics.TrueNegatives(name='tn'),
          keras.metrics.FalseNegatives(name='fn'), 
          keras.metrics.BinaryAccuracy(name='accuracy'),
          keras.metrics.Precision(name='precision'),
          keras.metrics.Recall(name='recall'),
          keras.metrics.AUC(name='auc'),
        ]


# In[ ]:


# defining model generator
def get_model(metrics = METRICS, output_bias=None):
    if output_bias is not None:
        output_bias = tf.keras.initializers.Constant(output_bias)
    
    densenet = tf.keras.applications.DenseNet201(weights = 'imagenet', include_top=False, pooling = 'avg', input_shape=[224, 224, 3])
    densenet.trainable = True # Using pretrained weights due to compute limitation on the worspace.
    model = tf.keras.Sequential([
            densenet,
            tf.keras.layers.Dense(1, activation='sigmoid', bias_initializer=output_bias)
            ])

    model.compile(
            optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=False),
            loss = keras.losses.BinaryCrossentropy(),
            metrics = METRICS
            )
    return model


# In[ ]:


# defining learning rate sheduler (currently not used)
LR_START = 0.0001
LR_MAX = 0.0001
LR_MIN = 0.00001
LR_RAMPUP_EPOCHS = 3
LR_SUSTAIN_EPOCHS = 0
LR_EXP_DECAY = .8

def lrfn(epoch):
    if epoch < LR_RAMPUP_EPOCHS:
        lr = np.random.random_sample() * LR_START # Using random learning rate for initial epochs.
    elif epoch < LR_RAMPUP_EPOCHS + LR_SUSTAIN_EPOCHS:
        lr = LR_MAX 
    else:
        lr = (LR_MAX - LR_MIN) * LR_EXP_DECAY**(epoch - LR_RAMPUP_EPOCHS - LR_SUSTAIN_EPOCHS) + LR_MIN # Rapid decay of learning rate to improve convergence.
    return lr
    
lr_callback = tf.keras.callbacks.LearningRateScheduler(lrfn, verbose=True)


# In[ ]:


# defining early stopping
es_callback = tf.keras.callbacks.EarlyStopping(
    monitor='val_auc', 
    verbose=1,
    patience=5,
    mode='max',
    restore_best_weights=True)


# In[ ]:


checkpoint_path = "training/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)


# ### Start training! 

# In[ ]:


print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU'))) #check gpu status


# In[ ]:


# calculating class weights to adress class imbalance
positive_findings = 630
negative_findings = 66680
total = positive_findings+negative_findings

initial_bias = np.log([positive_findings/negative_findings])

weight_for_0 = (1 / negative_findings)*(total)/2.0 
weight_for_1 = (1 / positive_findings)*(total)/2.0

class_weight = {0: weight_for_0, 1: weight_for_1}

print('Weight for class 0: {:.2f}'.format(weight_for_0))
print('Weight for class 1: {:.2f}'.format(weight_for_1))


# In[ ]:


model = get_model(output_bias = initial_bias)


# In[ ]:


model.summary()


# In[ ]:


#with active_session():
history = model.fit(train_generator, 
                        epochs = 10, 
                        verbose = 2, 
                        validation_data = validation_generator, 
                        callbacks = [lr_callback, es_callback, cp_callback], 
                        class_weight = class_weight)


# In[ ]:


"""Plotting the history of model training 
(due to time requirement of the training 
and workspace timing out this may not be available):"""

def plot_metrics(history):
    metrics =  ['loss', 'auc', 'precision', 'recall']
    for n, metric in enumerate(metrics):
        name = metric.replace("_"," ").capitalize()
        plt.subplot(2,2,n+1)
        plt.plot(history.epoch,  history.history[metric], color='b', label='Train')
        plt.plot(history.epoch, history.history['val_'+metric],
             color='r', linestyle="--", label='Val')
        plt.xlabel('Epoch')
        plt.ylabel(name)
        if metric == 'loss':
          plt.ylim([0, plt.ylim()[1]])
        elif metric == 'auc':
          plt.ylim([0.8,1])
        else:
          plt.ylim([0,1])

    plt.legend()


# In[ ]:


if history is not None:
    plot_metrics(history)


# In[ ]:


model.save('models/dense_model_retrained')


# ##### Plotting some performance statistics:

# In[ ]:


## After training, make some predictions to assess your model's overall performance
## Note that detecting pneumonia is hard even for trained expert radiologists, 
## so there is no need to make the model perfect.
weight_path = checkpoint_path
model.load_weights(weight_path)


# In[ ]:


results = model.evaluate(validation_generator, verbose=2)
print("Loss: {:0.4f}".format(results[0]))


# In[ ]:


# Plotting AUC.
def plot_auc(t_y, p_y):
    fig, c_ax = plt.subplots(1,1, figsize = (9, 9))
    fpr, tpr, thresholds = roc_curve(t_y, p_y)
    c_ax.plot(fpr, tpr, label = '%s (AUC:%0.2f)'  % ('Pneumonia', auc(fpr, tpr)))
    c_ax.legend()
    c_ax.set_xlabel('False Positive Rate')
    c_ax.set_ylabel('True Positive Rate')

## Checking presicion recall curve based on thresholds.

def plot_precision_recall_curve(t_y, p_y):
    fig, c_ax = plt.subplots(1,1, figsize = (9, 9))
    precision, recall, thresholds = precision_recall_curve(t_y, p_y)
    c_ax.plot(recall, precision, label = '%s (AP Score:%0.2f)'  % ('Pneumonia', average_precision_score(t_y,p_y)))
    c_ax.legend()
    c_ax.set_xlabel('Recall')
    c_ax.set_ylabel('Precision')


# In[ ]:


valX, valY = next(validation_generator)
pred_Y = model.predict(valX, batch_size = 32, verbose = True)


# In[ ]:


plot_auc(valY, pred_Y)


# In[ ]:


plot_precision_recall_curve(valY, pred_Y)


# Playing with classification thresholds:

# In[ ]:


# F1 calulator helper fuction.
def  calc_f1(prec,recall):
    return 2*(prec*recall)/(prec+recall)


# In[ ]:


precision, recall, thresholds = precision_recall_curve(valY, pred_Y)


# In[ ]:


# Look at the threshold where precision is 0.8
precision_value = 0.8
idx = (np.abs(precision - precision_value)).argmin() 
print('Precision is: '+ str(precision[idx]))
print('Recall is: '+ str(recall[idx]))
print('Threshold is: '+ str(thresholds[idx]))
print('F1 Score is: ' + str(calc_f1(precision[idx],recall[idx])))


# In[ ]:


# Look at the threshold where recall is 0.8
recall_value = 0.8
idx = (np.abs(recall - recall_value)).argmin() 
print('Precision is: '+ str(precision[idx]))
print('Recall is: '+ str(recall[idx]))
print('Threshold is: '+ str(thresholds[idx]))
print('F1 Score is: ' + str(calc_f1(precision[idx],recall[idx])))


# In[ ]:


## Let's look at some examples of true vs. predicted with our best model: 

YOUR_THRESHOLD = 0.5

fig, m_axs = plt.subplots(10, 10, figsize = (16, 16))
i = 0
for (c_x, c_y, c_ax) in zip(valX[0:100], valY[0:100], m_axs.flatten()):
    c_ax.imshow(c_x[:,:,0], cmap = 'bone')
    if c_y == 1: 
        if pred_Y[i] > YOUR_THRESHOLD:
             c_ax.set_title('1, 1')
        else:
             c_ax.set_title('1, 0')
    else:
        if pred_Y[i] > YOUR_THRESHOLD: 
             c_ax.set_title('0, 1')
        else:
             c_ax.set_title('0, 0')
    c_ax.axis('off')
    i=i+1


# In[ ]:


## Just save model architecture to a .json:

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

