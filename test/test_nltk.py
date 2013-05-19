#-*-coding: utf-8-*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien
#
# Created:     19/05/2013
# Copyright:   (c) Julien 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import nltk
from urllib import urlopen


url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
raw = urlopen(url).read()

tokens = nltk.word_tokenize(raw)
print tokens[:75]
print '\t\n', len(tokens)

text = nltk.Text(tokens)
print text[:75]

raw2 = nltk.clean_html(raw)
tokens2 = nltk.word_tokenize(raw2)
print tokens2[:75]
print '\t\n', len(tokens2)