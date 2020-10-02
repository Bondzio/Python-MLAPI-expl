#!/usr/bin/env python
# coding: utf-8

# # What's this
# - Visualize battle results for easier analysis

# # create agent
# - create your agent "submission.py"
# - here is copied from https://www.kaggle.com/yegorbiryukov/halite-swarm-intelligence
# 

# In[ ]:


get_ipython().run_cell_magic('writefile', 'submission.py', '# for Debug/Train previous line (%%writefile submission.py) should be commented out, uncomment to write submission.py\n\n#FUNCTIONS###################################################\ndef get_map_and_average_halite(obs):\n    """\n        get average amount of halite per halite source\n        and map as two dimensional array of objects and set amounts of halite in each cell\n    """\n    game_map = []\n    halite_sources_amount = 0\n    halite_total_amount = 0\n    for x in range(conf.size):\n        game_map.append([])\n        for y in range(conf.size):\n            game_map[x].append({\n                # value will be ID of owner\n                "shipyard": None,\n                # value will be ID of owner\n                "ship": None,\n                # value will be amount of halite\n                "ship_cargo": None,\n                # amount of halite\n                "halite": obs.halite[conf.size * y + x]\n            })\n            if game_map[x][y]["halite"] > 0:\n                halite_total_amount += game_map[x][y]["halite"]\n                halite_sources_amount += 1\n    average_halite = halite_total_amount / halite_sources_amount\n    return game_map, average_halite\n\ndef get_swarm_units_coords_and_update_map(s_env):\n    """ get lists of coords of Swarm\'s units and update locations of ships and shipyards on the map """\n    # arrays of (x, y) coords\n    swarm_shipyards_coords = []\n    swarm_ships_coords = []\n    # place on the map locations of units of every player\n    for player in range(len(s_env["obs"].players)):\n        # place on the map locations of every shipyard of the player\n        shipyards = list(s_env["obs"].players[player][1].values())\n        for shipyard in shipyards:\n            x = shipyard % conf.size\n            y = shipyard // conf.size\n            # place shipyard on the map\n            s_env["map"][x][y]["shipyard"] = player\n            if player == s_env["obs"].player:\n                swarm_shipyards_coords.append((x, y))\n        # place on the map locations of every ship of the player\n        ships = list(s_env["obs"].players[player][2].values())\n        for ship in ships:\n            x = ship[0] % conf.size\n            y = ship[0] // conf.size\n            # place ship on the map\n            s_env["map"][x][y]["ship"] = player\n            s_env["map"][x][y]["ship_cargo"] = ship[1]\n            if player == s_env["obs"].player:\n                swarm_ships_coords.append((x, y))\n    return swarm_shipyards_coords, swarm_ships_coords\n\ndef get_c(c):\n    """ get coordinate, considering donut type of the map """\n    return c % conf.size\n\ndef clear(x, y, player, game_map):\n    """ check if cell is safe to move in """\n    # if there is no shipyard, or there is player\'s shipyard\n    # and there is no ship\n    if ((game_map[x][y]["shipyard"] == player or game_map[x][y]["shipyard"] == None) and\n            game_map[x][y]["ship"] == None):\n        return True\n    return False\n\ndef move_ship(x_initial, y_initial, actions, s_env, ship_index):\n    """ move the ship according to first acceptable tactic """\n    ok, actions = go_for_halite(x_initial, y_initial, s_env["ships_keys"][ship_index], actions, s_env, ship_index)\n    if ok:\n        return actions\n    ok, actions = unload_halite(x_initial, y_initial, s_env["ships_keys"][ship_index], actions, s_env, ship_index)\n    if ok:\n        return actions\n    return standard_patrol(x_initial, y_initial, s_env["ships_keys"][ship_index], actions, s_env, ship_index)\n\ndef go_for_halite(x_initial, y_initial, ship_id, actions, s_env, ship_index):\n    """ ship will go to safe cell with enough halite, if it is found """\n    # biggest amount of halite among scanned cells\n    most_halite = s_env["low_amount_of_halite"]\n    for d in range(len(directions_list)):\n        x = directions_list[d]["x"](x_initial)\n        y = directions_list[d]["y"](y_initial)\n        # if cell is safe to move in\n        if (clear(x, y, s_env["obs"].player, s_env["map"]) and\n                not hostile_ship_near(x, y, s_env["obs"].player, s_env["map"], s_env["ships_values"][ship_index][1])):\n            # if current cell has more than biggest amount of halite\n            if s_env["map"][x][y]["halite"] > most_halite:\n                most_halite = s_env["map"][x][y]["halite"]\n                direction = directions_list[d]["direction"]\n                direction_x = x\n                direction_y = y\n    # if cell is safe to move in and has substantial amount of halite\n    if most_halite > s_env["low_amount_of_halite"]:\n        actions[ship_id] = direction\n        s_env["map"][x_initial][y_initial]["ship"] = None\n        s_env["map"][direction_x][direction_y]["ship"] = s_env["obs"].player\n        return True, actions\n    return False, actions\n\ndef unload_halite(x_initial, y_initial, ship_id, actions, s_env, ship_index):\n    """ unload ship\'s halite if there is any and Swarm\'s shipyard is near """\n    if s_env["ships_values"][ship_index][1] > 0:\n        for d in range(len(directions_list)):\n            x = directions_list[d]["x"](x_initial)\n            y = directions_list[d]["y"](y_initial)\n            # if shipyard is there and unoccupied\n            if (clear(x, y, s_env["obs"].player, s_env["map"]) and\n                    s_env["map"][x][y]["shipyard"] == s_env["obs"].player):\n                actions[ship_id] = directions_list[d]["direction"]\n                s_env["map"][x_initial][y_initial]["ship"] = None\n                s_env["map"][x][y]["ship"] = s_env["obs"].player\n                return True, actions\n    return False, actions\n\ndef standard_patrol(x_initial, y_initial, ship_id, actions, s_env, ship_index):\n    """ \n        ship will move in expanding circles clockwise or counterclockwise\n        until reaching maximum radius, then radius will be minimal again\n    """\n    directions = ships_data[ship_id]["directions"]\n    # set index of direction\n    i = ships_data[ship_id]["directions_index"]\n    direction_found = False\n    for j in range(len(directions)):\n        x = directions[i]["x"](x_initial)\n        y = directions[i]["y"](y_initial)\n        # if cell is ok to move in\n        if (clear(x, y, s_env["obs"].player, s_env["map"]) and\n                (s_env["map"][x][y]["shipyard"] == s_env["obs"].player or\n                not hostile_ship_near(x, y, s_env["obs"].player, s_env["map"], s_env["ships_values"][ship_index][1]))):\n            ships_data[ship_id]["moves_done"] += 1\n            # apply changes to game_map, to avoid collisions of player\'s ships next turn\n            s_env["map"][x_initial][y_initial]["ship"] = None\n            s_env["map"][x][y]["ship"] = s_env["obs"].player\n            # if it was last move in this direction\n            if ships_data[ship_id]["moves_done"] >= ships_data[ship_id]["ship_max_moves"]:\n                ships_data[ship_id]["moves_done"] = 0\n                ships_data[ship_id]["directions_index"] += 1\n                # if it is last direction in a list\n                if ships_data[ship_id]["directions_index"] >= len(directions):\n                    ships_data[ship_id]["directions_index"] = 0\n                    ships_data[ship_id]["ship_max_moves"] += 1\n                    # if ship_max_moves reached maximum radius expansion\n                    if ships_data[ship_id]["ship_max_moves"] > max_moves_amount:\n                        ships_data[ship_id]["ship_max_moves"] = 2\n            actions[ship_id] = directions[i]["direction"]\n            direction_found = True\n            break\n        else:\n            # loop through directions\n            i += 1\n            if i >= len(directions):\n                i = 0\n    # if ship is not on shipyard and hostile ship is near\n    if (not direction_found and s_env["map"][x_initial][y_initial]["shipyard"] == None and\n            hostile_ship_near(x_initial, y_initial, s_env["obs"].player, s_env["map"],\n                              s_env["ships_values"][ship_index][1])):\n        # if there is enough halite to convert\n        if s_env["ships_values"][ship_index][1] >= conf.convertCost:\n            actions[ship_id] = "CONVERT"\n            s_env["map"][x_initial][y_initial]["ship"] = None\n        else:\n            for i in range(len(directions)):\n                x = directions[i]["x"](x_initial)\n                y = directions[i]["y"](y_initial)\n                # if it is opponent\'s shipyard\n                if s_env["map"][x][y]["shipyard"] != None:\n                    # apply changes to game_map, to avoid collisions of player\'s ships next turn\n                    s_env["map"][x_initial][y_initial]["ship"] = None\n                    s_env["map"][x][y]["ship"] = s_env["obs"].player\n                    actions[ship_id] = directions[i]["direction"]\n                    break\n    return actions\n\ndef get_directions(i0, i1, i2, i3):\n    """ get list of directions in a certain sequence """\n    return [directions_list[i0], directions_list[i1], directions_list[i2], directions_list[i3]]\n\ndef hostile_ship_near(x, y, player, m, cargo):\n    """ check if hostile ship is in one move away from game_map[x][y] and has less or equal halite """\n    # m = game map\n    n = get_c(y - 1)\n    e = get_c(x + 1)\n    s = get_c(y + 1)\n    w = get_c(x - 1)\n    if (\n            (m[x][n]["ship"] != player and m[x][n]["ship"] != None and m[x][n]["ship_cargo"] <= cargo) or\n            (m[x][s]["ship"] != player and m[x][s]["ship"] != None and m[x][s]["ship_cargo"] <= cargo) or\n            (m[e][y]["ship"] != player and m[e][y]["ship"] != None and m[e][y]["ship_cargo"] <= cargo) or\n            (m[w][y]["ship"] != player and m[w][y]["ship"] != None and m[w][y]["ship_cargo"] <= cargo)\n        ):\n        return True\n    return False\n\ndef to_spawn_or_not_to_spawn(s_env):\n    """ to spawn, or not to spawn, that is the question """\n    # get ships_max_amount to decide whether to spawn new ships or not\n    ships_max_amount = 0\n    # decrease spawn_limit if half or less of game steps remained\n    if s_env["obs"].step < middle_step:\n        # sum of all ships of every player\n        total_ships_amount = 0\n        for player in range(len(s_env["obs"].players)):\n            total_ships_amount += len(s_env["obs"].players[player][2])\n        # to avoid division by zero\n        if total_ships_amount > 0:\n            ships_max_amount = (s_env["average_halite"] // total_ships_amount) * 10\n        # if ships_max_amount is less than minimal allowed amount of ships in the Swarm\n    if ships_max_amount < ships_min_amount:\n        ships_max_amount = ships_min_amount\n    return ships_max_amount\n\ndef define_some_globals(configuration):\n    """ define some of the global variables """\n    global conf\n    global middle_step\n    global convert_threshold\n    global max_moves_amount\n    global globals_not_defined\n    conf = configuration\n    middle_step = conf.episodeSteps // 2\n    convert_threshold = conf.convertCost + conf.spawnCost * 3\n    max_moves_amount = conf.size\n    globals_not_defined = False\n\ndef adapt_environment(observation, configuration):\n    """ adapt environment for the Swarm """\n    s_env = {}\n    s_env["obs"] = observation\n    if globals_not_defined:\n        define_some_globals(configuration)\n    s_env["map"], s_env["average_halite"] = get_map_and_average_halite(s_env["obs"])\n    s_env["low_amount_of_halite"] = s_env["average_halite"] / 2\n    s_env["swarm_halite"] = s_env["obs"].players[s_env["obs"].player][0]\n    s_env["swarm_shipyards_coords"], s_env["swarm_ships_coords"] = get_swarm_units_coords_and_update_map(s_env)\n    s_env["ships_keys"] = list(s_env["obs"].players[s_env["obs"].player][2].keys())\n    s_env["ships_values"] = list(s_env["obs"].players[s_env["obs"].player][2].values())\n    s_env["shipyards_keys"] = list(s_env["obs"].players[s_env["obs"].player][1].keys())\n    s_env["ships_max_amount"] = to_spawn_or_not_to_spawn(s_env)\n    return s_env\n    \ndef actions_of_ships(s_env):\n    """ actions of every ship of the Swarm """\n    global movement_tactics_index\n    actions = {}\n    shipyards_amount = len(s_env["shipyards_keys"])\n    for i in range(len(s_env["swarm_ships_coords"])):\n        x = s_env["swarm_ships_coords"][i][0]\n        y = s_env["swarm_ships_coords"][i][1]\n        # if this is a new ship\n        if s_env["ships_keys"][i] not in ships_data:\n            ships_data[s_env["ships_keys"][i]] = {\n                "moves_done": 0,\n                "ship_max_moves": 2,\n                "directions": movement_tactics[movement_tactics_index]["directions"],\n                "directions_index": 0\n            }\n            movement_tactics_index += 1\n            if movement_tactics_index >= movement_tactics_amount:\n                movement_tactics_index = 0\n        # if it is last step\n        elif s_env["obs"].step == (conf.episodeSteps - 2) and s_env["ships_values"][i][1] >= conf.convertCost:\n            actions[s_env["ships_keys"][i]] = "CONVERT"\n            s_env["map"][x][y]["ship"] = None\n        # if there is no shipyards, necessity to have shipyard, no hostile ships near,\n        # first half of the game and enough halite to spawn few ships\n        elif (shipyards_amount == 0 and len(s_env["ships_keys"]) < s_env["ships_max_amount"] and\n                not hostile_ship_near(x, y, s_env["obs"].player, s_env["map"], s_env["ships_values"][i][1]) and\n                s_env["obs"].step < middle_step and\n                (s_env["swarm_halite"] + s_env["ships_values"][i][1]) >= convert_threshold):\n            s_env["swarm_halite"] = s_env["swarm_halite"] + s_env["ships_values"][i][1] - conf.convertCost\n            actions[s_env["ships_keys"][i]] = "CONVERT"\n            s_env["map"][x][y]["ship"] = None\n            shipyards_amount += 1\n        else:\n            # if this cell has low amount of halite or hostile ship is near\n            if (s_env["map"][x][y]["halite"] < s_env["low_amount_of_halite"] or\n                    hostile_ship_near(x, y, s_env["obs"].player, s_env["map"], s_env["ships_values"][i][1])):\n                actions = move_ship(x, y, actions, s_env, i)\n    return actions\n     \ndef actions_of_shipyards(actions, s_env):\n    """ actions of every shipyard of the Swarm """\n    ships_amount = len(s_env["ships_keys"])\n    # spawn ships from every shipyard, if possible\n    for i in range(len(s_env["swarm_shipyards_coords"])):\n        if s_env["swarm_halite"] >= conf.spawnCost and ships_amount < s_env["ships_max_amount"]:\n            x = s_env["swarm_shipyards_coords"][i][0]\n            y = s_env["swarm_shipyards_coords"][i][1]\n            # if there is currently no ship on shipyard\n            if clear(x, y, s_env["obs"].player, s_env["map"]):\n                s_env["swarm_halite"] -= conf.spawnCost\n                actions[s_env["shipyards_keys"][i]] = "SPAWN"\n                s_env["map"][x][y]["ship"] = s_env["obs"].player\n                ships_amount += 1\n        else:\n            break\n    return actions\n\n\n#GLOBAL_VARIABLES#############################################\nconf = None\nmiddle_step = None\n# max amount of moves in one direction before turning\nmax_moves_amount = None\n# threshold of harvested by a ship halite to convert\nconvert_threshold = None\n# object with ship ids and their data\nships_data = {}\n# initial movement_tactics index\nmovement_tactics_index = 0\n# minimum amount of ships that should be in the Swarm at any time\nships_min_amount = 10\n# not all global variables are defined\nglobals_not_defined = True\n\n# list of directions\ndirections_list = [\n    {\n        "direction": "NORTH",\n        "x": lambda z: z,\n        "y": lambda z: get_c(z - 1)\n    },\n    {\n        "direction": "EAST",\n        "x": lambda z: get_c(z + 1),\n        "y": lambda z: z\n    },\n    {\n        "direction": "SOUTH",\n        "x": lambda z: z,\n        "y": lambda z: get_c(z + 1)\n    },\n    {\n        "direction": "WEST",\n        "x": lambda z: get_c(z - 1),\n        "y": lambda z: z\n    }\n]\n\n# list of movement tactics\nmovement_tactics = [\n    # N -> E -> S -> W\n    {"directions": get_directions(0, 1, 2, 3)},\n    # S -> E -> N -> W\n    {"directions": get_directions(2, 1, 0, 3)},\n    # N -> W -> S -> E\n    {"directions": get_directions(0, 3, 2, 1)},\n    # S -> W -> N -> E\n    {"directions": get_directions(2, 3, 0, 1)},\n    # E -> N -> W -> S\n    {"directions": get_directions(1, 0, 3, 2)},\n    # W -> S -> E -> N\n    {"directions": get_directions(3, 2, 1, 0)},\n    # E -> S -> W -> N\n    {"directions": get_directions(1, 2, 3, 0)},\n    # W -> N -> E -> S\n    {"directions": get_directions(3, 0, 1, 2)},\n]\nmovement_tactics_amount = len(movement_tactics)\n\n#THE_SWARM####################################################\ndef swarm_agent(observation, configuration):\n    """ RELEASE THE SWARM!!! """\n    s_env = adapt_environment(observation, configuration)\n    actions = actions_of_ships(s_env)\n    actions = actions_of_shipyards(actions, s_env)\n    return actions')


# In[ ]:


from kaggle_environments.envs.halite.helpers import *
from kaggle_environments import evaluate, make
from kaggle_environments.envs.halite.helpers import *
import numpy as np
import pandas as pd
import submission
env = make("halite", debug=True)

trainer = env.train([None, "submission.py", "submission.py", "submission.py"])
observation: Observation = trainer.reset()
pre_count = 1
steps = []
board_halite = []
p0_halite = []
p1_halite = []
p2_halite = []
p3_halite = []
p0_cargo = []
p1_cargo = []
p2_cargo = []
p3_cargo = []
p0_ships = []
p1_ships = []
p2_ships = []
p3_ships = []
p0_shipyards = []
p1_shipyards = []
p2_shipyards = []
p3_shipyards = []
while not env.done:
    my_action = submission.swarm_agent(observation, env.configuration)
    observation, reward, done, info = trainer.step(my_action)
    board = Board(observation, env.configuration)
    steps.append(observation.step)
    last_step = observation.step
    board_halite.append(sum(observation.halite))
    p0_halite.append(board.players[0].halite)
    p1_halite.append(board.players[1].halite)
    p2_halite.append(board.players[2].halite)
    p3_halite.append(board.players[3].halite)
    p0_cargo.append(sum([ship.halite for ship in board.players[0].ships]))
    p1_cargo.append(sum([ship.halite for ship in board.players[1].ships]))
    p2_cargo.append(sum([ship.halite for ship in board.players[2].ships]))
    p3_cargo.append(sum([ship.halite for ship in board.players[3].ships]))
    p0_ships.append(len(board.players[0].ship_ids))
    p1_ships.append(len(board.players[1].ship_ids))
    p2_ships.append(len(board.players[2].ship_ids))
    p3_ships.append(len(board.players[3].ship_ids))
    p0_shipyards.append(len(board.players[0].shipyard_ids))
    p1_shipyards.append(len(board.players[1].shipyard_ids))
    p2_shipyards.append(len(board.players[2].shipyard_ids))
    p3_shipyards.append(len(board.players[3].shipyard_ids))
env.render(mode="ipython", width=800, height=600)


# # create data frame

# In[ ]:


df = pd.DataFrame(
data={'step': steps, 'board_halite': board_halite,
    'p0_halite': p0_halite,
    'p1_halite': p1_halite,
    'p2_halite': p2_halite,
    'p3_halite': p3_halite,
    'p0_cargo': p0_cargo,
    'p1_cargo': p1_cargo,
    'p2_cargo': p2_cargo,
    'p3_cargo': p3_cargo,
    'p0_ships': p0_ships,
    'p1_ships': p1_ships,
    'p2_ships': p2_ships,
    'p3_ships': p3_ships,
    'p0_shipyards': p0_shipyards,
    'p1_shipyards': p1_shipyards,
    'p2_shipyards': p2_shipyards,
    'p3_shipyards': p3_shipyards,
},
columns=['step', 'board_halite',
     'p0_halite',
     'p1_halite',
     'p2_halite',
     'p3_halite',
     'p0_cargo',
     'p1_cargo',
     'p2_cargo',
     'p3_cargo',
     'p0_ships',
     'p1_ships',
     'p2_ships',
     'p3_ships',
     'p0_shipyards',
     'p1_shipyards',
     'p2_shipyards',
     'p3_shipyards',
 ]
)
df['p0_total_halite']  = df['p0_halite'] + df['p0_cargo']
df['p1_total_halite']  = df['p1_halite'] + df['p1_cargo']
df['p2_total_halite']  = df['p2_halite'] + df['p2_cargo']
df['p3_total_halite']  = df['p3_halite'] + df['p3_cargo']

df


# In[ ]:


df.describe()


# In[ ]:


import seaborn as sns
import numpy as np                             
import pandas as pd                              
import matplotlib.pyplot as plt
import seaborn as sns; sns.set() 
sns.set()


# In[ ]:


df0 = pd.DataFrame(
data={'player':'p0','step': steps, 'board_halite': board_halite,
    'halite': p0_halite,
    'cargo': p0_cargo,
    'ships': p0_ships,
    'shipyards': p0_shipyards,
},
columns=['player','step', 'board_halite',
     'halite',
     'cargo',
     'ships',
     'shipyards',
 ]
)
df1 = pd.DataFrame(
data={'player':'p1','step': steps, 'board_halite': board_halite,
    'halite': p1_halite,
    'cargo': p1_cargo,
    'ships': p1_ships,
    'shipyards': p1_shipyards,
},
columns=['player','step', 'board_halite',
     'halite',
     'cargo',
     'ships',
     'shipyards',
 ]
)
df2 = pd.DataFrame(
data={'player':'p2','step': steps, 'board_halite': board_halite,
    'halite': p2_halite,
    'cargo': p2_cargo,
    'ships': p2_ships,
    'shipyards': p2_shipyards,
},
columns=['player','step', 'board_halite',
     'halite',
     'cargo',
     'ships',
     'shipyards',
 ]
)
df3 = pd.DataFrame(
data={'player':'p3','step': steps, 'board_halite': board_halite,
    'halite': p3_halite,
    'cargo': p3_cargo,
    'ships': p3_ships,
    'shipyards': p3_shipyards,
},
columns=['player','step', 'board_halite',
     'halite',
     'cargo',
     'ships',
     'shipyards',
 ]
)

df_merged = pd.concat([df0,df1,df2,df3])


# In[ ]:


df_merged['total_halite'] = df_merged['halite'] + df_merged['cargo']
df_merged['cargo_average']  = df_merged['cargo'] / df_merged['ships']
df_merged['cargo_percentage'] = df_merged['cargo'] / df_merged['total_halite']


# In[ ]:


df_merged


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("player halite at game end", fontsize=15)
sns.barplot(data=df_merged[df_merged['step']==last_step],x='player',y='halite',ci=None)
plt.ylabel('halite', fontsize=12)
plt.xlabel('player', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("average halite in game", fontsize=15)
sns.barplot(data=df_merged,x='player',y='halite',ci=None)
plt.ylabel('mean halite', fontsize=12)
plt.xlabel('player', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("player cargo at game end", fontsize=15)
sns.barplot(data=df_merged[df_merged['step']==last_step],x='player',y='cargo',ci=None)
plt.ylabel('cargo', fontsize=12)
plt.xlabel('player', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("player halite time line", fontsize=15)
sns.lineplot(data=df_merged,x='step',y='halite' ,hue='player')
plt.ylabel('halite', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("player and board halite time line", fontsize=15)
sns.lineplot(data=df_merged,x='step',y='halite' ,hue='player')
sns.lineplot(data=df,x='step',y='board_halite' ,color='black')
plt.ylabel('halite', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("player cargo time line", fontsize=15)
sns.lineplot(data=df_merged,x='step',y='cargo', hue='player')
plt.ylabel('cargo', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("player cargo and board halite time line", fontsize=15)
sns.lineplot(data=df_merged,x='step',y='cargo', hue='player')
sns.lineplot(data=df,x='step',y='board_halite' ,color='black')
plt.ylabel('cargo', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("total halite (halite + cargo) time line", fontsize=15)
sns.lineplot(data=df_merged,x='step',y='total_halite', hue='player')
plt.ylabel('halite (halite + cargo)', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("cargo percentage (cargo / (halite + cargo)) time line", fontsize=15)
sns.lineplot(data=df_merged,x='step',y='cargo_percentage', hue='player')
plt.ylabel('cargo percentage (cargo / (halite + cargo))', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("total shipyard count time line", fontsize=15)
sns.lineplot(data=df_merged,x='step',y='shipyards', hue='player')
plt.ylabel('shipyard count', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("average shipyard count in game", fontsize=15)
sns.barplot(data=df_merged,x='player',y='shipyards',ci=None)
plt.ylabel('mean shipyard count', fontsize=12)
plt.xlabel('player', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("total ship count time line", fontsize=15)
sns.lineplot(data=df_merged,x='step',y='ships', hue='player')
plt.ylabel('ship count', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("average ship count in game", fontsize=15)
sns.barplot(data=df_merged,x='player',y='ships',ci=None)
plt.ylabel('mean ship count', fontsize=12)
plt.xlabel('player', fontsize=12)
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
plt.title("cargo average(cargo / ship count)  time line", fontsize=15)
sns.lineplot(data=df_merged,x='step',y='cargo_average', hue='player')
plt.ylabel('cargo average', fontsize=12)
plt.show()

