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



## Ces 2 listes stockent les noms propres et communs pour tout le dictionnaire
lista_all_NNP = []
lista_all_NN = []

spanish_stops = set(stopwords.words('spanish'))





def scan_palabras(dico):

     # une key est un article   
    for key in dico.keys():

        # Je mets tous mes mots dans une liste
        #lista_palabras = dico[key][1].split(' ')

        # ou autre solution avec nltk
        lista_palabras =  nltk.word_tokenize(dico[key][1].decode('utf8').encode('latin1'))


        # Une liste pour récupérer les mots ok
        lista_palabras_ok = []

        # Dans la boucle si dessous  je peux faire palabra.lower() mais je ne reconnaitrai plus les noms propres
        # A améliorer !

        lista_stop_custom = ['uno', 'dos', 'tres','si']

        for palabra in lista_palabras:
            if palabra not in spanish_stops and palabra not in lista_stop_custom:
                lista_palabras_ok.append(palabra)

        tagged = nltk.pos_tag(lista_palabras_ok)

        # Identify named entities
        #entities = nltk.chunk.ne_chunk(tagged)

        ## Ces 2 listes stockent les noms propres et communs pour chaque news (cle du dico)
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

        for propre in lista_NNP:
            lista_all_NNP.append(propre)

        for commun in lista_NN:
            lista_all_NN.append(commun)


## Debut corps du programme


# Ne pas enlever la 1ere majuscule car peut etre un nom propre -- cas résolu je pense
# Cas inverse où un nom commun est en debut de phrase. Ici il ne faut pas le confondre avec un nom propre

dico_ec = {1: (('23/07/2012', 'Feliz Fiesta', 'http://elcomercio.pe/economia/1447283/noticia-hay6-millones-personas-pobres-invisibles-estado'), 
    'Lima Callao si esta alineacion no del sol de Ollanta Humala con las calles pares de la Gran Manzana ocurre \
    dos veces a la semana durante dos noches en cada ocasion dijo Alan Garcia de la Mancho'), 

    2: (('11/08/2011', 'Asalto', 'http://elcomercio.pe/tag/170883/fiestas-patrias'),
    'La via permanecera cerrada hasta la tarde del domingo, cuando finalice el desfile por Fiestas Patrias, adelanto el coronel PNP \
    Jorge San Martin'),

    3: (('01/01/1991', 'Museos y sitios arqueológicos del país no cobrarán ingreso por Fiestas Patrias', 
        'http://elcomercio.pe/tag/7176/ministerio-de-cultura'),
    'Esta disposición es valida para todos los locales administrados por el Ministerio de Cultura con excepción de los que \
    estan en Cusco')     
    }

scan_palabras(dico_ec)


print lista_all_NNP
print ''
print lista_all_NN
