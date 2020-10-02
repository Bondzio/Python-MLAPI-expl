#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:


df = pd.read_csv('../input/sites-information-data-from-alexacom-dataset/alexa.com_site_info.csv')


# In[ ]:


prediction_columns = ['all_topics_buyer_keywords_Avg_traffic_parameter_1', 'all_topics_buyer_keywords_Avg_traffic_parameter_2'
                   , 'all_topics_buyer_keywords_Avg_traffic_parameter_3', 'all_topics_buyer_keywords_Avg_traffic_parameter_4']
training_columns = ['all_topics_keyword_gaps_Avg_traffic_parameter_1', 'all_topics_keyword_gaps_Avg_traffic_parameter_2',
                   'all_topics_keyword_gaps_Avg_traffic_parameter_3', 'all_topics_keyword_gaps_Avg_traffic_parameter_4',
                   'keyword_opportunities_breakdown_keyword_gaps', 'keyword_opportunities_breakdown_easy_to_rank_keywords']


# In[ ]:


train_size = 1500


# In[ ]:


df = df.dropna()


# In[ ]:


X_train = df[training_columns][:train_size]
Y_train = df[prediction_columns][:train_size]
X_test = df[training_columns][train_size:]
Y_test = df[prediction_columns][train_size:]


# In[ ]:


model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(units=len(training_columns), activation='relu', input_shape=(len(training_columns),)))
model.add(tf.keras.layers.Dropout(0.1))
model.add(tf.keras.layers.Dense(units=len(prediction_columns)))
model.compile(optimizer='adam', loss='MSE')
model.summary()


# In[ ]:


history = model.fit(X_train, Y_train, epochs=1000)


# In[ ]:


model.evaluate(X_test, Y_test)


# In[ ]:


plt.plot(history.history['loss'][:18])


# In[ ]:


plt.plot(history.history['loss'][18:30])


# In[ ]:


plt.plot(history.history['loss'][30:200])


# In[ ]:


plt.plot(history.history['loss'][200:1000])


# In[ ]:


dots = model.predict(X_test)


# In[ ]:


dots[3:10]


# In[ ]:


Y_test.to_numpy()[3:10]

