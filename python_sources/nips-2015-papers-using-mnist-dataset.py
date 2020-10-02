#!/usr/bin/env python
# coding: utf-8

# # Who said MNIST was dead?
# 
# Let's load up the NIPS 2015 papers data and see how many papers used the MNIST dataset.

# In[ ]:


from IPython.display import HTML
import pandas as pd
import re
import sqlite3

con = sqlite3.connect('../input/database.sqlite')


dataset_name = "MNIST"

papers = pd.read_sql_query("""
SELECT *
FROM Papers
WHERE PaperText LIKE '%%%s%%'""" % dataset_name, con)
papers["NumMnistReferences"] = 0
papers["Paper"] = ""

for i in range(len(papers)):
    papers.loc[i, "Paper"] = "<" + "a href='https://papers.nips.cc/paper/" + papers["PdfName"][i] + "'>" + papers["Title"][i] + "<" + "/a>"
    papers.loc[i, "NumMnistReferences"] = len(re.findall(dataset_name, papers["PaperText"][i], re.IGNORECASE))

papers = papers.sort_values("NumMnistReferences", ascending=False)
papers.index = range(1, len(papers)+1)
pd.set_option("display.max_colwidth", -1)

HTML(papers[["Paper", "NumMnistReferences"]].to_html(escape=False))


# 52 of the 403 (12.9%) accepted NIPS papers this year reference the MNIST dataset. This may make it the most commonly used dataset at NIPS.
# 
# We can also look at the context around some of the references:

# In[ ]:


for i in papers.index:
    m = re.search(dataset_name, papers["PaperText"][i], re.IGNORECASE)
    if m:
        p = m.start()
        context = papers["PaperText"][i][p-40:p+40].replace("\n", " ")
        print(papers["Title"][i] + "\n\n" + context + "\n\n================================================================================\n")


# In[ ]:




