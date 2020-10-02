#!/usr/bin/env python
# coding: utf-8

# # Artificial Neural Network using Keras
# Titanic <br>
# Damien Park

# ---

# In[ ]:


import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers.core import Dense
import keras
from keras.optimizers import *
from keras.initializers import *

from sklearn.metrics import classification_report

import matplotlib.pyplot as plt

from itertools import chain


# In[ ]:


df = pd.read_csv("../input/train.csv")
df.head(10)


# ## Data Dictionary

# |Variable|Definition|Key|
# |----------|-----------|:---:|
# |Survival|Survival|0 = No, 1 = Yes|
# |Pclass|Ticket class|1 = 1st, 2 = 2nd, 3 = 3rd|
# |Sex|Sex|Male and Female|
# |Age|Age in years|-|
# |Sibsp|# of siblings / spouses aboard the Titanic|-|
# |Parch|# of parents / children aboard the Titanic|-|
# |Ticket|Ticket number|-|
# |Fare|Passenger fare|-|
# |Cabin|Cabin number|-|
# |Embarked|Port of Embarkation|C = Cherbourg, Q = Queenstown, S = Southampton|

# ---

# ## 1. Data Preprocessing

# ## Fare

# In[ ]:


df.query("Fare == 0").head()


# There are a few recode which Fare is zero.
# I think it is error

# In[ ]:


plt.figure(figsize=(20,10))
plt.suptitle("Fare Distribution", size=20)

plt.subplot(2, 4, 1)
plt.title("Fare")
plt.hist(df.Fare, bins=45)

plt.subplot(2, 4, 2)
plt.title("+1, log2, log10")
plt.hist(np.log2(np.log10(df.Fare + 1) + 1), bins=45)

plt.subplot(2, 4, 3)
plt.title("+2, log2, log2")
plt.hist(np.log2(np.log2(df.Fare + 2) + 2), bins=45)

plt.subplot(2, 4, 4)
plt.title(">0, log10, round")
plt.hist(np.round(np.log10(df.query("Fare > 0").Fare), 2), bins=45)

plt.subplot(2, 4, 5)
plt.title("log2")
plt.hist(np.log2(df.Fare + 0.1), bins=45)

plt.subplot(2, 4, 6)
plt.title("log10")
plt.hist(np.log10(df.Fare + 0.1), bins=45)

plt.subplot(2, 4, 7)
plt.title(">0, log2, round")
plt.hist(np.round(np.log2(df.query("Fare > 0").Fare), 2), bins=45)

plt.subplot(2, 4, 8)
plt.title("normalization, +1, log10")
plt.hist(np.log10((df.Fare + 1 - df.Fare.min())/df.Fare.max()) +1.5, bins=45)
plt.show()


# In[ ]:


np.mean(df.Fare), np.std(df.Fare)


# In[ ]:


mean_fare = np.mean(df.Fare)
df.loc[df.Fare == 0, "Fare"] = mean_fare


# In[ ]:


# Fare normalization
#for i in range(len(df.Fare)):
#    df.loc[i, "nor_Fare"] = np.log10(np.abs((df.Fare[i]+0.1-np.mean(df.Fare)))/np.std(df.Fare))

# Fare normalization
#df["nor_Fare"] = (df.Fare - np.mean(df.Fare)) / np.std(df.Fare)

# # Fare normalization by Pclass
# for i in np.unique(df.Pclass):
#     df.loc[df.Pclass == i, "nor_Fare"] = (df.loc[df.Pclass == i, "Fare"] - np.min(df.loc[df.Pclass == i, "Fare"])) / (np.max(df.loc[df.Pclass == i, "Fare"]) - np.min(df.loc[df.Pclass == i, "Fare"]))

# Fare standardization by Pclass
# for i in np.unique(df.Pclass):
#     df.loc[df.Pclass == i, "nor_Fare"] = (df[df.Pclass == i]["Fare"] - np.mean(df[df.Pclass == i]["Fare"])) / np.std(df[df.Pclass == i]["Fare"])


# In[ ]:


# plt.hist(df.nor_Fare, bins=45)
# plt.show()


# In[ ]:


# df.Fare = np.log10((df.Fare + 1 - df.Fare.min())/df.Fare.max()) +1.5


# In[ ]:


# for idx, value in enumerate(df.Fare):
#     if value != 0:
#         df.loc[idx, "Fare"] = np.round(np.log10(value), 2)


# In[ ]:


df.head(10)


# ## Encoding
# Sex(One-Hot-Encoding) <br>
# Pclass(Label Encoding) <br>
# Embarked(Label Encoding)

# In[ ]:


# Sex Encoding
binar = LabelBinarizer().fit(df.loc[:, "Sex"])
df["Sex"] = binar.transform(df["Sex"])
df.head(10)


# In[ ]:


# Pclass Encoding
# df_Pclass = pd.DataFrame(OneHotEncoder().fit_transform(np.array(df["Pclass"])[:,np.newaxis]).toarray(), columns=["A_Class", "B_Class", "C_Class"])
# df_Pclass = df_Pclass.astype(int)
# df_Pclass.head()


# In[ ]:


# Pclass Encoding
df["A_Class"] = 0
df["B_Class"] = 0
df["C_Class"] = 0

df.loc[df.Pclass == 1, "A_Class"] = 1
df.loc[df.Pclass == 2, "B_Class"] = 1
df.loc[df.Pclass == 3, "C_Class"] = 1
df.head()


# In[ ]:


# Embarked Encoding
df_Embarked = pd.get_dummies(df.Embarked)
df_Embarked.head()


# ## Interpolation for Age

# In[ ]:


plt.hist(df.query("Age>0").Age, bins=40)
plt.show()


# In[ ]:


df.Age.isna().sum()


# In[ ]:


df.Age[df.Age.notna()][df.Age[df.Age.notna()] % 1 != 0].head()


# Age is not integer

# In[ ]:


# Nan Age is fill using average age
#df.loc[:, "Age"].fillna(int(df["Age"].mean()), inplace=True)
#df.loc[:, "Age"].fillna(int(df["Age"].median()), inplace=True)

#df.query("Sex == 'male' & Age == 'Nan'").fillna(30, inplace=True)
#df.query("Sex == 'female' & Age == 'Nan'").fillna(28, inplace=True)


# In[ ]:


df.groupby(["Sex", "Pclass"]).Age.mean()


# In[ ]:


# df.loc[:, "Age"].fillna(0, inplace=True)

# for idx, value in enumerate(df.Age):
#     if value == 0:
#         if df.Sex[idx] == 1:
#             df.Age[idx] = 30.7
#         else:
#             df.Age[idx] = 27.9


# In[ ]:


df.loc[(df.Sex == 0) & (df.Age.isna()) & (df.Pclass == 1), "Age"] = 34.6
df.loc[(df.Sex == 0) & (df.Age.isna()) & (df.Pclass == 2), "Age"] = 28.7
df.loc[(df.Sex == 0) & (df.Age.isna()) & (df.Pclass == 3), "Age"] = 21.7

df.loc[(df.Sex == 1) & (df.Age.isna()) & (df.Pclass == 1), "Age"] = 41.2
df.loc[(df.Sex == 1) & (df.Age.isna()) & (df.Pclass == 2), "Age"] = 30.7
df.loc[(df.Sex == 1) & (df.Age.isna()) & (df.Pclass == 3), "Age"] = 26.5


# In[ ]:


plt.figure(figsize=(25, 5))
plt.subplot(1, 6, 1)
plt.title("Age")
plt.hist(df.Age, bins=40)
plt.subplot(1, 6, 2)
plt.title("Age, standard")
plt.hist((df.Age-np.mean(df.Age))/np.std(df.Age)+5, bins=40)
plt.subplot(1, 6, 3)
plt.title("Age, log10")
plt.hist(np.log10(df.Age), bins=40)
plt.subplot(1, 6, 4)
plt.title("Age, log2")
plt.hist(np.log2(df.Age), bins=40)
plt.subplot(1, 6, 5)
plt.title("Age, log e")
plt.hist(np.log(df.Age), bins=40)
plt.subplot(1, 6, 6)
plt.title("Age, log 10 - mean")
plt.hist(np.log10(df.Age)-np.mean(np.log10(df.Age)), bins=40)

plt.show()


# In[ ]:


#df.Age = np.log10(df.Age) - np.mean(np.log10(df.Age))

# for i in pd.unique(df.Sex):
#     for j in pd.unique(df.Pclass):
#         df.loc[(df.Sex == i) & (df.Pclass == j), "Age"] = (df.loc[(df.Sex == i) & (df.Pclass == j), "Age"] - np.min(df.loc[(df.Sex == i) & (df.Pclass == j), "Age"])) / (np.max(df.loc[(df.Sex == i) & (df.Pclass == j), "Age"]) - np.min(df.loc[(df.Sex == i) & (df.Pclass == j), "Age"]))


# In[ ]:


df.head(10)


# ## New columes
# Boarding Together or Alone

# In[ ]:


# Boarding Together or Alone
for i in range(len(df)):
    if df.loc[i, "SibSp"] + df.loc[i, "Parch"] == 0:
        df.loc[i, "Alone"] = 1
    else:
        df.loc[i, "Alone"] = 0

df.Alone = df.Alone.astype(int)
df.head()


# ## Data Marge

# In[ ]:


df_new = pd.concat([df, df_Embarked], axis=1)
df_new.head()


# In[ ]:


#feature_name = ["Sex", "Age", "Fare", "Alone", "A_Class", "B_Class", "C_Class", "C", "Q", "S"]
feature_name = ["Sex", "Age", "Fare", "Alone", "A_Class", "B_Class", "C_Class", "C", "Q", "S", "SibSp", "Parch"]

dfX = df_new[feature_name]
dfY = df_new["Survived"]


# ## MinMaxScale

# In[ ]:


scaler = MinMaxScaler()


# In[ ]:


scaler.fit(dfX)


# In[ ]:


dfX = scaler.transform(dfX)


# In[ ]:


dfX = pd.DataFrame(dfX, columns=feature_name)


# In[ ]:


dfX.head()


# ## Split data(train, test)

# In[ ]:


#X_train, X_test, y_train, y_test = train_test_split(dfX, dfY, test_size=0.20, random_state=1)
#X_train, X_test, y_train, y_test


# ---

# ## 2. Set Artifial neural network and Learning
# multi layers

# In[ ]:


df.Survived.sum() / len(df)


# In[ ]:


model = Sequential()

model.add(Dense(32, input_dim=12, activation="elu", kernel_initializer="he_normal"))
model.add(Dense(64, activation="elu", kernel_initializer="he_normal"))
model.add(Dense(128, activation="elu", kernel_initializer="he_normal"))
model.add(keras.layers.Dropout(0.3))

model.add(Dense(512, activation="elu", kernel_initializer="he_normal"))
model.add(Dense(1024, activation="elu", kernel_initializer="he_normal"))
model.add(Dense(512, activation="elu", kernel_initializer="he_normal"))
model.add(keras.layers.Dropout(0.3))

model.add(Dense(512, activation="elu", kernel_initializer="he_normal"))
model.add(Dense(1024, activation="elu", kernel_initializer="he_normal"))
model.add(Dense(512, activation="elu", kernel_initializer="he_normal"))
model.add(keras.layers.Dropout(0.3))

model.add(Dense(128, activation="elu", kernel_initializer="he_normal"))
model.add(Dense(64, activation="elu", kernel_initializer="he_normal"))
model.add(Dense(32, activation="elu", kernel_initializer="he_normal"))
model.add(keras.layers.Dropout(0.3))

model.add(Dense(1, activation="sigmoid"))
model.compile(optimizer="SGD", loss='binary_crossentropy', metrics=["binary_accuracy"])


# In[ ]:


model.summary()


# In[ ]:


# keras.backend.reset_uids()


# In[ ]:


model_result = model.fit(dfX, dfY, batch_size=100, epochs=200, validation_split=0.2, shuffle=True, verbose=2)


# ## Result

# In[ ]:


plt.figure(figsize=(30, 10))

plt.subplot(1, 2, 1)
plt.plot(model_result.history["loss"], label="training")
plt.plot(model_result.history["val_loss"], label="validation")
plt.axhline(0.55, c="red", linestyle="--")
plt.axhline(0.35, c="yellow", linestyle="--")
plt.axhline(0.15, c="green", linestyle="--")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(model_result.history["binary_accuracy"], label="training")
plt.plot(model_result.history["val_binary_accuracy"], label="validation")
plt.axhline(0.75, c="red", linestyle="--")
plt.axhline(0.80, c="green", linestyle="--")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.show()


# In[ ]:


#y_predict = model.predict_classes(X_test.values)


# In[ ]:


#print(classification_report(y_test, y_predict))


# ---

# ## 3. Predict_OUTPUT

# In[ ]:


test = pd.read_csv("../input/test.csv")
test.head()


# In[ ]:


# Log Fare
# for idx, value in enumerate(test.Fare):
#     if value != 0:
#         test.loc[idx, "Fare"] =  np.round(np.log10(value), 2)
# test.Fare = np.log10((test.Fare + 1 - test.Fare.min())/test.Fare.max()) +1.5
# for i in range(len(test.Fare)):
#     test.loc[i, "nor_Fare"] = (test.Fare[i]-np.mean(test.Fare))/np.std(test.Fare)

# # fare
# #for i in range(len(test.Fare)):
# #    test.loc[i, "nor_Fare"] = np.log10(np.abs((test.Fare[i]+0.1-np.mean(test.Fare)))/np.std(test.Fare))
# #test.Fare = test.nor_Fare

# #test.nor_Fare = (test.Fare - np.mean(test.Fare)) / test.std(df.Fare)
# #test.Fare = test.nor_Fare

# # for i in np.unique(test.Pclass):
# #     test.loc[test.Pclass == i, "nor_Fare"] = (test[test.Pclass == i]["Fare"] - np.mean(test[test.Pclass == i]["Fare"])) / np.std(test[test.Pclass == i]["Fare"])

# for i in np.unique(test.Pclass):
#     test.loc[test.Pclass == i, "nor_Fare"] = (test.loc[test.Pclass == i, "Fare"] - np.min(test.loc[test.Pclass == i, "Fare"])) / (np.max(test.loc[test.Pclass == i, "Fare"]) - np.min(test.loc[test.Pclass == i, "Fare"]))
# test.Fare = test.nor_Fare
# test.head()


# In[ ]:


np.mean(df.Fare), mean_fare


# In[ ]:


test.loc[test.Fare == 0, "Fare"] = mean_fare


# In[ ]:


# Sex Encoding
test["Sex"] = binar.transform(test["Sex"])


# In[ ]:


# # Pclass Encoding
# test_Pclass = pd.DataFrame(OneHotEncoder().fit_transform(np.array(test["Pclass"])[:,np.newaxis]).toarray(), columns=["A_Class", "B_Class", "C_Class"])
# test_Pclass = test_Pclass.astype(int)


# In[ ]:


# Pclass Encoding

test["A_Class"] = 0
test["B_Class"] = 0
test["C_Class"] = 0

test.loc[test.Pclass == 1, "A_Class"] = 1
test.loc[test.Pclass == 2, "B_Class"] = 1
test.loc[test.Pclass == 3, "C_Class"] = 1


# In[ ]:


# Embarked Encoding
test_Embarked = pd.get_dummies(test.Embarked)


# In[ ]:


# Nan Age is filled using average age
#test.loc[:, "Age"].fillna(int(test["Age"].mean()), inplace=True)
#test.loc[:, "Age"].fillna(int(test["Age"].median()), inplace=True)


# In[ ]:


test.groupby(["Sex", "Pclass"]).Age.mean()


# Basically We don't know test dataset's information, so we have to use train dataset's info

# In[ ]:


# Nan Age filled by sex
# test.loc[:, "Age"].fillna(0, inplace=True)

# for idx, value in enumerate(test.Age):
#     if value == 0:
#         if test.Sex[idx] == 1:
#             test.Age[idx] = 30.7
#         else:
#             test.Age[idx] = 28.9


# In[ ]:


# test.loc[(test.Sex == 1) & (test.Age.isna()) & (test.Pclass == 1), "Age"] = 40.5
# test.loc[(test.Sex == 1) & (test.Age.isna()) & (test.Pclass == 2), "Age"] = 30.9
# test.loc[(test.Sex == 1) & (test.Age.isna()) & (test.Pclass == 3), "Age"] = 24.5

# test.loc[(test.Sex == 0) & (test.Age.isna()) & (test.Pclass == 1), "Age"] = 41.3
# test.loc[(test.Sex == 0) & (test.Age.isna()) & (test.Pclass == 2), "Age"] = 24.3
# test.loc[(test.Sex == 0) & (test.Age.isna()) & (test.Pclass == 3), "Age"] = 23.0


# In[ ]:


test.loc[(test.Sex == 0) & (test.Age.isna()) & (test.Pclass == 1), "Age"] = 34.6
test.loc[(test.Sex == 0) & (test.Age.isna()) & (test.Pclass == 2), "Age"] = 28.7
test.loc[(test.Sex == 0) & (test.Age.isna()) & (test.Pclass == 3), "Age"] = 21.7

test.loc[(test.Sex == 1) & (test.Age.isna()) & (test.Pclass == 1), "Age"] = 41.2
test.loc[(test.Sex == 1) & (test.Age.isna()) & (test.Pclass == 2), "Age"] = 30.7
test.loc[(test.Sex == 1) & (test.Age.isna()) & (test.Pclass == 3), "Age"] = 26.5


# In[ ]:


#test.Age = np.log10(test.Age) - np.mean(np.log10(test.Age))


# In[ ]:


# for i in pd.unique(test.Sex):
#     for j in pd.unique(test.Pclass):
#         test.loc[(test.Sex == i) & (test.Pclass == j), "Age"] = (test.loc[(test.Sex == i) & (test.Pclass == j), "Age"] - np.min(test.loc[(test.Sex == i) & (test.Pclass == j), "Age"])) / (np.max(test.loc[(test.Sex == i) & (test.Pclass == j), "Age"]) - np.min(test.loc[(test.Sex == i) & (test.Pclass == j), "Age"]))


# In[ ]:


# Boarding Together or Alone
for i in range(len(test)):
    if test.loc[i, "SibSp"] + test.loc[i, "Parch"] == 0:
        test.loc[i, "Alone"] = 1
    else:
        test.loc[i, "Alone"] = 0

test.Alone = test.Alone.astype(int)


# In[ ]:


test_new = pd.concat([test, test_Embarked], axis=1)
test_new.head()


# In[ ]:


testX = test_new[feature_name]


# In[ ]:


testX = scaler.transform(testX)


# In[ ]:


testX = pd.DataFrame(testX, columns=feature_name)
testX.head()


# In[ ]:


predict = model.predict_classes(testX)


# In[ ]:


predict = list(chain.from_iterable(predict))


# In[ ]:


my_submission = pd.DataFrame({'PassengerId': test.PassengerId, 'Survived': predict})
my_submission.to_csv('submission.csv', index=False)


# -End of Analysis <br>
# R.I.P

# In[ ]:




