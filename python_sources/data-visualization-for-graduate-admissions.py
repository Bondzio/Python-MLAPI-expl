#!/usr/bin/env python
# coding: utf-8

# **Importing Dataset, Getting some information about our Dataset**

# In[ ]:


#Importing Dataset, Getting some information about our Dataset

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)

df = pd.read_csv("../input/Admission_Predict.csv")

print(df.head())
print(df.columns)


# **Boxplots**

# In[ ]:


df.drop(["Serial No.", "Research"], axis = 1).describe()

sns.boxplot("TOEFL Score", data = df)
plt.xlabel("TOEFL Score")
plt.show()
sns.boxplot("GRE Score", data = df)
plt.xlabel("GRE Score")
plt.show()
sns.boxplot("CGPA", data = df)
plt.xlabel("CGPA")
plt.show()
sns.boxplot("SOP", data = df)
plt.xlabel("SOP")
plt.show()
sns.boxplot("LOR ", data = df)
plt.xlabel("LOR ")
plt.show()


# **Better results for people who have conducted Research**

# In[ ]:


sns.boxplot(x = "Research", y = "TOEFL Score", data = df)
plt.ylabel("TOEFL Score")
plt.show()
sns.boxplot(x = "Research", y = "GRE Score", data = df)
plt.ylabel("GRE Score")
plt.show()
sns.boxplot(x = "Research", y = "CGPA", data = df)
plt.ylabel("CGPA")
plt.show()
sns.boxplot(x = "Research", y = "SOP", data = df)
plt.ylabel("SOP")
plt.show()
sns.boxplot(x = "Research", y = "LOR ", data = df)
plt.ylabel("LOR ")
plt.show()


# **Linear Regression Plots**

# In[ ]:


sns.lmplot(x = "TOEFL Score", y = "Chance of Admit ", data = df, markers = ".", scatter_kws = {"color":"red"})
plt.show()
sns.lmplot(x = "GRE Score", y = "Chance of Admit ", data = df, markers = ".")
plt.show()
sns.lmplot(x = "CGPA", y = "Chance of Admit ", data = df, markers = ".", scatter_kws = {"color":"orange"})
plt.show()
sns.lmplot(x = "SOP", y = "Chance of Admit ", data = df, markers = ".", scatter_kws = {"color":"magenta"})
plt.show()
sns.lmplot(x = "LOR ", y = "Chance of Admit ", data = df, markers = ".", scatter_kws = {"color":"brown"})
plt.show()


# **Again, Researchers have better results**

# In[ ]:


sns.lmplot(x = "TOEFL Score", y = "Chance of Admit ", data = df, hue = "Research", markers = ".")
plt.show()
sns.lmplot(x = "GRE Score", y = "Chance of Admit ", data = df, hue = "Research", markers = ".")
plt.show()
sns.lmplot(x = "CGPA", y = "Chance of Admit ", data = df, hue = "Research", markers = ".")
plt.show()
sns.lmplot(x = "SOP", y = "Chance of Admit ", data = df, hue = "Research", markers = ".")
plt.show()
sns.lmplot(x = "LOR ", y = "Chance of Admit ", data = df, hue = "Research", markers = ".")
plt.show()


# **General Pair-Plot**

# In[ ]:


sns.pairplot(df.drop(["Serial No.", "Research"], axis = 1))
plt.show()

