#!/usr/bin/env python
# coding: utf-8

# <font color="red">Note: This is building on and expanding the notebook from Annalie and I</font> [Here](https://www.kaggle.com/annalie/kivampi)
# # Kiva's Current Poverty Targeting System
# 
# ## The Challenge
# Kiva.org provides zero-interest, risk-tolerant capital to microfinance institutions and businesses around the world with the goal of supporting financial services to poor and financially excluded borrowers. Because we reach the borrowers on our [Lending Page](http://www.kiva.org/lend) through field partners, we don't usually have a chance to directly assess their level of wealth or poverty. Having a more accurate or precise estimate of each borrower's level of poverty would be valuable to us for several reasons. For example:
# 
# Making sure new funding sources target the poorest Kiva borrowers.
# Allowing lenders to select low-income borrowers when that's their goal.
# Assessing new potential field partners
# 
# While we don't have direct measures, we do have a variety of informative variables that (we suspect) could jointly predict levels of income or financial access given the right training data. We're working with Kaggle because we'd like to build such a model. Our primary criteria for a good predictive model of poverty will be accuracy and coverage. Improvements on our current global model would be welcome progress, but equally welcome would be a highly accurate country-level model, especially in a country with lots of borrowers like Kenya, the Philippines, Senegal, Paraguay, or many others.

# ## Kiva's Current Poverty Targeting System
# Now I'll introduce you to Kiva's current poverty targeting system, which assigns scores to field partners and loan themes based on their location using the [Multi-dimensional Poverty Index (MPI)](http://ophi.org.uk/multidimensional-poverty-index/global-mpi-2017/mpi-data/) and the Global Findex dataset for financial inclusion.

# ## MPI Scores
# MPI scores are assigned at two levels of granularity, national and sub-national.
# 
# ### Making National MPI Scores for each Field Partner
# Nation-level MPI Scores are broken into rural and urban scores. So Kiva's broadest measure simply
# 
# 1. Merges Kiva Loan Theme data with National MPI Data on *ISO* Codes. 
# 2. Makes the average MPI (weighted by *rural_pct*) into a Loan Theme MPI Score
# 3. For about 12 multi-country partners, we then have to take volume-weighted averages across  countries.

# In[ ]:


# Load libraries
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pandas as pd
from numpy import log10, ceil, ones
from numpy.linalg import inv 
from matplotlib import pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

# Supress unnecessary warnings so that presentation looks clean
import warnings
warnings.filterwarnings("ignore")

# Print all rows and columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[ ]:


# Load & Merge data
LT = pd.read_csv("../input/data-science-for-good-kiva-crowdfunding/loan_themes_by_region.csv").set_index('Loan Theme ID')
MPI = pd.read_csv("../input/mpi/MPI_national.csv")[['ISO','MPI Urban','MPI Rural']].set_index("ISO")
LT = LT.join(MPI,how='left',on="ISO")[['Partner ID','Field Partner Name','ISO','MPI Rural','MPI Urban','rural_pct','amount']].dropna()
print("Merged Loan Theme data with National MPI Scores (Rural & Urban)")
LT.head()


# In[ ]:


LT['Rural'] = LT['rural_pct']/100        #~ Convert rural percentage to 0-1
LT['MPI Natl'] = LT['Rural']*LT['MPI Rural'] + (1-LT['Rural'])*LT['MPI Urban'] #~ Compute the MPI Score for each loan theme, weighting by rural_pct
weighted_avg = lambda df: pd.Series(np.average(df['MPI Natl'],weights=df['amount']))             #~ Need a volume-weighted average for mutli-country partners. 
Scores = LT.groupby(['Partner ID','ISO']).agg({'MPI Natl': np.mean,'amount':np.sum}).groupby(level='Partner ID').apply(weighted_avg)
Scores.columns = ['MPI Natl']
Scores = Scores.join(LT.groupby('Partner ID')['Rural'].mean())


# So we can see that the scores in this case follow a predictable distribution with a long tail. The MPI is clearly suited to differentiating one poor country from another, and does less to differentiate among middle- and high-income countries. You can also see that rual areas scores are (pretty much) always poorer than urban areas, as you might expect. 
# 
# That said, the relationship between *'% rural'* and the national-level MPI Score is noisy-- most of the variation in MPI is driven by geography.

# In[ ]:


fig, ax = plt.subplots(2, 2,figsize=(8,8))
Scores['MPI Natl'].plot(kind='hist', bins=30,ax=ax[0,0], title= "Rural-weighted MPI Scores by Field Parnter")
MPI['MPI Rural'].plot(kind='hist', bins=30,ax=ax[0,1], title="Rural MPI Scores by Country")
MPI.plot(kind='scatter',x = 'MPI Rural', y = 'MPI Urban', title = "Urban vs. Rural MPI Scores by Country\n(w/ y=x line)", ax=ax[1,0])
ax[1,0].plot(ax[1,0].get_xlim(),ax[1,0].get_ylim(),label="Rural==Urban line"); ax[1,0].legend()
sns.regplot('Rural','MPI Natl', data=Scores, order=2, ax=ax[1,1]).set_title('Rural Share of Borrowers vs. Country-level MPI')
plt.tight_layout()


# ### Making Sub-National MPI Scores for each Loan Theme & Field Partner
# A big reason for chosing [OPHI's MPI](ophi.org.uk/multidimensional-poverty-index/global-mpi-2017/mpi-data/) as our poverty index was that it is disaggregated at the administrative region level, so that we can account for targeting within countries to some extent.  Once we have a loan's region as specified by OPHI (i.e. *mpi_region* ), we simply:
# 
# 1. Merge in the region's MPI <br>
#    <font size="2">(For partners/countries without sub-national MPI scores, merge in the country-level rural/urban MPI Scores from before)</font>
# 2. Take the average across all regions (weighted by volume) for a given loan theme. (This is the Loan Theme MPI Score)
# 3. Further aggregate to get Field Partner MPI Scores (if we're interested)
# 
# <font color="green">Note that it might be slightly better in this context to use loan-level coordinates (found [HERE](https://www.kaggle.com/gaborfodor/additional-kiva-snapshot/data)) instead of theme-level coordinates. But loan_themes_by_region.csv should cover most or all of the relevant geographic variation in a conveniently aggregated format.</font>

# In[ ]:


# Load data
MPI = pd.read_csv("../input/mpi/MPI_subnational.csv")[['Country', 'Sub-national region', 'World region', 'MPI Regional']]
MPInat = pd.read_csv("../input/mpi/MPI_national.csv")[['ISO','Country','MPI Rural', 'MPI Urban']].set_index('ISO')
LT = pd.read_csv("../input/data-science-for-good-kiva-crowdfunding/loan_themes_by_region.csv")[['country','Partner ID', 'Loan Theme ID', 'region', 'mpi_region', 'ISO', 'number', 'amount','rural_pct', 'LocationName', 'Loan Theme Type']]
# Create new column mpi_region and join MPI data to Loan themes on it
MPI['mpi_region'] = MPI[['Sub-national region', 'Country']].apply(lambda x: ', '.join(x), axis=1)
MPI = MPI.set_index('mpi_region')
LT = LT.join(MPI, on='mpi_region', rsuffix='_mpi') #[['country','Partner ID', 'Loan Theme ID', 'Country', 'ISO', 'mpi_region', 'MPI Regional', 'number', 'amount','Loan Theme Type']]
#~ Pull in country-level MPI Scores for when there aren't regional MPI Scores
LT = LT.join(MPInat, on='ISO',rsuffix='_mpinat')
LT['Rural'] = LT['rural_pct']/100        #~ Convert rural percentage to 0-1
LT['MPI Natl'] = LT['Rural']*LT['MPI Rural'] + (1-LT['Rural'])*LT['MPI Urban']
LT['MPI Regional'] = LT['MPI Regional'].fillna(LT['MPI Natl'])
#~ Get "Scores": volume-weighted average of MPI Region within each loan theme.
Scores = LT.groupby('Loan Theme ID').apply(lambda df: np.average(df['MPI Regional'], weights=df['amount'])).to_frame()
Scores.columns=["MPI Score"]
#~ Pull loan theme details
LT = LT.groupby('Loan Theme ID').first()[['country','Partner ID','Loan Theme Type','MPI Natl','Rural','World region']].join(Scores)#.join(LT_['MPI Natl'])
notmissing = LT['MPI Score'].count()
notmissing_pct = round(100*notmissing/float(LT.shape[0]),1)
print("Now we've made Subnational MPI Scores for each loan theme.\nNote we only have scores for {}% ({}) of Loan Themes.".format(notmissing_pct, notmissing))


# #### Comparing Country & Sub-national MPI Scores
# The first thing we notice with sub-national scores is that they are broadly similar *on average* to the country-level MPI Score, with similar distributions.  To be sure, we can see plenty of loan themes where the two diverge, but this seems like an improvement in granularity, rather than solving any systematic bias. It also looks like the relationship to the field partner-level *rural percentage* is broadly the same, suggesting to me that the distinction between Rural MPI and Urban MPI from above is largely captured by the region-level disaggregation (i.e. when distinguishing between rural and urban Kiva borrowers, we are usually talking about distinct regions with corresponding differences in MPI score).

# In[ ]:


fig, ax = plt.subplots(2, 2, figsize=(10,10))
# Compare distributions 
LT[['MPI Score','MPI Natl']].plot(kind='kde', ax=ax[0,0], title = "Distribution of National & Regional MPI")

# Compare Regions
sns.boxplot(y='MPI Score',x='World region',data=LT,ax=ax[0,1])
for tick in ax[0,1].get_xticklabels(): tick.set_rotation(35)

#~ Rural/Urban vs Sub-national MPI Scores
colors = dict(zip(set(LT['World region']),'red,blue,green,orange,black,purple,yellow'.split(",")))
for area,df in LT.groupby('World region'): ax[1,0].scatter(df['MPI Score'],df['MPI Natl'],c=colors[area],label=area,marker='.')
x,y = ax[1,0].get_xlim(),ax[1,0].get_ylim()
sns.regplot('MPI Score','MPI Natl', data=LT, marker = '.', scatter=False, ax=ax[1,0]).set_title("National vs. Regional MPI")
ax[1,0].set_xlim(x);ax[1,0].set_ylim(y)
ax[1,0].plot(ax[1,0].get_xlim(),ax[1,0].get_ylim(),'g--',label="Regional==National"); ax[1,0].legend()
#~ Compare to Rural % by field partner
sns.regplot('Rural','MPI Score', data=LT, order=2, marker = '.', ax=ax[1,1]).set_title("Rural % of Borrowers vs. Regional MPI")
plt.legend(); plt.tight_layout()

