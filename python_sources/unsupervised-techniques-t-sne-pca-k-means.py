#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fivethirtyeight')

import collections
import itertools

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly as py
import plotly.graph_objs as go

import scipy.stats as stats
from scipy.stats import norm
from scipy.special import boxcox1p

import statsmodels
import statsmodels.api as sm
#print(statsmodels.__version__)

from sklearn.preprocessing import scale, StandardScaler, RobustScaler, OneHotEncoder
from sklearn.utils import resample
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import colorlover as cl
from IPython.display import HTML

chosen_colors=cl.scales['7']['qual'][np.random.choice(list(cl.scales['7']['qual'].keys()))]

print('The color palette chosen for this notebook is:')
HTML(cl.to_html(chosen_colors))


# # Load data

# In[ ]:


Combined_data = pd.read_csv('../input/new-york-city-airbnb-open-data/AB_NYC_2019.csv')
Combined_data.head()


# In[ ]:


print('Number of features: {}'.format(Combined_data.shape[1]))
print('Number of examples: {}'.format(Combined_data.shape[0]))


# In[ ]:


#for c in df.columns:
#    print(c, dtype(df_train[c]))
Combined_data.dtypes


# In[ ]:


Combined_data['last_review'] = pd.to_datetime(Combined_data['last_review'],infer_datetime_format=True) 


# # Input processing

# ### Missing data

# In[ ]:


total = Combined_data.isnull().sum().sort_values(ascending=False)
percent = (Combined_data.isnull().sum())/Combined_data.isnull().count().sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total','Percent'], sort=False).sort_values('Total', ascending=False)
missing_data.head(40)


# In[ ]:


Combined_data.drop(['host_name','name'], axis=1, inplace=True)


# In[ ]:


Combined_data[Combined_data['number_of_reviews']== 0.0].shape


# The NaN values in the last_review and reviews_per_month columns all occur for examples where no reviews were given in the first place. 
# 
# For reviews_per_month, I will fill those values with 0's.

# In[ ]:


Combined_data['reviews_per_month'] = Combined_data['reviews_per_month'].fillna(0)


# In[ ]:


earliest = min(Combined_data['last_review'])
Combined_data['last_review'] = Combined_data['last_review'].fillna(earliest)
Combined_data['last_review'] = Combined_data['last_review'].apply(lambda x: x.toordinal() - earliest.toordinal())


# In[ ]:


total = Combined_data.isnull().sum().sort_values(ascending=False)
percent = (Combined_data.isnull().sum())/Combined_data.isnull().count().sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total','Percent'], sort=False).sort_values('Total', ascending=False)
missing_data.head(40)


# ### Outliers & input transformations

# See my rental price prediction notebook for details!
# 

# In[ ]:


Combined_data = Combined_data[np.log1p(Combined_data['price']) < 8]
Combined_data = Combined_data[np.log1p(Combined_data['price']) > 3]
Combined_data['price'] = np.log1p(Combined_data['price'])

Combined_data = Combined_data.drop(['host_id', 'id'], axis=1)

Combined_data['minimum_nights'] = np.log1p(Combined_data['minimum_nights'])

Combined_data['reviews_per_month'] = Combined_data[Combined_data['reviews_per_month'] < 17.5]['reviews_per_month']


# #### Categorical features

# In[ ]:


categorical_features = Combined_data.select_dtypes(include=['object'])
print('Categorical features: {}'.format(categorical_features.shape))
categorical_features_one_hot = pd.get_dummies(categorical_features)
categorical_features_one_hot.head()
Combined_data['reviews_per_month'] = Combined_data['reviews_per_month'].fillna(0)

numerical_features =  Combined_data.select_dtypes(exclude=['object'])
y = numerical_features.price
numerical_features = numerical_features.drop(['price'], axis=1)
print('Numerical features: {}'.format(numerical_features.shape))


# In[ ]:


X = np.concatenate((numerical_features, categorical_features_one_hot), axis=1)
X_df = pd.concat([numerical_features, categorical_features_one_hot], axis=1)
#print('Dimensions of the design matrix: {}'.format(X.shape))
#print('Dimension of the target vector: {}'.format(y.shape))

Processed_data = pd.concat([X_df, y], axis = 1)
#Processed_data.to_csv('NYC_Airbnb_Processed.dat')


# In[ ]:





# ### Scaling

# In[ ]:


scaler = RobustScaler()
scaler.fit(X)
X = scaler.transform(X)
X;


# # PCA

# In[ ]:


pca = PCA()
X_pca = pca.fit_transform(X);
pca.get_covariance();

explained_variance = pca.explained_variance_ratio_
explained_variance = pd.DataFrame({'PCA Component': [1+x for x in range(len(explained_variance))], 'Explained Variance': explained_variance})
explained_variance.head()


# In[ ]:


n_components = 50
trace1 = go.Scatter(
    x=explained_variance["PCA Component"][:n_components], 
    y=100*explained_variance["Explained Variance"][:n_components],
    
    mode='markers',
    line=dict(
        color='red'
    ),
)

trace2 = go.Scatter(
    x=explained_variance["PCA Component"][:n_components], 
    y=100*explained_variance["Explained Variance"][:n_components],
    
    mode='lines',
    line=dict(
        color='red'
    ),
)

data=[trace1, trace2]

layout = go.Layout(
    title='Proportion of Explained Variance per PCA component',
    xaxis=dict(
        title='Component',
        showgrid=True
    ),
    yaxis=dict(
        title='Explained variance [%]',
        type='log'
    ),
    hovermode='closest',
)

figure = go.Figure(data=data, layout=layout)

figure.update_layout(showlegend=False)

iplot(figure)


# In[ ]:


pca_cov = pca.get_covariance();
pca_cov = pca_cov[:12, :12]
f, ax = plt.subplots(figsize=(15,12))
sns.heatmap(pca_cov, vmax=0.8, square=True, annot=True)


# In[ ]:


n_components = 235
pca_cov = pca.get_covariance();
pca_cov = pca_cov[:14, :n_components]
f, ax = plt.subplots(figsize=(28,5))
sns.heatmap(pca_cov, vmax=0.8, cmap="YlGnBu")


# # t-SNE

# In[ ]:


print("Calculating TSNE")
tsne = TSNE(n_components=3, perplexity=5, verbose=2, n_iter=1000,early_exaggeration=1)
tsne0 = tsne.fit_transform(X)

fig, axes = plt.subplots(1,3,figsize=(18.5, 10.5))

axes[0].scatter(tsne0[:,0],tsne0[:,1], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[0].set_title('TSNE[0] vs TSNE[1]')

axes[1].scatter(tsne0[:,0],tsne0[:,2], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[1].set_title('TSNE[0] vs TSNE[2]')

axes[2].scatter(tsne0[:,1],tsne0[:,2], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[2].set_title('TSNE[1] vs TSNE[2]')


# In[ ]:


print("Calculating TSNE")
tsne = TSNE(n_components=3, perplexity=5, verbose=2, n_iter=1000,early_exaggeration=12)
tsne0 = tsne.fit_transform(X)

fig, axes = plt.subplots(1,3,figsize=(18.5, 10.5))

axes[0].scatter(tsne0[:,0],tsne0[:,1], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[0].set_title('TSNE[0] vs TSNE[1]')

axes[1].scatter(tsne0[:,0],tsne0[:,2], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[1].set_title('TSNE[0] vs TSNE[2]')

axes[2].scatter(tsne0[:,1],tsne0[:,2], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[2].set_title('TSNE[1] vs TSNE[2]')


# In[ ]:


print("Calculating TSNE")
tsne = TSNE(n_components=3, perplexity=50, verbose=2, n_iter=5000,early_exaggeration=1)
tsne0 = tsne.fit_transform(X)

fig, axes = plt.subplots(1,3,figsize=(18.5, 10.5))

axes[0].scatter(tsne0[:,0],tsne0[:,1], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[0].set_title('TSNE[0] vs TSNE[1]')

axes[1].scatter(tsne0[:,0],tsne0[:,2], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[1].set_title('TSNE[0] vs TSNE[2]')

axes[2].scatter(tsne0[:,1],tsne0[:,2], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[2].set_title('TSNE[1] vs TSNE[2]')


# In[ ]:


print("Calculating TSNE")
tsne = TSNE(n_components=3, perplexity=50, verbose=2, n_iter=1000,early_exaggeration=4)
tsne0 = tsne.fit_transform(X_pca)

fig, axes = plt.subplots(1,3,figsize=(18.5, 10.5))

axes[0].scatter(tsne0[:,0],tsne0[:,1], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[0].set_title('TSNE[0] vs TSNE[1]')

axes[1].scatter(tsne0[:,0],tsne0[:,2], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[1].set_title('TSNE[0] vs TSNE[2]')

axes[2].scatter(tsne0[:,1],tsne0[:,2], 
            cmap = "coolwarm", edgecolor = "None", alpha=0.35)
axes[2].set_title('TSNE[1] vs TSNE[2]')


# # K-means clustering

# In[ ]:


X1 = X_df[['Longitude' , 'Latitude']].iloc[: , :].values
inertia = []
for n in range(1 , 11):
    algorithm = (KMeans(n_clusters = n ,init='k-means++', n_init = 10 ,max_iter=300, 
                        tol=0.0001,  random_state= 111  , algorithm='elkan') )
    algorithm.fit(X1)
    inertia.append(algorithm.inertia_)

print(intertia)


# In[ ]:


plt.figure(1 , figsize = (15 ,6))
plt.plot(np.arange(1 , 11) , inertia , 'o')
plt.plot(np.arange(1 , 11) , inertia , '-' , alpha = 0.5)
plt.xlabel('Number of Clusters') , plt.ylabel('Inertia')
plt.show()


# In[ ]:


X2 = X_df[['Longitude' , 'Latitude']].iloc[: , :].values
inertia = []
for n in range(1 , 11):
    algorithm = (KMeans(n_clusters = n ,init='k-means++', n_init = 10 ,max_iter=300, 
                        tol=0.0001,  random_state= 111  , algorithm='elkan') )
    algorithm.fit(X2)
    inertia.append(algorithm.inertia_)

print(inertia)


# In[ ]:


plt.figure(1 , figsize = (15 ,6))
plt.plot(np.arange(1 , 11) , inertia , 'o')
plt.plot(np.arange(1 , 11) , inertia , '-' , alpha = 0.5)
plt.xlabel('Number of Clusters') , plt.ylabel('Inertia')
plt.show()


# # Acknowledgements

# ### t-SNE

# 1. [This Google Tech Talk by Laurens Van Der Maaten](https://www.youtube.com/watch?v=RJVL80Gg3lA) is a fantastic introduction to t-SNE.
# 2. A great reference for python code for t-SNE is [this kernel](https://www.kaggle.com/arthurtok/tsne-pca-quick-and-dirty-visuals).
# 3. [This blog post is a tremendously enlightening discussion of how to correctly use t-SNE.](https://distill.pub/2016/misread-tsne/)

# ### K-means

# 1. [This Mall Customer Segmentation Data notebook](https://www.kaggle.com/kushal1996/customer-segmentation-k-means-analysis) contains lost of great K-means visualizations coded up clearly.

# In[ ]:




