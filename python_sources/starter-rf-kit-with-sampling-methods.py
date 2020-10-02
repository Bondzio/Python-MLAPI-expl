#!/usr/bin/env python
# coding: utf-8

# As always we try and see how well a Random Forest is able to perform on this dataset to obtain a starting benchmark.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns

get_ipython().run_line_magic('pylab', 'inline')

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import roc_curve, classification_report, confusion_matrix, precision_score, recall_score, f1_score

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))


# In[ ]:


def process(df):
    """We turn some of the features in to binary."""
    for col in ['potential_issue', 'deck_risk', 'oe_constraint', 'ppap_risk',
               'stop_auto_buy', 'rev_stop', 'went_on_backorder']:
        df[col] = (df[col] == 'Yes').astype(int)
    return df

df = pd.read_csv('../input/Kaggle_Training_Dataset.csv')
df = process(df).dropna()

df.info()


# In[ ]:


df2 = pd.read_csv('../input/Kaggle_Test_Dataset.csv')
df2 = process(df2).dropna()


# In[ ]:


sns.countplot(df.went_on_backorder)


# This is a highly imbalanced problem. Perhaps some data augmentation methods may come in handy. Let's see how the baseline performs first then move on to trying out other methods

# In[ ]:


pd.tools.plotting.radviz(df.sample(10000), 'went_on_backorder')


# In[ ]:


est = RandomForestClassifier(n_jobs=-1, n_estimators=100, min_samples_split=10,
                             max_depth=10, class_weight='balanced')
X, y = df.drop('went_on_backorder', axis=1), df.went_on_backorder


# In[ ]:


est.fit(X, y)
X2, y2 = df2.drop('went_on_backorder', axis=1), df2.went_on_backorder
preds = est.predict_proba(X2)


# In[ ]:


def measure(y, preds):
    fpr, tpr, thresholds = roc_curve(y2, preds[:,0])
    area = np.trapz(fpr, tpr)
    plt.subplots(figsize=(7, 3))
    plt.subplot(121)
    plt.plot(tpr, fpr)
    plt.xlabel('True Positive Rate')
    plt.ylabel('False Positive Rate')
    plt.title('AUC : {}'.format(area))
    plt.subplot(122)
    pred_labels = np.argmax(preds, axis=1)
    c_m = confusion_matrix(y2, pred_labels)
    #c_m = c_m / c_m.sum(axis=1)
    sns.heatmap(c_m, annot=True)
    print('Precision: ', precision_score(y, pred_labels),
          '\nRecall:    ', recall_score(y, pred_labels),
          '\nF1         ', f1_score(y, pred_labels)
         )
measure(y2, preds)


# This raw confusion matrix does not really show us anything due to the overwhelming support of one class. A classification report may be better. 
# 
# That's our baseline Precision Recall. Let's try and see if simple undersampling during training beats that.

# ## Under sample the majority class

# In[ ]:


positives = df.loc[df.went_on_backorder == 1].sample(10000).copy()
negatives = df.loc[df.went_on_backorder == 0].sample(10000).copy()
sample = pd.concat([positives, negatives]).sample(20000)
X, y = sample.drop('went_on_backorder', axis=1), sample.went_on_backorder


# In[ ]:


est.fit(X, y)
X2, y2 = df2.drop('went_on_backorder', axis=1), df2.went_on_backorder
preds = est.predict_proba(X2)


# In[ ]:


measure(y2, preds)


# We see that the ROC AUC does indeed increase, though marginally. Recall has gone up while precision has gone down. What an interesting thing indeed!

# ## Over sample minority class

# In[ ]:


positives = df.loc[df.went_on_backorder == 1].copy()
while True:
    sample = pd.concat([positives]*100+ [df]).sample(50000)
    print(sample.went_on_backorder.mean())
    if sample.went_on_backorder.mean() > 0.4:
        break
    
X, y = sample.drop('went_on_backorder', axis=1), sample.went_on_backorder


# In[ ]:


est.fit(X, y)
X2, y2 = df2.drop('went_on_backorder', axis=1), df2.went_on_backorder
preds = est.predict_proba(X2)


# In[ ]:


measure(y2, preds)


# '## Gaussian noise around points
# 
# Instead of simple oversampling, let's add Gaussian noise around randomly selected points in the minority class. Imagine it to be a bleeding effect of sorts where the minority data points start "bleeding" new minority points

# In[ ]:


positives = df.loc[df.went_on_backorder == 1].copy()
X = positives.drop('went_on_backorder', axis=1).values
new_points, n_samples = [], X.shape[0]
multiplier = 150

print(X.shape, n_samples, multiplier)
for _ in range(X.shape[0]):
    index = random.choice(range(n_samples))
    center = X[index]
    for __ in range(multiplier):
        new_point = [center[i]*(1 + 0.1 * random.random()) for i in range(center.shape[0])]
        new_points.append(new_point)
print(np.array(new_points).shape)


# In[ ]:


sample = pd.DataFrame(list(X) + new_points,
                      columns=positives.drop('went_on_backorder', axis=1).columns)
sample['went_on_backorder'] = 1
print(sample.shape, df.shape)
sample = pd.concat([sample, df])
sample = sample.sample(50000)
print(sample.shape)
X = sample.drop('went_on_backorder', axis=1)
y = sample.went_on_backorder
sns.countplot(y)


# In[ ]:


est.fit(X, y)
X2, y2 = df2.drop('went_on_backorder', axis=1), df2.went_on_backorder
preds = est.predict_proba(X2)


# In[ ]:


measure(y2, preds)


# We've managed to push up Precision at the cost of recall this time. Perhaps a good thing?
