#!/usr/bin/env python
# coding: utf-8

# # Student Test Scores Analysis - Linear Regression

# The following analysis is performed on a generated data structure of hypothetical student test scores and the student's various characteristics. 
# 
# The analysis includes an exploratory data analysis, regression modeling, and assumption checks.
# 
# Much of the modeling code was sourced from the following article: https://towardsdatascience.com/verifying-the-assumptions-of-linear-regression-in-python-and-r-f4cd2907d4c0

# **Load Libraries**

# In[ ]:


import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np


# # Environment Set Up

# **Load Data**

# In[ ]:


df = pd.read_csv('../input/students-performance-in-exams/StudentsPerformance.csv')


# **Data Overview**

# In[ ]:


df.shape


# In[ ]:


df.columns


# In[ ]:


df.info()


# In[ ]:


df.describe()


# In[ ]:


df.head()


# # Data Cleaning

# **Check for nulls**

# In[ ]:


df.isnull().sum()


# Awesome, no nulls

# **Rename Columns**

# In[ ]:


df.rename(columns = {'race/ethnicity':'race'}, inplace = True)
df.rename(columns = {'parental level of education':'parent_education'}, inplace = True)
df.rename(columns = {'test preparation course':'prep_course'}, inplace = True)
df.rename(columns = {'math score':'math_score'}, inplace = True)
df.rename(columns = {'reading score':'reading_score'}, inplace = True)
df.rename(columns = {'writing score':'writing_score'}, inplace = True)


# **Create a total_score column**

# In[ ]:


df['total_score'] = df['math_score'] + df['reading_score'] + df['writing_score']


# Check the column now

# In[ ]:


df.columns


# # Data Exploration - Visualization

# **Load Libaries**

# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt


# **Variable Distributions**

# In[ ]:


plt.figure(figsize = (6,8))
sns.set(style = 'darkgrid', font = 'sans-serif', font_scale = 1.25, palette = 'Set2')
ax = sns.countplot(
    x = 'gender',
    data = df,
    edgecolor = 'black')
ax.set_title('Distribution of Student Genders', fontsize = 15)
ax.set(xlabel = 'Gender', ylabel = 'Frequency')


# In[ ]:


plt.figure(figsize = (9,6))
sns.set(style = 'darkgrid', font = 'sans-serif', font_scale = 1.25, palette = 'deep')
ax = sns.countplot(
    x = 'race',
    data = df,
    edgecolor = 'black')
ax.set_title('Distribution of Student Race/Ethnicity', fontsize = 15)
ax.set(xlabel = 'Race/Ethnicity', ylabel = 'Frequency')


# In[ ]:


plt.figure(figsize = (13,6))
sns.set(style = 'darkgrid', font = 'sans-serif', font_scale = 1.25, palette = 'deep')
ax = sns.countplot(
    x = 'parent_education',
    data = df,
    edgecolor = 'black')
ax.set_title('Distribution of Parent Education Level', fontsize = 20)
ax.set(xlabel = 'Parental Education Level', ylabel = 'Frequency')


# In[ ]:


plt.figure(figsize = (6,8))
sns.set(style = 'darkgrid', font = 'sans-serif', font_scale = 1.25, palette = 'deep')
ax = sns.countplot(
    x = 'lunch',
    data = df,
    edgecolor = 'black')
ax.set_title('Distribution of Lunch Options', fontsize = 15)
ax.set(xlabel = 'Lunch Option', ylabel = 'Frequency')


# In[ ]:


plt.figure(figsize = (6,8))
sns.set(style = 'darkgrid', font = 'sans-serif', font_scale = 1.25, palette = 'deep')
ax = sns.countplot(
    x = 'prep_course',
    data = df,
    edgecolor = 'black')
ax.set_title('Distribution of Prep Course', fontsize = 15)
ax.set(xlabel = 'Prep Course', ylabel = 'Frequency')


# In[ ]:


sns.set(style = 'darkgrid', font = 'sans-serif', font_scale = 1.25)
plt.figure(figsize = (10,6))
plt.hist(df['math_score'], bins = 20, color = 'cornflowerblue')
plt.xlabel('Math Score', fontsize = 13)
plt.ylabel('Frequency', fontsize = 13)
plt.title('Distribution of Math Scores', fontsize = 13)
plt.show()


# In[ ]:


sns.set(style = 'darkgrid', font = 'sans-serif', font_scale = 1.25)
plt.figure(figsize = (10,6))
plt.hist(df['reading_score'], bins = 20, color = 'lightcoral')
plt.xlabel('Reading Score', fontsize = 13)
plt.ylabel('Frequency', fontsize = 13)
plt.title('Distribution of Reading Scores', fontsize = 13)
plt.show()


# In[ ]:


sns.set(style = 'darkgrid', font = 'sans-serif', font_scale = 1.25)
plt.figure(figsize = (10,6))
plt.hist(df['writing_score'], bins = 20, color = 'goldenrod')
plt.xlabel('Writing Score', fontsize = 13)
plt.ylabel('Frequency', fontsize = 13)
plt.title('Distribution of Writing Score', fontsize = 13)
plt.show()


# In[ ]:


sns.set(style = 'darkgrid', font = 'sans-serif', font_scale = 1.25)
plt.figure(figsize = (10,6))
plt.hist(df['total_score'], bins = 20, color = 'darkorchid')
plt.xlabel('Total Score', fontsize = 13)
plt.ylabel('Frequency', fontsize = 13)
plt.title('Distribution of Total Score', fontsize = 13)
plt.show()


# # Modeling - Linear Regression

# **Setting up**

# In[ ]:


df1 = df[['gender', 'race', 'parent_education', 'prep_course', 'lunch']]
X = pd.get_dummies(df1, columns = ['gender', 'race', 'parent_education', 'prep_course', 'lunch'], dtype = int)
y = df['total_score']


# **Model**

# In[ ]:


from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

X_constant = sm.add_constant(X)
lin_reg = sm.OLS(y, X_constant).fit()
lin_reg.summary()


# # Checking Assumptions

# In[ ]:


import statsmodels.stats.api as sms
sns.set_style('darkgrid')
sns.mpl.rcParams['figure.figsize'] = (15.0, 9.0)


# **Assumption Check: Linearity**

# Y (response variable) is assumed to be a linear function of the features. We will inspect plots of observed vs predicted values AND residuals vs predicted values. We hope to find a linear plot for the former and a horizontal line for the latter.

# In[ ]:


def linearity_test(model, y):
    fitted_vals = model.predict()
    resids = model.resid
    
    fig, ax = plt.subplots(1,2)
    
    sns.regplot(x = fitted_vals, y = y, lowess = True, ax = ax[0], line_kws = {'color': 'red'})
    ax[0].set_title('Observed vs. Predicted Values', fontsize = 16)
    ax[0].set(xlabel = 'Predicted', ylabel = 'Observed')
    
    sns.regplot(x = fitted_vals, y = resids, lowess = True, ax = ax[1], line_kws = {'color' : 'red'})
    ax[1].set_title('Residuals vs. Predicted Values', fontsize = 16)
    ax[1].set(xlabel = 'Predicted', ylabel = 'Residuals')
    
linearity_test(lin_reg, y)


# Looks good! Linearity assumption is satisifed.

# **Assumption Check: Mean of residuals is zero**

# In[ ]:


lin_reg.resid.mean()


# Good, very small.

# **Assumption check: no multicollinearity**

# First, lets take a look at the corr map

# In[ ]:


plt.figure(figsize = (10,8))
sns.heatmap(X.corr(), annot = True, cmap = 'cubehelix_r')
plt.show()


# It definitely looks like the variables are not highly correlated. Let's make a function to determine the VIF of each variable

# In[ ]:


from statsmodels.stats.outliers_influence import variance_inflation_factor

vif = [variance_inflation_factor(X_constant.values, i) for i in range(X_constant.shape[1])]
pd.DataFrame({'vif': vif[1:]}, index = X.columns).to_csv


# To be honest, I'm not sure why the output is "inf" for most of these variables when it should be super low.

# **Assumption Check: homoscedasticity (equality of residual variance)**

# In[ ]:


def homoscedasticity_test(model):
    fitted_vals = model.predict()
    resids = model.resid
    resids_standardized = model.get_influence().resid_studentized_internal

    fig, ax = plt.subplots(1,2)

    sns.regplot(x=fitted_vals, y=resids, lowess=True, ax=ax[0], line_kws={'color': 'red'})
    ax[0].set_title('Residuals vs Fitted', fontsize=16)
    ax[0].set(xlabel='Fitted Values', ylabel='Residuals')

    sns.regplot(x=fitted_vals, y=np.sqrt(np.abs(resids_standardized)), lowess=True, ax=ax[1], line_kws={'color': 'red'})
    ax[1].set_title('Scale-Location', fontsize=16)
    ax[1].set(xlabel='Fitted Values', ylabel='sqrt(abs(Residuals))')

    bp_test = pd.DataFrame(sms.het_breuschpagan(resids, model.model.exog), 
                           columns=['value'],
                           index=['Lagrange multiplier statistic', 'p-value', 'f-value', 'f p-value'])

    gq_test = pd.DataFrame(sms.het_goldfeldquandt(resids, model.model.exog)[:-1],
                           columns=['value'],
                           index=['F statistic', 'p-value'])

    print('\n Breusch-Pagan test ----')
    print(bp_test)
    print('\n Goldfeld-Quandt test ----')
    print(gq_test)
    print('\n Residuals plots ----')

homoscedasticity_test(lin_reg)


# Plots look like they satisfy the assumption, and the outputs certify that assertion with p-values > 0.05

# **Assumption Check: no autocorrelation of residuals

# In[ ]:


import statsmodels.tsa.api as smt

acf = smt.graphics.plot_acf(lin_reg.resid, lags = 40, alpha = 0.05)
acf.show()


# **Assumption Check: normality of residuals**

# In[ ]:


from scipy import stats

def normality_of_residuals_test(model):
    sm.ProbPlot(model.resid).qqplot(line='s');
    plt.title('Q-Q plot');

    jb = stats.jarque_bera(model.resid)
    sw = stats.shapiro(model.resid)
    ad = stats.anderson(model.resid, dist='norm')
    ks = stats.kstest(model.resid, 'norm')
    
    print(f'Jarque-Bera test ---- statistic: {jb[0]:.4f}, p-value: {jb[1]}')
    print(f'Shapiro-Wilk test ---- statistic: {sw[0]:.4f}, p-value: {sw[1]:.4f}')
    print(f'Kolmogorov-Smirnov test ---- statistic: {ks.statistic:.4f}, p-value: {ks.pvalue:.4f}')
    print(f'Anderson-Darling test ---- statistic: {ad.statistic:.4f}, 5% critical value: {ad.critical_values[2]:.4f}')
    print('If the returned AD statistic is larger than the critical value, then for the 5% significance level, the null hypothesis that the data come from the Normal distribution should be rejected. ')
    
normality_of_residuals_test(lin_reg)


# The plot looks pretty good, quite normally distributed. Additionally, the Jarque-Bera, Kolmogorov-Smirnov and Shapiro-Wilk test confirm this. However the Anderson-Darling test appears to claim that the residuals are not normally distributed because the test statistic is greater than the critical value.

# Let's finish out this notebook with another iteration of the linear regression test to review our results.

# In[ ]:


lin_reg.summary()


# It appears that parental education is the greatest predictor of student success (in this fake dataset).
