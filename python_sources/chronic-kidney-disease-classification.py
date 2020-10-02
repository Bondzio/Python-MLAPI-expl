#!/usr/bin/env python
# coding: utf-8

# #  <font color=black>Chronic Kidney Disease classification</font>

# The task is to classify patients into two groups. In the first group there are patients who have Chronic Kidney Disease and in the second patients without this disease. Initial dataset contains personal parameters such as age, blood pessure etc. And the last parameter is the class of particular patient, which shows presence or absence of Chronic Kidney Disease (ckd/notckd).

# In[ ]:


#importing libraries
import numpy as np
import pandas as pd
from pandas import DataFrame,Series
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn import model_selection
from sklearn.model_selection import StratifiedKFold, StratifiedShuffleSplit
from sklearn.feature_selection import RFECV,SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR, SVC, LinearSVC

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB

from IPython.core.display import display, HTML


# 
# 
# ##  <font color=black>About dataset</font>
# 
# I downloaded dataset from "UCI Machine Learning Repository": 
# https://archive.ics.uci.edu/ml/datasets/chronic_kidney_disease
# 
# Below you can see description of this dataset:
#     
# 
# 1. Title: Early stage of Indians Chronic Kidney Disease(CKD)
# 
# 2. Source Information:
#    (a) Source: 
# 			Dr.P.Soundarapandian.M.D.,D.M
# 			(Senior Consultant Nephrologist), 
# 			Apollo  Hospitals, 
# 			Managiri,
# 			Madurai Main Road, 
# 			Karaikudi,
# 			Tamilnadu,
# 			India.
#             
#    (b) Creator: 
# 			L.Jerlin Rubini(Research Scholar)
# 			Alagappa University,
# 			EmailId   :jel.jerlin@gmail.com
# 			ContactNo :+91-9597231281
# 
#    (c) Guided by: 
# 			Dr.P.Eswaran Assistant Professor,
# 			Department of Computer Science and Engineering,
# 			Alagappa University,
# 			Karaikudi,
# 			Tamilnadu,
# 			India.
# 			Emailid:eswaranperumal@gmail.com
# 
#    (d) Date     : July 2015
#    
# <p style="white-space:pre">
# 3.Relevant Information:
# 			age		-	age
# 			bp		-	blood pressure
# 			sg		-	specific gravity
# 			al		-   albumin
# 			su		-	sugar
# 			rbc		-	red blood cells
# 			pc		-	pus cell
# 			pcc		-	pus cell clumps
# 			ba		-	bacteria
# 			bgr		-	blood glucose random
# 			bu		-	blood urea
# 			sc		-	serum creatinine
# 			sod		-	sodium
# 			pot		-	potassium
# 			hemo		-	hemoglobin
# 			pcv		-	packed cell volume
# 			wc		-	white blood cell count
# 			rc		-	red blood cell count
# 			htn		-	hypertension
# 			dm		-	diabetes mellitus
# 			cad		-	coronary artery disease
# 			appet		-	appetite
# 			pe		-	pedal edema
# 			ane		-	anemia
# 			class		-	class	
# </p>
# 
# 4.Number of Instances:  400 (250 CKD, 150 notckd)
# 
# 5.Number of Attributes: 24 + class = 25 ( 11  numeric ,14  nominal) 
# 
# <p style="white-space:pre">
# 6.Attribute Information :
#  	1.Age(numerical)
#   	  	age in years
#  	2.Blood Pressure(numerical)
# 	       	bp in mm/Hg
#  	3.Specific Gravity(nominal)
# 	  	sg - (1.005,1.010,1.015,1.020,1.025)
#  	4.Albumin(nominal)
# 		al - (0,1,2,3,4,5)
#  	5.Sugar(nominal)
# 		su - (0,1,2,3,4,5)
#  	6.Red Blood Cells(nominal)
# 		rbc - (normal,abnormal)
#  	7.Pus Cell (nominal)
# 		pc - (normal,abnormal)
#  	8.Pus Cell clumps(nominal)
# 		pcc - (present,notpresent)
#  	9.Bacteria(nominal)
# 		ba  - (present,notpresent)
#  	10.Blood Glucose Random(numerical)		
# 		bgr in mgs/dl
#  	11.Blood Urea(numerical)	
# 		bu in mgs/dl
#  	12.Serum Creatinine(numerical)	
# 		sc in mgs/dl
#  	13.Sodium(numerical)
# 		sod in mEq/L
#  	14.Potassium(numerical)	
# 		pot in mEq/L
#  	15.Hemoglobin(numerical)
# 		hemo in gms
#  	16.Packed  Cell Volume(numerical)
#  	17.White Blood Cell Count(numerical)
# 		wc in cells/cumm
#  	18.Red Blood Cell Count(numerical)	
# 		rc in millions/cmm
#  	19.Hypertension(nominal)	
# 		htn - (yes,no)
#  	20.Diabetes Mellitus(nominal)	
# 		dm - (yes,no)
#  	21.Coronary Artery Disease(nominal)
# 		cad - (yes,no)
#  	22.Appetite(nominal)	
# 		appet - (good,poor)
#  	23.Pedal Edema(nominal)
# 		pe - (yes,no)	
#  	24.Anemia(nominal)
# 		ane - (yes,no)
#  	25.Class (nominal)		
# 		class - (ckd,notckd)
# </p>
# 7. Missing Attribute Values: Yes(Denoted by "?")
# 
# 8. Class Distribution: ( 2 classes)
#     		Class 	  Number of instances
#     		ckd          	  250
#     		notckd       	  150   
# </span>

# In[ ]:


#create a list from intial dataset
lst_f = ['@relation Chronic_Kidney_Disease\n',
 '\n',
 "@attribute 'age' numeric\n",
 "@attribute 'bp'  numeric\n",
 "@attribute 'sg' {1.005,1.010,1.015,1.020,1.025}\n",
 "@attribute 'al' {0,1,2,3,4,5}  \n",
 "@attribute 'su' {0,1,2,3,4,5}  \n",
 "@attribute 'rbc' {normal,abnormal}\n",
 "@attribute 'pc' {normal,abnormal} \n",
 "@attribute 'pcc' {present,notpresent}\n",
 "@attribute 'ba' {present,notpresent}\n",
 "@attribute 'bgr'  numeric\n",
 "@attribute 'bu' numeric\n",
 "@attribute 'sc' numeric\n",
 "@attribute 'sod' numeric\n",
 "@attribute 'pot' numeric\n",
 "@attribute 'hemo' numeric\n",
 "@attribute 'pcv' numeric\n",
 "@attribute 'wbcc' numeric\n",
 "@attribute 'rbcc' numeric\n",
 "@attribute 'htn' {yes,no}\n",
 "@attribute 'dm' {yes,no}\n",
 "@attribute 'cad' {yes,no}\n",
 "@attribute 'appet' {good,poor}\n",
 "@attribute 'pe' {yes,no} \n",
 "@attribute 'ane' {yes,no}\n",
 "@attribute 'class' {ckd,notckd}\n",
 '\n',
 '@data\n',
 '48,80,1.020,1,0,?,normal,notpresent,notpresent,121,36,1.2,?,?,15.4,44,7800,5.2,yes,yes,no,good,no,no,ckd\n',
 '7,50,1.020,4,0,?,normal,notpresent,notpresent,?,18,0.8,?,?,11.3,38,6000,?,no,no,no,good,no,no,ckd\n',
 '62,80,1.010,2,3,normal,normal,notpresent,notpresent,423,53,1.8,?,?,9.6,31,7500,?,no,yes,no,poor,no,yes,ckd\n',
 '48,70,1.005,4,0,normal,abnormal,present,notpresent,117,56,3.8,111,2.5,11.2,32,6700,3.9,yes,no,no,poor,yes,yes,ckd\n',
 '51,80,1.010,2,0,normal,normal,notpresent,notpresent,106,26,1.4,?,?,11.6,35,7300,4.6,no,no,no,good,no,no,ckd\n',
 '60,90,1.015,3,0,?,?,notpresent,notpresent,74,25,1.1,142,3.2,12.2,39,7800,4.4,yes,yes,no,good,yes,no,ckd\n',
 '68,70,1.010,0,0,?,normal,notpresent,notpresent,100,54,24.0,104,4.0,12.4,36,?,?,no,no,no,good,no,no,ckd\n',
 '24,?,1.015,2,4,normal,abnormal,notpresent,notpresent,410,31,1.1,?,?,12.4,44,6900,5,no,yes,no,good,yes,no,ckd\n',
 '52,100,1.015,3,0,normal,abnormal,present,notpresent,138,60,1.9,?,?,10.8,33,9600,4.0,yes,yes,no,good,no,yes,ckd\n',
 '53,90,1.020,2,0,abnormal,abnormal,present,notpresent,70,107,7.2,114,3.7,9.5,29,12100,3.7,yes,yes,no,poor,no,yes,ckd\n',
 '50,60,1.010,2,4,?,abnormal,present,notpresent,490,55,4.0,?,?,9.4,28,?,?,yes,yes,no,good,no,yes,ckd\n',
 '63,70,1.010,3,0,abnormal,abnormal,present,notpresent,380,60,2.7,131,4.2,10.8,32,4500,3.8,yes,yes,no,poor,yes,no,ckd\n',
 '68,70,1.015,3,1,?,normal,present,notpresent,208,72,2.1,138,5.8,9.7,28,12200,3.4,yes,yes,yes,poor,yes,no,ckd\n',
 '68,70,?,?,?,?,?,notpresent,notpresent,98,86,4.6,135,3.4,9.8,?,?,?,yes,yes,yes,poor,yes,no,ckd\n',
 '68,80,1.010,3,2,normal,abnormal,present,present,157,90,4.1,130,6.4,5.6,16,11000,2.6,yes,yes,yes,poor,yes,no,ckd\n',
 '40,80,1.015,3,0,?,normal,notpresent,notpresent,76,162,9.6,141,4.9,7.6,24,3800,2.8,yes,no,no,good,no,yes,ckd\n',
 '47,70,1.015,2,0,?,normal,notpresent,notpresent,99,46,2.2,138,4.1,12.6,?,?,?,no,no,no,good,no,no,ckd\n',
 '47,80,?,?,?,?,?,notpresent,notpresent,114,87,5.2,139,3.7,12.1,?,?,?,yes,no,no,poor,no,no,ckd\n',
 '60,100,1.025,0,3,?,normal,notpresent,notpresent,263,27,1.3,135,4.3,12.7,37,11400,4.3,yes,yes,yes,good,no,no,ckd\n',
 '62,60,1.015,1,0,?,abnormal,present,notpresent,100,31,1.6,?,?,10.3,30,5300,3.7,yes,no,yes,good,no,no,ckd\n',
 '61,80,1.015,2,0,abnormal,abnormal,notpresent,notpresent,173,148,3.9,135,5.2,7.7,24,9200,3.2,yes,yes,yes,poor,yes,yes,ckd\n',
 '60,90,?,?,?,?,?,notpresent,notpresent,?,180,76,4.5,?,10.9,32,6200,3.6,yes,yes,yes,good,no,no,ckd\n',
 '48,80,1.025,4,0,normal,abnormal,notpresent,notpresent,95,163,7.7,136,3.8,9.8,32,6900,3.4,yes,no,no,good,no,yes,ckd\n',
 '21,70,1.010,0,0,?,normal,notpresent,notpresent,?,?,?,?,?,?,?,?,?,no,no,no,poor,no,yes,ckd\n',
 '42,100,1.015,4,0,normal,abnormal,notpresent,present,?,50,1.4,129,4.0,11.1,39,8300,4.6,yes,no,no,poor,no,no,ckd\n',
 '61,60,1.025,0,0,?,normal,notpresent,notpresent,108,75,1.9,141,5.2,9.9,29,8400,3.7,yes,yes,no,good,no,yes,ckd\n',
 '75,80,1.015,0,0,?,normal,notpresent,notpresent,156,45,2.4,140,3.4,11.6,35,10300,4,yes,yes,no,poor,no,no,ckd\n',
 '69,70,1.010,3,4,normal,abnormal,notpresent,notpresent,264,87,2.7,130,4.0,12.5,37,9600,4.1,yes,yes,yes,good,yes,no,ckd\n',
 '75,70,?,1,3,?,?,notpresent,notpresent,123,31,1.4,?,?,?,?,?,?,no,yes,no,good,no,no,ckd\n',
 '68,70,1.005,1,0,abnormal,abnormal,present,notpresent,?,28,1.4,?,?,12.9,38,?,?,no,no,yes,good,no,no,ckd\n',
 '?,70,?,?,?,?,?,notpresent,notpresent,93,155,7.3,132,4.9,?,?,?,?,yes, yes,no,good,no,no,ckd\n',
 '73,90,1.015,3,0,?,abnormal,present,notpresent,107,33,1.5,141,4.6,10.1,30,7800,4,no,no,no,poor,no,no,ckd\n',
 '61,90,1.010,1,1,?,normal,notpresent,notpresent,159,39,1.5,133,4.9,11.3,34,9600,4.0,yes,yes,no,poor,no,no,ckd\n',
 '60,100,1.020,2,0,abnormal,abnormal,notpresent,notpresent,140,55,2.5,?,?,10.1,29,?,?,yes,no,no,poor,no,no,ckd\n',
 '70,70,1.010,1,0,normal,?,present,present,171,153,5.2,?,?,?,?,?,?,no,yes,no,poor,no,no,ckd\n',
 '65,90,1.020,2,1,abnormal,normal,notpresent,notpresent,270,39,2.0,?,?,12.0,36,9800,4.9,yes,yes,no,poor,no,yes,ckd\n',
 '76,70,1.015,1,0,normal,normal,notpresent,notpresent,92,29,1.8,133,3.9,10.3,32,?,?,yes,no,no,good,no,no,ckd\n',
 '72,80,?,?,?,?,?,notpresent,notpresent,137,65,3.4,141,4.7,9.7,28,6900,2.5,yes,yes,no,poor,no,yes,ckd\t\n',
 '69,80,1.020,3,0,abnormal,normal,notpresent,notpresent,?,103,4.1,132,5.9,12.5,?,?,?,yes,no,no,good,no,no,ckd\n',
 '82,80,1.010,2,2,normal,?,notpresent,notpresent,140,70,3.4,136,4.2,13.0,40,9800,4.2,yes,yes,no,good,no,no,ckd\n',
 '46,90,1.010,2,0,normal,abnormal,notpresent,notpresent,99,80,2.1,?,?,11.1,32,9100,4.1,yes,no,\tno,good,no,no,ckd\n',
 '45,70,1.010,0,0,?,normal,notpresent,notpresent,?,20,0.7,?,?,?,?,?,?,no,no,no,good,yes,no,ckd\n',
 '47,100,1.010,0,0,?,normal,notpresent,notpresent,204,29,1.0,139,4.2,9.7,33,9200,4.5,yes,no,no,good,no,yes,ckd\n',
 '35,80,1.010,1,0,abnormal,?,notpresent,notpresent,79,202,10.8,134,3.4,7.9,24,7900,3.1,no,yes,no,good,no,no,ckd\n',
 '54,80,1.010,3,0,abnormal,abnormal,notpresent,notpresent,207,77,6.3,134,4.8,9.7,28,?,?,yes,yes,no,poor,yes,no,ckd\n',
 '54,80,1.020,3,0,?,abnormal,notpresent,notpresent,208,89,5.9,130,4.9,9.3,?,?,?,yes,yes,no,poor,yes,no,ckd\n',
 '48,70,1.015,0,0,?,normal,notpresent,notpresent,124,24,1.2,142,4.2,12.4,37,6400,4.7,no,yes,no,good,no,no,ckd\n',
 '11,80,1.010,3,0,?,normal,notpresent,notpresent,?,17,0.8,?,?,15.0,45,8600,?,no,no,no,good,no,no,ckd\n',
 '73,70,1.005,0,0,normal,normal,notpresent,notpresent,70,32,0.9,125,4.0,10.0,29,18900,3.5,yes,yes,no,good,yes,no,ckd\n',
 '60,70,1.010,2,0,normal,abnormal,present,notpresent,144,72,3.0,?,?,9.7,29,21600,3.5,yes,yes,no,poor,no,yes,ckd\n',
 '53,60,?,?,?,?,?,notpresent,notpresent,91,114,3.25,142,4.3,8.6,28,11000,3.8,yes,yes,no,poor,yes,yes,ckd\n',
 '54,100,1.015,3,0,?,normal,present,notpresent,162,66,1.6,136,4.4,10.3,33,?,?,yes,yes,no,poor,yes,no,ckd\n',
 '53,90,1.015,0,0,?,normal,notpresent,notpresent,?,38,2.2,?,?,10.9,34,4300,3.7,no,no,no,poor,no,yes,ckd\n',
 '62,80,1.015,0,5,?,?,notpresent,notpresent,246,24,1.0,?,?,13.6,40,8500,4.7,yes,yes,no,good,no,no,ckd\n',
 '63,80,1.010,2,2,normal,?,notpresent,notpresent,?,?,3.4,136,4.2,13.0,40,9800,4.2,yes,no,yes,good,no,no,ckd\n',
 '35,80,1.005,3,0,abnormal,normal,notpresent,notpresent,?,?,?,?,?,9.5,28,?,?,no,no,no,good,yes,no,ckd\n',
 '76,70,1.015,3,4,normal,abnormal,present,notpresent,?,164,9.7,131,4.4,10.2,30,11300,3.4,yes,yes,yes,poor,yes,no,ckd\n',
 '76,90,?,?,?,?,normal,notpresent,notpresent,93,155,7.3,132,4.9,?,?,?,?,yes,yes,yes,poor,no,no,ckd\n',
 '73,80,1.020,2,0,abnormal,abnormal,notpresent,notpresent,253,142,4.6,138,5.8,10.5,33,7200,4.3,yes,yes,yes,good,no,no,ckd\n',
 '59,100,?,?,?,?,?,notpresent,notpresent,?,96,6.4,?,?,6.6,?,?,?,yes,yes,no,good,no,yes,ckd\n',
 '67,90,1.020,1,0,?,abnormal,present,notpresent,141,66,3.2,138,6.6,?,?,?,?,yes,no,no,good,no,no,ckd\n',
 '67,80,1.010,1,3,normal,abnormal,notpresent,notpresent,182,391,32.0,163,39.0,?,?,?,?,no,no,no,good,yes,no,ckd\n',
 '15,60,1.020,3,0,?,normal,notpresent,notpresent,86,15,0.6,138,4.0,11.0,33,7700,3.8,yes,yes,no,good,no,no,ckd\n',
 '46,70,1.015,1,0,abnormal,normal,notpresent,notpresent,150,111,6.1,131,3.7,7.5,27,?,?,no,no,no,good,no,yes,ckd\n',
 '55,80,1.010,0,0,?,normal,notpresent,notpresent,146,?,?,?,?,9.8,?,?,?,no,no,\tno,good,no,no,ckd\n',
 '44,90,1.010,1,0,?,normal,notpresent,notpresent,?,20,1.1,?,?,15.0,48,?,?,no,\tno,no,good,no,no,ckd\n',
 '67,70,1.020,2,0,abnormal,normal,notpresent,notpresent,150,55,1.6,131,4.8,?,\t?,?,?,yes,yes,no,good,yes,no,ckd\n',
 '45,80,1.020,3,0,normal,abnormal,notpresent,notpresent,425,?,?,?,?,?,?,?,?,no,no,no,poor,no,no,ckd\n',
 '65,70,1.010,2,0,?,normal,present,notpresent,112,73,3.3,?,?,10.9,37,?,?,no,no,no,good,no,no,ckd\n',
 '26,70,1.015,0,4,?,normal,notpresent,notpresent,250,20,1.1,?,?,15.6,52,6900,6.0,no,yes,no,good,no,no,ckd,\n',
 '61,80,1.015,0,4,?,normal,notpresent,notpresent,360,19,0.7,137,4.4,15.2,44,8300,5.2,yes,yes,no,good,no,no,ckd\n',
 '46,60,1.010,1,0,normal,normal,notpresent,notpresent,163,92,3.3,141,4.0,9.8,28,14600,3.2,yes,yes,no,good,no,no,ckd\n',
 '64,90,1.010,3,3,?,abnormal,present,notpresent,?,35,1.3,?,?,10.3,?,?,?,yes,yes,no,good,yes,no,ckd,\n',
 '?,100,1.015,2,0,abnormal,abnormal,notpresent,notpresent,129,107,6.7,132,4.4,4.8,14,6300,?,yes,no,no,good,yes,yes,ckd\n',
 '56,90,1.015,2,0,abnormal,abnormal,notpresent,notpresent,129,107,6.7,131,4.8,9.1,29,6400,3.4,yes,no,no,good,no,no,ckd\n',
 '5,?,1.015,1,0,?,normal,notpresent,notpresent,?,16,0.7,138,3.2,8.1,?,?,?,no,no,no,good,no,yes,ckd\n',
 '48,80,1.005,4,0,abnormal,abnormal,notpresent,present,133,139,8.5,132,5.5,10.3,36,\t6200,4,no,yes,no,good,yes,no,ckd\n',
 '67,70,1.010,1,0,?,normal,notpresent,notpresent,102,48,3.2,137,5.0,11.9,34,7100,3.7,yes,yes,no,good,yes,no,ckd\n',
 '70,80,?,?,?,?,?,notpresent,notpresent,158,85,3.2,141,3.5,10.1,30,?,?,yes,no,no,good,yes,no,ckd\n',
 '56,80,1.010,1,0,?,normal,notpresent,notpresent,165,55,1.8,?,?,13.5,40,11800,5.0,yes,yes,no,poor,yes,no,ckd\n',
 '74,80,1.010,0,0,?,normal,notpresent,notpresent,132,98,2.8,133,5.0,10.8,31,9400,3.8,yes,yes,no,good,no,no,ckd\n',
 '45,90,?,?,?,?,?,notpresent,notpresent,360,45,2.4,128,4.4,8.3,29,5500,3.7,yes,yes,no,good,no,no,ckd\n',
 '38,70,?,?,?,?,?,notpresent,notpresent,104,77,1.9,140,3.9,?,?,?,?,yes,no,no,poor,yes,no,ckd\n',
 '48,70,1.015,1,0,normal,normal,notpresent,notpresent,127,19,1.0,134,3.6,?,?,?,?,yes,yes,no,good,no,no,ckd\n',
 '59,70,1.010,3,0,normal,abnormal,notpresent,notpresent,76,186,15,135,7.6,7.1,22,3800,2.1,yes,no,no,poor,yes,yes,ckd\n',
 '70,70,1.015,2,?,?,?,notpresent,notpresent,?,46,1.5,?,?,9.9,?,?,?,no,yes,no,poor,yes,no,ckd\n',
 '56,80,?,?,?,?,?,notpresent,notpresent,415,37,1.9,?,?,?,?,?,?,no,yes,no,good,no,no,ckd\n',
 '70,100,1.005,1,0,normal,abnormal,present,notpresent,169,47,2.9,?,?,11.1,32,5800,5,yes,yes,no,poor,no,no,ckd\n',
 '58,110,1.010,4,0,?,normal,notpresent,notpresent,251,52,2.2,?,?,?,?,13200,4.7,yes,\tyes,no,good,no,no,ckd\n',
 '50,70,1.020,0,0,?,normal,notpresent,notpresent,109,32,1.4,139,4.7,?,?,?,?,no,no,no,poor,no,no,ckd\n',
 '63,100,1.010,2,2,normal,normal,notpresent,present,280,35,3.2,143,3.5,13.0,40,9800,4.2,yes,no,yes,good,no,no,ckd\n',
 '56,70,1.015,4,1,abnormal,normal,notpresent,notpresent,210,26,1.7,136,3.8,16.1,52,12500,5.6,no,no,no,good,no,no,ckd\n',
 '71,70,1.010,3,0,normal,abnormal,present,present,219,82,3.6,133,4.4,10.4,33,5600,3.6,yes,yes,yes,good,no,no,ckd\n',
 '73,100,1.010,3,2,abnormal,abnormal,present,notpresent,295,90,5.6,140,2.9,9.2,30,7000,3.2,yes,yes,yes,poor,no,no,ckd\n',
 '65,70,1.010,0,0,?,normal,notpresent,notpresent,93,66,1.6,137,4.5,11.6,36,11900,3.9,no,yes,no,good,no,no,ckd\n',
 '62,90,1.015,1,0,?,normal,notpresent,notpresent,94,25,1.1,131,3.7,?,?,?,?,yes,no,no,good,yes,yes,ckd\n',
 '60,80,1.010,1,1,?,normal,notpresent,notpresent,172,32,2.7,?,?,11.2,36,?,?,no,yes,yes,poor,no,no,ckd\n',
 '65,60,1.015,1,0,?,normal,notpresent,notpresent,91,51,2.2,132,3.8,10.0,32,9100,4.0,yes,yes,no,poor,yes,no,ckd\n',
 '50,140,?,?,?,?,?,notpresent,notpresent,101,106,6.5,135,4.3,6.2,18,5800,2.3,yes,yes,no,poor,no,yes,ckd\n',
 '56,180,?,0,4,?,abnormal,notpresent,notpresent,298,24,1.2,139,3.9,11.2,32,10400,4.2,yes,yes,no,poor,yes,no,ckd\n',
 '34,70,1.015,4,0,abnormal,abnormal,notpresent,notpresent,153,22,0.9,133,3.8,?,?,?,?,no,no,no,good,yes,no,ckd\n',
 '71,90,1.015,2,0,?,abnormal,present,present,88,80,4.4,139,5.7,11.3,33,10700,3.9,no,no,no,good,no,no,ckd\n',
 '17,60,1.010,0,0,?,normal,notpresent,notpresent,92,32,2.1,141,4.2,13.9,52,7000,?,no,no,no,good,no,no,ckd\n',
 '76,70,1.015,2,0,normal,abnormal,present,notpresent,226,217,10.2,?,?,10.2,36,12700,4.2,yes,no,no,poor,yes,yes,ckd\n',
 '55,90,?,?,?,?,?,notpresent,notpresent,143,88,2.0,?,?,?,?,?,?,yes,yes,no,poor,yes,no,ckd\n',
 '65,80,1.015,0,0,?,normal,notpresent,notpresent,115,32,11.5,139,4.0,14.1,42,6800,5.2,no,no,no,good,no,no,ckd\n',
 '50,90,?,?,?,?,?,notpresent,notpresent,89,118,6.1,127,4.4,6.0,17,6500,?,yes,yes,no,good,yes,yes,ckd\n',
 '55,100,1.015,1,4,normal,?,notpresent,notpresent,297,53,2.8,139,4.5,11.2,34,13600,4.4,yes,yes,no,good,no,no,ckd\n',
 '45,80,1.015,0,0,?,abnormal,notpresent,notpresent,107,15,1.0,141,4.2,11.8,37,10200,4.2,no,no,no,good,no,no,ckd\n',
 '54,70,?,?,?,?,?,notpresent,notpresent,233,50.1,1.9,?,?,11.7,?,?,?,no,yes,no,good,no,no,ckd\n',
 '63,90,1.015,0,0,?,normal,notpresent,notpresent,123,19,2.0,142,3.8,11.7,34,11400,4.7,no,no,no,good,no,no,ckd\n',
 '65,80,1.010,3,3,?,normal,notpresent,notpresent,294,71,4.4,128,5.4,10.0,32,9000,3.9,yes,yes,yes,good,no,no,ckd\n',
 '?,60,1.015,3,0,abnormal,abnormal,notpresent,notpresent,?,34,1.2,?,?,10.8,33,?,?,no,no,no,good,no,no,ckd\n',
 '61,90,1.015,0,2,?,normal,notpresent,notpresent,?,?,?,?,?,?,?,9800,?,no,yes,no,poor,no,yes,ckd\n',
 '12,60,1.015,3,0,abnormal,abnormal,present,notpresent,?,51,1.8,?,?,12.1,?,10300,?,no,no,no,good,no,no,ckd\n',
 '47,80,1.010,0,0,?,abnormal,notpresent,notpresent,?,28,0.9,?,?,12.4,44,5600,4.3,no,no,no,good,no,yes,ckd\n',
 '?,70,1.015,4,0,abnormal,normal,notpresent,notpresent,104,16,0.5,?,?,?,?,?,?,no,no,no,good,yes,no,ckd\n',
 '?,70,1.020,0,0,?,?,notpresent,notpresent,219,36,1.3,139,3.7,12.5,37,9800,4.4,no,no,no,good,no,no,ckd\n',
 '55,70,1.010,3,0,?,normal,notpresent,notpresent,99,25,1.2,?,?,11.4,?,?,?,no,no,no,poor,yes,no,ckd\n',
 '60,70,1.010,0,0,?,normal,notpresent,notpresent,140,27,1.2,?,?,?,?,?,?,no,no,no,good,no,no,ckd\n',
 '72,90,1.025,1,3,?,normal,notpresent,notpresent,323,40,2.2,137,5.3,12.6,?,?,?,no,yes,yes,poor,no,no,ckd\n',
 '54,60,?,3,?,?,?,notpresent,notpresent,125,21,1.3,137,3.4,15.0,46,?,?,yes,yes,no,good,yes,no,ckd\n',
 '34,70,?,?,?,?,?,notpresent,notpresent,?,219,12.2,130,3.8,6.0,?,?,?,yes,no,no,good,no,yes,ckd\n',
 '43,80,1.015,2,3,?,abnormal,present,present,?,30,1.1,?,?,14.0,42,14900,?,no,no,no,good,no,no,ckd\n',
 '65,100,1.015,0,0,?,normal,notpresent,notpresent,90,98,2.5,?,?,9.1,28,5500,3.6,yes,no,no,good,no,no,ckd\n',
 '72,90,?,?,?,?,?,notpresent,notpresent,308,36,2.5,131,4.3,?,?,?,?,yes,yes,no,poor,no,no,ckd\n',
 '70,90,1.015,0,0,?,normal,notpresent,notpresent,144,125,4.0,136,4.6,12.0,37,8200,4.5,yes,yes,no,poor,yes,no,ckd\n',
 '71,60,1.015,4,0,normal,normal,notpresent,notpresent,118,125,5.3,136,4.9,11.4,35,15200,4.3,yes,yes,no,poor,yes,no,ckd\n',
 '52,90,1.015,4,3,normal,abnormal,notpresent,notpresent,224,166,5.6,133,47,8.1,23,5000,2.9,yes,yes,no,good,no,yes,ckd\n',
 '75,70,1.025,1,0,?,normal,notpresent,notpresent,158,49,1.4,135,4.7,11.1,?,?,?,yes,no,no,poor,yes,no,ckd\n',
 '50,90,1.010,2,0,normal,abnormal,present,present,128,208,9.2,134,4.8,8.2,22,16300,2.7,no,no,no,poor,yes,yes,ckd\n',
 '5,50,1.010,0,0,?,normal,notpresent,notpresent,?,25,0.6,?,?,11.8,36,12400,?,no,no,no,good,no,no,ckd\n',
 '50,?,?,?,?,normal,?,notpresent,notpresent,219,176,13.8,136,4.5,8.6,24,13200,2.7,yes,no,no,good,yes,yes,ckd\n',
 '70,100,1.015,4,0,normal,normal,notpresent,notpresent,118,125,5.3,136,4.9,12.0,37,\t8400,8.0,yes,no,no,good,no,no,ckd\n',
 '47,100,1.010,?,?,normal,?,notpresent,notpresent,122,?,16.9,138,5.2,10.8,33,10200,3.8,no,yes,no,good,no,no,ckd\n',
 '48,80,1.015,0,2,?,normal,notpresent,notpresent,214,24,1.3,140,4.0,13.2,39,?,?,no,yes,no,poor,no,no,ckd\n',
 '46,90,1.020,?,?,?,normal,notpresent,notpresent,213,68,2.8,146,6.3,9.3,?,?,?,yes,yes,no,good,no,no,ckd\n',
 '45,60,1.010,2,0,normal,abnormal,present,notpresent,268,86,4.0,134,5.1,10.0,29,9200,?,yes,yes,no,good,no,no,ckd\n',
 '73,?,1.010,1,0,?,?,notpresent,notpresent,95,51,1.6,142,3.5,?,?,?,?,no,\tno,no,good,no,no,ckd\n',
 '41,70,1.015,2,0,?,abnormal,notpresent,present,?,68,2.8,132,4.1,11.1,33,?,?,yes,no,no,good,yes,yes,ckd\n',
 '69,70,1.010,0,4,?,normal,notpresent,notpresent,256,40,1.2,142,5.6,?,?,?,?,no,no,no,good,no,no,ckd\n',
 '67,70,1.010,1,0,normal,normal,notpresent,notpresent,?,106,6.0,137,4.9,6.1,19,6500,?,yes,no,no,good,no,yes,ckd\n',
 '72,90,?,?,?,?,?,notpresent,notpresent,84,145,7.1,135,5.3,?,?,?,?,no,yes,no,good,no,no,ckd\n',
 '41,80,1.015,1,4,abnormal,normal,notpresent,notpresent,210,165,18.0,135,4.7,?,?,?,?,no,yes,no,good,no,no,ckd\n',
 '60,90,1.010,2,0,abnormal,normal,notpresent,notpresent,105,53,2.3,136,5.2,11.1,33,10500,4.1,no,no,no,good,no,no,ckd\n',
 '57,90,1.015,5,0,abnormal,abnormal,notpresent,present,?,322,13.0,126,4.8,8.0,24,4200,3.3,yes,yes,yes,poor,yes,yes,ckd\n',
 '53,100,1.010,1,3,abnormal,normal,notpresent,notpresent,213,23,1.0,139,4,?,?,?,?,no,yes,no,good,no,no,ckd\n',
 '60,60,1.010,3,1,normal,abnormal,present,notpresent,288,36,1.7,130,3.0,7.9,25,15200,3.0,yes,no,no,poor,no,yes,ckd\n',
 '69,60,?,?,?,?,?,notpresent,notpresent,171,26,48.1,?,?,?,?,?,?,yes,no,no,poor,no,no,ckd\n',
 '65,70,1.020,1,0,abnormal,abnormal,notpresent,notpresent,139,29,1.0,?,?,10.5,32,?,?,yes,no,no,good,yes,no,ckd\n',
 '8,60,1.025,3,0,normal,normal,notpresent,notpresent,78,27,0.9,?,?,12.3,41,6700,?,no,no,no,poor,yes,no,ckd\n',
 '76,90,?,?,?,?,?,notpresent,notpresent,172,46,1.7,141,5.5,9.6,30,?,?,yes,yes,no,good,no,yes,ckd\n',
 '39,70,1.010,0,0,?,normal,notpresent,notpresent,121,20,0.8,133,3.5,10.9,32,?,?,no,yes,no,good,no,no,ckd\n',
 '55,90,1.010,2,1,abnormal,abnormal,notpresent,notpresent,273,235,14.2,132,3.4,8.3,22,14600,2.9,yes,yes,no,poor,yes,yes,ckd\n',
 '56,90,1.005,4,3,abnormal,abnormal,notpresent,notpresent,242,132,16.4,140,4.2,8.4,26,?,3,yes,yes,no,poor,yes,yes,ckd\n',
 '50,70,1.020,3,0,abnormal,normal,present,present,123,40,1.8,?,?,11.1,36,4700,?,no,no,no,good,no,no,ckd\n',
 '66,90,1.015,2,0,?,normal,notpresent,present,153,76,3.3,?,?,?,?,?,?,no,no,no,poor,no,no,ckd\n',
 '62,70,1.025,3,0,normal,abnormal,notpresent,notpresent,122,42,1.7,136,4.7,12.6,39,7900,3.9,yes,yes,no,good,no,no,ckd\n',
 '71,60,1.020,3,2,normal,normal,present,notpresent,424,48,1.5,132,4.0,10.9,31,?,?,yes,yes,yes,good,no,no,ckd\n',
 '59,80,1.010,1,0,abnormal,normal,notpresent,notpresent,303,35,1.3,122,3.5,10.4,35,10900,4.3,no,yes,no,poor,no,no,ckd\n',
 '81,60,?,?,?,?,?,notpresent,notpresent,148,39,2.1,147,4.2,10.9,35,9400,2.4,yes,yes,yes,poor,yes,no,ckd\n',
 '62,?,1.015,3,0,abnormal,?,notpresent,notpresent,?,?,?,?,?,14.3,42,10200,4.8,yes,yes,no,good,no,no,ckd\n',
 '59,70,?,?,?,?,?,notpresent,notpresent,204,34,1.5,124,4.1,9.8,37,6000,\t?,no,yes,no,good,no,no,ckd\n',
 '46,80,1.010,0,0,?,normal,notpresent,notpresent,160,40,2,140,4.1,9.0,27,8100,3.2,yes,no,no,poor,no,yes,ckd\n',
 '14,?,1.015,0,0,?,?,notpresent,notpresent,192,15,0.8,137,4.2,14.3,40,9500,5.4,no,yes,no,poor,yes,no,ckd\n',
 '60,80,1.020,0,2,?,?,notpresent,notpresent,?,?,?,?,?,?,?,?,?,no,yes,no,good,no,no,ckd\n',
 '27,60,?,?,?,?,?,notpresent,notpresent,76,44,3.9,127,4.3,?,?,?,?,no,no,no,poor,yes,yes,ckd\n',
 '34,70,1.020,0,0,abnormal,normal,notpresent,notpresent,139,19,0.9,?,?,12.7,42,2200,?,no,no,no,poor,no,no,ckd\n',
 '65,70,1.015,4,4,?,normal,present,notpresent,307,28,1.5,?,?,11.0,39,6700,?,yes,yes,no,good,no,no,ckd\n',
 '?,70,1.010,0,2,?,normal,notpresent,notpresent,220,68,2.8,?,?,8.7,27,?,?,yes,yes,no,good,no,yes,ckd\n',
 '66,70,1.015,2,5,?,normal,notpresent,notpresent,447,41,1.7,131,3.9,12.5,33,9600,4.4,yes,yes,no,good,no,no,ckd\n',
 '83,70,1.020,3,0,normal,normal,notpresent,notpresent,102,60,2.6,115,5.7,8.7,26,12800,3.1,yes,no,no,poor,no,yes,ckd\n',
 '62,80,1.010,1,2,?,?,notpresent,notpresent,309,113,2.9,130,2.5,10.6,34,12800,4.9,no,no,no,good,no,no,ckd\n',
 '17,70,1.015,1,0,abnormal,normal,notpresent,notpresent,22,1.5,7.3,145,2.8,13.1,41,11200,?,no,no,no,good,no,no,ckd\n',
 '54,70,?,?,?,?,?,notpresent,notpresent,111,146,7.5,141,4.7,11.0,35,8600,4.6,no,no,no,good,no,no,ckd\n',
 '60,50,1.010,0,0,?,normal,notpresent,notpresent,261,58,2.2,113,3.0,?,?,4200,3.4,yes,no,no,good,no,no,ckd\n',
 '21,90,1.010,4,0,normal,abnormal,present,present,107,40,1.7,125,3.5,8.3,23,12400,3.9,no,no,no,good,no,yes,ckd\n',
 '65,80,1.015,2,1,normal,normal,present,notpresent,215,133,2.5,?,?,13.2,41,?,?,no,yes,no,good,no,no,ckd\n',
 '42,90,1.020,2,0,abnormal,abnormal,present,notpresent,93,153,2.7,139,4.3,9.8,34,9800,?,no,no,no,poor,yes,yes,ckd\n',
 '72,90,1.010,2,0,?,abnormal,present,notpresent,124,53,2.3,?,?,11.9,39,?,?,no,no,no,good,no,no,ckd\n',
 '73,90,1.010,1,4,abnormal,abnormal,present,notpresent,234,56,1.9,?,?,10.3,28,?,?,no,yes,no,good,no,no,ckd\n',
 '45,70,1.025,2,0,normal,abnormal,present,notpresent,117,52,2.2,136,3.8,10.0,30,19100,3.7,no,no,no,good,no,no,ckd\n',
 '61,80,1.020,0,0,?,normal,notpresent,notpresent,131,23,0.8,140,4.1,11.3,35,?,?,no,no,no,good,no,no,ckd\n',
 '30,70,1.015,0,0,?,normal,notpresent,notpresent,101,106,6.5,135,4.3,?,?,?,?,no,no,no,poor,no,no,ckd\n',
 '54,60,1.015,3,2,?,abnormal,notpresent,notpresent,352,137,3.3,133,4.5,11.3,31,5800,3.6,yes,yes,yes,poor,yes,no,ckd\n',
 '4,?,1.020,1,0,?,normal,notpresent,notpresent,99,23,0.6,138,4.4,12,34,\t?,?,no,no,no,good,no,no,ckd\n',
 '8,50,1.020,4,0,normal,normal,notpresent,notpresent,?,46,1.0,135,3.8,?,?,?,?,no,no,no,good,yes,no,ckd\n',
 '3,?,1.010,2,0,normal,normal,notpresent,notpresent,?,22,0.7,?,?,10.7,34,12300,?,no,no,no,good,no,no,ckd\n',
 '8,?,?,?,?,?,?,notpresent,notpresent,80,66,2.5,142,3.6,12.2,38,?,?,no,\tno,no,good,no,no,ckd\n',
 '64,60,1.010,4,1,abnormal,abnormal,notpresent,present,239,58,4.3,137,5.4,9.5,29,7500,3.4,yes,yes,no,poor,yes,no,ckd\n',
 '6,60,1.010,4,0,abnormal,abnormal,notpresent,present,94,67,1.0,135,4.9,9.9,30,16700,4.8,no,no,no,poor,no,no,ckd\n',
 '?,70,1.010,3,0,normal,normal,notpresent,notpresent,110,115,6.0,134,2.7,9.1,26,9200,3.4,yes,yes,no,poor,no,no,ckd\n',
 '46,110,1.015,0,0,?,normal,notpresent,notpresent,130,16,0.9,?,?,?,?,?,?,no,no,no,good,no,no,ckd\n',
 '32,90,1.025,1,0,abnormal,abnormal,notpresent,notpresent,?,223,18.1,113,6.5,5.5,15,2600,2.8,yes,yes,no,poor,yes,yes,ckd\n',
 '80,70,1.010,2,?,?,abnormal,notpresent,notpresent,?,49,1.2,?,?,?,?,?,?,yes,\tyes,no,good,no,no,ckd\n',
 '70,90,1.020,2,1,abnormal,abnormal,notpresent,present,184,98.6,3.3,138,3.9,5.8,?,?,?,yes,yes,yes,poor,no,no,ckd\n',
 '49,100,1.010,3,0,abnormal,abnormal,notpresent,notpresent,129,158,11.8,122,3.2,8.1,24,9600,3.5,yes,yes,no,poor,yes,yes,ckd\n',
 '57,80,?,?,?,?,?,notpresent,notpresent,?,111,9.3,124,5.3,6.8,?,4300,3.0,yes,yes,no,good,no,yes,ckd\n',
 '59,100,1.020,4,2,normal,normal,notpresent,notpresent,252,40,3.2,137,4.7,11.2,30,26400,3.9,yes,yes,no,poor,yes,no,ckd\n',
 '65,80,1.015,0,0,?,normal,notpresent,notpresent,92,37,1.5,140,5.2,8.8,25,10700,3.2,yes,no,yes,good,yes,no,ckd\n',
 '90,90,1.025,1,0,?,normal,notpresent,notpresent,139,89,3.0,140,4.1,12.0,37,7900,3.9,yes,yes,no,good,no,no,ckd\n',
 '64,70,?,?,?,?,?,notpresent,notpresent,113,94,7.3,137,4.3,7.9,21,?,?,yes,yes,yes,good,yes,yes,ckd\n',
 '78,60,?,?,?,?,?,notpresent,notpresent,114,74,2.9,135,5.9,8.0,24,?,?,no,yes,no,good,no,yes,ckd\n',
 '?,90,?,?,?,?,?,notpresent,notpresent,207,80,6.8,142,5.5,8.5,?,?,?,yes,yes,no,good,no,yes,ckd\n',
 '65,90,1.010,4,2,normal,normal,notpresent,notpresent,172,82,13.5,145,6.3,8.8,31,?,?,yes,yes,no,good,yes,yes,ckd\n',
 '61,70,?,?,?,?,?,notpresent,notpresent,100,28,2.1,?,?,12.6,43,?,?,yes,yes,no,good,no,no,ckd\n',
 '60,70,1.010,1,0,?,normal,notpresent,notpresent,109,96,3.9,135,4.0,13.8,41,?,?,yes,no,no,good,no,no,ckd\n',
 '50,70,1.010,0,0,?,normal,notpresent,notpresent,230,50,2.2,?,?,12,41,10400,4.6,yes,yes,no,good,no,no,ckd\n',
 '67,80,?,?,?,?,?,notpresent,notpresent,341,37,1.5,?,?,12.3,41,6900,4.9,yes,yes,no,good,no,yes,ckd\n',
 '19,70,1.020,0,0,?,normal,notpresent,notpresent,?,?,?,?,?,11.5,?,6900,?,no,no,no,good,no,no,ckd\n',
 '59,100,1.015,4,2,normal,normal,notpresent,notpresent,255,132,12.8,135,5.7,7.3,20,9800,3.9,yes,yes,yes,good,no,yes,ckd\n',
 '54,120,1.015,0,0,?,normal,notpresent,notpresent,103,18,1.2,?,?,?,?,?,?,no,no,no,good,no,no,ckd\n',
 '40,70,1.015,3,4,normal,normal,notpresent,notpresent,253,150,11.9,132,5.6,10.9,31,8800,3.4,yes,yes,no,poor,yes,no,ckd\n',
 '55,80,1.010,3,1,normal,abnormal,present,present,214,73,3.9,137,4.9,10.9,34,7400,3.7,yes,yes,no,good,yes,no,ckd\n',
 '68,80,1.015,0,0,?,abnormal,notpresent,notpresent,171,30,1.0,?,?,13.7,\t43,4900,5.2,no,yes,no,good,no,no,ckd\n',
 '2,?,1.010,3,0,normal,abnormal,notpresent,notpresent,?,?,?,?,?,?,?,?,?,no,no,no,good,yes,no,ckd\n',
 '64,70,1.010,0,0,?,normal,notpresent,notpresent,107,15,?,?,?,12.8,38,?,?,no,no,no,good,no,no,ckd\n',
 '63,100,1.010,1,0,?,normal,notpresent,notpresent,78,61,1.8,141,4.4,12.2,36,10500,4.3,no,yes,no,good,no,no,ckd\n',
 '33,90,1.015,0,0,?,normal,notpresent,notpresent,92,19,0.8,?,?,11.8,34,7000,?,no,no,no,good,no,no,ckd\n',
 '68,90,1.010,0,0,?,normal,notpresent,notpresent,238,57,2.5,?,?,9.8,28,8000,3.3,yes,yes,no,poor,no,no,ckd\n',
 '36,80,1.010,0,0,?,normal,notpresent,notpresent,103,?,?,?,?,11.9,36,8800,?,no,no,no,good,no,no,ckd\n',
 '66,70,1.020,1,0,normal,?,notpresent,notpresent,248,30,1.7,138,5.3,?,?,?,?,yes,yes,no,good,no,no,ckd\n',
 '74,60,?,?,?,?,?,notpresent,notpresent,108,68,1.8,?,?,?,?,?,?,yes,yes,no,good,no,no,ckd\n',
 '71,90,1.010,0,3,?,normal,notpresent,notpresent,303,30,1.3,136,4.1,13.0,38,9200,4.6,yes,yes,no,good,no,no,ckd\n',
 '34,60,1.020,0,0,?,normal,notpresent,notpresent,117,28,2.2,138,3.8,?,?,?,?,no,no,no,good,yes,no,ckd\n',
 '60,90,1.010,3,5,abnormal,normal,notpresent,present,490,95,2.7,131,3.8,11.5,35,12000,4.5,yes,yes,no,good,no,no,ckd\n',
 '64,100,1.015,4,2,abnormal,abnormal,notpresent,present,163,54,7.2,140,4.6,7.9,26,7500,3.4,yes,yes,no,good,yes,no,ckd\n',
 '57,80,1.015,0,0,?,normal,notpresent,notpresent,120,48,1.6,?,?,11.3,36,7200,3.8,yes,yes,no,good,no,no,ckd\n',
 '60,70,?,?,?,?,?,notpresent,notpresent,124,52,2.5,?,?,?,?,?,?,yes,no,no,good,no,no,ckd\n',
 '59,50,1.010,3,0,normal,abnormal,notpresent,notpresent,241,191,12.0,114,2.9,9.6,31,15700,3.8,no,yes,no,good,yes,no,ckd\n',
 '65,60,1.010,2,0,normal,abnormal,present,notpresent,192,17,1.7,130,4.3,?,?,9500,?,yes,yes,no,poor,no,no,ckd\t\n',
 '60,90,?,?,?,?,?,notpresent,notpresent,269,51,2.8,138,3.7,11.5,35,?,?,yes,yes,yes,good,yes,no,ckd\n',
 '50,90,1.015,1,0,abnormal,abnormal,notpresent,notpresent,?,?,?,?,?,?,?,?,?,no,no,no,good,yes,no,ckd\n',
 '51,100,1.015,2,0,normal,normal,notpresent,present,93,20,1.6,146,4.5,?,?,?,?,no,no,no,poor,no,no,ckd\n',
 '37,100,1.010,0,0,abnormal,normal,notpresent,notpresent,?,19,1.3,?,?,15.0,44,4100,5.2,yes,no,no,good,no,no,ckd\n',
 '45,70,1.010,2,0,?,normal,notpresent,notpresent,113,93,2.3,?,?,7.9,26,5700,?,no,no,yes,good,no,yes,ckd\n',
 '65,80,?,?,?,?,?,notpresent,notpresent,74,66,2.0,136,5.4,9.1,25,?,?,yes,yes,yes,good,yes,no,ckd\n',
 '80,70,1.015,2,2,?,normal,notpresent,notpresent,141,53,2.2,?,?,12.7,40,9600,?,yes,yes,no,poor,yes,no,ckd\n',
 '72,100,?,?,?,?,?,notpresent,notpresent,201,241,13.4,127,4.8,9.4,28,?,?,yes,yes,no,good,no,yes,ckd\n',
 '34,90,1.015,2,0,normal,normal,notpresent,notpresent,104,50,1.6,137,4.1,11.9,39,?,?,no,no,no,good,no,no,ckd\n',
 '65,70,1.015,1,0,?,normal,notpresent,notpresent,203,46,1.4,?,?,11.4,36,5000,4.1,yes,yes,no,poor,yes,no,ckd\n',
 '57,70,1.015,1,0,?,abnormal,notpresent,notpresent,165,45,1.5,140,3.3,10.4,31,4200,3.9,no,no,no,good,no,no,ckd\n',
 '69,70,1.010,4,3,normal,abnormal,present,present,214,96,6.3,120,3.9,9.4,28,11500,3.3,yes,yes,yes,good,yes,yes,ckd\n',
 '62,90,1.020,2,1,?,normal,notpresent,notpresent,169,48,2.4,138,2.9,13.4,47,11000,6.1,yes,no,no,good,no,no,ckd\n',
 '64,90,1.015,3,2,?,abnormal,present,notpresent,463,64,2.8,135,4.1,12.2,40,9800,4.6,yes,yes,no,good,no,yes,ckd\n',
 '48,100,?,?,?,?,?,notpresent,notpresent,103,79,5.3,135,6.3,6.3,19,7200,2.6,yes,no,yes,poor,no,no,ckd\n',
 '48,110,1.015,3,0,abnormal,normal,present,notpresent,106,215,15.2,120,5.7,8.6,26,5000,2.5,yes,no,yes,good,no,yes,ckd\n',
 '54,90,1.025,1,0,normal,abnormal,notpresent,notpresent,150,18,1.2,140,4.2,?,?,?,?,no,no,no,poor,yes,yes,ckd\n',
 '59,70,1.010,1,3,abnormal,abnormal,notpresent,notpresent,424,55,1.7,138,4.5,12.6,37,10200,4.1,yes,yes,yes,good,no,no,ckd\n',
 '56,90,1.010,4,1,normal,abnormal,present,notpresent,176,309,13.3,124,6.5,3.1,9,5400,2.1,yes,yes,no,poor,yes,yes,ckd\n',
 '40,80,1.025,0,0,normal,normal,notpresent,notpresent,140,10,1.2,135,5.0,15.0,48,10400,4.5,no,no,no,good,no,no,notckd\n',
 '23,80,1.025,0,0,normal,normal,notpresent,notpresent,70,36,1.0,150,4.6,17.0,52,9800,5.0,no,no,no,good,no,no,notckd\n',
 '45,80,1.025,0,0,normal,normal,notpresent,notpresent,82,49,0.6,147,4.4,15.9,46,9100,4.7,no,no,no,good,no,no,notckd\n',
 '57,80,1.025,0,0,normal,normal,notpresent,notpresent,119,17,1.2,135,4.7,15.4,42,6200,6.2,no,no,no,good,no,no,notckd\n',
 '51,60,1.025,0,0,normal,normal,notpresent,notpresent,99,38,0.8,135,3.7,13.0,49,8300,5.2,no,no,no,good,no,no,notckd\n',
 '34,80,1.025,0,0,normal,normal,notpresent,notpresent,121,27,1.2,144,3.9,13.6,52,9200,6.3,no,no,no,good,no,no,notckd\n',
 '60,80,1.025,0,0,normal,normal,notpresent,notpresent,131,10,0.5,146,5.0,14.5,41,10700,5.1,no,no,no,good,no,no,notckd\n',
 '38,60,1.020,0,0,normal,normal,notpresent,notpresent,91,36,0.7,135,3.7,14.0,46,9100,5.8,no,no,no,good,no,no,notckd\n',
 '42,80,1.020,0,0,normal,normal,notpresent,notpresent,98,20,0.5,140,3.5,13.9,44,8400,5.5,no,no,no,good,no,no,notckd\n',
 '35,80,1.020,0,0,normal,normal,notpresent,notpresent,104,31,1.2,135,5.0,16.1,45,4300,5.2,no,no,no,good,no,no,notckd\n',
 '30,80,1.020,0,0,normal,normal,notpresent,notpresent,131,38,1.0,147,3.8,14.1,45,9400,5.3,no,no,no,good,no,no,notckd\n',
 '49,80,1.020,0,0,normal,normal,notpresent,notpresent,122,32,1.2,139,3.9,17.0,41,5600,4.9,no,no,no,good,no,no,notckd\n',
 '55,80,1.020,0,0,normal,normal,notpresent,notpresent,118,18,0.9,135,3.6,15.5,43,7200,5.4,no,no,no,good,no,no,notckd\n',
 '45,80,1.020,0,0,normal,normal,notpresent,notpresent,117,46,1.2,137,5.0,16.2,45,8600,5.2,no,no,no,good,no,no,notckd\n',
 '42,80,1.020,0,0,normal,normal,notpresent,notpresent,132,24,0.7,140,4.1,14.4,50,5000,4.5,no,no,no,good,no,no,notckd\n',
 '50,80,1.020,0,0,normal,normal,notpresent,notpresent,97,40,0.6,150,4.5,14.2,48,10500,5.0,no,no,no,good,no,no,notckd\n',
 '55,80,1.020,0,0,normal,normal,notpresent,notpresent,133,17,1.2,135,4.8,13.2,41,6800,5.3,no,no,no,good,no,no,notckd\n',
 '48,80,1.025,0,0,normal,normal,notpresent,notpresent,122,33,0.9,146,3.9,13.9,48,9500,4.8,no,no,no,good,no,no,notckd\n',
 '?,80,?,?,?,?,?,notpresent,notpresent,100,49,1.0,140,5.0,16.3,53,8500,4.9,no,no,no,good,no,no,notckd\n',
 '25,80,1.025,0,0,normal,normal,notpresent,notpresent,121,19,1.2,142,4.9,15.0,48,6900,5.3,no,no,no,good,no,no,notckd\n',
 '23,80,1.025,0,0,normal,normal,notpresent,notpresent,111,34,1.1,145,4.0,14.3,41,7200,5.0,no,no,no,good,no,no,notckd\n',
 '30,80,1.025,0,0,normal,normal,notpresent,notpresent,96,25,0.5,144,4.8,13.8,42,9000,4.5,no,no,no,good,no,no,notckd\n',
 '56,80,1.025,0,0,normal,normal,notpresent,notpresent,139,15,1.2,135,5.0,14.8,42,5600,5.5,no,no,no,good,no,no,notckd\n',
 '47,80,1.020,0,0,normal,normal,notpresent,notpresent,95,35,0.9,140,4.1,?,?,?,?,no,no,no,good,no,no,notckd\n',
 '19,80,1.020,0,0,normal,normal,notpresent,notpresent,107,23,0.7,141,4.2,14.4,44,?,?,no,no,no,good,no,no,notckd\n',
 '52,80,1.020,0,0,normal,normal,notpresent,notpresent,125,22,1.2,139,4.6,16.5,43,4700,4.6,no,no,no,good,no,no,notckd\n',
 '20,60,1.025,0,0,normal,normal,notpresent,notpresent,?,?,?,137,4.7,14.0,41,4500,5.5,no,no,no,good,no,no,notckd\n',
 '46,60,1.025,0,0,normal,normal,notpresent,notpresent,123,46,1.0,135,5.0,15.7,50,6300,4.8,no,no,no,good,no,no,notckd\n',
 '48,60,1.020,0,0,normal,normal,notpresent,notpresent,112,44,1.2,142,4.9,14.5,44,9400,6.4,no,no,no,good,no,no,notckd\n',
 '24,70,1.025,0,0,normal,normal,notpresent,notpresent,140,23,0.6,140,4.7,16.3,48,5800,5.6,no,no,no,good,no,no,notckd\n',
 '47,80,?,?,?,?,?,notpresent,notpresent,93,33,0.9,144,4.5,13.3,52,8100,5.2,no,no,no,good,no,no,notckd\n',
 '55,80,1.025,0,0,normal,normal,notpresent,notpresent,130,50,1.2,147,5,15.5,41,9100,6.0,no,no,no,good,no,no,notckd\n',
 '20,70,1.020,0,0,normal,normal,notpresent,notpresent,123,44,1.0,135,3.8,14.6,44,5500,4.8,no,no,no,good,no,no,notckd\n',
 '60,70,1.020,0,0,normal,normal,notpresent,notpresent,?,?,?,?,?,16.4,43,10800,5.7,no,no,no,good,no,no,notckd\n',
 '33,80,1.025,0,0,normal,normal,notpresent,notpresent,100,37,1.2,142,4.0,16.9,52,6700,6.0,no,no,no,good,no,no,notckd\n',
 '66,70,1.020,0,0,normal,normal,notpresent,notpresent,94,19,0.7,135,3.9,16.0,41,5300,5.9,no,no,no,good,no,no,notckd\n',
 '71,70,1.020,0,0,normal,normal,notpresent,notpresent,81,18,0.8,145,5.0,14.7,44,9800,6.0,no,no,no,good,no,no,notckd\n',
 '39,70,1.025,0,0,normal,normal,notpresent,notpresent,124,22,0.6,137,3.8,13.4,43,?,?,no,no,no,good,no,no,notckd\n',
 '56,70,1.025,0,0,normal,normal,notpresent,notpresent,70,46,1.2,135,4.9,15.9,50,11000,5.1,?,?,?,good,no,no,notckd\n',
 '42,70,1.020,0,0,normal,normal,notpresent,notpresent,93,32,0.9,143,4.7,16.6,43,7100,5.3,no,no,no,good,no,no,notckd\n',
 '54,70,1.020,0,0,?,?,?,?,76,28,0.6,146,3.5,14.8,52,8400,5.9,no,no,no,good,no,no,notckd\n',
 '47,80,1.025,0,0,normal,normal,notpresent,notpresent,124,44,1.0,140,4.9,14.9,41,7000,5.7,no,no,no,good,no,no,notckd\n',
 '30,80,1.020,0,0,normal,normal,notpresent,notpresent,89,42,0.5,139,5.0,16.7,52,10200,5.0,no,no,no,good,no,no,notckd\n',
 '50,?,1.020,0,0,normal,normal,notpresent,notpresent,92,19,1.2,150,4.8,14.9,48,4700,5.4,no,no,no,good,no,no,notckd\n',
 '75,60,1.020,0,0,normal,normal,notpresent,notpresent,110,50,0.7,135,5.0,14.3,40,8300,5.8,no,no,no,?,?,?,notckd\n',
 '44,70,?,?,?,?,?,notpresent,notpresent,106,25,0.9,150,3.6,15.0,50,9600,6.5,no,no,no,good,no,no,notckd\n',
 '41,70,1.020,0,0,normal,normal,notpresent,notpresent,125,38,0.6,140,5.0,16.8,41,6300,5.9,no,no,no,good,no,no,notckd\n',
 '53,60,1.025,0,0,normal,normal,notpresent,notpresent,116,26,1.0,146,4.9,15.8,45,7700,5.2,?,?,?,good,no,no,notckd\n',
 '34,60,1.020,0,0,normal,normal,notpresent,notpresent,91,49,1.2,135,4.5,13.5,48,8600,4.9,no,no,no,good,no,no,notckd\n',
 '73,60,1.020,0,0,normal,normal,notpresent,notpresent,127,48,0.5,150,3.5,15.1,52,11000,4.7,no,no,no,good,no,no,notckd\n',
 '45,60,1.020,0,0,normal,normal,?,?,114,26,0.7,141,4.2,15.0,43,9200,5.8,no,no,no,good,no,no,notckd\n',
 '44,60,1.025,0,0,normal,normal,notpresent,notpresent,96,33,0.9,147,4.5,16.9,41,7200,5.0,no,no,no,good,no,no,notckd\n',
 '29,70,1.020,0,0,normal,normal,notpresent,notpresent,127,44,1.2,145,5.0,14.8,48,?,?,no,no,no,good,no,no,notckd\n',
 '55,70,1.020,0,0,normal,normal,notpresent,notpresent,107,26,1.1,?,?,17.0,50,6700,6.1,no,no,no,good,no,no,notckd\n',
 '33,80,1.025,0,0,normal,normal,notpresent,notpresent,128,38,0.6,135,3.9,13.1,45,6200,4.5,no,no,no,good,no,no,notckd\n',
 '41,80,1.020,0,0,normal,normal,notpresent,notpresent,122,25,0.8,138,5.0,17.1,41,9100,5.2,no,no,no,good,no,no,notckd\n',
 '52,80,1.020,0,0,normal,normal,notpresent,notpresent,128,30,1.2,140,4.5,15.2,52,4300,5.7,no,no,no,good,no,no,notckd\n',
 '47,60,1.020,0,0,normal,normal,notpresent,notpresent,137,17,0.5,150,3.5,13.6,44,7900,4.5,no,no,no,good,no,no,notckd\n',
 '43,80,1.025,0,0,normal,normal,notpresent,notpresent,81,46,0.6,135,4.9,13.9,48,6900,4.9,no,no,no,good,no,no,notckd\n',
 '51,60,1.020,0,0,?,?,notpresent,notpresent,129,25,1.2,139,5.0,17.2,40,8100,5.9,no,no,no,good,no,no,notckd\n',
 '46,60,1.020,0,0,normal,normal,notpresent,notpresent,102,27,0.7,142,4.9,13.2,44,11000,5.4,no,no,no,good,no,no,notckd\n',
 '56,60,1.025,0,0,normal,normal,notpresent,notpresent,132,18,1.1,147,4.7,13.7,45,7500,5.6,no,no,no,good,no,no,notckd\n',
 '80,70,1.020,0,0,normal,normal,notpresent,notpresent,?,?,?,135,4.1,15.3,48,6300,6.1,no,no,no,good,no,no,notckd\n',
 '55,80,1.020,0,0,normal,normal,notpresent,notpresent,104,28,0.9,142,4.8,17.3,52,8200,4.8,no,no,no,good,no,no,notckd\n',
 '39,70,1.025,0,0,normal,normal,notpresent,notpresent,131,46,0.6,145,5.0,15.6,41,9400,4.7,no,no,no,good,no,no,notckd\n',
 '44,70,1.025,0,0,normal,normal,notpresent,notpresent,?,?,?,?,?,13.8,48,7800,4.4,no,no,no,good,no,no,notckd\n',
 '35,?,1.020,0,0,normal,normal,?,?,99,30,0.5,135,4.9,15.4,48,5000,5.2,no,no,no,good,no,no,notckd\n',
 '58,70,1.020,0,0,normal,normal,notpresent,notpresent,102,48,1.2,139,4.3,15.0,40,8100,4.9,no,no,no,good,no,no,notckd\n',
 '61,70,1.025,0,0,normal,normal,notpresent,notpresent,120,29,0.7,137,3.5,17.4,52,7000,5.3,no,no,no,good,no,no,notckd\n',
 '30,60,1.020,0,0,normal,normal,notpresent,notpresent,138,15,1.1,135,4.4,?,?,?,?,no,no,no,good,no,no,notckd\n',
 '57,60,1.020,0,0,normal,normal,notpresent,notpresent,105,49,1.2,150,4.7,15.7,44,10400,6.2,no,no,no,good,no,no,notckd\n',
 '65,60,1.020,0,0,normal,normal,notpresent,notpresent,109,39,1.0,144,3.5,13.9,48,9600,4.8,no,no,no,good,no,no,notckd\n',
 '70,60,?,?,?,?,?,notpresent,notpresent,120,40,0.5,140,4.6,16.0,43,4500,4.9,no,no,no,good,no,no,notckd\n',
 '43,80,1.025,0,0,normal,normal,notpresent,notpresent,130,30,1.1,143,5.0,15.9,45,7800,4.5,no,no,no,good,no,no,notckd\n',
 '40,80,1.020,0,0,normal,normal,notpresent,notpresent,119,15,0.7,150,4.9,?,?,?,?,no,no,no,good,no,no,notckd\n',
 '58,80,1.020,0,0,normal,normal,notpresent,notpresent,100,50,1.2,140,3.5,14.0,50,6700,6.5,no,no,no,good,no,no,notckd\n',
 '47,60,1.020,0,0,normal,normal,notpresent,notpresent,109,25,1.1,141,4.7,15.8,41,8300,5.2,no,no,no,good,no,no,notckd\n',
 '30,60,1.025,0,0,normal,normal,notpresent,notpresent,120,31,0.8,150,4.6,13.4,44,10700,5.8,no,no,no,good,no,no,notckd\n',
 '28,70,1.020,0,0,normal,normal,?,?,131,29,0.6,145,4.9,?,45,8600,6.5,no,no,no,good,no,no,notckd\n',
 '33,60,1.025,0,0,normal,normal,notpresent,notpresent,80,25,0.9,146,3.5,14.1,48,7800,5.1,no,no,no,good,no,no,notckd\n',
 '43,80,1.020,0,0,normal,normal,notpresent,notpresent,114,32,1.1,135,3.9,?,42,?,?,no,no,no,good,no,no,notckd\n',
 '59,70,1.025,0,0,normal,normal,notpresent,notpresent,130,39,0.7,147,4.7,13.5,46,6700,4.5,no,no,no,good,no,no,notckd\n',
 '34,70,1.025,0,0,normal,normal,notpresent,notpresent,?,33,1,150,5.0,15.3,44,10500,6.1,no,no,no,good,no,no,notckd\n',
 '23,80,1.020,0,0,normal,normal,notpresent,notpresent,99,46,1.2,142,4.0,17.7,46,4300,5.5,no,no,no,good,no,no,notckd\n',
 '24,80,1.025,0,0,normal,normal,notpresent,notpresent,125,?,?,136,3.5,15.4,43,5600,4.5,no,no,no,good,no,no,notckd\n',
 '60,60,1.020,0,0,normal,normal,notpresent,notpresent,134,45,0.5,139,4.8,14.2,48,10700,5.6,no,no,no,good,no,no,notckd\n',
 '25,60,1.020,0,0,normal,normal,notpresent,notpresent,119,27,0.5,?,?,15.2,40,9200,5.2,no,no,no,good,no,no,notckd\n',
 '44,70,1.025,0,0,normal,normal,notpresent,notpresent,92,40,0.9,141,4.9,14.0,52,7500,6.2,no,no,no,good,no,no,notckd\n',
 '62,80,1.020,0,0,normal,normal,notpresent,notpresent,132,34,0.8,147,3.5,17.8,44,4700,4.5,no,no,no,good,no,no,notckd\n',
 '25,70,1.020,0,0,normal,normal,notpresent,notpresent,88,42,0.5,136,3.5,13.3,48,7000,4.9,no,no,no,good,no,no,notckd\n',
 '32,70,1.025,0,0,normal,normal,notpresent,notpresent,100,29,1.1,142,4.5,14.3,43,6700,5.9,no,no,no,good,no,no,notckd\n',
 '63,70,1.025,0,0,normal,normal,notpresent,notpresent,130,37,0.9,150,5.0,13.4,41,7300,4.7,no,no,no,good,no,no,notckd\n',
 '44,60,1.020,0,0,normal,normal,notpresent,notpresent,95,46,0.5,138,4.2,15.0,50,7700,6.3,no,no,no,good,no,no,notckd\n',
 '37,60,1.025,0,0,normal,normal,notpresent,notpresent,111,35,0.8,135,4.1,16.2,50,5500,5.7,no,no,no,good,no,no,notckd\n',
 '64,60,1.020,0,0,normal,normal,notpresent,notpresent,106,27,0.7,150,3.3,14.4,42,8100,4.7,no,no,no,good,no,no,notckd\n',
 '22,60,1.025,0,0,normal,normal,notpresent,notpresent,97,18,1.2,138,4.3,13.5,42,7900,6.4,no,no,no,good,no,no,notckd\n',
 '33,60,?,?,?,normal,normal,notpresent,notpresent,130,41,0.9,141,4.4,15.5,52,4300,5.8,no,no,no,good,no,no,notckd\n',
 '43,60,1.025,0,0,normal,normal,notpresent,notpresent,108,25,1.0,144,5.0,17.8,43,7200,5.5,no,no,no,good,no,no,notckd\n',
 '38,80,1.020,0,0,normal,normal,notpresent,notpresent,99,19,0.5,147,3.5,13.6,44,7300,6.4,no,no,no,good,no,no,notckd\n',
 '35,70,1.025,0,0,?,?,notpresent,notpresent,82,36,1.1,150,3.5,14.5,52,9400,6.1,no,no,no,good,no,no,notckd\n',
 '65,70,1.025,0,0,?,?,notpresent,notpresent,85,20,1.0,142,4.8,16.1,43,9600,4.5,no,no,no,good,no,no,notckd\n',
 '29,80,1.020,0,0,normal,normal,notpresent,notpresent,83,49,0.9,139,3.3,17.5,40,9900,4.7,no,no,no,good,no,no,notckd\n',
 '37,60,1.020,0,0,normal,normal,notpresent,notpresent,109,47,1.1,141,4.9,15.0,48,7000,5.2,no,no,no,good,no,no,notckd\n',
 '39,60,1.020,0,0,normal,normal,notpresent,notpresent,86,37,0.6,150,5.0,13.6,51,5800,4.5,no,no,no,good,no,no,notckd\n',
 '32,60,1.025,0,0,normal,normal,notpresent,notpresent,102,17,0.4,147,4.7,14.6,41,6800,5.1,no,no,no,good,no,no,notckd\n',
 '23,60,1.020,0,0,normal,normal,notpresent,notpresent,95,24,0.8,145,5.0,15,52,6300,4.6,no,no,no,good,no,no,notckd\n',
 '34,70,1.025,0,0,normal,normal,notpresent,notpresent,87,38,0.5,144,4.8,17.1,47,7400,6.1,no,no,no,good,no,no,notckd\n',
 '66,70,1.025,0,0,normal,normal,notpresent,notpresent,107,16,1.1,140,3.6,13.6,42,11000,4.9,no,no,no,good,no,no,notckd\n',
 '47,60,1.020,0,0,normal,normal,notpresent,notpresent,117,22,1.2,138,3.5,13,45,5200,5.6,no,no,no,good,no,no,notckd\n',
 '74,60,1.020,0,0,normal,normal,notpresent,notpresent,88,50,0.6,147,3.7,17.2,53,6000,4.5,no,no,no,good,no,no,notckd\n',
 '35,60,1.025,0,0,normal,normal,notpresent,notpresent,105,39,0.5,135,3.9,14.7,43,5800,6.2,no,no,no,good,no,no,notckd\n',
 '29,80,1.020,0,0,normal,normal,notpresent,notpresent,70,16,0.7,138,3.5,13.7,54,5400,5.8,no,no,no,good,no,no,notckd\n',
 '33,80,1.025,0,0,normal,normal,notpresent,notpresent,89,19,1.1,144,5.0,15,40,10300,4.8,no,no,no,good,no,no,notckd\n',
 '67,80,1.025,0,0,normal,normal,notpresent,notpresent,99,40,0.5,?,?,17.8,44,5900,5.2,no,no,no,good,no,no,notckd\n',
 '73,80,1.025,0,0,normal,normal,notpresent,notpresent,118,44,0.7,137,3.5,14.8,45,9300,4.7,no,no,no,good,no,no,notckd\n',
 '24,80,1.020,0,0,normal,normal,notpresent,notpresent,93,46,1.0,145,3.5,?,?,10700,6.3,no,no,no,good,no,no,notckd\n',
 '60,80,1.025,0,0,normal,normal,notpresent,notpresent,81,15,0.5,141,3.6,15,46,10500,5.3,no,no,no,good,no,no,notckd\n',
 '68,60,1.025,0,0,normal,normal,notpresent,notpresent,125,41,1.1,139,3.8,17.4,50,6700,6.1,no,no,no,good,no,no,notckd\n',
 '30,80,1.025,0,0,normal,normal,notpresent,notpresent,82,42,0.7,146,5.0,14.9,45,9400,5.9,no,no,no,good,no,no,notckd\n',
 '75,70,1.020,0,0,normal,normal,notpresent,notpresent,107,48,0.8,144,3.5,13.6,46,10300,4.8,no,,no,no,good,no,no,notckd\n',
 '69,70,1.020,0,0,normal,normal,notpresent,notpresent,83,42,1.2,139,3.7,16.2,50,9300,5.4,no,no,no,good,no,no,notckd\n',
 '28,60,1.025,0,0,normal,normal,notpresent,notpresent,79,50,0.5,145,5.0,17.6,51,6500,5.0,no,no,no,good,no,no,notckd\n',
 '72,60,1.020,0,0,normal,normal,notpresent,notpresent,109,26,0.9,150,4.9,15,52,10500,5.5,no,no,no,good,no,no,notckd\n',
 '61,70,1.025,0,0,normal,normal,notpresent,notpresent,133,38,1.0,142,3.6,13.7,47,9200,4.9,no,no,no,good,no,no,notckd\n',
 '79,80,1.025,0,0,normal,normal,notpresent,notpresent,111,44,1.2,146,3.6,16.3,40,8000,6.4,no,no,no,good,no,no,notckd\n',
 '70,80,1.020,0,0,normal,normal,notpresent,notpresent,74,41,0.5,143,4.5,15.1,48,9700,5.6,no,no,no,good,no,no,notckd\n',
 '58,70,1.025,0,0,normal,normal,notpresent,notpresent,88,16,1.1,147,3.5,16.4,53,9100,5.2,no,no,no,good,no,no,notckd\n',
 '64,70,1.020,0,0,normal,normal,notpresent,notpresent,97,27,0.7,145,4.8,13.8,49,6400,4.8,no,no,no,good,no,no,notckd\n',
 '71,60,1.025,0,0,normal,normal,notpresent,notpresent,?,?,0.9,140,4.8,15.2,42,7700,5.5,no,no,no,good,no,no,notckd\n',
 '62,80,1.025,0,0,normal,normal,notpresent,notpresent,78,45,0.6,138,3.5,16.1,50,5400,5.7,no,no,no,good,no,no,notckd\n',
 '59,60,1.020,0,0,normal,normal,notpresent,notpresent,113,23,1.1,139,3.5,15.3,54,6500,4.9,no,no,no,good,no,no,notckd\n',
 '71,70,1.025,0,0,?,?,notpresent,notpresent,79,47,0.5,142,4.8,16.6,40,5800,5.9,no,no,no,good,no,no,notckd\n',
 '48,80,1.025,0,0,normal,normal,notpresent,notpresent,75,22,0.8,137,5.0,16.8,51,6000,6.5,no,no,no,good,no,no,notckd\n',
 '80,80,1.025,0,0,normal,normal,notpresent,notpresent,119,46,0.7,141,4.9,13.9,49,5100,5.0,no,no,no,good,no,no,notckd\n',
 '57,60,1.020,0,0,normal,normal,notpresent,notpresent,132,18,1.1,150,4.7,15.4,42,11000,4.5,no,no,no,good,no,no,notckd\n',
 '63,70,1.020,0,0,normal,normal,notpresent,notpresent,113,25,0.6,146,4.9,16.5,52,8000,5.1,no,no,no,good,no,no,notckd\n',
 '46,70,1.025,0,0,normal,normal,notpresent,notpresent,100,47,0.5,142,3.5,16.4,43,5700,6.5,no,no,no,good,no,no,notckd\n',
 '15,80,1.025,0,0,normal,normal,notpresent,notpresent,93,17,0.9,136,3.9,16.7,50,6200,5.2,no,no,no,good,no,no,notckd\n',
 '51,80,1.020,0,0,normal,normal,notpresent,notpresent,94,15,1.2,144,3.7,15.5,46,9500,6.4,no,no,no,good,no,no,notckd\n',
 '41,80,1.025,0,0,normal,normal,notpresent,notpresent,112,48,0.7,140,5.0,17.0,52,7200,5.8,no,no,no,good,no,no,notckd\n',
 '52,80,1.025,0,0,normal,normal,notpresent,notpresent,99,25,0.8,135,3.7,15.0,52,6300,5.3,no,no,no,good,no,no,notckd\n',
 '36,80,1.025,0,0,normal,normal,notpresent,notpresent,85,16,1.1,142,4.1,15.6,44,5800,6.3,no,no,no,good,no,no,notckd\n',
 '57,80,1.020,0,0,normal,normal,notpresent,notpresent,133,48,1.2,147,4.3,14.8,46,6600,5.5,no,no,no,good,no,no,notckd\n',
 '43,60,1.025,0,0,normal,normal,notpresent,notpresent,117,45,0.7,141,4.4,13.0,54,7400,5.4,no,no,no,good,no,no,notckd\n',
 '50,80,1.020,0,0,normal,normal,notpresent,notpresent,137,46,0.8,139,5.0,14.1,45,9500,4.6,no,no,no,good,no,no,notckd\n',
 '55,80,1.020,0,0,normal,normal,notpresent,notpresent,140,49,0.5,150,4.9,15.7,47,6700,4.9,no,no,no,good,no,no,notckd\n',
 '42,70,1.025,0,0,normal,normal,notpresent,notpresent,75,31,1.2,141,3.5,16.5,54,7800,6.2,no,no,no,good,no,no,notckd\n',
 '12,80,1.020,0,0,normal,normal,notpresent,notpresent,100,26,0.6,137,4.4,15.8,49,6600,5.4,no,no,no,good,no,no,notckd\n',
 '17,60,1.025,0,0,normal,normal,notpresent,notpresent,114,50,1.0,135,4.9,14.2,51,7200,5.9,no,no,no,good,no,no,notckd\n',
 '58,80,1.025,0,0,normal,normal,notpresent,notpresent,131,18,1.1,141,3.5,15.8,53,6800,6.1,no,no,no,good,no,no,notckd\n',
 '\n']


# In[ ]:


f_names = []


# In[ ]:


#creating list of feature names
for line in lst_f:
    if '@attribute' in line:
        spltd = line.split()
        f_names.append(spltd[1].replace("'",''))
f_names


# In[ ]:


#lists of numeric and string indexes according to info
items = list(range(25))   
num_items = items[:5] + items[9:18]
str_items = items[5:9] + items[18:25]

#function which removes garbage from strings
def garb_remove(string):
    if spltd.index(string) in num_items:
        string = ''.join(e for e in string if e.isdigit() or e == '.')
    else:
        string = ''.join(e for e in string if e.isalpha())
    return string

#function which converting strings of numbers to numbers
def convert_nums(string):    
    if spltd.index(string) in num_items:
        string = float(string)
    else:
        pass
    return string


# In[ ]:


#creating matrix from text data, deleting missing values 
f_items = []
for line in lst_f:
    if '@' not in line and '?' not in line and line is not '\n':
        spltd = line.split(',')
        spltd = [garb_remove(string) for string in spltd]
        spltd = [convert_nums(string) for string in spltd]
        f_items.append(spltd)


# In[ ]:


#creating dataframe from matrix
df = pd.DataFrame(f_items)
df = df.drop(columns = [25])
df.columns = f_names
df


# In[ ]:


#replacing empty strings with NaN and dropping rows with NaN values
df = df.replace('',np.nan)
df = df.dropna().reset_index(drop=True)


# In[ ]:


#check for NA values
df.isna().values.any()


# In[ ]:


#shape of dataframe
df.shape


# In[ ]:


#preparing variables for plotting
y_cols = [df[col] for col in df.columns[:-1]]
x = list(range(157))


# ##  <font color=black>Plots of features</font>
# Below you can see scatter and bar plots of each feature of the dataframe.
# Where x-axis is value of particular feature and y-axis is number of dataframe's instances.
# The red items are the instances with Chronic Kidney Disease and the green ones  - without.

# In[ ]:


#dividing dataframe by numerical and categorical values
y_cols_num = [y_cols[i] for i in num_items]
y_cols_cat = [y_cols[i] for i in str_items[:-1]]


# In[ ]:


#plotting bars of categorical values
for i in range(len(str_items) - 1):
    bar_values = y_cols_cat[i].value_counts()
    bar_names = bar_values.index

    c0 = df[(df['class'] == 'ckd') & (df[df.columns[str_items[i]]] == bar_names[0])].count()
    c1 = df[(df['class'] == 'ckd') & (df[df.columns[str_items[i]]] == bar_names[1])].count()
    nc0 = bar_values[0] - c0[0]
    nc1 = bar_values[1] - c1[0]
    
    p1 = plt.bar(bar_names, (nc0,nc1),color = 'red')
    p2 = plt.bar(bar_names, (c0[0],c1[0]), bottom = (nc0,nc1), color = 'green')
    plt.legend((p1[0],p2[0]),('CKD','not CKD'))
    plt.ylabel('Instances')
    plt.title(df.columns[str_items[i]],fontweight='bold')
    
    plt.show()


# In[ ]:


#scatter plots of numerical values
for y in enumerate(y_cols_num):
    fig, ax = plt.subplots()
    for cl in x:
        if df['class'][cl] == 'ckd':
            c = 'r'
        else:
            c = 'g'
        plt.xlabel('Instances')
        plt.ylabel('Values')
        plt.title(df.columns[y[0]],fontweight="bold")
        plt.autoscale(tight=True)
        plt.scatter(x[cl], y[1][cl], c=c, s=8, edgecolors='none')

    red_patch = mpatches.Patch(color='red', label='CKD')
    green_patch = mpatches.Patch(color='green', label='not CKD')

    plt.legend(handles=[red_patch,green_patch], loc='upper right')

    plt.show()


# In[ ]:


#formatting dataframe by replacing strings in it
replacements = {
    'poor' : 0.0,
    'good' : 1.0,
    'normal' : 1.0,
    'abnormal' : 0.0,
    'notpresent' : 0.0,
    'present' : 1.0,
    'yes' : 1.0,
    'no' : 0.0,
    'ckd' : 1.0,
    'notckd' : 0.0
}
df_num = df.replace(replacements)
df_num


# In[ ]:


#prepare variables for feature selection
y = df_num['class']
X = df_num.loc[:, df.columns != 'class']

X = X.apply(pd.to_numeric, errors='coerce')
y = y.apply(pd.to_numeric, errors='coerce')

X.fillna(0, inplace=True)
y.fillna(0, inplace=True)

#checking for NA values
X.isna().values.any()
y.isna().values.any()


# ##  <font color=black>Feature selection</font>
# I used feature ranking with recursive feature elimination and cross-validated selection.
# I chose this type of RFE, because it has cross-validation selection, which helped to identify threshold more precisely.

# In[ ]:


# rfecv for classification
svc = SVC(kernel="linear")

rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(3),
              scoring='accuracy')
rfecv.fit(X, y)

print("Optimal number of features : %d" % rfecv.n_features_)

# Plotting number of features and cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation score (nb of correct classifications)")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()
print(rfecv.ranking_)


# As we can see, we should use 2 features. And it's 'al' and 'cad' columns in our dataframe.

# In[ ]:


#reshape data by new features
X = df_num[['al','cad']]


# ##  <font color=black>Build models</font>
# 

# I decided to use six popular algorithms for classification:
# 
#     Logistic Regression (LR)
#     Linear Discriminant Analysis (LDA)
#     K-Nearest Neighbors (KNN)
#     Classification and Regression Trees (CART)
#     Gaussian Naive Bayes (NB)
#     Support Vector Machines (SVM)
#     
#  And for evaluation i choose Stratified Shuffle Split validation algorithm. Because provided data isn't so big, and we should check, that train and test groups contain both classes.

# In[ ]:


#randomise data
X = X.sample(n=157)
y = y.sample(n=157)
print(X,y)


# In[ ]:


# Split-out validation dataset

sss = StratifiedShuffleSplit(n_splits=3, test_size=0.20, random_state=7)
sss.get_n_splits(X, y)

print(sss)       

for train_index, test_index in sss.split(X, y):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]


# In[ ]:


# Test options and evaluation metric
seed = 7
scoring = 'accuracy'


# In[ ]:


# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
# evaluate each model in turn
results = []
names = []
for name, model in models:
    skfold = model_selection.StratifiedShuffleSplit(n_splits=3, test_size=0.20, random_state=seed)
    cv_results = model_selection.cross_val_score(model, X_train, y_train, cv=skfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)


# ##  <font color=black>Make predictions</font>
# 
# After evaluation of algorithms our goal is to choose the most accurate model.
# Moreover, we should check prediction accuracy for both classes.
# So, the "1.0" class means ckd diagnosed and the "0.0" means doesn't.<br>
# 
# For this goals i decided to make confusion matrix and classification report.

# In[ ]:


# Make predictions on validation dataset
for model in models:
    nb = model[1]
    nb.fit(X_train, y_train)
    predictions = nb.predict(X_test)

    tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()
    
    print(model[0])
    print(accuracy_score(y_test, predictions))
    print(confusion_matrix(y_test, predictions))
    print(tn, fp, fn, tp)
    print(classification_report(y_test, predictions))
    print(predictions)


# As we can see, results of evaluating may differ between several randomised splittings of dataset.
# Prediction accuracy varies between about __68%__ and __75%__ . According to outputs above, standart deviation of cross validation score in every algorithm is no more than __4%__.<br><br>
# 

# ##  <font color=black>Summary</font>
# 1. We can predict diagnosis of Chronic Kidney Disease with 68%-75% accuracy based on provided dataset.
# 2. The most valuable features for prediction of Chronic Kidney Disease are level of Albumin and Coronary Artery Disease.
# 3. Using this models there is about 3% probability to diagnose Chronic Kidney Disease in patients who doesn't have it.
# 4. Using this models there is about 25% probability to diagnose absence of Chronic Kidney Disease in patients who have this disease.
# 

# In[ ]:




