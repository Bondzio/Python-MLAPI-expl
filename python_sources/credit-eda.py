#!/usr/bin/env python
# coding: utf-8

# import pandas as pd 
# import numpy as np 
# import seaborn as sns
# application_test=pd.read_csv(r'C:\Users\Admin\Desktop\Kaggle\application_test.csv')
# application_test.head
# ![image.png](attachment:image.png)

# import pandas as pd 
# import numpy as np 
# import seaborn as sns
# application_train=pd.read_csv(r'C:\Users\Admin\Desktop\Kaggle\application_train.csv')
# #application_train['NAME_HOUSING_TYPE'].unique()
# application_train['CODE_GENDER'].unique()
# application_train.groupby('CODE_GENDER').mean()
# ![image.png](attachment:image.png)

# > pd.crosstab(application_train.CODE_GENDER,application_train.NAME_HOUSING_TYPE, normalize=True)
# ![image.png](attachment:image.png)

# > pd.crosstab(index=application_train["CODE_GENDER"], columns=application_train["NAME_HOUSING_TYPE"]).plot(kind="bar", figsize=(8,8),stacked=True)
# ![image.png](attachment:image.png)

# > pd.crosstab(application_train.CODE_GENDER, application_train.NAME_FAMILY_STATUS, normalize='index')
# ![image.png](attachment:image.png)

# > pd.crosstab(application_train.CODE_GENDER, application_train.NAME_FAMILY_STATUS).plot(kind='bar', stacked=True)
# ![image.png](attachment:image.png)

# > import pandas as pd 
# > import numpy as np 
# > import seaborn as sns
# > application_train=pd.read_csv(r'C:\Users\Admin\Desktop\Kaggle\application_train.csv')
# > #application_train['NAME_HOUSING_TYPE'].unique()
# > %matplotlib inline
# > application_train['NAME_HOUSING_TYPE'].value_counts().plot('bar')
# ![image.png](attachment:image.png)

# ###analyst with application_test
# > import pandas as pd 
# > import numpy as np 
# > import seaborn as sns
# > application_test=pd.read_csv(r'C:\Users\Admin\Desktop\Kaggle\application_test.csv')
# > application_test['NAME_CONTRACT_TYPE'].unique()
# > pd.crosstab(application_test.NAME_CONTRACT_TYPE, application_test.NAME_HOUSING_TYPE,normalize='columns')
# ![image.png](attachment:image.png)

# > import pandas as pd
# > import pyodbc 
# > import matplotlib.pyplot as plt
# > conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=DESKTOP-LPKAQDC;'
#                       'Database=TEST;'
#                       'Trusted_Connection=yes;')
# 
# > query="SELECT [SK_ID_CURR], [NAME_CONTRACT_TYPE], [CODE_GENDER], [FLAG_OWN_CAR],[AMT_INCOME_TOTAL], [AMT_CREDIT],[AMT_ANNUITY], [DAYS_BIRTH]/-365 AS [AGE] from Test.dbo.application_test "
# > raw_data=pd.read_sql(query,conn)
# >*raw_data.head(3)
# ![image.png](attachment:image.png)

# > import matplotlib.pyplot as plt
# > sns.heatmap(raw_data.corr(), annot=True, fmt=".2f")
# > plt.show()
# ![image.png](attachment:image.png)

# > sns.pairplot(raw_data[['NAME_CONTRACT_TYPE','CODE_GENDER', 'FLAG_OWN_CAR','AMT_INCOME_TOTAL', 'AMT_CREDIT','AMT_ANNUITY']].dropna(), kind="reg")

# ![image.png](attachment:image.png)

# > import pandas as pd
# import pyodbc 
# import matplotlib.pyplot as plt
# import seaborn as sns
# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=DESKTOP-LPKAQDC;'
#                       'Database=TEST;'
#                       'Trusted_Connection=yes;')
# 
# > query="SELECT [SK_ID_CURR], [NAME_CONTRACT_TYPE], [CODE_GENDER], [FLAG_OWN_CAR],[AMT_INCOME_TOTAL], [AMT_CREDIT],[AMT_ANNUITY], [DAYS_BIRTH]/-365 AS [AGE] from Test.dbo.application_test "
# raw_data=pd.read_sql(query,conn)
# 
# > credit_card_balance=pd.read_csv(r'C:\Users\Admin\Desktop\Kaggle\credit_card_balance.csv')
# 
# > credit_card_table=pd.merge(raw_data,credit_card_balance, on='SK_ID_CURR', how='left')
# 
# > sns.pairplot(raw_data[['AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY','AGE']].dropna(), kind="scatter", hue="FLAG_OWN_CAR", plot_kws=dict(s=80, edgecolor="white", linewidth=2.5))
# > plt.show()**

# > raw_data.boxplot(column='AGE', by='NAME_CONTRACT_TYPE')

# ![image.png](attachment:image.png)

# > raw_data.boxplot(column='AMT_INCOME_TOTAL', by='FLAG_OWN_CAR',showfliers=False)
# ![image.png](attachment:image.png)

# > import matplotlib.pyplot as plt
# > sns.heatmap(data_imp[['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY']].corr(), annot=True, fmt=".2f")
# > plt.show()

# > from sklearn.feature_selection import RFE
# > from sklearn.linear_model import LogisticRegression
# > import pandas as pd
# > import pyodbc 
# > conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=DESKTOP-LPKAQDC;'
#                       'Database=TEST;'
#                       'Trusted_Connection=yes;')
# > query_02="SELECT [SK_ID_CURR], [WEEKDAY_APPR_PROCESS_START],[NAME_CONTRACT_TYPE],[NAME_HOUSING_TYPE], [NAME_INCOME_TYPE], [NAME_FAMILY_STATUS],[OCCUPATION_TYPE],[CODE_GENDER], [FLAG_OWN_CAR],[AMT_INCOME_TOTAL], [AMT_CREDIT],[AMT_ANNUITY], [DAYS_BIRTH]/-365 AS [AGE] from TEST.DBO.application_train"
# > data=pd.read_sql(query_02,conn)
# > logreg = LogisticRegression()
# > rfe = RFE(logreg,5)
# 
# > data=data[to_keep].dropna()
# > data_X=data.drop(['FLAG_OWN_CAR','SK_ID_CURR'],axis=1)
# > data_y=data['SK_ID_CURR']

# 

# 

# 

# 

# 
