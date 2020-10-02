#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# Create my first agent

# In[ ]:


get_ipython().run_cell_magic('writefile', 'submission.py', '\n# Imports helper functions\nfrom kaggle_environments.envs.halite.helpers import *\n\n# Returns best direction to move from one position (fromPos) to another (toPos)\n# Example: If I\'m at pos 0 and want to get to pos 55, which direction should I choose?\ndef getDirTo(fromPos, toPos, size):\n    fromX, fromY = divmod(fromPos[0],size), divmod(fromPos[1],size)\n    toX, toY = divmod(toPos[0],size), divmod(toPos[1],size)\n    if fromY < toY: return ShipAction.NORTH\n    if fromY > toY: return ShipAction.SOUTH\n    if fromX < toX: return ShipAction.EAST\n    if fromX > toX: return ShipAction.WEST\n\n# Directions a ship can move\ndirections = [ShipAction.NORTH, ShipAction.EAST, ShipAction.SOUTH, ShipAction.WEST]\n\n# Will keep track of whether a ship is collecting halite or carrying cargo to a shipyard\nship_states = {}\n\n# Returns the commands we send to our ships and shipyards\ndef agent(obs, config):\n    size = config.size\n    board = Board(obs, config)\n    me = board.current_player\n\n    # If there are no ships, use first shipyard to spawn a ship.\n    if len(me.ships) == 0 and len(me.shipyards) > 0:\n        me.shipyards[0].next_action = ShipyardAction.SPAWN\n\n    # If there are no shipyards, convert first ship into shipyard.\n    if len(me.shipyards) == 0 and len(me.ships) > 0:\n        me.ships[0].next_action = ShipAction.CONVERT\n    \n    for ship in me.ships:\n        if ship.next_action == None:\n            \n            ### Part 1: Set the ship\'s state \n            if ship.halite < 200: # If cargo is too low, collect halite\n                ship_states[ship.id] = "COLLECT"\n            if ship.halite > 500: # If cargo gets very big, deposit halite\n                ship_states[ship.id] = "DEPOSIT"\n                \n            ### Part 2: Use the ship\'s state to select an action\n            if ship_states[ship.id] == "COLLECT":\n                # If halite at current location running low, \n                # move to the adjacent square containing the most halite\n                if ship.cell.halite < 100:\n                    neighbors = [ship.cell.north.halite, ship.cell.east.halite, \n                                 ship.cell.south.halite, ship.cell.west.halite]\n                    best = max(range(len(neighbors)), key=neighbors.__getitem__)\n                    ship.next_action = directions[best]\n            if ship_states[ship.id] == "DEPOSIT":\n                # Move towards shipyard to deposit cargo\n                direction = getDirTo(ship.position, me.shipyards[0].position, size)\n                if direction: ship.next_action = direction\n                \n    return me.next_actions')


# Play my agent against three random agents. My agent is in the top left corner of the screen.

# In[ ]:


from kaggle_environments import make
env = make("halite", debug=True)
env.run(["submission.py", "random", "random", "random"])
env.render(mode="ipython", width=800, height=600)


# In[ ]:




