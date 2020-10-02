#!/usr/bin/env python
# coding: utf-8

# For logistic regression on heart disease:
# <br><br> First step is to load dataset as utf-8:
# <br><br> Second step is to check the information of dataset such as columns and distribution of data in the dataset
# <br><br> Third step which is very important step to select features, feature plays very important step. If properly features are not selected then model performance is affected.
# <br><br>  Fourth step to train the model with dataset
# <br><br>  Fifth step predict values and generate accuracy and confusion metrics.
# 

# In[ ]:


#importing libraries:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


# In[ ]:


# First step loading dataset in dataframe:
df=pd.read_csv("../input/heart.csv",encoding = "utf-8")
df.head()


# In[ ]:


# Second step check dataset information:
df.info()


# In[ ]:


df.describe()


# In[ ]:


# to check whether dataset column has any null values
# graph method is quick method to check 
# null values will be shown in yellow if any exists, so with the help this we can quickly check the null values

sns.heatmap(df.isnull(),yticklabels=False,cmap="viridis")

#below graph shows there is no null in the dataset


# In[ ]:


#third step feature selection, although there are three methods for selecting fetaures, 
# here i am demostrating simple method using correlation in the dataframe.
# to visualize the correlation, heatmap of sns library is used and three colors are specified Red,Yellow and green
# for better visualisation.

plt.figure(figsize=(20,20))

sns.heatmap(df.corr(),annot=True,cmap="RdYlGn")

# in below graph we observed that with target the lowest correlation is of column chol and fbs
# chol means cholestrol
# fbs means fasting blood sugar
# so in heart disease chol has significance where as fbs does not have any role hence we can exclude the column fbs 
# from features and train the model excluding this column


# In[ ]:


#checking distribution of the target values
sns.distplot(df['target'])


# In[ ]:


# Step fourth training dataset with excluding features "fbs" and checking accuracy

lgC=LogisticRegression()

#droping feature fbs
df_features=df.drop("target",axis=1)
df_features=df_features.drop("fbs",axis=1)
df_label=df['target']
#training set and test set
X_train_new, X_test_new, y_train_new, y_test_new = train_test_split(df_features, df_label, test_size=0.2, random_state=42)

# training the model
lgC.fit(X_train_new,y_train_new)

# making predictions
predictions_new=lgC.predict(X_test_new)


print("Accuracy of the model excluding fbs column {:.2f}%".format(lgC.score(X_test_new,y_test_new)*100))


# In[ ]:


# looking for confussion matrix,false positive and false negative 
cnf=confusion_matrix(y_test_new,predictions_new)
sns.heatmap(cnf,annot=True)


# Conclusion:
# Accuracy of the model can be improved based on the feature selection.
# 
# 
# If you find this helpful then vote and share your thoughts on it.
