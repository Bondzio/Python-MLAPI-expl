#!/usr/bin/env python
# coding: utf-8

# ## Selectively Hiding Code ##
# 
# Suppose you have 500 lines of a dictionary definition, which if displayed on default 
# would probably overwhelm your user.  This is a problem I'm facing with the [US Income for Select States][1], although for that Kernel I chose to hide all the cells on default.  This is different.  Suppose
# you want the user to dictate the input cell.
# 
# <button onclick="javascript:toggleInput(0)" class="button">Show Code</button>
# 
# 
#   [1]: https://www.kaggle.com/mchirico/d/census/2015-american-community-survey/us-income-for-select-states

# In[ ]:


from IPython.display import HTML
from IPython.display import display
baseCodeHide="""
<style>
.button {
    background-color: #008CBA;;
    border: none;
    color: white;
    padding: 8px 22px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
}
</style>
 <script>
   // Assume 3 input cells. Manage from here.
   var divTag0 = document.getElementsByClassName("input")[0]
   var displaySetting0 = divTag0.style.display;
   // Default display - set to 'none'.  To hide, set to 'block'.
   // divTag0.style.display = 'block';
   divTag0.style.display = 'none';
   
   var divTag1 = document.getElementsByClassName("input")[1]
   var displaySetting1 = divTag1.style.display;
   // Default display - set to 'none'.  To hide, set to 'block'.
      divTag1.style.display = 'block';
   //divTag1.style.display = 'none';
   
   var divTag2 = document.getElementsByClassName("input")[2]
   var displaySetting2 = divTag2.style.display;
   // Default display - set to 'none'.  To hide, set to 'none'.
   divTag2.style.display = 'block';
   //divTag2.style.display = 'none';
 
    function toggleInput(i) { 
      var divTag = document.getElementsByClassName("input")[i]
      var displaySetting = divTag.style.display;
     
      if (displaySetting == 'block') { 
         divTag.style.display = 'none';
       }
      else { 
         divTag.style.display = 'block';
       } 
  }  
  </script>
  <!-- <button onclick="javascript:toggleInput(0)" class="button">Show Code</button> -->
"""
h=HTML(baseCodeHide)


display(h)
print("Code above produced me...click Show Code to see it.")


# ## Next Section... ##
# 
# Here you may some conversation about code, but you don't
# want to pollute the screen, until the user is ready to see it.
# 
# Note...the input for the **toggleInput(1)** .. the next input will be **toggleInput(2)**
# 
# <button onclick="javascript:toggleInput(1)" class="button">Toggle Code</button>

# In[ ]:




# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory





from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


from IPython.display import HTML
from IPython.display import display

cellNum=2
cellDisp='none'  # Other option is 'block'
cell="""
<script>
   var divTag = document.getElementsByClassName("input")[%s]
   var displaySetting = divTag.style.display;
   // Default display - set to 'none'.  To hide, set to 'block'.
   // divTag.style.display = 'block';
   divTag.style.display = '%s';
<script>
<!-- <button onclick="javascript:toggleInput(%s)" class="button">Toggle Code</button> -->
""" % (cellNum,'none',cellNum)
h=HTML(cell)
display(h)


# Last Line.... not sure why this isn't being displayed...
# 
# 
# 

# In[ ]:


from IPython.display import HTML
from IPython.display import display
# Last line.. this is a hack
# so that the browser can expand. You'll need to adjust
br="<br>"*1000
HTML(br)

