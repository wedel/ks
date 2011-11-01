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

# ---------------------------------------------------------------------------- #
    
    def von_netzwerk(self, t_idu):
        a_pdu = t_idu.sdu
        print "empfangen: ", a_pdu.text

        # hier Funktion des Servers implementieren
        # ...
        
        a_pdu = A_PDU()
        a_pdu.text = "OK"
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
