#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import time


# In[ ]:


np.random.seed(2)  # reproducible

N_STATES = 6   # the length of the 1 dimensional world
ACTIONS = ['left', 'right']     # available actions
EPSILON = 0.9   # greedy police
ALPHA = 0.1     # learning rate
GAMMA = 0.9    # discount factor
MAX_EPISODES = 13   # maximum episodes
FRESH_TIME = 0.3    # fresh time for one move


# In[ ]:


def build_q_table(n_states, actions):
    table = pd.DataFrame(np.zeros((n_states, len(actions))),columns=actions)
    return table


# In[ ]:


def choose_action(state, q_table):
    actions = q_table.iloc[state,:]
    if(np.random.uniform()>EPSILON or (actions == 0).all()):
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = actions.idxmax()
    return action_name


# In[ ]:


def get_env_feedback(S, A):
    R = 0
    if (A == 'right'):
        if(S == N_STATES-2):
            S_ = 'terminal'
            R = 1
        else:
            S_ = S+1
            R = 0
    else:
        if(S == 0):
            S_ = S
            R = 0
        else:
            S_ = S-1
            R = 0
    return S_,R


# In[ ]:


def update_env(S, episode, step_counter):
    # This is how environment be updated
    env_list = ['-']*(N_STATES-1) + ['T']   # '---------T' our environment
    if S == 'terminal':
        interaction = 'Episode %s: total_steps = %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                                ', end='')
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)


# In[ ]:


def rl():
    q_table = build_q_table(N_STATES,ACTIONS)
    
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_terminated = False
        update_env(S, episode, step_counter)
        
        while is_terminated == False:
            A = choose_action(S,q_table)
            S_,R = get_env_feedback(S,A)
            q_predict = q_table.loc[S, A]
                
            if S_ != 'terminal':
                q_target = R + GAMMA * q_table.iloc[S_, :].max()
            else:
                q_target = R
                is_terminated = True

                
            q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # update
            S = S_  # move to next state

            update_env(S, episode, step_counter+1)
            step_counter += 1
    return q_table


# In[ ]:


q_table = rl()


# In[ ]:


q_table


# In[ ]:




