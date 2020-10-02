#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import math


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data_train=pd.read_csv("../input/train.csv")
data_test=pd.read_csv("../input/test.csv")


# In[ ]:


data_train.sample(7)


# In[ ]:


data_train.dtypes
data_test.dtypes


# In[ ]:


data_train.info()


# In[ ]:


data_train.isna().sum()


# In[ ]:


def DF_initial_observations(data_train):
    '''Gives basic details of columns in a dataframe : Data types, distinct values, NAs and sample'''
    if isinstance(data_train, pd.DataFrame):
        total_na=0
        for i in range(len(data_train.columns)):        
            total_na+= data_train.isna().sum()[i]
        print('Dimensions : %d rows, %d columns' % (data_train.shape[0],data_train.shape[1]))
        print("Total NA values : %d" % (total_na))
        print('%38s %10s     %10s %10s %15s' % ('Column name', ' Data Type', '# Distinct', ' NA values', ' Sample value'))
        for i in range(len(data_train.columns)):
            col_name = data_train.columns[i]
            sampl = data_train[col_name].sample(1)
            sampl.apply(pd.Categorical)
            sampl_p = str(sampl.iloc[0,])
            print('%38s %10s :   %10d  %10d %15s' % (data_train.columns[i],data_train.dtypes[i],data_train.nunique()[i],data_train.isna().sum()[i], sampl_p))
    else:
        print('Expected a DataFrame but got a %15s ' % (type(data)))


# In[ ]:


DF_initial_observations(data_train)


# In[ ]:


data_train.corr().style.format("{:.3}").background_gradient(cmap=plt.get_cmap('coolwarm'), axis=1)


# Different Ways of defining Correlation Syntax

# In[ ]:


data_train.corr()[2:8] [["GarageCars","SalePrice","GarageYrBlt"]]     #correlation value for corresponding columns with the indexed columns


# In[ ]:


data_train["GarageCars"].corr(data_train["SalePrice"])  #correlation between 2 columns


# In[ ]:


#data_train.corr()
data_train[data_train.columns].corr()["GarageCars"][:]    #correlation of GarageCars with all other columns
#here garage cars and garage area are highly correlated


# In[ ]:


#heatmap for the generating correlated values

sns.set(style="white")

# Compute the correlation matrix
correln = data_train.corr()

# Generate a mask for the upper triangle
#mask = np.zeros_like(correln, dtype=np.bool)
#mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(correln,  cmap=cmap, vmax=.3, #mask=mask,
            linewidths=.5, cbar_kws={"shrink": .7})


# In[ ]:


data_train.corr()[["TotalBsmtSF","1stFlrSF"]]      #correaltion of TotalBsmtSF and 1stFlrSF with all other columns


# In[ ]:


plt.boxplot(data_train["MiscVal"])


# In[ ]:


plt.boxplot(data_train["GrLivArea"])


# In[ ]:


plt.boxplot(data_train["LotArea"])


# In[ ]:


data_train.describe()


# In[ ]:


plt.boxplot(data_train["3SsnPorch"])


# In[ ]:


plt.boxplot(data_train["GrLivArea"])


# In[ ]:


data_train["MasVnrType"].isna().sum()


# In[ ]:


data_train["MasVnrType"].value_counts()


# In[ ]:


DF_initial_observations(data_train)


# In[ ]:


data_train["MasVnrType"].unique()


# In[ ]:


data_train.loc[data_train["MasVnrType"]=="None"]


# In[ ]:


data_train.columns


# In[ ]:


data1=data_train[(data_train["Foundation"]=="PConc") & (data_train["Exterior1st"]=="VinylSd") & (data_train["Exterior2nd"]=="VinylSd")]


# In[ ]:


max_value=data_train["MasVnrArea"].value_counts().index.tolist()


# In[ ]:


max_value[0]


# In[ ]:


data_train["MasVnrArea"]=data_train["MasVnrArea"].replace(np.nan,max_value[0])


# In[ ]:


data_train["MasVnrArea"].unique()


# In[ ]:


data1["MasVnrArea"].value_counts()


# In[ ]:


data_train["Foundation"].value_counts()


# In[ ]:


data_train["Foundation"]== "PConc"


# In[ ]:


data=data_train["MasVnrType"].value_counts().index.tolist()


# In[ ]:


data_train["MasVnrType"]=data_train["MasVnrType"].replace(np.nan,data[0])


# In[ ]:


data_train["MasVnrType"].isna().sum()


# In[ ]:


data_train["LotFrontage"].value_counts()


# In[ ]:


data_train.loc[data_train["LotFrontage"]==60]


# In[ ]:


data_train=data_train.drop(["Alley","PoolQC","MiscFeature"],axis=1)


# In[ ]:


data_train.shape


# In[ ]:


DF_initial_observations(data_train)


# In[ ]:


data_train["BsmtQual"].unique()


# In[ ]:


data_train["BsmtQual"].isna().sum()


# In[ ]:


data_train["BsmtExposure"].value_counts()


# In[ ]:


data_count1=data_train["BsmtExposure"].value_counts().index.tolist()


# In[ ]:


data_count1[1]


# In[ ]:


data_train["BsmtExposure"]=data_train["BsmtExposure"].replace(np.nan,data_count1[0])


# In[ ]:


data_train["BsmtExposure"].unique()


# In[ ]:


data_count1=data_train["BsmtFinType2"].value_counts().index.tolist()


# In[ ]:


data_train["BsmtFinType2"]=data_train["BsmtFinType2"].replace(np.nan,data_count1[0])


# In[ ]:


data_train["BsmtFinType2"].isna().sum()


# In[ ]:


data_train["FireplaceQu"].value_counts()


# In[ ]:


data_train[data_train["FireplaceQu"]=="Gd"]


# In[ ]:


data_train.corr()


# In[ ]:


data_train["FireplaceQu"].isnull().sum()


# In[ ]:


data_train[data_train["LotShape"]== "IR1"]


# In[ ]:


data_train[data_train["LotFrontage"].isnull()]


# In[ ]:


data_train.columns


# In[ ]:


data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(), np.nanmedian(data_train[data_train["Neighborhood"]=="NWAmes"]["LotFrontage"]),data_train["LotFrontage"])


# In[ ]:


data_train["LotFrontage"].unique


# In[ ]:


data_train["Neighborhood"].unique()


# In[ ]:


data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="Veenker"]["LotFrontage"]),data_train["LotFrontage"])


# In[ ]:


data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="NoRidge"]["LotFrontage"]),data_train["LotFrontage"])


# In[ ]:


data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="CollgCr"]["LotFrontage"]),data_train["LotFrontage"])


# In[ ]:


data_train["Neighborhood"].unique()


# In[ ]:


data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="Mitchel"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="Somerst"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="OldTown"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="BrkSide"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="Sawyer"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="NridgHt"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="NAmes"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="SawyerW"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="IDOTRR"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="MeadowV"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="Edwards"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="Gilbert"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="Timber"]["LotFrontage"]),data_train["LotFrontage"])
data_train["LotFrontage"]=np.where(data_train["LotFrontage"].isna(),np.nanmedian(data_train[data_train["Neighborhood"]=="StoneBr"]["LotFrontage"]),data_train["LotFrontage"])


# In[ ]:


data_train["LotFrontage"].isnull().sum()


# In[ ]:


data_train.columns


# In[ ]:


data_train[['GarageType', 'GarageYrBlt',
       'GarageFinish', 'GarageCars', 'GarageArea', 'GarageQual', 'GarageCond']].info()


# In[ ]:


data_train.GarageArea.unique()


# In[ ]:


data_train.shape


# In[ ]:


data_train1=data_train[["GarageType","GarageYrBlt","GarageFinish","GarageQual","GarageCond","Fence","BsmtQual","FireplaceQu"]]


# In[ ]:


data_train.dropna(how="all",thresh=6,subset=["GarageType","GarageYrBlt","GarageFinish","GarageQual","GarageCond","Fence","BsmtQual","FireplaceQu"], inplace=True)


# In[ ]:


data_train.isna().sum()


# In[ ]:


y=data_train[['GarageType', 'GarageYrBlt',
       'GarageFinish', 'GarageCars', 'GarageArea', 'GarageQual', 'GarageCond']]
z=y[y.isnull().any(axis=1)]
z


# In[ ]:


data_train.info()


# In[ ]:


data_train[data_train.isna().any(axis = 1)]


# In[ ]:


data_train.columns.isnull()


# In[ ]:


data_train.columns


# In[ ]:


data_train.drop(["Fence"],axis=1,inplace=True)


# In[ ]:


DF_initial_observations(data_train)


# In[ ]:


data_train["Electrical"].isna().sum()


# In[ ]:


data_train["Electrical"].value_counts()


# In[ ]:


data_train["Electrical"]=data_train["Electrical"].replace(np.nan,"SBrkr")


# In[ ]:


data_train["Electrical"].isna().sum()


# In[ ]:


data_train["MasVnrType"].value_counts()


# In[ ]:


data_train["MasVnrType"]=data_train["MasVnrType"].replace(np.nan,"None")


# In[ ]:


data_train["BsmtQual"].value_counts()


# In[ ]:


data_train["BsmtFinType1"].value_counts()


# In[ ]:


data_train["BsmtCond"].value_counts()


# In[ ]:


data_train["BsmtCond"]=data_train["BsmtCond"].replace(np.nan,"TA")


# In[ ]:


data_train["BsmtFinType1"].fillna(method="ffill",inplace=True)


# In[ ]:


data_train["BsmtQual"].fillna(method="ffill",inplace=True)


# In[ ]:


data_train["BsmtQual"].isna().sum()


# In[ ]:


data_train["BsmtQual"].value_counts()


# In[ ]:


data_train.sample(7)


# In[ ]:


data_train["FireplaceQu"].value_counts()              


# In[ ]:


data_train["FireplaceQu"]=data_train["FireplaceQu"].replace(np.nan,"unknown")


# In[ ]:


data_train["FireplaceQu"].isna().sum()


# In[ ]:


data_train[(data_train['MiscVal'] == 15500.000000) | (data_train['GrLivArea'] == 5642.000000) | (data_train['LotFrontage'] == 313.000000) |(data_train['LotArea'] == 215245.000000) | (data_train['MasVnrArea'] == 1600.000000) |(data_train['BsmtFinSF1'] == 5644.000000)
| (data_train['BsmtFinSF2'] == 1474.000000) | (data_train['TotalBsmtSF'] == 6110.000000) | (data_train['1stFlrSF'] == 4692.000000)
    | (data_train['LowQualFinSF'] == 572.000000) | (data_train['WoodDeckSF'] == 857.000000)
    | (data_train['EnclosedPorch'] == 552.000000) | (data_train['PoolArea'] == 738.000000) | (data_train['3SsnPorch'] == 508.000000)]


# In[ ]:


final_data= data_train[(data_train['MiscVal'] != 15500.000000) & (data_train['GrLivArea'] != 5642.000000) & (data_train['LotFrontage'] != 313.000000) & (data_train['LotArea'] != 215245.000000) & (data_train['MasVnrArea'] != 1600.000000) & (data_train['BsmtFinSF1'] != 5644.000000)
& (data_train['BsmtFinSF2'] != 1474.000000) & (data_train['TotalBsmtSF'] != 6110.000000) & (data_train['1stFlrSF'] != 4692.000000)
    &(data_train['LowQualFinSF'] != 572.000000) & (data_train['WoodDeckSF'] != 857.000000)
    & (data_train['EnclosedPorch'] != 552.000000) & (data_train['PoolArea'] != 738.000000) & (data_train['3SsnPorch'] != 508.000000)]


# In[ ]:


final_data.shape


# DATA VISUALIZATION
# 

# In[ ]:


sns.set()
cols = ['SalePrice', 'OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath', 'YearBuilt']
sns.pairplot(final_data[cols],palette="colorblind", height = 3,diag_kind="kde")
plt.show()


# In[ ]:


var_name= "MSZoning"
col_order = np.sort(final_data[var_name].unique()).tolist()
col_order
plt.figure(figsize=(15,8))
sns.boxplot(x=var_name, y="SalePrice", data=final_data, order=col_order,width=.9,whis=.5)
plt.xlabel("MSZoning", fontsize=12)
plt.ylabel("SalePrice", fontsize=12)
plt.title("Distribution of Saleprice variable with "+var_name, fontsize=15)
plt.show()


# In[ ]:


col_name="Neighborhood"
col_value=np.sort(final_data[col_name].unique()).tolist()
plt.figure(figsize=(16,8))
sns.stripplot(x=col_name,y="SalePrice", data=final_data,order=col_value,linewidth=.6)
plt.xticks(rotation=45)
plt.xlabel("Neighborhood")
plt.ylabel("SalePrice")
plt.title("the plot between neighborhood with salesprice")
plt.show()


# In[ ]:


final_data


# In[ ]:


sns.lmplot(x="YearBuilt", y='SalePrice', hue='Foundation', 
           data=final_data,height=10,
           fit_reg=False)


# Here we can say the following:
# * we can say that upto 1980 we rarely had the prices above $300,000.
# * 1. Now a days the foundation is laid mostly by using PConc.
# * Brktil foundation was widely used back in 1920.
# * cblock foundation was widely used in 1960's.
# 
# 

# In[ ]:


DF_initial_observations(final_data)


# In[ ]:


final_data.shape


# In[ ]:


final_data=pd.get_dummies(final_data, columns=["Neighborhood",],prefix="neighbor",drop_first=True,dtype=int)
final_data.shape


# In[ ]:


final_data["MSZoning"].unique()


# In[ ]:


final_data['MSZoning'] = final_data['MSZoning'].map({'C (all)':0,'RH':3,'RM':4,'FV':6, 'RL':5, 'RP':7}).astype(int)


# In[ ]:


final_data["Street"].unique()


# In[ ]:


final_data['Street'] = final_data["Street"].map({'Grvl':0, 'Pave':1}).astype(int)


# In[ ]:


final_data['LotShape'] = final_data["LotShape"].map({'IR3':0, 'IR2':1, 'IR1':2,'Reg':3}).astype(int)


# In[ ]:


final_data["Utilities"].unique()


# In[ ]:


final_data['LandContour'] = final_data['LandContour'].map({'Low':0, 'Lvl':1, 'Bnk':2, 'HLS':3}).astype(int)


# In[ ]:


final_data['Utilities'] = final_data["Utilities"].map({"NoSeWa":2,"NoSewr":1,"AllPub":3,"ELO":0}).astype(int)


# In[ ]:


DF_initial_observations(final_data)


# In[ ]:


final_data=pd.get_dummies(final_data, columns=["LotConfig","Condition1","Condition2","BldgType","HouseStyle","RoofStyle","RoofMatl","Exterior1st", "Exterior2nd","MasVnrType","Foundation","Heating","Electrical","Functional","GarageType","SaleType","SaleCondition"],drop_first=True,dtype=int)


# In[ ]:


final_data.shape


# In[ ]:


final_data["LandSlope"].unique()


# In[ ]:


final_data["LandSlope"]=final_data["LandSlope"].map({"Gtl":2,"Mod":1,"Sev":0}).astype(int)


# In[ ]:


final_data["ExterQual"].unique()


# In[ ]:


final_data["ExterQual"]=final_data["ExterQual"].map({"Ex":4,"Gd":3,"TA":2,"Fa":1,"Po":0}).astype(int)


# In[ ]:


final_data["ExterCond"]=final_data["ExterCond"].map({"Ex":4,"Gd":3,"TA":2,"Fa":1,"Po":0}).astype(int)


# In[ ]:


final_data["BsmtQual"]=final_data["BsmtQual"].map({"Ex":5,"Gd":4,"TA":3,"Fa":1,"Po":0,"NA":2}).astype(int)
final_data["BsmtCond"]=final_data["BsmtCond"].map({"Ex":5,"Gd":4,"TA":3,"Fa":1,"Po":0,"NA":2}).astype(int)


# In[ ]:


final_data["BsmtExposure"]=final_data["BsmtExposure"].map({"Gd":4,"Av":3,"Mn":1,"No":0,"NA":2}).astype(int)


# In[ ]:


final_data["BsmtExposure"].unique()


# In[ ]:


final_data["BsmtFinType1"]=final_data["BsmtFinType1"].map({"GLQ":6,"ALQ":5,"BLQ":4,"Rec":3,"LwQ":2,"NA":1,"Unf":0}).astype(int)


# In[ ]:


final_data["HeatingQC"]=final_data["HeatingQC"].map({"Ex":4,"Gd":3,"TA":2,"Fa":1,"Po":0}).astype(int)


# In[ ]:


final_data["KitchenQual"]=final_data["KitchenQual"].map({"Ex":4,"Gd":3,"TA":2,"Fa":1,"Po":0}).astype(int)


# In[ ]:


final_data["FireplaceQu"].unique()


# In[ ]:


final_data["FireplaceQu"].isna().sum()


# In[ ]:


final_data["FireplaceQu"].unique()


# In[ ]:


final_data["FireplaceQu"]=final_data["FireplaceQu"].map({"Ex":5,"Gd":4,"TA":3,"Fa":2,"Po":1,"unknown":0}).astype(int)


# In[ ]:


final_data["GarageFinish"].value_counts()


# In[ ]:


final_data["GarageFinish"]=final_data["GarageFinish"].map({"Fin":3,"RFn":2, "Unf":1,"NA":0}).astype(int)


# In[ ]:


final_data["GarageQual"]=final_data["GarageQual"].map({"Ex":5,"Gd":4,"TA":3,"Fa":1,"Po":0,"NA":2}).astype(int)
final_data["GarageCond"]=final_data["GarageCond"].map({"Ex":5,"Gd":4,"TA":3,"Fa":1,"Po":0,"NA":2}).astype(int)


# In[ ]:


final_data.shape


# In[ ]:


DF_initial_observations(final_data)


# In[ ]:


final_data["BsmtFinType2"]=final_data["BsmtFinType2"].map({"GLQ":6,"ALQ":5,"BLQ":4,"Rec":3,"LwQ":2,"NA":1,"Unf":0}).astype(int)


# In[ ]:


final_data["PavedDrive"]=final_data["PavedDrive"].map({"Y":2,"P":1,"N":0}).astype(int)


# In[ ]:


final_data["CentralAir"]=final_data["CentralAir"].map({"Y":1,"N":0}).astype(int)


# Finally I got the shape of my train data as 1348 rows and 191 columns.

# In[ ]:


DF_initial_observations(data_test)


# In[ ]:


data_test.dropna(how="all",subset=["GarageType","GarageYrBlt","GarageFinish","GarageQual","GarageCond"], inplace=True)


# In[ ]:


data_test["FireplaceQu"]=data_test["FireplaceQu"].replace(np.nan,"unknown")


# In[ ]:


data_test=data_test.drop(["Alley"],axis=1)


# In[ ]:


data_test=data_test.drop(["PoolQC","Fence","MiscFeature"],axis=1)


# Firstly I woud like to fill the null values
# * for SaleType Null Value. I considered SaleCondition and Neighborhood.
# * secondly I choosed the Sawyer Neighborhood and SaleCondition to Normal then I took the majority of cases, the saletype andfilled the null.
# here is the code

# In[ ]:


sale_null_table=data_test[["SaleType","Neighborhood","SaleCondition"]]
y=sale_null_table[sale_null_table.isnull().any(axis=1)]
y


# In[ ]:


x=sale_null_table[(sale_null_table["Neighborhood"]=="Sawyer")&(sale_null_table["SaleCondition"]=="Normal")]
z=x["SaleType"].value_counts().index.tolist()
z[0]


# In[ ]:


data_test["SaleType"].unique()


# In[ ]:


data_test["SaleType"]=data_test["SaleType"].replace(np.nan,z[0])


# In[ ]:


data_test["GarageArea"].corr(data_test["GarageCars"])


# In[ ]:


data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="Veenker"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="CollgCr"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="NoRidge"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="Mitchel"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="Somerst"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="OldTown"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="BrkSide"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="Sawyer"]["LotFrontage"]),data_test["LotFrontage"])


# In[ ]:


data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="NridgHt"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="NAmes"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="SawyerW"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="IDOTRR"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="MeadowV"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="Edwards"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="Gilbert"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="Timber"]["LotFrontage"]),data_test["LotFrontage"])
data_test["LotFrontage"]=np.where(data_test["LotFrontage"].isna(),np.nanmedian(data_test[data_test["Neighborhood"]=="StoneBr"]["LotFrontage"]),data_test["LotFrontage"])


# In[ ]:


bsmt_null=data_test["BsmtCond"].value_counts().index.tolist()
data_test["BsmtCond"]=data_test["BsmtCond"].replace(np.nan,bsmt_null[0])
data_test["BsmtCond"].unique()


# In[ ]:


mszone_null=data_test["MSZoning"].value_counts().index.tolist()
data_test["MSZoning"]=data_test["MSZoning"].replace(np.nan,mszone_null[0])
data_test["MSZoning"].unique()


# In[ ]:


bsmth_null=data_test["BsmtHalfBath"].value_counts().index.tolist()
data_test["BsmtHalfBath"]=data_test["BsmtHalfBath"].replace(np.nan,bsmth_null[0])
data_test["BsmtHalfBath"].unique()


# In[ ]:


func_null=data_test["Functional"].value_counts().index.tolist()
data_test["Functional"]=data_test["Functional"].replace(np.nan,func_null[0])
data_test["Functional"].unique()


# In[ ]:


util_null=data_test["Utilities"].value_counts().index.tolist()
data_test["Utilities"]=data_test["Utilities"].replace(np.nan,util_null[0])
data_test["Utilities"].unique()


# In[ ]:


data_test[data_test["GarageYrBlt"].isna()]


# In[ ]:


data_test["GarageCars"].unique()


# In[ ]:


data_test.dropna(how="all",subset=["GarageYrBlt","GarageFinish","GarageQual","GarageCond","GarageCars","GarageArea"],inplace=True)


# In[ ]:


data_test.dropna(how="any",subset=["BsmtQual","BsmtExposure","BsmtFinType1","BsmtFinType2","BsmtHalfBath"],inplace=True)


# In[ ]:


data_test[data_test["MasVnrType"].isna()]


# In[ ]:


masty_null=data_test["MasVnrType"].value_counts().index.tolist()
data_test["MasVnrType"]=data_test["MasVnrType"].replace(np.nan,masty_null[0])
data_test["MasVnrType"].unique()


# In[ ]:


data_test["MasVnrArea"]=data_test["MasVnrArea"].replace(np.nan,data_test["MasVnrArea"].mean())


# In[ ]:


DF_initial_observations(data_test)


# In[ ]:


data_test["GarageFinish"].value_counts()


# In[ ]:


GarF_null=data_test["GarageFinish"].value_counts().index.tolist()
data_test["GarageFinish"]=data_test["GarageFinish"].replace(np.nan,GarF_null[0])
data_test["GarageFinish"].unique()


# In[ ]:


data_test.dropna(how="any",subset=["GarageYrBlt","GarageQual","GarageCond"],inplace=True)


# In[ ]:


data_test['MSZoning'] = data_test['MSZoning'].map({'C (all)':0,'RH':3,'RM':4,'FV':6, 'RL':5, 'RP':7}).astype(int)
data_test['LotShape'] = data_test["LotShape"].map({'IR3':0, 'IR2':1, 'IR1':2,'Reg':3}).astype(int)
data_test['Street'] = data_test["Street"].map({'Grvl':0, 'Pave':1}).astype(int)
data_test['LandContour'] = data_test['LandContour'].map({'Low':0, 'Lvl':1, 'Bnk':2, 'HLS':3}).astype(int)
data_test['Utilities'] = data_test["Utilities"].map({"NoSeWa":2,"NoSewr":1,"AllPub":3,"ELO":0}).astype(int)
data_test["LandSlope"]=data_test["LandSlope"].map({"Gtl":2,"Mod":1,"Sev":0}).astype(int)
data_test["ExterQual"]=data_test["ExterQual"].map({"Ex":4,"Gd":3,"TA":2,"Fa":1,"Po":0}).astype(int)
data_test["BsmtQual"]=data_test["BsmtQual"].map({"Ex":5,"Gd":4,"TA":3,"Fa":1,"Po":0,"NA":2}).astype(int)
data_test["BsmtCond"]=data_test["BsmtCond"].map({"Ex":5,"Gd":4,"TA":3,"Fa":1,"Po":0,"NA":2}).astype(int)
data_test["ExterCond"]=data_test["ExterCond"].map({"Ex":4,"Gd":3,"TA":2,"Fa":1,"Po":0}).astype(int)
data_test["BsmtExposure"]=data_test["BsmtExposure"].map({"Gd":4,"Av":3,"Mn":1,"No":0,"NA":2}).astype(int)


# In[ ]:


kit_null=data_test["KitchenQual"].value_counts().index.tolist()
data_test["KitchenQual"]=data_test["KitchenQual"].replace(np.nan,kit_null[0])


# In[ ]:


bsmt1_null=data_test["BsmtFinType1"].value_counts().index.tolist()
data_test["BsmtFinType1"]=data_test["BsmtFinType1"].replace(np.nan,bsmt1_null[0])


# In[ ]:


heaq_null=data_test["HeatingQC"].value_counts().index.tolist()
data_test["HeatingQC"]=data_test["HeatingQC"].replace(np.nan,heaq_null[0])


# In[ ]:


data_test["KitchenQual"]=data_test["KitchenQual"].map({"Ex":4,"Gd":3,"TA":2,"Fa":1}).astype(int)


# In[ ]:


data_test["HeatingQC"]=data_test["HeatingQC"].map({"Ex":4,"Gd":3,"TA":2,"Fa":1,"Po":0}).astype(int)


# In[ ]:


data_test["BsmtFinType1"]=data_test["BsmtFinType1"].map({"GLQ":6,"ALQ":5,"BLQ":4,"Rec":3,"LwQ":2,"NA":1,"Unf":0}).astype(int)


# In[ ]:


data_test["FireplaceQu"]=data_test["FireplaceQu"].map({"Ex":5,"Gd":4,"TA":3,"Fa":2,"Po":1,"unknown":0}).astype(int)
data_test["GarageFinish"]=data_test["GarageFinish"].map({"Fin":3,"RFn":2, "Unf":1,"NA":0}).astype(int)
data_test["PavedDrive"]=data_test["PavedDrive"].map({"Y":2,"P":1,"N":0}).astype(int)
data_test["BsmtFinType2"]=data_test["BsmtFinType2"].map({"GLQ":6,"ALQ":5,"BLQ":4,"Rec":3,"LwQ":2,"NA":1,"Unf":0}).astype(int)


# In[ ]:


data_test["GarageQual"]=data_test["GarageQual"].map({"Ex":5,"Gd":4,"TA":3,"Fa":1,"Po":0,"NA":2}).astype(int)
data_test["GarageCond"]=data_test["GarageCond"].map({"Ex":5,"Gd":4,"TA":3,"Fa":1,"Po":0,"NA":2}).astype(int)


# In[ ]:


data_test["GarageCond"].unique()


# In[ ]:


data_test=pd.get_dummies(data_test, columns=["LotConfig","Condition1","Condition2","BldgType","HouseStyle","RoofStyle","RoofMatl","Exterior1st", "Exterior2nd","MasVnrType","Foundation","Heating","Electrical","Functional","GarageType","SaleType","SaleCondition"],drop_first=True,dtype=int)


# In[ ]:


data_test=pd.get_dummies(data_test, columns=["Neighborhood",],prefix="neighbor",drop_first=True,dtype=int)
data_test.shape


# In[ ]:


data_test["CentralAir"]=data_test["CentralAir"].map({"Y":1,"N":0}).astype(int)


# In[ ]:


final_data.shape


# In[ ]:


data_test.shape


# **Imbalance in Test and Train Columns**
# We can clearly see that there is an imbalance in the number of columns. We need to balance it.

# In[ ]:


x_final_data=final_data.drop(["SalePrice"],axis=1)
y_final_data=final_data["SalePrice"]
missing_cols = set(x_final_data.columns)-set(data_test.columns)
for c in missing_cols:
    data_test[c]=0
    
    
data_test.shape    


# In[ ]:


x_stand_train_data=x_final_data.copy()
x_stand_test_data=data_test.copy()
numcol=x_stand_train_data.columns


# In[ ]:


from sklearn.preprocessing import MinMaxScaler,StandardScaler
sc=StandardScaler()
standard_x=sc.fit_transform(x_stand_train_data[numcol])
standard_test_x=sc.transform(x_stand_test_data[numcol])
mm=MinMaxScaler()
normal_x=mm.fit_transform(x_stand_train_data[numcol])
normal_test_y=mm.transform(x_stand_test_data[numcol])


# In[ ]:


from sklearn.model_selection import train_test_split
x_train,x_val,y_train,y_val=train_test_split(standard_x,y_final_data,test_size=.20)


# Support Vector Machine is computationally expensive to get the right hyperparameters with GridsearchCV.
# 

# In[ ]:


from sklearn.svm import SVR
svr=SVR(kernel='linear',C=100,epsilon=0.6)
svr.fit(x_train,y_train)
print("train score{:.4f}".format(svr.score(x_train,y_train)))
print("validation score{:.4f} ".format(svr.score(x_val,y_val)))


# In[ ]:


from sklearn import metrics
svr_tr_pred = svr.predict(x_train)
svr_val_pred =svr.predict(x_val)
svr_tr_mse = metrics.mean_squared_error(y_train,svr_tr_pred)
svr_tr_rmse = np.sqrt(svr_tr_mse)
svr_val_mse = metrics.mean_squared_error(y_val, svr_val_pred)
svr_val_rmse = np.sqrt(svr_val_mse)

print('train mse: ', svr_tr_mse)
print('train rmse: ', svr_tr_rmse)

print('val mse: ', svr_val_mse)
print('val rmse: ', svr_val_rmse)


# In[ ]:


svr_test_pred=svr.predict(standard_test_x)
svr_test_pred


# Gradient Boosting Regressor

# In[ ]:


from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error

estimator = [5,7,8,9,10,15,20,25]
max_depth_val= [1,5,6,7,9,10]
learning_rate_val = [0.01,0.1,1,10,100]
max_features_val=[10,60,30,70,100,130]

param_grid_val = dict(n_estimators=estimator, max_depth=max_depth_val, learning_rate=learning_rate_val, max_features=max_features_val)


# In[ ]:


gbr=GradientBoostingRegressor()
gr_gbr=GridSearchCV(estimator=gbr,param_grid=param_grid_val,scoring= "r2",cv=10)
gr_gbr.fit(standard_x,y_final_data)


# In[ ]:


gbr=GradientBoostingRegressor(learning_rate=0.1,max_depth=7,max_features=100,n_estimators=25, random_state=42)
gbr.fit(x_train,y_train)
print("train score{:.4f}".format(gbr.score(x_train,y_train)))
print("validation score{:.4f} ".format(gbr.score(x_val,y_val)))


# In[ ]:


gbr_tr_pred = gbr.predict(x_train)
gbr_val_pred =gbr.predict(x_val)
gbr_tr_mse = metrics.mean_squared_error(y_train,gbr_tr_pred)
gbr_tr_rmse = np.sqrt(gbr_tr_mse)
gbr_val_mse = metrics.mean_squared_error(y_val, gbr_val_pred)
gbr_val_rmse = np.sqrt(gbr_val_mse)

print('train mse: ', gbr_tr_mse)
print('train rmse: ', gbr_tr_rmse)

print('val mse: ', gbr_val_mse)
print('val rmse: ', gbr_val_rmse)


# In[ ]:


gbr_pred=gbr.predict(standard_test_x)
gbr_pred

