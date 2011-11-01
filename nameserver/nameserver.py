# Modul server.py
# Aufruf: python server.py

import sys

from basisklassen import Anwendung, NetzwerkKomponente
import kabel as Kabel
import stack as Stack
from protokoll_datentypen import *
import punkt_zu_punkt_adapter
# import ethernet_adapter, token_ring_adapter

import konfig    # Netzwerkkonfiguration einlesen

# Server ################################################################### #

class FServer(Anwendung):

    def __init__(self):
        Anwendung.__init__(self)
        self.readin()
        
# nameserver methods--(tim 01.11.11)--------------------------------------------#
    database = {}

    #resolve network name and return address
    def resolve(self, name):
        if name in self.database:
            #print database[name]
            address = self.database[name]
        else:
            #print 0
            address = 0
        return address

    # read in nameserver database
    def readin(self):
        file = open('database.txt', "r")
        for line in file:
            line = line.split()
            if len(line) > 1:
                nr = line[0]
                name = line[1]
                self.database[name] = nr
                #print name + ": " + nr

# ---------------------------------------------------------------------------- #
    def von_netzwerk(self, t_idu):
        a_pdu = t_idu.sdu
        print "empfangen: ", a_pdu.text

        # hier Funktion des Servers implementieren
        address = self.resolve(a_pdu.text)
                
        a_pdu = A_PDU()
        #a_pdu.text = "OK"
        a_pdu.text = address
        t_idu = T_IDU()
        t_idu.sdu = a_pdu
        self.an_netzwerk(t_idu)
        
# Server ENDE ########################################################### #

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX #

# Netzwerkkomponente zusammenfuegen und einschalten

# ------------------- #
# die Netzwerkkomponente erzeugen
server = NetzwerkKomponente()
# ------------------- #

# ------------------- #
# einen oder mehrere Netzwerkadapter einbauen
adapter1 = punkt_zu_punkt_adapter.Netzwerkadapter()
server.insertAdapter1(adapter1)

#adapter2 = token_ring_adapter.Netzwerkadapter()
#adapter2.MAC_Adresse = konfig.mac1
#client.insertAdapter2(adapter2)

#adapter3 = ethernet_adapter.Netzwerkadapter()
#adapter3.MAC_Adresse = konfig.mac2
#client.insertAdapter3(adapter3)
# ------------------- #

# ------------------- #
# den Protokollstack hinzufuegen
pstack = Stack.Stack()
# pstack.netzwerkAdresse = konfig.netzwerk_adresse
server.insertProtokollstack(pstack)
# ------------------- #

# ------------------- #
# die Netzwerkanwendung hinzufuegen
anwendung = FServer()
server.insertAnwendung(anwendung)
# ------------------- #

# ------------------- #
# Anschluss an das Netzwerk herstellen
# fuer p2p:
server.adapter1.verbinde(Kabel.kabel1.anschluss_a()) # client benutzt "anschluss_b"

# fuer HUB:
#server.adapter1.verbinde(Kabel.kabel2.anschluss_b()) # hub benutzt "anschluss_a"

#anschluss = Kabel.kabel2.anschluss_b()
#client.adapter2.verbinde(anschluss)

#anschluss1 = Kabel.kabel3.anschluss_b()
#anschluss2 = Kabel.kabel4.anschluss_a()
#adapter3.verbinde(anschluss1, anschluss2)
# ------------------- #

# ------------------- #
# Netzwerkkomponente einschalten
server.start()
# ------------------- #

# Komponente laueft, bei Tastenbetaetigung anhalten
raw_input("Eingabetaste druecken zum Ausschalten")

# ------------------- #
# Netzwerkkomponente ausschalten
server.stop()
# ------------------- #
