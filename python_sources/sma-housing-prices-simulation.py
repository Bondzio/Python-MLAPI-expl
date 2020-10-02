#!/usr/bin/env python
# coding: utf-8

# lifecycle of a person
# - born with a certain wealth
# - buys a house immediately
# - dies and goes nowhere (probability of death) 
# 
# characterisitics of a person
# - age
# - net income
# - wealth (which changes with purchases and net income)
# - satisfaction (an indicator which cumulates)
# - probability of death
# 
# objective of a person
# - maximise satisfaction
# 
# objective of the government
# - maximise satisfaction of all the people
# 
# lifecycle of a house
# - empty initially
# - bought by a person
# - vacated when it is empty
# 
# characteristics of a house
# - location and coordinates 
# - occupancy
# - amentities
# 
# pricing mechanism
# - ???
# 
# process of purchase
# - each person only know a limited number of choices
# - each person will get the option that is 
#   - possible (house is empty and they have the money)
#   - best utility (x-factor for now)

# In[ ]:


get_ipython().run_cell_magic('time', '', "# installing ffmpeg so that animation module can work\n!apt-get -y install ffmpeg > /dev/null\n\nimport secrets  # python 3.6 necessary\nimport random\nimport numpy as np\nimport pandas as pd  # we try not to depend on pandas, to better translate later?\nfrom copy import deepcopy\nfrom IPython.display import display, HTML\nimport matplotlib.animation as animation\nimport matplotlib.pyplot as plt  # for viz\n\nDEATH_RATE = 0.05\npd.set_option('display.max_rows', 100)")


# # Initial state

# In[ ]:


# defining utility functions which forms the basis of housing valuation
def utility_general(house):
    '''
    Every person considers a house to have a certain utility.
    This is not based on personal perferences.
    '''
    utility_due_to_location = 2/(1 + (house["location"][0] - 5.3)**2 
                                   + (house["location"][1] - 5.3)**2)
    return utility_due_to_location + house["amenities"]["fengshui"]

def utility_function(person, house):
    '''
    A person considers each house to have a different utility.
    This assigns an additional utility of each house based on personal preferences.
    '''
    utility_due_to_person = 1/(1 + (house["location"][0] - person["idio"]["preferred_location"][0])**2 
                                 + (house["location"][1] - person["idio"]["preferred_location"][1])**2)
    return utility_general(house) + utility_due_to_person

### Weets' Vectorised Utility Functions (works with pd.Series) ###
# mere translation of above functions
# its quite hardcoded so not comfortable rofl

def utility_general_vectorised(house):
    '''
    Every person considers a house to have a certain utility.
    This is not based on personal perferences.
    '''
    utility_due_to_location = 2/(1 + (house["location"].apply(lambda tup: tup[0]) - 5.3)**2 
                                   + (house["location"].apply(lambda tup: tup[1]) - 5.3)**2)
    return utility_due_to_location + house["amenities"].apply(lambda amen_dt: amen_dt["fengshui"])

def utility_function_vectorised(person, house):
    '''
    A person considers each house to have a different utility.
    This assigns an additional utility of each house based on personal preferences.
    Input
        person: a dict or pandas df row
    '''
    # print(house["location"])
    # print(house["location"].apply(lambda tup: tup[0]))
    
    xloc = (house["location"].apply(lambda tup: tup[0]) - person["idio"]["preferred_location"][0])
    yloc = (house["location"].apply(lambda tup: tup[1]) - person["idio"]["preferred_location"][1])
    
    utility_due_to_person = 1/(1 + xloc**2 + yloc**2)
    return utility_general_vectorised(house) + utility_due_to_person


# In[ ]:


# defining a template person and generate persons
def generate_person():
    person = {
        "age": 20,
        "income": 10,
        "wealth": 400*np.random.uniform(),
        "house_staying": np.NaN,
        "house_selling": np.NaN,
        "utility": 0, # WEETS: utility here is person's 'score'. Every decision person makes must immediately result in increase of 0 or more, never decrease.
        "idio": {"preferred_location": (10*np.random.uniform(), 10*np.random.uniform())}
    }
    return person

persons = {}
for _ in range(10):
    persons[secrets.token_hex(4)] = generate_person()
persons = pd.DataFrame.from_dict(persons, orient='index')

persons['house_staying'] = persons['house_staying'].astype(object)
persons['house_selling'] = persons['house_selling'].astype(object)

persons.head()


# In[ ]:


# defining a template house and generate houses
houses = {}
for x in range(10):
    for y in range(10):
        houses[(x,y)] = {
            "location": (x,y),  # also the key 
            "last_bought_price": 400*np.random.uniform(),
            "status": "empty",  # "empty", "occupied", "selling" 
            "amenities": {"fengshui" : np.random.uniform()},
            "occupant": np.NaN,
            "last_updated": 0
        }
        houses[(x,y)]["market_price"] = houses[(x,y)]["last_bought_price"]

houses = pd.DataFrame.from_dict(houses, orient='index')

def status_to_float(status):
    if status == "empty": return 0 
    if status == "occupied": return 1 
    if status == "selling": return 2
    
houses.head()


# # Activities in timestep
# In every time step, people age, people die, and people get born.

# ### Aging

# In[ ]:


def aging(verbose = False): # change this a function of age
    persons["age"] += 1
    persons["wealth"] += persons["income"]
    houses["last_updated"] += 1


# ### Death

# In[ ]:


def dying_prob_function(age):
    return 1./(1.+np.exp(-(0.2*(age-50))))
plt.figure(figsize = (14,2))
plt.plot([dying_prob_function(age) for age in np.arange(100)])
plt.title("death probability over age")
plt.show()


# In[ ]:


def dying(verbose = False): # change this a function of age
    persons_id_dead = []
    for person_id in persons.index:
        if np.random.uniform() < dying_prob_function(persons.loc[person_id,"age"]):
            if verbose: print(person_id, " died")
            dead_person = persons.loc[person_id]
            if dead_person["house_staying"] != None:
                if verbose: print("vacated ", dead_person["house_staying"])
                houses.loc[dead_person["house_staying"],"status"] = "empty"
                houses.loc[dead_person["house_staying"],"occupant"] = None
            persons_id_dead.append(person_id)
    persons.drop(persons_id_dead, inplace=True)


# ### Birth

# In[ ]:


def birth(verbose = False):
    born = np.random.binomial(10, 0.2)
    for _ in range(born):
        persons.loc[secrets.token_hex(4)] = generate_person()


# ### Update history

# In[ ]:


from collections import defaultdict
history = defaultdict(list)

def update_history(verbose = False):
    history["popn_with_zero_house"].append((persons.house_staying.values == None).sum())
    history["popn_with_one_house"].append((persons.house_staying.values != None).sum())
    history["popn_with_two_house"].append((persons.house_selling.values != None).sum())
    history["average_wealth"].append(np.mean(persons["wealth"]))
    return None


# # Transactions
# People without a house will try and buy the best house available to them.

# In[ ]:


def choose(person_id):
    candidates = []
    if persons.loc[person_id,"house_staying"] != None:
        return None
    for addr,house in houses.to_dict('index').items():
        if house["market_price"] > persons.loc[person_id,"wealth"]:
            continue
        if house["status"] != "empty":
            continue
        candidates.append((addr,house))
    
    best = 0
    best_option = None
    for addr,house in candidates:
        user_utility_on_house = persons.loc[person_id,"utility"](persons.loc[person_id], house)
        if user_utility_on_house > best:
            best = user_utility_on_house
            best_option = addr,house
    return best_option


# In[ ]:


def allocation():
    for person_id,v in persons.to_dict('index').items():
        decision = choose(person_id)
        if not decision:
            continue
        addr, house = decision
        persons.loc[person_id,"wealth"] -= house["market_price"]
        persons.at[person_id,"house_staying"] = addr
        houses.loc[addr,"last_bought_price"] = house["market_price"]
        houses.loc[addr,"status"] = "occupied"
        houses.loc[addr,"occupant"] = person_id
        houses.loc[addr,"last_updated"] = 0


# In[ ]:


### Phase 2: ASK -> BID -> MATCH -> UPDATE
# this is meant to be ran just once at the start
ask_df = pd.DataFrame(columns = ['location','occupant_id','amenities', 'ask_price']) # init empty ask_df with col
            
def gen_asks():
    ''' phase 2 bid-ask
    1. Refresh ask_df pd.DataFrame()
    2. Add empty houses from `houses` to ask_df
    3. Add more listings from persons who can and want to sell houses
    '''
    global ask_df # may not be necessary
    ask_df_columns = ask_df.columns.to_list() # ['house_pos','current_occupant_id','amenities', 'ask_price']
    
    # 1. Refresh ask_df pd.DataFrame()
    ask_df.drop(ask_df.index, inplace=True) # drops all rows
    
    # 2. Add empty houses from `houses` to ask_df
    empty_houses = houses[houses['status']=='empty']
    
    ## 2.1 Rename, reorder into ask_df column mold
    ## ask_df column order: ['house_pos','current_occupant_id','amenities', 'ask_price']
    empty_houses_listing = empty_houses.rename(columns={
        'occupant':'occupant_id',
        'last_bought_price':'ask_price',
    })
    empty_houses_listing = empty_houses_listing[ask_df_columns] # reorder
    
    ask_df = ask_df.append(empty_houses_listing, ignore_index=True) # TODO: optimise
    
    # 3. Add more listings from `persons` who can and want to sell houses
    ## 3.1 get sub df of persons who have a second house to sell
    COND_have_house_selling = persons['house_selling'] != None
    potential_sellers = persons[COND_have_house_selling] # a persons sub df
    
    ## 3.2 Get sellable houses that have market price >= cost price
    potential_house_selling_loc = potential_sellers['house_selling']
    potential_house_selling = houses[houses['location'].isin(potential_house_selling_loc.values)]
    COND_market_greater_or_equal_cost_price = potential_house_selling['market_price'] >= potential_house_selling['last_bought_price'] 
    no_loss_house_selling = potential_house_selling[COND_market_greater_or_equal_cost_price] # a houses subdf
    
    ## 3.3 Random decide if want to sell or not
    PROBA_SELL = 0.4 # arbitrary threshold; TODO: turn into adjustable param
    COND_want_sell = no_loss_house_selling['status'].apply(lambda runif: np.random.uniform()) <= PROBA_SELL
    want_sell_houses = no_loss_house_selling[COND_want_sell]
    want_sell_houses_loc = want_sell_houses['location']
    actual_house_selling = potential_house_selling[potential_house_selling['location'].isin(want_sell_houses_loc.values)]
    
    ## 3.4 Rename, reorder actual_house_selling into ask_df column mold
    ## ask_df column order: ['house_pos','current_occupant_id','amenities', 'ask_price']
    main_listing = actual_house_selling.rename(columns={'market_price':'ask_price',
                                               'occupant':'occupant_id'})
    main_listing = main_listing[ask_df_columns]
    
    ask_df = ask_df.append(main_listing, ignore_index=True)
    
    # strangely, there's a row with nan value in location appearing
    # this chunk fixes that
    if any(ask_df['location'].apply(lambda loc: type(loc)!=tuple)):
        # print('Missing location in ask_df, applying fix')
        ori_len = len(ask_df)
        ask_df = ask_df[~ask_df['location'].isna()]
        # print('Change in len', len(ask_df)-ori_len)
    
    
# test run
# gen_asks()
# ask_df.sample(10)


# In[ ]:


### Phase 2: ASK -> BID -> MATCH -> UPDATE
# init empty ask_df with col
bid_df = pd.DataFrame(columns = ['location', 'bidder_id', 'utility_to_buyer', 'max_bid_price', 'bid_price'])
    
def gen_bids():
    ''' phase 2 bid-ask
    1. Refresh bid_df pd.DataFrame()
    2. Generate subdf of persons who can and want to buy houses
    3. For each eligible person, iterate over ask, grow person_bids list of dict
    4. Merge 
    '''
    global bid_df # may not be necessary
    bid_df_columns = bid_df.columns.to_list() # ['location', 'bidder_id', 'utility', 'bid_price']
    
    # 1. Refresh bid_df pd.DataFrame()
    bid_df.drop(bid_df.index, inplace=True) # drops all rows
    
    # 2. Screen viable bidders
    ## 2.1 Does not own a second house (can have 1 or 0 houses)
    COND_only_one_house = persons['house_selling'].isna() # NOTE: do not use `persons['house_selling'] == None` to check
    potential_buyers = persons[COND_only_one_house]
    
    ## 2.2 Random decide if want to seek or not
    PROBA_BUY = 0.8 # arbitrary threshold; TODO: turn into adjustable param
    COND_want_buy = potential_buyers['age'].apply(lambda runif: np.random.uniform()) <= PROBA_BUY
    eligible_and_seeking_buyers = potential_buyers[COND_want_buy] # these are the eligible people who want to buy houses
    
    # 3. Each eligible buyer makes a bid for each house on sale
    list_of_bid_sets = [] # to be populated with df corr. to each person's bids
    
    ## 3.1 Define helper fn
    def _gen_bid_price(listing_row):
        max_bid_price = listing_row['max_bid_price']
        ask_price = listing_row['ask_price']
        if  max_bid_price >= ask_price:
            surplus = max_bid_price - ask_price
            return ask_price + np.random.uniform() * surplus
        else:
            return max_bid_price
    
    ## 3.2 Iterate over buyers
    for idx, buyer in eligible_and_seeking_buyers.iterrows():
        buyer_view_of_ask_df = ask_df.copy()
        
        ###  3.2.1 Calculate each listing's utility to buyer
        buyer_view_of_ask_df['bidder_id'] = idx
        buyer_view_of_ask_df['utility_to_buyer'] = utility_function_vectorised(buyer, buyer_view_of_ask_df)
        # NOTE: utility_to_buyer is partial -- it only consider's a houses's general and locational utility and buyer idio
        
        ### 3.2.2 Calculate bid_price
        buyer_view_of_ask_df['max_bid_price'] = buyer['wealth'] - buyer['utility'] + buyer_view_of_ask_df['utility_to_buyer'] # TODO: double check if this is a good rule
        # NOTE: WEETS suspects above formula may be wrong since it does not compare the differential in utility DUE TO HOUSE only
        # test: what if utility to buyer is negative? Would you still bid (and spend money)?
        buyer_view_of_ask_df['max_bid_price'] = buyer_view_of_ask_df['max_bid_price'].apply(lambda mbp: min(mbp, buyer['wealth']))
        # mbp must be capped at buyer's wealth
        buyer_view_of_ask_df['max_bid_price'] = buyer_view_of_ask_df['max_bid_price'].apply(lambda mbp: max(0,mbp))
        # mbp must be non-negative
        
        bid_price = buyer_view_of_ask_df.apply(_gen_bid_price, axis=1)
        buyer_view_of_ask_df['bid_price'] = bid_price
        
        ### 3.2.3 Append specific columns of buyer_view_of_ask_df to list_of_bid_sets
        select_columns = ['location', 'bidder_id', 'utility_to_buyer', 'max_bid_price', 'bid_price']
        list_of_bid_sets.append(buyer_view_of_ask_df[select_columns])
    
    # 4. Concatenate list of dataframes into one dataframe
    if list_of_bid_sets: # possible that no bids take place
        bid_df = pd.concat(list_of_bid_sets)
    return bid_df

# bid_df = gen_bids()
# # print(bid_df['bidder_id'].nunique())
# bid_df.head()


# In[ ]:


### Phase 2: ASK -> BID -> MATCH -> UPDATE

def match_ask_bid():
    '''
    1. Create a container list to store dicts of info relating to bidding for each listing
    2. Iterate over listings in ask_df, find best bid - is successful match
    3. For each successful match
        1. Create and append dict of info relating to bids for the listing
        2. Remove all bids for same listing
        3. Remove all other bids by same bidder
        4. Update asker and bidder
    4. For each unsuccessful match
        1. Create and append dict of info relating to bids for the listing
        2. Remove all bids for same listing
    5. Make match_df
    '''
    global bid_df, persons, houses
    # 1. Create a container list to store dicts of info relating to bidding for each listing
    list_of_matches = [] # contains info on winning bid
    
    # 2. Iterate over listings in ask_df, find best bid - is successful match
    for idx, listing in ask_df.iterrows():
        match_info_dict = {} # stats for each listing match
        
        ## 2.1 Get general data
        listing_loc = listing['location']
        match_info_dict['location'] = listing_loc
        
        match_info_dict['ask_price'] = listing['ask_price']
        
        relevant_bids = bid_df[bid_df['location']==listing_loc]
        match_info_dict['num_bids'] = len(relevant_bids) # expect 0 or more
        
        highest_bid_value = relevant_bids['bid_price'].max()
        match_info_dict['highest_bid_value'] = highest_bid_value
        
        match_info_dict['mean_bid_value'] = relevant_bids['bid_price'].mean()
        
        # 3. Found winning bid(s)
        if highest_bid_value >= listing['ask_price']: # there exists a successful match
            ## 3.1 Create and append dict of info relating to bids for the listing
            ### 3.1.1 Check for ties among highest bid
            highest_bids = relevant_bids[relevant_bids['bid_price']==highest_bid_value]
            num_highest_bid = len(highest_bids) # expect at least 1, rarely more
            assert num_highest_bid >= 1, 'ERR: num_highest_bid must be >= 1'
            
            ### 3.1.2 Get the winner
            winning_bid = highest_bids.sample(1) # tie-breaker: randomly choose one highest bidder to win
            
            winning_bidder_id = winning_bid['bidder_id'].iloc[0]
            match_info_dict['winning_bidder_id'] = winning_bidder_id
            match_info_dict['winning_bid_value'] = highest_bid_value # obviously; stated explicitly as highest_bid_value may not win for the `else` case
            
            ### 3.1.3 Append match info
            list_of_matches.append(match_info_dict)
            
            ## 3.2 Remove all corresponding bids, 3.3 Remove all other bids by same bidder
            bid_df = bid_df.drop(relevant_bids.index, axis=0)
            bid_df = bid_df[~(bid_df['bidder_id']==winning_bidder_id)]
            
            ## 3.4 Update asker and bidder
            asker_id = listing['occupant_id']
            
            ### 3.4.1 Update asker
            if type(asker_id) is str: # if str, then not empty house
                persons['wealth'].loc[asker_id] += highest_bid_value
                persons['house_selling'].iloc[asker_id] = np.NaN # potential problem here?
                # TODO: check where to update 'utility' (person's simulation score) -- here or elsewhere?
                # ENSURE: asker['utility'] increase or stay the same
                
            ### 3.4.2 Update bidder
            winning_bidder = persons.loc[winning_bidder_id]
            persons['wealth'].loc[winning_bidder_id] -= highest_bid_value
            
            #### Additional updates for bidder if second house buyer
            if type(winning_bidder['house_staying']) is tuple: # first house exists, buyer is buying second house
                persons['house_selling'].loc[winning_bidder_id] = winning_bidder['house_staying'] # set current house_staying to be house_selling
                houses['status'].loc[winning_bidder['house_staying']] = 'selling' # set that same current house to 'selling' status
            persons['house_staying'].loc[winning_bidder_id] = listing_loc
            # TODO: check where to update 'utility' (person's simulation score) -- here or elsewhere?
            # ENSURE: asker['utility'] increase or stay the same
            
            ### 3.4.3 Update house
            houses['last_bought_price'].loc[listing_loc] = highest_bid_value
            houses['status'].loc[listing_loc] = 'occupied'
            # Note: for second house buyers, their first house's status has already been updated
            houses['occupant'].loc[listing_loc] = winning_bidder_id
            houses['last_updated'].loc[listing_loc] = 0
            # TODO: update houses['market_price'] at the end of each time step, somewhere else perhaps
            
        # 4. No successful match   
        else:
            ## 4.1 Create and append dict of info relating to bids for the listing
            match_info_dict['winning_bidder_id'] = np.NaN
            match_info_dict['winning_bid_value'] = np.NaN
            list_of_matches.append(match_info_dict)
            
            ## 4.2 Remove all bids for same listing
            bid_df = bid_df.drop(relevant_bids.index, axis=0)
            
    # 5. Make match_df
    match_df = pd.DataFrame(list_of_matches)
    return match_df

# gen_asks()
# bid_df = gen_bids()
# match_df = match_ask_bid() # Note: changes bid_df each time it is called
# match_df.head(10)


# In[ ]:


persons


# In[ ]:


houses


# # Begin simulation

# In[ ]:


get_ipython().run_cell_magic('time', '', 'fig, ax = plt.subplots(2,5,figsize=(12,7))\nplt.subplots_adjust(wspace=0.4)\nim0 = ax[0,0].imshow(np.random.randn(10,10), vmin=0, vmax=2)\nim1 = ax[0,1].imshow(np.random.randn(10,10), vmin=0, vmax=400)\nim2 = ax[0,2].imshow(np.random.randn(10,10), vmin=0, vmax=400)\nim3 = ax[0,3].imshow(np.random.randn(10,10), vmin=0, vmax=100)\nim4 = ax[0,4].imshow(np.random.randn(10,10), vmin=0, vmax=1)\nax[0,0].set_title("utility_general")\nax[0,1].set_title("market_price")\nax[0,2].set_title("last_bought_price")\nax[0,3].set_title("last_updated")\nax[0,4].set_title("status")\n\nline_pop_0, = ax[1,0].plot([], lw=3)\nline_pop_1, = ax[1,0].plot([], lw=3)\nline_pop_2, = ax[1,0].plot([], lw=3)\nax[1,0].set_ylim((0, 60))\nax[1,0].set_xlim((-20, 0))\nax[1,0].set_title("population")\n\nline_wealth_0, = ax[1,1].plot(range(len(history["average_wealth"][-20:])), \n                              history["average_wealth"][-20:], lw=3)\nax[1,1].set_ylim((0, 600))\nax[1,1].set_xlim((-20, 0))\nax[1,1].set_title("average wealth")\n\nscat_income_age = ax[1,2].scatter([], [], s=20)\nax[1,2].set_ylim((0, 600))\nax[1,2].set_xlim((20, 60))\nax[1,2].set_title("wealth against age")\n\npatches = [im0, im1, im2, im3, im4]\n\na1 = np.random.randn(10,10)\na2 = np.random.randn(10,10)\na3 = np.random.randn(10,10)\na4 = np.random.randn(10,10)\na5 = np.random.randn(10,10)\n\ndef update_plot():\n    for x in range(10):\n        for y in range(10):\n            a1[x,y] = utility_general(houses.loc[(x,y)])\n            a2[x,y] = houses.loc[(x,y),"market_price"]\n            a3[x,y] = houses.loc[(x,y),"last_bought_price"]\n            a4[x,y] = houses.loc[(x,y),"last_updated"]\n            a5[x,y] = status_to_float(houses.loc[(x,y),"status"])\n    im0.set_data(a1)\n    im1.set_data(a2)\n    im2.set_data(a3)\n    im3.set_data(a4)\n    im4.set_data(a5)\n    line_pop_0.set_data(range(0,-len(history["popn_with_zero_house"][-20:]),-1), \n                        history["popn_with_zero_house"][-20:])\n    line_pop_1.set_data(range(0,-len(history["popn_with_one_house"][-20:]),-1), \n                        history["popn_with_one_house"][-20:])\n    line_pop_2.set_data(range(0,-len(history["popn_with_two_house"][-20:]),-1), \n                        history["popn_with_two_house"][-20:])\n    line_wealth_0.set_data(range(0,-len(history["average_wealth"][-20:]),-1), \n                           history["average_wealth"][-20:])\n    scat_income_age.set_offsets(np.transpose((persons["age"], persons["wealth"])))\n\ndef init():\n    return patches\n\ndef next_time_step(i):\n    aging()\n    birth()\n    dying()\n    # allocation()\n    gen_asks()\n    gen_bids()\n    match_ask_bid()\n    update_history()\n    update_plot()\n    return patches\n\n# call the animator. blit=True means only re-draw the parts that have changed.\nanim = animation.FuncAnimation(fig, next_time_step, init_func=init,\n                               frames=100, interval=100, blit=True)\n\nvid = anim.to_html5_video()\nplt.close()')


# In[ ]:


HTML(vid)


# In[ ]:


# def next_time_step(i):
#     aging()
#     birth()
#     dying()
#     # allocation()
#     gen_asks()
#     gen_bids()
#     match_ask_bid()
#     update_history()
#     update_plot()
#     return patches

# for i in range(100):
#     print('>>>>>>TIME STEP<<<<<<',i)
#     next_time_step(i)


# In[ ]:


persons


# In[ ]:


houses


# In[ ]:




