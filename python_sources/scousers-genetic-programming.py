#!/usr/bin/env python
# coding: utf-8

# A quick GP predictor.
# Two warnings:
# It was only trained on 10% of the training data (train[::10])
# I used a savgol_filter to conservatively clip the signal to try and eliminate drift - this reduces the score slightly

# In[ ]:


from statsmodels.robust import mad
import matplotlib.pyplot as plt
from scipy.signal import butter
from scipy import signal
from scipy.signal import savgol_filter
import seaborn as sns
from sklearn import *
import pandas as pd 
import numpy as np
import warnings
import scipy
import pywt
import os
import gc
from sklearn.metrics import f1_score
plt.style.use('ggplot')
sns.set_style('darkgrid')


# In[ ]:


class GP:
    def __init__(self):
        self.classes = 11
        self.class_names = [ 'class_0',
                             'class_1',
                             'class_2',
                             'class_3',
                             'class_4',
                             'class_5',
                             'class_6',
                             'class_7',
                             'class_8',
                             'class_9',
                             'class_10']


    def GrabPredictions(self, data):
        oof_preds = np.zeros((len(data), len(self.class_names)))
        oof_preds[:,0] = self.GP_class_0(data)
        oof_preds[:,1] = self.GP_class_1(data)
        oof_preds[:,2] = self.GP_class_2(data)
        oof_preds[:,3] = self.GP_class_3(data)
        oof_preds[:,4] = self.GP_class_4(data)
        oof_preds[:,5] = self.GP_class_5(data)
        oof_preds[:,6] = self.GP_class_6(data)
        oof_preds[:,7] = self.GP_class_7(data)
        oof_preds[:,8] = self.GP_class_8(data)
        oof_preds[:,9] = self.GP_class_9(data)
        oof_preds[:,10] = self.GP_class_10(data)
        oof_df = pd.DataFrame(oof_preds, columns=self.class_names)
        oof_df =oof_df.div(oof_df.sum(axis=1), axis=0)
        return oof_df

    def Output(self, p):
        return 1.0/(1.0+np.exp(-p))
   
    def GP_class_0(self,data):
        return self.Output( -1.394065 +
                            0.100000*np.tanh(((((data["abs_avgbatch_msignal"]) + (((data["minbatch_msignal"]) + (data["abs_minbatch_slices2_msignal"]))))) + (np.where(data["minbatch_msignal"] > -998, ((data["minbatch_slices2_msignal"]) + (data["minbatch_msignal"])), data["mean_abs_chgbatch_msignal"] )))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2_msignal"] > -998, ((((data["minbatch_msignal"]) * 2.0)) + (np.where(((((((data["mean_abs_chgbatch_slices2_msignal"]) - (data["signal_shift_-1"]))) * 2.0)) * 2.0) <= -998, data["signal_shift_+1"], data["abs_avgbatch_msignal"] ))), data["signal_shift_-1"] )) +
                            0.100000*np.tanh(((((data["minbatch_slices2_msignal"]) + (((data["minbatch_slices2_msignal"]) + (((np.where(data["abs_avgbatch_msignal"] > -998, data["abs_minbatch_slices2_msignal"], ((data["abs_avgbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"])) )) * 2.0)))))) + (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) + ((((data["abs_minbatch_msignal"]) + (data["meanbatch_slices2"]))/2.0)))) + (((((np.where(data["stdbatch_slices2_msignal"] > -998, data["minbatch_msignal"], data["minbatch_slices2_msignal"] )) + (data["abs_minbatch_msignal"]))) * 2.0)))) +
                            0.100000*np.tanh(((np.tanh((((data["minbatch_slices2_msignal"]) / 2.0)))) + (((data["minbatch_slices2_msignal"]) + (data["abs_minbatch_msignal"]))))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(((data["abs_minbatch_msignal"]) + (data["abs_minbatch_msignal"])) <= -998, data["minbatch_msignal"], ((((((data["minbatch_msignal"]) + (data["abs_minbatch_msignal"]))) * 2.0)) + (data["minbatch_msignal"])) )) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_msignal"] > -998, np.where(data["minbatch_msignal"] <= -998, data["abs_minbatch_msignal"], ((data["abs_minbatch_slices2_msignal"]) * 2.0) ), data["maxtominbatch_msignal"] )) +
                            0.100000*np.tanh(((((data["minbatch_slices2_msignal"]) + (data["abs_minbatch_slices2_msignal"]))) + (data["maxtominbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((((data["minbatch_msignal"]) + (data["abs_avgbatch_msignal"]))) + (((((data["minbatch_slices2_msignal"]) + (np.where(((data["maxtominbatch_slices2_msignal"]) + (((data["minbatch_msignal"]) * 2.0))) > -998, data["maxtominbatch_slices2_msignal"], data["maxtominbatch_msignal"] )))) * 2.0)))/2.0)) +
                            0.100000*np.tanh(((np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, ((data["maxbatch_msignal"]) + (data["minbatch_msignal"])), np.where(data["maxbatch_msignal"] <= -998, ((data["maxbatch_msignal"]) + (data["minbatch_msignal"])), ((data["maxbatch_msignal"]) + (data["minbatch_msignal"])) ) )) * 2.0)) +
                            0.100000*np.tanh((((data["minbatch_slices2_msignal"]) + (data["maxtominbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(((((data["stdbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))) + (np.where(data["abs_minbatch_msignal"] > -998, ((data["abs_minbatch_slices2_msignal"]) + (((data["medianbatch_msignal"]) + (data["minbatch"])))), data["abs_minbatch_msignal"] )))) +
                            0.100000*np.tanh(((((data["minbatch_slices2_msignal"]) + ((2.0)))) + (((data["minbatch_slices2_msignal"]) + ((((data["maxtominbatch_msignal"]) + (((((data["rangebatch_slices2_msignal"]) / 2.0)) + (data["minbatch_slices2_msignal"]))))/2.0)))))) +
                            0.100000*np.tanh(((((data["maxbatch_msignal"]) + (np.where(data["abs_avgbatch_slices2"] <= -998, ((data["maxbatch_msignal"]) + (((data["mean_abs_chgbatch_msignal"]) + (data["abs_minbatch_slices2_msignal"])))), data["minbatch_msignal"] )))) * 2.0)) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) + (data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_msignal"] <= -998, data["abs_maxbatch_slices2_msignal"], ((data["maxtominbatch_slices2_msignal"]) + (data["minbatch_msignal"])) )) +
                            0.100000*np.tanh(((((np.where(data["abs_minbatch_msignal"] <= -998, data["minbatch_msignal"], data["minbatch_slices2_msignal"] )) + (((data["minbatch_msignal"]) + ((((6.0)) / 2.0)))))) + ((((6.0)) + (((data["minbatch_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh(((np.where(data["abs_minbatch_slices2"] <= -998, data["abs_avgbatch_slices2_msignal"], ((data["abs_avgbatch_msignal"]) * 2.0) )) * 2.0)) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((((data["minbatch_msignal"]) + (((((7.0)) + (data["minbatch"]))/2.0)))) + (data["mean_abs_chgbatch_msignal"]))))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - (((((data["minbatch_msignal"]) * (np.where((11.18674182891845703) <= -998, np.where(data["minbatch_slices2_msignal"] <= -998, data["minbatch_msignal"], data["maxbatch_msignal"] ), data["minbatch_slices2_msignal"] )))) / 2.0)))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((data["minbatch_slices2_msignal"]) + ((((data["abs_avgbatch_slices2_msignal"]) + ((5.0)))/2.0)))))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((((data["minbatch_slices2_msignal"]) + (np.where(data["minbatch_slices2_msignal"] > -998, ((data["minbatch_slices2_msignal"]) + ((4.0))), (4.0) )))) * 2.0)))) +
                            0.100000*np.tanh(((((data["minbatch_slices2_msignal"]) + ((4.0)))) + (np.where((((((data["minbatch_msignal"]) * (data["abs_avgbatch_msignal"]))) + (data["abs_maxbatch_slices2_msignal"]))/2.0) > -998, data["minbatch_slices2_msignal"], (((data["minbatch_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0) )))) +
                            0.100000*np.tanh(((((((data["minbatch_msignal"]) + ((1.75699043273925781)))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) + (data["meanbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((data["minbatch_slices2_msignal"]) + ((((data["abs_minbatch_slices2"]) + (np.where((6.18558311462402344) > -998, (6.18558311462402344), np.where(data["minbatch_slices2_msignal"] > -998, data["maxtominbatch_msignal"], data["minbatch_slices2_msignal"] ) )))/2.0)))))) +
                            0.100000*np.tanh(np.where((((2.0)) + ((2.0))) > -998, ((((data["minbatch_slices2_msignal"]) + ((2.0)))) * 2.0), ((((((10.14909553527832031)) / 2.0)) + ((((((2.0)) * 2.0)) * 2.0)))/2.0) )) +
                            0.100000*np.tanh(((((((((data["minbatch_slices2_msignal"]) * 2.0)) + (data["maxbatch_msignal"]))) + (((data["abs_maxbatch"]) + (data["maxbatch_msignal"]))))) + (data["maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((np.where(data["maxbatch_msignal"] > -998, ((data["minbatch_slices2_msignal"]) + (data["maxbatch_msignal"])), np.where(data["minbatch_msignal"] <= -998, data["abs_maxbatch_msignal"], data["maxbatch_msignal"] ) )) * (((data["maxbatch_msignal"]) + (data["rangebatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((data["minbatch_msignal"]) + (np.where(data["maxbatch_slices2_msignal"] <= -998, data["maxbatch_slices2_msignal"], (4.0) )))))) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2_msignal"] > -998, ((data["abs_avgbatch_msignal"]) * 2.0), data["abs_avgbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + ((3.0)))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where(data["minbatch_slices2_msignal"] > -998, data["maxbatch_msignal"], data["maxbatch_msignal"] )))) +
                            0.100000*np.tanh(((((((((data["minbatch_slices2_msignal"]) * 2.0)) + ((((((3.0)) + (data["minbatch_msignal"]))) * 2.0)))) * 2.0)) + ((((3.0)) * 2.0)))) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] > -998, (3.0), data["maxbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((6.07105970382690430)) + (np.where((6.07105970382690430) <= -998, data["minbatch_msignal"], ((data["abs_maxbatch"]) * (data["minbatch_msignal"])) )))) +
                            0.100000*np.tanh(((((np.where(data["minbatch_slices2_msignal"] <= -998, data["minbatch_slices2_msignal"], ((data["minbatch_slices2_msignal"]) + (data["minbatch_msignal"])) )) * 2.0)) + ((6.36680364608764648)))) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_slices2"] > -998, ((data["abs_maxbatch_slices2"]) + (data["minbatch_slices2_msignal"])), data["abs_maxbatch_msignal"] )) +
                            0.100000*np.tanh(((((np.where((((8.0)) * ((2.0))) > -998, (8.0), data["abs_maxbatch_slices2_msignal"] )) * ((((data["minbatch_slices2_msignal"]) + ((2.0)))/2.0)))) - ((2.0)))) +
                            0.100000*np.tanh(data["maxtominbatch_msignal"]) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) + (np.where((14.34354209899902344) > -998, data["abs_avgbatch_msignal"], ((((data["meanbatch_slices2_msignal"]) + (((data["maxbatch_msignal"]) * 2.0)))) * 2.0) )))) * 2.0)) +
                            0.100000*np.tanh(((((((5.0)) + ((-(((((data["rangebatch_slices2"]) + (np.where(((((((5.75685548782348633)) + (data["meanbatch_slices2_msignal"]))/2.0)) * (data["maxbatch_msignal"])) > -998, data["rangebatch_slices2"], data["meanbatch_slices2_msignal"] )))/2.0))))))/2.0)) * 2.0)) +
                            0.100000*np.tanh(((((((((14.40077304840087891)) + (((data["rangebatch_msignal"]) * 2.0)))) + (data["maxbatch_msignal"]))/2.0)) + (data["rangebatch_msignal"]))) +
                            0.100000*np.tanh(((np.where(((data["minbatch_msignal"]) + (((data["minbatch_msignal"]) * ((8.0))))) > -998, (8.0), data["minbatch_msignal"] )) + (((data["abs_maxbatch_msignal"]) * (data["minbatch_msignal"]))))) +
                            0.100000*np.tanh(((((data["abs_maxbatch_msignal"]) * (data["minbatch_slices2_msignal"]))) + ((7.0)))) +
                            0.100000*np.tanh((9.0)) +
                            0.100000*np.tanh((((((data["abs_avgbatch_slices2"]) + (((np.where(data["abs_maxbatch"] > -998, ((data["rangebatch_slices2_msignal"]) * (data["minbatch_slices2_msignal"])), data["abs_maxbatch"] )) + ((((((data["rangebatch_slices2_msignal"]) * 2.0)) + (data["abs_avgbatch_slices2"]))/2.0)))))/2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where((((12.98433399200439453)) * 2.0) <= -998, ((data["medianbatch_msignal"]) / 2.0), data["maxbatch_msignal"] )) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * ((10.0)))) +
                            0.100000*np.tanh(((((((((data["minbatch_slices2_msignal"]) * (((data["abs_maxbatch"]) * 2.0)))) + (((data["rangebatch_msignal"]) / 2.0)))) * 2.0)) + ((((((7.03666973114013672)) * 2.0)) + (((data["minbatch_slices2"]) * 2.0)))))) +
                            0.100000*np.tanh(np.where((3.87161946296691895) <= -998, data["minbatch_msignal"], ((((((7.37184619903564453)) / 2.0)) + (data["minbatch_msignal"]))/2.0) )) +
                            0.100000*np.tanh((((5.46549940109252930)) + (((((((data["abs_maxbatch"]) * (data["minbatch_slices2_msignal"]))) / 2.0)) * (data["abs_maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((5.0)) + (((data["minbatch_msignal"]) + (np.where(data["maxbatch_msignal"] > -998, (((data["abs_maxbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"]))/2.0), ((((data["maxbatch_msignal"]) + (data["minbatch_msignal"]))) + ((4.31423044204711914))) )))))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (np.where((6.0) > -998, data["maxbatch_msignal"], data["meanbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(data["abs_maxbatch_msignal"]) +
                            0.100000*np.tanh(((((((((data["abs_maxbatch_msignal"]) + (data["abs_maxbatch_msignal"]))/2.0)) * 2.0)) + ((((11.79059314727783203)) * 2.0)))/2.0)) +
                            0.100000*np.tanh((((((3.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((((5.0)) + (((data["abs_maxbatch_slices2_msignal"]) * (data["minbatch_msignal"]))))/2.0)) * ((4.0)))) +
                            0.100000*np.tanh((((((7.0)) + (data["abs_avgbatch_slices2"]))) + (((data["minbatch_slices2_msignal"]) * (np.where((8.0) <= -998, (8.0), data["rangebatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(np.where((4.50527191162109375) <= -998, data["abs_maxbatch_slices2"], ((((((12.67150592803955078)) / 2.0)) + ((4.50527191162109375)))/2.0) )) +
                            0.100000*np.tanh((((((data["rangebatch_slices2"]) * (data["minbatch"]))) + ((((((4.27161550521850586)) / 2.0)) + (((np.where((10.0) <= -998, (4.27161550521850586), (4.27161550521850586) )) + ((4.27161550521850586)))))))/2.0)) +
                            0.100000*np.tanh(((((data["minbatch_slices2_msignal"]) * (data["rangebatch_slices2"]))) - ((((data["maxbatch_slices2_msignal"]) + (np.where(data["rangebatch_slices2"] > -998, (-(((9.0)))), ((data["maxbatch_msignal"]) + (data["minbatch_slices2_msignal"])) )))/2.0)))) +
                            0.100000*np.tanh(((((np.where(data["abs_avgbatch_slices2_msignal"] > -998, ((data["abs_avgbatch_slices2_msignal"]) * 2.0), ((np.where(((((data["abs_avgbatch_slices2_msignal"]) * 2.0)) * 2.0) > -998, (3.77810692787170410), data["abs_avgbatch_slices2_msignal"] )) * 2.0) )) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(((data["maxbatch_msignal"]) * 2.0) > -998, (((7.0)) - (((data["rangebatch_slices2_msignal"]) - (((data["minbatch_slices2_msignal"]) * 2.0))))), data["abs_avgbatch_msignal"] )) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((data["minbatch_msignal"]) + (np.where((((data["stdbatch_slices2"]) + ((((-((data["minbatch_msignal"])))) + (((((4.12169790267944336)) + ((((3.92451262474060059)) / 2.0)))/2.0)))))/2.0) > -998, (4.12169790267944336), data["abs_avgbatch_slices2"] )))/2.0)) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) + (np.where(data["medianbatch_slices2_msignal"] > -998, data["minbatch_msignal"], (((3.32866501808166504)) / 2.0) )))) +
                            0.100000*np.tanh(np.where((3.53696203231811523) > -998, (((((3.53696203231811523)) - (np.where((3.53696203231811523) > -998, data["rangebatch_slices2"], data["rangebatch_slices2"] )))) * 2.0), data["maxbatch_msignal"] )) +
                            0.100000*np.tanh((10.0)) +
                            0.100000*np.tanh(data["abs_maxbatch"]) +
                            0.100000*np.tanh((((((((5.0)) + ((((data["abs_avgbatch_slices2_msignal"]) + (data["minbatch_msignal"]))/2.0)))/2.0)) + (data["minbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) * 2.0)) + (np.where((9.03761196136474609) > -998, data["signal_shift_+1"], (9.03761196136474609) )))) +
                            0.100000*np.tanh(((((((((((data["minbatch_slices2_msignal"]) + (data["maxbatch_msignal"]))) + (data["stdbatch_slices2"]))/2.0)) + ((8.0)))/2.0)) + (data["stdbatch_slices2"]))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where(data["maxbatch_msignal"] <= -998, (-(((7.57825469970703125)))), (((7.57825469970703125)) - (((data["rangebatch_slices2"]) * 2.0))) )))) +
                            0.100000*np.tanh(((((5.0)) + (np.where((5.0) <= -998, (((((5.0)) - (data["rangebatch_slices2"]))) + (data["abs_avgbatch_slices2_msignal"])), (((5.0)) - (data["rangebatch_slices2"])) )))/2.0)) +
                            0.100000*np.tanh(((((np.tanh((((data["abs_maxbatch_slices2"]) * (data["abs_avgbatch_slices2_msignal"]))))) * 2.0)) + (data["maxtominbatch_slices2"]))) +
                            0.100000*np.tanh((((np.where(data["abs_minbatch_slices2"] <= -998, data["rangebatch_slices2"], data["minbatch_slices2_msignal"] )) + (np.where((-((((data["rangebatch_slices2"]) + (data["meanbatch_slices2_msignal"]))))) > -998, (4.0), data["abs_maxbatch"] )))/2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) + (((((data["minbatch_msignal"]) + (((np.tanh((data["abs_maxbatch_msignal"]))) * 2.0)))) + (((data["minbatch_slices2_msignal"]) * (data["abs_maxbatch_msignal"]))))))) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch"] <= -998, data["rangebatch_slices2"], data["rangebatch_msignal"] )) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] <= -998, np.where((2.0) > -998, (2.0), data["minbatch_slices2_msignal"] ), ((((data["minbatch_slices2_msignal"]) + ((2.0)))) * 2.0) )) +
                            0.100000*np.tanh(np.where(data["rangebatch_msignal"] > -998, ((data["rangebatch_slices2"]) * 2.0), data["maxbatch_msignal"] )) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) + (((np.where(np.where(data["medianbatch_slices2_msignal"] > -998, (-((np.where(data["maxbatch_msignal"] <= -998, data["meanbatch_slices2"], data["meanbatch_msignal"] )))), data["maxbatch_msignal"] ) > -998, data["abs_avgbatch_slices2_msignal"], data["abs_maxbatch_slices2"] )) * 2.0)))) +
                            0.100000*np.tanh((((((data["rangebatch_slices2"]) + ((4.0)))/2.0)) * ((((4.0)) - ((((data["rangebatch_slices2"]) + (data["rangebatch_slices2"]))/2.0)))))) +
                            0.100000*np.tanh((-((((((((data["stdbatch_slices2"]) * (data["abs_maxbatch_msignal"]))) * (np.where((6.15387201309204102) > -998, data["abs_avgbatch_slices2_msignal"], (6.15387201309204102) )))) - ((10.0))))))) +
                            0.100000*np.tanh(((((data["abs_avgbatch_msignal"]) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((np.where(data["maxbatch_slices2_msignal"] <= -998, data["signal_shift_+1_msignal"], (6.77088403701782227) )) - (data["abs_maxbatch_slices2"]))))) +
                            0.100000*np.tanh(np.where(((data["minbatch_msignal"]) / 2.0) > -998, ((data["minbatch_msignal"]) + ((((data["minbatch_msignal"]) + ((6.0)))/2.0))), ((((data["abs_maxbatch"]) + (data["minbatch"]))) + ((7.0))) )) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) * (((np.where(data["minbatch_slices2_msignal"] > -998, data["minbatch_slices2_msignal"], ((np.where(data["abs_maxbatch_msignal"] > -998, data["minbatch_slices2_msignal"], data["abs_maxbatch_msignal"] )) / 2.0) )) + (data["maxbatch_msignal"]))))) +
                            0.100000*np.tanh(((((((data["abs_maxbatch_slices2_msignal"]) + (np.where(data["abs_maxbatch_msignal"] > -998, (5.62084245681762695), data["abs_maxbatch_slices2_msignal"] )))) + (data["minbatch_msignal"]))) - (((data["abs_maxbatch_msignal"]) * ((-((data["minbatch_msignal"])))))))) +
                            0.100000*np.tanh((((((10.0)) - (((((data["minbatch_slices2_msignal"]) / 2.0)) + (data["rangebatch_slices2"]))))) + (((np.where(data["rangebatch_slices2"] <= -998, data["rangebatch_slices2"], (4.0) )) * (data["minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((((data["minbatch"]) * (data["abs_maxbatch"]))) + ((7.22241830825805664)))/2.0)) +
                            0.100000*np.tanh((((((10.0)) * ((((10.13583469390869141)) + ((((8.0)) * (data["minbatch_slices2_msignal"]))))))) + ((((((((10.0)) + (data["minbatch_slices2_msignal"]))) * 2.0)) + (data["minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2"] > -998, (((6.0)) - (data["rangebatch_slices2"])), (((((data["rangebatch_slices2"]) + (np.where((6.0) > -998, data["abs_avgbatch_slices2"], data["abs_avgbatch_slices2_msignal"] )))/2.0)) * ((6.0))) )) +
                            0.100000*np.tanh(((data["abs_maxbatch"]) + (((data["abs_minbatch_msignal"]) * (np.where((7.20649671554565430) > -998, data["abs_avgbatch_slices2"], np.tanh(((((14.06450271606445312)) + (((data["minbatch_msignal"]) - (data["minbatch_msignal"])))))) )))))) +
                            0.100000*np.tanh((((13.77110767364501953)) + (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2_msignal"] > -998, data["maxbatch_slices2"], data["minbatch"] )) +
                            0.100000*np.tanh(data["maxbatch_msignal"]) +
                            0.100000*np.tanh(((((data["signal"]) * (np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], np.where(data["signal"] <= -998, data["rangebatch_msignal"], data["signal"] ) )))) * (np.where(data["signal"] > -998, data["abs_maxbatch_slices2"], data["signal"] )))) +
                            0.100000*np.tanh((((data["meanbatch_slices2_msignal"]) + ((9.97540187835693359)))/2.0)) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2"] > -998, ((((data["rangebatch_msignal"]) * 2.0)) * 2.0), data["rangebatch_msignal"] )) +
                            0.100000*np.tanh((((7.53276443481445312)) - (((np.where(data["abs_avgbatch_msignal"] <= -998, np.where(data["maxbatch_slices2"] <= -998, (7.53276443481445312), ((data["mean_abs_chgbatch_slices2_msignal"]) - (((data["abs_avgbatch_msignal"]) + (data["abs_maxbatch_msignal"])))) ), data["abs_maxbatch_msignal"] )) * 2.0)))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where((((data["abs_avgbatch_slices2_msignal"]) + (data["minbatch_slices2"]))/2.0) > -998, data["maxbatch_msignal"], data["maxbatch_msignal"] )))) +
                            0.100000*np.tanh(((((((((((((((data["minbatch_slices2_msignal"]) + (data["maxbatch_msignal"]))) + (data["minbatch_slices2_msignal"]))/2.0)) * 2.0)) * 2.0)) * 2.0)) + (data["minbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh((8.71119499206542969)) +
                            0.100000*np.tanh(((np.where(data["maxbatch_msignal"] <= -998, data["abs_maxbatch_slices2"], data["minbatch_slices2_msignal"] )) + (np.where(data["signal_shift_-1_msignal"] > -998, data["maxbatch_msignal"], ((((data["minbatch_slices2_msignal"]) + (data["maxbatch_msignal"]))) * 2.0) )))) +
                            0.100000*np.tanh(((((((data["abs_maxbatch_slices2"]) + (((data["maxbatch_msignal"]) * 2.0)))) * (((np.tanh((data["maxbatch_msignal"]))) + (data["abs_maxbatch_slices2_msignal"]))))) * ((-((data["signal_shift_-1_msignal"])))))) +
                            0.100000*np.tanh((8.0)) +
                            0.100000*np.tanh(np.where(((data["rangebatch_msignal"]) * 2.0) <= -998, data["signal_shift_+1_msignal"], ((((data["abs_avgbatch_slices2"]) * ((4.0)))) + (data["rangebatch_msignal"])) )) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) + (np.where((((3.0)) * 2.0) <= -998, (((3.0)) + (((data["minbatch_msignal"]) + (data["minbatch_msignal"])))), (3.0) )))) * 2.0)) +
                            0.100000*np.tanh((((((2.0)) + ((((data["maxbatch_msignal"]) + (((((13.07838630676269531)) + ((((((13.07838630676269531)) * (data["minbatch_msignal"]))) + ((-(((2.0))))))))/2.0)))/2.0)))) * 2.0)) +
                            0.100000*np.tanh((((5.07780599594116211)) - (data["rangebatch_slices2"]))) +
                            0.100000*np.tanh((((((((3.0)) * 2.0)) / 2.0)) + (((((data["medianbatch_slices2_msignal"]) * (data["abs_maxbatch"]))) * ((((3.0)) - (np.where((3.0) > -998, data["rangebatch_slices2"], data["abs_maxbatch_slices2_msignal"] )))))))) +
                            0.100000*np.tanh((((data["abs_avgbatch_slices2_msignal"]) + (np.where(data["maxbatch_msignal"] > -998, ((data["abs_maxbatch_slices2_msignal"]) / 2.0), data["mean_abs_chgbatch_slices2"] )))/2.0)) +
                            0.100000*np.tanh(((((((data["minbatch_msignal"]) - (data["signal_shift_-1"]))) * (np.where((-((np.tanh((data["abs_maxbatch"]))))) > -998, data["abs_maxbatch_msignal"], ((data["abs_minbatch_slices2_msignal"]) + (data["abs_maxbatch_slices2"])) )))) * (data["abs_minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((np.where((13.49042701721191406) <= -998, np.where((1.72230756282806396) <= -998, data["abs_maxbatch_msignal"], (6.03513622283935547) ), data["abs_maxbatch_msignal"] )) + (data["minbatch_msignal"]))) +
                            0.100000*np.tanh((((3.89857029914855957)) - (((data["minbatch_msignal"]) * 2.0)))) +
                            0.100000*np.tanh((((9.05197429656982422)) + (((data["minbatch_msignal"]) * (((((((((9.05197429656982422)) + (data["minbatch_msignal"]))) + (data["signal_shift_-1_msignal"]))) + (np.where(data["abs_maxbatch"] > -998, data["abs_maxbatch"], data["mean_abs_chgbatch_slices2_msignal"] )))/2.0)))))) +
                            0.100000*np.tanh(np.where((7.0) <= -998, data["rangebatch_msignal"], (((7.0)) - (data["abs_maxbatch"])) )) +
                            0.100000*np.tanh(((((data["minbatch_slices2"]) + (data["stdbatch_slices2_msignal"]))) * (data["signal_shift_-1_msignal"]))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2_msignal"]) + (((data["maxbatch_msignal"]) + (data["meanbatch_msignal"]))))) + ((4.0)))) +
                            0.100000*np.tanh(np.where(np.tanh((data["abs_maxbatch"])) <= -998, data["rangebatch_slices2_msignal"], data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.where((((5.0)) - (data["rangebatch_slices2"])) > -998, (((5.0)) - (data["rangebatch_slices2"])), data["medianbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((2.90549468994140625)) + (np.where(data["abs_maxbatch_slices2_msignal"] <= -998, ((data["abs_maxbatch_msignal"]) + (data["maxbatch_slices2"])), data["maxbatch_msignal"] )))) +
                            0.100000*np.tanh(((np.where((((data["maxbatch_slices2_msignal"]) + ((((data["medianbatch_slices2_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0)))/2.0) > -998, np.where(data["maxbatch_slices2"] <= -998, data["maxbatch_slices2"], ((data["minbatch_msignal"]) + (data["maxbatch_slices2_msignal"])) ), data["abs_maxbatch_slices2"] )) * 2.0)) +
                            0.100000*np.tanh(data["maxbatch_slices2"]) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) * (((np.where(data["maxbatch_msignal"] > -998, data["maxbatch_msignal"], data["abs_maxbatch_slices2_msignal"] )) * ((((9.0)) - (data["maxbatch_msignal"]))))))) +
                            0.100000*np.tanh(((((data["signal_shift_+1_msignal"]) / 2.0)) + ((((((data["meanbatch_slices2_msignal"]) + ((((-((data["signal_shift_+1_msignal"])))) * 2.0)))/2.0)) * ((((7.0)) + (((data["maxbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))))))))) +
                            0.100000*np.tanh(((((7.85957908630371094)) + (((data["minbatch_msignal"]) * (((data["rangebatch_slices2"]) + (np.tanh(((((((data["medianbatch_slices2_msignal"]) + (data["abs_avgbatch_msignal"]))) + (((data["abs_maxbatch_slices2_msignal"]) * (data["rangebatch_msignal"]))))/2.0)))))))))/2.0)) +
                            0.100000*np.tanh(((((((data["minbatch_slices2_msignal"]) + (np.where(np.where(data["medianbatch_msignal"] <= -998, ((data["maxbatch_msignal"]) / 2.0), data["maxbatch_msignal"] ) <= -998, data["maxbatch_slices2_msignal"], data["maxbatch_msignal"] )))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((((((3.39122486114501953)) * 2.0)) + (data["maxbatch_slices2"]))) +
                            0.100000*np.tanh(np.where((((data["rangebatch_msignal"]) + (((data["meanbatch_slices2_msignal"]) / 2.0)))/2.0) > -998, (((8.59417152404785156)) - (data["maxbatch_msignal"])), (((9.44304466247558594)) * (data["maxtominbatch_msignal"])) )) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) * 2.0)) * (((((((data["maxbatch_msignal"]) * (((data["abs_avgbatch_slices2_msignal"]) * ((((((6.0)) / 2.0)) - (data["maxbatch_slices2_msignal"]))))))) * 2.0)) + ((9.0)))))) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] <= -998, (1.89028906822204590), ((data["minbatch_msignal"]) - (((data["meanbatch_msignal"]) - ((((1.89029264450073242)) * 2.0))))) )) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))) * 2.0)) +
                            0.100000*np.tanh(((np.where(data["mean_abs_chgbatch_slices2"] <= -998, np.where(data["minbatch_msignal"] > -998, ((data["minbatch_msignal"]) + (data["minbatch_msignal"])), data["minbatch_msignal"] ), ((data["minbatch_msignal"]) + (data["maxbatch_slices2_msignal"])) )) * 2.0)) +
                            0.100000*np.tanh((((3.0)) + (((((data["rangebatch_slices2_msignal"]) * (((((data["abs_avgbatch_msignal"]) + (data["abs_maxbatch_msignal"]))) * 2.0)))) * (((data["minbatch_slices2_msignal"]) + (np.tanh(((10.0)))))))))) +
                            0.100000*np.tanh(((((6.0)) + (data["abs_avgbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.where((((data["maxbatch_msignal"]) + (np.where(data["stdbatch_slices2"] > -998, np.tanh(((7.0))), (9.99630165100097656) )))/2.0) <= -998, (1.26823818683624268), ((data["abs_avgbatch_msignal"]) * 2.0) )) +
                            0.100000*np.tanh(data["maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((np.tanh((((((((5.0)) + ((11.45873928070068359)))/2.0)) - ((4.0)))))) + ((((((4.0)) * 2.0)) + ((((-((data["signal_shift_+1"])))) * 2.0)))))) +
                            0.100000*np.tanh((((3.0)) * (data["abs_avgbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(((data["abs_avgbatch_msignal"]) - ((9.0))) <= -998, ((data["abs_maxbatch_msignal"]) + (np.tanh(((9.0))))), (3.0) )) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + ((((2.53492069244384766)) - (data["signal_shift_-1_msignal"]))))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2"]) + (data["rangebatch_slices2"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (((data["signal"]) + (((data["minbatch_slices2"]) + (data["minbatch"]))))))) +
                            0.100000*np.tanh((((((((((data["abs_avgbatch_slices2"]) * 2.0)) * 2.0)) + ((5.40367650985717773)))/2.0)) * (((((np.where(data["signal"] <= -998, ((data["meanbatch_slices2_msignal"]) * 2.0), data["medianbatch_slices2_msignal"] )) * (data["signal"]))) * 2.0)))) +
                            0.100000*np.tanh(((((((((data["minbatch_msignal"]) + (data["maxbatch_slices2_msignal"]))) * 2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((((((((8.0)) + (data["meanbatch_slices2_msignal"]))) / 2.0)) * 2.0)) +
                            0.100000*np.tanh((((5.0)) - (np.where(np.where(np.tanh(((5.0))) > -998, (6.31894254684448242), data["rangebatch_slices2"] ) <= -998, data["rangebatch_slices2"], data["rangebatch_slices2"] )))) +
                            0.100000*np.tanh(((((((((data["maxbatch_msignal"]) + ((4.0)))) + (((((data["minbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"]))) + ((-((data["signal_shift_+1_msignal"])))))))) * 2.0)) - (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh((((((((data["abs_maxbatch_msignal"]) * 2.0)) + (data["abs_avgbatch_slices2_msignal"]))/2.0)) * 2.0)) +
                            0.100000*np.tanh((((5.0)) * 2.0)) +
                            0.100000*np.tanh((3.0)) +
                            0.100000*np.tanh((((((5.09629154205322266)) - (data["maxbatch_slices2_msignal"]))) * (((data["maxbatch_slices2_msignal"]) * ((((((np.where(data["rangebatch_slices2"] <= -998, ((data["maxbatch_slices2_msignal"]) * 2.0), data["minbatch_msignal"] )) + (data["maxbatch_slices2_msignal"]))/2.0)) * 2.0)))))) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] <= -998, np.tanh((np.where(data["abs_maxbatch_slices2"] <= -998, data["abs_avgbatch_slices2_msignal"], data["abs_maxbatch_slices2"] ))), ((((((data["minbatch_slices2_msignal"]) + (data["maxbatch_msignal"]))) * (data["rangebatch_slices2"]))) * (data["rangebatch_slices2"])) )) +
                            0.100000*np.tanh((((((((((11.47881698608398438)) + (data["stdbatch_slices2"]))) + (((data["stdbatch_slices2"]) * 2.0)))) + (data["maxbatch_slices2"]))) * 2.0)) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] <= -998, data["minbatch_msignal"], ((data["minbatch"]) + ((((7.0)) + (((data["minbatch_msignal"]) * 2.0))))) )) +
                            0.100000*np.tanh(((((np.where((4.45449209213256836) <= -998, (((-((data["signal_shift_-1_msignal"])))) * 2.0), (((((3.0)) - (data["medianbatch_msignal"]))) * 2.0) )) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((((4.18359279632568359)) - (np.where((((4.18359279632568359)) - (np.where((4.18359279632568359) > -998, data["rangebatch_slices2"], np.where((4.18359279632568359) > -998, data["abs_maxbatch"], data["minbatch_slices2"] ) ))) > -998, data["rangebatch_slices2"], (4.18359279632568359) )))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) + (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh((((data["maxbatch_msignal"]) + (data["abs_avgbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((data["minbatch"]) + (np.where((-((np.where(data["minbatch_slices2_msignal"] > -998, data["abs_avgbatch_slices2_msignal"], data["abs_avgbatch_slices2_msignal"] )))) > -998, data["abs_avgbatch_slices2_msignal"], data["abs_avgbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((data["minbatch"]) + (((data["abs_maxbatch_slices2"]) * (((((data["minbatch_slices2_msignal"]) + ((((3.0)) - ((0.0)))))) / 2.0)))))) +
                            0.100000*np.tanh(np.where(data["signal"] > -998, data["maxbatch_slices2"], data["maxbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.tanh((np.where(data["maxtominbatch_slices2_msignal"] <= -998, (((3.90524721145629883)) * (data["abs_minbatch_msignal"])), (((((-((((((data["signal_shift_-1_msignal"]) * ((3.90524721145629883)))) * 2.0))))) * ((3.90524721145629883)))) * 2.0) )))) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"]))) * ((((((5.93324804306030273)) / 2.0)) - (data["meanbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((((data["maxbatch_slices2"]) * ((((data["abs_avgbatch_msignal"]) + (data["meanbatch_slices2_msignal"]))/2.0)))) * 2.0)) * (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(data["maxbatch_msignal"]) +
                            0.100000*np.tanh(np.tanh((((data["minbatch_msignal"]) + (np.where((-(((((3.0)) * ((((3.0)) + (data["minbatch_msignal"]))))))) <= -998, data["minbatch_slices2"], (((5.0)) - (data["rangebatch_slices2"])) )))))) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((((8.0)) * (data["signal_shift_+1_msignal"]))) * (((data["minbatch_slices2_msignal"]) + (np.where((((8.0)) + (((data["medianbatch_slices2_msignal"]) * (data["minbatch_slices2_msignal"])))) > -998, data["medianbatch_slices2_msignal"], data["signal_shift_+1_msignal"] )))))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) + ((4.58797311782836914)))) +
                            0.100000*np.tanh((((9.0)) - (np.where(data["rangebatch_slices2_msignal"] <= -998, (9.0), ((data["meanbatch_slices2_msignal"]) * (data["meanbatch_msignal"])) )))) +
                            0.100000*np.tanh(np.where(((data["signal_shift_-1_msignal"]) * ((-((data["meanbatch_slices2_msignal"]))))) > -998, ((data["signal_shift_-1_msignal"]) * ((-((data["abs_maxbatch"]))))), data["abs_maxbatch"] )) +
                            0.100000*np.tanh((((6.0)) + (((data["rangebatch_slices2"]) * (((data["abs_avgbatch_slices2"]) + (((np.where(((data["rangebatch_slices2"]) * (data["abs_avgbatch_msignal"])) <= -998, (((6.0)) * 2.0), data["minbatch_msignal"] )) * 2.0)))))))) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) + ((((((data["abs_maxbatch_msignal"]) + (((((data["abs_maxbatch_msignal"]) * 2.0)) * 2.0)))) + (data["abs_avgbatch_slices2_msignal"]))/2.0)))) +
                            0.100000*np.tanh((((data["rangebatch_msignal"]) + (((data["rangebatch_slices2"]) * (((data["stdbatch_slices2"]) * (data["minbatch"]))))))/2.0)) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] > -998, data["abs_avgbatch_slices2_msignal"], data["rangebatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.where(data["rangebatch_msignal"] > -998, data["abs_maxbatch"], data["abs_avgbatch_msignal"] )) +
                            0.100000*np.tanh(((np.where(((data["maxbatch_slices2_msignal"]) * (data["signal"])) <= -998, ((data["signal"]) * (data["signal"])), data["medianbatch_slices2_msignal"] )) * (np.where(data["meanbatch_msignal"] > -998, data["signal"], data["meanbatch_msignal"] )))) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1"] > -998, np.where(data["maxbatch_slices2"] <= -998, data["abs_avgbatch_slices2"], ((((data["meanbatch_slices2"]) - (data["signal_shift_-1"]))) * 2.0) ), data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((np.where(data["meanbatch_slices2_msignal"] <= -998, data["meanbatch_slices2_msignal"], ((((data["maxbatch_slices2_msignal"]) + ((((data["minbatch"]) + (data["meanbatch_slices2_msignal"]))/2.0)))) + (data["minbatch_slices2_msignal"])) )) + (data["maxbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(((((6.0)) + ((8.81655883789062500)))/2.0)) +
                            0.100000*np.tanh(((np.where((((8.76273536682128906)) - (data["abs_maxbatch_slices2_msignal"])) > -998, (((8.76273536682128906)) - (data["abs_maxbatch_msignal"])), ((data["abs_maxbatch_msignal"]) + (data["meanbatch_slices2_msignal"])) )) * 2.0)) +
                            0.100000*np.tanh((((((11.57792282104492188)) - (((data["maxbatch_msignal"]) * 2.0)))) - (data["maxtominbatch_slices2"]))) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2_msignal"] <= -998, np.where(data["abs_maxbatch_slices2_msignal"] > -998, (14.33471202850341797), data["meanbatch_msignal"] ), data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((((((((((4.0)) + (data["abs_avgbatch_msignal"]))/2.0)) + (((data["maxbatch_msignal"]) * (((data["abs_maxbatch"]) - (data["rangebatch_slices2"]))))))/2.0)) + (data["maxbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.tanh((data["maxbatch_slices2"]))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) * ((((13.21634769439697266)) - (((np.tanh((data["maxbatch_slices2_msignal"]))) + (((data["meanbatch_msignal"]) * (np.where(data["meanbatch_slices2_msignal"] <= -998, data["meanbatch_msignal"], data["meanbatch_msignal"] )))))))))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) * (data["signal"]))) - (np.where(data["medianbatch_slices2_msignal"] > -998, data["medianbatch_slices2_msignal"], np.where(data["signal_shift_-1_msignal"] > -998, data["abs_maxbatch_msignal"], data["meanbatch_slices2_msignal"] ) )))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (np.where(((data["minbatch_msignal"]) + (data["minbatch_msignal"])) <= -998, data["abs_avgbatch_slices2_msignal"], ((((data["meanbatch_msignal"]) + (data["maxbatch_slices2_msignal"]))) / 2.0) )))) +
                            0.100000*np.tanh((((((data["abs_avgbatch_msignal"]) * (np.where(((((((data["mean_abs_chgbatch_slices2"]) + (data["abs_maxbatch_msignal"]))/2.0)) + ((11.62196445465087891)))/2.0) > -998, data["minbatch"], data["abs_avgbatch_slices2_msignal"] )))) + ((10.0)))/2.0)) +
                            0.100000*np.tanh((((9.0)) + (((np.tanh((data["mean_abs_chgbatch_slices2"]))) - (np.where(((data["rangebatch_msignal"]) - ((9.0))) > -998, data["rangebatch_msignal"], data["stdbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2"] > -998, ((data["minbatch_slices2_msignal"]) + ((2.0))), (((np.tanh(((5.0)))) + ((((((2.0)) + ((2.0)))) / 2.0)))/2.0) )) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) - (((data["minbatch_msignal"]) * ((((data["minbatch_msignal"]) + (np.where(data["signal"] > -998, (-((data["medianbatch_slices2_msignal"]))), data["medianbatch_slices2_msignal"] )))/2.0)))))))  
    
    def GP_class_1(self,data):
        return self.Output( -1.623877 +
                            0.100000*np.tanh(np.where(((data["maxtominbatch_slices2_msignal"]) + (((data["maxtominbatch_msignal"]) * 2.0))) > -998, ((((data["maxtominbatch_msignal"]) * 2.0)) + (((data["maxtominbatch_msignal"]) * 2.0))), data["maxtominbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((((np.where(data["maxtominbatch_slices2_msignal"] > -998, data["maxtominbatch_slices2_msignal"], ((((data["rangebatch_slices2"]) - (data["abs_minbatch_msignal"]))) - (data["rangebatch_slices2"])) )) * 2.0)) * (((data["rangebatch_slices2"]) - (data["abs_minbatch_msignal"]))))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * ((-((((data["minbatch_msignal"]) - (np.where(((((data["maxtominbatch_msignal"]) * 2.0)) * 2.0) > -998, data["maxbatch_slices2"], data["abs_minbatch_slices2_msignal"] ))))))))) +
                            0.100000*np.tanh((((((5.75591468811035156)) + (np.where(((data["minbatch_slices2_msignal"]) * 2.0) > -998, data["minbatch_slices2_msignal"], data["stdbatch_slices2_msignal"] )))) + (np.where(((data["minbatch_msignal"]) * 2.0) > -998, data["minbatch_msignal"], ((data["minbatch_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh((((8.0)) + (((np.where(data["abs_minbatch_slices2_msignal"] > -998, np.where(np.where(data["abs_minbatch_slices2_msignal"] > -998, data["abs_minbatch_slices2_msignal"], data["meanbatch_slices2"] ) > -998, data["abs_minbatch_slices2_msignal"], (8.0) ), data["meanbatch_slices2"] )) * (data["meanbatch_slices2"]))))) +
                            0.100000*np.tanh(((np.where(data["maxtominbatch_slices2_msignal"] > -998, (((data["maxtominbatch_slices2_msignal"]) + (data["maxtominbatch_slices2_msignal"]))/2.0), data["maxtominbatch_slices2_msignal"] )) * 2.0)) +
                            0.100000*np.tanh((((((7.0)) - (((np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["maxbatch_slices2"], data["maxtominbatch_slices2_msignal"] )) / 2.0)))) - (((data["maxtominbatch_slices2_msignal"]) * (data["maxtominbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2"]) + (((data["maxtominbatch_slices2_msignal"]) * ((-((np.where(data["abs_maxbatch_slices2"] > -998, data["maxtominbatch_slices2_msignal"], data["maxtominbatch_msignal"] ))))))))) + (data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where((((6.0)) + (data["minbatch_slices2_msignal"])) > -998, (((6.0)) + (data["minbatch_slices2_msignal"])), data["minbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) * (((data["rangebatch_slices2"]) - (np.where(data["rangebatch_slices2"] > -998, data["stdbatch_msignal"], data["maxtominbatch_msignal"] )))))) +
                            0.100000*np.tanh(((data["abs_maxbatch"]) * (((((((data["signal_shift_+1"]) * (data["abs_minbatch_slices2_msignal"]))) * 2.0)) + ((((((9.0)) - ((((4.0)) / 2.0)))) * 2.0)))))) +
                            0.100000*np.tanh(((((((((data["minbatch_slices2_msignal"]) + ((4.0)))) * ((4.0)))) * ((4.0)))) * ((((data["signal_shift_+1"]) + ((-((((data["minbatch_slices2_msignal"]) * 2.0))))))/2.0)))) +
                            0.100000*np.tanh(((((((data["rangebatch_msignal"]) + (data["stdbatch_msignal"]))) * ((((5.0)) - (data["rangebatch_msignal"]))))) + (data["mean_abs_chgbatch_msignal"]))) +
                            0.100000*np.tanh((((1.81757616996765137)) - (np.where((1.81757259368896484) > -998, ((data["maxbatch_msignal"]) * (data["maxbatch_msignal"])), np.tanh((np.where((1.81757259368896484) > -998, data["maxbatch_msignal"], data["maxbatch_msignal"] ))) )))) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] <= -998, data["minbatch_msignal"], ((data["minbatch_msignal"]) + (((((data["minbatch_msignal"]) + ((((2.26485776901245117)) * 2.0)))) * 2.0))) )) +
                            0.100000*np.tanh((((6.36823797225952148)) + (((np.where(((((7.0)) + ((6.36823797225952148)))/2.0) <= -998, data["abs_minbatch_slices2_msignal"], data["minbatch_msignal"] )) * 2.0)))) +
                            0.100000*np.tanh((((7.49696540832519531)) + (np.where((7.49696540832519531) <= -998, data["medianbatch_slices2"], ((data["minbatch_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2"] > -998, (((data["maxbatch_msignal"]) + ((((14.66286468505859375)) - ((((10.0)) * (data["maxbatch_msignal"]))))))/2.0), (10.0) )) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1"] > -998, (((((3.0)) + (data["minbatch_msignal"]))) * 2.0), (((((3.0)) + (data["minbatch_msignal"]))) * 2.0) )) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (np.where(data["maxtominbatch"] <= -998, ((data["rangebatch_slices2"]) * 2.0), np.where(data["rangebatch_slices2"] > -998, data["abs_minbatch_slices2_msignal"], data["maxtominbatch"] ) )))) +
                            0.100000*np.tanh(((((((data["signal"]) * ((((3.0)) + (data["minbatch_msignal"]))))) + ((3.0)))) + ((((3.04699373245239258)) + (data["minbatch_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] <= -998, data["minbatch"], (((((((5.0)) / 2.0)) + (data["minbatch_slices2_msignal"]))) * ((4.94477462768554688))) )) +
                            0.100000*np.tanh((((8.0)) + (((np.where((((((2.0)) + (data["minbatch_slices2_msignal"]))) / 2.0) > -998, ((np.tanh(((8.0)))) + (data["minbatch_slices2_msignal"])), data["rangebatch_slices2"] )) * (data["rangebatch_slices2"]))))) +
                            0.100000*np.tanh(data["maxbatch_slices2"]) +
                            0.100000*np.tanh(np.where((4.73289108276367188) <= -998, ((data["minbatch_msignal"]) + (((((data["minbatch_msignal"]) - ((4.73289108276367188)))) * (data["minbatch_msignal"])))), ((data["minbatch_msignal"]) + ((4.73289108276367188))) )) +
                            0.100000*np.tanh(((np.where((((11.73651981353759766)) / 2.0) > -998, data["minbatch_slices2_msignal"], (((11.73651981353759766)) / 2.0) )) + ((((((11.73651981353759766)) / 2.0)) / 2.0)))) +
                            0.100000*np.tanh(np.where((((data["abs_maxbatch_slices2"]) + (data["abs_minbatch_slices2"]))/2.0) <= -998, (((9.0)) - ((9.0))), (((9.0)) - (((data["abs_minbatch_slices2"]) - (((data["minbatch_msignal"]) * 2.0))))) )) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh((((((3.0)) + (np.where(data["medianbatch_msignal"] > -998, data["minbatch_msignal"], data["minbatch_msignal"] )))) + ((((((3.0)) + (data["minbatch_msignal"]))) / 2.0)))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) + (data["medianbatch_slices2"]))) +
                            0.100000*np.tanh(((((((((data["minbatch_msignal"]) + ((3.0)))) + (((((((data["minbatch_msignal"]) + ((3.0)))) * 2.0)) * 2.0)))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((((data["medianbatch_slices2"]) + (data["minbatch"]))/2.0)) +
                            0.100000*np.tanh((((5.25920152664184570)) - (np.where((5.25920152664184570) <= -998, (((data["abs_avgbatch_msignal"]) + (data["medianbatch_msignal"]))/2.0), np.where(data["abs_minbatch_slices2_msignal"] <= -998, data["signal_shift_+1_msignal"], data["rangebatch_slices2"] ) )))) +
                            0.100000*np.tanh((((((3.0)) - (((data["maxbatch_msignal"]) * 2.0)))) * (data["abs_maxbatch"]))) +
                            0.100000*np.tanh(np.where((2.0) > -998, ((np.where(((np.tanh(((8.0)))) * 2.0) > -998, (((3.24906778335571289)) + (data["minbatch_msignal"])), data["minbatch_msignal"] )) * 2.0), (3.24906778335571289) )) +
                            0.100000*np.tanh((((((np.where((((((((((data["rangebatch_slices2"]) - ((6.0)))) * 2.0)) * 2.0)) + (data["meanbatch_slices2"]))/2.0) <= -998, np.tanh(((9.0))), data["minbatch_msignal"] )) * 2.0)) + ((9.0)))/2.0)) +
                            0.100000*np.tanh(((((((((data["signal"]) + ((2.0)))) * (data["maxtominbatch_slices2_msignal"]))) * (((data["maxtominbatch_slices2_msignal"]) * (data["abs_minbatch_msignal"]))))) + (((data["stdbatch_slices2"]) - (data["maxtominbatch"]))))) +
                            0.100000*np.tanh((((((8.98653984069824219)) + (data["medianbatch_msignal"]))) - (((data["medianbatch_slices2_msignal"]) * (((data["maxtominbatch"]) + (data["medianbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((((data["maxtominbatch_msignal"]) * 2.0)) * (((data["stdbatch_slices2_msignal"]) * ((((((((data["rangebatch_slices2_msignal"]) + (data["stdbatch_slices2_msignal"]))) + (data["stdbatch_slices2_msignal"]))) + (data["abs_maxbatch_slices2"]))/2.0)))))) +
                            0.100000*np.tanh(((np.where((((((((4.0)) + (data["minbatch_msignal"]))/2.0)) + ((4.0)))/2.0) <= -998, data["minbatch_msignal"], np.where(data["minbatch_msignal"] <= -998, (4.0), data["minbatch_msignal"] ) )) + ((4.0)))) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1_msignal"] <= -998, ((((data["abs_avgbatch_slices2_msignal"]) + ((((data["medianbatch_slices2_msignal"]) + (data["medianbatch_slices2"]))/2.0)))) + (data["medianbatch_slices2"])), data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(((((data["abs_maxbatch"]) * 2.0)) + (np.where(np.where(data["meanbatch_slices2"] > -998, data["abs_maxbatch"], data["abs_maxbatch"] ) > -998, ((data["abs_minbatch_msignal"]) * (data["meanbatch_slices2"])), data["abs_maxbatch"] )))) +
                            0.100000*np.tanh(((np.where(data["maxtominbatch_slices2_msignal"] <= -998, data["stdbatch_slices2_msignal"], data["maxtominbatch_slices2_msignal"] )) * (data["stdbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((((5.0)) + (data["minbatch_slices2_msignal"]))) + (np.where((((5.0)) + (data["minbatch_slices2_msignal"])) > -998, data["minbatch_slices2_msignal"], data["minbatch"] )))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * (((np.where(data["abs_minbatch_msignal"] <= -998, ((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])), data["medianbatch_slices2_msignal"] )) * (data["mean_abs_chgbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] > -998, (((data["signal_shift_+1"]) + (data["abs_maxbatch_slices2"]))/2.0), ((data["mean_abs_chgbatch_slices2"]) * 2.0) )) +
                            0.100000*np.tanh(((((((((14.00762557983398438)) - (((data["minbatch_msignal"]) * (data["minbatch_msignal"]))))) + (data["minbatch_msignal"]))) + (np.where(data["signal_shift_+1"] <= -998, data["minbatch_msignal"], data["minbatch_msignal"] )))/2.0)) +
                            0.100000*np.tanh((-((((np.tanh((np.where((-((data["stdbatch_slices2"]))) > -998, data["maxbatch_slices2"], (-((data["abs_minbatch_slices2"]))) )))) - (data["meanbatch_slices2"])))))) +
                            0.100000*np.tanh(np.where(np.where((((-((data["medianbatch_msignal"])))) * 2.0) > -998, data["minbatch"], data["medianbatch_slices2_msignal"] ) <= -998, data["abs_maxbatch"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_msignal"] > -998, ((data["meanbatch_msignal"]) * (data["mean_abs_chgbatch_slices2"])), ((np.where(data["abs_avgbatch_slices2"] <= -998, (-((data["abs_minbatch_msignal"]))), (2.30200099945068359) )) + (np.tanh((data["stdbatch_slices2"])))) )) +
                            0.100000*np.tanh((((((3.0)) + (data["minbatch_msignal"]))) * ((((10.0)) - ((((((3.0)) + (data["minbatch_msignal"]))) * ((((10.0)) - ((3.0)))))))))) +
                            0.100000*np.tanh((((7.0)) * 2.0)) +
                            0.100000*np.tanh((((11.38669204711914062)) - ((((((((data["meanbatch_msignal"]) + (data["meanbatch_slices2_msignal"]))/2.0)) - (data["rangebatch_slices2"]))) * (data["minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((5.22413635253906250)) + (np.where(np.where((5.22413635253906250) > -998, np.tanh((data["maxtominbatch"])), ((data["minbatch_msignal"]) + ((3.77917981147766113))) ) > -998, data["minbatch_msignal"], (-(((3.77917981147766113)))) )))) +
                            0.100000*np.tanh(((data["rangebatch_slices2_msignal"]) * (((data["minbatch_msignal"]) - (np.where(data["maxtominbatch_msignal"] > -998, data["maxtominbatch_msignal"], np.where(data["rangebatch_slices2_msignal"] > -998, data["rangebatch_slices2_msignal"], data["minbatch_msignal"] ) )))))) +
                            0.100000*np.tanh(((np.where(data["rangebatch_slices2_msignal"] > -998, data["signal_shift_+1_msignal"], data["medianbatch_slices2_msignal"] )) + (((data["abs_maxbatch_msignal"]) + (data["meanbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(((data["stdbatch_slices2_msignal"]) * (data["maxtominbatch_slices2_msignal"])) > -998, ((data["stdbatch_slices2_msignal"]) * (data["maxtominbatch_slices2_msignal"])), data["maxtominbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch"] <= -998, data["abs_avgbatch_msignal"], ((((((data["medianbatch_slices2_msignal"]) * (((data["abs_avgbatch_slices2_msignal"]) * (data["mean_abs_chgbatch_slices2"]))))) * (data["mean_abs_chgbatch_slices2"]))) * (data["medianbatch_msignal"])) )) +
                            0.100000*np.tanh(np.where(np.where((((12.77474212646484375)) - (((data["minbatch_slices2"]) * (data["abs_minbatch_slices2_msignal"])))) > -998, (12.77474212646484375), data["mean_abs_chgbatch_slices2"] ) > -998, (12.77474212646484375), data["rangebatch_slices2"] )) +
                            0.100000*np.tanh(((data["rangebatch_msignal"]) * (np.tanh(((((data["meanbatch_msignal"]) + (np.tanh(((-((data["rangebatch_slices2_msignal"])))))))/2.0)))))) +
                            0.100000*np.tanh(((np.where((((3.0)) + ((-(((-((data["maxbatch_msignal"])))))))) <= -998, data["maxbatch_msignal"], (((3.0)) + ((-((((data["maxbatch_msignal"]) * 2.0)))))) )) * 2.0)) +
                            0.100000*np.tanh((((11.76923561096191406)) + (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] <= -998, (((8.73951148986816406)) / 2.0), (12.41387081146240234) )) +
                            0.100000*np.tanh(((data["maxtominbatch"]) * (((data["maxtominbatch"]) + (np.where(data["maxtominbatch"] <= -998, ((data["abs_maxbatch_slices2_msignal"]) / 2.0), ((data["rangebatch_slices2"]) / 2.0) )))))) +
                            0.100000*np.tanh((((np.where((((((data["minbatch_slices2_msignal"]) * (data["abs_avgbatch_slices2"]))) + ((6.0)))/2.0) <= -998, data["stdbatch_slices2"], (6.0) )) + (((data["minbatch_slices2_msignal"]) * (data["abs_avgbatch_slices2"]))))/2.0)) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["medianbatch_slices2_msignal"], ((np.tanh(((11.49774646759033203)))) * (data["abs_avgbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((np.where(data["maxtominbatch"] > -998, data["abs_minbatch_slices2_msignal"], (-(((2.83021759986877441)))) )) - (((data["maxtominbatch"]) - (np.where(data["minbatch_msignal"] > -998, ((data["abs_minbatch_slices2_msignal"]) - (data["stdbatch_slices2_msignal"])), data["minbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * (np.where(data["abs_avgbatch_msignal"] <= -998, data["maxtominbatch_msignal"], np.where(data["stdbatch_msignal"] > -998, data["stdbatch_msignal"], (7.0) ) )))) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2"] > -998, (((((3.0)) + (data["minbatch_msignal"]))) * 2.0), (((((((((((3.0)) + (data["minbatch_msignal"]))) * 2.0)) * 2.0)) * 2.0)) / 2.0) )) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where(data["abs_avgbatch_slices2"] > -998, (3.0), (((3.0)) * (((data["minbatch_slices2_msignal"]) * 2.0))) )))) +
                            0.100000*np.tanh((6.0)) +
                            0.100000*np.tanh((6.0)) +
                            0.100000*np.tanh(((((np.where(((data["maxtominbatch"]) - ((10.0))) <= -998, ((((data["maxbatch_slices2"]) * (data["maxtominbatch_msignal"]))) / 2.0), ((data["minbatch"]) * 2.0) )) - (data["maxtominbatch"]))) * (data["meanbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.tanh((data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(((np.where(data["maxtominbatch_msignal"] > -998, ((data["abs_maxbatch_msignal"]) * (data["medianbatch_slices2_msignal"])), data["maxtominbatch"] )) - (((data["rangebatch_slices2"]) - ((7.0)))))) +
                            0.100000*np.tanh(((((((data["abs_minbatch_msignal"]) + (data["rangebatch_slices2_msignal"]))) * (np.where(((data["abs_minbatch_msignal"]) / 2.0) > -998, data["medianbatch_slices2_msignal"], data["abs_minbatch_msignal"] )))) * 2.0)) +
                            0.100000*np.tanh(np.where((((data["abs_avgbatch_slices2_msignal"]) + ((((4.0)) * 2.0)))/2.0) > -998, (((((((4.0)) + (data["minbatch_msignal"]))) * 2.0)) * 2.0), data["minbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((-((((np.where((((5.27644681930541992)) * (data["abs_minbatch_slices2_msignal"])) > -998, data["abs_avgbatch_msignal"], np.where(data["stdbatch_msignal"] > -998, data["abs_maxbatch"], data["maxbatch_slices2_msignal"] ) )) - (((data["stdbatch_msignal"]) * (data["abs_minbatch_slices2_msignal"])))))))) +
                            0.100000*np.tanh(((((np.where((((4.0)) + (data["minbatch_msignal"])) > -998, (((((4.0)) + (data["minbatch_msignal"]))) * 2.0), (4.0) )) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((0.91890358924865723)) +
                            0.100000*np.tanh(((np.where(np.where(data["medianbatch_slices2_msignal"] > -998, data["medianbatch_slices2_msignal"], data["rangebatch_slices2_msignal"] ) > -998, (4.00936698913574219), data["meanbatch_msignal"] )) + (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((4.23594951629638672)) + (((data["minbatch_slices2_msignal"]) * (np.where(((data["signal_shift_+1"]) - (((((data["minbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))) / 2.0))) <= -998, data["signal_shift_+1"], ((data["stdbatch_slices2"]) * 2.0) )))))) +
                            0.100000*np.tanh(np.where(data["meanbatch_msignal"] <= -998, ((data["medianbatch_slices2_msignal"]) * (((data["rangebatch_slices2"]) / 2.0))), data["rangebatch_slices2"] )) +
                            0.100000*np.tanh((((((-(((((data["minbatch_slices2_msignal"]) + (np.tanh((np.where(((data["abs_minbatch_msignal"]) * (data["medianbatch_msignal"])) <= -998, data["minbatch_slices2_msignal"], ((((data["abs_maxbatch_slices2"]) * 2.0)) / 2.0) )))))/2.0))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((((data["medianbatch_msignal"]) * (data["maxtominbatch_msignal"]))) / 2.0)) * (data["stdbatch_msignal"]))) +
                            0.100000*np.tanh((((4.64374876022338867)) - (((data["rangebatch_slices2"]) - (np.where((((((4.64374876022338867)) - ((((4.64374876022338867)) - (data["rangebatch_slices2"]))))) - ((4.64374876022338867))) <= -998, (4.64374876022338867), data["medianbatch_msignal"] )))))) +
                            0.100000*np.tanh(data["rangebatch_slices2"]) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) * ((((((8.0)) + (((data["abs_minbatch_slices2"]) * 2.0)))) * 2.0)))) +
                            0.100000*np.tanh((((9.11284255981445312)) + (((((((data["minbatch_slices2_msignal"]) * 2.0)) + (data["minbatch"]))) + (((((np.tanh(((9.11284255981445312)))) * 2.0)) + (data["minbatch"]))))))) +
                            0.100000*np.tanh(np.where((((data["mean_abs_chgbatch_msignal"]) + (data["minbatch_slices2_msignal"]))/2.0) > -998, (((8.0)) - (((data["minbatch_slices2_msignal"]) * (data["minbatch_msignal"])))), ((data["minbatch_msignal"]) * (data["minbatch_msignal"])) )) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2_msignal"] <= -998, data["signal_shift_-1_msignal"], (((((1.0)) - (data["maxbatch_slices2_msignal"]))) * 2.0) )) +
                            0.100000*np.tanh((8.37373352050781250)) +
                            0.100000*np.tanh(((((data["signal_shift_-1_msignal"]) - (data["maxtominbatch_slices2"]))) * (((data["abs_avgbatch_slices2_msignal"]) - (data["mean_abs_chgbatch_slices2"]))))) +
                            0.100000*np.tanh((((((data["minbatch"]) + (((data["abs_avgbatch_msignal"]) * (data["abs_maxbatch_slices2_msignal"]))))/2.0)) * (np.where(np.tanh((((data["signal"]) * ((10.0))))) > -998, data["signal"], data["abs_maxbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((np.where((-(((4.52580642700195312)))) <= -998, data["abs_avgbatch_msignal"], data["rangebatch_slices2"] )) * ((((4.21422672271728516)) - ((-((data["minbatch_msignal"])))))))) +
                            0.100000*np.tanh(((np.where(data["mean_abs_chgbatch_slices2_msignal"] <= -998, np.where(data["meanbatch_msignal"] <= -998, data["maxbatch_msignal"], ((data["stdbatch_slices2_msignal"]) * 2.0) ), (((data["maxtominbatch_msignal"]) + (data["mean_abs_chgbatch_slices2_msignal"]))/2.0) )) * (data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh((((5.0)) - (((data["medianbatch_msignal"]) / 2.0)))) +
                            0.100000*np.tanh(data["abs_avgbatch_msignal"]) +
                            0.100000*np.tanh(((data["abs_maxbatch"]) - (((np.where(((data["abs_maxbatch"]) * 2.0) <= -998, data["abs_maxbatch"], data["minbatch_msignal"] )) + (((data["abs_maxbatch"]) * (data["maxbatch_msignal"]))))))) +
                            0.100000*np.tanh((((12.52569007873535156)) * (np.where(data["medianbatch_slices2_msignal"] > -998, data["medianbatch_slices2_msignal"], (((1.04399466514587402)) * (((data["medianbatch_msignal"]) / 2.0))) )))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2"]) * (data["minbatch"]))) + (((((6.63453483581542969)) + (np.where(((((6.63453483581542969)) + (data["meanbatch_slices2"]))/2.0) <= -998, data["abs_avgbatch_slices2"], ((data["abs_avgbatch_msignal"]) * 2.0) )))/2.0)))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * (data["signal_shift_+1_msignal"]))) +
                            0.100000*np.tanh((((((1.86451840400695801)) - (data["meanbatch_msignal"]))) * ((((((((4.0)) * ((4.0)))) - ((1.86451840400695801)))) + ((((((4.0)) * 2.0)) + ((1.86452198028564453)))))))) +
                            0.100000*np.tanh(np.where(np.tanh((data["rangebatch_slices2_msignal"])) > -998, data["medianbatch_slices2_msignal"], data["medianbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh((((((4.69225025177001953)) + (np.tanh(((((4.69225025177001953)) + (data["minbatch_msignal"]))))))) + (((np.where((5.10185623168945312) <= -998, data["minbatch_slices2_msignal"], data["minbatch_slices2_msignal"] )) + (data["minbatch_msignal"]))))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((((np.where(((data["stdbatch_msignal"]) - ((9.63203620910644531))) <= -998, data["rangebatch_msignal"], ((data["abs_maxbatch_slices2"]) - (data["abs_maxbatch_slices2"])) )) + ((7.0)))) * ((((2.0)) - (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((((data["minbatch_msignal"]) + (np.where(((data["rangebatch_slices2"]) + ((4.11534643173217773))) > -998, (4.11534643173217773), (4.11534643173217773) )))) * 2.0)))) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) * 2.0)) +
                            0.100000*np.tanh((((((4.0)) + (((np.where(np.tanh((data["abs_maxbatch_slices2"])) <= -998, data["stdbatch_slices2"], ((data["stdbatch_slices2"]) * 2.0) )) * (data["minbatch_slices2_msignal"]))))) * 2.0)) +
                            0.100000*np.tanh(((((data["rangebatch_slices2"]) - (data["maxtominbatch_msignal"]))) * (((data["abs_maxbatch"]) - (np.where(data["rangebatch_slices2"] <= -998, data["maxtominbatch_msignal"], ((np.where(data["abs_maxbatch"] > -998, data["medianbatch_slices2"], data["maxtominbatch_msignal"] )) * 2.0) )))))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - ((((((np.tanh((data["medianbatch_msignal"]))) + (data["abs_maxbatch_slices2"]))/2.0)) - ((((-((data["minbatch_slices2_msignal"])))) * 2.0)))))) +
                            0.100000*np.tanh((((5.52949333190917969)) + (np.where(data["maxtominbatch_slices2_msignal"] <= -998, ((data["rangebatch_slices2"]) * (((data["abs_avgbatch_msignal"]) + (np.where(data["maxbatch_slices2_msignal"] > -998, data["meanbatch_slices2"], data["maxbatch_slices2_msignal"] ))))), ((data["minbatch_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * (((data["abs_avgbatch_msignal"]) * (data["abs_avgbatch_msignal"]))))) +
                            0.100000*np.tanh((-(((((data["minbatch_slices2_msignal"]) + (data["medianbatch_slices2_msignal"]))/2.0))))) +
                            0.100000*np.tanh(((np.where(data["signal_shift_-1_msignal"] <= -998, np.where(data["minbatch_slices2_msignal"] <= -998, data["medianbatch_msignal"], data["stdbatch_slices2"] ), data["abs_maxbatch_slices2"] )) - (data["signal"]))) +
                            0.100000*np.tanh(((data["abs_maxbatch"]) - (((np.where((-((np.tanh(((-((data["minbatch_slices2"])))))))) <= -998, (-((((data["maxbatch_slices2"]) / 2.0)))), data["abs_maxbatch_slices2_msignal"] )) * (data["maxbatch_slices2"]))))) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2"] > -998, ((data["medianbatch_msignal"]) * (((data["abs_avgbatch_msignal"]) * 2.0))), data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] > -998, data["abs_avgbatch_msignal"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(((((((data["abs_avgbatch_slices2"]) / 2.0)) * (np.where(data["signal_shift_+1"] <= -998, np.tanh((data["signal_shift_-1"])), data["signal_shift_-1"] )))) + (data["rangebatch_slices2"]))) +
                            0.100000*np.tanh(np.tanh((np.tanh((data["medianbatch_slices2"]))))) +
                            0.100000*np.tanh((((((data["maxtominbatch"]) + ((8.0)))/2.0)) * (((((((8.0)) + (((data["signal_shift_+1_msignal"]) + (data["maxtominbatch_msignal"]))))/2.0)) - (data["maxbatch_slices2"]))))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh((((((((3.0)) * 2.0)) - (np.where(data["abs_avgbatch_slices2"] > -998, data["rangebatch_slices2"], (((3.0)) - (np.where((((3.0)) * 2.0) <= -998, data["medianbatch_slices2_msignal"], (3.0) ))) )))) * 2.0)) +
                            0.100000*np.tanh((((5.0)) - (data["signal"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (((data["stdbatch_slices2_msignal"]) * ((((10.98334503173828125)) + (data["maxtominbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((data["minbatch"]) - (np.where(np.where(((data["meanbatch_slices2_msignal"]) - (data["maxtominbatch_slices2"])) > -998, data["medianbatch_slices2_msignal"], np.tanh((data["minbatch"])) ) <= -998, data["minbatch"], data["stdbatch_msignal"] )))) +
                            0.100000*np.tanh(np.where(((data["signal_shift_+1_msignal"]) - (data["abs_maxbatch"])) > -998, data["rangebatch_slices2"], np.tanh((data["medianbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh((((3.87513852119445801)) - (((data["rangebatch_slices2"]) - (data["abs_avgbatch_msignal"]))))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) - (np.where(data["signal_shift_-1_msignal"] <= -998, data["rangebatch_msignal"], np.tanh((np.where(data["medianbatch_msignal"] > -998, data["meanbatch_msignal"], data["abs_avgbatch_slices2_msignal"] ))) )))) * ((((6.75310277938842773)) * 2.0)))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) + (((data["minbatch"]) + ((((11.52776145935058594)) + (((data["minbatch_msignal"]) * (data["rangebatch_slices2"]))))))))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) + ((((7.0)) + (((data["abs_avgbatch_slices2_msignal"]) + (((data["maxtominbatch_slices2_msignal"]) * (((data["maxtominbatch"]) + (data["abs_maxbatch"]))))))))))) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] <= -998, data["medianbatch_slices2"], ((((((np.where(data["medianbatch_slices2"] <= -998, data["medianbatch_slices2"], ((data["medianbatch_slices2"]) * 2.0) )) + (data["medianbatch_slices2"]))) * 2.0)) * 2.0) )) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2"] <= -998, data["maxtominbatch_slices2"], data["abs_avgbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((6.50425815582275391)) + ((((6.50425815582275391)) - (((np.where(data["rangebatch_slices2_msignal"] <= -998, ((data["maxtominbatch_msignal"]) * 2.0), (7.0) )) * (data["medianbatch_msignal"]))))))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) - (np.tanh((((data["meanbatch_msignal"]) * ((8.0)))))))) * ((((8.0)) * 2.0)))) +
                            0.100000*np.tanh(np.where(((((data["signal_shift_-1"]) * 2.0)) * 2.0) > -998, ((((((data["signal_shift_-1"]) * 2.0)) * 2.0)) + ((9.0))), ((((data["medianbatch_slices2"]) * 2.0)) * 2.0) )) +
                            0.100000*np.tanh((((10.0)) * (np.tanh((((data["abs_avgbatch_msignal"]) + (np.tanh((((np.where(data["abs_avgbatch_msignal"] > -998, data["signal"], data["rangebatch_slices2"] )) + (data["maxtominbatch_msignal"]))))))))))) +
                            0.100000*np.tanh(np.where(((data["minbatch_msignal"]) * (data["meanbatch_msignal"])) > -998, ((((data["maxbatch_msignal"]) - ((-((((data["minbatch_msignal"]) * (data["meanbatch_msignal"])))))))) * 2.0), ((data["minbatch_msignal"]) * (data["minbatch_msignal"])) )) +
                            0.100000*np.tanh(((np.where(((data["abs_avgbatch_msignal"]) * 2.0) > -998, data["medianbatch_msignal"], np.tanh((data["medianbatch_slices2_msignal"])) )) * 2.0)) +
                            0.100000*np.tanh(data["abs_maxbatch_slices2"]) +
                            0.100000*np.tanh(np.tanh((data["abs_maxbatch"]))) +
                            0.100000*np.tanh(((((np.tanh((((data["minbatch_msignal"]) + (((data["maxbatch_msignal"]) - (data["medianbatch_msignal"]))))))) * (((data["signal_shift_-1"]) + (data["medianbatch_msignal"]))))) * (data["abs_maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((((((11.45215511322021484)) / 2.0)) + ((((5.41591405868530273)) + (data["rangebatch_slices2_msignal"]))))) - (((data["minbatch_msignal"]) * (data["minbatch_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, ((((data["minbatch_slices2_msignal"]) * (((data["medianbatch_msignal"]) + (data["minbatch_slices2_msignal"]))))) * 2.0), ((data["medianbatch_msignal"]) / 2.0) )) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * (((data["medianbatch_msignal"]) - (np.where(data["maxtominbatch_msignal"] > -998, data["abs_avgbatch_msignal"], ((((data["medianbatch_msignal"]) + (((data["stdbatch_slices2"]) * (data["stdbatch_slices2"]))))) / 2.0) )))))) +
                            0.100000*np.tanh((((((data["minbatch_slices2_msignal"]) + ((4.16833257675170898)))/2.0)) + (data["maxtominbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2"] > -998, (((9.0)) * ((((data["meanbatch_slices2"]) + ((((((data["minbatch_msignal"]) * (data["abs_maxbatch"]))) + ((9.0)))/2.0)))/2.0))), ((data["maxtominbatch_slices2"]) * (data["abs_maxbatch"])) )) +
                            0.100000*np.tanh(((data["minbatch"]) + (np.where(data["mean_abs_chgbatch_slices2"] <= -998, data["abs_maxbatch_slices2"], (((3.87601113319396973)) - ((-((((data["signal_shift_-1_msignal"]) * 2.0)))))) )))) +
                            0.100000*np.tanh((((data["minbatch_msignal"]) + (((np.where((-((data["maxbatch_slices2_msignal"]))) <= -998, np.where(data["minbatch_msignal"] > -998, data["maxbatch_slices2_msignal"], data["minbatch_msignal"] ), (2.50246596336364746) )) * 2.0)))/2.0)) +
                            0.100000*np.tanh((((5.52249479293823242)) - (((data["abs_avgbatch_msignal"]) * (((((np.where((6.0) <= -998, ((data["abs_maxbatch"]) / 2.0), data["abs_maxbatch_slices2"] )) / 2.0)) / 2.0)))))) +
                            0.100000*np.tanh((((((8.0)) / 2.0)) + (np.where(data["medianbatch_msignal"] > -998, data["minbatch_msignal"], (((8.0)) + (((data["medianbatch_msignal"]) - ((7.0))))) )))) +
                            0.100000*np.tanh(np.where((((9.87980842590332031)) - ((((((9.87980842590332031)) * 2.0)) * (data["meanbatch_slices2"])))) <= -998, (1.0), (((9.87980842590332031)) - (((data["medianbatch_slices2_msignal"]) * (data["meanbatch_slices2"])))) )) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) * ((((data["abs_avgbatch_msignal"]) + (np.where(data["maxbatch_slices2"] > -998, data["minbatch"], np.where(data["signal_shift_+1_msignal"] <= -998, data["abs_avgbatch_msignal"], data["medianbatch_slices2"] ) )))/2.0)))) +
                            0.100000*np.tanh((((data["abs_avgbatch_slices2_msignal"]) + ((8.13084983825683594)))/2.0)) +
                            0.100000*np.tanh(((np.where(data["medianbatch_msignal"] <= -998, data["medianbatch_msignal"], data["medianbatch_msignal"] )) * (((data["maxbatch_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(np.where(data["stdbatch_slices2"] > -998, data["medianbatch_msignal"], np.tanh((data["medianbatch_msignal"])) )) +
                            0.100000*np.tanh((((((6.63624048233032227)) - (data["abs_maxbatch_slices2_msignal"]))) * (data["abs_maxbatch_slices2"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (((data["medianbatch_msignal"]) * (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) * 2.0)) * (((((data["abs_minbatch_slices2"]) * (data["abs_maxbatch_slices2_msignal"]))) * (np.where(data["abs_avgbatch_msignal"] > -998, data["abs_avgbatch_msignal"], data["abs_avgbatch_msignal"] )))))) +
                            0.100000*np.tanh((((3.0)) + (((np.tanh((((((data["mean_abs_chgbatch_msignal"]) - (((np.tanh((data["abs_avgbatch_slices2"]))) * 2.0)))) / 2.0)))) - (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh((((((np.where((12.16507625579833984) <= -998, ((((data["maxtominbatch"]) * 2.0)) + ((2.0))), data["minbatch_msignal"] )) + ((((12.16507625579833984)) - (data["rangebatch_msignal"]))))/2.0)) + (data["minbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(np.tanh((data["rangebatch_msignal"])) > -998, np.where(((data["rangebatch_msignal"]) / 2.0) > -998, data["abs_maxbatch"], data["abs_maxbatch"] ), ((((7.0)) + (data["abs_maxbatch"]))/2.0) )) +
                            0.100000*np.tanh((((((data["stdbatch_slices2_msignal"]) + (((data["medianbatch_msignal"]) - (((data["abs_maxbatch_msignal"]) + (np.tanh((data["rangebatch_msignal"]))))))))) + ((((((data["signal_shift_+1"]) + (data["maxtominbatch_slices2_msignal"]))) + ((5.13937854766845703)))/2.0)))/2.0)) +
                            0.100000*np.tanh(((np.where(data["maxbatch_msignal"] <= -998, data["maxtominbatch_slices2_msignal"], (3.24438643455505371) )) * (((data["maxbatch_msignal"]) + ((-((np.where(data["mean_abs_chgbatch_msignal"] <= -998, data["signal"], (3.24438643455505371) ))))))))) +
                            0.100000*np.tanh(np.where((-(((((6.0)) + ((-((data["abs_avgbatch_slices2"])))))))) > -998, ((data["minbatch"]) + ((((6.0)) + (data["minbatch_msignal"])))), (6.0) )) +
                            0.100000*np.tanh(((((data["minbatch"]) * (data["meanbatch_slices2"]))) + (np.where(data["medianbatch_slices2"] > -998, data["abs_maxbatch_slices2_msignal"], ((((((data["meanbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"]))/2.0)) + (data["abs_maxbatch_slices2_msignal"]))/2.0) )))) +
                            0.100000*np.tanh((((10.0)) + ((((((((10.0)) - (((((data["abs_maxbatch"]) / 2.0)) * (data["abs_avgbatch_slices2_msignal"]))))) * (data["abs_avgbatch_slices2_msignal"]))) - (((data["abs_minbatch_msignal"]) * (data["abs_minbatch_msignal"]))))))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2_msignal"]) * (data["rangebatch_slices2_msignal"]))) * (np.where(np.where(np.tanh((data["stdbatch_slices2"])) <= -998, data["maxbatch_slices2_msignal"], data["minbatch_msignal"] ) <= -998, data["minbatch"], ((data["signal_shift_+1"]) - (data["minbatch_msignal"])) )))) +
                            0.100000*np.tanh(((((np.where(np.tanh((np.tanh((data["abs_minbatch_slices2"])))) > -998, data["maxtominbatch_msignal"], np.tanh((np.tanh((data["abs_minbatch_slices2"])))) )) * (data["signal_shift_-1_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(((np.where(data["meanbatch_slices2"] <= -998, data["meanbatch_slices2"], ((data["maxtominbatch_slices2_msignal"]) * (data["minbatch"])) )) * 2.0)) +
                            0.100000*np.tanh(np.where(np.where(np.tanh((np.tanh((data["medianbatch_msignal"])))) > -998, (9.93461036682128906), data["abs_avgbatch_msignal"] ) <= -998, data["abs_maxbatch_slices2"], np.where(data["meanbatch_msignal"] > -998, data["abs_avgbatch_slices2_msignal"], (1.75314950942993164) ) )) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2_msignal"] <= -998, data["signal_shift_-1"], data["abs_maxbatch_slices2"] )) +
                            0.100000*np.tanh(np.where(data["stdbatch_slices2"] <= -998, data["maxbatch_slices2_msignal"], data["abs_maxbatch"] )) +
                            0.100000*np.tanh(((((((((data["mean_abs_chgbatch_slices2_msignal"]) + (data["maxtominbatch_slices2_msignal"]))/2.0)) + (((data["maxtominbatch_slices2"]) * (data["mean_abs_chgbatch_slices2_msignal"]))))) + (((data["maxtominbatch_slices2_msignal"]) * 2.0)))/2.0)) +
                            0.100000*np.tanh(np.where((((data["maxbatch_slices2_msignal"]) + ((9.06326866149902344)))/2.0) > -998, data["stdbatch_slices2"], ((data["maxbatch_slices2_msignal"]) - (data["rangebatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(np.tanh((data["abs_minbatch_slices2"]))) +
                            0.100000*np.tanh((((-(((5.95391893386840820))))) - (((((np.where(np.where((5.95391893386840820) > -998, data["minbatch_msignal"], data["minbatch_msignal"] ) > -998, data["minbatch_msignal"], (5.95391893386840820) )) * 2.0)) * 2.0)))) +
                            0.100000*np.tanh(np.where(((data["abs_maxbatch_slices2_msignal"]) * (data["abs_maxbatch_slices2"])) > -998, ((((data["abs_maxbatch_slices2"]) + ((5.26387929916381836)))) + (((data["minbatch_slices2_msignal"]) * (data["abs_maxbatch_slices2"])))), data["stdbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(data["rangebatch_msignal"]) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] <= -998, np.where(((data["medianbatch_slices2"]) * 2.0) <= -998, data["medianbatch_slices2"], ((data["stdbatch_slices2"]) * (((np.tanh(((9.0)))) * 2.0))) ), (((9.0)) - (data["rangebatch_msignal"])) )) +
                            0.100000*np.tanh(((data["minbatch"]) + (((data["minbatch"]) + (((data["signal"]) - (data["abs_avgbatch_msignal"]))))))) +
                            0.100000*np.tanh(((data["abs_maxbatch"]) + ((((((((((7.0)) - (data["abs_maxbatch_msignal"]))) * (data["medianbatch_msignal"]))) * (data["maxbatch_msignal"]))) * (data["maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(((data["medianbatch_msignal"]) / 2.0) <= -998, np.tanh((data["medianbatch_msignal"])), ((data["medianbatch_slices2"]) * (((((np.tanh((((data["medianbatch_slices2"]) * (data["meanbatch_slices2"]))))) * 2.0)) * 2.0))) )) +
                            0.100000*np.tanh((((data["mean_abs_chgbatch_slices2_msignal"]) + (((((((4.0)) + ((((data["abs_minbatch_slices2_msignal"]) + (data["abs_avgbatch_msignal"]))/2.0)))) + ((((data["minbatch_msignal"]) + ((4.0)))/2.0)))/2.0)))/2.0)) +
                            0.100000*np.tanh((((((((((8.0)) - (((np.where((4.0) <= -998, (4.0), data["medianbatch_slices2_msignal"] )) + (((data["rangebatch_slices2"]) + ((-(((4.0))))))))))) * 2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((9.87458992004394531)) * 2.0)) +
                            0.100000*np.tanh(((((np.where(data["maxtominbatch_slices2_msignal"] <= -998, data["medianbatch_msignal"], ((data["stdbatch_slices2_msignal"]) - (data["maxbatch_slices2_msignal"])) )) - (((data["medianbatch_msignal"]) * 2.0)))) * (((data["stdbatch_slices2_msignal"]) * (((data["maxtominbatch_slices2_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh(np.tanh((((data["maxtominbatch_slices2_msignal"]) * (((((data["maxtominbatch_msignal"]) * 2.0)) - (np.tanh((data["rangebatch_msignal"]))))))))) +
                            0.100000*np.tanh((((data["minbatch_msignal"]) + (data["maxbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2_msignal"] > -998, ((data["maxbatch_slices2_msignal"]) * (((data["maxbatch_slices2_msignal"]) * ((((7.0)) - (((data["maxbatch_slices2_msignal"]) * ((((7.0)) - (data["maxbatch_msignal"])))))))))), (7.0) )) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2"]) * (np.where((6.24817132949829102) > -998, ((((data["minbatch_msignal"]) - (((data["medianbatch_msignal"]) * (data["medianbatch_slices2_msignal"]))))) - ((-(((6.24817132949829102)))))), (-(((6.57670259475708008)))) )))) +
                            0.100000*np.tanh(data["medianbatch_slices2"]) +
                            0.100000*np.tanh(((((np.where(np.tanh((data["abs_maxbatch_slices2"])) <= -998, data["medianbatch_msignal"], np.where(data["stdbatch_slices2"] <= -998, data["abs_maxbatch"], data["abs_avgbatch_msignal"] ) )) * (data["abs_minbatch_slices2"]))) + (np.tanh((data["medianbatch_slices2"]))))) +
                            0.100000*np.tanh(data["medianbatch_slices2"]) +
                            0.100000*np.tanh((((((data["abs_avgbatch_slices2_msignal"]) * (((((((data["maxtominbatch_msignal"]) / 2.0)) * 2.0)) / 2.0)))) + (((data["maxtominbatch_slices2_msignal"]) * 2.0)))/2.0)))  
    
    def GP_class_2(self,data):
        return self.Output( -2.200047 +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * ((((data["maxbatch_slices2"]) + (((((data["maxbatch_slices2"]) * (data["rangebatch_slices2"]))) + ((((data["minbatch_slices2_msignal"]) + (((data["abs_avgbatch_msignal"]) * (data["maxbatch_slices2"]))))/2.0)))))/2.0)))) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) * (data["meanbatch_msignal"]))) + (np.where(data["abs_avgbatch_slices2_msignal"] > -998, ((data["abs_avgbatch_slices2_msignal"]) * (data["maxbatch_slices2"])), data["abs_avgbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) * (data["maxbatch_slices2"]))) + (np.tanh((((data["stdbatch_slices2_msignal"]) * (data["meanbatch_slices2"]))))))) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) + (((((data["maxbatch_slices2"]) / 2.0)) + (((np.where(data["maxbatch_slices2"] <= -998, data["meanbatch_slices2_msignal"], data["maxbatch_slices2"] )) * 2.0)))))) * (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2_msignal"] <= -998, ((data["maxbatch_slices2"]) * 2.0), data["maxbatch_slices2"] )) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) * (data["abs_maxbatch"]))) * (data["mean_abs_chgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) + (((data["abs_minbatch_slices2_msignal"]) + (((data["maxbatch_slices2"]) * (data["abs_avgbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) * (np.where((((data["maxbatch_slices2"]) + (data["medianbatch_slices2"]))/2.0) > -998, ((data["maxbatch_slices2"]) * 2.0), ((data["medianbatch_msignal"]) + (data["maxbatch_slices2"])) )))) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1"] <= -998, ((data["maxbatch_slices2"]) * (((data["abs_avgbatch_slices2_msignal"]) * 2.0))), ((data["maxbatch_slices2"]) * (np.where(((data["maxtominbatch_msignal"]) * 2.0) > -998, data["abs_avgbatch_slices2_msignal"], data["maxbatch_slices2"] ))) )) +
                            0.100000*np.tanh(((((((data["mean_abs_chgbatch_slices2_msignal"]) * (data["abs_avgbatch_slices2"]))) * (data["maxbatch_slices2"]))) + (((data["mean_abs_chgbatch_slices2"]) * (((data["maxbatch_slices2"]) / 2.0)))))) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_msignal"] > -998, ((np.tanh((((((data["meanbatch_slices2_msignal"]) * (data["maxbatch_slices2"]))) * 2.0)))) / 2.0), data["meanbatch_msignal"] )) +
                            0.100000*np.tanh(((np.tanh((data["maxbatch_slices2"]))) * (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) * (np.where(np.tanh((data["abs_minbatch_slices2"])) > -998, data["signal_shift_+1"], np.tanh((((np.tanh((data["abs_maxbatch_msignal"]))) * (np.where(data["minbatch"] > -998, data["signal_shift_+1"], data["stdbatch_slices2_msignal"] ))))) )))) +
                            0.100000*np.tanh(np.where(((((data["maxbatch_slices2"]) * 2.0)) * 2.0) <= -998, data["signal_shift_-1"], np.where(data["maxbatch_slices2"] <= -998, np.where(((data["maxbatch_slices2_msignal"]) / 2.0) <= -998, data["abs_maxbatch_slices2_msignal"], ((data["maxbatch_slices2"]) * 2.0) ), data["maxbatch_slices2"] ) )) +
                            0.100000*np.tanh(((((((np.where(data["maxtominbatch"] > -998, data["minbatch"], data["medianbatch_slices2_msignal"] )) * 2.0)) - (data["maxtominbatch"]))) - (((data["minbatch"]) - (((data["maxtominbatch"]) + (data["meanbatch_slices2"]))))))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_msignal"]) * (((((((data["rangebatch_slices2_msignal"]) + (data["maxtominbatch_msignal"]))) * (data["stdbatch_msignal"]))) + (data["abs_minbatch_slices2_msignal"]))))) * (((data["mean_abs_chgbatch_msignal"]) * ((-((data["maxtominbatch_msignal"])))))))) +
                            0.100000*np.tanh(np.where((((7.10836696624755859)) / 2.0) > -998, data["stdbatch_slices2_msignal"], ((data["mean_abs_chgbatch_slices2_msignal"]) * 2.0) )) +
                            0.100000*np.tanh(((((data["abs_avgbatch_msignal"]) * (((((((((4.0)) * (data["mean_abs_chgbatch_slices2_msignal"]))) + (data["maxbatch_slices2"]))/2.0)) * (data["mean_abs_chgbatch_slices2_msignal"]))))) * 2.0)) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) * ((((data["maxbatch_slices2"]) + (((data["minbatch"]) * (np.where(np.tanh((((((data["meanbatch_slices2_msignal"]) * 2.0)) * 2.0))) <= -998, data["stdbatch_msignal"], data["medianbatch_slices2"] )))))/2.0)))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) * (data["rangebatch_slices2"]))) +
                            0.100000*np.tanh(np.where(((((((data["rangebatch_slices2"]) * 2.0)) / 2.0)) * 2.0) <= -998, data["mean_abs_chgbatch_slices2_msignal"], ((data["signal"]) - ((-((data["maxbatch_slices2"]))))) )) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) * (((data["maxtominbatch"]) + (np.where(np.where(data["abs_minbatch_msignal"] > -998, ((data["abs_minbatch_slices2_msignal"]) * 2.0), ((data["rangebatch_msignal"]) - (data["maxbatch_slices2"])) ) > -998, data["maxbatch_slices2"], data["abs_minbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2_msignal"]) + (data["maxbatch_slices2"]))) + (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(((((((data["abs_minbatch_msignal"]) * (((data["rangebatch_msignal"]) + (data["maxtominbatch"]))))) - (data["maxtominbatch"]))) - (data["maxtominbatch"]))) +
                            0.100000*np.tanh(np.where(((data["medianbatch_slices2_msignal"]) - (data["mean_abs_chgbatch_slices2_msignal"])) <= -998, ((data["maxbatch_slices2"]) / 2.0), ((data["mean_abs_chgbatch_slices2_msignal"]) * (((data["maxbatch_slices2"]) - (((data["abs_minbatch_msignal"]) + (data["meanbatch_msignal"])))))) )) +
                            0.100000*np.tanh(((np.where(data["stdbatch_msignal"] > -998, data["abs_avgbatch_msignal"], ((data["maxbatch_slices2"]) * (((data["meanbatch_slices2_msignal"]) * (((data["stdbatch_msignal"]) + (data["maxbatch_slices2"])))))) )) * (((data["abs_avgbatch_msignal"]) + (data["rangebatch_msignal"]))))) +
                            0.100000*np.tanh(((np.tanh((data["meanbatch_slices2_msignal"]))) + (((((data["meanbatch_slices2_msignal"]) * 2.0)) * 2.0)))) +
                            0.100000*np.tanh((((-(((-((data["meanbatch_slices2"]))))))) + (np.where((-((((data["minbatch_msignal"]) / 2.0)))) <= -998, data["minbatch_slices2"], ((data["signal_shift_+1"]) + (data["mean_abs_chgbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(((np.where((((data["stdbatch_slices2"]) + ((((-(((4.46349000930786133))))) * (data["maxtominbatch_slices2_msignal"]))))/2.0) > -998, data["meanbatch_slices2"], data["abs_avgbatch_msignal"] )) * ((((np.tanh((data["abs_avgbatch_msignal"]))) + (data["maxtominbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh((((-((((data["signal_shift_+1"]) * (data["signal"])))))) * (((data["abs_maxbatch"]) + ((((data["maxtominbatch_slices2_msignal"]) + (data["maxtominbatch_slices2_msignal"]))/2.0)))))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) / 2.0)) +
                            0.100000*np.tanh(((((((((data["stdbatch_slices2"]) + (data["minbatch"]))) * 2.0)) * 2.0)) + (((data["signal"]) * (data["medianbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch"] <= -998, data["minbatch"], ((data["maxbatch_slices2"]) - (((data["mean_abs_chgbatch_slices2"]) * (data["abs_maxbatch_slices2"])))) )) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) * ((((data["maxtominbatch_slices2"]) + (np.where(((data["meanbatch_slices2_msignal"]) * (data["maxtominbatch_slices2"])) > -998, data["abs_maxbatch_slices2"], np.where(data["maxtominbatch_slices2"] > -998, data["meanbatch_slices2_msignal"], data["abs_maxbatch_slices2"] ) )))/2.0)))) +
                            0.100000*np.tanh((((((5.0)) - (data["abs_maxbatch_msignal"]))) * 2.0)) +
                            0.100000*np.tanh(((np.where(data["abs_maxbatch_slices2"] <= -998, np.where(data["abs_maxbatch_slices2"] > -998, data["maxbatch_slices2_msignal"], data["abs_avgbatch_slices2"] ), data["maxbatch_slices2"] )) + (((data["meanbatch_msignal"]) * (((((data["maxbatch_slices2"]) * 2.0)) * 2.0)))))) +
                            0.100000*np.tanh(((data["minbatch"]) * ((((data["maxtominbatch_msignal"]) + (((data["medianbatch_slices2"]) * (np.where(data["maxtominbatch_msignal"] > -998, data["abs_avgbatch_slices2"], data["abs_minbatch_slices2"] )))))/2.0)))) +
                            0.100000*np.tanh(data["medianbatch_slices2"]) +
                            0.100000*np.tanh((((((6.0)) - (data["abs_minbatch_msignal"]))) - (((data["medianbatch_slices2"]) * (((data["abs_minbatch_slices2_msignal"]) * (data["minbatch"]))))))) +
                            0.100000*np.tanh(((np.where((((((data["medianbatch_msignal"]) + (data["minbatch_msignal"]))/2.0)) + (data["minbatch_msignal"])) > -998, (-(((((data["minbatch_msignal"]) + ((5.0)))/2.0)))), data["maxtominbatch_msignal"] )) * (((data["minbatch_msignal"]) / 2.0)))) +
                            0.100000*np.tanh(np.tanh(((-((data["abs_maxbatch_msignal"])))))) +
                            0.100000*np.tanh(((((((data["minbatch_msignal"]) * 2.0)) - ((-(((13.87994098663330078))))))) - (data["rangebatch_slices2"]))) +
                            0.100000*np.tanh(np.tanh((data["abs_avgbatch_slices2"]))) +
                            0.100000*np.tanh((5.46487379074096680)) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) + (np.where(((np.tanh((data["stdbatch_msignal"]))) - ((((10.0)) / 2.0))) > -998, (7.93056774139404297), data["abs_minbatch_slices2_msignal"] )))) - ((-((data["minbatch_msignal"])))))) +
                            0.100000*np.tanh((((data["minbatch"]) + (data["signal"]))/2.0)) +
                            0.100000*np.tanh(((np.tanh((data["rangebatch_msignal"]))) + (((((data["rangebatch_slices2_msignal"]) + (data["signal_shift_+1"]))) - (data["signal_shift_+1"]))))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2"]) * (((np.tanh((np.tanh((data["abs_maxbatch_slices2_msignal"]))))) - (((data["medianbatch_msignal"]) * (data["medianbatch_msignal"]))))))) +
                            0.100000*np.tanh((((7.0)) - (np.where(data["meanbatch_slices2"] > -998, data["rangebatch_msignal"], (((7.0)) - (np.where(np.tanh(((7.0))) > -998, (7.0), np.tanh((data["rangebatch_msignal"])) ))) )))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) + (np.where(((data["abs_minbatch_slices2_msignal"]) - (data["maxtominbatch"])) > -998, data["abs_avgbatch_slices2_msignal"], np.where(data["maxtominbatch_slices2"] <= -998, ((data["maxbatch_msignal"]) / 2.0), np.tanh((data["minbatch_msignal"])) ) )))) +
                            0.100000*np.tanh(((((data["stdbatch_slices2"]) / 2.0)) + (((data["minbatch"]) + (((data["abs_avgbatch_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh((-((((data["medianbatch_slices2_msignal"]) * (np.where(((data["medianbatch_slices2_msignal"]) * (np.where(((data["medianbatch_msignal"]) + (data["mean_abs_chgbatch_msignal"])) > -998, data["medianbatch_slices2_msignal"], data["maxbatch_slices2"] ))) > -998, data["medianbatch_slices2_msignal"], data["medianbatch_slices2_msignal"] ))))))) +
                            0.100000*np.tanh((((np.where(((data["mean_abs_chgbatch_slices2"]) + (data["abs_avgbatch_slices2"])) <= -998, data["maxtominbatch"], ((data["mean_abs_chgbatch_slices2"]) * (((data["maxbatch_slices2"]) - (data["mean_abs_chgbatch_slices2_msignal"])))) )) + (data["rangebatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh((((4.73975753784179688)) + (np.where(data["minbatch_msignal"] > -998, data["minbatch_msignal"], ((data["minbatch_msignal"]) + (np.where((((4.73975753784179688)) + (data["minbatch_msignal"])) > -998, data["minbatch_msignal"], data["minbatch_msignal"] ))) )))) +
                            0.100000*np.tanh(((data["minbatch_slices2"]) + ((((((((data["signal"]) - (data["minbatch"]))) + (data["maxtominbatch"]))/2.0)) * (data["mean_abs_chgbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((((np.where((((8.0)) / 2.0) <= -998, data["minbatch_slices2_msignal"], (8.0) )) - (((data["signal_shift_+1_msignal"]) + (((data["minbatch_msignal"]) * (((data["minbatch_msignal"]) / 2.0)))))))) * 2.0)) +
                            0.100000*np.tanh((((((5.63527631759643555)) * ((((5.63527631759643555)) - (np.where(data["medianbatch_slices2"] > -998, data["maxbatch_slices2_msignal"], data["minbatch"] )))))) * (((data["abs_maxbatch"]) - (data["maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((((-(((((data["stdbatch_slices2_msignal"]) + (np.tanh((((data["abs_avgbatch_slices2"]) + (data["mean_abs_chgbatch_msignal"]))))))/2.0))))) + (np.tanh((data["medianbatch_slices2"]))))/2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) + (np.where((((5.0)) + (data["minbatch_msignal"])) > -998, ((data["minbatch_msignal"]) + ((((5.0)) * ((((5.0)) + (data["minbatch_msignal"])))))), (5.0) )))) +
                            0.100000*np.tanh(((((((data["stdbatch_slices2_msignal"]) * (data["abs_avgbatch_msignal"]))) + (data["maxtominbatch_msignal"]))) * 2.0)) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) + (((data["signal"]) * (((((data["minbatch"]) + ((2.47419881820678711)))) * (data["abs_maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(data["abs_avgbatch_msignal"]) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) - (((((data["abs_maxbatch_slices2"]) * (data["medianbatch_msignal"]))) * (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2"]) * (((data["abs_maxbatch_msignal"]) - ((-((((data["meanbatch_slices2"]) * (((data["mean_abs_chgbatch_msignal"]) - ((-((data["abs_maxbatch_msignal"]))))))))))))))) * 2.0)) +
                            0.100000*np.tanh(np.where((5.0) <= -998, ((data["mean_abs_chgbatch_slices2"]) - (data["minbatch_msignal"])), ((((data["minbatch_msignal"]) - (((np.tanh((data["abs_avgbatch_slices2_msignal"]))) - ((5.0)))))) * 2.0) )) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) * (np.where(data["minbatch"] > -998, data["minbatch"], data["maxtominbatch_slices2"] )))) +
                            0.100000*np.tanh((((((12.84755516052246094)) - (((data["abs_maxbatch_msignal"]) * 2.0)))) + (np.tanh((np.tanh(((((12.84755516052246094)) - (((data["maxbatch_msignal"]) * 2.0)))))))))) +
                            0.100000*np.tanh(((np.where(data["meanbatch_slices2"] > -998, data["abs_avgbatch_msignal"], ((((data["abs_minbatch_slices2"]) * (data["meanbatch_slices2"]))) * (data["meanbatch_slices2"])) )) * (data["abs_minbatch_slices2"]))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2_msignal"]) * (((data["mean_abs_chgbatch_slices2"]) - (((data["medianbatch_msignal"]) * (data["medianbatch_msignal"]))))))) - (((((data["medianbatch_msignal"]) * 2.0)) * (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh((((12.58013534545898438)) - (((np.where(data["mean_abs_chgbatch_slices2_msignal"] <= -998, data["abs_minbatch_slices2_msignal"], data["minbatch_slices2_msignal"] )) * (data["minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2"]) * ((((12.26733589172363281)) + ((((-((data["maxbatch_slices2_msignal"])))) * 2.0)))))) / 2.0)) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2"] <= -998, data["medianbatch_slices2"], (((((((((8.0)) + (((((8.0)) + (((data["abs_avgbatch_msignal"]) / 2.0)))/2.0)))/2.0)) + (data["minbatch_msignal"]))/2.0)) * (data["medianbatch_slices2"])) )) +
                            0.100000*np.tanh(np.where(np.where(data["abs_minbatch_slices2_msignal"] <= -998, (((4.0)) + (data["abs_maxbatch_msignal"])), data["abs_minbatch_slices2_msignal"] ) <= -998, (7.52903413772583008), ((((data["minbatch_msignal"]) + ((4.0)))) * ((13.89663124084472656))) )) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(((np.where(data["mean_abs_chgbatch_msignal"] <= -998, (9.0), (9.0) )) * (((data["minbatch_slices2_msignal"]) + ((((8.0)) / 2.0)))))) +
                            0.100000*np.tanh(np.tanh(((((((data["abs_avgbatch_msignal"]) * (data["maxbatch_slices2"]))) + (data["abs_maxbatch"]))/2.0)))) +
                            0.100000*np.tanh((((((data["maxbatch_slices2"]) + (data["medianbatch_msignal"]))/2.0)) - (np.where(np.tanh((data["rangebatch_slices2"])) > -998, ((((data["rangebatch_slices2"]) * (data["medianbatch_slices2_msignal"]))) * (data["medianbatch_msignal"])), data["rangebatch_slices2"] )))) +
                            0.100000*np.tanh(((np.tanh((data["meanbatch_slices2"]))) + (data["stdbatch_slices2"]))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * (((np.tanh((data["meanbatch_slices2_msignal"]))) - (data["abs_avgbatch_msignal"]))))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2"]) + (np.where(((np.where(data["meanbatch_slices2_msignal"] > -998, data["meanbatch_slices2_msignal"], data["meanbatch_msignal"] )) * 2.0) > -998, data["meanbatch_msignal"], ((data["minbatch_slices2_msignal"]) * (data["maxbatch_slices2_msignal"])) )))) * (data["abs_maxbatch"]))) +
                            0.100000*np.tanh(((np.where(data["meanbatch_msignal"] > -998, data["minbatch_msignal"], np.where(data["meanbatch_slices2_msignal"] > -998, data["minbatch_msignal"], ((data["signal_shift_+1_msignal"]) + (np.where(data["minbatch_msignal"] <= -998, data["minbatch_msignal"], data["maxtominbatch_msignal"] ))) ) )) + ((4.0)))) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) + (((((data["mean_abs_chgbatch_msignal"]) * (data["abs_avgbatch_msignal"]))) * (data["abs_avgbatch_msignal"]))))) +
                            0.100000*np.tanh((((((((((5.19775438308715820)) * 2.0)) - (((data["rangebatch_slices2"]) + (np.where((4.0) > -998, ((((data["meanbatch_msignal"]) / 2.0)) * 2.0), data["meanbatch_msignal"] )))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) * (((np.where(np.where(data["abs_maxbatch_msignal"] <= -998, data["abs_maxbatch_msignal"], data["minbatch_msignal"] ) <= -998, data["abs_maxbatch_msignal"], data["minbatch_msignal"] )) + (data["abs_maxbatch_msignal"]))))) +
                            0.100000*np.tanh((((7.0)) - (((data["medianbatch_msignal"]) * (((((data["rangebatch_slices2"]) + ((7.0)))) * (((((data["medianbatch_msignal"]) / 2.0)) + (data["medianbatch_msignal"]))))))))) +
                            0.100000*np.tanh(((((((data["minbatch_msignal"]) + (((data["minbatch_msignal"]) + (np.where((8.56654834747314453) > -998, (8.56654834747314453), np.where((8.56654834747314453) > -998, data["minbatch_msignal"], data["minbatch_msignal"] ) )))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((data["stdbatch_msignal"]) * (np.where(data["stdbatch_msignal"] <= -998, ((((((data["meanbatch_msignal"]) * 2.0)) * 2.0)) * 2.0), ((data["meanbatch_msignal"]) * 2.0) )))) - (data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(((((((data["abs_avgbatch_slices2_msignal"]) * (((np.where(data["maxtominbatch_msignal"] > -998, data["mean_abs_chgbatch_slices2"], ((data["medianbatch_msignal"]) + (data["mean_abs_chgbatch_slices2_msignal"])) )) + (data["medianbatch_slices2"]))))) + (data["maxtominbatch_slices2_msignal"]))) * ((1.15666174888610840)))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((((10.0)) + ((-((np.where((-((data["minbatch_msignal"]))) <= -998, data["minbatch"], data["meanbatch_slices2_msignal"] ))))))/2.0)))) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) - (((((data["minbatch"]) + ((((data["minbatch"]) + (data["minbatch"]))/2.0)))) * (data["minbatch"]))))) +
                            0.100000*np.tanh((((6.07512617111206055)) - (np.where((6.07512617111206055) > -998, data["maxbatch_slices2_msignal"], data["maxbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((((((data["medianbatch_msignal"]) * 2.0)) + (np.tanh((((((-((data["signal"])))) + (((((data["abs_minbatch_msignal"]) * (((data["medianbatch_msignal"]) * 2.0)))) * 2.0)))/2.0)))))) * (data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh(((((((data["signal_shift_-1"]) / 2.0)) * (data["abs_avgbatch_msignal"]))) / 2.0)) +
                            0.100000*np.tanh((((data["mean_abs_chgbatch_msignal"]) + (((((np.where(((data["maxtominbatch_slices2_msignal"]) * (((data["maxtominbatch_slices2_msignal"]) - (data["meanbatch_slices2"])))) > -998, data["maxbatch_msignal"], data["maxbatch_msignal"] )) * 2.0)) + (data["minbatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh(((data["rangebatch_slices2_msignal"]) + (((((((data["rangebatch_slices2_msignal"]) * 2.0)) + (((data["rangebatch_slices2_msignal"]) + (((data["minbatch_msignal"]) * (data["rangebatch_msignal"]))))))) + (((data["abs_maxbatch_slices2_msignal"]) - (data["mean_abs_chgbatch_msignal"]))))))) +
                            0.100000*np.tanh(((np.where((((data["meanbatch_msignal"]) + (data["meanbatch_msignal"]))/2.0) > -998, np.tanh((data["meanbatch_msignal"])), data["meanbatch_msignal"] )) * (((((data["maxtominbatch"]) / 2.0)) / 2.0)))) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(((data["stdbatch_slices2_msignal"]) * (((data["mean_abs_chgbatch_slices2_msignal"]) * (np.tanh((((data["abs_avgbatch_msignal"]) - (((((data["medianbatch_msignal"]) * 2.0)) * 2.0)))))))))) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * (np.where(data["abs_maxbatch_msignal"] <= -998, np.tanh((data["abs_maxbatch_msignal"])), (((5.79516458511352539)) - (data["abs_maxbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh((((((((-((((data["minbatch"]) * (data["abs_minbatch_msignal"])))))) + (((data["minbatch"]) * (data["abs_minbatch_msignal"]))))) + (((((data["meanbatch_slices2"]) * 2.0)) / 2.0)))) / 2.0)) +
                            0.100000*np.tanh(((((((np.tanh((((data["meanbatch_slices2_msignal"]) * ((((((((((((((data["minbatch_slices2_msignal"]) + ((3.27702713012695312)))/2.0)) * 2.0)) * 2.0)) * 2.0)) * 2.0)) * 2.0)))))) * 2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((data["abs_avgbatch_msignal"]) + (data["meanbatch_msignal"]))) + (np.where(data["rangebatch_msignal"] <= -998, data["meanbatch_slices2_msignal"], ((data["meanbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2"])) )))) +
                            0.100000*np.tanh((((((((data["meanbatch_slices2_msignal"]) + (np.where(data["stdbatch_slices2_msignal"] > -998, data["meanbatch_slices2_msignal"], data["rangebatch_slices2"] )))) + ((13.57393360137939453)))/2.0)) - (np.where(data["meanbatch_slices2_msignal"] > -998, data["rangebatch_slices2"], data["medianbatch_msignal"] )))) +
                            0.100000*np.tanh((((((data["abs_maxbatch_slices2"]) * (((data["stdbatch_msignal"]) * (data["mean_abs_chgbatch_msignal"]))))) + (data["medianbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.where(data["stdbatch_slices2_msignal"] > -998, ((data["stdbatch_slices2_msignal"]) / 2.0), data["stdbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(((data["minbatch"]) + (np.where(data["medianbatch_slices2"] > -998, data["medianbatch_slices2"], (-(((13.15357017517089844)))) )))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2"]) - ((4.0)))) * ((((((4.0)) * 2.0)) - (data["rangebatch_slices2"]))))) +
                            0.100000*np.tanh((((np.where(data["mean_abs_chgbatch_slices2"] > -998, data["mean_abs_chgbatch_slices2"], data["abs_avgbatch_msignal"] )) + (data["abs_avgbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh((((6.0)) - (((data["rangebatch_slices2"]) - (np.where(np.tanh((data["mean_abs_chgbatch_msignal"])) <= -998, data["meanbatch_slices2_msignal"], data["meanbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) - (np.where(((data["minbatch_msignal"]) * (data["abs_maxbatch_slices2_msignal"])) <= -998, (((data["rangebatch_msignal"]) + (data["abs_maxbatch_slices2"]))/2.0), ((data["maxtominbatch_slices2"]) * 2.0) )))) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_slices2_msignal"] > -998, np.where(data["stdbatch_slices2_msignal"] > -998, ((data["signal_shift_+1_msignal"]) * (data["signal_shift_+1_msignal"])), data["abs_minbatch_slices2"] ), data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2"] <= -998, data["medianbatch_msignal"], ((((data["maxbatch_slices2_msignal"]) - (((((data["maxbatch_slices2_msignal"]) * (((data["medianbatch_msignal"]) * 2.0)))) * (data["medianbatch_slices2_msignal"]))))) * 2.0) )) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) + (((((data["meanbatch_slices2_msignal"]) * 2.0)) + (data["abs_minbatch_slices2_msignal"]))))) + (((data["maxtominbatch_slices2"]) / 2.0)))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2"]) - (((((-((data["abs_maxbatch"])))) + (((data["maxbatch_msignal"]) + ((7.0)))))/2.0)))) - (np.tanh((np.where((8.17136955261230469) > -998, (8.17136955261230469), data["rangebatch_slices2"] )))))) +
                            0.100000*np.tanh((((3.0)) - (((((((data["abs_maxbatch_slices2_msignal"]) * (((data["minbatch_msignal"]) + ((3.0)))))) * (((data["minbatch_msignal"]) + ((3.0)))))) * 2.0)))) +
                            0.100000*np.tanh(((np.where(data["minbatch"] > -998, (9.0), ((data["maxbatch_slices2"]) * (data["minbatch_msignal"])) )) + (((((data["signal_shift_-1"]) * (data["minbatch"]))) * 2.0)))) +
                            0.100000*np.tanh(np.where(data["rangebatch_msignal"] > -998, np.tanh((((((data["medianbatch_slices2"]) / 2.0)) / 2.0))), data["abs_maxbatch"] )) +
                            0.100000*np.tanh(np.where(((((data["stdbatch_msignal"]) / 2.0)) * ((1.44617950916290283))) <= -998, data["abs_maxbatch_slices2_msignal"], (((10.0)) - ((((-((data["minbatch_msignal"])))) * 2.0))) )) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] <= -998, ((data["meanbatch_msignal"]) + (data["abs_minbatch_slices2_msignal"])), ((((np.where(data["medianbatch_msignal"] <= -998, data["abs_minbatch_slices2_msignal"], data["medianbatch_msignal"] )) * (((data["medianbatch_msignal"]) + (data["abs_minbatch_slices2_msignal"]))))) * 2.0) )) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) + (((data["maxtominbatch_slices2_msignal"]) * ((((data["maxtominbatch"]) + (data["signal"]))/2.0)))))) +
                            0.100000*np.tanh(np.where(data["signal"] > -998, ((data["signal_shift_-1"]) + (data["stdbatch_slices2"])), data["signal_shift_-1"] )) +
                            0.100000*np.tanh(((data["stdbatch_slices2"]) - (np.where(data["stdbatch_slices2"] <= -998, data["mean_abs_chgbatch_slices2_msignal"], (((((10.0)) * (((data["maxbatch_slices2_msignal"]) - ((4.0)))))) * (((data["maxbatch_slices2_msignal"]) - ((5.0))))) )))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) * (np.where(data["abs_avgbatch_msignal"] <= -998, data["meanbatch_slices2_msignal"], ((data["signal_shift_+1"]) * 2.0) )))) + (((((((7.78565692901611328)) - (data["rangebatch_msignal"]))) + (data["abs_avgbatch_slices2"]))/2.0)))) +
                            0.100000*np.tanh(((((((11.90193367004394531)) + (data["abs_avgbatch_slices2_msignal"]))/2.0)) + ((-((np.where(data["abs_maxbatch_msignal"] > -998, data["abs_maxbatch_msignal"], data["meanbatch_slices2_msignal"] ))))))) +
                            0.100000*np.tanh(((np.where(data["maxbatch_slices2"] > -998, ((data["maxbatch_slices2"]) + (((data["rangebatch_slices2_msignal"]) * (((data["meanbatch_slices2_msignal"]) * (data["abs_avgbatch_msignal"])))))), data["signal_shift_+1"] )) + (data["meanbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.tanh((np.tanh((((((data["medianbatch_slices2_msignal"]) * 2.0)) * (data["maxtominbatch_msignal"]))))))) +
                            0.100000*np.tanh(((((np.where(data["abs_maxbatch_msignal"] <= -998, data["signal_shift_+1"], ((((data["abs_minbatch_slices2_msignal"]) * (((data["signal_shift_+1"]) - (data["meanbatch_slices2"]))))) * 2.0) )) + (data["abs_avgbatch_msignal"]))) + (data["abs_avgbatch_slices2"]))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) * (((((((((data["signal_shift_-1_msignal"]) * 2.0)) + (data["signal_shift_-1_msignal"]))) + (data["signal_shift_-1_msignal"]))) * 2.0)))) + (data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh(((((data["maxbatch_slices2_msignal"]) + (((data["signal"]) * (((((data["meanbatch_slices2_msignal"]) * 2.0)) * 2.0)))))) + (((data["meanbatch_slices2_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - (((((data["medianbatch_slices2_msignal"]) * 2.0)) * (((((data["medianbatch_slices2_msignal"]) * 2.0)) * 2.0)))))) +
                            0.100000*np.tanh(np.where((((4.0)) * 2.0) <= -998, data["minbatch_msignal"], ((((((data["minbatch_msignal"]) + ((4.0)))) * 2.0)) * 2.0) )) +
                            0.100000*np.tanh(((((data["minbatch_slices2"]) * (data["signal"]))) + (np.where(data["meanbatch_slices2_msignal"] > -998, data["maxbatch_slices2"], np.where(((((3.0)) + (data["abs_maxbatch_msignal"]))/2.0) > -998, (3.0), data["maxtominbatch"] ) )))) +
                            0.100000*np.tanh(data["stdbatch_slices2"]) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) * (np.where(data["abs_avgbatch_msignal"] <= -998, data["meanbatch_slices2"], ((((data["meanbatch_slices2_msignal"]) * (data["rangebatch_slices2_msignal"]))) * 2.0) )))) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2_msignal"] <= -998, ((data["minbatch"]) + (((data["rangebatch_slices2_msignal"]) * (data["rangebatch_slices2_msignal"])))), ((data["minbatch"]) + (((data["stdbatch_slices2"]) * (((data["stdbatch_slices2"]) * (data["rangebatch_slices2_msignal"])))))) )) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * (((((((data["abs_maxbatch_msignal"]) / 2.0)) - (np.tanh((data["abs_avgbatch_msignal"]))))) * 2.0)))) +
                            0.100000*np.tanh((((data["mean_abs_chgbatch_slices2"]) + (data["maxbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((((((-((((np.tanh((data["abs_maxbatch_msignal"]))) / 2.0))))) / 2.0)) + ((((7.0)) - (data["rangebatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh((((((9.12419033050537109)) - (data["rangebatch_slices2"]))) + (np.where(np.tanh((((((9.12419033050537109)) + (data["abs_avgbatch_slices2"]))/2.0))) <= -998, data["maxtominbatch_msignal"], data["abs_minbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] <= -998, data["medianbatch_msignal"], ((data["signal_shift_-1_msignal"]) * (((data["abs_minbatch_slices2_msignal"]) + (data["medianbatch_msignal"])))) )) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2"]) +
                            0.100000*np.tanh(np.tanh((data["minbatch"]))) +
                            0.100000*np.tanh((((6.94316434860229492)) - (data["abs_avgbatch_slices2"]))) +
                            0.100000*np.tanh((((np.tanh((data["stdbatch_slices2"]))) + (np.tanh(((((((data["stdbatch_slices2"]) + (data["stdbatch_slices2"]))/2.0)) + (np.tanh((data["stdbatch_slices2"]))))))))/2.0)) +
                            0.100000*np.tanh(np.tanh((((np.where(((np.tanh((data["abs_minbatch_slices2_msignal"]))) - ((6.0))) > -998, data["maxtominbatch_slices2_msignal"], np.tanh((np.tanh((data["maxtominbatch_msignal"])))) )) - (data["medianbatch_slices2"]))))) +
                            0.100000*np.tanh(((((((((data["minbatch_slices2_msignal"]) + (((((((13.39893531799316406)) + (np.tanh((((((13.39893531799316406)) + (data["abs_maxbatch_msignal"]))/2.0)))))/2.0)) / 2.0)))) * 2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["stdbatch_slices2"]) * (((data["mean_abs_chgbatch_msignal"]) - (np.where((((((data["maxbatch_slices2_msignal"]) + (((data["mean_abs_chgbatch_slices2"]) + (data["minbatch_slices2"]))))/2.0)) * (data["maxbatch_msignal"])) > -998, data["maxtominbatch"], data["stdbatch_msignal"] )))))) +
                            0.100000*np.tanh(((((data["signal_shift_-1"]) * (data["abs_avgbatch_slices2_msignal"]))) + (data["abs_maxbatch"]))) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2"] > -998, data["abs_avgbatch_msignal"], data["mean_abs_chgbatch_slices2"] )) +
                            0.100000*np.tanh(((np.where(data["maxtominbatch_msignal"] > -998, (((data["abs_maxbatch_slices2"]) + (data["maxtominbatch_msignal"]))/2.0), data["maxtominbatch_msignal"] )) * (data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh((((5.25216341018676758)) * (((((5.25216341018676758)) + (np.where(data["abs_avgbatch_msignal"] > -998, ((np.where((5.25216341018676758) <= -998, (5.25216341018676758), data["stdbatch_slices2"] )) * (data["minbatch_msignal"])), (5.25216341018676758) )))/2.0)))) +
                            0.100000*np.tanh((((data["meanbatch_msignal"]) + (data["maxbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(data["maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.tanh((data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) + (np.where(data["maxbatch_msignal"] > -998, ((data["minbatch_msignal"]) * (data["mean_abs_chgbatch_slices2"])), data["minbatch_msignal"] )))) +
                            0.100000*np.tanh(data["abs_avgbatch_msignal"]) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) - (((data["stdbatch_slices2_msignal"]) * (np.where(data["mean_abs_chgbatch_slices2"] <= -998, data["signal_shift_-1"], data["minbatch"] )))))) +
                            0.100000*np.tanh((((-((data["rangebatch_slices2"])))) * (np.where(data["minbatch"] > -998, (((data["abs_avgbatch_slices2_msignal"]) + (data["minbatch_msignal"]))/2.0), (((((data["medianbatch_msignal"]) / 2.0)) + (data["minbatch_msignal"]))/2.0) )))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_msignal"] > -998, ((np.where(data["medianbatch_msignal"] > -998, data["maxtominbatch_msignal"], data["meanbatch_slices2"] )) + (((((data["medianbatch_slices2"]) * (data["meanbatch_msignal"]))) * (data["meanbatch_msignal"])))), np.tanh((data["medianbatch_msignal"])) )) +
                            0.100000*np.tanh(np.where(((data["medianbatch_slices2_msignal"]) / 2.0) > -998, (((0.0)) - (data["medianbatch_slices2_msignal"])), np.tanh((data["maxbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((((((data["rangebatch_slices2"]) - ((((10.03983688354492188)) + (((data["minbatch_msignal"]) * 2.0)))))) * ((((10.03983688354492188)) + (((data["minbatch_msignal"]) * 2.0)))))) * ((10.03983688354492188)))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * ((((((-((data["medianbatch_msignal"])))) + (np.where(data["signal_shift_-1_msignal"] > -998, data["signal_shift_-1_msignal"], ((data["abs_avgbatch_slices2_msignal"]) + (data["medianbatch_msignal"])) )))) * 2.0)))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) * 2.0)) + (data["maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((((data["abs_avgbatch_slices2_msignal"]) - (np.tanh((np.where(data["abs_maxbatch"] <= -998, data["minbatch"], data["abs_maxbatch_slices2"] )))))) + (data["stdbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh((((data["maxbatch_slices2_msignal"]) + (data["meanbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(((((((data["maxtominbatch_msignal"]) * 2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(data["minbatch"] > -998, data["abs_avgbatch_msignal"], data["meanbatch_msignal"] )) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) * (((((np.tanh((data["maxtominbatch"]))) + (((data["maxtominbatch"]) - (((data["maxtominbatch"]) * (data["abs_avgbatch_slices2_msignal"]))))))) + (data["minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((((data["maxbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"]))/2.0)) - ((((13.49778652191162109)) * ((((13.49778652191162109)) + (((((data["maxbatch_slices2_msignal"]) * (((data["mean_abs_chgbatch_msignal"]) - (data["rangebatch_slices2_msignal"]))))) * 2.0)))))))) +
                            0.100000*np.tanh(data["abs_avgbatch_msignal"]) +
                            0.100000*np.tanh((((7.15542745590209961)) - (np.where(data["rangebatch_slices2"] > -998, data["maxbatch_msignal"], ((np.where(data["meanbatch_slices2"] > -998, data["maxbatch_msignal"], data["maxbatch_msignal"] )) - (data["signal_shift_+1"])) )))) +
                            0.100000*np.tanh(((((data["minbatch"]) * (data["medianbatch_slices2"]))) - (np.where(((data["medianbatch_slices2_msignal"]) * (data["maxtominbatch"])) > -998, data["maxtominbatch"], ((data["minbatch"]) * (data["medianbatch_slices2"])) )))) +
                            0.100000*np.tanh(((((((((7.02210712432861328)) - (((data["rangebatch_slices2"]) + (np.tanh(((((7.02210712432861328)) + (np.tanh(((7.02210712432861328)))))))))))) + (data["meanbatch_msignal"]))/2.0)) * (data["rangebatch_slices2"]))) +
                            0.100000*np.tanh(((np.where(data["rangebatch_slices2_msignal"] > -998, ((data["medianbatch_slices2"]) / 2.0), data["maxbatch_slices2"] )) * 2.0)) +
                            0.100000*np.tanh(np.where(data["rangebatch_msignal"] > -998, ((data["maxbatch_slices2"]) * 2.0), data["rangebatch_msignal"] )) +
                            0.100000*np.tanh(((((((data["minbatch"]) + (data["mean_abs_chgbatch_slices2"]))) + ((4.0)))) + (((data["abs_minbatch_msignal"]) - (((np.where(data["maxbatch_msignal"] > -998, data["medianbatch_slices2_msignal"], data["mean_abs_chgbatch_slices2"] )) / 2.0)))))) +
                            0.100000*np.tanh(((np.where(data["rangebatch_slices2"] <= -998, np.where(((np.where(data["mean_abs_chgbatch_slices2"] <= -998, data["minbatch"], data["mean_abs_chgbatch_slices2"] )) / 2.0) <= -998, data["minbatch"], data["maxbatch_slices2_msignal"] ), data["mean_abs_chgbatch_slices2"] )) + (data["minbatch"]))) +
                            0.100000*np.tanh(((np.where(data["medianbatch_msignal"] > -998, data["medianbatch_slices2"], data["medianbatch_msignal"] )) + (((data["medianbatch_msignal"]) * (((data["medianbatch_msignal"]) * (((data["signal_shift_+1"]) * (data["mean_abs_chgbatch_msignal"]))))))))) +
                            0.100000*np.tanh(data["rangebatch_msignal"]) +
                            0.100000*np.tanh(((((data["abs_avgbatch_msignal"]) * (((data["abs_avgbatch_msignal"]) * (data["stdbatch_msignal"]))))) + ((((data["minbatch"]) + (data["abs_maxbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh(data["abs_maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((data["maxbatch_slices2_msignal"]) / 2.0)) + (((data["meanbatch_slices2_msignal"]) * (((((data["rangebatch_msignal"]) + (data["meanbatch_msignal"]))) + (((data["abs_avgbatch_slices2"]) + (data["maxbatch_slices2_msignal"]))))))))) +
                            0.100000*np.tanh(np.where(data["minbatch"] <= -998, ((((data["meanbatch_slices2"]) - (((data["minbatch"]) * (data["stdbatch_slices2_msignal"]))))) / 2.0), (((1.83019685745239258)) - (((data["minbatch"]) * (data["stdbatch_slices2_msignal"])))) )) +
                            0.100000*np.tanh((((((4.0)) * 2.0)) * (np.where((((4.0)) * 2.0) <= -998, data["abs_minbatch_slices2"], ((data["maxbatch_slices2_msignal"]) + ((((-(((((4.0)) * 2.0))))) / 2.0))) )))) +
                            0.100000*np.tanh(((((((data["maxbatch_slices2"]) * 2.0)) * (data["rangebatch_slices2_msignal"]))) * 2.0)) +
                            0.100000*np.tanh(((np.tanh(((((data["abs_minbatch_slices2"]) + (((((np.tanh((data["maxbatch_slices2_msignal"]))) * (data["abs_minbatch_slices2"]))) / 2.0)))/2.0)))) / 2.0)) +
                            0.100000*np.tanh(np.where(np.tanh((data["rangebatch_msignal"])) <= -998, data["abs_maxbatch_msignal"], ((data["abs_avgbatch_slices2"]) / 2.0) )) +
                            0.100000*np.tanh(np.tanh((np.where(data["maxtominbatch_slices2_msignal"] > -998, data["maxtominbatch_slices2_msignal"], ((((np.tanh((((data["medianbatch_slices2"]) / 2.0)))) / 2.0)) / 2.0) )))) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2"] <= -998, data["rangebatch_slices2_msignal"], data["signal"] )) +
                            0.100000*np.tanh(np.tanh((np.tanh((np.tanh((((data["mean_abs_chgbatch_slices2"]) / 2.0)))))))) +
                            0.100000*np.tanh(((np.where(data["rangebatch_slices2"] <= -998, data["rangebatch_msignal"], ((((((data["minbatch_slices2_msignal"]) * 2.0)) + ((7.0)))) * 2.0) )) + ((((7.42360544204711914)) - (data["rangebatch_slices2"]))))) +
                            0.100000*np.tanh(data["stdbatch_slices2"]) +
                            0.100000*np.tanh(np.tanh((np.tanh((data["signal"]))))))  
    
    def GP_class_3(self,data):
        return self.Output( -2.013422 +
                            0.100000*np.tanh(((data["signal_shift_-1"]) + (np.where(data["signal"] > -998, np.where(((data["signal"]) * 2.0) > -998, ((data["signal"]) + (data["signal"])), data["signal"] ), data["maxbatch_slices2"] )))) +
                            0.100000*np.tanh(np.where((-((data["signal"]))) > -998, ((((data["signal_shift_+1"]) - (data["abs_minbatch_msignal"]))) * 2.0), data["signal_shift_+1"] )) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1"] > -998, ((((data["signal"]) * (data["mean_abs_chgbatch_slices2_msignal"]))) - (((data["maxtominbatch_msignal"]) * 2.0))), np.where(data["abs_maxbatch"] > -998, data["signal_shift_+1"], data["stdbatch_slices2_msignal"] ) )) +
                            0.100000*np.tanh((((((data["signal"]) * 2.0)) + (((data["maxbatch_slices2"]) + ((((((((data["signal"]) * 2.0)) + (data["signal"]))/2.0)) * 2.0)))))/2.0)) +
                            0.100000*np.tanh(((data["signal"]) - (data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh(((((data["signal_shift_+1"]) * (np.where(((data["signal"]) / 2.0) <= -998, data["maxbatch_slices2_msignal"], data["stdbatch_msignal"] )))) + (np.where(data["signal"] <= -998, data["signal_shift_+1"], data["signal_shift_+1"] )))) +
                            0.100000*np.tanh(((data["signal"]) * 2.0)) +
                            0.100000*np.tanh(((((data["stdbatch_slices2_msignal"]) * (((data["stdbatch_slices2_msignal"]) * (((np.where(data["maxtominbatch_slices2_msignal"] <= -998, data["signal_shift_-1"], data["maxtominbatch_msignal"] )) - (((data["stdbatch_slices2_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))))))))) - (data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) * (((((data["minbatch"]) * 2.0)) * (np.where(data["maxtominbatch_msignal"] <= -998, (9.83937454223632812), ((((9.83937454223632812)) + (((data["minbatch_slices2_msignal"]) * 2.0)))/2.0) )))))) +
                            0.100000*np.tanh(((np.where(data["signal_shift_-1_msignal"] <= -998, (((data["signal"]) + (((data["signal"]) * (((((((data["signal"]) + (np.tanh((data["signal"]))))) * 2.0)) * 2.0)))))/2.0), data["signal"] )) * 2.0)) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) * (((data["signal_shift_-1"]) * 2.0)))) +
                            0.100000*np.tanh(((((data["signal"]) * (((data["mean_abs_chgbatch_slices2_msignal"]) - (data["signal_shift_+1"]))))) + (((data["signal"]) + (data["abs_maxbatch_msignal"]))))) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh((-((np.where(data["abs_maxbatch_slices2_msignal"] > -998, ((data["minbatch_slices2_msignal"]) + (np.where(data["abs_maxbatch_slices2_msignal"] > -998, data["abs_maxbatch_slices2_msignal"], ((((((data["abs_avgbatch_slices2"]) / 2.0)) * 2.0)) * (data["minbatch_slices2_msignal"])) ))), data["mean_abs_chgbatch_slices2"] ))))) +
                            0.100000*np.tanh(data["maxtominbatch_msignal"]) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(((data["rangebatch_slices2"]) - (data["rangebatch_slices2"])) <= -998, ((((data["stdbatch_msignal"]) * (data["signal"]))) * 2.0), ((((((data["signal"]) * 2.0)) * 2.0)) * 2.0) )) +
                            0.100000*np.tanh(np.where(((data["mean_abs_chgbatch_slices2"]) - (data["medianbatch_slices2"])) <= -998, ((data["medianbatch_slices2"]) * 2.0), ((((data["medianbatch_msignal"]) * ((((data["medianbatch_slices2"]) + (data["maxtominbatch"]))/2.0)))) * (data["rangebatch_slices2"])) )) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) * (((data["signal_shift_-1"]) + (data["maxtominbatch"]))))) +
                            0.100000*np.tanh(((((((data["stdbatch_slices2_msignal"]) * (data["signal"]))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) * (((data["abs_maxbatch"]) * (np.where(((data["stdbatch_msignal"]) * (data["signal"])) > -998, data["medianbatch_slices2"], data["maxtominbatch_slices2"] )))))) +
                            0.100000*np.tanh(((((data["signal"]) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((((((((data["medianbatch_msignal"]) * 2.0)) * 2.0)) * 2.0)) * (data["medianbatch_msignal"]))) - (np.where(data["maxtominbatch"] > -998, data["rangebatch_slices2"], data["abs_maxbatch"] )))) +
                            0.100000*np.tanh(np.where((((data["maxbatch_slices2"]) + (data["signal"]))/2.0) > -998, ((((((6.16182565689086914)) + (data["minbatch_msignal"]))/2.0)) * ((((6.16182565689086914)) * (data["signal"])))), ((((6.16182565689086914)) + (data["minbatch_msignal"]))/2.0) )) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_msignal"]) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) * (((((data["meanbatch_msignal"]) + (data["maxtominbatch_slices2"]))) + (((data["maxbatch_slices2"]) + (data["medianbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh((((2.99833846092224121)) - (((((data["minbatch"]) / 2.0)) * (np.where((((-((data["abs_avgbatch_msignal"])))) / 2.0) <= -998, data["abs_maxbatch_msignal"], ((data["maxtominbatch_msignal"]) / 2.0) )))))) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2_msignal"] <= -998, ((data["meanbatch_slices2_msignal"]) / 2.0), ((((data["maxtominbatch_slices2"]) * (data["medianbatch_msignal"]))) * 2.0) )) +
                            0.100000*np.tanh((((9.0)) - (data["rangebatch_slices2"]))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) - (((data["rangebatch_slices2"]) * (np.where(np.tanh((((data["maxbatch_msignal"]) * ((-((data["abs_maxbatch_slices2_msignal"]))))))) > -998, data["medianbatch_msignal"], data["maxbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2"]) * (data["signal"]))) +
                            0.100000*np.tanh((((((-((((data["minbatch_slices2_msignal"]) - ((4.0))))))) * (((data["medianbatch_msignal"]) * (data["medianbatch_msignal"]))))) - ((((data["meanbatch_msignal"]) + ((4.0)))/2.0)))) +
                            0.100000*np.tanh(((data["minbatch"]) + (((data["maxtominbatch"]) * (np.where(data["meanbatch_msignal"] > -998, data["meanbatch_slices2_msignal"], ((data["minbatch"]) * (np.where(data["maxtominbatch"] > -998, data["medianbatch_msignal"], data["meanbatch_slices2_msignal"] ))) )))))) +
                            0.100000*np.tanh((((5.0)) * (np.where((((5.0)) * ((5.0))) > -998, (((5.0)) - ((-((data["minbatch_msignal"]))))), (((5.0)) - ((5.0))) )))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * (((((((data["maxtominbatch"]) + (data["medianbatch_slices2"]))) + (data["medianbatch_msignal"]))) + (data["meanbatch_slices2"]))))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (((((data["maxtominbatch_slices2"]) - (data["minbatch_slices2"]))) - (np.where(((data["maxtominbatch_slices2_msignal"]) - (data["maxbatch_msignal"])) <= -998, data["mean_abs_chgbatch_slices2_msignal"], data["abs_minbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((((data["minbatch"]) * (data["abs_avgbatch_slices2"]))) + (((data["minbatch"]) - ((-((((data["abs_avgbatch_slices2"]) - ((-(((12.46027278900146484)))))))))))))) +
                            0.100000*np.tanh((((-(((((-((((((data["stdbatch_slices2"]) + (data["medianbatch_msignal"]))) + (((data["stdbatch_slices2"]) + (((data["medianbatch_msignal"]) * 2.0))))))))) * 2.0))))) * (data["minbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2"] > -998, (((5.16128301620483398)) - (data["maxbatch_msignal"])), data["maxbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_msignal"] <= -998, data["stdbatch_slices2_msignal"], ((data["medianbatch_slices2_msignal"]) * (np.where(data["abs_avgbatch_msignal"] > -998, data["medianbatch_slices2_msignal"], np.tanh((data["maxbatch_msignal"])) ))) )) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2_msignal"] <= -998, ((data["signal_shift_+1"]) * (((data["meanbatch_msignal"]) * 2.0))), ((data["medianbatch_slices2"]) * (data["meanbatch_msignal"])) )) +
                            0.100000*np.tanh(((((data["stdbatch_msignal"]) * (data["meanbatch_slices2"]))) * (np.where((((data["signal_shift_-1_msignal"]) + (data["signal_shift_-1_msignal"]))/2.0) > -998, data["abs_avgbatch_msignal"], np.tanh((data["abs_avgbatch_msignal"])) )))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) - (np.tanh((data["maxtominbatch"]))))) +
                            0.100000*np.tanh(((((((((6.0)) + (np.where(((data["rangebatch_msignal"]) / 2.0) <= -998, (((6.0)) + ((6.0))), data["minbatch_msignal"] )))/2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["minbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) * (((data["meanbatch_slices2"]) + (((np.where(((data["maxbatch_slices2"]) + (data["minbatch_slices2"])) <= -998, ((data["maxtominbatch"]) + (data["stdbatch_slices2_msignal"])), ((data["maxtominbatch"]) * 2.0) )) / 2.0)))))) +
                            0.100000*np.tanh(((np.where(data["abs_avgbatch_slices2_msignal"] <= -998, (((((5.0)) + (data["minbatch_slices2_msignal"]))) * 2.0), (((5.0)) + (data["minbatch_slices2_msignal"])) )) * 2.0)) +
                            0.100000*np.tanh((-((((((data["rangebatch_msignal"]) - ((((((2.90958952903747559)) - (((data["stdbatch_slices2"]) * 2.0)))) * 2.0)))) * ((-(((((2.90958952903747559)) - (((data["stdbatch_slices2"]) * 2.0)))))))))))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch"] > -998, ((((data["abs_maxbatch"]) * (data["signal"]))) * 2.0), data["rangebatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] <= -998, data["maxtominbatch_msignal"], ((data["minbatch_slices2_msignal"]) - (data["maxtominbatch_slices2"])) )) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(((((((data["minbatch"]) * (np.where(data["rangebatch_slices2_msignal"] <= -998, (0.0), data["maxbatch_slices2_msignal"] )))) * 2.0)) - (((data["abs_maxbatch"]) * (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(((np.where(data["maxtominbatch_msignal"] <= -998, data["maxtominbatch"], np.where(data["maxbatch_slices2"] <= -998, data["abs_maxbatch_slices2"], data["maxtominbatch_msignal"] ) )) + (data["abs_maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) - (((((data["maxbatch_slices2"]) * (data["mean_abs_chgbatch_slices2"]))) + (np.where(data["mean_abs_chgbatch_slices2"] <= -998, data["abs_avgbatch_slices2_msignal"], data["stdbatch_msignal"] )))))) +
                            0.100000*np.tanh(((((((data["medianbatch_slices2_msignal"]) * (data["medianbatch_msignal"]))) * 2.0)) + (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + ((((((((np.where((7.52381992340087891) > -998, (9.26382255554199219), data["signal_shift_+1"] )) / 2.0)) / 2.0)) + (np.where(data["minbatch_msignal"] > -998, (9.26382255554199219), data["minbatch_msignal"] )))/2.0)))) +
                            0.100000*np.tanh((-((data["abs_avgbatch_slices2"])))) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_slices2_msignal"] <= -998, data["medianbatch_msignal"], ((((data["medianbatch_msignal"]) * (data["medianbatch_msignal"]))) * (((data["rangebatch_slices2_msignal"]) - (((data["abs_avgbatch_slices2_msignal"]) * (((data["abs_avgbatch_msignal"]) + (data["abs_avgbatch_slices2"])))))))) )) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) * ((((-((data["minbatch_msignal"])))) * (((((5.0)) + (np.where((5.0) > -998, data["minbatch_msignal"], data["maxtominbatch"] )))/2.0)))))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * ((((6.0)) - (((np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["meanbatch_msignal"], np.where(data["meanbatch_msignal"] <= -998, ((data["abs_maxbatch_msignal"]) * 2.0), data["abs_maxbatch_slices2_msignal"] ) )) * (data["abs_maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(np.where((((data["signal_shift_+1"]) + (((data["signal"]) * 2.0)))/2.0) <= -998, np.tanh((np.tanh((((data["stdbatch_slices2"]) / 2.0))))), ((data["mean_abs_chgbatch_slices2"]) * 2.0) )) +
                            0.100000*np.tanh((((-((data["abs_maxbatch_msignal"])))) / 2.0)) +
                            0.100000*np.tanh(((((((5.69096946716308594)) + (data["minbatch_msignal"]))/2.0)) * (np.where(((((5.69096946716308594)) + ((5.69096946716308594)))/2.0) <= -998, data["abs_maxbatch_slices2"], data["rangebatch_slices2"] )))) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh((-((np.tanh((data["signal_shift_-1_msignal"])))))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) * 2.0)) * (np.where(((np.where(data["medianbatch_msignal"] <= -998, data["medianbatch_msignal"], ((data["medianbatch_msignal"]) * 2.0) )) * 2.0) <= -998, data["medianbatch_msignal"], ((data["medianbatch_slices2_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) + ((-((np.where(np.tanh((((data["maxtominbatch_msignal"]) * (((data["maxtominbatch_msignal"]) * (data["rangebatch_slices2_msignal"])))))) <= -998, np.tanh((data["minbatch_slices2_msignal"])), data["minbatch"] ))))))) +
                            0.100000*np.tanh(((((np.tanh((np.where(data["medianbatch_msignal"] <= -998, data["abs_maxbatch_slices2"], data["medianbatch_msignal"] )))) * (((data["medianbatch_msignal"]) * (((data["abs_maxbatch_slices2"]) * (data["maxbatch_slices2_msignal"]))))))) - (data["maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) - (np.where(((data["maxtominbatch_slices2"]) * (data["abs_maxbatch_slices2_msignal"])) <= -998, data["maxtominbatch"], data["maxtominbatch"] )))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (((data["medianbatch_msignal"]) + (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(((((((data["minbatch_msignal"]) * (data["signal_shift_-1_msignal"]))) + (data["meanbatch_msignal"]))) * (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh((((4.72931480407714844)) - (((((data["abs_avgbatch_msignal"]) * (np.where(data["abs_avgbatch_msignal"] > -998, data["maxbatch_msignal"], ((((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0)) * (data["minbatch_slices2_msignal"])) )))) * (data["abs_avgbatch_msignal"]))))) +
                            0.100000*np.tanh(((((((data["meanbatch_msignal"]) * (((((((data["medianbatch_msignal"]) - (data["meanbatch_msignal"]))) * 2.0)) * 2.0)))) * (((data["signal_shift_-1"]) - (data["meanbatch_msignal"]))))) * 2.0)) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] <= -998, data["medianbatch_slices2_msignal"], (((((14.93104553222656250)) - (((data["meanbatch_slices2_msignal"]) * (((data["meanbatch_slices2_msignal"]) * (data["abs_maxbatch"]))))))) / 2.0) )) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) * ((((((6.0)) * (np.where(data["minbatch_slices2"] <= -998, (((6.0)) + (data["minbatch_msignal"])), (((6.0)) + (data["minbatch_msignal"])) )))) + (data["minbatch_msignal"]))))) +
                            0.100000*np.tanh(np.tanh((data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (np.where(((data["minbatch_msignal"]) + (np.where((5.0) > -998, (6.0), (5.0) ))) > -998, (6.0), (5.0) )))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((np.where(data["minbatch_msignal"] > -998, (12.92473506927490234), (12.92473506927490234) )) / 2.0)))) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * ((((-((((data["mean_abs_chgbatch_msignal"]) * (((data["minbatch"]) - (data["stdbatch_msignal"])))))))) - (((data["maxtominbatch_msignal"]) * (((data["maxtominbatch"]) - (data["minbatch_slices2_msignal"]))))))))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) - (((data["medianbatch_msignal"]) * (np.where(data["abs_avgbatch_msignal"] > -998, ((((data["minbatch_slices2_msignal"]) - (((data["medianbatch_msignal"]) * ((8.0)))))) - (data["abs_maxbatch_slices2"])), data["minbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) * (np.where(data["abs_maxbatch_msignal"] > -998, (((((5.0)) - (data["abs_maxbatch_msignal"]))) * 2.0), data["abs_maxbatch_msignal"] )))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((data["abs_maxbatch_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(((((np.tanh(((-((data["signal"])))))) * (np.tanh((data["maxtominbatch_slices2"]))))) + ((-((((data["maxtominbatch_slices2"]) + (data["rangebatch_slices2_msignal"])))))))) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) * ((((5.0)) - (data["maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) + (((data["signal_shift_-1_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(np.where(((((data["stdbatch_msignal"]) * (data["meanbatch_slices2_msignal"]))) - (data["meanbatch_slices2"])) > -998, (7.0), ((((data["signal_shift_+1_msignal"]) + (data["rangebatch_msignal"]))) + (data["stdbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh((((((data["abs_minbatch_slices2_msignal"]) * 2.0)) + (np.where(data["minbatch_slices2"] <= -998, np.where(data["minbatch_msignal"] <= -998, data["minbatch_slices2_msignal"], data["stdbatch_msignal"] ), data["minbatch_slices2_msignal"] )))/2.0)) +
                            0.100000*np.tanh(((np.where(data["rangebatch_slices2"] <= -998, (2.0), ((data["rangebatch_slices2"]) * (((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])))) )) - ((2.0)))) +
                            0.100000*np.tanh(np.where(((data["minbatch_msignal"]) + ((6.0))) > -998, ((data["minbatch_msignal"]) + ((6.0))), (6.0) )) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2_msignal"] <= -998, data["maxbatch_slices2_msignal"], ((((data["minbatch_msignal"]) + (data["maxbatch_msignal"]))) * ((-((data["abs_maxbatch_msignal"]))))) )) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (np.where((5.82459688186645508) > -998, (5.82459688186645508), data["minbatch"] )))) +
                            0.100000*np.tanh(data["minbatch"]) +
                            0.100000*np.tanh(data["stdbatch_msignal"]) +
                            0.100000*np.tanh(((((7.0)) + (np.where(np.tanh((np.where(data["medianbatch_slices2_msignal"] > -998, (8.0), data["minbatch_msignal"] ))) > -998, data["minbatch_msignal"], np.where(data["minbatch_msignal"] > -998, (8.0), (8.0) ) )))/2.0)) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_msignal"] <= -998, np.where(data["minbatch_msignal"] <= -998, data["minbatch"], ((((data["meanbatch_slices2_msignal"]) / 2.0)) - (data["meanbatch_slices2_msignal"])) ), ((data["minbatch"]) - (data["meanbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((np.where(((data["medianbatch_slices2_msignal"]) * 2.0) > -998, data["medianbatch_msignal"], ((data["abs_avgbatch_msignal"]) * 2.0) )) * (((data["medianbatch_msignal"]) * 2.0)))) +
                            0.100000*np.tanh((((-((((data["maxbatch_msignal"]) - ((5.0))))))) * 2.0)) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((data["medianbatch_msignal"]) * (((data["medianbatch_msignal"]) * (np.where(data["maxbatch_msignal"] <= -998, data["minbatch_slices2_msignal"], np.where((13.99128150939941406) <= -998, data["medianbatch_msignal"], (13.99128150939941406) ) )))))))) +
                            0.100000*np.tanh(((data["stdbatch_slices2_msignal"]) / 2.0)) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) * (((np.tanh((((np.tanh(((-(((((data["minbatch_msignal"]) + (data["maxbatch_slices2_msignal"]))/2.0))))))) * (data["maxbatch_slices2_msignal"]))))) * (((data["meanbatch_slices2_msignal"]) * (data["maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) * 2.0)) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) - (((data["rangebatch_slices2"]) + ((-(((8.0))))))))) * 2.0)) +
                            0.100000*np.tanh(np.where(((data["signal_shift_+1_msignal"]) + (((data["signal_shift_+1_msignal"]) / 2.0))) > -998, data["signal_shift_+1_msignal"], (((data["signal_shift_+1_msignal"]) + (((data["signal_shift_+1_msignal"]) / 2.0)))/2.0) )) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] > -998, (((data["mean_abs_chgbatch_slices2_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0), data["maxtominbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((((data["minbatch_msignal"]) + (((data["abs_maxbatch_msignal"]) * 2.0)))/2.0)) * (np.where((((((data["abs_maxbatch_msignal"]) * 2.0)) + (data["abs_maxbatch_msignal"]))/2.0) <= -998, data["abs_maxbatch_msignal"], data["maxbatch_slices2"] )))) +
                            0.100000*np.tanh(((((((((((((data["maxbatch_slices2_msignal"]) + (data["minbatch_msignal"]))) * 2.0)) * 2.0)) * 2.0)) * (data["abs_minbatch_slices2_msignal"]))) - ((((-((np.tanh((data["medianbatch_msignal"])))))) * 2.0)))) +
                            0.100000*np.tanh((-(((((13.59140300750732422)) + (((((np.where((((13.59140300750732422)) * (((data["minbatch_msignal"]) * ((13.59140300750732422))))) > -998, data["minbatch_msignal"], (4.0) )) * 2.0)) * 2.0))))))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) * (((((((data["meanbatch_msignal"]) * 2.0)) * ((-((((np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], data["abs_avgbatch_msignal"] )) - (data["meanbatch_msignal"])))))))) * 2.0)))) +
                            0.100000*np.tanh(np.tanh((np.tanh((data["minbatch"]))))) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] <= -998, data["meanbatch_msignal"], ((((((((data["medianbatch_msignal"]) * 2.0)) * 2.0)) * 2.0)) * (((((data["medianbatch_msignal"]) * 2.0)) - (((data["meanbatch_msignal"]) * 2.0))))) )) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(np.where(np.tanh((((((np.tanh(((-((data["signal_shift_+1"])))))) / 2.0)) / 2.0))) <= -998, data["medianbatch_slices2_msignal"], np.tanh((data["mean_abs_chgbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (((data["meanbatch_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(np.where((-((data["minbatch_msignal"]))) <= -998, data["minbatch_msignal"], (-((((data["minbatch_msignal"]) + (data["abs_maxbatch_slices2_msignal"]))))) )) +
                            0.100000*np.tanh((((5.87264776229858398)) + (np.where((5.87264776229858398) > -998, data["minbatch_msignal"], ((data["minbatch_msignal"]) + (data["maxtominbatch_msignal"])) )))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where(data["minbatch_msignal"] > -998, ((data["abs_avgbatch_msignal"]) / 2.0), data["minbatch_msignal"] )))) +
                            0.100000*np.tanh((((np.tanh((data["abs_maxbatch_msignal"]))) + (data["medianbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(np.where((((11.87125968933105469)) * 2.0) > -998, (((11.87125968933105469)) + (((data["minbatch_msignal"]) * 2.0))), ((((data["meanbatch_slices2"]) * ((11.87125968933105469)))) + (((((data["maxbatch_slices2_msignal"]) * 2.0)) * 2.0))) )) +
                            0.100000*np.tanh(np.tanh((((data["signal_shift_+1_msignal"]) / 2.0)))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * (((data["medianbatch_msignal"]) * 2.0)))) - ((((10.48543071746826172)) - (((data["meanbatch_slices2_msignal"]) * ((((((10.48543071746826172)) - (data["meanbatch_slices2_msignal"]))) * (data["medianbatch_msignal"]))))))))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) * (((((((np.tanh((((data["abs_maxbatch_slices2_msignal"]) - ((3.0)))))) * 2.0)) - (((data["abs_maxbatch_slices2_msignal"]) - ((3.0)))))) * 2.0)))) +
                            0.100000*np.tanh((-((((data["signal_shift_-1"]) * (((data["maxbatch_msignal"]) + (np.where((((data["maxbatch_msignal"]) + (np.where(data["minbatch"] > -998, data["minbatch_msignal"], data["maxbatch_msignal"] )))/2.0) > -998, data["minbatch_msignal"], data["minbatch_msignal"] ))))))))) +
                            0.100000*np.tanh(data["abs_avgbatch_msignal"]) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) / 2.0)) - (((data["rangebatch_slices2"]) - ((((((8.21354103088378906)) + (data["minbatch_msignal"]))) * ((((((((8.21354103088378906)) + (data["minbatch_msignal"]))) / 2.0)) * 2.0)))))))) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh(((((np.tanh((data["meanbatch_slices2"]))) + (np.where(data["maxbatch_msignal"] > -998, ((((2.50657868385314941)) + (((data["mean_abs_chgbatch_slices2"]) * (data["minbatch_msignal"]))))/2.0), data["stdbatch_slices2"] )))) * 2.0)) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) * (((np.tanh((data["abs_minbatch_slices2_msignal"]))) * (data["abs_avgbatch_slices2_msignal"]))))) + (data["stdbatch_slices2"]))) +
                            0.100000*np.tanh(np.where((((((data["meanbatch_slices2_msignal"]) / 2.0)) + (data["signal_shift_-1_msignal"]))/2.0) > -998, data["mean_abs_chgbatch_slices2"], np.where(np.tanh((data["mean_abs_chgbatch_slices2"])) > -998, data["mean_abs_chgbatch_slices2"], data["abs_maxbatch_msignal"] ) )) +
                            0.100000*np.tanh(np.tanh((((data["maxtominbatch_slices2_msignal"]) + (np.where(np.tanh((data["signal_shift_-1_msignal"])) > -998, data["abs_maxbatch_msignal"], data["maxtominbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) - (data["meanbatch_msignal"]))) * (((((((data["meanbatch_msignal"]) * 2.0)) * 2.0)) * (np.where(((data["medianbatch_msignal"]) - (data["meanbatch_msignal"])) <= -998, data["medianbatch_msignal"], data["abs_maxbatch_slices2"] )))))) +
                            0.100000*np.tanh((((((np.tanh((data["mean_abs_chgbatch_slices2"]))) + ((((data["medianbatch_msignal"]) + (np.where(data["mean_abs_chgbatch_slices2"] <= -998, np.tanh((data["maxbatch_msignal"])), data["signal_shift_-1"] )))/2.0)))/2.0)) / 2.0)) +
                            0.100000*np.tanh(np.tanh((((((data["signal_shift_+1_msignal"]) / 2.0)) / 2.0)))) +
                            0.100000*np.tanh((((np.tanh((data["mean_abs_chgbatch_slices2"]))) + (np.tanh((data["abs_minbatch_slices2"]))))/2.0)) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh((((np.where(data["maxtominbatch_msignal"] <= -998, data["mean_abs_chgbatch_slices2"], ((np.tanh((data["maxtominbatch_msignal"]))) + (data["minbatch"])) )) + ((((-((data["meanbatch_msignal"])))) / 2.0)))/2.0)) +
                            0.100000*np.tanh(np.where((6.0) > -998, ((((((data["minbatch_msignal"]) + ((6.0)))) * 2.0)) * 2.0), ((((data["abs_minbatch_msignal"]) + (data["stdbatch_msignal"]))) * 2.0) )) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2"] > -998, data["rangebatch_slices2_msignal"], (7.0) )) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) / 2.0)) +
                            0.100000*np.tanh(np.where((((((data["abs_avgbatch_slices2_msignal"]) + ((6.08511495590209961)))/2.0)) + (data["minbatch_msignal"])) > -998, (((6.08511495590209961)) + (np.where(data["minbatch_msignal"] > -998, data["minbatch_msignal"], (3.94063448905944824) ))), (6.08511495590209961) )) +
                            0.100000*np.tanh(((np.where(((((data["signal_shift_-1"]) + ((((5.0)) / 2.0)))) / 2.0) <= -998, ((data["abs_maxbatch_slices2_msignal"]) / 2.0), ((((data["abs_maxbatch_slices2_msignal"]) - ((((5.0)) / 2.0)))) * 2.0) )) * 2.0)) +
                            0.100000*np.tanh((((((6.0)) + (np.where(np.where(data["minbatch_msignal"] > -998, np.where(data["medianbatch_slices2"] <= -998, (6.0), (6.0) ), data["minbatch_msignal"] ) > -998, data["minbatch_msignal"], data["maxbatch_slices2_msignal"] )))) * 2.0)) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] > -998, (((6.73241043090820312)) + (data["minbatch_msignal"])), (((6.73241043090820312)) * ((6.73241043090820312))) )) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * (((data["minbatch_slices2_msignal"]) + (((np.where(data["abs_avgbatch_msignal"] <= -998, data["minbatch_slices2_msignal"], ((((data["minbatch_slices2_msignal"]) + (data["abs_avgbatch_msignal"]))) * (data["abs_avgbatch_msignal"])) )) / 2.0)))))) +
                            0.100000*np.tanh(((((((((data["abs_maxbatch_msignal"]) - (np.where(data["abs_maxbatch_msignal"] > -998, (3.0), np.where(data["abs_maxbatch_msignal"] > -998, data["maxbatch_slices2"], (5.04840517044067383) ) )))) * 2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) + (data["minbatch_slices2"]))) * (np.where(((((((data["meanbatch_slices2_msignal"]) + (data["minbatch_slices2"]))) * (data["meanbatch_slices2_msignal"]))) * 2.0) > -998, data["abs_minbatch_msignal"], data["meanbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(data["abs_maxbatch_slices2"]) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) * (np.where(((data["minbatch_slices2_msignal"]) * 2.0) <= -998, ((data["minbatch_slices2_msignal"]) * 2.0), np.tanh((((data["minbatch_msignal"]) + (data["abs_avgbatch_msignal"])))) )))) * (data["abs_avgbatch_msignal"]))) +
                            0.100000*np.tanh(((((np.where(data["minbatch_msignal"] > -998, data["minbatch_msignal"], data["abs_maxbatch_slices2"] )) + ((4.49531555175781250)))) + (np.tanh(((4.49531555175781250)))))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) * (np.where(data["mean_abs_chgbatch_slices2"] > -998, data["meanbatch_msignal"], data["medianbatch_slices2_msignal"] )))) * (data["abs_maxbatch"]))) +
                            0.100000*np.tanh(((np.tanh((((((data["maxtominbatch_msignal"]) / 2.0)) * 2.0)))) / 2.0)) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (np.where(np.where(((data["signal_shift_+1_msignal"]) * 2.0) > -998, data["medianbatch_msignal"], np.tanh((data["medianbatch_slices2_msignal"])) ) > -998, ((data["medianbatch_slices2_msignal"]) * 2.0), data["rangebatch_msignal"] )))) +
                            0.100000*np.tanh(np.tanh(((((data["meanbatch_slices2_msignal"]) + (np.where(((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0) > -998, data["maxtominbatch_slices2"], ((data["medianbatch_slices2_msignal"]) / 2.0) )))/2.0)))) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) + (np.where(((data["maxbatch_slices2"]) / 2.0) > -998, np.where(((data["mean_abs_chgbatch_slices2"]) * (data["stdbatch_slices2"])) > -998, ((data["stdbatch_msignal"]) * (data["stdbatch_slices2"])), data["abs_maxbatch"] ), data["abs_avgbatch_slices2"] )))) +
                            0.100000*np.tanh(np.where(((data["minbatch_msignal"]) + (((data["abs_maxbatch_slices2_msignal"]) * 2.0))) <= -998, data["abs_maxbatch_slices2_msignal"], ((data["minbatch_msignal"]) + (((data["abs_maxbatch_slices2_msignal"]) * 2.0))) )) +
                            0.100000*np.tanh(((np.where(np.tanh((((data["signal_shift_-1"]) * (((data["abs_maxbatch_slices2_msignal"]) * (data["meanbatch_slices2_msignal"])))))) <= -998, np.tanh((data["mean_abs_chgbatch_slices2"])), data["rangebatch_slices2"] )) / 2.0)) +
                            0.100000*np.tanh(((((np.where(data["mean_abs_chgbatch_slices2"] > -998, ((data["abs_avgbatch_msignal"]) * ((((((((data["medianbatch_slices2_msignal"]) + (data["stdbatch_slices2"]))/2.0)) + (data["minbatch_slices2_msignal"]))) / 2.0))), data["signal_shift_+1_msignal"] )) * (data["medianbatch_slices2_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(np.where(np.where(data["maxtominbatch"] <= -998, np.tanh((((data["abs_maxbatch"]) * (np.tanh((data["meanbatch_slices2"])))))), data["meanbatch_slices2"] ) <= -998, data["meanbatch_slices2"], data["medianbatch_slices2"] )) +
                            0.100000*np.tanh(((((np.where((6.0) <= -998, ((data["minbatch_msignal"]) * 2.0), np.where(data["minbatch_msignal"] <= -998, (((6.0)) + (data["minbatch_msignal"])), (((6.0)) + (data["minbatch_msignal"])) ) )) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((3.0)) + ((-(((((((3.0)) - (data["abs_maxbatch_slices2_msignal"]))) * ((((((((3.0)) - (data["abs_maxbatch_slices2_msignal"]))) * (data["maxbatch_slices2"]))) + (data["maxbatch_slices2"])))))))))/2.0)) +
                            0.100000*np.tanh((-((np.where(((data["medianbatch_msignal"]) * 2.0) <= -998, ((data["medianbatch_slices2"]) * (data["medianbatch_msignal"])), (((0.73649901151657104)) - (((((data["medianbatch_slices2_msignal"]) * 2.0)) * (data["medianbatch_msignal"])))) ))))) +
                            0.100000*np.tanh(np.where(np.where(data["medianbatch_msignal"] <= -998, data["abs_minbatch_slices2_msignal"], data["minbatch_msignal"] ) <= -998, data["maxtominbatch"], (((data["minbatch_msignal"]) + (data["medianbatch_msignal"]))/2.0) )) +
                            0.100000*np.tanh(np.where((((data["maxbatch_slices2"]) + (data["medianbatch_slices2"]))/2.0) <= -998, np.where(data["rangebatch_slices2"] > -998, ((data["meanbatch_slices2"]) + ((13.41741371154785156))), data["meanbatch_slices2"] ), data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(np.where((((6.0)) + (data["minbatch_msignal"])) <= -998, (((6.0)) + (data["minbatch_msignal"])), (((((6.0)) + (data["minbatch_msignal"]))) * 2.0) )) +
                            0.100000*np.tanh(np.where(np.tanh(((11.42908477783203125))) > -998, ((data["minbatch_msignal"]) + ((((11.42908477783203125)) + (data["minbatch_msignal"])))), np.tanh((((data["minbatch_msignal"]) + ((((11.42908477783203125)) + (data["minbatch_msignal"])))))) )) +
                            0.100000*np.tanh((((8.0)) - (((data["maxbatch_slices2_msignal"]) * ((((8.0)) - (np.where((8.0) <= -998, data["signal_shift_-1"], data["maxbatch_slices2_msignal"] )))))))) +
                            0.100000*np.tanh(data["rangebatch_slices2"]) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (np.where(data["minbatch_msignal"] > -998, data["abs_avgbatch_slices2_msignal"], data["stdbatch_msignal"] )))) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] <= -998, data["medianbatch_slices2"], ((data["medianbatch_slices2"]) + (data["mean_abs_chgbatch_slices2"])) )) +
                            0.100000*np.tanh(np.where(((data["maxtominbatch"]) / 2.0) > -998, (-((((data["abs_avgbatch_slices2_msignal"]) * (data["maxtominbatch"]))))), ((data["abs_avgbatch_msignal"]) * (((data["maxtominbatch"]) * (data["abs_maxbatch"])))) )) +
                            0.100000*np.tanh(data["medianbatch_slices2"]) +
                            0.100000*np.tanh(((np.tanh((np.tanh((data["maxtominbatch"]))))) + ((((((data["minbatch_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0)) * ((((data["abs_maxbatch_slices2_msignal"]) + (((data["abs_avgbatch_slices2_msignal"]) - ((7.70726490020751953)))))/2.0)))))) +
                            0.100000*np.tanh((((((data["abs_maxbatch_slices2_msignal"]) * (((((((data["abs_maxbatch_slices2_msignal"]) - ((((6.0)) - (data["abs_maxbatch_slices2_msignal"]))))) * 2.0)) * 2.0)))) + (((data["abs_avgbatch_slices2_msignal"]) - (data["minbatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh(((np.where((((data["minbatch_msignal"]) + (data["minbatch_msignal"]))/2.0) <= -998, (((data["medianbatch_msignal"]) + (((data["signal_shift_-1_msignal"]) / 2.0)))/2.0), data["minbatch_msignal"] )) + (((((data["minbatch_msignal"]) + (data["medianbatch_msignal"]))) * 2.0)))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) + ((((((((data["minbatch"]) / 2.0)) / 2.0)) + (data["abs_maxbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1_msignal"] <= -998, data["abs_maxbatch_slices2"], ((data["rangebatch_msignal"]) * (((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])))) )) +
                            0.100000*np.tanh(((((((data["minbatch_slices2_msignal"]) + ((((3.0)) * 2.0)))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh(((np.tanh((data["abs_minbatch_slices2"]))) + (data["signal_shift_+1_msignal"]))) +
                            0.100000*np.tanh(np.where(np.tanh((np.tanh((data["abs_maxbatch_slices2_msignal"])))) > -998, data["mean_abs_chgbatch_slices2"], np.where(data["abs_maxbatch_slices2_msignal"] > -998, data["mean_abs_chgbatch_slices2"], data["mean_abs_chgbatch_slices2"] ) )) +
                            0.100000*np.tanh(np.where((-((data["medianbatch_slices2"]))) > -998, ((((11.16993713378906250)) + (((data["meanbatch_msignal"]) * ((-((data["rangebatch_slices2"])))))))/2.0), (-((((data["rangebatch_slices2"]) + (data["mean_abs_chgbatch_slices2"]))))) )) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) * (np.where(data["medianbatch_msignal"] > -998, data["meanbatch_slices2_msignal"], data["maxtominbatch_slices2"] )))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2"]) * 2.0)) +
                            0.100000*np.tanh(((data["signal"]) * (((data["minbatch_slices2"]) * (((data["abs_maxbatch_slices2"]) + (((data["maxtominbatch_slices2"]) + (np.where(data["signal"] <= -998, data["maxtominbatch_slices2"], data["minbatch_slices2"] )))))))))) +
                            0.100000*np.tanh(((((data["stdbatch_slices2_msignal"]) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(((((data["stdbatch_msignal"]) + (np.where(data["abs_maxbatch_slices2"] > -998, data["medianbatch_slices2"], np.where(((data["mean_abs_chgbatch_slices2"]) / 2.0) > -998, data["abs_avgbatch_slices2"], data["abs_avgbatch_slices2"] ) )))) + (data["abs_avgbatch_slices2"]))) +
                            0.100000*np.tanh((((data["minbatch_msignal"]) + (np.where((((data["signal_shift_-1"]) + ((((0.0)) / 2.0)))/2.0) > -998, (7.0), (((data["abs_avgbatch_slices2_msignal"]) + (((data["meanbatch_msignal"]) - (((data["maxbatch_msignal"]) / 2.0)))))/2.0) )))/2.0)) +
                            0.100000*np.tanh(data["stdbatch_slices2"]) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], ((data["medianbatch_msignal"]) / 2.0) )) +
                            0.100000*np.tanh(np.where(np.tanh((((data["maxtominbatch_slices2_msignal"]) * 2.0))) <= -998, ((data["minbatch_msignal"]) * 2.0), (((10.74705314636230469)) + (np.where(data["abs_minbatch_slices2"] > -998, ((data["minbatch_msignal"]) * 2.0), ((data["mean_abs_chgbatch_slices2"]) * 2.0) ))) )) +
                            0.100000*np.tanh(((((data["signal_shift_+1_msignal"]) / 2.0)) * (((data["medianbatch_slices2_msignal"]) * (((data["minbatch_msignal"]) + (data["abs_avgbatch_msignal"]))))))) +
                            0.100000*np.tanh((((((data["abs_maxbatch"]) + (data["abs_maxbatch"]))/2.0)) * (((((data["abs_avgbatch_slices2"]) * (data["abs_maxbatch_msignal"]))) - (((data["meanbatch_slices2"]) + (data["abs_maxbatch"]))))))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) * (((data["maxbatch_slices2_msignal"]) - (((((10.0)) + (np.tanh((data["abs_minbatch_slices2_msignal"]))))/2.0)))))) +
                            0.100000*np.tanh((((data["mean_abs_chgbatch_slices2"]) + (((np.where(data["mean_abs_chgbatch_slices2"] > -998, data["meanbatch_slices2"], data["stdbatch_slices2"] )) / 2.0)))/2.0)) +
                            0.100000*np.tanh(((((data["minbatch_slices2_msignal"]) * 2.0)) + (np.where(data["minbatch_slices2_msignal"] <= -998, data["meanbatch_msignal"], data["meanbatch_msignal"] )))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) * (np.where(data["abs_avgbatch_slices2"] > -998, ((data["minbatch_msignal"]) + (data["stdbatch_msignal"])), (((11.52958583831787109)) - (((data["rangebatch_slices2_msignal"]) / 2.0))) )))) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) + ((((np.where(((data["maxbatch_slices2"]) * 2.0) > -998, data["meanbatch_slices2"], data["medianbatch_slices2"] )) + (((data["medianbatch_slices2"]) * (((data["minbatch_msignal"]) - (((data["mean_abs_chgbatch_msignal"]) / 2.0)))))))/2.0)))) +
                            0.100000*np.tanh(np.where((0.45348298549652100) > -998, np.where(data["maxbatch_slices2"] > -998, data["abs_avgbatch_slices2"], data["rangebatch_slices2"] ), ((data["abs_maxbatch_slices2"]) + (data["medianbatch_slices2"])) )) +
                            0.100000*np.tanh((((data["signal_shift_+1_msignal"]) + ((((data["maxtominbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"]))/2.0)))/2.0)) +
                            0.100000*np.tanh((((7.0)) + (data["minbatch_msignal"]))))    
      
    def GP_class_4(self,data):
        return self.Output( -2.514146 +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(np.where(((data["meanbatch_slices2"]) / 2.0) > -998, np.where(np.where(data["stdbatch_msignal"] <= -998, data["minbatch"], data["meanbatch_slices2"] ) > -998, data["medianbatch_slices2"], data["medianbatch_slices2"] ), data["medianbatch_slices2"] )) +
                            0.100000*np.tanh(((((np.where(data["medianbatch_slices2"] > -998, data["medianbatch_slices2"], data["signal_shift_-1"] )) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((np.where(data["maxtominbatch_slices2"] > -998, data["meanbatch_slices2"], (((((data["abs_maxbatch_slices2_msignal"]) + (data["medianbatch_slices2_msignal"]))/2.0)) * 2.0) )) - (((data["abs_avgbatch_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(np.where(data["signal"] > -998, data["signal"], data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1_msignal"] > -998, np.where(data["signal_shift_+1_msignal"] > -998, data["signal"], data["signal_shift_-1"] ), ((data["mean_abs_chgbatch_msignal"]) - ((-((data["signal"]))))) )) +
                            0.100000*np.tanh(np.where((((((data["signal_shift_+1"]) + (((data["signal"]) / 2.0)))/2.0)) - ((5.0))) <= -998, np.where((-((data["signal"]))) <= -998, data["abs_avgbatch_msignal"], data["maxtominbatch"] ), (-((data["abs_avgbatch_msignal"]))) )) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2"] > -998, ((data["meanbatch_slices2"]) * ((6.40869665145874023))), (-(((6.40869665145874023)))) )) +
                            0.100000*np.tanh(np.tanh((((data["maxbatch_slices2"]) + (((data["maxtominbatch"]) + (data["minbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(np.where(np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], data["minbatch_slices2_msignal"] ) <= -998, data["medianbatch_slices2"], (((((-((data["minbatch_slices2"])))) * 2.0)) * (data["medianbatch_slices2"])) )) +
                            0.100000*np.tanh((((((data["maxtominbatch_slices2_msignal"]) + (data["minbatch"]))/2.0)) - (np.tanh((np.where((((-((data["minbatch"])))) + (data["signal_shift_-1_msignal"])) > -998, (-(((-((data["abs_avgbatch_slices2_msignal"])))))), data["abs_avgbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((np.where((((data["signal"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0) <= -998, ((data["stdbatch_slices2_msignal"]) * 2.0), ((data["stdbatch_msignal"]) * (((data["abs_maxbatch_slices2_msignal"]) - ((3.04336380958557129))))) )) * 2.0)) +
                            0.100000*np.tanh((-((data["meanbatch_msignal"])))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2"] <= -998, data["signal_shift_-1"], ((((data["minbatch_slices2_msignal"]) * (data["signal_shift_+1_msignal"]))) + (((data["minbatch_slices2_msignal"]) * (data["meanbatch_slices2_msignal"])))) )) +
                            0.100000*np.tanh((((((((6.96916007995605469)) + (data["signal"]))) - ((((((data["abs_maxbatch"]) * (data["abs_maxbatch_slices2_msignal"]))) + (((data["abs_maxbatch"]) * (data["abs_maxbatch_slices2_msignal"]))))/2.0)))) + (data["abs_maxbatch_slices2"]))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * (((data["medianbatch_slices2_msignal"]) * (((data["mean_abs_chgbatch_msignal"]) - (np.tanh(((((data["mean_abs_chgbatch_msignal"]) + (data["abs_avgbatch_msignal"]))/2.0)))))))))) - (data["abs_avgbatch_msignal"]))) +
                            0.100000*np.tanh(((np.tanh((((data["meanbatch_msignal"]) * (data["medianbatch_slices2"]))))) * (data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, ((((data["rangebatch_slices2"]) / 2.0)) + (data["medianbatch_slices2_msignal"])), ((data["medianbatch_slices2_msignal"]) / 2.0) )) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] <= -998, np.where(np.tanh((((np.where((2.86545825004577637) <= -998, data["rangebatch_msignal"], data["minbatch_slices2_msignal"] )) * 2.0))) > -998, data["stdbatch_slices2"], data["abs_avgbatch_msignal"] ), np.tanh((data["minbatch_msignal"])) )) +
                            0.100000*np.tanh(np.where((((-(((((data["stdbatch_msignal"]) + (((((data["abs_minbatch_slices2_msignal"]) - (data["minbatch_msignal"]))) - ((11.35848236083984375)))))/2.0))))) + (data["abs_maxbatch_slices2_msignal"])) > -998, data["minbatch_msignal"], data["minbatch"] )) +
                            0.100000*np.tanh(((((((np.where(data["mean_abs_chgbatch_slices2"] > -998, data["medianbatch_msignal"], ((((data["mean_abs_chgbatch_slices2"]) + (data["meanbatch_msignal"]))) * 2.0) )) + (np.tanh((np.tanh((data["medianbatch_slices2"]))))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((np.where(np.tanh((data["stdbatch_slices2"])) <= -998, np.tanh((data["medianbatch_slices2"])), ((data["signal_shift_-1"]) * (data["mean_abs_chgbatch_msignal"])) )) - (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2"]) * (((((((data["abs_maxbatch_slices2"]) - (data["abs_avgbatch_slices2_msignal"]))) - (np.where(np.where(data["abs_avgbatch_slices2_msignal"] <= -998, data["maxtominbatch_slices2"], data["maxtominbatch_slices2"] ) <= -998, (5.0), (5.0) )))) * 2.0)))) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) * (((data["meanbatch_slices2"]) * (((((((((data["medianbatch_msignal"]) * 2.0)) + (data["abs_maxbatch_slices2_msignal"]))) * ((-((data["meanbatch_msignal"])))))) * (data["abs_maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) + (np.where(data["stdbatch_slices2_msignal"] > -998, (5.0), (5.0) )))) +
                            0.100000*np.tanh(((((data["signal_shift_-1"]) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((np.tanh((np.where((((((data["abs_minbatch_msignal"]) / 2.0)) + (((data["signal_shift_+1_msignal"]) / 2.0)))/2.0) <= -998, (-((data["abs_maxbatch_slices2"]))), (((data["medianbatch_msignal"]) + (data["stdbatch_slices2"]))/2.0) )))) * 2.0)) +
                            0.100000*np.tanh(np.where(data["stdbatch_slices2"] > -998, np.tanh((data["minbatch_slices2_msignal"])), data["minbatch_msignal"] )) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * 2.0)) / 2.0)) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) * (np.where(data["stdbatch_slices2"] <= -998, data["medianbatch_slices2"], (-((data["meanbatch_msignal"]))) )))) * 2.0)) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] <= -998, (11.30583953857421875), np.where(data["abs_maxbatch"] <= -998, np.tanh((data["medianbatch_msignal"])), ((data["meanbatch_slices2_msignal"]) * (((data["minbatch_slices2_msignal"]) * (((data["medianbatch_msignal"]) + ((1.0))))))) ) )) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2_msignal"] > -998, data["medianbatch_msignal"], data["rangebatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((4.04078483581542969)) - (np.where((4.04078483581542969) > -998, data["abs_maxbatch_msignal"], data["medianbatch_msignal"] )))) +
                            0.100000*np.tanh(np.where(((data["medianbatch_msignal"]) / 2.0) <= -998, data["minbatch_msignal"], data["minbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(((data["signal"]) + (np.where(np.tanh(((-((((data["medianbatch_msignal"]) * 2.0)))))) <= -998, ((data["medianbatch_msignal"]) * (data["signal_shift_-1"])), ((data["medianbatch_msignal"]) * (data["signal_shift_+1"])) )))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) + (np.tanh((((data["medianbatch_msignal"]) * (data["meanbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(np.where((-((data["abs_maxbatch_msignal"]))) <= -998, (((3.0)) * (((data["abs_maxbatch_slices2_msignal"]) * (data["abs_maxbatch_msignal"])))), (((((3.0)) - (data["abs_maxbatch_slices2_msignal"]))) * (data["rangebatch_msignal"])) )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (np.tanh((((data["medianbatch_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) + (((np.tanh((((data["mean_abs_chgbatch_slices2_msignal"]) * (data["meanbatch_msignal"]))))) * 2.0)))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) + ((((((data["minbatch"]) + (data["stdbatch_msignal"]))/2.0)) + (((((data["stdbatch_msignal"]) - (data["minbatch"]))) * 2.0)))))) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (((data["abs_minbatch_slices2_msignal"]) + ((((((((data["meanbatch_slices2_msignal"]) * (((data["meanbatch_slices2_msignal"]) + (data["abs_minbatch_slices2_msignal"]))))) * 2.0)) + (data["abs_minbatch_slices2_msignal"]))/2.0)))))) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) * (np.where(np.where(data["maxtominbatch_slices2"] > -998, data["abs_minbatch_msignal"], data["signal_shift_+1_msignal"] ) <= -998, data["meanbatch_slices2_msignal"], data["meanbatch_msignal"] )))) +
                            0.100000*np.tanh(data["rangebatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where(np.where(data["signal_shift_-1_msignal"] > -998, (((-(((8.0))))) + (data["maxbatch_msignal"])), data["signal"] ) > -998, (((-(((8.0))))) + (data["maxbatch_msignal"])), data["signal"] )) +
                            0.100000*np.tanh((((((((3.17613315582275391)) + ((3.17613315582275391)))) + (data["minbatch_slices2_msignal"]))) * 2.0)) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] > -998, (((((((data["medianbatch_msignal"]) / 2.0)) + (data["minbatch"]))/2.0)) + (((data["minbatch"]) + (((data["medianbatch_msignal"]) * 2.0))))), data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) * (((data["abs_maxbatch_msignal"]) - (np.where(data["abs_maxbatch_msignal"] > -998, (4.0), ((((data["abs_maxbatch_msignal"]) - (np.where(data["maxbatch_msignal"] > -998, (4.0), (4.0) )))) / 2.0) )))))) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2_msignal"] > -998, data["medianbatch_msignal"], np.where((((data["medianbatch_msignal"]) + (data["mean_abs_chgbatch_slices2"]))/2.0) > -998, ((((data["medianbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))) * 2.0), ((data["minbatch_slices2_msignal"]) - (data["signal_shift_-1_msignal"])) ) )) +
                            0.100000*np.tanh((((data["stdbatch_msignal"]) + (np.where(data["abs_avgbatch_slices2"] > -998, ((data["signal_shift_-1"]) / 2.0), data["abs_minbatch_msignal"] )))/2.0)) +
                            0.100000*np.tanh(np.where(data["rangebatch_msignal"] <= -998, ((data["meanbatch_msignal"]) / 2.0), data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] <= -998, data["stdbatch_slices2"], (((data["medianbatch_msignal"]) + (((data["minbatch"]) + (np.where(((data["minbatch"]) * 2.0) > -998, data["medianbatch_msignal"], data["medianbatch_msignal"] )))))/2.0) )) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) + ((((((7.0)) - ((-((((data["medianbatch_msignal"]) * ((9.22422599792480469))))))))) * ((-((data["meanbatch_msignal"])))))))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2"]) - (np.where(data["rangebatch_slices2"] > -998, (6.0), ((((((data["medianbatch_msignal"]) + (data["medianbatch_msignal"]))/2.0)) + (data["rangebatch_slices2"]))/2.0) )))) * 2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) + (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((((9.42602443695068359)) - ((-((np.where(data["minbatch"] <= -998, (9.42602443695068359), ((data["minbatch_msignal"]) - (np.where((9.42602443695068359) > -998, data["maxbatch_msignal"], data["medianbatch_slices2"] ))) ))))))) * 2.0)) +
                            0.100000*np.tanh(((np.where(data["meanbatch_msignal"] <= -998, data["minbatch_slices2_msignal"], data["meanbatch_slices2_msignal"] )) + (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) * (((((((((data["abs_avgbatch_slices2"]) * (((data["medianbatch_slices2_msignal"]) / 2.0)))) + (data["maxbatch_slices2_msignal"]))) * (data["meanbatch_slices2"]))) * (data["stdbatch_slices2"]))))) +
                            0.100000*np.tanh((-(((((11.40939426422119141)) - (((data["rangebatch_slices2"]) * 2.0))))))) +
                            0.100000*np.tanh(((np.where(data["meanbatch_msignal"] <= -998, data["medianbatch_msignal"], ((data["medianbatch_msignal"]) - (np.tanh((((((data["meanbatch_msignal"]) * 2.0)) * 2.0))))) )) * 2.0)) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2"] <= -998, data["abs_minbatch_msignal"], (((((((((data["stdbatch_slices2_msignal"]) + (data["rangebatch_slices2_msignal"]))/2.0)) * (data["abs_avgbatch_msignal"]))) - (data["maxbatch_msignal"]))) + (np.tanh((data["minbatch_msignal"])))) )) +
                            0.100000*np.tanh(((((data["maxtominbatch"]) + ((((data["medianbatch_slices2_msignal"]) + ((-((data["medianbatch_slices2_msignal"])))))/2.0)))) + (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) * (((np.tanh(((6.0)))) + ((((((6.0)) + (data["minbatch_msignal"]))) * 2.0)))))) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) * (np.where((((data["signal"]) + (data["stdbatch_slices2_msignal"]))/2.0) <= -998, data["maxbatch_msignal"], data["meanbatch_msignal"] )))) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((((((((data["medianbatch_msignal"]) / 2.0)) / 2.0)) * (data["medianbatch_msignal"]))) * (((data["minbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"]))))) / 2.0)) +
                            0.100000*np.tanh((((((((((((3.0)) - (data["abs_maxbatch_slices2_msignal"]))) * ((3.0)))) * (((data["abs_maxbatch_slices2_msignal"]) - ((((3.0)) - (data["abs_maxbatch_slices2_msignal"]))))))) * 2.0)) * (data["abs_maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["medianbatch_slices2"]) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (((data["medianbatch_slices2_msignal"]) / 2.0)))) +
                            0.100000*np.tanh((((((data["medianbatch_msignal"]) * (data["maxbatch_slices2"]))) + (data["abs_maxbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((((((data["rangebatch_slices2_msignal"]) * (data["meanbatch_slices2_msignal"]))) - ((6.0)))) * (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(np.where((((((data["meanbatch_msignal"]) / 2.0)) + (data["medianbatch_msignal"]))/2.0) > -998, data["medianbatch_msignal"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) - (((((data["minbatch_msignal"]) + ((7.0)))) * 2.0)))) * (np.where(data["minbatch_msignal"] <= -998, data["minbatch_msignal"], ((((data["minbatch_msignal"]) + ((7.0)))) * 2.0) )))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) - (data["medianbatch_slices2_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(((((((((((((6.0)) + (data["minbatch_msignal"]))/2.0)) * 2.0)) * ((6.0)))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (((data["minbatch_slices2_msignal"]) + (((data["medianbatch_msignal"]) * (((data["minbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"]))))))))) +
                            0.100000*np.tanh(np.where(np.tanh((((np.tanh((np.tanh((data["medianbatch_msignal"]))))) / 2.0))) <= -998, (((7.0)) / 2.0), ((data["medianbatch_msignal"]) - (((np.tanh((data["meanbatch_msignal"]))) * 2.0))) )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) / 2.0)) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) + (np.tanh((((data["meanbatch_slices2"]) + (data["medianbatch_msignal"]))))))) +
                            0.100000*np.tanh((((((((data["medianbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))/2.0)) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_slices2_msignal"] > -998, ((((data["medianbatch_slices2"]) * 2.0)) / 2.0), np.where(data["maxbatch_slices2"] > -998, data["meanbatch_slices2"], ((((data["meanbatch_msignal"]) * 2.0)) * 2.0) ) )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (np.where((7.0) <= -998, ((data["minbatch_slices2_msignal"]) - (np.where(data["stdbatch_slices2"] <= -998, data["medianbatch_msignal"], (((7.0)) - (data["medianbatch_msignal"])) ))), (-((data["minbatch_slices2_msignal"]))) )))) +
                            0.100000*np.tanh(np.where(data["signal"] <= -998, data["abs_maxbatch_slices2_msignal"], ((data["medianbatch_slices2"]) * (data["abs_maxbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((((((-((((((data["rangebatch_msignal"]) / 2.0)) / 2.0))))) + ((((data["medianbatch_slices2_msignal"]) + (data["meanbatch_msignal"]))/2.0)))/2.0)) - (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh((((6.0)) * (((data["rangebatch_slices2"]) * (((data["rangebatch_slices2"]) - (np.where(data["rangebatch_slices2"] > -998, (6.0), (((data["maxtominbatch_slices2_msignal"]) + (data["abs_maxbatch"]))/2.0) )))))))) +
                            0.100000*np.tanh((((((((((3.66002893447875977)) + ((((3.66002893447875977)) - (data["abs_maxbatch_msignal"]))))) * 2.0)) * ((((3.66002893447875977)) - (data["abs_maxbatch_msignal"]))))) - (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(((data["medianbatch_msignal"]) / 2.0) > -998, ((data["minbatch_slices2_msignal"]) - ((-((data["medianbatch_msignal"]))))), ((((data["signal_shift_+1_msignal"]) * 2.0)) - ((-((data["medianbatch_slices2_msignal"]))))) )) +
                            0.100000*np.tanh(np.where(data["rangebatch_msignal"] <= -998, ((data["medianbatch_slices2_msignal"]) + (((data["signal_shift_-1"]) * 2.0))), data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where(((data["minbatch_slices2_msignal"]) + (data["medianbatch_msignal"])) > -998, np.where(((data["minbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"])) > -998, data["medianbatch_slices2_msignal"], data["stdbatch_msignal"] ), data["medianbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((((data["signal_shift_+1"]) * (data["medianbatch_msignal"]))) + (np.where(data["abs_maxbatch"] <= -998, data["medianbatch_msignal"], data["medianbatch_slices2"] )))) +
                            0.100000*np.tanh((((data["medianbatch_msignal"]) + (np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], ((data["signal_shift_-1_msignal"]) - (data["signal_shift_+1_msignal"])) )))/2.0)) +
                            0.100000*np.tanh((((((3.0)) * ((((3.0)) * ((((3.0)) - (data["medianbatch_slices2_msignal"]))))))) * ((((3.0)) - (data["abs_maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] <= -998, np.where(data["minbatch_msignal"] <= -998, ((((data["medianbatch_slices2_msignal"]) + (data["maxtominbatch_msignal"]))) + ((7.0))), data["mean_abs_chgbatch_slices2"] ), ((data["minbatch_msignal"]) + ((7.0))) )) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) - (np.where(data["medianbatch_slices2_msignal"] <= -998, ((((((data["stdbatch_slices2_msignal"]) * 2.0)) / 2.0)) + ((3.0))), (3.0) )))) +
                            0.100000*np.tanh((((((data["stdbatch_slices2"]) + (data["medianbatch_msignal"]))/2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0) <= -998, data["maxbatch_slices2"], data["medianbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((np.where((((6.62587308883666992)) - ((((-((data["maxbatch_msignal"])))) * 2.0))) > -998, (6.62587308883666992), (6.62587308883666992) )) + ((((-((data["maxbatch_msignal"])))) * 2.0)))/2.0)) +
                            0.100000*np.tanh(data["stdbatch_slices2"]) +
                            0.100000*np.tanh((((data["maxtominbatch_slices2_msignal"]) + (((((13.10721111297607422)) + (((data["stdbatch_slices2"]) / 2.0)))/2.0)))/2.0)) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) + (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) + (((np.tanh((data["medianbatch_msignal"]))) / 2.0)))) +
                            0.100000*np.tanh(np.where(((data["meanbatch_slices2_msignal"]) + ((((data["meanbatch_slices2_msignal"]) + (data["signal"]))/2.0))) > -998, data["signal"], np.where(data["abs_minbatch_slices2_msignal"] <= -998, data["meanbatch_slices2"], ((data["abs_minbatch_slices2_msignal"]) * (data["meanbatch_msignal"])) ) )) +
                            0.100000*np.tanh(np.where(np.where((6.70463323593139648) <= -998, data["abs_maxbatch_slices2_msignal"], data["medianbatch_slices2_msignal"] ) <= -998, data["signal_shift_+1_msignal"], ((np.where((6.70463323593139648) <= -998, data["signal_shift_+1_msignal"], data["abs_maxbatch_slices2_msignal"] )) - ((6.70463323593139648))) )) +
                            0.100000*np.tanh((((data["stdbatch_slices2"]) + (np.where((1.0) > -998, (((11.21940040588378906)) + (((((data["rangebatch_slices2"]) / 2.0)) * 2.0))), np.where(((data["rangebatch_slices2_msignal"]) / 2.0) > -998, data["abs_maxbatch_slices2"], (11.21940040588378906) ) )))/2.0)) +
                            0.100000*np.tanh((((7.0)) - (np.where(data["maxtominbatch_slices2_msignal"] <= -998, data["maxtominbatch"], ((data["maxtominbatch_slices2_msignal"]) * (data["maxtominbatch"])) )))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) + (data["medianbatch_msignal"]))) + (np.where(data["minbatch_slices2"] > -998, ((np.where(data["meanbatch_msignal"] > -998, data["medianbatch_msignal"], data["medianbatch_msignal"] )) * 2.0), data["medianbatch_msignal"] )))) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) * 2.0)) +
                            0.100000*np.tanh(np.tanh((((((((data["medianbatch_msignal"]) * 2.0)) + (data["abs_avgbatch_msignal"]))) - (data["maxbatch_msignal"]))))) +
                            0.100000*np.tanh(((np.where((-(((7.87317562103271484)))) <= -998, np.tanh((data["maxbatch_slices2_msignal"])), (((((7.87317562103271484)) / 2.0)) - (data["maxbatch_msignal"])) )) * 2.0)) +
                            0.100000*np.tanh(((((((data["signal_shift_-1_msignal"]) + (((data["signal_shift_+1_msignal"]) / 2.0)))) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.where((0.07474781572818756) > -998, data["signal_shift_+1_msignal"], data["medianbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) + ((-((np.where(((np.tanh((np.where(data["medianbatch_msignal"] <= -998, data["abs_maxbatch_msignal"], data["abs_avgbatch_msignal"] )))) / 2.0) <= -998, data["abs_maxbatch_slices2"], data["abs_avgbatch_msignal"] ))))))) +
                            0.100000*np.tanh((((13.58806991577148438)) + (((((((data["abs_maxbatch"]) * (np.where(((data["minbatch_msignal"]) / 2.0) > -998, data["minbatch_msignal"], (13.58806991577148438) )))) / 2.0)) / 2.0)))) +
                            0.100000*np.tanh(data["stdbatch_slices2"]) +
                            0.100000*np.tanh(((((((data["medianbatch_slices2_msignal"]) - ((10.0)))) + (data["abs_maxbatch_msignal"]))) - ((-((((data["abs_maxbatch_msignal"]) - ((10.0))))))))) +
                            0.100000*np.tanh(((((((data["medianbatch_msignal"]) + (np.tanh((data["maxbatch_msignal"]))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((np.where(data["abs_minbatch_slices2"] > -998, ((data["signal_shift_-1_msignal"]) * (np.tanh((data["medianbatch_slices2_msignal"])))), data["abs_minbatch_slices2"] )) * 2.0)) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2_msignal"]) + (((data["minbatch_msignal"]) / 2.0)))) * (((((data["abs_maxbatch_slices2_msignal"]) * (((data["medianbatch_msignal"]) + (((data["minbatch_msignal"]) / 2.0)))))) + (((data["minbatch_msignal"]) / 2.0)))))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh((((7.0)) * (np.where(data["signal_shift_-1_msignal"] > -998, ((((7.0)) + (data["minbatch_msignal"]))/2.0), (-((np.where(data["abs_maxbatch"] > -998, (4.0), ((data["abs_maxbatch_slices2_msignal"]) / 2.0) )))) )))) +
                            0.100000*np.tanh(((((data["maxbatch_msignal"]) * 2.0)) * (((np.where(data["maxbatch_msignal"] > -998, (6.80128240585327148), ((data["maxbatch_msignal"]) * 2.0) )) - (((data["maxbatch_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh(np.tanh((((((data["meanbatch_msignal"]) - ((3.0)))) * (np.where((3.0) > -998, (3.0), np.where((3.0) > -998, (3.0), data["meanbatch_msignal"] ) )))))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) + (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(((np.tanh((((data["maxbatch_slices2_msignal"]) * (((data["minbatch_msignal"]) * (data["maxbatch_slices2_msignal"]))))))) - (((((data["abs_maxbatch"]) + (((data["minbatch_msignal"]) * (data["maxbatch_slices2_msignal"]))))) + (data["rangebatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) + (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(np.tanh((((((data["abs_maxbatch_slices2_msignal"]) * (data["maxtominbatch_slices2_msignal"]))) / 2.0)))) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) + (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(((np.where(data["abs_avgbatch_slices2_msignal"] > -998, np.where(data["maxtominbatch_slices2_msignal"] > -998, data["maxtominbatch_slices2_msignal"], data["medianbatch_slices2_msignal"] ), data["maxtominbatch_slices2_msignal"] )) * (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.tanh((data["rangebatch_msignal"]))) +
                            0.100000*np.tanh(np.where(np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, data["medianbatch_slices2_msignal"], ((data["stdbatch_slices2_msignal"]) / 2.0) ) <= -998, ((data["stdbatch_slices2_msignal"]) * 2.0), ((((data["meanbatch_msignal"]) - ((-((data["mean_abs_chgbatch_slices2_msignal"])))))) + (data["minbatch"])) )) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2"] <= -998, data["meanbatch_slices2"], ((((data["medianbatch_msignal"]) * 2.0)) + (np.where(data["abs_avgbatch_msignal"] <= -998, ((data["maxtominbatch_slices2_msignal"]) / 2.0), np.tanh((data["abs_maxbatch_slices2_msignal"])) ))) )) +
                            0.100000*np.tanh(np.where(data["minbatch"] > -998, data["maxbatch_slices2_msignal"], (((-((data["abs_maxbatch_slices2_msignal"])))) / 2.0) )) +
                            0.100000*np.tanh(np.tanh((((((np.tanh((data["stdbatch_slices2"]))) / 2.0)) - (np.tanh((data["maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh((((((data["maxbatch_slices2"]) * 2.0)) + (data["maxtominbatch"]))/2.0)) +
                            0.100000*np.tanh(np.where(((data["medianbatch_msignal"]) / 2.0) > -998, np.where(data["maxtominbatch_msignal"] <= -998, data["signal_shift_-1_msignal"], ((data["medianbatch_msignal"]) + (((data["signal_shift_-1_msignal"]) * 2.0))) ), data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) + ((((data["maxbatch_slices2"]) + (data["signal_shift_-1_msignal"]))/2.0)))) + (np.where(np.tanh((((data["signal_shift_+1"]) / 2.0))) <= -998, data["signal_shift_-1_msignal"], data["medianbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(np.where((-((data["maxbatch_msignal"]))) <= -998, (7.0), (((7.0)) + ((((-((data["maxbatch_msignal"])))) * 2.0))) )) +
                            0.100000*np.tanh(np.where(np.tanh((data["medianbatch_msignal"])) <= -998, np.where(((data["medianbatch_msignal"]) + (data["maxtominbatch_msignal"])) > -998, data["mean_abs_chgbatch_slices2"], np.tanh((data["maxbatch_slices2_msignal"])) ), ((data["medianbatch_msignal"]) * 2.0) )) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2"] > -998, np.where(((np.tanh((((data["medianbatch_msignal"]) - (np.tanh((data["medianbatch_slices2"]))))))) + ((5.81768417358398438))) > -998, data["medianbatch_msignal"], data["medianbatch_msignal"] ), data["stdbatch_msignal"] )) +
                            0.100000*np.tanh((((np.where(data["signal_shift_+1"] <= -998, np.where((((data["signal"]) + (data["medianbatch_slices2_msignal"]))/2.0) <= -998, data["mean_abs_chgbatch_slices2"], data["meanbatch_msignal"] ), data["signal_shift_-1"] )) + (data["mean_abs_chgbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh((((((data["medianbatch_msignal"]) - (data["minbatch"]))) + (data["minbatch"]))/2.0)) +
                            0.100000*np.tanh((((13.97538089752197266)) - (np.where(data["maxbatch_slices2_msignal"] <= -998, ((data["maxbatch_slices2_msignal"]) + (data["stdbatch_msignal"])), ((((data["abs_maxbatch"]) + (data["stdbatch_msignal"]))) * (data["abs_maxbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(np.where((((data["abs_minbatch_slices2"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0) <= -998, data["medianbatch_msignal"], (((data["stdbatch_slices2"]) + (data["medianbatch_msignal"]))/2.0) )) +
                            0.100000*np.tanh((((-((np.where(((data["maxtominbatch"]) / 2.0) <= -998, data["maxbatch_slices2"], data["stdbatch_msignal"] ))))) * (((((data["maxbatch_slices2"]) - ((8.0)))) * (data["maxtominbatch"]))))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((((data["medianbatch_slices2_msignal"]) / 2.0)) + (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(np.where(((data["signal_shift_-1"]) * 2.0) <= -998, data["signal_shift_-1"], (((data["abs_minbatch_slices2_msignal"]) + (data["medianbatch_slices2"]))/2.0) )) +
                            0.100000*np.tanh(data["maxbatch_slices2"]) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.tanh((data["maxbatch_msignal"]))) +
                            0.100000*np.tanh((((-((np.tanh((((data["mean_abs_chgbatch_msignal"]) * (((data["mean_abs_chgbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"])))))))))) / 2.0)) +
                            0.100000*np.tanh(np.tanh((((((((data["meanbatch_msignal"]) * 2.0)) + (((((data["minbatch_slices2_msignal"]) + (data["minbatch_msignal"]))) / 2.0)))) * 2.0)))) +
                            0.100000*np.tanh((((data["maxbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.where(data["maxtominbatch"] <= -998, data["signal"], (12.10330677032470703) )) +
                            0.100000*np.tanh(np.tanh((((np.tanh((data["medianbatch_slices2_msignal"]))) * 2.0)))) +
                            0.100000*np.tanh(data["minbatch_slices2"]) +
                            0.100000*np.tanh(((((((((data["medianbatch_msignal"]) + (data["stdbatch_slices2_msignal"]))) - (data["minbatch_slices2"]))) + (data["medianbatch_msignal"]))) - (((data["abs_avgbatch_slices2_msignal"]) / 2.0)))) +
                            0.100000*np.tanh(((np.tanh(((-((((data["maxbatch_msignal"]) - (((((((7.0)) + (data["meanbatch_slices2"]))/2.0)) * ((((data["minbatch_slices2_msignal"]) + ((7.0)))/2.0))))))))))) + (data["abs_minbatch_slices2"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["abs_avgbatch_slices2_msignal"], data["abs_avgbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(np.tanh((np.tanh(((-((np.tanh((data["signal_shift_-1"])))))))))) +
                            0.100000*np.tanh(((np.where(((data["abs_maxbatch_slices2_msignal"]) - (((data["abs_maxbatch_slices2_msignal"]) + ((8.0))))) <= -998, data["mean_abs_chgbatch_slices2"], data["maxbatch_slices2"] )) + (((data["abs_maxbatch_slices2_msignal"]) - ((((8.0)) + (data["minbatch_slices2"]))))))) +
                            0.100000*np.tanh((-(((((data["mean_abs_chgbatch_msignal"]) + ((((-((data["signal_shift_+1"])))) / 2.0)))/2.0))))) +
                            0.100000*np.tanh(((data["stdbatch_slices2_msignal"]) - (np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, data["minbatch_slices2"], (((((data["meanbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2_msignal"]))/2.0)) / 2.0) )))) +
                            0.100000*np.tanh((((data["minbatch"]) + (np.where(data["minbatch"] <= -998, ((((data["minbatch"]) * 2.0)) / 2.0), np.tanh((data["minbatch"])) )))/2.0)) +
                            0.100000*np.tanh(((((data["maxbatch_slices2_msignal"]) / 2.0)) + ((((data["medianbatch_msignal"]) + (data["medianbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh(((data["rangebatch_msignal"]) + (np.tanh((np.tanh(((1.0)))))))) +
                            0.100000*np.tanh(np.where(((data["mean_abs_chgbatch_slices2_msignal"]) * (data["medianbatch_msignal"])) <= -998, data["signal_shift_+1_msignal"], (-((np.tanh((((((data["abs_maxbatch_slices2_msignal"]) * (data["maxbatch_slices2_msignal"]))) - (data["rangebatch_slices2"]))))))) )) +
                            0.100000*np.tanh(((np.where(data["meanbatch_msignal"] > -998, (((((((data["meanbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))/2.0)) + (data["signal_shift_-1_msignal"]))) * 2.0), data["signal_shift_-1_msignal"] )) * 2.0)) +
                            0.100000*np.tanh(np.where(((data["medianbatch_msignal"]) / 2.0) > -998, data["medianbatch_msignal"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh(data["abs_maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((((data["signal_shift_+1"]) / 2.0)) * (((((data["signal"]) * (data["abs_maxbatch_slices2_msignal"]))) - (data["signal_shift_+1"]))))) * ((((3.0)) - (data["abs_maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(data["abs_maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh((((-((((((((((np.tanh(((-((data["medianbatch_msignal"])))))) / 2.0)) / 2.0)) / 2.0)) / 2.0))))) / 2.0)) +
                            0.100000*np.tanh(((data["signal"]) / 2.0)) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (((((np.tanh((data["signal_shift_-1_msignal"]))) * (data["signal"]))) * (data["abs_avgbatch_slices2"]))))) +
                            0.100000*np.tanh(((((((((np.where((6.55823850631713867) <= -998, (6.55823850631713867), (((data["minbatch_msignal"]) + ((6.55823850631713867)))/2.0) )) * 2.0)) * 2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) / 2.0)) - (((data["meanbatch_slices2_msignal"]) / 2.0)))) +
                            0.100000*np.tanh(np.tanh((np.tanh((((data["signal_shift_-1_msignal"]) - (data["signal_shift_-1_msignal"]))))))) +
                            0.100000*np.tanh(((((((((data["signal_shift_-1_msignal"]) + (data["signal_shift_+1_msignal"]))) / 2.0)) + (((((data["signal_shift_-1_msignal"]) + (((data["medianbatch_msignal"]) * 2.0)))) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) + ((((9.0)) - (data["rangebatch_slices2"]))))) * (((data["rangebatch_slices2"]) + (data["signal"]))))) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(np.where((((13.25647449493408203)) * (data["medianbatch_msignal"])) > -998, ((data["signal_shift_+1_msignal"]) * ((((13.25647449493408203)) * (data["medianbatch_msignal"])))), (13.25647449493408203) )) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) + (np.where(data["stdbatch_slices2"] > -998, data["stdbatch_slices2"], np.where(data["stdbatch_slices2"] <= -998, data["stdbatch_slices2"], data["medianbatch_slices2"] ) )))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2"] <= -998, ((((data["minbatch_msignal"]) + (((data["stdbatch_slices2"]) + (data["maxbatch_msignal"]))))) * 2.0), ((((data["minbatch_msignal"]) + (((data["stdbatch_slices2"]) + (data["meanbatch_slices2_msignal"]))))) * 2.0) )) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((((np.where(data["abs_maxbatch_slices2_msignal"] <= -998, data["maxbatch_slices2_msignal"], data["maxbatch_slices2_msignal"] )) * 2.0)) * 2.0)))) +
                            0.100000*np.tanh(np.tanh((data["mean_abs_chgbatch_slices2"]))) +
                            0.100000*np.tanh((((10.25863361358642578)) - (np.where(data["abs_maxbatch_slices2_msignal"] <= -998, data["abs_maxbatch_msignal"], ((data["maxbatch_msignal"]) * (data["abs_maxbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(((((data["signal_shift_+1_msignal"]) + (data["medianbatch_msignal"]))) + (np.where(data["signal_shift_+1_msignal"] <= -998, data["medianbatch_msignal"], data["medianbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((np.where(((data["abs_maxbatch"]) / 2.0) > -998, (((7.0)) + ((((((7.0)) + (data["minbatch_msignal"]))) + (data["minbatch_msignal"])))), data["abs_minbatch_slices2"] )) * 2.0)) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((-((data["minbatch_msignal"])))) +
                            0.100000*np.tanh(np.where(np.where(np.tanh((data["meanbatch_msignal"])) > -998, (0.0), data["meanbatch_msignal"] ) > -998, ((data["meanbatch_msignal"]) - ((3.0))), data["meanbatch_msignal"] )) +
                            0.100000*np.tanh((((data["signal"]) + (((data["medianbatch_slices2"]) - (np.where(((data["abs_avgbatch_msignal"]) - (data["signal"])) <= -998, data["signal"], (1.68725287914276123) )))))/2.0)))   
   
    def GP_class_5(self,data):
        return self.Output( -2.886555 +
                            0.100000*np.tanh(np.where(data["signal"] <= -998, data["meanbatch_slices2"], np.where(data["signal_shift_+1"] > -998, data["meanbatch_slices2"], data["meanbatch_slices2"] ) )) +
                            0.100000*np.tanh(np.where((((data["rangebatch_msignal"]) + (np.tanh(((-((((((data["maxtominbatch"]) / 2.0)) / 2.0))))))))/2.0) <= -998, data["signal_shift_-1_msignal"], (((data["signal_shift_+1"]) + (data["meanbatch_slices2"]))/2.0) )) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(((np.where(((data["signal_shift_-1"]) - (((np.tanh((data["maxbatch_slices2"]))) + (data["meanbatch_slices2"])))) > -998, data["medianbatch_slices2"], np.tanh((data["medianbatch_slices2"])) )) + (data["signal"]))) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1_msignal"] <= -998, data["meanbatch_slices2"], ((data["signal"]) + (data["meanbatch_slices2"])) )) +
                            0.100000*np.tanh(((((((data["meanbatch_msignal"]) * (data["medianbatch_slices2_msignal"]))) * (np.where(data["abs_maxbatch_slices2_msignal"] > -998, data["medianbatch_slices2"], data["abs_maxbatch_slices2"] )))) - (data["abs_avgbatch_slices2"]))) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) - (np.tanh((((data["abs_maxbatch_slices2"]) + ((((8.40865516662597656)) * (data["signal_shift_+1"]))))))))) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((-((np.where(np.tanh(((-((data["rangebatch_msignal"]))))) <= -998, data["signal"], data["abs_maxbatch_slices2_msignal"] ))))) +
                            0.100000*np.tanh(np.where(np.where(data["maxtominbatch_msignal"] <= -998, data["abs_avgbatch_slices2_msignal"], ((((data["abs_maxbatch_slices2"]) + (data["mean_abs_chgbatch_slices2"]))) * 2.0) ) <= -998, data["mean_abs_chgbatch_slices2"], (-((data["abs_avgbatch_msignal"]))) )) +
                            0.100000*np.tanh((((((((-((((data["meanbatch_slices2_msignal"]) + ((-((data["medianbatch_msignal"]))))))))) + (data["meanbatch_slices2_msignal"]))) * (((data["meanbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"]))))) - (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh((((((data["signal_shift_+1"]) / 2.0)) + (np.tanh((((data["meanbatch_slices2_msignal"]) / 2.0)))))/2.0)) +
                            0.100000*np.tanh((-((np.where(data["maxbatch_slices2_msignal"] > -998, ((data["abs_maxbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"])), ((data["medianbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"])) ))))) +
                            0.100000*np.tanh(((((((((data["meanbatch_msignal"]) * (data["meanbatch_msignal"]))) - (data["abs_avgbatch_slices2_msignal"]))) * 2.0)) - (np.where(data["signal_shift_-1"] <= -998, data["meanbatch_msignal"], data["signal_shift_+1"] )))) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_msignal"] > -998, np.tanh((data["meanbatch_slices2"])), ((np.where(data["meanbatch_slices2"] <= -998, ((data["meanbatch_slices2"]) - (data["meanbatch_slices2"])), data["meanbatch_slices2"] )) * 2.0) )) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1"] <= -998, data["signal_shift_-1"], ((((((((data["minbatch_msignal"]) * (data["signal_shift_-1"]))) * (data["abs_avgbatch_msignal"]))) - (data["abs_avgbatch_msignal"]))) * (data["medianbatch_slices2"])) )) +
                            0.100000*np.tanh(((((((data["medianbatch_msignal"]) * (np.where(data["medianbatch_slices2"] > -998, data["abs_avgbatch_msignal"], data["medianbatch_msignal"] )))) - (data["stdbatch_slices2"]))) * 2.0)) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) * (data["abs_avgbatch_slices2_msignal"]))) - (np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["abs_maxbatch_msignal"], (((data["abs_minbatch_slices2"]) + (data["mean_abs_chgbatch_msignal"]))/2.0) )))) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(np.where(np.where(data["medianbatch_slices2_msignal"] <= -998, data["meanbatch_msignal"], data["abs_avgbatch_slices2_msignal"] ) <= -998, data["signal"], ((data["abs_avgbatch_slices2_msignal"]) * (data["meanbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) + ((((-((np.where(data["abs_maxbatch"] > -998, data["medianbatch_msignal"], data["signal_shift_+1"] ))))) - (np.where((-((data["abs_avgbatch_msignal"]))) <= -998, data["rangebatch_msignal"], data["maxbatch_slices2"] )))))) +
                            0.100000*np.tanh((((((((data["meanbatch_slices2_msignal"]) * (data["medianbatch_msignal"]))) - (data["maxbatch_slices2_msignal"]))) + (data["meanbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh((((3.0)) * (data["medianbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where((-((data["abs_maxbatch_slices2_msignal"]))) <= -998, data["abs_avgbatch_slices2_msignal"], ((data["abs_avgbatch_slices2_msignal"]) * (data["medianbatch_msignal"])) )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (np.tanh((((data["meanbatch_msignal"]) + (np.where(data["meanbatch_slices2_msignal"] > -998, data["abs_maxbatch_msignal"], ((data["meanbatch_msignal"]) + ((((data["rangebatch_msignal"]) + (data["signal"]))/2.0))) )))))))) +
                            0.100000*np.tanh(((np.where(data["meanbatch_slices2_msignal"] > -998, data["abs_avgbatch_slices2_msignal"], data["meanbatch_slices2"] )) * (data["medianbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((-((((((data["abs_maxbatch"]) * (data["abs_maxbatch_msignal"]))) / 2.0))))) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * (np.tanh((data["medianbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) - ((2.23324704170227051)))) * (((data["meanbatch_slices2_msignal"]) + (np.where(data["abs_maxbatch_slices2_msignal"] <= -998, (2.23324704170227051), data["maxbatch_msignal"] )))))) +
                            0.100000*np.tanh(((((((data["abs_avgbatch_slices2_msignal"]) + (data["abs_avgbatch_msignal"]))) * (data["abs_maxbatch_slices2_msignal"]))) * ((-((((((3.09535932540893555)) + ((((-((data["stdbatch_slices2"])))) * 2.0)))/2.0))))))) +
                            0.100000*np.tanh(((np.where(np.where(data["rangebatch_slices2_msignal"] <= -998, data["meanbatch_slices2_msignal"], data["maxtominbatch_msignal"] ) <= -998, data["meanbatch_slices2_msignal"], ((data["medianbatch_msignal"]) * (data["meanbatch_slices2_msignal"])) )) - (data["stdbatch_slices2"]))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) * ((((data["meanbatch_msignal"]) + ((((data["mean_abs_chgbatch_msignal"]) + (data["signal_shift_-1"]))/2.0)))/2.0)))) +
                            0.100000*np.tanh(((((data["stdbatch_msignal"]) + (((data["stdbatch_msignal"]) * 2.0)))) * (np.where((((data["abs_maxbatch_msignal"]) + (data["abs_avgbatch_msignal"]))/2.0) > -998, ((data["abs_maxbatch_msignal"]) + (data["meanbatch_msignal"])), data["abs_maxbatch_msignal"] )))) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, data["abs_avgbatch_slices2_msignal"], data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((data["signal"]) + (((((data["signal"]) + (((data["mean_abs_chgbatch_msignal"]) * (data["abs_maxbatch_slices2_msignal"]))))) * (data["maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(np.where((((((((data["mean_abs_chgbatch_slices2"]) + (data["meanbatch_slices2_msignal"]))/2.0)) / 2.0)) / 2.0) > -998, data["abs_avgbatch_slices2_msignal"], (-((data["medianbatch_slices2_msignal"]))) ) <= -998, data["medianbatch_slices2_msignal"], ((data["meanbatch_msignal"]) * (data["meanbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) + (np.where(data["abs_maxbatch_msignal"] > -998, data["abs_maxbatch_msignal"], (((data["abs_maxbatch_msignal"]) + (data["stdbatch_slices2"]))/2.0) )))) * (((data["meanbatch_msignal"]) - (data["stdbatch_slices2"]))))) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) - (data["signal_shift_-1"]))) +
                            0.100000*np.tanh(np.where(np.where(data["rangebatch_msignal"] <= -998, data["stdbatch_slices2"], ((data["minbatch_msignal"]) * 2.0) ) > -998, (((9.0)) + (data["minbatch_msignal"])), (((data["meanbatch_slices2"]) + (data["abs_maxbatch_slices2"]))/2.0) )) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2_msignal"]) - (data["stdbatch_slices2"]))) * (((((np.where(data["stdbatch_slices2"] > -998, data["stdbatch_slices2"], data["stdbatch_slices2"] )) + (data["minbatch_slices2_msignal"]))) + (((data["meanbatch_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh((((((data["meanbatch_msignal"]) + (data["abs_maxbatch_msignal"]))/2.0)) * ((((data["minbatch_slices2_msignal"]) + (((((data["medianbatch_msignal"]) * (data["maxbatch_msignal"]))) + (data["minbatch_msignal"]))))/2.0)))) +
                            0.100000*np.tanh(np.where((8.0) > -998, np.where(data["minbatch_slices2"] > -998, (((8.0)) + (data["minbatch_slices2_msignal"])), (8.0) ), np.where((8.0) > -998, (8.0), ((data["maxbatch_slices2"]) + ((8.0))) ) )) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2_msignal"]) + (data["signal_shift_-1_msignal"]))) * (((data["meanbatch_slices2_msignal"]) - (((np.tanh((data["abs_maxbatch_slices2_msignal"]))) * 2.0)))))) +
                            0.100000*np.tanh((((((((data["meanbatch_slices2"]) + (data["rangebatch_msignal"]))/2.0)) / 2.0)) - (((data["maxbatch_slices2_msignal"]) * 2.0)))) +
                            0.100000*np.tanh((((((((8.0)) * 2.0)) * (((data["abs_maxbatch"]) - ((8.0)))))) * (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(data["minbatch_slices2"]) +
                            0.100000*np.tanh(np.where(((data["mean_abs_chgbatch_msignal"]) + ((0.0))) <= -998, (6.0), np.where(((data["minbatch_slices2"]) * 2.0) <= -998, data["minbatch"], ((data["abs_minbatch_slices2_msignal"]) * (((data["minbatch"]) - (data["mean_abs_chgbatch_msignal"])))) ) )) +
                            0.100000*np.tanh(((np.where((8.0) <= -998, (3.0), data["abs_avgbatch_msignal"] )) * (data["signal"]))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) * (data["signal"]))) * (np.where(((data["signal"]) - (data["medianbatch_slices2_msignal"])) > -998, data["abs_avgbatch_slices2_msignal"], ((data["signal_shift_+1"]) * 2.0) )))) +
                            0.100000*np.tanh((((data["meanbatch_slices2"]) + (((data["maxtominbatch"]) + ((((data["abs_avgbatch_slices2"]) + (np.where(data["meanbatch_slices2"] <= -998, data["maxtominbatch_msignal"], (((((data["signal"]) + (data["signal_shift_-1"]))/2.0)) + (data["signal_shift_-1"])) )))/2.0)))))/2.0)) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh((((data["minbatch_slices2"]) + (data["minbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.tanh((data["signal_shift_+1_msignal"]))) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] <= -998, data["medianbatch_slices2_msignal"], data["minbatch_slices2"] )) +
                            0.100000*np.tanh(((((((((data["signal_shift_-1_msignal"]) / 2.0)) / 2.0)) * (data["signal_shift_-1_msignal"]))) * (np.where(data["mean_abs_chgbatch_slices2_msignal"] <= -998, data["mean_abs_chgbatch_slices2_msignal"], ((data["signal_shift_-1"]) + (data["mean_abs_chgbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(((np.where((8.84894180297851562) > -998, (8.84894180297851562), (8.84894180297851562) )) + (np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, data["minbatch_msignal"], np.where((((8.84894180297851562)) + (data["medianbatch_msignal"])) > -998, (8.84894180297851562), data["minbatch_msignal"] ) )))) +
                            0.100000*np.tanh((((((data["stdbatch_msignal"]) + (((((data["abs_avgbatch_msignal"]) * 2.0)) * (data["meanbatch_slices2_msignal"]))))/2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(np.where(data["meanbatch_msignal"] <= -998, data["abs_minbatch_slices2_msignal"], ((data["meanbatch_slices2_msignal"]) * 2.0) ) <= -998, data["maxtominbatch"], data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(np.where(np.where(data["meanbatch_msignal"] <= -998, (3.0), ((data["signal_shift_-1_msignal"]) + (data["mean_abs_chgbatch_msignal"])) ) <= -998, data["mean_abs_chgbatch_slices2_msignal"], ((data["mean_abs_chgbatch_msignal"]) + (np.where((3.0) > -998, data["mean_abs_chgbatch_slices2_msignal"], data["medianbatch_msignal"] ))) )) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2"] <= -998, data["minbatch_slices2"], ((data["abs_avgbatch_msignal"]) * (((data["minbatch_slices2"]) - ((-((data["minbatch_slices2"]))))))) )) +
                            0.100000*np.tanh(((np.where(((data["abs_avgbatch_msignal"]) + (((data["meanbatch_msignal"]) * (data["maxtominbatch_msignal"])))) > -998, ((data["meanbatch_slices2_msignal"]) * (data["meanbatch_msignal"])), data["meanbatch_msignal"] )) - ((((data["abs_maxbatch"]) + (data["mean_abs_chgbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (np.where(data["medianbatch_msignal"] <= -998, np.where((10.0) > -998, data["rangebatch_msignal"], data["rangebatch_slices2"] ), (10.03490161895751953) )))) +
                            0.100000*np.tanh((((-(((6.24813604354858398))))) + (np.where((-(((6.24813604354858398)))) > -998, data["maxbatch_slices2_msignal"], data["maxbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh((((data["meanbatch_slices2"]) + (data["signal_shift_-1"]))/2.0)) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) - ((((data["maxbatch_slices2_msignal"]) + ((-((np.where(np.where(data["abs_avgbatch_slices2_msignal"] <= -998, data["medianbatch_msignal"], ((data["meanbatch_slices2_msignal"]) / 2.0) ) > -998, (5.0), data["minbatch"] ))))))/2.0)))) * 2.0)) +
                            0.100000*np.tanh(data["minbatch"]) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2"] <= -998, ((data["minbatch_msignal"]) + (data["abs_maxbatch_slices2_msignal"])), data["minbatch_msignal"] )) +
                            0.100000*np.tanh((((data["maxtominbatch_slices2"]) + (((((data["abs_minbatch_slices2_msignal"]) + ((6.32575893402099609)))) * 2.0)))/2.0)) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) + (((np.tanh(((-((data["medianbatch_msignal"])))))) * 2.0)))) * (np.where(((data["medianbatch_msignal"]) / 2.0) > -998, data["signal"], data["medianbatch_slices2"] )))) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((((((np.where(data["signal_shift_-1"] > -998, (5.0), data["abs_avgbatch_slices2"] )) * 2.0)) + (data["minbatch_msignal"]))/2.0)) * ((5.0)))) +
                            0.100000*np.tanh(np.where(data["signal"] <= -998, data["medianbatch_slices2"], data["meanbatch_msignal"] )) +
                            0.100000*np.tanh(((((data["signal"]) * (data["abs_maxbatch_slices2_msignal"]))) * (((data["abs_maxbatch"]) / 2.0)))) +
                            0.100000*np.tanh(np.tanh((np.where(data["stdbatch_slices2_msignal"] > -998, np.tanh((data["maxtominbatch"])), np.tanh((data["maxtominbatch"])) )))) +
                            0.100000*np.tanh(((((data["abs_minbatch_msignal"]) * ((((1.77593755722045898)) - (np.where(data["maxbatch_msignal"] <= -998, data["abs_maxbatch_slices2_msignal"], ((np.where((1.77593755722045898) <= -998, (1.77593755722045898), data["meanbatch_msignal"] )) * (data["meanbatch_msignal"])) )))))) * 2.0)) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) + ((-((data["minbatch_slices2"])))))) +
                            0.100000*np.tanh(np.where(np.tanh((np.tanh(((-(((((data["stdbatch_slices2"]) + (data["maxbatch_slices2_msignal"]))/2.0)))))))) > -998, ((data["medianbatch_msignal"]) * ((((data["meanbatch_msignal"]) + (data["maxbatch_slices2_msignal"]))/2.0))), data["maxtominbatch"] )) +
                            0.100000*np.tanh((((8.0)) * ((((2.0)) - (data["abs_maxbatch_msignal"]))))) +
                            0.100000*np.tanh((((np.where(data["abs_maxbatch_slices2_msignal"] <= -998, ((((data["signal_shift_-1"]) * 2.0)) * (np.where(data["maxtominbatch"] <= -998, data["mean_abs_chgbatch_slices2"], ((data["signal_shift_+1"]) * 2.0) ))), data["abs_minbatch_slices2_msignal"] )) + (data["abs_maxbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.where(((np.tanh((np.where(data["signal_shift_-1"] > -998, data["maxbatch_slices2_msignal"], (((data["stdbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2_msignal"]))/2.0) )))) / 2.0) > -998, ((data["meanbatch_msignal"]) / 2.0), data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(((((((data["abs_avgbatch_slices2_msignal"]) - (data["signal"]))) * 2.0)) * (((data["signal"]) * (((data["stdbatch_slices2_msignal"]) * (data["meanbatch_slices2"]))))))) +
                            0.100000*np.tanh((((-((data["rangebatch_slices2_msignal"])))) - (((np.where(data["minbatch_msignal"] <= -998, data["abs_avgbatch_slices2"], data["maxtominbatch_slices2"] )) * (data["minbatch_msignal"]))))) +
                            0.100000*np.tanh((((2.31002974510192871)) - (np.where((-(((2.31002974510192871)))) > -998, data["maxbatch_msignal"], (-((np.where((((2.31002974510192871)) - (data["maxbatch_msignal"])) > -998, data["maxbatch_msignal"], (((2.31002974510192871)) / 2.0) )))) )))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) - (data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh(((np.where(data["signal_shift_+1"] <= -998, (((1.0)) / 2.0), data["medianbatch_slices2_msignal"] )) - (np.tanh((np.tanh((data["maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2_msignal"] <= -998, np.tanh((data["abs_maxbatch_msignal"])), ((np.tanh((((((((data["medianbatch_msignal"]) - (((np.tanh((data["medianbatch_msignal"]))) * 2.0)))) * 2.0)) * 2.0)))) * 2.0) )) +
                            0.100000*np.tanh(((np.where((2.0) <= -998, data["abs_maxbatch"], (((1.64029991626739502)) - (((((data["maxbatch_msignal"]) / 2.0)) * (data["maxbatch_msignal"])))) )) * 2.0)) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] <= -998, data["rangebatch_slices2"], np.where(((data["mean_abs_chgbatch_slices2_msignal"]) * 2.0) <= -998, ((data["meanbatch_slices2"]) * 2.0), ((((data["abs_minbatch_slices2"]) / 2.0)) / 2.0) ) )) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((((-(((-((data["signal_shift_-1_msignal"]))))))) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.tanh((np.where(np.tanh((((((data["stdbatch_slices2_msignal"]) * 2.0)) * 2.0))) > -998, data["maxbatch_slices2"], (-((data["signal_shift_-1_msignal"]))) )))) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_msignal"] <= -998, np.where(data["abs_maxbatch_msignal"] <= -998, data["abs_maxbatch_slices2_msignal"], data["abs_maxbatch"] ), ((data["mean_abs_chgbatch_slices2_msignal"]) * (data["rangebatch_msignal"])) )) +
                            0.100000*np.tanh(((np.where(data["meanbatch_slices2_msignal"] <= -998, (((data["rangebatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"]))/2.0), ((data["signal_shift_-1"]) * (((((data["mean_abs_chgbatch_slices2"]) * (data["meanbatch_slices2_msignal"]))) - (data["meanbatch_slices2_msignal"])))) )) * 2.0)) +
                            0.100000*np.tanh(((np.where(data["medianbatch_slices2_msignal"] > -998, data["signal_shift_-1_msignal"], data["abs_minbatch_slices2"] )) + (data["maxtominbatch_slices2"]))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) - ((((data["meanbatch_slices2_msignal"]) + (np.where(data["minbatch_slices2"] > -998, ((np.tanh((data["medianbatch_slices2_msignal"]))) * 2.0), data["rangebatch_slices2_msignal"] )))/2.0)))) * (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(data["stdbatch_slices2"]) +
                            0.100000*np.tanh(np.where(data["stdbatch_msignal"] <= -998, ((((((data["signal_shift_-1_msignal"]) * (data["mean_abs_chgbatch_slices2_msignal"]))) / 2.0)) * ((14.59111690521240234))), data["stdbatch_msignal"] )) +
                            0.100000*np.tanh((((((-((data["abs_avgbatch_slices2_msignal"])))) * (data["signal_shift_-1_msignal"]))) - (data["signal_shift_+1_msignal"]))) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2_msignal"] <= -998, data["minbatch"], data["maxbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] <= -998, data["meanbatch_slices2_msignal"], np.where(((data["abs_avgbatch_slices2_msignal"]) * 2.0) <= -998, np.where(np.tanh((data["abs_avgbatch_slices2_msignal"])) <= -998, data["minbatch_msignal"], data["medianbatch_slices2_msignal"] ), ((data["abs_maxbatch_slices2_msignal"]) + (data["minbatch_msignal"])) ) )) +
                            0.100000*np.tanh((-((((((((((np.where(data["maxtominbatch"] <= -998, data["rangebatch_slices2_msignal"], (0.0) )) / 2.0)) / 2.0)) * 2.0)) + ((0.0))))))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) + (((np.tanh(((-((data["medianbatch_msignal"])))))) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((-((data["minbatch_slices2"])))) - ((((-((data["abs_minbatch_msignal"])))) + (np.tanh((((data["rangebatch_msignal"]) - (np.where(data["abs_maxbatch_slices2_msignal"] <= -998, data["meanbatch_msignal"], data["stdbatch_slices2_msignal"] )))))))))) +
                            0.100000*np.tanh(((((data["signal"]) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((-((np.tanh((((((data["abs_maxbatch"]) * (data["abs_minbatch_slices2"]))) + (data["abs_maxbatch_msignal"])))))))) +
                            0.100000*np.tanh((((((9.0)) + (data["minbatch_msignal"]))) * (((data["signal"]) - ((((9.0)) + (data["minbatch_msignal"]))))))) +
                            0.100000*np.tanh((((data["signal"]) + (((data["signal"]) * (((data["abs_maxbatch_msignal"]) * 2.0)))))/2.0)) +
                            0.100000*np.tanh(np.where(((data["maxtominbatch_msignal"]) / 2.0) > -998, (((7.64425468444824219)) + (data["maxtominbatch_msignal"])), ((data["medianbatch_msignal"]) / 2.0) )) +
                            0.100000*np.tanh(((((((((((np.tanh((((((0.0)) + (data["medianbatch_slices2_msignal"]))/2.0)))) * 2.0)) / 2.0)) + ((((-((((((5.0)) + (data["minbatch_msignal"]))/2.0))))) * 2.0)))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(((data["stdbatch_msignal"]) * 2.0) > -998, np.where(data["mean_abs_chgbatch_msignal"] > -998, np.tanh((data["stdbatch_slices2_msignal"])), np.where((-((data["medianbatch_slices2_msignal"]))) > -998, data["stdbatch_msignal"], data["mean_abs_chgbatch_slices2_msignal"] ) ), (-((data["stdbatch_msignal"]))) )) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((np.tanh((data["signal"]))))))) +
                            0.100000*np.tanh(((np.tanh((((data["minbatch_slices2_msignal"]) + ((8.0)))))) * 2.0)) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] <= -998, data["abs_maxbatch_msignal"], ((data["mean_abs_chgbatch_slices2_msignal"]) * (((((data["abs_maxbatch_msignal"]) / 2.0)) - (np.tanh(((10.0))))))) )) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) * (((((data["abs_minbatch_slices2_msignal"]) + (data["abs_minbatch_msignal"]))) * (np.where(data["medianbatch_slices2_msignal"] > -998, data["signal_shift_+1_msignal"], data["abs_minbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh((((6.86082410812377930)) + (np.where(data["medianbatch_slices2_msignal"] > -998, data["minbatch_slices2_msignal"], ((data["rangebatch_msignal"]) + (data["minbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(np.where(((data["abs_maxbatch_msignal"]) + (data["minbatch_msignal"])) <= -998, ((data["minbatch_msignal"]) + (((data["minbatch_msignal"]) - (data["signal_shift_+1_msignal"])))), data["signal_shift_+1"] )) +
                            0.100000*np.tanh(np.tanh((data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(((np.tanh((data["rangebatch_msignal"]))) * (data["mean_abs_chgbatch_slices2"])) <= -998, data["abs_avgbatch_slices2_msignal"], ((data["meanbatch_msignal"]) / 2.0) )) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) - (((((data["minbatch"]) / 2.0)) * 2.0)))) +
                            0.100000*np.tanh(data["abs_minbatch_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((7.0)) * (data["signal"]))) +
                            0.100000*np.tanh(((np.where(((data["medianbatch_msignal"]) * (data["minbatch_slices2_msignal"])) > -998, ((((data["medianbatch_msignal"]) * (data["signal_shift_-1_msignal"]))) * (data["minbatch_slices2_msignal"])), ((data["abs_minbatch_slices2"]) / 2.0) )) * 2.0)) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (np.where(data["maxtominbatch"] > -998, data["maxbatch_msignal"], data["signal_shift_-1_msignal"] )))) +
                            0.100000*np.tanh(((((data["signal"]) * (((((9.0)) + ((9.0)))/2.0)))) * (((data["minbatch_msignal"]) - ((-(((9.61425113677978516))))))))) +
                            0.100000*np.tanh((((data["abs_avgbatch_msignal"]) + (((((((((data["signal_shift_-1"]) - (data["abs_minbatch_slices2"]))) + (np.tanh((data["abs_minbatch_slices2"]))))/2.0)) + ((7.24919748306274414)))/2.0)))/2.0)) +
                            0.100000*np.tanh(np.where((7.0) <= -998, ((data["maxbatch_msignal"]) - (((data["maxbatch_slices2_msignal"]) - (data["maxbatch_msignal"])))), ((((data["maxbatch_msignal"]) - ((7.0)))) * ((7.09985542297363281))) )) +
                            0.100000*np.tanh(((((np.tanh((((((data["abs_avgbatch_slices2_msignal"]) * 2.0)) / 2.0)))) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.where(((np.tanh((data["signal_shift_-1"]))) / 2.0) > -998, ((data["maxbatch_slices2"]) * ((12.02711772918701172))), data["signal_shift_-1"] )) +
                            0.100000*np.tanh(((np.where(data["medianbatch_msignal"] > -998, ((data["medianbatch_msignal"]) / 2.0), data["abs_minbatch_msignal"] )) * (((data["signal_shift_-1_msignal"]) * (np.where(data["medianbatch_msignal"] <= -998, data["rangebatch_slices2"], data["mean_abs_chgbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(((((np.where(data["meanbatch_slices2_msignal"] > -998, ((data["medianbatch_msignal"]) / 2.0), ((data["medianbatch_msignal"]) * 2.0) )) - (np.tanh((data["abs_avgbatch_msignal"]))))) * 2.0)) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_msignal"] <= -998, data["maxbatch_slices2_msignal"], ((data["maxbatch_slices2_msignal"]) + (data["minbatch_msignal"])) )) +
                            0.100000*np.tanh(((((((data["mean_abs_chgbatch_slices2"]) - ((1.0)))) * ((-((data["meanbatch_slices2_msignal"])))))) * (((((((data["medianbatch_slices2"]) - ((1.0)))) * ((-((data["mean_abs_chgbatch_slices2"])))))) * 2.0)))) +
                            0.100000*np.tanh(np.where(np.where(data["mean_abs_chgbatch_slices2"] > -998, (((data["signal_shift_+1_msignal"]) + (data["abs_avgbatch_msignal"]))/2.0), data["meanbatch_msignal"] ) <= -998, data["abs_avgbatch_msignal"], np.tanh(((((((data["signal_shift_+1_msignal"]) + (data["maxtominbatch"]))/2.0)) + (data["medianbatch_msignal"])))) )) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) * (np.where(data["abs_minbatch_msignal"] <= -998, ((data["signal_shift_-1_msignal"]) + (data["meanbatch_msignal"])), ((data["minbatch"]) - (np.where(np.tanh((data["rangebatch_slices2"])) > -998, data["abs_minbatch_msignal"], data["abs_avgbatch_msignal"] ))) )))) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh(np.tanh((((((np.tanh((data["abs_minbatch_slices2"]))) / 2.0)) * (data["signal"]))))) +
                            0.100000*np.tanh(np.where(((data["rangebatch_msignal"]) * (data["medianbatch_slices2_msignal"])) > -998, (((-((data["signal_shift_+1_msignal"])))) * (data["abs_avgbatch_msignal"])), data["meanbatch_msignal"] )) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1"] > -998, ((data["signal_shift_-1"]) * 2.0), np.where(np.tanh((data["rangebatch_slices2"])) <= -998, ((data["signal"]) - (data["minbatch_slices2"])), data["signal"] ) )) +
                            0.100000*np.tanh((0.0)) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, ((data["medianbatch_msignal"]) + (data["medianbatch_msignal"])), ((data["meanbatch_slices2_msignal"]) * 2.0) )) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1"] > -998, data["signal_shift_+1"], ((data["abs_avgbatch_msignal"]) + (data["signal"])) )) +
                            0.100000*np.tanh(((((data["abs_maxbatch_msignal"]) - (((np.tanh(((((6.0)) - (data["rangebatch_slices2"]))))) + ((9.0)))))) * ((((6.0)) - (data["rangebatch_slices2"]))))) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh(((np.where(data["mean_abs_chgbatch_slices2"] <= -998, np.tanh((((((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0)) / 2.0))), data["minbatch_slices2_msignal"] )) + ((((8.59287643432617188)) - (np.tanh((data["mean_abs_chgbatch_slices2"]))))))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["minbatch_slices2"], data["signal_shift_-1_msignal"] )))) +
                            0.100000*np.tanh(np.where(np.where(data["abs_avgbatch_slices2"] > -998, ((data["abs_minbatch_msignal"]) - (data["maxtominbatch"])), data["maxtominbatch"] ) <= -998, np.tanh((np.tanh((data["maxtominbatch_slices2"])))), data["maxtominbatch"] )) +
                            0.100000*np.tanh((-(((((np.tanh((np.where(((data["maxbatch_slices2"]) * 2.0) > -998, data["rangebatch_msignal"], ((((data["abs_minbatch_slices2_msignal"]) * 2.0)) * 2.0) )))) + (data["maxtominbatch_msignal"]))/2.0))))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2_msignal"] > -998, (((((data["medianbatch_msignal"]) * 2.0)) + (data["maxtominbatch_slices2_msignal"]))/2.0), data["maxtominbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) / 2.0)) +
                            0.100000*np.tanh((((data["signal"]) + ((((((data["abs_maxbatch_slices2_msignal"]) / 2.0)) + (np.tanh((((np.tanh(((((data["rangebatch_slices2_msignal"]) + ((9.32928276062011719)))/2.0)))) / 2.0)))))/2.0)))/2.0)) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh(((((((((((data["maxtominbatch_slices2_msignal"]) / 2.0)) + (data["maxtominbatch_slices2_msignal"]))/2.0)) + (np.tanh((data["minbatch"]))))/2.0)) / 2.0)) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) - (((np.tanh((data["abs_avgbatch_msignal"]))) * 2.0)))) +
                            0.100000*np.tanh(((np.where(((data["minbatch_msignal"]) + (((data["medianbatch_msignal"]) + (data["minbatch_msignal"])))) > -998, (((8.0)) + (data["minbatch_msignal"])), data["medianbatch_msignal"] )) * 2.0)) +
                            0.100000*np.tanh(np.tanh((data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((np.where(data["abs_avgbatch_msignal"] > -998, data["medianbatch_msignal"], data["meanbatch_slices2_msignal"] )) + (((((data["medianbatch_slices2_msignal"]) - (data["meanbatch_slices2_msignal"]))) * (((data["abs_maxbatch"]) * 2.0)))))/2.0)) +
                            0.100000*np.tanh((-((((data["abs_avgbatch_slices2"]) * (np.where(data["abs_minbatch_msignal"] <= -998, data["minbatch_slices2_msignal"], ((data["medianbatch_msignal"]) + (data["minbatch_slices2_msignal"])) ))))))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(np.tanh((((data["abs_avgbatch_slices2_msignal"]) * (np.where(((data["stdbatch_slices2"]) / 2.0) > -998, ((data["signal_shift_+1"]) * 2.0), data["meanbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh((((((data["abs_avgbatch_msignal"]) + (data["minbatch_slices2_msignal"]))/2.0)) * (((np.tanh((((((data["signal_shift_-1_msignal"]) * 2.0)) * (data["abs_avgbatch_msignal"]))))) - (((data["signal_shift_+1_msignal"]) * (data["signal_shift_+1_msignal"]))))))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) + (((data["signal_shift_-1"]) * (((data["meanbatch_slices2"]) * ((((8.01053333282470703)) * ((((8.01053333282470703)) - (data["abs_maxbatch_slices2_msignal"]))))))))))) / 2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) / 2.0)) +
                            0.100000*np.tanh(((np.tanh((np.where(data["signal_shift_+1_msignal"] <= -998, data["signal_shift_+1_msignal"], data["signal_shift_+1_msignal"] )))) / 2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2"]) * (data["medianbatch_slices2"]))) +
                            0.100000*np.tanh(np.tanh((np.where(np.tanh((data["mean_abs_chgbatch_msignal"])) <= -998, np.tanh((((np.tanh((data["mean_abs_chgbatch_slices2_msignal"]))) * 2.0))), data["mean_abs_chgbatch_msignal"] )))) +
                            0.100000*np.tanh(((np.tanh((((data["medianbatch_msignal"]) - (((np.where(np.tanh((data["abs_maxbatch_slices2_msignal"])) <= -998, data["mean_abs_chgbatch_slices2"], np.tanh((data["medianbatch_msignal"])) )) * 2.0)))))) * 2.0)) +
                            0.100000*np.tanh(((((((data["mean_abs_chgbatch_slices2"]) - (np.tanh((data["signal_shift_-1"]))))) * (np.where(data["signal_shift_-1"] <= -998, data["signal_shift_-1"], data["meanbatch_msignal"] )))) * 2.0)) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(((np.tanh((data["medianbatch_slices2_msignal"]))) / 2.0)) +
                            0.100000*np.tanh((((((((-(((-((((data["signal_shift_+1_msignal"]) / 2.0)))))))) / 2.0)) * 2.0)) / 2.0)) +
                            0.100000*np.tanh(((data["signal"]) * (((data["medianbatch_msignal"]) - (np.where(data["minbatch_slices2_msignal"] > -998, data["meanbatch_msignal"], (((((data["signal"]) * (data["minbatch_slices2_msignal"]))) + ((0.0)))/2.0) )))))) +
                            0.100000*np.tanh((((((((data["stdbatch_slices2_msignal"]) * ((-((data["abs_minbatch_slices2"])))))) * (((data["abs_avgbatch_msignal"]) / 2.0)))) + (data["abs_minbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh((((9.61471939086914062)) - (((data["abs_maxbatch_slices2"]) + (np.where(((data["mean_abs_chgbatch_slices2_msignal"]) - (np.where((9.61471939086914062) > -998, data["mean_abs_chgbatch_slices2_msignal"], (9.61471939086914062) ))) > -998, data["mean_abs_chgbatch_slices2_msignal"], data["signal_shift_-1"] )))))) +
                            0.100000*np.tanh(np.tanh((np.tanh((data["abs_avgbatch_msignal"]))))) +
                            0.100000*np.tanh(data["abs_maxbatch"]) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) / 2.0)) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) * ((-((((data["mean_abs_chgbatch_slices2"]) - (data["meanbatch_slices2_msignal"])))))))) +
                            0.100000*np.tanh(((((((((data["maxbatch_slices2"]) * 2.0)) * 2.0)) + ((((1.58610856533050537)) * 2.0)))) * ((((-((data["meanbatch_msignal"])))) + (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) - (((np.where(data["minbatch_msignal"] > -998, (-(((5.0)))), data["maxbatch_slices2"] )) * 2.0)))) +
                            0.100000*np.tanh(((np.tanh(((((14.60794353485107422)) + (np.where(data["medianbatch_slices2"] <= -998, ((data["stdbatch_slices2"]) + (data["abs_avgbatch_slices2"])), ((data["abs_avgbatch_slices2"]) / 2.0) )))))) * 2.0)) +
                            0.100000*np.tanh(((((((((data["maxtominbatch"]) + (((np.tanh((data["maxtominbatch"]))) / 2.0)))/2.0)) / 2.0)) + (np.tanh((data["maxtominbatch"]))))/2.0)) +
                            0.100000*np.tanh((((((10.0)) * 2.0)) * (np.tanh((data["mean_abs_chgbatch_slices2"]))))) +
                            0.100000*np.tanh((((((np.where(data["minbatch_msignal"] <= -998, data["meanbatch_slices2_msignal"], (10.0) )) + (data["minbatch_msignal"]))/2.0)) * 2.0)) +
                            0.100000*np.tanh(((np.where(np.where(((data["meanbatch_msignal"]) * 2.0) > -998, data["meanbatch_msignal"], data["meanbatch_msignal"] ) > -998, ((data["signal_shift_+1_msignal"]) * ((-((data["abs_avgbatch_slices2_msignal"]))))), data["signal_shift_-1_msignal"] )) * 2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) + (np.where(data["abs_maxbatch_slices2_msignal"] <= -998, (((6.60356760025024414)) - ((((6.60356760025024414)) * 2.0))), ((data["abs_maxbatch_slices2_msignal"]) - ((((6.60356760025024414)) * 2.0))) )))) +
                            0.100000*np.tanh((((data["signal_shift_+1"]) + (data["signal_shift_+1"]))/2.0)))  
    
    def GP_class_6(self,data):
        return self.Output( -3.287690 +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((np.where(data["signal_shift_-1"] > -998, data["medianbatch_slices2_msignal"], ((data["meanbatch_msignal"]) / 2.0) )) + (np.where(data["medianbatch_slices2"] > -998, data["meanbatch_slices2_msignal"], data["meanbatch_msignal"] )))) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) * (np.where(data["signal_shift_-1"] > -998, data["abs_avgbatch_slices2_msignal"], data["medianbatch_msignal"] )))) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1"] > -998, np.where(data["minbatch_msignal"] > -998, ((data["medianbatch_slices2"]) * 2.0), data["abs_maxbatch"] ), data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(((data["signal"]) * (np.where(data["medianbatch_slices2_msignal"] > -998, data["meanbatch_msignal"], data["meanbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(np.where(data["signal"] > -998, np.tanh((data["meanbatch_slices2"])), ((data["signal_shift_-1"]) * (data["maxbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] <= -998, np.where(data["abs_avgbatch_msignal"] <= -998, data["abs_maxbatch_slices2_msignal"], data["meanbatch_msignal"] ), np.where((((data["medianbatch_slices2_msignal"]) + (data["medianbatch_slices2_msignal"]))/2.0) <= -998, data["meanbatch_msignal"], data["meanbatch_slices2_msignal"] ) )) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2"] <= -998, data["meanbatch_slices2_msignal"], data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(np.where(np.tanh((((data["meanbatch_slices2"]) + ((-((data["abs_avgbatch_slices2_msignal"]))))))) <= -998, data["stdbatch_slices2"], data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(np.where(((data["maxbatch_msignal"]) * ((((data["meanbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))/2.0))) > -998, data["meanbatch_slices2_msignal"], np.where(data["abs_maxbatch_slices2_msignal"] > -998, data["medianbatch_slices2_msignal"], ((data["signal"]) / 2.0) ) )) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh((((data["meanbatch_slices2_msignal"]) + (((data["meanbatch_slices2_msignal"]) + (((data["maxbatch_msignal"]) - (np.where(data["meanbatch_slices2"] > -998, (5.0), (((-((data["meanbatch_slices2_msignal"])))) / 2.0) )))))))/2.0)) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) - (np.where((4.0) <= -998, (4.0), np.where(data["maxbatch_slices2_msignal"] <= -998, data["abs_maxbatch_msignal"], np.where(data["signal_shift_+1_msignal"] <= -998, data["abs_avgbatch_slices2_msignal"], (4.0) ) ) )))) +
                            0.100000*np.tanh(((((((((data["signal_shift_-1"]) * 2.0)) * 2.0)) * (np.where(data["abs_minbatch_msignal"] <= -998, data["medianbatch_msignal"], ((((data["rangebatch_slices2"]) + (data["signal"]))) * (data["meanbatch_msignal"])) )))) * 2.0)) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((np.tanh((data["meanbatch_slices2_msignal"]))) - (((data["minbatch"]) + (np.where(data["meanbatch_msignal"] <= -998, data["signal"], (((5.0)) + (data["mean_abs_chgbatch_slices2_msignal"])) )))))) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(np.where(((np.tanh((np.tanh((np.tanh((((data["mean_abs_chgbatch_msignal"]) - (((data["meanbatch_msignal"]) * 2.0)))))))))) * 2.0) > -998, data["meanbatch_msignal"], np.tanh((data["meanbatch_msignal"])) )) +
                            0.100000*np.tanh(np.where(data["meanbatch_msignal"] > -998, ((data["mean_abs_chgbatch_slices2_msignal"]) + ((-((data["meanbatch_slices2_msignal"]))))), np.where(((data["maxbatch_msignal"]) - (data["signal_shift_+1"])) > -998, ((data["maxtominbatch_slices2_msignal"]) * 2.0), data["stdbatch_msignal"] ) )) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * (((((((data["meanbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))/2.0)) + (data["signal"]))/2.0)))) +
                            0.100000*np.tanh(np.tanh((((data["meanbatch_msignal"]) / 2.0)))) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where(np.tanh((((data["abs_maxbatch_msignal"]) * (data["mean_abs_chgbatch_msignal"])))) > -998, ((((data["maxbatch_msignal"]) * (np.where(data["meanbatch_msignal"] > -998, data["meanbatch_msignal"], data["abs_maxbatch_msignal"] )))) - ((4.51552104949951172))), data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.where((8.62043571472167969) > -998, ((data["maxtominbatch_slices2_msignal"]) - ((8.62043571472167969))), (8.62043571472167969) )) +
                            0.100000*np.tanh(((np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["mean_abs_chgbatch_msignal"], np.where(data["meanbatch_slices2"] > -998, (-((data["abs_avgbatch_slices2_msignal"]))), data["abs_avgbatch_slices2_msignal"] ) )) * ((-((data["abs_avgbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) + (((data["maxbatch_slices2_msignal"]) - ((8.16431045532226562)))))) +
                            0.100000*np.tanh(np.where(data["meanbatch_msignal"] <= -998, data["meanbatch_slices2_msignal"], data["meanbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(((data["maxbatch_slices2"]) - ((8.36985683441162109))) > -998, data["medianbatch_slices2_msignal"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(((np.where(data["signal_shift_-1"] > -998, data["abs_maxbatch_msignal"], (((5.0)) - ((5.0))) )) + ((-(((5.0))))))) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1"] <= -998, ((data["mean_abs_chgbatch_slices2"]) - (np.tanh((data["minbatch_msignal"])))), np.tanh((data["minbatch_msignal"])) )) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(((np.where(data["minbatch_slices2"] <= -998, data["stdbatch_slices2_msignal"], ((((np.tanh((data["stdbatch_slices2"]))) - ((-(((((data["signal_shift_+1"]) + ((-((data["signal_shift_+1"])))))/2.0))))))) * 2.0) )) * (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(((data["mean_abs_chgbatch_msignal"]) / 2.0) > -998, data["minbatch_slices2"], np.tanh((((((data["meanbatch_slices2"]) * (data["signal_shift_-1"]))) / 2.0))) )) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2"]) * (((np.where(data["medianbatch_msignal"] > -998, data["abs_minbatch_slices2_msignal"], (((data["medianbatch_slices2_msignal"]) + (data["signal"]))/2.0) )) / 2.0)))) +
                            0.100000*np.tanh(((((data["signal"]) - (data["meanbatch_msignal"]))) - (data["mean_abs_chgbatch_msignal"]))) +
                            0.100000*np.tanh(((((((((((data["maxtominbatch"]) + (data["signal_shift_-1"]))) * (data["abs_avgbatch_slices2_msignal"]))) * (data["abs_avgbatch_slices2"]))) * (data["signal"]))) - (((data["rangebatch_msignal"]) - (data["abs_avgbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (np.where(np.where((8.0) <= -998, data["maxbatch_slices2"], (8.0) ) <= -998, (8.0), (8.0) )))) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) / 2.0)) +
                            0.100000*np.tanh(np.tanh((data["meanbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(data["stdbatch_slices2_msignal"] > -998, data["stdbatch_slices2_msignal"], (-((data["rangebatch_msignal"]))) )) +
                            0.100000*np.tanh(((((data["signal_shift_-1"]) * (data["mean_abs_chgbatch_msignal"]))) * (np.where(data["signal_shift_-1"] > -998, data["mean_abs_chgbatch_msignal"], data["minbatch"] )))) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) / 2.0)) - (np.tanh((((data["abs_avgbatch_slices2_msignal"]) + (data["stdbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(np.where((-((np.where((-((data["meanbatch_slices2_msignal"]))) > -998, data["meanbatch_slices2_msignal"], data["abs_maxbatch"] )))) <= -998, ((data["stdbatch_slices2"]) * (data["maxtominbatch_msignal"])), (-((data["mean_abs_chgbatch_msignal"]))) )) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (((data["minbatch"]) * (((data["mean_abs_chgbatch_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh((((((data["maxtominbatch"]) + (data["minbatch"]))/2.0)) + (np.where(data["abs_minbatch_msignal"] <= -998, data["abs_minbatch_slices2_msignal"], ((data["abs_minbatch_msignal"]) * (((data["medianbatch_msignal"]) * (data["abs_minbatch_slices2_msignal"])))) )))) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) + ((-((np.where(data["abs_maxbatch_msignal"] <= -998, (((((-(((3.0))))) * 2.0)) * 2.0), (((3.0)) * 2.0) ))))))) +
                            0.100000*np.tanh(((data["stdbatch_slices2"]) - (((data["rangebatch_slices2_msignal"]) - (data["signal"]))))) +
                            0.100000*np.tanh(((((((data["rangebatch_msignal"]) / 2.0)) - ((9.73582649230957031)))) + ((((9.73582649230957031)) / 2.0)))) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_slices2"] > -998, data["medianbatch_slices2_msignal"], data["medianbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.where((5.0) <= -998, (((8.0)) * (((((((5.0)) + (data["minbatch_msignal"]))/2.0)) * (data["minbatch_msignal"])))), ((((((5.0)) + (data["minbatch_msignal"]))/2.0)) * (data["minbatch_msignal"])) )) +
                            0.100000*np.tanh(((((((data["meanbatch_msignal"]) + (((data["abs_avgbatch_slices2_msignal"]) * 2.0)))) + (data["stdbatch_msignal"]))) * ((-((((data["abs_avgbatch_msignal"]) * 2.0))))))) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(((((np.where(data["minbatch_slices2_msignal"] > -998, data["minbatch_slices2_msignal"], (-((data["maxbatch_msignal"]))) )) * (data["minbatch"]))) - (((data["signal_shift_+1"]) - (data["abs_minbatch_msignal"]))))) +
                            0.100000*np.tanh((((data["maxtominbatch_msignal"]) + (((data["maxtominbatch_slices2"]) * 2.0)))/2.0)) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2"] <= -998, data["minbatch_slices2"], ((data["minbatch_slices2"]) * (np.tanh((data["mean_abs_chgbatch_slices2_msignal"])))) )) +
                            0.100000*np.tanh(np.where((-((data["minbatch"]))) <= -998, data["medianbatch_msignal"], ((((((data["signal"]) * (data["meanbatch_msignal"]))) * 2.0)) + (data["maxtominbatch"])) )) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * (data["medianbatch_slices2"]))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2"] <= -998, np.where(np.tanh(((((data["maxtominbatch_slices2"]) + (data["rangebatch_slices2_msignal"]))/2.0))) <= -998, data["meanbatch_slices2_msignal"], data["meanbatch_msignal"] ), np.tanh((data["meanbatch_msignal"])) )) +
                            0.100000*np.tanh(((data["maxtominbatch"]) + (((data["signal"]) * (data["meanbatch_msignal"]))))) +
                            0.100000*np.tanh(((data["minbatch_slices2"]) - (data["abs_avgbatch_msignal"]))) +
                            0.100000*np.tanh(data["abs_maxbatch_slices2"]) +
                            0.100000*np.tanh((-((((data["minbatch_msignal"]) + (((np.where(data["mean_abs_chgbatch_msignal"] > -998, (10.21448040008544922), np.where(((data["mean_abs_chgbatch_msignal"]) * 2.0) > -998, (10.21448040008544922), (10.21448040008544922) ) )) / 2.0))))))) +
                            0.100000*np.tanh((((data["maxtominbatch_slices2_msignal"]) + (data["rangebatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((((((data["abs_minbatch_msignal"]) + (np.tanh((data["maxbatch_slices2_msignal"]))))) / 2.0)))))) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) * 2.0)) +
                            0.100000*np.tanh(data["stdbatch_slices2"]) +
                            0.100000*np.tanh(((((((data["minbatch_slices2_msignal"]) * 2.0)) * 2.0)) - (np.where((-((data["maxbatch_slices2_msignal"]))) <= -998, data["abs_maxbatch_slices2"], ((np.tanh((data["mean_abs_chgbatch_slices2_msignal"]))) / 2.0) )))) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2_msignal"] > -998, np.tanh((((data["rangebatch_msignal"]) - (data["abs_minbatch_msignal"])))), (7.09896183013916016) )) +
                            0.100000*np.tanh(np.tanh((((data["meanbatch_msignal"]) - (data["meanbatch_msignal"]))))) +
                            0.100000*np.tanh(((((((data["meanbatch_msignal"]) + (((data["abs_avgbatch_slices2_msignal"]) / 2.0)))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((((-((np.tanh((((((data["minbatch_slices2_msignal"]) + (data["meanbatch_msignal"]))) - ((-((data["medianbatch_slices2_msignal"]))))))))))) * 2.0)) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) / 2.0)) + (((data["minbatch_slices2_msignal"]) + (data["stdbatch_msignal"]))))) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(np.where((((((((data["medianbatch_slices2"]) + ((((np.where(data["meanbatch_msignal"] > -998, data["maxtominbatch"], data["minbatch_slices2"] )) + ((-((data["meanbatch_msignal"])))))/2.0)))/2.0)) * 2.0)) * 2.0) > -998, data["medianbatch_msignal"], data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(np.where(np.tanh((data["minbatch"])) <= -998, np.tanh((np.tanh((data["minbatch_msignal"])))), (-((np.where(data["meanbatch_msignal"] > -998, data["signal_shift_-1_msignal"], data["rangebatch_slices2_msignal"] )))) )) +
                            0.100000*np.tanh(((np.where(data["signal_shift_+1_msignal"] > -998, data["abs_avgbatch_slices2_msignal"], data["medianbatch_msignal"] )) * ((-((((data["minbatch_msignal"]) + (((data["rangebatch_slices2"]) / 2.0))))))))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2"] <= -998, (-((((data["stdbatch_msignal"]) + (np.tanh((data["medianbatch_msignal"]))))))), data["meanbatch_msignal"] )) +
                            0.100000*np.tanh((((-((np.tanh((data["rangebatch_slices2"])))))) * (data["meanbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((((data["meanbatch_slices2_msignal"]) + (((data["abs_avgbatch_slices2_msignal"]) / 2.0)))/2.0)) * (data["rangebatch_slices2"]))) +
                            0.100000*np.tanh((((((8.0)) / 2.0)) - ((((3.0)) + ((((((data["maxbatch_slices2_msignal"]) + (data["meanbatch_slices2"]))/2.0)) / 2.0)))))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) + (np.tanh((data["signal"]))))) +
                            0.100000*np.tanh((((data["signal"]) + (np.tanh((data["signal"]))))/2.0)) +
                            0.100000*np.tanh(data["stdbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((np.tanh((np.tanh((data["minbatch_slices2_msignal"]))))) - (np.tanh((((data["rangebatch_slices2_msignal"]) / 2.0)))))) + (np.where(data["maxtominbatch"] > -998, data["maxtominbatch_slices2_msignal"], ((data["maxtominbatch_slices2_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh((((data["meanbatch_msignal"]) + ((((data["minbatch"]) + (data["meanbatch_slices2"]))/2.0)))/2.0)) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2"]) * 2.0)) - (np.where(np.tanh((((data["signal_shift_+1_msignal"]) - (np.tanh((data["mean_abs_chgbatch_slices2"])))))) > -998, data["meanbatch_msignal"], data["signal_shift_-1"] )))) +
                            0.100000*np.tanh(((np.where(((data["meanbatch_msignal"]) / 2.0) > -998, data["minbatch_slices2_msignal"], np.tanh((np.where(((((((data["abs_avgbatch_slices2_msignal"]) / 2.0)) * 2.0)) * 2.0) > -998, data["meanbatch_slices2_msignal"], ((data["abs_avgbatch_slices2_msignal"]) / 2.0) ))) )) / 2.0)) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) + (np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["maxtominbatch_slices2_msignal"], data["meanbatch_slices2"] )))) +
                            0.100000*np.tanh(((((np.where(((data["mean_abs_chgbatch_msignal"]) + (data["abs_avgbatch_msignal"])) > -998, data["signal_shift_+1"], ((data["maxtominbatch_msignal"]) * (data["medianbatch_slices2_msignal"])) )) * 2.0)) - (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh(data["stdbatch_msignal"]) +
                            0.100000*np.tanh(np.where((((np.tanh((np.tanh((data["abs_avgbatch_slices2_msignal"]))))) + (((data["abs_avgbatch_slices2_msignal"]) * 2.0)))/2.0) > -998, data["meanbatch_msignal"], data["maxtominbatch_msignal"] )) +
                            0.100000*np.tanh(np.tanh((((data["mean_abs_chgbatch_msignal"]) / 2.0)))) +
                            0.100000*np.tanh(((((((data["medianbatch_msignal"]) + (((data["medianbatch_msignal"]) / 2.0)))) + (((np.where(data["maxbatch_slices2"] > -998, data["meanbatch_msignal"], data["medianbatch_slices2_msignal"] )) / 2.0)))) * 2.0)) +
                            0.100000*np.tanh(np.tanh((data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh((-(((((data["minbatch"]) + (data["abs_avgbatch_msignal"]))/2.0))))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * (((np.where(np.tanh((data["stdbatch_slices2"])) <= -998, data["signal"], ((data["stdbatch_slices2"]) - (data["medianbatch_slices2_msignal"])) )) * (data["stdbatch_slices2"]))))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(np.tanh((((data["stdbatch_slices2"]) * (((data["stdbatch_slices2"]) - (data["medianbatch_msignal"]))))))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * (((np.where(data["signal_shift_-1_msignal"] > -998, data["meanbatch_msignal"], data["signal_shift_-1"] )) + (np.tanh((data["meanbatch_msignal"]))))))) +
                            0.100000*np.tanh(np.tanh((data["minbatch"]))) +
                            0.100000*np.tanh(((np.where(((data["maxbatch_msignal"]) - (data["abs_maxbatch_slices2_msignal"])) > -998, ((data["maxbatch_msignal"]) - ((7.0))), data["maxbatch_slices2"] )) * ((((7.0)) - (((data["abs_maxbatch_slices2_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch"] <= -998, (((data["stdbatch_slices2_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0), data["meanbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] > -998, data["stdbatch_msignal"], ((data["mean_abs_chgbatch_msignal"]) - (data["mean_abs_chgbatch_msignal"])) )) +
                            0.100000*np.tanh((-(((((((data["medianbatch_slices2_msignal"]) * 2.0)) + (np.where(np.where(data["minbatch"] <= -998, ((data["meanbatch_msignal"]) * 2.0), data["signal_shift_+1_msignal"] ) > -998, data["minbatch_msignal"], data["maxtominbatch_slices2_msignal"] )))/2.0))))) +
                            0.100000*np.tanh((((data["stdbatch_msignal"]) + (((((data["mean_abs_chgbatch_slices2_msignal"]) * (data["minbatch_slices2_msignal"]))) * (data["stdbatch_slices2_msignal"]))))/2.0)) +
                            0.100000*np.tanh(np.tanh((data["medianbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((((((data["rangebatch_slices2"]) * (((((((np.where(data["maxbatch_slices2_msignal"] <= -998, data["maxbatch_slices2_msignal"], data["maxbatch_slices2_msignal"] )) - ((5.0)))) * 2.0)) * 2.0)))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((np.tanh(((-((((np.where(data["maxbatch_slices2"] > -998, data["abs_minbatch_msignal"], np.where(data["maxtominbatch"] > -998, data["maxtominbatch_msignal"], np.where(data["abs_minbatch_msignal"] > -998, data["meanbatch_msignal"], data["maxtominbatch"] ) ) )) * 2.0))))))) / 2.0)) +
                            0.100000*np.tanh((((data["abs_avgbatch_msignal"]) + (np.where((((data["stdbatch_slices2_msignal"]) + (((((data["stdbatch_slices2_msignal"]) / 2.0)) - ((-((data["stdbatch_slices2_msignal"])))))))/2.0) > -998, data["maxtominbatch"], data["abs_maxbatch_slices2"] )))/2.0)) +
                            0.100000*np.tanh((-((((np.where(data["meanbatch_msignal"] <= -998, (4.0), data["minbatch_slices2_msignal"] )) + ((3.0))))))) +
                            0.100000*np.tanh(np.tanh((data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) + ((((data["maxtominbatch_slices2"]) + (data["meanbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1_msignal"] > -998, data["medianbatch_msignal"], ((data["maxtominbatch"]) + (((np.tanh((((data["meanbatch_slices2_msignal"]) / 2.0)))) / 2.0))) )) +
                            0.100000*np.tanh(((np.where(data["minbatch_slices2"] > -998, (0.0), data["meanbatch_slices2_msignal"] )) - (data["abs_minbatch_slices2"]))) +
                            0.100000*np.tanh((((np.tanh((data["maxbatch_msignal"]))) + (data["signal_shift_+1"]))/2.0)) +
                            0.100000*np.tanh(data["minbatch_slices2"]) +
                            0.100000*np.tanh((11.75360012054443359)) +
                            0.100000*np.tanh((((0.0)) / 2.0)) +
                            0.100000*np.tanh(((((((data["meanbatch_msignal"]) / 2.0)) * (((data["medianbatch_msignal"]) * (data["meanbatch_msignal"]))))) * (((data["mean_abs_chgbatch_slices2"]) - (((data["meanbatch_msignal"]) / 2.0)))))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(np.tanh((data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2"] <= -998, np.where(data["maxtominbatch"] <= -998, np.tanh((((data["meanbatch_slices2_msignal"]) * 2.0))), data["signal_shift_+1_msignal"] ), ((data["stdbatch_slices2"]) - (data["meanbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * (data["stdbatch_msignal"]))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (np.where(np.where((8.91666603088378906) > -998, (9.0), ((data["rangebatch_slices2"]) - (data["rangebatch_slices2"])) ) > -998, (9.0), data["rangebatch_slices2"] )))) +
                            0.100000*np.tanh(((np.tanh((data["meanbatch_msignal"]))) + (np.tanh((((data["meanbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))))))) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_slices2"] <= -998, data["abs_maxbatch"], ((((data["abs_maxbatch"]) * (data["medianbatch_msignal"]))) - (data["abs_maxbatch"])) )) +
                            0.100000*np.tanh(((np.tanh((((((data["signal_shift_+1"]) / 2.0)) * (data["mean_abs_chgbatch_slices2"]))))) * (data["stdbatch_slices2"]))) +
                            0.100000*np.tanh(data["rangebatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2"]))) +
                            0.100000*np.tanh(((np.where(data["abs_minbatch_msignal"] <= -998, data["signal_shift_+1"], data["meanbatch_msignal"] )) / 2.0)) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh((-((np.tanh((data["medianbatch_msignal"])))))) +
                            0.100000*np.tanh(((np.where(np.where(data["medianbatch_slices2_msignal"] > -998, data["signal_shift_+1"], (((((data["minbatch"]) + (data["abs_maxbatch"]))/2.0)) / 2.0) ) > -998, data["meanbatch_msignal"], data["signal"] )) * 2.0)) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) + (data["abs_maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where((((((data["abs_avgbatch_msignal"]) + (((data["signal_shift_-1"]) * 2.0)))/2.0)) / 2.0) > -998, (-((np.tanh((data["abs_avgbatch_slices2_msignal"]))))), data["minbatch"] )) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1"] > -998, ((data["maxtominbatch"]) + (((data["signal"]) + (data["stdbatch_slices2"])))), data["signal"] )) +
                            0.100000*np.tanh(data["rangebatch_slices2_msignal"]) +
                            0.100000*np.tanh((-((((np.where(((data["signal_shift_-1"]) / 2.0) <= -998, data["abs_minbatch_slices2"], data["abs_maxbatch_slices2_msignal"] )) - (data["abs_maxbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh((((((data["signal_shift_-1"]) - (((data["meanbatch_slices2_msignal"]) - (data["mean_abs_chgbatch_slices2_msignal"]))))) + (data["signal_shift_-1"]))/2.0)) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_msignal"] <= -998, (-((data["stdbatch_slices2"]))), ((data["mean_abs_chgbatch_msignal"]) * (data["maxtominbatch_slices2"])) )) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((np.where(data["rangebatch_slices2_msignal"] > -998, data["maxbatch_slices2"], np.where(data["stdbatch_slices2"] > -998, (0.97140693664550781), data["mean_abs_chgbatch_slices2_msignal"] ) )) / 2.0)) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch"] <= -998, data["meanbatch_msignal"], np.tanh((data["meanbatch_msignal"])) )) +
                            0.100000*np.tanh(((np.tanh((data["signal_shift_+1"]))) / 2.0)) +
                            0.100000*np.tanh(np.tanh((data["signal_shift_-1"]))) +
                            0.100000*np.tanh((-(((((((data["mean_abs_chgbatch_slices2"]) + ((((data["abs_maxbatch_slices2"]) + (((data["abs_avgbatch_msignal"]) / 2.0)))/2.0)))/2.0)) / 2.0))))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2"] <= -998, data["signal_shift_-1"], np.tanh((data["medianbatch_msignal"])) )) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) - (np.where(data["abs_minbatch_slices2"] <= -998, np.tanh((np.tanh((data["signal_shift_-1"])))), (5.0) )))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh((0.01850366964936256)) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2_msignal"] > -998, np.tanh((data["signal_shift_+1"])), (((data["signal_shift_+1"]) + (data["mean_abs_chgbatch_slices2"]))/2.0) )) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0)) +
                            0.100000*np.tanh((((data["medianbatch_slices2"]) + (np.where(data["maxtominbatch_msignal"] > -998, data["meanbatch_msignal"], data["abs_minbatch_slices2_msignal"] )))/2.0)) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2"]) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2"]) * (data["minbatch_slices2"]))) +
                            0.100000*np.tanh(((((np.tanh((((data["maxtominbatch"]) - (data["maxtominbatch_slices2_msignal"]))))) / 2.0)) * (data["stdbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) - (np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], np.tanh(((((data["meanbatch_msignal"]) + ((((-((data["signal_shift_-1"])))) + (data["meanbatch_msignal"]))))/2.0))) )))) +
                            0.100000*np.tanh(np.tanh((data["signal_shift_-1"]))) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh((-(((((5.0)) + (np.where(data["medianbatch_msignal"] <= -998, ((data["signal_shift_+1_msignal"]) - ((-((data["mean_abs_chgbatch_msignal"]))))), data["minbatch_slices2_msignal"] ))))))) +
                            0.100000*np.tanh((((0.17004851996898651)) / 2.0)) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_msignal"] > -998, ((data["maxbatch_slices2"]) + (((data["maxtominbatch"]) * (data["meanbatch_slices2_msignal"])))), np.where(data["maxbatch_slices2"] <= -998, data["maxtominbatch"], data["meanbatch_slices2_msignal"] ) )) +
                            0.100000*np.tanh((-(((((data["stdbatch_slices2_msignal"]) + (data["meanbatch_msignal"]))/2.0))))) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(np.where(data["meanbatch_msignal"] > -998, data["signal_shift_-1_msignal"], data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(np.where(((((data["abs_avgbatch_slices2_msignal"]) * (data["signal_shift_-1_msignal"]))) - (((data["abs_minbatch_slices2"]) + (data["minbatch_slices2_msignal"])))) <= -998, ((data["signal_shift_+1_msignal"]) * (data["stdbatch_msignal"])), ((data["signal_shift_-1_msignal"]) * (data["stdbatch_msignal"])) )) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh((((((data["meanbatch_msignal"]) + (data["medianbatch_msignal"]))/2.0)) * (np.where(data["medianbatch_msignal"] > -998, np.tanh((((data["signal_shift_+1"]) / 2.0))), data["signal"] )))) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1_msignal"] > -998, np.where(data["signal_shift_+1_msignal"] > -998, ((((((np.tanh((data["signal_shift_+1_msignal"]))) * 2.0)) / 2.0)) * (data["signal_shift_+1_msignal"])), data["signal_shift_+1_msignal"] ), np.tanh((data["signal_shift_-1_msignal"])) )) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(np.where(np.tanh((data["stdbatch_slices2"])) > -998, data["medianbatch_msignal"], data["abs_maxbatch"] )) +
                            0.100000*np.tanh(np.where(((data["signal"]) - (np.tanh((np.where(data["abs_maxbatch_slices2"] > -998, data["rangebatch_slices2_msignal"], np.tanh((data["minbatch_slices2"])) ))))) > -998, np.tanh((((data["meanbatch_msignal"]) / 2.0))), data["abs_avgbatch_msignal"] )) +
                            0.100000*np.tanh(((data["maxtominbatch"]) - ((-(((((-((data["minbatch"])))) * (((np.tanh((data["stdbatch_slices2_msignal"]))) / 2.0))))))))) +
                            0.100000*np.tanh(np.tanh((np.where(((data["abs_maxbatch"]) * (data["maxbatch_slices2_msignal"])) > -998, data["signal_shift_+1"], data["meanbatch_slices2"] )))) +
                            0.100000*np.tanh(np.where(data["signal"] <= -998, (1.0), (((data["signal"]) + (data["signal"]))/2.0) )) +
                            0.100000*np.tanh((-(((0.0))))) +
                            0.100000*np.tanh(np.tanh((data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh((-((((np.tanh((((data["mean_abs_chgbatch_slices2"]) + (np.tanh((np.tanh(((((-((np.tanh((data["meanbatch_slices2"])))))) / 2.0)))))))))) / 2.0))))) +
                            0.100000*np.tanh(((data["rangebatch_slices2_msignal"]) * (np.where(np.tanh((np.tanh(((1.0))))) <= -998, ((data["abs_avgbatch_msignal"]) / 2.0), ((data["abs_maxbatch_slices2_msignal"]) * (((data["mean_abs_chgbatch_slices2"]) - ((1.0))))) )))))     
    
    def GP_class_7(self,data):
        return self.Output(-2.939522 +
                            0.100000*np.tanh(np.where(((data["signal_shift_-1"]) / 2.0) > -998, data["signal"], ((data["stdbatch_slices2"]) - (((data["meanbatch_msignal"]) + (((data["meanbatch_msignal"]) * 2.0))))) )) +
                            0.100000*np.tanh(np.where(np.where(data["signal"] <= -998, data["signal"], data["minbatch_slices2"] ) <= -998, data["medianbatch_slices2"], data["medianbatch_slices2"] )) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) * 2.0)) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh((((data["meanbatch_msignal"]) + (((data["signal_shift_+1"]) - (np.where(((data["signal_shift_-1_msignal"]) * 2.0) > -998, (4.0), data["signal_shift_+1"] )))))/2.0)) +
                            0.100000*np.tanh(np.where(((((data["minbatch_slices2_msignal"]) + (data["minbatch"]))) / 2.0) <= -998, data["signal"], (-((data["stdbatch_msignal"]))) )) +
                            0.100000*np.tanh((-((data["minbatch_slices2"])))) +
                            0.100000*np.tanh(np.where(((data["stdbatch_slices2_msignal"]) + (data["signal_shift_+1"])) > -998, data["signal"], data["signal_shift_-1"] )) +
                            0.100000*np.tanh(((((((data["maxbatch_slices2_msignal"]) * 2.0)) - ((8.0)))) * 2.0)) +
                            0.100000*np.tanh(((np.where(data["signal_shift_+1"] <= -998, data["minbatch_msignal"], (-((np.tanh((((data["minbatch_msignal"]) + ((5.0)))))))) )) * 2.0)) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(np.where(((data["medianbatch_slices2"]) / 2.0) > -998, ((data["minbatch_msignal"]) - (((data["abs_minbatch_slices2_msignal"]) * (((data["rangebatch_msignal"]) / 2.0))))), np.where(data["medianbatch_slices2_msignal"] > -998, data["rangebatch_msignal"], data["abs_minbatch_slices2_msignal"] ) )) +
                            0.100000*np.tanh((-(((-((data["abs_avgbatch_slices2"]))))))) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) - ((((6.20869684219360352)) + ((-((data["maxbatch_slices2_msignal"])))))))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh((((-((data["abs_minbatch_slices2_msignal"])))) * (((data["minbatch_msignal"]) * ((-((np.where(data["stdbatch_msignal"] <= -998, np.tanh(((7.0))), data["meanbatch_slices2_msignal"] ))))))))) +
                            0.100000*np.tanh((((data["meanbatch_slices2_msignal"]) + (data["medianbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) * (np.where(((np.tanh((data["maxbatch_slices2"]))) - (data["abs_maxbatch"])) > -998, data["abs_avgbatch_slices2_msignal"], ((data["minbatch_msignal"]) * (data["meanbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) - (data["rangebatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) * (np.where((((data["rangebatch_msignal"]) + (data["maxbatch_slices2"]))/2.0) > -998, data["minbatch_slices2"], data["abs_avgbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh((((((data["stdbatch_msignal"]) * (((((((((data["maxtominbatch_msignal"]) / 2.0)) - (data["meanbatch_msignal"]))) - (data["maxtominbatch_slices2_msignal"]))) - (data["rangebatch_slices2_msignal"]))))) + (data["meanbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(((((((data["mean_abs_chgbatch_slices2"]) * (((data["mean_abs_chgbatch_slices2"]) / 2.0)))) * 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.where(((((data["maxbatch_msignal"]) * (data["mean_abs_chgbatch_slices2"]))) - ((9.03093528747558594))) <= -998, data["mean_abs_chgbatch_slices2"], ((data["mean_abs_chgbatch_slices2_msignal"]) + (((data["abs_avgbatch_slices2"]) * (data["mean_abs_chgbatch_slices2"])))) )) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2"]) - (np.where((((8.0)) + (((((((data["abs_maxbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"]))/2.0)) + (data["meanbatch_slices2"]))/2.0))) > -998, (8.0), data["meanbatch_msignal"] )))) + (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(np.where((8.87376499176025391) <= -998, (8.87376499176025391), (-(((8.87376499176025391)))) ) <= -998, (8.87376499176025391), (((-(((8.87376499176025391))))) - (((data["minbatch_slices2"]) - (data["abs_maxbatch_slices2"])))) )) +
                            0.100000*np.tanh((-(((((((data["medianbatch_msignal"]) + (data["meanbatch_slices2_msignal"]))/2.0)) * (data["medianbatch_msignal"])))))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) + ((-((((np.where(((data["maxtominbatch_msignal"]) * (data["abs_avgbatch_slices2"])) <= -998, data["maxtominbatch_msignal"], data["mean_abs_chgbatch_msignal"] )) * (data["signal"])))))))) +
                            0.100000*np.tanh(((((-((data["abs_minbatch_msignal"])))) + (((data["medianbatch_slices2_msignal"]) * (((data["maxbatch_slices2_msignal"]) - (((data["abs_maxbatch_slices2"]) * (((data["meanbatch_msignal"]) * 2.0)))))))))/2.0)) +
                            0.100000*np.tanh(np.where((4.0) > -998, ((((data["maxbatch_msignal"]) - ((4.0)))) * 2.0), (-((((data["maxbatch_slices2_msignal"]) * (data["maxbatch_msignal"]))))) )) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) - (np.where(((data["signal"]) * 2.0) > -998, (3.22585415840148926), ((data["rangebatch_slices2_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh(((((np.tanh((np.where(data["signal_shift_+1"] > -998, data["rangebatch_slices2_msignal"], ((data["signal_shift_-1"]) - (data["meanbatch_slices2_msignal"])) )))) - (data["mean_abs_chgbatch_slices2"]))) / 2.0)) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_msignal"] <= -998, data["minbatch_slices2"], ((data["maxtominbatch"]) + (((data["stdbatch_slices2_msignal"]) * (np.where(data["signal_shift_-1"] <= -998, data["mean_abs_chgbatch_slices2"], ((data["minbatch_msignal"]) + (np.tanh((data["abs_avgbatch_slices2_msignal"])))) ))))) )) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] <= -998, ((data["meanbatch_msignal"]) / 2.0), np.tanh((data["maxtominbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh((((data["minbatch_slices2"]) + ((((-((np.tanh((data["mean_abs_chgbatch_msignal"])))))) * (data["rangebatch_slices2_msignal"]))))/2.0)) +
                            0.100000*np.tanh(((((data["rangebatch_slices2"]) - (np.where(np.where(data["stdbatch_slices2_msignal"] <= -998, ((data["rangebatch_slices2"]) - (((data["meanbatch_slices2_msignal"]) / 2.0))), data["maxtominbatch_slices2"] ) > -998, (8.0), data["abs_avgbatch_msignal"] )))) * 2.0)) +
                            0.100000*np.tanh(np.tanh((data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) - (((np.where(data["stdbatch_msignal"] > -998, np.where(data["mean_abs_chgbatch_slices2"] > -998, data["stdbatch_msignal"], data["maxbatch_slices2_msignal"] ), data["maxbatch_slices2_msignal"] )) * (data["abs_maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((-((data["medianbatch_slices2_msignal"])))) - (((data["meanbatch_msignal"]) * (((data["meanbatch_msignal"]) + (data["meanbatch_msignal"]))))))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_msignal"]) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where((((((data["meanbatch_msignal"]) - (data["meanbatch_slices2"]))) + (data["mean_abs_chgbatch_msignal"]))/2.0) > -998, data["meanbatch_slices2"], data["meanbatch_msignal"] )) +
                            0.100000*np.tanh(((((data["rangebatch_slices2_msignal"]) - (((data["meanbatch_msignal"]) * (data["rangebatch_slices2"]))))) - (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] > -998, data["medianbatch_msignal"], data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((-((data["meanbatch_msignal"])))) + (((np.where(((data["meanbatch_msignal"]) / 2.0) > -998, ((data["meanbatch_msignal"]) * ((-((data["meanbatch_msignal"]))))), data["medianbatch_msignal"] )) + (data["meanbatch_msignal"]))))) +
                            0.100000*np.tanh((-((((((2.05244112014770508)) + (np.where(data["maxtominbatch_msignal"] > -998, (((5.34226083755493164)) - (((data["maxbatch_slices2_msignal"]) * 2.0))), ((((2.05244112014770508)) + (data["minbatch_slices2_msignal"]))/2.0) )))/2.0))))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * (((data["maxtominbatch_slices2"]) + (((((((((data["maxtominbatch_slices2"]) * (data["abs_avgbatch_slices2_msignal"]))) - (data["minbatch_msignal"]))) * ((-((data["minbatch"])))))) * (data["maxbatch_slices2"]))))))) +
                            0.100000*np.tanh((((((data["maxtominbatch_msignal"]) + (np.where((((data["minbatch_slices2_msignal"]) + (data["rangebatch_slices2_msignal"]))/2.0) > -998, data["rangebatch_slices2_msignal"], data["mean_abs_chgbatch_slices2"] )))/2.0)) - (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) + (((np.where(data["meanbatch_msignal"] > -998, data["mean_abs_chgbatch_slices2"], data["abs_avgbatch_slices2"] )) + (((data["meanbatch_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) * (np.tanh((np.where(data["medianbatch_msignal"] <= -998, (4.0), ((data["maxbatch_msignal"]) - ((4.0))) )))))) +
                            0.100000*np.tanh(((np.where(data["abs_maxbatch"] > -998, data["abs_avgbatch_slices2_msignal"], np.tanh((np.where(((np.tanh((data["abs_maxbatch"]))) / 2.0) > -998, data["minbatch_msignal"], data["maxtominbatch_slices2_msignal"] ))) )) + ((-(((7.0))))))) +
                            0.100000*np.tanh(((((((((data["abs_maxbatch_msignal"]) + (data["maxtominbatch_slices2"]))) * 2.0)) - (((data["maxbatch_slices2_msignal"]) * (((data["abs_avgbatch_slices2_msignal"]) + (data["maxbatch_slices2_msignal"]))))))) - (((data["abs_maxbatch_msignal"]) / 2.0)))) +
                            0.100000*np.tanh((((-((((((data["stdbatch_slices2"]) + (data["meanbatch_msignal"]))) * (data["mean_abs_chgbatch_slices2_msignal"])))))) - (((data["meanbatch_msignal"]) * (data["meanbatch_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, ((data["meanbatch_slices2_msignal"]) - ((((((6.0)) + (data["minbatch_slices2_msignal"]))) * 2.0))), data["maxbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) - (((np.where(data["medianbatch_slices2_msignal"] <= -998, data["medianbatch_slices2_msignal"], data["medianbatch_slices2_msignal"] )) * ((-((((data["minbatch_slices2_msignal"]) * (data["medianbatch_slices2_msignal"])))))))))) +
                            0.100000*np.tanh(((((((data["maxtominbatch_msignal"]) * 2.0)) / 2.0)) + (np.where(data["maxtominbatch_slices2_msignal"] > -998, data["rangebatch_slices2"], data["mean_abs_chgbatch_slices2"] )))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) - ((((5.69999599456787109)) + (np.tanh((data["rangebatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2_msignal"]) + (data["stdbatch_slices2"]))) + (data["stdbatch_slices2"]))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) - (((((((((((data["meanbatch_msignal"]) * (data["meanbatch_msignal"]))) * 2.0)) * (data["medianbatch_msignal"]))) * (data["meanbatch_msignal"]))) * 2.0)))) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) + (((data["medianbatch_slices2_msignal"]) * (np.where(data["abs_maxbatch_slices2_msignal"] <= -998, np.tanh((((data["meanbatch_slices2_msignal"]) / 2.0))), (-((data["medianbatch_msignal"]))) )))))) +
                            0.100000*np.tanh((((6.0)) + (((np.tanh((data["signal"]))) * (((data["maxtominbatch_slices2_msignal"]) / 2.0)))))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - ((((10.0)) + (data["minbatch_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] <= -998, data["minbatch_msignal"], data["mean_abs_chgbatch_msignal"] )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (np.where(data["rangebatch_msignal"] > -998, ((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])), (-((data["medianbatch_msignal"]))) )))) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) - (np.where(data["abs_maxbatch_slices2"] > -998, np.where(data["maxbatch_slices2_msignal"] > -998, (3.0), ((((data["maxbatch_slices2_msignal"]) * 2.0)) + ((3.0))) ), ((data["minbatch_msignal"]) / 2.0) )))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) + (np.where(data["mean_abs_chgbatch_slices2"] <= -998, data["maxtominbatch_slices2_msignal"], ((data["meanbatch_msignal"]) + (np.where(data["meanbatch_msignal"] <= -998, data["mean_abs_chgbatch_msignal"], data["stdbatch_slices2"] ))) )))) +
                            0.100000*np.tanh(((np.where(data["minbatch"] <= -998, data["medianbatch_msignal"], (-((data["medianbatch_msignal"]))) )) * (np.tanh((data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(data["maxtominbatch_slices2"]) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1"] > -998, ((data["mean_abs_chgbatch_slices2"]) - (((data["meanbatch_msignal"]) * (data["meanbatch_msignal"])))), np.where(data["stdbatch_slices2"] > -998, data["meanbatch_msignal"], data["meanbatch_msignal"] ) )) +
                            0.100000*np.tanh((((data["stdbatch_slices2"]) + (np.tanh((data["maxtominbatch_slices2"]))))/2.0)) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2_msignal"] <= -998, ((data["meanbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2"])), data["mean_abs_chgbatch_slices2"] )) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) * (((data["minbatch_slices2_msignal"]) * ((9.16776371002197266)))))) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2"]) + (((data["meanbatch_msignal"]) * 2.0)))) * (np.where(data["rangebatch_slices2_msignal"] <= -998, ((data["mean_abs_chgbatch_slices2"]) - (data["mean_abs_chgbatch_slices2"])), ((data["mean_abs_chgbatch_slices2"]) - (data["medianbatch_msignal"])) )))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2"]) * (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2"]) * ((((((data["mean_abs_chgbatch_slices2"]) * 2.0)) + (np.where(((data["signal"]) / 2.0) <= -998, data["abs_maxbatch_slices2"], np.tanh((data["minbatch_slices2_msignal"])) )))/2.0)))) +
                            0.100000*np.tanh((((-(((10.0))))) + (np.where(data["stdbatch_slices2"] > -998, data["abs_maxbatch"], (((((10.0)) + (np.tanh((data["meanbatch_msignal"]))))) * (data["abs_maxbatch"])) )))) +
                            0.100000*np.tanh((-((((data["maxtominbatch_slices2"]) * (data["abs_avgbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh((((((-((data["medianbatch_slices2_msignal"])))) + (np.tanh((data["abs_minbatch_slices2"]))))) / 2.0)) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) + (((data["medianbatch_msignal"]) * 2.0)))) / 2.0)) +
                            0.100000*np.tanh(data["rangebatch_msignal"]) +
                            0.100000*np.tanh((-(((((-(((-((data["medianbatch_slices2_msignal"]))))))) * (np.where(data["mean_abs_chgbatch_slices2"] > -998, data["medianbatch_msignal"], ((data["stdbatch_msignal"]) / 2.0) ))))))) +
                            0.100000*np.tanh(((np.where(((data["abs_maxbatch_msignal"]) * (np.tanh((data["abs_maxbatch"])))) > -998, ((data["maxbatch_slices2_msignal"]) - ((4.0))), ((data["abs_maxbatch_slices2_msignal"]) / 2.0) )) + (data["stdbatch_slices2"]))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - ((10.47484111785888672)))) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(((data["maxtominbatch"]) - (np.where(np.tanh((data["maxtominbatch"])) <= -998, np.where(data["meanbatch_msignal"] > -998, data["maxtominbatch"], data["maxtominbatch"] ), data["abs_minbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh((((2.0)) * ((0.0)))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - (np.where(((data["meanbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"])) <= -998, data["maxbatch_msignal"], ((data["meanbatch_msignal"]) * (data["maxbatch_msignal"])) )))) +
                            0.100000*np.tanh((((data["meanbatch_slices2"]) + (((((data["meanbatch_msignal"]) * (np.where(((data["meanbatch_msignal"]) / 2.0) > -998, data["meanbatch_msignal"], data["meanbatch_msignal"] )))) * (data["minbatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh(((np.where((-((np.tanh(((-(((8.65891265869140625))))))))) <= -998, data["rangebatch_slices2"], data["rangebatch_slices2"] )) - ((8.65891265869140625)))) +
                            0.100000*np.tanh(((np.where(np.tanh((data["abs_minbatch_slices2_msignal"])) <= -998, (-((data["stdbatch_msignal"]))), data["abs_minbatch_slices2_msignal"] )) / 2.0)) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (((data["mean_abs_chgbatch_slices2"]) - (((((data["medianbatch_msignal"]) * ((((((data["medianbatch_msignal"]) * (data["medianbatch_msignal"]))) + (data["medianbatch_msignal"]))/2.0)))) * (data["medianbatch_msignal"]))))))) +
                            0.100000*np.tanh(((np.where(((((data["meanbatch_msignal"]) + (np.tanh((data["maxbatch_slices2_msignal"]))))) * 2.0) > -998, data["abs_avgbatch_slices2_msignal"], data["meanbatch_msignal"] )) / 2.0)) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (np.where(((data["maxtominbatch"]) + (data["rangebatch_slices2"])) > -998, (10.0), data["rangebatch_slices2"] )))) +
                            0.100000*np.tanh((-((np.where(data["signal_shift_+1_msignal"] <= -998, data["abs_minbatch_msignal"], ((data["stdbatch_slices2_msignal"]) / 2.0) ))))) +
                            0.100000*np.tanh((((data["abs_minbatch_slices2_msignal"]) + (((data["abs_minbatch_slices2_msignal"]) + (data["abs_minbatch_slices2_msignal"]))))/2.0)) +
                            0.100000*np.tanh(((data["maxtominbatch"]) + (((data["signal_shift_+1"]) * 2.0)))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) + (np.where(data["maxbatch_msignal"] > -998, data["meanbatch_msignal"], (14.19020938873291016) )))) +
                            0.100000*np.tanh((-((data["abs_maxbatch"])))) +
                            0.100000*np.tanh((((data["rangebatch_msignal"]) + (np.where(data["rangebatch_slices2_msignal"] > -998, data["maxtominbatch_slices2_msignal"], data["rangebatch_msignal"] )))/2.0)) +
                            0.100000*np.tanh((((-((((data["medianbatch_msignal"]) * (data["meanbatch_msignal"])))))) + (np.tanh((((data["signal_shift_-1"]) + (np.tanh((((((data["meanbatch_msignal"]) * (data["medianbatch_slices2_msignal"]))) + (data["abs_avgbatch_slices2"]))))))))))) +
                            0.100000*np.tanh(((np.where(data["abs_maxbatch_slices2"] <= -998, data["abs_avgbatch_slices2"], (-((((((np.where(data["maxbatch_msignal"] > -998, data["minbatch_msignal"], data["maxtominbatch_msignal"] )) / 2.0)) / 2.0)))) )) + (((data["abs_minbatch_slices2"]) + (data["abs_minbatch_slices2"]))))) +
                            0.100000*np.tanh((((data["meanbatch_msignal"]) + (((data["maxtominbatch"]) / 2.0)))/2.0)) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) - (((data["medianbatch_slices2_msignal"]) * (((np.where(((data["minbatch_msignal"]) - (data["medianbatch_slices2_msignal"])) > -998, data["meanbatch_msignal"], data["medianbatch_slices2_msignal"] )) * 2.0)))))) +
                            0.100000*np.tanh((-((data["medianbatch_slices2_msignal"])))) +
                            0.100000*np.tanh(((((np.where(data["medianbatch_msignal"] > -998, data["meanbatch_msignal"], data["signal_shift_-1"] )) - ((8.40038681030273438)))) + (data["rangebatch_slices2"]))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((np.where(data["signal"] > -998, data["signal_shift_-1_msignal"], data["meanbatch_msignal"] )) * (np.where(data["signal"] > -998, data["medianbatch_msignal"], ((data["meanbatch_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh((((((-((data["medianbatch_msignal"])))) / 2.0)) * (((data["minbatch_slices2_msignal"]) + (np.tanh(((((-(((1.39753139019012451))))) - (data["medianbatch_msignal"]))))))))) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] > -998, ((((data["signal_shift_+1"]) - (data["meanbatch_slices2"]))) * (data["abs_minbatch_slices2"])), (-((np.where(data["abs_minbatch_slices2"] <= -998, data["abs_minbatch_slices2"], data["abs_avgbatch_slices2_msignal"] )))) )) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) - (((((data["meanbatch_msignal"]) * (data["medianbatch_msignal"]))) * (((data["rangebatch_slices2"]) + ((((-((data["medianbatch_msignal"])))) * 2.0)))))))) +
                            0.100000*np.tanh(np.where(np.tanh((data["maxbatch_slices2_msignal"])) <= -998, data["abs_minbatch_slices2"], ((data["medianbatch_msignal"]) - (((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])))) )) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((((data["abs_avgbatch_slices2_msignal"]) * (data["abs_avgbatch_slices2_msignal"]))) - (data["rangebatch_msignal"]))) * (((data["mean_abs_chgbatch_msignal"]) + (data["mean_abs_chgbatch_slices2"]))))) +
                            0.100000*np.tanh(((np.where(((data["abs_maxbatch_slices2"]) * 2.0) > -998, data["abs_minbatch_slices2_msignal"], data["mean_abs_chgbatch_msignal"] )) * (data["abs_avgbatch_msignal"]))) +
                            0.100000*np.tanh((((data["abs_maxbatch_slices2"]) + ((((-((((data["minbatch_slices2"]) * (((((((data["stdbatch_slices2_msignal"]) * 2.0)) / 2.0)) * 2.0))))))) / 2.0)))/2.0)) +
                            0.100000*np.tanh(np.where((((np.where(data["minbatch_slices2_msignal"] > -998, data["minbatch_msignal"], data["minbatch_msignal"] )) + (data["meanbatch_slices2_msignal"]))/2.0) > -998, ((data["mean_abs_chgbatch_msignal"]) / 2.0), data["abs_minbatch_slices2"] )) +
                            0.100000*np.tanh(((((data["abs_minbatch_slices2"]) / 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((data["maxbatch_slices2_msignal"]) - (((data["maxtominbatch"]) * (data["maxtominbatch"]))))) + ((((((data["abs_maxbatch_msignal"]) + (np.tanh((data["signal_shift_+1"]))))/2.0)) / 2.0)))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2_msignal"] > -998, data["mean_abs_chgbatch_slices2"], np.tanh((data["meanbatch_msignal"])) )) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh((-((np.tanh((((data["meanbatch_msignal"]) * 2.0))))))) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_slices2"] <= -998, ((data["medianbatch_msignal"]) + (((np.tanh((data["maxtominbatch_slices2"]))) * 2.0))), ((data["maxtominbatch_slices2"]) - (data["medianbatch_msignal"])) )) +
                            0.100000*np.tanh((((((((data["maxbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))/2.0)) / 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.tanh((((data["rangebatch_slices2"]) - (np.tanh((data["medianbatch_msignal"]))))))) +
                            0.100000*np.tanh(np.where(((data["signal_shift_-1_msignal"]) * 2.0) <= -998, (((((1.0)) * (data["meanbatch_msignal"]))) * (((data["signal_shift_-1_msignal"]) * 2.0))), ((data["mean_abs_chgbatch_slices2"]) * (((data["signal_shift_-1_msignal"]) * (data["signal_shift_-1_msignal"])))) )) +
                            0.100000*np.tanh(((np.where(np.where(data["abs_maxbatch_slices2"] <= -998, data["meanbatch_slices2_msignal"], (-((data["abs_minbatch_slices2_msignal"]))) ) <= -998, data["signal_shift_+1"], data["minbatch"] )) - (data["signal_shift_+1"]))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((np.where(((((data["signal_shift_-1_msignal"]) + (data["abs_maxbatch_slices2"]))) + (data["minbatch"])) > -998, data["maxbatch_slices2_msignal"], data["abs_maxbatch_slices2_msignal"] )) * 2.0)))) +
                            0.100000*np.tanh((-((((np.where(((data["abs_maxbatch_msignal"]) - ((8.0))) <= -998, data["abs_maxbatch_msignal"], (((8.0)) - (((data["abs_maxbatch_msignal"]) * 2.0))) )) * 2.0))))) +
                            0.100000*np.tanh(((np.tanh((data["mean_abs_chgbatch_slices2"]))) * ((((((-((data["medianbatch_msignal"])))) * 2.0)) + (data["mean_abs_chgbatch_slices2"]))))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) / 2.0)) +
                            0.100000*np.tanh((((((((((data["signal_shift_-1_msignal"]) + (data["rangebatch_msignal"]))/2.0)) + ((((data["meanbatch_slices2"]) + (data["medianbatch_msignal"]))/2.0)))) * (data["signal_shift_-1_msignal"]))) * (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh((((np.where((((8.0)) * ((((data["rangebatch_slices2_msignal"]) + (data["maxtominbatch"]))/2.0))) > -998, data["maxtominbatch"], data["abs_avgbatch_slices2"] )) + ((8.0)))/2.0)) +
                            0.100000*np.tanh((-((((data["mean_abs_chgbatch_slices2_msignal"]) + (((((10.0)) + (((np.where(data["mean_abs_chgbatch_slices2_msignal"] <= -998, data["maxtominbatch_msignal"], data["minbatch"] )) * 2.0)))/2.0))))))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((((np.where(data["abs_maxbatch_msignal"] <= -998, np.where((2.0) > -998, (((2.0)) * 2.0), data["meanbatch_msignal"] ), data["abs_maxbatch_msignal"] )) - ((((2.0)) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh((-((np.where((((data["maxbatch_slices2_msignal"]) + (data["minbatch_msignal"]))/2.0) > -998, (((data["maxbatch_slices2_msignal"]) + (data["minbatch_msignal"]))/2.0), data["minbatch_msignal"] ))))) +
                            0.100000*np.tanh((((((-(((((4.0)) / 2.0))))) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(data["rangebatch_slices2"]) +
                            0.100000*np.tanh((((data["medianbatch_msignal"]) + (data["abs_minbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((data["meanbatch_msignal"]))))) +
                            0.100000*np.tanh(np.tanh((((data["signal_shift_-1_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * ((((((((((np.where(data["abs_avgbatch_slices2_msignal"] <= -998, data["maxtominbatch_slices2_msignal"], data["medianbatch_slices2_msignal"] )) * (data["stdbatch_slices2_msignal"]))) + ((-((data["abs_maxbatch"])))))/2.0)) / 2.0)) / 2.0)))) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, np.tanh((data["meanbatch_msignal"])), data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_msignal"] > -998, data["maxbatch_slices2_msignal"], np.where((-((data["maxbatch_msignal"]))) > -998, ((data["stdbatch_slices2"]) / 2.0), data["meanbatch_slices2"] ) )) +
                            0.100000*np.tanh((-(((((-((((np.tanh((((((data["abs_minbatch_msignal"]) * 2.0)) / 2.0)))) / 2.0))))) / 2.0))))) +
                            0.100000*np.tanh(((data["rangebatch_msignal"]) - (np.where(data["rangebatch_slices2"] > -998, np.where((-((data["rangebatch_msignal"]))) > -998, data["abs_maxbatch"], data["abs_maxbatch"] ), ((data["rangebatch_msignal"]) - (data["rangebatch_msignal"])) )))) +
                            0.100000*np.tanh(((((((data["rangebatch_slices2_msignal"]) + ((((data["abs_maxbatch_slices2"]) + (data["mean_abs_chgbatch_slices2"]))/2.0)))) + (((data["signal_shift_-1"]) / 2.0)))) * 2.0)) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh(((((data["maxtominbatch_slices2"]) * (data["medianbatch_msignal"]))) * (np.tanh((data["stdbatch_msignal"]))))) +
                            0.100000*np.tanh((((np.where(data["maxtominbatch"] > -998, (-((data["abs_maxbatch_slices2_msignal"]))), data["abs_maxbatch_slices2_msignal"] )) + ((-((data["minbatch_msignal"])))))/2.0)) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (data["signal_shift_-1_msignal"]))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) - (np.where(data["signal_shift_-1_msignal"] > -998, np.where(data["abs_maxbatch_slices2_msignal"] > -998, (3.0), np.where(data["abs_maxbatch_slices2_msignal"] <= -998, (3.0), ((data["abs_maxbatch_slices2_msignal"]) - (data["abs_maxbatch_slices2_msignal"])) ) ), data["abs_maxbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] > -998, data["meanbatch_msignal"], data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh((((data["maxbatch_msignal"]) + (((np.where(data["abs_maxbatch_slices2_msignal"] > -998, data["maxbatch_msignal"], np.tanh((data["meanbatch_slices2_msignal"])) )) - (((data["mean_abs_chgbatch_msignal"]) * (data["medianbatch_slices2_msignal"]))))))/2.0)) +
                            0.100000*np.tanh((((-((((np.tanh((((np.tanh((np.tanh((data["abs_avgbatch_slices2_msignal"]))))) / 2.0)))) / 2.0))))) * (((data["signal"]) - (np.tanh((data["maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh(((((np.tanh((data["medianbatch_msignal"]))) * ((((-((data["medianbatch_msignal"])))) / 2.0)))) / 2.0)) +
                            0.100000*np.tanh(((np.where(data["rangebatch_slices2_msignal"] > -998, (((((((data["meanbatch_msignal"]) * 2.0)) + (data["abs_minbatch_slices2"]))/2.0)) + (((data["rangebatch_slices2_msignal"]) + (data["maxtominbatch_slices2_msignal"])))), data["rangebatch_slices2_msignal"] )) * (data["rangebatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(((data["maxtominbatch_msignal"]) - (data["maxtominbatch_msignal"])) <= -998, data["abs_avgbatch_msignal"], ((np.tanh((data["abs_avgbatch_msignal"]))) * ((((data["maxtominbatch_msignal"]) + (data["maxtominbatch_msignal"]))/2.0))) )) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2_msignal"] > -998, ((data["abs_maxbatch_msignal"]) - ((4.0))), np.where((4.0) > -998, ((data["abs_maxbatch_msignal"]) + (data["abs_maxbatch_msignal"])), data["abs_maxbatch_msignal"] ) )) +
                            0.100000*np.tanh(((((data["maxtominbatch"]) + (data["signal_shift_-1"]))) + ((((data["maxtominbatch"]) + (np.where(data["rangebatch_slices2_msignal"] <= -998, data["abs_avgbatch_msignal"], data["medianbatch_slices2"] )))/2.0)))) +
                            0.100000*np.tanh(((((data["abs_minbatch_slices2"]) * (np.tanh(((((-((data["minbatch_slices2"])))) * 2.0)))))) / 2.0)) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(np.tanh((data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) + (((data["mean_abs_chgbatch_slices2"]) + (((np.where(data["meanbatch_slices2_msignal"] > -998, data["medianbatch_msignal"], data["medianbatch_slices2_msignal"] )) * 2.0)))))) +
                            0.100000*np.tanh(((np.where((-((((np.tanh((((data["signal_shift_+1_msignal"]) * (data["rangebatch_slices2"]))))) / 2.0)))) <= -998, data["mean_abs_chgbatch_slices2"], ((((data["meanbatch_msignal"]) * (data["signal_shift_+1_msignal"]))) * 2.0) )) / 2.0)) +
                            0.100000*np.tanh(np.where(data["stdbatch_msignal"] <= -998, np.tanh((data["rangebatch_slices2_msignal"])), ((np.tanh((np.tanh((data["abs_minbatch_slices2"]))))) / 2.0) )) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2"] <= -998, data["signal_shift_-1"], ((data["signal_shift_-1"]) / 2.0) )) +
                            0.100000*np.tanh(np.tanh((((data["abs_maxbatch_msignal"]) / 2.0)))) +
                            0.100000*np.tanh((((((((((0.40583977103233337)) * 2.0)) / 2.0)) + ((0.0)))) / 2.0)) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) * (((data["meanbatch_msignal"]) + (np.tanh(((((data["maxbatch_slices2_msignal"]) + ((((data["mean_abs_chgbatch_slices2"]) + (np.tanh((data["mean_abs_chgbatch_slices2_msignal"]))))/2.0)))/2.0)))))))) +
                            0.100000*np.tanh(((np.tanh((np.where(data["stdbatch_slices2"] <= -998, data["abs_avgbatch_slices2"], ((data["stdbatch_slices2"]) + (data["stdbatch_slices2"])) )))) / 2.0)) +
                            0.100000*np.tanh((-((((np.where(data["medianbatch_msignal"] <= -998, data["minbatch_msignal"], (((13.77824592590332031)) / 2.0) )) + (data["minbatch_msignal"])))))) +
                            0.100000*np.tanh(np.where(data["meanbatch_msignal"] > -998, data["medianbatch_msignal"], data["meanbatch_msignal"] )) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) + ((((data["abs_avgbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2"]))/2.0)))) +
                            0.100000*np.tanh((((data["stdbatch_slices2"]) + (np.where(data["meanbatch_msignal"] > -998, data["meanbatch_msignal"], np.where(data["abs_maxbatch_msignal"] > -998, data["medianbatch_msignal"], (((data["abs_minbatch_slices2"]) + (data["signal_shift_+1_msignal"]))/2.0) ) )))/2.0)) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2_msignal"] > -998, ((data["mean_abs_chgbatch_slices2"]) / 2.0), ((((np.where(data["signal_shift_+1_msignal"] > -998, ((((((data["abs_minbatch_slices2"]) / 2.0)) / 2.0)) / 2.0), (1.0) )) / 2.0)) / 2.0) )) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) * (np.where(((np.tanh(((14.24121093750000000)))) / 2.0) > -998, np.where(((data["signal_shift_-1_msignal"]) * (np.tanh((data["medianbatch_msignal"])))) > -998, data["medianbatch_msignal"], data["abs_avgbatch_slices2_msignal"] ), data["abs_avgbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((((-((data["abs_avgbatch_msignal"])))) * (np.where((-((data["abs_avgbatch_msignal"]))) <= -998, data["abs_minbatch_slices2"], ((data["medianbatch_msignal"]) / 2.0) )))) * (((np.tanh((data["rangebatch_msignal"]))) / 2.0)))) +
                            0.100000*np.tanh(np.tanh((((((((((2.08959150314331055)) / 2.0)) + (data["rangebatch_slices2_msignal"]))/2.0)) / 2.0)))) +
                            0.100000*np.tanh(((((data["signal_shift_+1_msignal"]) * (((((data["meanbatch_msignal"]) / 2.0)) * (data["rangebatch_slices2_msignal"]))))) / 2.0)) +
                            0.100000*np.tanh((((((data["abs_minbatch_slices2"]) + (data["abs_minbatch_slices2"]))/2.0)) / 2.0)) +
                            0.100000*np.tanh((((((data["medianbatch_slices2_msignal"]) * (((data["stdbatch_msignal"]) * (np.where(data["abs_maxbatch_slices2_msignal"] > -998, data["meanbatch_slices2_msignal"], data["medianbatch_slices2_msignal"] )))))) + ((6.0)))/2.0)) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.where(np.tanh((((np.tanh((data["mean_abs_chgbatch_slices2"]))) / 2.0))) <= -998, ((data["signal_shift_+1"]) / 2.0), data["abs_avgbatch_slices2"] )) +
                            0.100000*np.tanh(data["abs_minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where(np.where(data["abs_avgbatch_msignal"] > -998, (-((data["minbatch_msignal"]))), np.tanh((data["maxbatch_slices2_msignal"])) ) > -998, (-((((data["maxbatch_slices2_msignal"]) + (data["minbatch_msignal"]))))), data["medianbatch_slices2"] )) +
                            0.100000*np.tanh(np.tanh((data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where((0.0) > -998, data["meanbatch_slices2_msignal"], np.where(data["meanbatch_msignal"] > -998, data["abs_minbatch_slices2"], data["meanbatch_msignal"] ) )) +
                            0.100000*np.tanh(np.tanh((((data["abs_minbatch_slices2"]) - (data["abs_minbatch_slices2"]))))) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) + (np.where(np.where(data["signal_shift_+1"] <= -998, data["meanbatch_slices2"], data["signal_shift_+1"] ) <= -998, data["abs_maxbatch_slices2_msignal"], ((np.where(data["mean_abs_chgbatch_slices2_msignal"] <= -998, data["meanbatch_msignal"], ((data["stdbatch_msignal"]) * 2.0) )) / 2.0) )))) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] <= -998, ((data["medianbatch_msignal"]) / 2.0), data["abs_minbatch_slices2"] )) +
                            0.100000*np.tanh(((np.where(data["signal_shift_-1_msignal"] > -998, np.tanh((np.where(data["maxbatch_slices2_msignal"] > -998, np.tanh((data["signal_shift_+1_msignal"])), ((np.tanh((data["maxtominbatch_slices2_msignal"]))) / 2.0) ))), data["maxtominbatch_msignal"] )) / 2.0)) )   
        
    def GP_class_8(self,data):
        return self.Output( -3.012512 +
                            0.100000*np.tanh(np.where((((data["signal_shift_+1"]) + (data["signal_shift_+1_msignal"]))/2.0) <= -998, data["meanbatch_msignal"], data["signal_shift_-1"] )) +
                            0.100000*np.tanh(((data["signal"]) + (data["signal"]))) +
                            0.100000*np.tanh(((np.where(data["meanbatch_slices2"] <= -998, np.where(data["abs_avgbatch_slices2_msignal"] > -998, (10.51450538635253906), data["abs_avgbatch_slices2_msignal"] ), data["stdbatch_slices2_msignal"] )) * (data["minbatch_msignal"]))) +
                            0.100000*np.tanh(np.where((((data["minbatch"]) + (data["signal_shift_+1"]))/2.0) <= -998, (-((np.where(np.where(data["minbatch"] > -998, data["signal"], (4.0) ) > -998, (9.0), data["abs_avgbatch_slices2"] )))), (-((data["abs_avgbatch_slices2_msignal"]))) )) +
                            0.100000*np.tanh(((((data["signal_shift_-1"]) / 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where((-((data["meanbatch_slices2"]))) <= -998, ((data["abs_avgbatch_slices2_msignal"]) * 2.0), (-((((data["abs_avgbatch_slices2_msignal"]) * 2.0)))) )) +
                            0.100000*np.tanh(np.where((((data["maxtominbatch"]) + (data["signal_shift_-1_msignal"]))/2.0) > -998, ((data["signal_shift_-1"]) * ((-((data["medianbatch_msignal"]))))), (((data["minbatch_msignal"]) + (data["abs_minbatch_slices2"]))/2.0) )) +
                            0.100000*np.tanh((((data["meanbatch_slices2"]) + (data["maxtominbatch"]))/2.0)) +
                            0.100000*np.tanh(np.where(np.where(((data["signal_shift_+1"]) * 2.0) <= -998, data["signal_shift_+1"], data["signal_shift_+1"] ) <= -998, data["stdbatch_slices2_msignal"], data["signal_shift_+1"] )) +
                            0.100000*np.tanh((((-((data["stdbatch_msignal"])))) * ((((-((data["stdbatch_msignal"])))) * ((-((data["abs_avgbatch_msignal"])))))))) +
                            0.100000*np.tanh(np.where((6.00140142440795898) > -998, np.where(data["abs_avgbatch_slices2_msignal"] <= -998, (-((((data["meanbatch_slices2"]) * 2.0)))), data["signal_shift_+1"] ), ((((data["signal_shift_+1"]) - (data["signal_shift_-1"]))) * 2.0) )) +
                            0.100000*np.tanh(np.where((-((((data["abs_avgbatch_slices2_msignal"]) * (data["abs_maxbatch"]))))) > -998, (-((data["abs_avgbatch_slices2_msignal"]))), np.where(((data["medianbatch_slices2"]) * (data["medianbatch_slices2"])) > -998, data["signal_shift_-1"], data["abs_minbatch_slices2"] ) )) +
                            0.100000*np.tanh(((np.where(data["abs_maxbatch_slices2_msignal"] <= -998, (9.0), ((data["medianbatch_msignal"]) * (data["minbatch_msignal"])) )) + (((data["medianbatch_slices2"]) - (np.where(data["maxbatch_slices2"] > -998, (9.0), data["maxbatch_slices2"] )))))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2"]) * (np.where(((data["stdbatch_slices2"]) / 2.0) <= -998, (2.0), ((data["mean_abs_chgbatch_slices2"]) * (np.where(np.tanh((data["minbatch_msignal"])) <= -998, data["abs_maxbatch_slices2_msignal"], (-((data["meanbatch_msignal"]))) ))) )))) +
                            0.100000*np.tanh(((((((np.tanh((((data["signal_shift_+1_msignal"]) - (data["meanbatch_slices2_msignal"]))))) / 2.0)) * 2.0)) - (np.tanh((((data["signal_shift_+1_msignal"]) - (data["meanbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((((data["rangebatch_msignal"]) + (((data["abs_maxbatch_slices2"]) + ((-(((11.64076900482177734))))))))) - (np.tanh((data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh((-((((data["meanbatch_slices2_msignal"]) / 2.0))))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) - (np.where(data["meanbatch_msignal"] <= -998, data["stdbatch_slices2_msignal"], ((data["abs_maxbatch"]) + (((data["stdbatch_msignal"]) * (data["maxbatch_slices2_msignal"])))) )))) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) - (((((np.where(((data["abs_maxbatch_slices2_msignal"]) * ((-((data["meanbatch_slices2_msignal"]))))) > -998, data["minbatch_msignal"], np.tanh((((data["meanbatch_slices2_msignal"]) * 2.0))) )) * 2.0)) + ((13.73357105255126953)))))) +
                            0.100000*np.tanh((((np.tanh((data["mean_abs_chgbatch_msignal"]))) + ((-((data["medianbatch_msignal"])))))/2.0)) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh((((((((data["signal_shift_+1_msignal"]) + (data["medianbatch_slices2"]))) * 2.0)) + (data["medianbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch"] > -998, ((data["abs_maxbatch_slices2_msignal"]) - (((((((((data["maxtominbatch_slices2_msignal"]) / 2.0)) * (((data["maxbatch_msignal"]) / 2.0)))) / 2.0)) / 2.0))), data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(((((data["maxbatch_slices2_msignal"]) - ((6.0)))) + (np.where((6.0) <= -998, (6.0), data["maxbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (np.where((((((data["abs_avgbatch_slices2"]) * 2.0)) + ((((data["abs_minbatch_msignal"]) + (((data["signal_shift_+1"]) * 2.0)))/2.0)))/2.0) <= -998, (-((data["signal_shift_-1_msignal"]))), data["abs_minbatch_msignal"] )))) +
                            0.100000*np.tanh(((((((data["meanbatch_slices2_msignal"]) + (((data["minbatch_msignal"]) * 2.0)))/2.0)) + (((np.where(((data["maxbatch_msignal"]) * 2.0) > -998, data["minbatch_msignal"], ((((data["minbatch_slices2_msignal"]) * 2.0)) + (data["maxbatch_slices2_msignal"])) )) * 2.0)))/2.0)) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) + (((((data["rangebatch_slices2_msignal"]) * (((data["meanbatch_msignal"]) * ((((-((data["maxbatch_msignal"])))) - (((data["maxbatch_msignal"]) * ((-((data["meanbatch_slices2_msignal"])))))))))))) * 2.0)))) +
                            0.100000*np.tanh((((((((data["mean_abs_chgbatch_slices2"]) / 2.0)) + (((data["maxbatch_msignal"]) * ((5.0)))))/2.0)) - (np.where(data["minbatch_slices2_msignal"] > -998, (8.0), data["mean_abs_chgbatch_msignal"] )))) +
                            0.100000*np.tanh(np.where((5.90521717071533203) > -998, ((data["rangebatch_msignal"]) - ((5.90521717071533203))), ((data["rangebatch_msignal"]) + (((data["maxbatch_slices2_msignal"]) * (((data["stdbatch_slices2"]) - (((data["maxbatch_slices2_msignal"]) * (data["abs_maxbatch_msignal"])))))))) )) +
                            0.100000*np.tanh(((((((data["rangebatch_slices2"]) - ((7.96194982528686523)))) * 2.0)) - ((7.96194982528686523)))) +
                            0.100000*np.tanh((-(((((7.02787208557128906)) + (data["minbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh((((-((np.where(data["stdbatch_slices2_msignal"] > -998, ((data["maxbatch_slices2_msignal"]) * 2.0), np.tanh((np.where((((data["minbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"]))/2.0) > -998, data["medianbatch_slices2"], data["meanbatch_slices2_msignal"] ))) ))))) * (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2_msignal"] > -998, data["maxbatch_msignal"], data["abs_minbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.where(np.where(data["abs_avgbatch_slices2"] > -998, data["mean_abs_chgbatch_msignal"], ((data["abs_maxbatch_slices2_msignal"]) * 2.0) ) > -998, ((data["minbatch_msignal"]) / 2.0), (((((data["minbatch_msignal"]) * 2.0)) + ((-((data["minbatch_msignal"])))))/2.0) )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * ((-((((((np.where((6.0) <= -998, (6.0), data["maxbatch_slices2_msignal"] )) + ((((-((data["abs_maxbatch_msignal"])))) / 2.0)))) * (data["abs_maxbatch_slices2"])))))))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) + ((-((np.tanh(((-(((-((data["mean_abs_chgbatch_slices2"])))))))))))))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_msignal"] <= -998, data["minbatch_msignal"], (-((data["medianbatch_msignal"]))) )) +
                            0.100000*np.tanh(((((-(((9.85576820373535156))))) + (((data["abs_maxbatch_msignal"]) * (data["abs_maxbatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh((-(((((data["minbatch_msignal"]) + (np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, np.where(data["minbatch_slices2_msignal"] > -998, (6.56804466247558594), data["minbatch_msignal"] ), data["abs_minbatch_slices2"] )))/2.0))))) +
                            0.100000*np.tanh(((data["stdbatch_slices2"]) - ((((8.11329078674316406)) + (np.where(data["stdbatch_slices2"] > -998, data["minbatch_slices2_msignal"], data["minbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(data["maxtominbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((np.where(data["medianbatch_msignal"] > -998, (((((data["meanbatch_slices2_msignal"]) + (data["abs_maxbatch_slices2_msignal"]))) + (data["meanbatch_slices2_msignal"]))/2.0), data["meanbatch_slices2_msignal"] )) * ((-((data["medianbatch_msignal"])))))) +
                            0.100000*np.tanh((((((data["maxtominbatch_slices2_msignal"]) + (((data["abs_maxbatch_msignal"]) * (data["meanbatch_slices2"]))))/2.0)) + (np.tanh((((data["abs_maxbatch_msignal"]) - (((data["medianbatch_msignal"]) / 2.0)))))))) +
                            0.100000*np.tanh((((data["maxtominbatch_slices2"]) + (((data["maxtominbatch_slices2"]) * ((-((data["medianbatch_msignal"])))))))/2.0)) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) + (np.where(((((data["meanbatch_slices2_msignal"]) - (((data["abs_minbatch_slices2_msignal"]) / 2.0)))) * (data["maxtominbatch"])) > -998, data["meanbatch_slices2_msignal"], ((((data["maxbatch_slices2_msignal"]) + (data["maxtominbatch"]))) * 2.0) )))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2"]) - (np.where(np.where(data["rangebatch_slices2"] > -998, (9.0), (9.0) ) > -998, (9.0), data["abs_maxbatch"] )))) - (np.where((9.0) > -998, (9.0), data["abs_maxbatch"] )))) +
                            0.100000*np.tanh(((np.tanh((np.tanh((data["maxbatch_msignal"]))))) - ((((7.92655563354492188)) - (data["rangebatch_msignal"]))))) +
                            0.100000*np.tanh(np.where((-(((((data["minbatch_msignal"]) + (data["minbatch_msignal"]))/2.0)))) <= -998, data["mean_abs_chgbatch_slices2_msignal"], (((((-((((((8.0)) + (data["minbatch_msignal"]))/2.0))))) * (data["maxbatch_msignal"]))) * 2.0) )) +
                            0.100000*np.tanh((-((((((data["abs_maxbatch"]) - (data["minbatch_slices2"]))) - (data["stdbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (data["abs_minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((-((((data["signal_shift_+1_msignal"]) - (((data["minbatch_slices2_msignal"]) / 2.0))))))) + (((data["rangebatch_msignal"]) + (data["maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] <= -998, data["meanbatch_msignal"], ((data["abs_minbatch_msignal"]) / 2.0) )) +
                            0.100000*np.tanh((((9.44000816345214844)) * (((data["mean_abs_chgbatch_slices2"]) * (((data["rangebatch_slices2"]) * (((data["abs_maxbatch_slices2"]) * (((data["mean_abs_chgbatch_slices2"]) + (np.tanh((data["minbatch_msignal"]))))))))))))) +
                            0.100000*np.tanh(np.tanh((((data["minbatch_slices2_msignal"]) * (((data["abs_avgbatch_slices2_msignal"]) + (((((data["maxbatch_slices2"]) * (data["signal"]))) + (np.tanh(((-((np.tanh((data["minbatch_slices2_msignal"])))))))))))))))) +
                            0.100000*np.tanh(((((data["stdbatch_slices2"]) + (data["medianbatch_msignal"]))) * (((data["abs_maxbatch"]) * ((((((((data["stdbatch_slices2"]) + (data["medianbatch_msignal"]))) + (data["abs_maxbatch_msignal"]))/2.0)) * (data["maxbatch_msignal"]))))))) +
                            0.100000*np.tanh((((np.where(((data["minbatch_slices2"]) + (data["medianbatch_msignal"])) <= -998, (0.0), data["maxbatch_slices2_msignal"] )) + (data["medianbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(data["minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((np.where(((data["minbatch"]) + (data["abs_maxbatch_slices2_msignal"])) <= -998, data["stdbatch_slices2_msignal"], data["meanbatch_slices2_msignal"] )) + (data["abs_maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) - (((np.where(((((data["maxbatch_slices2_msignal"]) / 2.0)) / 2.0) > -998, data["maxbatch_slices2_msignal"], ((np.tanh((data["maxbatch_slices2_msignal"]))) + (data["abs_minbatch_msignal"])) )) * (((data["abs_minbatch_msignal"]) / 2.0)))))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_msignal"] > -998, ((data["mean_abs_chgbatch_slices2_msignal"]) - (np.where(data["meanbatch_msignal"] > -998, data["rangebatch_slices2_msignal"], data["mean_abs_chgbatch_slices2_msignal"] ))), ((((data["abs_minbatch_msignal"]) / 2.0)) - (data["rangebatch_slices2"])) )) +
                            0.100000*np.tanh(((data["rangebatch_slices2_msignal"]) - ((-((np.where(((data["maxtominbatch_slices2"]) - ((9.10140609741210938))) <= -998, (9.10140609741210938), data["meanbatch_msignal"] ))))))) +
                            0.100000*np.tanh((((((((data["minbatch_msignal"]) + (data["minbatch_msignal"]))) + (data["maxtominbatch"]))/2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["rangebatch_msignal"]) + (np.where(np.tanh(((((data["rangebatch_msignal"]) + (data["rangebatch_msignal"]))/2.0))) > -998, data["maxtominbatch_slices2_msignal"], np.where(data["medianbatch_msignal"] <= -998, data["maxtominbatch_slices2_msignal"], data["minbatch_slices2"] ) )))) +
                            0.100000*np.tanh(((data["stdbatch_slices2_msignal"]) - ((((4.0)) - (np.where(data["stdbatch_slices2_msignal"] > -998, data["maxbatch_slices2"], (4.0) )))))) +
                            0.100000*np.tanh(np.tanh((data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) - (np.where(np.where(((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0) > -998, data["mean_abs_chgbatch_slices2"], data["abs_minbatch_slices2"] ) > -998, (10.0), data["maxbatch_slices2"] )))) +
                            0.100000*np.tanh(((((np.where(((data["stdbatch_slices2"]) + (data["stdbatch_slices2"])) <= -998, data["abs_maxbatch_msignal"], data["meanbatch_msignal"] )) + (data["stdbatch_slices2"]))) * (data["maxbatch_slices2"]))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * ((8.50926399230957031)))) - (((np.where(data["maxbatch_slices2_msignal"] <= -998, ((data["medianbatch_msignal"]) * (data["maxbatch_slices2_msignal"])), data["maxbatch_slices2_msignal"] )) * (((data["medianbatch_msignal"]) * (data["maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(np.tanh(((-(((-(((7.02199268341064453)))))))))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(data["stdbatch_msignal"]) +
                            0.100000*np.tanh((((-((data["meanbatch_msignal"])))) * (((((data["maxbatch_slices2_msignal"]) + (data["meanbatch_msignal"]))) * (np.where(((data["rangebatch_msignal"]) - (data["minbatch_msignal"])) > -998, data["maxbatch_slices2"], data["maxbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(np.tanh((data["signal_shift_-1_msignal"]))) +
                            0.100000*np.tanh(np.where((((data["maxtominbatch"]) + (data["abs_maxbatch"]))/2.0) <= -998, np.where(np.tanh((data["medianbatch_slices2_msignal"])) > -998, data["maxtominbatch"], data["meanbatch_msignal"] ), (((data["signal"]) + (data["maxtominbatch"]))/2.0) )) +
                            0.100000*np.tanh(((np.where(data["medianbatch_msignal"] > -998, data["abs_avgbatch_msignal"], data["medianbatch_msignal"] )) - (((data["rangebatch_msignal"]) * (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) - (((((((((np.tanh((data["mean_abs_chgbatch_slices2"]))) - ((((9.03389644622802734)) - (np.tanh((data["minbatch"]))))))) / 2.0)) / 2.0)) - (data["abs_minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) + (data["maxbatch_slices2_msignal"]))) + (((data["maxbatch_slices2_msignal"]) * (((((((((data["meanbatch_msignal"]) + (((data["maxbatch_slices2_msignal"]) / 2.0)))/2.0)) + (((data["maxbatch_slices2_msignal"]) / 2.0)))/2.0)) * 2.0)))))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - (np.where(data["medianbatch_slices2_msignal"] <= -998, (14.71962356567382812), np.where(((data["maxbatch_msignal"]) - (data["signal_shift_-1"])) <= -998, data["maxtominbatch_slices2_msignal"], ((data["meanbatch_msignal"]) * (data["meanbatch_msignal"])) ) )))) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] > -998, data["abs_minbatch_msignal"], data["abs_minbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.tanh((np.tanh((((np.where(((np.tanh((data["meanbatch_msignal"]))) * 2.0) > -998, data["medianbatch_msignal"], data["abs_minbatch_slices2"] )) + (data["maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2"]) / 2.0)) / 2.0)) +
                            0.100000*np.tanh((-((np.where(((((data["signal_shift_-1_msignal"]) * 2.0)) + (data["signal_shift_+1_msignal"])) <= -998, ((np.tanh((data["rangebatch_msignal"]))) + (data["medianbatch_msignal"])), ((data["medianbatch_msignal"]) / 2.0) ))))) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] > -998, (((-(((((7.34612560272216797)) + (data["minbatch_msignal"])))))) * 2.0), (((7.34612560272216797)) + ((7.34612560272216797))) )) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(data["minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.tanh((((data["maxtominbatch_slices2_msignal"]) + (data["rangebatch_msignal"]))))) +
                            0.100000*np.tanh(data["abs_avgbatch_msignal"]) +
                            0.100000*np.tanh(data["maxtominbatch_msignal"]) +
                            0.100000*np.tanh(np.where(((data["medianbatch_msignal"]) * 2.0) <= -998, np.where(data["abs_minbatch_slices2"] <= -998, (-((data["medianbatch_slices2_msignal"]))), ((data["medianbatch_msignal"]) * 2.0) ), (-((data["medianbatch_msignal"]))) )) +
                            0.100000*np.tanh(np.where((((data["abs_maxbatch"]) + (((data["abs_maxbatch"]) - (((data["minbatch"]) + (data["signal_shift_+1_msignal"]))))))/2.0) <= -998, np.tanh((data["minbatch_msignal"])), data["signal_shift_+1_msignal"] )) +
                            0.100000*np.tanh((((((data["stdbatch_slices2"]) + (data["medianbatch_msignal"]))/2.0)) * (((((data["medianbatch_msignal"]) * (((((data["stdbatch_slices2_msignal"]) * 2.0)) * (data["abs_maxbatch_slices2"]))))) + (((data["signal_shift_-1"]) * ((1.74672639369964600)))))))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (np.where(np.where(((data["rangebatch_slices2_msignal"]) * 2.0) <= -998, (-((np.where((0.0) <= -998, data["maxbatch_msignal"], (9.48639965057373047) )))), (9.48639965057373047) ) <= -998, data["rangebatch_slices2"], (9.48639965057373047) )))) +
                            0.100000*np.tanh(np.where((((-((data["mean_abs_chgbatch_slices2"])))) * 2.0) > -998, np.where(((data["maxbatch_slices2_msignal"]) * (((((data["signal_shift_-1_msignal"]) * 2.0)) / 2.0))) > -998, data["minbatch_msignal"], data["minbatch_slices2_msignal"] ), data["medianbatch_msignal"] )) +
                            0.100000*np.tanh((-((np.tanh((((np.tanh((np.tanh((data["signal"]))))) / 2.0))))))) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2"]) - ((7.0)))) * 2.0)) +
                            0.100000*np.tanh(((np.where(data["meanbatch_slices2"] <= -998, data["signal_shift_-1_msignal"], data["minbatch_slices2_msignal"] )) * 2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) - ((((data["mean_abs_chgbatch_slices2_msignal"]) + (np.where(data["abs_avgbatch_slices2"] > -998, data["medianbatch_slices2"], np.tanh((data["maxbatch_msignal"])) )))/2.0)))) +
                            0.100000*np.tanh(np.tanh((np.where(((np.tanh((((data["minbatch_msignal"]) / 2.0)))) * 2.0) > -998, data["signal_shift_-1_msignal"], data["signal_shift_-1_msignal"] )))) +
                            0.100000*np.tanh((((((data["medianbatch_slices2_msignal"]) + (data["maxbatch_msignal"]))/2.0)) + (data["signal_shift_-1_msignal"]))) +
                            0.100000*np.tanh(np.tanh((((data["mean_abs_chgbatch_slices2_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(((np.where(data["maxbatch_slices2_msignal"] <= -998, data["signal_shift_-1_msignal"], ((data["medianbatch_msignal"]) + (data["maxbatch_slices2_msignal"])) )) + (data["maxtominbatch"]))) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2"] > -998, (((((6.03964948654174805)) - (((data["abs_maxbatch_msignal"]) * 2.0)))) * (data["minbatch_msignal"])), (6.03964948654174805) )) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] > -998, np.where(data["abs_minbatch_slices2"] <= -998, ((((((data["mean_abs_chgbatch_msignal"]) / 2.0)) * 2.0)) * 2.0), data["abs_minbatch_slices2"] ), data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(data["stdbatch_msignal"]) +
                            0.100000*np.tanh(((((1.0)) + (((data["maxtominbatch"]) + (data["maxtominbatch"]))))/2.0)) +
                            0.100000*np.tanh((((2.56278347969055176)) * (((((data["maxbatch_slices2_msignal"]) - ((2.56278347969055176)))) * ((((((data["abs_maxbatch_msignal"]) + (data["maxbatch_slices2"]))) + (data["abs_maxbatch_msignal"]))/2.0)))))) +
                            0.100000*np.tanh(((np.where(data["stdbatch_slices2_msignal"] > -998, data["meanbatch_slices2_msignal"], ((((data["signal_shift_-1_msignal"]) - (np.where((1.63965260982513428) > -998, ((data["medianbatch_slices2"]) / 2.0), data["medianbatch_msignal"] )))) / 2.0) )) - (data["maxtominbatch"]))) +
                            0.100000*np.tanh(data["rangebatch_slices2"]) +
                            0.100000*np.tanh(data["maxtominbatch_slices2_msignal"]) +
                            0.100000*np.tanh((-((data["abs_minbatch_slices2_msignal"])))) +
                            0.100000*np.tanh(np.where((((((data["abs_minbatch_slices2_msignal"]) + (data["minbatch_msignal"]))/2.0)) * 2.0) <= -998, np.where(data["stdbatch_slices2_msignal"] <= -998, data["minbatch_msignal"], data["abs_minbatch_slices2_msignal"] ), np.where(data["stdbatch_slices2_msignal"] <= -998, data["abs_minbatch_slices2_msignal"], data["mean_abs_chgbatch_msignal"] ) )) +
                            0.100000*np.tanh((((data["mean_abs_chgbatch_msignal"]) + (((data["minbatch"]) * (np.where(data["maxtominbatch_slices2_msignal"] <= -998, data["maxtominbatch_slices2_msignal"], ((data["minbatch"]) * 2.0) )))))/2.0)) +
                            0.100000*np.tanh(data["maxtominbatch_slices2"]) +
                            0.100000*np.tanh(((((((np.tanh(((-((data["abs_maxbatch_slices2_msignal"])))))) / 2.0)) + (np.tanh(((-((data["maxtominbatch_slices2_msignal"])))))))) / 2.0)) +
                            0.100000*np.tanh((((data["abs_avgbatch_msignal"]) + (np.where((((np.tanh((data["medianbatch_msignal"]))) + (data["rangebatch_slices2_msignal"]))/2.0) <= -998, data["medianbatch_slices2"], data["maxbatch_msignal"] )))/2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) * ((-((((((4.0)) + ((((data["stdbatch_msignal"]) + (((data["maxbatch_slices2"]) * (((data["minbatch_slices2"]) / 2.0)))))/2.0)))/2.0))))))) +
                            0.100000*np.tanh(((np.where(data["stdbatch_msignal"] > -998, np.where(((data["signal_shift_+1_msignal"]) + (data["minbatch_slices2"])) > -998, data["signal_shift_+1_msignal"], data["signal_shift_+1_msignal"] ), data["minbatch_slices2"] )) + (data["minbatch_slices2"]))) +
                            0.100000*np.tanh(data["maxtominbatch_slices2"]) +
                            0.100000*np.tanh(((np.where(((data["abs_avgbatch_slices2_msignal"]) + (((data["abs_maxbatch_slices2_msignal"]) + (np.tanh((data["mean_abs_chgbatch_slices2"])))))) <= -998, data["abs_maxbatch_slices2_msignal"], ((data["abs_maxbatch_slices2_msignal"]) + (data["medianbatch_msignal"])) )) * 2.0)) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - (((((-((((data["abs_maxbatch_msignal"]) - (((data["rangebatch_slices2"]) + (((((data["meanbatch_msignal"]) / 2.0)) * 2.0))))))))) + (np.tanh((data["abs_minbatch_slices2"]))))/2.0)))) +
                            0.100000*np.tanh((((7.69423294067382812)) * (np.where(data["abs_minbatch_slices2"] <= -998, np.tanh((data["minbatch_msignal"])), (-((((((7.69423294067382812)) + (data["minbatch_msignal"]))/2.0)))) )))) +
                            0.100000*np.tanh(((np.tanh(((-((np.tanh((((((data["minbatch_slices2"]) / 2.0)) * (((data["abs_maxbatch_slices2_msignal"]) * 2.0))))))))))) / 2.0)) +
                            0.100000*np.tanh((((-((((data["maxtominbatch"]) - (np.where(((data["maxtominbatch"]) / 2.0) <= -998, ((data["meanbatch_slices2"]) / 2.0), data["mean_abs_chgbatch_slices2_msignal"] ))))))) * (data["maxtominbatch"]))) +
                            0.100000*np.tanh(((np.where(data["minbatch_slices2_msignal"] > -998, data["minbatch_msignal"], np.where(np.tanh(((6.0))) <= -998, (((6.0)) + ((6.0))), (6.0) ) )) * ((((data["stdbatch_slices2_msignal"]) + ((6.0)))/2.0)))) +
                            0.100000*np.tanh(((((data["maxbatch_msignal"]) + (data["medianbatch_msignal"]))) + (np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], np.where(data["medianbatch_msignal"] <= -998, ((data["maxbatch_msignal"]) / 2.0), data["maxbatch_msignal"] ) )))) +
                            0.100000*np.tanh((4.0)) +
                            0.100000*np.tanh(((np.where((-(((((-((data["signal_shift_-1_msignal"])))) / 2.0)))) > -998, data["maxtominbatch"], data["signal_shift_-1_msignal"] )) + (data["signal"]))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) + (((data["abs_avgbatch_msignal"]) * (np.tanh((data["signal_shift_+1_msignal"]))))))) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) + (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(data["abs_maxbatch_msignal"]) +
                            0.100000*np.tanh(((((((np.where(((data["abs_minbatch_slices2"]) / 2.0) > -998, data["abs_avgbatch_msignal"], data["abs_minbatch_slices2"] )) / 2.0)) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(((((((data["abs_maxbatch_slices2_msignal"]) * (((data["maxbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"]))))) * (data["abs_minbatch_slices2"]))) / 2.0)) +
                            0.100000*np.tanh(((((((((data["maxtominbatch_slices2_msignal"]) + (np.tanh((data["signal_shift_+1_msignal"]))))/2.0)) + (data["abs_maxbatch_msignal"]))) + (((data["abs_avgbatch_slices2_msignal"]) / 2.0)))/2.0)) +
                            0.100000*np.tanh(data["maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) + (((np.where(data["abs_avgbatch_msignal"] > -998, data["signal_shift_-1_msignal"], data["mean_abs_chgbatch_slices2"] )) + (((data["meanbatch_slices2_msignal"]) / 2.0)))))) +
                            0.100000*np.tanh(np.where(((data["maxbatch_slices2_msignal"]) + (((((((((data["maxbatch_slices2_msignal"]) / 2.0)) + (data["maxbatch_msignal"]))/2.0)) + (data["abs_maxbatch"]))/2.0))) <= -998, data["minbatch"], (((data["maxbatch_slices2_msignal"]) + (data["minbatch_slices2"]))/2.0) )) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2_msignal"]) * (np.tanh((data["minbatch_slices2"]))))) / 2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((((np.tanh((data["maxtominbatch"]))) * 2.0)))))) +
                            0.100000*np.tanh(np.tanh((((data["maxtominbatch_slices2"]) / 2.0)))) +
                            0.100000*np.tanh(((((data["abs_avgbatch_msignal"]) * ((-((data["abs_avgbatch_msignal"])))))) / 2.0)) +
                            0.100000*np.tanh(np.where(((data["minbatch_msignal"]) - (np.tanh((data["abs_avgbatch_slices2"])))) <= -998, ((((data["medianbatch_slices2"]) * 2.0)) + (data["meanbatch_msignal"])), ((data["abs_maxbatch"]) / 2.0) )) +
                            0.100000*np.tanh(data["abs_maxbatch"]) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((np.tanh((((data["maxtominbatch_slices2_msignal"]) * ((-(((((data["signal_shift_+1_msignal"]) + (((data["maxbatch_slices2_msignal"]) / 2.0)))/2.0))))))))) * (data["signal_shift_+1_msignal"]))) +
                            0.100000*np.tanh(((data["stdbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(((((data["maxtominbatch"]) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.where(data["meanbatch_msignal"] <= -998, ((((data["signal_shift_-1_msignal"]) * (((((np.tanh((data["abs_avgbatch_msignal"]))) / 2.0)) / 2.0)))) / 2.0), ((data["maxtominbatch"]) * (((data["abs_avgbatch_msignal"]) - (data["medianbatch_msignal"])))) )) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] <= -998, ((data["maxbatch_msignal"]) + (((((((7.0)) + (data["maxbatch_slices2_msignal"]))) + (data["stdbatch_slices2"]))/2.0))), ((data["maxbatch_slices2_msignal"]) + (data["meanbatch_msignal"])) )) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh(data["abs_avgbatch_msignal"]) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) / 2.0)) * (data["signal_shift_+1_msignal"]))) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) - (((((data["abs_maxbatch_slices2_msignal"]) * (data["abs_maxbatch_slices2"]))) * (np.tanh((np.where(((data["minbatch_msignal"]) + (data["maxtominbatch_slices2_msignal"])) > -998, data["abs_minbatch_msignal"], np.tanh((data["abs_maxbatch_msignal"])) )))))))) +
                            0.100000*np.tanh(np.tanh((np.where(data["signal"] <= -998, np.tanh((np.where(data["signal_shift_-1_msignal"] <= -998, data["signal_shift_+1_msignal"], ((data["stdbatch_slices2_msignal"]) * 2.0) ))), data["stdbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2"]) * 2.0)) +
                            0.100000*np.tanh(np.where((0.0) > -998, np.where(data["abs_maxbatch_slices2_msignal"] > -998, np.tanh((((data["abs_minbatch_slices2"]) + (data["abs_minbatch_slices2"])))), data["abs_minbatch_slices2"] ), data["mean_abs_chgbatch_slices2"] )) +
                            0.100000*np.tanh(((np.tanh((((data["abs_minbatch_slices2_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))))) / 2.0)) +
                            0.100000*np.tanh(((np.where(data["signal_shift_-1_msignal"] <= -998, data["signal_shift_+1_msignal"], ((data["meanbatch_msignal"]) + (data["signal_shift_+1_msignal"])) )) * 2.0)) +
                            0.100000*np.tanh(((((data["abs_maxbatch_msignal"]) - (np.tanh(((((data["abs_maxbatch"]) + (((data["abs_maxbatch_msignal"]) / 2.0)))/2.0)))))) - ((2.0)))) +
                            0.100000*np.tanh(np.where(((data["abs_maxbatch_slices2_msignal"]) + (data["maxbatch_slices2_msignal"])) > -998, ((data["maxbatch_slices2_msignal"]) + (data["abs_avgbatch_slices2_msignal"])), data["medianbatch_slices2"] )) +
                            0.100000*np.tanh((((((np.tanh((data["minbatch_slices2"]))) * 2.0)) + (data["signal_shift_-1_msignal"]))/2.0)) +
                            0.100000*np.tanh(data["abs_minbatch_msignal"]) +
                            0.100000*np.tanh(((data["stdbatch_slices2_msignal"]) * (np.where(data["abs_maxbatch_msignal"] <= -998, data["signal"], np.tanh((((((data["stdbatch_slices2_msignal"]) - (((data["maxtominbatch_slices2"]) + (data["medianbatch_slices2"]))))) / 2.0))) )))) +
                            0.100000*np.tanh(np.tanh((((((((((((((((data["stdbatch_slices2"]) / 2.0)) / 2.0)) / 2.0)) / 2.0)) / 2.0)) / 2.0)) / 2.0)))) +
                            0.100000*np.tanh(np.tanh((np.tanh((((np.where(data["abs_minbatch_slices2"] > -998, data["maxbatch_slices2_msignal"], data["abs_minbatch_slices2"] )) + (data["medianbatch_msignal"]))))))) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) * (((data["rangebatch_slices2"]) * (data["abs_avgbatch_msignal"]))))) +
                            0.100000*np.tanh((((((data["maxbatch_msignal"]) + (data["maxtominbatch_msignal"]))/2.0)) + (data["maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.tanh((np.tanh((data["meanbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((data["medianbatch_msignal"]) + (data["maxbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(((np.tanh((data["mean_abs_chgbatch_slices2"]))) + (np.tanh((((data["meanbatch_slices2_msignal"]) + (data["maxbatch_msignal"]))))))) +
                            0.100000*np.tanh(np.where(((data["meanbatch_slices2_msignal"]) / 2.0) <= -998, ((data["maxbatch_slices2_msignal"]) / 2.0), ((np.tanh((data["abs_minbatch_slices2"]))) / 2.0) )) +
                            0.100000*np.tanh(np.tanh((data["abs_avgbatch_slices2"]))) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2_msignal"]) + (((np.where(data["abs_maxbatch_slices2_msignal"] <= -998, ((((data["rangebatch_slices2_msignal"]) / 2.0)) * (((data["abs_maxbatch_msignal"]) * (((data["rangebatch_slices2_msignal"]) * 2.0))))), data["meanbatch_msignal"] )) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.tanh((np.tanh((((data["medianbatch_msignal"]) + (np.where(np.tanh((data["maxbatch_slices2_msignal"])) > -998, data["signal_shift_+1"], np.where(data["mean_abs_chgbatch_slices2"] <= -998, (8.77771377563476562), data["abs_maxbatch"] ) )))))))) +
                            0.100000*np.tanh(np.tanh((data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(((data["signal_shift_-1_msignal"]) * (data["abs_minbatch_slices2"])) <= -998, data["signal_shift_-1_msignal"], data["abs_minbatch_slices2"] )) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh((-((np.tanh((((data["signal_shift_-1_msignal"]) / 2.0))))))) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh(np.where((-((data["medianbatch_slices2"]))) > -998, data["stdbatch_slices2_msignal"], data["minbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.where(((((np.where(data["abs_minbatch_slices2"] > -998, data["rangebatch_msignal"], data["maxbatch_slices2"] )) * 2.0)) / 2.0) > -998, data["rangebatch_slices2_msignal"], data["mean_abs_chgbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((np.where(data["meanbatch_slices2_msignal"] <= -998, (-((data["maxtominbatch"]))), ((data["maxtominbatch"]) - (data["signal_shift_+1_msignal"])) )) - (data["maxtominbatch"]))) +
                            0.100000*np.tanh(data["maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((((((np.where((((data["signal_shift_+1_msignal"]) + (((data["signal_shift_+1_msignal"]) / 2.0)))/2.0) > -998, (0.0), data["signal_shift_+1_msignal"] )) / 2.0)) / 2.0)) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.where(np.tanh((data["signal_shift_+1_msignal"])) <= -998, ((np.tanh(((-((data["signal_shift_+1_msignal"])))))) / 2.0), ((np.tanh((data["signal_shift_+1_msignal"]))) / 2.0) )) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) - (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2_msignal"] <= -998, (((data["rangebatch_msignal"]) + (np.where(data["minbatch_slices2_msignal"] > -998, data["meanbatch_slices2_msignal"], data["rangebatch_slices2_msignal"] )))/2.0), data["stdbatch_slices2"] )) +
                            0.100000*np.tanh(np.tanh((np.tanh(((((((((np.tanh(((((((((data["minbatch_slices2_msignal"]) + ((-((data["abs_avgbatch_slices2"])))))/2.0)) / 2.0)) / 2.0)))) * 2.0)) / 2.0)) + (np.tanh((data["signal_shift_-1_msignal"]))))/2.0)))))) +
                            0.100000*np.tanh((3.0)) +
                            0.100000*np.tanh(np.tanh((data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where((0.0) > -998, data["signal_shift_+1_msignal"], data["signal_shift_+1_msignal"] )) +
                            0.100000*np.tanh(((((((((((((data["medianbatch_slices2_msignal"]) / 2.0)) / 2.0)) / 2.0)) / 2.0)) / 2.0)) / 2.0)) +
                            0.100000*np.tanh((((data["stdbatch_slices2"]) + ((((data["rangebatch_msignal"]) + (np.where(((data["minbatch_slices2_msignal"]) - (np.tanh((data["maxbatch_slices2_msignal"])))) > -998, data["abs_avgbatch_slices2_msignal"], data["rangebatch_msignal"] )))/2.0)))/2.0)) +
                            0.100000*np.tanh(np.where(((data["abs_avgbatch_msignal"]) * 2.0) <= -998, data["stdbatch_slices2_msignal"], np.where(np.where(data["abs_maxbatch_msignal"] <= -998, data["meanbatch_slices2_msignal"], data["minbatch_slices2_msignal"] ) <= -998, data["meanbatch_slices2_msignal"], data["meanbatch_slices2_msignal"] ) )) +
                            0.100000*np.tanh(np.tanh((((((-((np.tanh((data["abs_minbatch_slices2"])))))) + (((data["meanbatch_slices2_msignal"]) / 2.0)))/2.0)))))  
    
    def GP_class_9(self,data):
        return self.Output( -3.605458 +
                            0.100000*np.tanh(((np.tanh(((-((data["maxbatch_slices2_msignal"])))))) - (np.where(data["signal"] > -998, data["abs_avgbatch_slices2_msignal"], (-((data["maxbatch_slices2"]))) )))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh((((((data["signal_shift_-1"]) + (data["meanbatch_slices2"]))/2.0)) * 2.0)) +
                            0.100000*np.tanh((-((data["abs_avgbatch_slices2_msignal"])))) +
                            0.100000*np.tanh(np.where(((data["medianbatch_slices2"]) + (((data["signal_shift_+1"]) + (data["signal_shift_-1"])))) <= -998, ((data["maxbatch_slices2"]) + (data["rangebatch_msignal"])), data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2"]) + (np.tanh((data["signal"]))))) +
                            0.100000*np.tanh(((((((-((((((data["abs_minbatch_slices2_msignal"]) + (data["abs_minbatch_msignal"]))) - (data["rangebatch_slices2_msignal"])))))) + (data["medianbatch_slices2_msignal"]))/2.0)) - (data["rangebatch_slices2_msignal"]))) +
                            0.100000*np.tanh((-((data["abs_avgbatch_msignal"])))) +
                            0.100000*np.tanh(((np.tanh(((((5.0)) + (data["abs_avgbatch_slices2_msignal"]))))) + (np.where(((data["abs_avgbatch_slices2_msignal"]) + (data["maxtominbatch_slices2"])) > -998, data["signal_shift_+1"], data["minbatch_msignal"] )))) +
                            0.100000*np.tanh((-((np.where(data["abs_maxbatch"] > -998, data["abs_avgbatch_msignal"], (-(((-((data["maxtominbatch_slices2_msignal"])))))) ))))) +
                            0.100000*np.tanh((-((((data["abs_minbatch_msignal"]) * 2.0))))) +
                            0.100000*np.tanh((-((((data["medianbatch_msignal"]) + (np.where(((((data["signal_shift_-1_msignal"]) / 2.0)) + ((-((data["mean_abs_chgbatch_slices2_msignal"]))))) > -998, data["abs_avgbatch_msignal"], data["signal_shift_-1"] ))))))) +
                            0.100000*np.tanh(np.where((0.0) <= -998, (-((data["signal"]))), data["medianbatch_slices2"] )) +
                            0.100000*np.tanh((-((data["abs_avgbatch_msignal"])))) +
                            0.100000*np.tanh((-((((np.where(data["signal_shift_-1_msignal"] <= -998, (((-((data["signal_shift_+1_msignal"])))) * 2.0), data["mean_abs_chgbatch_msignal"] )) * 2.0))))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where((-((data["minbatch_slices2_msignal"]))) > -998, ((data["medianbatch_msignal"]) * (((data["medianbatch_msignal"]) * 2.0))), (-((data["rangebatch_slices2"]))) )))) +
                            0.100000*np.tanh((-((np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, data["medianbatch_msignal"], np.where(data["stdbatch_slices2"] > -998, ((data["stdbatch_slices2"]) / 2.0), (((data["minbatch_slices2"]) + (np.tanh((((data["signal"]) + (data["rangebatch_msignal"]))))))/2.0) ) ))))) +
                            0.100000*np.tanh(((((((data["meanbatch_msignal"]) - (data["meanbatch_msignal"]))) * (data["medianbatch_slices2_msignal"]))) - (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2_msignal"]) * (np.where(((data["stdbatch_slices2_msignal"]) + (((data["abs_avgbatch_slices2"]) * 2.0))) > -998, data["meanbatch_slices2_msignal"], data["stdbatch_slices2_msignal"] )))) - (((data["abs_avgbatch_slices2"]) * 2.0)))) +
                            0.100000*np.tanh((((-((data["signal_shift_-1"])))) - (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((-((data["medianbatch_slices2_msignal"])))) +
                            0.100000*np.tanh((((((((data["abs_minbatch_slices2_msignal"]) * (((data["abs_avgbatch_slices2_msignal"]) * (data["signal"]))))) + (((data["medianbatch_msignal"]) * 2.0)))/2.0)) - (((data["signal"]) * (data["medianbatch_slices2"]))))) +
                            0.100000*np.tanh((((-((np.where(data["signal"] <= -998, data["abs_avgbatch_msignal"], data["abs_avgbatch_slices2_msignal"] ))))) - (data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh((((-((((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0))))) - ((-((data["mean_abs_chgbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) - (data["abs_minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((data["medianbatch_msignal"]) + ((-((((data["abs_avgbatch_slices2_msignal"]) - ((((-((data["minbatch"])))) * 2.0))))))))/2.0)) +
                            0.100000*np.tanh((-((np.where((6.0) > -998, (((6.0)) - (((data["meanbatch_msignal"]) * (data["abs_minbatch_msignal"])))), (((data["abs_minbatch_msignal"]) + (data["abs_minbatch_msignal"]))/2.0) ))))) +
                            0.100000*np.tanh((((-((np.where(data["minbatch_slices2_msignal"] > -998, data["medianbatch_msignal"], ((data["abs_maxbatch_slices2_msignal"]) * (data["minbatch_slices2_msignal"])) ))))) + (np.tanh((data["minbatch_msignal"]))))) +
                            0.100000*np.tanh((-((((((((((9.0)) + (np.where(((np.tanh((np.tanh(((9.0)))))) / 2.0) <= -998, (((9.0)) - (data["minbatch_msignal"])), data["minbatch_msignal"] )))/2.0)) * 2.0)) * 2.0))))) +
                            0.100000*np.tanh(((data["signal"]) - (np.where(data["abs_maxbatch_slices2"] <= -998, np.where(data["signal"] <= -998, data["signal"], data["abs_maxbatch_slices2"] ), data["abs_maxbatch_slices2"] )))) +
                            0.100000*np.tanh((((data["maxtominbatch"]) + (np.where(data["mean_abs_chgbatch_msignal"] <= -998, data["meanbatch_slices2_msignal"], (((data["signal"]) + (((data["medianbatch_slices2"]) - (((data["medianbatch_slices2_msignal"]) * (data["rangebatch_slices2_msignal"]))))))/2.0) )))/2.0)) +
                            0.100000*np.tanh((-((((np.where(data["mean_abs_chgbatch_msignal"] <= -998, data["abs_avgbatch_slices2_msignal"], data["medianbatch_msignal"] )) + (((data["abs_minbatch_slices2"]) + ((((data["abs_avgbatch_slices2_msignal"]) + (((data["stdbatch_slices2_msignal"]) / 2.0)))/2.0))))))))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(((np.tanh((data["abs_minbatch_slices2_msignal"]))) * 2.0)) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) + (((((-((data["medianbatch_msignal"])))) + (((data["medianbatch_msignal"]) * (data["minbatch_slices2_msignal"]))))/2.0)))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) - (((data["medianbatch_msignal"]) * (((((data["mean_abs_chgbatch_msignal"]) - (data["medianbatch_msignal"]))) * (data["medianbatch_msignal"]))))))) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) + (((data["stdbatch_slices2_msignal"]) * (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh((((data["abs_minbatch_msignal"]) + (np.where(((data["signal_shift_+1"]) * 2.0) <= -998, data["abs_minbatch_slices2_msignal"], data["maxtominbatch_slices2_msignal"] )))/2.0)) +
                            0.100000*np.tanh((-(((((((np.tanh((((((data["signal_shift_+1_msignal"]) + ((12.48767375946044922)))) * 2.0)))) * 2.0)) + (np.tanh((data["signal_shift_+1_msignal"]))))/2.0))))) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) * (np.where((1.76193284988403320) <= -998, ((((data["abs_avgbatch_msignal"]) / 2.0)) * ((1.76193284988403320))), (((1.76193284988403320)) + (data["medianbatch_msignal"])) )))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) / 2.0)) - (((data["signal_shift_+1"]) - (((data["medianbatch_slices2_msignal"]) * (data["mean_abs_chgbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((np.where(data["minbatch_slices2_msignal"] <= -998, (((-(((-((data["minbatch_msignal"]))))))) * 2.0), (((((-((data["minbatch_msignal"])))) + ((-(((9.0))))))) * 2.0) )) * 2.0)) +
                            0.100000*np.tanh((-((((((((4.88298034667968750)) * (data["stdbatch_msignal"]))) + (np.where((4.88298034667968750) > -998, np.tanh((data["meanbatch_msignal"])), ((data["abs_maxbatch_msignal"]) * 2.0) )))/2.0))))) +
                            0.100000*np.tanh(np.tanh((data["maxtominbatch"]))) +
                            0.100000*np.tanh((-((np.where((((-((data["minbatch_msignal"])))) - (((data["rangebatch_slices2_msignal"]) * 2.0))) > -998, ((data["minbatch_slices2_msignal"]) + ((7.19959831237792969))), ((((data["medianbatch_msignal"]) * (data["rangebatch_slices2_msignal"]))) / 2.0) ))))) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(data["abs_maxbatch_slices2"]) +
                            0.100000*np.tanh((((-(((5.0))))) * (np.where((((-((data["maxtominbatch"])))) + (data["abs_minbatch_slices2"])) <= -998, ((data["signal_shift_+1"]) / 2.0), data["medianbatch_msignal"] )))) +
                            0.100000*np.tanh(data["stdbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2"]) - (((data["rangebatch_slices2_msignal"]) * (data["abs_avgbatch_msignal"]))))) +
                            0.100000*np.tanh((-((np.tanh((((data["abs_avgbatch_slices2"]) - (((data["abs_maxbatch"]) + ((-((np.where(data["maxbatch_slices2_msignal"] > -998, data["maxbatch_msignal"], data["mean_abs_chgbatch_slices2_msignal"] )))))))))))))) +
                            0.100000*np.tanh((((((((3.0)) / 2.0)) + (data["medianbatch_msignal"]))) * (np.where(data["rangebatch_msignal"] <= -998, ((np.where(data["stdbatch_slices2"] <= -998, data["maxbatch_slices2_msignal"], (4.83874177932739258) )) - ((3.0))), data["minbatch_msignal"] )))) +
                            0.100000*np.tanh(((((((data["mean_abs_chgbatch_msignal"]) + (data["abs_minbatch_slices2_msignal"]))) * 2.0)) * (((data["maxbatch_slices2_msignal"]) * 2.0)))) +
                            0.100000*np.tanh((((-((((data["abs_maxbatch_slices2_msignal"]) * ((((((data["minbatch_msignal"]) + (data["abs_maxbatch_slices2_msignal"]))/2.0)) * 2.0))))))) - ((10.0)))) +
                            0.100000*np.tanh(np.tanh((data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2_msignal"] <= -998, data["abs_minbatch_slices2_msignal"], ((data["abs_minbatch_slices2_msignal"]) - (data["abs_avgbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) - ((((-(((((-((data["maxbatch_slices2_msignal"])))) - (((data["maxbatch_slices2_msignal"]) * (data["abs_avgbatch_msignal"])))))))) * (data["rangebatch_msignal"]))))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (np.where(data["rangebatch_slices2"] <= -998, ((data["medianbatch_slices2"]) - (np.where(data["rangebatch_slices2"] <= -998, data["minbatch_slices2"], (10.0) ))), (10.0) )))) +
                            0.100000*np.tanh(np.where(np.where(np.tanh((data["abs_maxbatch_slices2_msignal"])) <= -998, ((data["minbatch_slices2"]) * 2.0), data["signal_shift_+1_msignal"] ) <= -998, np.where(data["maxbatch_slices2_msignal"] <= -998, data["signal_shift_-1"], (6.27133131027221680) ), data["abs_minbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) - (((data["mean_abs_chgbatch_slices2_msignal"]) - (data["abs_maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.tanh((np.tanh(((-(((-((np.where(((((data["medianbatch_msignal"]) / 2.0)) / 2.0) <= -998, np.tanh((np.tanh((data["meanbatch_msignal"])))), ((data["rangebatch_msignal"]) + (data["meanbatch_msignal"])) )))))))))))) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) + (np.tanh(((-((data["signal"])))))))) +
                            0.100000*np.tanh(((((data["minbatch_slices2_msignal"]) * 2.0)) / 2.0)) +
                            0.100000*np.tanh((-((data["maxtominbatch"])))) +
                            0.100000*np.tanh(data["minbatch_slices2"]) +
                            0.100000*np.tanh(((((-((((data["minbatch_slices2_msignal"]) * (data["minbatch_slices2"])))))) + (data["maxtominbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh((-((((((np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], data["stdbatch_slices2"] )) * (np.where(data["signal_shift_-1"] > -998, (((data["medianbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"]))/2.0), data["signal"] )))) + (data["abs_avgbatch_slices2"])))))) +
                            0.100000*np.tanh(((((np.where((1.0) <= -998, np.tanh((np.where(data["rangebatch_slices2_msignal"] <= -998, data["maxbatch_msignal"], ((data["maxbatch_slices2_msignal"]) / 2.0) ))), data["abs_maxbatch_msignal"] )) * 2.0)) + ((((-((data["signal_shift_-1"])))) / 2.0)))) +
                            0.100000*np.tanh((((data["stdbatch_slices2_msignal"]) + ((-(((((data["stdbatch_slices2"]) + (np.where(data["signal_shift_+1_msignal"] <= -998, data["rangebatch_msignal"], ((np.where(data["rangebatch_msignal"] > -998, data["abs_maxbatch_slices2_msignal"], ((data["mean_abs_chgbatch_msignal"]) / 2.0) )) / 2.0) )))/2.0))))))/2.0)) +
                            0.100000*np.tanh(((((np.where(data["signal_shift_-1_msignal"] <= -998, (10.98400974273681641), ((data["abs_maxbatch_slices2_msignal"]) - (data["stdbatch_slices2"])) )) * (((data["rangebatch_msignal"]) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((((((data["signal_shift_-1_msignal"]) / 2.0)) * (data["abs_minbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((data["maxtominbatch"]) - (np.where(data["abs_avgbatch_slices2"] > -998, data["mean_abs_chgbatch_msignal"], (-((np.where(data["maxbatch_msignal"] > -998, data["maxtominbatch_msignal"], data["medianbatch_slices2"] )))) )))) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] <= -998, ((data["maxbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"])), data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) * (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) + (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(((((1.50520956516265869)) + (data["stdbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh((((data["maxtominbatch"]) + (data["maxbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((data["abs_minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_msignal"] <= -998, data["rangebatch_slices2_msignal"], data["abs_minbatch_msignal"] )) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) * (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where((((4.61868953704833984)) * (data["meanbatch_slices2_msignal"])) <= -998, np.where(data["signal_shift_-1_msignal"] <= -998, ((data["signal_shift_-1_msignal"]) * 2.0), ((data["abs_maxbatch_msignal"]) * (data["abs_maxbatch_msignal"])) ), data["mean_abs_chgbatch_slices2"] )) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) * (np.where(data["signal_shift_+1_msignal"] > -998, data["medianbatch_slices2"], data["minbatch_slices2"] )))) +
                            0.100000*np.tanh(((np.tanh((((data["abs_minbatch_slices2_msignal"]) - (data["meanbatch_slices2_msignal"]))))) + ((((10.0)) + (data["rangebatch_slices2"]))))) +
                            0.100000*np.tanh((((7.0)) * ((-((((((data["maxbatch_slices2_msignal"]) * (data["maxbatch_slices2_msignal"]))) + (((((data["maxbatch_msignal"]) / 2.0)) * (data["abs_maxbatch"])))))))))) +
                            0.100000*np.tanh(((data["stdbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(((((np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, np.where(data["maxbatch_slices2_msignal"] > -998, data["meanbatch_slices2_msignal"], data["mean_abs_chgbatch_slices2_msignal"] ), data["maxbatch_slices2_msignal"] )) * 2.0)) - (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) - (((data["abs_maxbatch_slices2_msignal"]) * (((data["abs_avgbatch_msignal"]) * (data["rangebatch_msignal"]))))))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((((data["medianbatch_msignal"]) * (data["abs_maxbatch_msignal"]))) * (data["medianbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((((data["minbatch_slices2"]) + (np.where(data["abs_minbatch_slices2"] > -998, ((data["meanbatch_slices2"]) * (data["abs_maxbatch_slices2_msignal"])), data["mean_abs_chgbatch_slices2_msignal"] )))) + (data["maxtominbatch_slices2"]))) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1_msignal"] <= -998, np.tanh((data["signal_shift_-1_msignal"])), data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) * (data["signal_shift_+1"]))) +
                            0.100000*np.tanh((-(((((data["maxbatch_slices2_msignal"]) + (((data["abs_maxbatch_slices2_msignal"]) - (data["signal_shift_+1"]))))/2.0))))) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_msignal"] > -998, data["abs_minbatch_msignal"], data["stdbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_msignal"] <= -998, data["minbatch"], ((((data["stdbatch_msignal"]) * (data["meanbatch_msignal"]))) + (data["abs_minbatch_msignal"])) )) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) * (np.where(((data["meanbatch_msignal"]) * ((((data["maxtominbatch"]) + (data["abs_maxbatch"]))/2.0))) <= -998, data["signal_shift_+1_msignal"], (((data["maxtominbatch"]) + (data["maxbatch_msignal"]))/2.0) )))) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) - (np.where((((((data["abs_maxbatch_slices2_msignal"]) * (data["stdbatch_msignal"]))) + (data["maxbatch_msignal"]))/2.0) <= -998, data["abs_maxbatch_slices2_msignal"], ((data["stdbatch_msignal"]) * (data["abs_maxbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(((((((((np.tanh((((((data["minbatch_msignal"]) / 2.0)) / 2.0)))) * 2.0)) + (data["maxbatch_msignal"]))) / 2.0)) * (data["signal"]))) +
                            0.100000*np.tanh((((((((((np.where(data["meanbatch_slices2_msignal"] <= -998, data["meanbatch_slices2"], data["stdbatch_slices2_msignal"] )) - ((((-((data["minbatch_slices2_msignal"])))) / 2.0)))) * 2.0)) * 2.0)) + ((-((data["abs_maxbatch_slices2"])))))/2.0)) +
                            0.100000*np.tanh(((data["maxtominbatch"]) - (np.tanh((((data["signal"]) + (((data["signal_shift_-1_msignal"]) * 2.0)))))))) +
                            0.100000*np.tanh(data["minbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((((((data["abs_maxbatch_msignal"]) * (data["maxbatch_slices2_msignal"]))) + (data["abs_minbatch_slices2"]))/2.0)) - (((((((data["abs_maxbatch_msignal"]) / 2.0)) + (data["rangebatch_slices2_msignal"]))) / 2.0)))) +
                            0.100000*np.tanh(((data["rangebatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh(data["maxtominbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.tanh((((((data["mean_abs_chgbatch_msignal"]) / 2.0)) / 2.0)))) +
                            0.100000*np.tanh(np.where(((data["abs_maxbatch_slices2_msignal"]) * 2.0) > -998, np.where(data["signal_shift_-1"] > -998, data["rangebatch_msignal"], data["maxtominbatch"] ), (-((data["signal_shift_+1_msignal"]))) )) +
                            0.100000*np.tanh(np.where(((data["meanbatch_msignal"]) - (data["abs_maxbatch_slices2_msignal"])) > -998, (((data["minbatch_slices2"]) + (np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["abs_maxbatch_msignal"], data["meanbatch_msignal"] )))/2.0), data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) + (data["maxtominbatch_slices2"]))) * 2.0)) +
                            0.100000*np.tanh((((((((2.64627885818481445)) * ((((((data["abs_maxbatch_msignal"]) - (((data["meanbatch_msignal"]) * (data["meanbatch_msignal"]))))) + (data["abs_avgbatch_slices2_msignal"]))/2.0)))) * 2.0)) * (data["minbatch"]))) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh(((((((data["stdbatch_msignal"]) / 2.0)) + (((data["abs_minbatch_msignal"]) + (data["abs_minbatch_msignal"]))))) * (data["stdbatch_slices2"]))) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_slices2_msignal"] > -998, np.where(data["mean_abs_chgbatch_msignal"] <= -998, data["abs_maxbatch_slices2"], data["maxbatch_slices2_msignal"] ), data["maxbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((((((np.tanh(((-(((0.0))))))) + ((((-((data["minbatch_slices2"])))) / 2.0)))) / 2.0)) * 2.0)) +
                            0.100000*np.tanh((((((data["maxbatch_slices2_msignal"]) + (data["abs_maxbatch_msignal"]))) + (data["meanbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((data["minbatch_slices2_msignal"]) / 2.0)))) +
                            0.100000*np.tanh((((((data["abs_minbatch_slices2_msignal"]) + (((data["abs_avgbatch_slices2"]) * (data["maxbatch_msignal"]))))/2.0)) * 2.0)) +
                            0.100000*np.tanh((((-((data["abs_avgbatch_msignal"])))) * (np.where(((data["signal_shift_+1_msignal"]) + ((((-((((data["minbatch_slices2_msignal"]) / 2.0))))) * (data["minbatch_slices2_msignal"])))) <= -998, data["abs_maxbatch_slices2"], data["medianbatch_msignal"] )))) +
                            0.100000*np.tanh(np.tanh((data["mean_abs_chgbatch_slices2"]))) +
                            0.100000*np.tanh(((((data["maxbatch_msignal"]) + (((data["rangebatch_msignal"]) + (data["stdbatch_slices2"]))))) + (data["maxtominbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh(np.tanh(((-((((data["maxbatch_slices2_msignal"]) * 2.0))))))) +
                            0.100000*np.tanh(np.where(np.where(np.tanh((data["abs_minbatch_slices2"])) <= -998, data["medianbatch_slices2"], (((7.25608539581298828)) / 2.0) ) <= -998, data["rangebatch_msignal"], (((data["medianbatch_slices2"]) + (data["maxtominbatch"]))/2.0) )) +
                            0.100000*np.tanh(data["rangebatch_msignal"]) +
                            0.100000*np.tanh((((((data["abs_avgbatch_slices2"]) + ((((-((data["abs_avgbatch_slices2"])))) / 2.0)))/2.0)) - ((((10.64788627624511719)) + (np.where(data["abs_avgbatch_msignal"] <= -998, data["signal_shift_+1_msignal"], data["minbatch_msignal"] )))))) +
                            0.100000*np.tanh((((((np.tanh((data["abs_minbatch_slices2_msignal"]))) + (np.tanh((data["maxtominbatch_msignal"]))))/2.0)) + (((np.tanh((((data["signal_shift_+1_msignal"]) * 2.0)))) / 2.0)))) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * (((data["abs_maxbatch"]) + (((data["signal_shift_+1"]) * (np.where(((((4.17650079727172852)) + (data["abs_maxbatch_slices2_msignal"]))/2.0) > -998, data["meanbatch_slices2_msignal"], data["stdbatch_slices2_msignal"] )))))))) +
                            0.100000*np.tanh(((((data["signal_shift_+1_msignal"]) / 2.0)) + (((np.tanh((data["rangebatch_slices2_msignal"]))) / 2.0)))) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh((((((((np.where(data["mean_abs_chgbatch_slices2"] > -998, data["abs_maxbatch_slices2_msignal"], (-((data["maxtominbatch"]))) )) + (data["abs_maxbatch_msignal"]))/2.0)) / 2.0)) - (np.tanh((((((data["abs_maxbatch_slices2_msignal"]) / 2.0)) / 2.0)))))) +
                            0.100000*np.tanh(np.tanh(((((data["minbatch_slices2_msignal"]) + (data["stdbatch_slices2_msignal"]))/2.0)))) +
                            0.100000*np.tanh(data["maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2_msignal"] > -998, ((data["rangebatch_msignal"]) - (np.where(data["rangebatch_slices2_msignal"] > -998, (6.21980428695678711), data["rangebatch_msignal"] ))), data["maxtominbatch_slices2"] )) +
                            0.100000*np.tanh(((((data["maxtominbatch"]) + (data["mean_abs_chgbatch_slices2_msignal"]))) * 2.0)) +
                            0.100000*np.tanh(((np.where(data["abs_maxbatch_slices2_msignal"] > -998, ((data["meanbatch_slices2_msignal"]) / 2.0), (((data["abs_minbatch_slices2_msignal"]) + ((-((data["minbatch_slices2"])))))/2.0) )) * (((data["meanbatch_msignal"]) / 2.0)))) +
                            0.100000*np.tanh((-((data["abs_minbatch_slices2"])))) +
                            0.100000*np.tanh(((((((((((data["maxtominbatch"]) / 2.0)) / 2.0)) / 2.0)) * (data["rangebatch_slices2"]))) * 2.0)) +
                            0.100000*np.tanh(data["stdbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.tanh((data["abs_maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(((((((data["maxbatch_slices2_msignal"]) * ((((1.58761417865753174)) * 2.0)))) + ((1.58761060237884521)))) * 2.0) > -998, ((((data["abs_maxbatch_slices2_msignal"]) - ((1.58761060237884521)))) * 2.0), np.tanh((data["minbatch"])) )) +
                            0.100000*np.tanh(((np.tanh(((-((np.tanh((((np.where(data["stdbatch_slices2_msignal"] > -998, data["mean_abs_chgbatch_slices2"], ((data["medianbatch_slices2"]) + (((data["mean_abs_chgbatch_slices2_msignal"]) + (data["signal"])))) )) * 2.0))))))))) / 2.0)) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) - (np.tanh(((((np.tanh((data["abs_maxbatch_slices2_msignal"]))) + (np.tanh(((((((data["abs_minbatch_slices2"]) + (data["maxbatch_msignal"]))/2.0)) / 2.0)))))/2.0)))))) +
                            0.100000*np.tanh(np.where((-((((data["meanbatch_slices2_msignal"]) - (data["signal"]))))) <= -998, np.where(data["signal_shift_-1"] <= -998, data["signal_shift_-1"], data["signal"] ), (((data["stdbatch_msignal"]) + (data["abs_avgbatch_msignal"]))/2.0) )) +
                            0.100000*np.tanh(np.where(((data["meanbatch_msignal"]) * 2.0) <= -998, (((data["abs_maxbatch_msignal"]) + (data["maxbatch_slices2_msignal"]))/2.0), (-((data["medianbatch_msignal"]))) )) +
                            0.100000*np.tanh((0.0)) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1_msignal"] <= -998, np.tanh((data["minbatch_slices2"])), ((data["signal_shift_+1_msignal"]) * (data["signal_shift_-1_msignal"])) )) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) * 2.0)) +
                            0.100000*np.tanh((((((((data["abs_maxbatch_msignal"]) + (data["abs_maxbatch_msignal"]))/2.0)) * (((data["abs_avgbatch_slices2"]) / 2.0)))) - (data["abs_avgbatch_slices2"]))) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh((((data["maxtominbatch_slices2"]) + (data["stdbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((((data["maxbatch_slices2_msignal"]) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.tanh((data["signal_shift_-1_msignal"]))) +
                            0.100000*np.tanh(np.where(((data["stdbatch_msignal"]) - (data["rangebatch_slices2_msignal"])) <= -998, data["maxtominbatch"], ((data["stdbatch_msignal"]) + (data["rangebatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh(np.tanh((np.tanh((((np.tanh((data["abs_minbatch_slices2"]))) * 2.0)))))) +
                            0.100000*np.tanh(np.where((-(((-((((data["abs_minbatch_slices2"]) - (np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, data["maxtominbatch"], (((0.0)) / 2.0) ))))))))) > -998, data["mean_abs_chgbatch_slices2_msignal"], data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh((((data["abs_avgbatch_slices2_msignal"]) + (data["abs_maxbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(((np.tanh((data["abs_minbatch_slices2"]))) / 2.0)) +
                            0.100000*np.tanh((((np.tanh(((((data["signal_shift_-1_msignal"]) + (((data["signal_shift_-1_msignal"]) * 2.0)))/2.0)))) + (np.tanh((np.tanh(((0.0)))))))/2.0)) +
                            0.100000*np.tanh(((np.tanh(((-((((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0))))))) - (np.tanh((data["mean_abs_chgbatch_slices2"]))))) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2_msignal"] <= -998, data["maxtominbatch"], np.tanh((data["abs_minbatch_slices2"])) )) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_msignal"] > -998, ((data["rangebatch_slices2"]) - ((10.0))), data["signal_shift_+1"] )) +
                            0.100000*np.tanh(((np.tanh((((((data["abs_minbatch_slices2_msignal"]) + (data["stdbatch_slices2"]))) * 2.0)))) + (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(np.where((((data["maxtominbatch"]) + ((((data["signal_shift_-1"]) + ((-((np.tanh((data["signal_shift_-1"])))))))/2.0)))/2.0) > -998, data["meanbatch_slices2"], data["signal_shift_-1"] ) <= -998, data["abs_minbatch_slices2"], data["rangebatch_msignal"] )) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) / 2.0)) +
                            0.100000*np.tanh(np.tanh((((data["abs_avgbatch_slices2"]) * 2.0)))) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_msignal"]) +
                            0.100000*np.tanh(np.tanh(((-((((np.tanh((np.where((((((-((((data["mean_abs_chgbatch_slices2"]) - (data["maxbatch_slices2_msignal"])))))) * 2.0)) * 2.0) <= -998, data["maxbatch_slices2_msignal"], data["maxbatch_slices2"] )))) - (data["maxbatch_slices2_msignal"])))))))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((np.where(data["maxtominbatch_msignal"] <= -998, ((((((data["abs_maxbatch_slices2_msignal"]) + (data["abs_maxbatch_slices2"]))/2.0)) + (data["maxtominbatch"]))/2.0), ((data["abs_maxbatch_slices2"]) - (data["maxbatch_slices2_msignal"])) )) + (data["maxtominbatch"]))/2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((data["signal_shift_-1_msignal"]))))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((((((np.tanh((np.tanh((data["maxtominbatch"]))))) / 2.0)) / 2.0)))))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_msignal"]) - (data["abs_maxbatch_slices2"]))) - (((data["abs_maxbatch_slices2"]) * (np.where(((data["mean_abs_chgbatch_msignal"]) - (data["abs_maxbatch_slices2"])) > -998, data["medianbatch_msignal"], data["abs_maxbatch_slices2"] )))))) +
                            0.100000*np.tanh(np.tanh(((-((((data["mean_abs_chgbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"])))))))) +
                            0.100000*np.tanh((((data["maxbatch_slices2_msignal"]) + (((data["medianbatch_msignal"]) / 2.0)))/2.0)) +
                            0.100000*np.tanh(((np.where(data["maxbatch_slices2"] > -998, data["abs_maxbatch_slices2_msignal"], data["abs_minbatch_slices2_msignal"] )) - (np.tanh((((data["meanbatch_slices2"]) * (data["abs_maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(np.tanh((data["signal_shift_-1_msignal"]))) +
                            0.100000*np.tanh(((((np.where(data["medianbatch_slices2"] > -998, ((data["abs_maxbatch_msignal"]) + (((data["meanbatch_msignal"]) / 2.0))), np.where(data["medianbatch_slices2"] <= -998, data["signal_shift_-1_msignal"], data["signal"] ) )) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((np.tanh((np.tanh(((((data["mean_abs_chgbatch_slices2"]) + (((data["minbatch_slices2"]) - ((9.53928947448730469)))))/2.0)))))) / 2.0)) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh(np.tanh((data["signal_shift_-1"]))) +
                            0.100000*np.tanh(np.tanh((data["signal_shift_+1_msignal"]))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) / 2.0)) +
                            0.100000*np.tanh((((((data["abs_maxbatch_msignal"]) / 2.0)) + (data["abs_maxbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] <= -998, (((data["minbatch_slices2_msignal"]) + (((data["medianbatch_slices2_msignal"]) * (np.tanh(((-((data["abs_minbatch_msignal"])))))))))/2.0), data["medianbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.tanh((np.where(((data["maxbatch_slices2_msignal"]) + (np.tanh((np.tanh((data["stdbatch_slices2"])))))) > -998, data["abs_maxbatch_msignal"], data["signal"] )))) +
                            0.100000*np.tanh(np.tanh((((((data["abs_maxbatch_msignal"]) / 2.0)) / 2.0)))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((data["abs_minbatch_slices2"]) + (np.tanh((np.where(((np.tanh((((((data["rangebatch_slices2_msignal"]) / 2.0)) / 2.0)))) / 2.0) <= -998, data["maxtominbatch_slices2"], data["maxbatch_slices2_msignal"] )))))/2.0)))    
    
    def GP_class_10(self,data):
        return self.Output( -4.933813 +
                            0.100000*np.tanh(((((data["signal_shift_-1"]) / 2.0)) - (np.tanh((((((data["mean_abs_chgbatch_slices2"]) - (data["abs_minbatch_slices2_msignal"]))) - ((-((data["rangebatch_slices2_msignal"])))))))))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_msignal"]) * ((-(((5.76542758941650391))))))) * (data["signal_shift_+1"]))) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh((-((data["abs_avgbatch_slices2"])))) +
                            0.100000*np.tanh(data["maxbatch_slices2"]) +
                            0.100000*np.tanh(data["medianbatch_slices2"]) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) * (((((data["abs_maxbatch_slices2"]) * (((data["abs_maxbatch"]) * (np.tanh((np.tanh((data["mean_abs_chgbatch_slices2"]))))))))) + (data["meanbatch_slices2"]))))) +
                            0.100000*np.tanh(((np.tanh(((-((data["rangebatch_slices2_msignal"])))))) - ((-(((((data["mean_abs_chgbatch_slices2_msignal"]) + (data["minbatch"]))/2.0))))))) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, data["signal_shift_+1_msignal"], data["maxtominbatch_msignal"] )) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh((9.0)) +
                            0.100000*np.tanh(data["minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((-(((-((data["signal_shift_-1"]))))))) + (data["signal"]))/2.0)) +
                            0.100000*np.tanh(np.tanh((data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh((-((data["abs_maxbatch_msignal"])))) +
                            0.100000*np.tanh(data["rangebatch_slices2"]) +
                            0.100000*np.tanh(((((data["signal"]) * 2.0)) / 2.0)) +
                            0.100000*np.tanh(data["maxtominbatch_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh((-((np.where(data["minbatch_slices2"] <= -998, data["meanbatch_slices2_msignal"], np.tanh((data["meanbatch_slices2"])) ))))) +
                            0.100000*np.tanh((((data["mean_abs_chgbatch_slices2"]) + (np.tanh((((data["maxbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2"]))))))/2.0)) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1"] <= -998, data["abs_maxbatch_slices2"], data["mean_abs_chgbatch_slices2"] )) +
                            0.100000*np.tanh(np.where(((data["mean_abs_chgbatch_slices2"]) / 2.0) <= -998, data["signal"], data["maxbatch_slices2"] )) +
                            0.100000*np.tanh(np.where(((data["medianbatch_slices2"]) * 2.0) > -998, ((((data["medianbatch_slices2"]) * 2.0)) * 2.0), (((-(((-((data["medianbatch_slices2"]))))))) / 2.0) )) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) - (data["stdbatch_msignal"]))) +
                            0.100000*np.tanh((-((data["meanbatch_msignal"])))) +
                            0.100000*np.tanh(data["minbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((((-((data["minbatch_msignal"])))) * (data["signal_shift_-1_msignal"]))) - (data["stdbatch_msignal"]))) +
                            0.100000*np.tanh(data["rangebatch_msignal"]) +
                            0.100000*np.tanh((((-((((((data["rangebatch_msignal"]) + ((-((data["medianbatch_slices2"])))))) / 2.0))))) * 2.0)) +
                            0.100000*np.tanh((-((np.where((-((data["mean_abs_chgbatch_slices2"]))) <= -998, data["abs_minbatch_msignal"], data["abs_maxbatch"] ))))) +
                            0.100000*np.tanh(np.tanh(((-((data["minbatch"])))))) +
                            0.100000*np.tanh(((np.tanh((data["mean_abs_chgbatch_slices2"]))) * (np.tanh((data["mean_abs_chgbatch_slices2"]))))) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(np.where(np.where(data["rangebatch_slices2"] > -998, data["medianbatch_slices2_msignal"], data["abs_minbatch_msignal"] ) <= -998, data["rangebatch_slices2"], (-(((-(((-((data["meanbatch_msignal"]))))))))) )) +
                            0.100000*np.tanh((((-((((data["abs_minbatch_slices2_msignal"]) * (((data["maxbatch_slices2"]) * (data["maxtominbatch_msignal"])))))))) - (((data["abs_minbatch_slices2_msignal"]) / 2.0)))) +
                            0.100000*np.tanh(((data["minbatch"]) - (np.where((-(((-(((-((data["rangebatch_msignal"]))))))))) <= -998, data["signal_shift_-1"], data["abs_avgbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh((-((data["maxbatch_msignal"])))) +
                            0.100000*np.tanh(np.tanh((((data["medianbatch_slices2"]) / 2.0)))) +
                            0.100000*np.tanh((((((((-((((((data["minbatch_slices2"]) + (data["rangebatch_msignal"]))) - (data["medianbatch_slices2"])))))) - (data["maxtominbatch_msignal"]))) / 2.0)) - ((-((data["minbatch_slices2"])))))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(((((np.tanh(((-((data["medianbatch_slices2_msignal"])))))) - (data["abs_maxbatch_slices2_msignal"]))) / 2.0)) +
                            0.100000*np.tanh((-((data["maxtominbatch_slices2"])))) +
                            0.100000*np.tanh((((data["meanbatch_slices2_msignal"]) + (((data["medianbatch_slices2_msignal"]) * (((data["minbatch_slices2_msignal"]) + (((data["maxbatch_msignal"]) - (np.tanh((((((data["abs_maxbatch_slices2_msignal"]) / 2.0)) * 2.0)))))))))))/2.0)) +
                            0.100000*np.tanh(((((((((data["meanbatch_msignal"]) * (data["mean_abs_chgbatch_msignal"]))) - (data["abs_maxbatch_msignal"]))) / 2.0)) / 2.0)) +
                            0.100000*np.tanh((-((np.where(((data["medianbatch_slices2_msignal"]) * (data["medianbatch_slices2_msignal"])) <= -998, data["meanbatch_msignal"], np.tanh((data["maxtominbatch_msignal"])) ))))) +
                            0.100000*np.tanh((-(((((((data["meanbatch_msignal"]) + ((((data["maxbatch_slices2_msignal"]) + (((data["maxtominbatch"]) / 2.0)))/2.0)))/2.0)) * 2.0))))) +
                            0.100000*np.tanh((((-((data["maxbatch_slices2_msignal"])))) + ((-((np.where((-((np.where(data["meanbatch_slices2_msignal"] > -998, data["stdbatch_slices2_msignal"], data["maxbatch_slices2_msignal"] )))) > -998, data["meanbatch_msignal"], data["stdbatch_slices2"] ))))))) +
                            0.100000*np.tanh((-((np.where(data["abs_maxbatch_slices2"] > -998, np.where(data["minbatch_msignal"] <= -998, ((np.tanh((data["abs_avgbatch_msignal"]))) + (data["meanbatch_slices2_msignal"])), (((data["abs_maxbatch_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0) ), data["signal"] ))))) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(((np.where(data["minbatch_slices2_msignal"] > -998, data["minbatch_slices2_msignal"], data["abs_minbatch_slices2"] )) * (((np.where((7.83431625366210938) > -998, data["minbatch_slices2_msignal"], data["abs_minbatch_slices2"] )) + ((7.83431625366210938)))))) +
                            0.100000*np.tanh(np.where(((data["rangebatch_msignal"]) * (data["maxbatch_msignal"])) > -998, data["maxtominbatch_msignal"], data["meanbatch_slices2"] )) +
                            0.100000*np.tanh((-((((data["abs_avgbatch_slices2_msignal"]) * ((-(((((np.tanh((data["maxtominbatch"]))) + ((8.68455123901367188)))/2.0)))))))))) +
                            0.100000*np.tanh((((data["abs_maxbatch_slices2"]) + (((np.tanh((data["stdbatch_slices2_msignal"]))) - (data["abs_avgbatch_slices2"]))))/2.0)) +
                            0.100000*np.tanh(np.tanh(((((6.34843587875366211)) + (np.where((((data["abs_maxbatch_slices2_msignal"]) + (data["abs_minbatch_slices2"]))/2.0) <= -998, data["maxtominbatch_msignal"], ((data["signal_shift_-1_msignal"]) + (np.tanh((data["mean_abs_chgbatch_slices2_msignal"])))) )))))) +
                            0.100000*np.tanh((-((((data["abs_maxbatch_msignal"]) + (((data["meanbatch_msignal"]) * 2.0))))))) +
                            0.100000*np.tanh(np.where((((data["rangebatch_msignal"]) + (data["abs_minbatch_slices2"]))/2.0) <= -998, np.where(data["abs_avgbatch_slices2"] > -998, data["meanbatch_msignal"], np.where(data["rangebatch_msignal"] > -998, data["meanbatch_msignal"], data["medianbatch_slices2_msignal"] ) ), (-((data["medianbatch_slices2_msignal"]))) )) +
                            0.100000*np.tanh((-((np.where(data["abs_avgbatch_msignal"] <= -998, data["meanbatch_slices2"], (-((((data["meanbatch_slices2"]) / 2.0)))) ))))) +
                            0.100000*np.tanh(np.where(((data["maxbatch_msignal"]) - (data["stdbatch_slices2"])) <= -998, data["signal_shift_-1_msignal"], data["maxtominbatch_slices2"] )) +
                            0.100000*np.tanh((-(((((data["meanbatch_slices2_msignal"]) + (((data["stdbatch_slices2"]) / 2.0)))/2.0))))) +
                            0.100000*np.tanh((-((((data["maxbatch_slices2_msignal"]) + (np.where((-((((data["abs_maxbatch_msignal"]) + (data["medianbatch_msignal"]))))) > -998, data["medianbatch_msignal"], ((((data["abs_maxbatch_msignal"]) / 2.0)) * 2.0) ))))))) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) + (np.where(data["abs_minbatch_slices2"] <= -998, data["rangebatch_msignal"], data["meanbatch_slices2"] )))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.tanh((data["signal_shift_+1"]))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) / 2.0)) + (((data["abs_avgbatch_msignal"]) * (data["abs_avgbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((((data["abs_maxbatch"]) + (data["maxbatch_slices2_msignal"]))/2.0)) / 2.0)) +
                            0.100000*np.tanh((((-((data["abs_minbatch_slices2_msignal"])))) - (data["abs_minbatch_slices2"]))) +
                            0.100000*np.tanh((-((np.where((1.0) <= -998, data["medianbatch_msignal"], ((data["medianbatch_msignal"]) + (data["abs_maxbatch_msignal"])) ))))) +
                            0.100000*np.tanh((4.0)) +
                            0.100000*np.tanh((((((-((data["medianbatch_slices2_msignal"])))) - (data["maxbatch_slices2_msignal"]))) - (data["maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_slices2_msignal"] <= -998, (-((data["meanbatch_slices2_msignal"]))), (((-((data["medianbatch_msignal"])))) - (data["abs_maxbatch_msignal"])) )) +
                            0.100000*np.tanh(((np.where(data["medianbatch_slices2_msignal"] <= -998, ((data["stdbatch_slices2"]) * ((1.79480957984924316))), np.where(data["maxbatch_msignal"] <= -998, data["maxbatch_msignal"], (-((data["medianbatch_slices2_msignal"]))) ) )) - (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_slices2_msignal"] <= -998, (8.0), ((data["minbatch_slices2_msignal"]) * ((((data["minbatch_slices2_msignal"]) + ((9.0)))/2.0))) )) +
                            0.100000*np.tanh(np.where(data["minbatch"] <= -998, data["abs_maxbatch_msignal"], ((((data["medianbatch_slices2_msignal"]) * (((data["minbatch"]) / 2.0)))) + (((data["medianbatch_slices2_msignal"]) * (data["mean_abs_chgbatch_msignal"])))) )) +
                            0.100000*np.tanh((((((data["mean_abs_chgbatch_msignal"]) + (data["meanbatch_msignal"]))) + (((data["meanbatch_msignal"]) + (((data["abs_minbatch_msignal"]) + (((data["meanbatch_msignal"]) * (data["abs_minbatch_msignal"]))))))))/2.0)) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh((((-((data["maxbatch_slices2_msignal"])))) - (np.where(data["abs_minbatch_msignal"] > -998, np.where(data["medianbatch_slices2_msignal"] > -998, ((data["medianbatch_msignal"]) / 2.0), data["abs_maxbatch_slices2_msignal"] ), np.tanh((data["mean_abs_chgbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(((np.tanh((data["maxtominbatch_msignal"]))) - (np.where(((data["maxtominbatch"]) / 2.0) <= -998, data["mean_abs_chgbatch_msignal"], data["minbatch_slices2"] )))) +
                            0.100000*np.tanh((-((((((data["meanbatch_msignal"]) - (np.tanh((data["medianbatch_msignal"]))))) + (np.where(np.where(data["abs_minbatch_slices2_msignal"] <= -998, data["minbatch"], data["maxbatch_msignal"] ) <= -998, data["maxtominbatch_slices2"], data["maxbatch_msignal"] ))))))) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) * ((((data["minbatch_slices2_msignal"]) + (np.where(data["stdbatch_slices2"] <= -998, data["signal_shift_-1_msignal"], (-((((np.where(data["signal_shift_+1"] <= -998, data["abs_maxbatch_msignal"], data["stdbatch_msignal"] )) * 2.0)))) )))/2.0)))) +
                            0.100000*np.tanh((-(((((data["medianbatch_msignal"]) + ((((data["medianbatch_msignal"]) + ((9.0)))/2.0)))/2.0))))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2"]) / 2.0)) * 2.0)) +
                            0.100000*np.tanh((-((np.where(data["abs_maxbatch_slices2_msignal"] <= -998, data["abs_avgbatch_slices2_msignal"], ((((8.0)) + (np.where(data["minbatch_msignal"] > -998, data["minbatch_msignal"], data["abs_minbatch_slices2"] )))/2.0) ))))) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) * ((((data["abs_maxbatch_msignal"]) + (data["meanbatch_msignal"]))/2.0)))) - (((data["abs_maxbatch_msignal"]) + (data["mean_abs_chgbatch_slices2"]))))) +
                            0.100000*np.tanh(((data["signal"]) - (((((((data["meanbatch_slices2_msignal"]) + ((-((data["rangebatch_slices2"])))))) - (np.tanh((np.tanh(((-(((-(((-((data["abs_maxbatch_msignal"])))))))))))))))) * 2.0)))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((data["stdbatch_slices2_msignal"]) * (np.where(((((((-((data["stdbatch_msignal"])))) + (data["stdbatch_slices2_msignal"]))/2.0)) + (data["abs_avgbatch_slices2_msignal"])) > -998, data["meanbatch_msignal"], data["stdbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) * ((((((data["medianbatch_slices2_msignal"]) + (np.where(((data["mean_abs_chgbatch_slices2_msignal"]) * (data["maxbatch_slices2_msignal"])) > -998, data["abs_maxbatch_msignal"], np.tanh((data["mean_abs_chgbatch_slices2_msignal"])) )))/2.0)) * 2.0)))) +
                            0.100000*np.tanh(np.tanh((((data["medianbatch_msignal"]) + (np.where(data["signal_shift_-1_msignal"] <= -998, np.tanh((data["maxtominbatch_msignal"])), (-((data["abs_maxbatch"]))) )))))) +
                            0.100000*np.tanh(((np.where(((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])) > -998, ((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])), data["medianbatch_msignal"] )) - (np.where(data["maxtominbatch"] <= -998, data["maxbatch_msignal"], (6.0) )))) +
                            0.100000*np.tanh(((np.tanh(((-((data["medianbatch_slices2_msignal"])))))) + (data["signal_shift_+1"]))) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh((((((-((data["abs_avgbatch_msignal"])))) - (((data["abs_maxbatch_slices2_msignal"]) - (data["mean_abs_chgbatch_slices2"]))))) - ((((((((((data["abs_maxbatch_slices2_msignal"]) + (data["abs_maxbatch_slices2_msignal"]))) * 2.0)) + (data["abs_avgbatch_slices2_msignal"]))/2.0)) / 2.0)))) +
                            0.100000*np.tanh(data["maxtominbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((((data["meanbatch_slices2"]) - (((data["meanbatch_slices2_msignal"]) * (data["signal_shift_+1"]))))) + (data["abs_minbatch_slices2"]))) - (data["minbatch_msignal"]))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) * ((((data["meanbatch_msignal"]) + (data["abs_maxbatch_slices2"]))/2.0)))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) * ((((data["medianbatch_msignal"]) + ((3.0)))/2.0)))) +
                            0.100000*np.tanh((6.0)) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) * (data["medianbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((-((data["maxbatch_slices2"])))) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) + (data["stdbatch_msignal"]))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2_msignal"]) +
                            0.100000*np.tanh((-(((((9.0)) + (np.where(data["medianbatch_slices2_msignal"] > -998, data["minbatch_msignal"], np.where((((-((data["minbatch_msignal"])))) - (data["minbatch_msignal"])) <= -998, data["minbatch_msignal"], data["minbatch_msignal"] ) ))))))) +
                            0.100000*np.tanh(((data["maxtominbatch"]) - (np.where(((data["maxtominbatch"]) - (data["maxtominbatch_slices2"])) > -998, data["meanbatch_msignal"], data["signal"] )))) +
                            0.100000*np.tanh(((data["maxtominbatch"]) - (np.where(data["meanbatch_slices2"] > -998, data["meanbatch_msignal"], (((data["medianbatch_slices2_msignal"]) + (data["maxtominbatch"]))/2.0) )))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2"] <= -998, ((data["signal_shift_+1_msignal"]) + (((data["medianbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2"])))), data["mean_abs_chgbatch_slices2"] )) +
                            0.100000*np.tanh(np.where(((data["maxtominbatch_msignal"]) * 2.0) <= -998, (-((((data["mean_abs_chgbatch_msignal"]) * 2.0)))), data["mean_abs_chgbatch_msignal"] )) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((np.tanh((np.where(data["maxtominbatch_slices2"] > -998, data["signal_shift_-1"], ((data["medianbatch_slices2_msignal"]) + (data["rangebatch_msignal"])) )))) - (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where((-((data["maxtominbatch"]))) > -998, data["signal_shift_-1_msignal"], data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh((2.0)) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) * (((((8.0)) + (np.where(data["stdbatch_msignal"] <= -998, (8.0), data["minbatch_slices2_msignal"] )))/2.0)))) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_slices2"] > -998, data["signal_shift_+1_msignal"], data["maxtominbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(data["minbatch_slices2"]) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) * (((((((data["signal_shift_-1"]) - (data["signal_shift_-1_msignal"]))) + (data["maxbatch_slices2"]))) * ((((((data["abs_maxbatch_slices2_msignal"]) + ((-((data["abs_avgbatch_slices2_msignal"])))))/2.0)) * ((4.84204959869384766)))))))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (np.where(data["abs_maxbatch_slices2"] <= -998, data["minbatch_slices2"], ((data["maxbatch_slices2"]) * (data["maxtominbatch_slices2"])) )))) +
                            0.100000*np.tanh(data["abs_minbatch_msignal"]) +
                            0.100000*np.tanh((((((data["maxtominbatch_slices2"]) + ((((data["rangebatch_slices2"]) + (((data["mean_abs_chgbatch_slices2"]) * 2.0)))/2.0)))) + (np.tanh(((((((data["medianbatch_msignal"]) * 2.0)) + (np.tanh((data["meanbatch_slices2_msignal"]))))/2.0)))))/2.0)) +
                            0.100000*np.tanh((((((-((data["rangebatch_slices2_msignal"])))) + (data["abs_avgbatch_slices2"]))) / 2.0)) +
                            0.100000*np.tanh((((data["maxtominbatch"]) + ((8.00233268737792969)))/2.0)) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) * ((((((np.tanh(((-((data["meanbatch_msignal"])))))) + (data["medianbatch_msignal"]))/2.0)) - (np.tanh((data["meanbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) + (data["stdbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.tanh((data["rangebatch_slices2"]))) +
                            0.100000*np.tanh(((data["maxtominbatch"]) / 2.0)) +
                            0.100000*np.tanh(((((data["abs_maxbatch_msignal"]) / 2.0)) - (((((data["mean_abs_chgbatch_slices2"]) * ((1.0)))) - (((((data["abs_maxbatch_msignal"]) - (data["abs_minbatch_slices2_msignal"]))) * 2.0)))))) +
                            0.100000*np.tanh(np.where(((data["maxbatch_slices2_msignal"]) / 2.0) > -998, data["stdbatch_slices2_msignal"], data["maxtominbatch_msignal"] )) +
                            0.100000*np.tanh(np.tanh((((data["signal_shift_+1_msignal"]) * ((6.0)))))) +
                            0.100000*np.tanh(np.where((3.0) <= -998, data["signal_shift_-1_msignal"], np.where(((data["abs_minbatch_slices2"]) / 2.0) > -998, (-((data["abs_minbatch_msignal"]))), np.tanh(((5.0))) ) )) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (((data["abs_avgbatch_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_msignal"] > -998, ((data["mean_abs_chgbatch_slices2_msignal"]) * 2.0), np.where(data["maxtominbatch"] <= -998, data["abs_minbatch_slices2_msignal"], (((data["maxtominbatch_msignal"]) + (data["abs_minbatch_slices2"]))/2.0) ) )) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) - (data["medianbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["stdbatch_msignal"]) +
                            0.100000*np.tanh(np.tanh((((data["mean_abs_chgbatch_slices2"]) * 2.0)))) +
                            0.100000*np.tanh((((((np.where((9.0) > -998, data["meanbatch_slices2_msignal"], (1.0) )) * (data["abs_avgbatch_msignal"]))) + (data["abs_minbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_msignal"] > -998, (((((((data["maxtominbatch"]) + (((data["maxtominbatch"]) + (data["signal_shift_-1"]))))) + (data["meanbatch_slices2"]))/2.0)) - (data["stdbatch_slices2"])), data["abs_minbatch_msignal"] )) +
                            0.100000*np.tanh(data["rangebatch_msignal"]) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh(np.tanh((data["signal_shift_-1_msignal"]))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) * (((data["abs_minbatch_slices2_msignal"]) + (((data["abs_avgbatch_slices2"]) * (data["abs_maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch"] > -998, np.where(data["rangebatch_msignal"] <= -998, np.tanh((data["medianbatch_slices2_msignal"])), data["signal_shift_+1_msignal"] ), data["abs_minbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh(data["abs_maxbatch_msignal"]) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) - (data["abs_maxbatch"]))) +
                            0.100000*np.tanh(((np.where(data["maxbatch_slices2"] <= -998, data["signal_shift_-1"], data["rangebatch_msignal"] )) - (np.where(((data["rangebatch_slices2"]) / 2.0) <= -998, ((data["rangebatch_slices2"]) * 2.0), (4.73793363571166992) )))) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) * 2.0)) +
                            0.100000*np.tanh(data["maxbatch_msignal"]) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) / 2.0)) + (((data["abs_avgbatch_msignal"]) / 2.0)))) +
                            0.100000*np.tanh((((np.where(data["mean_abs_chgbatch_msignal"] > -998, ((data["signal_shift_-1_msignal"]) * 2.0), data["abs_minbatch_slices2"] )) + (data["signal_shift_+1_msignal"]))/2.0)) +
                            0.100000*np.tanh(((((data["rangebatch_msignal"]) + (data["maxtominbatch_slices2"]))) * 2.0)) +
                            0.100000*np.tanh(np.where(((data["meanbatch_slices2_msignal"]) * 2.0) <= -998, data["medianbatch_msignal"], (((((data["stdbatch_slices2_msignal"]) + (data["minbatch_msignal"]))/2.0)) + (((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])))) )) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh(np.tanh((np.tanh((data["maxtominbatch_slices2"]))))) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh((-(((-(((-((((data["abs_avgbatch_msignal"]) + ((((data["medianbatch_slices2"]) + (np.tanh((((np.where((-((data["signal_shift_-1"]))) <= -998, data["maxtominbatch_msignal"], data["stdbatch_msignal"] )) / 2.0)))))/2.0))))))))))))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) + (data["minbatch"]))) +
                            0.100000*np.tanh(np.where(((data["signal_shift_-1_msignal"]) * 2.0) > -998, data["abs_minbatch_slices2"], data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) / 2.0)) +
                            0.100000*np.tanh(data["maxtominbatch_slices2"]) +
                            0.100000*np.tanh(np.where((((-((data["minbatch_msignal"])))) + ((-((data["abs_minbatch_slices2"]))))) <= -998, (-(((10.34993553161621094)))), (((-((data["minbatch_msignal"])))) + ((-(((10.34993553161621094)))))) )) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh(np.tanh(((-((np.tanh((((((data["maxbatch_slices2_msignal"]) + (data["abs_maxbatch_slices2_msignal"]))) / 2.0))))))))) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["signal"]) + (((data["maxtominbatch_slices2"]) + (((data["maxtominbatch_slices2"]) + (data["signal"]))))))) +
                            0.100000*np.tanh(np.tanh((data["stdbatch_slices2"]))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) - (data["maxtominbatch"]))) +
                            0.100000*np.tanh(np.where(((data["maxbatch_msignal"]) / 2.0) <= -998, data["rangebatch_slices2_msignal"], ((data["rangebatch_slices2_msignal"]) - (data["maxtominbatch"])) )) +
                            0.100000*np.tanh(data["maxtominbatch_slices2"]) +
                            0.100000*np.tanh(((((((((data["abs_maxbatch_slices2"]) + (((data["maxtominbatch"]) / 2.0)))) + (((data["maxtominbatch"]) / 2.0)))/2.0)) + (data["abs_minbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((((((data["stdbatch_slices2_msignal"]) / 2.0)) + (((data["rangebatch_slices2_msignal"]) - (((((data["abs_minbatch_slices2_msignal"]) * 2.0)) * 2.0)))))) + (data["maxtominbatch"]))) +
                            0.100000*np.tanh(np.where((((data["signal"]) + (((data["signal_shift_+1_msignal"]) * 2.0)))/2.0) <= -998, (-((data["abs_minbatch_slices2"]))), (-((np.where(data["meanbatch_slices2_msignal"] <= -998, ((data["abs_avgbatch_msignal"]) + (data["stdbatch_msignal"])), (0.0) )))) )) +
                            0.100000*np.tanh(data["rangebatch_msignal"]) +
                            0.100000*np.tanh(np.where(np.where(data["signal_shift_-1_msignal"] <= -998, data["mean_abs_chgbatch_slices2_msignal"], data["rangebatch_slices2_msignal"] ) > -998, data["mean_abs_chgbatch_slices2_msignal"], data["rangebatch_slices2"] )) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(np.tanh((data["stdbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((((np.where(((data["signal_shift_+1_msignal"]) + (((data["maxbatch_slices2_msignal"]) + (((data["rangebatch_msignal"]) - (data["maxbatch_msignal"])))))) <= -998, data["signal_shift_-1_msignal"], data["signal_shift_-1"] )) * 2.0)) * (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where((((-((data["medianbatch_msignal"])))) * 2.0) <= -998, (-(((((-((data["abs_maxbatch_msignal"])))) * 2.0)))), ((((data["maxtominbatch"]) - (data["medianbatch_msignal"]))) * 2.0) )) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1_msignal"] <= -998, data["abs_maxbatch_msignal"], ((((((data["maxtominbatch"]) - (np.where((((-((data["maxtominbatch"])))) * 2.0) <= -998, data["abs_minbatch_slices2_msignal"], data["stdbatch_slices2_msignal"] )))) * 2.0)) / 2.0) )) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) - (data["signal_shift_+1"]))) +
                            0.100000*np.tanh(((data["rangebatch_slices2_msignal"]) + ((((data["maxbatch_msignal"]) + (((data["stdbatch_msignal"]) / 2.0)))/2.0)))) +
                            0.100000*np.tanh(((np.where(data["rangebatch_slices2"] > -998, data["maxtominbatch_slices2"], data["meanbatch_slices2_msignal"] )) - (((data["signal_shift_-1"]) / 2.0)))) +
                            0.100000*np.tanh(((np.tanh((data["rangebatch_msignal"]))) * 2.0)) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] <= -998, np.where(data["abs_avgbatch_slices2"] <= -998, data["signal_shift_-1_msignal"], data["abs_avgbatch_slices2"] ), data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) / 2.0)) +
                            0.100000*np.tanh(np.tanh(((-((data["minbatch_msignal"])))))) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) / 2.0)) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2"]) - (np.where((((11.32286262512207031)) - (((data["stdbatch_slices2"]) * 2.0))) > -998, data["signal_shift_+1_msignal"], data["signal_shift_+1"] )))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) * ((((data["meanbatch_slices2"]) + (data["rangebatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh((-((np.where(data["stdbatch_msignal"] > -998, (((data["minbatch"]) + (np.tanh((data["abs_minbatch_slices2"]))))/2.0), data["abs_maxbatch"] ))))) +
                            0.100000*np.tanh(np.where(np.tanh((data["signal_shift_+1_msignal"])) > -998, np.where((-((data["signal_shift_+1_msignal"]))) <= -998, data["maxtominbatch"], np.where(data["abs_maxbatch"] > -998, data["abs_maxbatch"], data["signal_shift_+1_msignal"] ) ), np.tanh((data["minbatch_msignal"])) )) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, data["mean_abs_chgbatch_msignal"], data["mean_abs_chgbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] <= -998, ((data["signal_shift_-1_msignal"]) * 2.0), data["abs_maxbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(np.where(data["stdbatch_slices2_msignal"] <= -998, data["mean_abs_chgbatch_slices2_msignal"], data["signal_shift_+1_msignal"] )) +
                            0.100000*np.tanh(np.tanh((((data["abs_minbatch_msignal"]) - (((np.where(((data["maxtominbatch"]) * (data["stdbatch_msignal"])) > -998, data["signal_shift_+1"], data["abs_minbatch_msignal"] )) / 2.0)))))))    


# In[ ]:


def maddest(d, axis=None):
    return np.mean(np.absolute(d - np.mean(d, axis)), axis)

def high_pass_filter(x, low_cutoff=1000, sample_rate=10000):

    nyquist = 0.5 * sample_rate
    norm_low_cutoff = low_cutoff / nyquist
    print(norm_low_cutoff)
    sos = butter(10, Wn=[norm_low_cutoff], btype='highpass', output='sos')
    filtered_sig = signal.sosfilt(sos, x)

    return filtered_sig

def denoise_signal( x, wavelet='db4', level=1):
    
    coeff = pywt.wavedec( x, wavelet, mode="per" )
    sigma = (1/0.6745) * maddest( coeff[-level] )
    uthresh = sigma * np.sqrt( 2*np.log( len( x ) ) )
    coeff[1:] = ( pywt.threshold( i, value=uthresh, mode='hard' ) for i in coeff[1:] )
    return pywt.waverec( coeff, wavelet, mode='per' )


# In[ ]:


def add_rooling_data(df : pd.DataFrame) -> pd.DataFrame:
    window_sizes = [10, 50, 100, 1000]
    for window in window_sizes:
        df["rolling_mean_" + str(window)] = df['signal'].rolling(window=window).mean()
        df["rolling_std_" + str(window)] = df['signal'].rolling(window=window).std()
    return df


# In[ ]:


base = '../input/liverpool-ion-switching'
train = pd.read_csv(os.path.join(base + '/train.csv'))
test  = pd.read_csv(os.path.join(base + '/test.csv'))


# In[ ]:


def features(df):
    df = df.sort_values(by=['time']).reset_index(drop=True)
    
    df.index = ((df.time * 10_000) - 1).values
    df['batch'] = df.index // 25_000
    df['batch_index'] = df.index  - (df.batch * 25_000)
    df['batch_slices'] = df['batch_index']  // 2500
    df['batch_slices2'] = df.apply(lambda r: '_'.join([str(r['batch']).zfill(3), str(r['batch_slices']).zfill(3)]), axis=1)
    
    for c in ['batch','batch_slices2']:
        d = {}
        d['mean'+c] = df.groupby([c])['signal'].mean()
        d['median'+c] = df.groupby([c])['signal'].median()
        d['max'+c] = df.groupby([c])['signal'].max()
        d['min'+c] = df.groupby([c])['signal'].min()
        d['std'+c] = df.groupby([c])['signal'].std()
        d['mean_abs_chg'+c] = df.groupby([c])['signal'].apply(lambda x: np.mean(np.abs(np.diff(x))))
        d['abs_max'+c] = df.groupby([c])['signal'].apply(lambda x: np.max(np.abs(x)))
        d['abs_min'+c] = df.groupby([c])['signal'].apply(lambda x: np.min(np.abs(x)))
        d['range'+c] = d['max'+c] - d['min'+c]
        d['maxtomin'+c] = d['max'+c] / d['min'+c]
        d['abs_avg'+c] = (d['abs_min'+c] + d['abs_max'+c]) / 2
        for v in d:
            df[v] = df[c].map(d[v].to_dict())

    
    #add shifts
    df['signal_shift_+1'] = [0,] + list(df['signal'].values[:-1])
    df['signal_shift_-1'] = list(df['signal'].values[1:]) + [0]
    for i in df[df['batch_index']==0].index:
        df['signal_shift_+1'][i] = np.nan
    for i in df[df['batch_index']==49999].index:
        df['signal_shift_-1'][i] = np.nan

    for c in [c1 for c1 in df.columns if c1 not in ['time', 'signal', 'open_channels', 'batch',
                                                    'batch_index', 'batch_slices', 'batch_slices2'
                                                    
                                                   ]]:
        df[c+'_msignal'] = df[c] - df['signal']
        
    return df

train = features(train)
test = features(test)

col = [c for c in train.columns if c not in ['time', 'open_channels', 'batch', 'batch_index', 'batch_slices', 'batch_slices2',
                                             'mean_abs_chgbatch', 'meanbatch', 'rangebatch', 'stdbatch',
                                             'maxbatch', 'medianbatch', 'abs_minbatch', 'abs_avgbatch']]
target = train['open_channels']
train = train[col]


# In[ ]:


train.replace(np.inf,np.nan,inplace=True)
train.replace(-np.inf,np.nan,inplace=True)
train.fillna(-999,inplace=True)
test.replace(np.inf,np.nan,inplace=True)
test.replace(-np.inf,np.nan,inplace=True)
test.fillna(-999,inplace=True)


# In[ ]:


gp = GP()
train_preds = gp.GrabPredictions(train)


# In[ ]:


f1_score(target.values,np.argmax(train_preds.values,axis=1),average='macro')


# In[ ]:


test_preds = gp.GrabPredictions(test)


# In[ ]:


test['open_channels'] = np.argmax(test_preds.values,axis=1)
test[['time','open_channels']].to_csv('submission.csv', index=False, float_format='%.4f')


# In[ ]:


test[['time','open_channels']].head()

