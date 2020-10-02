#!/usr/bin/env python
# coding: utf-8

# # INCOME CLASS PREDICTION USING MACHINE LEARING
# 
# Hello all, for this classification task I have used the Census Income Dataset (Both data and test set) from UCI <br>
# (https://archive.ics.uci.edu/ml/datasets/census+income)

# In[ ]:


#Import Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split,cross_val_score,RandomizedSearchCV
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.under_sampling import OneSidedSelection
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_curve, roc_auc_score, classification_report
pd.set_option('display.max_columns', None)
plt.rcParams['figure.figsize']=(16, 8.27) #set graphs size to A4 dimensions
sns.set_style('darkgrid')
sns.set(font_scale = 1.4)


# In[ ]:


#import train and test set from UCI links

train = pd.read_csv('http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data', header = None)

test = pd.read_csv('http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test' , skiprows = 1, header = None)

col_labels = ['age', 'workclass', 'fnlwgt', 'education', 'education_num','marital_status', 'occupation','relationship', 
              'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country', 'wage_class']
train.columns = col_labels
test.columns = col_labels


# # Exploratory Data Analysis

# Let's get deeper and exploring the data

# ###### TRAIN SET

# In[ ]:


train.info()


# In[ ]:


train.head()


# In[ ]:


train.describe()


# In[ ]:


#find out numerical and categorical features for train set

numerical_features=[feature for feature in train.columns if train[feature].dtype!='O']
categorical_features=[feature for feature in  train.columns if  train[feature].dtype=='O' and feature!='wage_class']

print('categorical features: ''\n',categorical_features)
print('\n')
print('numerical features: ''\n',numerical_features)


# In[ ]:


#Check for missing values
for feature in train.columns:
    print(feature,':', train[feature].isnull().sum())


# In[ ]:


#Find out distinct values for each numerical feature
for feature in numerical_features:
    print(feature,':', train[feature].nunique())


# In[ ]:


#Find out distinct values for each categorical feature
for feature in categorical_features:
    print(feature,':', train[feature].nunique())


# In[ ]:


#for each categorical value we calculate relative frequency of unique classes.
for feature in categorical_features:
    freq=train[feature].value_counts('f').rename_axis(feature).reset_index(name='relative frequency')
    print('\n')
    print(freq)


# In[ ]:


#Check for imbalanced target (In our case 76% are in class <=50K and 24% >50K)
train['wage_class'].value_counts('f') 


# ###### Now let's do some graphs for train set in order to find key relationships !!!

# In[ ]:


ax=sns.countplot(train['wage_class'],hue=train['wage_class'],edgecolor='k',palette='Set2')
ax.set_title('Wage Class Count')
ax.set_xlabel('Wage Class')
plt.show()


# In[ ]:


ax=sns.countplot(train['marital_status'], hue=train['wage_class'],edgecolor='k',palette='Set2')
ax.set_title('Marital Status / Wage Class')
ax.set_xlabel('Marital Status')
plt.show()


# In[ ]:


ax=sns.countplot(train['sex'], hue=train['wage_class'],edgecolor='k',palette='Set2')
ax.set_title('Sex / Wage Class')
ax.set_xlabel('Sex')
plt.show()


# In[ ]:


ax=sns.countplot(train['race'], hue=train['wage_class'],edgecolor='k',palette='Set2')
ax.set_title('Race / Wage Class')
ax.set_xlabel('Race')
plt.show()


# In[ ]:


ax=sns.countplot(train['relationship'], hue=train['wage_class'],edgecolor='k',palette='Set2')
ax.set_title('Relationship Status / Wage Class')
ax.set_xlabel('Relationship')
plt.show()


# In[ ]:


ax=sns.countplot(train['education'], hue=train['wage_class'],edgecolor='k',palette='Set2')
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
ax.set_title('Education / Wage Class')
ax.set_xlabel('Education')
plt.show()


# In[ ]:


ax=sns.countplot(train['occupation'], hue=train['wage_class'],edgecolor='k',palette='Set2')
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
ax.set_title('Occupation / Wage Class')
ax.set_xlabel('Occupation')
plt.show()


# In[ ]:


ax=sns.distplot(train['age'],hist_kws=dict(edgecolor="k", linewidth=2),kde_kws={"color": "#ce0d55", "lw": 2})
ax.set_title('Age Distribution')
ax.set_xlabel('Age')
plt.show()


# In[ ]:


ax=sns.distplot(train['hours_per_week'],hist_kws=dict(edgecolor="k", linewidth=2),kde_kws={"color": "#ce0d55", "lw": 2})
ax.set_title('Hours/Week Distribution')
ax.set_xlabel('Hours Per Week')
plt.show()


# In[ ]:


ax=sns.distplot(train['capital_loss'],bins=10,kde=False,hist_kws=dict(edgecolor="k", linewidth=2))
ax.set_title('Capital Loss Histogram')
ax.set_xlabel('Capital Loss')
plt.show()


# In[ ]:


ax=sns.distplot(train['capital_gain'],bins=10,kde=False,hist_kws=dict(edgecolor="k", linewidth=2))
ax.set_title('Capital Gain Histogram')
ax.set_xlabel('Capital Gain')
plt.show()


# In[ ]:


#median age for each wage_class
ax=sns.barplot(train.groupby('wage_class')['age'].median().index,train.groupby('wage_class')['age'].median().values,
               edgecolor='k', palette='Set2')
ax.set_ylabel('Age')
ax.set_xlabel('Wage Class')
ax.set_title('Median Age / Wage Class')
plt.show()


# In[ ]:


corr_train=train.copy()
for feature in categorical_features:
    corr_train.drop(feature,axis=1,inplace=True)

    
ax=sns.heatmap(corr_train.corr(), cmap='RdYlGn',annot=True)
ax.set_title('Correlation Map')
plt.show()


# ###### TEST SET

# Now we have to follow the same procedure for the test set in order to assure that both train set and test set come from same distribution

# In[ ]:


test.info()


# In[ ]:


test.head()


# In[ ]:


train.describe()


# In[ ]:


#find out numerical and categorical features for test set

numerical_features_test=[feature for feature in test.columns if test[feature].dtype!='O']
categorical_features_test=[feature for feature in  test.columns if  test[feature].dtype=='O' and feature!='wage_class']

print('categorical features: ''\n',categorical_features_test)
print('\n')
print('numerical features: ''\n',numerical_features_test)


# In[ ]:


#Check for missing values
for feature in test.columns:
    print(feature,':', test[feature].isnull().sum())


# In[ ]:


#Find out distinct values for each numerical feature
for feature in numerical_features_test:
    print(feature,':', test[feature].nunique())


# In[ ]:


#Find out distinct values for each categorical feature
for feature in categorical_features_test:
    print(feature,':', test[feature].nunique())


# In[ ]:


#for each categorical value we calculate relative frequency of unique classes.
for feature in categorical_features_test:
    freq_test=test[feature].value_counts('f').rename_axis(feature).reset_index(name='relative frequency')
    print('\n')
    print(freq_test)


# In[ ]:


#Check for imbalanced target (In our case approx 76% are in class <=50K and  approx 24% >50K)
test['wage_class'].value_counts('f') 


# ###### Now let's do some graphs for test in order to find key relationships !!!

# In[ ]:


ax=sns.countplot(test['wage_class'],hue=test['wage_class'], edgecolor='k',palette='Set2')
ax.set_title('Wage Class Count')
ax.set_xlabel('Wage Class')
plt.show()


# In[ ]:


ax=sns.countplot(test['marital_status'], hue=test['wage_class'],edgecolor='k', palette='Set2')
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
ax.set_title('Marital Status / Wage Class')
ax.set_xlabel('Marital Status')
plt.show()


# In[ ]:


ax=sns.countplot(test['sex'], hue=test['wage_class'],edgecolor='k', palette='Set2')
ax.set_title('Sex / Wage Class')
ax.set_xlabel('Sex')
plt.show()


# In[ ]:


ax=sns.countplot(test['race'], hue=test['wage_class'],edgecolor='k', palette='Set2')
ax.set_title('Race / Wage Class')
ax.set_xlabel('Race')
plt.show()


# In[ ]:


ax=sns.countplot(test['relationship'], hue=test['wage_class'],edgecolor='k', palette='Set2')
ax.set_title('Relationship Status / Wage Class')
ax.set_xlabel('Relationship')
plt.show()


# In[ ]:


ax=sns.countplot(test['education'], hue=test['wage_class'],edgecolor='k', palette='Set2')
ax.set_title('Education / Wage Class')
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
ax.set_xlabel('Education')
plt.show()


# In[ ]:


ax=sns.countplot(test['occupation'], hue=test['wage_class'],edgecolor='k', palette='Set2')
ax.set_title('Occupation / Wage Class')
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
ax.set_xlabel('Occupation')
plt.show()


# In[ ]:


ax=sns.distplot(test['age'],hist_kws=dict(edgecolor="k", linewidth=2),kde_kws={"color": "#ce0d55", "lw": 2})
ax.set_title('Age Distribution')
ax.set_xlabel('Age')
plt.show()


# In[ ]:


ax=sns.distplot(test['hours_per_week'],hist_kws=dict(edgecolor="k", linewidth=2),kde_kws={"color": "#ce0d55", "lw": 2})
ax.set_title('Hours / Week Distribution')
ax.set_xlabel('Hours per Week')
plt.show()


# In[ ]:


ax=sns.distplot(test['capital_loss'],bins=10,kde=False,hist_kws=dict(edgecolor="k", linewidth=2))
ax.set_title('Capital Loss Histogram')
ax.set_xlabel('Capital Loss')
plt.show()


# In[ ]:


ax=sns.distplot(test['capital_gain'],bins=10,kde=False,hist_kws=dict(edgecolor="k", linewidth=2))
ax.set_title('Capital Gain Histogram')
ax.set_xlabel('Capital Gain')
plt.show()


# In[ ]:


#median age for each wage_class
ax=sns.barplot(test.groupby('wage_class')['age'].median().index,test.groupby('wage_class')['age'].median().values,
               edgecolor='k', palette='Set2')
ax.set_ylabel('Age')
ax.set_xlabel('Wage Class')
ax.set_title('Median Age / Wage Class')
plt.show()


# In[ ]:


corr_test=test.copy()
for feature in categorical_features_test:
    corr_test.drop(feature,axis=1,inplace=True)

    
ax=sns.heatmap(corr_test.corr(), cmap='RdYlGn',annot=True)
ax.set_title('Correlation Map')
plt.show()


# # Feature Engineering

# In[ ]:


#convert <=50K and >50K to 0, 1 respectively
encoder=LabelEncoder()
train['wage_class']=encoder.fit_transform(train['wage_class'])


# In[ ]:


categorical_features=[feature for feature in  train.columns if  train[feature].dtype=='O' and feature!='wage_class']
for feature in categorical_features:
    freq=train[feature].value_counts().rename_axis(feature).reset_index(name='frequency')
    print('\n')
    print(freq)


# In[ ]:


#transform country feature to be 1 if country is the United States. Otherwise is equal to 0
train['native_country']=np.where(train['native_country']==' United-States',1,0)


# In[ ]:


#transform marital status and concatenate some classes to reduce distinct classes
train['marital_status']=train['marital_status'].replace({' Married-civ-spouse': 'Married', ' Never-married': 'Single',  
                                                        ' Separated':'Divorced', ' Married-spouse-absent' : 'Divorced', 
                                                         ' Divorced':'Divorced', 
                                                         ' Married-AF-spouse' :'Divorced', ' Widowed':'Widowed' })


# In[ ]:


#transform workclass feature to be 1 if the workclass is Private and 0 if doesn't
train['workclass']=np.where(train['workclass']==' Private',1,0)


# In[ ]:


#transform workclass feature to be 1 if the Sex is Male and 0 if doesn't
train['sex']=np.where(train['sex']==' Male',1,0)


# In[ ]:


#transform workclass feature to be 1 if the Race is White and 0 if doesn't
train['race']=np.where(train['race']==' White',1,0)


# In[ ]:


#create ordered label for education 
education_mapping={' Preschool':0,' 1st-4th':1,' 5th-6th':2,' 7th-8th':3,' 9th':4,' 10th':5,
                   ' 11th':6,' 12th':7,' HS-grad':8,' Some-college':0,' Assoc-acdm':10,
                   ' Assoc-voc':11, ' Bachelors':12, ' Prof-school':13, ' Masters':14,' Doctorate':15
                   }
train['education']=train['education'].map(education_mapping)


# In[ ]:


relationship_ordered=train.groupby(['relationship'])['wage_class'].count().sort_values().index
relationship_ordered={k:i for i,k in enumerate(relationship_ordered,0)}
train['relationship']=train['relationship'].map(relationship_ordered)  


# In[ ]:


occupation_ordered=train.groupby(['occupation'])['wage_class'].count().sort_values().index
occupation_ordered={k:i for i,k in enumerate(occupation_ordered,0)}
train['occupation']=train['occupation'].map(occupation_ordered)


# In[ ]:


marital_ordered=train.groupby(['marital_status'])['wage_class'].count().sort_values().index
marital_ordered={k:i for i,k in enumerate(marital_ordered,0)}
train['marital_status']=train['marital_status'].map(marital_ordered)


# In[ ]:


train.head(10)


# In[ ]:


train.isnull().sum()


# In[ ]:


train.drop('fnlwgt',axis=1,inplace=True) # it is not a useful feature for predicting the wage class


# In[ ]:


#scaling the train set with StandardScaler
scaler=StandardScaler()
scaled_features_train=scaler.fit_transform(train.drop('wage_class',axis=1))
scaled_features_train=pd.DataFrame(scaled_features_train, columns=train.drop('wage_class',axis=1).columns)


# In[ ]:


#undersampling the train set
under=OneSidedSelection()
X_train_res, y_train_res=under.fit_resample(scaled_features_train, train['wage_class'])


#oversampling the train set
sm=SMOTE()
X_train_res, y_train_res= sm.fit_resample(X_train_res, y_train_res)

X_train_res=pd.DataFrame(X_train_res, columns=train.drop('wage_class',axis=1).columns)



#creating the final train 
final_train=pd.concat([X_train_res, y_train_res],axis=1)


# In[ ]:


final_train.head(10)


# In[ ]:


final_train.info()


# In[ ]:


final_train['wage_class'].value_counts() #now train set is balanced


# ###### Test Set

# Now for the test set we have to apply all the transformations that we did before for the train set

# In[ ]:


test['wage_class']=np.where(test['wage_class']== ' >50K.',1,0)


# In[ ]:


test['wage_class'].value_counts()


# In[ ]:


#transform country feature to be 1 if country is the United States. Otherwise is equal to 0
test['native_country']=np.where(test['native_country']==' United-States',1,0)


# In[ ]:


#transform workclass feature to be 1 if the workclass is Private and 0 if doesn't
test['workclass']=np.where(test['workclass']==' Private',1,0)


# In[ ]:


#transform workclass feature to be 1 if the Sex is Male and 0 if doesn't
test['sex']=np.where(test['sex']==' Male',1,0)


# In[ ]:


test['race']=np.where(test['race']==' White',1,0)


# In[ ]:


test['education']=test['education'].map(education_mapping)


# In[ ]:


test['relationship']=test['relationship'].map(relationship_ordered) 


# In[ ]:


test['occupation']=test['occupation'].map(occupation_ordered)


# In[ ]:


#transform marital status and concatenate some classes to reduce distinct classes
test['marital_status']=test['marital_status'].replace({' Married-civ-spouse': 'Married', ' Never-married': 'Single',  
                                                        ' Separated':'Divorced', ' Married-spouse-absent' : 'Divorced', 
                                                         ' Divorced':'Divorced', 
                                                         ' Married-AF-spouse' :'Divorced', ' Widowed':'Widowed' })


# In[ ]:


test['marital_status']=test['marital_status'].map(marital_ordered)


# In[ ]:


test.head(10)


# In[ ]:


test.isnull().sum()


# In[ ]:


test.drop('fnlwgt',axis=1,inplace=True)


# In[ ]:


scaled_features_test=scaler.transform(test.drop('wage_class',axis=1))
scaled_features_test=pd.DataFrame(scaled_features_test, columns=test.drop('wage_class',axis=1).columns)

final_test=pd.concat([scaled_features_test,test['wage_class']],axis=1)


# In[ ]:


final_test.head(10)


# # Feature Selection

# In[ ]:


X=final_train.drop('wage_class',axis=1)
y=final_train['wage_class']


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)


# In[ ]:


model=xgb.XGBClassifier()


# In[ ]:


model.fit(X_train, y_train)


# In[ ]:


feat_importances = pd.Series(model.feature_importances_, index=X_train.columns)
feat_importances=feat_importances.nlargest(X_train.shape[1])
ax=sns.barplot(feat_importances.index, feat_importances.values ,edgecolor='k', palette='Set2')
ax.set_ylabel('Feature Importance')
ax.set_xlabel('Features')
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.show()


# As we can see, Race, Workclass and Native Country are not important features and we will drop them

# In[ ]:


final_train.drop(['native_country','race','workclass'],axis=1,inplace=True)
final_test.drop(['native_country','race','workclass'],axis=1,inplace=True)


# # Model Selection

# #### XGBoost

# In[ ]:


xgb_classifier=xgb.XGBClassifier()
score_xgb=cross_val_score(xgb_classifier, X, y, cv=5, n_jobs=-1)


# #### Random Forest

# In[ ]:


rf=RandomForestClassifier()
score_rf=cross_val_score(rf, X, y, cv=5, n_jobs=-1)


# #### SVC

# In[ ]:


svc=SVC()
score_svc=cross_val_score(svc, X, y, cv=5, n_jobs=-1)


# #### Logistic Regression

# In[ ]:


logReg=LogisticRegression()
score_logReg=cross_val_score(logReg, X, y, cv=5, n_jobs=-1)


# #### KNN

# In[ ]:


knn=KNeighborsClassifier()
score_knn=cross_val_score(knn, X, y, cv=5, n_jobs=-1)


# #### AdaBoost

# In[ ]:


adaboost=AdaBoostClassifier()
score_adaboost=cross_val_score(adaboost, X, y, cv=5, n_jobs=-1)


# In[ ]:


scores=pd.DataFrame({'Model':['XGBoost','Random Forest','SVC','Logistic Regression','KNN','Adaboost'],
                    'Accuracy':[score_xgb.mean(),score_rf.mean(),score_svc.mean(),score_logReg.mean(),score_knn.mean(),
                             score_adaboost.mean()]})


# In[ ]:


print(scores)


# # Final Model Evaluation

# At this point we are going to evaluate the model in the initial test set

# In[ ]:


X_train=final_train.drop('wage_class',axis=1)
y_train=final_train['wage_class']

X_test=final_test.drop('wage_class',axis=1)
y_test=final_test['wage_class']


# In[ ]:


xgb_classifier.fit(X_train,y_train)
y_pred=xgb_classifier.predict(X_test)


# In[ ]:


print(classification_report(y_test,y_pred))


# In[ ]:


xgboost_auc=roc_auc_score(y_test,y_pred)
r_probs = [0 for _ in range(len(y_test))]
random_auc = roc_auc_score(y_test, r_probs)
print(xgboost_auc)


# In[ ]:


probs=xgb_classifier.predict_proba(X_test)


# In[ ]:


probs=probs[:,1] #keep probabilities for one class


# In[ ]:


r_fpr, r_tpr, _=roc_curve(y_test,probs)
x=np.arange(0,1.01,0.01)


# In[ ]:


plt.plot(r_fpr, r_tpr, label='XGBoost (AUROC = %0.3f)' % xgboost_auc)
plt.plot(x,x, linestyle='--', label='Random prediction (AUROC = %0.3f)' % random_auc)
plt.legend()
plt.title('ROC CURVE')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.show()

