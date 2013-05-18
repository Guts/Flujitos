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
######## Libraries import #########
###################################
# Standard library
from os import getcwd, path, getcwd, chdir
import re
from datetime import datetime
import pickle

# Python 3 backported
from collections import OrderedDict as OD

# 3rd party libraries
from feedparser import parse
import nltk
from nltk.corpus import stopwords
import sqlite3

# Custom modules


###################################
############ Classes ##############
###################################

class Flujitos:
    """ Main class of Flujitos program """
    def __init__(self, feed, periodico):
        """ feed = a RSS feed
            periodico = integer code corresponding to the newspaper website:
                1: El Comercio (Peru)
                2: La Republica (Peru)
                3: New York Times (US) """
        # object variables
        self.dico_flux = OD()       # feed entries dictionary (ordered)
        self.dico_hist = OD()       # feed entries history (dates and url)
        self.li_all_propre = []     # list of proper nouns
        self.dico_propre = OD()     # proper nouns and number of occurrences
        self.li_all_common = []     # list of common nouns
        self.dico_common = OD()     # common nouns and number of occurrences


        # extracting and filtering feed entries
        rss_extract(feed)

        # tokenizing and filtering words
        scan_words(self.dico_flux)

        # calculating occurrences


        # writing into the database


        # noting the last update date
        lastup_EC = parse(feed).modified_parsed
        note_last_date(lastup_EC, periodico)



    def rss_extract(self, feed):
        """ parse and extract feed entries needed """
        flux = parse(feed)
        self.dico_flux['lastupd'] = flux.get('updated_parsed')
        for i in flux.entries:
            self.dico_flux[flux.entries.index(i)] = (i['published_parsed'],
                                                     i['title'],
                                                     i['id']),\
                                                     i['summary']
            self.dico_hist[i['id']] = (i['published_parsed'], i['published'])
            # Exit function
            return self.dico_flux, self.dico_hist


    def scan_words(self, dico_feed):
        """ uses nltk tools to tokenize and filter the feed """
        stop_es = set(stopwords.words('spanish'))   # add specific spanish words
        for feed_item in sorted(dico_feed.keys()):
            """ each dictionary key is a feed item """
            # local variables
            li_words_ok = []    # list to store words OK
            li_propre  = []     # list to store proper nouns
            li_common = []      # list to store common nouns
            tup_stop_custom = ('uno', 'dos', 'tres','si', 'asi', 'el', 'img',
                              'http', 'br', 'amp', '<', '>', '%', 'border',
                              'border=')   # tuple of custom stop words


            # tokenizing
            li_words_all =  nltk.word_tokenize(dico_feed[feed_item][1])

            # filtering
            for word in li_words_all:
                if word not in stop_es and word not in tup_stop_custom:
                    li_words_ok.append(word)

            # tagging: identifiy words with their type (verb, noun, etc.)
                # see: http://nltk.googlecode.com/svn/trunk/doc/book/ch05.html
                # also see: http://nltk.org/api/nltk.tag.html
            tagged = nltk.pos_tag(li_words_ok)

            # filtering by type
            for tag in tagged:
                if (tag[1] == 'NNP' or tag[1] =='NNPS') and tagged.index(tag) == 0:
                    li_propre.append(tag[0])
                if (tag[1] == 'NNP' or tag[1] =='NNPS') and (tagged[tagged.index(tag)-1][1] <> 'NNP' and tagged[tagged.index(tag)-1][1] <> 'NNPS') \
                   and tagged.index(tag) > 0:
                    li_propre.append(tag[0])
                elif (tag[1] == 'NNP' or tag[1] =='NNPS') and (tagged[tagged.index(tag)-1][1] == 'NNP' or tagged[tagged.index(tag)-1][1] == 'NNPS') \
                     and tagged.index(tag) > 0:
                    li_propre[len(li_propre)-1] = li_propre[len(li_propre)-1] + ' ' + tag[0]
                elif (tag[1] == 'NN' or tag[1] == 'NNS'):
                    li_common.append(tag[0])
                else:
                    pass

            # adding to global lists
                ## use expand method maybe?
            for propre in li_propre:
                self.li_all_propre.append(propre)

            for commun in li_common:
                self.li_all_common.append(commun)

            # End of function
            return self.li_all_common, self.li_all_propre

    def occurences(self, list_words, dico_dest):
        """ returns an ordered dictionary of words and number of occurrences
        from an iterable """
        for word in list_words:
            if dico_dest.has_key(word):
                dico_dest[word] = dico_dest.get(word) +1
            else:
                dico_dest[word] = 1
        # End of function
        return dico_dest


    def db_insertion(self, database, values):
        """  """






    def note_last_date(self, date, nom):
        """ dumps the last update of a feed into a file """
        fic = "lastupdate_" + nom + ".txt"
        with open(path.join("data", fic), "wb") as f:
            pickle.dump(date, f)
        # End fo function
        return f, fic



###################################
########### Programme #############
###################################


db =  path.join(getcwd(), 'data/bd_keywords_prensa.sqlite')

conn = sqlite3.connect(db)          # connexion BD
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








################################################################################
###### Stand alone program ########
###################################
if __name__ == '__main__':
    flux_EC = "http://elcomercio.feedsportal.com/rss/portada.xml"
    flux_REP = "http://www.larepublica.pe/rss/rss"
    flux_NYT = "http://feeds.nytimes.com/nyt/rss/HomePage"
    Flujitos(flux_EC, 1)



################################################################################
######## Former codelines #########
###################################


##def rss_extract(self, feed, periodico):
##    """ parse and extract feed entries needed """
##    flux = parse(feed)
##    if periodico == 1:
##        """ data from El Comercio.pe """
##        self.dico_flux['lastupd'] = flux.get('updated_parsed')
##        for i in flux.entries:
##            self.dico_flux[re.findall(u'[0-9]{7}', i['id'])[0]] = (i['published_parsed'],
##                                                            i['title'],
##                                                            i['id']),\
##                                                            i['summary']
##        # Exit function
##        return self.dico_flux, flux
##
##    elif periodico == 2:
##        """ data from LaRepublica.pe """
##        self.dico_flux['lastupd'] = flux.get('updated_parsed')
##        for i in flux.entries:
##            self.dico_flux[flux.entries.index(i)] = (i['published_parsed'],
##                                                             i['title'],
##                                                             i['id']), \
##                                                             i['summary']
##        # Exit function
##        return dico_REP, flux
##
##    elif periodico == 3:
##        """ data from New York Times """
##        self.dico_flux['lastupd'] = flux.get('updated_parsed')
##        for i in flux.entries:
##            self.dico_flux[flux.entries.index(i)] = (i['published_parsed'],
##                                                             i['title'],
##                                                             i['id']), \
##                                                             i['summary']
##        # Exit function
##        return dico_NYT, flux



#### Note the last update of RSS
##lastup_EC = parse(flux_EC).modified_parsed
##note_last_date(lastup_EC, "EC")
##lastup_REP = parse(flux_REP).modified_parsed
##note_last_date(lastup_EC, "REP")
