# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

from Bio.PDB import *
import os
import collections
location = '/home/saul/protein/544698_993839_bundle_archive/structures_4_3_2020'
os.chdir(location)
import xpdb   # this is the module described below
import pandas as pd
from collections import Counter
from itertools import groupby
import glob

# read
sloppyparser = PDBParser(PERMISSIVE=True,
                         structure_builder=xpdb.SloppyStructureBuilder())
structure = sloppyparser.get_structure('MD_system', 'M_protein.pdb')

class Atoms:

    def __init__(self):
        self.atomlist= []
        self.atoms = structure.get_atoms()

    def atomdict(self):
        print("atomdict called!!!")
        for atom in self.atoms:
            # print(type(atom))
            self.atomlist.append(atom)

        atomdict = Counter(self.atomlist)
        #print(atomdict)
        self.__atomfreq(atomdict)

    def __atomfreq(self, atomdict):
        atoms = []
        for item, val in enumerate(atomdict):
            # print(" Item {} has the value of {}".format(item, val))
            value = str(val).strip('<>Atom ')
            atoms.append(value)
            # print(value)
            atoms.append(value)

        atomfreq = collections.Counter(atoms)
        sortedatomfreq = {k: v for k, v in sorted(atomfreq.items(), key=lambda item: item[1], reverse=True)}
        #print(sortedatomfreq)
        self.__printAtomFreq(sortedatomfreq, atomfreq)

    def __printAtomFreq(self, sortedatomfreq, atomfreq):
        # Print Atom frequency by descented order
        for item, val in enumerate(sortedatomfreq):
            # print(" Item {} has the value of {}".format(item, val))
            print(" Atom {} has the value of {}".format(val, atomfreq[val]))
            # print(" Item {} has the value of {}".format(item, val))


if __name__ == '__main__':
    proteins= Atoms()
    proteins.atomdict()







