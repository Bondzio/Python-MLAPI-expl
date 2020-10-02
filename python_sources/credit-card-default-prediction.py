#!/usr/bin/env python
# coding: utf-8

# ## Predicted with 80% accuracy on the previous months credit card data wether a person will default in his upcoming month payment or not. Used Logistic regression with hyper-parameter tunning to find the best fit model and important features which matters most in default payment.

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import os
IS_LOCAL = False

if(IS_LOCAL):
    PATH="../input/default-of-credit-card-clients-dataset"
else:
    PATH="../input"
print(os.listdir(PATH))

data=pd.read_csv(PATH+"/default-of-credit-card-clients-dataset/UCI_Credit_Card.csv")


# In[ ]:


data.head()


# In[ ]:


data.drop(['ID'],axis=1,inplace=True)


# In[ ]:


data.rename(columns=lambda x:x.lower(),inplace=True)


# In[ ]:


data.rename(columns={'default.payment.next.month':'default'},inplace=True)


# In[ ]:


print(data.default.value_counts().index[0],(data.default.value_counts()[0]/len(data)*100),data.default.value_counts().index[1],(data.default.value_counts()[1]/len(data)*100))


# In[ ]:


data.head()


# In[ ]:


def check_count(var):
    return(sorted(data[var].unique()))


# In[ ]:


#check_count('sex')
#check_count('education')
#check_count('marriage')
check_count('pay_0')


# In[ ]:


pay_features=['pay_0','pay_2','pay_3','pay_4','pay_5','pay_6']

for p in pay_features:
    data.loc[data[p]<0,p]=0


# In[ ]:


check_count('pay_0')
#check_count('pay_6')


# In[ ]:


def order_cat(df,col,order):
    df[col]=df[col].astype('category')
    df[col]=df[col].cat.reorder_categories(order,ordered=True)
    df[col]=df[col].cat.codes.astype(int)


for col in pay_features:
    order_cat(data,col,check_count(col))


# In[ ]:


data['grad_school']=(data['education']==1).astype('int')
data['university']=(data['education']==2).astype('int')
data['high_school']=(data['education']==3).astype('int')
data['others_education']=(data['education']==4).astype('int')
data['unknown_education']=(~data['education'].isin([1,2,3,4])).astype('int')


data['male']=(data['sex']==1).astype(int)
data['female']=(data['sex']==0).astype(int)

data['married']=(data['marriage']==1).astype(int)
data['single']=(data['marriage']==2).astype(int)
data['other_marriage']=(~data['marriage'].isin([1,2])).astype(int)


# In[ ]:


data.drop(['sex','education','marriage'],axis=1,inplace=True)


# In[ ]:


data.head()


# In[ ]:


from sklearn.preprocessing import RobustScaler

scaler=RobustScaler()

label='default'
X=data.drop(label,axis=1)

features=X.columns

X=scaler.fit_transform(X)
y=data[label]


# In[ ]:


def CFMatrix(cm,labels=['pay','default']):
    df=pd.DataFrame(data=cm,index=labels,columns=labels)
    df.index.name='TRUE'
    df.columns.name='PREDICTION'
    df.loc['Total']=df.sum()
    df['Total']=df.sum(axis=1)
    return df


# In[ ]:


from sklearn.metrics import accuracy_score,precision_score,recall_score, confusion_matrix

def predict(model,X_test,y_test):
    
    pred=model.predict(X_test)
    
    acc_score=accuracy_score(y_pred=pred,y_true=y_test)
    precision=precision_score(y_pred=pred,y_true=y_test)
    recall=recall_score(y_pred=pred,y_true=y_test)

    print('Acc Score:',acc_score)
    print('Precission: ',precision)
    print('Recall: ',recall)
    
    return CFMatrix(confusion_matrix(y_pred=pred,y_true=y_test))


# In[ ]:


from sklearn.metrics import roc_auc_score,roc_curve

def plot_roc_curve(model,X_test,y_test):
    
    log_roc_auc=roc_auc_score(y_test,model.predict(X_test))
    
    fpr,tpr,thresholds=roc_curve(y_test,model.predict_proba(X_test)[:,1])
    
    plt.figure()
    plt.plot(fpr,tpr,label='Logistic Regression (area = %0.2f)'%log_roc_auc)
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([0.0,1.0])
    plt.ylim([0.0,1.05])

    plt.xlabel('False Positive Rate')
    plt.ylabel('True Posiive Rate')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    plt.show()
    return


# In[ ]:


from sklearn.metrics import precision_recall_curve

def recall_to_precision(model,X_test,y_test):
    precision_p,recall_p,thresholds=precision_recall_curve(y_true=y_test,probas_pred=model.predict_proba(X_test)[:,1])

    fig,ax=plt.subplots(figsize=(8,5))

    ax.plot(thresholds,precision_p[1:],label='Precision')
    ax.plot(thresholds,recall_p[1:],label='Recall')

    ax.set_xlabel('Classification Threshold')
    ax.set_ylabel('Precision, Recall')
    ax.set_title('Logistic Regression Classifier: Precision-Recall')
    ax.hlines(y=0.6,xmin=0,xmax=1,color='red')
    ax.legend()
    ax.grid();
    return


# In[ ]:


def predict_threshold(model,X_test,y_test,threshold):
    pred_02_prob=model.predict_proba(X_test)[:,1]

    pred_02= (pred_02_prob >= threshold).astype('int')

    acc_score=accuracy_score(y_pred=pred_02,y_true=y_test)
    precision=precision_score(y_pred=pred_02,y_true=y_test)
    recall=recall_score(y_pred=pred_02,y_true=y_test)

    print('Acc Score:',acc_score)
    print('Precission: ',precision)
    print('Recall: ',recall)

    return CFMatrix(confusion_matrix(y_pred=pred_02,y_true=y_test))


# ## Feature Importance:

# In[ ]:


def plot_feature_imp(model,features):
    
    df=pd.DataFrame({'features':features.tolist(),'relation':model.coef_.reshape(X_train.shape[1]).tolist()})
    df=df.sort_values(by='relation',ascending=False)
    
    p_pos= np.arange(len(df.loc[df['relation']>=0,'relation']))
    n_pos= np.arange(len(p_pos),len(p_pos)+len(df.loc[df['relation']<0,'relation']))
    
    plt.figure(figsize=(13,16))
    plt.barh(p_pos,df.loc[df['relation']>=0,'relation'])
    plt.barh(n_pos,df.loc[df['relation']<0,'relation'])
    plt.yticks(np.arange(len(p_pos)+len(n_pos)),df['features'].tolist())
    plt.title('Feature Coefficents with respect to Label')
    plt.show()
    return


# ## Normal Model

# In[ ]:


from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.15,random_state=99,stratify=y)

from sklearn.linear_model import LogisticRegression

model= LogisticRegression(random_state=0)

model.fit(X_train,y_train)

predict(model,X_test,y_test)


# In[ ]:


plot_roc_curve(model,X_test,y_test)


# ### ROC curve shows 0.64 for AUC score.
# ### But we want ot minimize the False Negative rate with respect to True positive, because we don't wan't to classify any person who is potential defaulter to be classified as non-defaulter. We can tolerate with some False Positive cases i.e. Non defaulters classified as defaulters. So we require high Recall rate, so lets compare the model to find true positive with respect to false positive rate.

# In[ ]:


recall_to_precision(model,X_test,y_test)


# ### So from graph we can see with threshold of 0.2 we can can get Recall of 60%. 
# ### So lets now predict the test data with threshold of 0.2.

# In[ ]:


predict_threshold(model,X_test,y_test,0.2)


# In[ ]:


plot_feature_imp(model,features)


# ## Hyper-Parameter Tuning

# In[ ]:


#dual=[True,False]
max_iter=[100,110,120,130,140]
penalty=['l1','l2']
#C=np.logspace(-4,4,20)
class_weight=['balanced']
solver=['saga']

#param_grid=dict(dual=dual,max_iter=max_iter,penalty=penalty,C=C,class_weight=class_weight,solver=solver)
param_grid=dict(max_iter=max_iter,penalty=penalty,class_weight=class_weight,solver=solver)


# In[ ]:


from sklearn.model_selection import GridSearchCV

grid=GridSearchCV(estimator=model,param_grid=param_grid,cv=4,n_jobs=-1)
grid.fit(X_train,y_train)


# In[ ]:


tuned_model=grid.best_estimator_
tuned_model


# In[ ]:


predict(tuned_model,X_test,y_test)


# In[ ]:


plot_roc_curve(tuned_model,X_test,y_test)


# In[ ]:


recall_to_precision(tuned_model,X_test,y_test)


# In[ ]:


plot_feature_imp(tuned_model,features)

