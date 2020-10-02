# M�dulos utilizados
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

# Leitura dos arquivos, preenchendo valores faltantes com -1
train = pd.read_csv('../input/train.csv', index_col='sku').fillna(-1)
test = pd.read_csv('../input/test.csv', index_col='sku').fillna(-1)

# Separa��o de atributos de entrada (X) e sa�da (y)
X_train, y_train = train.drop('isBackorder', axis=1), train['isBackorder']

# Ajuste do modelo de Regress�o Log�stica
model = LogisticRegression(solver='liblinear')
model.fit(X_train, y_train)

# Predi��o da probabilidade de falta (y) para novos valores
y_pred = model.predict_proba(test)[:,1]

# Cria e salva arquivo para submiss�o
test['isBackorder'] = y_pred
pred = test['isBackorder'].reset_index()
pred.to_csv('submission.csv',index=False)