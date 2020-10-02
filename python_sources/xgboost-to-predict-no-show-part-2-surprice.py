#!/usr/bin/env python
# coding: utf-8

# **Hyperparameter tunning, model fitting and more surprices!**
# 
# In [part 1](https://www.kaggle.com/molihn/xgboost-to-predict-patients-no-show-part-1) we studied the variables, created new ones and performed a very thorough EDA, focusing on how the features are related with the variable of interest: no-show. 
# 
# From this analysis, transformations were applied to the data: 
# * Change PatientId type to integer
# * Set AppointmentID as index 
# * Change variable No-show to binary (1 for no-show, 0 for show)
# * Create new variable PreviousApp which indicates the number of previous appointments scheduled by the patient
# * Create new variable PreviousNoShow which indicates the proportion of patient's No-Show previous to the appointment studied
# * Create new variables WeekdayScheduled and WeekdayAppointment, which indicate the day of the week (1: Monday, ..., 7: Sunday) the appointment was scheduled/was respectively
# * Delete appointments scheduled or done on Saturdays (atypical values)
# * Delete patients with negative Age (less than zero)
# * Create new variable HasHandicap which indicates if the patient has some sort of handicap (the original variable indicates how many handicaps the patient has)
# * Create new variable PreviousDisease, which indicates if the patient has a previous condition diagnosed such as hypertension, diabetes or alcoholism
# * Create new variable DaysBeforeApp, which indicates how many days in advanced the appointment was scheduled and filter by those appointments with negative values (scheduling done after the appointment)
# * Create new variable DaysBeforeCat, which categorizes the previous variable in 5 groups: 0 days, 1-2 days, 3-7 days, 8-31 days and more than 31 days in advance
# 
# These transformations will be applied to obtain the data ready to model. 

# In[ ]:


import numpy as np 
import pandas as pd 
from scipy import stats as ss
import statsmodels.api as sm
from sklearn import metrics
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
import xgboost as xgb
from xgboost.sklearn import XGBClassifier

from bayes_opt import BayesianOptimization
from skopt  import BayesSearchCV 
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import shap 


# In[ ]:


df = pd.read_csv("../input/KaggleV2-May-2016.csv")

def get_day(x):
    return x.date()

def DaysBeforeCat(days):
    if days == 0:
        return '0 days'
    elif days in range(1,3):
        return '1-2 days'
    elif days in range(3,8):
        return '3-7 days'
    elif days in range(8, 32):
        return '8-31 days'
    else:
        return '> 31 days'

def getting_ready(df):
    
    df['PatientId'].astype('int64')
    df.set_index('AppointmentID', inplace = True)
    
    # Creating new variables
    df['NoShow'] = (df['No-show'] == 'Yes')*1
    df['PreviousApp'] = df.sort_values(by = ['PatientId','ScheduledDay']).groupby(['PatientId']).cumcount()
    df['PreviousNoShow'] = (df[df['PreviousApp'] > 0].sort_values(['PatientId', 'ScheduledDay']).groupby(['PatientId'])['NoShow'].cumsum() / df[df['PreviousApp'] > 0]['PreviousApp'])
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['WeekdayScheduled'] = df.apply(lambda x: x.ScheduledDay.isoweekday(), axis = 1)
    df['HasHandicap'] = (df['Handcap'] > 0)*1
    df['PreviousDisease'] = df.apply(lambda x: ((x.Hipertension == 1 )| x.Diabetes == 1 | x.Alcoholism == 1)*1, axis = 1)
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
    df['WeekdayAppointment'] = df.apply(lambda x: x.AppointmentDay.isoweekday(), axis = 1)
    df['DaysBeforeApp'] = ((df.AppointmentDay.apply(get_day) - df.ScheduledDay.apply(get_day)).astype('timedelta64[D]')).astype(int)
    df['DaysBeforeCat'] = df.DaysBeforeApp.apply(DaysBeforeCat)
    
    # Filtering
    
    df2 = df[(df['WeekdayScheduled'] < 6) &
             (df['WeekdayAppointment'] < 6) &
             (df['Age'] >= 0) &
             (df['DaysBeforeApp'] >= 0)]
    
    return df2
    
df_done = getting_ready(df)


# In[ ]:


df_done.columns


# The features we will use are: Gender, Age, Scholarship, Hipertension, Diabetes, Alcoholism, SMS_received, PreviousApp, PreviousNoShow, WeekdayScheduled, WeekdayAppointment, HasHandicap, PreviousDisease, DaysBeforeApp and DaysBeforeCat. 
# 
# As XGBoost only receives numerical features, we must transform the categorical variables into dummy variables. We could change each variable to a number but this makes no sense as, for example, Mondays (1 in WeekdayAppointment) is not twice as Tuesdays (2 in WeekdayAppointment). Values must make sense. Given this, the transformations we will apply are: 
# * Change Gender to "IsFemale" which takes the value 1 if Gender = F and 0 in other case
# * Change WeekdayScheduled to five variables: ScheduledMonday, ScheduledTuesday, ..., ScheduledFriday. Each variable is 1 if the appointment was scheduled in that particular day and 0 in other case. Same transformation will be apply to WeekdayAppointment (variables will be AppointmentMonday and so on)
# * Change DaysBeforeCat to five variables: 

# In[ ]:


# WeekdayScheduled to dummies
df_done = df_done.assign(ScheduledMonday = (df['WeekdayScheduled'] == 1)*1, 
                         ScheduledTuesday = (df['WeekdayScheduled'] == 2)*1, 
                         ScheduledWednesday = (df['WeekdayScheduled'] == 3)*1,
                         ScheduledThursday = (df['WeekdayScheduled'] == 4)*1,
                         ScheduledFriday = (df['WeekdayScheduled'] == 5)*1)

# WeekdayAppointment to dummies
df_done = df_done.assign(AppointmentMonday = (df['WeekdayAppointment'] == 1)*1, 
                         AppointmentTuesday = (df['WeekdayAppointment'] == 2)*1, 
                         AppointmentWednesday = (df['WeekdayAppointment'] == 3)*1,
                         AppointmentThursday = (df['WeekdayAppointment'] == 4)*1,
                         AppointmentFriday = (df['WeekdayAppointment'] == 5)*1)

# Gender to dummy 
df_done['IsFemale'] = (df_done['Gender'] == 'F')*1

# DaysBeforeCat to dummies
def ant_days(df):
    df.loc[:, 'Ant0Days'] = (df['DaysBeforeCat'] == '0 days')*1
    df.loc[:, 'Ant12Days'] = (df['DaysBeforeCat'] == '1-2 days')*1
    df.loc[:, 'Ant37Days'] = (df['DaysBeforeCat'] == '3-7 days')*1
    df.loc[:, 'Ant831Days'] = (df['DaysBeforeCat'] == '8-31 days')*1
    df.loc[:, 'Ant32Days'] = (df['DaysBeforeCat'] == '> 31 days')*1
    
ant_days(df_done)


# The features we will use are number type as well as our label (NoShow). For hyperparameter tunning (and model training) we will separate the data between train and test. As data is not so sparse in time, the separation will be done using random sampling, where 70% of the data will be used for training and 30% for testing. 

# In[ ]:


features = ['Age', 'Scholarship', 'Hipertension', 'Diabetes',
            'Alcoholism', 'SMS_received', 'PreviousApp', 'PreviousNoShow', 
            'HasHandicap', 'PreviousDisease', 'DaysBeforeApp',
            'ScheduledMonday', 'ScheduledTuesday', 'ScheduledWednesday', 
            'ScheduledThursday', 'ScheduledFriday', 'AppointmentMonday', 
            'AppointmentTuesday', 'AppointmentWednesday', 'AppointmentThursday', 
            'AppointmentFriday', 'IsFemale', 'Ant0Days', 'Ant12Days', 
            'Ant37Days', 'Ant831Days', 'Ant32Days']

label = 'NoShow'


# To reduce computing times, we will reduce memory usage using a function developed by @somang1418 (see [here](http://www.kaggle.com/somang1418/tuning-hyperparameters-under-10-minutes-lgbm)). Thanks to his work, we are able to perform Bayesian Optimization on hyperparameters in an optimal way (loved your work!)

# In[ ]:


# Special thanks to https://www.kaggle.com/somang1418/tuning-hyperparameters-under-10-minutes-lgbm
def reduce_mem_usage(df, verbose=True):
    numerics = ['int8','int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2    
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)    
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df


# In[ ]:


df_done = reduce_mem_usage(df_done)

X_train, X_test, y_train, y_test = train_test_split(df_done[features], df_done[label], test_size=0.3, random_state=6)
y_train = pd.DataFrame(y_train)
train = X_train.merge(y_train, left_index = True, right_index = True)
y_test = pd.DataFrame(y_test)
test = X_test.merge(y_test, left_index = True, right_index = True)


# Some time ago, I worked with a medical hospital to optimize scheduling in order to avoid no-shows. They were willing to try new methods, as long as doctors weren't bothered by overbooking practices. In plain english: as they have many doctors who share offices, predicting a patient not showing up and failing was worse than predicting a patient showing up but then failing. In this case, where success/positive outcome is no-show, this is known as false positive (predicted positive no-show but actually got negative no-show).
# 
# If we just wanted to be accurate, then as our data is unbalanced it will be easier to just predict everyone as not no-show and have 79% accuracy (more or less). But then we wouldn't be attacking the problem of no-show. So we must keep in mind that not only accuracy is important, but recall (the hability to capture positive results) is also important. 
# 
# As we have more negative results than positive, rather than optimizing for AUROC we will optimize for precision-recall curve (for more info, see [here](http://www.chioka.in/differences-between-roc-auc-and-pr-auc/)). We will define our optimization function, parameters to be evaluated and perform bayesian optimization.

# In[ ]:


def param_opt_xgb(X, y, init_round=10, opt_round=10, n_folds=3, random_seed=6, output_process=False):
    # Prepare data
    dtest = xgb.DMatrix(X, y)

    def xgb_eval(learning_rate, n_estimators, max_depth, min_child_weight, gamma, subsample, colsample_bytree, scale_pos_weight):
        params = {'objective' : 'binary:logistic', 'nthread' : 4, 'seed' : random_seed, "silent":1}
        params['learning_rate'] = max(min(learning_rate, 1), 0)
        params['n_estimators'] = int(round(n_estimators))
        params['max_depth'] = int(round(max_depth))
        params['min_child_weight'] = int(round(min_child_weight))
        params['gamma'] = gamma
        params['subsample'] = max(min(subsample, 1), 0)
        params['colsample_bytree'] = max(min(colsample_bytree, 1), 0)
        params['scale_pos_weight'] = int(round(scale_pos_weight))

        cv_result = xgb.cv(params, dtest, nfold=n_folds, seed=random_seed, stratified=True, verbose_eval =200, metrics=['auc'])
        
        
        return max(cv_result['train-auc-mean'])
    
    xgbBO = BayesianOptimization(xgb_eval, {'learning_rate': (0.01, 0.3),
                                                'n_estimators': (100, 200),
                                                'max_depth': (2, 7),
                                                'min_child_weight': (0, 7),
                                                'gamma': (0, 0.3),
                                                'subsample':(0.5,1),
                                                'colsample_bytree': (0.5, 1),
                                                'scale_pos_weight':(2,7)}, random_state=random_seed)

    xgbBO.maximize(init_points=init_round, n_iter=opt_round)

    model_aucpr=[]
    for model in range(len(xgbBO.res)):
        model_aucpr.append(xgbBO.res[model]['target'])

    # return best parameters
    return xgbBO.res[pd.Series(model_aucpr).idxmax()]['target'],xgbBO.res[pd.Series(model_aucpr).idxmax()]['params']


# In[ ]:


opt_params = param_opt_xgb(df_done[features], df_done[label])


# In[ ]:


opt_params[1]['n_estimators'] = int(round(opt_params[1]['n_estimators']))
opt_params[1]['max_depth'] = int(round(opt_params[1]['max_depth']))
opt_params[1]['min_child_weight'] = int(round(opt_params[1]['min_child_weight']))
opt_params[1]['scale_pos_weight'] = int(round(opt_params[1]['scale_pos_weight']))
opt_params[1]['objective']='binary:logistic'
opt_params[1]['metric']='auc'
opt_params[1]['nthread']=4
opt_params[1]['seed']=6
opt_params=opt_params[1]
opt_params


# In[ ]:


def modelfit(alg, dtrain, dtest, predictors, target, eval_metric = True):
        #Fit the algorithm on the data
        if eval_metric:
            alg.fit(dtrain[predictors], dtrain[target].values.ravel(), eval_metric = ['auc'])
        else: 
            alg.fit(dtrain[predictors], dtrain[target].values.ravel())
            
        #Predict training set:
        dtrain_predictions = alg.predict(dtrain[predictors])
        dtrain_predprob = alg.predict_proba(dtrain[predictors])[:,1]
        
        #Predict test set:
        dtest_predictions = alg.predict(dtest[predictors])
        dtest_predprob = alg.predict_proba(dtest[predictors])[:,1]
            
        #Print model report:
        print( " Model Report")
        print("Accuracy Train: %.4g" % metrics.accuracy_score(dtrain[target].values, dtrain_predictions))
        print("Recall Train: %.4g" % metrics.recall_score(dtrain[target].values, dtrain_predictions))
        print("Accuracy Test: %.4g" % metrics.accuracy_score(dtest[target].values, dtest_predictions))
        print("Recall Test: %.4g" % metrics.recall_score(dtest[target].values, dtest_predictions))
        print("AUC Score (Train): %f" % metrics.roc_auc_score(dtrain[target], dtrain_predprob))


# In[ ]:


xgb1 = XGBClassifier(
        learning_rate =opt_params['learning_rate'],
        n_estimators=opt_params['n_estimators'],
        max_depth=6,
        min_child_weight=opt_params['min_child_weight'],
        gamma=opt_params['gamma'],
        subsample=opt_params['subsample'],
        colsample_bytree=opt_params['colsample_bytree'],
        objective= 'binary:logistic',
        nthread=4,
        scale_pos_weight=opt_params['scale_pos_weight'],
        seed=6)

modelfit(xgb1, train, test, features, target = label)


# In[ ]:


print('Accuracy naive model: {:1.4f}'.format(1-test[label].mean()))


# We've gained 6% from the naive model, not so much. 
# 
# For this reason, we'll try with **Logistic Regression** (back to my dear glms)  and check accuracy for train and test datasets. First, we will study correlations: 

# In[ ]:


df.columns


# In[ ]:


features0 = ['Gender', 'Age', 'Scholarship', 'Hipertension', 'Diabetes',
       'Alcoholism', 'SMS_received','PreviousApp', 'PreviousNoShow', 'WeekdayScheduled', 'HasHandicap',
       'PreviousDisease', 'WeekdayAppointment', 'DaysBeforeApp',
       'DaysBeforeCat']
corr = df_done[features0].corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
plt.title('Correlation Matrix')
plt.gcf().set_size_inches(10, 6)
plt.show()

corr


# From the matrix, we can see that Hipertension is highly correlated with PreviousDisease, Age and Diabetes. Also, Age is highly correlated with PreviousDisease. For this reason, we will eliminate PreviousDisease from the analysis but shall keep the others (correlation is high but not extreme). 
# 
# Previously, NaN values didn't matter, as XGBoost learned from the data which path was the best. As now observations with missing values can not be used, we will change the variable PreviousNoShow as MissedAppointments : number of previous appointments with no-show. 
# 
# Also, we will scale the data so all values are between 1 and 0. 

# In[ ]:


df_done.loc[:, 'MissedAppointments'] = df_done.sort_values(['ScheduledDay']).groupby(['PatientId'])['NoShow'].cumsum()


# In[ ]:


features2 = ['Age','Scholarship','Hipertension','Diabetes', 'Alcoholism', 'SMS_received',
             'PreviousApp','MissedAppointments','HasHandicap', 'ScheduledMonday',
             'ScheduledTuesday', 'ScheduledWednesday', 'ScheduledThursday', 'ScheduledFriday',
             'AppointmentMonday', 'AppointmentTuesday', 'AppointmentWednesday',
             'AppointmentThursday', 'AppointmentFriday','IsFemale', 'Ant0Days', 'Ant12Days',
             'Ant37Days', 'Ant831Days', 'Ant32Days']


# In[ ]:


scaler = StandardScaler().fit(df_done[features2])
df_rescaled = scaler.transform(df_done[features2])

X_train, X_test, y_train, y_test = train_test_split(df_done[features2], df_done[label], test_size=0.3, random_state=6)
y_train = pd.DataFrame(y_train)
train = X_train.merge(y_train, left_index = True, right_index = True)
y_test = pd.DataFrame(y_test)
test = X_test.merge(y_test, left_index = True, right_index = True)


# In[ ]:


logit = LogisticRegression(class_weight = 'balanced', solver = 'liblinear')
modelfit(logit, train, test, features2, label, eval_metric = False)


# Accuracy is way better than XGBoost ! Compared to naive model, we got an improvement of almost 14% for test data on accuracy. 
# 
# We will train a **Decision Tree**, just to check how does this model compare to the two we already have. 

# In[ ]:


tree = DecisionTreeClassifier(max_depth=12, random_state=0)
modelfit(tree, train, test,features2, label, eval_metric=False)


# The decision tree performs even better for accuracy! If we set class_weight as 'balanced', recall is higher but accuracy lowers its value. As explained before, medical hospitals contacted prefered accuracy over recall so we choose the tree without balance. Keep in mind that having recall over 0.85 is very high (85% of no-shows are being captured by the model) ! 
# 
# *Note: For a long time I have used XGBoost without consulting other models (I know, my bad). I loved this example as it hit my pride and made me reconsiderate my initial approach, changing the whole problem for better performance. Every day we can learn something new !*
# 
# Finally, we will train a **Random Forest**: as one decision tree performed better, maybe several decision trees perform best. 

# In[ ]:


rf = RandomForestClassifier(random_state = 0, class_weight = 'balanced')
modelfit(rf, train, test,features2, label, eval_metric=False)


# The best so far !! We will use this model to study variable importance and predictive power. 

# In[ ]:


feature_importance = pd.DataFrame({'feature' : features2,
                                   'importances' : rf.feature_importances_})
ordered = feature_importance.sort_values(['importances'], ascending = False)
best = ordered[:10]
sns.barplot(x = 'importances', y = 'feature', data = best)
plt.xlabel('Feature Importance')
plt.title('Feature Importance Plot - Decision Tree')
plt.show()


# We can see that the most important feature is "MissedAppointments", "Age" and "PreviousApp". Two of these three variables make reference to the patient's past behavior, which supports the hypothesis of patients repeating behaviors over time. As we have little history this is not enough to say that patients will always behave the same way but for this period of time this is true. 
# 
# For better understanding, we will use SHAP Values. DanB made a marvelous job explaining advanced uses of SHAP Values (see [here](https://www.kaggle.com/dansbecker/advanced-uses-of-shap-values))  and for better understanding you can check this [medium post](https://medium.com/@gabrieltseng/interpreting-complex-models-with-shap-values-1c187db6ec83) . 

# In[ ]:


sample = X_test.sample(300)
shap.initjs()
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(sample[features2])
shap.summary_plot(shap_values[1], sample[features2])


# From SHAP Values, we can see that the most important variable is "MissedAppointments" (as mentioned before). In fact, this variable is able to divide the data, impact negatively on the model output for low values of MissedApointments and impact positively for higher values of missed appointments (which makes sense). 
# 
# Another variable to watch is "Ant0days". As a reminder, this variable takes the value 1 when the appointment was scheduled with less than a day of anticipation and 0 for any other case (which means that low values of the variable correspond to appointments scheduled with at least one day of anticipation, while high values are for appointments with less than a day of anticipation). In the plot above, we can see there's a clear separation for Ant0days: appointments with value 1 lower the chanses of noshow, while appointments with value 0 receive a positive impact (elevates chances of no-show, also makes sense). 
# 
# Now we shall study how the model clasificates in general: 

# In[ ]:


df_done['preds'] = rf.predict(df_done[features2])
cm = metrics.confusion_matrix(df_done['NoShow'], (df_done['preds'] > 0.5)*1)
normalize = False 

fig, ax = plt.subplots()
im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
ax.figure.colorbar(im, ax=ax)
# We want to show all ticks...
ax.set(xticks=np.arange(cm.shape[1]),
       yticks=np.arange(cm.shape[0]),
       xticklabels=['Show', 'No Show'], yticklabels=['Show', 'No Show'],
       title='Confusion Matrix',
       ylabel='True label',
       xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
fmt = '.2f' if normalize else 'd'
thresh = cm.max() / 2.
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j, i, format(cm[i, j], fmt),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black")

ax

print('True Positive Rate (recall): {:1.3f}'.format(metrics.recall_score(df_done['NoShow'], (df_done['preds'] > 0.5)*1)))
print('Accuracy: {:1.3f}'.format(metrics.accuracy_score(df_done['NoShow'], (df_done['preds'] > 0.5)*1)))


# From the above, we can see how the random forest classifies correctly or incorrectly each appointment. The model is able to correctly predict more than 93% of No-Shows, which is very high. At the same time, more than 97% of cases are correctly labeled so the hospital should expect less than 3% of error (very very low). 

# In[ ]:


# ROC Curve 
probs = rf.predict_proba(df_done[features2])[:,1]

fpr, tpr, threshold = metrics.roc_curve(df_done['NoShow'], probs)
roc_auc = metrics.auc(fpr, tpr)


plt.title('Receiver Operating Characteristic Curve')
plt.plot(fpr, tpr, label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()


# ROC Curve is almost perfect ! We have very early return (high true positive rate with low false positive rate, the ideal) which indicates that the model is very good. 
# 
# Sometimes accuracy this high (over 90%) makes one wonder if we are overfitting data and that if we change the sample, the model will lower it's performance. However we must keep in mind that, because we have a very unbalanced data set, the naive model already has accuracy score near 80%, so this should be our point of start. In most "academic" excercises, data is perfectly balanced (50-50) so achieving accuracy above 90% is considered at least suspicious.But for unbalanced data, this doesn't apply (actually, no model should give accuracy below the naive model). 

# Hope you enjoyed this study as much as I did ! I personally loved that everything went exactly opposite as I planned, forcing me to reconsider XGBoost for all cases and realizing that the nature of the problem defines the best model (and of course, the data!). 
#  
# If you have a different point of view, or just want to add something to the analysis I encourage to do so! In the meantime, I'll try to improve the analysis with more plots or comments that clarifies any doubt. 

# 
