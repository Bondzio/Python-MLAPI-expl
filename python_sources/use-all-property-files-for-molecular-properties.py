#!/usr/bin/env python
# coding: utf-8

# # Use All Property Files for Molecular Properties

# Many participants in the "Predicting Molecular Properties" challenge at https://www.kaggle.com/c/champs-scalar-coupling have generously shared their great kernels (codes).
# 
# Most kernels have incorporated "scalar_coupling_contributions" and "structures" property files and ignored others. A few kernels have incorporated "mulliken_charges" file and ignored others.
# 
# This kernel attempts to prepare "train_plus.csv" and "test_plus.csv" files, which incorporate all property files. The "train_plus.csv" file can be used to train a better model.
# 
# I have used some parts from https://www.kaggle.com/adrianoavelar/bond-calculaltion-lb-0-82 and a few other kernels.
# 
# To run this kernel locally, please uncomment the cells.

# ## Plan the work.

# In[ ]:


from IPython.core.display import display, HTML, Javascript
import IPython.display

html_string = """
<g id="colimg"></g>
"""
js_string = """
require.config({paths:{d3: "https://d3js.org/d3.v4.min"}});
require(["d3"], function(d3) {d3.select("#colimg").append("img").attr("src", "http://lipy.us/img/Columns.png");});
"""
h = display(HTML(html_string))
j = IPython.display.Javascript(js_string)
IPython.display.display_javascript(j)


# - Load structures .
# - Update structures by adding atomics.
# - Update structures by computing bonds.
# - Update structures by merging dipole_moments.
# - Update structures by merging potential_energy.
# - Update structures by merging mulliken_charges.
# - Update structures by merging magnetic_shielding_tensors.
# - Load train|test .
# - Update train|test by merging scalar_coupling_contributions.
# - Update train|test by merging updated structures.
# - Update train|test by computing distance statistics.

# ## Import packages.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\nimport numpy as np\nimport pandas as pd\nimport time\nimport gc\n'''")


# ## Define method to reduce memory.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ndef reduceMemory(df):\n    \n    beg_mem = df.memory_usage().sum() / 1024**2    \n    for col in df.columns:\n        col_type = df[col].dtypes\n        if col_type in ['int16','int32','int64','float16','float32','float64']:\n            c_min = df[col].min()\n            c_max = df[col].max()\n            if str(col_type)[:3] == 'int':\n                if c_min >= np.iinfo(np.int8).min and c_max <= np.iinfo(np.int8).max:\n                    df[col] = df[col].astype(np.int8)\n                elif c_min >= np.iinfo(np.int16).min and c_max <= np.iinfo(np.int16).max:\n                    df[col] = df[col].astype(np.int16)\n                elif c_min >= np.iinfo(np.int32).min and c_max <= np.iinfo(np.int32).max:\n                    df[col] = df[col].astype(np.int32)\n                elif c_min >= np.iinfo(np.int64).min and c_max <= np.iinfo(np.int64).max:\n                    df[col] = df[col].astype(np.int64)  \n            else:\n                if c_min >= np.finfo(np.float16).min and c_max <= np.finfo(np.float16).max:\n                    df[col] = df[col].astype(np.float16)\n                elif c_min >= np.finfo(np.float32).min and c_max <= np.finfo(np.float32).max:\n                    df[col] = df[col].astype(np.float32)\n                else:\n                    df[col] = df[col].astype(np.float64)    \n    end_mem = df.memory_usage().sum() / 1024**2\n    print('Memory usage reduced by {0:0.1f} % to {0:5.2f} Mb'.format(100*(beg_mem-end_mem)/(beg_mem), end_mem))\n        \n    return df\n'''")


# ## Load structures.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ndf0 = pd.read_csv('../input/structures.csv')\n'''")


# ##  Update structures by adding atomics.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ndf0 = pd.merge(df0, pd.DataFrame([['H',0.43,2.2], ['C',0.82,2.55], ['N',0.80,3.04], ['O',0.78,3.44], ['F',0.76,3.98]],\n                    columns=['atom','rad','EN']), how='left', on=['atom']) # radius, electronegativity\n'''")


# ## Update structures by computing bonds.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\nind1 = df0['atom_index'].values\n\nmol1 = df0['molecule_name'].values\npos1 = df0[['x', 'y', 'z']].values\nrad1 = df0['rad'].values\n\nmol2 = mol1\npos2 = pos1\nrad2 = rad1\n\natmx = 28\ndlen = len(df0)\nrec1 = np.arange(dlen)\nbond = np.zeros((dlen+1, atmx+1), dtype=np.int8)\nbdis = np.zeros((dlen+1, atmx+1), dtype=np.float32)\n\nfor atmi in range(atmx-1):\n    \n    mol2 = np.roll(mol2, -1, axis=0)\n    pos2 = np.roll(pos2, -1, axis=0)\n    rad2 = np.roll(rad2, -1, axis=0)\n  \n    mask = np.where(mol1==mol2, 1, 0)\n    dist = np.linalg.norm(pos1 - pos2, axis=1) * mask\n    chec = np.where(np.logical_and(dist > 0.0001, dist < rad1 + rad2), 1, 0)  \n    \n    ind1 = ind1\n    ind2 = ind1 + atmi + 1\n    ind2 = np.where(np.logical_or(ind2 > atmx, mask==0), atmx, ind2)\n    \n    rec1 = rec1\n    rec2 = rec1 + atmi + 1\n    rec2 = np.where(np.logical_or(rec2 > dlen, mask==0), dlen, rec2)\n\n    bond[(rec1, ind2)] = chec\n    bond[(rec2, ind1)] = chec\n    bdis[(rec1, ind2)] = dist\n    bdis[(rec2, ind1)] = dist\n\nbond = np.delete(bond, axis=0, obj=-1) # Delete dummy row.\nbond = np.delete(bond, axis=1, obj=-1) # Delete dummy col.\n\nbdis = np.delete(bdis, axis=0, obj=-1) # Delete dummy row.\nbdis = np.delete(bdis, axis=1, obj=-1) # Delete dummy col.\n\nbnum = [[ i for i,x in enumerate(row) if x] for row in bond ]\nbqty = [ len(x) for x in bnum ]\nblen = [[ dist for i,dist in enumerate(row) if i in bnum[j] ] for j,row in enumerate(bdis)]\n\nblen_avg = [ np.mean(x) for x in blen ]\nblen_med = [ np.median(x) for x in blen ]\nblen_std = [ np.std(x) for x in blen ]\n\ndf0 = df0.join(pd.DataFrame({'bond_num':bqty, 'bondleng_avg':blen_avg, 'bondleng_med':blen_med, 'bondleng_std':blen_std}))\n'''")


# ## Upadte structures by merging dipole_moments.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ndf0 = pd.merge(df0, pd.read_csv('../input/dipole_moments.csv'), how='left', on=['molecule_name'])\n'''")


# ## Update structures by merging potential_energy.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ndf0 = pd.merge(df0, pd.read_csv('../input/potential_energy.csv'), how='left', on=['molecule_name'])\n'''")


# ## Update structures by merging mulliken_charges.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ndf0 = pd.merge(df0, pd.read_csv('../input/mulliken_charges.csv'), how='left', on=['molecule_name','atom_index'])\n'''")


# ## Update structures by merging magnetic_shielding_tensors.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ndf0 = pd.merge(df0, pd.read_csv('../input/magnetic_shielding_tensors.csv'), how='left', on=['molecule_name','atom_index'])\n'''")


# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ndf0 = reduceMemory(df0)\n'''")


# ## Load train|test.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ntrain = pd.read_csv('../input/train.csv')\ntest = pd.read_csv('../input/test.csv')\n'''")


# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ntrain = reduceMemory(train)\ntest = reduceMemory(test)\n'''")


# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ntrain.head()\n'''")


# ## Update train|test by merging scalar_coupling_contributions.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ndf1 = pd.read_csv('../input/scalar_coupling_contributions.csv')\ntrain = pd.merge(train, df1, how='left', on=['molecule_name','atom_index_0','atom_index_1','type'])\ntest = pd.merge(test, df1, how='left', on=['molecule_name','atom_index_0','atom_index_1','type'])\n'''")


# ## Update train|test by merging updated structures.

# In[ ]:


get_ipython().run_cell_magic('capture', '', '\'\'\'\ndf0.columns = [(c if (c=="molecule_name") else c+"_0") for c in df0.columns]\ntrain = pd.merge(train, df0, how=\'left\', on=[\'molecule_name\',\'atom_index_0\'])\ntest = pd.merge(test, df0, how=\'left\', on=[\'molecule_name\',\'atom_index_0\'])\ndf0.columns = [(c if (c=="molecule_name") else c.replace("_0","_1")) for c in df0.columns]\ntrain = pd.merge(train, df0, how=\'left\', on=[\'molecule_name\',\'atom_index_1\'])\ntest = pd.merge(test, df0, how=\'left\', on=[\'molecule_name\',\'atom_index_1\'])\n\'\'\'')


# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ntrain = reduceMemory(train)\ntest = reduceMemory(test)\n'''")


# ## Update train|test by computing distance statistics.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ndef addStat(df):\n    \n    df['dist'] = np.linalg.norm( df[['x_0','y_0','z_0']].values - df[['x_1','y_1','z_1']].values, axis=1 )\n    df['dist'] = 1/(df['dist']**3)\n    for w in ['x','y','z']:\n        df['dist_'+w] = (df[w+'_0'] - df[w+'_1']) ** 2\n    df['type_0'] = df['type'].apply(lambda x: x[0])\n    \n    df['molecule_couples'] = df.groupby('molecule_name')['id'].transform('count')\n    df['atom_index_0_couples'] = df.groupby(['molecule_name','atom_index_0'])['id'].transform('count')\n    df['atom_index_1_couples'] = df.groupby(['molecule_name','atom_index_1'])['id'].transform('count')\n    \n    for zact in ['min','max','mean','std']:\n        df['molecule_dist_'+zact] = df.groupby('molecule_name')['dist'].transform(zact)\n        \n        for zfor in ['dist']: # ['x_1','y_1','z_1','dist']:\n            for zato in ['atom_index_0','atom_index_1','type','atom_0','atom_1','type_0']:\n                try:\n                    df[f'molecule_'+zato+'_'+zfor+'_'+zact] = df.groupby(['molecule_name',zato])[zfor].transform(zact)\n                except:\n                    df[f'molecule_'+zato+'_'+zfor+'_'+zact] = 0\n                try:\n                    df[f'molecule_'+zato+'_'+zfor+'_'+zact+'_dif'] = df[f'molecule_'+zato+'_'+zfor+'_'+zact] - df[zfor]\n                except:\n                    df[f'molecule_'+zato+'_'+zfor+'_'+zact+'_dif'] = 0\n                try:\n                    df[f'molecule_'+zato+'_'+zfor+'_'+zact+'_div'] = df[f'molecule_'+zato+'_'+zfor+'_'+zact] / df[zfor]\n                except:\n                    df[f'molecule_'+zato+'_'+zfor+'_'+zact+'_div'] = 0\n              \n    return df\n'''")


# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ntrain = addStat(train)\ntest = addStat(test)\n'''")


# In[ ]:


get_ipython().run_cell_magic('capture', '', '\'\'\'\nprint("Dataset                   Rows   Columns")\nprint(\'{0:20s}{1:10d}{2:10d}\'.format("df0", df0.shape[0], df0.shape[1]))\nprint(\'{0:20s}{1:10d}{2:10d}\'.format("df1", df1.shape[0], df1.shape[1]))\nprint(\'{0:20s}{1:10d}{2:10d}\'.format("train", train.shape[0], train.shape[1]))\nprint(\'{0:20s}{1:10d}{2:10d}\'.format("test", test.shape[0], test.shape[1]))\n\'\'\'')


# ## Save train|test.

# In[ ]:


get_ipython().run_cell_magic('capture', '', "'''\ntrain.to_csv('train_plus.csv', index=True)\ntest.to_csv('test_plus.csv', index=True)\n'''")


# In[ ]:


# This is to register this kernel in this specific challenge.
import pandas as pd
pd.read_csv('../input/sample_submission.csv')[:10]

