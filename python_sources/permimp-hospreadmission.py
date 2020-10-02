#!/usr/bin/env python
# coding: utf-8

# ### Using Permutation Importance to Identify Hospital Readmission Risk Factors

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print('Input directory listing:\n', os.listdir("../input"))

# Any results you write to the current directory are saved as output.

data = pd.read_csv('../input/train.csv')
print(data.columns)
print(data.dtypes)
print(data.head())
print(data.tail())
print(data.describe())


# In[ ]:


# perm imp for hosp readmit

# def target, features
y = data['readmitted']
X = data.loc[:, :'diabetesMed_Yes']
print('-'*74)
print('X: ', X.columns)
print('-'*74)

# train_test_split
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)
model = RandomForestClassifier(random_state=0).fit(train_X, train_y)


# In[ ]:


# perm imp
import eli5
from eli5.sklearn import PermutationImportance

perm_imp = PermutationImportance(model, random_state=1).fit(val_X, val_y)
eli5.show_weights(perm_imp, feature_names = val_X.columns.tolist())


# ### Preliminary Insights on Hospital Readmission Risk Factors:
# * Number of prior visits to the hospital (inpatient and outpatient) and emergency room (as expected)
# * Type of insurance coverage (not specified but could include Medicaid)
# * CV and Diabetes diagnoses (HF: 428, Diabetes: 250, diabetesMed_Yes) and related conditions (electrolyte imbalances: 276, heart arrhythmia: 427)
# * Disease severity: number of labs, Metformin not working (glipizide_No), seen by Cardiologist (medical_specialty_Cardiology)
# * Multiple comorbid conditions (number of diagnoses) - obesity not listed but could indicate (Pre) Metabolic Syndrome
# ***
# ### Takeaway:
# * Should probe deeper into **feature interactions** and identification of **high risk subpopulations**.

# ## Appendix
# 
# ### **Heart failure 428- >**
# * A disorder characterized by the inability of the heart to pump blood at an adequate volume to meet tissue metabolic requirements, or, the ability to do so only at an elevation in the filling pressure.
# * A heterogeneous condition in which the heart is unable to pump out sufficient blood to meet the metabolic need of the body. Heart failure can be caused by structural defects, functional abnormalities (ventricular dysfunction), or a sudden overload beyond its capacity. Chronic heart failure is more common than acute heart failure which results from sudden insult to cardiac function, such as myocardial infarction.
# * Complication of heart diseases; defective cardiac filling and/or impaired contraction and emptying, resulting in the heart's inability to pump a sufficient amount of blood to meet the needs of the body tissues or to be able to do so only with an elevated filling pressure.
# * Failure of the heart to pump a sufficient amount of blood to meet the needs of the body tissues, resulting in tissue congestion and edema. Signs and symptoms include shortness of breath, pitting edema, enlarged tender liver, engorged neck veins, and pulmonary rales.
# * Heart failure accompanied by edema, such as swelling of the legs and ankles and congestion in the lungs.
# * Heart failure is a condition in which the heart can't pump enough blood throughout the body. Heart failure does not mean that your heart has stopped or is about to stop working. It means that your heart is not able to pump blood the way it should. The weakening of the heart's pumping ability causes:
#         - blood and fluid to back up into the lungs 
#         - the buildup of fluid in the feet, ankles and legs - called edema
#         - tiredness and shortness of breath
# the leading causes of heart failure are coronary artery disease, high blood pressure and diabetes.treatment includes treating the underlying cause of your heart failure, medicines, and heart transplantation if other treatments fail.heart failure is a serious condition. About 5 million people in the United States Have heart failure. It contributes to 300,000 deaths each year.
# * Inability of the heart to pump blood at an adequate rate to fill tissue metabolic requirements or the ability to do so only at an elevated filling pressure.
# * Inability of the heart to pump blood at an adequate rate to meet tissue metabolic requirements or the ability to do so only at an elevated filling pressure.
# * Inability of the heart to pump blood at an adequate rate to meet tissue metabolic requirements. Clinical symptoms of heart failure include: unusual dyspnea on light exertion, recurrent dyspnea occurring in the supine position, fluid retention or rales, jugular venous distension, pulmonary edema on physical exam, or pulmonary edema on chest x-ray presumed to be cardiac dysfunction.
# * Weakness of the heart muscle that leads to a buildup of fluid in body tissues.

# ### **Diabetes mellitus 250- >**
# * (dye-a-bee-teez) a disease in which the body does not properly control the amount of sugar in the blood. As a result, the level of sugar in the blood is too high. This disease occurs when the body does not produce enough insulin or does not use it properly.
# 
# * A disease in which the body does not control the amount of glucose (a type of sugar) in the blood and the kidneys make a large amount of urine. This disease occurs when the body does not make enough insulin or does not use it the way it should.
# 
# * A heterogeneous group of disorders characterized by hyperglycemia and glucose intolerance.
# 
# * A metabolic disorder characterized by abnormally high blood sugar levels due to diminished production of insulin or insulin resistance/desensitization.
# 
# * Diabetes is a disease in which your blood glucose, or sugar, levels are too high. Glucose comes from the foods you eat. Insulin is a hormone that helps the glucose get into your cells to give them energy. With type 1 diabetes, your body does not make insulin. With type 2 diabetes, the more common type, your body does not make or use insulin well. Without enough insulin, the glucose stays in your blood.over time, having too much glucose in your blood can cause serious problems. It can damage your eyes, kidneys, and nerves. Diabetes can also cause heart disease, stroke and even the need to remove a limb. Pregnant women can also get diabetes, called gestational diabetes.a blood test can show if you have diabetes. Exercise, weight control and sticking to your meal plan can help control your diabetes. You should also monitor your glucose level and take medicine if prescribed. nih: national institute of diabetes and digestive and kidney diseases
# 
# **Diabetes mellitus**
# * Heterogeneous group of disorders that share glucose intolerance in common.
# 
# * Type 2 diabetes, characterized by target-tissue resistance to insulin, is epidemic in industrialized societies and is strongly associated with obesity; however, the mechanism by which increased adiposity causes insulin resistance is unclear. Adipocytes secrete a unique signalling molecule, which was named resistin (for resistance to insulin). Circulating resistin levels are decreased by the anti-diabetic drug rosiglitazone, and increased in diet-induced and genetic forms of obesity. Administration of anti-resistin antibody improves blood sugar and insulin action in mice with diet-induced obesity. Moreover, treatment of normal mice with recombinant resistin impairs glucose tolerance and insulin action. Insulin-stimulated glucose uptake by adipocytes is enhanced by neutralization of resistin and is reduced by resistin treatment. Resistin is thus a hormone that potentially links obesity to diabetes.

# ### Disorders of fluid electrolyte and acid-base balance 276- >
# **276 Disorders of fluid electrolyte and acid-base balance**
# * 276.0 Hyperosmolality and/or hypernatremia 
# * 276.1 Hyposmolality and/or hyponatremia 
# * 276.2 Acidosis 
# * 276.3 Alkalosis 
# * 276.4 Mixed acid-base balance disorder 
# * 276.5 Volume depletion disorder
#         - 276.50 Volume depletion, unspecified 
#         - 276.51 Dehydration 
#         - 276.52 Hypovolemia  
# * 276.6 Fluid overload disorder
#         - 276.61 Transfusion associated circulatory overload 
#         - 276.69 Other fluid overload 
# * 276.7 Hyperpotassemia 
# * 276.8 Hypopotassemia 
# * 276.9 Electrolyte and fluid disorders not elsewhere classified 

# **Cardiac dysrhythmias 427- >**
# * An arrhythmia is a problem with the rate or rhythm of your heartbeat. It means that your heart beats too quickly, too slowly, or with an irregular pattern. When the heart beats faster than normal, it is called tachycardia. When the heart beats too slowly, it is called bradycardia. The most common type of arrhythmia is atrial fibrillation, which causes an irregular and fast heart beat.many factors can affect your heart's rhythm, such as having had a heart attack, smoking, congenital heart defects, and stress. Some substances or medicines may also cause arrhythmias. Symptoms of arrhythmias include:
#         - fast or slow heart beat
#         - skipping beats
#         - lightheadedness or dizziness
#         - chest pain
#         - shortness of breath
#         - sweating
# your doctor can run tests to find out if you have an arrhythmia. Treatment to restore a normal heart rhythm may include medicines, an implantable cardioverter-defibrillator (icd) or pacemaker, or sometimes surgery.
# * An episodic form of supraventricular tachycardia, with abrupt onset and termination.
# * Any disturbances of the normal rhythmic beating of the heart or myocardial contraction. Cardiac arrhythmias can be classified by the abnormalities in heart rate, disorders of electrical impulse generation, or impulse conduction.
# * Any variation from the normal rate or rhythm (which may include the origin of the impulse and/or its subsequent propagation) in the heart.
# * Any variation from the normal rhythm or rate of the heart beat.
# > * Periods of very rapid heart beats that begin and end abruptly

# 
