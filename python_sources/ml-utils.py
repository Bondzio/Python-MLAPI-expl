"""
    Script criado para consolidar fun��es �teis utilizadas no treinamento dos mais variados modelos de
    Machine Learning.
"""

"""
--------------------------------------------
---------- IMPORTANDO BIBLIOTECAS ----------
--------------------------------------------
"""
import pandas as pd
import numpy as np
import time
from datetime import datetime
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
from viz_utils import *
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score, cross_val_predict, \
                                    learning_curve
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve, \
    accuracy_score, precision_score, recall_score, f1_score


"""
--------------------------------------------
-------- 1. MODELOS DE AGRUPAMENTO ---------
--------------------------------------------
"""


# Fun��o para plotagem do M�todo do Cotovelo (agrupamento)
def elbow_method_kmeans(df, K_min, K_max, figsize=(10, 5)):
    """
    Etapas:
        1. treinar diferentes modelos KMeans pra cada cluster no range definido
        2. plotar m�todo do cotovelo (elbow m�todo) baseado na dist�ncia euclidiana

    Argumentos:
        df -- dados j� filtrados com as colunas alvo de an�lise [pandas.DataFrame]
        K_min -- �ndice m�nimo de an�lise dos clusters [int]
        K_max -- �ndice m�ximo de an�lise dos clusters [int]
        figsize -- dimens�es da figura de plotagem [tupla]

    Retorno:
        None
    """

    # Treinando algoritmo KMeans para diferentes clusters
    square_dist = []
    for k in range(K_min, K_max):
        km = KMeans(n_clusters=k)
        km.fit(df)
        square_dist.append(km.inertia_)

    # Plotando an�lise Elbow
    fig, ax = plt.subplots(figsize=figsize)
    sns.lineplot(x=range(K_min, K_max), y=square_dist, color='cornflowerblue', marker='o')

    # Customizando gr�fico
    format_spines(ax, right_border=False)
    ax.set_title('Elbow Method - Modelo KMeans', size=14, color='dimgrey')
    ax.set_xlabel('N�mero de Clusters')
    ax.set_ylabel('Dist�ncia Euclidiana')
    plt.show()


# Fun��o para plotagem do resultado do algoritmo KMeans treinado
def plot_kmeans_clusters(df, y_kmeans, centers, figsize=(14, 7), cmap='viridis'):
    """
    Etapas:
        1. retorno de par�metros de plotagem
        3. plotagem de clusters j� preditos

    Argumentos:
        df -- conjunto de dados utilizados no algoritmo KMeans [pandas.DataFrame]
        y_kmeans -- predi��es do modelo (cluster ao qual o registro se refere) [np.array]
        centers -- centr�ides de cada cluster [np.array]
        figsize -- dimens�es da figura de plotagem [tupla]
        cmap -- mapeamento colorim�trico da plotagem [string]

    Retorno:
        None
    """

    # Retornando valores e definindo layout
    variaveis = df.columns
    X = df.values
    sns.set(style='white', palette='muted', color_codes=True)

    # Plotando gr�fico de dispers�o
    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap=cmap)
    ax.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)

    # Customizando gr�fico
    ax.set_title(f'K_Means aplicado entre {variaveis[0].upper()} e {variaveis[1].upper()}', size=14, color='dimgrey')
    format_spines(ax, right_border=False)
    ax.set_xlabel(variaveis[0])
    ax.set_ylabel(variaveis[1])
    plt.show()
    

"""
--------------------------------------------
------- 1. MODELOS DE CLASSIFICA��O --------
--------------------------------------------
"""


class BinaryBaselineClassifier():

    def __init__(self, model, set_prep, features):
        self.model = model
        self.X_train = set_prep['X_train_prep']
        self.y_train = set_prep['y_train']
        self.X_test = set_prep['X_test_prep']
        self.y_test = set_prep['y_test']
        self.features = features
        self.model_name = model.__class__.__name__

    def random_search(self, scoring, param_grid=None, cv=5):
        """
        Etapas:
            1. defini��o autom�tica de par�metros de busca caso o modelo sej� uma �rvore de Decis�o
            2. aplica��o de RandomizedSearchCV com os par�metros definidos

        Argumentos:
            scoring -- m�trica a ser otimizada durante a busca [string]
            param_grid -- dicion�rio com os par�metros a serem utilizados na busca [dict]
            tree -- flag para indicar se o modelo baseline � uma �rvore de decis�o [bool]

        Retorno:
            best_estimator_ -- melhor modelo encontrado na busca
        """

        # Validando baseline como �rvore de Decis�o (grid definido automaticamente)
        """if tree:
            param_grid = {
                'criterion': ['entropy', 'gini'],
                'max_depth': [3, 4, 5, 8, 10],
                'max_features': np.arange(1, self.X_train.shape[1]),
                'class_weight': ['balanced', None]
            }"""

        # Aplicando busca aleat�ria dos hiperpar�metros
        rnd_search = RandomizedSearchCV(self.model, param_grid, scoring=scoring, cv=cv, verbose=1,
                                        random_state=42, n_jobs=-1)
        rnd_search.fit(self.X_train, self.y_train)

        return rnd_search.best_estimator_

    def fit(self, rnd_search=False, scoring=None, param_grid=None):
        """
        Etapas:
            1. treinamento do modelo e atribui��o do resultado como um atributo da classe

        Argumentos:
            rnd_search -- flag indicativo de aplica��o de RandomizedSearchCV [bool]
            scoring -- m�trica a ser otimizada durante a busca [string]
            param_grid -- dicion�rio com os par�metros a serem utilizados na busca [dict]
            tree -- flag para indicar se o modelo baseline � uma �rvore de decis�o [bool]

        Retorno:
            None
        """

        # Treinando modelo de acordo com o argumento selecionado
        if rnd_search:
            print(f'Treinando modelo {self.model_name} com RandomSearchCV.')
            self.trained_model = self.random_search(param_grid=param_grid, scoring=scoring)
            print(f'Treinamento finalizado com sucesso! Configura��es do modelo: \n\n{self.trained_model}')
        else:
            print(f'Treinando modelo {self.model_name}.')
            self.trained_model = self.model.fit(self.X_train, self.y_train)
            print(f'Treinamento finalizado com sucesso! Configura��es do modelo: \n\n{self.trained_model}')

    def evaluate_performance(self, approach, cv=5, test=False):
        """
        Etapas:
            1. medi��o das principais m�tricas pro modelo

        Argumentos:
            cv -- n�mero de k-folds durante a aplica��o do cross validation [int]

        Retorno:
            df_performance -- DataFrame contendo a performance do modelo frente as m�tricas [pandas.DataFrame]
        """

        # Iniciando medi��o de tempo
        t0 = time.time()

        if test:
            # Retornando predi��es com os dados de teste
            y_pred = self.trained_model.predict(self.X_test)
            y_proba = self.trained_model.predict_proba(self.X_test)[:, 1]

            # Retornando m�tricas para os dados de teste
            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred)
            recall = recall_score(self.y_test, y_pred)
            f1 = f1_score(self.y_test, y_pred)
            auc = roc_auc_score(self.y_test, y_proba)
        else:
            # Avaliando principais m�tricas do modelo atrav�s de valida��o cruzada
            accuracy = cross_val_score(self.trained_model, self.X_train, self.y_train, cv=cv,
                                       scoring='accuracy').mean()
            precision = cross_val_score(self.trained_model, self.X_train, self.y_train, cv=cv,
                                        scoring='precision').mean()
            recall = cross_val_score(self.trained_model, self.X_train, self.y_train, cv=cv,
                                     scoring='recall').mean()
            f1 = cross_val_score(self.trained_model, self.X_train, self.y_train, cv=cv,
                                 scoring='f1').mean()

            # AUC score
            try:
                y_scores = cross_val_predict(self.trained_model, self.X_train, self.y_train, cv=cv,
                                             method='decision_function')
            except:
                # Modelos baseados em �rvores n�o possuem o m�todo 'decision_function', mas sim 'predict_proba'
                y_probas = cross_val_predict(self.trained_model, self.X_train, self.y_train, cv=cv,
                                             method='predict_proba')
                y_scores = y_probas[:, 1]
            # Calculando AUC
            auc = roc_auc_score(self.y_train, y_scores)

        # Finalizando medi��o de tempo
        t1 = time.time()
        delta_time = t1 - t0

        # Salvando dados em um DataFrame
        performance = {}
        performance['approach'] = approach
        performance['acc'] = round(accuracy, 4)
        performance['precision'] = round(precision, 4)
        performance['recall'] = round(recall, 4)
        performance['f1'] = round(f1, 4)
        performance['auc'] = round(auc, 4)
        performance['total_time'] = round(delta_time, 3)

        df_performance = pd.DataFrame(performance, index=performance.keys()).reset_index(drop=True).loc[:0, :]
        df_performance.index = [self.model_name]

        return df_performance

    def plot_confusion_matrix(self, classes, cv=5, cmap=plt.cm.Blues, title='Confusion Matrix', normalize=False):
        """
        Etapas:
            1. c�lculo de matriz de confus�o utilizando predi��es com cross-validation
            2. configura��o e constru��o de plotagem
            3. formata��o dos labels da plotagem

        Argumentos:
            classes -- nome das classes envolvidas no modelo [list]
            cv -- n�mero de folds aplicados na valida��o cruzada [int - default: 5]
            cmap -- mapeamento colorim�trico da matriz [plt.colormap - default: plt.cm.Blues]
            title -- t�tulo da matriz de confus�o [string - default: 'Confusion Matrix']
            normaliza -- indicador para normaliza��o dos dados da matriz [bool - default: False]

        Retorno
        """

        # Realizando predi��es e retornando matriz de confus�o
        y_pred = cross_val_predict(self.trained_model, self.X_train, self.y_train, cv=cv)
        conf_mx = confusion_matrix(self.y_train, y_pred)

        # Plotando matriz
        sns.set(style='white', palette='muted', color_codes=True)
        plt.imshow(conf_mx, interpolation='nearest', cmap=cmap)
        plt.colorbar()
        tick_marks = np.arange(len(classes))

        # Customizando eixos
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        # Customizando entradas
        fmt = '.2f' if normalize else 'd'
        thresh = conf_mx.max() / 2.
        for i, j in itertools.product(range(conf_mx.shape[0]), range(conf_mx.shape[1])):
            plt.text(j, i, format(conf_mx[i, j]),
                     horizontalalignment='center',
                     color='white' if conf_mx[i, j] > thresh else 'black')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.title(title, size=14)

    def plot_roc_curve(self, cv=5):
        """
        Etapas:
            1. retorno dos scores do modelo utilizando predi��o por valida��o cruzada
            2. encontro das taxas de falsos positivos e verdadeiros negativos
            3. c�lculo da m�trica AUC e plotagem da curva ROC

        Argumentos:
            cv -- n�mero de k-folds utilizados na valida��o cruzada [int - default: 5]

        Retorno:
            None
        """

        # Calculando scores utilizando predi��o por valida��o cruzada
        try:
            y_scores = cross_val_predict(self.trained_model, self.X_train, self.y_train, cv=cv,
                                         method='decision_function')
        except:
            # Algoritmos baseados em �rvore n�o possuem o methodo "decision_function"
            y_probas = cross_val_predict(self.trained_model, self.X_train, self.y_train, cv=cv,
                                         method='predict_proba')
            y_scores = y_probas[:, 1]

        # Calculando taxas de falsos positivos e verdadeiros positivos
        fpr, tpr, thresholds = roc_curve(self.y_train, y_scores)
        auc = roc_auc_score(self.y_train, y_scores)

        # Plotando curva ROC
        plt.plot(fpr, tpr, linewidth=2, label=f'{self.model_name} auc={auc: .3f}')
        plt.plot([0, 1], [0, 1], 'k--')
        plt.axis([-0.02, 1.02, -0.02, 1.02])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()

    def feature_importance_analysis(self):
        """
        Etapas:
            1. retorno de import�ncia das features
            2. constru��o de um DataFrame com as features mais importantes pro modelo

        Argumentos:
            None

        Retorno:
            feat_imp -- DataFrame com feature importances [pandas.DataFrame]
        """

        # Retornando feature importance do modelo
        importances = self.trained_model.feature_importances_
        feat_imp = pd.DataFrame({})
        feat_imp['feature'] = self.features
        feat_imp['importance'] = importances
        feat_imp = feat_imp.sort_values(by='importance', ascending=False)
        feat_imp.reset_index(drop=True, inplace=True)

        return feat_imp

    def plot_learning_curve(self, ylim=None, cv=5, n_jobs=1, train_sizes=np.linspace(.1, 1.0, 10),
                            figsize=(12, 6)):
        """
        Etapas:
            1. c�lculo dos scores de treino e valida��o de acordo com a quantidade m de dados
            2. c�lculo de par�metros estat�sticos (m�dia e desvio padr�o) dos scores
            3. plotagem da curva de aprendizado de treino e valida��o

        Argumentos:
            y_lim -- defini��o de limites do eixo y [list - default: None]
            cv -- k folds na aplica��o de valida��o cruzada [int - default: 5]
            n_jobs -- n�mero de jobs durante a execu��o da fun��o learning_curve [int - default: 1]
            train_sizes -- tamanhos considerados para as fatias do dataset [np.array - default: linspace(.1, 1, 10)]
            figsize -- dimens�es da plotagem gr�fica [tupla - default: (12, 6)]

        Retorno:
            None
        """

        # Retornando par�metros de scores de treino e valida��o
        train_sizes, train_scores, val_scores = learning_curve(self.trained_model, self.X_train, self.y_train,
                                                               cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)

        # Calculando m�dias e desvios padr�o (treino e valida��o)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        val_scores_mean = np.mean(val_scores, axis=1)
        val_scores_std = np.std(val_scores, axis=1)

        # Plotando gr�fico de curva de aprendizado
        fig, ax = plt.subplots(figsize=figsize)

        # Resultado em dados de treino
        ax.plot(train_sizes, train_scores_mean, 'o-', color='navy', label='Training Score')
        ax.fill_between(train_sizes, (train_scores_mean - train_scores_std), (train_scores_mean + train_scores_std),
                        alpha=0.1, color='blue')

        # Resultado em valida��o cruzada
        ax.plot(train_sizes, val_scores_mean, 'o-', color='red', label='Cross Val Score')
        ax.fill_between(train_sizes, (val_scores_mean - val_scores_std), (val_scores_mean + val_scores_std),
                        alpha=0.1, color='crimson')

        # Customizando gr�fico
        ax.set_title(f'Modelo {self.model_name} - Curva de Aprendizado', size=14)
        ax.set_xlabel('Training size (m)')
        ax.set_ylabel('Score')
        ax.grid(True)
        ax.legend(loc='best')
        plt.show()


"""
--------------------------------------------
------ 2. AN�LISE DE CLASSIFICADORES -------
--------------------------------------------
"""


class BinaryClassifiersAnalysis():

    def __init__(self):
        self.classifiers_info = {}

    def fit(self, classifiers, X, y, approach='', random_search=False, scoring='roc_auc', cv=5, verbose=5, n_jobs=-1):
        """
        Par�metros
        ----------
        classifiers: conjunto de classificadores em forma de dicion�rio [dict]
        X: array com os dados a serem utilizados no treinamento [np.array]
        y: array com o vetor target do modelo [np.array]

        Retorno
        -------
        None
        """

        # Iterando sobre cada modelo no dicion�rio de classificadores
        for model_name, model_info in classifiers.items():
            clf_key = model_name + approach
            print(f'Training model {clf_key}\n')
            self.classifiers_info[clf_key] = {}

            # Validando aplica��o de RandomizedSearchCV
            if random_search:
                rnd_search = RandomizedSearchCV(model_info['model'], model_info['params'], scoring=scoring, cv=cv,
                                                verbose=verbose, random_state=42, n_jobs=n_jobs)
                rnd_search.fit(X, y)
                self.classifiers_info[clf_key]['estimator'] = rnd_search.best_estimator_
            else:
                self.classifiers_info[clf_key]['estimator'] = model_info['model'].fit(X, y)

    def compute_train_performance(self, model_name, estimator, X, y, cv=5):
        """
        Par�metros
        ----------
        classifiers: conjunto de classificadores em forma de dicion�rio [dict]
        X: array com os dados a serem utilizados no treinamento [np.array]
        y: array com o vetor target do modelo [np.array]

        Retorno
        -------
        None
        """

        # Computando as principais m�tricas por valida��o cruzada
        t0 = time.time()
        accuracy = cross_val_score(estimator, X, y, cv=cv, scoring='accuracy').mean()
        precision = cross_val_score(estimator, X, y, cv=cv, scoring='precision').mean()
        recall = cross_val_score(estimator, X, y, cv=cv, scoring='recall').mean()
        f1 = cross_val_score(estimator, X, y, cv=cv, scoring='f1').mean()

        # Probabilidades para o c�lculo da AUC
        try:
            y_scores = cross_val_predict(estimator, X, y, cv=cv, method='decision_function')
        except:
            # Modelos baseados em �rvores n�o possuem o m�todo 'decision_function', mas sim 'predict_proba'
            y_probas = cross_val_predict(estimator, X, y, cv=cv, method='predict_proba')
            y_scores = y_probas[:, 1]
        auc = roc_auc_score(y, y_scores)

        # Salvando scores no dicion�rio do classificador
        self.classifiers_info[model_name]['train_scores'] = y_scores

        # Criando DataFrame com as m�tricas
        t1 = time.time()
        delta_time = t1 - t0
        train_performance = {}
        train_performance['model'] = model_name
        train_performance['approach'] = f'Treino {cv} K-folds'
        train_performance['acc'] = round(accuracy, 4)
        train_performance['precision'] = round(precision, 4)
        train_performance['recall'] = round(recall, 4)
        train_performance['f1'] = round(f1, 4)
        train_performance['auc'] = round(auc, 4)
        train_performance['total_time'] = round(delta_time, 3)

        df_train_performance = pd.DataFrame(train_performance,
                                            index=train_performance.keys()).reset_index(drop=True).loc[:0, :]

        return df_train_performance

    def compute_test_performance(self, model_name, estimator, X, y, cv=5):
        """
        Par�metros
        ----------
        classifiers: conjunto de classificadores em forma de dicion�rio [dict]
        X: array com os dados a serem utilizados no treinamento [np.array]
        y: array com o vetor target do modelo [np.array]

        Retorno
        -------
        None
        """

        # Calculando predi��es e scores com dados de treino
        t0 = time.time()
        y_pred = estimator.predict(X)
        y_proba = estimator.predict_proba(X)
        y_scores = y_proba[:, 1]

        # Retornando m�tricas para os dados de teste
        accuracy = accuracy_score(y, y_pred)
        precision = precision_score(y, y_pred)
        recall = recall_score(y, y_pred)
        f1 = f1_score(y, y_pred)
        auc = roc_auc_score(y, y_scores)

        # Salvando probabilidades nos stats dos classificadores treinados
        self.classifiers_info[model_name]['test_scores'] = y_scores

        # Cria��o de DataFrame para aloca��o das m�tricas
        t1 = time.time()
        delta_time = t1 - t0
        test_performance = {}
        test_performance['model'] = model_name
        test_performance['approach'] = f'Teste'
        test_performance['acc'] = round(accuracy, 4)
        test_performance['precision'] = round(precision, 4)
        test_performance['recall'] = round(recall, 4)
        test_performance['f1'] = round(f1, 4)
        test_performance['auc'] = round(auc, 4)
        test_performance['total_time'] = round(delta_time, 3)

        df_test_performance = pd.DataFrame(test_performance,
                                           index=test_performance.keys()).reset_index(drop=True).loc[:0, :]

        return df_test_performance

    def evaluate_performance(self, X_train, y_train, X_test, y_test, cv=5, approach=''):
        """
        Par�metros
        ----------
        classifiers: conjunto de classificadores em forma de dicion�rio [dict]
        X: array com os dados a serem utilizados no treinamento [np.array]
        y: array com o vetor target do modelo [np.array]

        Retorno
        -------
        None
        """

        # Iterando sobre cada classificador j� treinado
        df_performances = pd.DataFrame({})
        for model_name, model_info in self.classifiers_info.items():

            # Verificando se o modelo j� foi avaliado anteriormente
            if 'train_performance' in model_info.keys():
                df_performances = df_performances.append(model_info['train_performance'])
                df_performances = df_performances.append(model_info['test_performance'])
                continue

            # Indexando vari�veis para os c�lculos
            print(f'Evaluating model {model_name}\n')
            estimator = model_info['estimator']

            # Retornando m�tricas nos dados de treino
            train_performance = self.compute_train_performance(model_name, estimator, X_train, y_train)
            test_performance = self.compute_test_performance(model_name, estimator, X_test, y_test)

            # Salvando resultados no dicion�rio do modelo
            self.classifiers_info[model_name]['train_performance'] = train_performance
            self.classifiers_info[model_name]['test_performance'] = test_performance

            # Retornando DataFrame �nico com as performances obtidas
            model_performance = train_performance.append(test_performance)
            df_performances = df_performances.append(model_performance)

            # Salvando conjuntos de dados como atributos para acesso futuro
            model_data = {
                'X_train': X_train,
                'y_train': y_train,
                'X_test': X_test,
                'y_test': y_test
            }
            model_info['model_data'] = model_data

        return df_performances

    def feature_importance_analysis(self, features, specific_model=None, graph=True, ax=None, top_n=30,
                                    palette='viridis'):
        """
        Par�metros
        ----------
        classifiers: conjunto de classificadores em forma de dicion�rio [dict]
        X: array com os dados a serem utilizados no treinamento [np.array]
        y: array com o vetor target do modelo [np.array]

        Retorno
        -------
        None
        """

        # Iterando sobre cada um dos classificadores j� treinados
        feat_imp = pd.DataFrame({})
        for model_name, model_info in self.classifiers_info.items():
            # Criando DataFrame com as features importances
            try:
                importances = model_info['estimator'].feature_importances_
            except:
                continue
            feat_imp['feature'] = features
            feat_imp['importance'] = importances
            feat_imp.sort_values(by='importance', ascending=False, inplace=True)
            feat_imp.reset_index(drop=True, inplace=True)

            # Salvando set de feature importances no dicion�rio do classificador
            self.classifiers_info[model_name]['feature_importances'] = feat_imp

        # Retornando feature importances de um classificador espec�fico
        if specific_model is not None:
            try:
                model_feature_importance = self.classifiers_info[specific_model]['feature_importances']
                if graph:  # Plotando gr�fico
                    sns.barplot(x='importance', y='feature', data=model_feature_importance.iloc[:top_n, :],
                                ax=ax, palette=palette)
                    format_spines(ax, right_border=False)
                    ax.set_title(f'Top {top_n} {model_name} Features mais Relevantes', size=14, color='dimgrey')
                return model_feature_importance
            except:
                print(f'Classificador {specific_model} n�o foi treinado.')
                print(f'Op��es poss�veis: {list(self.classifiers_info.keys())}')
                return None

        # Validando combina��o incoerente de argumentos
        if graph and specific_model is None:
            print('Por favor, escolha um modelo espec�fico para visualizar o gr�fico das feature importances')
            return None

    def plot_roc_curve(self, figsize=(16, 6)):
        """
        Par�metros
        ----------
        classifiers: conjunto de classificadores em forma de dicion�rio [dict]
        X: array com os dados a serem utilizados no treinamento [np.array]
        y: array com o vetor target do modelo [np.array]

        Retorno
        -------
        None
        """

        # Criando figura para plotagem da curva ROC
        fig, axs = plt.subplots(ncols=2, figsize=figsize)

        # Iterando sobre cada um dos classificadores treinados
        for model_name, model_info in self.classifiers_info.items():
            # Retornando conjuntos y do modelo
            y_train = model_info['model_data']['y_train']
            y_test = model_info['model_data']['y_test']

            # Retornando scores
            train_scores = model_info['train_scores']
            test_scores = model_info['test_scores']

            # Calculando taxas de falsos positivos e verdadeiros positivos
            train_fpr, train_tpr, train_thresholds = roc_curve(y_train, train_scores)
            test_fpr, test_tpr, test_thresholds = roc_curve(y_test, test_scores)

            # Retornando AUC pra treino e teste
            train_auc = model_info['train_performance']['auc'].values[0]
            test_auc = model_info['test_performance']['auc'].values[0]

            # Plotando gr�fico (dados de treino)
            plt.subplot(1, 2, 1)
            plt.plot(train_fpr, train_tpr, linewidth=2, label=f'{model_name} auc={train_auc}')
            plt.plot([0, 1], [0, 1], 'k--')
            plt.axis([-0.02, 1.02, -0.02, 1.02])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title(f'ROC Curve - Train Data')
            plt.legend()

            # Plotando gr�fico (dados de teste)
            plt.subplot(1, 2, 2)
            plt.plot(test_fpr, test_tpr, linewidth=2, label=f'{model_name} auc={test_auc}')
            plt.plot([0, 1], [0, 1], 'k--')
            plt.axis([-0.02, 1.02, -0.02, 1.02])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title(f'ROC Curve - Test Data', size=12)
            plt.legend()

        plt.show()

    def custom_confusion_matrix(self, model_name, y_true, y_pred, classes, cmap, normalize=False):
        """
        Par�metros
        ----------
        classifiers: conjunto de classificadores em forma de dicion�rio [dict]
        X: array com os dados a serem utilizados no treinamento [np.array]
        y: array com o vetor target do modelo [np.array]

        Retorno
        -------
        None
        """

        # Retornando matriz de confus�o
        conf_mx = confusion_matrix(y_true, y_pred)

        # Plotando matriz
        plt.imshow(conf_mx, interpolation='nearest', cmap=cmap)
        plt.colorbar()
        tick_marks = np.arange(len(classes))

        # Customizando eixos
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        # Customizando entradas
        fmt = '.2f' if normalize else 'd'
        thresh = conf_mx.max() / 2.
        for i, j in itertools.product(range(conf_mx.shape[0]), range(conf_mx.shape[1])):
            plt.text(j, i, format(conf_mx[i, j]),
                     horizontalalignment='center',
                     color='white' if conf_mx[i, j] > thresh else 'black')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.title(f'{model_name}\nConfusion Matrix', size=12)

    def plot_confusion_matrix(self, classes, normalize=False, cmap=plt.cm.Blues):
        """
        Par�metros
        ----------
        classifiers: conjunto de classificadores em forma de dicion�rio [dict]
        X: array com os dados a serem utilizados no treinamento [np.array]
        y: array com o vetor target do modelo [np.array]

        Retorno
        -------
        None
        """

        k = 1
        nrows = len(self.classifiers_info.keys())
        fig = plt.figure(figsize=(10, nrows * 4))
        sns.set(style='white', palette='muted', color_codes=True)

        # Iterando por cada um dos classificadores
        for model_name, model_info in self.classifiers_info.items():
            # Retornando dados em cada modelo
            X_train = model_info['model_data']['X_train']
            y_train = model_info['model_data']['y_train']
            X_test = model_info['model_data']['X_test']
            y_test = model_info['model_data']['y_test']

            # Realizando predi��es e retornando matriz de confus�o
            train_pred = cross_val_predict(model_info['estimator'], X_train, y_train, cv=5)
            test_pred = model_info['estimator'].predict(X_test)

            # Plotando matriz (dados de treino)
            plt.subplot(nrows, 2, k)
            self.custom_confusion_matrix(model_name + ' Train', y_train, train_pred, classes=classes, cmap=cmap,
                                         normalize=normalize)
            k += 1

            # Plotando matriz (dados de teste)
            plt.subplot(nrows, 2, k)
            self.custom_confusion_matrix(model_name + ' Test', y_test, test_pred, classes=classes, cmap=plt.cm.Greens,
                                         normalize=normalize)
            k += 1

        plt.tight_layout()
        plt.show()

    def plot_learning_curve(self, model_name, ax, ylim=None, cv=5, n_jobs=1, train_sizes=np.linspace(.1, 1.0, 10)):
        """
        Par�metros
        ----------
        classifiers: conjunto de classificadores em forma de dicion�rio [dict]
        X: array com os dados a serem utilizados no treinamento [np.array]
        y: array com o vetor target do modelo [np.array]

        Retorno
        -------
        None
        """

        # Retornando modelo a ser avaliado
        try:
            model = self.classifiers_info[model_name]
        except:
            print(f'Classificador {model_name} n�o foi treinado.')
            print(f'Op��es poss�veis: {list(self.classifiers_info.keys())}')
            return None

        # Retornando dados em cada modelo
        X_train = model['model_data']['X_train']
        y_train = model['model_data']['y_train']
        X_test = model['model_data']['X_test']
        y_test = model['model_data']['y_test']

        # Retornando par�metros de scores de treino e valida��o
        train_sizes, train_scores, val_scores = learning_curve(model['estimator'], X_train, y_train, cv=cv,
                                                               n_jobs=n_jobs, train_sizes=train_sizes)

        # Calculando m�dias e desvios padr�o (treino e valida��o)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        val_scores_mean = np.mean(val_scores, axis=1)
        val_scores_std = np.std(val_scores, axis=1)

        # Resultado em dados de treino
        ax.plot(train_sizes, train_scores_mean, 'o-', color='navy', label='Training Score')
        ax.fill_between(train_sizes, (train_scores_mean - train_scores_std), (train_scores_mean + train_scores_std),
                        alpha=0.1, color='blue')

        # Resultado em valida��o cruzada
        ax.plot(train_sizes, val_scores_mean, 'o-', color='red', label='Cross Val Score')
        ax.fill_between(train_sizes, (val_scores_mean - val_scores_std), (val_scores_mean + val_scores_std),
                        alpha=0.1, color='crimson')

        # Customizando gr�fico
        ax.set_title(f'Model {model_name} - Learning Curve', size=14)
        ax.set_xlabel('Training size (m)')
        ax.set_ylabel('Score')
        ax.grid(True)
        ax.legend(loc='best')

    def plot_score_distribution(self, model_name, shade=False):
        """
        Par�metros
        ----------
        classifiers: conjunto de classificadores em forma de dicion�rio [dict]
        X: array com os dados a serem utilizados no treinamento [np.array]
        y: array com o vetor target do modelo [np.array]

        Retorno
        -------
        None
        """

        # Retornando modelo a ser avaliado
        try:
            model = self.classifiers_info[model_name]
        except:
            print(f'Classificador {model_name} n�o foi treinado.')
            print(f'Op��es poss�veis: {list(self.classifiers_info.keys())}')
            return None

        # Retornando conjuntos y do modelo
        y_train = self.classifiers_info[model_name]['model_data']['y_train']
        y_test = self.classifiers_info[model_name]['model_data']['y_test']

        # Retornando scores de treino e de teste
        train_scores = self.classifiers_info[model_name]['train_scores']
        test_scores = self.classifiers_info[model_name]['test_scores']

        # Plotando distribui��o de scores
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(16, 5))
        sns.kdeplot(train_scores[y_train == 1], ax=axs[0], label='y=1', shade=shade, color='darkslateblue')
        sns.kdeplot(train_scores[y_train == 0], ax=axs[0], label='y=0', shade=shade, color='crimson')
        sns.kdeplot(test_scores[y_test == 1], ax=axs[1], label='y=1', shade=shade, color='darkslateblue')
        sns.kdeplot(test_scores[y_test == 0], ax=axs[1], label='y=0', shade=shade, color='crimson')

        # Customizando plotagem
        format_spines(axs[0], right_border=False)
        format_spines(axs[1], right_border=False)
        axs[0].set_title('Score Distribution - Training Data', size=12, color='dimgrey')
        axs[1].set_title('Score Distribution - Testing Data', size=12, color='dimgrey')
        plt.suptitle(f'Score Distribution: a Probability Approach for {model_name}\n', size=14, color='black')
        plt.show()

    def plot_score_bins(self, model_name, bin_range):
        """
        Etapas:

        Argumentos:

        Retorno:
        """

        # Retornando modelo a ser avaliado
        try:
            model = self.classifiers_info[model_name]
        except:
            print(f'Classificador {model_name} n�o foi treinado.')
            print(f'Op��es poss�veis: {list(self.classifiers_info.keys())}')
            return None

        # Criando array de bins
        bins = np.arange(0, 1.01, bin_range)
        bins_labels = [str(round(list(bins)[i - 1], 2)) + ' a ' + str(round(list(bins)[i], 2)) for i in range(len(bins))
                       if i > 0]

        # Retornando scores de treino e criando um DataFrame
        train_scores = self.classifiers_info[model_name]['train_scores']
        y_train = self.classifiers_info[model_name]['model_data']['y_train']
        df_train_scores = pd.DataFrame({})
        df_train_scores['scores'] = train_scores
        df_train_scores['target'] = y_train
        df_train_scores['faixa'] = pd.cut(train_scores, bins, labels=bins_labels)

        # Calculando distribui��o por cada faixa - treino
        df_train_rate = pd.crosstab(df_train_scores['faixa'], df_train_scores['target'])
        df_train_percent = df_train_rate.div(df_train_rate.sum(1).astype(float), axis=0)

        # Retornando scores de teste e criando um DataFrame
        test_scores = self.classifiers_info[model_name]['test_scores']
        y_test = self.classifiers_info[model_name]['model_data']['y_test']
        df_test_scores = pd.DataFrame({})
        df_test_scores['scores'] = test_scores
        df_test_scores['target'] = y_test
        df_test_scores['faixa'] = pd.cut(test_scores, bins, labels=bins_labels)

        # Calculando distribui��o por cada faixa - teste
        df_test_rate = pd.crosstab(df_test_scores['faixa'], df_test_scores['target'])
        df_test_percent = df_test_rate.div(df_test_rate.sum(1).astype(float), axis=0)

        # Definindo figura de plotagem
        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))

        # Plotando gr�ficos de volumetria de cada classe por faixa
        for df_scores, ax in zip([df_train_scores, df_test_scores], [axs[0, 0], axs[0, 1]]):
            sns.countplot(x='faixa', data=df_scores, hue='target', ax=ax, palette=['darkslateblue', 'crimson'])
            AnnotateBars(n_dec=0, color='dimgrey').vertical(ax)
            ax.legend(loc='upper right')
            format_spines(ax, right_border=False)

        # Plotando percentual de representatividade de cada classe por faixa
        for df_percent, ax in zip([df_train_percent, df_test_percent], [axs[1, 0], axs[1, 1]]):
            df_percent.plot(kind='bar', ax=ax, stacked=True, color=['darkslateblue', 'crimson'], width=0.6)

            # Customizando plotagem
            for p in ax.patches:
                # Coletando par�metros para r�tulos
                height = p.get_height()
                width = p.get_width()
                x = p.get_x()
                y = p.get_y()

                # Formatando par�metros coletados e inserindo no gr�fico
                label_text = f'{round(100 * height, 1)}%'
                label_x = x + width - 0.30
                label_y = y + height / 2
                ax.text(label_x, label_y, label_text, ha='center', va='center', color='white',
                        fontweight='bold', size=10)
            format_spines(ax, right_border=False)

        # Defini��es finais
        axs[0, 0].set_title('Quantity of each Class by Range - Train', size=12, color='dimgrey')
        axs[0, 1].set_title('Quantity of each Class by Range - Test', size=12, color='dimgrey')
        axs[1, 0].set_title('Percentage of each Class by Range - Train', size=12, color='dimgrey')
        axs[1, 1].set_title('Percentage of each Class by Range - Test', size=12, color='dimgrey')
        plt.suptitle(f'Score Distribution by Range - {model_name}\n', size=14, color='black')
        plt.tight_layout()
        plt.show()