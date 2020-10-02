#!/usr/bin/env python
# coding: utf-8

# # TelCo Churn Analysis

# ## Introduction

# TelCo is a company that offers telecommunications services (e.g. telephone, internet, television) to consumers in exchange for a subscription fee. They have provided us with a dataset concerning their customers, and they would like to know which customers are likely to **churn** (i.e. cancel their subscription) and which attributes affect a customer's likelihood to churn. If TelCo can predict which customers are going to cancel their subscription, measures can be taken to persuade the customers to stay. They could send promotional emails, offer a discount, or provide extra services. After all, retaining a customer is cheaper than attaining a new one. 
# 
# To attain our goal, we will first explore the dataset using Exploratory Data Analysis, after which we can build a model that can predict which customers will churn.

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv('../input/WA_Fn-UseC_-Telco-Customer-Churn.csv')
df.head()


# In[ ]:


df_copy = df


# ## Exploratory Data Analysis

# In[ ]:


df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(0, inplace=True)


# In[ ]:


df.isna().any()


# First, we will create a barchart for all categorical features that show the distribution per class (non-churn or churn).

# In[ ]:


axis_y = "percentage of customers"

#Grouped by partner
gp_partner = df.groupby('Partner')["Churn"].value_counts()/len(df)
gp_partner = gp_partner.to_frame().rename({"Churn": axis_y}, axis=1).reset_index()

#Grouped on dependents
gp_dep = df.groupby('Dependents')["Churn"].value_counts()/len(df)
gp_dep = gp_dep.to_frame().rename({"Churn": axis_y}, axis=1).reset_index()

#Grouped multiple lines per customer by churn rate
gp_mpl = df.groupby('MultipleLines')["Churn"].value_counts()/len(df)
gp_mpl = gp_mpl.to_frame().rename({"Churn": axis_y}, axis=1).reset_index()

#Grouped internet services per customer by churn rate
gp_is = df.groupby('InternetService')["Churn"].value_counts()/len(df)
gp_is = gp_is.to_frame().rename({"Churn": axis_y}, axis=1).reset_index()

#Grouped online backup per customer by churn rate
gp_ob = df.groupby('OnlineBackup')["Churn"].value_counts()/len(df)
gp_ob = gp_ob.to_frame().rename({"Churn":axis_y}, axis=1).reset_index()

#Grouped device protection per customer by churn rate
gp_dp = df.groupby('DeviceProtection')["Churn"].value_counts()/len(df)
gp_dp = gp_dp.to_frame().rename({"Churn": axis_y}, axis=1).reset_index()

#Grouped tech support per customer by churn rate
gp_ts = df.groupby('TechSupport')["Churn"].value_counts()/len(df)
gp_ts = gp_ts.to_frame().rename({"Churn": axis_y}, axis=1).reset_index()

#Grouped streaming TV per customer by churn rate
gp_st = df.groupby('StreamingTV')["Churn"].value_counts()/len(df)
gp_st = gp_st.to_frame().rename({"Churn":axis_y}, axis=1).reset_index()        
                                    
#Grouped streaming movies per customer by churn rate
gp_sm = df.groupby('StreamingMovies')["Churn"].value_counts()/len(df)
gp_sm = gp_sm.to_frame().rename({"Churn": axis_y}, axis=1).reset_index()

#Grouped contract per customer by churn rate
gp_con = df.groupby('Contract')["Churn"].value_counts()/len(df)
gp_con = gp_con.to_frame().rename({"Churn": axis_y}, axis=1).reset_index()

#Grouped paperless billing per customer by churn rate
gp_pb = df.groupby('PaperlessBilling')["Churn"].value_counts()/len(df)
gp_pb = gp_pb.to_frame().rename({"Churn":axis_y}, axis=1).reset_index()   

#Grouped payment method per customer by churn rate
gp_pm = df.groupby('PaymentMethod')["Churn"].value_counts()/len(df)
gp_pm = gp_pm.to_frame().rename({"Churn": axis_y}, axis=1).reset_index()


# In[ ]:


fig, axis = plt.subplots(4,3, figsize=(25,25))
axis[0,0].set_title("Has partner")
axis[0,1].set_title("Has dependents")
axis[0,2].set_title("Has multiple lines")
axis[1,0].set_title("Type of internet services")
axis[1,1].set_title("Has online backup")
axis[1,2].set_title("Has device protection")
axis[2,0].set_title("Has tech support")
axis[2,1].set_title("Has streaming TV")
axis[2,2].set_title("Has streaming movies")
axis[3,0].set_title("Type of contract")
axis[3,1].set_title("Has paperless billing")
axis[3,2].set_title("Type of payment method")

ax = sns.barplot(x='Partner', y=axis_y, hue='Churn', data=gp_partner, ax=axis[0,0])
ax = sns.barplot(x='Dependents', y=axis_y, hue='Churn', data=gp_dep, ax=axis[0,1])
ax = sns.barplot(x='MultipleLines', y=axis_y, hue='Churn', data=gp_mpl, ax=axis[0,2])
ax = sns.barplot(x='InternetService', y=axis_y, hue='Churn', data=gp_is, ax=axis[1,0])
ax = sns.barplot(x='OnlineBackup', y=axis_y, hue='Churn', data=gp_ob, ax=axis[1,1])
ax = sns.barplot(x='DeviceProtection', y=axis_y, hue='Churn', data=gp_dp, ax=axis[1,2])
ax = sns.barplot(x='TechSupport', y=axis_y, hue='Churn', data=gp_ts, ax=axis[2,0])
ax = sns.barplot(x='StreamingTV', y=axis_y, hue='Churn', data=gp_st, ax=axis[2,1])
ax = sns.barplot(x='StreamingMovies', y=axis_y, hue='Churn', data=gp_sm, ax=axis[2,2])
ax = sns.barplot(x='Contract', y=axis_y, hue='Churn', data=gp_con, ax=axis[3,0])
ax = sns.barplot(x='PaperlessBilling', y=axis_y, hue='Churn', data=gp_pb, ax=axis[3,1])
ax = sns.barplot(x='PaymentMethod', y=axis_y, hue='Churn', data=gp_pm, ax=axis[3,2])


# Next, we have donut charts showing the distibution of gender (Male/Female) and the distribution of our classes (Non-Churn/Churn). Sadly, there are more non-churners than churners. This means that our dataset is unbalanced, which needs to be handled before we can build our models.

# In[ ]:


plt.figure(1)

plt.pie(x=df['gender'].value_counts().values, labels=df['gender'].value_counts().index, autopct='%1.2f', data=df)
my_circle=plt.Circle((0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.title('Distribution of Gender')

plt.figure(2)
plt.pie(x=df['Churn'].value_counts().values, labels=df['Churn'].value_counts().index, autopct='%1.2f', data=df)
my_circle=plt.Circle((0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.title('Distribution of Churn rate')

plt.show()


# We will also show the distribution of the tenure feature (the duration of a customers subscription in months) per class. This graph shows that there are more customers that churn early in comparison to intermediate months. There are also many customers that have 72 months of tenure. This might mean that there are actually customers that have a longer tenure than 72 months, but that 72 months is chosen to be a cutoff point. What is certain, however, is that the churn rate diminishes for customers with longer tenure. 

# In[ ]:


plt.figure(figsize=(20,10))
sns.countplot(x='tenure', hue='Churn', data=df, palette='pastel')

plt.title("Number of months the customer has stayed with the company")
plt.xlabel('Number of months')
plt.ylabel('Count');


# Finally, we will show a density plot for the continuous variables ('Monthly Charges', 'Total Charges', and 'Tenure') per class. These density plots show that customers with higher montly charges are more likely to churn, while churn is rather independent of total charges. This can be explained by the fact that customers with large total charges are by definition a customer for longer, while having large monthly charges is independent of tenure. The 'Tenure' distribution again shows that customers that churn are likely to churn early. 

# In[ ]:


fig, axis = plt.subplots(1,3, figsize=(15,5))
axis[0].set_title("Distribution of Monthly Charges based on Churn")
axis[1].set_title("Distribution of Total Charges based on Churn")
axis[2].set_title("Distribution of Tenure based on Churn")

sns.kdeplot(df.MonthlyCharges[df.Churn=='Yes'], label='yes', shade=True, ax=axis[0])
sns.kdeplot(df.MonthlyCharges[df.Churn=='No'], label='No', shade=True, ax=axis[0])

sns.kdeplot(df.TotalCharges[df.Churn=='Yes'], label='yes', shade=True, ax=axis[1])
sns.kdeplot(df.TotalCharges[df.Churn=='No'], label='No', shade=True, ax=axis[1])

sns.kdeplot(df.tenure[df.Churn=='Yes'], label='yes', shade=True, ax=axis[2])
sns.kdeplot(df.tenure[df.Churn=='No'], label='No', shade=True, ax=axis[2])


# ## Data Manipulation & Feature Extraction

# Before we can train our models, we need to manipulate/transform our data, and to extract relevant features. For one thing, it is necessary that the features inserted in our model are numerical. So we need to convert our categorical features (that contain text) to numerical features.

# In[ ]:


df.info()


# In[ ]:


df['TotalCharges'].value_counts()


# Transform the categorical gender column to a numerical category (Female = 0, Male = 1).

# In[ ]:


gender_mapping = {'Female': 0, 'Male': 1}
df['gender'] = df['gender'].map(gender_mapping).astype(int)


# Transform the variables that onlyl have 'No'/'Yes' values to a binary variable (No = 0, Yes = 1).

# In[ ]:


no_yes_mapping = {'No': 0, 'Yes': 1}
df['Partner'] = df['Partner'].map(no_yes_mapping).astype(int)
df['Dependents'] = df['Dependents'].map(no_yes_mapping).astype(int)
df['PhoneService'] = df['PhoneService'].map(no_yes_mapping).astype(int)
df['PaperlessBilling'] = df['PaperlessBilling'].map(no_yes_mapping).astype(int)
df['Churn'] = df['Churn'].map(no_yes_mapping).astype(int)


# There are also some variables with a category like 'No internet service' or 'No phone service'. This category is equivalent to not having the service, so transform these to a binary variable as well (No = 0, Yes = 1). 

# In[ ]:


df['MultipleLines'].value_counts()


# In[ ]:


no_yes_mapping = {'No': 0, 'No internet service': 0, 'No phone service': 0, 'Yes': 1}
df['MultipleLines'] = df['MultipleLines'].map(no_yes_mapping).astype(int)
df['OnlineSecurity'] = df['OnlineSecurity'].map(no_yes_mapping).astype(int)
df['OnlineBackup'] = df['OnlineBackup'].map(no_yes_mapping).astype(int)
df['DeviceProtection'] = df['DeviceProtection'].map(no_yes_mapping).astype(int)
df['TechSupport'] = df['TechSupport'].map(no_yes_mapping).astype(int)
df['StreamingTV'] = df['StreamingTV'].map(no_yes_mapping).astype(int)
df['StreamingMovies'] = df['StreamingMovies'].map(no_yes_mapping).astype(int)


# The 'TotalCharges' column has some invalid rows. Convert the 'TotalCharges' column from 'Object' dtype to a 'float' dtype. Enter 0 in the rows with NaN/incorrect values.

# In[ ]:


df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')


# In[ ]:


df['TotalCharges'].fillna(0, inplace=True)


# In[ ]:


df.info()


# The remaining categorical variables have to be transformed into dummy variables. 

# In[ ]:


df['InternetService'].value_counts()


# In[ ]:


df = pd.concat([df, pd.get_dummies(df['InternetService'], prefix='InternetService')], axis=1)
df.drop('InternetService', axis=1, inplace=True)
df.rename(columns={'InternetService_Fiber optic': 'InternetService_Fiber'}, inplace=True)


# In[ ]:


df = pd.concat([df, pd.get_dummies(df['Contract'], prefix='Contract')], axis=1)
df.drop('Contract', axis=1, inplace=True)
df.rename(columns={'Contract_Month-to-month': 'Contract_Monthly',
                   'Contract_One year': 'Contract_1Year',
                   'Contract_Two year': 'Contract_2Year'}, inplace=True)


# In[ ]:


df = pd.concat([df, pd.get_dummies(df['PaymentMethod'], prefix='Payment')], axis=1)
df.drop('PaymentMethod', axis=1, inplace=True)
df.rename(columns={'Payment_Bank transfer (automatic)': 'Payment_Bank',
                   'Payment_Credit card (automatic)': 'Payment_Creditcard',
                   'Payment_Electronic check': 'Payment_ElectronicCheck',
                   'Payment_Mailed check': 'Payment_MailedCheck'}, inplace=True)


# Drop the customerID column, since it won't be needed for further analysis.

# In[ ]:


df.drop('customerID', axis=1, inplace=True)


# ## Correlation Matrices

# Change the order of the columns of our dataframe, so the churn variable is presented first.

# In[ ]:


df = df[['Churn', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
       'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
       'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
       'PaperlessBilling', 'MonthlyCharges', 'TotalCharges',
       'InternetService_DSL', 'InternetService_Fiber', 'InternetService_No',
       'Contract_Monthly', 'Contract_1Year', 'Contract_2Year', 'Payment_Bank',
       'Payment_Creditcard', 'Payment_ElectronicCheck', 'Payment_MailedCheck']]


# In[ ]:


# Get a correlation DataFrame.
corr = df.corr()

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(14, 14))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, cmap=cmap, vmin=-0.5, vmax=0.5, center=0,
            square=True, linewidths=.5);


# Get a correlation DataFrame, sorted descending, and get only the 'Churn' column, since this is our dependent variable. As you can see, there are some features that have a positive correlation with 'Churn', like having a monthly contract, having higher charges, and having more services. Other features are negatively correlated with 'Churn', like a customer's tenure and having longer-term contracts. These will probably be important features for training our model.

# In[ ]:


corr = df.corr()
corr = corr[['Churn']]
corr.sort_values(by='Churn', ascending=False, inplace=True)
corr = corr.iloc[1:]

f, ax = plt.subplots(figsize=(11, 9))

cmap = sns.diverging_palette(220, 10, as_cmap=True)

sns.heatmap(corr, cmap=cmap, vmin=-0.5, vmax=0.5, center=0,
            square=True, linewidths=.5);


# ## Data Preparation

# Split the dependent variable (y) from the independent variables (X).

# In[ ]:


X = df[['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
       'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
       'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
       'PaperlessBilling', 'MonthlyCharges', 'TotalCharges',
       'InternetService_DSL', 'InternetService_Fiber', 'InternetService_No',
       'Contract_Monthly', 'Contract_1Year', 'Contract_2Year', 'Payment_Bank',
       'Payment_Creditcard', 'Payment_ElectronicCheck', 'Payment_MailedCheck']]
y = df['Churn']


# Some of our variables are on different scales (the categorical variables between 0 and 1, while 'MonthlyCharges' and 'TotalCharges' are between 0 and 9000). A MinMaxScaler will be applied to our independent variables to convert the values to be within 0 and 1, so that all the variables will receive the same weight when training our models.

# In[ ]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

columns = X.columns
X = scaler.fit_transform(X)

X = pd.DataFrame(X, columns=columns)


# Since our dataset is unbalanced (more non-churners than churners (75% and 25%, respectively)), we need to apply an oversampling technique called SMOTE (Synthetic Minority Over-sampling Technique) that will oversample rows from the minority class, making it a balanced dataset. 

# In[ ]:


from imblearn.over_sampling import SMOTE

os = SMOTE(random_state = 0)
X, y = os.fit_sample(X, y)
X = pd.DataFrame(data = X, columns=columns)
y = pd.Series(data = y);


# ## Logistic Regression

# We will try to fit a first logistic regression to the dataset. We use cross-validation to test how well our models perform on unseen data. 

# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, cross_val_predict, cross_validate
from sklearn.metrics import accuracy_score
reg = LogisticRegression(C=2, solver='liblinear')
reg.fit(X, y)
print("Logistic Regression:\n")
y_test_predict = cross_val_predict(reg, X, y, cv=10)
print("The accuracy score for the test set is:     ", cross_val_score(reg, X, y, cv=10).mean())


# The coefficients of our logistic regression model are as follows: 

# In[ ]:


print('{:30s}{:10s}\n'.format('Feature', 'Coefficient'))
print('{:30s}{:5.3f}'.format('Intercept', reg.intercept_[0]))
for i, feature in enumerate(reg.coef_[0]):
    print('{:30s}{:5.3f}'.format(X.columns[i], feature))


# In[ ]:


from sklearn.metrics import classification_report
print(classification_report(y, y_test_predict))


# For all our models, we will analyze their **recall** (% of the actual churners that the model correctly predicts), **precision** (% of the predicted churners that are correct) and **accuracy** (% of the predictions that are correct). These metrics will be used to compare the models. We will also compare the training accuracy score with the test accuracy score to determine how well the model performs on unseen data.

# In[ ]:


from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
model_scores = pd.DataFrame(columns=['Model', 'Recall', 'Precision', 'Accuracy'])
model_scores.loc[0] = ['Logistic Regression',
                       recall_score(y, y_test_predict),
                       precision_score(y, y_test_predict),
                       accuracy_score(y, y_test_predict)]


# In[ ]:


bias_variance = pd.DataFrame(columns=['Model', 'Training Score', 'Test Score'])
scores = cross_validate(reg, X, y, cv=10, return_train_score=True)
bias_variance.loc[0] = 'Logistic Regression', scores['test_score'].mean(), scores['train_score'].mean()


# In[ ]:


model_scores


# Also, for all models we will create a **Receiver Operating Characteristic (ROC)**, which shows the relationship between the **True Positive Rate** and the **False Positive Rate** at various threshold settings. It tells you how well the model is capable to distinguish between classes, in our case non-churners and churners. A better model has a higher **Area under the curve (AUC)**.

# In[ ]:


from sklearn.metrics import roc_auc_score, roc_curve, scorer, auc
probabilities = reg.predict_proba(X)
fpr_reg, tpr_reg, thresholds = roc_curve(y, probabilities[:,1])
reg_auc = auc(fpr_reg, tpr_reg)
print("Area under curve: ", reg_auc)


# In[ ]:


plt.figure(figsize=(10, 8))
plt.title('Receiver Operating Characteristic (Logistic Regression)')
plt.plot(fpr_reg, tpr_reg, 'b', label = 'AUC = %0.2f' % reg_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()


# We will now plot the coefficients in a sorted bar-chart to get a better overview. It is clear that **tenure** negatively affects churn and that **TotalCharges** has a positive effect on churn.

# In[ ]:


coefficients  = pd.DataFrame(reg.coef_.ravel())
column_df     = pd.DataFrame(['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
                              'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
                              'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                              'PaperlessBilling', 'MonthlyCharges', 'TotalCharges',
                              'InternetService_DSL', 'InternetService_Fiber', 'InternetService_No',
                              'Contract_Monthly', 'Contract_1Year', 'Contract_2Year', 'Payment_Bank',
                              'Payment_Creditcard', 'Payment_ElectronicCheck', 'Payment_MailedCheck'])
coef_sumry    = (pd.merge(coefficients, column_df, left_index=True,
                              right_index=True, how="left"))
coef_sumry.columns = ["coefficients","features"]
coef_sumry    = coef_sumry.sort_values(by="coefficients", ascending=False)


# In[ ]:


plt.figure(figsize=(20, 10))
sns.barplot(data=coef_sumry, x='coefficients', y='features', palette='pastel')
plt.xlabel(xlabel='Features', fontsize=20)
plt.ylabel(ylabel='Coefficients', fontsize=20)
plt.title(label='Feature Coefficients', fontsize=20)
plt.xticks(rotation=0);


# Last but not least, we will provide a confusion matrix to determine the amount of True Negatives (TN), False Posivites (FP), False Negatives (FN) and True Posivites (TP). The red blocks are the instances that the model has correctly predicted (either the non-churners or the churners), and are fortunately much bigger than the incorrect predictions (the blue blocks).

# In[ ]:


from sklearn.metrics import confusion_matrix
cfn_matrix = confusion_matrix(y, y_test_predict)

# Plot confusion matrix in a beautiful manner
ax = plt.subplot()
sns.heatmap(cfn_matrix, annot=True, fmt='g', ax = ax, cmap=cmap, linewidths=1); 

# labels, title and ticks
ax.set_xlabel('Predicted', fontsize=20)
ax.xaxis.set_label_position('top') 
ax.xaxis.set_ticklabels(['No Churn', 'Churn'], fontsize = 15)
ax.xaxis.tick_top()

ax.set_ylabel('True', fontsize=20)
ax.yaxis.set_ticklabels(['No Churn', 'Churn'], fontsize = 15)
plt.show()


# ## Random Forest

# We will now do the same, but with a **Random Forest**:

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier(n_estimators=350, max_features='auto', max_depth=5, criterion='gini',
                             min_samples_leaf=3, min_samples_split=12)
RFC.fit(X, y)
y_test_predict = cross_val_predict(RFC, X, y, cv=10)
print("Random Forest Classifier:\n")
print("The accuracy score for the test set is:     ", cross_val_score(RFC, X, y, cv=10).mean())


# In[ ]:


print(classification_report(y, y_test_predict))


# In[ ]:


model_scores.loc[1] = ['Random Forest',
                       recall_score(y, y_test_predict),
                       precision_score(y, y_test_predict),
                       accuracy_score(y, y_test_predict)]


# In[ ]:


scores = cross_validate(RFC, X, y, cv=10, return_train_score=True)
bias_variance.loc[1] = 'Random Forest', scores['test_score'].mean(), scores['train_score'].mean()


# In[ ]:


probabilities = RFC.predict_proba(X)
fpr_RFC, tpr_RFC, thresholds = roc_curve(y, probabilities[:,1])
RFC_auc = auc(fpr_RFC, tpr_RFC)
print("Area under curve is: ", RFC_auc)
# Plot the ROC curve of the Random Forest Classifier
plt.figure(figsize=(10, 8))
plt.title('Receiver Operating Characteristic (Random Forest Classifier)')
plt.plot(fpr_RFC, tpr_RFC, 'b', label = 'AUC = %0.2f' % RFC_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1], 'r--')
plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()


# In[ ]:


cfn_matrix = confusion_matrix(y, y_test_predict)

# Plot confusion matrix in a beautiful manner
ax = plt.subplot()
sns.heatmap(cfn_matrix, annot=True, fmt='g', ax = ax, cmap=cmap, linewidths=1); 

# labels, title and ticks
ax.set_xlabel('Predicted', fontsize=20)
ax.xaxis.set_label_position('top') 
ax.xaxis.set_ticklabels(['No Churn', 'Churn'], fontsize = 15)
ax.xaxis.tick_top()

ax.set_ylabel('True', fontsize=20)
ax.yaxis.set_ticklabels(['No Churn', 'Churn'], fontsize = 15)
plt.show()


# Instead of coefficients, a Random Forest has **Feature Importances** that demonstrate how important a feature was for building the decision trees. These weights say nothing about whether the features affect churn negatively or positively though.

# In[ ]:


importances = pd.DataFrame(RFC.feature_importances_)
importances_df = (pd.merge(importances, column_df, left_index=True,
                              right_index=True, how="left"))
importances_df.columns = ["feature importance", "features"]
importances_df = importances_df.sort_values(by="feature importance", ascending=False)

# Plot the feature importances
plt.figure(figsize=(20, 10))
sns.barplot(data=importances_df, x='features', y='feature importance', palette='Blues')
plt.xlabel(xlabel='Features', fontsize=20)
plt.ylabel(ylabel='Feature importance', fontsize=20)
plt.title(label='Feature Importance (Random Forest Classifier)', fontsize=20)
plt.xticks(rotation=90);


# ## K-Nearest Neighbors

# Last but not least, we will make a K-Nearest Neighbors classifier:

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=10)
knn.fit(X, y)
y_test_predict = cross_val_predict(knn, X, y, cv=10)
print("K-Nearest Neighbors Classification (k=10): ")
print("Accuracy of the test data:", cross_val_score(knn, X, y, cv=10).mean())


# In[ ]:


scores = cross_validate(knn, X, y, cv=10, return_train_score=True)
bias_variance.loc[2] = 'K-Nearest Neighbors', scores['test_score'].mean(), scores['train_score'].mean()


# In[ ]:


print(classification_report(y, y_test_predict))


# In[ ]:


model_scores.loc[2] = ['K-Nearest Neighbors',
                       recall_score(y, y_test_predict),
                       precision_score(y, y_test_predict),
                       accuracy_score(y, y_test_predict)]


# In[ ]:


probabilities = knn.predict_proba(X)
fpr_knn, tpr_knn, thresholds = roc_curve(y, probabilities[:,1])
knn_auc = auc(fpr_knn, tpr_knn)
print("Area under the curve is : ", knn_auc)

# Plot the ROC curve of the K-Nearest Neighbors Classifier
plt.figure(figsize=(10, 8))
plt.title('Receiver Operating Characteristic (K-Nearest Neighbor)')
plt.plot(fpr_knn, tpr_knn, 'b', label = 'AUC = %0.2f' % knn_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()


# In[ ]:


cfn_matrix = confusion_matrix(y, y_test_predict)

# Plot confusion matrix in a beautiful manner
ax = plt.subplot()
sns.heatmap(cfn_matrix, annot=True, fmt='g', ax = ax, cmap=cmap, linewidths=1); 

# labels, title and ticks
ax.set_xlabel('Predicted', fontsize=20)
ax.xaxis.set_label_position('top') 
ax.xaxis.set_ticklabels(['No Churn', 'Churn'], fontsize = 15)
ax.xaxis.tick_top()

ax.set_ylabel('True', fontsize=20)
ax.yaxis.set_ticklabels(['No Churn', 'Churn'], fontsize = 15)
plt.show()


# # Conclusion

# K-Nearest Neighbors is the best-scoring model on the TelCo dataset. Although it has a smaller **Precision** than the other models, its **Recall** and **Accuracy** is significantly better, as well as having the highest **AUC (Area under the curve)**. In our opinion, TelCo should aim for a higher recall instead of precision, since it is better to incorrectly label a non-churner as a churner, than to incorrectly label a churner as a non-churner. Sending an email or a discount coupon is cheap, while losing a customer means losing its revenue. 

# In[ ]:


model_scores


# In[ ]:


# Plot the ROC curve of all the models together
plt.style.use('seaborn')
plt.figure(figsize=(13, 9))
plt.title('Receiver Operating Characteristic (All Models))')
plt.plot(fpr_reg, tpr_reg, 'g', label = 'Logistic Regression, AUC = %0.2f' % reg_auc)
plt.plot(fpr_RFC, tpr_RFC, 'r', label = 'Random Forest, AUC = %0.2f' % RFC_auc)
plt.plot(fpr_knn, tpr_knn, 'y', label = 'K-NN, AUC = %0.2f' % knn_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.savefig('Test2.png', dpi=300, bbox_inches='tight', pad_inches=0.3)


# To check whether the models are overfit, here is an overview of the training and test accuracy of the models. The models are scoring better on the testing data, meaning the models are not overfit and are thus suited for predicting unseen data. 

# In[ ]:


bias_variance


# ## Extra: Survival Analysis

# As an extra analysis, we will also employ survival analysis on our dataset. Survival analysis is used to calculate the expected duration of time until a specific event happens, in our case whether a customer is going to churn. So instead of predicting which customers are going to churn, with survival analysis we can predict when customers are going to churn.
# 
# However, we needed to import a package called 'lifelines' that is unavailable on Kaggle. If you want to see our Survival Analysis on this dataset, head over to the notebook on our github page: https://github.com/nieklambrechts/TelCo-Churn-Analysis
