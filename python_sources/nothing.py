import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from scipy.linalg import sqrtm
from copy import deepcopy
from sklearn.cluster import MiniBatchKMeans


usecols1 = ['fecha_dato', 'ncodpers', 'ind_ahor_fin_ult1', 'ind_aval_fin_ult1', 'ind_cco_fin_ult1',
       'ind_cder_fin_ult1', 'ind_cno_fin_ult1', 'ind_ctju_fin_ult1',
       'ind_ctma_fin_ult1', 'ind_ctop_fin_ult1', 'ind_ctpp_fin_ult1',
       'ind_deco_fin_ult1', 'ind_deme_fin_ult1', 'ind_dela_fin_ult1',
       'ind_ecue_fin_ult1', 'ind_fond_fin_ult1', 'ind_hip_fin_ult1',
       'ind_plan_fin_ult1', 'ind_pres_fin_ult1', 'ind_reca_fin_ult1',
       'ind_tjcr_fin_ult1', 'ind_valo_fin_ult1', 'ind_viv_fin_ult1',
       'ind_nomina_ult1', 'ind_nom_pens_ult1', 'ind_recibo_ult1']

train = pd.read_csv("../input/train_ver2.csv", usecols=usecols1)
train1 = train[train['fecha_dato']=="2016-05-28"].drop("fecha_dato", axis = 1)
train2 = train[train['fecha_dato']=="2016-04-28"].drop("fecha_dato", axis = 1)
#train3 = train[train['fecha_dato']=="2016-03-28"].drop("fecha_dato", axis = 1)


true = deepcopy(train1)
#############################################################################

test = pd.read_csv("../input/test_ver2.csv")
test = test[['ncodpers']]

#test.to_csv("test.csv", index=False)
#test = test[['ncodpers']]

print("datasets loaded")
#############################################################################

users = true['ncodpers'].tolist()
true.drop('ncodpers', axis=1, inplace=True)

items = true.columns.tolist()
u = {}
for i in range(len(users)):
    u[users[i]] = i

trueMat = np.array(true)
print("users dict formed")

############################################################################

def reorder(train):
    train.index = train['ncodpers'].tolist()
    train.drop('ncodpers', axis=1, inplace=True)
    train = train.reindex(users)
    return train

#train3 = reorder(train3)
train2 = reorder(train2)
train1 = reorder(train1)

###################### kPOD ##############################

def kpod(utilMat, mask, iter=40, n_clusters=3, method='transpose'):

    if method=='transpose':
        utilMat = np.transpose(utilMat)
        mask = np.transpose(mask)

    #print mask
    #print utilMat

    for ii in range(iter):
        print(ii)
        cls = MiniBatchKMeans(n_clusters=n_clusters, n_init=4)
        labels_hat = cls.fit_predict(utilMat)

        #utilMat = mask.filled(cls.cluster_centers_[labels_hat])

        for jj in range(len(labels_hat)):
            c = labels_hat[jj]
            utilMat[jj, :] = mask[jj, :].filled(cls.cluster_centers_[c])

    del mask
    cluster_indices = [ [] for i in range(n_clusters) ]
    for i in range(len(labels_hat)):
        cluster_indices[labels_hat[i]].append(i)

    for i in range(n_clusters):
        print(len(cluster_indices[i]))

    if method=='transpose':
        utilMat = np.transpose(utilMat)

    return utilMat


###################### COMPUTING THE SVD ##########################

def svd(train, trueMat, k):
    utilMat = np.array(train)

    masked_arr = np.ma.masked_where(utilMat==0,utilMat)
    item_means = np.mean(masked_arr, axis=0)
    #utilMat = masked_arr.filled(item_means)
    print(utilMat)
    #x = np.tile(item_means, (utilMat.shape[0],1))
    utilMat = kpod(utilMat=utilMat, mask=masked_arr, iter=24, n_clusters=20, method="normal")

    print(utilMat)
    
    item_means=np.mean(utilMat, axis=0)
    item_means_tiled = np.tile(item_means, (utilMat.shape[0],1))

    utilMat = utilMat - item_means_tiled
    
    U, s, V=np.linalg.svd(utilMat, full_matrices=False)
    s=np.diag(s)
    s=s[0:k,0:k]
    U=U[:,0:k]
    V=V[0:k,:]

    s_root=sqrtm(s)

    Usk=np.dot(U,s_root)
    skV=np.dot(s_root,V)
    UsV = np.dot(Usk, skV)

    UsV = UsV + item_means_tiled

    UsV = np.ma.masked_where(trueMat==1,UsV).filled(fill_value=-999)

    #print(UsV)
    print("svd done")
    return UsV

######################### PREDICTION #################################

def max_items(UsV,x,j):
    out = []

    for xx in x:
        if UsV[j,xx]>0.001: # setting a threshold
            out.append(items[xx])

    return out

def recommend(test):

    UsV = svd(train=train1,trueMat=trueMat,k=3)
    
    pred = []
    testusers = test['ncodpers'].tolist()

    n = 7
    for user in testusers[:]:
        j = u[user]
        p = max_items(UsV, UsV[j,:].argsort()[-n:][::-1], j)
        pred.append(" ".join(p))
        print(len(p))
    test['added_products'] = pred
    test.to_csv('sub.csv', index=False)


recommend(test)
##################################################################