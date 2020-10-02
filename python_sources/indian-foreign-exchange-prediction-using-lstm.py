#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

sns.set_style("darkgrid")


# ## Data Preprocessing

# In[ ]:


df = pd.read_csv("/kaggle/input/foreign-exchange-rates-per-dollar-20002019/Foreign_Exchange_Rates.csv")

df = df.drop(columns=["Unnamed: 0"])
newColumnsNames = list(map(lambda c: c.split(" - ")[0] if "-" in c else "DATE", df.columns))
newColumnsNames
df.columns = newColumnsNames


# In[ ]:


# Fill ND values with previous and next values

df = df.replace("ND", np.nan)
df = df.bfill().ffill() 

# Make date wise indexing 

df = df.set_index("DATE")
df.index = pd.to_datetime(df.index)
df = df.astype(float)


# In[ ]:


print("Total number of records", len(df))
print("Total number of days between {} and {} are {}".format(df.index.min().date(), df.index.max().date(), (df.index.max() - df.index.min()).days+1))


# ### Interpolate missing data

# In[ ]:


# Prepare a full dataframe
num_records = 7303
data = {}
data["DATE"] = pd.date_range("2000-01-03", "2019-12-31", freq="D")

complete = pd.DataFrame(data=data)
complete = complete.set_index("DATE")
complete = complete.merge(df, left_index=True, right_index=True, how="left")
complete = complete.bfill().ffill()


# In[ ]:


complete.head()


# ### Compare initial records with complete records

# In[ ]:


toInspect = ["INDIA", "CHINA", "EURO AREA"]
rows, cols = 3, 2
fig, ax = plt.subplots(rows, cols, figsize=(20,rows*5))

for row in range(rows):
    sns.lineplot(data=df[[toInspect[row]]], ax=ax[row][0])
    sns.lineplot(data=complete[[toInspect[row]]], ax=ax[row][1])


# So far so good, we have created a full series data which is almost same as original one. 
# 
# 
# #### Why we created a complete time series data ?
# 
# 1. It enables us to resample the data, and now we can try to see seasonality pattern(In any) in the data on different time scale.
# 2. Resampling data on a larger scale will reduce the amount of error induced by inputing values using `bfill and ffill`
# 3. We can create different models on different sampled data and compare their accuracy

# ## Now Lets create a Task
# 
# ### We want to predict stock exchange value of INR (INDIAN curreny) 
# 1. Using only values of Indian stock (Univariate)
# 2. Using other countries stock values as well (Multivariate)

# In[ ]:


sampled2d = complete.resample("2D").mean()


# Before proceding further we need to convert the data into a proper time steps data from which a ML model can learn something(A pattern or seasonality)
# 
# For example: If we keep a time window of 3 steps, then data A will be converted to X and Y
# 
# `A = [1, 2, 3, 4, 5, 6, 7, 8]`
# 
# 
# `X = [[1, 2, 3],
#      [2, 3, 4],
#      [3, 4, 5],
#      [4, 5, 6],
#      [5, 6, 7]]`
#      
#      
# `Y = [4,
#       5,
#       6,
#       7,
#       8]`
# 
# `
# X.shape = (5, 3)
# Y.shape = (5,)`

# In[ ]:


# Data Conversion Utility

def getTimeSeriesData(A, window=7):
    X, y = list(), list()
    for i in range(len(A)):
        end_ix = i + window
        if end_ix > len(A) - 1:
            break
        seq_x, seq_y = A[i:end_ix], A[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


# In[ ]:


window = 2
num_features = 1

X, y = getTimeSeriesData(list(sampled2d["INDIA"]), window=window)
print("X:", X.shape)
print("Y:", y.shape)

# We need to add one more dimension to X, i.e Num of features in 1 sample of time step. as we are doing a univariate prediction which means number of features are 1 only
X = X.reshape((X.shape[0], X.shape[1], num_features))  # For LSTM
print("-----------")
print("X:", X.shape)
print("Y:", y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print("-----------")
print("X train:", X_train.shape)
print("y train:", y_train.shape)
print("X test:", X_test.shape)
print("y test:", y_test.shape)


# In[ ]:


# Define Model
model = Sequential()
model.add(LSTM(7, activation='relu', input_shape=(window, num_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
history = model.fit(X_train, y_train, epochs=5, verbose=1)


# In[ ]:


plt.plot(history.history["loss"])
# plt.plot(history.history["val_loss"])
plt.title("Model Loss")
plt.ylabel('Loss')
plt.xlabel('epoch')
plt.legend(['train'], loc='upper left')
plt.show()


# In[ ]:


yPred = model.predict(X_test, verbose=0)
yPred.shape = yPred.shape[0]


# ### Lets see how well we did it

# In[ ]:


plt.figure(figsize=(30,5))
sns.set(rc={"lines.linewidth": 8})
sns.lineplot(x=np.arange(y_test.shape[0]), y=y_test, color="green")
sns.set(rc={"lines.linewidth": 3})
sns.lineplot(x=np.arange(y_test.shape[0]), y=yPred, color="coral")
plt.margins(x=0, y=0.5)
plt.legend(["Original", "Predicted"])


# ##### lets zoom it a bit

# In[ ]:


points = 200
plt.figure(figsize=(30,5))
sns.set(rc={"lines.linewidth": 8})
sns.lineplot(x=np.arange(points), y=y_test[:points], color="green")
sns.set(rc={"lines.linewidth": 3})
sns.lineplot(x=np.arange(points), y=yPred[:points], color="coral")
plt.margins(x=0, y=0.5)
plt.legend(["Original", "Predicted"])


# ### Well its working pretty great in univariate itself in just 5 epochs
# 
# ## Please upvote if you Like
# 

# In[ ]:




