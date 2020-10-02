#!/usr/bin/env python
# coding: utf-8

# ## Setup
# 
# This code loads all the libraries that we will need, and also lists the input files that we have available to us.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns # for making graphs
import os

from sklearn.model_selection import train_test_split

for dirname, _, filenames in os.walk('/kaggle/input/titanic'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# ## Read training data file into a dataframe

# In[ ]:


train_df = pd.read_csv("../input/titanic/train.csv")
train_df.head()


# ## Explore the data

# In[ ]:


sns.distplot(train_df[(train_df["Survived"]==0) & (train_df["Age"].isna() == False)].Age, bins=17, kde=False)
sns.distplot(train_df[(train_df["Survived"]==1) & (train_df["Age"].isna() == False)].Age, bins=17, kde=False)


# ## Estimate missing passenger ages
# 
# A number of the passengers do not have recorded ages. We are going to fill in those missing ages with the average (mean) age for every passenger!
# 
# As we are also going to have to fill in any missing ages in the test dataset (when we make our predictions for submission), we will create a function so that we can just write the code once.

# In[ ]:


def transform_data(df_in):
    df_out = df_in.copy()
    df_out["age_imputed"] = df_out.Age
    df_out["age_imputed"].fillna(value=df_out.Age.mean(), inplace=True)
    return df_out


# If we apply this function to our training data, `train_df`, we see that the 177 missing values in the Age column get replaced.

# In[ ]:


train_filled = transform_data(train_df)

print(sum(train_filled.Age.isna()))
print(sum(train_filled.age_imputed.isna()))


# ## Build a model
# 
# We are going to use logistic regression using the `glm` function.

# In[ ]:





# In[ ]:


from sklearn.linear_model import LogisticRegression

logmodel = LogisticRegression()
logmodel.fit(np.array(train_filled.age_imputed).reshape(-1,1),train_filled.Survived)


# ## Make predictions

# In[ ]:


test_df = pd.read_csv("../input/titanic/test.csv")
test_df.head()


# In[ ]:


test_filled = transform_data(test_df)
predictions = logmodel.predict(np.array(test_filled.age_imputed).reshape(-1,1))


# In[ ]:


predictions


# In[ ]:


submission = pd.DataFrame(test_filled.PassengerId)
submission["Survived"] = predictions
submission.to_csv("submission.csv", index=False)

