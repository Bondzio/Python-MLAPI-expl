#!/usr/bin/env python
# coding: utf-8

# # Setup
# We install deeplabcut without dependencies and manually add a few since it breaks a lot of Kaggle's setup

# In[2]:


get_ipython().system('pip install -qq ruamel.yaml easydict')


# In[3]:


get_ipython().system('pip install -qq --no-deps git+https://github.com/AlexEMG/DeepLabCut')


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
import os
os.environ["DLClight"]="True"
os.environ["Colab"]="True"
import deeplabcut as dlc


# In[27]:


import yaml, shutil
exp_dir = '../input/repository/AlexEMG-DeepLabCut-4306877/examples/Reaching-Mackenzie-2018-08-30'
get_ipython().system('rm -rf Reaching-Mackenzie-2018-08-30')
shutil.copytree(exp_dir, 'Reaching-Mackenzie-2018-08-30')
get_ipython().system('cp ../input/repository/AlexEMG-DeepLabCut-4306877/deeplabcut/pose_cfg.yaml pose_cfg.yaml')
exp_dir = 'Reaching-Mackenzie-2018-08-30'
old_path_config_file = os.path.join(exp_dir, 'config.yaml')
path_config_file = 'config.yaml'

# patch and make a new one    
with open(old_path_config_file, 'r') as f:
    config_data = yaml.load(f)
    f.seek(0)
    config_lines = f.readlines()
with open(path_config_file, 'w') as f:
    patched_lines = [c_line.replace('WILL BE AUTOMATICALLY UPDATED BY DEMO CODE', exp_dir)
                    for c_line in config_lines]
    f.writelines(patched_lines)
get_ipython().system('cat {path_config_file}')
old_path_config_file = path_config_file


# In[28]:


# If you are using the demo data (i.e. examples/Reaching-Mackenzie-2018-08-30/), first delete the folder called dlc-models! 
#Then, run this cell. 
dlc.create_training_dataset(path_config_file)


# In[29]:


#let's also change the display and save_iters just in case Colab takes away the GPU... 
#if that happens, you can reload from a saved point. Typically, you want to train to 200,000 + iterations.
#more info and there are more things you can set: https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#g-train-the-network

dlc.train_network(path_config_file, shuffle=1, displayiters=10,saveiters=500)

#this will run until you stop it (CTRL+C), or hit "STOP" icon, or when it hits the end (default, 1.03M iterations). 
#Whichever you chose, you will see what looks like an error message, but it's not an error - don't worry....


# In[30]:


get_ipython().run_line_magic('matplotlib', 'inline')
dlc.evaluate_network(path_config_file)#,plotting=True)
# Here you want to see a low pixel error! Of course, it can only be as good as the labeler, so be sure your labels are good!


# In[8]:


videofile_path = [os.path.join(exp_dir, 'videos/MovieS2_Perturbation_noLaser_compressed.avi')] #Enter the list of videos to analyze.
dlc.analyze_videos(path_config_file, videofile_path)


# In[31]:


dlc.create_labeled_video(path_config_file,videofile_path)


# In[32]:


#for making interactive plots.
dlc.plot_trajectories(path_config_file, videofile_path)


# In[ ]:




