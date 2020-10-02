#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.linear_model import LogisticRegression 
model = LogisticRegression()
model.fit([[-1],[-1],[0],[1],[1]],[1,1,1,0,0]) 
print(model.intercept_) 
print(model.coef_) 
print(model.predict([[12]]))


# In[ ]:




