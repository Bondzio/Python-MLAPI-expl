#!/usr/bin/env python
# coding: utf-8

# ###  Objective
# The main objective here is to score clients so we know who to email . We will evaluate our models using ROC curve and AUC.

# In[ ]:


from fastai.imports import *
os. listdir('../input/')


# In[ ]:


df = pd.read_csv('../input/caravan-insurance-challenge.csv')
original = df.copy()
df.head()


# adding the real labels :
# (sorry for the messy cell will be the only one i promise :p )

# In[ ]:


labels = ['ORIGIN', 'CustomerSubtype', 'NumberOfHouses1', 'AvgSizeHousehold1', 'AvgAge', 'CustomerMainType', 'RomanCatholic', 'Protestant...', 'OtherReligion', 'NoReligion', 'Married', 'LivingTogether', 'OtherRelation', 'Singles', 'HouseholdWithoutChildren', 'HouseholdWithChildren', 'HighLevelEducation', 'MediumLevelEducation', 'LowerLevelEducation', 'HighStatus', 'Entrepreneur', 'Farmer', 'MiddleManagement', 'SkilledLabourers', 'UnskilledLabourers', 'SocialClassA', 'SocialClassB1', 'SocialClassB2', 'SocialClassC', 'SocialClassD', 'RentedHouse', 'HomeOwners', '1Car', '2Cars', 'NoCar', 'NationalHealthService', 'PrivateHealthInsurance', 'Income<30.000', 'Income30-45.000', 'Income45-75.000', 'Income75-122.000', 'Income>123.000', 'AverageIncome', 'PurchasingPowerClass', 'ContributionPrivateThirdPartyInsurance', 'ContributionThirdPartyInsurance(firms)...', 'ContributionThirdPartyInsurane(agriculture)', 'ContributionCarPolicies', 'ContributionDeliveryVanPolicies', 'ContributionMotorcycle/scooterPolicies', 'ContributionLorryPolicies', 'ContributionTrailerPolicies', 'ContributionTractorPolicies', 'ContributionAgriculturalMachinesPolicies', 'ContributionMopedPolicies', 'ContributionLifeInsurances', 'ContributionPrivateAccidentInsurancePolicies', 'ContributionFamilyAccidentsInsurancePolicies', 'ContributionDisabilityInsurancePolicies', 'ContributionFirePolicies', 'ContributionSurfboardPolicies', 'ContributionBoatPolicies', 'ContributionBicyclePolicies', 'ContributionPropertyInsurancePolicies', 'ContributionSocialSecurityInsurancePolicies', 'NumberOfPrivateThirdPartyInsurance1-12', 'NumberOfThirdPartyInsurance(firms)...', 'NumberOfThirdPartyInsurane(agriculture)', 'NumberOfCarPolicies', 'NumberOfDeliveryVanPolicies', 'NumberOfMotorcycle/scooterPolicies', 'NumberOfLorryPolicies', 'NumberOfTrailerPolicies', 'NumberOfTractorPolicies', 'NumberOfAgriculturalMachinesPolicies', 'NumberOfMopedPolicies', 'NumberOfLifeInsurances', 'NumberOfPrivateAccidentInsurancePolicies', 'NumberOfFamilyAccidentsInsurancePolicies', 'NumberOfDisabilityInsurancePolicies', 'NumberOfFirePolicies', 'NumberOfSurfboardPolicies', 'NumberOfBoatPolicies', 'NumberOfBicyclePolicies', 'NumberOfPropertyInsurancePolicies', 'NumberOfSocialSecurityInsurancePolicies', 'CARAVAN']


# ## Data preparation

# In[ ]:


df.columns = labels
df.shape


# In[ ]:


df.CARAVAN.value_counts().plot.pie(autopct='%1.1f%%', shadow=True, startangle=140,explode=(0.5, 0))


# ### Conclusion:
# 
#    - It's a dataset with 9822 observations.
#    - The dataset is without null values and outliers
#    - The dataset is imbalanced as Yes answer represent only 6%
# 

# In[ ]:


yes = df[df.CARAVAN == 1].copy()


# ### Customer Sub Type

# In[ ]:


plt.figure(figsize=(15,8))
yes['CustomerSubtype'].value_counts().plot(kind='bar', align='center',color='deepskyblue', grid=True);


# ### Number of houses

# ### Age

# In[ ]:


plt.figure(figsize=(15,8))
yes['AvgAge'].value_counts().plot(kind='bar', align='center',color='deepskyblue', grid=True);


# ### Customer main type 

# In[ ]:


plt.figure(figsize=(15,8))
yes['CustomerMainType'].value_counts().plot(kind='bar', align='center',color='deepskyblue', grid=True);


# # Model Training 

# In[ ]:


from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


# In[ ]:


train = df[df.ORIGIN == 'train'].copy()
test = df[df.ORIGIN == 'test'].copy()


# In[ ]:


Train_Y = train.CARAVAN
Train_X = train.drop(['CARAVAN','ORIGIN'], axis=1)


# In[ ]:


Test_Y = test.CARAVAN
Test_X = test.drop(['CARAVAN','ORIGIN'], axis=1)


# ## KNN

# In[ ]:


from sklearn import neighbors
print("Nearest Neighbors Dataframe Test score :")
clf = neighbors.KNeighborsClassifier(3,'distance')
clf.fit(X=Train_X,y=Train_Y)
clf.score(Test_X,Test_Y)


# In[ ]:


KNN_y_pred_class = clf.predict(Test_X)
class_names = np.unique(np.array(Test_Y))
confusion_matrix(Test_Y, KNN_y_pred_class)


# In[ ]:


from sklearn.metrics import classification_report
print(classification_report(Test_Y, KNN_y_pred_class))


# In[ ]:


from sklearn.metrics import roc_curve, auc
knn_pred_prob = clf.predict_proba(Test_X)[:, 1]
fpr, tpr, thresholds = roc_curve(Test_Y, knn_pred_prob)
roc_auc = auc(fpr, tpr)
lw = 2
plt.plot(fpr, tpr,label='ROC curve KNN (AUC = %0.2f)' % roc_auc)
plt.xlim([0.0, 1])
plt.ylim([0.0, 1])
plt.title('ROC curve for KNN CLASS 1')
plt.xlabel('(1 - Specificity)')
plt.ylabel('(Sensitivity)')
plt.grid(True)
plt.legend(loc="lower right")
plt.show()


# ### SVM
# 

# In[ ]:


from sklearn.svm import SVC
clf_S = SVC(kernel='rbf',probability=True,random_state=0, gamma=.01, C=100000)
clf_S.fit(Train_X, Train_Y) 
print("SVM Dataframe Test score :")
print(clf_S.score(Test_X,Test_Y))


# In[ ]:


SVM_y_pred_class = clf_S.predict(Test_X)
class_names = np.unique(np.array(Test_Y))
confusion_matrix(Test_Y, SVM_y_pred_class)


# In[ ]:


from sklearn.metrics import classification_report
report = classification_report(Test_Y,SVM_y_pred_class)
print(report)


# In[ ]:


from sklearn.metrics import roc_curve, auc
svm_pred_prob = clf_S.predict_proba(Test_X)[:, 1]
fpr, tpr, thresholds = roc_curve(Test_Y, svm_pred_prob)
roc_auc = auc(fpr, tpr)
lw = 2
plt.plot(fpr, tpr,label='ROC curve SVM (AUC = %0.2f)' % roc_auc)
plt.xlim([0.0, 1])
plt.ylim([0.0, 1])
plt.title('ROC curve for SVM CLASS 1')
plt.xlabel('(1 - Specificity)')
plt.ylabel('(Sensitivity)')
plt.grid(True)
plt.legend(loc="lower right")
plt.show()


# ### Decision Tree
# 

# In[ ]:


from sklearn import tree
clf_tree = tree.DecisionTreeClassifier()
clf_tree.fit(Train_X, Train_Y) 
print(clf_tree.score(Test_X,Test_Y))


# In[ ]:


tree_y_pred_class = clf_tree.predict(Test_X)
class_names = np.unique(np.array(Test_Y))
confusion_matrix(Test_Y, tree_y_pred_class)


# In[ ]:


print(classification_report(Test_Y, KNN_y_pred_class))


# In[ ]:


from sklearn.metrics import roc_curve, auc
tree_pred_prob = clf_tree.predict_proba(Test_X)[:, 1]
fpr, tpr, thresholds = roc_curve(Test_Y, tree_pred_prob)
roc_auc = auc(fpr, tpr)
lw = 2
plt.plot(fpr, tpr,label='ROC curve Decision Tree (AUC = %0.2f)' % roc_auc)
plt.xlim([0.0, 1])
plt.ylim([0.0, 1])
plt.title('ROC curve for Decision Tree CLASS 1')
plt.xlabel('(1 - Specificity)')
plt.ylabel('(Sensitivity)')
plt.grid(True)
plt.legend(loc="lower right")
plt.show()


# ## Random Forest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(Train_X, Train_Y) 
print(rf.score(Test_X,Test_Y))


# In[ ]:


rf_y_pred_class = rf.predict(Test_X)
class_names = np.unique(np.array(Test_Y))
confusion_matrix(Test_Y, rf_y_pred_class)


# In[ ]:


print(classification_report(Test_Y, rf_y_pred_class))


# In[ ]:


from sklearn.metrics import roc_curve, auc
rf_pred_prob = rf.predict_proba(Test_X)[:, 1]
fpr, tpr, thresholds = roc_curve(Test_Y, rf_pred_prob)
roc_auc = auc(fpr, tpr)
lw = 2
plt.plot(fpr, tpr,label='ROC curve  Random Forest (AUC = %0.2f)' % roc_auc)
plt.xlim([0.0, 1])
plt.ylim([0.0, 1])
plt.title('ROC curve for  random forest CLASS 1')
plt.xlabel('(1 - Specificity)')
plt.ylabel('(Sensitivity)')
plt.grid(True)
plt.legend(loc="lower right")
plt.show()


# A small tuning of the random forest gets us an even better AUC

# In[ ]:


rf = RandomForestClassifier(n_estimators=100,max_leaf_nodes=3)
rf.fit(Train_X, Train_Y) 
print(rf.score(Test_X,Test_Y))


# In[ ]:


rf_y_pred_class = rf.predict(Test_X)
class_names = np.unique(np.array(Test_Y))
confusion_matrix(Test_Y, rf_y_pred_class)


# In[ ]:


print(classification_report(Test_Y, rf_y_pred_class))


# In[ ]:


from sklearn.metrics import roc_curve, auc
rf_pred_prob = rf.predict_proba(Test_X)[:, 1]
fpr, tpr, thresholds = roc_curve(Test_Y, rf_pred_prob)
roc_auc = auc(fpr, tpr)
lw = 2
plt.plot(fpr, tpr,label='ROC curve  Random Forest (AUC = %0.2f)' % roc_auc)
plt.xlim([0.0, 1])
plt.ylim([0.0, 1])
plt.title('ROC curve for  random forest CLASS 1')
plt.xlabel('(1 - Specificity)')
plt.ylabel('(Sensitivity)')
plt.grid(True)
plt.legend(loc="lower right")
plt.show()


# This model seems good enough let's plot feature importance using a function from the fast ai library

# In[ ]:


def rf_feat_importance(m, df):
    return pd.DataFrame({'cols':df.columns, 'imp':m.feature_importances_}
                       ).sort_values('imp', ascending=False)
def plot_fi(fi): return fi.plot('cols', 'imp', 'barh', figsize=(12,7), legend=False)
fi = rf_feat_importance(rf, Train_X); fi[:10]


# In[ ]:


plot_fi(fi[:30]);


# ## Balanced Models
# ### Balanced Random Forest

# In[ ]:


from imblearn.ensemble import BalancedRandomForestClassifier


# In[ ]:


brf=BalancedRandomForestClassifier()


# In[ ]:


brf.fit(X=Train_X,y=Train_Y)


# In[ ]:


print("Test score :")
print(brf.score(Test_X,Test_Y))


# In[ ]:


from sklearn.metrics import roc_curve, auc
brf_pred_prob = brf.predict_proba(Test_X)[:, 1]
fpr, tpr, thresholds = roc_curve(Test_Y, brf_pred_prob)
roc_auc = auc(fpr, tpr)
lw = 2
plt.plot(fpr, tpr,label='ROC curve Balanced Random Forest (AUC = %0.2f)' % roc_auc)
plt.xlim([0.0, 1])
plt.ylim([0.0, 1])
plt.title('ROC curve for Balanced random forest CLASS 1')
plt.xlabel('(1 - Specificity)')
plt.ylabel('(Sensitivity)')
plt.grid(True)
plt.legend(loc="lower right")
plt.show()


# This balanced random forest model seems to be outperforming the others , trying to tune it doesn't seem to improve our AUC.

#  ### LDA model

# In[ ]:


from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
lda = LDA()
lda.fit(X=Train_X,y=Train_Y)


# In[ ]:


print("Test score :")
print(lda.score(Test_X,Test_Y))


# In[ ]:


lda_pred_prob = lda.predict_proba(Test_X)[:, 1]
fpr, tpr, thresholds = roc_curve(Test_Y, lda_pred_prob)
roc_auc = auc(fpr, tpr)
lw = 2
plt.plot(fpr, tpr,label='ROC curve LDA (AUC = %0.2f)' % roc_auc)
plt.xlim([0.0, 1])
plt.ylim([0.0, 1])
plt.title('ROC curve for Balanced random forest CLASS 1')
plt.xlabel('(1 - Specificity)')
plt.ylabel('(Sensitivity)')
plt.grid(True)
plt.legend(loc="lower right")
plt.show()


#  ### XGBOOST

# In[ ]:


from xgboost import XGBClassifier
train = original[original.ORIGIN == 'train'].copy()
test = original[original.ORIGIN == 'test'].copy()

m = XGBClassifier()
# Add silent=True to avoid printing out updates with each cycle
Train_Y = train.CARAVAN
Train_X = train.drop(['CARAVAN','ORIGIN'], axis=1)
Test_Y = test.CARAVAN
Test_X = test.drop(['CARAVAN','ORIGIN'], axis=1)
m.fit(Train_X,Train_Y, verbose=False)


# In[ ]:


print("Test score :")
print(m.score(Test_X,Test_Y))


# In[ ]:


xgb_pred_prob = m.predict_proba(Test_X)[:, 1]
fpr, tpr, thresholds = roc_curve(Test_Y, xgb_pred_prob)
roc_auc = auc(fpr, tpr)
lw = 2
plt.plot(fpr, tpr,label='ROC curve LDA (AUC = %0.2f)' % roc_auc)
plt.xlim([0.0, 1])
plt.ylim([0.0, 1])
plt.title('ROC curve for Balanced random forest CLASS 1')
plt.xlabel('(1 - Specificity)')
plt.ylabel('(Sensitivity)')
plt.grid(True)
plt.legend(loc="lower right")
plt.show()


# ## Comparing the models 

# In[ ]:


fpr6, tpr6, thresholds6 = roc_curve(Test_Y, lda_pred_prob)
roc_auc6 = auc(fpr6, tpr6)

fpr5, tpr5, thresholds5 = roc_curve(Test_Y, knn_pred_prob)
roc_auc5 = auc(fpr5, tpr5)

fpr4, tpr4, thresholds4 = roc_curve(Test_Y, rf_pred_prob)
roc_auc4 = auc(fpr4, tpr4)

fpr3, tpr3, thresholds3 = roc_curve(Test_Y, xgb_pred_prob)
roc_auc3 = auc(fpr3, tpr3)

fpr2, tpr2, thresholds2 = roc_curve(Test_Y, brf_pred_prob)
roc_auc2 = auc(fpr2, tpr2)

fpr1, tpr1, thresholds1 = roc_curve(Test_Y,svm_pred_prob)
roc_auc1 = auc(fpr1, tpr1)
lw = 2
plt.plot(fpr6, tpr6,color='orange',label='ROC curve LDA (AUC = %0.2f)' % roc_auc6)
plt.plot(fpr5, tpr5,color='green',label='ROC curve KNN (AUC = %0.2f)' % roc_auc5)
plt.plot(fpr4, tpr4,color='gold',label='ROC curve RF (AUC = %0.2f)' % roc_auc4)
plt.plot(fpr3, tpr3,color='gold',label='ROC curve XGBOOST (AUC = %0.2f)' % roc_auc3)
plt.plot(fpr2, tpr2,color='black',label='ROC curve BRF (AUC = %0.2f)' % roc_auc2)
plt.plot(fpr1, tpr1,color='navy',label='ROC curve SVM (AUC = %0.2f)' % roc_auc1)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.title('ROC curve ')
plt.xlabel('(1 - Specificity)')
plt.ylabel('(Sensitivity)')
plt.grid(True)
plt.legend(loc="lower right")
plt.show()


# The curves for each model are thus indicative of relative predictive power of each model. For instance, BRF model has higher probability of accurate prediction of correct class member, and gaining high level of accuracy prediction probability as compared to RP and SVM models.  xgboost is close .
# 

# # Scoring:
# Balanced Random Forest seems to offer the best results with an AUC of 0.73 , we will use this model for our scoring

# In[ ]:


test_target = Test_Y.copy()
test_target.reset_index(drop=True, inplace=True)
test_target=test_target.replace({
    1:'Yes',
    0:'No'
})
predicted_target=brf.predict(Test_X)
predicted_target=pd.Series(predicted_target).replace({
    1:'Yes',
    0:'No'
})


# In[ ]:


ranks=pd.DataFrame(data={
    'realClass':test_target,
    'predictedClass':predicted_target,
    'rank':brf_pred_prob
})
ranks.sort_values(by=['rank'],ascending=False,inplace=True)
ranks.head()


# In[ ]:


top = ranks.where(ranks['rank']>0.5,).dropna()
top.head()


# In[ ]:


top.shape


# # Conclusion
# 

# Our modeling process has provided some useful insights about the target market. In particular, it can be safely concluded that the target market is probably not a single group. There are at least two main customer profiles who are likely to own caravans and therefore are potential buyers of Caravan Insurance. For marketing purposes, each group would probably need to be approached in different ways, both in terms of the communication message as well as the medium of communication.
# We identified 1307 customer who have higher probability of answering our mails ( Please note that in the original competition we didn't have the real class of the test set and so we built a mailing strategy accordingly )

# <br>
