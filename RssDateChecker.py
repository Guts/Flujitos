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
import time
import pickle
from os import path

# 3rd party libraries
from feedparser import parse

# Custom modules


###################################
############# Classes #############
###################################

class RssDateChecker:
    """ Extracts and then compares date of the last item modified in a rss feed
    with the date of the last execution of Flujitos """
    def __init__(self, flux, nom):
        """ initialization function """
        # extracting dates
        self.last_EC = self.extract_last_date(flux, nom)
        self.rss_EC = self.extract_rss_date(flux)
        # comparing dates
        self.compare_dates(self.last_EC, self.rss_EC)

    def extract_last_date(self, flux, nom):
        """ Pick up the date of Flujitos last execution """
        fic = "lastupdate_" + nom + ".txt"
        with open(path.join("data", fic), "r") as f:
            last_date = pickle.load(f)
        # End of function
        return last_date

    def extract_rss_date(self, flux):
        """ Pick up the date of the date of last modified item of the RSS feed """
        rss_date = parse(flux_EC).modified_parsed
        # End of function
        return rss_date

    def compare_dates(self, date_rss, date_lastupdate):
        """ compare the two dates """
        print date_lastupdate
        print '/t', date_rss
        if date_rss < date_lastupdate:
            print "Flujitos needs to be executed"
            return 1
        else:
            print "No new execution needed"
            return 0




################################################################################
if __name__ == '__main__':
    flux_EC = "http://elcomercio.feedsportal.com/rss/portada.xml"
    nom = "EC"
    app = RssDateChecker(flux_EC, nom)



