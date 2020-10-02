#!/usr/bin/env python
# coding: utf-8

# Trying to find the minimum raw features to get a decent score.  I couldn't be bothered using Time Stuff which definitely improve things ;)

# In[ ]:


import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.metrics import roc_auc_score


# In[ ]:


def add_noise(series, noise_level):
    return series * (1 + noise_level * np.random.randn(len(series)))

def target_encode(trn_series=None, 
                  tst_series=None, 
                  target=None, 
                  min_samples_leaf=100, 
                  smoothing=10,
                  noise_level=0):
    """
    Smoothing is computed like in the following paper by Daniele Micci-Barreca
    https://kaggle2.blob.core.windows.net/forum-message-attachments/225952/7441/high%20cardinality%20categoricals.pdf
    trn_series : training categorical feature as a pd.Series
    tst_series : test categorical feature as a pd.Series
    target : target data as a pd.Series
    min_samples_leaf (int) : minimum samples to take category average into account
    smoothing (int) : smoothing effect to balance categorical average vs prior  
    """ 
    assert len(trn_series) == len(target)
    assert trn_series.name == tst_series.name
    temp = pd.concat([trn_series, target], axis=1)
    # Compute target mean 
    averages = temp.groupby(by=trn_series.name)[target.name].agg(["mean", "count"])
    # Compute smoothing
    smoothing = 1 / (1 + np.exp(-(averages["count"] - min_samples_leaf) / smoothing))
    # Apply average function to all target data
    prior = target.mean()
    # The bigger the count the less full_avg is taken into account
    averages[target.name] = prior * (1 - smoothing) + averages["mean"] * smoothing
    averages.drop(["mean", "count"], axis=1, inplace=True)
    # Apply averages to trn and tst series
    ft_trn_series = pd.merge(
        trn_series.to_frame(trn_series.name),
        averages.reset_index().rename(columns={'index': target.name, target.name: 'average'}),
        on=trn_series.name,
        how='left')['average'].rename(trn_series.name + '_mean').fillna(prior)
    # pd.merge does not keep the index so restore it
    ft_trn_series.index = trn_series.index 
    ft_tst_series = pd.merge(
        tst_series.to_frame(tst_series.name),
        averages.reset_index().rename(columns={'index': target.name, target.name: 'average'}),
        on=tst_series.name,
        how='left')['average'].rename(trn_series.name + '_mean').fillna(prior)
    # pd.merge does not keep the index so restore it
    ft_tst_series.index = tst_series.index
    return add_noise(ft_trn_series, noise_level), add_noise(ft_tst_series, noise_level)


# In[ ]:


features = ['card1', 'C1', 'card4', 'C6', 'C14', 'V45', 'M6', 'M5', 'card2',
           'C5', 'V283', 'V294', 'TransactionAmt', 'D8', 'M4', 'C2', 'D14',
           'dist2', 'C10', 'D2', 'R_emaildomain', 'D10', 'V315', 'D1',
           'dist1', 'D11', 'C12', 'P_emaildomain', 'D15', 'C11', 'D4', 'V313',
           'C8', 'D9', 'V312', 'C13', 'D3', 'C9', 'V310', 'V133', 'V314',
           'V130', 'V317', 'V83', 'card5', 'V308', 'addr1', 'V127', 'V307',
           'D5']
len(features)


# In[ ]:


def Output(p):
    return 1./(1.+np.exp(-p))

def GP(data):
    return Output(-3.317076 +
                    0.094000*np.tanh(((((((((((((((((data["card1"]) * ((6.0)))) - ((((((data["dist2"]) > (np.where((3.0) < -9998, data["V294"], (((((((((data["card4"]) <= (((data["R_emaildomain"]) / 2.0)))*1.)) + (data["V294"]))/2.0)) + (data["card1"]))/2.0) )))*1.)) / 2.0)))) * 2.0)) * 2.0)) * 2.0)) * 2.0)) * 2.0)) * 2.0)) +
                    0.097000*np.tanh((((11.96328830718994141)) * ((((11.96328830718994141)) * (np.where((((data["card4"]) <= (data["V317"]))*1.)>0, data["card1"], (((((((11.96328830718994141)) * (data["card1"]))) - ((((data["C6"]) <= (data["M5"]))*1.)))) - ((((data["C8"]) <= (data["M5"]))*1.))) )))))) +
                    0.099970*np.tanh(((np.where((((((data["card4"]) > ((((((((((data["C2"]) + (data["D2"]))/2.0)) + (data["C14"]))/2.0)) + ((((((((((data["V294"]) + (data["C14"]))/2.0)) + (data["V312"]))/2.0)) + (data["card1"]))/2.0)))/2.0)))*1.)) - (data["card1"]))<0, (2.26337718963623047), -2.0 )) * 2.0)) +
                    0.094768*np.tanh(((((6.0)) + (((data["V313"]) - (np.where(data["M5"]<0, data["M5"], np.where(((data["M5"]) - (np.where(((data["C5"]) - ((((data["C5"]) > ((((data["C13"]) + (data["D1"]))/2.0)))*1.)))<0, data["card1"], data["C5"] )))>0, (((12.88493824005126953)) - (data["M5"])), data["M5"] ) )))))/2.0)) +
                    0.098048*np.tanh(np.where(np.where(data["C2"]<0, (((data["card4"]) + ((11.99994850158691406)))/2.0), ((data["card4"]) - (((((((data["C11"]) + (data["D2"]))/2.0)) + (((((((data["C14"]) + (data["card1"]))/2.0)) + (data["D3"]))/2.0)))/2.0))) )<0, (8.54772281646728516), (-1.0*(((5.81678628921508789)))) )) +
                    0.003360*np.tanh(((np.where((((((np.where(data["V133"]>0, data["card4"], data["card4"] )) <= ((((((((((data["card2"]) + (data["V294"]))/2.0)) + (data["V133"]))/2.0)) + (((((((data["C13"]) + (data["V294"]))/2.0)) + (data["C1"]))/2.0)))/2.0)))*1.)) - ((((data["C12"]) + (data["V133"]))/2.0)))<0, -3.0, 3.0 )) * 2.0)) +
                    0.0*np.tanh((((((((data["C10"]) > (data["V294"]))*1.)) * ((14.70462417602539062)))) + (np.where((((data["V294"]) > (data["card4"]))*1.)>0, (8.0), np.where((((data["C8"]) > (np.where(0.0<0, data["D2"], data["V294"] )))*1.)>0, (8.0), ((-2.0) + (((-2.0) + (-2.0)))) ) )))) +
                    0.097536*np.tanh(np.where((((data["M5"]) <= (np.tanh(((((np.tanh(((((((data["card1"]) * 2.0)) + ((((data["C14"]) + (data["V294"]))/2.0)))/2.0)))) + ((((((data["C1"]) > (data["card4"]))*1.)) * (data["C5"]))))/2.0)))))*1.)>0, 3.0, ((data["M5"]) - (3.0)) )) +
                    0.099993*np.tanh(np.where((((data["card4"]) <= ((((((((((data["V294"]) + ((((data["C14"]) + ((((data["C8"]) + ((((data["card1"]) + (data["V307"]))/2.0)))/2.0)))/2.0)))/2.0)) + ((((((data["C2"]) / 2.0)) + (data["V283"]))/2.0)))/2.0)) + ((((data["V315"]) + (data["V130"]))/2.0)))/2.0)))*1.)>0, (3.0), (-1.0*((3.0))) )) +
                    0.097088*np.tanh(np.where((((data["M5"]) <= (((data["C9"]) + ((((((data["dist2"]) <= (data["card1"]))*1.)) * 2.0)))))*1.)>0, np.where(((((((((data["card1"]) > (data["M5"]))*1.)) + ((((data["dist2"]) <= (data["C14"]))*1.)))/2.0)) * 2.0)>0, (11.30409431457519531), -1.0 ), (-1.0*(((((7.98520994186401367)) - (data["dist2"]))))) )) +
                    0.099192*np.tanh(((np.where(((np.where(((data["card4"]) - (data["card2"]))<0, data["D1"], (((((((data["D15"]) / 2.0)) > (((data["card4"]) - (data["card2"]))))*1.)) * 2.0) )) * (np.where(data["C5"]<0, data["V317"], (((data["M5"]) <= (data["C5"]))*1.) )))>0, 2.0, -1.0 )) * ((4.0)))) +
                    0.099584*np.tanh((((np.where(data["D2"]>0, (6.0), (-1.0*((data["TransactionAmt"]))) )) + (((data["TransactionAmt"]) * (((data["V45"]) + ((((-2.0) + (((data["TransactionAmt"]) * (((np.where((((data["C5"]) + (data["V312"]))/2.0) < -9998, -2.0, data["card1"] )) * ((((data["C5"]) > (data["M5"]))*1.)))))))/2.0)))))))/2.0)) +
                    0.099500*np.tanh(np.where((((((data["C5"]) > (data["M5"]))*1.)) * (((data["V130"]) * ((((data["C11"]) > (((data["C5"]) - (((((data["D15"]) / 2.0)) + (((data["C13"]) * (data["C13"]))))))))*1.)))))>0, data["TransactionAmt"], (-1.0*(((14.01870536804199219)))) )) +
                    0.099545*np.tanh(np.where((((((((data["card1"]) * (((np.where(data["V314"]>0, np.where(data["D15"]>0, (((((data["M5"]) + ((-1.0*((data["D2"])))))) <= (((data["D4"]) / 2.0)))*1.), ((-1.0) * 2.0) ), data["V314"] )) * 2.0)))) > (data["M5"]))*1.)) * 2.0)>0, (9.0), ((-2.0) * 2.0) )) +
                    0.099506*np.tanh(np.where(((data["V130"]) + (((np.where((((data["C1"]) > (data["V315"]))*1.)>0, (((data["C9"]) > (data["card4"]))*1.), data["M4"] )) - ((((data["V315"]) <= (data["D9"]))*1.)))))>0, (10.56288909912109375), (-1.0*(((9.0)))) )) +
                    0.099398*np.tanh((((14.00820541381835938)) * (((((((np.where((((((data["V314"]) - ((((data["V314"]) > (data["D14"]))*1.)))) <= (((data["C1"]) - (((data["card1"]) * ((-1.0*((data["C13"])))))))))*1.)>0, data["card1"], (-1.0*(((7.97236728668212891)))) )) * 2.0)) * 2.0)) + (data["C1"]))))) +
                    0.099480*np.tanh((((((((10.23559093475341797)) * 2.0)) * ((((((((7.60636425018310547)) * 2.0)) * (((((data["TransactionAmt"]) * (((((data["TransactionAmt"]) * (((data["card1"]) + (data["C10"]))))) * (data["card2"]))))) * (data["card1"]))))) * (((data["D15"]) * 2.0)))))) * (data["D5"]))) +
                    0.099208*np.tanh((((-1.0*((np.where(data["D2"]>0, 3.0, ((data["TransactionAmt"]) * 2.0) ))))) + ((((((((-1.0*(((((((data["V317"]) * 2.0)) > (data["R_emaildomain"]))*1.))))) + (((data["V294"]) * ((((9.0)) * 2.0)))))) * ((11.38016891479492188)))) + (((data["D2"]) * (data["TransactionAmt"]))))))) +
                    0.099960*np.tanh((((10.40301132202148438)) * ((((((data["C5"]) > (data["M6"]))*1.)) - (((np.where((((((((data["C14"]) > (((data["C9"]) - (np.where((((data["M6"]) > (((data["M5"]) - (data["card1"]))))*1.)>0, data["C1"], -3.0 )))))*1.)) * 2.0)) * 2.0)>0, 1.0, (10.40300750732421875) )) / 2.0)))))) +
                    0.099982*np.tanh(((-3.0) - (((data["TransactionAmt"]) * ((-1.0*((np.where(data["M6"]<0, data["M6"], ((((data["card2"]) * ((((((((data["M6"]) <= (((data["C14"]) + ((((data["M6"]) <= (data["C1"]))*1.)))))*1.)) * 2.0)) * 2.0)))) * ((((data["M6"]) <= (((data["D2"]) * 2.0)))*1.))) ))))))))) +
                    0.000604*np.tanh((((((data["C1"]) > (data["card4"]))*1.)) + ((((((data["C1"]) > (data["card4"]))*1.)) + (np.where((((data["card1"]) > (data["dist2"]))*1.)>0, (3.21562957763671875), ((((-2.0) + ((((((((data["C10"]) > (data["V294"]))*1.)) * 2.0)) * 2.0)))) + (-2.0)) )))))) +
                    0.098730*np.tanh(((data["TransactionAmt"]) * (((((-1.0) + (((((np.where((((data["card4"]) <= (((((((data["R_emaildomain"]) + (data["card1"]))/2.0)) + (data["V308"]))/2.0)))*1.)>0, (((data["C1"]) > (data["M6"]))*1.), np.where(data["V308"] < -9998, data["TransactionAmt"], data["card4"] ) )) * ((8.58146858215332031)))) * 2.0)))) * 2.0)))) +
                    0.093773*np.tanh((-1.0*((((((((data["TransactionAmt"]) + (data["TransactionAmt"]))/2.0)) + (((((data["TransactionAmt"]) * ((((((8.0)) * ((-1.0*(((((data["card4"]) <= (((((((data["C11"]) + ((((data["C13"]) + (data["C14"]))/2.0)))/2.0)) + ((((data["D4"]) + (data["V310"]))/2.0)))/2.0)))*1.))))))) * 2.0)))) * 2.0)))/2.0))))) +
                    0.013568*np.tanh(((data["TransactionAmt"]) * (((np.where(((data["D2"]) * ((((data["card4"]) <= (((data["C2"]) + ((((data["D9"]) <= (((data["V312"]) + ((((((data["V312"]) * 2.0)) <= (np.where(data["addr1"]<0, ((data["card4"]) * 2.0), data["card2"] )))*1.)))))*1.)))))*1.)))>0, data["card2"], -1.0 )) * 2.0)))) +
                    0.086432*np.tanh((((((((data["card2"]) * (data["TransactionAmt"]))) + ((-1.0*((np.where(((((((data["D4"]) > ((((data["card4"]) + ((((data["M5"]) > (data["C11"]))*1.)))/2.0)))*1.)) > ((((data["M5"]) > (data["C5"]))*1.)))*1.)>0, (((data["M5"]) > (data["C5"]))*1.), (4.0) ))))))/2.0)) * 2.0)) +
                    0.000652*np.tanh((((10.0)) * ((((10.0)) * (((data["C10"]) + ((((-1.0*((data["card4"])))) + (np.where(((((data["card4"]) - (data["D15"]))) - (data["D15"]))<0, (((((data["card1"]) > (data["dist2"]))*1.)) * 2.0), (-1.0*(((((3.0) + (data["dist2"]))/2.0)))) )))))))))) +
                    0.097494*np.tanh(np.where((((data["D11"]) > ((((data["card4"]) > (((((data["C5"]) / 2.0)) + ((((data["D15"]) + ((((((((((data["card4"]) + ((((((data["D11"]) / 2.0)) > (data["M4"]))*1.)))/2.0)) > (data["M4"]))*1.)) > (data["card4"]))*1.)))/2.0)))))*1.)))*1.)>0, (12.99686813354492188), ((((-2.0) * 2.0)) * 2.0) )) +
                    0.099993*np.tanh((((((((((((((((((data["D15"]) * 2.0)) > (data["card4"]))*1.)) - (((((((((data["C1"]) > (data["card4"]))*1.)) <= (data["C1"]))*1.)) * ((((((((data["card1"]) <= (data["C9"]))*1.)) * 2.0)) * 2.0)))))) * 2.0)) * 2.0)) - ((((data["D15"]) <= (data["M4"]))*1.)))) * 2.0)) * 2.0)) +
                    0.100000*np.tanh((((((((data["D14"]) <= (((data["V312"]) + ((((data["card4"]) <= (np.where((((data["D11"]) > (data["C14"]))*1.)>0, np.where((((data["D11"]) > (data["C6"]))*1.)>0, data["C6"], ((data["D10"]) * 2.0) ), data["C8"] )))*1.)))))*1.)) * 2.0)) * 2.0)) +
                    0.093200*np.tanh(((np.where((((data["V317"]) > (data["V45"]))*1.)>0, (-1.0*(((((((data["R_emaildomain"]) > (data["card1"]))*1.)) * 2.0)))), ((np.where((((data["V317"]) > (data["C1"]))*1.)>0, (-1.0*((3.0))), (((((data["C1"]) > (data["V317"]))*1.)) * 2.0) )) * 2.0) )) * 2.0)) +
                    0.053610*np.tanh(((np.where(((((((data["C10"]) > (data["M5"]))*1.)) > ((((data["C1"]) <= (data["V308"]))*1.)))*1.)>0, (5.0), -3.0 )) * (np.where((5.0) < -9998, data["V308"], ((((data["M5"]) * (-3.0))) + ((((data["D8"]) > (data["V313"]))*1.))) )))) +
                    0.082688*np.tanh(((((data["TransactionAmt"]) * (np.tanh((np.where(((data["D8"]) - (((data["V294"]) + ((((data["V45"]) > (data["V317"]))*1.)))))<0, data["card2"], ((((data["V45"]) - (((((np.tanh(((7.0)))) - (data["TransactionAmt"]))) * (data["V317"]))))) - ((11.21205139160156250))) )))))) * 2.0)) +
                    0.079200*np.tanh(((((data["V45"]) - (-2.0))) - (np.where((((((data["V45"]) + (data["C6"]))/2.0)) - (data["V130"]))>0, -2.0, np.where((((((data["C1"]) + (data["C14"]))/2.0)) - (data["V130"]))>0, data["C6"], np.where(((data["D9"]) - (data["V127"]))<0, -2.0, (10.24477863311767578) ) ) )))) +
                    0.092394*np.tanh(((((((-1.0) + (((((((((((9.37636756896972656)) * (((data["R_emaildomain"]) + ((((((data["R_emaildomain"]) + (data["M5"]))/2.0)) * 2.0)))))) > (np.where((((data["V283"]) > (-1.0))*1.) < -9998, data["V283"], (((data["V283"]) > (-1.0))*1.) )))*1.)) * 2.0)) * 2.0)))) * 2.0)) * 2.0)) +
                    0.095672*np.tanh(np.where((((((data["C1"]) <= (((((((data["M6"]) <= (((((((((((((data["C1"]) + (data["V45"]))/2.0)) + (data["D11"]))/2.0)) + (data["dist1"]))/2.0)) + (data["dist1"]))/2.0)))*1.)) + (data["C6"]))/2.0)))*1.)) - (data["D2"]))>0, (6.88358688354492188), ((((-1.0) * ((6.88358688354492188)))) / 2.0) )) +
                    0.065920*np.tanh(np.where((((data["M5"]) <= (((((((data["R_emaildomain"]) + (((((((data["card1"]) > (data["M4"]))*1.)) > ((((data["D14"]) > (data["V312"]))*1.)))*1.)))/2.0)) + (np.where(data["TransactionAmt"]>0, ((data["D9"]) / 2.0), (((data["M5"]) <= (data["C6"]))*1.) )))/2.0)))*1.)>0, data["TransactionAmt"], -3.0 )) +
                    0.039840*np.tanh((((((((((((((data["C5"]) <= (((data["D2"]) + (((data["D1"]) - ((((data["C2"]) <= (((data["M4"]) - ((((data["V314"]) <= (data["addr1"]))*1.)))))*1.)))))))*1.)) * 2.0)) * 2.0)) - ((((data["D2"]) <= (data["C5"]))*1.)))) * 2.0)) * 2.0)) +
                    0.043952*np.tanh(((((np.where((((data["V283"]) <= (np.where((((data["M4"]) <= (data["D1"]))*1.)>0, data["R_emaildomain"], data["D1"] )))*1.)>0, 3.0, (((((-1.0*(((((((data["M4"]) > (data["card1"]))*1.)) + ((-1.0*((data["V283"]))))))))) * 2.0)) * 2.0) )) * 2.0)) * 2.0)) +
                    0.099726*np.tanh(((((data["card1"]) * (np.where(data["D11"]>0, ((data["TransactionAmt"]) * ((((((data["C5"]) <= (((np.where((((data["C5"]) <= (((data["addr1"]) + (data["P_emaildomain"]))))*1.)>0, data["D4"], -2.0 )) + (data["D11"]))))*1.)) * 2.0))), data["D4"] )))) + (-2.0))) +
                    0.027152*np.tanh((((((((((((((data["V45"]) + ((((data["card4"]) <= (((((((data["card4"]) <= ((((data["C14"]) + (data["C6"]))/2.0)))*1.)) + (data["V310"]))/2.0)))*1.)))/2.0)) * 2.0)) * 2.0)) - (((((((((data["D8"]) <= (data["V315"]))*1.)) <= (data["card4"]))*1.)) / 2.0)))) * 2.0)) * 2.0)) +
                    0.075046*np.tanh(((((data["card4"]) - (((3.0) * ((-1.0*((((((-1.0) - ((((-1.0*(((((((data["V294"]) <= ((((data["C13"]) + ((((data["card4"]) <= (np.where((((data["C6"]) > (data["card4"]))*1.)>0, data["V130"], -1.0 )))*1.)))/2.0)))*1.)) * 2.0))))) * 2.0)))) * 2.0))))))))) * 2.0)) +
                    0.099642*np.tanh(((((((((((((data["card4"]) <= ((((((((((data["D10"]) + ((((data["C5"]) + (data["V315"]))/2.0)))/2.0)) + (data["D1"]))/2.0)) + ((((data["D4"]) + (data["D11"]))/2.0)))/2.0)))*1.)) > ((((data["M5"]) > (np.where(data["C5"] < -9998, data["card4"], data["C11"] )))*1.)))*1.)) * 2.0)) * 2.0)) * 2.0)) +
                    0.099984*np.tanh(((((data["card1"]) + (((((((((((((data["card1"]) - ((((data["M6"]) > (data["V310"]))*1.)))) * 2.0)) + (((data["V45"]) + (data["D8"]))))) + (((data["card1"]) - ((((data["M6"]) > (data["C1"]))*1.)))))) * 2.0)) - ((((data["M6"]) > (data["D1"]))*1.)))))) * 2.0)) +
                    0.099100*np.tanh(((((data["card1"]) + (((((((((((((((((data["R_emaildomain"]) > (((data["C12"]) * 2.0)))*1.)) * 2.0)) - ((((((data["C1"]) <= (data["C1"]))*1.)) * ((((data["D14"]) > (data["V312"]))*1.)))))) + (((((data["card1"]) * 2.0)) * 2.0)))) + (data["V45"]))/2.0)) * 2.0)) * 2.0)))) * 2.0)) +
                    0.000640*np.tanh(((((data["V133"]) - ((5.79200649261474609)))) + ((((((((((((data["C6"]) <= ((((data["card4"]) + ((((data["V294"]) <= (((((((data["card4"]) <= ((((np.tanh((data["V133"]))) + (data["C6"]))/2.0)))*1.)) + (data["C14"]))/2.0)))*1.)))/2.0)))*1.)) * 2.0)) * 2.0)) * 2.0)) * 2.0)))) +
                    0.097336*np.tanh(((np.where((((data["V312"]) > (data["D10"]))*1.)>0, np.where((((data["C6"]) <= (data["C1"]))*1.)>0, -3.0, (((data["V312"]) > (data["C1"]))*1.) ), (-1.0*((np.where((((data["D10"]) <= (data["C1"]))*1.)>0, -3.0, (((data["C6"]) <= (data["C9"]))*1.) )))) )) * 2.0)) +
                    0.078432*np.tanh(((np.where(data["C6"]<0, -1.0, (((data["V308"]) <= (((((((((data["D2"]) + (data["C6"]))/2.0)) / 2.0)) + ((((data["C14"]) + (data["C1"]))/2.0)))/2.0)))*1.) )) * ((((4.02401161193847656)) * ((((data["V308"]) <= (np.where(data["C14"] < -9998, data["C6"], (((data["C6"]) + (data["M6"]))/2.0) )))*1.)))))) +
                    0.099500*np.tanh(((((np.where(data["card2"]>0, -1.0, -1.0 )) + ((((((((data["card4"]) <= ((((((data["card2"]) + (data["C6"]))/2.0)) / 2.0)))*1.)) + (((((((data["card4"]) + (data["card2"]))/2.0)) <= ((((((data["D8"]) + (data["card1"]))/2.0)) / 2.0)))*1.)))) * 2.0)))) * 2.0)) +
                    0.093600*np.tanh(((data["TransactionAmt"]) * (((data["TransactionAmt"]) * (np.where((9.78537940979003906)>0, (((((data["C6"]) + ((((data["C1"]) + (((((((data["C1"]) + ((((data["C14"]) > (data["M6"]))*1.)))/2.0)) > (data["C6"]))*1.)))/2.0)))/2.0)) - (((((data["M6"]) / 2.0)) * 2.0))), data["TransactionAmt"] )))))) +
                    0.099950*np.tanh((((7.0)) * (((((data["C10"]) - ((((((data["P_emaildomain"]) > (((data["D10"]) * 2.0)))*1.)) - (((data["card1"]) - (np.where(((data["P_emaildomain"]) * 2.0) < -9998, data["P_emaildomain"], (((data["P_emaildomain"]) > (((data["V45"]) * 2.0)))*1.) )))))))) + (((((data["card2"]) - (data["V308"]))) * 2.0)))))) +
                    0.099997*np.tanh(((((np.tanh(((((data["V283"]) <= ((((data["C10"]) + (data["D10"]))/2.0)))*1.)))) * ((((data["D2"]) > ((((data["M6"]) + (((data["M4"]) * (data["M4"]))))/2.0)))*1.)))) * (np.where(data["D4"]>0, data["TransactionAmt"], ((((data["M4"]) * (data["M4"]))) * 2.0) )))) +
                    0.025578*np.tanh((((((((((((((((((((((data["C14"]) + (((((data["D9"]) + (((data["V315"]) * 2.0)))) + (((((((10.32048892974853516)) * (data["C6"]))) + (-1.0))/2.0)))))/2.0)) * 2.0)) * 2.0)) + (data["C1"]))) * 2.0)) + (data["card1"]))) * 2.0)) + (data["D8"]))) * 2.0)) * 2.0)) +
                    0.099699*np.tanh(((((((((((((((data["D8"]) * 2.0)) * 2.0)) - ((((data["D1"]) <= (data["V283"]))*1.)))) * (data["TransactionAmt"]))) * (((((((data["D5"]) - (data["V283"]))) + (data["D8"]))) + (data["V45"]))))) - ((((data["D5"]) <= (data["V283"]))*1.)))) * 2.0)) +
                    0.099704*np.tanh(((((((((((data["V45"]) + (((data["dist2"]) + ((((((-1.0*(((((data["P_emaildomain"]) > (data["C5"]))*1.))))) + ((((data["C5"]) <= (data["C6"]))*1.)))) - ((((data["D4"]) <= (((data["C5"]) - (((data["P_emaildomain"]) / 2.0)))))*1.)))))))) * 2.0)) + (data["V45"]))) * 2.0)) * 2.0)) +
                    0.085203*np.tanh(((((np.where((((data["D15"]) > (data["V312"]))*1.)>0, data["V45"], ((-3.0) * ((((data["V315"]) <= (data["C1"]))*1.))) )) * 2.0)) - ((((((data["C1"]) <= (data["D15"]))*1.)) - (((((((((data["V315"]) * 2.0)) * 2.0)) * 2.0)) + (((((data["card2"]) * 2.0)) * 2.0)))))))) +
                    0.098080*np.tanh(((((((((data["D14"]) + (((((((data["C6"]) + (data["V45"]))) + (((data["D14"]) + (data["V45"]))))) - ((((data["card1"]) <= (((data["D14"]) * 2.0)))*1.)))))) + ((((data["dist2"]) <= ((((data["D2"]) + (data["V310"]))/2.0)))*1.)))) * 2.0)) * 2.0)) +
                    0.001638*np.tanh((((((((((data["V315"]) + ((-1.0*(((((data["V45"]) > ((((data["D14"]) <= (data["V315"]))*1.)))*1.))))))/2.0)) + ((((((data["V283"]) <= (data["R_emaildomain"]))*1.)) - (np.where(data["V283"]<0, data["D15"], (((data["D4"]) <= (((data["C9"]) + ((-1.0*((data["V45"])))))))*1.) )))))) * 2.0)) * 2.0)) +
                    0.099900*np.tanh(((((((data["card1"]) + (((data["V45"]) + (((((data["card1"]) + ((((((((((data["C2"]) / 2.0)) / 2.0)) + (data["C1"]))) <= (data["C6"]))*1.)))) - (np.tanh(((((data["D10"]) > ((((data["V83"]) + ((((data["C1"]) + (data["C1"]))/2.0)))/2.0)))*1.)))))))))) * 2.0)) * 2.0)) +
                    0.099930*np.tanh(((((((((((((data["V45"]) + (((((data["V315"]) + (((data["V315"]) + ((((((data["C2"]) <= (((data["C6"]) / 2.0)))*1.)) + (data["D9"]))))))) * 2.0)))) * 2.0)) - ((((data["card5"]) > ((((data["D14"]) + (data["addr1"]))/2.0)))*1.)))) + (data["D8"]))) * 2.0)) * 2.0)) +
                    0.099500*np.tanh((((((((((((data["V45"]) * 2.0)) * 2.0)) * 2.0)) * 2.0)) + ((((((((8.0)) * (data["D14"]))) * 2.0)) - ((((3.0) + (np.where(data["V45"]>0, (((((8.0)) - (data["V45"]))) - (((data["D10"]) * (((data["TransactionAmt"]) * 2.0))))), data["P_emaildomain"] )))/2.0)))))/2.0)) +
                    0.080080*np.tanh(((((((data["D8"]) + ((((((-1.0*(((((((data["C2"]) <= (data["card1"]))*1.)) - (((np.where(data["C8"] < -9998, -1.0, ((data["card1"]) - (data["C12"])) )) * ((((9.0)) * 2.0))))))))) + (((((data["card2"]) * 2.0)) * 2.0)))) + (data["V45"]))))) * 2.0)) * 2.0)) +
                    0.099908*np.tanh((((((((((((((data["C12"]) <= (((data["R_emaildomain"]) / 2.0)))*1.)) * 2.0)) + (((((data["M4"]) - ((((data["D11"]) <= (((data["R_emaildomain"]) / 2.0)))*1.)))) - (((data["R_emaildomain"]) - (((data["D3"]) - ((((data["D3"]) > (((data["R_emaildomain"]) * 2.0)))*1.)))))))))) * 2.0)) * 2.0)) * 2.0)) +
                    0.093360*np.tanh(((-1.0) + ((((((((data["V307"]) > (data["D9"]))*1.)) + (((np.where(data["V294"]<0, data["V307"], (((data["V45"]) > (((((((((3.54591345787048340)) - ((3.39796972274780273)))) > (np.where((((data["V315"]) > (data["V294"]))*1.)>0, data["D8"], data["card1"] )))*1.)) / 2.0)))*1.) )) * 2.0)))) * 2.0)))) +
                    0.099923*np.tanh(((((((((((((((data["V283"]) + ((((data["V283"]) <= (data["C10"]))*1.)))) + (data["V45"]))) - ((((data["D4"]) <= (((((((data["D15"]) <= ((((0.0) + (data["M6"]))/2.0)))*1.)) + (data["M6"]))/2.0)))*1.)))) - ((((data["M6"]) <= (data["C10"]))*1.)))) * 2.0)) * 2.0)) * 2.0)) +
                    0.099896*np.tanh((((((((((((data["D14"]) <= (((((((data["V312"]) + (data["dist1"]))/2.0)) + (data["M4"]))/2.0)))*1.)) + ((((((data["C12"]) <= (((data["D14"]) / 2.0)))*1.)) * 2.0)))) * 2.0)) - (((((((data["R_emaildomain"]) + (data["M4"]))/2.0)) <= (data["D14"]))*1.)))) * 2.0)) +
                    0.059597*np.tanh(((((((((((data["V45"]) * 2.0)) - (np.where(data["C1"] < -9998, data["dist1"], ((((((data["C6"]) + (((data["dist1"]) / 2.0)))/2.0)) <= (data["C1"]))*1.) )))) + (((((((((data["C1"]) + (((data["C6"]) / 2.0)))/2.0)) > (data["C6"]))*1.)) * 2.0)))) * 2.0)) * 2.0)) +
                    0.097968*np.tanh((((((((((data["M5"]) > (np.where(((data["card4"]) - (data["C11"]))>0, data["V283"], (((data["M5"]) > (data["D1"]))*1.) )))*1.)) * 2.0)) + (np.where(data["C14"]<0, data["V127"], (-1.0*(((-1.0*(((-1.0*(((((data["dist1"]) <= (data["C8"]))*1.)))))))))) )))) * 2.0)) +
                    0.010384*np.tanh((((((data["V283"]) <= ((((data["D1"]) + (((((((data["C14"]) + (((data["D8"]) / 2.0)))/2.0)) + (((((((data["V283"]) + (data["card4"]))/2.0)) > (((data["C14"]) + (data["D9"]))))*1.)))/2.0)))/2.0)))*1.)) * ((((8.0)) + (data["V45"]))))) +
                    0.099320*np.tanh((((((((data["C5"]) <= (((((((data["C6"]) + (np.where(((data["card1"]) * 2.0)>0, data["V294"], data["card1"] )))/2.0)) + (data["C13"]))/2.0)))*1.)) - ((((data["V294"]) > (((data["C5"]) + (data["card1"]))))*1.)))) - ((((data["C9"]) > (((data["D10"]) + (data["D4"]))))*1.)))) +
                    0.099968*np.tanh((((((((((data["C1"]) <= (data["C14"]))*1.)) * 2.0)) - ((((data["C1"]) > (np.tanh(((((data["M5"]) > (data["M4"]))*1.)))))*1.)))) + (((((((data["C1"]) - ((((data["C14"]) > (((data["card2"]) * 2.0)))*1.)))) + (((((data["C1"]) + (data["C1"]))) * 2.0)))) * 2.0)))) +
                    0.099480*np.tanh(((((((((((data["C8"]) + ((((((data["V45"]) * 2.0)) + (((((data["D14"]) * 2.0)) + (((((data["D9"]) * 2.0)) - ((((data["dist1"]) <= (((data["V45"]) / 2.0)))*1.)))))))/2.0)))) * 2.0)) * 2.0)) - ((((data["D14"]) <= ((((data["V313"]) <= (data["M6"]))*1.)))*1.)))) * 2.0)) +
                    0.096000*np.tanh(((((((data["V45"]) + (((data["D5"]) - ((((data["V310"]) <= ((((data["V45"]) > (((((data["R_emaildomain"]) * 2.0)) - ((((data["V307"]) > (((data["V310"]) - ((((data["M6"]) > (((data["D4"]) * 2.0)))*1.)))))*1.)))))*1.)))*1.)))))) * 2.0)) * 2.0)) +
                    0.092493*np.tanh(((((((((data["D8"]) * 2.0)) * 2.0)) - ((((data["C10"]) <= (np.where(data["D10"]>0, data["V283"], data["C10"] )))*1.)))) + ((((((data["V127"]) <= (data["C12"]))*1.)) - ((((((((data["D10"]) <= (data["C12"]))*1.)) - ((((data["D8"]) <= (data["V127"]))*1.)))) * 2.0)))))) +
                    0.000300*np.tanh(((data["D14"]) + (((((((data["D14"]) + (((((((((data["card4"]) > (((data["C1"]) * 2.0)))*1.)) + ((((data["V283"]) + ((((((data["C6"]) > (((data["C1"]) * 2.0)))*1.)) - ((((data["card1"]) <= ((((data["C10"]) <= (data["V283"]))*1.)))*1.)))))/2.0)))/2.0)) * 2.0)))) * 2.0)) * 2.0)))) +
                    0.044918*np.tanh(((((((((((data["D8"]) + (((data["V294"]) + (((data["V294"]) - (np.tanh(((((data["D8"]) > ((((data["card2"]) + ((((data["C9"]) > (data["V283"]))*1.)))/2.0)))*1.)))))))))) * 2.0)) - (np.tanh(((((data["D10"]) > (((data["V283"]) + (data["V283"]))))*1.)))))) * 2.0)) * 2.0)) +
                    0.097003*np.tanh(((((((((((data["card1"]) + ((((((data["V294"]) <= (((data["C13"]) * ((((data["card1"]) > ((((data["card1"]) > (((((((data["card2"]) + (data["card2"]))/2.0)) + (data["dist2"]))/2.0)))*1.)))*1.)))))*1.)) - (((((data["M5"]) * 2.0)) * 2.0)))))) * 2.0)) * 2.0)) * 2.0)) * 2.0)) +
                    0.098997*np.tanh(((((((((data["D9"]) + ((((((np.where((((data["card5"]) <= (data["V127"]))*1.)>0, data["M5"], data["V313"] )) > (data["D9"]))*1.)) + (data["R_emaildomain"]))))) * 2.0)) * 2.0)) + (((data["V45"]) - (((((((data["V133"]) > (data["V313"]))*1.)) <= ((((data["card5"]) <= (data["V127"]))*1.)))*1.)))))) +
                    0.081920*np.tanh((((((((-1.0*(((((data["C1"]) > (data["C14"]))*1.))))) + ((((data["V312"]) <= (data["V133"]))*1.)))) + (((((data["C8"]) + (np.where((((data["V133"]) > (data["C14"]))*1.)>0, (((data["M4"]) <= (data["C2"]))*1.), (-1.0*(((((data["C2"]) <= (data["V133"]))*1.)))) )))) * 2.0)))) * 2.0)) +
                    0.098624*np.tanh(((data["C10"]) + (((((((((((data["D14"]) * 2.0)) * 2.0)) + ((((data["D5"]) > (data["C14"]))*1.)))) - ((-1.0*((((((((data["C10"]) * 2.0)) - ((((data["D2"]) <= ((((data["C14"]) <= (np.where(data["card2"]>0, data["C10"], data["C14"] )))*1.)))*1.)))) * 2.0))))))) * 2.0)))) +
                    0.091411*np.tanh((((((data["C2"]) > (data["card2"]))*1.)) + ((((((((data["C6"]) > (((data["C2"]) * 2.0)))*1.)) + ((((((((data["card4"]) > (((data["C6"]) * 2.0)))*1.)) - ((((data["D10"]) <= (np.tanh((((data["D4"]) - (data["card2"]))))))*1.)))) * 2.0)))) * 2.0)))) +
                    0.038800*np.tanh(((((((data["card1"]) * 2.0)) - ((((data["D11"]) <= ((((data["M6"]) + ((((data["M6"]) > (((data["D3"]) * 2.0)))*1.)))/2.0)))*1.)))) - ((((data["D1"]) <= ((((data["M6"]) + ((((((1.0) * (data["C10"]))) <= (np.where(data["D11"]>0, data["V283"], data["C10"] )))*1.)))/2.0)))*1.)))) +
                    0.096800*np.tanh(((((((((((-1.0) * ((((data["addr1"]) <= (((data["C5"]) / 2.0)))*1.)))) + ((((data["V283"]) > (data["V313"]))*1.)))) + ((((-1.0*(((((((((data["C5"]) <= (data["D3"]))*1.)) * 2.0)) * 2.0))))) * ((((data["V283"]) > (data["V313"]))*1.)))))) * 2.0)) * 2.0)) +
                    0.099600*np.tanh(((((-2.0) * ((((np.where(((data["D8"]) - (data["card1"]))<0, data["C14"], ((((((data["D8"]) - (data["card1"]))) * 2.0)) * 2.0) )) <= (data["C8"]))*1.)))) + ((((((data["V313"]) <= (((data["dist1"]) * 2.0)))*1.)) - ((((data["C14"]) > (data["V313"]))*1.)))))) +
                    0.098914*np.tanh((((((data["C11"]) > (data["C8"]))*1.)) + (((((((data["C11"]) - (np.where((((data["C10"]) > (data["V314"]))*1.)>0, data["V314"], (((data["card2"]) <= (((np.where((((data["V307"]) > (data["D14"]))*1.)>0, data["D14"], (((data["D14"]) > (data["C8"]))*1.) )) / 2.0)))*1.) )))) * 2.0)) * 2.0)))) +
                    0.099740*np.tanh(((((((data["V45"]) * 2.0)) + (((data["D8"]) - ((((((data["C13"]) > (np.where((((data["dist2"]) > (np.where(data["D4"] < -9998, data["D8"], data["V294"] )))*1.)>0, data["V83"], (((data["V315"]) > (data["D8"]))*1.) )))*1.)) * 2.0)))))) + (np.tanh(((((data["V314"]) > (data["C1"]))*1.)))))) +
                    0.098520*np.tanh((((data["card2"]) > (np.tanh(((((-1.0*((((data["C9"]) * (data["V283"])))))) - ((((-1.0*((np.tanh((np.tanh((((data["C2"]) + ((((data["C2"]) <= (((data["card2"]) + (((data["C9"]) * (data["V127"]))))))*1.))))))))))) / 2.0)))))))*1.)) +
                    0.096120*np.tanh(((data["TransactionAmt"]) * ((((np.where(data["M6"]<0, data["D1"], ((data["TransactionAmt"]) * (((data["C5"]) * (((data["V83"]) + (data["C10"])))))) )) > ((((data["C14"]) <= (np.where((((data["V294"]) > (data["M6"]))*1.)>0, (((data["V83"]) > (data["M6"]))*1.), ((data["V308"]) * 2.0) )))*1.)))*1.)))) +
                    0.093600*np.tanh(((data["D9"]) + ((-1.0*(((((np.where((((((data["C11"]) > (data["D1"]))*1.)) / 2.0)>0, data["dist2"], (((data["D9"]) <= (data["M4"]))*1.) )) <= ((((data["D1"]) <= (np.where((((data["M6"]) > (data["V45"]))*1.)>0, data["card2"], (((data["M6"]) > (((data["card2"]) * 2.0)))*1.) )))*1.)))*1.))))))) +
                    0.092400*np.tanh(np.where(data["card5"]<0, data["V45"], np.where((((data["D1"]) > (((data["card5"]) - (((((data["V310"]) + (((((data["D4"]) + (np.where((((data["D11"]) > (data["D1"]))*1.)<0, data["card5"], data["D1"] )))) / 2.0)))) / 2.0)))))*1.)>0, (((data["card5"]) > (data["D15"]))*1.), -2.0 ) )) +
                    0.098400*np.tanh(((((data["V83"]) - ((((data["card1"]) <= ((((data["D3"]) <= (data["V294"]))*1.)))*1.)))) + (((((np.where(data["card1"]<0, data["V294"], (((((((((data["C8"]) * 2.0)) <= (np.where(data["dist2"]>0, data["dist1"], data["C14"] )))*1.)) + (data["V294"]))) + (data["C8"])) )) * 2.0)) * 2.0)))) +
                    0.089680*np.tanh(((3.0) * (np.where(((((data["C14"]) * 2.0)) - (data["R_emaildomain"]))>0, (((data["dist1"]) > (((((((data["C14"]) * 2.0)) - (data["R_emaildomain"]))) * 2.0)))*1.), ((((((data["R_emaildomain"]) * 2.0)) * 2.0)) - ((((data["C9"]) > (((data["C1"]) + (((data["D1"]) / 2.0)))))*1.))) )))) +
                    0.099985*np.tanh((((((((data["C6"]) > (((data["C2"]) * 2.0)))*1.)) + ((-1.0*(((((data["D11"]) <= (((((((((((data["P_emaildomain"]) * 2.0)) * 2.0)) <= (data["card4"]))*1.)) + ((((((((data["C8"]) * 2.0)) + (-1.0))) + ((((data["D11"]) <= (data["C6"]))*1.)))/2.0)))/2.0)))*1.))))))) * 2.0)) +
                    0.099840*np.tanh(((((((data["C2"]) + (((((data["card1"]) * 2.0)) + ((((((data["C2"]) * 2.0)) <= ((((np.tanh((data["C6"]))) + (data["P_emaildomain"]))/2.0)))*1.)))))) - ((((((data["card1"]) * 2.0)) <= (np.tanh(((((data["C6"]) + ((((((data["card1"]) / 2.0)) > (data["C13"]))*1.)))/2.0)))))*1.)))) * 2.0)) +
                    0.086816*np.tanh((((((((((((((data["M4"]) * 2.0)) <= (data["card4"]))*1.)) + (((data["card4"]) + ((((((data["card4"]) * 2.0)) <= ((((data["M4"]) + (data["V283"]))/2.0)))*1.)))))) * 2.0)) * 2.0)) - ((((data["D10"]) <= ((((data["V283"]) + ((((np.tanh((data["D8"]))) <= (data["D10"]))*1.)))/2.0)))*1.)))) +
                    0.099120*np.tanh((((((((((((data["C5"]) > ((((data["C11"]) > (((data["C6"]) / 2.0)))*1.)))*1.)) + ((((data["dist1"]) > (((data["M5"]) - (np.where(data["V83"] < -9998, data["V317"], ((((data["V83"]) - (((data["M5"]) * 2.0)))) / 2.0) )))))*1.)))) * 2.0)) * 2.0)) * 2.0)) +
                    0.091354*np.tanh(np.where(((data["card1"]) - (data["V283"]))>0, (((data["C6"]) > (data["V310"]))*1.), (((((((np.tanh((data["V315"]))) > (data["V307"]))*1.)) - ((((data["P_emaildomain"]) <= ((((data["V315"]) <= (data["C12"]))*1.)))*1.)))) - ((((data["P_emaildomain"]) <= (data["C6"]))*1.))) )) +
                    0.099969*np.tanh(((np.where(((data["C11"]) - (data["V310"]))<0, data["V283"], ((data["M6"]) + ((((8.91212749481201172)) * (((((data["R_emaildomain"]) - ((((data["D4"]) <= (((data["D10"]) / 2.0)))*1.)))) * 2.0))))) )) - ((((data["M6"]) <= (np.where(data["D9"] < -9998, data["card2"], ((data["R_emaildomain"]) / 2.0) )))*1.)))) +
                    0.099995*np.tanh((((((((data["V45"]) <= ((((data["card4"]) + ((((data["C2"]) <= (((data["C6"]) / 2.0)))*1.)))/2.0)))*1.)) * 2.0)) - ((((((data["V45"]) * 2.0)) <= ((((((data["D1"]) <= ((((data["C6"]) > (((((np.tanh((data["R_emaildomain"]))) * 2.0)) - (data["V45"]))))*1.)))*1.)) / 2.0)))*1.)))) +
                    0.099840*np.tanh(((((((((((data["C1"]) * 2.0)) + (data["dist2"]))) * 2.0)) - ((((data["C6"]) > (data["C2"]))*1.)))) + ((((((((data["C2"]) <= ((((((data["V83"]) + ((((((((data["C6"]) * 2.0)) + (data["D3"]))/2.0)) * 2.0)))/2.0)) - (((data["C1"]) * 2.0)))))*1.)) * 2.0)) * 2.0)))) +
                    0.093904*np.tanh(((3.0) * (((((np.where(data["C2"]<0, data["V314"], (-1.0*(((((data["card1"]) <= (((((np.where(((data["V315"]) - (data["C10"]))<0, data["C10"], data["C2"] )) / 2.0)) / 2.0)))*1.)))) )) * 2.0)) + ((((((data["D14"]) - (data["C10"]))) > (((data["card1"]) / 2.0)))*1.)))))) +
                    0.099806*np.tanh((((((data["V310"]) > (data["card2"]))*1.)) + (((((((data["D1"]) + (((((data["C10"]) - ((((data["dist2"]) > ((((data["D10"]) > (((data["C12"]) / 2.0)))*1.)))*1.)))) * 2.0)))) - ((((data["V314"]) > (np.where(data["D11"]>0, data["card4"], ((data["C12"]) / 2.0) )))*1.)))) * 2.0)))) +
                    0.097120*np.tanh((((((((((data["M5"]) <= (((data["dist2"]) - (((data["D8"]) + (((data["V307"]) - (((data["V313"]) - (data["addr1"]))))))))))*1.)) + (((data["V315"]) - ((((data["card1"]) <= (((data["D8"]) - ((((data["M6"]) > (data["C12"]))*1.)))))*1.)))))) * 2.0)) * 2.0)) +
                    0.080000*np.tanh(((((((((((((((((((data["D2"]) * 2.0)) - ((((((data["D15"]) * 2.0)) <= ((((data["M6"]) + (((data["D2"]) / 2.0)))/2.0)))*1.)))) * 2.0)) - ((((data["C2"]) <= (((data["D15"]) - (((data["C12"]) / 2.0)))))*1.)))) * 2.0)) * 2.0)) * 2.0)) * 2.0)) - (data["C12"]))) +
                    0.100000*np.tanh((((((data["dist1"]) <= (data["V313"]))*1.)) - ((((data["D15"]) <= (np.where(((data["M4"]) - (data["C13"]))>0, np.where(((-3.0) * (((data["V313"]) - (data["C13"]))))>0, data["D15"], np.tanh((((data["C11"]) - (data["C13"])))) ), (((data["C11"]) <= (data["M4"]))*1.) )))*1.)))) +
                    0.099760*np.tanh((((((data["V83"]) <= ((((data["card4"]) + ((((data["P_emaildomain"]) + (np.where(data["V130"]<0, data["V310"], (((data["C6"]) <= ((((((data["C1"]) / 2.0)) + (((((((((data["C12"]) <= (((data["D14"]) / 2.0)))*1.)) + (((data["C1"]) / 2.0)))) + (data["V83"]))/2.0)))/2.0)))*1.) )))/2.0)))/2.0)))*1.)) * 2.0)) +
                    0.099100*np.tanh(((((((((data["C6"]) * 2.0)) * 2.0)) * 2.0)) + (((((data["V45"]) - (((((((data["V314"]) + (data["C1"]))/2.0)) > (data["R_emaildomain"]))*1.)))) - (((((((data["C1"]) + ((((data["C2"]) > (data["C11"]))*1.)))/2.0)) > (np.tanh(((((((data["V314"]) + (data["C2"]))/2.0)) / 2.0)))))*1.)))))) +
                    0.099812*np.tanh((((np.where(((data["D2"]) - (data["V313"]))>0, (((data["V313"]) <= ((((data["P_emaildomain"]) + ((((data["card1"]) <= ((((data["M5"]) + (np.tanh(((((data["card1"]) + (np.where(data["card1"]>0, data["card2"], -2.0 )))/2.0)))))/2.0)))*1.)))/2.0)))*1.), data["card1"] )) > (data["D9"]))*1.)) +
                    0.099797*np.tanh(((((((((data["D10"]) - ((((data["M5"]) > (((data["P_emaildomain"]) * 2.0)))*1.)))) - ((((data["D2"]) <= (((data["D10"]) / 2.0)))*1.)))) * 2.0)) - (((((((data["C5"]) > ((((((data["C9"]) + (data["M5"]))/2.0)) * 2.0)))*1.)) > ((((data["M4"]) <= (((data["D10"]) / 2.0)))*1.)))*1.)))) +
                    0.099200*np.tanh((((((data["C14"]) <= (data["C14"]))*1.)) + ((-1.0*(((((((((data["card1"]) > (((((((data["D1"]) + ((-1.0*(((((data["C14"]) > (np.where(((data["C11"]) - (data["C14"]))>0, data["C13"], (3.0) )))*1.))))))) * 2.0)) - ((-1.0*((data["C8"])))))))*1.)) * 2.0)) * 2.0))))))) +
                    0.082381*np.tanh(((((((((((((((data["card1"]) - ((((data["D10"]) <= (np.tanh((((((((data["card2"]) + ((((data["M5"]) <= ((((data["card1"]) <= (np.tanh((data["M4"]))))*1.)))*1.)))/2.0)) + ((((data["M4"]) <= (np.tanh((data["dist2"]))))*1.)))/2.0)))))*1.)))) * 2.0)) * 2.0)) * 2.0)) * 2.0)) * 2.0)) * 2.0)) +
                    0.098326*np.tanh(((((data["card2"]) - ((((((data["C5"]) > (((data["C13"]) * 2.0)))*1.)) + ((((((data["C8"]) > (data["card5"]))*1.)) + ((((data["C5"]) > (((data["C9"]) * 2.0)))*1.)))))))) + ((((data["V283"]) <= (np.where(((data["card2"]) - (data["V283"]))>0, data["C11"], data["C5"] )))*1.)))) +
                    0.099900*np.tanh(((((((((((((data["D8"]) * 2.0)) <= ((((data["V313"]) + (data["P_emaildomain"]))/2.0)))*1.)) > (data["D11"]))*1.)) + ((((((data["V313"]) > (data["D11"]))*1.)) - ((((data["dist1"]) <= ((((data["V313"]) + ((((data["V313"]) > (((np.tanh((data["P_emaildomain"]))) * 2.0)))*1.)))/2.0)))*1.)))))) * 2.0)) +
                    0.083443*np.tanh((((((((((data["C14"]) > ((((((data["V130"]) - (data["D3"]))) <= ((((((data["M4"]) - ((((data["D4"]) <= (data["C6"]))*1.)))) <= (((data["card2"]) * ((((((data["D15"]) > (((data["C8"]) - (data["C6"]))))*1.)) * 2.0)))))*1.)))*1.)))*1.)) * 2.0)) * 2.0)) * 2.0)) +
                    0.034768*np.tanh((((((data["D5"]) <= (((data["V294"]) + ((((data["V294"]) <= (data["C2"]))*1.)))))*1.)) - ((((((((data["card1"]) - (((data["V294"]) - (data["C14"]))))) * 2.0)) <= ((((data["V294"]) <= (np.where(data["V312"]>0, data["C14"], data["V294"] )))*1.)))*1.)))) +
                    0.099948*np.tanh((((((((((data["dist1"]) <= (np.tanh((((data["D3"]) - (data["V83"]))))))*1.)) + ((((((((data["M6"]) <= (np.tanh((((((data["dist1"]) - (data["M4"]))) * 2.0)))))*1.)) + ((-1.0*(((((data["D3"]) > (((data["D11"]) * ((5.66594266891479492)))))*1.))))))) * 2.0)))) * 2.0)) * 2.0)) +
                    0.079600*np.tanh(((((((data["D9"]) + (data["dist2"]))) * 2.0)) + (((data["card2"]) + (((data["card2"]) + (((data["D9"]) + (((data["card2"]) + (((data["card2"]) - ((((data["card2"]) > (((((data["D11"]) + (data["D4"]))) - ((((data["card1"]) <= (data["D4"]))*1.)))))*1.)))))))))))))) +
                    0.099462*np.tanh((((((((((-1.0*(((((data["M6"]) > (((data["D10"]) * 2.0)))*1.))))) + ((((data["dist1"]) > (((data["C10"]) * 2.0)))*1.)))) + ((((data["C6"]) <= (((data["C11"]) / 2.0)))*1.)))) * 2.0)) + ((((((data["C8"]) / 2.0)) > ((((((data["C6"]) / 2.0)) + (data["C10"]))/2.0)))*1.)))) +
                    0.096720*np.tanh((((((((((data["addr1"]) > (((data["M6"]) * 2.0)))*1.)) * 2.0)) * 2.0)) - ((((((((data["D11"]) <= ((((data["M6"]) + ((((((data["dist2"]) <= ((((data["M6"]) + (np.where(data["D11"] < -9998, data["P_emaildomain"], (((data["M6"]) > (data["D14"]))*1.) )))/2.0)))*1.)) * 2.0)))/2.0)))*1.)) * 2.0)) * 2.0)))) +
                    0.095440*np.tanh((((((((((((((data["V317"]) * 2.0)) <= (((data["D2"]) - (((np.where(((data["V317"]) * 2.0)>0, data["V315"], data["dist1"] )) - (data["dist1"]))))))*1.)) - ((((data["M6"]) > (((data["D15"]) * 2.0)))*1.)))) * 2.0)) - ((((data["M6"]) > (((data["D2"]) * 2.0)))*1.)))) * 2.0)) +
                    0.099999*np.tanh((-1.0*((np.where(((((((data["dist2"]) > (data["V310"]))*1.)) <= (data["dist2"]))*1.)>0, (((data["dist2"]) > (data["V130"]))*1.), ((((((((data["TransactionAmt"]) * (data["V283"]))) * ((((data["C5"]) > (data["M5"]))*1.)))) - ((((data["card1"]) > (data["V130"]))*1.)))) * 2.0) ))))) +
                    0.090032*np.tanh((((((data["C13"]) <= (((data["V133"]) + (((data["V315"]) * (data["C14"]))))))*1.)) + ((((((data["D10"]) <= (((data["V308"]) + (((((data["D9"]) * (data["C14"]))) * 2.0)))))*1.)) - ((((((data["V133"]) + (((data["V315"]) * (data["C14"]))))) <= (data["V315"]))*1.)))))) +
                    0.094000*np.tanh(((((data["dist2"]) - ((((data["V294"]) > (data["D3"]))*1.)))) + ((((((((((((((data["D14"]) * 2.0)) > (data["V310"]))*1.)) > ((((data["C1"]) > (((data["C11"]) * 2.0)))*1.)))*1.)) <= ((((data["dist1"]) > (((data["C1"]) * 2.0)))*1.)))*1.)) * 2.0)))) +
                    0.094032*np.tanh(((((((((data["C5"]) + (data["dist2"]))/2.0)) <= ((((data["card1"]) + (np.tanh((np.tanh((((((np.where(data["card1"]>0, ((((((data["C5"]) + (data["card2"]))/2.0)) > (((np.where(data["D3"]>0, data["card1"], data["dist2"] )) * 2.0)))*1.), data["card1"] )) * 2.0)) - (data["card2"]))))))))/2.0)))*1.)) * 2.0)) +
                    0.100000*np.tanh((((((((((((((data["V312"]) / 2.0)) > (data["D8"]))*1.)) + ((((((-1.0*(((((data["C9"]) <= (np.where(-2.0<0, ((data["V312"]) / 2.0), data["V312"] )))*1.))))) * 2.0)) + ((((data["V312"]) > (data["D8"]))*1.)))))) * 2.0)) * 2.0)) + ((((data["V133"]) > (data["D8"]))*1.)))) +
                    0.057200*np.tanh(((((((((((((((((data["card1"]) > (data["dist2"]))*1.)) * (data["V294"]))) > (((((((data["dist1"]) + (data["D3"]))) / 2.0)) * 2.0)))*1.)) - ((((data["V130"]) <= (data["V133"]))*1.)))) * 2.0)) * 2.0)) - ((((data["V130"]) <= (data["D3"]))*1.)))) +
                    0.081840*np.tanh((((data["M5"]) > ((((data["V283"]) + (((data["C11"]) * ((((3.0) + ((-1.0*(((((((data["C11"]) > (np.tanh((data["P_emaildomain"]))))*1.)) * ((((((((data["card1"]) > (((data["M5"]) + (data["C12"]))))*1.)) * ((((3.0) + (data["C12"]))/2.0)))) * 2.0))))))))/2.0)))))/2.0)))*1.)) +
                    0.093800*np.tanh(((((((((((((((data["P_emaildomain"]) - (data["C12"]))) - (((data["C12"]) - ((((data["D14"]) <= (((data["dist1"]) - (((data["V45"]) - (((data["C12"]) * (((((((data["V313"]) > (data["card5"]))*1.)) > (data["card5"]))*1.)))))))))*1.)))))) * 2.0)) * 2.0)) * 2.0)) * 2.0)) * 2.0)) +
                    0.099928*np.tanh((((((((((((data["D1"]) <= (data["D2"]))*1.)) + (((((np.where(data["D3"] < -9998, data["D2"], np.where(data["card1"]>0, (((data["D2"]) > (((data["card1"]) * 2.0)))*1.), -3.0 ) )) + ((((data["C12"]) > (data["D3"]))*1.)))) - (((data["card1"]) * 2.0)))))) * 2.0)) * 2.0)) * 2.0)))


# In[ ]:


train = pd.read_csv('../input/ieee-fraud-detection/train_transaction.csv')
test = pd.read_csv('../input/ieee-fraud-detection/test_transaction.csv')


# In[ ]:


tr = pd.DataFrame()
te = pd.DataFrame()
for c in features:
    if(c!='TransactionAmt'):
        tr[c], te[c] = target_encode( train[c],
                                      test[c],
                                      train.isFraud,
                                      min_samples_leaf=100, 
                                      smoothing=10,
                                      noise_level=.01)
    else:
        tr[c], te[c] = train[c], test[c]
tr['isFraud'] = train.isFraud


# In[ ]:


roc_auc_score(tr.isFraud,GP(tr))


# In[ ]:


test_predictions = pd.DataFrame()
test_predictions['TransactionID'] = test.TransactionID.values
test_predictions['isFraud'] = GP(te).values
test_predictions[['TransactionID','isFraud']].to_csv('gpsubmission.csv', index=False)

