#-*-coding: utf-8-*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        Flujitos
# Purpose:
#
# Author:      Guts
#
# Created:     05/07/2012
#-------------------------------------------------------------------------------


###################################
##### Import des librairies #######
###################################

from feedparser import parse
import sqlite3
import re
from datetime import datetime
import nltk
from nltk.corpus import stopwords

###################################
###### Fonctions #######
###################################

def rss_extract(flux, periodico):
    u"""remplit le dictionnaire avec les données du flux rss en entrée"""
    flux = parse(flux)
    if periodico == 1:
        print 'Données el comercio'
        # dico_EC['lastupd'] = flux.get('updated_parsed')
        for i in flux.entries:
            dico_EC[re.findall(u'[0-9]{7}', i['id'])[0]] = (i['published_parsed'],
                                                            i['title'],
                                                            i['id']),\
                                                            i['summary']
        return dico_EC, flux

    elif periodico == 2:
        print 'Données La Republica'
        # dico_REP['lastupd'] = flux.get('updated_parsed')
        for i in flux.entries:
            dico_REP[flux.entries.index(i)] = (i['published_parsed'],
                                                             i['title'],
                                                             i['id']), \
                                                             i['summary']
        return dico_REP, flux

    elif periodico == 3:
        print 'Données New-York Times'
        # dico_NYT['lastupd'] = flux.get('updated_parsed')
        for i in flux.entries:
            dico_NYT[flux.entries.index(i)] = (i['published_parsed'],
                                                             i['title'],
                                                             i['id']), \
                                                             i['summary']
        return dico_NYT, flux

def scan_palabras(dico):

     # une key est un article
    for key in sorted(dico.keys()):
        print key

        # Je mets tous mes mots dans une liste
        #lista_palabras = dico[key][1].split(' ')

        # ou autre solution avec nltk
        #lista_palabras =  nltk.word_tokenize(dico[key][1].decode('utf8').encode('latin1'))
        print 'token'
        lista_palabras =  nltk.word_tokenize(dico[key][1])


        # Une liste pour récupérer les mots ok
        lista_palabras_ok = []

        # Dans la boucle si dessous  je peux faire palabra.lower() mais je ne reconnaitrai plus les noms propres
        # A améliorer !

        lista_stop_custom = ['uno', 'dos', 'tres','si', 'http', 'img', 'br', 'amp', '<', '>', '%', 'border', 'border=', ]

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

###################################
####### Variables globales ########
###################################

flux_EC = "http://elcomercio.feedsportal.com/rss/portada.xml"
flux_REP = "http://www.larepublica.pe/rss/rss"
flux_NYT = "http://feeds.nytimes.com/nyt/rss/HomePage"

dico_EC = {}
dico_REP = {}
dico_NYT = {}

## Ces 2 listes stockent les noms propres et communs pour tout le dictionnaire
lista_all_NNP = []
lista_all_NN = []

spanish_stops = set(stopwords.words('spanish'))

###################################
########### Programme #############
###################################

rss_extract(flux_EC, 1) # extrait données du RSS
##rss_extract(flux_REP, 2)
##rss_extract(flux_NYT, 3)

##scan_palabras(dico_NYT)
scan_palabras(dico_EC)  # filtre avec nltk et renvoie 2 listes : noms propres / noms communs



conn = sqlite3.connect('/home/geotest/code/Flujitos/bd_keywords_prensa.sqlite')          # connexion BD
cur = conn.cursor()                                          # curseur BD



## SQL CREATE  TABLE "main"."flujitos_glob" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE  DEFAULT CURRENT_TIMESTAMP, "mots" VARCHAR NOT NULL  UNIQUE , "occurences" INTEGER, "tipo" BOOL)
## CREATE  INDEX "main"."glob_flujitos" ON "flujitos_glob" ("ID" ASC, "mots" ASC, "occurences" ASC, "tipo" ASC)

noms_coms = {}
# nc = [u'futbol', u'estudio', 'economicamente', u'estudio', u'estudio',u'estudio' ]
noms_prop = {}
# np = [u'Ollanta', u'Vernier', u'Vernier', u'Moura', u'Vargàs']

# calcul occurrences des mots de chaque liste
for commun in lista_all_NN:
    if noms_coms.has_key(commun):
        noms_coms[commun] = noms_coms.get(commun) +1
    else:
        noms_coms[commun] = 1

for propre in lista_all_NNP:
    if noms_prop.has_key(propre):
        noms_prop[propre] = noms_prop.get(propre) +1
    else:
        noms_prop[propre] = 1

# Insertion
## Syntaxe SQL d'insertion d'un mot :
## cur.execute("INSERT INTO flujitos_glob VALUES ('date '%Y-%m-%d %H:%M:%S'', 'mot', occurrence, tipo)")
## occurrence est un entier ; tipo un binaire : 1=propre / 0=commun

##cur.execute("INSERT INTO flujitos_glob VALUES ('', 'Ollanta', 2, 1)")

## Récupérer tous les mots déjà inscrits dans la BD
## cur.execute('SELECT * FROM flujitos_glob')
## mots_exists = cur.fetchall()

## Récupérer un mot en particulier
## arecup = (mot, )
## cur.execute('SELECT * FROM flujitos_glob WHERE mots=?', arecup)
## print cur.fetchone()

## Dernier enregistrement
## cur.lastrowid


for mot in sorted(noms_coms.keys()):
    # print mot
    # test s'il est déjà présent dans la BD
    arecup = (mot, )
    cur.execute('SELECT * FROM flujitos_glob WHERE mots=?', arecup)
    row = cur.fetchone()
    if row:
        # S'il est déjà présent on met à jour les occurences
        print "Déjà présent"
        cur.execute("UPDATE flujitos_glob SET occurences = ? WHERE mots= ?", (row[1] + noms_coms.get(mot), mot))
    else:
        # Sinon, on l'ajoute à la BD
        print "Pas encore présent"
        timestamp = datetime.now()
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        cur.execute("INSERT INTO flujitos_glob VALUES ( ?, ?, 1)", (mot, noms_coms.get(mot)))


### Enregistrement des changements dans la base et fermeture du curseur
conn.commit()

##cur.close()
##conn.close()
