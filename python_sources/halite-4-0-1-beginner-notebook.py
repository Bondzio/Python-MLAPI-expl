#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system("pip install 'kaggle-environments>=0.2.1'")

import kaggle_environments


# In[ ]:


from kaggle_environments import evaluate, make
import numpy as np
env = make("halite", debug=True)


# # Contents
# - [Preamble](#preamble)
# - [Submission](#submission)
# - [Debugging](#debug)
# - [Evaluate agent](#evaluate)
# - [Conclusions](#conclusions)

# ## Preamble <a name="preamble"></a>
# 
# I am making this Notebook because I am trying to get better at using classes in my programming. I have made a few notebooks prior to this with different agents,and I was making good progress, but as the script became more complicated I found it hard to keep up with what was going on.
# 
# ![](https://i.pinimg.com/originals/e5/d3/69/e5d369ecc7b99d71963050c5f6f0479a.jpg)
# 
# I competed solo in Halite 3 and came in position ~300 (I think), so I have the general jist of the task but I am still very much a beginner in all aspects.
# 
# In Halite 3, there was much more help and documentation in how to get involved and start. From reading the discussion page here, something similar may be in the works. I hope it does as it opens up the competition to much more people and I wouldn't of been able to compete if it wasn't for that.
# 
# 
# I hope you get something out of this, even if it is how not to do it
# 

# ## Submission file <a name="submission"></a>

# In[ ]:


get_ipython().run_cell_magic('writefile', 'submission.py', '\nimport numpy as np\nclass gameInfo:\n    \'\'\'Infomation about the state of the game\'\'\'\n    def __init__(self, observation):\n        #player id\n        self.player = observation[\'player\']\n        # gives a list containing two player lists - which contain:\n        # - player halite (int); dict(\'shipyardid\': shipyardloc); dict(\'shipn\': shipn_loc) \n        self.players = observation[\'players\']\n        # turn number\n        self.step = observation[\'step\']\n        \n\n\nclass haliteBoard:\n    \'\'\' Functions for the board\n    observation - dict with 3 keys\n        player: 0 # player id\n        step: turn in the game\n        halite map - array of halite\n    \'\'\'\n    def __init__(self, observation):\n         # creates a 1d array that matches the halite board for reference\n        self.loc_board1d = np.array(list(range(225)))\n        # creates a 2d array that matches the halite board for reference\n        self.loc_board2d = np.array(list(range(225))).reshape(15,15)\n        # the halite board - this should contain positions of all assets 1d\n        self.halite_board1d = np.array(observation.halite)\n         # the halite board - this should contain positions of all assets 2d\n        self.halite_board2d = np.array(observation.halite).reshape(15,15)\n        # map details\n        self.width = 15\n        self.height = 15\n        \n    def get_xy(self,posistion):\n        \'\'\' Takes a position e.g 101 and returns the x,y coordinates as a tuple\'\'\' \n        x,y = np.where(self.loc_board2d == posistion)\n        coords = list(zip(x,y))\n        return coords[0]\n    \n    # make function that takes coordinates and gets the index of the map\n    def get_index(self, xy):\n        \'\'\'takes tuple of (x, y) and returns position on board\'\'\'\n        index = (xy[0] * 15) + xy[1] \n        return index\n        \n    \n    \n    \n    def get_nearest_halite(self,posistion):\n        \'\'\'finds the coordiantes for the nearest halite, \n        not accounting for wraparound returns (x,y)\'\'\'\n        # where the ship is\n        current_coords = self.get_xy(posistion)\n        # where the location on the board has halite\n        # this isn\'t working correctly\n        hx, hy = np.where(self.halite_board2d > 100)\n        #list of halite locations\n        halite_coords = list(zip(hx,hy))\n        distances = {}\n        \n        for i in halite_coords:\n            # find euclidean distance, doesn\'t take into account wrap around\n            dist = np.sqrt((i[0] - current_coords[0])**2 + (i[1] - current_coords[1])**2)\n            distances[i] = dist\n        # from the dict get the closest set of coords     \n        closest_xy =  min(distances, key=distances.get)\n        return closest_xy\n    \n   \n    def get_surrounding_halite(self, posistion):\n        \'\'\'returns a dict with halite in each direction accounting for wrap\'\'\'\n        b = self.halite_board1d\n        surrounding = {None:b[posistion],\'NORTH\':np.take(b,[posistion-15], mode = \'wrap\'), \n                       \'SOUTH\':np.take(b,[posistion+15],mode = \'wrap\'),\n                       \'EAST\':np.take(b,[posistion+1],mode = \'wrap\'), \n                       \'WEST\':np.take(b,[posistion-1],mode = \'wrap\')}\n        return surrounding\n\n    def get_surrounding_loc(self,posistion):\n        \'\'\' returns the board location number of the surrounding locations \n        - N,S,E,W accounting for wrap \'\'\'\n        tb = self.loc_board1d\n        surrounding_locations = [np.take(tb,[posistion-15], mode = \'wrap\'),\n                                 np.take(tb,[posistion+15],mode = \'wrap\'),\n                                np.take(tb,[posistion+1],mode = \'wrap\'),\n                                np.take(tb,[posistion-1],mode = \'wrap\')]\n\n        return surrounding_locations\n    \n    def get_occupied_locs(self, posistion, shipyards, ships, opp_shipyards, opp_ships):\n        \'\'\' Returns all the occupied locations (number) on the map \n        excluding the current position\'\'\'\n        \n        # need to handle for when there are no ships or shipyards\n        opp_ship_locs = [i[0] for i in list(opp_ships.values())]  # e.g [0, 34, 59]\n        player_ship_locs = [i[0] for i in list(ships.values())]\n        #logic ish\n        if len(opp_shipyards.values()) == 0:\n            return opp_ship_locs + player_ship_locs\n           \n        else:\n            opp_shipyard_locs = [i for i in list(opp_shipyards.values())]\n            return opp_ship_locs + player_ship_locs + opp_shipyard_locs\n        \n     # working well   \n    def is_shipyard_occupied(self, ships, shipyards):\n        \'\'\' Returns true if there is a ship in our shipyard\'\'\'\n        player_ship_locs  = [i[0] for i in list(ships.values())]\n        if len(shipyards.values()) > 1:\n            shipyards = [i[0] for i in list(shipyards.values())]\n        elif len(shipyards.values()) < 1:\n            return False\n        else:\n            #we have one shipyard\n            shipyards =[i for i in list(shipyards.values())]\n            for i in player_ship_locs:\n                if i in shipyards:\n                    return True\n                else:\n                    return False\n                \n    def get_safe_options_surrounding(self, posistion, ship_locations,surrounding):\n        \'\'\' Will take the ships position and the dict (ship_action) of moves \n        for greedy navigation and check if they are safe\'\'\'\n        # get the number locations around the ship\n        surrounding_locs = self.get_surrounding_loc(posistion)\n        # I want to remove the occupied locations from the max halite dict\n        surrounding_locs = [i[0] for i in surrounding_locs]\n        nav_dict = {}\n        nav_dict[\'NORTH\'], nav_dict[\'SOUTH\'], nav_dict[\'EAST\'], nav_dict[\'WEST\'] = surrounding_locs\n        # now simply remove the keys where their values are in ship_locations\n        for k,v in list(nav_dict.items()):\n            if v in ship_locations:\n                surrounding.pop(k)\n        return surrounding   \n        \n\ndef get_moves_to_target(ship_loc,ship_locations, board, target):\n    \'\'\'Takes ship location and target and returns a list of 1 or more viable moves\'\'\'\n    posistion_xy = board.get_xy(ship_loc)\n    # takes int\n    target_xy = board.get_xy(target)\n\n    move_dict = {}\n    if posistion_xy[0] > target_xy[0]:\n        move_dict[\'NORTH\'] = ship_loc + 15\n    if posistion_xy[0] < target_xy[0]:\n        move_dict[\'SOUTH\'] = ship_loc - 15\n    if posistion_xy[1] < target_xy[1]:\n         move_dict[\'EAST\'] = ship_loc + 1\n    if posistion_xy[1] > target_xy[1]:\n         move_dict[\'WEST\'] = ship_loc - 1\n    for k,v in list(move_dict.items()):\n            if v in ship_locations:\n                move_dict.pop(k)\n    return move_dict\n\n\n\ndef greedy_collect(ship_loc, ship_locations, board):\n    \'\'\' Takes a ship location and the halite board returns a valid move\'\'\'\n    # needs to get the greedy move with a bias, and check if moves are safe\n    # How much it cost\'s to move?\n    move_cost = 0.1\n    surrounding = board.get_surrounding_halite(ship_loc)\n    #Bias staying still to stop wasting halite\n    surrounding[None] = surrounding[None] + (surrounding[None]* move_cost)\n    # for now if there is no halite at all move south\n    if sum([i for i in surrounding.values()]) == 0.0:\n        nearest_halite = board.get_nearest_halite(ship_loc)\n        target = board.get_index(nearest_halite)\n        moves = get_moves_to_target(ship_loc, ship_locations, board, target)\n        # now need to somehow check if the NORTH, SOUTH, WEST etc is \n        return np.random.choice(list(moves.keys()))\n\n    else:\n        surrounding = board.get_safe_options_surrounding(ship_loc, ship_locations,surrounding)\n        return max(surrounding, key=surrounding.get)\n    \n# Each ship id will be assigned a state, one of COLLECT or DEPOSIT, \n# this was something that was in the tutorial in halite 3\nglobal states\nstates = {}\n\nCOLLECT = "COLLECT"\nDEPOSIT = "DEPOSIT"\n    \n\ndef my_agent(obs):\n    state = gameInfo(obs)\n    board = haliteBoard(obs)\n    \n   \n    \n    halite, shipyards, ships = state.players[state.player]\n    opp_halite, opp_shipyards, opp_ships = state.players[1]\n    \n    action = {}\n    \n    for uid, shipyard in shipyards.items():\n    # Maintain one ship \n        if len(ships) == 0:\n            action[uid] = "SPAWN"\n    \n    for uid, ship in ships.items():\n        # Maintain one shipyard \n        if len(shipyards) == 0:\n            action[uid] = "CONVERT"\n            continue        \n    \n    for uid, ship_info in ships.items():\n        #Assuming it has just spawned\n        if uid not in states:\n            states[uid] = COLLECT\n        # If we are collecting    \n        if states[uid] == COLLECT:\n            if ship_info[1] > 500:\n                states[uid] = DEPOSIT\n            else:\n                #greedy collect\n                surrounding = board.get_surrounding_halite(ship_info[0])  # index 0 is the location, 1 is the amount of halite of the ship\n                # get ship locations\n                ship_locations = board.get_occupied_locs(ship_info[0], shipyards, ships, opp_shipyards, opp_ships)\n                ship_action = greedy_collect(ship_info[0], ship_locations, board)\n                if ship_action is not None:\n                    action[uid] = ship_action\n        \n        # return to shipyard\n        if states[uid] == DEPOSIT:\n            if ship_info[1] < 20:\n                states[uid] = COLLECT\n            else:\n                ship_locations = board.get_occupied_locs(ship_info[0], shipyards, ships, opp_shipyards, opp_ships)\n                moves = get_moves_to_target(ship_info[0], ship_locations, board, shipyard)\n                if moves == {}:\n                    ship_action = None\n                else:\n                    ship_action = np.random.choice(list(moves.keys()))\n                if ship_action is not None:\n                    action[uid] = ship_action    \n\n    return action')


# ## Debugging zone <a name="debug"></a>
# 
# - list of things that need to be done

# In[ ]:


class gameInfo:
    '''Infomation about the state of the game'''
    def __init__(self, observation):
        #player id
        self.player = observation['player']
        # gives a list containing two player lists - which contain:
        # - player halite (int); dict('shipyardid': shipyardloc); dict('shipn': shipn_loc) 
        self.players = observation['players']
        # turn number
        self.step = observation['step']
        


class haliteBoard:
    ''' Functions for the board
    observation - dict with 3 keys
        player: 0 # player id
        step: turn in the game
        halite map - array of halite
    '''
    def __init__(self, observation):
         # creates a 1d array that matches the halite board for reference
        self.loc_board1d = np.array(list(range(225)))
        # creates a 2d array that matches the halite board for reference
        self.loc_board2d = np.array(list(range(225))).reshape(15,15)
        # the halite board - this should contain positions of all assets 1d
        self.halite_board1d = np.array(observation.halite)
         # the halite board - this should contain positions of all assets 2d
        self.halite_board2d = np.array(observation.halite).reshape(15,15)
        # map details
        self.width = 15
        self.height = 15
        
    def get_xy(self,posistion):
        ''' Takes a position e.g 101 and returns the x,y coordinates as a tuple''' 
        x,y = np.where(self.loc_board2d == posistion)
        coords = list(zip(x,y))
        return coords[0]
    
    # make function that takes coordinates and gets the index of the map
    def get_index(self, xy):
        '''takes tuple of (x, y) and returns position on board'''
        index = (xy[0] * 15) + xy[1] 
        return index
        
    
    
    
    def get_nearest_halite(self,posistion):
        '''finds the coordiantes for the nearest halite, 
        not accounting for wraparound returns (x,y)'''
        # where the ship is
        current_coords = self.get_xy(posistion)
        # where the location on the board has halite
        # this isn't working correctly
        hx, hy = np.where(self.halite_board2d > 100)
        #list of halite locations
        halite_coords = list(zip(hx,hy))
        distances = {}
        
        for i in halite_coords:
            # find euclidean distance, doesn't take into account wrap around
            dist = np.sqrt((i[0] - current_coords[0])**2 + (i[1] - current_coords[1])**2)
            distances[i] = dist
        # from the dict get the closest set of coords     
        closest_xy =  min(distances, key=distances.get)
        return closest_xy
    
   
    def get_surrounding_halite(self, posistion):
        '''returns a dict with halite in each direction accounting for wrap'''
        b = self.halite_board1d
        surrounding = {None:b[posistion],'NORTH':np.take(b,[posistion-15], mode = 'wrap'), 
                       'SOUTH':np.take(b,[posistion+15],mode = 'wrap'),
                       'EAST':np.take(b,[posistion+1],mode = 'wrap'), 
                       'WEST':np.take(b,[posistion-1],mode = 'wrap')}
        return surrounding

    def get_surrounding_loc(self,posistion):
        ''' returns the board location number of the surrounding locations 
        - N,S,E,W accounting for wrap '''
        tb = self.loc_board1d
        surrounding_locations = [np.take(tb,[posistion-15], mode = 'wrap'),
                                 np.take(tb,[posistion+15],mode = 'wrap'),
                                np.take(tb,[posistion+1],mode = 'wrap'),
                                np.take(tb,[posistion-1],mode = 'wrap')]

        return surrounding_locations
    
    def get_occupied_locs(self, posistion, shipyards, ships, opp_shipyards, opp_ships):
        ''' Returns all the occupied locations (number) on the map 
        excluding the current position'''
        
        # need to handle for when there are no ships or shipyards
        opp_ship_locs = [i[0] for i in list(opp_ships.values())]  # e.g [0, 34, 59]
        player_ship_locs = [i[0] for i in list(ships.values())]
        #logic ish
        if len(opp_shipyards.values()) == 0:
            return opp_ship_locs + player_ship_locs
           
        else:
            opp_shipyard_locs = [i for i in list(opp_shipyards.values())]
            return opp_ship_locs + player_ship_locs + opp_shipyard_locs
        
     # working well   
    def is_shipyard_occupied(self, ships, shipyards):
        ''' Returns true if there is a ship in our shipyard'''
        player_ship_locs  = [i[0] for i in list(ships.values())]
        if len(shipyards.values()) > 1:
            shipyards = [i[0] for i in list(shipyards.values())]
        elif len(shipyards.values()) < 1:
            return False
        else:
            #we have one shipyard
            shipyards =[i for i in list(shipyards.values())]
            for i in player_ship_locs:
                if i in shipyards:
                    return True
                else:
                    return False
                
    def get_safe_options_surrounding(self, posistion, ship_locations,surrounding):
        ''' Will take the ships position and the dict (ship_action) of moves 
        for greedy navigation and check if they are safe'''
        # get the number locations around the ship
        surrounding_locs = self.get_surrounding_loc(posistion)
        # I want to remove the occupied locations from the max halite dict
        surrounding_locs = [i[0] for i in surrounding_locs]
        nav_dict = {}
        nav_dict['NORTH'], nav_dict['SOUTH'], nav_dict['EAST'], nav_dict['WEST'] = surrounding_locs
        # now simply remove the keys where their values are in ship_locations
        for k,v in list(nav_dict.items()):
            if v in ship_locations:
                surrounding.pop(k)
        return surrounding   
        


# ### main()

# In[ ]:


# Play as first position against random agent.
trainer = env.train([None, "random"])

observation = trainer.reset()

def get_moves_to_target(ship_loc,ship_locations, board, target):
    '''Takes ship location and target and returns a list of 1 or more viable moves'''
    posistion_xy = board.get_xy(ship_loc)
    # takes int
    target_xy = board.get_xy(target)

    move_dict = {}
    if posistion_xy[0] > target_xy[0]:
        move_dict['NORTH'] = ship_loc + 15
    if posistion_xy[0] < target_xy[0]:
        move_dict['SOUTH'] = ship_loc - 15
    if posistion_xy[1] < target_xy[1]:
         move_dict['EAST'] = ship_loc + 1
    if posistion_xy[1] > target_xy[1]:
         move_dict['WEST'] = ship_loc - 1
    for k,v in list(move_dict.items()):
            if v in ship_locations:
                move_dict.pop(k)
    return move_dict



def greedy_collect(ship_loc, ship_locations, board):
    ''' Takes a ship location and the halite board returns a valid move'''
    # needs to get the greedy move with a bias, and check if moves are safe
    # How much it cost's to move?
    move_cost = 0.1
    surrounding = board.get_surrounding_halite(ship_loc)
    #Bias staying still to stop wasting halite
    surrounding[None] = surrounding[None] + (surrounding[None]* move_cost)
    # for now if there is no halite at all move south
    if sum([i for i in surrounding.values()]) == 0.0:
        nearest_halite = board.get_nearest_halite(ship_loc)
        target = board.get_index(nearest_halite)
        moves = get_moves_to_target(ship_loc, ship_locations, board, target)
        # now need to somehow check if the NORTH, SOUTH, WEST etc is 
        return np.random.choice(list(moves.keys()))

    else:
        surrounding = board.get_safe_options_surrounding(ship_loc, ship_locations,surrounding)
        return max(surrounding, key=surrounding.get)
    
# Each ship id will be assigned a state, one of COLLECT or DEPOSIT, 
# this was something that was in the tutorial in halite 3
global states
states = {}

COLLECT = "COLLECT"
DEPOSIT = "DEPOSIT"
    

def my_agent(obs):
    state = gameInfo(obs)
    board = haliteBoard(obs)
    
   
    
    halite, shipyards, ships = state.players[state.player]
    opp_halite, opp_shipyards, opp_ships = state.players[1]
    
    action = {}
    
    for uid, shipyard in shipyards.items():
    # Maintain one ship 
        if len(ships) == 0:
            action[uid] = "SPAWN"
    
    for uid, ship in ships.items():
        # Maintain one shipyard 
        if len(shipyards) == 0:
            action[uid] = "CONVERT"
            continue        
    
    for uid, ship_info in ships.items():
        #Assuming it has just spawned
        if uid not in states:
            states[uid] = COLLECT
        # If we are collecting    
        if states[uid] == COLLECT:
            if ship_info[1] > 500:
                states[uid] = DEPOSIT
            else:
                #greedy collect
                surrounding = board.get_surrounding_halite(ship_info[0])  # index 0 is the location, 1 is the amount of halite of the ship
                # get ship locations
                ship_locations = board.get_occupied_locs(ship_info[0], shipyards, ships, opp_shipyards, opp_ships)
                ship_action = greedy_collect(ship_info[0], ship_locations, board)
                if ship_action is not None:
                    action[uid] = ship_action
        
        # return to shipyard
        if states[uid] == DEPOSIT:
            if ship_info[1] < 20:
                states[uid] = COLLECT
            else:
                ship_locations = board.get_occupied_locs(ship_info[0], shipyards, ships, opp_shipyards, opp_ships)
                moves = get_moves_to_target(ship_info[0], ship_locations, board, shipyard)
                if moves == {}:
                    ship_action = None
                else:
                    ship_action = np.random.choice(list(moves.keys()))
                if ship_action is not None:
                    action[uid] = ship_action    

    return action



while not env.done:
    my_action = my_agent(observation)
    print("My Action", my_action)
    observation, reward, done, info = trainer.step(my_action)
    


# In[ ]:


env.render(mode = 'ipython')


# ## Evaluation  <a name="evaluate"></a>

# In[ ]:


def mean_reward(rewards):
    wins = 0
    ties = 0
    loses = 0
    for r in rewards:
        r0 = 0 if r[0] is None else r[0]
        r1 = 0 if r[1] is None else r[1]
        if r0 > r1:
            wins += 1
        elif r1 > r0:
            loses += 1
        else:
            ties += 1
    return f'wins={wins/len(rewards)}, ties={ties/len(rewards)}, loses={loses/len(rewards)}'

# Run multiple episodes to estimate its performance.
# Setup agentExec as LOCAL to run in memory (runs faster) without process isolation.
print("My Agent vs Random Agent:", mean_reward(evaluate(
    "halite",
    ["/kaggle/working/submission.py", "random"],
    num_episodes=10, configuration={"agentExec": "LOCAL"}
)))


# ## Conclusions <a name="conclusions"></a>
# 
# * Documenting eveything really helped keep track of what was going on.
# * The agent is very hacky and in my next development I will change things a lot, but it does feel like somewhat of an accomplishment to complete something.
# 
# ### Next time
# 
# * accounting for wrap-around should be a priority
# * add multiple ships
# * optimise paramters.
