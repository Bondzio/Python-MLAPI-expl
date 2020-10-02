#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
import matplotlib.pyplot as plt # this is used for the plot the graph 
import seaborn as sns # plot library of python
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.linear_model import LogisticRegression # to apply the Logistic regression
from sklearn.model_selection import train_test_split # to split the data into two partsas
from sklearn.model_selection import GridSearchCV# for tuning parameter
from sklearn.ensemble import RandomForestClassifier # for random forest classifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics # to check the error and accuracy of the model
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, learning_curve
import plotly.figure_factory as ff
import plotly.offline as py


# In[ ]:


data_df= pd.read_csv("../input/data.csv")


# In[ ]:


data_df.head()


# In[ ]:


data_df.shape


# In[ ]:


data_df.isna().sum()


#      It's good idea to drop Unnamed: 32 Column

# In[ ]:


data_df.drop(['Unnamed: 32'],axis = 1,inplace = True)


# In[ ]:


data_df.describe()


# In[ ]:


data_df[['diagnosis','radius_worst','radius_mean','radius_se']].groupby('diagnosis').mean()


# We can observe that on an average of radius in all scenarios is less in Benign Tumor as compared to Malignant one.

# In[ ]:


M = data_df[(data_df['diagnosis'] == 'M')]
B = data_df[(data_df['diagnosis'] == 'B')]


# In[ ]:


def myplot(data_new,bin_size):
    tmp1 = M[data_new]
    tmp2 = B[data_new]
    hist_data = [tmp1, tmp2]
    group_labels = ["Malignant","Benign"]
    colors = ['#F24027', '#2CD166']
    fig  = ff.create_distplot(hist_data,group_labels,colors = colors, show_hist = True, bin_size = bin_size,curve_type = 'kde')
    fig['layout'].update(title = data_new)
    py.iplot(fig, filename = 'Density Plot')


# In[ ]:


myplot('radius_mean',.5)
myplot('texture_mean',.5)
myplot('compactness_mean' , 0.005)


# Segregating the features

# In[ ]:


features_mean = data_df.columns[2:11]
features_mean


# In[ ]:


features_se = data_df.columns[12:22]
features_se


# In[ ]:


features_worst = data_df.columns[23:]
features_worst


# In[ ]:


data_df['diagnosis'] = data_df['diagnosis'].map({'M':1,'B':0})


# In[ ]:


sns.catplot(x="diagnosis", kind="count", palette="ch:.30", data=data_df)


# In[ ]:


corr_mean = data_df[features_mean].corr()


# In[ ]:


plt.figure(figsize= (10,10))
sns.heatmap(corr_mean,annot = True)


# > ****Highly Correalted Pairs:
# >     (radius_mean <-> area_mean)
# >     (perimeter_mean <-> area_mean)
# >     (concavity_mean <-> concave points_mean)

# In[ ]:


corr_mean.abs()


# In[ ]:


select_pred_mean = ['radius_mean','texture_mean','smoothness_mean','compactness_mean','symmetry_mean']


# > Modelling

# In[ ]:


train , test = train_test_split(data_df,test_size = 0.2)
print(train.shape)
print(test.shape)


# In[ ]:


train_X = train[select_pred_mean]# taking the training data input 
train_y=train.diagnosis
test_X= test[select_pred_mean] # taking test data inputs
test_y =test.diagnosis   #output value of test data
model_rf=RandomForestClassifier(n_estimators=100)
model_rf.fit(train_X,train_y)


# In[ ]:


predict_value = model_rf.predict(test_X)


# In[ ]:


predict_value


# In[ ]:


metrics.accuracy_score(predict_value,test_y)


# In[ ]:


model_logreg = LogisticRegression()
model_logreg.fit(train_X,train_y)


# In[ ]:


predict_logreg = model_logreg.predict(test_X)
metrics.accuracy_score(predict_logreg,test_y)


# In[ ]:


metrics.f1_score(predict_logreg,test_y)


# In[ ]:


metrics.confusion_matrix(predict_logreg,test_y)


# In[ ]:


metrics.confusion_matrix(predict_value,test_y)


# In[ ]:


metrics.f1_score(predict_value,test_y)


# ROC Curves
# tells how much model is capable of distinguishing between classes.  

# In[ ]:


def roc_curve(model_num,name_model):
    probs = model_num.predict_proba(test_X)
    preds = probs[:,1] # tpr
    fpr, tpr, threshold = metrics.roc_curve(test_y, preds)
    roc_auc = metrics.auc(fpr, tpr)
    plt.title('Receiver Operating Characteristic for ' + name_model)
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


# In[ ]:


roc_curve(model_logreg,"LogisticRegression")
roc_curve(model_rf,"Random Forest")


# In[ ]:


#Checking with taking all features
select_pred_mean_full = features_mean
train_X= train[select_pred_mean_full]
train_y= train.diagnosis
test_X = test[select_pred_mean_full]
test_y = test.diagnosis


# In[ ]:


#Default Random Forest Classifier Algorithm without any tuning
model=RandomForestClassifier(n_estimators=100)
model.fit(train_X,train_y)
prediction = model.predict(test_X)
metrics.accuracy_score(prediction,test_y)


# Accuracy Increases a Bit by including all mean features but not by a significant margin. So we keep the model complexity low.

# In[ ]:


#Calculating Feature Importance
featimp = pd.Series(model.feature_importances_, index=select_pred_mean_full).sort_values(ascending=False)
print(featimp)


# In[ ]:


#Using Xgboost
from xgboost import XGBRegressor
model_xgb = XGBRegressor()
# We can Add silent=True to avoid printing out updates with each cycle
model_xgb.fit(train_X, train_y, verbose=False)


# In[ ]:


y_pred = model_xgb.predict(test_X)


# Calculating Accuracy 

# In[ ]:


predictions = [round(value) for value in y_pred]
# evaluate predictions
accuracy = metrics.accuracy_score(predictions,test_y)
print("Accuracy: %.2f%%" % (accuracy * 100.0))


# https://stackoverflow.com/questions/36063014/what-does-kfold-in-python-exactly-do

# In[ ]:


kfold = StratifiedKFold(n_splits=10)


# In[ ]:


random_state = 2
classifiers = []
classifiers.append(SVC(random_state=random_state))
classifiers.append(DecisionTreeClassifier(random_state=random_state))
classifiers.append(AdaBoostClassifier(DecisionTreeClassifier(random_state=random_state),random_state=random_state,learning_rate=0.1))
classifiers.append(RandomForestClassifier(random_state=random_state))
classifiers.append(ExtraTreesClassifier(random_state=random_state))
classifiers.append(GradientBoostingClassifier(random_state=random_state))
classifiers.append(MLPClassifier(random_state=random_state))
classifiers.append(KNeighborsClassifier())
classifiers.append(LogisticRegression(random_state = random_state))
classifiers.append(LinearDiscriminantAnalysis())

cv_results = []
for classifier in classifiers :
    cv_results.append(cross_val_score(classifier, train_X, y = train_y, scoring = "accuracy", cv = kfold, n_jobs=4))

cv_means = []
cv_std = []
for cv_result in cv_results:
    cv_means.append(cv_result.mean())
    cv_std.append(cv_result.std())

cv_res = pd.DataFrame({"CrossValMeans":cv_means,"CrossValerrors": cv_std,"Algorithm":["SVC","DecisionTree","AdaBoost",
"RandomForest","ExtraTrees","GradientBoosting","MultipleLayerPerceptron","KNeighboors","LogisticRegression","LinearDiscriminantAnalysis"]})

g = sns.barplot("CrossValMeans","Algorithm",data = cv_res, palette="Set2",orient = "h",**{'xerr':cv_std})
g.set_xlabel("Mean Accuracy")
g = g.set_title("Cross validation scores")


# Decision Tree
# Random Forest
# ET
# GB

# In[ ]:


### META MODELING  WITH ADABOOST, RF, EXTRATREES and GRADIENTBOOSTING

# Adaboost
DTC = DecisionTreeClassifier()

adaDTC = AdaBoostClassifier(DTC, random_state=7)

ada_param_grid = {"base_estimator__criterion" : ["gini", "entropy"],
              "base_estimator__splitter" :   ["best", "random"],
              "algorithm" : ["SAMME","SAMME.R"],
              "n_estimators" :[1,2],
              "learning_rate":  [0.0001, 0.001, 0.01, 0.1, 0.2, 0.3,1.5]}

gsadaDTC = GridSearchCV(adaDTC,param_grid = ada_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)

gsadaDTC.fit(train_X,train_y)
pp = gsadaDTC.predict(test_X)

gsadaDTC_Acc = metrics.accuracy_score(pp,test_y)

print(gsadaDTC_Acc)

ada_best = gsadaDTC.best_estimator_


# In[ ]:


gsadaDTC.best_score_


# https://datascience.stackexchange.com/questions/21877/how-to-use-the-output-of-gridsearch

# In[ ]:


#ExtraTrees 
ExtC = ExtraTreesClassifier()
## Search grid for optimal parameters
ex_param_grid = {"max_depth": [None],
              "max_features": [1, 3, 9],
              "min_samples_split": [2, 3, 9],
              "min_samples_leaf": [1, 3, 9],
              "bootstrap": [False],
              "n_estimators" :[100,300],
              "criterion": ["gini"]}


gsExtC = GridSearchCV(ExtC,param_grid = ex_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)

gsExtC.fit(train_X,train_y)

ExtC_best = gsExtC.best_estimator_

# Best score
gsExtC.best_score_


# In[ ]:


# RFC Parameters tunning 
RFC = RandomForestClassifier()
## Search grid for optimal parameters
rf_param_grid = {"max_depth": [None],
              "max_features": [1, 3, 9],
              "min_samples_split": [2, 3, 9],
              "min_samples_leaf": [1, 3, 9],
              "bootstrap": [False],
              "n_estimators" :[100,300],
              "criterion": ["gini"]}


gsRFC = GridSearchCV(RFC,param_grid = rf_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)

gsRFC.fit(train_X,train_y)

RFC_best = gsRFC.best_estimator_

# Best score
gsRFC.best_score_


# In[ ]:


# Gradient boosting tunning
GBC = GradientBoostingClassifier()
gb_param_grid = {'loss' : ["deviance"],
              'n_estimators' : [100,200,300],
              'learning_rate': [0.1, 0.05, 0.01],
              'max_depth': [4, 8],
              'min_samples_leaf': [100,150],
              'max_features': [0.3, 0.1] 
              }

gsGBC = GridSearchCV(GBC,param_grid = gb_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)

gsGBC.fit(train_X,train_y)

GBC_best = gsGBC.best_estimator_
# Best score
gsGBC.best_score_


# https://medium.com/all-things-ai/in-depth-parameter-tuning-for-gradient-boosting-3363992e9bae

# In[ ]:


#Checking HyperParameter Values
RFC_best


# https://medium.com/@srnghn/the-mathematics-of-decision-trees-random-forest-and-feature-importance-in-scikit-learn-and-spark-f2861df67e3

# In[ ]:


rows = cols = 2
fig, axes = plt.subplots(rows , cols ,figsize=(14,14))

best_classifiers = [("AdaBoosting", ada_best),("GradientBoosting",GBC_best),("ExtraTrees",ExtC_best),("RandomForest",RFC_best)]

nclassifier = 0
for row in range(rows):
    for col in range(cols):
        name = best_classifiers[nclassifier][0]
        classifier = best_classifiers[nclassifier][1]
        indices = np.argsort(classifier.feature_importances_)[::-1][:9]
        g = sns.barplot(y=train_X.columns[indices][:9],x = classifier.feature_importances_[indices][:9] ,
                        orient='h',ax=axes[row][col],palette="rocket")
        g.set_xlabel("Relative importance",fontsize=10)
        g.set_ylabel("Features",fontsize=10)
        g.tick_params(labelsize=10)
        g.set_title(name + " feature importance")
        nclassifier += 1


# ** Ensembled Voting**

# In[ ]:


votingC = VotingClassifier(estimators=[('rfc', RFC_best), ('extc', ExtC_best),
('adac',ada_best),('gbc',GBC_best)], voting='soft', n_jobs=4)
votingC = votingC.fit(train_X,train_y)


# Hard voting is where a model is selected from an ensemble to make the final prediction by a simple majority vote for accuracy.
# 
# Soft Voting can only be done when all your classifiers can calculate probabilities for the outcomes. Soft voting arrives at the best result by averaging out the probabilities calculated by individual algorithms.

# https://towardsdatascience.com/ensemble-learning-in-machine-learning-getting-started-4ed85eb38e00****

# In[ ]:


pred_voting = votingC.predict(test_X)
metrics.accuracy_score(pred_voting,test_y)


# In[ ]:


metrics.f1_score(pred_voting,test_y)


# In[ ]:


pd.crosstab(pred_voting,test_y)


# In[ ]:


def roc_curve(model_num,name_model):
    probs = model_num.predict_proba(test_X)
    preds = probs[:,1] # True Positive Rate
    fpr, tpr, threshold = metrics.roc_curve(test_y, preds)
    roc_auc = metrics.auc(fpr, tpr)
    plt.title('Receiver Operating Characteristic for ' + name_model)
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


# In[ ]:


roc_curve(votingC,"Vf")


# In[ ]:


final_sub = pd.DataFrame({'Id': test.id, 'Ensembled_Diagnosis_Prediction': pred_voting})
final_sub.head()


# Thanks for your time ! This is my first Kernel. Please let me know any suggestion for improvement.
# Do Upvote if you liked the kernel it will motivate me. 
# 
# **Happy Learning ! **

# In[ ]:




