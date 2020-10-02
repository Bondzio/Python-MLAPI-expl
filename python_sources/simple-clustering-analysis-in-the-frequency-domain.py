#!/usr/bin/env python
# coding: utf-8

# # Simple Clustering Analysis in the Frequency Domain
# 
# **In this kernel, we are going to present some simple observations based on clusters created based on the frequency spectrum of the signals.  
# This competition provides a good challenge (and a lot of fun!) regarding the stability of the training and the differences beetwen results in the local CV and LB score. While the discussions on adversarial validation can help with the issues, maybe the information in the clusters provide some complementary insights.**

# In[ ]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import Parallel, delayed
import pyarrow.parquet as pq
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA


# In[ ]:


N_THREADS = 4
FEATURES_DIM = 1000
CLUSTER_DIM = 100
N_SAMPLES = 3
RANDOM_SEED = 2019

np.random.seed(RANDOM_SEED)


# **Let's start by defining the features that will be used to cluster the signals.  
# We are going to use a simple median of the slices of the frequency spectrum from a discrete Fourrier transform. It's a very simple feature space to start the analysis, but let's Keep It Sweet & Simple!  
# We can expect a very skewed distribution of the data in the spectrum slices, but we are not going to transform the data this time.  
# Let's stop to write and start to coding. Here is the function to extract the features of a list of `signal_id`'s**
# 
#     def cluster_features(signals, dataset='train'):
#         if dataset == 'train':
#             data = pq.read_pandas('../input/train.parquet', columns=[str(s) for s in signals]).to_pandas().values
#         else:
#             data = pq.read_pandas('../input/test.parquet', columns=[str(s) for s in signals]).to_pandas().values
#         features = np.zeros((data.shape[1], FEATURES_DIM))
#         for i, signal in enumerate(data.T):
#             fft = np.fft.rfft(signal)
#             fft = np.abs(fft)
#             fft = np.array_split(fft, FEATURES_DIM)
#             features[i] = [np.median(d) for d in fft]
#     return features
#     
# **In this case, the spectrum is been splitted in ranges of 20 KHz. Later, we will use PCA to reduce the dimension of the feature space.**

# In[ ]:


def load_signal(signal_id):
    if signal_id <= 8711:
        signal = pd.read_parquet('../input/train.parquet', columns=[str(signal_id)])
    else:   
        signal = pd.read_parquet('../input/test.parquet', columns=[str(signal_id)])
    return np.squeeze(signal.values)

def plot_grid(id_measurements=None, signal_id=None, frame_size=(5,3), preprocessing=None):
    meta_df = pd.read_csv('../input/metadata_train.csv')
    meta_df2 = pd.read_csv('../input/metadata_test.csv')
    meta_df = pd.concat((meta_df, meta_df2), axis=0, ignore_index=True, sort=False)
    if signal_id is not None:
        id_measurements = meta_df.loc[meta_df['signal_id'].isin(signal_id), 'id_measurement'].unique()
    n_imgs = len(id_measurements)
    fig = plt.figure(figsize=(frame_size[0]*3, frame_size[1]*n_imgs))
    img_cursor = 1
    for i in id_measurements:
        signal_ids = meta_df.loc[meta_df['id_measurement']==i, 'signal_id'].values
        targets = meta_df.loc[meta_df['id_measurement']==i, 'target'].values
        for s,t in zip(signal_ids, targets):
            color = '#007fff'
            if signal_id is not None and s not in signal_id:
                color = '#c0c0c0'
            ax = fig.add_subplot(n_imgs, 3, img_cursor)
            signal = load_signal(s)
            if preprocessing is not None: 
                ax.plot(signal, color)
                ax.plot(preprocessing(signal))
            else:
                ax.plot(signal, color) 
            ax.ticklabel_format(style='sci',scilimits=(-3,4),axis='x')
            ax.grid(True)
            ax.set_title('signal_id = {} , target = {}'.format(str(s), t))
            img_cursor += 1
    plt.tight_layout()
    
def cluster_features(signals, dataset='train'):
    if dataset == 'train':
        data = pq.read_pandas('../input/train.parquet', columns=[str(s) for s in signals]).to_pandas().values
    else:
        data = pq.read_pandas('../input/test.parquet', columns=[str(s) for s in signals]).to_pandas().values
    features = np.zeros((data.shape[1], FEATURES_DIM))
    for i, signal in enumerate(data.T):
        fft = np.fft.rfft(signal)
        fft = np.abs(fft)
        fft = np.array_split(fft, FEATURES_DIM)
        features[i] = [np.median(d) for d in fft]
    return features


# **Let's load the features for the training and test datasets (s2 joblib!)**

# In[ ]:


train_meta = pd.read_csv('../input/metadata_train.csv')
train_meta = train_meta.loc[train_meta['phase'] == 0]
train_sig_ids = train_meta['signal_id'].values
train_feat = Parallel(n_jobs=N_THREADS, verbose=2)(delayed(cluster_features)(s, 'train') for s in np.array_split(train_sig_ids, 3*N_THREADS))
train_feat = np.concatenate(train_feat, axis=0)


# In[ ]:


test_meta = pd.read_csv('../input/metadata_test.csv')
test_meta = test_meta.loc[test_meta['phase'] == 0]
test_sig_ids = np.asarray([str(s) for s in test_meta['signal_id'].values])
test_feat = Parallel(n_jobs=N_THREADS, verbose=2)(delayed(cluster_features)(s, 'test') for s in np.array_split(test_sig_ids, 3*N_THREADS))
test_feat = np.concatenate(test_feat, axis=0)


# **The number of components in the PCA was enough to explain almost 99% of the variance of the training data and, as we were expecting, the features present a lot of outliers.**

# In[ ]:


features_idx = np.random.choice(np.arange(CLUSTER_DIM), 10)
norm_feat = MinMaxScaler().fit_transform(train_feat)
pca = PCA(n_components=CLUSTER_DIM).fit(norm_feat)
norm_feat = pca.transform(norm_feat)
print('PCA Explained Variance: {:.2f}%'.format(pca.explained_variance_ratio_.sum()*100))
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot('111')
ax.set_title ('Random Subset of Features')
_ = sns.boxplot(data=norm_feat[:, features_idx], ax=ax)


# **Now, we are going to select the number of clusters based on the [Silhouette Score](https://en.wikipedia.org/wiki/Silhouette_%28clustering%29). For now, just the training data is been used.**

# In[ ]:


n_clusters = np.arange(2, 10)

train_norm_feat = MinMaxScaler().fit_transform(train_feat)
pca = PCA(n_components=CLUSTER_DIM).fit(train_norm_feat)
train_norm_feat = pca.transform(train_norm_feat)
print('PCA Explained Variance: {:.2f}%'.format(pca.explained_variance_ratio_.sum()*100))
def get_silhouette(n):
    clt = KMeans(n_clusters=n, random_state=RANDOM_SEED).fit(train_norm_feat)
    #clt = DBSCAN(0.5*n).fit(train_norm_feat)
    try:
        result = silhouette_score(train_norm_feat, clt.labels_)
    except:
        result = -1
    return result
silhouette = Parallel(n_jobs=N_THREADS)(delayed(get_silhouette)(n) for n in n_clusters)
plt.plot(np.arange(2, len(silhouette)+2), silhouette)
plt.xlabel('N_Clusters')
plt.ylabel('Silhoutte Score')
plt.grid(True)
_ = plt.title('Clustering Score - Training Set')


# **It's clear that five cluster work well in our training data. Now we can see how the `target` are spread across these clusters: **

# In[ ]:


best_n_clusters = 5
clt = KMeans(n_clusters=best_n_clusters, random_state=RANDOM_SEED).fit(train_norm_feat)
train_clusters = pd.DataFrame(clt.labels_, columns=['cluster'], index=pd.Index([int(x) for x in train_sig_ids], name='signal_id'))
train_clusters['target'] = train_meta.loc[train_meta['phase']==0, 'target'].values
stats_df = train_clusters.groupby('cluster')['target'].agg(['count','sum'])
stats_df.columns = ['count', 'pos_count']
stats_df['pos_rate'] = stats_df['pos_count']/stats_df['count']
stats_df['pos_rate'] = stats_df['pos_rate'].apply(lambda x: '{:.1f} %'.format(x*100))
display(stats_df)


# **Interesting to note the clusters 4 and 2. The former virtually has no positive samples while tha latter has almost 50% of positive samples.**  
# **Let's plot a small sample of the signals in each cluster to get a feel of how they look like.**

# ### **Cluster 0**

# In[ ]:


plot_ids = train_clusters.loc[train_clusters['cluster']==0].sample(N_SAMPLES).index
plot_grid(signal_id=plot_ids)


# ### **Cluster 1**

# In[ ]:


plot_ids = train_clusters.loc[train_clusters['cluster']==1].sample(N_SAMPLES).index
plot_grid(signal_id=plot_ids)


# ### **Cluster 2**

# In[ ]:


plot_ids = train_clusters.loc[train_clusters['cluster']==2].sample(N_SAMPLES).index
plot_grid(signal_id=plot_ids)


# ### **Cluster 3**

# In[ ]:


plot_ids = train_clusters.loc[train_clusters['cluster']==3].sample(N_SAMPLES).index
plot_grid(signal_id=plot_ids)


# ### **Cluster 4**

# In[ ]:


plot_ids = train_clusters.loc[train_clusters['cluster']==4].sample(N_SAMPLES).index
plot_grid(signal_id=plot_ids)


# **Now, the clusters will be created using just the test set.**

# In[ ]:


test_norm_feat = MinMaxScaler().fit_transform(test_feat)
pca = PCA(n_components=CLUSTER_DIM).fit(test_norm_feat)
test_norm_feat = pca.transform(test_norm_feat)
print('PCA Explained Variance: {:.2f}%'.format(pca.explained_variance_ratio_.sum()*100))
def get_silhouette(n):
    clt = KMeans(n_clusters=n, random_state=RANDOM_SEED).fit(test_norm_feat)
    return silhouette_score(test_norm_feat, clt.labels_)
silhouette = Parallel(n_jobs=N_THREADS)(delayed(get_silhouette)(n) for n in n_clusters)
plt.plot(np.arange(2, len(silhouette)+2), silhouette)
plt.xlabel('N_Clusters')
plt.ylabel('Silhoutte Score')
plt.grid(True)
_ = plt.title('Clustering Score - Test Set')


# **Good! We've got five cluster again.**  
# **The number of samples in each cluster is the following: **

# In[ ]:


best_n_clusters = 5
norm_feat = MinMaxScaler().fit_transform(test_feat)
clt = KMeans(n_clusters=best_n_clusters, random_state=RANDOM_SEED).fit(norm_feat)
test_clusters = pd.DataFrame(clt.labels_, columns=['cluster'], index=test_meta['signal_id'])
stats_df = test_clusters.reset_index().groupby('cluster').count()
stats_df.columns = ['count']
display(stats_df)


# **Let's straight to the clusters using the whole dataset (training + test). We hope to find the same clusters in both dataset.**

# In[ ]:


norm_feat = MinMaxScaler().fit_transform(np.concatenate((train_feat, test_feat), axis=0))
pca = PCA(n_components=CLUSTER_DIM).fit(norm_feat)
norm_feat = pca.transform(norm_feat)
print('PCA Explained Variance: {:.2f} %'.format(pca.explained_variance_ratio_.sum()*100))

def get_silhouette(n):
    clt = KMeans(n_clusters=n, random_state=RANDOM_SEED).fit(norm_feat)
    return silhouette_score(norm_feat, clt.labels_)
silhouette = Parallel(n_jobs=N_THREADS)(delayed(get_silhouette)(n) for n in n_clusters)
plt.plot(np.arange(2, len(silhouette)+2), silhouette)
plt.xlabel('N_Clusters')
plt.ylabel('Silhoutte Score')
plt.grid(True)
_ = plt.title('Clustering Score - Test Set')


# **Now, it seems the data have 6 clusters! We have some cluster in a dataset that don't matches a cluster in the other one**
# **Getting some statistics in each cluster: **

# In[ ]:


best_n_clusters = 6
norm_feat = MinMaxScaler().fit_transform(np.concatenate((train_feat, test_feat), axis=0))
pca = PCA(n_components=CLUSTER_DIM).fit(norm_feat)
norm_feat = pca.transform(norm_feat)
clt = KMeans(n_clusters=best_n_clusters, random_state=RANDOM_SEED).fit(norm_feat)
clusters = pd.DataFrame(clt.labels_, columns=['cluster'], index=pd.Index([int(x) for x in np.concatenate((train_sig_ids, test_sig_ids), 0)], name='signal_id'))
clusters['dataset'] = 0
clusters.iloc[train_sig_ids.shape[0]:, 1] = 1
clusters['target'] = 0
clusters.iloc[:train_sig_ids.shape[0], -1] = train_meta['target'].values
stats_df = pd.DataFrame()
stats_df['count'] = clusters['cluster'].value_counts()
stats_df['train'] = clusters.groupby('cluster')['dataset'].apply(lambda x: (x==0).sum())
stats_df['test'] = clusters.groupby('cluster')['dataset'].apply(lambda x: (x==1).sum())
stats_df['pos_count'] = clusters.groupby('cluster')['target'].sum()
stats_df['pos_rate'] = clusters.groupby('cluster')['target'].sum()/stats_df['train']
stats_df['pos_rate'] = stats_df['pos_rate'].apply(lambda x: '{:.2f} %'.format(x*100))
display(stats_df)


# **We have a couple of interesting obsevations in the above dataframe:**
# 1. The cluster 5 matches the cluster 2 in the training analysis and it has no proper equivalent in the test set
# 2. The cluster 2 matches the cluster 1 in the test analysis and it has no proper equivalent in the training set
# 3. The proportion of training/test samples in cluster 0 matches the proportion of training/test samples in the dataset => Can we expect the same positive rate in the test set - cluster 0 ?  
# 
# **Let's take a look in the clusters: **

# ### **Cluster 0**

# In[ ]:


plot_grid(signal_id=clusters.loc[clusters['cluster']==0].sample(N_SAMPLES).index)


# ### **Cluster 1**

# In[ ]:


plot_grid(signal_id=clusters.loc[clusters['cluster']==1].sample(N_SAMPLES).index)


# ### **Cluster 2 (Problematic)**

# In[ ]:


plot_grid(signal_id=clusters.loc[clusters['cluster']==2].index[:6])


# ### **Cluster 3**

# In[ ]:


plot_grid(signal_id=clusters.loc[clusters['cluster']==3].sample(N_SAMPLES).index)


# ### **Cluster 4**

# In[ ]:


plot_grid(signal_id=clusters.loc[clusters['cluster']==4].sample(N_SAMPLES).index)


# ### **Cluster 5 (Problematic)**

# In[ ]:


plot_grid(signal_id=clusters.loc[clusters['cluster']==5].index[-6:])


# In[ ]:


train_clusters.to_csv('train_clusters.csv')
test_clusters.to_csv('test_clusters.csv')
clusters.to_csv('clusters.csv')


# # Final Notes
# 
# **This analysis still have a wide margin to improvements. Note the clusters are imperfect, e.g the test examples in the cluster 5 seems more similar to the cluster 4 and the clusters 2 and 3 are similar except the number of peaks.  
# Yet, it can maybe help in a post processing phase. As an example, all positive predictions in my current solution are placed in the cluster 0. It can also be used to stratify the folds in the training **
# 
# ### **That's all Folks!**
# ### **Please, leave your suggestions, comments or feedback**
