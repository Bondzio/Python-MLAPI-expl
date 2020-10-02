#!/usr/bin/env python
# coding: utf-8

# In[17]:


# This notebook is used to calculate the baseline for measuring how accurate your predictions are.
# It measures in 2 ways. 1) RMSE 2) Correct Trend Prediction Percentage


# In[18]:


# Import library
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas as pd
# load dataset
def parser(x):
	return datetime.strptime(x, '%Y-%m-%d')
series = read_csv('../input/corn2013-2017.txt', header=None, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
# scale up 100 for easy reading
series = series*100
# check the head and tail rows
print(series.head())
print(series.tail())
# line plot
series.plot()
pyplot.show()


# In[19]:


# Calculate baseline (RMSE, Correct Trend Predictions) for the predictions by shifting the predicted as the last observed price
# split data into train and test
X = series.values
train, test = X[0:-12], X[-12:]
# walk-forward validation, this get the baseline prediction base on the last observed price
history = [x for x in train]
predictions = list()
nb_correct_predict = 0
for i in range(len(test)):
    # get the history last row as predictions
    predictions.append(history[-1])
    # append the test set to the history
    history.append(test[i])
    # expected price
    expected = history[-1]
    #predicted price
    yhat = predictions[-1]
    #calculate number of correct trend predictions
    if i != 0:
        if (expected > old_expected) and (yhat > old_yhat):
            nb_correct_predict = nb_correct_predict+1
        elif (expected < old_expected) and (yhat < old_yhat):
            nb_correct_predict = nb_correct_predict+1
        elif (expected == old_expected) and (yhat == old_yhat):
            nb_correct_predict = nb_correct_predict+1
    print('Date=%s, Predicted=%.2f, Expected=%.2f' % (series.index[-12+i], yhat, expected))
    old_yhat = yhat
    old_expected = expected
# calculate rmse
rmse = sqrt(mean_squared_error(test, predictions))
print('RMSE: %.3f' % rmse)
# print correct number of trend predictions
p_correct_predict = nb_correct_predict/(len(test)-1) * 100
print('Number of correct trend predictions: %d, percentage: %.1f' % (nb_correct_predict, p_correct_predict))
# line plot of observed vs predicted
pyplot.plot(test, label = 'Expected Value')
pyplot.plot(predictions, label = 'Predicted Value')
pyplot.legend()
pyplot.show()


# In[22]:


# So you can use RMSE = 6.466, Correct Trend Predictions = 54.5% 
# as a comparison to your prediction algorithms to see how it works better or worse:)


# In[ ]:




