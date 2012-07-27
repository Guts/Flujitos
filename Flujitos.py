#-*-coding: utf-8-*-
#-------------------------------------------------------------------------------
# Name:        Flujitos
# Purpose:
#
# Author:      Guts
#
# Created:     05/07/2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python

###################################
##### Import des librairies #######
###################################

from feedparser import parse
##import nltk
import sqlite3
import re
from datetime import datetime

###################################
###### DÃ©finition fonctions #######
###################################



def rss_extract(flux, periodico):
    """remplit le dictionnaire avec les donnÃ©es du flux rss en entrÃ©e"""
    flux = parse(flux)
    if periodico == 1:
        print u'Données el comercio'
        dico_EC['lastupd'] = flux.get('updated_parsed')
        for i in flux.entries:
            dico_EC[re.findall(u'[0-9]{7}', i['id'])[0]] = (i['published_parsed'],
                                                            i['title'],
                                                            i['id']),\
                                                            i['summary']
        return dico_EC, flux
    elif periodico == 2:
        print u'Données La Republica'
        dico_REP['lastupd'] = flux.get('updated_parsed')
        for i in flux.entries:
            dico_REP[flux.entries.index(i)] = (i['published_parsed'],
                                                             i['title'],
                                                             i['id']), \
                                                             i['summary']
        return dico_REP, flux



###################################
####### Variables globales ########
###################################

flux_EC = "http://elcomercio.feedsportal.com/rss/portada.xml"
flux_REP = "http://www.larepublica.pe/rss/rss"

dico_EC = {}
dico_REP = {}

###################################
########### Programme #############
###################################

rss_extract(flux_EC, 1)
##rss_extract(flux_REP, 2)


conn = sqlite3.connect('bd_keywords_prensa.sqlite')          # connexion BD
cur = conn.cursor()                                          # curseur BD



## SQL CREATE  TABLE "main"."flujitos_glob" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE  DEFAULT CURRENT_TIMESTAMP, "mots" VARCHAR NOT NULL  UNIQUE , "occurences" INTEGER, "tipo" BOOL)
## CREATE  INDEX "main"."glob_flujitos" ON "flujitos_glob" ("ID" ASC, "mots" ASC, "occurences" ASC, "tipo" ASC)

noms_coms = {}
nc = [u'futbol', u'estudio', 'economicamente', u'estudio', u'estudio',u'estudio' ]
noms_prop = {}
np = [u'Ollanta', u'Vernier', u'Vernier', u'Moura', u'Vargàs']


for commun in nc:
    if noms_coms.has_key(commun):
        noms_coms[commun] = noms_coms.get(commun) +1
    else:
        noms_coms[commun] = 1

for propre in np:
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
    print mot
    # test s'il est déjà présent dans la BD
    arecup = (mot, )
    cur.execute('SELECT * FROM flujitos_glob WHERE mots=?', arecup)
    row = cur.fetchone()
    if row:
        # S'il est déjà présent on met à jour les occurences
        print u"Déjà présent"
        cur.execute("UPDATE flujitos_glob SET occurences = ? WHERE mots= ?", (row[1] + noms_coms.get(mot), mot))
    else:
        # Sinon, on l'ajoute à la BD
        print u"Pas encore présent"
        timestamp = datetime.now()
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        cur.execute("INSERT INTO flujitos_glob VALUES ( ?, ?, 1)", (mot, noms_coms.get(mot)))


### Enregistrement des changements dans la base et fermeture du curseur
## conn.commit()

##cur.close()
##conn.close()
