#!/usr/bin/env python
# coding: utf-8

# A quick GP predictor.
# As ordered by Konrad - there is a limits on the size of a notebook so with 11 classes I decided to limit it to 100 lines per class.  I also trained it on 20% of the data.

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
        return self.Output(-1.394065 +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((((((((((data["minbatch_slices2_msignal"]) + ((((7.0)) + (data["minbatch_slices2_msignal"]))))) + (data["minbatch_slices2_msignal"]))) * 2.0)) + (data["minbatch_slices2_msignal"]))) + (data["minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) + (np.where(np.where(((data["abs_minbatch_slices2"]) + (data["abs_minbatch_msignal"])) > -998, data["abs_minbatch_slices2_msignal"], data["minbatch_slices2_msignal"] ) > -998, data["minbatch_slices2_msignal"], data["abs_minbatch_msignal"] )))) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) * 2.0)) + ((((((((data["minbatch_slices2_msignal"]) * 2.0)) + (data["abs_maxbatch_slices2"]))/2.0)) + (data["abs_avgbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) + (np.where(((data["abs_minbatch_slices2_msignal"]) * 2.0) > -998, data["minbatch_slices2_msignal"], ((data["mean_abs_chgbatch_slices2_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((data["abs_minbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2_msignal"] <= -998, ((data["minbatch_slices2_msignal"]) / 2.0), ((data["abs_minbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((((((3.31194949150085449)) + (((data["minbatch_slices2_msignal"]) * 2.0)))/2.0)) * 2.0)) +
                            0.100000*np.tanh((((data["abs_minbatch_slices2_msignal"]) + (((np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, ((data["abs_minbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"])), data["minbatch_slices2_msignal"] )) + (data["maxtominbatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh(((np.where(data["abs_minbatch_slices2_msignal"] > -998, data["minbatch_slices2_msignal"], ((data["abs_minbatch_slices2_msignal"]) + (np.where(data["abs_minbatch_slices2_msignal"] > -998, data["minbatch_slices2_msignal"], ((data["maxbatch_msignal"]) + (data["minbatch_slices2_msignal"])) ))) )) + (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_msignal"] <= -998, np.where(data["abs_maxbatch_msignal"] > -998, data["abs_minbatch_slices2"], data["mean_abs_chgbatch_slices2_msignal"] ), ((((data["minbatch_msignal"]) + ((2.0)))) * 2.0) )) +
                            0.100000*np.tanh(((np.where(data["abs_minbatch_slices2_msignal"] > -998, data["minbatch_slices2_msignal"], np.where(data["stdbatch_msignal"] > -998, data["maxtominbatch_slices2_msignal"], data["mean_abs_chgbatch_msignal"] ) )) + (data["abs_minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((((((((data["minbatch_slices2_msignal"]) + (((np.where((1.13687419891357422) > -998, (1.13687419891357422), data["maxtominbatch_slices2_msignal"] )) * 2.0)))) * 2.0)) * 2.0)) + ((((((data["minbatch_msignal"]) + (data["minbatch_slices2_msignal"]))/2.0)) * 2.0)))) +
                            0.100000*np.tanh(((((((((data["maxtominbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"]))) + ((((((((((((2.0)) + (data["minbatch_slices2_msignal"]))) * 2.0)) + (data["minbatch_slices2_msignal"]))) * 2.0)) * 2.0)))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) + (np.where(((data["minbatch_msignal"]) * 2.0) > -998, data["minbatch_msignal"], (-((np.tanh((data["rangebatch_slices2_msignal"]))))) )))) +
                            0.100000*np.tanh(((np.where(np.where(data["abs_minbatch_slices2"] > -998, ((data["maxbatch_msignal"]) + (data["minbatch_msignal"])), data["abs_maxbatch_msignal"] ) > -998, data["maxbatch_msignal"], np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["maxbatch_msignal"], data["abs_avgbatch_msignal"] ) )) + (data["minbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_msignal"] > -998, data["maxtominbatch_slices2_msignal"], (((data["maxtominbatch_slices2_msignal"]) + (data["abs_minbatch_slices2"]))/2.0) )) +
                            0.100000*np.tanh((((((((((data["abs_maxbatch_msignal"]) + (((data["abs_minbatch_msignal"]) * 2.0)))/2.0)) + (data["abs_minbatch_slices2_msignal"]))) * 2.0)) + (data["abs_avgbatch_msignal"]))) +
                            0.100000*np.tanh(((((data["minbatch_slices2_msignal"]) + ((((data["maxtominbatch_slices2_msignal"]) + (data["maxtominbatch_msignal"]))/2.0)))) + (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(((data["maxtominbatch_slices2_msignal"]) + (data["abs_minbatch_slices2_msignal"])) > -998, ((data["maxtominbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"])), ((data["abs_minbatch_msignal"]) + (((data["abs_minbatch_slices2"]) + (data["maxtominbatch_slices2_msignal"])))) )) +
                            0.100000*np.tanh(((((((((((((data["maxtominbatch_slices2_msignal"]) + (data["abs_minbatch_msignal"]))/2.0)) + (data["minbatch_msignal"]))) + (data["maxbatch_msignal"]))/2.0)) * 2.0)) + (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (np.where(np.where((((4.0)) + (data["minbatch_slices2_msignal"])) > -998, data["minbatch_msignal"], data["abs_avgbatch_slices2"] ) <= -998, data["stdbatch_slices2_msignal"], (((4.0)) + (data["minbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh((((4.0)) + (((data["minbatch_slices2_msignal"]) + ((((4.0)) + (((data["minbatch_slices2_msignal"]) + ((4.0)))))))))) +
                            0.100000*np.tanh((((2.30758714675903320)) + (np.where(((((data["minbatch_msignal"]) - ((2.30758714675903320)))) * 2.0) > -998, data["minbatch_msignal"], (((2.30758714675903320)) - (np.where((2.30758714675903320) > -998, data["minbatch_msignal"], data["rangebatch_slices2"] ))) )))) +
                            0.100000*np.tanh(np.where((((data["abs_maxbatch_msignal"]) + ((2.0)))/2.0) <= -998, ((data["abs_maxbatch_msignal"]) + ((2.0))), ((np.where(data["abs_minbatch_slices2_msignal"] <= -998, (2.0), (((2.0)) + (data["minbatch_slices2_msignal"])) )) * 2.0) )) +
                            0.100000*np.tanh(np.where((((2.0)) * (((data["abs_avgbatch_msignal"]) * 2.0))) <= -998, data["meanbatch_msignal"], ((data["abs_minbatch_msignal"]) + (((data["abs_avgbatch_msignal"]) + (np.where(data["abs_minbatch_msignal"] > -998, data["abs_avgbatch_msignal"], data["abs_avgbatch_msignal"] ))))) )) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (np.where(data["meanbatch_slices2_msignal"] > -998, data["maxbatch_msignal"], np.where(data["minbatch_msignal"] > -998, ((((data["minbatch_msignal"]) + (data["abs_maxbatch_msignal"]))) + (data["abs_avgbatch_msignal"])), data["minbatch_msignal"] ) )))) +
                            0.100000*np.tanh(((np.tanh((((data["maxbatch_msignal"]) + (data["minbatch_msignal"]))))) * 2.0)) +
                            0.100000*np.tanh((((((5.45460939407348633)) + (((data["abs_avgbatch_slices2_msignal"]) + ((3.0)))))) + (((data["minbatch_slices2_msignal"]) * ((6.0)))))) +
                            0.100000*np.tanh(data["maxbatch_msignal"]) +
                            0.100000*np.tanh(((np.where((((data["abs_avgbatch_msignal"]) + (data["minbatch_msignal"]))/2.0) > -998, data["abs_maxbatch_msignal"], data["abs_maxbatch_msignal"] )) + (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] <= -998, data["signal_shift_+1_msignal"], ((((((data["minbatch_slices2_msignal"]) + (data["maxbatch_msignal"]))) * 2.0)) * 2.0) )) +
                            0.100000*np.tanh((((3.0)) - ((-((((np.where(((data["minbatch_msignal"]) * 2.0) > -998, np.where((3.0) > -998, data["minbatch_msignal"], (3.0) ), (3.0) )) * 2.0))))))) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] > -998, ((np.where(((data["minbatch_slices2_msignal"]) * 2.0) > -998, ((data["minbatch_slices2_msignal"]) + ((1.88652682304382324))), data["minbatch_slices2"] )) * 2.0), data["minbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((((np.where(data["abs_avgbatch_slices2_msignal"] <= -998, data["maxbatch_slices2_msignal"], (((7.0)) - (data["rangebatch_slices2"])) )) * 2.0)) + (np.tanh(((((((7.0)) - (data["rangebatch_slices2"]))) * 2.0)))))) +
                            0.100000*np.tanh(((((((np.where(data["minbatch_msignal"] <= -998, data["minbatch_slices2_msignal"], ((data["maxbatch_msignal"]) + (data["minbatch_msignal"])) )) + (data["abs_avgbatch_slices2"]))) + (data["minbatch_msignal"]))) * 2.0)) +
                            0.100000*np.tanh((((((((data["abs_maxbatch"]) + ((14.95801162719726562)))/2.0)) - (((data["rangebatch_slices2"]) * (data["rangebatch_slices2"]))))) + (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2"] <= -998, np.where((6.0) <= -998, (((4.0)) + (data["minbatch_slices2_msignal"])), ((((data["minbatch_slices2_msignal"]) / 2.0)) * 2.0) ), (((3.0)) + (((data["minbatch_slices2_msignal"]) * 2.0))) )) +
                            0.100000*np.tanh(np.where((((data["abs_maxbatch_slices2_msignal"]) + (((data["abs_avgbatch_slices2"]) + ((((((7.0)) * 2.0)) * (data["abs_maxbatch"]))))))/2.0) > -998, data["maxbatch_msignal"], (7.0) )) +
                            0.100000*np.tanh(((((data["abs_avgbatch_msignal"]) * 2.0)) * ((10.0)))) +
                            0.100000*np.tanh(np.where(((data["rangebatch_slices2"]) - (data["rangebatch_slices2"])) > -998, (((5.93238592147827148)) + (((data["minbatch_msignal"]) - (data["rangebatch_slices2"])))), (5.93238592147827148) )) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] <= -998, data["maxbatch_msignal"], ((((((((((data["maxbatch_msignal"]) + (data["minbatch_slices2_msignal"]))) * 2.0)) * 2.0)) + (((((data["maxbatch_msignal"]) + (data["minbatch_slices2_msignal"]))) * 2.0)))) * 2.0) )) +
                            0.100000*np.tanh(((((((8.92164039611816406)) / 2.0)) + (((((data["minbatch_msignal"]) * (data["abs_maxbatch"]))) + (data["maxbatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh(np.where(((data["meanbatch_slices2"]) + ((2.18381571769714355))) > -998, (((2.18381571769714355)) + (data["minbatch_slices2_msignal"])), (2.18381571769714355) )) +
                            0.100000*np.tanh(((((8.0)) + ((((((8.90596199035644531)) - (((data["maxbatch_msignal"]) * (data["rangebatch_slices2"]))))) * (data["maxbatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh(np.where(data["maxtominbatch"] <= -998, (9.0), (((data["abs_maxbatch"]) + (((data["abs_maxbatch_slices2"]) * (data["abs_avgbatch_msignal"]))))/2.0) )) +
                            0.100000*np.tanh((7.63479518890380859)) +
                            0.100000*np.tanh(((np.where(data["abs_maxbatch_slices2"] <= -998, data["minbatch_slices2_msignal"], data["abs_minbatch_msignal"] )) + ((7.03963851928710938)))) +
                            0.100000*np.tanh(((np.tanh((((((data["minbatch_slices2_msignal"]) + (((np.where(data["maxbatch_slices2_msignal"] <= -998, ((data["minbatch_msignal"]) + (data["minbatch_slices2_msignal"])), ((data["minbatch_slices2_msignal"]) + ((1.88456702232360840))) )) * 2.0)))) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(data["maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where((((3.0)) * (np.where(data["abs_avgbatch_msignal"] > -998, (3.0), data["abs_maxbatch_slices2_msignal"] ))) > -998, ((((4.65008258819580078)) + (data["minbatch_slices2_msignal"]))/2.0), (3.0) )) +
                            0.100000*np.tanh(np.where((2.06466484069824219) <= -998, (2.06466484069824219), ((data["minbatch_slices2_msignal"]) + ((2.06466484069824219))) )) +
                            0.100000*np.tanh(((((5.0)) + (np.where(((data["abs_maxbatch_msignal"]) * (data["rangebatch_msignal"])) <= -998, (-((data["rangebatch_msignal"]))), ((data["rangebatch_slices2"]) * ((-((data["stdbatch_slices2"]))))) )))/2.0)) +
                            0.100000*np.tanh((((4.73483657836914062)) - (np.where(data["abs_avgbatch_slices2_msignal"] <= -998, np.where((4.73483657836914062) <= -998, data["minbatch_slices2"], data["minbatch_slices2"] ), data["rangebatch_slices2"] )))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((((data["minbatch_msignal"]) + ((2.10528779029846191)))) + ((2.10528779029846191)))))) +
                            0.100000*np.tanh(((((4.0)) + (np.where(data["signal_shift_+1_msignal"] <= -998, data["minbatch_slices2_msignal"], ((((((data["minbatch_slices2_msignal"]) + (np.tanh((data["maxbatch_msignal"]))))) * 2.0)) * 2.0) )))/2.0)) +
                            0.100000*np.tanh((((((((((9.0)) * 2.0)) * 2.0)) + (((((data["rangebatch_msignal"]) * 2.0)) * (((data["abs_minbatch_slices2"]) + (data["abs_maxbatch_msignal"]))))))) + ((((data["abs_avgbatch_msignal"]) + (data["maxbatch_slices2"]))/2.0)))) +
                            0.100000*np.tanh((((((((13.79771518707275391)) - (data["rangebatch_slices2"]))) - (((data["rangebatch_slices2"]) * 2.0)))) / 2.0)) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2_msignal"] <= -998, data["maxbatch_msignal"], (-(((-((data["abs_maxbatch_slices2"])))))) )) +
                            0.100000*np.tanh((((9.54191780090332031)) - (((data["rangebatch_slices2"]) - (data["abs_maxbatch"]))))) +
                            0.100000*np.tanh(((((((4.99336910247802734)) + ((((4.99337291717529297)) * 2.0)))/2.0)) + (((((np.where((4.99337291717529297) > -998, data["minbatch_msignal"], data["abs_maxbatch"] )) * 2.0)) * 2.0)))) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) * (data["rangebatch_slices2"]))) + (((data["maxbatch_msignal"]) + (np.where(((data["minbatch_msignal"]) * (data["rangebatch_slices2"])) > -998, data["abs_avgbatch_slices2"], data["maxbatch_msignal"] )))))) +
                            0.100000*np.tanh((((((data["maxbatch_slices2_msignal"]) + (data["rangebatch_msignal"]))) + (((((np.where(data["abs_minbatch_msignal"] > -998, data["abs_maxbatch"], (6.0) )) * 2.0)) * 2.0)))/2.0)) +
                            0.100000*np.tanh(np.where(((data["maxbatch_msignal"]) * 2.0) <= -998, data["medianbatch_slices2_msignal"], (((((((((data["rangebatch_slices2"]) * ((((data["minbatch_msignal"]) + (data["minbatch_slices2_msignal"]))/2.0)))) * 2.0)) + ((13.31092643737792969)))/2.0)) * 2.0) )) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh((10.0)) +
                            0.100000*np.tanh((((((1.53610146045684814)) - (((data["minbatch_slices2_msignal"]) * (np.where((1.53610146045684814) > -998, (((1.53610146045684814)) - (((data["minbatch_slices2_msignal"]) * (data["minbatch_slices2_msignal"])))), data["minbatch_slices2_msignal"] )))))) * 2.0)) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * (((data["abs_avgbatch_msignal"]) * (np.where(data["abs_maxbatch_slices2_msignal"] <= -998, data["maxbatch_msignal"], (7.05499124526977539) )))))) +
                            0.100000*np.tanh(((np.tanh((np.where(((data["minbatch_slices2_msignal"]) * (data["minbatch_slices2_msignal"])) <= -998, (8.0), data["maxbatch_msignal"] )))) + (((data["rangebatch_slices2"]) + (((data["minbatch_slices2_msignal"]) * (data["rangebatch_slices2"]))))))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where(data["meanbatch_msignal"] > -998, data["maxbatch_msignal"], data["minbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((np.where((-(((3.0)))) <= -998, (((((data["minbatch_slices2_msignal"]) + (data["maxbatch_msignal"]))) + (data["minbatch_slices2_msignal"]))/2.0), ((data["minbatch_slices2_msignal"]) + (((data["minbatch_slices2_msignal"]) + ((3.0))))) )) * 2.0)) +
                            0.100000*np.tanh(((((data["maxbatch_msignal"]) * 2.0)) - (np.where((((9.0)) * ((9.0))) > -998, data["maxbatch_slices2_msignal"], np.where(data["maxbatch_msignal"] > -998, (1.0), data["abs_maxbatch_slices2_msignal"] ) )))) +
                            0.100000*np.tanh(((((((7.0)) + (((np.where((8.0) <= -998, data["abs_maxbatch_msignal"], data["minbatch_msignal"] )) * (data["rangebatch_slices2"]))))/2.0)) * ((5.0)))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) + (((np.where(data["maxbatch_msignal"] > -998, data["maxbatch_msignal"], data["abs_avgbatch_slices2"] )) - (((data["rangebatch_msignal"]) * (data["stdbatch_slices2"]))))))) +
                            0.100000*np.tanh((((data["abs_maxbatch"]) + (data["abs_maxbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(((np.where((8.0) <= -998, (((3.0)) + (data["minbatch"])), (((3.0)) + (data["minbatch"])) )) * (data["maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((((((data["abs_maxbatch"]) + ((3.70935654640197754)))) - ((((4.0)) - (data["abs_maxbatch"]))))) * 2.0)) +
                            0.100000*np.tanh(np.where((((((7.0)) + (data["abs_maxbatch_msignal"]))) + (data["abs_avgbatch_msignal"])) <= -998, data["signal_shift_-1"], (((7.0)) + (((data["minbatch_msignal"]) - (data["maxbatch_slices2"])))) )) +
                            0.100000*np.tanh(((np.where(((data["maxbatch_slices2"]) * 2.0) > -998, (6.0), data["rangebatch_slices2"] )) + ((-((data["rangebatch_slices2"])))))) +
                            0.100000*np.tanh(((((5.0)) + (np.where(data["maxbatch_slices2"] <= -998, data["abs_maxbatch_slices2"], (-((data["rangebatch_slices2"]))) )))/2.0)) +
                            0.100000*np.tanh(((((data["maxbatch_msignal"]) + (data["minbatch_slices2_msignal"]))) * 2.0)) +
                            0.100000*np.tanh((((6.0)) / 2.0)) +
                            0.100000*np.tanh(((((np.where(data["maxtominbatch_msignal"] > -998, (6.35829210281372070), data["maxbatch_slices2_msignal"] )) * 2.0)) - (np.where((6.35829210281372070) > -998, ((np.where((6.51710748672485352) > -998, data["abs_maxbatch"], (2.0) )) * 2.0), (6.35829210281372070) )))) +
                            0.100000*np.tanh(((((data["maxbatch_msignal"]) * 2.0)) + (((((((data["maxbatch_msignal"]) / 2.0)) + ((1.92305850982666016)))) + (data["maxbatch_slices2"]))))) +
                            0.100000*np.tanh((4.66952991485595703)) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2_msignal"] <= -998, ((((data["abs_avgbatch_msignal"]) * 2.0)) * 2.0), ((data["abs_avgbatch_msignal"]) + (np.where(data["abs_avgbatch_msignal"] <= -998, data["maxtominbatch"], ((data["abs_avgbatch_msignal"]) * 2.0) ))) )) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh(data["maxbatch_msignal"]) +
                            0.100000*np.tanh((((((14.44665718078613281)) + (data["abs_avgbatch_msignal"]))) + ((7.54055309295654297)))) +
                            0.100000*np.tanh(data["abs_avgbatch_msignal"]) +
                            0.100000*np.tanh(((((((((3.0)) + (np.where(data["minbatch_msignal"] > -998, data["abs_maxbatch_slices2_msignal"], ((data["rangebatch_slices2_msignal"]) * (data["minbatch_msignal"])) )))) * (data["minbatch_msignal"]))) + ((11.54459190368652344)))/2.0)) +
                            0.100000*np.tanh((((5.0)) - (np.where(np.where(data["rangebatch_slices2"] > -998, (((data["abs_avgbatch_slices2"]) + ((5.0)))/2.0), data["abs_minbatch_slices2"] ) > -998, data["rangebatch_slices2"], (((5.0)) / 2.0) )))) +
                            0.100000*np.tanh((((10.58393192291259766)) - (((data["rangebatch_msignal"]) * ((-((data["minbatch_msignal"])))))))) +
                            0.100000*np.tanh(((data["abs_maxbatch"]) + (((data["abs_avgbatch_msignal"]) + ((4.0)))))) +
                            0.100000*np.tanh(((np.where((((((data["maxbatch_msignal"]) + (data["minbatch_slices2_msignal"]))) + (data["abs_avgbatch_msignal"]))/2.0) <= -998, ((data["maxbatch_msignal"]) * 2.0), ((((data["maxbatch_msignal"]) + (data["minbatch_slices2_msignal"]))) * 2.0) )) * 2.0)) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - (np.where(data["abs_minbatch_slices2"] > -998, ((((data["signal_shift_-1_msignal"]) * (data["rangebatch_slices2_msignal"]))) * (data["rangebatch_slices2_msignal"])), ((data["signal_shift_-1_msignal"]) * (data["abs_maxbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(((((((np.where(data["maxbatch_slices2_msignal"] <= -998, data["maxbatch_msignal"], data["minbatch_slices2_msignal"] )) + (((data["abs_maxbatch_slices2_msignal"]) / 2.0)))) / 2.0)) + (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(((((data["maxbatch_msignal"]) + (np.where(data["maxbatch_msignal"] <= -998, data["abs_avgbatch_slices2_msignal"], data["minbatch_msignal"] )))) * 2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2"]) + ((((((6.0)) + ((((((6.0)) + (((data["minbatch_slices2_msignal"]) * ((6.0)))))) * (data["abs_maxbatch_slices2"]))))) * 2.0)))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh((((4.0)) + (((np.where((-((data["minbatch_msignal"]))) <= -998, (-((data["minbatch_msignal"]))), ((data["minbatch_msignal"]) * (data["abs_maxbatch_slices2_msignal"])) )) / 2.0)))))
    
    def GP_class_1(self,data):
        return self.Output(-1.623877 +
                            0.100000*np.tanh(data["abs_minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((((((data["maxbatch_msignal"]) + (((data["rangebatch_slices2_msignal"]) * (data["mean_abs_chgbatch_msignal"]))))) * 2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((((-((((np.where(data["maxtominbatch_msignal"] > -998, data["maxtominbatch_slices2_msignal"], data["maxtominbatch_msignal"] )) + (((data["minbatch_slices2_msignal"]) + (data["maxtominbatch_slices2_msignal"])))))))) - (((((data["maxtominbatch_msignal"]) * 2.0)) * (data["minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((((((data["maxtominbatch_slices2"]) + (data["maxtominbatch_slices2_msignal"]))) + (data["maxtominbatch_slices2_msignal"]))) * 2.0)) +
                            0.100000*np.tanh((((((np.where(data["meanbatch_slices2"] > -998, (4.89374160766601562), data["maxtominbatch"] )) + (((data["maxtominbatch_slices2_msignal"]) * (data["meanbatch_slices2"]))))/2.0)) * (np.where((4.89374160766601562) > -998, (4.89374160766601562), data["maxtominbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh((((-((((data["minbatch_msignal"]) + ((((((((data["minbatch_msignal"]) + ((4.0)))) * 2.0)) + ((9.0)))/2.0))))))) * ((((data["minbatch_msignal"]) + (data["abs_minbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * (np.where(data["abs_maxbatch"] > -998, ((((11.27809810638427734)) + ((-((np.where(data["maxtominbatch_slices2_msignal"] > -998, ((data["abs_maxbatch_msignal"]) * (data["maxtominbatch_msignal"])), data["minbatch"] ))))))/2.0), data["minbatch"] )))) +
                            0.100000*np.tanh(((((np.where(((data["abs_minbatch_slices2_msignal"]) * 2.0) <= -998, data["maxtominbatch_msignal"], data["maxtominbatch_msignal"] )) * 2.0)) * (((((((data["rangebatch_slices2"]) - (data["mean_abs_chgbatch_msignal"]))) * 2.0)) * 2.0)))) +
                            0.100000*np.tanh((((((np.where(np.tanh((data["signal_shift_+1_msignal"])) <= -998, data["signal_shift_+1"], data["medianbatch_slices2"] )) * (data["abs_minbatch_slices2_msignal"]))) + ((((4.0)) * 2.0)))/2.0)) +
                            0.100000*np.tanh((((4.0)) - (np.where(data["minbatch_slices2_msignal"] > -998, ((data["maxbatch_msignal"]) * 2.0), data["maxtominbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh((((9.29093456268310547)) * (((((data["signal"]) - (data["minbatch_msignal"]))) * (((((((((3.0)) + (data["minbatch_msignal"]))/2.0)) * 2.0)) * 2.0)))))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2"]) - (data["stdbatch_slices2_msignal"]))) * (np.where(data["signal_shift_+1"] <= -998, data["stdbatch_slices2_msignal"], ((((data["minbatch_slices2_msignal"]) + ((2.47070121765136719)))) * 2.0) )))) +
                            0.100000*np.tanh(np.where((((-((data["minbatch_msignal"])))) - ((5.0))) <= -998, (((-((data["minbatch_msignal"])))) * 2.0), (((5.0)) + (((data["maxbatch_msignal"]) * (data["minbatch_slices2"])))) )) +
                            0.100000*np.tanh(((((data["signal"]) * (data["abs_minbatch_slices2_msignal"]))) + ((9.0)))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) - ((((np.where(data["minbatch_msignal"] > -998, data["rangebatch_slices2"], (9.0) )) + ((-(((11.70643997192382812))))))/2.0)))) +
                            0.100000*np.tanh(((((((np.where((13.89030170440673828) > -998, ((data["minbatch_slices2_msignal"]) * 2.0), data["abs_maxbatch"] )) * 2.0)) + ((13.89030170440673828)))) * 2.0)) +
                            0.100000*np.tanh(((((np.where(data["rangebatch_slices2"] <= -998, (2.84804892539978027), np.where((2.84804892539978027) <= -998, data["minbatch_slices2_msignal"], np.where(data["minbatch_msignal"] <= -998, (13.71419143676757812), (2.84804892539978027) ) ) )) + (data["minbatch_slices2_msignal"]))) * ((2.84804892539978027)))) +
                            0.100000*np.tanh(np.where(((data["minbatch_msignal"]) + (((((data["minbatch_msignal"]) + ((3.36590838432312012)))) * 2.0))) <= -998, (3.36590480804443359), ((((data["minbatch_msignal"]) + ((3.36590838432312012)))) * 2.0) )) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) + (np.where(data["signal_shift_+1"] > -998, np.where(data["medianbatch_slices2"] > -998, data["rangebatch_slices2"], ((data["mean_abs_chgbatch_slices2"]) / 2.0) ), ((data["rangebatch_slices2"]) / 2.0) )))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) + (np.where(((data["rangebatch_slices2"]) / 2.0) > -998, data["signal"], ((((data["signal"]) * 2.0)) / 2.0) )))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((data["minbatch_msignal"]) + ((((((((8.0)) + ((((data["minbatch_msignal"]) + ((4.0)))/2.0)))/2.0)) + ((9.77750873565673828)))/2.0)))))) +
                            0.100000*np.tanh(((np.where(data["minbatch_slices2_msignal"] <= -998, data["signal_shift_+1"], ((((data["meanbatch_slices2"]) - (data["minbatch_slices2_msignal"]))) * 2.0) )) - (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((np.where(data["abs_avgbatch_msignal"] > -998, (((8.0)) - (((data["minbatch_msignal"]) * (data["minbatch_msignal"])))), (3.0) )) * 2.0)) +
                            0.100000*np.tanh((((5.83992528915405273)) - (np.where(data["rangebatch_slices2"] > -998, data["rangebatch_slices2"], (5.83992862701416016) )))) +
                            0.100000*np.tanh((((((-((data["minbatch_slices2_msignal"])))) - (np.tanh(((3.0)))))) * ((((3.0)) + (((data["minbatch_slices2_msignal"]) + (((data["minbatch_slices2_msignal"]) + ((3.0)))))))))) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) + (np.where(data["abs_maxbatch_msignal"] <= -998, (6.0), ((np.where(data["signal_shift_+1"] > -998, (6.0), (6.0) )) / 2.0) )))) * 2.0)) +
                            0.100000*np.tanh(np.where((((((data["abs_avgbatch_slices2"]) - (((data["rangebatch_slices2"]) - (data["abs_maxbatch_slices2"]))))) + (data["rangebatch_slices2"]))/2.0) <= -998, data["rangebatch_slices2"], ((((data["minbatch_slices2"]) * 2.0)) - (data["abs_minbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(np.where(((((((((data["minbatch_msignal"]) + ((3.70837664604187012)))) + ((3.70837664604187012)))) * 2.0)) * 2.0) > -998, ((((data["minbatch_slices2_msignal"]) + ((3.70837664604187012)))) * 2.0), data["minbatch_msignal"] )) +
                            0.100000*np.tanh((((np.where(data["signal_shift_+1"] <= -998, data["maxbatch_slices2"], (11.30395126342773438) )) + ((((((((data["maxbatch_slices2"]) - (data["rangebatch_slices2"]))) + (data["abs_maxbatch_slices2"]))/2.0)) + (((data["minbatch_msignal"]) * (data["rangebatch_slices2"]))))))/2.0)) +
                            0.100000*np.tanh((((10.44334125518798828)) + (np.where((10.44334125518798828) <= -998, (10.44334125518798828), ((((((data["signal"]) + (((data["maxtominbatch_slices2"]) / 2.0)))) * (data["stdbatch_slices2_msignal"]))) * 2.0) )))) +
                            0.100000*np.tanh((((5.0)) + (np.where(data["abs_maxbatch"] > -998, data["minbatch_msignal"], (5.0) )))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) + (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(data["medianbatch_slices2"]) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * (data["maxtominbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where((6.28817224502563477) <= -998, np.where((6.28817605972290039) <= -998, (((6.28817224502563477)) + ((5.45574331283569336))), data["minbatch_slices2_msignal"] ), ((((data["minbatch_slices2_msignal"]) + ((((6.28817224502563477)) / 2.0)))) * 2.0) )) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) - ((-((data["maxtominbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh((4.0)) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((((5.56805992126464844)) + (data["minbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(((data["minbatch_slices2"]) - (data["rangebatch_msignal"]))) +
                            0.100000*np.tanh(((((((((((data["maxtominbatch_msignal"]) * (data["stdbatch_msignal"]))) * (data["rangebatch_slices2_msignal"]))) + (data["maxtominbatch"]))) * (data["rangebatch_slices2_msignal"]))) * (data["abs_minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) * (((data["maxtominbatch"]) + (((data["maxtominbatch"]) + (((data["meanbatch_slices2"]) - (np.where(((data["minbatch_msignal"]) - (data["maxtominbatch"])) > -998, data["minbatch_msignal"], data["maxtominbatch_msignal"] )))))))))) +
                            0.100000*np.tanh((((np.where(data["abs_maxbatch"] > -998, data["abs_maxbatch_slices2"], data["maxbatch_msignal"] )) + (np.tanh(((10.0)))))/2.0)) +
                            0.100000*np.tanh(((((((np.where(data["minbatch_slices2_msignal"] > -998, data["minbatch_msignal"], ((np.where(data["stdbatch_slices2_msignal"] > -998, data["minbatch_msignal"], data["stdbatch_slices2_msignal"] )) + ((3.0))) )) + ((3.0)))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((((((4.0)) - (data["rangebatch_slices2"]))) * (((((data["signal"]) - (data["maxbatch_msignal"]))) + (data["rangebatch_slices2"]))))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) - (np.where((2.0) > -998, data["maxtominbatch"], np.where((2.0) > -998, data["meanbatch_slices2_msignal"], data["signal"] ) )))) +
                            0.100000*np.tanh((((((data["minbatch_msignal"]) + (np.where(((((4.59522247314453125)) + (np.where(data["minbatch_msignal"] > -998, (4.59522247314453125), (4.59522247314453125) )))/2.0) > -998, (4.59522247314453125), data["abs_maxbatch_msignal"] )))/2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] <= -998, ((data["abs_maxbatch_slices2"]) + ((8.29026985168457031))), ((data["abs_maxbatch"]) + (((data["abs_maxbatch_slices2"]) + ((4.05078029632568359))))) )) +
                            0.100000*np.tanh(np.where((((10.0)) * (data["minbatch_slices2_msignal"])) <= -998, data["minbatch_slices2_msignal"], (((10.0)) - ((((-((data["rangebatch_slices2"])))) * (data["minbatch_slices2_msignal"])))) )) +
                            0.100000*np.tanh(((data["maxtominbatch"]) + (((((data["mean_abs_chgbatch_slices2_msignal"]) - (data["maxtominbatch"]))) * (np.where(((data["medianbatch_slices2_msignal"]) + (data["abs_avgbatch_slices2_msignal"])) <= -998, data["meanbatch_slices2_msignal"], data["meanbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh((((7.93269920349121094)) - (((((data["rangebatch_slices2"]) - (np.where((7.93269586563110352) > -998, data["medianbatch_msignal"], data["rangebatch_slices2"] )))) * 2.0)))) +
                            0.100000*np.tanh(((((((data["abs_minbatch_msignal"]) * (data["medianbatch_slices2"]))) + (((data["abs_maxbatch"]) * 2.0)))) * ((8.0)))) +
                            0.100000*np.tanh(((np.where((2.05579924583435059) <= -998, data["minbatch"], (2.05579924583435059) )) - ((((data["minbatch_slices2_msignal"]) + ((((10.0)) * (((data["minbatch_slices2_msignal"]) + ((2.05579924583435059)))))))/2.0)))) +
                            0.100000*np.tanh(((((data["maxtominbatch_slices2_msignal"]) * (np.where(((data["stdbatch_msignal"]) + ((3.0))) > -998, data["abs_minbatch_msignal"], data["stdbatch_msignal"] )))) * 2.0)) +
                            0.100000*np.tanh(np.where((3.08704447746276855) > -998, (((((((((((data["minbatch_msignal"]) + ((3.08704447746276855)))/2.0)) * 2.0)) * 2.0)) * 2.0)) * 2.0), np.tanh(((((((data["minbatch_msignal"]) + ((3.08704447746276855)))/2.0)) * 2.0))) )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (((data["maxtominbatch"]) - (np.where(data["maxtominbatch_msignal"] > -998, np.where(data["abs_maxbatch_slices2"] > -998, data["minbatch_msignal"], data["minbatch_msignal"] ), (-((data["minbatch_msignal"]))) )))))) +
                            0.100000*np.tanh((4.0)) +
                            0.100000*np.tanh(np.where((((4.0)) / 2.0) > -998, (((4.0)) + (data["minbatch_slices2_msignal"])), ((data["medianbatch_msignal"]) * (((data["minbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"])))) )) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * (np.where(((data["abs_avgbatch_msignal"]) - (np.where(np.where(data["maxtominbatch_slices2_msignal"] > -998, data["medianbatch_slices2_msignal"], data["maxtominbatch_slices2"] ) > -998, data["maxtominbatch_msignal"], data["abs_maxbatch_slices2"] ))) > -998, data["stdbatch_slices2_msignal"], data["stdbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((((9.0)) + (data["minbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh(((np.where((((5.0)) + ((5.0))) > -998, (((4.0)) + (data["minbatch_msignal"])), ((((data["minbatch_msignal"]) * 2.0)) * 2.0) )) * 2.0)) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2_msignal"] > -998, data["medianbatch_slices2_msignal"], ((((((data["signal_shift_-1"]) + (np.where(data["medianbatch_slices2_msignal"] <= -998, data["signal_shift_+1_msignal"], (8.0) )))/2.0)) + (data["medianbatch_slices2_msignal"]))/2.0) )) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, data["abs_maxbatch_slices2"], ((data["medianbatch_slices2_msignal"]) * 2.0) )) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * ((((data["maxtominbatch_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0)))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where(np.where(data["maxtominbatch_slices2"] <= -998, ((data["abs_avgbatch_msignal"]) * 2.0), (-((((data["signal_shift_+1_msignal"]) / 2.0)))) ) > -998, ((data["minbatch_slices2_msignal"]) + ((5.0))), data["signal_shift_+1_msignal"] )))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(np.where(((data["minbatch_msignal"]) + (data["minbatch_slices2_msignal"])) > -998, ((data["minbatch_msignal"]) + ((4.45129871368408203))), ((data["minbatch_msignal"]) + (((data["minbatch_msignal"]) + ((4.45129871368408203))))) )) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) * (data["stdbatch_msignal"]))) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) + (((((data["rangebatch_slices2_msignal"]) * (((data["medianbatch_msignal"]) / 2.0)))) / 2.0)))) +
                            0.100000*np.tanh(np.where((2.94744443893432617) <= -998, (2.94744443893432617), ((np.tanh((data["stdbatch_msignal"]))) * (data["stdbatch_msignal"])) )) +
                            0.100000*np.tanh((((((4.36138010025024414)) - (((np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["maxbatch_slices2_msignal"], data["abs_maxbatch_slices2"] )) * ((4.36138010025024414)))))) + ((((data["signal_shift_+1_msignal"]) + (data["abs_maxbatch"]))/2.0)))) +
                            0.100000*np.tanh(np.where((5.0) <= -998, np.where((5.0) <= -998, (((5.0)) + (data["minbatch_slices2_msignal"])), (((5.0)) + (data["rangebatch_slices2_msignal"])) ), (((5.0)) + (data["minbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_slices2"] > -998, np.where(np.where(data["medianbatch_slices2_msignal"] > -998, data["maxtominbatch"], data["medianbatch_slices2_msignal"] ) > -998, data["medianbatch_msignal"], data["medianbatch_msignal"] ), data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(((((data["medianbatch_slices2_msignal"]) * (((((data["abs_minbatch_slices2_msignal"]) + (((data["abs_avgbatch_slices2_msignal"]) / 2.0)))) * (data["medianbatch_slices2_msignal"]))))) * 2.0) <= -998, ((data["medianbatch_slices2_msignal"]) / 2.0), data["medianbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((np.where(data["maxbatch_slices2"] > -998, (13.93287754058837891), data["meanbatch_slices2"] )) + (((data["rangebatch_slices2_msignal"]) * (((((data["stdbatch_msignal"]) - (((data["abs_maxbatch"]) + (data["maxtominbatch_slices2"]))))) * 2.0)))))/2.0)) +
                            0.100000*np.tanh(((np.where(data["maxbatch_slices2"] <= -998, data["rangebatch_slices2"], ((data["abs_avgbatch_slices2_msignal"]) + (((data["abs_maxbatch_slices2"]) + (((data["signal_shift_+1"]) * (data["abs_avgbatch_slices2_msignal"])))))) )) * 2.0)) +
                            0.100000*np.tanh(np.where(np.where(data["abs_avgbatch_slices2_msignal"] <= -998, data["abs_avgbatch_msignal"], data["abs_avgbatch_slices2_msignal"] ) <= -998, data["rangebatch_slices2"], data["abs_avgbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) * (data["maxtominbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) * (np.where(((data["maxtominbatch_slices2_msignal"]) * (data["maxtominbatch_slices2_msignal"])) <= -998, ((data["mean_abs_chgbatch_slices2_msignal"]) + (((data["abs_maxbatch_msignal"]) / 2.0))), ((data["maxtominbatch_slices2"]) + (data["abs_maxbatch_slices2"])) )))) +
                            0.100000*np.tanh((((((np.where(data["abs_minbatch_msignal"] <= -998, ((data["abs_minbatch_slices2_msignal"]) - ((((3.73890733718872070)) / 2.0))), data["minbatch_slices2_msignal"] )) + ((3.73890733718872070)))/2.0)) * 2.0)) +
                            0.100000*np.tanh((((((data["maxtominbatch_msignal"]) + (data["maxtominbatch_msignal"]))/2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["stdbatch_slices2"]) + (data["abs_avgbatch_slices2"]))) +
                            0.100000*np.tanh((7.0)) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2_msignal"] > -998, data["abs_avgbatch_msignal"], data["signal_shift_+1_msignal"] )) +
                            0.100000*np.tanh((14.45354843139648438)) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) - ((((((data["maxtominbatch"]) / 2.0)) + (((data["medianbatch_slices2_msignal"]) * (((((np.where((-((data["minbatch"]))) <= -998, data["abs_minbatch_slices2"], data["abs_avgbatch_slices2_msignal"] )) / 2.0)) / 2.0)))))/2.0)))) +
                            0.100000*np.tanh((((((3.0)) + (np.where((3.0) <= -998, (((-((((data["minbatch_msignal"]) * 2.0))))) * 2.0), data["minbatch_msignal"] )))) * (((data["maxtominbatch_msignal"]) + ((8.19196128845214844)))))) +
                            0.100000*np.tanh(((data["abs_maxbatch"]) - (np.tanh((((data["stdbatch_slices2"]) / 2.0)))))) +
                            0.100000*np.tanh(np.where(((data["signal_shift_-1_msignal"]) * 2.0) > -998, data["signal_shift_+1_msignal"], data["signal_shift_-1_msignal"] )) +
                            0.100000*np.tanh(((((data["maxtominbatch_slices2_msignal"]) * (((np.where(data["abs_minbatch_msignal"] <= -998, (6.0), data["abs_maxbatch_slices2"] )) + ((((data["maxtominbatch"]) + (data["maxtominbatch_slices2_msignal"]))/2.0)))))) + ((6.0)))) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) * (((np.tanh((data["maxbatch_slices2_msignal"]))) + (((data["maxbatch_slices2_msignal"]) * (((data["abs_avgbatch_msignal"]) + (data["minbatch"]))))))))) +
                            0.100000*np.tanh(np.tanh(((((-((((data["abs_avgbatch_slices2"]) + (data["meanbatch_slices2_msignal"])))))) * 2.0)))) +
                            0.100000*np.tanh((((-(((((((((data["rangebatch_slices2"]) + (data["maxbatch_slices2_msignal"]))/2.0)) * (data["maxbatch_slices2_msignal"]))) * (data["maxbatch_slices2_msignal"])))))) + (np.where(data["rangebatch_slices2"] > -998, (5.86559200286865234), data["rangebatch_slices2"] )))) +
                            0.100000*np.tanh((((5.0)) + (np.where(data["mean_abs_chgbatch_msignal"] > -998, data["minbatch_msignal"], ((data["minbatch_msignal"]) + (np.where(data["mean_abs_chgbatch_msignal"] > -998, data["minbatch_msignal"], data["minbatch_msignal"] ))) )))) +
                            0.100000*np.tanh((2.0)) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] <= -998, data["medianbatch_msignal"], data["abs_avgbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) + (((data["abs_maxbatch_msignal"]) * (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh((((((((((4.0)) * (np.tanh(((((4.0)) * ((((((4.0)) + (data["minbatch_msignal"]))) * 2.0)))))))) + (data["minbatch_msignal"]))) * 2.0)) * ((4.0)))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2"]) + (((data["maxbatch_slices2_msignal"]) * (data["medianbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((11.09516429901123047)) + (((((data["minbatch_slices2_msignal"]) * (data["rangebatch_slices2"]))) - (((data["minbatch_slices2_msignal"]) + ((-((data["minbatch_slices2_msignal"])))))))))))
    
    def GP_class_2(self,data):
        return self.Output(-2.200047 +
                            0.100000*np.tanh(np.where(np.tanh((data["maxbatch_slices2"])) <= -998, data["meanbatch_slices2"], ((data["abs_avgbatch_slices2_msignal"]) * (data["maxbatch_slices2"])) )) +
                            0.100000*np.tanh(((((((data["maxbatch_slices2"]) * 2.0)) * (np.where(data["rangebatch_msignal"] <= -998, ((np.tanh((data["maxbatch_slices2"]))) / 2.0), data["abs_avgbatch_msignal"] )))) - (data["abs_avgbatch_msignal"]))) +
                            0.100000*np.tanh(np.where((-((data["maxbatch_slices2"]))) <= -998, (((((data["maxtominbatch"]) / 2.0)) + (data["maxbatch_slices2"]))/2.0), ((data["abs_avgbatch_msignal"]) * (data["maxbatch_slices2"])) )) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) * (data["medianbatch_slices2_msignal"]))) + (((data["maxbatch_slices2"]) + (((((data["maxbatch_slices2"]) + (data["meanbatch_slices2_msignal"]))) * (((data["minbatch_msignal"]) + (data["rangebatch_msignal"]))))))))) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) * (np.where(data["maxbatch_slices2"] > -998, ((np.where(data["abs_maxbatch"] > -998, data["abs_avgbatch_msignal"], data["maxbatch_slices2"] )) * 2.0), ((data["maxbatch_slices2"]) * (data["stdbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(((np.where(data["maxbatch_slices2"] > -998, data["maxbatch_slices2"], data["signal_shift_+1_msignal"] )) * 2.0)) +
                            0.100000*np.tanh(np.where(data["meanbatch_msignal"] <= -998, ((data["meanbatch_msignal"]) * 2.0), ((((data["meanbatch_slices2_msignal"]) + (((data["meanbatch_msignal"]) + (data["meanbatch_slices2_msignal"]))))) * 2.0) )) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) + (((data["abs_minbatch_slices2_msignal"]) * (((data["signal"]) - (data["mean_abs_chgbatch_msignal"]))))))) +
                            0.100000*np.tanh(((((((data["meanbatch_msignal"]) * 2.0)) * (data["maxbatch_slices2"]))) + (((data["maxbatch_slices2"]) + (((data["maxbatch_slices2"]) / 2.0)))))) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) + (((((data["meanbatch_slices2"]) * 2.0)) * (np.where(((data["stdbatch_msignal"]) + (((data["maxtominbatch_slices2_msignal"]) * (data["abs_maxbatch_msignal"])))) <= -998, data["minbatch_slices2"], data["maxtominbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) * (((data["mean_abs_chgbatch_slices2_msignal"]) + (np.where(data["maxbatch_slices2"] > -998, ((data["abs_maxbatch_slices2"]) * (data["mean_abs_chgbatch_slices2_msignal"])), data["maxbatch_slices2"] )))))) +
                            0.100000*np.tanh(np.where(data["rangebatch_msignal"] > -998, data["maxbatch_slices2"], data["mean_abs_chgbatch_slices2"] )) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) * (data["maxbatch_slices2"]))) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) - (((np.where(np.where((((8.79133892059326172)) * 2.0) <= -998, data["medianbatch_slices2"], np.tanh((data["maxbatch_slices2_msignal"])) ) > -998, data["maxtominbatch"], data["meanbatch_slices2"] )) + (data["abs_avgbatch_slices2"]))))) +
                            0.100000*np.tanh(np.where((-((data["medianbatch_slices2"]))) > -998, np.where(data["abs_avgbatch_slices2"] > -998, data["maxbatch_slices2"], data["maxbatch_slices2"] ), np.where(data["maxbatch_slices2"] <= -998, data["maxbatch_slices2"], data["medianbatch_slices2"] ) )) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) * (((data["mean_abs_chgbatch_slices2_msignal"]) * (((((data["minbatch_msignal"]) * 2.0)) + (((data["maxbatch_slices2"]) + ((((((6.0)) + (data["minbatch_msignal"]))) * 2.0)))))))))) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2"] <= -998, np.tanh((data["minbatch_slices2"])), data["maxbatch_slices2"] )) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) * 2.0)) * (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) * (((data["maxtominbatch"]) + (data["rangebatch_slices2"]))))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_msignal"]) * (np.where(data["mean_abs_chgbatch_msignal"] <= -998, data["maxbatch_slices2"], np.where(data["rangebatch_slices2"] <= -998, data["maxtominbatch"], ((data["maxtominbatch"]) + (data["maxbatch_slices2"])) ) )))) * (data["maxbatch_slices2"]))) +
                            0.100000*np.tanh((((4.37047815322875977)) * ((((4.37047815322875977)) + (np.where(data["signal_shift_+1_msignal"] > -998, data["minbatch_msignal"], ((data["meanbatch_slices2"]) * 2.0) )))))) +
                            0.100000*np.tanh((((((data["abs_minbatch_msignal"]) + (data["rangebatch_slices2"]))) + (((data["rangebatch_slices2"]) * (((data["meanbatch_slices2_msignal"]) / 2.0)))))/2.0)) +
                            0.100000*np.tanh(((((np.where(data["mean_abs_chgbatch_slices2_msignal"] <= -998, data["mean_abs_chgbatch_msignal"], (10.0) )) * (data["mean_abs_chgbatch_slices2_msignal"]))) * (((data["maxtominbatch"]) + (((data["maxbatch_slices2"]) / 2.0)))))) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_msignal"] > -998, data["rangebatch_slices2_msignal"], np.where(((data["meanbatch_msignal"]) * 2.0) > -998, data["abs_minbatch_msignal"], ((((np.tanh((data["medianbatch_msignal"]))) * 2.0)) / 2.0) ) )) +
                            0.100000*np.tanh((-(((((((data["rangebatch_slices2"]) + (((((data["abs_maxbatch_msignal"]) / 2.0)) * 2.0)))/2.0)) + (((np.where(data["stdbatch_slices2_msignal"] > -998, data["meanbatch_slices2"], data["maxbatch_slices2"] )) - (data["meanbatch_msignal"])))))))) +
                            0.100000*np.tanh(((np.where(data["stdbatch_slices2_msignal"] > -998, data["abs_avgbatch_msignal"], data["mean_abs_chgbatch_msignal"] )) + (((data["signal"]) + (data["abs_avgbatch_slices2"]))))) +
                            0.100000*np.tanh(((((np.where(((data["meanbatch_slices2_msignal"]) - (data["maxbatch_msignal"])) <= -998, data["mean_abs_chgbatch_msignal"], (7.0) )) - (((data["maxbatch_msignal"]) - (data["minbatch"]))))) * 2.0)) +
                            0.100000*np.tanh(((data["signal"]) * (data["minbatch"]))) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) + (((data["medianbatch_slices2"]) / 2.0)))) +
                            0.100000*np.tanh((((-((np.where(data["mean_abs_chgbatch_msignal"] > -998, ((data["maxtominbatch_slices2_msignal"]) * (data["mean_abs_chgbatch_slices2_msignal"])), data["abs_maxbatch_msignal"] ))))) * 2.0)) +
                            0.100000*np.tanh(((np.tanh((((((((data["medianbatch_slices2_msignal"]) + (data["maxbatch_slices2_msignal"]))/2.0)) + (data["abs_avgbatch_msignal"]))/2.0)))) * (data["maxbatch_slices2"]))) +
                            0.100000*np.tanh(data["minbatch"]) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) - (((data["meanbatch_slices2_msignal"]) * (((np.where(data["maxbatch_slices2"] <= -998, data["meanbatch_slices2_msignal"], ((((data["meanbatch_slices2_msignal"]) * 2.0)) * 2.0) )) * (data["maxbatch_slices2"]))))))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) + (np.tanh((((data["abs_avgbatch_msignal"]) * 2.0)))))) + ((0.64695614576339722)))) +
                            0.100000*np.tanh(((np.where(((data["maxbatch_slices2"]) + (data["medianbatch_msignal"])) > -998, data["rangebatch_slices2_msignal"], data["medianbatch_slices2_msignal"] )) + (((data["signal"]) * (data["rangebatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) * ((((data["rangebatch_slices2_msignal"]) + (data["maxtominbatch_slices2"]))/2.0)))) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) - (((np.where((((((data["minbatch"]) * (data["medianbatch_slices2"]))) + (data["maxbatch_slices2"]))/2.0) > -998, data["abs_minbatch_slices2_msignal"], data["minbatch"] )) * (data["minbatch"]))))) +
                            0.100000*np.tanh(np.where(np.where(data["maxtominbatch_slices2_msignal"] <= -998, np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, data["abs_minbatch_msignal"], ((data["stdbatch_slices2_msignal"]) + (data["medianbatch_msignal"])) ), data["signal_shift_+1_msignal"] ) > -998, data["minbatch"], data["signal_shift_+1_msignal"] )) +
                            0.100000*np.tanh((((12.97694110870361328)) - (((data["rangebatch_slices2"]) - (np.where((12.97694110870361328) <= -998, ((data["minbatch_slices2_msignal"]) / 2.0), (-((((data["minbatch_slices2_msignal"]) * (((data["minbatch_slices2_msignal"]) / 2.0)))))) )))))) +
                            0.100000*np.tanh((((5.0)) + (np.where(data["signal_shift_-1"] <= -998, np.where(data["stdbatch_slices2"] <= -998, (-((np.where((4.0) > -998, data["signal_shift_-1"], (5.0) )))), data["mean_abs_chgbatch_msignal"] ), data["minbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_msignal"] <= -998, data["maxtominbatch_msignal"], ((data["maxtominbatch_msignal"]) * (np.where(data["meanbatch_slices2"] > -998, data["minbatch_slices2"], data["meanbatch_slices2"] ))) )) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2"] <= -998, (3.55061626434326172), ((np.where(((np.where(data["abs_avgbatch_msignal"] > -998, (3.55061626434326172), data["mean_abs_chgbatch_slices2_msignal"] )) + (data["medianbatch_slices2_msignal"])) <= -998, data["minbatch_slices2_msignal"], data["minbatch_slices2_msignal"] )) + ((4.0))) )) +
                            0.100000*np.tanh(np.where(((data["abs_maxbatch_msignal"]) + (data["minbatch_msignal"])) > -998, ((data["abs_maxbatch_msignal"]) + (data["minbatch_msignal"])), data["abs_maxbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((-((((data["minbatch_slices2_msignal"]) - (((data["mean_abs_chgbatch_slices2"]) - (((((data["stdbatch_slices2_msignal"]) - (((data["rangebatch_msignal"]) - (data["meanbatch_slices2"]))))) / 2.0))))))))) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2_msignal"] > -998, data["maxbatch_slices2"], ((data["abs_maxbatch_slices2_msignal"]) * 2.0) )) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) - (data["maxtominbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2_msignal"]) + (((data["maxtominbatch_msignal"]) + (data["stdbatch_msignal"]))))) + (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(((np.where(np.tanh((((data["maxbatch_slices2_msignal"]) / 2.0))) > -998, data["minbatch"], ((((data["maxbatch_slices2"]) * 2.0)) - (np.tanh((data["minbatch"])))) )) + (data["stdbatch_slices2"]))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - (np.where(data["abs_avgbatch_slices2"] > -998, ((data["medianbatch_msignal"]) * (((data["maxbatch_slices2"]) * (data["maxbatch_slices2"])))), data["medianbatch_msignal"] )))) +
                            0.100000*np.tanh((((5.0)) + (data["minbatch_msignal"]))) +
                            0.100000*np.tanh(((np.where(data["signal_shift_+1"] <= -998, data["medianbatch_slices2_msignal"], ((data["signal"]) - ((((data["abs_minbatch_msignal"]) + (data["minbatch_msignal"]))/2.0))) )) * (data["abs_avgbatch_msignal"]))) +
                            0.100000*np.tanh((-((((data["maxtominbatch_msignal"]) * (data["abs_minbatch_msignal"])))))) +
                            0.100000*np.tanh(np.where((((6.20770597457885742)) - ((((6.20770597457885742)) - (data["maxbatch_msignal"])))) > -998, (((((6.20770597457885742)) - (data["maxbatch_msignal"]))) * 2.0), data["maxbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((((-((data["maxtominbatch"])))) * (((((data["meanbatch_msignal"]) + (((((data["abs_minbatch_slices2_msignal"]) + ((-((data["maxtominbatch"])))))) * 2.0)))) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (np.where(data["medianbatch_slices2_msignal"] > -998, (-((np.where(data["maxtominbatch_msignal"] > -998, data["medianbatch_slices2_msignal"], ((((((data["mean_abs_chgbatch_msignal"]) + (data["rangebatch_msignal"]))/2.0)) + (data["maxbatch_slices2"]))/2.0) )))), data["abs_maxbatch_msignal"] )))) +
                            0.100000*np.tanh(((((((data["abs_avgbatch_msignal"]) / 2.0)) * ((((9.20713138580322266)) * ((((9.20713138580322266)) + ((-((data["rangebatch_msignal"])))))))))) * (((data["rangebatch_msignal"]) / 2.0)))) +
                            0.100000*np.tanh((((np.where(np.tanh((data["mean_abs_chgbatch_msignal"])) > -998, np.where(data["abs_avgbatch_msignal"] <= -998, data["meanbatch_slices2"], data["signal_shift_-1"] ), data["minbatch_slices2_msignal"] )) + (data["meanbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh((((9.0)) - ((-((((data["minbatch_msignal"]) + (((data["minbatch_msignal"]) - (((((data["mean_abs_chgbatch_slices2"]) / 2.0)) * (((data["abs_maxbatch_slices2_msignal"]) / 2.0))))))))))))) +
                            0.100000*np.tanh((-((((data["maxtominbatch_slices2"]) - (np.where(data["abs_maxbatch_slices2_msignal"] <= -998, (-((data["signal_shift_+1"]))), ((data["abs_minbatch_slices2_msignal"]) * 2.0) ))))))) +
                            0.100000*np.tanh((((((6.0)) / 2.0)) + (((data["medianbatch_slices2_msignal"]) - (((((np.where(data["maxbatch_msignal"] <= -998, data["maxbatch_msignal"], data["medianbatch_slices2_msignal"] )) * (data["medianbatch_slices2_msignal"]))) * ((6.93181657791137695)))))))) +
                            0.100000*np.tanh(np.where(np.where((((data["maxbatch_slices2_msignal"]) + (data["minbatch_msignal"]))/2.0) <= -998, (6.0), (6.0) ) <= -998, data["stdbatch_slices2"], (((((6.0)) + (data["minbatch_msignal"]))) - (data["stdbatch_slices2"])) )) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_slices2_msignal"] <= -998, data["abs_avgbatch_msignal"], ((np.where(data["stdbatch_msignal"] <= -998, data["abs_maxbatch_slices2_msignal"], ((((((6.0)) + (data["minbatch_msignal"]))/2.0)) * 2.0) )) - (data["meanbatch_msignal"])) )) +
                            0.100000*np.tanh(((((data["stdbatch_slices2_msignal"]) + (data["maxtominbatch"]))) * ((((data["stdbatch_slices2_msignal"]) + (((data["abs_maxbatch_msignal"]) + (((data["maxtominbatch"]) + (data["abs_avgbatch_msignal"]))))))/2.0)))) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) + (np.where(data["medianbatch_slices2"] > -998, data["maxtominbatch_msignal"], np.where((((data["mean_abs_chgbatch_slices2_msignal"]) + ((((data["maxtominbatch_msignal"]) + (data["stdbatch_msignal"]))/2.0)))/2.0) <= -998, data["rangebatch_slices2"], data["abs_minbatch_slices2"] ) )))) +
                            0.100000*np.tanh((((((((((10.53426837921142578)) - (data["rangebatch_slices2"]))) + (data["minbatch_slices2_msignal"]))) * (((data["meanbatch_slices2"]) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) + (((data["medianbatch_slices2"]) + (data["meanbatch_msignal"]))))) +
                            0.100000*np.tanh(((np.where(data["abs_maxbatch_msignal"] > -998, data["stdbatch_slices2"], (-((((data["signal"]) * (data["meanbatch_msignal"]))))) )) - (((data["medianbatch_slices2_msignal"]) * (((data["abs_maxbatch_msignal"]) * (data["medianbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) * (np.where(data["abs_maxbatch_slices2_msignal"] > -998, ((data["abs_maxbatch_msignal"]) * ((((7.0)) + (((data["minbatch_msignal"]) + (data["abs_minbatch_msignal"])))))), (7.0) )))) +
                            0.100000*np.tanh((((data["maxbatch_slices2"]) + (data["maxbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) / 2.0)) +
                            0.100000*np.tanh((((np.where(data["mean_abs_chgbatch_msignal"] <= -998, data["abs_avgbatch_msignal"], data["meanbatch_msignal"] )) + (((data["medianbatch_msignal"]) + (((((data["maxbatch_slices2"]) / 2.0)) * ((-(((-((((data["mean_abs_chgbatch_slices2"]) / 2.0)))))))))))))/2.0)) +
                            0.100000*np.tanh((((((data["maxbatch_slices2"]) + (data["medianbatch_msignal"]))/2.0)) - (np.where(((data["medianbatch_msignal"]) * (data["maxbatch_slices2"])) <= -998, data["medianbatch_msignal"], ((data["medianbatch_msignal"]) * (((data["medianbatch_msignal"]) * (data["maxbatch_slices2"])))) )))) +
                            0.100000*np.tanh(((((5.38583040237426758)) + (np.where(np.where((((data["abs_avgbatch_msignal"]) + (data["signal_shift_-1"]))/2.0) > -998, data["signal_shift_-1"], data["minbatch_slices2_msignal"] ) <= -998, ((data["abs_minbatch_msignal"]) / 2.0), data["minbatch_slices2_msignal"] )))/2.0)) +
                            0.100000*np.tanh(np.where(np.where(data["minbatch_slices2_msignal"] <= -998, data["abs_avgbatch_msignal"], data["abs_avgbatch_msignal"] ) > -998, data["abs_avgbatch_msignal"], np.where(data["medianbatch_slices2_msignal"] > -998, data["abs_avgbatch_slices2"], data["abs_avgbatch_msignal"] ) )) +
                            0.100000*np.tanh(((((data["abs_avgbatch_msignal"]) * (data["maxbatch_slices2_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(((data["maxtominbatch"]) * (np.where(data["meanbatch_msignal"] > -998, data["medianbatch_slices2_msignal"], np.where(data["maxtominbatch"] > -998, data["maxbatch_slices2"], data["meanbatch_msignal"] ) )))) +
                            0.100000*np.tanh(((data["rangebatch_msignal"]) * ((((6.15587139129638672)) - (np.where(data["minbatch"] > -998, np.where(np.tanh((data["maxbatch_slices2_msignal"])) > -998, data["abs_maxbatch_msignal"], (6.15587139129638672) ), data["abs_maxbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh((-((((((data["maxbatch_msignal"]) + (np.where((7.0) > -998, (7.0), (((data["maxbatch_slices2"]) + (data["maxbatch_msignal"]))/2.0) )))) - (((data["maxbatch_msignal"]) * (data["rangebatch_slices2"])))))))) +
                            0.100000*np.tanh(((((((data["minbatch"]) + (data["medianbatch_slices2"]))) * (((data["abs_avgbatch_slices2_msignal"]) * ((((data["minbatch"]) + (data["meanbatch_slices2"]))/2.0)))))) + (((((data["minbatch"]) + (data["meanbatch_slices2"]))) * 2.0)))) +
                            0.100000*np.tanh(((np.where((-((np.where(data["rangebatch_slices2"] <= -998, (6.59240961074829102), (7.22993946075439453) )))) > -998, (6.59240961074829102), (-(((6.59240961074829102)))) )) - (np.where((6.59240961074829102) > -998, data["rangebatch_slices2"], data["rangebatch_slices2"] )))) +
                            0.100000*np.tanh((((data["abs_avgbatch_msignal"]) + (data["meanbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + ((((-((data["stdbatch_slices2_msignal"])))) + (((((((data["minbatch_msignal"]) + ((5.47259473800659180)))) * 2.0)) * 2.0)))))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2"] > -998, (((((data["maxtominbatch"]) + (data["signal_shift_-1"]))/2.0)) * (data["maxtominbatch_slices2_msignal"])), np.where(data["signal_shift_-1"] <= -998, (-((data["signal_shift_-1"]))), data["stdbatch_msignal"] ) )) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, data["abs_avgbatch_msignal"], ((data["abs_avgbatch_slices2"]) - (((data["meanbatch_slices2_msignal"]) * (data["abs_avgbatch_msignal"])))) )) +
                            0.100000*np.tanh(((((data["abs_avgbatch_msignal"]) / 2.0)) + (data["abs_avgbatch_slices2"]))) +
                            0.100000*np.tanh(np.where(np.where(np.tanh((data["meanbatch_msignal"])) <= -998, ((data["mean_abs_chgbatch_msignal"]) * (data["meanbatch_msignal"])), data["maxtominbatch_msignal"] ) <= -998, data["signal"], ((((data["maxtominbatch_msignal"]) + (data["medianbatch_msignal"]))) + (data["maxtominbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh((((6.0)) * ((((-((((data["abs_maxbatch_slices2_msignal"]) / 2.0))))) + (((np.where(data["abs_maxbatch_slices2_msignal"] > -998, (6.0), data["medianbatch_msignal"] )) + (data["minbatch_msignal"]))))))) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2_msignal"] > -998, data["abs_avgbatch_msignal"], np.where(data["maxtominbatch"] <= -998, data["rangebatch_msignal"], np.where(data["rangebatch_slices2_msignal"] > -998, data["meanbatch_slices2_msignal"], data["abs_minbatch_slices2"] ) ) )) +
                            0.100000*np.tanh(((np.where(data["maxbatch_msignal"] > -998, data["meanbatch_slices2"], (5.99081182479858398) )) * ((((5.99081182479858398)) - (np.where(data["meanbatch_slices2"] > -998, data["maxbatch_msignal"], (5.99081182479858398) )))))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) - ((-((np.where((-((np.where(data["minbatch_msignal"] <= -998, (5.0), (5.0) )))) <= -998, data["minbatch_msignal"], (5.0) ))))))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2"]) * (((data["abs_maxbatch_slices2"]) * ((((np.where(data["medianbatch_msignal"] > -998, data["mean_abs_chgbatch_slices2"], data["mean_abs_chgbatch_slices2"] )) + (((((data["medianbatch_msignal"]) * 2.0)) * ((-((data["medianbatch_msignal"])))))))/2.0)))))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2"]) / 2.0)) * (np.where(((data["meanbatch_slices2"]) / 2.0) > -998, np.where(data["signal"] > -998, data["signal_shift_-1_msignal"], data["signal_shift_+1_msignal"] ), np.tanh((((data["stdbatch_slices2"]) / 2.0))) )))) +
                            0.100000*np.tanh(((data["stdbatch_slices2_msignal"]) * (np.where((-((((data["abs_avgbatch_msignal"]) - (data["maxtominbatch"]))))) <= -998, ((((((((data["stdbatch_msignal"]) * 2.0)) * (data["meanbatch_msignal"]))) * 2.0)) * 2.0), data["medianbatch_msignal"] )))) +
                            0.100000*np.tanh((((((4.0)) * (((((data["minbatch_msignal"]) + ((4.0)))) * 2.0)))) * (((data["maxbatch_msignal"]) + ((-(((((4.0)) + (data["minbatch_msignal"])))))))))) +
                            0.100000*np.tanh((((data["minbatch_msignal"]) + ((5.72789096832275391)))/2.0)) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] > -998, data["meanbatch_slices2"], np.where(((np.tanh((data["meanbatch_slices2"]))) + (np.tanh((data["maxbatch_slices2_msignal"])))) > -998, data["meanbatch_slices2"], ((data["meanbatch_slices2"]) / 2.0) ) )) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) + (((data["abs_maxbatch_slices2"]) - (np.where(data["abs_avgbatch_slices2_msignal"] > -998, (3.43759489059448242), np.where(data["abs_avgbatch_slices2_msignal"] > -998, (3.43759489059448242), (-((data["abs_maxbatch"]))) ) )))))) +
                            0.100000*np.tanh((((data["minbatch"]) + (data["abs_minbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh((((4.0)) + (((data["maxbatch_msignal"]) + (((data["maxbatch_msignal"]) - (data["abs_avgbatch_msignal"]))))))))    
    
    def GP_class_3(self,data):
        return self.Output(-2.013422 +
                            0.100000*np.tanh(((((((data["signal"]) * 2.0)) * 2.0)) + (data["signal"]))) +
                            0.100000*np.tanh(((((((data["signal"]) * 2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(data["signal"] <= -998, np.where(data["signal"] > -998, data["signal"], data["signal"] ), ((((((data["signal"]) * 2.0)) * (data["stdbatch_msignal"]))) + (data["signal"])) )) +
                            0.100000*np.tanh(((((((np.where(data["maxbatch_slices2"] > -998, data["signal_shift_+1"], data["maxtominbatch_msignal"] )) * 2.0)) - (data["maxtominbatch_msignal"]))) - (data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["signal"] > -998, ((data["signal"]) + (((data["signal"]) * 2.0))), data["maxbatch_msignal"] )) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(((((((((data["signal"]) * 2.0)) * 2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["signal"]) + (((((data["abs_maxbatch_slices2_msignal"]) * (data["stdbatch_msignal"]))) * (data["medianbatch_slices2"]))))) +
                            0.100000*np.tanh(np.where((((6.0)) * 2.0) > -998, ((((data["minbatch"]) / 2.0)) * (data["maxtominbatch_slices2_msignal"])), (((((data["minbatch_slices2"]) * 2.0)) + (((data["maxtominbatch_slices2_msignal"]) * (np.tanh((data["rangebatch_slices2_msignal"]))))))/2.0) )) +
                            0.100000*np.tanh(((np.where(data["abs_maxbatch"] <= -998, ((data["abs_maxbatch_msignal"]) * (data["abs_avgbatch_slices2_msignal"])), np.tanh((data["signal"])) )) + (((data["signal"]) * (data["mean_abs_chgbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1"] > -998, np.where((((8.52326107025146484)) / 2.0) > -998, data["signal"], data["signal"] ), ((data["signal"]) / 2.0) )) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) + (((data["mean_abs_chgbatch_slices2_msignal"]) * (data["stdbatch_slices2"]))))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2_msignal"]) * (((data["abs_minbatch_msignal"]) * (data["minbatch"]))))) - (data["maxtominbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((-((np.where(data["rangebatch_slices2"] > -998, data["rangebatch_slices2"], (((-((np.tanh(((9.0))))))) + ((9.0))) ))))) + ((9.0)))) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_msignal"] > -998, ((data["meanbatch_msignal"]) * (((data["maxtominbatch"]) + (((((data["medianbatch_slices2"]) * 2.0)) + (np.tanh((data["meanbatch_msignal"])))))))), data["signal"] )) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2_msignal"]) - (data["minbatch_slices2"]))) * (data["signal_shift_-1"]))) +
                            0.100000*np.tanh(((data["signal"]) * (((((np.where((-(((10.16006755828857422)))) <= -998, (-((data["signal"]))), (-((data["rangebatch_slices2"]))) )) - ((-(((10.16006374359130859))))))) * ((10.16006374359130859)))))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * ((((data["maxtominbatch"]) + (np.where(data["maxtominbatch_msignal"] > -998, (((data["meanbatch_slices2"]) + (data["meanbatch_slices2"]))/2.0), ((data["meanbatch_slices2"]) + (data["meanbatch_slices2"])) )))/2.0)))) +
                            0.100000*np.tanh(((np.tanh((((data["abs_avgbatch_slices2_msignal"]) * ((((data["signal"]) + (((np.where(data["signal"] <= -998, ((data["maxbatch_msignal"]) * 2.0), ((data["abs_avgbatch_msignal"]) * (data["signal"])) )) * 2.0)))/2.0)))))) * 2.0)) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh(((((((7.78544616699218750)) + (data["rangebatch_slices2_msignal"]))/2.0)) * (np.where(data["minbatch"] > -998, ((data["maxtominbatch_slices2_msignal"]) - (data["minbatch"])), ((data["minbatch"]) - (((data["signal_shift_-1"]) - (data["minbatch"])))) )))) +
                            0.100000*np.tanh((((((((data["minbatch_msignal"]) * ((((-(((12.63433742523193359))))) - (((data["minbatch_msignal"]) * 2.0)))))) + (((data["minbatch_slices2_msignal"]) * 2.0)))/2.0)) * 2.0)) +
                            0.100000*np.tanh(((np.where(np.where(data["maxtominbatch_slices2"] > -998, data["maxtominbatch_slices2"], (-((data["signal_shift_+1_msignal"]))) ) <= -998, np.tanh((data["abs_minbatch_msignal"])), data["meanbatch_slices2_msignal"] )) * (((data["meanbatch_slices2"]) + (data["maxtominbatch_slices2"]))))) +
                            0.100000*np.tanh((((((((5.0)) - ((-((np.where(data["stdbatch_msignal"] > -998, data["minbatch_slices2_msignal"], (((5.0)) - (data["minbatch_slices2_msignal"])) ))))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((data["stdbatch_msignal"]) * (data["signal_shift_-1"]))) - (data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh(np.tanh((((data["medianbatch_slices2_msignal"]) * (((data["maxtominbatch"]) * (((data["abs_maxbatch_slices2_msignal"]) + (((data["minbatch_slices2"]) * (data["medianbatch_slices2"]))))))))))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2"]) + (data["mean_abs_chgbatch_msignal"]))) * (data["minbatch"]))) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) * (((((data["stdbatch_slices2_msignal"]) - (((data["signal_shift_+1"]) - (data["stdbatch_msignal"]))))) * (np.where(data["maxtominbatch_slices2"] <= -998, data["medianbatch_slices2_msignal"], data["maxbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * (np.where(data["abs_avgbatch_slices2"] <= -998, np.where((10.68740749359130859) > -998, data["minbatch"], data["minbatch"] ), ((data["abs_minbatch_slices2_msignal"]) * (((data["minbatch"]) + (data["medianbatch_slices2"])))) )))) +
                            0.100000*np.tanh(np.where(np.tanh((data["mean_abs_chgbatch_slices2_msignal"])) <= -998, (-(((-((data["medianbatch_slices2_msignal"])))))), data["maxtominbatch"] )) +
                            0.100000*np.tanh((((((((((7.0)) - (data["meanbatch_slices2"]))) * (((data["signal"]) * 2.0)))) * 2.0)) * (((data["minbatch_msignal"]) + ((7.0)))))) +
                            0.100000*np.tanh(((((data["maxtominbatch_slices2_msignal"]) + (np.where(data["maxtominbatch_slices2_msignal"] > -998, data["abs_maxbatch_slices2_msignal"], data["meanbatch_msignal"] )))) * (data["maxbatch_slices2"]))) +
                            0.100000*np.tanh(((((data["maxtominbatch_slices2"]) * (data["meanbatch_msignal"]))) - (data["maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) + (data["signal_shift_-1"]))) +
                            0.100000*np.tanh((((-(((-((data["mean_abs_chgbatch_msignal"]))))))) * (np.where(((data["stdbatch_slices2_msignal"]) * 2.0) > -998, data["signal_shift_-1"], data["stdbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((np.where((4.79668807983398438) > -998, (((4.79668807983398438)) - (data["maxbatch_slices2_msignal"])), (((((((data["signal_shift_+1"]) / 2.0)) + ((4.79668807983398438)))/2.0)) - (data["rangebatch_msignal"])) )) * (data["maxbatch_slices2"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (np.where((6.53165960311889648) <= -998, data["meanbatch_msignal"], np.where(data["medianbatch_msignal"] <= -998, data["medianbatch_slices2_msignal"], ((data["medianbatch_msignal"]) * 2.0) ) )))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * (((((data["medianbatch_msignal"]) * 2.0)) * 2.0)))) - (np.tanh((np.where(data["abs_maxbatch_msignal"] > -998, data["abs_maxbatch_slices2"], data["medianbatch_msignal"] )))))) +
                            0.100000*np.tanh(((((np.where(((data["meanbatch_msignal"]) - (data["minbatch"])) <= -998, data["signal_shift_-1"], ((data["mean_abs_chgbatch_slices2_msignal"]) - ((0.0))) )) - ((((data["maxtominbatch_slices2"]) + (data["meanbatch_msignal"]))/2.0)))) / 2.0)) +
                            0.100000*np.tanh((((((data["maxtominbatch"]) + (data["signal"]))/2.0)) * (((np.where(data["stdbatch_msignal"] > -998, data["maxtominbatch"], data["signal"] )) * 2.0)))) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) * (((np.where(data["stdbatch_slices2"] <= -998, data["stdbatch_msignal"], ((data["meanbatch_slices2"]) + ((((data["maxtominbatch"]) + (data["stdbatch_msignal"]))/2.0))) )) - (np.tanh((data["stdbatch_msignal"]))))))) +
                            0.100000*np.tanh(((((data["signal_shift_-1"]) * (((((data["medianbatch_msignal"]) * (data["maxtominbatch"]))) - (np.where(data["maxtominbatch"] > -998, data["signal"], data["signal_shift_+1"] )))))) - (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh((((((((4.0)) - (data["meanbatch_msignal"]))) * 2.0)) * ((((((4.0)) * ((((np.tanh((data["meanbatch_slices2_msignal"]))) + (data["mean_abs_chgbatch_slices2"]))/2.0)))) * (data["meanbatch_msignal"]))))) +
                            0.100000*np.tanh(((np.where(((((data["stdbatch_slices2"]) / 2.0)) + (data["rangebatch_msignal"])) <= -998, (-((((((np.tanh((data["stdbatch_slices2_msignal"]))) / 2.0)) * 2.0)))), data["stdbatch_msignal"] )) * 2.0)) +
                            0.100000*np.tanh((((((5.02029943466186523)) + (np.where(((((data["minbatch"]) * 2.0)) * ((((5.02029943466186523)) * (data["rangebatch_slices2"])))) > -998, ((data["minbatch"]) * (data["signal"])), data["medianbatch_msignal"] )))) * 2.0)) +
                            0.100000*np.tanh((((-((((data["abs_avgbatch_msignal"]) * (data["abs_avgbatch_msignal"])))))) * (data["minbatch_slices2"]))) +
                            0.100000*np.tanh((((6.0)) - (np.where(np.where(((data["minbatch_msignal"]) / 2.0) <= -998, (6.0), (6.0) ) <= -998, data["rangebatch_slices2"], (-((data["minbatch_msignal"]))) )))) +
                            0.100000*np.tanh(data["minbatch"]) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * (data["medianbatch_slices2_msignal"]))) * ((((data["rangebatch_slices2_msignal"]) + (((data["signal"]) - (((data["meanbatch_msignal"]) * (((data["medianbatch_msignal"]) * (data["maxbatch_msignal"]))))))))/2.0)))) +
                            0.100000*np.tanh(((np.where(data["abs_maxbatch_slices2_msignal"] <= -998, data["signal_shift_-1"], data["abs_minbatch_slices2"] )) - (((data["abs_maxbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] > -998, ((data["minbatch_slices2_msignal"]) - ((((-((data["minbatch_slices2_msignal"])))) - ((9.56960487365722656))))), (((data["signal"]) + ((-((data["medianbatch_msignal"])))))/2.0) )) +
                            0.100000*np.tanh(((data["minbatch"]) + ((((np.tanh((((np.where(np.tanh((data["mean_abs_chgbatch_msignal"])) > -998, data["abs_minbatch_slices2_msignal"], data["abs_maxbatch_msignal"] )) / 2.0)))) + (((data["meanbatch_msignal"]) * 2.0)))/2.0)))) +
                            0.100000*np.tanh(((np.where(((data["minbatch_msignal"]) + (data["minbatch_msignal"])) > -998, (2.82138061523437500), data["rangebatch_slices2_msignal"] )) - ((((-((data["minbatch_msignal"])))) - ((2.82138061523437500)))))) +
                            0.100000*np.tanh((((((((data["abs_minbatch_slices2"]) + (((data["minbatch_slices2_msignal"]) - ((-((data["maxtominbatch"])))))))) / 2.0)) + (((data["mean_abs_chgbatch_slices2_msignal"]) - ((((data["maxtominbatch"]) + (((data["abs_minbatch_msignal"]) / 2.0)))/2.0)))))/2.0)) +
                            0.100000*np.tanh(((((np.where(data["abs_maxbatch_slices2"] > -998, np.where(data["abs_avgbatch_msignal"] > -998, data["rangebatch_slices2"], ((((data["rangebatch_msignal"]) * 2.0)) * 2.0) ), ((data["abs_minbatch_slices2"]) * 2.0) )) - ((((2.0)) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(np.where(((((data["mean_abs_chgbatch_msignal"]) * (data["mean_abs_chgbatch_slices2"]))) / 2.0) > -998, ((data["mean_abs_chgbatch_msignal"]) * (data["minbatch"])), (((((7.0)) - (data["abs_maxbatch_slices2_msignal"]))) * (data["abs_avgbatch_msignal"])) )) +
                            0.100000*np.tanh(((np.where(data["meanbatch_msignal"] > -998, np.where(data["meanbatch_slices2"] > -998, data["meanbatch_msignal"], data["meanbatch_msignal"] ), data["meanbatch_slices2"] )) * (data["medianbatch_slices2"]))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2"] > -998, data["abs_minbatch_msignal"], data["mean_abs_chgbatch_msignal"] )) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) * (((data["abs_maxbatch_slices2_msignal"]) + (np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, data["minbatch_msignal"], np.tanh(((-((data["abs_maxbatch_slices2_msignal"]))))) )))))) +
                            0.100000*np.tanh(((((((data["meanbatch_slices2_msignal"]) * (((data["meanbatch_slices2"]) + ((((data["maxtominbatch_msignal"]) + (data["meanbatch_slices2"]))/2.0)))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(np.tanh((data["minbatch_msignal"])) <= -998, data["abs_minbatch_slices2"], (((9.0)) - ((-((((data["minbatch_msignal"]) - (((data["rangebatch_msignal"]) / 2.0)))))))) )) +
                            0.100000*np.tanh(np.where(((data["signal_shift_-1_msignal"]) - ((-((data["meanbatch_slices2_msignal"]))))) <= -998, data["stdbatch_slices2_msignal"], ((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])) )) +
                            0.100000*np.tanh(((data["minbatch"]) - (np.tanh((((data["minbatch_msignal"]) + (((((data["abs_maxbatch"]) * 2.0)) + (data["maxbatch_slices2_msignal"]))))))))) +
                            0.100000*np.tanh(((np.where(np.where(data["medianbatch_msignal"] <= -998, ((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])), ((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])) ) <= -998, data["meanbatch_msignal"], ((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])) )) * 2.0)) +
                            0.100000*np.tanh(np.where(((((data["abs_avgbatch_slices2_msignal"]) - (data["abs_maxbatch"]))) + ((6.0))) <= -998, (6.0), (((6.0)) * (((((6.0)) + (data["minbatch_msignal"]))/2.0))) )) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] > -998, data["minbatch_msignal"], (-((data["minbatch_slices2_msignal"]))) )) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * 2.0)) * (((((((np.tanh(((((0.65872925519943237)) * (data["medianbatch_slices2_msignal"]))))) * (((data["medianbatch_msignal"]) * 2.0)))) * (data["medianbatch_slices2_msignal"]))) * 2.0)))) +
                            0.100000*np.tanh(((((data["maxbatch_msignal"]) * (data["meanbatch_msignal"]))) - (((((data["abs_avgbatch_slices2_msignal"]) * (((data["meanbatch_msignal"]) * 2.0)))) * 2.0)))) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2"] > -998, ((data["mean_abs_chgbatch_msignal"]) - (data["maxtominbatch"])), data["mean_abs_chgbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] <= -998, np.tanh((np.where(np.where(data["maxtominbatch"] <= -998, data["abs_minbatch_slices2"], ((np.tanh((data["abs_minbatch_slices2"]))) / 2.0) ) <= -998, data["abs_maxbatch"], ((data["abs_maxbatch_slices2"]) * 2.0) ))), data["maxtominbatch"] )) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1"] > -998, ((data["medianbatch_slices2_msignal"]) * (((data["medianbatch_msignal"]) * 2.0))), np.where(data["maxbatch_slices2"] <= -998, np.tanh((((data["medianbatch_msignal"]) / 2.0))), np.tanh((data["rangebatch_msignal"])) ) )) +
                            0.100000*np.tanh(((((np.tanh((((data["medianbatch_slices2"]) * ((((((((data["medianbatch_msignal"]) + (data["medianbatch_msignal"]))/2.0)) * (data["medianbatch_msignal"]))) - (((data["meanbatch_msignal"]) * (data["medianbatch_msignal"]))))))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((((10.0)) * (np.where((((10.0)) / 2.0) > -998, (((((10.0)) / 2.0)) + (data["minbatch_msignal"])), (((10.0)) / 2.0) )))) +
                            0.100000*np.tanh(data["abs_avgbatch_msignal"]) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) + (((data["abs_avgbatch_msignal"]) * (((data["meanbatch_slices2"]) * ((-((((np.where(data["medianbatch_slices2"] > -998, data["abs_avgbatch_msignal"], data["abs_minbatch_slices2_msignal"] )) / 2.0))))))))))) +
                            0.100000*np.tanh((((-((np.where((((data["maxbatch_msignal"]) + (data["signal_shift_-1"]))/2.0) > -998, data["maxbatch_msignal"], data["minbatch_msignal"] ))))) * ((((data["maxbatch_msignal"]) + (data["minbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (np.where(((data["medianbatch_msignal"]) * (data["abs_minbatch_slices2"])) > -998, data["medianbatch_msignal"], ((data["medianbatch_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh((((9.12392902374267578)) - (np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["rangebatch_slices2"], np.where((((((data["rangebatch_slices2"]) * (data["rangebatch_slices2"]))) + (data["rangebatch_slices2"]))/2.0) <= -998, data["rangebatch_slices2"], data["rangebatch_slices2"] ) )))) +
                            0.100000*np.tanh(((data["minbatch"]) - (np.where((-((((data["minbatch"]) - (np.where(data["maxtominbatch_msignal"] <= -998, data["meanbatch_msignal"], data["minbatch"] )))))) <= -998, data["minbatch"], data["meanbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) * ((((((data["abs_maxbatch_msignal"]) * (data["abs_maxbatch_msignal"]))) + (((np.where(data["maxbatch_slices2_msignal"] > -998, data["mean_abs_chgbatch_slices2"], data["signal_shift_-1_msignal"] )) - ((10.10028266906738281)))))/2.0)))) +
                            0.100000*np.tanh(np.tanh(((-((((np.where(data["abs_minbatch_slices2_msignal"] > -998, (7.25337457656860352), data["maxtominbatch_slices2"] )) - ((7.25337457656860352))))))))) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) * (((data["medianbatch_msignal"]) * (((data["signal"]) * ((((7.0)) * ((((7.0)) - (data["abs_maxbatch_slices2"]))))))))))) - (data["abs_maxbatch_slices2"]))) +
                            0.100000*np.tanh(((np.where(((data["maxbatch_slices2_msignal"]) - (((data["minbatch"]) * ((6.0))))) <= -998, (6.0), (((6.0)) - (data["signal"])) )) + (data["minbatch"]))) +
                            0.100000*np.tanh(((np.where(((((6.0)) + (data["minbatch_msignal"]))/2.0) > -998, (((6.0)) + (data["minbatch_msignal"])), ((np.where(data["stdbatch_slices2_msignal"] > -998, data["minbatch_msignal"], data["minbatch_msignal"] )) * 2.0) )) * 2.0)) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) * (data["meanbatch_msignal"]))) * ((((np.where(data["signal_shift_-1"] <= -998, data["maxtominbatch"], data["abs_maxbatch_msignal"] )) + (((data["meanbatch_msignal"]) * (((data["meanbatch_msignal"]) * (data["meanbatch_slices2"]))))))/2.0)))) +
                            0.100000*np.tanh((((((((9.38610649108886719)) - (np.where(np.tanh((data["rangebatch_slices2"])) > -998, data["rangebatch_slices2"], data["medianbatch_msignal"] )))) * (data["meanbatch_msignal"]))) * (data["medianbatch_slices2"]))) +
                            0.100000*np.tanh(((((((((data["medianbatch_msignal"]) - (data["meanbatch_msignal"]))) * (((((np.where(data["meanbatch_msignal"] <= -998, data["meanbatch_msignal"], (10.0) )) * (data["meanbatch_msignal"]))) * 2.0)))) * 2.0)) - (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh((((((((data["minbatch_msignal"]) + ((6.0)))/2.0)) * (data["abs_maxbatch_msignal"]))) * ((((((((-((data["abs_maxbatch_msignal"])))) - (data["minbatch_msignal"]))) * 2.0)) * 2.0)))) +
                            0.100000*np.tanh((((((((data["maxbatch_slices2_msignal"]) - ((3.0)))) + (data["medianbatch_slices2_msignal"]))/2.0)) - (((data["minbatch_msignal"]) * (((data["maxbatch_slices2_msignal"]) - ((3.0)))))))) +
                            0.100000*np.tanh(np.tanh((((((((data["signal_shift_+1"]) + (data["signal_shift_-1"]))/2.0)) + (np.where(data["mean_abs_chgbatch_slices2"] > -998, ((data["abs_avgbatch_slices2"]) / 2.0), data["signal_shift_-1"] )))/2.0)))) +
                            0.100000*np.tanh((((((6.0)) + (np.where(data["minbatch_msignal"] <= -998, data["medianbatch_msignal"], np.where(np.where(data["abs_minbatch_slices2"] > -998, (6.0), data["rangebatch_slices2"] ) <= -998, ((data["rangebatch_slices2"]) / 2.0), data["minbatch_msignal"] ) )))) * 2.0)) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) + (((data["maxbatch_slices2_msignal"]) * (np.where(((data["maxbatch_slices2_msignal"]) * (np.where(data["abs_minbatch_msignal"] > -998, data["abs_minbatch_slices2"], data["abs_minbatch_slices2_msignal"] ))) > -998, data["abs_minbatch_slices2_msignal"], data["maxtominbatch_msignal"] )))))) +
                            0.100000*np.tanh(((((((np.tanh((data["stdbatch_msignal"]))) + (((data["signal_shift_+1_msignal"]) / 2.0)))/2.0)) + (data["meanbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((((((((5.05809354782104492)) + (np.where((5.05809354782104492) > -998, data["minbatch_msignal"], np.where(((data["rangebatch_msignal"]) * 2.0) > -998, data["minbatch_msignal"], (9.94349479675292969) ) )))/2.0)) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(data["abs_minbatch_msignal"]) +
                            0.100000*np.tanh((((6.0)) + (np.where(np.where(((data["stdbatch_slices2"]) * 2.0) <= -998, np.tanh(((((data["maxbatch_msignal"]) + ((6.0)))/2.0))), data["abs_avgbatch_slices2_msignal"] ) <= -998, data["minbatch_msignal"], data["minbatch_msignal"] )))) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) + (np.tanh((data["maxtominbatch_slices2"]))))) +
                            0.100000*np.tanh(((np.where(data["minbatch_msignal"] <= -998, data["maxbatch_slices2_msignal"], (((8.0)) - (((data["maxbatch_slices2_msignal"]) * 2.0))) )) * 2.0)) +
                            0.100000*np.tanh((((-((np.where(data["minbatch_msignal"] <= -998, data["abs_avgbatch_msignal"], ((data["minbatch_msignal"]) + (data["abs_maxbatch_msignal"])) ))))) * 2.0)))    
      
    def GP_class_4(self,data):
        return self.Output(-2.514146 +
                            0.100000*np.tanh(np.where((-((data["signal"]))) <= -998, np.where(data["meanbatch_slices2"] > -998, data["medianbatch_slices2"], data["medianbatch_slices2"] ), np.where(((data["signal"]) - (data["signal"])) > -998, data["medianbatch_slices2"], data["mean_abs_chgbatch_msignal"] ) )) +
                            0.100000*np.tanh(((((((data["minbatch"]) + (((data["meanbatch_slices2"]) + (np.where(data["signal"] > -998, data["signal"], data["signal_shift_+1"] )))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(np.where(data["meanbatch_msignal"] <= -998, (-((data["mean_abs_chgbatch_slices2"]))), np.where(data["meanbatch_slices2"] > -998, data["medianbatch_slices2"], data["rangebatch_msignal"] ) )) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2"]) - (data["abs_maxbatch_slices2_msignal"]))) + (((data["signal"]) + (np.where(data["minbatch_slices2"] > -998, data["signal_shift_+1"], data["medianbatch_slices2"] )))))) +
                            0.100000*np.tanh(np.where(((((data["maxtominbatch_slices2_msignal"]) * (np.where(data["maxtominbatch_msignal"] <= -998, data["signal_shift_-1"], np.tanh((data["signal_shift_-1"])) )))) * 2.0) > -998, data["meanbatch_slices2"], data["signal"] )) +
                            0.100000*np.tanh((-((data["abs_avgbatch_slices2_msignal"])))) +
                            0.100000*np.tanh(np.where((-((((data["meanbatch_msignal"]) * 2.0)))) > -998, (-((((data["meanbatch_msignal"]) * (((((data["meanbatch_slices2"]) * 2.0)) * 2.0)))))), (-((((data["meanbatch_msignal"]) * (data["signal_shift_-1"]))))) )) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(((np.where(data["stdbatch_msignal"] > -998, np.where(data["abs_maxbatch_slices2"] <= -998, data["abs_minbatch_msignal"], (3.0) ), np.where((-((data["rangebatch_slices2_msignal"]))) <= -998, data["abs_maxbatch_msignal"], data["abs_avgbatch_slices2_msignal"] ) )) - (data["abs_maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((((((1.16302394866943359)) - (data["maxbatch_msignal"]))) * (np.where(((data["abs_avgbatch_slices2_msignal"]) * ((-((data["abs_avgbatch_slices2_msignal"]))))) <= -998, data["medianbatch_msignal"], data["mean_abs_chgbatch_msignal"] )))) +
                            0.100000*np.tanh((((((data["medianbatch_slices2"]) + (((data["minbatch"]) / 2.0)))/2.0)) - (((data["rangebatch_slices2"]) - ((((-((data["minbatch"])))) / 2.0)))))) +
                            0.100000*np.tanh(np.tanh(((((data["minbatch"]) + (((data["abs_avgbatch_slices2_msignal"]) / 2.0)))/2.0)))) +
                            0.100000*np.tanh(np.where(np.where(np.tanh((data["medianbatch_slices2"])) > -998, data["stdbatch_msignal"], data["medianbatch_slices2"] ) <= -998, data["signal_shift_+1"], data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2_msignal"] <= -998, data["medianbatch_slices2"], np.tanh((((data["abs_minbatch_slices2"]) * ((((((((-((((data["rangebatch_msignal"]) * 2.0))))) * 2.0)) * 2.0)) - (data["maxbatch_slices2_msignal"])))))) )) +
                            0.100000*np.tanh((((5.79395198822021484)) - (((np.where((-((((data["maxtominbatch_slices2"]) / 2.0)))) > -998, data["abs_maxbatch_slices2_msignal"], (-((((data["abs_avgbatch_slices2_msignal"]) * 2.0)))) )) * 2.0)))) +
                            0.100000*np.tanh(((((data["stdbatch_msignal"]) * 2.0)) * ((-((np.where(data["mean_abs_chgbatch_slices2"] > -998, data["stdbatch_slices2"], ((((data["stdbatch_msignal"]) * (data["minbatch"]))) - (np.tanh((((data["stdbatch_slices2"]) / 2.0))))) ))))))) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) * (np.where((-(((-((data["signal_shift_+1_msignal"])))))) > -998, ((data["minbatch_msignal"]) + ((7.19189453125000000))), np.tanh((data["minbatch"])) )))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) * (((data["minbatch_slices2_msignal"]) - (((data["rangebatch_msignal"]) * 2.0)))))) * 2.0)) +
                            0.100000*np.tanh((((((((data["abs_minbatch_msignal"]) * (((((((data["maxbatch_slices2_msignal"]) + (data["meanbatch_msignal"]))) * 2.0)) * (data["meanbatch_msignal"]))))) + (data["meanbatch_msignal"]))/2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["minbatch_slices2"]) - ((((-((data["minbatch_msignal"])))) - (data["signal_shift_-1"]))))) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_msignal"] <= -998, ((data["abs_minbatch_msignal"]) - ((((((data["minbatch_slices2"]) * 2.0)) + (data["signal_shift_+1_msignal"]))/2.0))), ((data["abs_minbatch_msignal"]) - (data["minbatch_slices2"])) )) +
                            0.100000*np.tanh(((data["rangebatch_msignal"]) - (((data["medianbatch_msignal"]) * (((data["rangebatch_slices2"]) - (((data["medianbatch_msignal"]) * (np.where(data["maxtominbatch_slices2_msignal"] > -998, ((data["minbatch_slices2_msignal"]) * 2.0), data["medianbatch_msignal"] )))))))))) +
                            0.100000*np.tanh(((data["maxtominbatch"]) + (((data["abs_minbatch_msignal"]) + (data["rangebatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) - (((data["medianbatch_msignal"]) * (((data["meanbatch_slices2"]) - (((data["stdbatch_slices2_msignal"]) * (((data["meanbatch_msignal"]) * (data["meanbatch_slices2"]))))))))))) +
                            0.100000*np.tanh((((((data["meanbatch_slices2"]) + (np.tanh((((np.tanh((np.tanh((((data["maxbatch_msignal"]) + (data["medianbatch_slices2"]))))))) * 2.0)))))) + (data["meanbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(((((((data["meanbatch_slices2_msignal"]) + (data["meanbatch_msignal"]))) * (((((data["medianbatch_slices2_msignal"]) * (((data["meanbatch_msignal"]) * 2.0)))) - (data["maxbatch_slices2_msignal"]))))) + ((-((data["meanbatch_msignal"])))))) +
                            0.100000*np.tanh(data["minbatch"]) +
                            0.100000*np.tanh((((-((np.where(np.tanh((data["maxtominbatch"])) <= -998, data["maxtominbatch_slices2"], ((data["abs_maxbatch_slices2"]) * (data["rangebatch_msignal"])) ))))) * (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) * ((((data["stdbatch_slices2"]) + (data["stdbatch_slices2"]))/2.0)))) +
                            0.100000*np.tanh(((data["rangebatch_msignal"]) + (((np.where(np.where(data["medianbatch_msignal"] <= -998, data["minbatch_slices2"], ((data["stdbatch_slices2_msignal"]) * 2.0) ) <= -998, data["rangebatch_msignal"], ((data["medianbatch_msignal"]) - (data["abs_maxbatch_msignal"])) )) * 2.0)))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_slices2_msignal"] > -998, data["medianbatch_msignal"], (((data["abs_minbatch_slices2"]) + (data["medianbatch_msignal"]))/2.0) )) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) + (((data["medianbatch_msignal"]) * (data["abs_maxbatch"]))))) +
                            0.100000*np.tanh((((((data["rangebatch_slices2_msignal"]) + (np.where(np.tanh((data["rangebatch_slices2_msignal"])) <= -998, ((data["stdbatch_msignal"]) / 2.0), data["abs_maxbatch_msignal"] )))/2.0)) - ((((-((data["stdbatch_msignal"])))) * 2.0)))) +
                            0.100000*np.tanh(((((((data["meanbatch_msignal"]) * (((data["abs_minbatch_msignal"]) * (((data["maxbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_msignal"] <= -998, ((data["mean_abs_chgbatch_msignal"]) / 2.0), ((((((7.87415218353271484)) + (((data["mean_abs_chgbatch_msignal"]) * (((data["rangebatch_msignal"]) / 2.0)))))/2.0)) * (data["rangebatch_msignal"])) )) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(((np.tanh((np.where(((data["rangebatch_slices2_msignal"]) - (data["meanbatch_msignal"])) <= -998, data["abs_maxbatch_slices2_msignal"], ((data["medianbatch_msignal"]) * 2.0) )))) + (((((data["abs_maxbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))) * 2.0)))) +
                            0.100000*np.tanh(((data["abs_maxbatch"]) + ((((data["abs_maxbatch"]) + ((-((((data["abs_maxbatch_msignal"]) * (data["abs_maxbatch"])))))))/2.0)))) +
                            0.100000*np.tanh((((data["medianbatch_msignal"]) + (data["mean_abs_chgbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(((np.tanh((data["medianbatch_slices2"]))) + (np.where(data["rangebatch_slices2_msignal"] > -998, data["meanbatch_msignal"], ((((((14.12201690673828125)) * (data["medianbatch_slices2"]))) + ((2.93570351600646973)))/2.0) )))) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((((data["medianbatch_msignal"]) + (np.tanh(((-(((((((data["medianbatch_msignal"]) * (((data["stdbatch_slices2_msignal"]) - (data["meanbatch_slices2_msignal"]))))) + (data["mean_abs_chgbatch_slices2_msignal"]))/2.0))))))))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) * 2.0)) * (np.where(((data["abs_avgbatch_msignal"]) / 2.0) > -998, data["abs_minbatch_slices2_msignal"], np.tanh((data["minbatch_msignal"])) )))) +
                            0.100000*np.tanh(((((data["stdbatch_slices2_msignal"]) / 2.0)) + (((((np.where(data["mean_abs_chgbatch_msignal"] <= -998, data["abs_minbatch_msignal"], data["minbatch_msignal"] )) / 2.0)) + (data["meanbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(np.where(data["stdbatch_msignal"] > -998, data["abs_maxbatch_msignal"], (7.63543224334716797) ) > -998, (((7.63543224334716797)) - (((data["abs_maxbatch_msignal"]) * 2.0))), (7.63543224334716797) )) +
                            0.100000*np.tanh((((((data["abs_minbatch_msignal"]) + (((data["medianbatch_msignal"]) + (data["signal_shift_-1_msignal"]))))/2.0)) / 2.0)) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) * (((data["meanbatch_msignal"]) - (((data["rangebatch_slices2"]) - (np.where((9.62103939056396484) > -998, (9.62103939056396484), data["rangebatch_slices2"] )))))))) +
                            0.100000*np.tanh(np.where((5.0) <= -998, np.tanh(((2.00369644165039062))), ((data["rangebatch_slices2"]) - ((6.0))) )) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] <= -998, np.where((((data["mean_abs_chgbatch_msignal"]) + ((-((((data["abs_minbatch_slices2_msignal"]) / 2.0))))))/2.0) <= -998, ((data["stdbatch_msignal"]) / 2.0), data["medianbatch_msignal"] ), data["stdbatch_msignal"] )) +
                            0.100000*np.tanh(((((data["meanbatch_slices2"]) / 2.0)) + ((-((data["meanbatch_slices2"])))))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2"]) + (((data["abs_maxbatch_slices2_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where(((data["stdbatch_slices2"]) / 2.0) <= -998, ((data["stdbatch_slices2"]) / 2.0), ((((((6.0)) + (((data["maxbatch_slices2_msignal"]) * (np.where((6.0) > -998, data["maxtominbatch_slices2"], data["abs_minbatch_msignal"] )))))/2.0)) * 2.0) )) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_slices2_msignal"] <= -998, ((data["meanbatch_slices2_msignal"]) * ((-((((np.tanh((data["mean_abs_chgbatch_slices2_msignal"]))) * (data["meanbatch_slices2_msignal"]))))))), ((data["meanbatch_slices2_msignal"]) * (data["mean_abs_chgbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) + ((((-((data["abs_minbatch_slices2_msignal"])))) * (((data["meanbatch_slices2"]) - (((data["abs_minbatch_slices2_msignal"]) * (data["medianbatch_msignal"]))))))))) + (data["meanbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) / 2.0)) +
                            0.100000*np.tanh(data["stdbatch_slices2"]) +
                            0.100000*np.tanh((((((data["signal_shift_-1_msignal"]) + (((np.tanh((np.tanh((data["stdbatch_msignal"]))))) / 2.0)))/2.0)) / 2.0)) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (((((((((((data["meanbatch_slices2_msignal"]) + (data["minbatch_slices2_msignal"]))) * (data["meanbatch_slices2_msignal"]))) + (data["meanbatch_slices2_msignal"]))) + (data["minbatch_slices2_msignal"]))) + (data["meanbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where(((((data["minbatch_slices2_msignal"]) + (np.where(data["maxbatch_slices2_msignal"] > -998, (6.0), data["minbatch_slices2_msignal"] )))) + (data["meanbatch_msignal"])) > -998, (6.0), data["minbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh(data["abs_minbatch_msignal"]) +
                            0.100000*np.tanh(((((data["abs_minbatch_msignal"]) * (np.where((((data["maxbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2"]))/2.0) > -998, data["meanbatch_slices2_msignal"], data["maxbatch_slices2_msignal"] )))) * (np.tanh((((data["meanbatch_msignal"]) + (data["maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(((np.where(((data["abs_maxbatch_msignal"]) * 2.0) > -998, (7.0), (-((((data["abs_maxbatch_msignal"]) * 2.0)))) )) + ((-((((data["maxbatch_msignal"]) * 2.0))))))) +
                            0.100000*np.tanh(np.tanh((np.where(((((data["medianbatch_msignal"]) + (np.tanh((data["abs_avgbatch_msignal"]))))) / 2.0) > -998, data["medianbatch_msignal"], (-((data["signal_shift_+1_msignal"]))) )))) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] > -998, data["medianbatch_msignal"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh((((data["medianbatch_msignal"]) + (data["stdbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh((-((((((np.where(data["abs_maxbatch_msignal"] > -998, data["abs_maxbatch_msignal"], np.where(data["minbatch_slices2"] <= -998, (-((data["minbatch_msignal"]))), data["maxtominbatch_slices2"] ) )) * 2.0)) + (data["minbatch_msignal"])))))) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) + (((((data["medianbatch_msignal"]) + (np.where(data["medianbatch_msignal"] <= -998, data["medianbatch_msignal"], np.tanh((((data["signal_shift_-1"]) * 2.0))) )))) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) * (((data["rangebatch_slices2"]) - (np.where(data["maxtominbatch_slices2_msignal"] > -998, (8.0), np.where(data["minbatch_slices2"] <= -998, ((np.tanh((data["abs_maxbatch_slices2"]))) / 2.0), data["medianbatch_slices2_msignal"] ) )))))) +
                            0.100000*np.tanh(np.where(((data["medianbatch_slices2_msignal"]) - (data["medianbatch_msignal"])) <= -998, (((data["minbatch_slices2_msignal"]) + (data["medianbatch_slices2_msignal"]))/2.0), (((data["minbatch_slices2_msignal"]) + (((data["medianbatch_msignal"]) + ((((data["medianbatch_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0)))))/2.0) )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (((np.where(data["medianbatch_slices2_msignal"] <= -998, data["meanbatch_msignal"], np.tanh((data["meanbatch_slices2_msignal"])) )) * 2.0)))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) + (data["minbatch_slices2"]))) / 2.0)) +
                            0.100000*np.tanh(((((data["rangebatch_slices2"]) + (np.where(((data["abs_maxbatch_slices2_msignal"]) - ((8.0))) <= -998, (8.0), ((data["maxbatch_msignal"]) - ((8.0))) )))) * 2.0)) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) + (np.where(data["medianbatch_slices2_msignal"] <= -998, data["maxbatch_slices2"], ((data["medianbatch_msignal"]) + (data["maxbatch_slices2_msignal"])) )))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (np.tanh((((data["meanbatch_slices2_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) + (data["signal_shift_+1_msignal"]))) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) + ((-((((((6.0)) + (((np.tanh((((data["medianbatch_msignal"]) + (data["abs_maxbatch_slices2_msignal"]))))) / 2.0)))/2.0))))))) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) + (data["maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) - ((3.0)))) +
                            0.100000*np.tanh((((((((data["signal_shift_-1"]) + (data["maxbatch_msignal"]))/2.0)) / 2.0)) * 2.0)) +
                            0.100000*np.tanh((((((((((data["meanbatch_slices2"]) + (data["signal_shift_-1"]))/2.0)) + (data["mean_abs_chgbatch_slices2"]))/2.0)) + (data["abs_minbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((((data["abs_maxbatch_msignal"]) * (data["abs_minbatch_slices2_msignal"]))) + (((((np.where((12.74442958831787109) <= -998, ((data["abs_maxbatch_msignal"]) + (data["abs_minbatch_slices2"])), (12.74442958831787109) )) - (data["mean_abs_chgbatch_slices2_msignal"]))) - (data["abs_maxbatch_msignal"]))))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (np.tanh((data["abs_avgbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((((np.tanh((((data["meanbatch_slices2_msignal"]) / 2.0)))) + (np.where(data["abs_maxbatch"] <= -998, data["medianbatch_msignal"], data["medianbatch_slices2_msignal"] )))) - ((3.64274477958679199)))) +
                            0.100000*np.tanh(data["abs_maxbatch_slices2"]) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] <= -998, ((data["medianbatch_msignal"]) / 2.0), data["medianbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((((data["meanbatch_msignal"]) + (np.where(np.tanh((data["medianbatch_slices2_msignal"])) <= -998, data["meanbatch_slices2"], data["minbatch_slices2_msignal"] )))/2.0)) * (((data["meanbatch_slices2_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2"] > -998, data["medianbatch_slices2_msignal"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((((((data["medianbatch_slices2_msignal"]) / 2.0)) + (np.tanh((((data["meanbatch_msignal"]) * (np.where(data["meanbatch_msignal"] > -998, data["abs_minbatch_slices2_msignal"], ((data["medianbatch_msignal"]) + (data["stdbatch_slices2"])) )))))))) * 2.0)) +
                            0.100000*np.tanh((((7.0)) + (data["minbatch_msignal"]))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (np.where((5.51959419250488281) > -998, (5.51959419250488281), (5.51959419250488281) )))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) + (((((data["minbatch_msignal"]) + (((data["minbatch_msignal"]) + ((((((-((((data["stdbatch_slices2_msignal"]) / 2.0))))) / 2.0)) + (data["meanbatch_msignal"]))))))) + (data["meanbatch_msignal"]))))) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) - ((((-((np.where((4.0) <= -998, data["stdbatch_msignal"], np.where(data["stdbatch_msignal"] <= -998, data["minbatch_msignal"], (4.0) ) ))))) * 2.0)))) +
                            0.100000*np.tanh(((((((((data["abs_maxbatch_slices2_msignal"]) - ((3.46380186080932617)))) * 2.0)) * (((((data["medianbatch_slices2_msignal"]) - ((3.46380186080932617)))) * 2.0)))) - ((3.46379828453063965)))) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]))    
   
    def GP_class_5(self,data):
        return self.Output(-2.886555 +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] > -998, data["signal_shift_+1"], np.where((-(((((data["mean_abs_chgbatch_slices2_msignal"]) + (data["meanbatch_slices2"]))/2.0)))) > -998, data["medianbatch_slices2"], data["signal_shift_+1"] ) )) +
                            0.100000*np.tanh(data["medianbatch_slices2"]) +
                            0.100000*np.tanh(((np.where(((np.tanh((data["meanbatch_slices2"]))) / 2.0) > -998, data["medianbatch_slices2"], np.where(data["maxtominbatch"] <= -998, data["medianbatch_msignal"], ((data["signal"]) - (data["signal_shift_+1"])) ) )) * 2.0)) +
                            0.100000*np.tanh(((np.where(np.where(data["minbatch_slices2_msignal"] <= -998, data["signal_shift_-1"], data["signal_shift_-1"] ) <= -998, data["signal_shift_-1"], ((data["signal_shift_-1"]) + (data["signal_shift_-1"])) )) + (data["signal_shift_+1"]))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(np.where(data["stdbatch_slices2"] > -998, ((((data["stdbatch_slices2"]) - (np.where(data["meanbatch_slices2_msignal"] > -998, ((data["abs_avgbatch_slices2_msignal"]) - (data["abs_avgbatch_msignal"])), data["signal_shift_-1"] )))) - (data["maxbatch_slices2_msignal"])), data["signal_shift_+1"] )) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) * 2.0)) +
                            0.100000*np.tanh((-((np.where((0.0) <= -998, data["stdbatch_slices2_msignal"], (((((data["abs_avgbatch_msignal"]) + (data["minbatch_slices2"]))/2.0)) + (((((((data["abs_avgbatch_msignal"]) + (((data["abs_maxbatch_slices2_msignal"]) / 2.0)))/2.0)) + (data["abs_maxbatch_slices2_msignal"]))/2.0))) ))))) +
                            0.100000*np.tanh(np.where(((data["signal"]) / 2.0) > -998, ((data["meanbatch_slices2"]) - (np.tanh((((data["abs_avgbatch_slices2"]) - (data["medianbatch_slices2"])))))), data["minbatch_msignal"] )) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(np.where(np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, data["stdbatch_msignal"], (-((np.where(data["signal_shift_+1"] > -998, np.tanh((data["stdbatch_slices2_msignal"])), data["abs_minbatch_msignal"] )))) ) <= -998, (10.0), data["signal_shift_-1"] )) +
                            0.100000*np.tanh((-((data["abs_avgbatch_slices2_msignal"])))) +
                            0.100000*np.tanh((((((-((data["medianbatch_slices2"])))) - (((data["abs_maxbatch_slices2_msignal"]) * (data["maxtominbatch_slices2"]))))) - (((data["meanbatch_slices2_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2_msignal"] <= -998, (-((data["abs_avgbatch_slices2"]))), (((((data["mean_abs_chgbatch_slices2_msignal"]) + (np.tanh((((data["medianbatch_msignal"]) * (((data["abs_avgbatch_slices2_msignal"]) + (data["medianbatch_slices2"]))))))))/2.0)) * (data["abs_avgbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((np.where(((data["medianbatch_slices2"]) - (data["stdbatch_slices2"])) > -998, (((-((data["medianbatch_msignal"])))) - (data["abs_maxbatch_msignal"])), data["abs_maxbatch_msignal"] )) * 2.0)) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (data["meanbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2_msignal"]) * (np.tanh((data["abs_avgbatch_msignal"]))))) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2_msignal"]) - (data["stdbatch_slices2"]))) * (((((((data["meanbatch_slices2_msignal"]) - (np.tanh((data["abs_maxbatch_slices2_msignal"]))))) * 2.0)) * 2.0)))) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (np.tanh((((data["abs_maxbatch_msignal"]) + (np.where(((data["meanbatch_msignal"]) * (data["stdbatch_msignal"])) > -998, data["meanbatch_msignal"], data["meanbatch_slices2_msignal"] )))))))) +
                            0.100000*np.tanh((((((data["signal_shift_+1_msignal"]) * (data["abs_avgbatch_msignal"]))) + (((np.where(data["medianbatch_slices2_msignal"] > -998, data["abs_avgbatch_msignal"], data["abs_avgbatch_slices2_msignal"] )) * (data["meanbatch_slices2_msignal"]))))/2.0)) +
                            0.100000*np.tanh(((((data["minbatch_msignal"]) - (((data["medianbatch_slices2"]) / 2.0)))) + (((((((((data["medianbatch_slices2_msignal"]) * 2.0)) * 2.0)) * (data["meanbatch_msignal"]))) * 2.0)))) +
                            0.100000*np.tanh(((np.where(np.tanh((data["abs_avgbatch_msignal"])) <= -998, data["abs_avgbatch_msignal"], data["minbatch_msignal"] )) + (((((((data["medianbatch_slices2_msignal"]) * 2.0)) * (data["abs_avgbatch_msignal"]))) * (data["medianbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((((data["signal"]) + (np.tanh((data["meanbatch_slices2"]))))/2.0)) * 2.0)) +
                            0.100000*np.tanh(((((data["maxbatch_slices2_msignal"]) + (data["abs_avgbatch_msignal"]))) * (np.where(((data["maxbatch_slices2_msignal"]) / 2.0) > -998, data["abs_avgbatch_msignal"], ((data["signal"]) / 2.0) )))) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) - (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2_msignal"] <= -998, data["rangebatch_slices2"], ((((data["stdbatch_slices2"]) - (data["abs_maxbatch_slices2_msignal"]))) * 2.0) )) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) * (data["maxbatch_msignal"]))) - (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(((((np.where((4.0) > -998, data["meanbatch_slices2_msignal"], ((data["meanbatch_msignal"]) * (data["abs_avgbatch_slices2_msignal"])) )) * (data["abs_maxbatch_slices2_msignal"]))) * (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] <= -998, np.where(((data["stdbatch_slices2"]) + (((data["abs_avgbatch_msignal"]) * 2.0))) <= -998, (-((data["abs_avgbatch_slices2_msignal"]))), data["meanbatch_msignal"] ), ((data["meanbatch_msignal"]) * (data["abs_avgbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(np.where(((data["meanbatch_slices2"]) / 2.0) <= -998, ((data["meanbatch_slices2"]) / 2.0), (((((6.0)) / 2.0)) * (((data["abs_maxbatch_slices2_msignal"]) - ((6.0))))) )) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) * (np.where((((data["meanbatch_slices2_msignal"]) + (data["medianbatch_slices2"]))/2.0) > -998, data["meanbatch_slices2_msignal"], data["stdbatch_slices2"] )))) - (data["stdbatch_slices2"]))) +
                            0.100000*np.tanh((((((data["medianbatch_slices2_msignal"]) + (data["abs_maxbatch_slices2_msignal"]))/2.0)) * (((((data["medianbatch_slices2_msignal"]) + (data["stdbatch_msignal"]))) + ((((data["minbatch_msignal"]) + (data["abs_maxbatch_slices2_msignal"]))/2.0)))))) +
                            0.100000*np.tanh(data["maxbatch_slices2"]) +
                            0.100000*np.tanh(np.where((((-((((data["meanbatch_msignal"]) + (((data["meanbatch_msignal"]) * (data["abs_avgbatch_slices2_msignal"])))))))) + (data["medianbatch_msignal"])) <= -998, data["medianbatch_msignal"], data["meanbatch_msignal"] )) +
                            0.100000*np.tanh((((9.0)) + (((np.where(np.where(((data["rangebatch_msignal"]) / 2.0) <= -998, data["meanbatch_slices2_msignal"], data["meanbatch_slices2"] ) > -998, data["minbatch_slices2_msignal"], data["rangebatch_msignal"] )) * (data["maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((data["maxtominbatch_slices2"]) + ((((data["maxbatch_slices2"]) + (data["stdbatch_slices2"]))/2.0)))/2.0)) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2"] <= -998, np.tanh((data["rangebatch_slices2"])), ((((data["rangebatch_slices2"]) + (((data["abs_avgbatch_slices2_msignal"]) - ((8.0)))))) * (data["abs_avgbatch_msignal"])) )) +
                            0.100000*np.tanh((((data["minbatch_msignal"]) + (((((data["medianbatch_msignal"]) * 2.0)) * (np.where(data["signal_shift_+1_msignal"] <= -998, data["medianbatch_msignal"], data["meanbatch_msignal"] )))))/2.0)) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(((((data["stdbatch_msignal"]) * (np.where(data["stdbatch_msignal"] <= -998, data["abs_maxbatch_msignal"], np.where(data["abs_maxbatch_slices2"] <= -998, data["stdbatch_slices2"], ((data["maxbatch_slices2_msignal"]) - (data["stdbatch_slices2"])) ) )))) * 2.0)) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (((data["medianbatch_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(np.where((-((data["abs_maxbatch_msignal"]))) > -998, (((-((data["abs_maxbatch_msignal"])))) + (((data["meanbatch_msignal"]) * (data["meanbatch_msignal"])))), data["medianbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((((data["maxbatch_slices2_msignal"]) + (np.where(((data["meanbatch_slices2"]) * 2.0) > -998, data["minbatch_msignal"], data["mean_abs_chgbatch_slices2"] )))) * (data["rangebatch_slices2"]))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) * 2.0)) +
                            0.100000*np.tanh(((np.tanh((((((data["meanbatch_slices2_msignal"]) * (data["meanbatch_slices2_msignal"]))) - (np.tanh((np.tanh((data["signal"]))))))))) * (data["medianbatch_slices2"]))) +
                            0.100000*np.tanh(np.where(((((data["meanbatch_slices2_msignal"]) * 2.0)) / 2.0) <= -998, ((data["meanbatch_slices2_msignal"]) / 2.0), data["signal_shift_+1_msignal"] )) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) - (np.where(((data["stdbatch_slices2"]) * (data["meanbatch_msignal"])) <= -998, data["medianbatch_msignal"], data["stdbatch_slices2"] )))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2"]) - (data["minbatch_slices2_msignal"]))) * (((data["medianbatch_msignal"]) - (((np.tanh((data["medianbatch_slices2_msignal"]))) * 2.0)))))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * (((data["maxbatch_slices2"]) / 2.0)))) - (np.where(np.where(((data["medianbatch_msignal"]) * 2.0) <= -998, data["medianbatch_slices2"], data["maxbatch_slices2"] ) > -998, data["abs_maxbatch"], data["maxtominbatch"] )))) +
                            0.100000*np.tanh(((((data["signal_shift_+1"]) - (data["stdbatch_slices2_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) + (((np.where((2.59933662414550781) > -998, (-(((2.76859831809997559)))), (-((data["abs_maxbatch_msignal"]))) )) * 2.0)))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) - (np.where(data["maxbatch_slices2_msignal"] <= -998, ((((data["stdbatch_slices2"]) + (data["abs_avgbatch_slices2"]))) + (data["abs_avgbatch_slices2_msignal"])), (((8.0)) - ((((8.0)) + (data["abs_avgbatch_slices2"])))) )))) +
                            0.100000*np.tanh(data["maxtominbatch_slices2"]) +
                            0.100000*np.tanh(((((np.where(np.tanh((data["maxtominbatch_slices2_msignal"])) > -998, data["abs_avgbatch_msignal"], data["maxbatch_msignal"] )) * (data["abs_avgbatch_slices2_msignal"]))) + (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(data["signal"] <= -998, data["meanbatch_msignal"], ((np.where(data["abs_maxbatch_msignal"] > -998, (3.85183548927307129), ((data["abs_maxbatch_msignal"]) * 2.0) )) - (((data["abs_maxbatch_msignal"]) * 2.0))) )) +
                            0.100000*np.tanh(((data["signal"]) * (np.where(np.tanh((((((data["rangebatch_slices2_msignal"]) + (data["rangebatch_slices2_msignal"]))) + (data["medianbatch_slices2"])))) <= -998, np.tanh((data["medianbatch_slices2_msignal"])), ((data["rangebatch_slices2_msignal"]) + (data["mean_abs_chgbatch_msignal"])) )))) +
                            0.100000*np.tanh(((((((data["mean_abs_chgbatch_slices2"]) * (data["maxbatch_slices2"]))) * (((data["medianbatch_msignal"]) - ((2.0)))))) * (((data["maxbatch_slices2"]) * ((((np.tanh((data["medianbatch_msignal"]))) + (data["mean_abs_chgbatch_slices2"]))/2.0)))))) +
                            0.100000*np.tanh(((np.where(data["abs_maxbatch"] > -998, data["abs_avgbatch_slices2_msignal"], (6.0) )) * (np.where((((3.0)) * ((7.0))) > -998, ((data["abs_maxbatch"]) - ((7.0))), data["abs_maxbatch"] )))) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2_msignal"] <= -998, ((data["signal_shift_-1_msignal"]) + (((data["signal_shift_-1_msignal"]) + (((data["medianbatch_slices2_msignal"]) + (data["medianbatch_slices2_msignal"])))))), ((((data["signal_shift_-1_msignal"]) + (data["medianbatch_slices2_msignal"]))) / 2.0) )) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) + (((((14.59570217132568359)) + (np.tanh((((data["maxtominbatch_slices2_msignal"]) + (((data["maxtominbatch_slices2_msignal"]) + (data["maxtominbatch_slices2_msignal"]))))))))/2.0)))) +
                            0.100000*np.tanh(((((data["stdbatch_slices2"]) - (data["maxbatch_slices2_msignal"]))) * (((data["abs_minbatch_msignal"]) * (data["meanbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) - (data["stdbatch_slices2"]))) * (((data["abs_avgbatch_slices2_msignal"]) + (((data["maxbatch_slices2_msignal"]) + (np.tanh((data["meanbatch_msignal"]))))))))) +
                            0.100000*np.tanh(data["maxtominbatch"]) +
                            0.100000*np.tanh((-((((data["signal_shift_-1_msignal"]) - (((data["meanbatch_msignal"]) / 2.0))))))) +
                            0.100000*np.tanh(((((((((data["medianbatch_slices2"]) * (((data["maxbatch_slices2"]) * (data["rangebatch_slices2_msignal"]))))) / 2.0)) * (((((data["signal"]) * 2.0)) * 2.0)))) * (data["mean_abs_chgbatch_msignal"]))) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) * (data["abs_avgbatch_slices2"]))) - (np.where(((data["meanbatch_msignal"]) * (data["abs_avgbatch_slices2"])) > -998, data["maxbatch_msignal"], data["rangebatch_msignal"] )))) +
                            0.100000*np.tanh(data["rangebatch_msignal"]) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh((((data["abs_minbatch_msignal"]) + (data["stdbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) - (((np.tanh((data["medianbatch_msignal"]))) * 2.0)))) * 2.0)) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) * ((((((data["meanbatch_slices2"]) * 2.0)) + ((-((np.where(data["maxbatch_slices2_msignal"] > -998, np.where(data["abs_avgbatch_msignal"] > -998, data["mean_abs_chgbatch_msignal"], data["meanbatch_slices2_msignal"] ), np.tanh((data["stdbatch_slices2_msignal"])) ))))))/2.0)))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) * (np.where(((((data["signal"]) - (data["signal"]))) * (data["abs_minbatch_slices2"])) <= -998, data["meanbatch_slices2"], ((data["meanbatch_msignal"]) - ((2.0))) )))) +
                            0.100000*np.tanh((((14.49304103851318359)) * ((((14.49304103851318359)) * ((((data["minbatch_msignal"]) + (np.where((14.49304103851318359) <= -998, (14.49304103851318359), ((((14.49304103851318359)) + (np.tanh(((14.49304103851318359)))))/2.0) )))/2.0)))))) +
                            0.100000*np.tanh(np.where(((data["signal"]) / 2.0) > -998, data["signal"], (-((data["meanbatch_slices2_msignal"]))) )) +
                            0.100000*np.tanh(np.where(data["signal_shift_-1_msignal"] > -998, np.where(np.tanh((data["signal_shift_-1_msignal"])) > -998, data["signal_shift_-1_msignal"], data["rangebatch_slices2"] ), (-((data["abs_avgbatch_slices2"]))) )) +
                            0.100000*np.tanh(((data["signal"]) - (((np.where((14.50152778625488281) > -998, data["abs_maxbatch_msignal"], np.where(data["abs_avgbatch_slices2"] > -998, data["abs_maxbatch_msignal"], (2.62557578086853027) ) )) * 2.0)))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((data["signal_shift_-1_msignal"]))))) +
                            0.100000*np.tanh(((((9.0)) + (np.where((-(((-((((data["minbatch_msignal"]) * 2.0))))))) > -998, data["minbatch_msignal"], (9.0) )))/2.0)) +
                            0.100000*np.tanh(data["medianbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((((((data["maxtominbatch_slices2"]) - (((data["abs_avgbatch_msignal"]) - (data["maxtominbatch_msignal"]))))) + (np.tanh((((data["maxtominbatch_slices2"]) - (data["mean_abs_chgbatch_slices2"]))))))/2.0)) - ((-((data["signal"])))))) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) + ((-((np.where(((data["maxtominbatch_msignal"]) + ((-((data["maxbatch_slices2_msignal"]))))) > -998, (6.0), ((data["abs_maxbatch"]) * (data["maxbatch_slices2_msignal"])) ))))))) +
                            0.100000*np.tanh(((data["signal"]) + (((data["signal"]) * 2.0)))) +
                            0.100000*np.tanh(((np.where(data["maxbatch_slices2_msignal"] <= -998, ((data["rangebatch_msignal"]) - (((data["stdbatch_msignal"]) * 2.0))), (9.0) )) + (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) - ((6.0)))) +
                            0.100000*np.tanh(np.tanh((np.where(data["minbatch"] <= -998, ((data["maxtominbatch_msignal"]) / 2.0), ((data["maxbatch_slices2"]) - (((data["maxbatch_slices2"]) * (data["abs_maxbatch_slices2_msignal"])))) )))) +
                            0.100000*np.tanh(np.where(data["signal"] <= -998, data["signal"], (((((((6.0)) * 2.0)) / 2.0)) * (data["meanbatch_slices2"])) )) +
                            0.100000*np.tanh(((np.where(np.where(data["rangebatch_msignal"] > -998, data["abs_maxbatch_msignal"], ((((((data["mean_abs_chgbatch_slices2_msignal"]) * 2.0)) * 2.0)) / 2.0) ) > -998, ((data["rangebatch_msignal"]) * 2.0), ((data["rangebatch_msignal"]) * 2.0) )) * (data["mean_abs_chgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2"]) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) - (np.where(np.where(data["minbatch"] > -998, np.tanh((data["abs_maxbatch_msignal"])), data["abs_minbatch_slices2_msignal"] ) > -998, data["minbatch"], np.tanh((np.where(data["abs_avgbatch_slices2_msignal"] <= -998, data["minbatch"], data["stdbatch_msignal"] ))) )))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (data["abs_maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((((((((data["abs_minbatch_slices2"]) / 2.0)) + (data["signal"]))/2.0)) + (data["meanbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) * (((data["medianbatch_msignal"]) - (((np.tanh(((((((data["medianbatch_msignal"]) + ((((data["abs_maxbatch_msignal"]) + (data["abs_avgbatch_msignal"]))/2.0)))) + (data["medianbatch_msignal"]))/2.0)))) * 2.0)))))) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (np.where(data["mean_abs_chgbatch_slices2_msignal"] > -998, (6.98720216751098633), data["meanbatch_msignal"] )))) +
                            0.100000*np.tanh(data["maxtominbatch_slices2"]) +
                            0.100000*np.tanh(((((data["maxbatch_slices2_msignal"]) - (np.where((6.29931974411010742) > -998, (6.29932308197021484), np.where(data["medianbatch_slices2_msignal"] <= -998, data["maxbatch_slices2_msignal"], ((data["maxbatch_slices2_msignal"]) * 2.0) ) )))) * 2.0)))    
    
    def GP_class_6(self,data):
        return self.Output(-3.287690 +
                            0.100000*np.tanh(((np.where(np.tanh((np.where(data["meanbatch_msignal"] > -998, data["meanbatch_msignal"], data["meanbatch_slices2_msignal"] ))) > -998, data["meanbatch_msignal"], ((data["meanbatch_slices2_msignal"]) / 2.0) )) * 2.0)) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(np.where(data["signal"] > -998, ((data["signal"]) * 2.0), data["medianbatch_slices2"] )) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(np.where(((data["medianbatch_slices2_msignal"]) / 2.0) <= -998, np.where(np.where(((data["meanbatch_msignal"]) * 2.0) > -998, data["stdbatch_slices2_msignal"], data["meanbatch_slices2_msignal"] ) <= -998, data["medianbatch_slices2_msignal"], data["maxbatch_slices2_msignal"] ), data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where(data["meanbatch_msignal"] <= -998, np.where(data["medianbatch_msignal"] > -998, ((data["medianbatch_slices2_msignal"]) / 2.0), data["medianbatch_msignal"] ), data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((np.where(data["meanbatch_slices2_msignal"] > -998, data["meanbatch_slices2_msignal"], data["meanbatch_msignal"] )) * 2.0)) * (data["signal"]))) +
                            0.100000*np.tanh(((np.where(data["meanbatch_slices2"] > -998, data["meanbatch_msignal"], ((data["signal"]) + (data["meanbatch_msignal"])) )) / 2.0)) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) * 2.0)) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((((np.tanh((data["signal"]))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (np.where((8.0) > -998, (8.03822803497314453), ((data["stdbatch_slices2_msignal"]) + (((data["meanbatch_slices2_msignal"]) + (data["medianbatch_slices2_msignal"])))) )))) +
                            0.100000*np.tanh(np.where(np.where(data["mean_abs_chgbatch_msignal"] > -998, data["meanbatch_slices2_msignal"], np.tanh((data["stdbatch_msignal"])) ) > -998, data["signal_shift_-1"], data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2_msignal"] > -998, data["medianbatch_msignal"], ((data["minbatch"]) + ((((4.0)) * ((((data["maxtominbatch_slices2_msignal"]) + (data["meanbatch_slices2_msignal"]))/2.0))))) )) +
                            0.100000*np.tanh(np.where(((((data["minbatch"]) * (data["maxbatch_slices2"]))) + (np.tanh((((data["meanbatch_slices2_msignal"]) * 2.0))))) <= -998, ((np.where(data["meanbatch_msignal"] <= -998, data["signal_shift_-1"], data["abs_avgbatch_msignal"] )) * 2.0), data["meanbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(((((data["maxbatch_slices2"]) - ((7.0)))) - (((data["abs_maxbatch_msignal"]) - (data["maxbatch_slices2"])))) > -998, ((data["maxbatch_slices2"]) - ((7.0))), ((data["maxbatch_slices2"]) - ((7.0))) )) +
                            0.100000*np.tanh(np.where(((data["medianbatch_slices2"]) * (data["medianbatch_slices2_msignal"])) > -998, ((((((data["signal"]) / 2.0)) / 2.0)) * (np.where(data["minbatch_slices2_msignal"] > -998, data["abs_avgbatch_slices2_msignal"], data["abs_avgbatch_slices2_msignal"] ))), data["medianbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (((data["minbatch_msignal"]) + (np.where((13.45460319519042969) > -998, (13.45460319519042969), data["meanbatch_slices2_msignal"] )))))) +
                            0.100000*np.tanh(((np.where(data["minbatch_slices2"] <= -998, np.where((((-((((data["meanbatch_slices2_msignal"]) - (data["minbatch_slices2_msignal"])))))) / 2.0) <= -998, data["maxbatch_msignal"], (-((data["abs_maxbatch"]))) ), data["minbatch_msignal"] )) * 2.0)) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_msignal"]) +
                            0.100000*np.tanh(((np.where(data["stdbatch_slices2"] <= -998, ((data["minbatch_slices2_msignal"]) - (((((data["abs_avgbatch_msignal"]) * 2.0)) * 2.0))), np.where(data["signal_shift_+1_msignal"] > -998, data["abs_avgbatch_slices2_msignal"], data["mean_abs_chgbatch_slices2"] ) )) / 2.0)) +
                            0.100000*np.tanh(np.where((9.0) <= -998, ((data["abs_maxbatch_msignal"]) / 2.0), (((((((((((data["abs_maxbatch_msignal"]) * 2.0)) - ((13.37454128265380859)))) * 2.0)) * 2.0)) + (data["abs_maxbatch_msignal"]))/2.0) )) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where(np.tanh(((-(((5.0)))))) > -998, data["minbatch_msignal"], (-(((((data["signal_shift_-1"]) + ((-((data["mean_abs_chgbatch_slices2_msignal"])))))/2.0)))) )) +
                            0.100000*np.tanh(((np.where(data["signal_shift_-1_msignal"] > -998, ((((np.where((9.0) <= -998, data["maxbatch_msignal"], data["rangebatch_msignal"] )) - ((9.0)))) * 2.0), (10.0) )) * 2.0)) +
                            0.100000*np.tanh(((((data["abs_maxbatch_msignal"]) - ((6.0)))) * 2.0)) +
                            0.100000*np.tanh(np.tanh((data["maxtominbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (data["maxbatch_msignal"]))) +
                            0.100000*np.tanh(((((data["meanbatch_slices2_msignal"]) * ((((((10.04012966156005859)) * ((9.0)))) - (((data["meanbatch_msignal"]) - ((((data["abs_avgbatch_slices2"]) + (data["medianbatch_msignal"]))/2.0)))))))) * 2.0)) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) * (np.where((-((data["abs_avgbatch_slices2_msignal"]))) <= -998, ((data["stdbatch_slices2"]) * (np.where((3.0) <= -998, data["meanbatch_slices2"], (-((data["signal_shift_-1"]))) ))), (-((data["abs_avgbatch_slices2_msignal"]))) )))) +
                            0.100000*np.tanh(data["stdbatch_msignal"]) +
                            0.100000*np.tanh((((((data["maxtominbatch_slices2"]) / 2.0)) + (np.where(((data["abs_avgbatch_slices2_msignal"]) / 2.0) <= -998, data["minbatch_slices2"], data["mean_abs_chgbatch_slices2_msignal"] )))/2.0)) +
                            0.100000*np.tanh(np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) + (((((data["signal"]) * 2.0)) * (data["abs_maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) * (((data["stdbatch_slices2"]) - (np.where((4.0) > -998, (1.61215817928314209), data["meanbatch_slices2"] )))))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) * ((-((data["mean_abs_chgbatch_msignal"])))))) +
                            0.100000*np.tanh(((np.tanh((((np.tanh((data["medianbatch_slices2_msignal"]))) - (np.tanh(((((-(((-(((((data["rangebatch_slices2"]) + (data["medianbatch_slices2_msignal"]))/2.0)))))))) * 2.0)))))))) * 2.0)) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.where((-((((((data["medianbatch_slices2_msignal"]) * 2.0)) * (data["medianbatch_slices2_msignal"]))))) > -998, (-((((((((data["medianbatch_slices2_msignal"]) * 2.0)) + (data["minbatch_slices2_msignal"]))) * (data["medianbatch_slices2_msignal"]))))), data["abs_maxbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2"] > -998, ((np.tanh((((((data["minbatch_slices2"]) * (data["mean_abs_chgbatch_msignal"]))) * 2.0)))) / 2.0), data["stdbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((-((np.tanh((data["maxbatch_slices2"])))))) +
                            0.100000*np.tanh(((np.where(data["abs_avgbatch_slices2_msignal"] > -998, np.where(np.where(data["signal"] <= -998, data["mean_abs_chgbatch_slices2_msignal"], data["meanbatch_slices2_msignal"] ) > -998, np.tanh((data["meanbatch_msignal"])), data["stdbatch_slices2"] ), data["meanbatch_msignal"] )) * 2.0)) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) / 2.0)) +
                            0.100000*np.tanh(((((((((data["maxbatch_slices2"]) / 2.0)) * 2.0)) * (((data["maxtominbatch"]) * (data["meanbatch_slices2_msignal"]))))) - (((data["minbatch_msignal"]) * (data["maxtominbatch"]))))) +
                            0.100000*np.tanh(((((((data["meanbatch_slices2_msignal"]) * 2.0)) * (data["medianbatch_msignal"]))) - ((((((data["medianbatch_msignal"]) * 2.0)) + (data["mean_abs_chgbatch_slices2"]))/2.0)))) +
                            0.100000*np.tanh((((((((((data["maxbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))) / 2.0)) * (data["abs_maxbatch_msignal"]))) + (((((((((data["abs_maxbatch_msignal"]) / 2.0)) * 2.0)) / 2.0)) - ((13.80771827697753906)))))/2.0)) +
                            0.100000*np.tanh((-(((((9.0)) - (np.where(np.tanh((data["mean_abs_chgbatch_slices2"])) <= -998, (9.0), data["rangebatch_slices2"] ))))))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (((data["signal_shift_-1"]) * 2.0)))) +
                            0.100000*np.tanh(np.tanh((data["maxtominbatch_slices2"]))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - (np.where(np.tanh((data["maxtominbatch"])) <= -998, data["minbatch_slices2_msignal"], (((data["stdbatch_slices2_msignal"]) + (data["stdbatch_slices2"]))/2.0) )))) +
                            0.100000*np.tanh((-(((((6.0)) + (data["minbatch_msignal"])))))) +
                            0.100000*np.tanh(((((((data["minbatch_slices2_msignal"]) / 2.0)) * 2.0)) + (data["stdbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - (((np.tanh((data["abs_avgbatch_slices2"]))) * (data["meanbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(((data["maxtominbatch"]) - (((data["medianbatch_msignal"]) * (data["abs_minbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((-((np.tanh((data["abs_maxbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh(np.where(data["meanbatch_msignal"] > -998, ((data["signal"]) - (data["meanbatch_msignal"])), data["meanbatch_msignal"] )) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(((data["minbatch"]) + (data["minbatch"]))) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) * (data["medianbatch_slices2"]))) * (((np.where(data["mean_abs_chgbatch_slices2"] > -998, ((data["mean_abs_chgbatch_slices2"]) * 2.0), (((data["meanbatch_slices2_msignal"]) + (data["meanbatch_msignal"]))/2.0) )) - (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * (((((((data["meanbatch_slices2"]) * 2.0)) - (((((data["stdbatch_msignal"]) * (data["signal_shift_-1_msignal"]))) * (data["meanbatch_slices2"]))))) / 2.0)))) +
                            0.100000*np.tanh((((data["rangebatch_slices2_msignal"]) + (data["medianbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(data["medianbatch_msignal"]) +
                            0.100000*np.tanh(np.where(((data["minbatch"]) - (data["minbatch_msignal"])) > -998, data["stdbatch_msignal"], data["stdbatch_msignal"] )) +
                            0.100000*np.tanh((((-(((((data["minbatch_msignal"]) + ((((9.0)) + (data["minbatch_msignal"]))))/2.0))))) * 2.0)) +
                            0.100000*np.tanh(((np.where(np.where(((((data["abs_maxbatch_slices2"]) / 2.0)) * (((data["mean_abs_chgbatch_slices2"]) * (data["mean_abs_chgbatch_slices2"])))) > -998, data["minbatch_msignal"], data["stdbatch_msignal"] ) <= -998, np.tanh((data["abs_minbatch_slices2"])), data["abs_minbatch_slices2"] )) / 2.0)) +
                            0.100000*np.tanh(np.tanh((data["stdbatch_msignal"]))) +
                            0.100000*np.tanh(((np.tanh((data["medianbatch_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2"] <= -998, data["meanbatch_msignal"], (-(((((data["medianbatch_slices2_msignal"]) + (data["abs_avgbatch_msignal"]))/2.0)))) )) +
                            0.100000*np.tanh(np.tanh((np.where(data["medianbatch_msignal"] <= -998, data["abs_minbatch_slices2"], data["medianbatch_msignal"] )))) +
                            0.100000*np.tanh(np.where(data["minbatch_msignal"] <= -998, ((data["maxtominbatch_slices2_msignal"]) + ((((5.51079654693603516)) + (data["signal_shift_-1_msignal"])))), (((((5.51079654693603516)) + (data["minbatch_msignal"]))) * (data["minbatch_msignal"])) )) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1"] > -998, data["meanbatch_msignal"], ((np.tanh((((data["maxbatch_slices2_msignal"]) + (data["maxtominbatch_slices2"]))))) * 2.0) )) +
                            0.100000*np.tanh((((-(((14.48416519165039062))))) - (((((data["medianbatch_slices2_msignal"]) + (data["rangebatch_slices2_msignal"]))) * (data["maxtominbatch_slices2"]))))) +
                            0.100000*np.tanh((((((((np.tanh((data["abs_maxbatch_slices2_msignal"]))) + (((data["abs_maxbatch_slices2_msignal"]) + (data["maxtominbatch_slices2_msignal"]))))) * 2.0)) + (data["maxtominbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((np.tanh(((((-((np.tanh((((np.tanh((data["maxtominbatch_slices2"]))) + (data["stdbatch_msignal"])))))))) * 2.0)))) * (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) + ((((((-((data["minbatch_slices2"])))) / 2.0)) + ((-((data["minbatch_slices2"])))))))) +
                            0.100000*np.tanh(np.tanh((((data["medianbatch_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(data["maxtominbatch_slices2"]) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((-(((13.80227470397949219))))) * (((data["rangebatch_slices2_msignal"]) - (data["mean_abs_chgbatch_slices2"]))))) +
                            0.100000*np.tanh((((data["stdbatch_slices2"]) + (data["signal"]))/2.0)) +
                            0.100000*np.tanh(np.tanh((((((data["meanbatch_msignal"]) + (((data["meanbatch_msignal"]) * (data["minbatch_msignal"]))))) * (((((data["meanbatch_msignal"]) + (((data["minbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))))) + (data["signal"]))))))) +
                            0.100000*np.tanh(((np.tanh((np.where(data["meanbatch_msignal"] <= -998, data["meanbatch_msignal"], ((((data["rangebatch_slices2_msignal"]) * (((data["signal_shift_+1_msignal"]) / 2.0)))) / 2.0) )))) + (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(data["maxtominbatch_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["signal"]) - ((-((data["medianbatch_msignal"])))))) +
                            0.100000*np.tanh((-((np.where(data["abs_maxbatch_slices2_msignal"] <= -998, (14.97682571411132812), (5.23909616470336914) ))))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2"]) * (((np.where(data["abs_maxbatch_msignal"] > -998, data["abs_avgbatch_slices2"], np.tanh((data["signal_shift_-1_msignal"])) )) * 2.0)))) +
                            0.100000*np.tanh(np.tanh((((data["minbatch_slices2_msignal"]) - ((((0.0)) * (np.where(((data["rangebatch_slices2_msignal"]) / 2.0) > -998, ((data["rangebatch_slices2_msignal"]) / 2.0), data["signal"] )))))))))    
    
    def GP_class_7(self,data):
        return self.Output(-2.939522 +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] <= -998, data["maxtominbatch_slices2"], np.where(data["signal"] > -998, ((data["signal"]) * 2.0), data["abs_minbatch_slices2_msignal"] ) )) +
                            0.100000*np.tanh(((np.tanh(((((data["signal"]) + (data["signal"]))/2.0)))) + (np.where(data["maxbatch_slices2"] > -998, data["meanbatch_slices2"], data["maxbatch_slices2"] )))) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] > -998, data["signal"], np.tanh((data["signal"])) )) +
                            0.100000*np.tanh(np.where(np.where(data["maxtominbatch_slices2"] <= -998, data["abs_avgbatch_msignal"], data["signal_shift_-1"] ) <= -998, data["meanbatch_msignal"], np.where(data["signal_shift_+1"] <= -998, data["minbatch_msignal"], (-((data["stdbatch_msignal"]))) ) )) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - ((7.63624000549316406)))) +
                            0.100000*np.tanh((((((((data["minbatch_slices2"]) + (data["signal"]))/2.0)) + (((data["signal_shift_-1"]) / 2.0)))) + (data["signal_shift_-1"]))) +
                            0.100000*np.tanh((((((data["medianbatch_slices2"]) + (data["medianbatch_msignal"]))/2.0)) / 2.0)) +
                            0.100000*np.tanh(np.where(data["stdbatch_slices2_msignal"] > -998, (((data["medianbatch_slices2"]) + (((np.where(data["medianbatch_slices2"] > -998, ((data["medianbatch_msignal"]) * 2.0), data["medianbatch_slices2"] )) * 2.0)))/2.0), (-((data["maxtominbatch"]))) )) +
                            0.100000*np.tanh(np.tanh((data["abs_minbatch_msignal"]))) +
                            0.100000*np.tanh(((((data["signal_shift_-1"]) - (data["abs_avgbatch_slices2_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(((np.where(data["meanbatch_slices2"] <= -998, data["meanbatch_slices2"], data["abs_maxbatch"] )) - ((8.0)))) +
                            0.100000*np.tanh((((((np.where(data["meanbatch_slices2_msignal"] <= -998, data["minbatch_slices2"], data["meanbatch_msignal"] )) + (np.where(((((data["medianbatch_slices2_msignal"]) * 2.0)) / 2.0) <= -998, data["mean_abs_chgbatch_slices2"], data["medianbatch_msignal"] )))/2.0)) * (data["medianbatch_slices2"]))) +
                            0.100000*np.tanh((((data["meanbatch_slices2"]) + (((data["medianbatch_slices2_msignal"]) * 2.0)))/2.0)) +
                            0.100000*np.tanh(((((((data["mean_abs_chgbatch_slices2"]) / 2.0)) * (data["medianbatch_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) - ((-((data["medianbatch_slices2"])))))) +
                            0.100000*np.tanh(np.tanh((((((np.where(data["meanbatch_slices2_msignal"] <= -998, ((data["meanbatch_slices2_msignal"]) * 2.0), data["medianbatch_msignal"] )) / 2.0)) * 2.0)))) +
                            0.100000*np.tanh(((((((data["abs_avgbatch_slices2_msignal"]) * (data["minbatch_slices2_msignal"]))) * (data["medianbatch_msignal"]))) + (((data["meanbatch_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) + ((-((data["maxtominbatch"])))))) - (data["stdbatch_msignal"]))) +
                            0.100000*np.tanh(((((data["signal_shift_-1"]) * (((data["abs_maxbatch_msignal"]) * (((data["abs_maxbatch_msignal"]) - ((4.0)))))))) - ((9.77668571472167969)))) +
                            0.100000*np.tanh((((data["rangebatch_slices2_msignal"]) + (((data["rangebatch_slices2_msignal"]) + ((-(((5.0))))))))/2.0)) +
                            0.100000*np.tanh((((((((data["maxbatch_msignal"]) * 2.0)) + (np.tanh((((data["maxbatch_msignal"]) - (((((data["maxbatch_msignal"]) * 2.0)) * 2.0)))))))) + (data["mean_abs_chgbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh((((data["signal_shift_+1_msignal"]) + ((-((np.where(data["medianbatch_slices2"] <= -998, data["rangebatch_msignal"], ((((-((data["abs_minbatch_msignal"])))) + (data["maxtominbatch_msignal"]))/2.0) ))))))/2.0)) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) - ((((11.44612216949462891)) + (((data["signal_shift_+1"]) + (data["abs_minbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh(np.where((5.84053659439086914) <= -998, np.tanh(((0.0))), ((data["abs_maxbatch_slices2"]) - ((5.84053659439086914))) )) +
                            0.100000*np.tanh(((((((((data["abs_avgbatch_msignal"]) - (((data["medianbatch_slices2_msignal"]) * (data["medianbatch_slices2_msignal"]))))) + (data["abs_avgbatch_msignal"]))) - (((data["meanbatch_slices2_msignal"]) * (data["medianbatch_msignal"]))))) * 2.0)) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) - (((np.where((((-((((data["medianbatch_msignal"]) * (data["rangebatch_slices2_msignal"])))))) * (data["rangebatch_msignal"])) > -998, data["meanbatch_slices2_msignal"], data["rangebatch_msignal"] )) * (((data["meanbatch_slices2_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) - (((data["abs_maxbatch_slices2"]) + (np.where(data["maxtominbatch_msignal"] <= -998, data["maxtominbatch_msignal"], (((data["abs_maxbatch_slices2"]) + (((data["abs_maxbatch"]) * ((-((data["maxbatch_msignal"])))))))/2.0) )))))) +
                            0.100000*np.tanh(((data["meanbatch_slices2"]) + (((data["medianbatch_msignal"]) * (((((((np.tanh(((-((data["minbatch_msignal"])))))) + ((-((data["abs_minbatch_slices2"])))))) - (data["medianbatch_msignal"]))) - (data["medianbatch_msignal"]))))))) +
                            0.100000*np.tanh(np.where(((data["rangebatch_msignal"]) - (data["rangebatch_msignal"])) > -998, (((((((data["rangebatch_slices2"]) + (data["stdbatch_slices2"]))/2.0)) * (data["stdbatch_slices2"]))) - ((8.0))), data["maxbatch_msignal"] )) +
                            0.100000*np.tanh((-((data["meanbatch_msignal"])))) +
                            0.100000*np.tanh(((((data["signal"]) + (data["maxtominbatch"]))) - (((np.where(((data["signal_shift_+1"]) / 2.0) > -998, data["medianbatch_msignal"], ((data["rangebatch_slices2_msignal"]) * ((-((data["abs_maxbatch_slices2"]))))) )) * 2.0)))) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_slices2"] <= -998, data["abs_avgbatch_slices2_msignal"], ((((data["medianbatch_msignal"]) * (((data["rangebatch_slices2_msignal"]) * 2.0)))) - (np.where(data["abs_avgbatch_slices2_msignal"] <= -998, data["abs_maxbatch"], data["abs_minbatch_slices2_msignal"] ))) )) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - (np.where((((4.61900424957275391)) - (data["stdbatch_msignal"])) <= -998, data["signal"], (4.61900424957275391) )))) +
                            0.100000*np.tanh(data["maxbatch_slices2"]) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(((np.where((0.0) <= -998, data["minbatch_msignal"], (-(((5.85408735275268555)))) )) - (data["minbatch_msignal"]))) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(data["maxtominbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) - (((data["minbatch"]) * (np.where(data["minbatch"] <= -998, ((data["medianbatch_slices2"]) + (np.tanh((data["minbatch_msignal"])))), data["meanbatch_slices2"] )))))) +
                            0.100000*np.tanh((((data["minbatch_slices2_msignal"]) + (((np.where(data["maxbatch_slices2_msignal"] <= -998, ((data["rangebatch_msignal"]) + (data["maxbatch_slices2_msignal"])), data["minbatch_slices2_msignal"] )) * (np.where(data["minbatch_slices2_msignal"] <= -998, data["abs_maxbatch_slices2_msignal"], data["abs_maxbatch_msignal"] )))))/2.0)) +
                            0.100000*np.tanh(((((14.32711219787597656)) + ((((((-((data["meanbatch_msignal"])))) - ((((((np.tanh((data["medianbatch_slices2_msignal"]))) + ((((14.32711219787597656)) * (data["meanbatch_slices2_msignal"]))))/2.0)) * 2.0)))) * (data["medianbatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh((((data["abs_avgbatch_msignal"]) + (np.tanh(((((data["meanbatch_msignal"]) + (data["maxtominbatch_slices2"]))/2.0)))))/2.0)) +
                            0.100000*np.tanh(((((((((data["abs_maxbatch_msignal"]) - ((((7.0)) - (data["abs_maxbatch_msignal"]))))) + (data["meanbatch_msignal"]))) * 2.0)) * 2.0)) +
                            0.100000*np.tanh((((((((5.0)) * 2.0)) * 2.0)) * (((data["rangebatch_slices2"]) - (np.where(data["meanbatch_slices2_msignal"] <= -998, (((5.0)) * 2.0), (((5.0)) * 2.0) )))))) +
                            0.100000*np.tanh(np.where(data["abs_maxbatch_msignal"] <= -998, data["abs_maxbatch_msignal"], ((((((data["abs_maxbatch_slices2_msignal"]) - ((3.80149221420288086)))) * (data["abs_maxbatch_msignal"]))) * (((data["abs_maxbatch_msignal"]) * 2.0))) )) +
                            0.100000*np.tanh((((data["meanbatch_slices2"]) + (((((((data["maxbatch_slices2"]) - ((10.0)))) + (data["meanbatch_slices2"]))) - ((-((data["maxtominbatch_slices2"])))))))/2.0)) +
                            0.100000*np.tanh(((np.where(((data["rangebatch_slices2"]) * 2.0) <= -998, data["mean_abs_chgbatch_slices2_msignal"], data["minbatch_slices2_msignal"] )) + (np.where(data["rangebatch_msignal"] <= -998, data["minbatch_slices2"], ((data["rangebatch_slices2"]) - ((3.43867135047912598))) )))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_msignal"] <= -998, np.where((5.0) <= -998, data["abs_maxbatch_slices2_msignal"], data["medianbatch_slices2_msignal"] ), np.where(data["meanbatch_slices2_msignal"] > -998, ((data["abs_minbatch_msignal"]) - ((6.94710493087768555))), (-(((6.94710493087768555)))) ) )) +
                            0.100000*np.tanh(((((np.where(data["abs_minbatch_msignal"] > -998, ((data["rangebatch_slices2"]) - (data["minbatch_msignal"])), np.where(data["maxbatch_slices2"] > -998, data["maxbatch_slices2"], (8.39489746093750000) ) )) - ((14.97333526611328125)))) / 2.0)) +
                            0.100000*np.tanh(np.where(data["stdbatch_msignal"] > -998, ((data["minbatch_msignal"]) * ((((7.00788784027099609)) + (data["minbatch_msignal"])))), np.tanh((((data["abs_minbatch_msignal"]) * (((data["abs_minbatch_msignal"]) + (data["minbatch_msignal"])))))) )) +
                            0.100000*np.tanh(((data["rangebatch_slices2_msignal"]) + (np.where(((((data["maxtominbatch_msignal"]) + ((-((((data["maxtominbatch_msignal"]) + (data["meanbatch_msignal"])))))))) / 2.0) > -998, data["maxtominbatch_msignal"], ((data["abs_avgbatch_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh(((((data["minbatch_slices2"]) + (data["maxtominbatch_slices2_msignal"]))) + (np.where(np.tanh((np.where(data["maxtominbatch_slices2"] > -998, data["signal_shift_+1_msignal"], data["rangebatch_msignal"] ))) > -998, data["signal_shift_+1_msignal"], data["maxtominbatch_slices2"] )))) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2"]) * (np.where(data["medianbatch_msignal"] > -998, data["medianbatch_msignal"], data["maxbatch_slices2"] )))) * 2.0)) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (((np.where(data["rangebatch_msignal"] > -998, data["abs_maxbatch_msignal"], np.where(data["rangebatch_msignal"] > -998, data["abs_maxbatch_msignal"], (((((7.16786575317382812)) * 2.0)) + (data["rangebatch_msignal"])) ) )) * 2.0)))) +
                            0.100000*np.tanh((-((((data["meanbatch_slices2_msignal"]) * (np.where(data["rangebatch_slices2"] > -998, data["meanbatch_slices2_msignal"], ((data["maxtominbatch_slices2"]) * (data["rangebatch_msignal"])) ))))))) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * ((-((np.where((-((np.where(data["meanbatch_slices2_msignal"] > -998, data["meanbatch_slices2_msignal"], data["medianbatch_msignal"] )))) > -998, data["medianbatch_msignal"], (-((data["meanbatch_slices2_msignal"]))) ))))))) +
                            0.100000*np.tanh((((np.where((-(((2.0)))) <= -998, data["meanbatch_msignal"], data["abs_maxbatch_slices2_msignal"] )) + (((np.tanh((data["meanbatch_msignal"]))) + (((data["signal_shift_-1"]) * (data["meanbatch_msignal"]))))))/2.0)) +
                            0.100000*np.tanh(np.tanh((np.where(np.tanh((data["abs_maxbatch"])) > -998, data["maxtominbatch"], (-(((-((data["abs_maxbatch_slices2"])))))) )))) +
                            0.100000*np.tanh(np.tanh(((-((data["maxtominbatch_slices2"])))))) +
                            0.100000*np.tanh(np.where(((((3.0)) + ((3.0)))/2.0) <= -998, (3.0), data["abs_avgbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((((-(((7.0))))) - ((((np.where(((((7.0)) + (data["abs_maxbatch_slices2_msignal"]))/2.0) <= -998, data["maxtominbatch_msignal"], (-(((7.0)))) )) + (data["minbatch_msignal"]))/2.0)))) * 2.0)) +
                            0.100000*np.tanh(((((((data["abs_avgbatch_slices2"]) + (np.where(data["minbatch_slices2_msignal"] > -998, data["signal"], ((data["maxtominbatch"]) * 2.0) )))/2.0)) + (data["maxtominbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(((data["signal"]) - (((((data["medianbatch_slices2_msignal"]) * (data["medianbatch_msignal"]))) * (((data["rangebatch_slices2_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh((-((np.tanh((data["meanbatch_msignal"])))))) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) + (((np.where((((-((data["abs_minbatch_slices2"])))) + (data["maxtominbatch_msignal"])) <= -998, data["abs_minbatch_slices2_msignal"], data["rangebatch_msignal"] )) + (data["maxtominbatch_msignal"]))))) +
                            0.100000*np.tanh(((np.where((3.0) <= -998, np.tanh(((3.0))), data["minbatch_msignal"] )) * (((((((3.0)) * 2.0)) + (data["minbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh(np.tanh((data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * ((-(((((data["medianbatch_msignal"]) + (((((data["medianbatch_msignal"]) / 2.0)) * 2.0)))/2.0))))))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) + (((((data["stdbatch_slices2"]) / 2.0)) - (((((((data["meanbatch_msignal"]) * (data["meanbatch_msignal"]))) * 2.0)) * 2.0)))))) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) + (np.where(data["abs_avgbatch_slices2_msignal"] > -998, np.where(((data["medianbatch_msignal"]) / 2.0) > -998, ((data["medianbatch_msignal"]) * 2.0), ((data["medianbatch_slices2_msignal"]) * 2.0) ), data["maxtominbatch_msignal"] )))) +
                            0.100000*np.tanh(data["abs_avgbatch_slices2_msignal"]) +
                            0.100000*np.tanh(np.tanh((((np.tanh((data["minbatch_slices2"]))) * (np.tanh((data["abs_avgbatch_slices2"]))))))) +
                            0.100000*np.tanh(np.tanh((np.where(((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0) > -998, data["meanbatch_slices2"], ((data["meanbatch_slices2"]) * 2.0) )))) +
                            0.100000*np.tanh((-((np.where((-((((((data["meanbatch_msignal"]) / 2.0)) * (data["medianbatch_slices2_msignal"]))))) <= -998, data["minbatch"], ((((data["meanbatch_msignal"]) * 2.0)) * (data["medianbatch_msignal"])) ))))) +
                            0.100000*np.tanh((((1.0)) * (data["rangebatch_msignal"]))) +
                            0.100000*np.tanh(((data["rangebatch_slices2_msignal"]) - (((data["meanbatch_msignal"]) * (((data["medianbatch_msignal"]) * (data["abs_maxbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(np.tanh((np.where(((((data["signal_shift_+1_msignal"]) / 2.0)) * 2.0) <= -998, ((((data["minbatch_slices2"]) / 2.0)) * 2.0), ((data["medianbatch_slices2_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh(((((data["signal_shift_+1"]) - (np.where(data["minbatch_slices2_msignal"] > -998, data["minbatch"], data["minbatch_slices2"] )))) - (np.where((6.85090303421020508) > -998, (6.85090303421020508), data["stdbatch_msignal"] )))) +
                            0.100000*np.tanh(data["maxtominbatch"]) +
                            0.100000*np.tanh((((((((((((((((1.0)) - (data["meanbatch_msignal"]))) * 2.0)) * 2.0)) * 2.0)) * 2.0)) * 2.0)) - ((1.0)))) +
                            0.100000*np.tanh(((((np.where(data["maxbatch_slices2_msignal"] <= -998, data["abs_minbatch_slices2"], data["meanbatch_slices2_msignal"] )) / 2.0)) + (((((data["meanbatch_slices2_msignal"]) + (data["abs_avgbatch_slices2"]))) * 2.0)))) +
                            0.100000*np.tanh(((data["abs_minbatch_msignal"]) / 2.0)) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] > -998, ((data["maxtominbatch"]) - (((data["stdbatch_slices2_msignal"]) * (data["medianbatch_slices2"])))), ((data["maxtominbatch"]) - (((data["minbatch"]) * ((((0.26543861627578735)) - (data["minbatch_slices2"])))))) )) +
                            0.100000*np.tanh(((data["abs_maxbatch_msignal"]) - (((((data["meanbatch_msignal"]) * (((((data["meanbatch_msignal"]) * 2.0)) * 2.0)))) * 2.0)))) +
                            0.100000*np.tanh((((((data["medianbatch_msignal"]) * 2.0)) + (((data["mean_abs_chgbatch_slices2"]) / 2.0)))/2.0)) +
                            0.100000*np.tanh(np.where(data["maxbatch_msignal"] <= -998, data["abs_avgbatch_msignal"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(np.where(((data["medianbatch_slices2_msignal"]) / 2.0) <= -998, data["maxtominbatch_slices2"], np.tanh(((((data["abs_minbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"]))/2.0))) )) +
                            0.100000*np.tanh(((np.where(((data["maxbatch_slices2_msignal"]) - ((4.0))) > -998, data["maxtominbatch_slices2_msignal"], np.tanh((data["maxtominbatch_slices2_msignal"])) )) / 2.0)) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) / 2.0)) +
                            0.100000*np.tanh((-((((data["medianbatch_msignal"]) * (data["abs_avgbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh(((data["abs_maxbatch_slices2_msignal"]) / 2.0)) +
                            0.100000*np.tanh(np.where((((data["maxtominbatch_slices2_msignal"]) + (data["abs_avgbatch_slices2_msignal"]))/2.0) <= -998, data["medianbatch_slices2_msignal"], data["abs_minbatch_msignal"] )) +
                            0.100000*np.tanh(((np.where(((data["abs_maxbatch_slices2_msignal"]) * 2.0) > -998, data["signal"], data["medianbatch_msignal"] )) + (((data["medianbatch_msignal"]) * (data["abs_maxbatch"]))))) +
                            0.100000*np.tanh((((((data["rangebatch_slices2_msignal"]) + (data["abs_minbatch_slices2"]))/2.0)) - (np.where(((data["medianbatch_msignal"]) * 2.0) > -998, ((data["medianbatch_msignal"]) * (((((data["medianbatch_msignal"]) * 2.0)) * 2.0))), ((data["medianbatch_msignal"]) * 2.0) )))) +
                            0.100000*np.tanh(((((data["minbatch_slices2"]) * (np.where(data["minbatch_slices2_msignal"] <= -998, data["rangebatch_slices2_msignal"], ((data["abs_avgbatch_msignal"]) * (data["mean_abs_chgbatch_msignal"])) )))) - (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * ((((data["signal_shift_-1_msignal"]) + (np.where(data["mean_abs_chgbatch_slices2_msignal"] <= -998, data["mean_abs_chgbatch_slices2"], ((data["maxbatch_msignal"]) / 2.0) )))/2.0)))) +
                            0.100000*np.tanh(data["rangebatch_slices2_msignal"]) +
                            0.100000*np.tanh((-((data["signal_shift_+1_msignal"])))))    
        
    def GP_class_8(self,data):
        return self.Output(-3.012512 +
                            0.100000*np.tanh(np.where(data["signal_shift_+1"] <= -998, data["signal_shift_+1"], ((data["rangebatch_slices2"]) - (np.where(data["medianbatch_slices2"] > -998, (9.44130611419677734), np.where(data["medianbatch_slices2"] <= -998, data["meanbatch_slices2_msignal"], data["medianbatch_msignal"] ) ))) )) +
                            0.100000*np.tanh(np.where(((np.where((((((data["signal_shift_+1"]) + (data["meanbatch_slices2"]))/2.0)) / 2.0) > -998, data["signal_shift_-1"], ((data["signal"]) / 2.0) )) / 2.0) > -998, data["signal"], data["maxbatch_slices2"] )) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) * 2.0)) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2"] <= -998, data["signal_shift_-1"], data["signal_shift_+1"] )) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1"] <= -998, ((data["signal_shift_-1"]) - (data["medianbatch_slices2"])), ((((data["signal_shift_-1"]) - (np.tanh((np.where(data["maxbatch_slices2_msignal"] <= -998, data["signal_shift_+1"], (6.0) )))))) - (data["meanbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(np.where(data["abs_avgbatch_slices2"] <= -998, data["signal"], ((data["signal"]) - (data["abs_avgbatch_slices2"])) )) +
                            0.100000*np.tanh(np.where((-((data["medianbatch_slices2"]))) > -998, data["medianbatch_slices2"], data["signal_shift_-1"] )) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] > -998, data["medianbatch_slices2"], ((data["medianbatch_slices2_msignal"]) + (np.where(data["maxtominbatch_slices2"] > -998, data["signal"], data["signal_shift_+1"] ))) )) +
                            0.100000*np.tanh((((((((((data["meanbatch_msignal"]) + ((((-((data["stdbatch_slices2_msignal"])))) / 2.0)))/2.0)) * 2.0)) - (data["minbatch_slices2_msignal"]))) * ((((data["medianbatch_msignal"]) + (data["minbatch_slices2_msignal"]))/2.0)))) +
                            0.100000*np.tanh((-((data["meanbatch_msignal"])))) +
                            0.100000*np.tanh((-((data["medianbatch_msignal"])))) +
                            0.100000*np.tanh(np.where(((data["abs_avgbatch_slices2_msignal"]) * 2.0) <= -998, (((((((-(((3.0))))) * 2.0)) + ((3.0)))) * 2.0), (-((data["abs_avgbatch_slices2_msignal"]))) )) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) + (np.where(data["minbatch_slices2"] <= -998, ((((data["minbatch_slices2"]) + (np.tanh((data["abs_maxbatch_slices2_msignal"]))))) * 2.0), (-((((data["abs_maxbatch_slices2_msignal"]) * (np.tanh((data["medianbatch_msignal"]))))))) )))) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2_msignal"] <= -998, ((data["rangebatch_slices2"]) / 2.0), data["signal"] )) +
                            0.100000*np.tanh(((data["signal"]) - ((((data["meanbatch_msignal"]) + ((((((data["medianbatch_slices2"]) * 2.0)) + (np.tanh((data["stdbatch_slices2_msignal"]))))/2.0)))/2.0)))) +
                            0.100000*np.tanh(np.where((((((data["rangebatch_slices2"]) - ((9.0)))) + (data["stdbatch_slices2_msignal"]))/2.0) <= -998, (((((9.0)) * 2.0)) - ((4.60220336914062500))), ((((data["rangebatch_slices2"]) - ((9.0)))) / 2.0) )) +
                            0.100000*np.tanh(((data["meanbatch_msignal"]) * (np.where(data["signal_shift_+1"] > -998, data["mean_abs_chgbatch_slices2_msignal"], np.where(data["signal_shift_+1_msignal"] > -998, data["mean_abs_chgbatch_slices2_msignal"], np.where(data["abs_maxbatch_msignal"] > -998, data["mean_abs_chgbatch_slices2_msignal"], data["signal_shift_+1"] ) ) )))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) * (np.where(data["medianbatch_slices2_msignal"] > -998, data["abs_minbatch_msignal"], ((((data["medianbatch_msignal"]) * (data["minbatch_msignal"]))) * 2.0) )))) +
                            0.100000*np.tanh(((((data["medianbatch_slices2_msignal"]) * ((-(((7.0))))))) + ((-(((2.0))))))) +
                            0.100000*np.tanh(((data["maxbatch_slices2"]) - ((7.65225839614868164)))) +
                            0.100000*np.tanh(np.where(data["signal"] <= -998, np.tanh((((data["abs_avgbatch_slices2"]) + ((-((data["maxbatch_slices2"]))))))), (-((((data["abs_maxbatch_msignal"]) - (data["mean_abs_chgbatch_slices2_msignal"]))))) )) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) * (data["meanbatch_slices2"]))) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2_msignal"] > -998, data["mean_abs_chgbatch_slices2"], data["medianbatch_msignal"] )) +
                            0.100000*np.tanh(((np.where(data["abs_minbatch_msignal"] <= -998, (9.77578830718994141), (((3.0)) - (data["abs_maxbatch_slices2_msignal"])) )) * (((data["abs_maxbatch_msignal"]) + (((data["abs_minbatch_msignal"]) * 2.0)))))) +
                            0.100000*np.tanh(((((data["rangebatch_slices2_msignal"]) / 2.0)) + (data["mean_abs_chgbatch_slices2"]))) +
                            0.100000*np.tanh(((np.tanh(((-((np.where(data["meanbatch_slices2_msignal"] > -998, (5.74424171447753906), ((np.tanh((data["signal"]))) * ((-((data["maxtominbatch_msignal"]))))) ))))))) * ((((data["minbatch_msignal"]) + ((9.0)))/2.0)))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (((((4.0)) + ((((12.46765041351318359)) + (data["minbatch_slices2"]))))/2.0)))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) - ((((data["signal"]) + (((data["rangebatch_msignal"]) + ((((data["rangebatch_slices2_msignal"]) + (data["abs_minbatch_slices2"]))/2.0)))))/2.0)))) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) * ((-(((((data["abs_avgbatch_slices2_msignal"]) + (np.where(((data["abs_avgbatch_slices2_msignal"]) * (data["abs_avgbatch_slices2_msignal"])) > -998, data["maxbatch_slices2_msignal"], data["abs_avgbatch_slices2_msignal"] )))/2.0))))))) * (data["maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((-((data["medianbatch_msignal"])))) +
                            0.100000*np.tanh(((data["maxbatch_msignal"]) - ((1.99520635604858398)))) +
                            0.100000*np.tanh(((np.where(data["minbatch_slices2"] > -998, data["minbatch_slices2_msignal"], data["mean_abs_chgbatch_slices2"] )) - (((data["minbatch_msignal"]) * (np.where(data["minbatch_msignal"] <= -998, data["minbatch_msignal"], data["mean_abs_chgbatch_slices2"] )))))) +
                            0.100000*np.tanh((-((np.where(data["minbatch_slices2"] <= -998, data["medianbatch_slices2_msignal"], data["signal_shift_+1"] ))))) +
                            0.100000*np.tanh(((((data["abs_maxbatch_msignal"]) + (data["meanbatch_slices2_msignal"]))) * ((-((data["medianbatch_msignal"])))))) +
                            0.100000*np.tanh(((((data["maxbatch_slices2"]) + (np.where(data["maxtominbatch_slices2"] > -998, (((data["stdbatch_msignal"]) + (data["stdbatch_msignal"]))/2.0), (-((data["medianbatch_slices2"]))) )))) * 2.0)) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(((data["stdbatch_slices2"]) * (np.where(((data["maxbatch_msignal"]) + (data["maxbatch_slices2_msignal"])) <= -998, data["abs_maxbatch_slices2_msignal"], (((data["minbatch_slices2_msignal"]) + (((data["maxbatch_slices2_msignal"]) * (data["maxbatch_msignal"]))))/2.0) )))) +
                            0.100000*np.tanh(((((data["maxbatch_msignal"]) - ((((4.0)) - (data["maxbatch_msignal"]))))) - ((((4.0)) / 2.0)))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2"]) - ((((12.57265377044677734)) - (data["signal_shift_-1"]))))) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) - (((data["meanbatch_slices2_msignal"]) * ((((data["maxbatch_msignal"]) + (((np.tanh(((((data["abs_maxbatch"]) + (data["maxbatch_msignal"]))/2.0)))) * 2.0)))/2.0)))))) +
                            0.100000*np.tanh((-((((np.where(np.tanh((((((data["medianbatch_msignal"]) * 2.0)) * (data["minbatch_msignal"])))) > -998, data["meanbatch_msignal"], ((((data["abs_maxbatch_msignal"]) * 2.0)) * (data["medianbatch_slices2"])) )) * 2.0))))) +
                            0.100000*np.tanh(np.where(data["maxbatch_slices2_msignal"] <= -998, data["abs_avgbatch_msignal"], ((data["abs_minbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_msignal"])) )) +
                            0.100000*np.tanh(data["medianbatch_slices2"]) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + ((-((data["rangebatch_msignal"])))))) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) + (((data["maxbatch_slices2_msignal"]) * (np.where(data["abs_maxbatch_msignal"] <= -998, data["maxbatch_slices2_msignal"], data["abs_maxbatch_msignal"] )))))) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh((((((np.tanh((((data["medianbatch_slices2"]) + (((data["abs_avgbatch_msignal"]) - (np.tanh((data["abs_minbatch_slices2_msignal"]))))))))) + (data["abs_avgbatch_msignal"]))) + (np.where(data["medianbatch_slices2"] > -998, data["abs_maxbatch"], data["maxtominbatch"] )))/2.0)) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] <= -998, data["abs_maxbatch_msignal"], ((data["mean_abs_chgbatch_msignal"]) + (((data["mean_abs_chgbatch_slices2_msignal"]) - (data["abs_maxbatch_msignal"])))) )) +
                            0.100000*np.tanh(((data["maxtominbatch"]) + ((((((-((np.where(data["minbatch_slices2"] <= -998, data["maxbatch_slices2_msignal"], ((((data["maxtominbatch_slices2_msignal"]) / 2.0)) * 2.0) ))))) / 2.0)) * (((data["maxtominbatch"]) - (data["mean_abs_chgbatch_msignal"]))))))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) / 2.0)) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) + (((data["maxbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))))) +
                            0.100000*np.tanh(((data["medianbatch_slices2"]) - ((((10.0)) + ((-((np.where(data["medianbatch_slices2_msignal"] <= -998, ((data["maxtominbatch_msignal"]) + (np.where(data["abs_avgbatch_slices2"] <= -998, data["maxtominbatch_slices2_msignal"], data["stdbatch_msignal"] ))), data["rangebatch_msignal"] ))))))))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - (np.where(((data["rangebatch_slices2"]) - (data["abs_minbatch_msignal"])) <= -998, np.where((8.46519660949707031) > -998, data["meanbatch_slices2"], np.where(data["signal_shift_-1_msignal"] > -998, (8.46519660949707031), data["minbatch_msignal"] ) ), (8.46519660949707031) )))) +
                            0.100000*np.tanh(np.where(np.where(data["abs_minbatch_slices2"] > -998, data["abs_minbatch_slices2_msignal"], data["mean_abs_chgbatch_slices2_msignal"] ) > -998, np.where(data["minbatch_msignal"] <= -998, ((data["minbatch_slices2_msignal"]) * 2.0), data["minbatch_msignal"] ), data["minbatch_msignal"] )) +
                            0.100000*np.tanh(((data["maxtominbatch"]) - (np.tanh((data["minbatch_slices2"]))))) +
                            0.100000*np.tanh((((data["minbatch_msignal"]) + (((data["abs_avgbatch_slices2"]) / 2.0)))/2.0)) +
                            0.100000*np.tanh((((((-(((-(((-((data["maxbatch_msignal"])))))))))) + ((-((data["meanbatch_msignal"])))))) * (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2_msignal"] <= -998, data["maxtominbatch_slices2"], ((data["maxbatch_slices2"]) + (np.where(data["medianbatch_slices2_msignal"] > -998, data["maxtominbatch_slices2_msignal"], ((data["maxtominbatch_slices2_msignal"]) * 2.0) ))) )) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(data["signal"]) +
                            0.100000*np.tanh(((data["minbatch_slices2_msignal"]) + (((data["minbatch"]) * (np.where((((((data["stdbatch_msignal"]) + (data["abs_minbatch_slices2_msignal"]))) + (data["minbatch"]))/2.0) <= -998, data["maxbatch_msignal"], data["stdbatch_msignal"] )))))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2"] <= -998, ((data["minbatch_slices2"]) * (data["minbatch_msignal"])), ((data["abs_minbatch_slices2"]) + (data["stdbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_msignal"]) - ((((np.tanh((np.tanh((np.tanh((data["stdbatch_msignal"]))))))) + (((data["abs_maxbatch_slices2_msignal"]) * (data["stdbatch_msignal"]))))/2.0)))) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2_msignal"]) + (data["abs_minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((np.where(data["rangebatch_slices2_msignal"] > -998, data["abs_maxbatch_slices2_msignal"], np.where((7.0) > -998, data["abs_maxbatch_slices2"], data["maxtominbatch_slices2_msignal"] ) )) + (np.where(data["rangebatch_slices2_msignal"] <= -998, data["medianbatch_slices2_msignal"], data["maxtominbatch"] )))) +
                            0.100000*np.tanh(((((np.where(data["medianbatch_msignal"] > -998, data["meanbatch_msignal"], data["maxbatch_msignal"] )) + (((((data["medianbatch_msignal"]) + (data["maxbatch_msignal"]))) * ((-((data["medianbatch_msignal"])))))))) * 2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((((np.where(data["stdbatch_slices2_msignal"] > -998, data["abs_avgbatch_msignal"], np.where(((data["maxtominbatch_slices2"]) - (data["medianbatch_slices2"])) > -998, data["medianbatch_msignal"], data["stdbatch_msignal"] ) )) * 2.0)))))) +
                            0.100000*np.tanh(((((np.where(data["maxtominbatch"] <= -998, data["meanbatch_msignal"], data["maxbatch_msignal"] )) * (((data["meanbatch_msignal"]) + (data["abs_maxbatch_slices2_msignal"]))))) / 2.0)) +
                            0.100000*np.tanh(np.where(np.where(((data["medianbatch_msignal"]) - (np.where(data["stdbatch_slices2"] <= -998, data["maxtominbatch"], (-((data["maxtominbatch_slices2_msignal"]))) ))) > -998, data["maxtominbatch_slices2_msignal"], data["stdbatch_slices2"] ) <= -998, data["stdbatch_slices2"], data["maxtominbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(np.where(np.tanh((data["minbatch_slices2_msignal"])) > -998, data["minbatch_slices2_msignal"], ((data["abs_maxbatch_msignal"]) * (data["maxtominbatch_msignal"])) )) +
                            0.100000*np.tanh(((((((((data["maxtominbatch_slices2_msignal"]) - (np.tanh((data["maxtominbatch_slices2"]))))) + (((((((data["abs_maxbatch_msignal"]) + (data["medianbatch_slices2_msignal"]))) * 2.0)) * (data["maxbatch_slices2_msignal"]))))) / 2.0)) / 2.0)) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) * 2.0)) - (np.tanh((data["maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((((-((((data["meanbatch_msignal"]) / 2.0))))) * 2.0)) +
                            0.100000*np.tanh(((data["stdbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(((data["rangebatch_msignal"]) + (np.tanh((data["minbatch_msignal"]))))) +
                            0.100000*np.tanh(((data["stdbatch_slices2"]) + (np.where((((data["medianbatch_msignal"]) + (data["meanbatch_msignal"]))/2.0) > -998, data["meanbatch_msignal"], ((data["stdbatch_slices2"]) + (((((data["stdbatch_slices2"]) + (data["meanbatch_msignal"]))) + (data["stdbatch_slices2"])))) )))) +
                            0.100000*np.tanh((((np.where(np.where(data["stdbatch_slices2_msignal"] <= -998, data["maxbatch_slices2_msignal"], data["stdbatch_slices2_msignal"] ) <= -998, ((data["stdbatch_slices2_msignal"]) - ((((data["maxtominbatch_slices2"]) + (data["maxbatch_slices2_msignal"]))/2.0))), data["mean_abs_chgbatch_slices2"] )) + (data["minbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh(np.where(data["signal_shift_+1_msignal"] <= -998, data["medianbatch_slices2_msignal"], (((data["abs_avgbatch_slices2_msignal"]) + (data["maxbatch_msignal"]))/2.0) )) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) + (data["maxtominbatch_msignal"]))) +
                            0.100000*np.tanh(((((((((((((data["signal_shift_+1_msignal"]) * (((data["maxbatch_slices2_msignal"]) / 2.0)))) - (((data["maxbatch_slices2"]) + (data["rangebatch_msignal"]))))) / 2.0)) / 2.0)) * 2.0)) * (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh(((((((data["abs_maxbatch_slices2_msignal"]) - ((3.23600721359252930)))) * ((3.10972166061401367)))) + (np.where((3.23601078987121582) > -998, data["abs_maxbatch_slices2_msignal"], (((data["abs_maxbatch_slices2_msignal"]) + (data["rangebatch_msignal"]))/2.0) )))) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * ((-((((data["stdbatch_slices2"]) + (data["meanbatch_msignal"])))))))) * 2.0)) +
                            0.100000*np.tanh(np.tanh((((data["abs_avgbatch_slices2_msignal"]) * (np.tanh(((-((np.where((-(((((-((data["medianbatch_slices2"])))) / 2.0)))) > -998, ((data["minbatch_slices2"]) / 2.0), (-((data["abs_maxbatch_slices2"]))) ))))))))))) +
                            0.100000*np.tanh((-(((((((3.37617230415344238)) + (((data["minbatch"]) * 2.0)))) * 2.0))))) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) - (((np.where(data["abs_maxbatch_slices2"] > -998, data["maxtominbatch"], ((data["abs_avgbatch_msignal"]) + (np.where(((data["rangebatch_msignal"]) / 2.0) > -998, ((data["maxtominbatch_msignal"]) / 2.0), data["abs_maxbatch"] ))) )) * 2.0)))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) * (((data["minbatch_msignal"]) + (np.where(((data["minbatch_msignal"]) + ((((7.0)) + ((7.0))))) > -998, (7.0), (7.0) )))))) +
                            0.100000*np.tanh(((data["maxbatch_slices2_msignal"]) + (data["maxtominbatch_slices2"]))) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(((data["signal_shift_-1_msignal"]) + (data["minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["maxbatch_msignal"]) +
                            0.100000*np.tanh(((data["abs_avgbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(((((np.where(data["meanbatch_slices2_msignal"] <= -998, data["abs_maxbatch_msignal"], (((np.where(data["meanbatch_msignal"] <= -998, data["abs_maxbatch_msignal"], data["abs_maxbatch_msignal"] )) + (((data["meanbatch_msignal"]) * 2.0)))/2.0) )) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(np.where(((np.where(data["rangebatch_slices2"] > -998, data["abs_avgbatch_msignal"], data["maxtominbatch"] )) + (data["meanbatch_slices2"])) > -998, ((data["maxtominbatch"]) - (data["stdbatch_slices2_msignal"])), data["maxtominbatch"] )) +
                            0.100000*np.tanh(np.where(((data["medianbatch_slices2"]) + (data["rangebatch_slices2_msignal"])) > -998, ((data["medianbatch_slices2"]) + (data["stdbatch_msignal"])), data["maxbatch_slices2"] )) +
                            0.100000*np.tanh(((((((data["signal_shift_-1_msignal"]) / 2.0)) + (data["signal_shift_-1_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(((np.where(data["mean_abs_chgbatch_msignal"] > -998, data["abs_minbatch_slices2_msignal"], ((data["mean_abs_chgbatch_msignal"]) * ((((2.51184296607971191)) - (data["mean_abs_chgbatch_msignal"])))) )) * ((((2.51184296607971191)) - (data["abs_maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(data["maxtominbatch_slices2"]))    
    
    def GP_class_9(self,data):
        return self.Output(-3.605458 +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2"] > -998, data["meanbatch_slices2"], np.where(((data["meanbatch_slices2"]) / 2.0) <= -998, (-((data["maxbatch_slices2"]))), ((((((data["rangebatch_msignal"]) / 2.0)) * 2.0)) - (data["medianbatch_msignal"])) ) )) +
                            0.100000*np.tanh((-((((np.where(data["abs_avgbatch_slices2_msignal"] > -998, data["medianbatch_msignal"], data["medianbatch_msignal"] )) * 2.0))))) +
                            0.100000*np.tanh(np.where((((data["minbatch_msignal"]) + (((data["signal_shift_-1"]) / 2.0)))/2.0) <= -998, np.where(data["maxbatch_slices2"] <= -998, data["signal_shift_-1"], data["meanbatch_slices2"] ), np.where(((data["mean_abs_chgbatch_slices2"]) * 2.0) <= -998, data["maxtominbatch_slices2_msignal"], data["signal_shift_-1"] ) )) +
                            0.100000*np.tanh((-((np.where(np.where(data["abs_maxbatch_slices2_msignal"] <= -998, (-((data["stdbatch_slices2_msignal"]))), data["abs_avgbatch_slices2_msignal"] ) <= -998, data["abs_avgbatch_slices2_msignal"], data["abs_avgbatch_slices2_msignal"] ))))) +
                            0.100000*np.tanh((((((-((np.tanh((np.tanh((data["rangebatch_slices2"])))))))) - (data["meanbatch_slices2_msignal"]))) - (np.tanh(((((1.20318198204040527)) - (data["meanbatch_slices2_msignal"]))))))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(((((np.where(((data["meanbatch_slices2"]) * 2.0) <= -998, data["minbatch_slices2_msignal"], ((data["signal"]) - (data["maxbatch_msignal"])) )) * 2.0)) / 2.0)) +
                            0.100000*np.tanh(np.tanh(((-((np.where(data["minbatch_slices2"] > -998, (-(((-((data["meanbatch_msignal"])))))), data["minbatch_slices2_msignal"] ))))))) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(data["stdbatch_slices2"]) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_msignal"]) / 2.0)) * (np.where(((data["abs_maxbatch_slices2"]) / 2.0) <= -998, ((data["abs_minbatch_slices2"]) / 2.0), (((-((data["abs_maxbatch_msignal"])))) * 2.0) )))) +
                            0.100000*np.tanh((-(((((data["stdbatch_msignal"]) + ((((data["maxtominbatch_slices2"]) + (np.where(np.where(data["mean_abs_chgbatch_slices2"] > -998, data["rangebatch_slices2"], data["maxbatch_slices2_msignal"] ) > -998, data["signal_shift_-1"], data["stdbatch_msignal"] )))/2.0)))/2.0))))) +
                            0.100000*np.tanh(((np.where(((np.where((1.29980242252349854) <= -998, data["maxtominbatch_slices2_msignal"], data["signal_shift_-1"] )) * (data["meanbatch_msignal"])) <= -998, data["mean_abs_chgbatch_slices2_msignal"], data["signal_shift_+1"] )) - (data["minbatch_slices2"]))) +
                            0.100000*np.tanh(((np.where(((data["maxbatch_slices2"]) * 2.0) > -998, data["minbatch_msignal"], data["minbatch_slices2"] )) * ((((data["abs_maxbatch_slices2_msignal"]) + ((((data["minbatch"]) + (data["stdbatch_msignal"]))/2.0)))/2.0)))) +
                            0.100000*np.tanh(((data["minbatch"]) - (((data["medianbatch_slices2_msignal"]) - (((((data["minbatch_slices2_msignal"]) * (np.where(data["medianbatch_slices2"] > -998, data["abs_avgbatch_slices2_msignal"], data["medianbatch_slices2_msignal"] )))) / 2.0)))))) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) * (np.where((9.0) <= -998, ((data["minbatch_slices2_msignal"]) - ((-((data["minbatch_slices2_msignal"]))))), data["minbatch_slices2_msignal"] )))) - (data["maxbatch_slices2"]))) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_slices2"] <= -998, ((data["minbatch"]) / 2.0), ((np.where((-((data["medianbatch_slices2"]))) <= -998, (-(((-(((-((data["abs_avgbatch_msignal"]))))))))), (-((data["abs_avgbatch_msignal"]))) )) * 2.0) )) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) - (data["abs_avgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["rangebatch_slices2"]) - ((9.58928871154785156)))) +
                            0.100000*np.tanh(((((-((((data["medianbatch_slices2_msignal"]) + (data["signal_shift_+1_msignal"])))))) + (((data["medianbatch_slices2_msignal"]) - (data["stdbatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh((-((((data["minbatch_msignal"]) + (np.where((-((data["mean_abs_chgbatch_slices2_msignal"]))) <= -998, ((data["mean_abs_chgbatch_msignal"]) * (np.where(data["abs_minbatch_slices2_msignal"] > -998, data["maxbatch_msignal"], data["mean_abs_chgbatch_slices2_msignal"] ))), (8.08646869659423828) ))))))) +
                            0.100000*np.tanh(((np.where(data["medianbatch_slices2"] > -998, ((((data["stdbatch_slices2_msignal"]) + ((-((data["abs_minbatch_slices2_msignal"])))))) / 2.0), ((data["stdbatch_slices2_msignal"]) - (np.tanh((data["medianbatch_slices2_msignal"])))) )) - (data["medianbatch_msignal"]))) +
                            0.100000*np.tanh(((np.tanh((data["signal_shift_-1"]))) * 2.0)) +
                            0.100000*np.tanh(np.tanh((data["abs_minbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(np.where(data["mean_abs_chgbatch_slices2"] <= -998, data["minbatch_slices2_msignal"], data["meanbatch_slices2"] )) +
                            0.100000*np.tanh((-((np.tanh(((-((((data["rangebatch_msignal"]) * ((((-((np.tanh((np.where(data["abs_minbatch_msignal"] > -998, (-((data["mean_abs_chgbatch_msignal"]))), np.tanh((data["abs_minbatch_msignal"])) ))))))) / 2.0)))))))))))) +
                            0.100000*np.tanh((-((np.where(data["mean_abs_chgbatch_msignal"] > -998, (-((data["medianbatch_msignal"]))), (-(((-(((-(((-(((-(((0.62542694807052612)))))))))))))))) ))))) +
                            0.100000*np.tanh(((np.where(np.where((9.0) > -998, data["rangebatch_slices2"], (10.0) ) > -998, data["rangebatch_slices2"], data["abs_minbatch_slices2"] )) - ((10.0)))) +
                            0.100000*np.tanh((-((np.where(data["minbatch_slices2"] <= -998, np.where(((data["maxtominbatch_msignal"]) + ((-((data["mean_abs_chgbatch_slices2"]))))) > -998, data["abs_minbatch_msignal"], ((data["abs_minbatch_msignal"]) * (data["meanbatch_slices2_msignal"])) ), data["meanbatch_slices2_msignal"] ))))) +
                            0.100000*np.tanh(np.where(data["minbatch_slices2_msignal"] > -998, ((data["abs_minbatch_msignal"]) + (((data["minbatch_slices2_msignal"]) + (((data["meanbatch_msignal"]) * (data["minbatch_slices2_msignal"])))))), data["abs_minbatch_msignal"] )) +
                            0.100000*np.tanh(np.tanh((data["minbatch_slices2"]))) +
                            0.100000*np.tanh((-((((data["signal"]) + (((data["medianbatch_slices2"]) * (np.where(data["abs_avgbatch_slices2"] > -998, data["medianbatch_slices2_msignal"], data["abs_avgbatch_msignal"] ))))))))) +
                            0.100000*np.tanh(np.where((((-((data["abs_maxbatch"])))) * 2.0) > -998, (((-((data["medianbatch_slices2"])))) + (data["signal"])), (-((data["minbatch_slices2_msignal"]))) )) +
                            0.100000*np.tanh(np.tanh((((np.tanh((((data["signal"]) / 2.0)))) * 2.0)))) +
                            0.100000*np.tanh(((np.where(((data["minbatch_msignal"]) + ((7.66306591033935547))) <= -998, ((data["abs_minbatch_slices2_msignal"]) + ((7.66306591033935547))), ((data["minbatch_msignal"]) + ((7.66306591033935547))) )) * (data["mean_abs_chgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((-((((((data["minbatch_msignal"]) + (np.where((((-((((data["abs_avgbatch_slices2"]) * (((data["minbatch_msignal"]) + ((8.0))))))))) * 2.0) <= -998, data["minbatch_slices2"], (8.0) )))) * 2.0))))) +
                            0.100000*np.tanh(((data["medianbatch_msignal"]) + (((((((np.tanh((data["abs_minbatch_slices2"]))) + (data["abs_minbatch_msignal"]))) + (((data["medianbatch_msignal"]) * (data["abs_minbatch_msignal"]))))) / 2.0)))) +
                            0.100000*np.tanh((((-((data["abs_maxbatch_slices2_msignal"])))) * (np.where(data["signal_shift_+1"] <= -998, data["meanbatch_slices2"], data["abs_avgbatch_msignal"] )))) +
                            0.100000*np.tanh((-(((((((-((data["minbatch_slices2_msignal"])))) + (((data["minbatch_slices2_msignal"]) * ((-((data["medianbatch_slices2_msignal"])))))))) + (((data["abs_avgbatch_msignal"]) * (data["abs_minbatch_slices2"])))))))) +
                            0.100000*np.tanh(((np.where(data["minbatch_slices2_msignal"] > -998, ((((9.0)) + (data["minbatch_msignal"]))/2.0), ((data["stdbatch_msignal"]) / 2.0) )) * (((data["mean_abs_chgbatch_slices2_msignal"]) * 2.0)))) +
                            0.100000*np.tanh(data["minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((((data["minbatch_slices2_msignal"]) - (((data["medianbatch_slices2_msignal"]) - (data["mean_abs_chgbatch_msignal"]))))) + (data["minbatch_slices2_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2"] <= -998, (((data["maxtominbatch_slices2"]) + (data["medianbatch_slices2_msignal"]))/2.0), (((-((data["signal_shift_+1"])))) - (((data["medianbatch_slices2_msignal"]) * (data["medianbatch_slices2"])))) )) +
                            0.100000*np.tanh(((((data["abs_minbatch_msignal"]) + ((-((data["abs_avgbatch_msignal"])))))) - ((((data["abs_minbatch_msignal"]) + (((data["signal_shift_+1_msignal"]) - (data["stdbatch_msignal"]))))/2.0)))) +
                            0.100000*np.tanh(np.where((((-((data["mean_abs_chgbatch_msignal"])))) * 2.0) > -998, data["signal_shift_+1"], data["stdbatch_slices2"] )) +
                            0.100000*np.tanh(((np.where(((((data["signal_shift_+1"]) * (data["abs_maxbatch_msignal"]))) * (data["abs_minbatch_msignal"])) <= -998, data["meanbatch_slices2"], data["mean_abs_chgbatch_slices2_msignal"] )) * ((((data["medianbatch_msignal"]) + (data["stdbatch_slices2"]))/2.0)))) +
                            0.100000*np.tanh(((((data["medianbatch_msignal"]) * (((np.tanh(((-((((data["minbatch_slices2_msignal"]) * 2.0))))))) - (data["maxbatch_msignal"]))))) - (((data["maxbatch_msignal"]) / 2.0)))) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2"] > -998, data["meanbatch_slices2"], ((((data["signal_shift_+1"]) * 2.0)) / 2.0) )) +
                            0.100000*np.tanh((0.42772302031517029)) +
                            0.100000*np.tanh((((data["minbatch_msignal"]) + (data["minbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(data["stdbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) * 2.0)) +
                            0.100000*np.tanh(((data["abs_maxbatch"]) - ((5.20704507827758789)))) +
                            0.100000*np.tanh((-((data["maxtominbatch_slices2_msignal"])))) +
                            0.100000*np.tanh(((((((data["stdbatch_slices2_msignal"]) + ((-(((-((data["minbatch_msignal"]))))))))) * ((4.0)))) * (((((data["meanbatch_msignal"]) * (data["maxbatch_slices2_msignal"]))) + ((4.0)))))) +
                            0.100000*np.tanh(((((data["maxtominbatch_slices2"]) - (data["minbatch_slices2_msignal"]))) + (data["abs_maxbatch_msignal"]))) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((data["maxtominbatch_msignal"]) * 2.0)) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(((data["maxtominbatch_slices2_msignal"]) * 2.0)) +
                            0.100000*np.tanh(((data["signal_shift_+1_msignal"]) * (((((data["rangebatch_msignal"]) * ((((-((data["signal_shift_-1"])))) - (((data["abs_avgbatch_slices2"]) * ((-((data["minbatch_slices2_msignal"])))))))))) * (data["abs_maxbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(data["maxtominbatch"]) +
                            0.100000*np.tanh(data["stdbatch_slices2"]) +
                            0.100000*np.tanh(np.tanh(((((((((((data["signal_shift_+1"]) / 2.0)) + (((data["abs_minbatch_msignal"]) + (data["abs_minbatch_slices2_msignal"]))))/2.0)) / 2.0)) / 2.0)))) +
                            0.100000*np.tanh(((np.tanh((data["medianbatch_msignal"]))) - ((((data["maxtominbatch"]) + (data["abs_avgbatch_msignal"]))/2.0)))) +
                            0.100000*np.tanh(data["abs_maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh(data["minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((np.tanh((((data["signal_shift_-1_msignal"]) * 2.0)))) * (((data["rangebatch_slices2"]) * ((-((data["maxtominbatch_slices2"])))))))) +
                            0.100000*np.tanh(np.tanh((((data["abs_maxbatch"]) / 2.0)))) +
                            0.100000*np.tanh(data["signal_shift_+1_msignal"]) +
                            0.100000*np.tanh(np.where(((data["maxbatch_slices2"]) + (((data["minbatch_msignal"]) - (((((data["meanbatch_slices2_msignal"]) * 2.0)) / 2.0))))) <= -998, data["abs_minbatch_slices2_msignal"], data["abs_minbatch_msignal"] )) +
                            0.100000*np.tanh(data["maxbatch_msignal"]) +
                            0.100000*np.tanh(data["minbatch_slices2"]) +
                            0.100000*np.tanh(data["minbatch_msignal"]) +
                            0.100000*np.tanh(data["meanbatch_slices2"]) +
                            0.100000*np.tanh(np.tanh((np.where(data["minbatch_msignal"] <= -998, data["mean_abs_chgbatch_msignal"], ((data["minbatch_msignal"]) - (data["maxbatch_slices2"])) )))) +
                            0.100000*np.tanh(np.tanh((data["minbatch_msignal"]))) +
                            0.100000*np.tanh(data["abs_maxbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((((data["stdbatch_msignal"]) - (data["maxbatch_slices2"]))) + ((-((((data["minbatch_slices2_msignal"]) - (data["signal_shift_+1"])))))))/2.0)) +
                            0.100000*np.tanh(data["minbatch"]) +
                            0.100000*np.tanh(np.tanh((((data["signal_shift_-1_msignal"]) / 2.0)))) +
                            0.100000*np.tanh(np.where(data["stdbatch_slices2"] <= -998, data["abs_maxbatch_slices2_msignal"], np.tanh((data["abs_maxbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(((data["rangebatch_msignal"]) * (((data["stdbatch_slices2_msignal"]) + (np.where(data["abs_maxbatch_msignal"] <= -998, ((((data["signal"]) - (np.tanh((data["rangebatch_msignal"]))))) / 2.0), ((data["mean_abs_chgbatch_msignal"]) * (data["medianbatch_slices2_msignal"])) )))))) +
                            0.100000*np.tanh(((((((2.0)) + (data["medianbatch_msignal"]))/2.0)) * (((((data["medianbatch_msignal"]) - (np.where(data["maxbatch_slices2_msignal"] <= -998, (8.0), ((data["rangebatch_slices2"]) - ((8.0))) )))) - (data["abs_maxbatch_slices2"]))))) +
                            0.100000*np.tanh(np.where(np.tanh((data["abs_minbatch_msignal"])) > -998, data["meanbatch_slices2_msignal"], (-((data["abs_minbatch_slices2"]))) )) +
                            0.100000*np.tanh(np.where(data["rangebatch_slices2_msignal"] <= -998, ((data["maxtominbatch_msignal"]) - (((np.where(data["abs_maxbatch_slices2_msignal"] <= -998, data["mean_abs_chgbatch_msignal"], data["abs_maxbatch_msignal"] )) - (data["maxbatch_slices2_msignal"])))), ((np.tanh((data["abs_minbatch_slices2_msignal"]))) + (data["maxbatch_slices2_msignal"])) )) +
                            0.100000*np.tanh(np.where((10.0) > -998, np.tanh((data["rangebatch_msignal"])), ((data["abs_minbatch_slices2"]) / 2.0) )) +
                            0.100000*np.tanh((((((data["signal_shift_+1"]) + (data["signal"]))/2.0)) + (data["signal_shift_+1"]))) +
                            0.100000*np.tanh((((((data["maxbatch_slices2"]) * ((-(((((data["maxbatch_msignal"]) + (np.where(data["mean_abs_chgbatch_slices2_msignal"] <= -998, data["stdbatch_msignal"], ((data["maxbatch_msignal"]) * (data["meanbatch_msignal"])) )))/2.0))))))) + (data["abs_minbatch_msignal"]))/2.0)) +
                            0.100000*np.tanh(np.where(data["meanbatch_slices2"] <= -998, ((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0), data["abs_minbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((((data["signal_shift_-1_msignal"]) + (data["signal_shift_-1_msignal"]))/2.0)) +
                            0.100000*np.tanh((-((data["maxbatch_slices2"])))) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2_msignal"]) + (np.where(data["maxbatch_msignal"] <= -998, ((data["maxbatch_msignal"]) * (data["maxbatch_msignal"])), ((data["maxbatch_msignal"]) * (data["maxbatch_msignal"])) )))) +
                            0.100000*np.tanh(np.tanh((((data["minbatch_msignal"]) * ((-((np.tanh((data["signal_shift_+1_msignal"])))))))))) +
                            0.100000*np.tanh(((np.tanh((((data["abs_minbatch_slices2_msignal"]) * (((data["minbatch_slices2"]) - (data["minbatch"]))))))) / 2.0)) +
                            0.100000*np.tanh((((np.where((((data["maxtominbatch"]) + (data["stdbatch_msignal"]))/2.0) <= -998, data["medianbatch_msignal"], ((data["medianbatch_msignal"]) * (((data["medianbatch_msignal"]) - (((data["medianbatch_msignal"]) * (data["medianbatch_msignal"])))))) )) + (data["abs_minbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh(((((data["abs_minbatch_slices2_msignal"]) + (data["maxtominbatch_slices2_msignal"]))) / 2.0)) +
                            0.100000*np.tanh(np.tanh((np.tanh((((data["signal_shift_+1_msignal"]) + (((data["signal_shift_-1_msignal"]) / 2.0)))))))) +
                            0.100000*np.tanh(np.where(((data["maxtominbatch"]) * 2.0) > -998, ((data["maxtominbatch"]) + (data["abs_maxbatch_slices2_msignal"])), ((((data["maxbatch_msignal"]) / 2.0)) + (data["maxtominbatch"])) )) +
                            0.100000*np.tanh(((data["rangebatch_msignal"]) + (data["maxtominbatch_slices2"]))))    
    
    def GP_class_10(self,data):
        return self.Output(-4.933813 +
                            0.100000*np.tanh((-(((7.0))))) +
                            0.100000*np.tanh(((data["signal_shift_-1"]) / 2.0)) +
                            0.100000*np.tanh(data["maxbatch_slices2"]) +
                            0.100000*np.tanh((((((data["rangebatch_slices2_msignal"]) * 2.0)) + (np.tanh((((data["abs_avgbatch_msignal"]) - (data["maxbatch_msignal"]))))))/2.0)) +
                            0.100000*np.tanh(((((((13.80353736877441406)) * (data["medianbatch_slices2_msignal"]))) + ((-((data["abs_minbatch_slices2_msignal"])))))/2.0)) +
                            0.100000*np.tanh(np.where(np.where(data["signal_shift_+1"] > -998, ((data["signal_shift_-1"]) + (data["abs_minbatch_slices2"])), data["stdbatch_slices2"] ) > -998, data["stdbatch_slices2"], data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh((-((np.where((-((data["maxbatch_slices2_msignal"]))) > -998, (6.0), data["medianbatch_slices2"] ))))) +
                            0.100000*np.tanh(data["mean_abs_chgbatch_slices2"]) +
                            0.100000*np.tanh(((data["mean_abs_chgbatch_slices2"]) * 2.0)) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2_msignal"]) / 2.0)) - (data["meanbatch_slices2"]))) +
                            0.100000*np.tanh((((8.89876651763916016)) + ((-((((((data["stdbatch_slices2"]) / 2.0)) + (data["minbatch_slices2"])))))))) +
                            0.100000*np.tanh((((((((((np.where(data["minbatch"] <= -998, data["abs_avgbatch_msignal"], ((data["meanbatch_slices2"]) - (((data["mean_abs_chgbatch_slices2"]) / 2.0))) )) + (data["medianbatch_msignal"]))/2.0)) + (data["mean_abs_chgbatch_slices2_msignal"]))) * 2.0)) / 2.0)) +
                            0.100000*np.tanh((((((data["rangebatch_slices2"]) / 2.0)) + (data["minbatch_slices2"]))/2.0)) +
                            0.100000*np.tanh((((data["medianbatch_msignal"]) + (data["stdbatch_slices2_msignal"]))/2.0)) +
                            0.100000*np.tanh((-(((-((np.tanh((data["signal_shift_+1"]))))))))) +
                            0.100000*np.tanh(data["signal_shift_-1"]) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) / 2.0)) +
                            0.100000*np.tanh((((-((data["meanbatch_msignal"])))) - (data["stdbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2"]) - (((data["signal_shift_-1"]) - (data["stdbatch_slices2"]))))) +
                            0.100000*np.tanh(((data["medianbatch_slices2_msignal"]) * (np.where(data["minbatch_msignal"] <= -998, data["abs_minbatch_slices2_msignal"], ((((data["abs_minbatch_slices2_msignal"]) * ((-((np.tanh(((-((data["abs_minbatch_slices2_msignal"]))))))))))) / 2.0) )))) +
                            0.100000*np.tanh((-((((data["signal_shift_+1"]) * ((((((-((((data["stdbatch_msignal"]) * 2.0))))) * 2.0)) * 2.0))))))) +
                            0.100000*np.tanh((-((data["meanbatch_slices2"])))) +
                            0.100000*np.tanh(((data["meanbatch_slices2_msignal"]) * (data["maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh((((((-((((np.tanh(((-(((-(((8.0)))))))))) * 2.0))))) + (data["medianbatch_slices2"]))) / 2.0)) +
                            0.100000*np.tanh(((data["abs_minbatch_slices2"]) + ((4.0)))) +
                            0.100000*np.tanh((((((data["maxtominbatch_slices2_msignal"]) * 2.0)) + (data["signal"]))/2.0)) +
                            0.100000*np.tanh((((data["signal"]) + (((np.where(((data["signal_shift_-1"]) * 2.0) <= -998, data["minbatch"], data["signal_shift_-1"] )) - (((data["maxtominbatch_msignal"]) * 2.0)))))/2.0)) +
                            0.100000*np.tanh(data["abs_maxbatch"]) +
                            0.100000*np.tanh(((((data["mean_abs_chgbatch_slices2"]) - (data["abs_avgbatch_slices2"]))) / 2.0)) +
                            0.100000*np.tanh(((data["signal"]) - (data["signal_shift_+1"]))) +
                            0.100000*np.tanh((((data["maxbatch_slices2_msignal"]) + (np.tanh((data["maxbatch_msignal"]))))/2.0)) +
                            0.100000*np.tanh((-((data["maxtominbatch"])))) +
                            0.100000*np.tanh(((((np.where((((((7.54857158660888672)) + (data["stdbatch_slices2_msignal"]))) * 2.0) > -998, ((data["maxbatch_slices2_msignal"]) * ((-((data["meanbatch_slices2_msignal"]))))), data["maxbatch_slices2_msignal"] )) * 2.0)) * 2.0)) +
                            0.100000*np.tanh(np.where(np.where((-((np.tanh((np.tanh((data["abs_minbatch_slices2_msignal"]))))))) > -998, (-((data["abs_avgbatch_msignal"]))), (-((data["abs_avgbatch_msignal"]))) ) > -998, (-((data["abs_avgbatch_msignal"]))), data["signal"] )) +
                            0.100000*np.tanh((-((((((((-((np.tanh((data["abs_maxbatch_slices2"])))))) + ((((-(((-((data["medianbatch_slices2_msignal"]))))))) - (data["signal_shift_+1_msignal"]))))/2.0)) * (data["signal_shift_-1_msignal"])))))) +
                            0.100000*np.tanh((-((((data["abs_maxbatch_msignal"]) - (((((((-((((data["stdbatch_msignal"]) * 2.0))))) + (np.tanh(((-((data["stdbatch_slices2"])))))))/2.0)) / 2.0))))))) +
                            0.100000*np.tanh(data["maxbatch_msignal"]) +
                            0.100000*np.tanh((-(((-((data["maxbatch_slices2"]))))))) +
                            0.100000*np.tanh(((np.tanh((np.tanh((np.tanh((data["meanbatch_msignal"]))))))) - (data["meanbatch_msignal"]))) +
                            0.100000*np.tanh((((-((np.where(data["abs_minbatch_slices2_msignal"] <= -998, (-((data["maxtominbatch"]))), data["rangebatch_msignal"] ))))) - ((((data["stdbatch_slices2"]) + (data["abs_maxbatch_slices2_msignal"]))/2.0)))) +
                            0.100000*np.tanh(((((((data["mean_abs_chgbatch_msignal"]) - (data["minbatch_slices2_msignal"]))) * (data["abs_avgbatch_msignal"]))) - (((((data["abs_maxbatch_slices2_msignal"]) * (((data["abs_avgbatch_slices2_msignal"]) - (data["maxbatch_slices2"]))))) * 2.0)))) +
                            0.100000*np.tanh(np.where((-((((data["minbatch_slices2"]) + (data["signal"]))))) > -998, ((data["signal_shift_-1"]) + (data["stdbatch_slices2_msignal"])), ((data["signal_shift_+1"]) - (data["minbatch_slices2"])) )) +
                            0.100000*np.tanh((-((((np.where((-((data["minbatch_msignal"]))) <= -998, ((data["minbatch_msignal"]) + ((9.0))), np.tanh(((-(((9.0)))))) )) + (data["minbatch_msignal"])))))) +
                            0.100000*np.tanh(np.where((-((((data["maxbatch_slices2_msignal"]) + (data["medianbatch_slices2_msignal"]))))) <= -998, ((data["medianbatch_msignal"]) + (data["abs_maxbatch_slices2_msignal"])), (-((((data["maxbatch_slices2_msignal"]) + (data["medianbatch_msignal"]))))) )) +
                            0.100000*np.tanh((((((data["signal"]) * ((-((data["stdbatch_slices2"])))))) + ((-((data["medianbatch_slices2"])))))/2.0)) +
                            0.100000*np.tanh((-((data["medianbatch_slices2_msignal"])))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2"]) +
                            0.100000*np.tanh((-((data["meanbatch_msignal"])))) +
                            0.100000*np.tanh((-(((-((np.tanh(((-(((((data["mean_abs_chgbatch_msignal"]) + (((data["minbatch_slices2"]) / 2.0)))/2.0))))))))))))) +
                            0.100000*np.tanh((((-((np.where(data["maxbatch_slices2_msignal"] <= -998, (((((data["abs_minbatch_slices2"]) * 2.0)) + (((data["minbatch_msignal"]) + (data["signal_shift_-1"]))))/2.0), data["medianbatch_slices2"] ))))) - (data["medianbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(((np.where(data["signal"] <= -998, data["abs_avgbatch_slices2_msignal"], (-((data["mean_abs_chgbatch_msignal"]))) )) / 2.0)) +
                            0.100000*np.tanh((((-((np.where(data["medianbatch_slices2_msignal"] <= -998, np.where((-(((2.0)))) <= -998, ((data["mean_abs_chgbatch_slices2"]) / 2.0), (2.0) ), data["medianbatch_slices2_msignal"] ))))) - ((2.0)))) +
                            0.100000*np.tanh((((-((data["maxtominbatch_slices2_msignal"])))) + ((-((data["stdbatch_slices2"])))))) +
                            0.100000*np.tanh((-((((data["medianbatch_msignal"]) + (data["maxbatch_msignal"])))))) +
                            0.100000*np.tanh((-((((np.where(data["medianbatch_msignal"] <= -998, np.tanh((((data["maxbatch_slices2"]) * 2.0))), ((np.tanh((data["meanbatch_slices2"]))) + (((data["meanbatch_msignal"]) + (np.tanh((data["meanbatch_slices2"])))))) )) * 2.0))))) +
                            0.100000*np.tanh(((((np.tanh((data["maxbatch_slices2_msignal"]))) - (data["maxbatch_slices2_msignal"]))) - (data["medianbatch_slices2_msignal"]))) +
                            0.100000*np.tanh((-(((-((data["stdbatch_slices2"]))))))) +
                            0.100000*np.tanh(data["maxbatch_msignal"]) +
                            0.100000*np.tanh((((-(((13.33689022064208984))))) / 2.0)) +
                            0.100000*np.tanh(((((data["abs_avgbatch_slices2_msignal"]) * (np.where(data["mean_abs_chgbatch_slices2"] <= -998, np.where(data["abs_avgbatch_slices2_msignal"] <= -998, data["meanbatch_slices2_msignal"], data["abs_avgbatch_slices2_msignal"] ), data["stdbatch_msignal"] )))) - (data["abs_maxbatch"]))) +
                            0.100000*np.tanh(np.tanh((((((data["minbatch_msignal"]) - (((data["abs_avgbatch_msignal"]) * 2.0)))) - (data["medianbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh((-((np.where((-((((data["medianbatch_msignal"]) + (data["maxbatch_slices2_msignal"]))))) > -998, ((data["meanbatch_slices2_msignal"]) + (data["maxbatch_slices2_msignal"])), ((((data["meanbatch_slices2_msignal"]) + (data["maxbatch_slices2_msignal"]))) * 2.0) ))))) +
                            0.100000*np.tanh(np.where(data["medianbatch_slices2"] <= -998, data["rangebatch_slices2_msignal"], data["medianbatch_slices2"] )) +
                            0.100000*np.tanh((((((data["abs_avgbatch_slices2_msignal"]) + ((((data["stdbatch_msignal"]) + ((((data["medianbatch_slices2_msignal"]) + (np.where(data["signal_shift_+1"] <= -998, (-((data["minbatch_slices2"]))), (-((data["stdbatch_msignal"]))) )))/2.0)))/2.0)))/2.0)) * (data["medianbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["signal_shift_+1"]) +
                            0.100000*np.tanh((-((np.where(data["meanbatch_msignal"] > -998, (((data["maxbatch_slices2_msignal"]) + (((((((data["meanbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_slices2_msignal"]))/2.0)) + (data["meanbatch_msignal"]))/2.0)))/2.0), (-(((-((((data["abs_maxbatch_msignal"]) / 2.0))))))) ))))) +
                            0.100000*np.tanh((-((((data["abs_avgbatch_slices2_msignal"]) + (np.where((-((data["medianbatch_msignal"]))) <= -998, data["stdbatch_slices2"], data["maxbatch_msignal"] ))))))) +
                            0.100000*np.tanh(((((((data["maxbatch_slices2"]) * (((data["maxtominbatch"]) - (data["stdbatch_msignal"]))))) - (data["abs_maxbatch"]))) - (((data["signal"]) / 2.0)))) +
                            0.100000*np.tanh(((data["minbatch_msignal"]) + (np.where(data["medianbatch_slices2_msignal"] > -998, ((data["minbatch_msignal"]) * (((data["medianbatch_slices2_msignal"]) / 2.0))), data["medianbatch_slices2_msignal"] )))) +
                            0.100000*np.tanh((((((data["minbatch_msignal"]) + ((((5.0)) * 2.0)))/2.0)) * (((np.where((-((data["minbatch_msignal"]))) > -998, data["abs_minbatch_msignal"], (5.0) )) / 2.0)))) +
                            0.100000*np.tanh((-((((np.where(data["mean_abs_chgbatch_msignal"] > -998, data["abs_maxbatch_slices2_msignal"], (((-((data["rangebatch_slices2_msignal"])))) * (data["meanbatch_slices2_msignal"])) )) + (data["abs_avgbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh(((((-((data["abs_avgbatch_slices2"])))) + (((((data["medianbatch_msignal"]) * 2.0)) - ((((((-((((data["stdbatch_slices2_msignal"]) / 2.0))))) + (data["minbatch_slices2_msignal"]))) * 2.0)))))/2.0)) +
                            0.100000*np.tanh(((((((((((-((data["abs_maxbatch_msignal"])))) + (data["maxbatch_slices2"]))) - (data["abs_maxbatch_slices2_msignal"]))) + (data["abs_minbatch_slices2"]))/2.0)) - (data["abs_maxbatch_slices2_msignal"]))) +
                            0.100000*np.tanh(data["meanbatch_slices2_msignal"]) +
                            0.100000*np.tanh((((-((((data["medianbatch_slices2"]) / 2.0))))) + ((-((data["abs_avgbatch_slices2_msignal"])))))) +
                            0.100000*np.tanh((-((((np.where(np.tanh((data["maxbatch_msignal"])) <= -998, ((((data["abs_minbatch_slices2"]) * 2.0)) * 2.0), data["abs_avgbatch_slices2"] )) + (((data["abs_avgbatch_msignal"]) * 2.0))))))) +
                            0.100000*np.tanh((((((-((data["abs_avgbatch_msignal"])))) * (data["stdbatch_slices2"]))) + ((((((((data["meanbatch_slices2_msignal"]) / 2.0)) + ((-((data["stdbatch_slices2"])))))/2.0)) / 2.0)))) +
                            0.100000*np.tanh((-((np.where(data["maxtominbatch"] > -998, (((data["medianbatch_slices2_msignal"]) + ((-((data["maxbatch_msignal"])))))/2.0), data["maxbatch_msignal"] ))))) +
                            0.100000*np.tanh(((((((data["abs_maxbatch_msignal"]) / 2.0)) - (data["mean_abs_chgbatch_slices2"]))) * (data["minbatch_msignal"]))) +
                            0.100000*np.tanh(((data["stdbatch_slices2_msignal"]) - (((np.where(((((data["maxtominbatch"]) / 2.0)) - (data["maxtominbatch_slices2"])) <= -998, data["maxbatch_slices2"], ((data["meanbatch_slices2_msignal"]) * (data["abs_avgbatch_slices2"])) )) / 2.0)))) +
                            0.100000*np.tanh(np.where(data["maxtominbatch_slices2_msignal"] <= -998, data["meanbatch_slices2_msignal"], data["meanbatch_slices2_msignal"] )) +
                            0.100000*np.tanh(((np.tanh((data["medianbatch_slices2_msignal"]))) + (((data["maxtominbatch_slices2_msignal"]) + (np.where(data["abs_avgbatch_slices2_msignal"] <= -998, data["mean_abs_chgbatch_slices2"], ((data["medianbatch_slices2_msignal"]) * (((data["abs_avgbatch_slices2_msignal"]) * 2.0))) )))))) +
                            0.100000*np.tanh(((((data["meanbatch_msignal"]) + ((-((data["medianbatch_slices2"])))))) * 2.0)) +
                            0.100000*np.tanh(((data["signal_shift_+1"]) * (data["signal"]))) +
                            0.100000*np.tanh(np.where((-((np.tanh((((data["abs_maxbatch_msignal"]) * 2.0)))))) > -998, np.where(data["abs_maxbatch"] > -998, np.tanh((((np.tanh((data["mean_abs_chgbatch_msignal"]))) / 2.0))), data["meanbatch_slices2"] ), data["meanbatch_slices2"] )) +
                            0.100000*np.tanh(((data["abs_avgbatch_slices2"]) / 2.0)) +
                            0.100000*np.tanh((((data["signal_shift_+1"]) + (np.where((((data["meanbatch_msignal"]) + (((data["abs_maxbatch"]) / 2.0)))/2.0) > -998, (-((data["signal"]))), (-((data["abs_maxbatch_msignal"]))) )))/2.0)) +
                            0.100000*np.tanh(np.where((-((data["mean_abs_chgbatch_slices2"]))) <= -998, data["mean_abs_chgbatch_slices2"], data["signal"] )) +
                            0.100000*np.tanh(((((data["signal_shift_-1"]) - (np.where((-((data["medianbatch_slices2"]))) <= -998, data["abs_minbatch_msignal"], data["abs_avgbatch_slices2_msignal"] )))) - ((((9.0)) + ((((data["meanbatch_msignal"]) + (data["signal_shift_-1_msignal"]))/2.0)))))) +
                            0.100000*np.tanh((((-(((-(((-(((((data["meanbatch_slices2_msignal"]) + (data["maxbatch_slices2_msignal"]))/2.0))))))))))) / 2.0)) +
                            0.100000*np.tanh((-((((np.where(data["medianbatch_msignal"] <= -998, np.tanh(((-((data["meanbatch_msignal"]))))), ((np.where(data["medianbatch_msignal"] > -998, (((3.0)) + (data["medianbatch_msignal"])), data["maxbatch_msignal"] )) * 2.0) )) * 2.0))))) +
                            0.100000*np.tanh(data["signal_shift_-1_msignal"]) +
                            0.100000*np.tanh((-((data["signal_shift_-1"])))) +
                            0.100000*np.tanh((-((data["medianbatch_msignal"])))) +
                            0.100000*np.tanh(data["abs_minbatch_slices2_msignal"]) +
                            0.100000*np.tanh(((((data["abs_maxbatch_slices2"]) + (data["abs_minbatch_slices2"]))) - (data["mean_abs_chgbatch_msignal"]))) +
                            0.100000*np.tanh(((np.where(((data["stdbatch_slices2_msignal"]) + (data["abs_maxbatch_slices2_msignal"])) > -998, ((data["mean_abs_chgbatch_slices2_msignal"]) * 2.0), ((data["meanbatch_slices2_msignal"]) + (data["mean_abs_chgbatch_msignal"])) )) + (((data["meanbatch_slices2_msignal"]) * (data["stdbatch_slices2_msignal"]))))) +
                            0.100000*np.tanh(np.where(data["abs_minbatch_msignal"] <= -998, (-((data["rangebatch_slices2_msignal"]))), np.tanh((data["stdbatch_slices2"])) ))    )    


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

