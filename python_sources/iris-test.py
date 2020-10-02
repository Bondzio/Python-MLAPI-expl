# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import warnings
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output

import seaborn as sns
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.

sns.set(style="white", color_codes=True)

iris = pd.read_csv("../input/Iris.csv")
iris.head()

iris["Species"].value_counts()
iris.plot(kind="scatter",x="SepalLengthCm",y="SepalWidthCm")
plt.show()