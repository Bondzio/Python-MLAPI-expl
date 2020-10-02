#Primeiramente importei as bibliotecas para manipula��o dos dados
import classification_features_test.csv as np
import classification_features_train.csv as pd
import os
import itertools
#Em seguida importei as bibliotecas de Machine Learning do Scikit Learning que
#ir�o possibilitar a gera��o de um modelo preditivo e o treinamento do mesmo.
#Aqui utilizei uma rede neural artificial (RNA):from sklearn import preprocessing.
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
#Agora importei os dados de treino e dados de teste dentro de um dataframe para
#poder manipular estes dados.
Dados_Treino = pd.read_csv("train.csv")
Dados_Teste = pd.read_csv("test.csv")
#Utilizei apenas a vari�vel: rain. Para isso,
#selecionei no dataframe de treino e teste tais colunas utilizando o c�digo abaixo.
Variaveis_Treino =pd.DataFrame(Dados_Treino, columns=['rain'])
Variaveis_Teste = pd.DataFrame(Dados_Teste, columns=['rain'])
#Em seguida declarei o modelo preditor que utilizei, no caso uma RNA
RNA = MLPClassifier()
RNA.fit(X=Variaveis_Treino,
        y=Dados_Treino["Choveu"])
#Com o modelo gerado, apliquei ele em cima dos dados de teste. Com isso ir� gerei
#um vetor de valores com as predi��es do modelo, neste caso os valores s�o 0 e 1 para
#caso chovesse e caso n�o chovesse respectivamente.
predicoes = RNA.predict(Variaveis_Teste)
print("Resultado dos dados de Teste.: ")