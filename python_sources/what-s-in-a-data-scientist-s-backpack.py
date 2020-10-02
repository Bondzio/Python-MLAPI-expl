#!/usr/bin/env python
# coding: utf-8

# # What's in a Data Scientist's backpack?
# 
# Data Scientist is certainly the sexiest job of the 21st century and to aspire as a data scientist includes knowing the best modern tools and techniques of the field. I've created a visualization for some of those questions that give insights into the current favourites (tool) in data science.
# 
# ![Kaggle Survey 2018](https://lh3.googleusercontent.com/_dAGBDOntAtS2atJybHI-ptSOVbd8g5JTJUyhV8vNvaBTkRvz4vymQCp7zbLCXr3n4BUNxm9_sWnSaVAvWNJsDOBrbiQmcJL5w2nPcjhSqAcF5jdTX0p2STWuZxES94AYmXh05w__1i3oo_ze1EMcC0HUTnHrmixcSH8jHhq47GItZqKMP9wvsmqevuWJZqMOKzhVVvxjdIIASVNKdUoJDnoQJaCdD5ow1AOk4mHlwXq7puAidFUuZdx0GYaP-3b2suoagI4FfSvkWGokgwRdbEG8LhKzMp9ZcK-7gPcUHBDgxL3UfFplxCHlFI_nvP8ME7VwAAAHvy2F8ssBr2Imo-2Vh2mDWZ1MUa5pF1ODdoI1OnnhhEX6S5usC_KcbVWt6x9LdT9MK7LCmtFScmQEHVMvi9SoDF6KL5aZIMDlg4eyeQR6TDbp_h8VODBY88dhOI6iIdYK8V9Q3guwJ3bKeWFkmsb9oXW9p1cSmnhqyVYwCzDvGa5WJsJpAw3puc0nJTxsKNs1R_he5R0p37Oz3yZKq-zTbmz5A26TO2Amh1byMB7Bz9fSSJPDjTfDBFAws3pH39mNFu2bhwDh2Dk5IO2vNJPYlL3GhV-9PLukkMpw68lz9llyj4gIX5Uw_llQafT6RUuIBO_V80e9xFgo-ZFRA=w542-h577-no)

# In[ ]:


import pandas as pd
import numpy as np
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
# %matplotlib inline


# In[ ]:


response = pd.read_csv('../input/freeFormResponses.csv', low_memory=False)
survey = pd.read_csv('../input/SurveySchema.csv', low_memory=False)
mcr = pd.read_csv('../input/multipleChoiceResponses.csv', low_memory=False)


# ## Data preprocessing
# 
# Basic data cleaning and pre-processing.

# In[ ]:


def clean_data(t_res_Q12):
  res_Q12 = []
  res_Q12_res = 0
  dic_res_Q12 = {}
  for i in t_res_Q12:
    if i.lower() != 'nan':
      res_Q12.append(i.lower().strip())
      res_Q12_res += 1
  del(res_Q12[0])
  temp_split = []
  temp_index = []
  for i in range(len(res_Q12)):
    if len(res_Q12[i].split()) > 1:
      temp_split += res_Q12[i].split()
      temp_index.append(i)
    elif len(res_Q12[i].split(',')) > 1:
      temp_split += res_Q12[i].split(',')
      temp_index.append(i)
    elif len(res_Q12[i].split(', ')) > 1:
      temp_split += res_Q12[i].split(',')
      temp_index.append(i)
    elif len(res_Q12[i].split('/')) > 1:
      temp_split += res_Q12[i].split(',')
      temp_index.append(i)
  for i in sorted(temp_index, reverse=True):
    del(res_Q12[i])
  res_Q12 += temp_split
  stop_words = stopwords.words('english')
  stop_words += ['none', 'nothing','use',' ', ',', '.', 'software', 'tool', 'tools', 'mostly', 'notebook', 'ide', 'studio', 'data']
  for i in res_Q12:
    if i not in stop_words:
      i = i.strip(',')
      i = i.strip()
      if i == 'microsoft' or i == 'ms':
        i = 'excel'
      elif i == 'google' or i =='sheet':
        i = 'sheets'
      elif i == 'power' or i == 'bi':
        i = 'powerbi'
      elif i == 'qlik':
        i = 'qlikview'
      elif i == 'rstudio':
        i = 'r'
      elif i == 'jupyterlab':
        i = 'jupyter'
      elif i == 'watson':
        i = 'ibm'
      elif i == 'pytorch':
        i = 'torch'
      elif i == 'vidhya' or i == 'analytics':
        i = 'analytics vidhya'
      elif i == 'science' or i == 'central':
        i = 'data science central'
      dic_res_Q12[i] = dic_res_Q12.get(i, 0) + 1
  dic_res_Q12 = sorted(dic_res_Q12.items(), key= lambda x: x[1], reverse=True)
  return dic_res_Q12


# ## Primary analysis tools
# 
# User responses for their primary analysis tools

# In[ ]:


t_res_Q12 = np.array(list(response['Q12_OTHER_TEXT']))
dic_res_Q12 = clean_data(t_res_Q12)
plt_res_Q12 = dic_res_Q12[:10]
plt.bar(range(len(plt_res_Q12)), [val[1] for val in plt_res_Q12], align='center', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q12)), [val[0] for val in plt_res_Q12])
plt.xticks(rotation=70)
plt.legend()
plt.title('Other analysis tools')
plt.draw()
plt.savefig('foo.png', bbox_inches='tight', dpi=300)
plt.show()


# ![Other analysis tools](https://lh3.googleusercontent.com/21AO6MqREvpTSdq1dgbm2qXfHYMcNb7V4henMXzmTqdxjWCZNBn7mucYHS9-vqY2p-uXHPTKfh60H4Bx8zK8xTW8dcKq0t6583KfrOr-apsZcaG9O7p8NSiAtOsy9Z0vt1foQSZbmW60s5sj_8IY1P_vU6uMqI9mAt3UMuENA2vOCixG5Ghn76zVF6TIDIZxX7G6lPdwDG4trdCiN9iKdSgVjzKALroyjWxKZ8BjdCn9CLohB6UaZMhYG-1-tS5OOi9dPGUOtUR8CsnWHsxI5VUvPKEGiTDqYXzhJXpuCwtGyN7UT4jkqcPbxcfes53HF94GdS3j2LwSpSwuzO3WZCIAERq2WXDLb4kNgScCMVx10IP9mmtRrLSNXMnugAGy37U-6cRtaCpKJ2ikM7K9iD0hyOL8PxGmdp0kf3msbl2BmzfC5DFMdJOzoq9scr1IeajsnSCOaoMHRA9wMVtgz_To8kwLQDrY1Ot3jrFTqra3iZjr2NBdQoO-wnLeu3wQLUE0XAwBc-ms9mRB1Wx6BlB4KeCTdGlKpwC1DP1gQtRzusf6grmvGSWrBaDrv8tLOzqsFMrxeAZ5s9I0bc_LRqgkU91fT2fEqhuTHHVKod8HSNEPgD13xYnK22z9-BaKol9Szn-UzuqPPoYjP1SXxkYYhA=w719-h577-no)

# ## Basic statistical analysis tools
# 
# User responses for their basic statistical analysis tools such as Microsoft Excel,  Google Sheets, etc.

# In[ ]:


t_res_Q121 = np.array(list(response['Q12_Part_1_TEXT']))
dic_res_Q121 = clean_data(t_res_Q121)
plt_res_Q121 = dic_res_Q121[:10]
plt.bar(range(len(plt_res_Q121)), [val[1] for val in plt_res_Q121], align='center', color='r', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q121)), [val[0] for val in plt_res_Q121])
plt.xticks(rotation=70)
plt.legend()
plt.title('Basic statistical analysis tools')
plt.draw()
plt.savefig('foo1.png', bbox_inches='tight', dpi=300)
plt.show()


# ![Basic statistical analysis tools](https://lh3.googleusercontent.com/cNo1pML9PdyChNUOwsmFYbKa-cw4yLFpMpvZPW96a0MeVWbwFn0V4s_Z_4Z5sOxNcgah44giRCnzQw04lCGbXIitSO2lcaWE5HtWuDxHqV4oE-YGqcfsb6P8PbuS0tJ7AWXH1ordHexmpWLmgel-Lcy59_KG9qg8Wr9NloJMm6_zGiYFi9OdGR0-6rS1RD0z1AFExMsHNvDfCNhmJFthQzIlJsmEjDDLUG6BU_H87eec-TfIx-nAtvAa5AwE1xG-9hcDIVLtQx_syvGPpQffkZ_9XnWnI-D5EGDhAeDDISwWf-Evqqel_pCzquyWNlkkaRAJYffeSKk37Fu575ypBECSVzC2jocBBKGqOGe6IwewaSg8_Ug1KO0D_eewxNgvK637-W8nx7giRKIozGEFSG8PZpBiQKKvuHSDdyXyNGZnRCXm6DFGaz857xwOAea0uopV3efypkPmiBSGO0b8Gam4LHwcnYN6AaCtvumyFuyATrASVpb27_EEErrMZNZ2l7hC-TAiPUsW1F1-T_Lacjowq6XMk9HV9da4N-P8xL8PlB2V731OQrx0M39ITG5BtSRxzb6L-JDVE6A3QCoi3r4GckbszS5qzQ0iKZsKSrOXsVlsv9fy17EMD7X-mSguiA043chUVibTMKokA9hiGNueNw=w819-h626-no)

# ## Advanced statistical analysis tools
# 
# User responses for their advanced statistical analysis tools such as SPSS, SAS, etc.

# In[ ]:


t_res_Q122 = np.array(list(response['Q12_Part_2_TEXT']))
dic_res_Q122 = clean_data(t_res_Q122)
plt_res_Q122 = dic_res_Q122[:10]
plt.bar(range(len(plt_res_Q122)), [val[1] for val in plt_res_Q122], align='center', color='g', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q122)), [val[0] for val in plt_res_Q122])
plt.xticks(rotation=70)
plt.legend()
plt.title('Advanced statistical analysis tools')
plt.draw()
plt.savefig('foo2.png', bbox_inches='tight', dpi=300)
plt.show()


# ![Advance tools](https://lh3.googleusercontent.com/7JV_6bC06wn1g_Vr8qkrflbq_pEEJEj54POQVEbtAf6bSQ7nF369Vg1bkDRMK25vVczngDJOWvugapg9WkCricLweq9P2po01071SZg_pabkl9bM-eCVXE_Us0NF0vKT8xZFhrpL53ee6vf34kS4PD6nghV57j6bzNsdtywOee6wPnPeB-1zoWdJez0Od6WkC6GYQg3uutAu-CPhaoOj5zWWiXhmT9g7uihY5BCEGvULMJrLT1LCoAT6_ohR6yJgk6cTukwNx36sG_F4bPEda1kuVfeQJpvc6JTUxPwwLtUWTr5DwVmBFlmnwm0oaKww6AgssFBPFfodoJ67nl3oIqkcPysZYnQ5dE1ehcJ_fuzWFOARRwKAsUnZc2wAPXuez_PWLnzwp6jrZvoBKCBaXtHoyek5BSVSLNnqlrloNsSCFOeI2VJBjRqQ1FQosMJcJrOsTHMvylZ8eY4sTVn6luowipYsupRZeNG-wLzcfLORaqAama6zFqmFSoaqYctDPFkPfd28f3gQapXl77e8kJZcvNFO3idu9CxOjMG63eFFa6_RQuyhvWdQkOyk3iuIN-ZmtNrIXga4mepC18iu8wX_sWH6oSV_8IcPHNQyogtKxt1HW5X6md8ww9Sr5HdDYygjZGbYZFx5fwL3ApkLdU7vcg=w814-h626-no)

# ## Business intelligence tools
# 
# User responses for business intelligence tools such as Salesforce, Tableau, Spotfire, etc.

# In[ ]:


t_res_Q123 = np.array(list(response['Q12_Part_3_TEXT']))
dic_res_Q123 = clean_data(t_res_Q123)
plt_res_Q123 = dic_res_Q123[:10]
plt.bar(range(len(plt_res_Q123)), [val[1] for val in plt_res_Q123], align='center', color='orange', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q123)), [val[0] for val in plt_res_Q123])
plt.xticks(rotation=70)
plt.legend()
plt.title('Business intelligence tools')
plt.draw()
plt.savefig('foo3.png', bbox_inches='tight', dpi=300)
plt.show()


# ![Business intelligence tools](https://lh3.googleusercontent.com/sY8QcWtQvcMZD21ytVOje1nC_hvbRxIw_he2pYfR7m7-rW3M8GUwxXd4FY8njmSNe1oULmuaeWORa_sZ2ZRLLk2z3Jg3Z-269HI_SI0zZPRf4I25v0MMfjFy-TJi3tvRtcUAobFq2gN7x7fW0Vi_yectS1c-08tzBvHnAWwGFe9p0f5e7YTCCn9C4tOSiZzT32puSiVAFinNI99Ct7DS879JI_sUXb0k9DPl2knv54Qlk4f1Hvnoz5rF3CBzVJSYkMhU8qHROgkzCP3LFnaHVFglAtZ6xX658gm2wdmr1QMRgQ80axy8hE7gvoQNLdsL-t4fGqYmXaJLxEEMkyJNbKz3XRFJ3qC156RK3mqSSCCwbQrC-STcC4cWk9B-YVslun6fK4PrH1MAmK4qampfuIbJyWtPmqXMOapwAla1Jr0Gjs6dLfD93XSMXIJ2-r_Vy_tLMmHYNTM7WyM2h08hukS8Ly19aG72dW1yFXX1JzdBWlR5dn4rtJAfca1qr8VWTjZ6Rde9pFheaNtd_wNj7JAJpDWc-IVjBDlv5kWYIpyJE3--Uzh9XrwsGTZ-OHufaaoymqR4Wvhm6JHIsaLurd0LQxz5xxPRO6oyuE-AA6uGLADK0QvobzFwrhONaX8PSGBcic1trNMUJUE2Z3PH2cPHLA=w779-h626-no)

# ## Local or hosted enviroment tools
# 
# User responses for local or hosted enviroment tools such as RStudio, JupyterLab, etc.

# In[ ]:


t_res_Q124 = np.array(list(response['Q12_Part_4_TEXT']))
dic_res_Q124 = clean_data(t_res_Q124)
plt_res_Q124 = dic_res_Q124[:10]
plt.bar(range(len(plt_res_Q124)), [val[1] for val in plt_res_Q124], align='center', color='pink', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q124)), [val[0] for val in plt_res_Q124])
plt.xticks(rotation=70)
plt.legend()
plt.title('Local or hosted enviroment tools')
plt.draw()
plt.savefig('foo4.png', bbox_inches='tight', dpi=300)
plt.show()


# ![Local or hosted env tools](https://lh3.googleusercontent.com/cVuRJKNzMeg7Gy741Cb2Srgg_E0nOpOZyaKpJNrHJ5fH7pAPFaZjefOzWC4m7irqQnSIZSY60gVTRCCAreIvyZGMehlUgQXBbnHICJt03juCWxR3BYI0ZbRjy9KUT3FURKS1--ADvEFtxl8Ot1OxHPzo87paiHQzrVhKku62cwqzZxctK3EY_n5XxOXk1ggHC4tOSitnouoUAt8OVyL06RIAPfsbClG8vVFIvDWvDQZ1KyAoNnSJ8Zzx7UjYxSBiubthEWGjCdCmEqu5IMISFm3q58-WJ-pYRcQ3lw9OT8-P4IOMbhSmryiAT-EqAzhZODVZ9rgGO0RrvvX3_gjoMpp6J7V3apaMatLWZxfY7meCruTd2-3XT7qOZStg-_ghKkgFWPp8h7pepua0Q1EhrWHJMlQj3LIHUncnutQFtMFf1HZhgRx273zlKCdx_gtdu2COMA5Lve9HO2PIgpK1zbp7n4kMbU2j0DMRLEKn0HYlfdnNZ9mpDBT91q2g8KBJX5VhZH9K7vDIWez_Q2TkpSzkfV0h14O09uHTKhCASEJX_V7MGFpG-z3u0auVdN50dQ6spj20hZgGBydVesmQY0k1C3T6DNtLhvkznin58tF1Qkvp6b_75IMHFZ4axtbD4eXBfl_KV4FU5nCJjzFnptRR-A=w790-h626-no)

# ## Cloud based tools
# 
# User responses for Cloud based tools such as AWS, GCP, Azure, etc.

# In[ ]:


t_res_Q125 = np.array(list(response['Q12_Part_5_TEXT']))
dic_res_Q125 = clean_data(t_res_Q125)
plt_res_Q125 = dic_res_Q125[:10]
plt.bar(range(len(plt_res_Q125)), [val[1] for val in plt_res_Q125], align='center', color='skyblue', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q125)), [val[0] for val in plt_res_Q125])
plt.xticks(rotation=70)
plt.legend()
plt.title('Cloud based tools')
plt.draw()
plt.savefig('foo5.png', bbox_inches='tight', dpi=300)
plt.show()


# ![Cloud based tools](https://lh3.googleusercontent.com/ywq4BDHP4S-tnsx8Qkx1MSGHXvXJMhIkcpnpS4ZWyti0w7-0J6Dskj_OsNZWsp9GUzRlWl4dg2w6eyvbGfTSK7YUAG_GiQqIDpXCGDPbkkyXJ7xttjktH1Uf2JHuYrmX2nxNp91Ijfw9jS1wtigQPWUZcuJJBP8nBuuL6PXssp3Pz0wsSRgsHYydvLYR63F-ENJGElBp5162V5HLL14Th94O0PvBirGzP2xm7Q17Ou41_Hd_4n9ZxKyoSh9oN6lKZwwk7ufC32x38_qKy4HDItFrsgFrWmjoAKpsgcdQM1BZ2BA4qhz9WaGFhz_iM3phNpjT0Noo5KiIB053QsmKRN4_9B-TS8P5ZfYUe7aeToIckvmwHkpjj-v8LIX0MBYtqa_T9w8WJZMkAx0jmoyEXnN_H6lFg0rRa2EmJpEPVsQtgONuYKldEIC4h5LVfx2c-Ht4mGbEY-3vX3AUWN5b6cW8CYZjXDr9HnKNY_xHR0vv_Ly5bVcgYtFFf-WvnxKr2qfasqg_CV0FYGbM78LAn2tY1IcgxWgNtIbWcsnWIX6QYU9nADuBXVtJjHyponM3GYlnyViPmgPIXQssgPInGyHJI9m8DS550jgFyONrdw9p3yx65BwZE0Odf6Px3KfkDCiOEyoDysjMnvVBIHS6QT3qhg=w780-h626-no)

# ## Programming language used on a regular basis
# 
# User responses for programming language used on a regular basis such as Python, JAVA, Swift, etc.

# In[ ]:


t_res_Q13 = np.array(list(response['Q16_OTHER_TEXT']))
dic_res_Q13 = clean_data(t_res_Q13)
plt_res_Q13 = dic_res_Q13[:15]
plt.bar(range(len(plt_res_Q13)), [val[1] for val in plt_res_Q13], align='center', color='purple', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q13)), [val[0] for val in plt_res_Q13])
plt.xticks(rotation=70)
plt.legend()
plt.title('Programming language used on a regular basis')
plt.draw()
plt.savefig('foo6.png', bbox_inches='tight', dpi=300)
plt.show()


# ![Programming languages](https://lh3.googleusercontent.com/y2nL69UNMoJ5zFh2PaMWbmVsLA4kcfH_X-qk3Wg0AzLCfioeEfbwnN3s8NUyIJOdPHOyVz-LoJ-V2SP0shtku3RGeg0msXw1x9Ct-tfytx8aRs5gEA-oKYs_NYtCme9gKjIUZ4CMjzxNYnc8_gHVXE9DdSV8cwn6CmT2e67bANQFdd_-eqLi2sTCfeBiwixuUUVepuzAk9Oe60Lz6uk1sB-Ne-gvT_B8DL46GWfMcncPypvqgCLbs6Zx_CpcPRgMQULUaleyKC5CpcZC_DwAQoKTnLx3oqdkuJJabjQfkLhifONOoRfEJZCIol7vfHzRKEGtUHRrwOhkImtNJupVtu_mk7fjFspB1u_q6agB8XTIc6vLI8LUlWFLajsCjM_8hCEe2gJALMqAAVKP3fc4MaCeaW5AzpbflnaVAh7ebclAWus_5TIJec6WaDBa1X1JRXgQ-5ErhalFWSizF-PWORz3SUlQFCdr-g2NQHUtb9E7uPA_JhdL2osvIMOu2Ipxff0gfFa5k2C-nuQzl5Maobb2AH5-jh8FsCGBmLepqiume8XmR541NmRv6tyKTvgAGSggA0DOdm3PJRp7M__8KswiKZfSONOXEP9fdtWWKyHBDBce-jTsMyKDI2ZYMYkEHAMlGeHBsaWB0BZ_ljlPQfRBwg=w741-h626-no)

# ## Most used ML frameworks in the past 5 years
# 
# User responses for most used ML frameworks in the past 5 years.

# In[ ]:


t_res_Q14 = np.array(list(response['Q19_OTHER_TEXT']))
dic_res_Q14 = clean_data(t_res_Q14)
plt_res_Q14 = dic_res_Q14[:15]
plt.bar(range(len(plt_res_Q14)), [val[1] for val in plt_res_Q14], align='center', color='crimson', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q14)), [val[0] for val in plt_res_Q14])
plt.xticks(rotation=70)
plt.legend()
plt.title('Most used ML frameworks in the past 5 years')
plt.draw()
plt.savefig('foo7.png', bbox_inches='tight', dpi=300)
plt.show()


# ![ML frameworks](https://lh3.googleusercontent.com/kp5z7JE3b_9m8KrNwJO9IBnGGZAJ0I2WJn6IFG_g9M3vQp1B-_Eb8gZQbpsc-O99aV7wlIvfQUYxNpHMrA4Zal-gyjZYmQdllBOjNWkopkXYu2-i0NEt-yLOaUd1k7JRdWSPaQFqpP4fzM5N5gNygVcB0JVZQH24Sg9N_7otY4f_MSCX536O8x0P75EjisiskIz6-KzjsOpNEdROM5gT-TtLYfhFo8FJZQDVCxLSwg1tFVidogPh0oQDUWIoheYJSOIaGF-pW-_-wtDETKye83nslKNsfAkkhY7Fu9kSD0F0W3ovOXxFzfs4jg3k3knXDuvkLUEvIx3YUynNf8oVixwrunB1zwhwGSh7j_t3pPUsU45bNXdgaTEFzNe1rZK9QwU3wMX437pKbg-CxiW1rWG9i4eYsJCVXTd7eTueN9TPW08wNuS3mxuRWF_yyVp6tVFBJOCJrNDRLdbvT8W3AQnbH9ESVI8sSproxw7iAEwC8HT02x11D9U8C4fhlybsU3EWokZ0c3j5tc5qHQZ_6kWZpwyMvMGROcNFfPa8lp6z9Kc3I8M1RxA6Y3oJqkIljFlUaNNXmspf1pSTtqAU3IfMDWbS74WJlmQcA50ssapO_0oKhcZqMBVZNGyStbN50y2RHjrAwP_grtgmzw-X5MM35w=w793-h626-no)

# ## Most used data visualization tools in the past 5 years
# 
# User responses for most used data visualization tools in the past 5 years.

# In[ ]:


t_res_Q15 = np.array(list(response['Q21_OTHER_TEXT']))
dic_res_Q15 = clean_data(t_res_Q15)
plt_res_Q15 = dic_res_Q15[:10]
plt.bar(range(len(plt_res_Q15)), [val[1] for val in plt_res_Q15], align='center', color='yellow', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q15)), [val[0] for val in plt_res_Q15])
plt.xticks(rotation=70)
plt.legend()
plt.title('Most used data visualization tools in the past 5 years')
plt.draw()
plt.savefig('foo8.png', bbox_inches='tight', dpi=300)
plt.show()


# ![Data Visualization tools](https://lh3.googleusercontent.com/EaMxaKpPtBvOePWwHw1IM4hKf_W4-YN9xD436xngR1m1Zcq8LWzkZtHFxpMH4rJs20lDQffh6YzcCTjVeK1Tn2vyGzma2O9DmZX1R2d8KVQEN3Rj-M9P7tQ_OiZB8lW1eU1wFCcfaeeFBhY6rdxF0PQIZcXILGrIcBxSxeCsqgcn9tjn3xkJhdkZTIs9F9wWZbPf3XOcFqVzA1_MSEpPKbyo42KcH5vRtaT8Fp4ni0Li2dpUeaoHtPyO0CGAIgPZ6K0XZBq7QQHR3rLOLdB_5fRJvSxSeCpBsdVG0LryEzpOhwTOfOMdRv6LK7ihPrLSYv_OkS2ziBgAk8rTN_nfI2gpqeYNlrN-nRSGqnrzBRvfhA6hidsZ1t7CLxJDF_8bWh0Xl8O_B0UjnP7PLXnORiU3clf4rbE7bxN3fHAPoIM6JTH9WVgf-hHOgn8ggV5QT3VJhJQdG_4jVGPZ8AQ1QHjmGNIA-7TqToWG8l4_gbUJWEgrcuyDRjoigkynW0OI6eyxqxC9waw_ocy2bGrGBtEkQ4rhAqPAMqMACjx44nuAGu8uVVeGtLCx58_JtZOqba_6H5TV5VFmLYT_Ag98O793f4x4FpIA6Z74KSddMONVWokyVk9y_j_x10GBZvlsc0MJ50FXgJyvL6_Y2xeDqOlR-g=w750-h626-no)

# ## Public dataset source
# 
# User responses for their most recognized public dataset source.

# In[ ]:


t_res_Q16 = np.array(list(response['Q33_OTHER_TEXT']))
dic_res_Q16 = clean_data(t_res_Q16)
plt_res_Q16 = dic_res_Q16[:10]
plt.bar(range(len(plt_res_Q16)), [val[1] for val in plt_res_Q16], align='center', color='violet', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q16)), [val[0] for val in plt_res_Q16])
plt.xticks(rotation=70)
plt.legend()
plt.title('Public dataset source')
plt.draw()
plt.savefig('foo9.png', bbox_inches='tight', dpi=300)
plt.show()


# ![Public dataset source](https://lh3.googleusercontent.com/8gn6XnEpfszoTi1UNHDHNMX1RYJ0eBpbkCYnEb9DgZPDkBZKS76DqoKjTiJHrwTrbDIEBBuCKFGONTYIWIjgfein7-tiTiTeCfElMsQz12mfrWYYIx2jRd7VYQNUjxKDlOwa0v91mXNELEXGZsx3m0FfxNEqvZbOGivJ55KqxdBCcYQmNuk4BqwS1e_2z_oa96cJkXtDfsvoxkiRrIePKbOwqM4_Tf7rfZE7NLX8QbZUnnh2UsAKOD0smqwG8mPmRIJcOYZ7iPAAf_zLepR9oFHDkC-JmI4V2vin0PH-c1c4cJeFOGq9RFdFNO0Uu4huLYcpL05Wtx0XzYnaYEyJb-OauFwBB3H2K2DwqGeilsePZprYRJyb-jNZQt1Os9lJU9qEFRMVGnCJUo-4tB5uLJhw4jCB3TXQZtkDSQbV6TS6VTpx6659mgntnpIrYs43nNq8kfN3CS8Eodbt15UjpcupyAOHRrcNEbhVd4YmUmcacM2ZQPZAGKdH3fRpqhlMez2KPtdzEMt_9VbxgPtfm4CEktWJifSxAiumlOWc8o8BXnWMHuaqUa6My6C8hEzItlj07mF4gov7G_Yf54Ki1EyNYwiIGtam_04y-DrmsYyGyczIMj3MsqKMI45BcoJM3BP9CKYPamM74rk4N2Y9m0y1gA=w767-h626-no)

# ## Favourite media sources for ML
# 
# User responses for their favourite media sources for ML.

# In[ ]:


t_res_Q17 = np.array(list(response['Q38_OTHER_TEXT']))
dic_res_Q17 = clean_data(t_res_Q17)
plt_res_Q17 = dic_res_Q17[:10]
plt.bar(range(len(plt_res_Q17)), [val[1] for val in plt_res_Q17], align='center', color='gold', label="Recorded user responses")
plt.xticks(range(len(plt_res_Q17)), [val[0] for val in plt_res_Q17])
plt.xticks(rotation=70)
plt.legend()
plt.title('Favourite media sources for ML')
plt.draw()
plt.savefig('foo10.png', bbox_inches='tight', dpi=300)
plt.show()


# ![Media sources](https://lh3.googleusercontent.com/FF4Gkz8Ez6HofliBqKQFAe3EbRfyaRlhE7_bdgSSP0z53UZNXGnuYaUGJXE4jrVs4AOrfQSf7jduy46v5gqNlQfqILTiDtl71UC401Eykz9G3_O_137gmGZjV5DQtPr6lFtnCv5Y1rTlZZMNbVGu_yt5Lzz755H_wS5axufubrqfUXfAgvwqQB-p6Z06rnjLHf_hSvLhL5EvknPRFhrAHJeAtN4_bUdDqu43ePc8HLWYKvKkuA3vlaV7MDOCW5wypiwoYJctJ32EtBbmW2Z72Vg2-sL_NurDGYQhpQVqW0cn3C5zIcE-9zIvqm6rRSzIubmK-te2c0dHvN0-9jCnGRqdfWRD-g-emyMDDKmN_f5FrSMhUvRdxmfBAdmu70N8N43kBD-yxs5k-j-9nOK-X9gR_RPLrFxkbU6c224Dus40Hv5z-z3H-d9DHGOBmTUgVRTYVwrTy85bbW6nlNb-IBS_zcIQOl6blRdZQ1SgHjiDkNwHzjJMNrIfYl3mcyt8hUh-6oi6MAtUk4QlOIeIY411YI4PVfjKyx8P4Xcs3T4IeTQdLZ4ZhT0snzinO_ulhBiwg5O_vDxH6J16iR-L_nMmEYuzWzpBF0C8lo9As9haMaogMNJKJbc_JJ4Sh6t9EpuCTKyckQJli6o8EeW4imAcxw=w687-h626-no)

# ## Conclusively
# 
# * Although tools do not define a datascientist, they're their greatest assets and it's important to know the trends in toolkits to maybe collborate efficiently with your team.
# * I've tried to clean and process much of the ambiguities in the responses but this may not represent appropriate trends or data.
# *  In my personal experience, there will be a stage where you'll combine multiple tools and libraries for your end product but if you're aspiring to be a data-scientist, learning the internal workings of the tools & libraries is an important experience in the early stages.
# * I'll try and figure out (hopefully) more from schema's and maybe other datasets and update the version as such. Hope this was insightful!
