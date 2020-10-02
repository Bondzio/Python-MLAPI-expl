#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
#from matplotlib.plot import plt
import matplotlib
# display graphs inline
get_ipython().run_line_magic('matplotlib', 'inline')

# Make graphs prettier
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 700)
#pd.set_option('display.mpl_style', 'default')
matplotlib.style.use('ggplot')
# Make the fonts bigger
matplotlib.rc('figure', figsize=(14, 7))
matplotlib.rc('font', weight='bold', size=15)
import seaborn as sns


# In[ ]:


consumer_complaint = pd.read_csv("../input/consumer_complaints.csv", encoding='utf8', sep=',', parse_dates=True,low_memory=False)


# In[ ]:


consumer_complaint.rename(columns = {'consumer_disputed?':'consumer_disputed'},inplace = True)


# In[ ]:


complain_flag = '1'*len(consumer_complaint['state'])
consumer_complaint['complains'] = [ int(x) for x in complain_flag if not x  == ',']
consumer_complaint_state_wise = consumer_complaint.groupby('state').aggregate(np.sum)
consumer_complaint_state_wise.drop('complaint_id', axis = 1, inplace =  True)
consumer_complaint_state_wise.plot(kind = 'bar')


# State(s) with Maximum complaints

# In[ ]:


consumer_complaint_state_wise[consumer_complaint_state_wise['complains'] == consumer_complaint_state_wise['complains'].max()]


# State(s) with Minimum complaints

# In[ ]:


consumer_complaint_state_wise[consumer_complaint_state_wise['complains'] == consumer_complaint_state_wise['complains'].min()]


# Company wise Complaint Analysis

# In[ ]:


consumer_complaint_compnay_wise = consumer_complaint.groupby('company').aggregate(np.sum)
consumer_complaint_compnay_wise.drop('complaint_id', axis = 1, inplace =  True)


# Company with most number of Complaints

# In[ ]:


consumer_complaint_compnay_wise[consumer_complaint_compnay_wise['complains'] == consumer_complaint_compnay_wise['complains'].max()]


# Compnaies with 10000 and more Complaints

# In[ ]:


consumer_complaint_compnay_wise[consumer_complaint_compnay_wise['complains'] > 10000].plot(kind = 'bar')


# Product Wise Analysis

# In[ ]:


consumer_complaint_product_wise = consumer_complaint.groupby('product').aggregate(np.sum)
consumer_complaint_product_wise.drop('complaint_id', axis = 1, inplace =  True)


# Product with Most number of Complaints

# In[ ]:


consumer_complaint_product_wise[consumer_complaint_product_wise['complains'] == consumer_complaint_product_wise['complains'].max()]


# Product with Least number of Complaints

# In[ ]:


consumer_complaint_product_wise[consumer_complaint_product_wise['complains'] == consumer_complaint_product_wise['complains'].min()]


# In[ ]:


consumer_complaint_product_wise.plot(kind = 'bar')


# Companies with Best Customer Services

# In[ ]:


consumer_complaint_best_cc =  consumer_complaint[(consumer_complaint.timely_response == 'Yes') &
                                                 (consumer_complaint.consumer_disputed == 'No')]
consumer_complaint_best_cc = consumer_complaint_best_cc.groupby('company').aggregate(np.sum)
consumer_complaint_best_cc.drop('complaint_id', axis = 1, inplace =  True)
consumer_complaint_best_cc[consumer_complaint_best_cc['complains'] == consumer_complaint_best_cc['complains'].max()]


# But wait!! this is just showing number of complained resolved where customers have not disputed.We need to do more to find the best and worst companies when it comes to customer services.

# In[ ]:


consumer_complaint['percent_resolution'] = np.where((consumer_complaint.timely_response.str.contains('Yes') &
                                                                    consumer_complaint.consumer_disputed.str.contains('No')), 1, 0)
consumer_complaint_best_cc = consumer_complaint.groupby('company').aggregate(np.sum)
consumer_complaint_best_cc.drop('complaint_id', axis = 1, inplace =  True)
consumer_complaint_best_cc['percent_resolution'] = consumer_complaint_best_cc['percent_resolution']/consumer_complaint_best_cc['complains']
consumer_complaint_best_cc['percent_resolution']  = consumer_complaint_best_cc['percent_resolution'] .apply(lambda x : float(x*100))


# To Make it more fair ,let's consider Companies with number of complains more than 5000

# In[ ]:


consumer_complaint_best_cc= consumer_complaint_best_cc[consumer_complaint_best_cc['complains'] >= 5000]
consumer_complaint_best_cc.sort_values('percent_resolution', ascending = False)


# In[ ]:


consumer_complaint_best_cc['percent_resolution'].plot(kind = 'bar')


# Experian is the compnay when it comes to customer satisfaction.
