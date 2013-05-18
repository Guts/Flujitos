#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien
#
# Created:     18/05/2013
# Copyright:   (c) Julien 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from RssDateChecker import *

flux_EC = "http://elcomercio.feedsportal.com/rss/portada.xml"
nom = "EC"
app = RssDateChecker(flux_EC, nom)


if app.status == 1:
    import Flujitos
