#!/usr/bin/env python
# coding: utf-8

# # 1st place (component) kernel
# 
# ### More competitive version of my starter kernel + features
# 
# * https://www.kaggle.com/danofer/wids-2020-starter-catboost-0-902-lb
# * Uses GPU for the catboost, can be disabled
# * V8 : + features, disable model CV, disable GPU , remove hospital and icu id
# 
# * V11 - try running without hospital_count or icu_count (don't know if they add information vs the test set? )  + export enriched data + add 2 features on poerson_hash
# 
# * V12 - more features (some to add):  + Drop ml models used to speed up (Ideally/ToDO - replace with  CV to see if added features contribute)
#     * (normalized) value range : ` (max - min )/(max)`
#     * daily diff median : `d1 ((max + min) /2) / h1(((max + min) /2))`
#     * Is value in first hour the most extreme? (`if min d1 < min h1  OR max d1 > max d1`) 
#     * added feature for (max) presence of any complicator (chronic disease, cancer etc')
#     
# * V13 - feature for how many d1 tests were run total 
#     * also todo : polynomial features ( + feature selection)
#     
# * V16 - add bmi imputation and ranges. tuned features of # tests run per day and hour (nan counts)
# * V17 - changed BMI to replace old values + add flag for different values (i.e cases where BMI was incorrectly calculated) + Added 2 isolation forest features + Added grouped bins of apache 3j diag codes + set it and the the int rounded 3j codes as categorical
# 
# * V18 - add some more count features for categoricals (hospital admit source..) , - based on : https://www.kaggle.com/binaicrai/fork-of-fork-of-wids-lgbm-gs#Visualization 
#     * + made ordinal bmi function be >= 35 , not 34-40.  
#     * changed daily change in value range  feature, removed division/normalizing by daily max
#          df[v+"_tot_change_value_range_normed"]

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from catboost import Pool, cv, CatBoostClassifier, CatBoostRegressor

import shap
shap.initjs()

from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

# import lightgbm as lgb
# from lightgbm import LGBMClassifier

from sklearn.compose import make_column_transformer
from sklearn.preprocessing import RobustScaler , OneHotEncoder , LabelEncoder
from sklearn.ensemble import IsolationForest

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
# pd.set_option('use_inf_as_na', True) ## this makes the fillna very slow!! 
## may be faster to just : df.replace([np.inf, -np.inf], np.nan)


# In[ ]:


def weightedclasst(x):
    """based on : https://www.kaggle.com/c/widsdatathon2020/discussion/127987 but made to use ordinals"""
    if pd.isna(x):
        return np.nan
    if x < 15: return 0 
    elif x >= 15 and x < 16: return 1
    elif x >=16 and x < 18.5: return 2 
    elif x >= 18.5 and x < 25: return 3 
    elif x >= 25 and x < 30: return 4 
    elif x >= 30 and x < 35: return 5 
    elif x >= 35: return 


# ## Load train/test data
# * If doing feature engineering, we could combine the 2 dataframes together then split them after. But we'll go for a naive approach in this kernel

# In[ ]:


TARGET_COL = "hospital_death"


# In[ ]:


df = pd.read_csv("/kaggle/input/widsdatathon2020/training_v2.csv")#.sample(5234)
print(df.shape)
display(df.nunique())
print()

df.head()


# In[ ]:


display(list(df.columns))


# In[ ]:


train, test = train_test_split(df, test_size=0.3)
#test = pd.read_csv("/kaggle/input/widsdatathon2020/unlabeled.csv")
print(test.shape)
display(test.nunique())
test.head()


# # Adversarial validation - hospital_id is disjoint!
# * Run externally - we have perfect seperation on basis of ICU ID or hospital id 
# * For now I add variables to check overlaps
# * validation set should possibly be split by icu_id or hospital id , rather than random . This also affects features we can create
# 
# 
# * There is a small subset of hospital_ids that overlap - ~ 1K rows
# * ICU and hospital ID are synonymous for this purpose
# 

# In[ ]:


df["icu_id_isin_test"] = df['icu_id'].isin(test['icu_id'])
test["icu_id_isin_test"] = True

test["icu_id_isin_train"] = test['icu_id'].isin(df['icu_id'])
df["icu_id_isin_train"] = True


df["hospital_id_isin_test"] = df['hospital_id'].isin(test['hospital_id'])
test["hospital_id_isin_test"] = True

test["hospital_id_isin_train"] = test['hospital_id'].isin(df['hospital_id'])
df["hospital_id_isin_train"] = True


# In[ ]:


# display(pd.concat([df,test])[["hospital_id_isin_train","hospital_id_isin_test","icu_id_isin_train","icu_id_isin_test"]].describe())

test[["hospital_id_isin_train","icu_id_isin_train"]].describe()


# ### concat train and test for easier feature engineering
# * e.g. less rows of code
# * for any predictive imputation (e.g. of apache model death prob)

# In[ ]:


USELESS_COLS = ["patient_id",
                "hospital_id_isin_train","icu_id_isin_train","icu_id_isin_test",
#                 'icu_id'  # doesn't cover test ?  - we still keep hospital ID though - which is as bad - we still want it for a count feature maybe? 
               ] 
# "encounter_id"  is useless (seemingly) for prediction as is patient number (all singletons, no apparent ordering). but we need encounter number for predictions


# In[ ]:


df = pd.concat([train,test])

df.drop(USELESS_COLS,axis=1,inplace=True)
print(df.shape)


# ## Add Features
# 
# * Consider predictive imputation (e.g. of apache model death prob)
# * Consider externally joining ICD code textual descriptions
#     * icd codes are hierarchical - can take prefix. 
#      * the icd codes here (from diag) have surprisingly low cardinality
#      
#      
#  * Consider adding "normalization" of features - e.g. BMI / "healthy" bmi for gender/age group?  , same for other variables - then sum "unhealthy".non normal readings

# In[ ]:


## get medium cardinality columns - possible categoricals +- icd codes ?
cardinal_cols = [c for c in df.columns if( 1<df[c].nunique()<3000)]
cardinal_cols =  [c for c in cardinal_cols if not((c.startswith("h1")) | (c.startswith("d1")))]
print(len(cardinal_cols))
print(cardinal_cols)


# In[ ]:


df[cardinal_cols].nunique()


# * `encounter_id ,	patient_id	` are unique. We could probably drop, but there may be leaks from them so we'll keep (And we need them for the submission)
# * Their being unique means they are not candidates for generating historical features from them per patient. 
#     * We could try the hospital ID or surgery type or apache codes for that purpose

# In[ ]:


## impute BMI and add BMI ranges
df["diff_bmi"] = df['bmi'].copy() # orig BMI values
df['bmi'] = df['weight']/((df['height']/100)**2)
df["diff_bmi"] = df["diff_bmi"]-df['bmi']

6 
#     else: return -1 
                                
df['weightclass'] = df['bmi'].map(weightedclasst)
df['weightclass'].value_counts()


# In[ ]:


display(df[['weightclass',"bmi","diff_bmi"]].describe())


# In[ ]:


## count missing , 0 values per row (very noisy proxy for # tests run/monitored)
df["row_nan_sum"] = df.drop([TARGET_COL,"hospital_id_isin_test"],axis=1).isna().sum(axis=1)
# test["row_nan_sum"] = test.isna().sum(axis=1)

df["row_zero_count"] = (df.drop([TARGET_COL,"hospital_id_isin_test"],axis=1) == 0).sum(axis=1)
# test["row_zero_count"] = (test == 0).sum(axis=1)

## can use death prob as baseline?  - there are missing values, in addition to "-1" - may be also missing value proxy ?  - we'll do joint feature
## -1 seems to be a nan proxy
df['apache_4a_icu_death_prob'] = df['apache_4a_icu_death_prob'].replace(-1,np.nan)
df['apache_4a_hospital_death_prob'] = df['apache_4a_hospital_death_prob'].replace(-1,np.nan)
df["max_apache_4a_death_prob"] = df[['apache_4a_hospital_death_prob', 'apache_4a_icu_death_prob']].max(axis=1)


# ## row level features on lab tests
# * count tests done
# * could do most extreme result (requires standardizing (z-score) or normalizing the mall first). 

# In[ ]:


## count missing values in d1 labs , and h1 labs
d_cols = [c for c in df.columns if(c.startswith("d1"))]
h_cols = [c for c in df.columns if(c.startswith("h1"))]

df["dailyLabs_row_nan_count"] = df[d_cols].isna().sum(axis=1)
df["hourlyLabs_row_nan_count"] = df[h_cols].isna().sum(axis=1)

df["diff_labTestsRun_daily_hourly"] = df["dailyLabs_row_nan_count"] - df["hourlyLabs_row_nan_count"]


# ## Time Series like feature interactions
# 
# * (normalized) value range : ` (max - min )/(max)` OR value range (no normalizing)?
#     * Currently I calc only for daily (d1) variable ranges ,could also do first hour
# * daily diff median : `d1 ((max + min) /2) / h1(((max + min) /2))`
# * Is value in first hour the most extreme? (`if min d1 < min h1  OR max d1 > max d1`) 
# 
# *  what about cases where there's no reading in the first hour, but only in later hours?
#     
# * First we get the names of variables that are relevant so we can apply to all the cols efficiently

# In[ ]:


lab_col = [c for c in df.columns if((c.startswith("h1")) | (c.startswith("d1")))]

# prefix (d1_, h1_) and Suffix (_min, max) removal from String list using map() + lambda 
lab_col_names = list(set(list(map(lambda i: i[ 3 : -4], lab_col))))

print("len lab_col",len(lab_col))
print("len lab_col_names",len(lab_col_names))
print("lab_col_names\n",lab_col_names)

lab_col_names =  ['pao2fio2ratio', 'wbc', 'arterial_ph', 'bilirubin',
  'glucose', 'mbp_noninvasive', 'calcium', 'spo2', 'inr', 'platelets', 'hco3',
  'creatinine', 'sysbp_invasive', 'mbp_invasive', 'resprate', 'temp', 'sysbp',
  'sysbp_noninvasive', 'heartrate', 'sodium', 'diasbp_invasive', 'bun', 'arterial_po2',
  'lactate', 'hematocrit', 'diasbp_noninvasive',
  'mbp', 'albumin', 'arterial_pco2', 'diasbp', 'hemaglobin', 'potassium']


# In[ ]:


df[lab_col].isna().mean()


# In[ ]:


first_h = []
for v in lab_col_names:
    df[v+"_d1_value_range"] = df[f"d1_{v}_max"].subtract(df[f"d1_{v}_min"])
    
    df[v+"_h1_value_range"] = df[f"h1_{v}_max"].subtract(df[f"h1_{v}_min"])
#     df[v+"_h1_value_range_normalized"] = df[f"h1_{v}_max"].subtract(df[f"h1_{v}_min"]).div(df[f"h1_{v}_max"])
    
    # daily change in value range - hour vs day. could do subtract or div here.. 
    df[v+"_tot_change_value_range_normed"] = abs((df[v+"_d1_value_range"].div(df[v+"_h1_value_range"])))#.div(df[f"d1_{v}_max"]))
    
    # Cases where there's no reading in the first hour, but only  later in day ?
    df[v+"_started_after_firstHour"] = ((df[f"h1_{v}_max"].isna()) & (df[f"h1_{v}_min"].isna())) & (~df[f"d1_{v}_max"].isna())
    first_h.append(v+"_started_after_firstHour")
    
    ## Did a reading get more extreme after the first hour. 
    ## This misses cases where the readying is in an unhealthy region and "improves"!!
    df[v+"_day_more_extreme"] = ((df[f"d1_{v}_max"]>df[f"h1_{v}_max"]) | (df[f"d1_{v}_min"]<df[f"h1_{v}_min"]))
    df[v+"_day_more_extreme"].fillna(False)


# In[ ]:


df["total_Tests_started_After_firstHour"] = df[first_h].sum(axis=1)
df["total_Tests_started_After_firstHour"].describe()


# In[ ]:


more_extreme_cols = [c for c in df.columns if(c.endswith("_day_more_extreme"))]

df["total_day_more_extreme"] = df[more_extreme_cols].sum(axis=1)


# In[ ]:


df[first_h].describe()


# ## continue with remaining  features engineering

# In[ ]:


## interaction type features: 
## SB derived features - col interactions
### May consider adding features of h1 / D1 (for each specific variable)

df["d1_resprate_div_mbp_min"] = df["d1_resprate_min"].div(df["d1_mbp_min"])
df["d1_resprate_div_sysbp_min"] = df["d1_resprate_min"].div(df["d1_sysbp_min"])
df["d1_lactate_min_div_diasbp_min"] = df["d1_lactate_min"].div(df["d1_diasbp_min"])
df["d1_heartrate_min_div_d1_sysbp_min"] = df["d1_heartrate_min"].div(df["d1_sysbp_min"])
df["apache_icu_div_apache_hospital"] = df["apache_4a_icu_death_prob"].div(df["apache_4a_hospital_death_prob"])
df["d1_hco3_div"]= df["d1_hco3_max"].div(df["d1_hco3_min"])


df["apache_hospital_minus_apache_icu"] = df["apache_4a_hospital_death_prob"] - df["apache_4a_icu_death_prob"]

df["d1_resprate_times_resprate"] = df["d1_resprate_min"].multiply(df["d1_resprate_max"])

df["left_average_spo2"] = (2*df["d1_spo2_max"] + df["d1_spo2_min"])/3


# ### count type features 
# * Count of a variable. Useful for rare things. 
# * only relevant for categorical type features. 
# 
# * V18 - add hospital encounter (despite it being low cardinalty + clean it

# In[ ]:


## could be done by batch more efficiently with groupby.agg({count"}) - but i'm lazy..
##  size counts NaN values, count does not. 


# df["icu_id_count"] = df.groupby(["icu_id"])["encounter_id"].transform("size")
# df["hospital_id_count"] = df.groupby(['hospital_id'])["encounter_id"].transform("size")

df["apache_2_diagnosis_count"] = df.groupby(["apache_2_diagnosis"])["encounter_id"].transform("size")
df["apache_3j_diagnosis_count"] = df.groupby(["apache_3j_diagnosis"])["encounter_id"].transform("size")

## V18 
df["hospital_admit_source_count"] = df.groupby(["hospital_admit_source"])["encounter_id"].transform("size")
df["apache_3j_bodysystem_count"] = df.groupby(["apache_3j_bodysystem"])["encounter_id"].transform("size")
df["apache_2_bodysystem_count"] = df.groupby(["apache_2_bodysystem"])["encounter_id"].transform("size")


# In[ ]:


# sum of chronic diseases or complicators  - we may want to ignore the cancers/tumors +- immunosuppresasnts cancers or seperate
df["total_chronic"] = df[["aids","cirrhosis", 'diabetes_mellitus', 'hepatic_failure']].sum(axis=1)
df["total_cancer_immuno"] = df[[ 'immunosuppression', 'leukemia', 'lymphoma', 'solid_tumor_with_metastasis']].sum(axis=1)
# df.head(50)[["total_chronic","total_cancer_immuno","aids","cirrhosis", 'diabetes_mellitus', 'hepatic_failure', 'immunosuppression', 'leukemia', 'lymphoma', 'solid_tumor_with_metastasis']].drop_duplicates()

## could also add extreme age/weight for this - 
df["has_complicator"] = df[["aids","cirrhosis", 'diabetes_mellitus', 'hepatic_failure',
                            'immunosuppression', 'leukemia', 'lymphoma', 'solid_tumor_with_metastasis']].max(axis=1)
df[["has_complicator","total_chronic","total_cancer_immuno","has_complicator"]].describe()


# In[ ]:


df["has_complicator"].sum()


# In[ ]:


print(df[['apache_4a_hospital_death_prob', 'apache_4a_icu_death_prob',]].isna().sum())

df[['apache_4a_hospital_death_prob', 'apache_4a_icu_death_prob',"max_apache_4a_death_prob"]].hist();


# In[ ]:


## proxy for identifying patient "clusters" - i.e possibly the same patient across encounters
### take relatively "immutable" patient attributes/demographics +- rounding (e.g. age changes over time, height may be recorded incorrectly)
### unsure how to regard things like cancer.. depends on time scale covered by study (months? years?)
### what about height/weight/BMI ?? 

import math
def myround(x, base=5):
    """https://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python"""   
    if math.isnan(x): return (np.nan) # handle missing values
    else:
        return int(base * round(x/base))

df["rounded_age"] = df['age'].apply(lambda x: myround(x,base=8))
df["rounded_height"] = df['height'].apply(lambda x: myround(x,base=3))

df.head()[['rounded_age', 'rounded_height','age','height']].drop_duplicates()

IDENTIFYING_COLS = ['rounded_age', 'rounded_height',  'ethnicity', 'gender' , "aids", 'diabetes_mellitus']  # , 'solid_tumor_with_metastasis'
## weight , BMI ?  ##  'immunosuppression', 'leukemia', 'lymphoma',


# In[ ]:


## hash these values into a new "id"
df["hash_person_profile"] = df[IDENTIFYING_COLS].apply(lambda x: hash(tuple(x)), axis = 1)

print(df["hash_person_profile"].nunique())
display(df[["hash_person_profile",'rounded_age', 'rounded_height','age','height']].tail(2))

df.drop(['rounded_age', 'rounded_height'],axis=1,inplace=True)


# In[ ]:


df["hash_person_profile_apache_death_risk_mean"] = df.groupby(["hash_person_profile"])["max_apache_4a_death_prob"].transform("mean")

df["hash_person_profile_size"] = df.groupby(["hash_person_profile"])["max_apache_4a_death_prob"].transform("size")


# ### ICD code features ?
#     * Externally - join with textual icd9 code descriptors
#     * Features: get prefix of code -> betetr generalization
#     * count "length" of code - proxy for detail assigned? (This is problematic due to missing values resulting in trailing zeroes - annoying to clean )
#         * There's only a few hundred codes in the data, may not add much to add generalizing features..
#         
#         
#     * TODO: Consider checking raw data - are zeroes being added incorrectly ? 
#     
#     Skipping for now.. 

# In[ ]:


## get integer rounded versions - this risks duplicaiton.. . It's pointless on the diag2 - they're all 3 digit integers (with nans) 
## we use pandas's "Int64" - supports null values!
#http://pandas.pydata.org/pandas-docs/stable/user_guide/integer_na.html

# #  ## pointless - no difference in values ! (but we do get an int instead of f laot - which would mess up joins to icd text desc)
### + plus - messes with catboost - unsupported
# df["apache_2_diagnosis"] = df["apache_2_diagnosis"].astype("Int64")
df["apache_2_diagnosis"] = df["apache_2_diagnosis"].fillna(0)

# df["int_apache_3j_diag"] = df["apache_3j_diagnosis"].fillna(0).astype("Int64")  ## gives error -  cannot safely cast non-equivalent float64 to int64
df["int_apache_3j_diag"] =  df["apache_3j_diagnosis"].fillna(0).astype(str).str.split(".",expand=True)[0].astype(int)

df.tail()[["int_apache_3j_diag","apache_3j_diagnosis","apache_2_diagnosis"]].drop_duplicates()


# In[ ]:


df["apache_2_diagnosis"].describe()


# In[ ]:


df[["int_apache_3j_diag","apache_3j_diagnosis","apache_2_diagnosis"]].nunique()


# In[ ]:


df["apache_3j_diagnosis"].astype(str).apply(len).describe()


# In[ ]:


df.loc[df["apache_2_diagnosis"].astype(str).str.len()<4][["apache_2_diagnosis","apache_3j_diagnosis"]]

## these 0.25 variables look weird... ? 


# #### Add subcode group features
# * based on codebook. Could do same for main code?? 
# * basically prefie groups.
# * can attach text lookup from [external (private for now) dataset of codes](https://www.kaggle.com/danofer/apache-iiij-icu-diagnosis-codes#ANZICS-APD-Data-Dictionary.pdf): https://www.kaggle.com/danofer/apache-iiij-icu-diagnosis-codes#ANZICS-APD-Data-Dictionary.pdf
#     * For Apache III : simple high level - round to nearest 100 , and treat as categorical/ohe. fill na with 0
# 
# * We lack a codebook for the apache 2 codes (and they cover a much smaller range : 100-300 , which is odd). So we don't group for now
# 
# * It is BAD to have 3 columns duplicating the same variable! (we could have it twice maybe , but we are still adding noise with the duplication)

# In[ ]:


df.head(10)[["int_apache_3j_diag","apache_3j_diagnosis","apache_2_diagnosis"]].drop_duplicates()


# In[ ]:


# import math

# df["grouped_apache_3j_diag"] = df['int_apache_3j_diag'].map(math.floor(100))
## round to nearest 100 - second digit
df["grouped_apache_3j_diag"] = df['int_apache_3j_diag'].fillna(0).astype(int).apply(lambda x: round(x,-2))//100

# marke/parse  as categorical


# In[ ]:


df.head(10)[["grouped_apache_3j_diag", "int_apache_3j_diag"]].drop_duplicates()


# In[ ]:


df[["grouped_apache_3j_diag", "int_apache_3j_diag"]].nunique()


# In[ ]:


df = df*1  ## force booleans to be integers


# # Isolation forest anomaly score
# * As a sklearn model - requires missing values to be imputed. And categoricals to be handled ideally
# * this is just a TOY example for this feature - I don't handle the cateogircals for it properly and do naive imputation 
# * the score of the model = probablity of a point being an anomaly

# In[ ]:


#clf = IsolationForest(n_estimators=120, max_samples=1100, max_features=0.9, n_jobs=3,behaviour="new",contamination='auto')
#clf2 = IsolationForest(n_estimators=150, max_samples=600, max_features=1.0, n_jobs=3,behaviour="new", contamination='auto')


# In[ ]:


c_cols = [c for c in df.columns if df[c].dtype =="O"]
print(c_cols)
## manually change for purposes of sklearn friendly encoding
# c_cols = ['ethnicity', 'gender', 'hospital_admit_source', 'icu_admit_source',
# 'icu_stay_type', 'icu_type', 'apache_3j_bodysystem', 'apache_2_bodysystem'] # "grouped_apache_3j_diag"


# In[ ]:


### pd.set_option('use_inf_as_na', True)  - to handle infs 
# X = df._get_numeric_data().drop([TARGET_COL],axis=1).copy()
X = df.drop([TARGET_COL],axis=1).copy()

X.replace([np.inf, -np.inf], np.nan,inplace=True)

for c in c_cols:
    le = LabelEncoder()
    X[c] = le.fit_transform(X[c].astype(str))

X = X.drop(["hash_person_profile","icu_id","hospital_id","hash_person_profile_apache_death_risk_mean"],axis=1,errors="ignore")*1
# X = X.fillna(-1)
# X = X*1  ## force booleans to be integers

X.dropna(thresh = 1000, axis = 1,inplace=True)
print(X.shape)
## https://stackoverflow.com/questions/24458645/label-encoding-across-multiple-columns-in-scikit-learn
# label encode (could also one hot) transform object cols 
# X.dtypes()


# In[ ]:


#%%time
#clf.fit(X.fillna(-1))
#df["isolation_forest_score_1"] = clf.score_samples(X.fillna(-1))


# In[ ]:


#%%time
## additional model, with less missing values (drop cols by threshhold) and alternate imputation (median)

#thresh = len(X) * .5
#X.dropna(thresh = thresh, axis = 1,inplace=True)
#print(X.shape)
#X.fillna(X.median(),inplace=True)
#print("filled")
#clf2.fit(X)
#df["isolation_forest_score_2"] = clf2.score_samples(X)


# In[ ]:


#del(X)


# ## Export semi enriched data

# In[ ]:


#df.drop(["icu_id","hospital_id"],axis=1).loc[~df[TARGET_COL].isna()].to_csv("wids_train_v3.csv.gz",index=False,compression="gzip")
#df.drop(["icu_id","hospital_id"],axis=1).loc[df[TARGET_COL].isna()].to_csv("wids_test_v3.csv.gz",index=False,compression="gzip")


# ### if using cartboost or lgbm, we can define categorical variables
# 
# * catboost hyperparam tuning : https://colab.research.google.com/github/catboost/tutorials/blob/master/python_tutorial.ipynb#scrollTo=nSteluuu_mif
# 
# 
# * We see that many clearly continous numeric variables have relatively low cardinality (e.g. icu sensor readings) - making it tricky to define them automatically. 
# * Categorical columns are not necessarily string columns, could be numerical - e.g. hospital codes.. 
# 

# In[ ]:


print([c for c in df.columns if 7<df[c].nunique()<800])
## 
# categorical_cols = ['hospital_id','apache_3j_bodysystem', 'apache_2_bodysystem',
# "hospital_admit_source","icu_id","ethnicity"]


# In[ ]:


## print non numeric columns : We may need to
## define them as categorical / encode as numeric with label encoder, depending on ml model used
print([c for c in df.columns if (1<df[c].nunique()) & (df[c].dtype != np.number)& (df[c].dtype != int) ])


# In[ ]:


categorical_cols =  [
 'ethnicity', 'gender', 'hospital_admit_source', 'icu_admit_source', 'icu_stay_type', 'icu_type',
                     'apache_3j_bodysystem', 'apache_2_bodysystem',
   # "hash_person_profile",
                     "int_apache_3j_diag",
#     "apache_3j_diagnosis",
#     "apache_2_diagnosis",  # fill na fails on it
  #  "grouped_apache_3j_diag"
                    ]
### 'hospital_id',   - From SB  Isee range features also get value from this. but also, it's a feature that may not generalize to test
### same for icu_id


# ## Build & Tune catboost/GBM models
# * We could make a validation subset for early stopping - allowing us to more easily tune our models hyperparameters
# *  we can go with a defualt model for now - it gets good results ,as we'll see
# 
# * We can run on the GPU, giving a speed boost - to do this modify the kaggle kernel to use the GPU, and in the `fit` parameters set `task_type = "GPU"`
# 
# * Catboost and lgbm have `Pool`/`Dataset` objects, that can be used "internally" by them for some functions, e.g. to efficienctly CV
# 
# 

# In[ ]:


display(df[categorical_cols].dtypes)
display(df[categorical_cols].tail(3))
display(df[categorical_cols].isna().sum())


# * We Fill in empty string for missing  values in the string columns , otherwise catboost will give an error - "CatBoostError: Invalid type for cat_feature: cat_features must be integer or string, real number values and NaN values should be converted to string."
# 

# In[ ]:


df[categorical_cols] = df[categorical_cols].fillna("").astype(str)

# # same transformation for test data
# test[categorical_cols] = test[categorical_cols].fillna("")

df[categorical_cols].isna().sum()


# ## Train model(s)

# In[ ]:


### drop columns we think don't generalize to test at this point 

df.drop(["icu_id","hospital_id"],axis=1,inplace=True,errors="ignore")


# In[ ]:


## useful "hidden" function - df._get_numeric_data()  - returns only numeric columns from a pandas dataframe. Useful for scikit learn models! 

X_train = df.loc[train.index].drop([TARGET_COL],axis=1)
y_train = df.loc[train.index][TARGET_COL].astype(int)

test_target = df.loc[test.index][TARGET_COL].astype(int)
test = df.loc[test.index].drop([TARGET_COL],axis=1)


# In[ ]:


display(df[categorical_cols].dtypes)
df[categorical_cols].tail()


# In[ ]:


## catBoost Pool object
train_pool = Pool(data=X_train,label = y_train,
                  cat_features=categorical_cols,
#                   baseline= X_train["max_apache_4a_death_prob"].fillna(X_train["max_apache_4a_death_prob"].median()) # ['apache_4a_hospital_death_prob', 'apache_4a_icu_death_prob'"],## baseline doesn't work with pool ## remove nans first!!
#                   group_id = X_train['joint_key']
                 )

### OPT/TODO:  do train test split for early stopping then this : 

# eval_pool = Pool(data=X_test,label = y_test,cat_features=categorical_cols,
# #                   baseline= X_train["mean_month_weekend_unit_sales"], ##
# #                   group_id = X_test['joint_key']
#                  )


# ## Train a basic model

# In[ ]:


model_basic = CatBoostClassifier(verbose=False,# task_type="CPU",depth=7,
#                                   iterations=7,
                                 metric_period=4,
                                 )
model_basic.fit(train_pool, plot=True,silent=True )
print(model_basic.get_best_score())


# In[ ]:


model = CatBoostClassifier(verbose=False, task_type="CPU",depth=10, #eval_metric="AUC",
                           iterations=1600,
                           learning_rate=0.06,
                           metric_period=4)#,learning_rate=0.1, task_type="GPU",)
model.fit(X_train,y_train,
                  cat_features=categorical_cols,
                  baseline= (0.2 + X_train["max_apache_4a_death_prob"].fillna(X_train["max_apache_4a_death_prob"].mean())), # remove nans.. 
          plot=True,silent=True)
print(model.get_best_score())


# ### Hyperparameter search
# * After training an actual model - improvements : 
#      * We can do a gridsearch for best hyperparameters, such as learning rate, etc' 
#      * Another improvement: split evaluation set from train , and use it for early stopping + tun
#       * I leave this to the reader :)  
#       
#   * Another hyperparam example with hyperopt / optuna / :  https://github.com/catboost/tutorials/blob/master/python_tutorial.ipynb
#   
#   * Params - https://catboost.ai/docs/concepts/parameter-tuning.html

# In[ ]:


# ### hyperparameter tuning example grid for catboost : 
# grid = {
#     'learning_rate': [0.04],#[0.035, 0.1],
#         'depth': [6, 9],
#         'l2_leaf_reg': [1, 3,7],
#         "iterations": [2000],
# }

# model = CatBoostClassifier(#eval_metric='AUC',
#                            task_type="GPU",
# #     use_best_model=True,
#     early_stopping_rounds=20,)

# ## can also do randomized search - more efficient typically, especially for large search space - `randomized_search`
# grid_search_result = model.grid_search(grid, 
#                                        train_pool,
#                                        plot=True,
#                                        refit = True, #  refit best model on all data
#                                       partition_random_seed=42)

# print(model.get_best_score())

# print("best model params: \n",grid_search_result["params"])


# ## Features importances
# 
# * What are the most important features for predicting death? 
# 
# * We also look also at Shapley values : https://github.com/slundberg/shap
#     * Shap + Catboost tutorial :  https://github.com/slundberg/shap/blob/master/notebooks/tree_explainer/Catboost%20tutorial.ipynb
# 

# In[ ]:


model = model_basic


# In[ ]:


feature_importances = model.get_feature_importance(train_pool)
feature_names = X_train.columns
for score, name in sorted(zip(feature_importances, feature_names), reverse=True):
    if score >= 0.24:
        print('{0}: {1:.2f}'.format(name, score))


# In[ ]:


#explainer = shap.TreeExplainer(model)
#shap_values = explainer.shap_values(train_pool)

# visualize the training set predictions
# SHAP plots for all the data is very slow, so we'll only do it for a sample. Taking the head instead of a random sample is dangerous! 
#shap.force_plot(explainer.expected_value,shap_values[:,:30000], X_train.iloc[:,:30000])


# In[ ]:





# In[ ]:


# # absolute importance to model, without directionality
# shap.summary_plot(shap_values, X_train, plot_type="bar")


# In[ ]:


# summarize the effects of all the features
#shap.summary_plot(shap_values, X_train)


# In[ ]:


# shap.dependence_plot("bmi", shap_values, X_train)


# * As we would expect, age is important. 
# * The top features are precalculated predictors of risk of death (which likely take age into account). 
#     * In our final ensemble model, we dropped the APACHE IV precalculated risk score!
# 
# * We see that there's a difference between hospitals , although it's not an especially clear or linear feature. One explanation may be differences in skill of departments/doctors inside each hospital, with these "latent"/hidden variables interacting with other factors in our dataset

# # Get predictions on test set and export for submission
# 
# * You can "ensemble"/average the predictions from the 2 catboost models as a quick improvement , even if there isn't much diversity added
# 
# * The difference in mean predictions can also be explained by the train data having discrete (0/1) labels, while our predictions are continous (0,1]).

# In[ ]:


test


# In[ ]:


pred1 = model.predict(test,prediction_type='Probability')[:,1]
pred2 = model_basic.predict(test,prediction_type='Probability')[:,1]
test["hospital_death_prob"] = (pred1 + pred2)/2

#print("train target mean",df[TARGET_COL].mean())
#print("predictions target mean",test["hospital_death"].mean())


# In[ ]:


test


# In[ ]:


test[["encounter_id","hospital_death","hospital_death_prob","apache_4a_hospital_death_prob"]].to_csv("solution_for_NRI.csv",index=False)


# ###### Interaction Feature Importance
# * Note: We would ideally do this on the test subset (not used here)
#     * Code source: https://towardsdatascience.com/deep-dive-into-catboost-functionalities-for-model-interpretation-7cdef669aeed

# In[ ]:


# https://gist.github.com/aswalin/595ac73f91c6268f9ca449a4ee05dee1#file-catboost-ipynb
get_ipython().run_line_magic('matplotlib', 'inline')
from catboost import *
import matplotlib.pyplot as plt

fi = model.get_feature_importance(Pool(X_train, label=y_train,cat_features=categorical_cols),type="Interaction")

fi_new = []
for k,item in enumerate(fi):  
    first = X_train.dtypes.index[fi[k][0]]
    second = X_train.dtypes.index[fi[k][1]]
    if first != second:
        fi_new.append([first + "_" + second, fi[k][2]])
        
feature_score = pd.DataFrame(fi_new,columns=['Feature-Pair','Score'])
feature_score = feature_score.sort_values(by='Score', ascending=False, inplace=False, kind='quicksort', na_position='last')
plt.rcParams["figure.figsize"] = (16,7)
ax = feature_score.plot('Feature-Pair', 'Score', kind='bar', color='c')
ax.set_title("Pairwise Feature Importance", fontsize = 14)
ax.set_xlabel("features Pair")
plt.show()


# In[ ]:




