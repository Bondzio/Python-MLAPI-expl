#!/usr/bin/env python
# coding: utf-8

# ### 1. Import Required Libraries

# In[ ]:


import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

warnings.filterwarnings("ignore")


# ### 2. Load Dataset

# In[ ]:


train_data_set = pd.read_csv("../input/train.csv")


# ### 3. Preview Data and Fill Missing Values

# In[ ]:


train_data_set.head()


# In[ ]:


# Check number of rows and columns.
train_data_set.shape


# In[ ]:


# df.describe() gives statistical information of numerical variables in the data.
train_data_set.describe()


# In[ ]:


train_data_set.info()


# ###### Column "Age", "Cabin", "Embarked" has missing values

# In[ ]:


train_data_set["Age"].hist(alpha=0.9, grid=False, color='blue')


# ###### The age feature is right skewed,will use median to fill the missing values

# In[ ]:


# Fill Missing Values for Age
train_data_set["Age"].fillna(train_data_set["Age"].median(), inplace=True)


# In[ ]:


train_data_set["Embarked"].value_counts()


# In[ ]:


# Fill Missing Values for Embarked
train_data_set["Embarked"].fillna("S", inplace=True)


# In[ ]:


# Fill Missing Values for Cabin
train_data_set["Cabin"] = train_data_set["Cabin"].apply(lambda x: str(x)[0])
train_data_set.groupby(["Cabin", "Pclass"])["Pclass"].count()


# In[ ]:


# Replace NaN with 0, and other Characters with numeric value
train_data_set["Cabin"] = train_data_set["Cabin"].replace("n", 0)
train_data_set["Cabin"] = train_data_set["Cabin"].replace(["A", "B", "C", "D", "E", "T"], 1)
train_data_set["Cabin"] = train_data_set["Cabin"].replace("F", 2)
train_data_set["Cabin"] = train_data_set["Cabin"].replace("G", 3)


# ### 4. EDA

# #### 4.1 Compare total survivors and male female survivors. 

# In[ ]:


# Get total number of male and females.
total_survivors = train_data_set[train_data_set['Survived'] == 1].count()[1]
total_non_survivors = train_data_set[train_data_set['Survived'] == 0].count()[1]

# Get total number of male and female survivors.
male_survivors = train_data_set['Survived'][train_data_set['Sex'] == 'male'].value_counts()[1]
female_survivors = train_data_set['Survived'][train_data_set['Sex'] == 'female'].value_counts()[1]


# In[ ]:


total = [total_survivors, total_non_survivors]
survivors = [male_survivors, female_survivors]


total_colors = ['#B2FF66', '#FF3333'] 
survive_colors = ['#66b3ff', '#FFB6C1']

plt.figure(figsize = (16, 10))
explode = (0.05,0.05)

ax1 = plt.subplot2grid((2,2), (0,0))
plt.pie(total, labels = ["Survived", "Not Survived"], colors = total_colors, explode = explode, autopct = '%1.1f%%', startangle = 90)
plt.title("Survivors vs Non Survivors")
plt.axis('equal')

ax1 = plt.subplot2grid((2,2), (0,1))
plt.pie(survivors, labels = ["Male", "Female"], colors = survive_colors, explode = explode, autopct = '%1.1f%%', startangle = 90)
plt.title("Male vs Female Survivors")
plt.axis('equal')

plt.axis('equal')
plt.tight_layout()
plt.show()


# ###### Not many survived the accident and Females have high probability of survival than Men.

# #### 4.2 Compare Survivors From The Place They Embarked

# In[ ]:


sns.barplot(x="Embarked", y="Survived", data=train_data_set)
plt.title("Survivors vs Embarked")
plt.show()


# ###### Passengers who embarked from Cherbourg has high probability of survival.

# #### 4.3 Compare Survivors Based On Pclass

# In[ ]:


sns.barplot(x="Pclass", y="Survived", data=train_data_set)
plt.title("Survivors vs Pclass")
plt.show()


# #### Passengers from 1st class has more survivals, maybe because of high fare.

# #### 4.4 Check SibSp Count

# In[ ]:


sns.countplot(x="SibSp", data=train_data_set)
plt.show()


# ###### Most of the passengers were travelling alone.

# #### 4.5 Compare Survivors and Age

# In[ ]:


sns.distplot(train_data_set[train_data_set['Survived'] == 1].Age.dropna(), bins=18, label = "Survived", kde =False)
sns.distplot(train_data_set[train_data_set["Survived"] == 0]["Age"].dropna(), bins = 30, label="Not Survived", kde=False)
plt.title("Survivors vs Age")
plt.legend()
plt.show()


# ### 5. Feature Engineering

# In[ ]:


# copy the data frame for future use.
copy_train_data = train_data_set.copy()


# In[ ]:


# Create a new feature "FamilySize", by combining "SibSP" and "Parch"
# Plus 1 is added as the passenger is also considered part of the family.
train_data_set["FamilySize"] = train_data_set["SibSp"] + train_data_set["Parch"] + 1


# In[ ]:


# Convert Categorical Data to Numeric
train_data_set["Sex"] = train_data_set["Sex"].map({"male": 1, "female": 0}).astype(int)
# Convert to numeric data
train_data_set["Embarked"] = train_data_set["Embarked"].map({"S": 1, "C": 2, "Q": 3})


# In[ ]:


# Drop unwanted columns
train_data_set.drop(["PassengerId", "Name", "SibSp", "Parch", "Ticket"], axis=1, inplace=True)


# In[ ]:


train_data_set.head()


# In[ ]:


# Find the correlation between the variables.
plt.figure(figsize=(12,10))
sns.heatmap(train_data_set.corr(), linewidths=0.05, fmt= ".2f", annot=True)
plt.show()


# ###### Fare, Cabin, Embarked, FamilySize has positive correlation with Survived

# ### 6. Model Fitting

# In[ ]:


X = train_data_set.drop("Survived", axis=1)
Y = train_data_set["Survived"]


# In[ ]:


x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# In[ ]:


standard_scaler = StandardScaler()

x_train = standard_scaler.fit_transform(x_train)
x_test = standard_scaler.transform(x_test)


# ##### Random Forest Classifier

# In[ ]:


# Random Forest Classifer Model
rf_model = RandomForestClassifier(criterion="entropy", max_depth=10, random_state=42)
rf_model.fit(x_train, y_train)
rf_pred = rf_model.predict(x_test)


# In[ ]:


rf_accuracy = accuracy_score(rf_pred, y_test)
print("Random Forest Accuracy: ", rf_accuracy)


# In[ ]:


print(classification_report(rf_pred, y_test))


# In[ ]:


rf_cm = confusion_matrix(rf_pred, y_test)


# In[ ]:


sns.heatmap(rf_cm, annot = True, fmt = ".0f", cmap = "YlGnBu")
plt.xlabel("Predicted Values")
plt.ylabel("Actual Values")
plt.title("Random Forest Validation Matrix\n\n")
plt.show()


# ##### Logistic Regression

# In[ ]:


# Logistic Regression Model
lr_model = LogisticRegression()
lr_model.fit(x_train, y_train)
lr_pred = lr_model.predict(x_test)


# In[ ]:


lr_accuracy = accuracy_score(lr_pred, y_test)
print("Logistic Regression Accuracy: ", lr_accuracy)


# In[ ]:


print(classification_report(lr_pred, y_test))


# In[ ]:


lr_cm = confusion_matrix(lr_pred, y_test)


# In[ ]:


sns.heatmap(lr_cm, annot = True, fmt = ".0f", cmap = "YlGnBu")
plt.xlabel("Predicted Values")
plt.ylabel("Actual Values")
plt.title("Logistic Regression Validation Matrix\n\n")
plt.show()


# ##### Decision Tree Classifier

# In[ ]:


# Decision Tree Classifier Model
dt_model = DecisionTreeClassifier(criterion="entropy", random_state=42)
dt_model.fit(x_train, y_train)
dt_pred = dt_model.predict(x_test)


# In[ ]:


dt_accuracy = accuracy_score(dt_pred, y_test)
print("Decision Tree Accuracy: ", dt_accuracy)


# In[ ]:


print(classification_report(dt_pred, y_test))


# In[ ]:


dt_cm = confusion_matrix(dt_pred, y_test)


# In[ ]:


sns.heatmap(dt_cm, annot = True, fmt = ".0f", cmap = "YlGnBu")
plt.xlabel("Predicted Values")
plt.ylabel("Actual Values")
plt.title("Decision Tree Validation Matrix\n\n")
plt.show()


# ##### Support Vector Machine

# In[ ]:


# Support Vector Machine Model
svm_model = SVC()
svm_model.fit(x_train, y_train)
svm_pred = svm_model.predict(x_test)


# In[ ]:


svm_accuracy = accuracy_score(svm_pred, y_test)
print("SVM Accuracy: ", svm_accuracy)


# In[ ]:


print(classification_report(svm_pred, y_test))


# In[ ]:


svm_cm = confusion_matrix(svm_pred, y_test)


# In[ ]:


sns.heatmap(svm_cm, annot = True, fmt = ".0f", cmap = "YlGnBu")
plt.xlabel("Predicted Values")
plt.ylabel("Actual Values")
plt.title("SVM Validation Matrix\n\n")
plt.show()


# ###### Plot Accuracy of Models

# In[ ]:


x = ["Random Forest", "Logistic Regression", "Decision Tree", "SVM"]
y = [rf_accuracy, lr_accuracy, dt_accuracy, svm_accuracy]
plt.bar(x=x, height=y)
plt.title("Algorithm Accuracy Comparison")
plt.xticks(rotation=15)
plt.xlabel("Algorithms")
plt.ylabel("Accuracy")
plt.show()


# ###### Plot Feature Importance of RandomForestClassifier

# In[ ]:


copy_data_set = train_data_set.copy()
copy_data_set.drop("Survived", axis=1, inplace=True)
plot_df = pd.DataFrame(columns=["Features", "Importance"])
plot_df["Features"] = copy_data_set.columns.values
plot_df["Importance"] = rf_model.feature_importances_

sns.barplot(x="Importance", y="Features", data=plot_df)


# ### 7. Submission

# In[ ]:


test_data_set = pd.read_csv("../input/test.csv")


# In[ ]:


test_data_set.info()


# In[ ]:


test_data_set["Age"].fillna(test_data_set["Age"].median(), inplace=True)
test_data_set["Fare"].fillna(test_data_set["Fare"].mean(), inplace=True)
test_data_set["Cabin"] = test_data_set["Cabin"].apply(lambda x: str(x)[0])
test_data_set.groupby(["Cabin", "Pclass"])["Pclass"].count()
test_data_set["Cabin"] = test_data_set["Cabin"].replace("n", 0)
test_data_set["Cabin"] = test_data_set["Cabin"].replace(["A", "B", "C", "D", "E", "T"], 1)
test_data_set["Cabin"] = test_data_set["Cabin"].replace("F", 2)
test_data_set["Cabin"] = test_data_set["Cabin"].replace("G", 3)


# In[ ]:


submission_df = pd.DataFrame(columns=["PassengerId", "Survived"])
submission_df["PassengerId"] = test_data_set["PassengerId"]


# In[ ]:


test_data_set["FamilySize"] = test_data_set["SibSp"] + test_data_set["Parch"] + 1
test_data_set["Sex"] = test_data_set["Sex"].map({"male": 1, "female": 0}).astype(int)
test_data_set.drop(["PassengerId", "Name", "SibSp", "Parch", "Ticket"], axis=1, inplace=True)
test_data_set["Embarked"] = test_data_set["Embarked"].map({"S": 1, "C": 2, "Q": 3})


# In[ ]:


scaled_test_data = standard_scaler.fit_transform(test_data_set)


# In[ ]:


rf_test_pred = rf_model.predict(scaled_test_data)


# In[ ]:


submission_df["Survived"] = rf_test_pred


# In[ ]:


submission_df.head()


# In[ ]:


submission_df.to_csv("my_submission.csv", index=False)


# In[ ]:




