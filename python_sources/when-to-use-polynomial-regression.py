#!/usr/bin/env python
# coding: utf-8

# # When to use Polynomial Regression?
# 
# In this notebook, we will compare linear regression model(degree=1) to polynomial regression models(degree=2,3) on the **electricity consumption** dataset, to understand when to use polynomial regression. The dataset contains two variables - year and electricity consumption. We will also decide untill what extent we can increase the degree of polynomial regression without overfitting.

# In[ ]:


#importing libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn import metrics


# In[ ]:


#fetching data
elec_cons = pd.read_csv("../input/us-yearly-electricity-consumption/total-electricity-consumption-us.csv",  sep = ',', header= 0 )
elec_cons.head()


# In[ ]:


# number of observations: 51
elec_cons.shape


# In[ ]:


# checking NA
# there are no missing values in the dataset
elec_cons.isnull().values.any()


# In[ ]:


size = len(elec_cons.index)
index = range(0, size, 5)

train = elec_cons[~elec_cons.index.isin(index)]
test = elec_cons[elec_cons.index.isin(index)]


# In[ ]:


print(len(train))
print(len(test))


# In[ ]:


# converting X to a two dimensional array, as required by the learning algorithm
X_train = train.Year.values.reshape(-1,1) #Making X two dimensional
y_train = train.Consumption

X_test = test.Year.values.reshape(-1,1) #Making X two dimensional
y_test = test.Consumption


# In[ ]:


# Doing a polynomial regression: Comparing linear, quadratic and cubic fits
# Pipeline helps you associate two models or objects to be built sequentially with each other, 
# in this case, the objects are PolynomialFeatures() and LinearRegression()

r2_train = []
r2_test = []
degrees = [1, 2, 3]

for degree in degrees:
    pipeline = Pipeline([('poly_features', PolynomialFeatures(degree=degree)),
                     ('model', LinearRegression())])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    r2_test.append(metrics.r2_score(y_test, y_pred))
    
    # training performance
    y_pred_train = pipeline.predict(X_train)
    r2_train.append(metrics.r2_score(y_train, y_pred_train))
    
# plot predictions and actual values against year
    fig, ax = plt.subplots()
    ax.set_xlabel("Year")                                
    ax.set_ylabel("Power consumption")
    ax.set_title("Degree= " + str(degree))
    
    # train data in blue
    ax.scatter(X_train, y_train)
    ax.plot(X_train, y_pred_train)
    
    # test data in orange
    ax.scatter(X_test, y_test)
    ax.plot(X_test, y_pred)
    plt.show()    
    
# plot errors vs y
    fig, ax = plt.subplots()
    ax.set_xlabel("y_test")                                
    ax.set_ylabel("error")
    ax.set_title("Degree= " + str(degree))
    
    ax.scatter(y_test,y_test-y_pred)
    ax.plot(y_test,y_test-y_test)
    plt.show()
    


# Looking at the distribution of errors for degree 1 we can say that the errors are following a certain pattern, implying there is a trend in the data that liner model could not capture. As we increase the degree of the regression we see that the errors decrease in magnitude and go random in distribution implying a positive result for increasing the degree of regression. Further increase in degree will result in overfitting as we already captured the trends in the data, which is why we have the errors so random.

# It is a common misconception of the neophytes that polynomial regression always overfits, but given a right approach it is a powerful tool to in your arsenal.

# In[ ]:


# respective train and test r-squared scores of predictions
print(degrees)
print(r2_train)
print(r2_test)

