#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('conda install openbabel -c openbabel -y')


# In[ ]:


import pybel

def xyz_to_smiles(fname: str) -> str:
    
    mol = next(pybel.readfile("xyz", fname))

    smi = mol.write(format="smi")

    return smi.split()[0].strip()


# In[ ]:


smi = xyz_to_smiles("../input/structures/dsgdb9nsd_028960.xyz")
print(smi)

