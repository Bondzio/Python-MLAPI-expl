#!/usr/bin/env python
# coding: utf-8

# Objectives:
# * Using pandas and sklearn for modeling
# * Feature engineering
#      a) Using statistical measures
#      b) Using Random Projections
#      c) Using clustering
#      d) USing interaction variables
# * Classifciation using Decision Tree and RandomForest

# In[17]:


get_ipython().run_line_magic('reset', '-f')


# **# 1.1 Call data manipulation libraries**

# In[18]:


import pandas as pd
import numpy as np


# **# 1.2 Feature creation libraries**

# In[19]:


from sklearn.random_projection import SparseRandomProjection as sr  # Projection features
from sklearn.cluster import KMeans                    # Cluster features
from sklearn.preprocessing import PolynomialFeatures  # Interaction features


# **# 1.3 For feature selection**

# In[20]:


# Ref: http://scikit-learn.org/stable/modules/classes.html#module-sklearn.feature_selection
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif  # Selection criteria


# In[21]:


# 1.4 Data processing
# 1.4.1 Scaling data in various manner********
from sklearn.preprocessing import StandardScaler, MinMaxScaler, scale
# 1.4.2 Transform categorical (integer) to dummy
from sklearn.preprocessing import OneHotEncoder


# In[22]:


# 1.5 Splitting data
from sklearn.model_selection import train_test_split


# In[23]:


# 1.6 Decision tree modeling
# http://scikit-learn.org/stable/modules/classes.html#module-sklearn.tree
# http://scikit-learn.org/stable/modules/tree.html#tree
from sklearn.tree import  DecisionTreeClassifier as dt


# In[24]:


# 1.7 RandomForest modeling
from sklearn.ensemble import RandomForestClassifier as rf


# In[25]:


# 1.8 Plotting libraries to plot feature importance
import matplotlib.pyplot as plt
import seaborn as sns


# In[26]:


# 1.9 Misc
import os, time, gc


# In[27]:


# 2.0 Set working directory and read file
os.chdir("../input")
print(os.listdir())


# In[28]:


# 2.1 Read heart data from files
heart = pd.read_csv("heart.csv")


# In[29]:


# 2.2 Look at data
heart.head(2)
heart.shape                        # 303 X 14


# In[30]:


# 2.3 Data types
heart.dtypes.value_counts()  


# In[ ]:


# 2.4 Target classes are almost balanced
heart.target.value_counts()


# **############################ BB. Feature Engineering #########################
# **############################ Using Statistical Numbers #####################

# In[ ]:


#  4. Feature 1: Row sums of features 1:93. More successful
#                when data is binary.

heart['sum'] = heart.sum(numeric_only = True, axis=1)  # numeric_only= None is default
heart.shape


# In[ ]:


# 4.1 Assume that value of '0' in a cell implies missing feature
#     Transform train and test dataframes
#     replacing '0' with NaN
#     Use pd.replace()
tmp_heart = heart.replace(0, np.nan)


# In[ ]:


# 4.2 Check if tmp_train is same as train or is a view
#     of train? That is check if tmp_train is a deep-copy

tmp_heart is heart                # False
#tmp_train is train.values.base    # False
tmp_heart._is_view                # False


# In[ ]:


# 4.3 Check if 0 has been replaced by NaN
tmp_heart.head(1)


# In[ ]:


# 5. Feature 2 : For every row, how many features exist
#                that is are non-zero/not NaN.
#                Use pd.notna()
tmp_heart.notna().head(1)
heart["count_not0"] = tmp_heart.notna().sum(axis = 1)
heart.shape


# In[ ]:


# 6. Similary create other statistical features
#    Feature 3
#    Pandas has a number of statistical functions
#    Ref: https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#computations-descriptive-stats

feat = [ "var", "median", "mean", "std", "max", "min"]
for i in feat:
    heart[i] = tmp_heart.aggregate(i,  axis =1)


# In[ ]:


# 7 Delete not needed variables and release memory
del(tmp_heart)
gc.collect()


# In[ ]:


# 7.1 So what do we have finally
heart.shape                # 303 X (14 + 1 + 1 + 6) ; 14th Index is target
heart.head(1)


# In[ ]:


# 8. Before we proceed further, keep target feature separately
target = heart['target']
target.tail(2)


# In[ ]:


# 9.1 Drop 'target' column
heart.drop(columns = ['target'], inplace = True)
heart.shape                # 303 X 21


# In[ ]:


# 9.2. Store column names of our data somewhere
#     We will need these later (at the end of this code)
colNames = heart.columns.values
colNames


# ############################################################################
# ################ Feature creation Using Random Projections ##################
# **# 10. Random projection is a fast dimensionality reduction feature
# **#     Also used to look at the structure of data
# ****

# In[ ]:


# 11. Transform tmp t0 numpy array
#      Henceforth we will work with array only
tmp = heart.values


# In[ ]:


# 12. tmp shape
tmp.shape       # (303, 21)


# In[ ]:


# 13. Let us create 10 random projections/columns
#     This decision, at present, is arbitrary
NUM_OF_COM = 12


# In[ ]:


# 13.1 Create an instance of class
rp_instance = sr(n_components = NUM_OF_COM)


# In[ ]:


# 13.2 fit and transform the (original) dataset
#      Random Projections with desired number
#      of components are returned
rp = rp_instance.fit_transform(tmp[:, :13])


# In[ ]:


# 13.3 Look at some features
rp[: 3, :  12]


# In[ ]:


# 13.4 Create some column names for these columns
#      We will use them at the end of this code
rp_col_names = ["r" + str(i) for i in range(12)]
rp_col_names


# ############################ Feature creation using kmeans ####################
# 

# In[ ]:


# 14. Before clustering, scale data
# 15.1 Create a StandardScaler instance
se = StandardScaler()


# In[ ]:


# 15.2 fit() and transform() in one step
tmp = se.fit_transform(tmp)


# In[ ]:


# 15.3
tmp.shape               # 303 X 21 (an ndarray)
target.shape


# In[ ]:


# 16. Perform kmeans using 93 features.
#     No of centroids is no of classes in the 'target'
centers = target.nunique()    # 2 unique classes
centers               # 9


# In[ ]:


# 17.1 Begin clustering
start = time.time()

# 17.2 First create object to perform clustering
kmeans = KMeans(n_clusters=centers, # How many
                n_jobs = 2)         # Parallel jobs for n_init



# 17.3 Next train the model on the original data only
kmeans.fit(tmp[:, : 13])

end = time.time()
(end-start)/60.0      # 5 minutes


# In[ ]:


# 18 Get clusterlabel for each row (data-point)
kmeans.labels_
kmeans.labels_.size   # 303


# In[ ]:


# 19. Cluster labels are categorical. So convert them to dummy

# 19.1 Create an instance of OneHotEncoder class
ohe = OneHotEncoder(sparse = False)


# In[ ]:


# 19.2 Use ohe to learn data
#      ohe.fit(kmeans.labels_)
ohe.fit(kmeans.labels_.reshape(-1,1))     # reshape(-1,1) recommended by fit()
                                          # '-1' is a placeholder for actual


# In[ ]:


# 19.3 Transform data now
dummy_clusterlabels = ohe.transform(kmeans.labels_.reshape(-1,1))
dummy_clusterlabels
dummy_clusterlabels.shape    # 206245 X 9 (as many as there are classes)


# In[ ]:


# 19.4 We will use the following as names of new nine columns
#      We need them at the end of this code

k_means_names = ["k" + str(i) for i in range(2)]
k_means_names


# ############################ Interaction features #######################
# **# 21. Will require lots of memory if we take large number of features
# 

# In[ ]:


degree = 2
poly = PolynomialFeatures(degree,                 # Degree 2
                          interaction_only=True,  # Avoid e.g. square(a)
                          include_bias = False    # No constant term
                          )


# In[ ]:


# 21.1 Consider only first 5 features
#      fit and transform
df =  poly.fit_transform(tmp[:, : 5])
df.shape     # 303 X 15


# In[ ]:


# 21.2 Generate some names for these 15 columns
poly_names = [ "poly" + str(i)  for i in range(15)]
poly_names


# ################# concatenate all features now ##############################

# In[ ]:


# 22 Append now all generated features together
# 22 Append random projections, kmeans and polynomial features to tmp array

tmp.shape          # 303 X 21


# In[ ]:


#  22.1 If variable, 'dummy_clusterlabels', exists, stack kmeans generated
#       columns also else not. 'vars()'' is an inbuilt function in python.
#       All python variables are contained in vars().

tmp = np.hstack([tmp,rp])       # No kmeans and polynomial      <==
tmp.shape          # 303 X 33   I  


# In[ ]:


# 22.1 Separate train and test
X = tmp[: 230, : ]
X.shape                             # 61878 X 135 if no kmeans: (61878, 126)


# In[ ]:


# 22.2
test = tmp[230 :, : ]
test.shape                         # 144367 X 135; if no kmeans: (144367, 126)


# In[ ]:


# 22.3 Delete tmp
del tmp
gc.collect()


# ################## Model building #####################

# In[ ]:


target.shape
X.shape

t1 = target.head(230)
t2 = target.tail(73)


# In[ ]:


# 23. Split train into training and validation dataset
X_train, X_test, y_train, y_test = train_test_split(
                                                    X,
                                                    t1,
                                                    test_size = 0.3)


# In[ ]:


# 23.1
X_train.shape    # 43314 X 135  if no kmeans: (43314, 126)
X_test.shape     # 18564 X 135; if no kmeans: (18564, 126)
y_train.shape


# In[ ]:


# 24 Decision tree classification
# 24.1 Create an instance of class
clf = dt(min_samples_split = 5,
         min_samples_leaf= 5
        )
start = time.time()
# 24.2 Fit/train the object on training data
#      Build model
clf = clf.fit(X_train, y_train)
end = time.time()
(end-start)/60                     # 1 minute


# In[ ]:


# 24.3 Use model to make predictions
predicted_target = clf.predict(X_test)


# In[ ]:


# 24.4 Check accuracy
(predicted_target == y_test).sum()/y_test.size      # 72%


# In[ ]:


# 25. Instantiate RandomForest classifier
clf = rf(n_estimators=20)


# In[ ]:


# 25.1 Fit/train the object on training data
#      Build model

start = time.time()
clf = clf.fit(X_train, y_train)
end = time.time()
(end-start)/60


# In[ ]:


# 25.2 Use model to make predictions
pre_target = clf.predict(X_test)
# 25.3 Check accuracy
(pre_target == y_test).sum()/y_test.size      # 72%


# ############################################  DONE ######################
# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




