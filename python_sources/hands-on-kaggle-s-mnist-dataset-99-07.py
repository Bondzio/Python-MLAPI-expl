#!/usr/bin/env python
# coding: utf-8

# # **Hands-on Kaggle's MNIST dataset**
# 
# * **1. Introduction**
# * **2. Data preparation**
#     * 2.1 Load and explore the data
#     * 2.2 Check for null and missing values
#     * 2.3 Data formatting & Label encoding
#     * 2.4 Splitting the training and validation set
# * **3. Minimal example: Densely connected network**
#     * 3.1 Model
#     * 3.2 Training and validation curves
#     * 3.3 Confusion Matrix
# * **4. K-folds cross-validation with a Densely connected network**
#     * 4.1 Splitting into K Folds
#     * 4.2 Model
#     * 4.3 Iterative training on the k-folds
#     * 4.4 Training and validation curves
# * **5. Simple Convnet**
#     * 5.1 Data preparation
#     * 5.2 Model
#     * 5.3 Training and validation curves
#     * 5.4 Confusion Matrix
#     * 5.5 Displaying some error results
#     * 5.6 Final prediction and submition

# # 1. Introduction
# 
# In this kernel, I'm experimenting with a densely connected network and then a small convnet, both trained with the MNIST dataset for digit recognition. I'll try different techniques to improve the models: dropout, regularizers, data augmentation, etc. 
# 
# There is probably room for improvements, and i'm open to any comment/critic/discussion on how to perform better.

# In[ ]:


# This is a Python 3 environment

get_ipython().run_line_magic('pylab', 'inline')
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np # linear algebra
import matplotlib.pyplot as plt # data visualisation
import matplotlib.image as mpimg
import seaborn as sns # data visualisation

np.random.seed(21)


# # 2. Data preparation
# ## 2.1 Load & explore the data

# In[ ]:


# Load data
train = pd.read_csv("../input/digit-recognizer/train.csv")
test = pd.read_csv("../input/digit-recognizer/test.csv")


# In[ ]:


# Explore data
print(train.shape)
train.head()


# In[ ]:


print(test.shape)
test.head()


# In[ ]:


# Separate between training features X and target Y:
Y_train = train["label"]
X_train = train.drop("label",1)

# train is not needed anymore
del train 

# Visualize how the labels are distributed
g = sns.countplot(Y_train)
Y_train.value_counts()


# All labels have approximatively the same number of occurence: it is possible to randomly split X_train into a training set and a validation set without fearing to have an unbalanced distribution.

# In[ ]:


# Let's plot some of the numbers

figure(figsize(6,6))
for digit_num in range(0,36):
    subplot(6,6,digit_num+1)
    grid_data = X_train.iloc[digit_num].values.reshape(28,28)  # reshape from 1d to 2d pixel array
    plt.imshow(grid_data, interpolation = "none", cmap = "bone_r")
    xticks([])
    yticks([])


# We note that some pair of numbers can be misleading: 7 might be mistaken with 1, 9 with 6, 8 with 3 ?

# ## 2.2 Check for null and missing values

# In[ ]:


# Check the data
X_train.isnull().any().describe()


# In[ ]:


test.isnull().any().describe()


# There are no missing values in the train and test dataset, i.e. we are good to go.

# ## 2.3 Data formatting & Label encoding

# In[ ]:


# We rescale the pixel values in the [0,1] intervalle since Neural networks prefer to deal with small input values.
X_train = X_train.astype('float32') / 255.0
test = test.astype('float32') / 255.0


# In[ ]:


#Save the X_train and Y_train for later when i'll use the k-fold cross validation
X_train_saved = X_train
Y_train_saved = Y_train


# In[ ]:


# One Hot Encoding (ex : 1 -> [0,1,0,0,0,0,0,0,0,0])
from keras.utils.np_utils import to_categorical
Y_train = to_categorical(Y_train, num_classes = 10)


# ## 2.4 Splitting training and validation set 

# In[ ]:


# Set the random seed
random_seed = 21


# In[ ]:


# Split the train and the validation set for the fitting
from sklearn.model_selection import train_test_split
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size = 0.1, random_state=random_seed)


# The train set is split in two parts : 80% are used for training, and 10% are used for validation. Since we have 42 000 training images of balanced labels, a random split of the train set doesn't cause some labels to be over represented in the validation set. (Else, we would have to use the stratify argument).

# # 3. Minimal example: Densely connected network

# In[ ]:


from keras.models import  Sequential
from keras.utils import np_utils
from keras.layers.core import  Dense, Flatten, Dropout
from keras import regularizers


# In[ ]:


# Verify the shape of X_train after the splitting
X_train.shape


# ## 3.1 Model

# ### Model definition

# In[ ]:


#Define the model:
network = Sequential()
network.add(Dense(128, activation='relu', input_shape=(28*28,)))
network.add(Dropout(0.3))
network.add(Dense(128, activation='relu'))
network.add(Dropout(0.3))
network.add(Dense(10, activation='softmax'))
network.summary()


# Before compiling the network we have to to add:
# - a loss function -- how the network will be able to measure its performance on the training data
# - an optimizer -- to update the network as it sees more data with the corresponding loss value
# - some metrics -- to monitor the performance of our network

# ### Callback

# In[ ]:


from keras.callbacks import EarlyStopping

earlystop = EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='min')


# ### Optimizer

# In[ ]:


from keras.optimizers import RMSprop
network.compile(optimizer=RMSprop(lr=0.0001), #small learning rate in order for the loss not to diverge
                loss='categorical_crossentropy',
                metrics=['acc'])


# ### Compilation

# In[ ]:


print("Training...")
# Fit the model
history = network.fit(X_train,Y_train, batch_size=16,epochs = 30, validation_data = (X_val,Y_val), verbose = 1, callbacks=[earlystop])


# ## 3.2 Training and validation curves

# In[ ]:


# Plot the loss and accuracy curves for training and validation 
def plot_learning_curves(history):
    fig, ax = plt.subplots(2,1, figsize=(12, 12))
    ax[0].plot(history.history['loss'], color='b', label="Training loss")
    ax[0].plot(history.history['val_loss'], color='r', label="validation loss",axes =ax[0])
    legend = ax[0].legend(loc='best', shadow=True)
    
    ax[1].plot(history.history['acc'], color='b', label="Training accuracy")
    ax[1].plot(history.history['val_acc'], color='r',label="Validation accuracy")
    legend = ax[1].legend(loc='best', shadow=True)
    return 

plot_learning_curves(history)


# We observe an accuracy of around 96.7% for the validation set. Both the training and validation losses converge towards the same plateau, indicating that we have a good fit. 23 to 25 epochs seem enough to train the final model. For that, use both full training data set (i.e. training + validation sets).
# 
# Here, i used only dropout and a small network to hinder overfitting. Regularization or more advanced techniques were unnecessary.

# ## 3.3 Confusion Matrix

# The confusion matrix is an useful tool to get an idea of the performance of your model and where it fails. More infos [here](http://machinelearningmastery.com/confusion-matrix-machine-learning/)

# In[ ]:


from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(model_name):
    # Predict the values from the validation dataset
    Y_pred = model_name.predict(X_val)
    # Because Y_pred is an array of probabilities, we have to convert it to one hot vectors 
    Y_pred_classes = np.argmax(Y_pred,axis = 1) 
    # Convert validation observations to one hot vectors
    Y_true = np.argmax(Y_val,axis = 1) 
    # compute the confusion matrix
    confusion_mtx = confusion_matrix(Y_true, Y_pred_classes) 
    # plot the confusion matrix
    plt.figure(figsize=[7,6])
    sns.heatmap(confusion_mtx, cmap="Reds", annot=True, fmt='.0f')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
    return

plot_confusion_matrix(network)

Surprisingly, the 9 has been most misclassified with 4. 8 have been most misclassified with 5s. The same thing goes for other number (5 with 3, 2 with 7, etc.), indicating that our model needs ameliorations.
# # 4. K-folds cross-validation with a Densely connected network

# In the previous section, we used a train_test_split as a resampling method. However,you might not be able to afford this splitting if you have very few samples to train on. K-folds cross validation solves this problem by splitting your entire dataset into K differents training/validation subsets (so that each sample is part of a validation set only one time), on which K different models will be trained. Thus, you are able to make predictions on all of your data.
# It is also useful for estimating the skill of a whole procedure (data engineering, choice of model, hyper-parameters, etc.) on future unseen data. Thanks to it, you can:
# * calculate performance measures of models that were trained with different training/validation sets.
# * calculate the standard deviation of these measures to get an idea of how much the skill of the procedure is expected to vary in practice.
# For example, with 10-fold CV you obtain 10 accuracy measurements, which allows you to estimate a central tendency and a spread (which is always better than a single point). Then, once you have confirmed the performance of your model on average, you may pass to the final model training stage, where you will train a new model on all the available data that you have.
# 
# More infos on K-folds cross validation [here](http://machinelearningmastery.com/train-final-machine-learning-model/).

# ## 4.1 Splitting into K folds

# In[ ]:


#First, split the dataset into 5 folds for cross validation.:
from sklearn.model_selection import StratifiedKFold

# Y_train has been one hot encoded already. However, the split method does not work with multilabel-indicator, thus we need to use Y_train_saved instead 
# (or inverse the to_categorical and split operation)

def kfold(k):
    #StratifiedKFold will return balanced fold where each label is equally represented.
    folds = list(StratifiedKFold(n_splits=k, shuffle=True, random_state=1).split(X_train_saved, Y_train_saved))
    
    return folds, X_train_saved, Y_train_saved

k = 5
folds, X_train_saved, Y_train_saved = kfold(k)


# ## 4.2 Model definition

# In[ ]:


# Function to define a model: we choose an architecture relatively similar as in Section 3 for simplicity.
def build_model():
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(28*28,)))
    model.add(Dropout(0.3))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer=RMSprop(lr=1e-4), loss='categorical_crossentropy', metrics=['acc'])
    return model


# In[ ]:


model = build_model()
model.summary()


# ## 4.3 Iterative training on the k-folds

# In[ ]:


num_epochs = 25
batch_size = 16
all_val_loss_histories = []
all_loss_histories = []
all_val_acc_histories = []
all_acc_histories = []

for j, (train_idx, val_idx) in enumerate(folds):
    
    print('\nRunning Fold {} / {}'.format(j+1, k))
    X_train_cv, Y_train_cv = X_train_saved.iloc[train_idx], Y_train_saved.iloc[train_idx]
    X_val_cv, Y_val_cv = X_train_saved.iloc[val_idx], Y_train_saved.iloc[val_idx]
    #Note: if data preparation is needed (normalisation, etc.), it should be done here on the training subset in order to avoid information leakage.
    
    #one-hot encode Y_val_cv and Y_train_cv:
    Y_train_cv = to_categorical(Y_train_cv)
    Y_val_cv = to_categorical(Y_val_cv)
    
    model = build_model()
    history = model.fit(X_train_cv, Y_train_cv, 
              epochs=num_epochs,
              batch_size=batch_size,
              verbose=0,
              validation_data = (X_val_cv, Y_val_cv))
    val_loss_history = history.history['val_loss']
    loss_history = history.history['loss']
    acc_history = history.history['acc']
    val_acc_history = history.history['val_acc']
    
    all_val_loss_histories.append(val_loss_history)
    all_loss_histories.append(loss_history)
    all_val_acc_histories.append(val_acc_history)
    all_acc_histories.append(acc_history)
    
    print(model.evaluate(X_val_cv, Y_val_cv))


# In[ ]:


# Uncomment to access the key values in history_dict
#history_dict = history.history
#print(history_dict.keys())


# ## 4.4 Training and validation curves

# In[ ]:


# Visualisation:
average_val_loss_history = [np.mean([x[i] for x in all_val_loss_histories]) for i in range(num_epochs)]
average_val_acc_history = [np.mean([x[i] for x in all_val_acc_histories]) for i in range(num_epochs)]
average_loss_history = [np.mean([x[i] for x in all_loss_histories]) for i in range(num_epochs)]
average_acc_history = [np.mean([x[i] for x in all_acc_histories]) for i in range(num_epochs)]

# Plot the loss and accuracy curves for training and validation 
fig, ax = plt.subplots(2,1, figsize=(12, 12))
ax[0].plot(average_loss_history, color='b', label="Average training loss")
ax[0].plot(average_val_loss_history, color='r', label="Average Validation loss",axes =ax[0])
legend = ax[0].legend(loc='best', shadow=True)
ax[0].set_xlabel('Epochs')
ax[0].set_ylabel('Loss')

ax[1].plot(average_acc_history, color='b', label="Average training accuracy")
ax[1].plot(average_val_acc_history, color='r',label="Average validation accuracy")
legend = ax[1].legend(loc='best', shadow=True)
ax[1].set_xlabel('Epochs')
ax[1].set_ylabel('Accuracy')


# No surprise here, we obtain an average accuracy similar to the accuracy obtained earlier.

# # 5. Simple Convnet

# ## 5.1 Data preparation

# In[ ]:


# One Hot Encoding
Y_train_saved = to_categorical(Y_train_saved, num_classes = 10)


# In[ ]:


# Reshape image in 3 dimensions (height = 28px, width = 28px , canal = 1 (grayscale image))
# Note: -1 means that the length in that dimension is inferred to keep the same number of elements once reshaped.
X_train = X_train_saved.values.reshape(-1,28,28,1)
test = test.values.reshape(-1,28,28,1)


# In[ ]:


# Set the random seed
random_seed = 2


# In[ ]:


# Split the train and the validation set for the fitting
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train_saved, test_size = 0.1, random_state=random_seed)


# ## 5.2 Model

# ### Model definition

# In[ ]:


# Set the CNN model 
from keras.layers import Conv2D, MaxPool2D

CNN = Sequential()

CNN.add(Conv2D(filters = 32, kernel_size = (3,3),padding = 'Same', activation ='relu', input_shape = (28,28,1)))
CNN.add(MaxPool2D(pool_size=(2,2)))

CNN.add(Conv2D(filters = 64, kernel_size = (3,3),padding = 'Same', activation ='relu'))
CNN.add(MaxPool2D(pool_size=(2,2)))

CNN.add(Conv2D(filters = 64, kernel_size = (3,3),padding = 'Same', activation ='relu'))
CNN.add(MaxPool2D(pool_size=(2,2)))
CNN.add(Dropout(0.25))

CNN.add(Flatten())
CNN.add(Dense(256, activation = "relu"))
CNN.add(Dropout(0.5))
CNN.add(Dense(10, activation = "softmax"))

CNN.summary()


# ### Optimizer & compilation

# In[ ]:


#compile the model
from keras import optimizers

CNN.compile(optimizer = optimizers.rmsprop(lr=1e-4), 
            loss = "categorical_crossentropy", 
            metrics=["acc"])


# ### Callback

# In[ ]:


#additional callback:
from keras.callbacks import ReduceLROnPlateau

learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc', 
                                            patience=2, 
                                            verbose=1, 
                                            factor=0.5, 
                                            min_lr=1e-5)


# ### Training

# In[ ]:


num_epochs = 20
batch_size = 16

history = CNN.fit(X_train, Y_train,
                  epochs=num_epochs,
                  batch_size=batch_size,
                  verbose=1,
                  validation_data = (X_val, Y_val),
                  callbacks=[earlystop, learning_rate_reduction])


# ## 5.3 Training and validation curves

# In[ ]:


# Plot the loss and accuracy curves for training and validation 
plot_learning_curves(history)


# The learning curves are good. We don't underfit nor overfit. We reach an accuracy of 99.07%.

# ## 5.4 Confusion Matrix

# In[ ]:


#plot the confusion matrix:
plot_confusion_matrix(CNN)


# ## 5.5 Displaying some error results

# In[ ]:


# Nice function for displaying some error results found on this kernel: https://www.kaggle.com/yassineghouzam/introduction-to-cnn-keras-0-997-top-6

# Predict the values from the validation dataset
Y_pred = CNN.predict(X_val)
# Because Y_pred is an array of probabilities, we have to convert it to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert validation observations to one hot vectors
Y_true = np.argmax(Y_val,axis = 1) 
# compute the confusion matrix
    
# Errors are difference between predicted labels and true labels
errors = (Y_pred_classes - Y_true != 0)

Y_pred_classes_errors = Y_pred_classes[errors]
Y_pred_errors = Y_pred[errors]
Y_true_errors = Y_true[errors]
X_val_errors = X_val[errors]

def display_errors(errors_index,img_errors,pred_errors, obs_errors):
    """ This function shows 6 images with their predicted and real labels"""
    n = 0
    nrows = 2
    ncols = 3
    fig, ax = plt.subplots(nrows,ncols,sharex=True,sharey=True)
    for row in range(nrows):
        for col in range(ncols):
            error = errors_index[n]
            ax[row,col].imshow((img_errors[error]).reshape((28,28)))
            ax[row,col].set_title("Predicted label :{}\nTrue label :{}".format(pred_errors[error],obs_errors[error]))
            n += 1

# Probabilities of the wrong predicted numbers
Y_pred_errors_prob = np.max(Y_pred_errors,axis = 1)

# Predicted probabilities of the true values in the error set
true_prob_errors = np.diagonal(np.take(Y_pred_errors, Y_true_errors, axis=1))

# Difference between the probability of the predicted label and the true label
delta_pred_true_errors = Y_pred_errors_prob - true_prob_errors

# Sorted list of the delta prob errors
sorted_dela_errors = np.argsort(delta_pred_true_errors)

# Top 6 errors 
most_important_errors = sorted_dela_errors[-6:]

# Show the top 6 errors
display_errors(most_important_errors, X_val_errors, Y_pred_classes_errors, Y_true_errors)


# ## 5.6 Final predictions and submition

# In[ ]:


print("Generating test predictions...")
preds = CNN.predict_classes(test, verbose=1)


# In[ ]:


def write_preds(preds, fname):
    pd.DataFrame({"ImageId": list(range(1,len(preds)+1)), "Label": preds}).to_csv(fname, index=False, header=True)

write_preds(preds, "keras-mlp.csv")

