#!/usr/bin/env python
# coding: utf-8

# The Following work is a part of the Medium Post an attempt to make everyone familiar with Confusion Matrix and related evaluation Metrics! 
# 
# You can [read the Article here](https://medium.com/@salrite/demystifying-confusion-matrix-confusion-9e82201592fd). Please upvote the Kernel in-case you liked the Article. 
# Forged & Authorized Note, Binary Classifier based on the [UCI Dataset](https://archive.ics.uci.edu/ml/datasets/banknote+authentication).
# 
# ![](https://img-aws.ehowcdn.com/877x500p/s3.amazonaws.com/photography.prod.demandstudios.com/8ac96de8-3f1f-438d-848a-c573e021532b.jpg)

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import os
print(os.listdir("../input"))
import itertools
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


df = pd.read_csv('../input/BankNote_Authentication.csv')
df.head(5)


# In[ ]:


#Class is our Target Label, with zero indicating the Bank Note is Forged and 1 Indicating it is Legit
df['class'].value_counts() #to check if the data is equally balanced between the two classes for prediction


# In[ ]:


#defining features and target variable
y = df['class']
X = df.drop(columns = ['class'])

#splitting the data into train and test set 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)


# In[ ]:


#Predicting using Logistic Regression for Binary classification 
from sklearn.linear_model import LogisticRegression
LR = LogisticRegression()
LR.fit(X_train,y_train) #fitting the model 
y_pred = LR.predict(X_test) #prediction 


# In[ ]:


#Evaluation 
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()


# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test, y_pred)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=['Forged','Authorized'],
                      title='Confusion matrix, without normalization')


# In[ ]:


#extracting true_positives, false_positives, true_negatives, false_negatives
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
print("True Negatives: ",tn)
print("False Positives: ",fp)
print("False Negatives: ",fn)
print("True Positives: ",tp)


# In[ ]:


#Accuracy (%) 
Accuracy = (tn+tp)*100/(tp+tn+fp+fn) 
print("Accuracy {:0.2f}%".format(Accuracy))


# In[ ]:


#Precision 
Precision = tp/(tp+fp) 
print("Precision {:0.2f}".format(Precision))


# In[ ]:


#Recall 
Recall = tp/(tp+fn) 
print("Recall {:0.2f}".format(Recall))


# In[ ]:


#F1 Score
f1 = (2*Precision*Recall)/(Precision + Recall)
print("F1 Score {:0.2f}".format(f1))


# In[ ]:


#Fbeta score
def fbeta(precision, recall, beta):
    return ((1+pow(beta,2))*precision*recall)/(pow(beta,2)*precision + recall)
            
f2 = fbeta(Precision, Recall, 2)
f0_5 = fbeta(Precision, Recall, 0.5)

print("F2 {:0.2f}".format(f2))
print("\nF0.5 {:0.2f}".format(f0_5))


# In[ ]:


#Specificity 
Specificity = tn/(tn+fp)
print("Specificity {:0.2f}".format(Specificity))


# In[ ]:


#ROC
import scikitplot as skplt #to make things easy
y_pred_proba = LR.predict_proba(X_test)
skplt.metrics.plot_roc_curve(y_test, y_pred_proba)
plt.show()


# In[ ]:




