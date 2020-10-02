#!/usr/bin/env python
# coding: utf-8

# # Portfolio Analysis
# 
# **ECE 478 Financial Signal Processing**
# 
# **Pset1: Portoflio Analysis**
# 
# Our general Steps will be:
# 1.  Preprocessing (can be found [here](https://www.kaggle.com/guybaryosef/portfolio-analysis-preprocessing/notebook))
#     * This will include loading, cleaning, and organizing the benchmark we will use benchmark, S&P 500 returns, and the USD Libor (interest rate).
# 2. Basic Markowitz Portfolio Analysis
# 3. Sparse Portfolio Analysis (In the not-to-distant-future)

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ### Basic Markovitz Portfolio Analysis
# 
# In the preprocessing stage, we did the following:
# 1. Took the Farma and French Dataset 48 benchmark, which was acquired from [Kenneth R. French](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html), cleaned it, and split its daily returns for the 48 securities into 17 files, one for each year 2000-2016.
# 2. Aquired the S&P500 daily lows and highs from [Yahoo Finance](https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC) and computed the daily returns, organizing the data into years equivalent to the benchmark in step 1.
# 3. Aquired the USD 3 month LIBOR rate from [here](http://iborate.com/usd-libor/). Converted it into an effective daily rate and packaged these daily rates into files by years 2000 - 2016, just as above. 
# 
# In this kernel we will use the 48 securities in our benchmark as the possible stocks in our portoflio. More so, we will model the S&P500 as our market portfolio (spolier alert, it won't do a good job), and the LIBOR rates as our risk-free interest rate (i.e. the interest rate of the money market).
# 
# We will go according to the pset1 specifications, allowing the user to input a year of their choice (between 2000 - 2016) to analyze. 
# 
# At the end of this analysis we will pipeline all the parts together and look at our results.
# 
# To show our results, lets begin with specifying a year to demonstrate the functions as we go through them.

# In[ ]:


year = 2004


# #### Part A)
# We will start by computing the sample mean and the sample covariance matrix of the 48 securities.

# In[ ]:


def openBenchmark(year, kind):
    '''
    Opens the dataset corresponding with specific year and type.
    Valid Input:
        year: between 2000 - 2016 (those are just the years we preprocessed)
        kind: Options are (note that there is no error checking):
            'benchmark' - The 48 security daily averages.
            'sp500' - Daily returns of the S&P 500'.
            'libor' - Effective daily interest rate for the USD 3-month LIBOR.
    '''
    
    base = ''
    if kind == 'benchmark':
        base = '../input/48_IP_eq_w_daily_returns_'
    elif kind == 'sp500':
        base = '../input/SP_daily_returns_'
    elif kind == 'libor':
        base = '../input/LIBOR_daily_interest_'
        
    try:
        benchmark = pd.read_csv(base + str(year) + '.csv')
    except:
        sys.exit('Unable to open the', kind, 'file for the specified year. :(')
    
    benchmark.set_index('Date', inplace=True) # set the date field as the row index
    return benchmark


# In[ ]:


def mean_cov(dataframe):
    '''
    Given a pandas dataframe, returns its mean (along the columns) and the
    covariance matrix of its columns.
    '''
    data = np.transpose(dataframe)
    
    meanVec = pd.DataFrame({'Mean': list(data.mean(axis=1))})
    work_days_in_year = data.columns.size
    
    covMat = (1/(work_days_in_year-1))*(np.subtract(data @ np.transpose(data), meanVec @ np.transpose(meanVec)))
    
    return meanVec, covMat


# In[ ]:


def find_mean_cov(year):
    ''' 
    Opens benchmark of specified year and returns the security means and covariance matrix.
    '''
    benchmark = openBenchmark(year, 'benchmark')
    if isinstance(benchmark, int):
        return -1    

    return mean_cov(benchmark)


# In[ ]:


find_mean_cov(year)


# #### Part B)
# Compute the expected risk and return of the portfolio, $\sigma$, $\mu$ respectively.
# Note that the risk is defined as the standard deviation of the returns.
# 
# We will do this for the inputted naive portfolio, market portfolio, and the minimum variance portfolio (MVP):
# * The naive portfolio is the one whose weights are equal for all the securities.
# * The market portofolio is the S&P500 returns (more on this later).
# * The minimum variance portfolio is the portfolio whose variance is the smallest possible.

# In[ ]:


def sigma_mu(year):
    '''
    Given a year, returns the following real-numbered values (in order):
        Naive Portfolio's Expected Returns
        Naive Portfolio's Expected Risk
        MVP's Expected Returns
        MVP's Expected Risk
        Market Portfolio's Expected Returns
        Market Portfolio's Expected Risk
    '''
    
    # NAIVE PORTFOLIO (assumes equal weights for each security)
    meanVec, covMat = find_mean_cov(year)    

    naive_weights = pd.DataFrame({'Weights': ([1/48] * 48)})
    mu_naive_portfolio = (np.transpose(meanVec) @ naive_weights).values[0][0]
    sigma_naive_portfolio =  np.sum(np.sqrt( np.transpose(naive_weights.values) @ covMat.values @ naive_weights.values ))

    # MVP PORTFOLIO
    sigma_mvp_portfolio = 1/np.sqrt( np.sum(np.linalg.inv(covMat.values)) )
    mvp_weights = np.sum(  (sigma_mvp_portfolio**2) * np.linalg.inv(covMat) , axis=1 )
    mu_mvp_portfolio = np.sum((np.transpose(meanVec) @ mvp_weights ) )
    
    # MARKET PORTFOLIO
    sp = openBenchmark(year, 'sp500')
    if (isinstance(sp, int) ):
        return -1
    
    mu_market_portfolio = sp['Return'].mean()
    sigma_market_portfolio = np.sqrt( sp['Return'].var() )
    
    return  mu_naive_portfolio, sigma_naive_portfolio, mu_mvp_portfolio, sigma_mvp_portfolio, mu_market_portfolio, sigma_market_portfolio


# Next we will plot the feasible portfolio curve of 5 pairs of randomly chosen securities, under the assumption of no short selling. 
# Note that for each of these pairs, there will be a different portfolio mean and variance as well as MVP.

# In[ ]:


def twoRand(low, high, notIn = []):
    '''
    Given a lower and upper bound, returns 2 random integers within the range, not including the integers in 'notIn'.
    Note that there is no other error checking.
    '''
    cur1 = cur2 = int(round(np.random.uniform(low, high)))
    while cur1 in notIn:
        cur1 = int(round(np.random.uniform(low, high)))
    
    notIn.append(cur1)
    while cur2 in notIn:
        cur2 = int(round(np.random.uniform(low, high)))
    return cur1, cur2


# In[ ]:


def twoSecFeasableCurve(year, num1, num2):
    '''
    Given a year and two numbers between 0 and 47 (representing two securities),
    this function plots the feasable portfolio curve of the securities under the assumption of no short selling.
    '''
    n_mean, n_cov = find_mean_cov(year)    
    mu_n_port, sig_n_port, _, _, _, _ = sigma_mu(2000)

    A=(n_cov.iloc[num1][num1] + n_cov.iloc[num2][num2] - 2*n_cov.iloc[num1][num2]) / ((n_mean.iloc[num1] - n_mean.iloc[num2])**2)
     
    # keeping the expected return between the two individual means lets us avoid short selling
    mu = []
    if n_mean.iloc[[num1],0].values > n_mean.iloc[[num2],0].values:
        mu = np.linspace(n_mean.iloc[[num2],0].values, n_mean.iloc[[num1],0].values, 1000)
    else:
        mu = np.linspace(n_mean.iloc[[num1],0].values, n_mean.iloc[[num2],0].values, 1000)
    
    # finally, lets compute the MVP (sigma, mu) for these two portfolios
    benchmark = openBenchmark(year, 'benchmark')
    two_securities = benchmark.iloc[:, [num1, num2]]
    two_mean, two_cov = mean_cov(two_securities)
    two_mvp_sig = 1 / np.sqrt(np.sum(np.linalg.inv(two_cov) ))
    two_mvp_weights = np.sum((two_mvp_sig**2) * np.linalg.inv(two_cov.values), axis=0)
    two_mvp_mean = np.sum(np.transpose(two_mean) @ two_mvp_weights )
    
    sig = [np.sqrt( (A)*(m - two_mvp_mean)**2 + two_mvp_sig**2 ) for m in mu]
    
    plt.plot(sig, mu, label='Securities:'+ benchmark.columns[num1]+ ' & '+ benchmark.columns[num2])


# In[ ]:


def fiveFeasalbeCurves(year):
    '''
    Given a year, this function plots the feasable portoflio curve of
    5 randomly chosen pairs of securities.
    '''
    notIn = []
    plt.figure(figsize=[15,10])
    for _ in range(5):
        num1, num2 = twoRand(0,47, notIn)
        notIn.append([num1, num2])
        twoSecFeasableCurve(year, num1, num2)
        
    plt.xlabel('$\sigma$, (Risk)')
    plt.ylabel('$\mu$, (Expected Return)')
    plt.title('Feasible Portfolios for 2 Random Securities')
    plt.legend()
    plt.show()


# In[ ]:


fiveFeasalbeCurves(year)


# #### Part C)
# Compute the efficient frontier and graph it.

# In[ ]:


def efficientFrontierSigma(year, mu):
    '''
    Given a year and list of expected returns, returns the expected risks corresponding to the efficient frontier.
    '''
    n_mean, n_cov = find_mean_cov(year)
    
    # equation for the Markovitz bullet
    mu_tild = pd.concat([n_mean, pd.DataFrame({'1s':[1]*len(n_mean.index)}) ], axis=1)
    B = np.transpose(mu_tild) @ np.linalg.inv(n_cov.values) @ mu_tild
    G = np.linalg.inv(B) @ np.transpose(mu_tild) @ np.linalg.inv(n_cov.values) @ mu_tild @ np.linalg.inv(B)
    
    return [np.sqrt(G[0][0]*((m + (G[1][0]/G[0][0]) )**2) + np.linalg.det(G)/G[0][0]) for m in mu]


# In[ ]:


def get_libor_rate(year):
    '''
    Returns the averaged effective daily USD 3-month LIBOR rate for the given year.
    '''
    libor = openBenchmark(year, 'libor')
    risk_free_rate = libor.mean(axis=0)
    return risk_free_rate.values[0]


# In[ ]:


def efficientFrontierGraph(year, theoret= []):
    '''
    Given a year, this function graphs the efficient frontier as well as the line segment connecting
    the risk-free interest rate (in our case, the libor rate) and the market portfolio (in our case, the S&P500).
    Will accept an optional input of [expected return, risk] that will be the theoretical market portfolo.
    '''
    _, _, mu_mvp, sig_mvp, mu_market, sig_market = sigma_mu(year)
    
    mu = np.linspace(-5,5, 1000)
    sig = efficientFrontierSigma(year, mu)
    
    plt.figure(figsize=[15,10])
    plt.plot(sig, mu, label='Markowitz Bullet')
    plt.xlabel('$\sigma$, Risk')
    plt.ylabel('$\mu$, Expected Return')
    plt.axis([0, 4, -1.5, 1.5])
    plt.title('The Efficient Frontier')
    
    #adding the line(s) connecting the risk-free interest rate and the market portfolios
    R = get_libor_rate(year)
    plt.plot([0, sig_market], [R, mu_market], marker='o', label='Risk-free rate to S&P500')
    
    if theoret:
        plt.plot([0, theoret[1]], [R, theoret[0]], marker='o', label='Risk-free rate to Theoretical Market Portfolio')
    
    plt.legend()
    plt.show()


# In[ ]:


efficientFrontierGraph(year)


# As we shall see, the S&P 500 does not do a good job approximating the market portfolio (which should lie on the efficient frontier and be the tangent line between the risk-free interest rate and the efficient frontier.
# 
# Because of this, we will also compute the theoretical market portoflio and continue our analysis with both the S&P500 and the correct (theoretical) market portofolio.

# In[ ]:


def theoreticalMarketPort(year):
    '''
    Finds the theoretical market portfolio for the benchmark portfolio given a specific year.
    Returns the market portolio's expected return and risk.
    '''
    meanVec, covMat = find_mean_cov(year)
    R = get_libor_rate(year)
    
    m_ex = meanVec - R
    weights = (1/np.sum(np.linalg.inv(covMat) @ m_ex))*(np.linalg.inv(covMat.values) @ m_ex)
    exp_ret = np.sum(np.transpose(meanVec) @ weights)
    risk = np.sum(np.sqrt( np.transpose(weights) @ covMat.values @ weights ))
    
    return exp_ret, risk


# In[ ]:


theoret_mu, theoret_sig = theoreticalMarketPort(year)
efficientFrontierGraph(year, [theoret_mu, theoret_sig])


# #### Parts D and E)
# Confirm that if we take 3 random points from the efficient frontier, we can obtain one of their weights as a convex combination of the weights of the other 2.
# This means that for the weights of any 3 efficient portoflios ($\vec{w_1}$, $\vec{w_2}$, $\vec{w_3}$), we can satisfy the equation:
#  $$ w_{1i} = uw_{2i} + (1-u)w_{3i} \ \ , for \ \ 0 < i < 47 $$
# 
# for any $u \in \mathbb{R}$. 
# 
# More so, for $R$ the risk-free interest rate, does the following inequality hold: $R < \mu_{MVP}$?

# In[ ]:


def confirmConvexCombo(year):
    '''
    This function does several things, given a specific year:
        1. Finds 3 random points on the efficient frontier and confirms that the returns and risk are both ascending together.
        2. Confirms that each point of the efficient frontier (the weights of said points) is a convex combination of the weights of any other 2 points (weights) on the efficient frontier.
        3. Checks whether the risk-free interest rate (libor rate) is lower or larger than the expected return of the MVP.
        4. Returns the weights, expected returns, and expected risk of the 3 randomly picked points on the efficient frontier.
    '''
    # PART D
    _, _, mu_mvp, _, _, _ = sigma_mu(year)
    mu = np.random.uniform(mu_mvp, 1, 3) # to check this, mu >= mu_MVP
    mu.sort()
    sig = efficientFrontierSigma(year, mu)
    
    # confirm expected risks are in same increasing order as the expected returns
    if (sig[0] < sig[1] and sig[1] < sig[2]):
        print('Sigmas are valued correctly!')
    else:
        print('Sigmas are not valued correctly :(')
    print('Expected Values:', mu, '\nRisk:', sig, end='\n\n')
    
    # get the weights of the three points
    meanVec, covMat = find_mean_cov(year)
    
    m_tild = pd.concat([meanVec, pd.DataFrame({'1s':[1]*len(meanVec.index)}) ], axis=1)
    B = np.transpose(m_tild) @ np.linalg.inv(covMat.values) @ m_tild
    
    mu_tild = [[[m], [1]] for m in mu]
    weights = [np.linalg.inv(covMat.values) @ m_tild @ np.linalg.inv(B) @ i for i in mu_tild]
    
    # confirm that each efficient portfolio is a combination of any 2 efficient portofolios
    u = np.divide(weights[0] - weights[2], weights[1] - weights[2])
    print('Confirming that the portoflios are made up of a convex combination of each other by showing that all the values in the vector u are the same:\n', u, end='\n\n')
    
    # PART E, is R < mu_MVP?
    R = get_libor_rate(year)
    if (R < mu_mvp):
        print('R is less than mu_MVP', end=' ')
    else:
        print('R is greater than the mu_MVP', end=' ')
    print(' R:', R, ', mu_MVP:', mu_mvp)
    
    return weights, sig, mu


# In[ ]:


three_rand_w, three_rand_sig, three_rand_mu = confirmConvexCombo(year)


# #### Part F)
# Find the equation for the Capital Market Line, knowing that its equation is:
# $$ \mu = R + \frac{\mu_M - R}{\sigma_M}\sigma$$
# 
# Where $\mu_M$, $\sigma_M$ are the expected return and the risk of the market portfolio respectively and $R$ is the risk-free interest rate.
# As stated previously,  the S&P500 is an inadequate estimator for our market portfolio and so we will use the theoretical values instead.

# In[ ]:


def CMLlambdaFunc(year):
    '''
    Returns the Capital Market Line (as a lambda function) for a given year.
    '''
    theoret_mu, theoret_sig = theoreticalMarketPort(year)
    R = get_libor_rate(year)
    
    return lambda sig: R + (theoret_mu - R)*sig/theoret_sig


# #### Part G)
# Find the beta factor of the MVP, the 3 portfolios we looked at on the efficient frontier, and the naive portfolio. The two relevant equations for the beta factor of a portfolio $V$ are:
# $$ \beta_V = \frac{cov (K_V, K_M)}{\sigma_M^2}  = \frac{\mu_V - R}{\mu_M - R} $$
# 
# where $V$ is refers to the specific portfolio, $M$ is referes to the market portfolio (we will use the theoretical one).

# In[ ]:


def betaFactor(year, sigma, mu): 
    '''
    Given a year and the returns and risks of any number of points:
        1. Finds the beta factors of the MVP, navie portfolio, and the inputted points.
        2. Finds the covariance between each of the inputted points' returns and the market portfolio's returns.
        3. Graphs the expected returns of beta factor graph, as well as the points found in step 1.
    '''
    theoret_mu, theoret_sig = theoreticalMarketPort(year)
    mu_naive, _, mu_mvp, _, _, _ = sigma_mu(year)
    R = get_libor_rate(year)
    
    # find 3 efficient frontier points' beta and covariance(b/w their returns and the market portofolio's)
    beta = [(mu_port - R)/(theoret_mu-R) for mu_port in mu]
    print('The beta for the three inputed points are:', beta)
    cov = [(theoret_sig**2)*i for i in beta]
    print('The covaraince between the inputed points\' returns and the market portfolio are:', cov)
    
    # plot the mu by beta
    plt.figure(figsize=[15,10])
    
    # mu by beta line
    plt_beta = np.linspace(0, 3, 100)
    plt_mu = [b*(theoret_mu - R) + R for b in plt_beta]
    plt.plot(plt_beta, plt_mu)
    
    # adding the individual points
    for i, (m,b) in enumerate(zip(mu, beta)):
        plt.plot(b,m, marker='o', label='Point '+ str(i))
    plt.plot((mu_mvp-R)/(theoret_mu-R), mu_mvp, marker='o', label='MVP')
    plt.plot((mu_naive-R)/(theoret_mu-R), mu_naive, marker='o', label='Naive Portoflio')
    
    plt.xlabel('$\\beta$ (Beta Factor)')
    plt.ylabel('$\mu$ (Expected Returns)')
    plt.title('The Expected Returns over Beta Factor graph')
    plt.legend()
    plt.show()


# In[ ]:


betaFactor(year, three_rand_sig, three_rand_mu)


# #### Part H)
# Suppose you start with $1 on January 1st for each of the following portfolios: the MVP, market portfolio (S&P500), the naive portfolio, and the three portfolios you chose on the efficient frontier. Graph their value in time for the year using the actual data.

# In[ ]:


def plotUtil(dataCol, lab):
    '''
    Helper function to 'graphValue'. Given a column of daily returns, plots the changing value of 1$.  
    '''
    time = range(np.size(dataCol,0))
    val = [1]
    for i in range(len(time)-1):
        val.append(val[i]*(1+dataCol[i]/100))
    plt.plot(time, val, label=lab)


# In[ ]:


def graphValue(year, points = []):
    '''
    Graphs the changing value of an initial investment of 1$ to the following portfolios:
        MVP
        naive portfolio
        market porfolio (S&P500)
        Any number of points (input their weights).
    '''
    plt.figure(figsize=[15,10])
    
    sp = openBenchmark(year, 'sp500')
    benchmark = openBenchmark(year, 'benchmark')
    if isinstance(sp, int) or isinstance(benchmark, int):
        return -1
    
    # S&P500
    plotUtil(sp['Return'].values, 'S&P500')
    
    # naive portfolio
    naive_weights = pd.DataFrame({'Weights': ([1/48] * 48)})
    naive_returns = benchmark.values @ naive_weights
    plotUtil(naive_returns, 'Naive Portfolio')
    
    # MVP
    n_mean, n_cov = find_mean_cov(year)
    sigma_mvp_portfolio = 1/np.sqrt( np.sum(np.linalg.inv(n_cov.values)) )
    mvp_weights = np.sum(  (sigma_mvp_portfolio**2) * np.linalg.inv(n_cov) , axis=1 )
    mvp_returns = benchmark.values @ mvp_weights
    plotUtil(mvp_returns, 'MVP Portfolio')
    
    # inputted weights of the inputted portfolios
    for i,weights in enumerate(points):
        cur_return = benchmark.values @ weights
        plotUtil(cur_return, 'Efficient Portfolio #'+str(i+1))
    
    plt.title('Value of Initial 1\$ investment over the course of '+str(year))
    plt.ylabel('Value in USD')
    plt.xticks([0,83, 164, 250], ('January', 'April', 'August', 'December'))
    plt.xlabel('Time (1 year)')
    plt.legend()
    plt.show()


# In[ ]:


graphValue(year)


# We can now run all the functions one after the other:

# In[ ]:


def the_works(year):
    '''
    Runs all the functions we have made in this kernel.
    '''
    m, c = find_mean_cov(year)
    print('For year ', year, 'the expected returns for each sector is:\n', m, '\n\nThe resulting covariance matrix for the securities is:\n', c)
    fiveFeasalbeCurves(year)
    theoret_mu, theoret_sig = theoreticalMarketPort(year)
    efficientFrontierGraph(year, [theoret_mu, theoret_sig])
    three_eff_front_weights, three_eff_front_sig, three_eff_front_mean = confirmConvexCombo(year)
    betaFactor(year, three_eff_front_mean, three_eff_front_sig)
    graphValue(year, three_eff_front_weights)


# In[ ]:


the_works(2008) # financial crash 


# In[ ]:


the_works(2014) # another example


# and thats Markowitz's Portfolio Theory!
# 
# It is encouraging to see a positive $\mu$ over $\beta$ graph for both of these experiments. When this graph was run using the S&P500 subsitutting the market portfolio the slope was seen to be negative, and so this could be seen as further proof that it cannot model the market portfolio. 
# 
# The original thought behind having the S&P500 stand as the market portfolio was the assumption that everyone will have knowledge of this analysis and so will all share the same market portfolio, leading to everyone having weights proportional to the market capitalization. The S&P500 is based off of the market capitalization and includes a large variety of stocks, and so was hypothesized to be a good approximation.
