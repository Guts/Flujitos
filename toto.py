#-------------------------------------------------------------------------------
# Name:        Parser RSS
# Purpose:
#
# Author:      Julien M.
#
# Created:     05/07/2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python

###################################
##### Import des librairies #######
###################################

from feedparser import parse
import nltk
import sqlite3
import re

###################################
###### Définition fonctions #######
###################################

def conn_BD():
    """paramètres connexion à la BD"""
    conn = sqlite3.connect(r"D:\A_Ordenar\Julien\python\Flujitos\bd_test.sqlite")
    return conn

def rss_extract(flux, periodico):
    """remplit le dictionnaire avec les données du flux rss en entrée"""
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
######### Lecture du RSS ##########
###################################

rss_extract(flux_EC, 1)

rss_extract(flux_REP, 2)


