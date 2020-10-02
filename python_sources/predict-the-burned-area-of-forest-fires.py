#!/usr/bin/env python
# coding: utf-8

# Predict the burned area of forest fires, in the northeast region of Portugal, by using meteorological and other data. Data Analysis, Data visualization, Feature Selection, about 10 Machine Learning models/estimators. Multilayer Perceptron(Deep Learning/Artificial Neural Network). Cross validation is used order to avoid overfitting.

# In[ ]:


import numpy
import pandas

from sklearn.feature_selection import RFE
from sklearn.ensemble import ExtraTreesRegressor


import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix


from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error



from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
from keras.constraints import maxnorm
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)


# In[ ]:


# load dataset
dataframe = pandas.read_csv(r"../input/forestfires.csv")



# Encode Data
dataframe.month.replace(('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'),(1,2,3,4,5,6,7,8,9,10,11,12), inplace=True)
dataframe.day.replace(('mon','tue','wed','thu','fri','sat','sun'),(1,2,3,4,5,6,7), inplace=True)


# In[ ]:


print("Head:", dataframe.head())


# In[ ]:



print("Statistical Description:", dataframe.describe())


# In[ ]:



print("Shape:", dataframe.shape)


# In[ ]:



print("Data Types:", dataframe.dtypes)


# In[ ]:



print("Correlation:", dataframe.corr(method='pearson'))


# 'temp' has the highest correlation with the area of forest fire(which is a positive correlation), followed by 'RH'
#  also a positive correlation, 'Rain' has the least correlation 

# In[ ]:


dataset = dataframe.values


X = dataset[:,0:12]
Y = dataset[:,12]


# In[ ]:


#Feature Selection
model = ExtraTreesRegressor()
rfe = RFE(model, 3)
fit = rfe.fit(X, Y)

print("Number of Features: ", fit.n_features_)
print("Selected Features: ", fit.support_)
print("Feature Ranking: ", fit.ranking_) 


# 'Wind', 'RH' and 'DMC' were top 3 selected features/feature combination for predicting 'Area'
#  using Recursive Feature Elimination, the 2nd selected feature was atually one of the attributes with the highest correlation with the 
#  'Area'
# 

# In[ ]:


plt.hist((dataframe.area))


# Most of the dataset's samples fall between 0 and 200 of 'Area' output class, with majority being less than 100

# In[ ]:


dataframe.hist()


# 'Temp' has a near Guassian Distribution. 
# There are a mixture of positive skews and negative skews among the other attributes

# In[ ]:


dataframe.plot(kind='density', subplots=True, layout=(4,4), sharex=False, sharey=False)


# In[ ]:



dataframe.plot(kind='box', subplots=True, layout=(4,4), sharex=False, sharey=False)


# In[ ]:


scatter_matrix(dataframe)


# In[ ]:


fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(dataframe.corr(), vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = numpy.arange(0,13,1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(dataframe.columns)
ax.set_yticklabels(dataframe.columns)


# 'cement' has the highest positive corelation as expected

# In[ ]:


num_instances = len(X)

models = []
models.append(('LiR', LinearRegression()))
models.append(('Ridge', Ridge()))
models.append(('Lasso', Lasso()))
models.append(('ElasticNet', ElasticNet()))
models.append(('Bag_Re', BaggingRegressor()))
models.append(('RandomForest', RandomForestRegressor()))
models.append(('ExtraTreesRegressor', ExtraTreesRegressor()))
models.append(('KNN', KNeighborsRegressor()))
models.append(('CART', DecisionTreeRegressor()))
models.append(('SVM', SVR()))

# Evaluations
results = []
names = []
scoring = []

for name, model in models:
    # Fit the model
    model.fit(X, Y)
    
    predictions = model.predict(X)
    
    # Evaluate the model
    score = explained_variance_score(Y, predictions)
    mae = mean_absolute_error(predictions, Y)
    # print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    results.append(mae)
    names.append(name)
    
    msg = "%s: %f (%f)" % (name, score, mae)
    print(msg)


# 'ExtraTreesRegressor' and 'DecisionTreeRegressor' are the best estimators/models for this dataset, followed by 'BaggingRegressor', ey can be further explored and their hyperparameters tuned

# In[ ]:


Y = numpy.array(Y).reshape((len(Y), 1))
#Y.reshape(-1, 1)

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
Y = scaler.fit_transform(Y)


# In[ ]:


# define base model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(12, input_dim=12, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    
    # compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# evaluate model with standardized dataset
estimator = KerasRegressor(build_fn=baseline_model, nb_epoch=600, batch_size=5, verbose=0)

kfold = KFold(n_splits=30, random_state=seed)
results = cross_val_score(estimator, X, Y, cv=kfold)
print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))


# ANN/MLP Score: 99% 

# In[ ]:




