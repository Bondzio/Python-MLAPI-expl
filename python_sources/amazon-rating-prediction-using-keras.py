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


df=pd.read_csv('/kaggle/input/amazon-music-reviews/Musical_instruments_reviews.csv')


# In[ ]:


df.head()


# In[ ]:


X=df.reviewText.astype('str')
y=df.overall


# In[ ]:


X


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


sns.countplot('overall',data=df)
plt.show()


# In[ ]:


y.value_counts()


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.1,stratify=y,random_state=42)


# In[ ]:


y_train.value_counts()


# In[ ]:


from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


# In[ ]:


vocab=1000
tokenizer=Tokenizer(vocab,oov_token="<oov>")


# In[ ]:


tokenizer.fit_on_texts(X_train)


# In[ ]:


train_sequence=tokenizer.texts_to_sequences(X_train)
test_sequence=tokenizer.texts_to_sequences(X_test)


# In[ ]:


padded_train=pad_sequences(train_sequence,maxlen=500)
padded_test=pad_sequences(test_sequence,maxlen=500)


# In[ ]:


padded_train.shape


# In[ ]:


padded_test.shape


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense,LSTM,Embedding,GlobalAveragePooling1D
from keras.optimizers import Adam


# In[ ]:


model=Sequential()
model.add(Embedding(vocab,1000))
model.add(GlobalAveragePooling1D())
model.add(Dense(128,activation='relu'))
model.add(Dense(6,activation='softmax'))
model.compile(optimizer=Adam(lr=0.001),loss='categorical_crossentropy',metrics=['accuracy'])


# In[ ]:


model.summary()


# In[ ]:


from keras.utils import to_categorical


# In[ ]:


cat_train=to_categorical(y_train)
cat_test=to_categorical(y_test)


# In[ ]:


cat_train.shape


# In[ ]:


from keras.callbacks import EarlyStopping


# In[ ]:


early=EarlyStopping(monitor='val_accuracy',patience=10)


# In[ ]:


model.fit(padded_train,cat_train,validation_data=(padded_test,cat_test),epochs=100,callbacks=[early])


# In[ ]:


model.fit(padded_train,cat_train,validation_data=(padded_test,cat_test),epochs=20)


# In[ ]:


metrics=pd.DataFrame(model.history.history)


# In[ ]:


metrics[['loss','val_loss']].plot()


# In[ ]:


metrics[['accuracy','val_accuracy']].plot()


# In[ ]:


y_pred=model.predict_classes(padded_test)


# In[ ]:


from sklearn.metrics import classification_report,confusion_matrix


# In[ ]:


print(classification_report(y_test,y_pred))


# In[ ]:


import numpy as np


def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")


    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()


# In[ ]:


plot_confusion_matrix(cm           = confusion_matrix(y_test,y_pred) ,
                      normalize    = False,
                      target_names = [1,2,3,4,5],
                      title        = "Confusion Matrix")


# In[ ]:


y_train.value_counts()


# In[ ]:


6244/len(X_train)*100


# In[ ]:


string=["This product is bad","This product is good but it may be better if it had this features","I love this product","The product i got was not the product i want","The Camera is worse"]


# In[ ]:


sequence_string=tokenizer.texts_to_sequences(string)


# In[ ]:


sequence_string


# In[ ]:


padded_string=pad_sequences(sequence_string)


# In[ ]:


padded_string.shape


# In[ ]:


model.predict_classes(padded_string)

