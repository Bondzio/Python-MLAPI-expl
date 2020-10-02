#!/usr/bin/env python
# coding: utf-8

# # White Wine Quality 
# Eng : Learning how to preprocessing, with data mining method.  
# Ind : Belajar bagaimana untuk pra proses data dengan metode data mining.  
# Data Mining Process :
# 1. Replace Outliers with mean
# 2. Classified the quality

# In[ ]:


# Import semua library yang dibutuhkan
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # data visualisation (2-D)
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns # data visualisation (3-D)
plt.style.use('seaborn') # set style for graph
from scipy import stats


# In[ ]:


# Import file dataset
rawdata = pd.read_csv('../input/whinequality/winequality-white.csv')


# In[ ]:


# Menampilkan data
display(rawdata.head(), rawdata.shape) 


# In[ ]:


# Menampilkan informasi pada dataset
# Seperti jumlah missing value, dan type field
rawdata.info()


# In[ ]:


# Mendapatkan deskripsi dari dataset berupa count, mean, std, min, q1, q2, q3, dan max
# pada masing-masing field
rawdata.describe()


# In[ ]:


# Mengecek nilai kolerasi antar masing-masing field, untuk melihat pesebaran datanya
rawdata.corr()


# In[ ]:


fl = ['fixed acidity','volatile acidity','citric acid','residual sugar','chlorides','free sulfur dioxide','total sulfur dioxide','density','pH','sulphates','alcohol']

for f in fl:
    print(stats.normaltest(rawdata[f]))


# In[ ]:


outliers = []  # list data untuk menampung nilai ouliers

# metode yang digunakan untuk mendeteksi outliers yaitu interquartile range 
def detect_outliers(data): 
    quantile1, quantile3 = np.percentile(data, [25, 75])  # create two quantiles for 25% and 75%
    iqr_val = quantile3 - quantile1                       # interquantilerange value
    lower_bound_value = quantile1 - (1.5 * iqr_val)       # lower limit of the data, anything greater are not outliers
    upper_bound_value = quantile3 + (1.5 * iqr_val)       # upper limit of the data, anything less are not outliers
    
    for i in data:
        if lower_bound_value < i < upper_bound_value:     # if data[value] is greater than lbv and less than ubv than it is not considered as an outlier
            pass
        else:
            outliers.append(i)
            
    return lower_bound_value, upper_bound_value        # return lower bound and upper bound value for the data

feature_list = ['fixed acidity','volatile acidity','citric acid','residual sugar','chlorides','free sulfur dioxide','total sulfur dioxide','density','pH','sulphates','alcohol']
# #Delete outlier
for i in feature_list:
    mean = rawdata[i].mean()
    bawah, atas = detect_outliers(rawdata[i])
    rawdata[i] = rawdata[i].mask(rawdata[i] > atas, mean)


# In[ ]:


rawdata.corr()


# In[ ]:


bins = (3, 6, 9)
group_names = ['bad','good']
rawdata['quality'] = pd.cut(rawdata['quality'], bins = bins, labels = group_names)


# In[ ]:


#Now lets assign a labels to our quality variable
label_quality = LabelEncoder()


# In[ ]:


rawdata['quality'].replace(['bad','good'],[0,1],inplace=True)

#Bad becomes 0 and good becomes 1 
# rawdata['quality'] = label_quality.fit_transform(rawdata['quality'])
rawdata['quality'].value_counts()


# In[ ]:


rawdata.corr()


# In[ ]:


print(stats.normaltest(rawdata['fixed acidity']))

