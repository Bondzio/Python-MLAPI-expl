#!/usr/bin/env python
# coding: utf-8

# # Baseball Data
# ## Description
# Major League Baseball Data from the 1986 and 1987 seasons.
# 
# ## Usage
# Hitters
# 
# ## Format
# A data frame with 322 observations of major league players on the following 20 variables.
# 
# - AtBat: Number of times at bat in 1986
# 
# - Hits: Number of hits in 1986
# 
# - HmRun: Number of home runs in 1986
# 
# - Runs: Number of runs in 1986
# 
# - RBI: Number of runs batted in in 1986
# 
# - Walks: Number of walks in 1986
# 
# - Years: Number of years in the major leagues
# 
# - CAtBat: Number of times at bat during his career
# 
# - CHits: Number of hits during his career
# 
# - CHmRun: Number of home runs during his career
# 
# - CRuns: Number of runs during his career
# 
# - CRBI: Number of runs batted in during his career
# 
# - CWalks: Number of walks during his career
# 
# - League: A factor with levels A and N indicating player's league at the end of 1986
# 
# - Division: A factor with levels E and W indicating player's division at the end of 1986
# 
# - PutOuts: Number of put outs in 1986
# 
# - Assists: Number of assists in 1986
# 
# - Errors: Number of errors in 1986
# 
# - Salary: 1987 annual salary on opening day in thousands of dollars
# 
# - NewLeague: A factor with levels A and N indicating player's league at the beginning of 1987
# 
# ## Source
# This dataset was taken from the StatLib library which is maintained at Carnegie Mellon University. This is part of the data that was used in the 1988 ASA Graphics Section Poster Session. The salary data were originally from Sports Illustrated, April 20, 1987. The 1986 and career statistics were obtained from The 1987 Baseball Encyclopedia Update published by Collier Books, Macmillan Publishing Company, New York.
# 
# ## References
# Games, G., Witten, D., Hastie, T., and Tibshirani, R. (2013) An Introduction to Statistical Learning with applications in R, www.StatLearning.com, Springer-Verlag, New York
# 
# ## Examples
# summary(Hitters)
# lm(Salary~AtBat+Hits,data=Hitters)
# --
# Dataset imported from https://www.r-project.org.

# In[ ]:


import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, RidgeCV, ElasticNet, Lasso, LassoCV
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
from sklearn.preprocessing import RobustScaler

Hitters=pd.read_csv("../input/hitters-baseball-data/Hitters.csv")


# # DATA UNDERSTANDING

# Lets take a copy and information about data set.

# In[ ]:


df=Hitters.copy()
df.info()


# Statistical view for all features:

# In[ ]:


df.describe().T


# Observe NaN values and take a head:

# In[ ]:


df[df.isnull().any(axis=1)].head(3)


# Total NaN values numbers:

# In[ ]:


df.isnull().sum().sum()


# See just 'Salary' feature has NaN values. Now, correlation that is what's going between features. How are they strict relation between them. We gave correlation values more than 0.5 between features

# In[ ]:


correlation_matrix = df.corr().round(2)
threshold=0.75
filtre=np.abs(correlation_matrix['Salary']) > 0.50
corr_features=correlation_matrix.columns[filtre].tolist()
sns.clustermap(df[corr_features].corr(),annot=True,fmt=".2f")
plt.title('Correlation btw features')
plt.show()


# Missing values visualization:

# In[ ]:


import missingno as msno
msno.bar(df);


# # DATA PREPROCESSING
# 
# We will consider some options for Missing Values.

# ###  First Option
# This method is drop all NaN values.

# In[ ]:


df1=df.copy()
df1=df1.dropna()
df1.shape


# Then, convert categorical variable into dummy/indicator variables with 'drop_first = True'. This is for Dummy trap.

# In[ ]:


df1=pd.get_dummies(df1,columns = ['League', 'Division', 'NewLeague'], drop_first = True)
df1.head()


# ## Outlier Detection
# 
# Using LOF(Local Outliers Factor) method.

# In[ ]:


clf=LocalOutlierFactor(n_neighbors=20, contamination=0.1)
clf.fit_predict(df1)
df1_scores=clf.negative_outlier_factor_
df1_scores= np.sort(df1_scores)
df1_scores[0:20]


# And show all outliers with boxplot.

# In[ ]:


sns.boxplot(df1_scores);


# Give threshold for LOF.

# In[ ]:


threshold=np.sort(df1_scores)[10]
print(threshold)
df1=df1.loc[df1_scores > threshold]
df1=df1.reset_index(drop=True)


# In[ ]:


df1.shape


# ## Standardization
# 
# This is first option with using drop method.

# In[ ]:


df1_X=df1.drop(["Salary","League_N","Division_W","NewLeague_N"], axis=1)
df1_X.head(2)


# In[ ]:


from sklearn.preprocessing import StandardScaler
scaled_cols=StandardScaler().fit_transform(df1_X)



scaled_cols=pd.DataFrame(scaled_cols, columns=df1_X.columns)
scaled_cols.head()


# In[ ]:


cat_df1=df1.loc[:, "League_N":"NewLeague_N"]
cat_df1.head()


# In[ ]:


Salary=pd.DataFrame(df1["Salary"])
Salary.head()


# Concatination for all prepared data frames:

# In[ ]:


df2=pd.concat([Salary,scaled_cols, cat_df1], axis=1)
df2.head(2)


# In[ ]:


df2.head()


# ### Second Option
# This is second option and method is fill NA values with mean.

# In[ ]:


df5=df.copy()


# In[ ]:


df5.corr()


# Lets take group between 'League','Division', 'Year_lab' features and use 'mean' aggrigation fonksiyon for 'Salary' column.

# In[ ]:


df5['Year_lab'] = pd.cut(x=df['Years'], bins=[0, 3, 6, 10, 15, 19, 24])
df5.groupby(['League','Division', 'Year_lab']).agg({'Salary':'mean'})


# Let's make assignments to NaN values according to the above grouping.

# In[ ]:


df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'E') & (df5['Years'] <= 3), "Salary"] = 112
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'E') & (df5['Years'] > 3) & (df5['Years'] <= 6), "Salary"] = 656
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'E') & (df5['Years'] > 6) & (df5['Years'] <= 10), "Salary"] = 853
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'E') & (df5['Years'] > 10) & (df5['Years'] <= 15), "Salary"] = 816
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'E') & (df5['Years'] > 15) & (df5['Years'] <= 19), "Salary"] = 665

df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'W') & (df5['Years'] <= 3), "Salary"] = 154
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'W') & (df5['Years'] > 3) & (df5['Years'] <= 6), "Salary"] = 401
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'W') & (df5['Years'] > 6) & (df5['Years'] <= 10), "Salary"] = 634
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'W') & (df5['Years'] > 10) & (df5['Years'] <= 15), "Salary"] = 835
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'W') & (df5['Years'] > 15) & (df5['Years'] <= 19), "Salary"] = 479
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "A") & (df5['Division'] == 'W') & (df5['Years'] > 19), "Salary"] = 487

df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'E') & (df5['Years'] <= 3), "Salary"] = 248
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'E') & (df5['Years'] > 3) & (df5['Years'] <= 6), "Salary"] = 501
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'E') & (df5['Years'] > 6) & (df5['Years'] <= 10), "Salary"] = 824
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'E') & (df5['Years'] > 10) & (df5['Years'] <= 15), "Salary"] = 894
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'E') & (df5['Years'] > 15) & (df5['Years'] <= 19), "Salary"] = 662

df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'W') & (df5['Years'] <= 3), "Salary"] = 192
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'W') & (df5['Years'] > 3) & (df5['Years'] <= 6), "Salary"] = 458
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'W') & (df5['Years'] > 6) & (df5['Years'] <= 10), "Salary"] = 563
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'W') & (df5['Years'] > 10) & (df5['Years'] <= 15), "Salary"] = 722
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'W') & (df5['Years'] > 15) & (df5['Years'] <= 19), "Salary"] = 761
df5.loc[(df["Salary"].isnull()) & (df5["League"] == "N") & (df5['Division'] == 'W') & (df5['Years'] > 19), "Salary"] = 475


# In[ ]:


df5.shape


# Now using Label Encoder object then apply 'League', 'Division' and 'NewLeague'.

# In[ ]:


le = LabelEncoder()
df5['League'] = le.fit_transform(df5['League'])
df5['Division'] = le.fit_transform(df5['Division'])
df5['NewLeague'] = le.fit_transform(df5['NewLeague'])


# In[ ]:


df5.head()


# and for 'Year_lab' column also.

# In[ ]:


df5['Year_lab'] = le.fit_transform(df5['Year_lab'])


# In[ ]:


df5.head(2)


# In[ ]:


df5.info()


# ## Normalization
# 
# After standartization lets normalize last features.

# In[ ]:


df5_X= df5.drop(["Salary","League","Division","NewLeague"], axis=1)

scaled_cols5=preprocessing.normalize(df5_X)


scaled_cols5=pd.DataFrame(scaled_cols5, columns=df5_X.columns)
scaled_cols5.head()


# Categorical dataframe:

# In[ ]:


cat_df5=pd.concat([df5.loc[:,"League":"Division"],df5.loc[:,"NewLeague":"Year_lab"]], axis=1)
cat_df5.head()


# Concatination for all prepared data frames:

# In[ ]:


df6= pd.concat([scaled_cols5,cat_df5,df5["Salary"]], axis=1)
df6


# In[ ]:


df6.shape


# ### Third Option
# 
# This is third option for NaN values considiration. Drop NaN values and outliers like first option and log transformation of the features which have multicorrelation above 0.8 between each other.

# In[ ]:


df3= df1.copy()
print(df3.shape)
df3.head(2)


# In[ ]:


# log transform the variables
df3['CRuns'] = np.log(df3['CRuns'])
df3['CHits'] = np.log(df3['CHits'])
df3['CAtBat'] = np.log(df3['CAtBat'])
df3['Years'] = np.log(df3['Years'])
df3['CRBI'] = np.log(df3['CRBI'])
df3['CWalks'] = np.log(df3['CWalks'])


# In[ ]:


df3_X=df3.drop(["Salary","League_N","Division_W","NewLeague_N"], axis=1)
df3_X.head(2)


# In[ ]:


df3_X.shape


# In[ ]:


Rscaler = RobustScaler().fit(df3_X)
scaled_cols3=Rscaler.transform(df3_X)
scaled_cols3=pd.DataFrame(scaled_cols3, columns=df3_X.columns)
scaled_cols3.head()


# Concatination for all prepared data frames:

# In[ ]:


df4=pd.concat([df3_X,df3.loc[:, "League_N": "NewLeague_N"], df3["Salary"]], axis=1)


# In[ ]:


df4.head()


# In[ ]:


scaled_cols3.shape


# In[ ]:


cat_df3=df3.loc[:, "League_N":"NewLeague_N"]
cat_df3.head()


# In[ ]:


df4.head()


# ### Fourth Option
# This is fourth option for NaN values and method with mean.

# In[ ]:


df7=df.copy()


# In[ ]:


# Filled NaN values with mean

df7.loc[(df7["Salary"].isnull()) & (df7["League"] == "A") & (df7['Division'] == 'E'),"Salary"] = 670.849559
df7.loc[(df7["Salary"].isnull()) & (df7["League"] == "A") & (df7['Division'] == 'W'),"Salary"] = 418.593901
df7.loc[(df7["Salary"].isnull()) & (df7["League"] == "N") & (df7['Division'] == 'E'),"Salary"] = 572.348131
df7.loc[(df7["Salary"].isnull()) & (df7["League"] == "N") & (df7['Division'] == 'W'),"Salary"] = 487.259270


# #### Transformation

# In[ ]:


le = LabelEncoder()
df7['League'] = le.fit_transform(df7['League'])
df7['Division'] = le.fit_transform(df7['Division'])
df7['NewLeague'] = le.fit_transform(df7['NewLeague'])


# #### Normalization

# In[ ]:


df7_X= df7.drop(["Salary","League","Division","NewLeague"], axis=1)

scaled_cols7=preprocessing.normalize(df7_X)


scaled_cols7=pd.DataFrame(scaled_cols7, columns=df7_X.columns)


# #### Concatenate

# In[ ]:


cat_df7=pd.concat([df7.loc[:,"League":"Division"],df7["NewLeague"]], axis=1)
cat_df7.head()


# In[ ]:


df8= pd.concat([scaled_cols7,cat_df7,df7["Salary"]], axis=1)
df8.head()


# In[ ]:


df8.shape


# # MODELING
# 
# Let's see different models error accuracy scores according to the DataFrames we created above.

# ## Linear Regression

# In[ ]:


y=df2["Salary"]
X=df2.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


linreg = LinearRegression()
model = linreg.fit(X_train,y_train)
y_pred = model.predict(X_test)
df2_linreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df2_linreg_rmse


# In[ ]:


y=df6["Salary"]
X=df6.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

linreg = LinearRegression()
model = linreg.fit(X_train,y_train)
y_pred = model.predict(X_test)
df6_linreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df6_linreg_rmse


# In[ ]:


y=df4["Salary"]
X=df4.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

linreg = LinearRegression()
model = linreg.fit(X_train,y_train)
y_pred = model.predict(X_test)
df4_linreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df4_linreg_rmse


# In[ ]:


y=df8["Salary"]
X=df8.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

linreg = LinearRegression()
model = linreg.fit(X_train,y_train)
y_pred = model.predict(X_test)
df8_linreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df8_linreg_rmse


# ## Ridge Regression

# In[ ]:


y=df2["Salary"]
X=df2.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


ridreg = Ridge()
model = ridreg.fit(X_train, y_train)
y_pred = model.predict(X_test)
df2_ridreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df2_ridreg_rmse 


# In[ ]:


y=df6["Salary"]
X=df6.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


ridreg = Ridge()
model = ridreg.fit(X_train, y_train)
y_pred = model.predict(X_test)
df6_ridreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df6_ridreg_rmse 


# In[ ]:


y=df4["Salary"]
X=df4.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


ridreg = Ridge()
model = ridreg.fit(X_train, y_train)
y_pred = model.predict(X_test)
df4_ridreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df4_ridreg_rmse 


# In[ ]:


y=df8["Salary"]
X=df8.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


ridreg = Ridge()
model = ridreg.fit(X_train, y_train)
y_pred = model.predict(X_test)
df8_ridreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df8_ridreg_rmse 


# ## Lasso Regression

# In[ ]:


y=df2["Salary"]
X=df2.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


lasreg = Lasso()
model = lasreg.fit(X_train,y_train)
y_pred = model.predict(X_test)
df2_lasreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df2_lasreg_rmse


# In[ ]:


y=df6["Salary"]
X=df6.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


lasreg = Lasso()
model = lasreg.fit(X_train,y_train)
y_pred = model.predict(X_test)
df6_lasreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df6_lasreg_rmse


# In[ ]:


y=df4["Salary"]
X=df4.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


lasreg = Lasso()
model = lasreg.fit(X_train,y_train)
y_pred = model.predict(X_test)
df4_lasreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df4_lasreg_rmse


# In[ ]:


y=df8["Salary"]
X=df8.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


lasreg = Lasso()
model = lasreg.fit(X_train,y_train)
y_pred = model.predict(X_test)
df8_lasreg_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df8_lasreg_rmse


# ## Elastic Net Regression

# In[ ]:


y=df2["Salary"]
X=df2.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


enet = ElasticNet()
model = enet.fit(X_train,y_train)
y_pred = model.predict(X_test)
df2_enet_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df2_enet_rmse


# In[ ]:


y=df6["Salary"]
X=df6.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


enet = ElasticNet()
model = enet.fit(X_train,y_train)
y_pred = model.predict(X_test)
df6_enet_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df6_enet_rmse


# In[ ]:


y=df4["Salary"]
X=df4.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


enet = ElasticNet()
model = enet.fit(X_train,y_train)
y_pred = model.predict(X_test)
df4_enet_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df4_enet_rmse


# In[ ]:


y=df8["Salary"]
X=df8.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


enet = ElasticNet()
model = enet.fit(X_train,y_train)
y_pred = model.predict(X_test)
df8_enet_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df8_enet_rmse


# # MODEL TUNING
# 
# Now, consider with model tunning and get accuracy scores.

# ## Ridge Regression with Model Tuning

# In[ ]:


y=df2["Salary"]
X=df2.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


alpha = [0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]
ridreg_cv = RidgeCV(alphas = alpha, scoring = "neg_mean_squared_error", cv = 10, normalize = True)
ridreg_cv.fit(X_train, y_train)
ridreg_cv.alpha_

#Final Model 
ridreg_tuned = Ridge(alpha = ridreg_cv.alpha_).fit(X_train,y_train)
y_pred = ridreg_tuned.predict(X_test)
df2_ridge_tuned_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df2_ridge_tuned_rmse


# In[ ]:


y=df6["Salary"]
X=df6.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


alpha = [0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]
ridreg_cv = RidgeCV(alphas = alpha, scoring = "neg_mean_squared_error", cv = 10, normalize = True)
ridreg_cv.fit(X_train, y_train)
ridreg_cv.alpha_

#Final Model 
ridreg_tuned = Ridge(alpha = ridreg_cv.alpha_).fit(X_train,y_train)
y_pred = ridreg_tuned.predict(X_test)
df6_ridge_tuned_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df6_ridge_tuned_rmse


# In[ ]:


y=df4["Salary"]
X=df4.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


alpha = [0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]
ridreg_cv = RidgeCV(alphas = alpha, scoring = "neg_mean_squared_error", cv = 10, normalize = True)
ridreg_cv.fit(X_train, y_train)
ridreg_cv.alpha_

#Final Model 
ridreg_tuned = Ridge(alpha = ridreg_cv.alpha_).fit(X_train,y_train)
y_pred = ridreg_tuned.predict(X_test)
df4_ridge_tuned_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df4_ridge_tuned_rmse


# In[ ]:


y=df8["Salary"]
X=df8.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)


alpha = [0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]
ridreg_cv = RidgeCV(alphas = alpha, scoring = "neg_mean_squared_error", cv = 10, normalize = True)
ridreg_cv.fit(X_train, y_train)
ridreg_cv.alpha_

#Final Model 
ridreg_tuned = Ridge(alpha = ridreg_cv.alpha_).fit(X_train,y_train)
y_pred = ridreg_tuned.predict(X_test)
df8_ridge_tuned_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df8_ridge_tuned_rmse


# ## Lasso Regression with Model Tuning

# In[ ]:


y=df2["Salary"]
X=df2.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

alpha = [0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]
lasso_cv = LassoCV(alphas = alpha, cv = 10, normalize = True)
lasso_cv.fit(X_train, y_train)
lasso_cv.alpha_

#Final Model 
lasso_tuned = Lasso(alpha = lasso_cv.alpha_).fit(X_train,y_train)
y_pred = lasso_tuned.predict(X_test)
df2_lasso_tuned_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
df2_lasso_tuned_rmse


# In[ ]:


y=df6["Salary"]
X=df6.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

alpha = [0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]
lasso_cv = LassoCV(alphas = alpha, cv = 10, normalize = True)
lasso_cv.fit(X_train, y_train)
lasso_cv.alpha_

#Final Model 
lasso_tuned = Lasso(alpha = lasso_cv.alpha_).fit(X_train,y_train)
y_pred = lasso_tuned.predict(X_test)
df6_lasso_tuned_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
df6_lasso_tuned_rmse


# In[ ]:


y=df4["Salary"]
X=df4.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

alpha = [0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]
lasso_cv = LassoCV(alphas = alpha, cv = 10, normalize = True)
lasso_cv.fit(X_train, y_train)
lasso_cv.alpha_

#Final Model 
lasso_tuned = Lasso(alpha = lasso_cv.alpha_).fit(X_train,y_train)
y_pred = lasso_tuned.predict(X_test)
df4_lasso_tuned_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
df4_lasso_tuned_rmse


# In[ ]:


y=df8["Salary"]
X=df8.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

alpha = [0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]
lasso_cv = LassoCV(alphas = alpha, cv = 10, normalize = True)
lasso_cv.fit(X_train, y_train)
lasso_cv.alpha_

#Final Model 
lasso_tuned = Lasso(alpha = lasso_cv.alpha_).fit(X_train,y_train)
y_pred = lasso_tuned.predict(X_test)
df8_lasso_tuned_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
df8_lasso_tuned_rmse


# ## Elastic Net Regression with Model Tuning

# In[ ]:


y=df2["Salary"]
X=df2.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

enet_params = {"l1_ratio": [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
              "alpha":[0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]}

enet_model = ElasticNet().fit(X_train,y_train)
enet_cv = GridSearchCV(enet_model, enet_params, cv = 10).fit(X, y)
enet_cv.best_params_

#Final Model 
enet_tuned = ElasticNet(**enet_cv.best_params_).fit(X_train,y_train)
y_pred = enet_tuned.predict(X_test)
df2_enet_tuned_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df2_enet_tuned_rmse 


# In[ ]:


y=df6["Salary"]
X=df6.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

enet_params = {"l1_ratio": [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
              "alpha":[0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]}

enet_model = ElasticNet().fit(X_train,y_train)
enet_cv = GridSearchCV(enet_model, enet_params, cv = 10).fit(X, y)
enet_cv.best_params_

#Final Model 
enet_tuned = ElasticNet(**enet_cv.best_params_).fit(X_train,y_train)
y_pred = enet_tuned.predict(X_test)
df6_enet_tuned_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df6_enet_tuned_rmse 


# In[ ]:


y=df4["Salary"]
X=df4.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

enet_params = {"l1_ratio": [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
              "alpha":[0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]}

enet_model = ElasticNet().fit(X_train,y_train)
enet_cv = GridSearchCV(enet_model, enet_params, cv = 10).fit(X, y)
enet_cv.best_params_

#Final Model 
enet_tuned = ElasticNet(**enet_cv.best_params_).fit(X_train,y_train)
y_pred = enet_tuned.predict(X_test)
df4_enet_tuned_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df4_enet_tuned_rmse 


# In[ ]:


y=df8["Salary"]
X=df8.drop("Salary", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=46)

enet_params = {"l1_ratio": [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
              "alpha":[0.1,0.01,0.001,0.2,0.3,0.5,0.8,0.9,1]}

enet_model = ElasticNet().fit(X_train,y_train)
enet_cv = GridSearchCV(enet_model, enet_params, cv = 10).fit(X, y)
enet_cv.best_params_

#Final Model 
enet_tuned = ElasticNet(**enet_cv.best_params_).fit(X_train,y_train)
y_pred = enet_tuned.predict(X_test)
df8_enet_tuned_rmse = np.sqrt(mean_squared_error(y_test,y_pred))
df8_enet_tuned_rmse 


# Let's put all created models into dataframe shape and watch them.

# In[ ]:


basicsonuc_df = pd.DataFrame({"CONDITIONS":["df2: drop NA and Outliers, normalized","df6: filled with mean, normalized","df4: drop NA and Outliers, log transformed","df8: filled with mean,normalized"],
                              "LINEAR":[df2_linreg_rmse,df6_linreg_rmse,df4_linreg_rmse,df8_linreg_rmse],
                               "RIDGE":[df2_ridreg_rmse,df6_ridreg_rmse,df4_ridreg_rmse,df8_ridreg_rmse],
                              "RIDGE TUNED":[df2_ridge_tuned_rmse,df6_ridge_tuned_rmse,df4_ridge_tuned_rmse,df8_ridge_tuned_rmse],
                              "LASSO":[df2_lasreg_rmse,df6_lasreg_rmse,df4_lasreg_rmse,df8_lasreg_rmse],
                              "LASSO TUNED":[df2_lasso_tuned_rmse,df6_lasso_tuned_rmse,df4_lasso_tuned_rmse,df8_lasso_tuned_rmse],                              
                              "ELASTIC NET":[df2_enet_rmse,df6_enet_rmse,df4_enet_rmse,df8_enet_rmse],
                              "ELASTIC NET TUNED":[df2_enet_tuned_rmse,df6_enet_tuned_rmse,df4_enet_tuned_rmse,df8_enet_tuned_rmse]
                              })

basicsonuc_df


# # REPORTING
# 
# The aim of this study is to set up linear regression models for the Hitters data set and minimize error scores in 4 data sets that have undergone different preprocessing. 
# 
# The studies conducted are as follows:
# 
# #### ** 1) ** Hitters Data Set was read.
# #### ** 2) ** With Exploratory Data Analysis:
# * Structural information of the dataset was checked.
# * Types of variables in data set were examined.
# * The size information of the data set has been accessed.
# * The number of missing observations from which variable in the data set was accessed. It was observed that there were 59 missing observations only in "Salary" which was dependent variable.
# * Descriptive statistics of the data set were examined.
# 
# #### ** 3) ** In Data PreProcessing:
# * ** For df2: ** NaN values are dropped, Outliers are detected by LOF and dropped. Dummy variables were created. The X variables were normalized.
# * ** For df6: ** NaN values were filled by looking at "Salary" averages in age, league and division variables, Dummy variables were created. The X variables were normalized.
# * ** For df4: ** NaN values and outlier detected by LOF were dropped, log transformation was applied to variables with more than 80% correlation. Dummy variables were created. All x variables were brought to the same range as Robust scaler.
# * ** For df8: ** NaN values were filled by looking at "Salary" averages in league and division variables, Dummy variables were created. The X variables were normalized.
# 
# #### ** 4) ** During the Model Building phase:
# 
# Using the Linear, Ridge, Lasso, ElasticNet machine learning models, ** RMSE ** values representing the difference between actual values and predicted values were calculated. Later, hyperparameter optimizations were applied for Ridge, Lasso and ElasticNet to further reduce the error value.
# 

# ## Conclusion
# 
# When the model created as a result of Elastic Net Hyperparameter optimization was applied to the df6 Data Frame, the lowest RMSE was obtained. (283)
# 
# #### Note: 
# - After this notebook, my aim is to prepare 'kernel' which is 'not clear' data set.
# 
# - If you have any suggestions, please could you write for me? I wil be happy for comment and critics!
# 
#  Thank you for your suggestion and votes ;) 

# In[ ]:




