#!/usr/bin/env python
# coding: utf-8

# # overview
# of different clustering - classifier combinations and efficiency
# 
# so with this information, the maximum accuracy should hoover approx 98.6%
# 
# the most difficult point is having a good confusion matrix for class 2 and 4

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import seaborn as sn

train = pd.read_csv("../input/mitbih-arrhythmia-database-de-chazal-class-labels/DS1_signals.csv", header=None)
labels = pd.read_csv("../input/mitbih-arrhythmia-database-de-chazal-class-labels//DS1_labels.csv", header=None)
test = pd.read_csv("../input/mitbih-arrhythmia-database-de-chazal-class-labels/DS2_signals.csv", header=None)
labels2 = pd.read_csv("../input/mitbih-arrhythmia-database-de-chazal-class-labels//DS2_labels.csv", header=None)

train['arrhytmia']=labels[0]
test['arrhytmia']=labels2[0]
total=train.append(test)


# In[ ]:


total


# In[ ]:


def clustertechniques2(dtrain,label,indexv):
    print('#encodings',dtrain.shape)
    cols=[ci for ci in dtrain.columns if ci not in [indexv,'index',label]]
    dtest=dtrain[dtrain[label].isnull()==True][[indexv,label]]
    print(dtest)
    #split data or use splitted data
    X_train=dtrain[dtrain[label].isnull()==False].drop([indexv,label],axis=1).fillna(0)
    Y_train=dtrain[dtrain[label].isnull()==False][label]
    X_test=dtrain[dtrain[label].isnull()==True].drop([indexv,label],axis=1).fillna(0)
    Y_test=np.random.random((X_test.shape[0],1))
    if len(X_test)==0:
        from sklearn.model_selection import train_test_split
        X_train,X_test,Y_train,Y_test = train_test_split(dtrain.drop(label,axis=1).fillna(0),dtrain[label],test_size=0.25,random_state=0)
    lenxtr=len(X_train)
    print('splitting data train test X-y',X_train.shape,Y_train.shape,X_test.shape,Y_test.shape)
   


    import matplotlib.pyplot as plt 
    from sklearn import preprocessing
    scale = preprocessing.MinMaxScaler().fit(X_train)
    X_train = scale.transform(X_train)
    X_test = scale.transform(X_test)

    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.neighbors import KNeighborsClassifier,NeighborhoodComponentsAnalysis
    from sklearn.decomposition import PCA,TruncatedSVD,NMF,FastICA
    from umap import UMAP  # knn lookalike of tSNE but faster, so scales up
    from sklearn.manifold import TSNE #limit number of records to 100000

    clusters = [TruncatedSVD(n_components=20, n_iter=7, random_state=42),
                Dummy(1),
                FastICA(n_components=7,random_state=0),
                 ] 
    clunaam=['tSVD','raw','ICA']
    
    
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC, LinearSVC,NuSVC
    from sklearn.multiclass import OneVsRestClassifier
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier,ExtraTreesClassifier, AdaBoostClassifier, GradientBoostingClassifier
    from sklearn.neural_network import MLPClassifier,MLPRegressor
    from sklearn.linear_model import PassiveAggressiveClassifier,Perceptron,SGDClassifier,LogisticRegression
    import xgboost as xgb
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
    
    classifiers = [KNeighborsClassifier(n_neighbors=5,n_jobs=-1),
                   RandomForestClassifier(n_estimators=100, random_state=42,n_jobs=-1, oob_score=True),
                   ExtraTreesClassifier(n_estimators=10, max_depth=50, min_samples_split=5, min_samples_leaf=1, random_state=None, min_impurity_decrease=1e-7),
                   xgb.XGBClassifier(n_estimators=50, max_depth = 9, learning_rate=0.01, subsample=0.75, random_state=11),
                   DecisionTreeClassifier(),
                  ]
    clanaam= ['KNN','rFor','Xtr','xgb','Decis']
    from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
    
    results=[]


    #cluster data
    for clu in clusters:
        clunm=clunaam[clusters.index(clu)] #find naam
        X_total_clu = clu.fit_transform(np.concatenate( (X_train,X_test),axis=0))
        X_total_clu = np.concatenate( (X_total_clu,np.concatenate( (X_train,X_test),axis=0)), axis=1)
        plt.scatter(X_total_clu[:lenxtr,0],X_total_clu[:lenxtr,1],c=Y_train.values,cmap='prism')
        plt.title(clu)
        plt.show()
        
        #classifiy 
        for cla in classifiers:
            import datetime
            start = datetime.datetime.now()
            clanm=clanaam[classifiers.index(cla)] #find naam
            
            print('    ',cla)
            #cla.fit(X_total_clu,np.concatenate( (Y_train,Y_test)) )
            cla.fit(X_total_clu[:lenxtr],Y_train )
            
            #predict
            trainpredi=cla.predict(X_total_clu[:lenxtr])

            print(classification_report(trainpredi,Y_train))            
            testpredi=cla.predict(X_total_clu[lenxtr:])  
            if classifiers.index(cla) in [0,2,3,4,5,7,8,9,10,11,12,13]:
                trainprediprob=cla.predict_proba(X_total_clu[:lenxtr])
                testprediprob=cla.predict_proba(X_total_clu[lenxtr:]) 
                plt.scatter(x=testprediprob[:,1], y=testpredi, marker='.', alpha=0.3)
                plt.show()            
            #testpredi=converging(pd.DataFrame(X_train),pd.DataFrame(X_test),Y_train,pd.DataFrame(testpredi),Y_test,clu,cla) #PCA(n_components=10,random_state=0,whiten=True),MLPClassifier(alpha=0.510,activation='logistic'))
            
            if len(dtest)==0:
                test_score=cla.score(X_total_clu[lenxtr:],Y_test)
                accscore=accuracy_score(testpredi,Y_test)
                
                train_score=cla.score(X_total_clu[:lenxtr],Y_train)

                li = [clunm,clanm,train_score,accscore]
                results.append(li)                
                print(confusion_matrix(testpredi,Y_test))

                plt.title(clanm+'test accuracy versus unknown:'+np.str(test_score)+' '+np.str(accscore)+' and test confusionmatrix')
                plt.scatter(x=Y_test, y=testpredi, marker='.', alpha=1)
                plt.scatter(x=[np.mean(Y_test)], y=[np.mean(testpredi)], marker='o', color='red')
                plt.xlabel('Real test'); plt.ylabel('Pred. test')
                plt.show()


            else:
#                testpredlabel=le.inverse_transform(testpredi)  #use if you labellezid the classes 
                testpredlabel=testpredi
                print(confusion_matrix(trainpredi,Y_train))
                submit = pd.DataFrame({indexv: dtest[indexv],label: testpredlabel})
                submit[label]=submit[label].astype('int')

                filenaam='subm_'+clunm+'_'+clanm+'.csv'
                submit.to_csv(path_or_buf =filenaam, index=False)
                
            print(clanm,'0 classifier time',datetime.datetime.now()-start)
            
    if len(dtest)==0:       
        print(pd.DataFrame(results).sort_values(3))
        submit=[]
    return submit

#Custom Transformer that extracts columns passed as argument to its constructor 
class Dummy( ):
    #Class Constructor 
    def __init__( self, feature_names ):
        self._feature_names = feature_names 
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def fit_transform( self, X, y = None ):
        return X 

clustertechniques2(total.reset_index(),'arrhytmia','index') 

