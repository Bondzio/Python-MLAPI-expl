#!/usr/bin/env python
# coding: utf-8

# **[Machine Learning Explainability Home Page](https://www.kaggle.com/learn/machine-learning-explainability)**
# 
# ---
# 

# ## Load Data

# In[ ]:


import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


# Data manipulation code below here
data = pd.read_csv('../input/new-york-city-taxi-fare-prediction/train.csv', nrows=50000)

# Remove data with extreme outlier coordinates or negative fares
data = data.query('pickup_latitude > 40.7 and pickup_latitude < 40.8 and ' +
                  'dropoff_latitude > 40.7 and dropoff_latitude < 40.8 and ' +
                  'pickup_longitude > -74 and pickup_longitude < -73.9 and ' +
                  'dropoff_longitude > -74 and dropoff_longitude < -73.9 and ' +
                  'fare_amount > 0'
                  )

y = data.fare_amount

base_features = ['pickup_longitude',
                 'pickup_latitude',
                 'dropoff_longitude',
                 'dropoff_latitude']

X = data[base_features]


train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)
first_model = RandomForestRegressor(n_estimators=30, random_state=1).fit(train_X, train_y)
print("Data sample:")
data.head()


# ## Here is the code to plot the partial dependence plot by **pdpbox**

# In[ ]:


from matplotlib import pyplot as plt
from pdpbox import pdp, get_dataset, info_plots


# In[ ]:


for feat_name in base_features:
    pdp_dist = pdp.pdp_isolate(model=first_model, dataset=val_X, model_features=base_features, feature=feat_name)
    pdp.pdp_plot(pdp_dist, feat_name)
    plt.show()


# ## Here is the code to plot the partial dependence plot by **sklearn**

# In[ ]:


from sklearn.inspection import plot_partial_dependence, partial_dependence


# In[ ]:


for i in range(4):
    plot_partial_dependence(first_model, val_X, [i], base_features)


# I used both sklearn.plotpartialdependence and pdpbox.pdp.pdp_plot.
# It looks the outcome graphs are pretty different.
# 
# I assume they are using diffident algorithms. Could someone tell me why they are different and which to use upon the scenarios?
