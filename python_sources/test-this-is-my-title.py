# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

from speedml import Speedml

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))
sml = Speedml('../input/train.csv', 
              '../input/test.csv', 
              target = 'Survived',
              uid = 'PassengerId')
sml.shape()


# Any results you write to the current directory are saved as output.