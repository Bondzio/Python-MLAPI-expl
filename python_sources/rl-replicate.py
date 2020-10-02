#!/usr/bin/env python
# coding: utf-8

# This replicate is made to enhance my research into Reinforcement Learning. I followed this youtube video to understand it better.
# The code is not mine. Its solely for me to test out
# 
# https://www.youtube.com/watch?v=gWNeMs1Fb8I

# In[ ]:


import numpy as np
import pandas as pd
import time


# In[ ]:


np.random.seed(2)


# In[ ]:


N_STATES = 6
ACTIONS = ['left', 'right'] 
EPSILON = 0.9  
ALPHA = 0.1    
GAMMA = 0.9    
MAX_EPISODES = 13  
FRESH_TIME = 0.3   


# In[ ]:


def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),
        columns=actions,  )

    return table


# In[ ]:


def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):
        action_name = np.random.choice(ACTIONS)
    else: 
        action_name = state_actions.idxmax()
    return action_name


# In[ ]:


def get_env_feedback(S, A):
    if A == 'right':   
        if S == N_STATES - 2: 
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else:   # move left
        R = 0
        if S == 0:
            S_ = S 
        else:
            S_ = S - 1
    return S_, R


# In[ ]:



def update_env(S, episode, step_counter):
  
    env_list = ['-']*(N_STATES-1) + ['T']  
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
    # main part of RL loop
    q_table = build_q_table(N_STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_terminated = False
        update_env(S, episode, step_counter)
        while not is_terminated:

            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)  # take action & get next state and reward
            q_predict = q_table.loc[S, A]
            if S_ != 'terminal':
                q_target = R + GAMMA * q_table.iloc[S_, :].max()   # next state is not terminal
            else:
                q_target = R     # next state is terminal
                is_terminated = True    # terminate this episode

            q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # update
            S = S_  # move to next state

            update_env(S, episode, step_counter+1)
            step_counter += 1
    return q_table


# In[ ]:




if __name__ == "__main__":
    q_table = rl()
    print('\r\nQ-table:\n')
    print(q_table)

