# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Any results you write to the current directory are saved as output.
df=pd.read_csv('../input/Survey.csv')

cols =pd.Series(df.columns)
cat = cols.map(lambda x: str(x).split(':')[0])[3:]
q = cols.map(lambda x: str(x).split(':')[-1])[3:]

qframe = pd.DataFrame({'q': q,'cat': 'General'})
qframe.loc[q!=cat,'cat']=cat[q!=cat]

qframe['num'] = qframe.cat.str.extract('#([0-9])').fillna(1)
qframe['cat'] = qframe.cat.str.replace(' #[0-9]','').str.replace(' / ','-')

qframe.loc[qframe.cat.str.contains('[oO]ther'),'cat'] = 'Write In'

#Update df columns with integers that represent the index of the qframe
# making finding information about each column and the question it represents
# a simple matter of a single lookup
df.columns = ['start','submit','status']+[str(x) for x in qframe.index]

qframe['sentiment'] = ['Neutral']*len(qframe)
qframe.loc[[4,14,15,16,20,21,22],'sentiment'] = 'Neg'
qframe.loc[[17,18,19,11,12,13],'sentiment'] = 'Pos'
qframe.to_csv('questions.csv')




