# -*- coding: utf-8 -*-
import nltk

#spanish_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
# Para cortar un texto segun las frases
#spanish_tokenizer.tokenize('Hola amigo. Estoy bien.')
#['Hola amigo.', 'Estoy bien.']

# importo las palabras que no se deberan tomar en cuenta
from nltk.corpus import stopwords

spanish_stops = set(stopwords.words('spanish'))


# Une phrase de test
frase = 'Esta alineación del sol con las calles pares de la Gran Manzana ocurre \
dos veces al año durante dos días en cada ocasión'

lista_palabras = frase.split(' ')

# Une liste pour récupérer les mots ok
lista_palabras_ok = []

for palabra in lista_palabras:
    if palabra.lower() not in spanish_stops :
        lista_palabras_ok.append(palabra.lower())
