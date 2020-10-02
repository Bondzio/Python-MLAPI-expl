#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Author : JEEVA T
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle


# In[ ]:


data=pd.read_csv("/content/500092.csv")


# In[ ]:


data.columns


# In[ ]:


len(data)


# In[ ]:



training_set = data.iloc[0:3935, 1:2].values
test_set=data.iloc[3935:,1:2].values


# In[ ]:



from matplotlib import pyplot
data.plot()
pyplot.show()


# In[ ]:




price=pd.DataFrame()
price['Date']=data['Date']
price['Open Price']=data['Open Price']


# In[ ]:



price.plot()
pyplot.show()


# In[ ]:



diet = price[['Open Price']]
diet.rolling(12).mean().plot()
plt.xlabel('Year', fontsize=20);


# In[ ]:



price.plot(style='k.')
pyplot.show()


# In[ ]:



price.hist()
pyplot.show()


# In[ ]:



price.plot(kind='kde')
pyplot.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:



training_set = data.iloc[0:3935, 1:2].values
test_set=data.iloc[3935:,1:2].values


# In[ ]:


training_set


# In[ ]:


test_set


# In[ ]:



from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)


# In[ ]:



X_train = []
y_train = []
for i in range(200, 3935):
    X_train.append(training_set_scaled[i-200:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)


# In[ ]:



X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))


# In[ ]:



from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


# In[ ]:





# In[ ]:



regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50,activation='relu', return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50,activation='relu', return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50,activation='relu', return_sequences = True))
#regressor.add(Dropout(0.2))

# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

# Adding the output layer
regressor.add(Dense(units = 1))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
#Long Training use 53 epoch because after that the loss is having lesser difference
regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)


# In[ ]:



path= "./jeeva.pkl"
with open(path, 'wb') as f:
        pickle.dump(regressor, f)
        print("Done Pickiling")
        #print("Pickled clf at {}".format(path))


# In[ ]:



with open("jeeva.pkl", 'rb') as f:
            regressor = pickle.load(f)
  


# In[ ]:


data.columns


# In[ ]:


len(data)


# In[ ]:



data_total = data['Open Price']
inputs = data_total[4135 - 400:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)


# In[ ]:



X_test = []
for i in range(200, len(inputs)):
    X_test.append(inputs[i-200:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)


# In[ ]:



plt.plot(test_set, color = 'red', label = 'Real Company Prices')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted company Price')
plt.title('Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()


# In[ ]:



from sklearn import metrics

#MAE
print(metrics.mean_absolute_error(test_set,predicted_stock_price))
#MSE
print(metrics.mean_squared_error(test_set,predicted_stock_price))
#RMSE Value
print(np.sqrt(((predicted_stock_price - test_set) ** 2).mean()))


# In[ ]:



print(min(test_set),max(test_set))
rmse=np.sqrt(((predicted_stock_price - test_set) ** 2).mean())
acc=(rmse-2)/(505749-2)
#Accuracy
print(1-acc)


# In[ ]:


#from sklearn.metrics import r2_score
#print(r2_score())


# In[ ]:



df=pd.DataFrame()
df["Predicted_Price"]=predicted_stock_price
df.to_csv("prediction_of_stock_price.csv")


# In[ ]:




