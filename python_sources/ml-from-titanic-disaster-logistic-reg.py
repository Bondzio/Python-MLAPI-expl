#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Supress Warnings
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn import metrics
from sklearn.metrics import precision_score, recall_score


# In[ ]:


pd.set_option('display.max_columns', 500)


# Reading the data

# In[ ]:


titanic_train = pd.read_csv("/kaggle/input/titanic/train.csv")
titanic_train.head()


# In[ ]:


titanic_train.shape


# In[ ]:


titanic_train.info()


# #### Data Preparation

# ##### Missing value treatment

# In[ ]:


titanic_train.isnull().sum()


# In[ ]:


titanic_train.Cabin.value_counts(dropna = False)


# In[ ]:


titanic_train.Cabin = titanic_train.Cabin.fillna("Unknown_Cabin")


# In[ ]:


titanic_train.Cabin = titanic_train.Cabin.str[0]


# In[ ]:


titanic_train.Cabin.value_counts()


# In[ ]:


titanic_train.isna().sum()/titanic_train.shape[0] *100


# In[ ]:


titanic_train.Embarked.value_counts(dropna = False)


# In[ ]:


titanic_train.Embarked = titanic_train.Embarked.fillna('S')


# In[ ]:


titanic_train['Title'] = titanic_train.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
titanic_train = titanic_train.drop('Name',axis=1)


# In[ ]:


titanic_train.head()


# In[ ]:


#let's replace a few titles -> "other" and fix a few titles
titanic_train['Title'] = np.where((titanic_train.Title=='Capt') | (titanic_train.Title=='Countess') |                                   (titanic_train.Title=='Don') | (titanic_train.Title=='Dona')| (titanic_train.Title=='Jonkheer')                                   | (titanic_train.Title=='Lady') | (titanic_train.Title=='Sir') | (titanic_train.Title=='Major') |                                   (titanic_train.Title=='Rev') | (titanic_train.Title=='Col'),'Other',titanic_train.Title)

titanic_train['Title'] = titanic_train['Title'].replace('Ms','Miss')
titanic_train['Title'] = titanic_train['Title'].replace('Mlle','Miss')
titanic_train['Title'] = titanic_train['Title'].replace('Mme','Mrs')


# In[ ]:


titanic_train.Title.value_counts()


# For imputing the missing value from the age we need to calculate average age value of title and then impute the average value to the missing one

# In[ ]:


titanic_train.groupby('Title').Age.mean()


# In[ ]:


titanic_train["Age"] = np.where((titanic_train.Age.isnull()) & (titanic_train.Title == 'Master'), 5,                               np.where((titanic_train.Age.isnull()) & (titanic_train.Title=='Miss'),22,                                        np.where((titanic_train.Age.isnull()) & (titanic_train.Title=='Mr'),32,                                                 np.where((titanic_train.Age.isnull()) & (titanic_train.Title=='Mrs'),36,                                                          np.where((titanic_train.Age.isnull()) & (titanic_train.Title=='Other'),47,                                                                   np.where((titanic_train.Age.isnull()) & (titanic_train.Title=='Dr'),42,titanic_train.Age))))))


# In[ ]:


titanic_train.isnull().sum()/titanic_train.shape[0] *100


# In[ ]:


titanic_train.shape


# In[ ]:


col_list = list(titanic_train.columns)
for col in col_list:
    print(titanic_train[col].value_counts())
    print("-----------------------------")


# In[ ]:


titanic_train = titanic_train.drop("Ticket", axis=1)
titanic_train.head()


# ### Dummy variable

# In[ ]:


dummy_1 = pd.get_dummies(titanic_train["Embarked"], prefix= "Embarked", drop_first=True)
dummy_2 = pd.get_dummies(titanic_train["Sex"], drop_first=False)
Pclass = pd.get_dummies(titanic_train["Pclass"], prefix= "Pclass")
siblings = pd.get_dummies(titanic_train["SibSp"], prefix= "SibSp")
Parch = pd.get_dummies(titanic_train["Parch"], prefix= "Parch")
cabin = pd.get_dummies(titanic_train["Cabin"], prefix= "Cabin")
Title = pd.get_dummies(titanic_train["Title"], prefix= "Title")


# In[ ]:


titanic_train = pd.concat([titanic_train, dummy_1, dummy_2, Pclass, siblings, Parch], axis=1)
titanic_train = titanic_train.drop(["Embarked","PassengerId", "Sex", "Pclass", "SibSp", "Parch", "Cabin", "Title"], axis=1)
titanic_train.head()


# ### Feature Scaling

# In[ ]:


scalar = MinMaxScaler()
scale_var = ["Age", "Fare"]
titanic_train[scale_var] = scalar.fit_transform(titanic_train[scale_var])
titanic_train.head()


# In[ ]:


y_train = titanic_train.pop("Survived")
y_train.head()


# In[ ]:


X_train = titanic_train
X_train.head()


# In[ ]:


plt.figure(figsize=(20, 15))
sns.heatmap(X_train.corr(), annot=True)
plt.show()


# ### Model Building

# In[ ]:


logreg = LogisticRegression()


# In[ ]:


rfe = RFE(logreg, 12)
rfe = rfe.fit(X_train, y_train)


# In[ ]:


list(zip(X_train.columns, rfe.support_, rfe.ranking_))


# In[ ]:


col_support = X_train.columns[rfe.support_]
col_support


# In[ ]:


X_train_sm = sm.add_constant(X_train[col_support])
logmodel1 = sm.GLM(y_train, X_train_sm, family=sm.families.Binomial()).fit()
logmodel1.summary()


# Most of the feature having P values more than 0.05 we have to drop those values but first calculate the vif

# In[ ]:


col_support = col_support.drop(["SibSp_8"])


# In[ ]:


X_train_sm = sm.add_constant(X_train[col_support])
logmodel2 = sm.GLM(y_train, X_train_sm, family=sm.families.Binomial()).fit()
logmodel2.summary()


# In[ ]:


col_support = col_support.drop(["Parch_4"])


# In[ ]:


X_train_sm = sm.add_constant(X_train[col_support])
logmodel3 = sm.GLM(y_train, X_train_sm, family=sm.families.Binomial()).fit()
logmodel3.summary()


# In[ ]:


vif = pd.DataFrame()
vif["Features"] = col_support
vif["VIF"] = [variance_inflation_factor(X_train[col_support].values, i) for i in range(X_train[col_support].shape[1])]
vif["VIF"] = round(vif['VIF'], 2)
vif = vif.sort_values(by="VIF", ascending=False)
vif


# In[ ]:


col_support = col_support.drop(["SibSp_3"])


# In[ ]:


X_train_sm = sm.add_constant(X_train[col_support])
logmodel4 = sm.GLM(y_train, X_train_sm, family=sm.families.Binomial()).fit()
logmodel4.summary()


# In[ ]:


col_support = col_support.drop("Fare")


# In[ ]:


X_train_sm = sm.add_constant(X_train[col_support])
logmodel5 = sm.GLM(y_train, X_train_sm, family=sm.families.Binomial()).fit()
logmodel5.summary()


# In[ ]:


vif = pd.DataFrame()
vif["Features"] = col_support
vif["VIF"] = [variance_inflation_factor(X_train[col_support].values, i) for i in range(X_train[col_support].shape[1])]
vif["VIF"] = round(vif['VIF'], 2)
vif = vif.sort_values(by="VIF", ascending=False)
vif


# In[ ]:


col_support = col_support.drop(["male"])


# In[ ]:


X_train_sm = sm.add_constant(X_train[col_support])
logmodel6 = sm.GLM(y_train, X_train_sm, family=sm.families.Binomial()).fit()
logmodel6.summary()


# In[ ]:


vif = pd.DataFrame()
vif["Features"] = col_support
vif["VIF"] = [variance_inflation_factor(X_train[col_support].values, i) for i in range(X_train[col_support].shape[1])]
vif["VIF"] = round(vif['VIF'], 2)
vif = vif.sort_values(by="VIF", ascending=False)
vif


# In[ ]:


col_support = col_support.drop(["Age"])


# In[ ]:


X_train_sm = sm.add_constant(X_train[col_support])
logmodel6 = sm.GLM(y_train, X_train_sm, family=sm.families.Binomial()).fit()
logmodel6.summary()


# In[ ]:


vif = pd.DataFrame()
vif["Features"] = col_support
vif["VIF"] = [variance_inflation_factor(X_train[col_support].values, i) for i in range(X_train[col_support].shape[1])]
vif["VIF"] = round(vif['VIF'], 2)
vif = vif.sort_values(by="VIF", ascending=False)
vif


# In[ ]:


y_train_pred = logmodel6.predict(X_train_sm)


# In[ ]:


y_train_pred[:10].values


# In[ ]:


y_train_pred_final = pd.DataFrame({'Survived': y_train.values, 'survived_prob':y_train_pred})
y_train_pred_final.head()


# In[ ]:


y_train_pred_final['Predicted_survived'] = y_train_pred_final.survived_prob.map(lambda x : 1 if x > 0.5 else 0)
y_train_pred_final.head()


# ### Ploting ROC curve and calculate the cutoff

# In[ ]:


def draw_roc_curve(actual, prob):
    fpr, tpr, threshold = metrics.roc_curve(actual, prob, drop_intermediate=False)
    auc_score = metrics.roc_auc_score(actual, prob)
    plt.figure(figsize=(5, 5))
    plt.plot( fpr, tpr, label='ROC curve (area = %0.2f)' % auc_score )
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate or [1 - True Negative Rate]')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

    return None


# In[ ]:


fpr, tpr, thresholds = metrics.roc_curve(y_train_pred_final.Survived, y_train_pred_final.Predicted_survived, drop_intermediate = False )


# In[ ]:


draw_roc_curve(y_train_pred_final.Survived, y_train_pred_final.Predicted_survived)


# In[ ]:


# Lets create columns with different cutoff points
numbers = [x/10 for x in range(10)]

for i in numbers:
    y_train_pred_final[i] = y_train_pred_final.survived_prob.map(lambda x : 1 if x > i else 0)
y_train_pred_final.head()


# In[ ]:


# Now calculate accuracy, sensitivity and specificity for variouse probability cuttoff
cutoff_df = pd.DataFrame(columns=['Probability', 'Accuracy', 'Sensitivity', 'Specificity'])
from sklearn.metrics import confusion_matrix

for i in numbers:
    conf_mat = metrics.confusion_matrix(y_train_pred_final.Survived, y_train_pred_final[i])
    total = sum(sum(conf_mat))
    accuracy = (conf_mat[0,0]+conf_mat[1,1])/total
    
    sensitivity = conf_mat[1,1]/(conf_mat[1,0]+conf_mat[1,1])
    specificity = conf_mat[0,0]/(conf_mat[0,0]+conf_mat[0,1])
    cutoff_df.loc[i] = [i, accuracy, sensitivity, specificity]
cutoff_df


# In[ ]:


# lets plot the accuracy, sensitivity and specificity over the probability
cutoff_df.plot.line(x = "Probability", y=['Accuracy', 'Sensitivity', 'Specificity'])
plt.vlines(x=0.423, ymax=1, ymin=0, colors='r', linestyles='--')
plt.show()


# In[ ]:


y_train_pred_final["Predicted_survived"] = y_train_pred_final.survived_prob.map(lambda x: 1 if x > 0.423 else 0)
y_train_pred_final.head()


# In[ ]:


metrics.accuracy_score(y_train_pred_final.Survived, y_train_pred_final.Predicted_survived)


# In[ ]:


confusion = metrics.confusion_matrix(y_train_pred_final.Survived, y_train_pred_final.Predicted_survived)
confusion


# In[ ]:


TN = confusion[0,0]
FP = confusion[0,1]
FN = confusion[1,0]
TP = confusion[1,1]


# In[ ]:


# calculate the sensitivity
TP/(TP+FN)


# In[ ]:


# calculate the specificity
TN/(FP+TN)


# In[ ]:


# calcuate false posititve rate
FP/(TN+FP)


# In[ ]:


#positive predicted value
TP / (TP+FP)


# In[ ]:


# negative predicted value
TN/(TN+FN)


# In[ ]:


precision_score(y_train_pred_final.Survived, y_train_pred_final.Predicted_survived)


# In[ ]:


recall_score(y_train_pred_final.Survived, y_train_pred_final.Predicted_survived)


# In[ ]:


#False negative rate
FN/(TP+FN)


# ### Making prediction on Test set

# In[ ]:


titanic_test = pd.read_csv(r"/kaggle/input/titanic/test.csv")
titanic_test.head()


# In[ ]:


servived_test = pd.read_csv(r"/kaggle/input/titanic/gender_submission.csv")
servived_test.head()


# In[ ]:


titanic_test = pd.merge(titanic_test, servived_test, how='inner', on='PassengerId')
titanic_test.head()


# In[ ]:


titanic_test.info()


# In[ ]:


titanic_test.Cabin = titanic_test.Cabin.fillna("Unknown_Cabin")
titanic_test.Cabin = titanic_test.Cabin.str[0]
titanic_test.Cabin.value_counts()


# In[ ]:


round(titanic_test.isnull().sum()/titanic_test.shape[0]*100, 2)


# In[ ]:


titanic_test['Title'] = titanic_test.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
titanic_test = titanic_test.drop('Name',axis=1)


# In[ ]:


titanic_test.head()


# In[ ]:


#let's replace a few titles -> "other" and fix a few titles
titanic_test['Title'] = np.where((titanic_test.Title=='Capt') | (titanic_test.Title=='Countess') |                                   (titanic_test.Title=='Don') | (titanic_test.Title=='Dona')| (titanic_test.Title=='Jonkheer')                                   | (titanic_test.Title=='Lady') | (titanic_test.Title=='Sir') | (titanic_test.Title=='Major') |                                   (titanic_test.Title=='Rev') | (titanic_test.Title=='Col'),'Other',titanic_test.Title)

titanic_test['Title'] = titanic_test['Title'].replace('Ms','Miss')
titanic_test['Title'] = titanic_test['Title'].replace('Mlle','Miss')
titanic_test['Title'] = titanic_test['Title'].replace('Mme','Mrs')


# In[ ]:


titanic_test.groupby('Title').Age.mean()


# In[ ]:


titanic_test["Age"] = np.where((titanic_test.Age.isnull()) & (titanic_test.Title == 'Master'), 7,                               np.where((titanic_test.Age.isnull()) & (titanic_test.Title=='Miss'),22,                                        np.where((titanic_test.Age.isnull()) & (titanic_test.Title=='Mr'),32,                                                 np.where((titanic_test.Age.isnull()) & (titanic_test.Title=='Mrs'),39,                                                          np.where((titanic_test.Age.isnull()) & (titanic_test.Title=='Other'),42,                                                                   np.where((titanic_test.Age.isnull()) & (titanic_test.Title=='Dr'),53,titanic_test.Age))))))


# In[ ]:


round(titanic_test.isnull().sum()/titanic_test.shape[0]*100, 2)


# In[ ]:


titanic_test.Fare = titanic_test.Fare.fillna(0)


# In[ ]:


round(titanic_test.isnull().sum()/titanic_test.shape[0]*100, 2)


# In[ ]:


PassengerId = titanic_test.PassengerId


# In[ ]:


dummy_1 = pd.get_dummies(titanic_test["Embarked"], prefix= "Embarked", drop_first=True)
dummy_2 = pd.get_dummies(titanic_test["Sex"], drop_first=False)
Pclass = pd.get_dummies(titanic_test["Pclass"], prefix= "Pclass")
siblings = pd.get_dummies(titanic_test["SibSp"], prefix= "SibSp")
Parch = pd.get_dummies(titanic_test["Parch"], prefix= "Parch")
cabin = pd.get_dummies(titanic_test["Cabin"], prefix= "Cabin")
Title = pd.get_dummies(titanic_test["Title"], prefix= "Title")


# In[ ]:


titanic_test = pd.concat([titanic_test, dummy_1, dummy_2, Pclass, siblings, Parch], axis=1)
titanic_test = titanic_test.drop(["Embarked","PassengerId", "Sex", "Pclass", "SibSp", "Parch", "Cabin", "Title"], axis=1)
titanic_test.head()


# In[ ]:


titanic_test = titanic_test.drop(["Ticket"], axis=1)


# In[ ]:


test_scale_var = ["Age", "Fare"]
titanic_test[test_scale_var] = scalar.transform(titanic_test[test_scale_var])


# In[ ]:


X_test = titanic_test[col_support]
X_test.head()


# In[ ]:


X_test_sm = sm.add_constant(X_test)


# In[ ]:


y_test_pred = logmodel6.predict(X_test_sm)


# In[ ]:


y_test_pred[:10]


# In[ ]:


y_test_pred_final = pd.DataFrame({"PassengerId":PassengerId ,"Survived":titanic_test.Survived, "Probability_survived": y_test_pred})
y_test_pred_final.head()


# In[ ]:


y_test_pred_final["Pred_Survived"] = y_test_pred_final.Probability_survived.map(lambda x: 1 if x > 0.423 else 0)
y_test_pred_final.head()


# In[ ]:


metrics.accuracy_score(y_test_pred_final.Survived, y_test_pred_final.Pred_Survived)


# In[ ]:


confusion = metrics.confusion_matrix(y_test_pred_final.Survived, y_test_pred_final.Pred_Survived)
confusion


# In[ ]:


TN = confusion[0,0]
FP = confusion[0,1]
FN = confusion[1,0]
TP = confusion[1,1]


# In[ ]:


# calculate the sensitivity
TP/(TP+FN)


# In[ ]:


# calculate the specificity
TN/(FP+TN)


# In[ ]:


# calcuate false posititve rate
FP/(TN+FP)


# In[ ]:


#positive predicted value
TP / (TP+FP)


# In[ ]:


# negative predicted value
TN/(TN+FN)


# In[ ]:


precision_score(y_test_pred_final.Survived, y_test_pred_final.Pred_Survived)


# In[ ]:


recall_score(y_test_pred_final.Survived, y_test_pred_final.Pred_Survived)


# In[ ]:


y_test_pred_final.shape

