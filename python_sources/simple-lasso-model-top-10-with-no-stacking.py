#!/usr/bin/env python
# coding: utf-8

# ## A simple Lasso model model to predict property prices 
# 
# I just wanted to share my first attempt at creating a predictive model in Python. Hopefully, you will find the notebook useful and can adapt it to your own regression projects.
# 
# ### Background on property valuations  
# 
# Before with dive into the data analysis, let's quickly recap how we would derive the value of a property 
# 
# **Property value = property size in sqft $\times$ property cost per sqft  $\times$ adjustments**, 
# 
# which is equivalent to
# 
# **Log (property value) = Log (living area in sqft) + Log(cost per sqft) + $\sum$  Log (adjustments)**
# 
# Thus, a linear model to predict the log of the property might be worth a try ...
# 
# Let's get started!

# In[ ]:


import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold, cross_val_score

train = pd.read_csv("../input/house-prices-advanced-regression-techniques/train.csv")
test = pd.read_csv("../input/house-prices-advanced-regression-techniques/test.csv")

train["Test"]=0
test["Test"]=1
X_all = pd.concat((train, test),sort=True).reset_index(drop=True)
X_all.loc[:,"SalePrice"] = np.log(X_all["SalePrice"])


# ## Preprocssing
# 
# ### Explore and understand the data
# 
# This is the key first step in any data science project. I know that this will take quite some time and effort but it is invaluable. There are excellent dicussions and visualisations in other notebooks - please have look! It will help you to become familiar with the data.  
# 
# ### Missing data
# 
# I decided to simply fill in missing values with the most typical value for each feature. Have a look at some of the other kernels that contain more in-depth explanations for this step. 

# In[ ]:


summary = pd.DataFrame({"Missing":len(X_all)- X_all.count(),"Typical":np.nan})

for col in summary[(summary.Missing > 0)].index: 
    if col == "SalePrice": continue
    colmode=X_all[col].mode()
    summary.loc[col,"Typical"]=colmode[0]
    X_all[col].fillna(colmode[0],inplace=True)

summary[summary.Missing > 0]


# ### Analyse and remove outliers
# 
# As identified in the original paper, the sale price for some of the new homes does not reflect the full market value. Two large and two smaller properties appear to be priced significantly below market value. In addition, there is one property with an abnormally high price. I decided to remove these properties from the train dataset.

# In[ ]:


outliers=[]
train=X_all[X_all.Test==0].copy()
hover=["Id","GrLivArea","OverallCond","MSZoning","YearBuilt","YearRemodAdd","Functional","SaleCondition","SaleType","BldgType","Neighborhood","LotArea"]
train["LogSF"]=np.log(train.GrLivArea)
fig = px.scatter(train[train.SaleType=="New"],y='SalePrice', x='LogSF',color="OverallQual",size="OverallCond",
           hover_data=hover)
fig.show()
outliers+=[524,1299,1325,49,689]


# Now, let's have a look at outliers for the pro-owned homes. A small number of properties are classed as commercial. We will take a deeper look at these to help us confirm the most significant outliers. 

# In[ ]:


fig = px.scatter(train[train.SaleType!="New"],y='SalePrice', x='LogSF',color="MSZoning",size="OverallQual",
           hover_data=hover)
fig.show()

fig = px.scatter(train[(train.MSZoning=="C (all)") & (train.SaleType!="New")],y='SalePrice', x='LogSF',color="SaleCondition",size="OverallQual",
           hover_data=hover,trendline="ols")
fig.show()
outliers+=[496,31,969]


# ## Feature engineering
# 
# As the number of samples is very small in relation to the number of features, I summarised the most relevant categorical features as numerical. This method should also limit the effect of outliers/gaps in the train dataset on the prediction.
# 
# The calibration for the weights in the mapping tables was estimated by fitting a regression model that includes the categorical features - you can find an example of this appraoch at the end of the notebook.

# In[ ]:


functional_map = {"Sal":1,"Sev":0.3,"Maj1":0.1,"Maj2":0.15,"Mod":0.1,"Min1":0.05,"Min2":0.05,"Typ":0} 
quality_map = {"Ex":5,"Gd":4,"TA":3,"Fa":2,"Po":1,"NA":0,0:0}
exposure_map = {"Gd":3,"Av":1,"Mn":0,"No":0,"NA":0}
lotqual_map = {"CulDSac":2,"Inside":0,"Corner":1,"FR2": -1,"FR3":-2}


def feature_eng (X,num_to_categ={},full_data=False):    
     
    # My preference has been to identify a small subset of features that will result in a good fit.
    # However, including all features (set the parameter full_data = True) will slighlty improve 
    # CV & Kaggle scores and the final run for the submission will include all features.
    
    new_columns= ["SF","BaseGood","BaseTA","Age","Pool_Ind","New","SaleCondition_Abn","Res","Pred"]
    for el in new_columns: X.insert(1,el,0)
    
    # Create summary indicators
    
    X.loc[(X.SaleType=="New") & (X.YearBuilt >= X.YrSold-1),"New"]= 1
    X.loc[X.SaleCondition == "Abnorml","SaleCondition_Abn"]=1
    X.loc[(X.PoolArea > 0),"Pool_Ind"]= 1
    
    # Summarise categorical features as numerical
    
    qual_cols = ["ExterQual","ExterCond","BsmtQual","BsmtCond","HeatingQC","KitchenQual","FireplaceQu","GarageQual"]
    for col in qual_cols: X.loc[:,col]= X[col].map(quality_map)
        
    X["LotConfig"]=X["LotConfig"].map(lotqual_map)
    X["Functional"]=X["Functional"].map(functional_map)
    X["Age"]= np.maximum((X["YrSold"]-X["YearBuilt"])/10,0)
    X["QualityScore"]= (X.KitchenQual * 2.5 + X.FireplaceQu *1 + X.GarageQual* 1.5 + X.HeatingQC * 1.5 + 2* X.BsmtQual)/8.5-3
    X["OverallCond"]= (X.OverallCond-5) 
    X["OverallQual"]= (X.OverallQual-5) 
    
    # Adjust total living area for above and below ground living areas based on quality:
    # GrLivArea capures only the above ground surface 
    # whilst some properties include significant good quality below ground living areas
    # First ground living space appears to be valued slightly higher than second ground
    
    X.loc[X.BsmtFinType1.isin({"GLQ","ALQ"}),"BaseGood"]+= X.loc[X.BsmtFinType1.isin({"GLQ","ALQ"}),"BsmtFinSF1"]
    X.loc[X.BsmtFinType1.isin({"BLQ","Rec","LwQ"}),"BaseTA"]+= X.loc[X.BsmtFinType1.isin({"BLQ","Rec","LwQ"}),"BsmtFinSF1"]
    X.loc[X.BsmtFinType2.isin({"GLQ","ALQ"}),"BaseGood"]+= X.loc[X.BsmtFinType2.isin({"GLQ","ALQ"}),"BsmtFinSF2"]
    X.loc[X.BsmtFinType2.isin({"BLQ","Rec","LwQ"}),"BaseTA"]+= X.loc[X.BsmtFinType2.isin({"BLQ","Rec","LwQ"}),"BsmtFinSF2"]
    X["SF"]=  X.GrLivArea - 0.1*X["2ndFlrSF"]+(X.BaseGood*.65+X.BaseTA*0.5)+0.25*X.BsmtUnfSF
    
    # Give additional credit for good exposure of the basement area
    
    X["BsmtExposure"]= X["BsmtExposure"].map(exposure_map)*((X.BaseGood+X.BaseTA)/X.SF)
    
    # Apply log transform to surface areas
    
    X["SFLog"]=np.log(X.SF)
    X["LotArea"]=np.log(X.LotArea) - np.log(X.SF)
    
    
    # Select features to include in the model (for the final run we will include all)
    
    if not full_data:
        X=X[["Res","Pred","SalePrice","Test","Id"] + ["SFLog","Functional","OverallQual","OverallCond",
            "LotArea","GarageCars","MSZoning","Neighborhood","New","Age","BldgType","SaleCondition_Abn",
            "Pool_Ind","BsmtExposure","QualityScore","LotConfig","Condition1"]]
          
    X = pd.get_dummies(X,columns=list(num_to_categ))
    X = pd.get_dummies(X)
    
    # Correct for overfit:
    # I decided to exclude all features where fewer than 5 samples differ from the mode 
    
    for el in set(X.columns).difference({"Test","Pred","Res"}):
        col_mode=X.loc[X.Test==0,el].mode()[0]
        if len(X.loc[(X.Test == 0) & (X[el] !=col_mode),"SFLog"]) < 5: 
                X.drop(columns=el, inplace = True)
                print ("Feature removed:",el)
            
    # Add interaction terms for key features, e.g.
    # overall quality tends to increase with surface area
    # overall condition is related to property age (all new properties are rated 5)
  
    inter_features ={"SFLog","Age","OverallCond","OverallQual","QualityScore","Functional"}.difference(num_to_categ) 
    poly = PolynomialFeatures(interaction_only=True,include_bias=False) 
    inter_cols = poly.fit_transform(X[inter_features])
    X1= pd.DataFrame(inter_cols,columns= poly.get_feature_names(list(inter_features)),index=X.index)                            
    X = pd.concat([X1,X.drop(columns=inter_features)],axis=1)
    
    return X


# ## Modelling
# 
# Let's go ahead and fit our regression model. 

# In[ ]:


def model_fit(model,X,target_col,folds=5):
    
    kf = KFold(folds, shuffle=True, random_state=4991)
    
    drop_cols = ["Test","Id","Pred","Res",target_col]
    X_train = X[X.Test==0].drop(columns=drop_cols)
    y_train = X.loc[X.Test==0,target_col]
    model.fit(X_train,y_train)
    X["Pred"] = model.predict(X.drop(columns=drop_cols))
    X["Res"]= X.Pred-X[target_col]
    
    score =  (-cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv = kf))**0.5
    df = pd.DataFrame({"Coeff":model.coef_,"Y mean":(X_train*model.coef_).mean(),"Y std":(X_train*model.coef_).std()}).sort_values("Y std",ascending=False)
    return X, df, score

X=X_all[~X_all.Id.isin(outliers)].copy()
model = Lasso(alpha=0.0003,random_state=3591,max_iter=100000,fit_intercept=True)

X = feature_eng(X,full_data=False)
X, df, score = model_fit(model,X,"SalePrice")
print("\nCV score: ",score,"\nMean: {:.4f} Std: {:.4f}\n".format(score.mean(), score.std()))
df.head(10)


# The most significant adjustments to property values relate to age, quality and condition of the property, as well as to lot and garage size. 
# 
# This feels all very reasonable. 
# 
# A a final step, we will check the residuals to detect any additional outliers.   

# In[ ]:


hover=["Id","OverallCond","Functional","SaleCondition_Abn","LotArea"]
fig = px.scatter(X,y="Res", x='SFLog',color="OverallQual",size="Age",hover_data=hover)
fig.show()


# I decided to remove properties with residuals greater than +0.4 as the property values for these data points are not explained by the model. 

# In[ ]:


outliers+=[589,633,463,813,1433,411,804]
X=X_all[~X_all.Id.isin(outliers)].copy()
X = feature_eng(X)
X, df, score = model_fit(model,X,"SalePrice")
print("\nModel RMSLE CV score: ",score,"\nMean: {:.4f} Std: {:.4f}\n".format(score.mean(), score.std()))
df.head(10)


# Finally, we re-run the model with all features included. This approach does slightly improve the CV (and submission) score but will be  difficult explain as many of the features are correlated. I am not sure that I would prefer it over the initial model.  

# In[ ]:


model = Lasso(alpha=0.00033,random_state=3591,max_iter=100000,fit_intercept=True)
X=X_all[~X_all.Id.isin(outliers)].copy()
X = feature_eng(X,full_data=True)
X, df, score = model_fit(model,X,"SalePrice")
print("\nModel RMSLE CV score: ",score,"\nMean: {:.4f} Std: {:.4f}\n".format(score.mean(), score.std()))
df.head(10)


# ### Submission

# In[ ]:


sub = pd.DataFrame({"Id":X.loc[X.Test==1,"Id"],"SalePrice":np.exp(X.loc[X.Test==1,"Pred"])})
sub.to_csv('submissionV1.1.csv',index=False)


# ### Conversion of categoricial features - Example
# 
# As promised, let's have a look at the functional deductions to check that the mapping weights are reasonable. 

# In[ ]:


X=X_all[~X_all.Id.isin(outliers)].copy()
X = feature_eng(X,["Functional"])
X, df, score = model_fit(model,X,"SalePrice")
df.loc[["Functional_0.0","Functional_0.05","Functional_0.15","Functional_0.1"],"Coeff"]-df.loc["Functional_0.0","Coeff"]

