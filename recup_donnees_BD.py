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

import sqlite3
import simplejson

conn = sqlite3.connect('/home/geotest/code/Flujitos/bd_keywords_prensa.sqlite')          # connexion BD
cur = conn.cursor()                                          # curseur BD

cur.execute('SELECT mots, occurences FROM flujitos_glob ORDER BY occurences desc LIMIT 50;')

mots_exists = cur.fetchall()

test = dict(mots_exists)
#print test

js = simplejson.dumps(test)
print js
