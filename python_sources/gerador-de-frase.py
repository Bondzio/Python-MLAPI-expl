# Gerador de frases
# Linguagens Formais e Aut�matos LAB - 2020
# 160027 - Gabriel Yudi Sanefugi
# 150017 - Lauren Maria Ferreira
# 000000 - Nathalia Louren�o

# As regras do gerador representam uma constru��o simples de uma frase em ingl�s. A frase � composta por:
# <artigo> <substantivo> <verbo conjugado> <adjetivo>
# O algoritmo seleciona um substantivo aleatoriamente, verifica a conjuga��o do verbo (se � plural ou singular, 
# que � um atributo booleano "plural" do objeto substantivo) e seleciona um adjetivo aleat�rio para gerar a senten�a.
# N�o foi feita uma curadoria detalhada das frases geradas, ent�o semanticamente muitas frases podem n�o fazer sentido.
# O projeto ser� evolu�do no decorrer do curso.

import json
from random import randint

# abertura do arquivo JSON, armazenamento em vari�vel e fechamento do arquivo JSON
with open('../input/gerador-de-frases/adjectives.json') as f:
        adjetivos = json.load(f)
with open('../input/gerador-de-frases/noun.json') as f:
        substantivos = json.load(f)

# escolha aleat�ria do substantivo
substantivo = substantivos['nouns'][randint(0,len(substantivos['nouns']))]

# conjuga��o (singular/plural [is/are])
if substantivo['plural']:
    conjugacao = 'are'
else:
    conjugacao = 'is'

#escolha aleat�ria do adjetivo
adjetivo = adjetivos['adjectives'][randint(0,len(adjetivos['adjectives']))]

# forma a frase
print("The "+ substantivo["noun"] + " " + conjugacao + " " + adjetivo)