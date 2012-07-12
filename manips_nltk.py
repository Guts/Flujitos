# -*- coding: utf-8 -*-
import nltk

## Pour le moment prend une string en entrée.
## A changer pour un dico

#spanish_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
# Para cortar un texto segun las frases
#spanish_tokenizer.tokenize('Hola amigo. Estoy bien.')
#['Hola amigo.', 'Estoy bien.']

# importo las palabras que no se deberan tomar en cuenta
from nltk.corpus import stopwords

spanish_stops = set(stopwords.words('spanish'))

# liste a completer
lista_stop_custom = ['uno', 'dos', 'tres','si']

# Une phrase de test
# Ne pas enlever la 1ere majuscule car peut etre un nom propre -- cas résolu je pense
# Cas inverse où un nom commun est en debut de phrase. Ici il ne faut pas le confondre avec un nom propre
frase = 'Lima Callao si esta alineacion no del sol de Ollanta Humala con las calles pares de la Gran Manzana ocurre \
dos veces a la semana durante dos noches en cada ocasion dijo Alan Garcia de la Mancha'

lista_palabras = frase.split(' ')

# autre possibilité avec nltk, si plus de probleme d'encodage avant
from nltk.tokenize import word_tokenize
lista_palabras_2 = word_tokenize(frase)


# Une liste pour récupérer les mots ok
lista_palabras_ok = []

# Dans la boucle si dessous  je peux faire palabra.lower() mais je ne reconnaitrai plus les noms propres
# A améliorer !

for palabra in lista_palabras:
    if palabra not in spanish_stops :
        lista_palabras_ok.append(palabra)



tagged = nltk.pos_tag(lista_palabras_ok)

# Identify named entities
#entities = nltk.chunk.ne_chunk(tagged)

# 1 liste pour les noms propres, 1 pour les noms communs. Rajouter une liste pour les lieux
lista_NNP  = []
lista_NN = []


for tag in tagged:
    if (tag[1] == 'NNP' or tag[1] =='NNPS') and tagged.index(tag) == 0:
        lista_NNP.append(tag[0])
    if (tag[1] == 'NNP' or tag[1] =='NNPS') and (tagged[tagged.index(tag)-1][1] <> 'NNP' and tagged[tagged.index(tag)-1][1] <> 'NNPS') \
       and tagged.index(tag) > 0:
        lista_NNP.append(tag[0])
    elif (tag[1] == 'NNP' or tag[1] =='NNPS') and (tagged[tagged.index(tag)-1][1] == 'NNP' or tagged[tagged.index(tag)-1][1] == 'NNPS') \
         and tagged.index(tag) > 0:
        lista_NNP[len(lista_NNP)-1] = lista_NNP[len(lista_NNP)-1] + ' ' + tag[0]
    elif (tag[1] == 'NN' or tag[1] == 'NNS'):
        lista_NN.append(tag[0])
    else:
        pass
