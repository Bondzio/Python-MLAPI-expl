#!/usr/bin/env python
# coding: utf-8

# ### This Docs is Speical for me. It's my first long doc in kernel and train my writing skills! Please enjoy it.
# [Section]  
# 
# 00. Basic Preprocessing
# 01. Normality Test & Indepdence Test
#  - Normality with Kurtosis and Skewness & Correlation Analysis  
#  - Chi-square Indepdence Test of Categorical and Ordinal Variables  
# 02. Imputation & Outliers with Statistical Analysis
#  - Imputation: Diagonse the Type of Missing, then Cure by a fitted way
#  - Outlier Dectection: Bivariate Access to let know the Outlier, then deletion  
# 03. Feature Engineering  
# 04. Cross Validation & Parameter Tuning  
# ---
# ### 1. Basic Preprocessing: Based on Feature Descriptions, Figuring Out Variables 
#     - Convert NA into 'No' categorical values
#     - Guess the Relationship with scheming variables name
#     - Discover a summation relationship    
#     - Unveil the possibility of transformation of time variables
#     - Grouping Num/Cat/Ord variables

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from scipy.stats import skew, kurtosis

df_train = pd.read_csv('../input/train.csv')
#df_train.sample(2)

#0. Delete MiscVal
df_train.drop('MiscVal', axis = 1, inplace = True)
#1. Convert NA into 'No' Categorical values
meaningfulNA = ['Alley', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'FireplaceQu', 
 'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond', 'PoolQC', 'Fence', 'MiscFeature']
df_train[meaningfulNA] = df_train[meaningfulNA].fillna('No')
#df_train[meaningfulNA].isnull().sum()
#print('Step1. Convert NA value as No cateogrical values From Description')

#2. Guess the Relationship with Scheming variables name
#if (df_train.loc[:,'TotalBsmtSF'] == df_train.loc[:,'BsmtFinSF1'] + df_train.loc[:,'BsmtFinSF2'] + df_train.loc[:,'BsmtUnfSF']).sum() == df_train.shape[0]:
    #print('Step2. TotalBsmtSF = BsmtFinSf1 + BsmtFinSf2 + BsmtUnfSF')

#3. Discover Summation Relationship
##df_train['totalFlrSF'] = df_train.loc[:,'1stFlrSF'] + df_train.loc[:,'2ndFlrSF']
#print('Step3. Find the feature "totalFlr", 1stFlrSF + 2ndFlrSF')

#4. Unveil the possibility of transformation of time variables
##df_train['SeasonSold'] = (df_train['YrSold'] % 2000) * 100 + df_train['MoSold']
#print("Step4. Find the time variable 'SeasonSold', YrSold + MoSold")

#5. Complex Categorical/Ordinal/Numerical Variables?
#qualCon = ['ExterQual', 'ExterCond', 'HeatingQC', 'KitchenQual', 'FireplaceQu', 'GarageQual', 'GarageCond', 'PoolQC', 'BsmtQual', 'BsmtCond', 'OverallQual', 'OverallCond']
#compl = ['MSSubClass']
#print("Step5. Extract variables that we don't know Categorical or Ordinal now")
# print(qualCon + compl)

qualCon = ['ExterQual', 'ExterCond', 'HeatingQC', 'KitchenQual', 'FireplaceQu', 'GarageQual', 'GarageCond', 'PoolQC', 'BsmtQual', 'BsmtCond', 'OverallQual', 'OverallCond']
compl = ['MSSubClass']
cat = df_train.select_dtypes(include=['object']).columns.tolist()
cat = set(cat).difference(qualCon + compl)
num = df_train.select_dtypes(exclude=['object']).columns
num = set(num).difference(qualCon + compl)

#Numerical
total = ['LowQualFinSF'] #OverallQual, OverallCond in qualCon
floor = ['TotalBsmtSF', 'BsmtUnfSF', '1stFlrSF', '2ndFlrSF']
room = ['BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd']
rest = ['BsmtFullBath', 'BsmtHalfBath', 'FullBath','HalfBath']
bsmt = ['BsmtFinSF1','BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF']
area = ['GrLivArea', 'LotArea', 'LotFrontage']
garage = ['GarageArea', 'GarageCars', 'GarageYrBlt']
outRoom = ['Fireplaces', 'WoodDeckSF','OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal']
season = ['YearRemodAdd', 'GarageYrBlt', 'YearBuilt']
season2 = ['MoSold', 'YrSold']
#Catgorical
total2 = ['MSSubClass','MSZoning','BldgType','Foundation','HouseStyle']
material = ['RoofStyle', 'RoofMatl',  'MasVnrType', 'Electrical','Exterior1st', 'Exterior2nd']
bsmt2 = ['BsmtExposure', 'BsmtFinType1', 'BsmtFinType2']
area2 = ['LotShape','LotConfig']
garage2 = ['GarageType', 'GarageFinish'] 
outRoom2 = ['Heating', 'CentralAir','Fence', 'MiscFeature']
town2 = ['Neighborhood','LandContour','LandSlope','Condition1', 'Condition2']
system2 = ['Street', 'Alley','PavedDrive',  'Utilities','Functional', 'SaleType', 'SaleCondition']
#Ordinal
total3 = ['OverallQual', 'OverallCond', 'MSSubClass']
material3 = [ 'ExterQual', 'ExterCond']
bsmt3 = ['BsmtQual', 'BsmtCond']
room3 = ['KitchenQual']
garage3 = ['GarageQual', 'GarageCond']
outRoom3 = ['FireplaceQu','HeatingQC', 'PoolQC']
ordVar = total3+material3+bsmt3 + room3 + garage3 + outRoom3


# ### 2. Independence Test with Visualization & Statistical Measurement
# 2.1. Indep_Dep Numerical Test
# - Separte Zero Varialbes and None Zero Variables
# - Find Distorted Variables regard of Normality by Kurtosis & Skewness
# - Correlation Test  **-> Find a direct and strong relationship with Indep **
# - VIF Test  **-> Deep insight of multicolinearity**
# ---
# 
# - Separe Zero variables and None zero variables  
# Since 0 means that there doesn't exsit in that instance. We have to see partially correlation matrix of them.  
# - Find Distorted Variables of Normality 

# In[2]:


overSkew = df_train.loc[:,num].columns[df_train.loc[:,num].skew() > 2.5].values
overKurt = df_train.loc[:,num].columns[df_train.loc[:,num].kurt() > 2.5].values
lowKurt = df_train.loc[:,num].columns[df_train.loc[:,num].kurt() < -2.5].values
if not overSkew.size: print('overSkew: ' ,overSkew) 
else:print('overSkew var exist')
if not overKurt.size: print('overKurt: ' ,overKurt) 
else: print('overKurt var exist')
if not lowKurt.size: print('lowKurt is None + No uniform distribution in Data Sets')
else: print('lowKurt var exist')

overDist = set(overSkew).union(set(overKurt)).union(set(lowKurt))
modNum = set(num) - overDist
zeroNum = df_train.loc[:, overDist].columns[(df_train.loc[:, overDist] == 0).sum() > 100]
overDistN0 = overDist - set(zeroNum)
overDist0 = set(zeroNum)
#print(list(zeroNum))
print('Distorted Variables None Zero ', overDistN0)
print('Distorted Varialbes Lot Zero ',overDist0)


# In[3]:


tmp_train = df_train.loc[:,overDistN0].dropna()
def reject_outliers(data, m=4):
    return data[abs(data - np.mean(data)) < m * np.std(data)]
f, axes = plt.subplots(2, 4, figsize = (12, 6), sharey = False)
colors = sns.color_palette("hls", 8)
for ix, var in enumerate(tmp_train.columns):
    row, col = divmod(ix, 4)
    tmpVar = reject_outliers(tmp_train[var])
    var_label = 'skew: ' + str(round(tmpVar.skew(),2)) + ' kurt: ' + str(round(tmpVar.skew(),2))
    axes[row,col] = sns.distplot(tmpVar,kde = True, ax = axes[row, col], color =colors[ix])
    axes[row, col].set_title(var)
    axes[row, col].set_xlabel(var_label)
plt.suptitle('The Distored Non Zero Variables Distribution +- 4 SD', fontsize = 12)
plt.tight_layout()
plt.subplots_adjust(wspace = 0.5, hspace = 0.5, top = 0.8)
plt.show()
#print(df_train.loc[:,overDistN0].apply(reject_outliers).dropna().apply(lambda x: pd.Series({'kurt': kurtosis(x), 'skew' : skew(x)})).T)
del tmp_train

logLot = np.log1p(df_train['LotArea']).kurt()
rootLot = np.sqrt(df_train['LotArea']).kurt()
cubicLot = np.power(df_train['LotArea'],2).kurt()
minVal = min([logLot, rootLot, cubicLot])
if logLot == minVal:
    best = 'log'
    df_train['LotArea_log'] = np.log1p(df_train['LotArea'])
elif rootLot == minVal:
    best = 'root'
    df_train['LotArea_root'] = np.sqrt(df_train['LotArea'])
elif cubicLot == minVal:
    best = 'cubic'
    df_train['LotArea_cubic'] = np.power(df_train['LotArea'],2)
print('The Most distorted variables is LotArea')
print('For LotArea, the Best TF is ' + best)


# Before Seeing the Analysis, I draw the distribution and got the kurt & skew for the range +- 4 standard deviation. Since if we look all of the values, such a values was so spiled by outliers. I hope to see a major impacts of them.  
# **Find**
# - The Shape of All looked a right skewed. But in statistical measurement, only LotArea has severe kurtosis.
# - the datatype of KitchenABvGr is 'int' and most of the values focused on 1.  
# 
# **Treat**
# - LotArea transformed by the best one among (Log, Root, Cubic)

# In[4]:


tmp_train = df_train.loc[:,overDist0].dropna()
def reject_outliers2(data, m=4):
    data = data[abs(data - np.mean(data)) < m * np.std(data)]
    return data.loc[data != 0]
f, axes = plt.subplots(3, 4, figsize = (12, 9), sharey = False)
colors = sns.color_palette("hls", 12)
dataF = dict()
for ix, var in enumerate(tmp_train.columns):
    row, col = divmod(ix, 4)
    tmpVar = reject_outliers2(tmp_train[var])
    var_label = 'skew:'+ str(round(tmpVar.skew(),2)) + ' kurt: ' + str(round(tmpVar.kurt(),2))
    sns.distplot(tmpVar,kde = True, ax = axes[row, col], color =colors[ix])
    axes[row,col].set_title(var)
    axes[row,col].set_xlabel(var_label)
plt.tight_layout()
plt.subplots_adjust(wspace = 0.5, hspace = 0.5, top = 0.85)
plt.suptitle('The Distored Zero Variables Distribution +- 4 SD', fontsize = 12)
plt.show()

del tmp_train


# **Find**
# - There are no severe distortion on Zero variables
# 
# ---
# #### Correlation Test  
# - Non-zero Case
# - zero Case

# In[5]:


num_none_zero = list(overDistN0) + list(modNum)
for ix, x in enumerate(num_none_zero):
    if x == 'SalePrice':
        salePos = ix
        break
num_none_zero[salePos], num_none_zero[len(num_none_zero) - 1] = num_none_zero[len(num_none_zero) - 1], num_none_zero[salePos]

numCorr = df_train.loc[:,num_none_zero].corr().round(1)
#numCorr = np.tril(numCorr.values, k = -1)
print('numVariables Shape : ', numCorr.shape)

f, ax = plt.subplots(1,1, figsize = (12, 12))
mask = np.zeros_like(numCorr)
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    sns.heatmap(numCorr, annot = True, mask=mask, vmin =0, square=True, linewidths = .5, cmap="YlGnBu", ax = ax,
               cbar_kws = {'shrink' : 0.7})
    ax.set_yticks([])
plt.title("Correlation Matrix", fontsize = 15)
plt.tight_layout()
plt.show()


# **Find**
# - Where we are using is important to SalePrice  
#   (Cor)TotalBsmtSF, 1stFlrSF, GrLivArea, FullBath, GargeCars, GarageArea > 0.5  
#   (Cor)LotArea = 0.3  
# - Kitchen, Beedroom, Bath(except FullBath) was trivial. 

# In[6]:


num_zero = list(overDist0) + ['SalePrice']
part_zero = df_train.loc[:, num_zero]
def zero_Corr(data, yVar):
    indexF = data.columns
    a = None
    for col in indexF:
        tmpVar = data.loc[data[col] != 0, :]
        if a is None:
            a = tmpVar.corr().loc[col,:]
        else:
            a = pd.concat([a, tmpVar.corr().loc[col,:]], axis = 1)
    return a
zeroCorr = zero_Corr(part_zero,  'SalePrice').round(1)
print('numVariables Shape : ', zeroCorr.shape)

f, ax = plt.subplots(1,1, figsize = (12, 12))
mask = np.zeros_like(zeroCorr)
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    sns.heatmap(zeroCorr, annot = True, mask=mask, vmin =0, square=True, linewidths = .5, cmap="Greens", ax = ax,
               cbar_kws = {'shrink' : 0.7})
    ax.set_yticks([])
plt.title("Correlation Matrix", fontsize = 15)
plt.tight_layout()
plt.show()


# **Find**
# - MasVnrArea, BsmtFinSF1 is important.
# - The other variables couldn't give an impact to SalePrice
# ---
#  
# #### VIF Test
# - to Get Deep insight of multicolinearity

# In[7]:


from statsmodels.stats.outliers_influence import variance_inflation_factor 
#https://stats.stackexchange.com/questions/155028/how-to-systematically-remove-collinear-variables-in-python
def calculate_vif_(X, thresh=5.0):
    variables = list(range(X.shape[1]))
    droppedLst = []
    dropped=True
    while dropped:
        dropped=False
        vif = [variance_inflation_factor(X.iloc[:,variables].values, ix) for ix in range(X.iloc[:,variables].shape[1])]

        maxloc = vif.index(max(vif))
        if max(vif) > thresh:
            #print('dropping \'' + X.iloc[:, variables].iloc[:, maxloc].name)
            droppedLst += variables[maxloc],
            del variables[maxloc]
            dropped=True
    #print('Dropped variables: ')
    #print(X.columns[droppedLst].tolist())
    print('Remaining variables:')
    print(X.columns[variables].tolist())
    return X.iloc[:,variables]

missingVar = df_train.columns[df_train.isnull().sum() != 0].tolist()
#print(missingVar)
#I hope these are a resonable reason to exclude them
#- GarageYrBlt has 0.8 correlation with YearBuilt
#- LotFrontage has 0.7-0.8 correlation with LotArea
#- MasVnrArea has lots of zero
#- Except them, they are categorical
part_VIF = set(num) - set(missingVar + ['SalePrice'])
df_VIF = df_train.loc[:, part_VIF].copy()
df_VIF_f = calculate_vif_(df_VIF)
df_VIF_f['SalePrice'] = df_train.loc[:, 'SalePrice']
corr_T = df_VIF_f.corr().round(1)
mask = np.zeros_like(corr_T)
mask[np.triu_indices_from(mask)] = True
plt.figure(figsize = (12,12))
sns.heatmap(corr_T, mask = mask, annot = True, cmap = 'BuGn', linewidth = .7, cbar_kws = {'shrink' : 0.7})
plt.show()


# **Find**
# - (Good)The correlation went to almost zero except the relationship with SalePrice.
# - (Bad) Since the code burtually delete the variable having max VIF value, the popularly known variables such as GrivArea was deleted!
# ---
#   
# ### 2.2. Indep_Dep Categorical Test
# - Boxplot with Indepdent Variables  **-> Find a Meaningful Categorical Variables**
# - Chi-Square with each others   **-> Discover the relationship between variables**
# 

# In[8]:


def boxplotSet(sample, title, col = 3):
    height, left = divmod(len(sample), col)
    if left: height += 1
    f, axes = plt.subplots(height, col, figsize = (12,3*height))
    for ix, var in enumerate(sample):
        r, c = divmod(ix, col)
        sns.boxplot(x = var, y = 'SalePrice', data = df_train, ax = axes[r,c])
        plt.xticks(rotation = 90)
    plt.subplots_adjust(0, 0, 1, 0.9)
    plt.suptitle(title, fontsize = 14)
    plt.show()
import scipy.stats as stats
from collections import defaultdict
def chiTest(dfCat):
    varList = dfCat.columns.tolist()
    posDict = defaultdict(list)
    for ix in range(len(varList)):
        var1 = varList[ix]
        for ix2 in range(ix+1, len(varList)):
            var2 = varList[ix2]
            obsv1 = pd.crosstab(dfCat.loc[:,var1], dfCat.loc[:, var2])
            obsv2 = pd.crosstab(dfCat.loc[:,var1], dfCat.loc[:, var2])
            #obsv1 = pd.crosstab(dfCat.loc[:,var1], dfCat.loc[:, var2], normalize= 'index')#'columns'
            #obsv2 = pd.crosstab(dfCat.loc[:,var1], dfCat.loc[:, var2], normalize= 'columns')#
            _, p1, *_ = stats.chi2_contingency(observed= obsv1)
            _, p2, *_ = stats.chi2_contingency(observed= obsv2)
            
            if p1 < 0.05:
                posDict[var1] += var2,
                #print(var1 + 'is important to ' + var2)
            if p2 < 0.05:
                posDict[var2] += var1,
                #print(var2 + 'is important to ' + var1)
    
    varList = set(varList)
    sd = True
    for x, y in posDict.items():
        if len(y) < len(varList) - 1:
            print(x, 'is independent on ',set(varList).difference(set(y)).difference(set([x])))
            sd = False
    
    if sd: print('Every variables are depedent on each others')
    return posDict


# In[9]:


sample = ['BldgType', 'MSSubClass', 'MasVnrType', 'BsmtExposure', 'Electrical', 'RoofMatl']
boxplotSet(sample, 'Representative Variables of Categorical Var')

#####
useCat = ['MSZoning', 'MasVnrType', 'LotShape', 'GarageFinish', 'CentralAir', 'Neighborhood', 'BsmtExposure', 'LotConfig', 'GarageType']
resDict = chiTest(df_train.loc[:, useCat])


# **Find**  
#   
# 1)Boxplots  
# - One_Biased Variables : BldgType  
# - Many_Baised Variables: MSSubClass, HouseStyle, RoofStyle  
# - Orderd Variables: MSZoning, MasVnrType, LotShape, GarageFinish, CentralAir, Neighborhood  
# - Uniform: BsmtExposure, LotConfig, GarageType  
# - One_Small Variables: Eletrical, BsmtFinType2, Heating, Fence, MiscFeature, Street, Alley, PavedDrive, Utilties, Functional, SaleType, SaleCondition  
# - Many_Small Variables: RoofMatl, Exterior1st, Exterior2nd, BsmtFinType1  
# *X_Biased And Y_Small is simultaneously shown*  
# _Neighborhood include [LandContour, LandSlope, Condition1, Condition2]_  
# _Even though some are ordered, it is hard to say 'Ordinal'._  
# **I think that 'x Biased Variables and y small Variables' cause severe biased prediction. So now I delete it!**  
#   
# 2) Chi Square:  
#   http://hamelg.blogspot.kr/2015/11/python-for-data-analysis-part-25-chi.htmlY  
#  - Based on Chi Independence Test, we can choose a categorical set ['MasVnrTypee', 'LotConfig'] or ['GarageFinsih', 'LotConfig']
# 
# ---
# 3) Indep_Dep Oridnal variables
# - Boxplot with Indepdent Variables  **-> Find a Meaningful Ordinal Variables and a proper order of variables**
# - Chi-Square with each others  **-> DIscover the relationship between varaibles**

# In[10]:


sample = ['OverallQual', 'ExterQual', 'BsmtQual','OverallCond', 'ExterCond', 'BsmtCond']
boxplotSet(sample, 'Representative Variables of Ordinal Var')
useOrd = ['OverallQual', 'ExterQual', 'BsmtQual', 'KitchenQual', 'FireplaceQu']
resDict1 = chiTest(df_train.loc[:, useOrd])


# **Find**  
#   
# 1) Boxplot  
# Linear :OverallQual, ExterQual, BsmtQual, KitchenQual, FireplaceQu  
# QuestionMark: OverallCond, ExterCond, BsmtCond, GarageQual, GarageCond, PoolQC, MSSubClass -> Categorical  
# 2) Chi Square  
# Every varialbes are depdent on each others  
# ---  
# etc1) Converted Ordinal variables  into Categorical  
# OverallCond, GarageQual, GarageCond, PoolQC, MSSubClass  
# All of them include in One_Biased Variables  
# etc2) circleGraph to visualize the dependence 

# ## 3. Imputation and Outliers
# 1) Imputaiton
#    - Find Null Variables
#    - Diagonse the type of Null value (MCAR/MAR) and type of the remedy based on Rules of Thums
#    - Cure the Null Variable, deletion, linear regression model(f), bayesian EM algorithm(not yet)  

# In[11]:


print('Step1. Find Null Varialbes')
print('Null Variables :' ,list(df_train.isnull().sum()[df_train.isnull().sum() != 0].index))
print('Step2. Diagonse the type of Error MCAR/MAR')
(df_train.isnull().sum()[df_train.isnull().sum() != 0]) / df_train.shape[0]


# I delete 'MasVnrType', 'MasVnrARea', 'Eletrical'. By Rules of Thumb2 "Deletions Based on Missing Data", (1)  
#  - Variables with as little as 15 percent missing data are candidates for deletion, but higher levels of missing data (20 -30%) can often be remedies

# In[12]:


df_train.loc[:, ['GarageYrBlt', 'YearBuilt']].corr()['GarageYrBlt']


# I delete since GarageYrBlt has a high correlation 0.82. By Rules of Thumb2, "Deletions Based on Missing Data", (2)  
# - When deleting a variable, ensure that alternative variables, hopefully highly correlated, are available to represent the intent of the orignal variable

# In[13]:


tmp = abs(numCorr.corr()['LotFrontage']).sort_values()
print(tmp.index.tolist()[-4:])
print(tmp.tolist()[-4:])


# I impute LotFrontage by mean imputation & regression method. By Rules of Thumbs3, "Imputation of Missing Data", (2)
# - 10% to 20%, The increased presence of missing data makes the all-available, hot deck case substituion, and regression methods preferred for MCAR data, whereas mdodel-based mehtods are necesary with MAR missing data process  
# 
# ---
# ** Linear Imputation **

# In[14]:


#mean Impute
#df_train.loc[:, 'LotFrontage'] = df_train.loc[:, 'LotFrontage'].fillna(df_train.loc[:, 'LotFrontage'].mean())
#Linear Regression Imputation
from sklearn import linear_model
dfImpute = df_train.loc[:, ['1stFlrSF', 'LotArea', 'LotArea_log', 'LotFrontage']].copy()
testIx = dfImpute.loc[:,'LotFrontage'].isnull()
dfTrain = dfImpute.loc[~testIx, :]
dfTest = dfImpute.loc[testIx, :]
lr = linear_model.LinearRegression()
lr.fit(dfTrain.loc[:, ['1stFlrSF', 'LotArea', 'LotArea_log']], dfTrain.loc[:, 'LotFrontage'])
lrImpute = lr.predict(dfTest.loc[:, ['1stFlrSF', 'LotArea', 'LotArea_log']])
#df_train.loc[testIx:, 'LotFrontage] = lrImpute


# However I can't make sure 100% they are MCAR type. So that I tried to make the model based method, even though the number of houses on the town, having highest probability of missing NA value for LotFrontage, is small 29(15 missing)  
# 
# 
# ### Rules Of Thums in Imputation
# 
# - Rules of Thumb2 "Deletions Based on Missing Data"  
#     - Variables with as little as 15 percent missing data are candidates for deletion, but higher levels of missing data (20 -30%) can often be remedies
#     - When deleting a variable, ensure that alternative variables, hopefully highly correlated, are available to represent the intent of the orignal variable
#     - Always consider performing the anaylsis with and without the deleted cases or variables to identify any marked differneces  
# - Rules of Thumb3 "Imputation of Missing Data"
#     - Under 10%, Any of the imputation methods can be applied when missing data are this low, although the complete case method has been shown to be the least preferred.
#     - 10% to 20%, The increased presence of missing data makes the all-available, hot deck case substituion, and regression methods preferred for MCAR data, whereas mdodel-based mehtods are necesary with MAR missing data process
#     - OVer 20%, If it deemed necessary to impute missing data when the level is over 20 percent, the preferred mehthods are:
#         - The regressiom method for MCAR situations
#         - Model based methods when MAR missing data occur
#   
# *etc1, complete case - delete the sample having NA value on one of the variables  
# etc2, MCAR - Missing completely ar random, that is, the cases with missing data are indistinguishable from cases with complete data  
# etc3, MAR - the missing values of Y depend on X, but not on X, for example, we know'the gender of respondents(X var) and are asking about household income(Y var). We find that the missing data are random for both but occur at a much higher frequency for males than females. We have to remedey the missing data by different way according to the gender.*
# 
# ---
# 
# 2) Outlier
#    - Univariate Methods, (+- 4 sigma)
#    - Bivariate Methods, (Bivaraite Normal Distribution 0.9994% ~ +- 4sigma)
#    - Multivariate Detect with Mahalanobis D Meausre(not yet)

# In[15]:


def checkOutlier(df, m = 4):
    uniOutlier = dict().fromkeys(df.columns, None)
    outSample = abs(df - df.mean()) > 4 * df.std()
    outSum = (abs(df - df.mean()) > 4 * df.std()).sum()
    for key in uniOutlier.keys():
        uniOutlier[key] = set(outSample.index[outSample.loc[:, key]])
    outportion = outSum / df.shape[0]
    print("No outlier: " ,outSum.index[outportion == 0].tolist())
    #print("Outlier Portion")
    #print(outportion[outportion != 0].index.tolist())
    #print(outportion[outportion != 0].values.tolist())
    outportion = outportion[outportion != 0].sort_values()
    outlierLst = outportion.index.tolist()
    return uniOutlier, outlierLst

from collections import Counter
def outlierCounter(outlierDict, exceptionLst = ['SalePrice']):
    inter = Counter()
    name = defaultdict(list)
    coreKey = set(outlierDict.keys()).difference(exceptionLst)
    for key in coreKey:
        value = outlierDict[key]
        for val in value:
            inter[val] += 1
            name[val].append(key)
    res = pd.DataFrame([inter, name], index = ['count', 'variable']).T
    res = res.sort_values('count', ascending = False)
    return res


# In[16]:


uniOutlier, outlierList = checkOutlier(df_train.loc[:, num_none_zero])


# Would you remember KitchenAbvGr just be dense on '1'. It's hard to say normality.

# In[17]:


uniOut = outlierCounter(uniOutlier, ['KitchenAbvGr','SalePrice'])


# - Bivariate Methods, (Bivaraite Normal Distribution 0.9994% ~ +- 4sigma)

# In[18]:


from scipy.stats import multivariate_normal
def bivarCI(dfNum, y = 'SalePrice', outer = 10, z_score = 0.00006, cols = 2):
    
    colNum = dfNum.shape[1]
    row, col = divmod(colNum-1, cols)
    if row == 1 and col == 0: row += 1
    if col != 0: row += 1
    
    
    z_under = z_score * 0.98
    z_upper = z_score * 1.02
    
    biOutlier = dict().fromkeys(dfNum.columns, None)
    f, axes = plt.subplots(row, cols, figsize = (4*cols, 4*row))
    f.suptitle('Bivaraite CI', fontsize = 12)
    for ix, var1 in enumerate(dfNum.columns):
        if var1 == y: break
        r,c = divmod(ix, cols)
        dfPart = dfNum.loc[:, [var1,y]]
        dfPart = dfPart[~dfPart.isnull()].copy()
        dfPart = dfPart.loc[dfPart.loc[:, var1] != 0,:]
        dfPart = (dfPart - dfPart.mean()) / dfPart.std()
        F, X, Y, posProb = bivarConverter(dfPart, outer, z_under, z_upper, N = 700)
        axes[r,c].contourf(X, Y, posProb)
        axes[r,c].scatter(dfPart.loc[:, var1], dfPart.loc[:, y], alpha = 1)
        axes[r,c].set_title('Bivaraite CI ' + var1)
        dfPartProb = F.pdf(dfPart.values)
        outIndex = dfPart.index[dfPartProb < z_score]
        biOutlier[var1] = set(outIndex.tolist())
    f.tight_layout(rect = [0, 0.03, 1, 0.95])
    plt.show()
    
    return biOutlier

def bivarConverter(df, outer, z_under, z_upper, N = 500):
    x_init, y_init = df.min() - outer
    x_end, y_end = df.max() + outer
    X = np.linspace(x_init, x_end, N)
    Y = np.linspace(y_init, y_end, N)
    X, Y = np.meshgrid(X, Y)
    pos = np.empty(X.shape + (2,))
    pos[:,:,0] = X
    pos[:,:,1] = Y
    F = multivariate_normal(mean=df.mean().values, cov=df.corr().values)
    posProb = F.pdf(pos)
    posProb[(z_under < posProb) & (posProb < z_upper)] = 1
    posProb[(z_under > posProb) | (posProb < z_upper)] = 0
    
    
    return F , X, Y, posProb


# In[19]:


biOutlier = bivarCI(df_train.loc[:, num_none_zero], outer = 2, z_score = 0.00006,  cols = 4)


# 'YrSold', 'SalePrice', 'KitchenAbvGr', 'BsmtUnfSF', 'BsmtFullBath', 'Id', 'Fireplace', 'HalfBath' are 100% hard to say bivaraite normal distribution

# In[20]:


biOut = outlierCounter(biOutlier, ['YrSold', 'SalePrice', 'KitchenAbvGr', 'BsmtUnfSF', 'BsmtFullBath', 'Id', 'Fireplace', 'HalfBath'])


# - Intersection of biOut and uniOut

# In[21]:


def mergeTwoOut(uni, bi, cutoff = 1):
    uni = uni.loc[uni.loc[:,'count'] != cutoff,:].copy()
    bi = bi.loc[bi.loc[:,'count'] != cutoff,:].copy()
    interIx = set(uni.index).intersection(bi.index)
    totCnt = uni.loc[interIx,'count'] + bi.loc[interIx,'count']
    totVar = (uni.loc[interIx,'variable'] + bi.loc[interIx, 'variable']).map(set)
    res = pd.concat([totCnt, totVar], axis = 1).sort_values('count', ascending = False)
    return res

interOut = mergeTwoOut(uniOut, biOut)
print(interOut)
print("See the Case Outlier with Red Dot")

f, axes = plt.subplots(1,3, figsize = (12, 4))
f.suptitle('Multivaraite Outlier Dot Graph')
axes[0].scatter(df_train.loc[:,'GrLivArea'], df_train.loc[:, 'SalePrice'])
axes[0].scatter(df_train.ix[1298,'GrLivArea'], df_train.ix[1298, 'SalePrice'], c = 'r', s = 30)
axes[0].set_title('GrLivArea + SalePrice')
axes[1].scatter(df_train.loc[:,'GrLivArea'], df_train.loc[:, 'SalePrice'])
axes[1].scatter(df_train.ix[523,'GrLivArea'], df_train.ix[523, 'SalePrice'], c = 'r', s = 30)
axes[1].set_title('GrLivArea + SalePrice')
axes[2].scatter(df_train.loc[:,'LotArea'], df_train.loc[:, 'SalePrice'])
axes[2].scatter(df_train.ix[706,'LotArea'], df_train.ix[706, 'SalePrice'], c = 'r', s = 30)
axes[2].set_title('LotArea + SalePrice')
f.tight_layout(rect = [0, 0.03, 1, 0.95])
plt.show()


# Undoubtely Delete the RED Point, InterOut!

# In[22]:


df_train = df_train.drop(interOut.index)


# - Multivariate Detect with Mahalanobis D Meausre(will do it)
# 
# 
# ### Rules of Tums in Outlier
# - Rules Of Thumb4 "Outlier Dectection"
#     - Univariate methods : Examine all metric variables to identify unique or extreme obsevations
#         - For small samples (<= 80), outliers typically are defined as cases with standard scores of 2.5 or greater
#         - For larger sample sizes, increa the threshold value of standard scores up to 4
#     - Bivaraite Methods: Focus on the relationships such as the independent vs dependent variables
#         - Use scatterplots with confidence intervals at a specified alpha level
#     - Multivariate methods: Best suited for examing a complete variate, such as the independent variables in regression or the variables in factor analysis
#         - Threshold levels for the D^2/measure should be conservative (.005 or .001), resulting in values of 2.5(small samples) vs 3 or 4 in larger samples
# ---
# 
# ## 4. Feature Enginering
#    1) Numerical Variables 
#    - Cerate new ratios and proportions
#    - Apply standard transformations
#    - Check variables for seasonality and create the model for right period  
# *https://www.analyticsvidhya.com/blog/2013/11/simple-manipulations-extract-data/*

# In[23]:


total = ['LowQualFinSF']
floor = ['1stFlrSF', '2ndFlrSF']
room = ['BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd']
rest = ['BsmtFullBath', 'BsmtHalfBath', 'FullBath','HalfBath']
bsmt = ['BsmtFinSF1','BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF']
area = ['GrLivArea', 'LotArea', 'LotFrontage']
garage = ['GarageArea', 'GarageCars']
season = ['YearRemodAdd', 'GarageYrBlt', 'YearBuilt']
season2 = ['MoSold', 'YrSold']
outRoom = ['Fireplaces', 'WoodDeckSF','OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal']

#New ideas
#0. Mean = OverallQual + OverallCOn
#1. Bath / Area  of Floor and Bsmt
#2. area, I can't think in now
#3. season, Check Remod or Not / Check the GarageYrBlt == YearBuilt
#4. outRoom, exist or Not

#total
df_total = df_train.loc[:, total].copy()
#Floor
df_floor = df_train.loc[:,floor].copy()
df_floor['totalFlrSF'] = df_floor.sum(axis = 1)
df_floor['1stFlrRatio'] = df_floor.loc[:,'1stFlrSF'] / df_floor.loc[:,'totalFlrSF']
df_floor['2ndFlrRatio'] = df_floor.loc[:,'2ndFlrSF'] / df_floor.loc[:,'totalFlrSF']
#rest
## Be careful where no have BsmBath, FullBath -> Dividng by 0
df_rest = df_train.loc[:, rest].copy()
df_rest['BsmtBath'] = df_rest.loc[:,'BsmtFullBath'] + df_rest.loc[:, 'BsmtHalfBath'] * 0.5
df_rest['BsmtFullBathRatio'] = df_rest.loc[:,'BsmtFullBath'] / df_rest['BsmtBath']
df_rest['BsmtHalfBathRatio'] = df_rest.loc[:,'BsmtHalfBath'] / df_rest['BsmtBath']
df_rest['FloorBath'] = df_rest.loc[:,'FullBath'] + df_rest.loc[:, 'HalfBath'] * 0.5
df_rest['FloorFullBathRatio'] = df_rest.loc[:,'FullBath'] / df_rest['FloorBath']
df_rest['FloorHalfBathRatio'] = df_rest.loc[:,'HalfBath'] / df_rest['FloorBath']
df_rest[np.isinf(df_rest)] = 0
#var_ = ['BsmtFullBathRatio', 'BsmtHalfBathRatio']
#var__ = ['FloorFullBathRatio', 'FloorHalfBathRatio']
#for var in var_:
#    df_rest.loc[:, var] = df_rest.loc[:, var].fillna(0)
#for var in var__:
#    df_rest.loc[:, var] = df_rest.loc[:, var].fillna(df_rest.loc[:, var].mean())
#Room
## Be careful where no have BsmBath, FullBath -> Dividng by 0
df_room = df_train.loc[:, room].copy()
df_room['AbvGrSum'] = df_room.sum(axis = 1)
df_room['BedroomAbvGrRatio'] = df_room.loc[:,'BedroomAbvGr'] / df_room.loc[:,'AbvGrSum']
df_room['KitchenAbvGrRatio'] = df_room.loc[:,'KitchenAbvGr'] / df_room.loc[:,'AbvGrSum']
df_room['TotRmsAbvGrdRatio'] = df_room.loc[:,'TotRmsAbvGrd'] / df_room.loc[:,'AbvGrSum']
df_room[np.isinf(df_room)] = 0
#Bsmt
## Be careful where no have BsmBath, FullBath -> Dividng by 0
df_bsmt = df_train.loc[:,bsmt].copy()
df_bsmt.loc[:,'BsmtFinSF1Ratio'] = df_bsmt.loc[:,'BsmtFinSF1'] / df_bsmt.loc[:,'TotalBsmtSF']
df_bsmt.loc[:,'BsmtFinSF2Ratio'] = df_bsmt.loc[:,'BsmtFinSF2'] / df_bsmt.loc[:,'TotalBsmtSF']
df_bsmt.loc[:,'BsmtUnfSFRatio']= df_bsmt.loc[:,'BsmtUnfSF'] / df_bsmt.loc[:,'TotalBsmtSF']
df_bsmt[np.isinf(df_bsmt)] = 0
df_bsmt = df_bsmt.fillna(0)
#area
df_area = df_train.loc[:, area].copy()
df_area.loc[:,'LotFrontage'] = df_area.loc[:,'LotFrontage'].fillna(df_area.loc[:,'LotFrontage'].mean())
#garage
df_garage = df_train.loc[:, garage].copy()
#outRoom
df_outRoom = df_train.loc[:, outRoom].copy()

#Adding
df_add = df_bsmt.loc[:,'TotalBsmtSF'] + df_floor.loc[:, 'totalFlrSF']
df_add.name = 'fullArea'

#Regard of Area, skewed or kurtosis

#Season
#I want to dropoff GarageYrBlt since it has not big difference with YrBuilt
#deletion = 'GarageYrBlt' since it has lots of NA and high correlation with YearBuilt
#New Cat : SeasonRemod, SeasonGarYr
df_season = df_train.loc[:, season].copy()
#df_season = df_season.drop('GarageYrBlt', axis = 1)
df_season['SeasonRemod'] = (df_season.loc[:,'YearRemodAdd'] - df_season.loc[:, 'YearBuilt'])
df_season.loc[df_season['SeasonRemod'] != 0, 'SeasonRemod'] = 1
#Season2
df_season2 = df_train.loc[:, season2].copy()
df_season2['SeasonSold'] = (df_season2['YrSold'] % 2000) * 100 + df_season2['MoSold']

df_Num = pd.concat([df_total, df_floor, df_rest, df_room, df_bsmt, df_area, df_garage,df_outRoom, df_season, df_season2, df_add], axis = 1)
del df_total, df_floor, df_rest, df_room, df_bsmt, df_area, df_garage,df_outRoom, df_season, df_season2, df_add


# 2) Categorical Variables, Get dummies!
# 

# In[24]:


useCat = ['MSZoning','BsmtExposure', 'GarageFinish', 'GarageType', 'MasVnrType', 'LotShape', 'LotConfig', 'CentralAir', 'Neighborhood']
df_Cat = df_train.loc[:, useCat].copy()
df_Cat = pd.get_dummies(df_Cat, prefix = useCat)


# 3) Ordinal Variables, Mapping values according to a correct order
# 

# In[25]:


useOrd = ['OverallQual', 'ExterQual', 'BsmtQual', 'KitchenQual', 'FireplaceQu']
df_Ord = df_train.loc[:, useOrd].copy()
df_Ord.loc[:,'ExterQual'] = df_Ord.loc[:,'ExterQual'].map({'Fa':1, 'TA':2, 'Gd' : 3, 'Ex': 4})
df_Ord.loc[:,'BsmtQual'] = df_Ord.loc[:,'BsmtQual'].map({'No':1, 'Fa':1, 'TA':2, 'Gd' : 3, 'Ex': 4})
df_Ord.loc[:,'KitchenQual'] = df_Ord.loc[:,'KitchenQual'].map({'Fa':1, 'TA':2, 'Gd' : 3, 'Ex': 4})
df_Ord.loc[:,'FireplaceQu'] = df_Ord.loc[:,'FireplaceQu'].map({'No':1, 'Po': 1,'Fa':1, 'TA':2, 'Gd' : 3, 'Ex': 4})


# Further Engineering is possible excpecially between Oridnal and Numerical Variables! And If you find any meaningful relationship, Do it! for example: TotalBsmtSF / BsmtQual

# In[26]:


df_train2 = pd.concat([df_Num, df_Cat,df_Ord], axis = 1)
print("Merging Finished")
if len(df_train2.columns) == len(df_train2.select_dtypes(exclude= ['object']).columns):
    print("All of them converted into numerical!")
else:
    print("Where is still categorical?")
    print(df_train2.select_dtypes(include = ['object']).columns)


# Feature Engineering Success!
# 
# ---
# ## 5. Tune Parameter 
# 
#    ** This is done before Chapter 02. Imputation and Outliers**
#    1) Parameter Tuning of Linear Regression
#     - 5 Fold Cross Validation & alpha
#         -> Ridge Regressoin, alpha = (5, RMSE: 32902), (10, MAE : 19793) in [1, 5, 10, 100]
#         -> Lasso Regression, alpha = (1, RMSE : 33516), (1, MAE : 20296) in [0.1, 0.3, 0.5, 0.7, 0.9, 1]
# 
#     
#     02. Parameter Tuning in GBM
#     - 5 Fold Cross Validation & (n_estimatprs & Tree-specific parameters & subsample & learing rate)
#         -> n_estimators, 5808 **This value gets easily after repeatation of the following procedures**
#         -> max_depth(and num_samples_split), 8
#         -> Tune min_samples_leaf,10
#         -> Tune max_features, 0.5
#         -> Tune subsample, 0.45
#         -> Tune learning rate, 0.3
# 

# In[ ]:


from sklearn import linear_model
from math import sqrt
import lightgbm as lgb
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, mean_absolute_error
from collections import defaultdict


# In[ ]:


def regressionCV(df, dfY, alpha, n_splits, sort):
    kf = KFold(n_splits = n_splits, random_state = 2)
    kf.get_n_splits(df)
    lstRMSE = []
    lstMAE = []
    for ixx, (train_index, test_index) in enumerate(kf.split(df)):
        #print(str(ixx) + 'th Fold Prediction')
        X_train, X_cross = df.iloc[train_index,:], df.iloc[test_index,:]
        y_train, y_cross = dfY.iloc[train_index], dfY.iloc[test_index]
        if sort == 'ridge':
            reg = linear_model.Ridge(alpha = alpha)
        elif sort == 'lasso':
            reg = linear_model.Lasso(alpha = alpha)
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_cross)
        rmse = sqrt(mean_squared_error(y_pred, y_cross))
        mae = mean_absolute_error(y_pred, y_cross)
        lstRMSE += rmse,
        lstMAE += mae,
            
        del reg, X_train, X_cross, y_train, y_cross
    
    meanRMSE = sum(lstRMSE) / n_splits
    meanMAE = sum(lstMAE) / n_splits
    print(sort, ' ', alpha, 'rmse: ', meanRMSE, 'mae: ',meanMAE)
    return [sort, alpha, meanRMSE, meanMAE]

def findAlpha(df, dfY, alphaLst, n_splits = 5, sort = 'ridge'):
    resultLst = []
    for alpha in alphaLst:
        resultLst += regressionCV(df, dfY, alpha, n_splits, sort),
    resultLst = sorted(resultLst, key=lambda x: (x[2], x[3]))
    return resultLst
    


# In[ ]:


def regressionResult(df, dfY):
    df_trainY = df_train.loc[:,'SalePrice'].copy()
    df_trainX = df_train2.copy()
    if df_trainX.isnull().sum().sum() == 0:
        print("Not Null in data")
    else:
        nanIndex = df_trainX.isnull().sum()[df_trainX.isnull().sum() != 0].index
        df_trainX = df_trainX.drop(nanIndex, axis = 1)
        print("Null in ", nanIndex)
    ridgeLst = findAlpha(df_trainX, df_trainY, [1, 5, 10, 100])
    lassoLst = findAlpha(df_trainX, df_trainY, [0.1, 0.3, 0.5, 0.7, 0.9, 1], sort = 'lasso')
    return ridgeLst, lassoLSt


# In[ ]:


#print('Ridge RMSE Min Alpha',sorted([(lst[1], lst[2]) for lst in ridgeLst], key = lambda x: x[1])[0])
#print('Ridge MAE Min Alpha', sorted([(lst[1], lst[3]) for lst in ridgeLst], key = lambda x: x[1])[0])
#print('Lasso RMSE Min Alpha',sorted([(lst[1], lst[2]) for lst in lassoLst], key = lambda x: x[1])[0])
#print('Lasso MAE Min Alpha', sorted([(lst[1], lst[3]) for lst in lassoLst], key = lambda x: x[1])[0])


# Ridge RMSE Min Alpha (5, 32902.72307681233)  
# Ridge MAE Min Alpha (10, 19793.760076860788)  
# Lasso RMSE Min Alpha (1, 33516.78681588221)  
# Lasso MAE Min Alpha (1, 20296.151435088632)  

# In[ ]:


def lightGBM(df, dfY, sort, val, params, num_round = 1000, n_splits = 5):
    #Paramrs
    early_stopping_rounds = 100
    params[sort] = val
    
    kf = KFold(n_splits = n_splits, random_state = 2)
    kf.get_n_splits(df)
    lstRound = []
    lstRMSE = []
    lstMAE = []
    for ixx, (train_index, test_index) in enumerate(kf.split(df)):
        #print(str(ixx) + 'th Fold Prediction')
        X_train, X_cross = df.iloc[train_index,:], df.iloc[test_index,:]
        y_train, y_cross = dfY.iloc[train_index], dfY.iloc[test_index]
    
        dtrain = lgb.Dataset(X_train, label = y_train, silent = True)
        dvalid = lgb.Dataset(X_cross, label = y_cross, silent = True)
        
        mdl = lgb.train(params, train_set = dtrain, num_boost_round = num_round, valid_sets = dvalid,
                early_stopping_rounds = early_stopping_rounds, verbose_eval = None)
        y_pred = mdl.predict(X_cross, num_iteration = mdl.best_iteration)
        rmse = sqrt(mean_squared_error(y_pred, y_cross))
        mae = mean_absolute_error(y_pred, y_cross)
        lstRound.append(mdl.best_iteration)
        lstRMSE += rmse,
        lstMAE += mae,
        del X_train, X_cross, y_train, y_cross, dtrain, dvalid, mdl
    tRound = max(lstRound)
    tRMSE = sum(lstRMSE) / n_splits
    tMAE = sum(lstMAE) / n_splits
    ans = [sort, val, tRMSE, tMAE, tRound]
    
    return ans
    


# In[ ]:


def lightgbmCV(df, dfY, sort, valLst, params, num_round = 1000, n_splits = 5):
    resLst = []
    for val in valLst:
        resLst += lightGBM(df, dfY, sort, val, nparams, num_round, n_splits),
    resLst = sorted(resLst, key = lambda x: x[2])
    print(resLst[0][0], '_', 'val: ', resLst[0][1], 'rmse: ', resLst[0][2], ' mae: ', resLst[0][3], ' ', resLst[0][4])
    return resLst

def getBoostParams(df, dfY, varArray, params, num_round = 10000, n_splits = 5):
    nparams = params.copy()
    depthCV = lightgbmCV(df, dfY, 'max_depth', varArray[0], nparams, num_round, n_splits)
    nparams['max_depth'] = depthCV[0][1]
    leafCV = lightgbmCV(df, dfY, 'min_data_in_leaf', varArray[1], nparams, num_round, n_splits)
    nparams['min_data_in_leaf'] = leafCV[0][1]
    featuremaxCV = lightgbmCV(df, dfY, 'colsample_bytree', varArray[2], nparams, num_round, n_splits)
    nparams['colsample_bytree'] = featuremaxCV[0][1]
    baggingCV = lightgbmCV(df, dfY, 'bagging_fraction', varArray[3], nparams, num_round, n_splits)
    nparams['bagging_fraction'] = baggingCV[0][1]
    learningCV = lightgbmCV(df, dfY, 'learning_rate', varArray[4], nparams, num_round, n_splits)
    nparams['learning_rate'] = learningCV[0][1]
    return nparams


# In[ ]:


#df_trainY = df_train.loc[:,'SalePrice'].copy()
#df_trainX = df_train2.copy()
#params_l2 = {'application' : 'regression','metric' : 'l2', 'boosting' : 'gbdt', 'reg_alpha' : 1, 
#'learning_rate' : 0.5  ,'max_depth' : 7, 'min_data_in_leaf' : 20, 'colsample_bytree': 0.7, 'bagging_fraction' :0.7 }
#params_l1 = {'application' : 'regression_l1','metric' : 'l1', 'boosting' : 'gbdt', 'reg_lambda' : 1, 
# 'learning_rate' : 0.5 ,'max_depth' : 7, 'min_data_in_leaf' : 20 , 'colsample_bytree': 0.7, 'bagging_fraction' :0.7 }
#params_huber = {'application' : 'huber','metric' : 'huber', 'boosting' : 'gbdt', 'reg_alpha' : 1, 
#'learning_rate' : 0.5 ,'max_depth' : 7, 'min_data_in_leaf' : 20 , 'colsample_bytree': 0.7, 'bagging_fraction' : 0.7}

#params_l2 = getBoostParams(df_trainX, df_trainY, varArray = [[3,5,7,9], [10, 20, 50, 100], [0.5, 0.7, 0.9], [0.5, 0.7, 0.9], [0.1, 0.3, 0.5]], params = params_l2)
#params_l2 = getBoostParams(df_trainX, df_trainY, varArray = [[6,7,8], [9, 10, 15], [0.45, 0.5, 0.55], [0.45, 0.5, 0.55], [0.28, 0.3, 0.32]], params = params_l2)


# **1st getBoostParams**  
# max_depth _ val:  7 rmse:  29323.298722332423  mae:  17944.8637161   4517  
# min_data_in_leaf _ val:  10 rmse:  27867.13170054141  mae:  17357.4795697   5209  
# colsample_bytree _ val:  0.5 rmse:  27663.93373367426  mae:  17273.9522368   5460  
# bagging_fraction _ val:  0.5 rmse:  27663.93373367426  mae:  17273.9522368   5460  
# learning_rate _ val:  0.3 rmse:  27609.021642548592  mae:  17162.3710014   5790  
# **2nd getBoostParams**  
# max_depth _ val:  8 rmse:  27474.760390151474  mae:  17178.4440785   5808  
# min_data_in_leaf _ val:  10 rmse:  27474.760390151474  mae:  17178.4440785   5808  
# colsample_bytree _ val:  0.5 rmse:  27474.760390151474  mae:  17178.4440785   5808  
# bagging_fraction _ val:  0.45 rmse:  27474.760390151474  mae:  17178.4440785   5808  
# learning_rate _ val:  0.3 rmse:  27474.760390151474  mae:  17178.4440785   5808  

# Finish!! Thank you for reading this doc!! I wish that you feel nice!

# In[ ]:




