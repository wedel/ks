#! /usr/bin/env python

from time import sleep
from threading import Thread
from Queue import Queue
from socket import timeout

from hub import HUB

import kabel as Kabel

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

hub = HUB()

########################
# hier Verkabelung konfigurieren:
hub.port1.connect(Kabel.kabel1.anschluss_a())
hub.port2.connect(Kabel.kabel2.anschluss_a())
hub.port3.connect(Kabel.kabel3.anschluss_a())
#hub.port4.connect(Kabel.kabel4.anschluss_a())
########################

# HUB einschalten
hub.start()

# auf Beendigung warten
raw_input("Ende mit beliebiger Taste:\n")
# HUB stoppen
hub.stop()
