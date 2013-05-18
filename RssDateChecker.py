#-*-coding: utf-8-*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        RSS date checker
# Purpose:     Check the last update date of a RSS and compare it to a date
#               stored in a text file. If it's newer, then executes another
#               program (typically a parser).
#
# Author:      Guts
#
# Created:     05/07/2012
# Updated:
#-------------------------------------------------------------------------------

###################################
######## Libraries import #########
###################################
# Standard library
import datetime
import pickle
from os import path

# 3rd party libraries
from feedparser import parse

# Custom modules


###################################
############# Classes #############
###################################

class RssDateChecker:
    """  """
    def __init__(self, flux, nom):
        print 'initialized'
        self.last_EC = self.extract_last_date(flux, nom)
        self.rss_EC = self.extract_rss_date(flux)

    def extract_last_date(self, flux, nom):
        fic = "lastupdate_" + nom + ".txt"
        with open(path.join("data", fic), "r") as f:
            last_date = pickle.load(f)
        # End of function
        return last_date

    def extract_rss_date(self, flux):
        rss_date = parse(flux_EC).modified_parsed
        return rss_date



################################################################################
if __name__ == '__main__':
    flux_EC = "http://elcomercio.feedsportal.com/rss/portada.xml"
    nom = "EC"
    app = RssDateChecker(flux_EC, nom)



