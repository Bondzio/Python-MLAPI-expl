#!/usr/bin/env python
# coding: utf-8

# ### Assume Postive class : 1 and Negative class : 0

# In[ ]:


ground_truth = [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1] 

prediction   = [0.1, 0.3, 0.2, 0.6, 0.8, 0.05, 0.9, 0.5, 0.3, 0.66, 0.3,  0.2, 0.85, 0.15, 0.99] 

thresholds    = [0, 0.1, 0.2, 0.3, 0.4, 0.5,  0.6, 0.7, 0.8, 0.85, 0.9, 0.99, 1.0] 


# ### True Positive:
# If model predicts Positive class correctly then its True Positive.

# In[ ]:


#True Positive
def true_positive(ground_truth, prediction):
    tp = 0
    for gt, pred in zip(ground_truth, prediction):
        if gt == 1 and pred == 1:
            tp +=1
    return tp


# ### True Negative:
# If model predicts Negative class correctly then its True Negative.

# In[ ]:


#True Negative
def true_negative(ground_truth, prediction):
    tn = 0
    for gt, pred in zip(ground_truth, prediction):
        if gt == 0 and pred == 0:
            tn +=1
    return tn


# ### False Positive:
# If model predicts Positive class incorrectly then its False Positive.

# In[ ]:


#False Positive
def false_positive(ground_truth, prediction):
    fp = 0
    for gt, pred in zip(ground_truth, prediction):
        if gt == 0 and pred == 1:
            fp +=1
    return fp


# ### False Negative:
# If model predicts Negative class incorrectly then its False Negative.

# In[ ]:


#False Negative
def false_negative(ground_truth, prediction):
    fn = 0
    for gt, pred in zip(ground_truth, prediction):
        if gt == 1 and pred == 0:
            fn +=1
    return fn


# ### True Positive Rate (Sensitivity or Recall) = TP/ (TP + FN)

# In[ ]:


def tpr(ground_truth, prediction):
    tp = true_positive(ground_truth, prediction)  
    fn = false_negative(ground_truth, prediction)  
    pr = tp/ (tp + fn)  
    return pr


# ### False Positive Rate (Sensitivity or Recall) = FP/ (TN + FP)

# In[ ]:


def fpr(ground_truth, prediction):
    fp = false_positive(ground_truth, prediction)  
    tn = true_negative(ground_truth, prediction)  
    fr = fp/ (tn + fp)  
    return fr


# ### ROC and AUC 

# In[ ]:


true_positive_rate = []
false_poitive_rate = []

for threshold in thresholds:  
    #calculate predictions for threshold  
    value_pred = [1 if x >= threshold else 0 for x in prediction]   
    value_tpr = tpr(ground_truth, value_pred)   
    value_fpr = fpr(ground_truth, value_pred)  
    true_positive_rate.append(value_tpr)  
    false_poitive_rate.append(value_fpr) 


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
plt.figure(figsize=(7, 7))  
plt.fill_between(false_poitive_rate, true_positive_rate, alpha=0.4)  
plt.plot(false_poitive_rate, true_positive_rate, lw=3)  
plt.xlim(0, 1.0)  
plt.ylim(0, 1.0)  
plt.xlabel('FPR', fontsize=15)  
plt.ylabel('TPR', fontsize=15)  
plt.show() 

