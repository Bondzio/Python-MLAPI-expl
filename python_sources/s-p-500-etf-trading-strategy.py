#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sb
import pandas_datareader.data as web
from pandas_datareader import data
from datetime import datetime
from pprint import pprint
import datetime
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings("ignore")
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# #STEP 1: Data Preprocessing

# In[ ]:


spy = pd.read_csv('/kaggle/input/spy-trading/data/SPY.csv')
spy


# In[ ]:


spx = pd.read_csv('/kaggle/input/spy-trading/data/^GSPC.csv')
dji = pd.read_csv('/kaggle/input/spy-trading/data/^DJI.csv')
ixic = pd.read_csv('/kaggle/input/spy-trading/data/^IXIC.csv')


# In[ ]:


indice = pd.DataFrame(index = spy.index)


# In[ ]:


indice['spy'] = spy['Open'].shift(-1) - spy['Open']
indice['spy_lag1'] = indice['spy'].shift(1)
indice['ixic'] = ixic['Open'] - ixic['Open'].shift(1)
indice['spx'] = spx["Open"] - spx['Open'].shift(1)
indice['dji'] = dji['Open'] - dji['Open'].shift(1)
indice['Price'] = spy['Open']


# In[ ]:


indice.head()


# In[ ]:


indice.isnull().sum()


# In[ ]:


indice = indice.fillna(method = 'ffill')
indice = indice.dropna()


# In[ ]:


indice.isnull().sum()


# In[ ]:


indice.to_csv('indice.csv',index=False)


# In[ ]:


print(indice.shape)


# #STEP 2: Split Dataset

# In[ ]:


Train = indice.iloc[-6820:-3410, :]
Test = indice.iloc[-3410:, :]
print(Train.shape, Test.shape)


# #STEP 3: Explore Dataset

# In[ ]:


from pandas.plotting import scatter_matrix
sm = scatter_matrix(Train, figsize=(12, 12))


# In[ ]:


sb.pairplot(Train, diag_kind="kde", height=3, aspect=0.6)


# #STEP 4: Check the Correlation

# In[ ]:


corr_data = Train.iloc[:, :-1].corr()
corr_data.style.background_gradient(cmap='coolwarm', axis=None)


# In[ ]:


Train


# In[ ]:


corr_array = Train.iloc[:, :-1].corr()['spy']
print(corr_array)


# In[ ]:


import statsmodels.formula.api as smf
formula = 'spy ~ spy_lag1 + ixic + spx + dji'
lm = smf.ols(formula=formula, data=Train).fit()
lm.summary()


# #STEP 5: Make Prediction

# In[ ]:


Train['PredictedY'] = lm.predict(Train)
Test['PredictedY'] = lm.predict(Test)


# In[ ]:


Train


# In[ ]:


plt.xlabel('spy')
plt.ylabel('PredictedY')
plt.scatter(Train['spy'], Train['PredictedY'])


# #STEP 6: Statictical Evalution

# In[ ]:


def adjustedMetric(data, model, model_k, yname):
    data['yhat'] = model.predict(data)
    SST = ((data[yname] - data[yname].mean())**2).sum()
    SSR = ((data['yhat'] - data[yname].mean())**2).sum()
    SSE = ((data[yname] - data['yhat'])**2).sum()
    r2 = SSR/SST
    adjustR2 = 1 - (1-r2)*(data.shape[0] - 1)/(data.shape[0] -model_k -1)
    RMSE = (SSE/(data.shape[0] -model_k -1))**0.5
    return adjustR2, RMSE
def assessTable(test, train, model, model_k, yname):
    r2test, RMSEtest = adjustedMetric(test, model, model_k, yname)
    r2train, RMSEtrain = adjustedMetric(train, model, model_k, yname)
    assessment = pd.DataFrame(index=['R2', 'RMSE'], columns=['Train', 'Test'])
    assessment['Train'] = [r2train, RMSEtrain]
    assessment['Test'] = [r2test, RMSEtest]
    return assessment


# In[ ]:


assessTable(Test, Train, lm, 4, 'spy')


# In[ ]:


print('Adjusted R2 and RMSE on Train:', adjustedMetric(Train, lm, 4, 'spy'))
print('Adjusted R2 and RMSE on Test:', adjustedMetric(Test, lm, 4, 'spy'))


# In[ ]:


indice.head()


# #STEP 7: Profit of Signal Based Strategy

# In[ ]:


Train['Order'] = [1 if sig>0 else -1 for sig in Train['PredictedY']]
Train['Profit'] = Train['spy'] * Train['Order']

Train['Wealth'] = Train['Profit'].cumsum()
print('Total profit made in Train: ', Train['Profit'].sum())


# In[ ]:


plt.figure(figsize=(12, 12))
plt.title('Performance of Strategy in Train')
plt.plot(Train['Wealth'].values, color='green', label='Signal based strategy')
plt.plot(Train['spy'].cumsum().values, color='red', label='Buy and Hold strategy')
plt.legend()
plt.show()


# In[ ]:


Test['Order'] = [1 if sig>0 else -1 for sig in Test['PredictedY']]
Test['Profit'] = Test['spy'] * Test['Order']

Test['Wealth'] = Test['Profit'].cumsum()
print('Total profit made in Test: ', Test['Profit'].sum())


# In[ ]:


plt.figure(figsize=(12, 12))
plt.title('Performance of Strategy in Train')
plt.plot(Test['Wealth'].values, color='green', label='Signal based strategy')
plt.plot(Test['spy'].cumsum().values, color='red', label='Buy and Hold strategy')
plt.legend()
plt.show()


# #STEP 8: Practical Evaluation

# In[ ]:


Train['Wealth'] = Train['Wealth'] + Train.loc[Train.index[0], 'Price']
Test['Wealth'] = Test['Wealth'] + Test.loc[Test.index[0], 'Price']


# In[ ]:


Train['Return'] = np.log(Train['Wealth']) - np.log(Train['Wealth'].shift(1))
dailyr = Train['Return'].dropna()

print('Daily Sharpe Ratio for training data is ', dailyr.mean()/dailyr.std(ddof=1))
print('Yearly Sharpe Ratio for training data is ', (252**0.5)*dailyr.mean()/dailyr.std(ddof=1))


# In[ ]:


Test['Return'] = np.log(Test['Wealth']) - np.log(Test['Wealth'].shift(1))
dailyr = Test['Return'].dropna()

print('Daily Sharpe Ratio for testing data is ', dailyr.mean()/dailyr.std(ddof=1))
print('Yearly Sharpe Ratio for testing data is ', (252**0.5)*dailyr.mean()/dailyr.std(ddof=1))


# In[ ]:


Train['Peak'] = Train['Wealth'].cummax()
Train['Drawdown'] = (Train['Peak'] - Train['Wealth'])/Train['Peak']
print('Maximum Drawdown in Train is ', Train['Drawdown'].max())


# In[ ]:


Test['Peak'] = Test['Wealth'].cummax()
Test['Drawdown'] = (Test['Peak'] - Test['Wealth'])/Test['Peak']
print('Maximum Drawdown in Test is ', Test['Drawdown'].max())

