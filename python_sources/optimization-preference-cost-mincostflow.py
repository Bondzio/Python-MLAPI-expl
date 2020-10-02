#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from collections import defaultdict
NUMBER_DAYS = 100
NUMBER_FAMILIES = 5000
MAX_BEST_CHOICE = 5
data = pd.read_csv('/kaggle/input/santa-workshop-tour-2019/family_data.csv')
submission = pd.read_csv('/kaggle/input/c-stochastic-product-search-65ns/submission.csv')
assigned_days = submission['assigned_day'].values
columns = data.columns[1:11]
DESIRED = data[columns].values

COST_PER_FAMILY        = [0,50,50,100,200,200,300,300,400,500]
COST_PER_FAMILY_MEMBER = [0, 0, 9,  9,  9, 18, 18, 36, 36,235]
N_PEOPLE = data['n_people'].astype(int).values

def get_daily_occupancy(assigned_days):
    daily_occupancy = np.zeros(100, np.int32)
    for i, r in enumerate(assigned_days):
        daily_occupancy[r-1] += N_PEOPLE[i]
    return daily_occupancy

def cost_function(prediction):
    N_DAYS = 100
    MAX_OCCUPANCY = 300
    MIN_OCCUPANCY = 125
    penalty = 0
    days = list(range(N_DAYS,0,-1))
    tmp = pd.read_csv('/kaggle/input/santa-workshop-tour-2019/family_data.csv', index_col='family_id')
    family_size_dict = tmp[['n_people']].to_dict()['n_people']

    cols = [f'choice_{i}' for i in range(10)]
    choice_dict = tmp[cols].to_dict()

    # We'll use this to count the number of people scheduled each day
    daily_occupancy = {k:0 for k in days}
    
    # Looping over each family; d is the day for each family f
    for f, d in enumerate(prediction):
        # Using our lookup dictionaries to make simpler variable names
        n = family_size_dict[f]
        choice_0 = choice_dict['choice_0'][f]
        choice_1 = choice_dict['choice_1'][f]
        choice_2 = choice_dict['choice_2'][f]
        choice_3 = choice_dict['choice_3'][f]
        choice_4 = choice_dict['choice_4'][f]
        choice_5 = choice_dict['choice_5'][f]
        choice_6 = choice_dict['choice_6'][f]
        choice_7 = choice_dict['choice_7'][f]
        choice_8 = choice_dict['choice_8'][f]
        choice_9 = choice_dict['choice_9'][f]

        # add the family member count to the daily occupancy
        daily_occupancy[d] += n

        # Calculate the penalty for not getting top preference
        if d == choice_0:
            penalty += 0
        elif d == choice_1:
            penalty += 50
        elif d == choice_2:
            penalty += 50 + 9 * n
        elif d == choice_3:
            penalty += 100 + 9 * n
        elif d == choice_4:
            penalty += 200 + 9 * n
        elif d == choice_5:
            penalty += 200 + 18 * n
        elif d == choice_6:
            penalty += 300 + 18 * n
        elif d == choice_7:
            penalty += 300 + 36 * n
        elif d == choice_8:
            penalty += 400 + 36 * n
        elif d == choice_9:
            penalty += 500 + 36 * n + 199 * n
        else:
            penalty += 500 + 36 * n + 398 * n

    # for each date, check total occupancy
    #  (using soft constraints instead of hard constraints)
    for _, v in daily_occupancy.items():
        if v > MAX_OCCUPANCY or v < MIN_OCCUPANCY:
            penalty += 100000000

    # Calculate the accounting cost
    # The first day (day 100) is treated special
    # using the max function because the soft constraints might allow occupancy to dip below 125
    accounting_cost = max(0, (daily_occupancy[days[0]]-125.0) / 400.0 * daily_occupancy[days[0]]**(0.5))
    # Loop over the rest of the days, keeping track of previous count
    yesterday_count = daily_occupancy[days[0]]
    for day in days[1:]:
        today_count = daily_occupancy[day]
        diff = abs(today_count - yesterday_count)
        accounting_cost += max(0, (today_count-125.0) / 400.0 * today_count**(0.5 + diff / 50.0))
        yesterday_count = today_count

    return penalty, accounting_cost, penalty + accounting_cost


# About Min Cost Flow (MCF) you can read there: [OR-Tools](https://developers.google.com/optimization/flow/mincostflow), [Wiki](https://en.wikipedia.org/wiki/Minimum-cost_flow_problem)
# 
# Don't have simple(!) way to get optimum preference cost from MCF because we can't split families, but if we could I recomend this notebook: [Lower bound](https://www.kaggle.com/mihaild/lower-bound-on-preference-cost)
# 
# In this example we will optimize preference cost between families with same numbers members without changing daily occupation:

# In[ ]:


get_ipython().run_cell_magic('time', '', 'from ortools.graph import pywrapgraph\nfor num_members in range(2, 9): # Families have minimum 2 and maximum 8 members\n    daily_occupancy = get_daily_occupancy(assigned_days)\n    fids = np.where(N_PEOPLE == num_members)[0]\n\n    PCOSTM = {}\n    for fid in range(NUMBER_FAMILIES):\n        if fid in fids:\n            for i in range(MAX_BEST_CHOICE):\n                PCOSTM[fid, DESIRED[fid][i]-1] = COST_PER_FAMILY[i] + N_PEOPLE[fid] * COST_PER_FAMILY_MEMBER[i]\n        else:\n            daily_occupancy[assigned_days[fid]-1] -= N_PEOPLE[fid]\n\n    offset = fids.shape[0]\n    solver = pywrapgraph.SimpleMinCostFlow()\n    for day in range(NUMBER_DAYS):\n        solver.SetNodeSupply(offset+day, int(daily_occupancy[day]//num_members))\n\n    for i in range(offset):\n        fid = fids[i]\n        solver.SetNodeSupply(i, -1)\n        for j in range(MAX_BEST_CHOICE):\n            day = DESIRED[fid][j]-1\n            solver.AddArcWithCapacityAndUnitCost(int(offset+day), i, 1, int(PCOSTM[fid, day]))\n    solver.SolveMaxFlowWithMinCost()\n\n    for i in range(solver.NumArcs()):\n        if solver.Flow(i) > 0:\n            assigned_days[fids[solver.Head(i)]] = solver.Tail(i) - offset + 1\n    print(cost_function(assigned_days))')


# In[ ]:


submission['assigned_day'] = assigned_days
submission.to_csv('submission.csv', index=False)


# As a fact we split the dataset for 7 parts and can't find the best swaps between these parts, but result almost immediately.

# ## Let's try my Santa2019 notebooks and datasets:
# * https://www.kaggle.com/golubev/manual-to-improve-submissions
# * https://www.kaggle.com/golubev/c-stochastic-product-search-65ns
# * https://www.kaggle.com/golubev/mip-optimization-preference-cost
# * https://www.kaggle.com/golubev/benchmark-mip-solvers-draft
# * https://www.kaggle.com/golubev/datasets

# ### Please upvote my notebooks and datasets if you like my work!

# 
# ### Merry Christmas and Happy New Year!
