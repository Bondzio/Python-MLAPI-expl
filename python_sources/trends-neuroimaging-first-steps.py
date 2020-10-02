#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


get_ipython().system('pip install --upgrade pip')


# In[ ]:


get_ipython().system('pip install h5py')


# In[ ]:


# Installing the nilearn
#!wget https://github.com/Chaogan-Yan/DPABI/raw/master/Templates/ch2better.nii


# In[ ]:


import h5py #reading .mat files and weights files .h5
import numpy as np # linear algebra
import pandas as pd  # data processing
import random
import matplotlib.pyplot as plt
import seaborn as sns

import nilearn as nl #statistical learning on NeuroImaging data
import nilearn.plotting as nlplt
import nibabel as nib
from nilearn import image
from nilearn import plotting
from nilearn import datasets
from nilearn import surface

import os 

from sklearn.svm import SVR
from sklearn.model_selection import KFold #consider using GridSearchCV


# In[ ]:


dataDir = '/kaggle/input/trends-assessment-prediction/'
workDir = '/kaggle/working/'
os.listdir(dataDir)


# In[ ]:


#Functional network connectivity (FNC) 
fnc_df = pd.read_csv(os.path.join(dataDir,'fnc.csv'))
fnc_df.head()


# In[ ]:


print(fnc_df.shape)
#fnc_df.dtypes


# In[ ]:


#sMRI SBM loadings
smri_sbm_df = pd.read_csv(os.path.join(dataDir, 'loading.csv'))
smri_sbm_df.head()


# In[ ]:


#smri_sbm_df.isnull().sum()


# In[ ]:


print(smri_sbm_df.shape)
#smri_sbm_df.dtypes


# In[ ]:


#target features
labels_df = pd.read_csv(os.path.join(dataDir, 'train_scores.csv'))
labels_df.head()


# In[ ]:


labels_df.shape


# In[ ]:


print('Nan values in domain1_var1: ', labels_df.domain1_var1.isnull().sum())
print('Nan values in domain1_var2: ', labels_df.domain1_var2.isnull().sum())
print('Nan values in domain2_var1: ', labels_df.domain2_var1.isnull().sum())
print('Nan values in domain2_var2: ', labels_df.domain2_var2.isnull().sum())


# In[ ]:


#TODO: make it interactive
fig, ax = plt.subplots(1, 4, figsize=(25, 5))

# sns.distplot(labels_df['age'], ax = ax[0],
#                   kde_kws = {"color": "green", "lw": 3},
#                   hist_kws = {"histtype": "bar", "linewidth": 3,
#                             "alpha": 1, "color": "orange"})

sns.distplot(labels_df['domain1_var1'], ax = ax[0],
                  kde_kws = {"color": "green", "lw": 3},
                  hist_kws = {"histtype": "bar", "linewidth": 3,
                            "alpha": 1, "color": "orange"})

sns.distplot(labels_df['domain1_var2'], ax = ax[1],
                  kde_kws = {"color": "green", "lw": 3},
                  hist_kws = {"histtype": "bar", "linewidth": 3,
                            "alpha": 1, "color": "orange"})

sns.distplot(labels_df['domain2_var1'], ax = ax[2],
                  kde_kws = {"color": "green", "lw": 3},
                  hist_kws = {"histtype": "bar", "linewidth": 3,
                            "alpha": 1, "color": "orange"})

sns.distplot(labels_df['domain2_var2'], ax = ax[3],
                  kde_kws = {"color": "green", "lw": 3},
                  hist_kws = {"histtype": "bar", "linewidth": 3,
                            "alpha": 1, "color": "orange"}) 

fig.suptitle('Labels Visualization', fontsize=16)


# In[ ]:


def plot_bar(df, feature, title='', show_percent = False, size=2):
    f, ax = plt.subplots(1,1, figsize=(4 * size,3 * size))
    total = float(len(df))
    sns.barplot(np.round(df[feature].value_counts().index).astype(int),
                df[feature].value_counts().values, 
                palette='cubehelix')

    plt.title(title)
    
    if show_percent:
        for p in ax.patches:
            height = p.get_height()
            ax.text(p.get_x() + p.get_width()/2.,
                    height + 3,
                    '{:1.2f}%'.format(100 * height / total),
                    ha = "center", rotation = 45) 
    plt.xlabel(feature, fontsize=12, )
    plt.ylabel('Number of Occurrences', fontsize=12)
    plt.xticks(rotation = -45)
    plt.show()


# In[ ]:


plot_bar(labels_df, 'age', 'Age Label Count and % Plot', show_percent = True, size = 4)


# In[ ]:


temp_data =  labels_df.drop(['Id'], axis = 1)

plt.figure(figsize = (15, 15))
sns.heatmap(temp_data.corr(), annot = True, cmap='Paired')
plt.yticks(rotation=0) 

plt.show()


# In[ ]:


fnc_features, loading_features = list(fnc_df.columns[1:]), list(smri_sbm_df.columns[1:])


# In[ ]:


labels_df['is_train'] = 1


# In[ ]:


df = fnc_df.merge(smri_sbm_df, on='Id')
df = df.merge(labels_df, how='left', on='Id')

df.loc[df['is_train'].isnull(), 'is_train'] = 0
df['is_train'] = df['is_train'].astype(np.uint8)
#TODO: split to train-test based on last column


# In[ ]:


df.head()


# In[ ]:


train_data = df[df['is_train'] == 1]
test_data = df[df['is_train'] == 0]


# In[ ]:


train_data.head()


# In[ ]:


train_data.isnull().sum()


# In[ ]:


test_data.head()


# In[ ]:


test_data.isnull().sum()


# ## About FNC Features
# *Functional Network Connectivity (FNC) are correlation values that summarize the overall connection between independent brain maps over time. Therefore, the FNC feature gives a picture of the connectivity pattern over time between independent networks (or brain maps). The provided FNC information was obtained from functional magnetic resonance imaging (fMRI) from a set of schizophrenic patients and healthy controls at rest, using group independent component analysis (GICA). The GICA decomposition of the fMRI data resulted in a set of brain maps, and corresponding timecourses. These timecourses indicated the activity level of the corresponding brain map at each point in time. The FNC feature are the correlations between these timecourses. In a way, FNC indicates a subject's overall level of 'synchronicity' between brain areas. Because this information is derived from functional MRI scans, FNCs are considered a functional modality feature (i.e., they describe patterns of the brain function).*
# 
# ## About SBM Loadings
# *Source-Based Morphometry (SBM) loadings correspond to the weights of brain maps obtained from the application of independent component analysis (ICA) on the gray-matter concentration maps of all subjects. Gray-matter corresponds to the outer-sheet of the brain; it is the brain region in which much of the brain signal processing actually occurs. In a way, the concentration of gray-matter is indicative of the "computational power" available in a certain region of the brain. Processing gray-matter concentration maps with ICA yields independent brain maps whose expression levels (i.e., loadings) vary across subjects. Simply put, a near-zero loading for a given ICA-derived brain map indicates that the brain regions outlined in that map are lowly present in the subject (i.e., the gray-matter concentration in those regions are very low in that subject). Because this information is derived from structural MRI scans, SBM loadings are considered a structural modality feature (i.e., they describe patterns of the brain structure).*
# 
# https://www.kaggle.com/anshumoudgil/brain-s-network-activation-via-eda/comments
# The paper above gives information about some basic definitions such as FNC, ICM, etc.

# ### TODO: Add more explanations for the features
# ### TODO: Fill NaN-s appropriately
# Should I drop the missing values, fill them with a test statistic or use ML algorithm(knn, other)
# ### TODO: Plot distributions
# ### TODO: Plot correlations
# ### TODO: Show more interesting scans. Check this out: https://www.kaggle.com/soham1024/visualization-using-nilearn
# ### TODO: Try basic NN 
# ### TODO: Run this on local machine and install RAPIDs to check how fast it works on GPU (if possible to load 160GB+ data to local)

# ### What is .nii file format?
# The [.nii] file type is primarily associated with NIfTI-1 Data Format by Neuroimaging Informatics Technology Initiative. 
# NIfTI-1 is adapted from the widely used ANALYZE 7.5 file format. NIfTI-1 uses the empty space in the ANALYZE 7.5 header to add several new features.
# 
# Credit: https://www.kaggle.com/saife245/neuroimaging-in-depth-understanding-eda-model

# In[ ]:


fmri_mask = os.path.join(dataDir, 'fMRI_mask.nii')


# In[ ]:


#smri = 'ch2better.nii'

mask_img = nl.image.load_img(fmri_mask)


# In[ ]:


def load_subject(filename, mask_img):
    subject_data = None
    with h5py.File(filename, 'r') as f:
        subject_data = f['SM_feature'][()]
    # It's necessary to reorient the axes, since h5py flips axis order
    subject_data = np.moveaxis(subject_data, [0,1,2,3], [3,2,1,0])
    subject_img = nl.image.new_img_like(mask_img, subject_data, affine=mask_img.affine, copy_header=True)

    return subject_img


# In[ ]:


files = random.choices(os.listdir('../input/trends-assessment-prediction/fMRI_train/'), k = 3)


# ### Plotting 4D probabilistic atlas maps...
# Probabilistic atlasing is a research strategy whose goal is to generate anatomical templates that retain quantitative information on inter-subject variations in brain architecture

# In[ ]:


for file in files:
    subject = os.path.join('../input/trends-assessment-prediction/fMRI_train/', file)
    subject_img = load_subject(subject, mask_img)
    print("Image shape is %s" % (str(subject_img.shape)))
    num_components = subject_img.shape[-1]
    print("Detected {num_components} spatial maps".format(num_components=num_components))
    nlplt.plot_prob_atlas(subject_img, view_type='filled_contours', #bg_img=smri
                          draw_cross=False, title='All %d spatial maps' % num_components, threshold='auto')
    print("-"*50)


# ### Plotting a statistical map...
# Statistical parametric mapping or SPM is a statistical technique for examining differences in brain activity recorded during functional neuroimaging experiments.

# In[ ]:


files = random.choices(os.listdir('../input/trends-assessment-prediction/fMRI_train/'), k = 3)


# In[ ]:


for file in files:
    subject = os.path.join('../input/trends-assessment-prediction/fMRI_train/', file)
    subject_img = load_subject(subject, mask_img)
    print("Image shape is %s" % (str(subject_img.shape)))
    num_components = subject_img.shape[-1]
    print("Detected {num_components} spatial maps".format(num_components=num_components))
    rsn = subject_img
    #convert to 3d image
    first_rsn = image.index_img(rsn, 0)
    print(first_rsn.shape)
    plotting.plot_stat_map(first_rsn)
    print("-"*50)


# In[ ]:


files = random.choices(os.listdir('../input/trends-assessment-prediction/fMRI_train/'), k = 1)


# In[ ]:


for file in files:
    subject = os.path.join('../input/trends-assessment-prediction/fMRI_train/', file)
    subject_img = load_subject(subject, mask_img)
    print("Image shape is %s" % (str(subject_img.shape)))
    num_components = subject_img.shape[-1]
    print("Detected {num_components} spatial maps".format(num_components=num_components))
    rsn = subject_img
    #convert to 3d image
    first_rsn = image.index_img(rsn, 0)
    print(first_rsn.shape)
    for img in image.iter_img(rsn):
        # img is now an in-memory 3D img
        plotting.plot_stat_map(img, threshold=3)
    print("-"*50)


# ### Glass brain visualization...
# Glass Brain is a tool that maps the electrical activity of your brain in realtime.

# In[ ]:


for file in files:
    subject = os.path.join('../input/trends-assessment-prediction/fMRI_train/', file)
    subject_img = load_subject(subject, mask_img)
    print("Image shape is %s" % (str(subject_img.shape)))
    num_components = subject_img.shape[-1]
    print("Detected {num_components} spatial maps".format(num_components=num_components))
    rsn = subject_img
    #convert to 3d image
    first_rsn = image.index_img(rsn, 0)
    print(first_rsn.shape)     
    plotting.plot_glass_brain(first_rsn,display_mode='lyrz')
    print("-"*50)


# ## Base model

# In[ ]:


def metric(y_true, y_pred):
    return np.mean(np.sum(np.abs(y_true - y_pred), axis=0)/np.sum(y_true, axis=0))


# In[ ]:


"""%%time

NUM_FOLDS = 7
kf = KFold(n_splits=NUM_FOLDS, shuffle=True, random_state=0)


features = loading_features + fnc_features

overal_score = 0

#The weights are [.3, .175, .175, .175, .175] corresponding to features [age, domain1_var1, domain1_var2, domain2_var1, domain2_var2].
for target, c, w in [("age", 100, 0.3), ("domain1_var1", 10, 0.175), ("domain1_var2", 10, 0.175), ("domain2_var1", 10, 0.175), ("domain2_var2", 10, 0.175)]:    
    y_oof = np.zeros(train_data.shape[0])
    y_test = np.zeros((test_data.shape[0], NUM_FOLDS))
    
    #consider gridsearchcv for doing the following :)
    for f, (train_ind, val_ind) in enumerate(kf.split(train_data, train_data)):
        train_df, val_df = train_data.iloc[train_ind], train_data.iloc[val_ind]
        train_df = train_df[train_df[target].notnull()]

        model = SVR(C=c, cache_size=3000.0)
        model.fit(train_df[features], train_df[target])

        y_oof[val_ind] = model.predict(val_df[features])
        y_test[:, f] = model.predict(test_data[features])
        
    train_data["pred_{}".format(target)] = y_oof
    test_data[target] = y_test.mean(axis=1)
    
    score = metric(train_data[train_data[target].notnull()][target].values, train_data[train_data[target].notnull()]["pred_{}".format(target)].values)
    overal_score += w * score
    print(target, np.round(score, 4))
    print()
    
print("Overal score:", np.round(overal_score, 4))"""


# In[ ]:


"""sub_df = pd.melt(test_data[["Id", "age", "domain1_var1", "domain1_var2", "domain2_var1", "domain2_var2"]], id_vars=["Id"], value_name="Predicted")
sub_df["Id"] = sub_df["Id"].astype("str") + "_" +  sub_df["variable"].astype("str")

sub_df = sub_df.drop("variable", axis=1).sort_values("Id") 
assert sub_df.shape[0] == test_data.shape[0]*5
sub_df.head(10)"""


# In[ ]:


"""sub_df.to_csv("submission.csv", index = False)"""


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




