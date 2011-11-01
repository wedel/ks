# client.py
# Beispiel: Punkt zu Punkt mit einem anderen Rechner verbunden
# Aufruf: python client.py text oder ./client1 text

import sys

from basisklassen import Anwendung, NetzwerkKomponente
import kabel as Kabel
import stack as Stack
from protokoll_datentypen import *
import punkt_zu_punkt_adapter
# import ethernet_adapter, token_ring_adapter

import konfig    # Netzwerkkonfiguration einlesen

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

# Anwendung ################################################################## #

class FClient(Anwendung):
    def __init__(self):
        Anwendung.__init__(self)            

# --------------------------------------------------------------------------- #

    def von_netzwerk(self, t_idu):
        # Daten von Netzwerk empfangen
        print "Client Empfang: "
        a_pdu = t_idu.sdu
        print "Text: ", a_pdu.text

# ---------------------------------------------------------------------------- #
    
    # Start der Anwendung
    def start_anwendung(self):
        a_pdu = A_PDU() # A_PDU erzeugen
        a_pdu.text = sys.argv[1] 
        # a_pdu.kommando wird nicht verwendet 
        t_idu = T_IDU()
        t_idu.sdu = a_pdu
        # idu.ici wird nicht verwendet
        print "Client Senden: "
        # an die Transportschicht uebergeben
        self.an_netzwerk(t_idu)

# Anwendung Ende ######################################################### #

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX #

# Netzwerkkomponente zusammenfuegen und einschalten

# ------------------- #
# die Netzwerkkomponente erzeugen
client = NetzwerkKomponente()
# ------------------- #

# ------------------- #
# einen oder mehrere Netzwerkadapter einbauen
adapter1 = punkt_zu_punkt_adapter.Netzwerkadapter()
client.insertAdapter1(adapter1)

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
# pstack.defaultRouter = konfig.default_router
# pstack.nameServer = konfig.name_server
client.insertProtokollstack(pstack)
# ------------------- #

# ------------------- #
# die Netzwerkanwendung hinzufuegen
anwendung = FClient()
client.insertAnwendung(anwendung)
# ------------------- #

# ------------------- #
# Anschluss an das Netzwerk herstellen   
# fuer p2p:
client.adapter1.verbinde(Kabel.kabel1.anschluss_b()) # server benutzt "anschluss_a"

# fuer hub:
#client.adapter1.verbinde(Kabel.kabel1.anschluss_b()) # hub benutzt "anschluss_a"

#client.adapter2.verbinde(Kabel.kabel2.anschluss_a())

#anschluss1 = Kabel.kabel3.anschluss_a()
#anschluss2 = Kabel.kabel4.anschluss_b()
#adapter3.verbinde(anschluss1, anschluss2)
# ------------------- #

# ------------------- #
# Netzwerkkomponente einschalten
client.start()
# ------------------- #

# Komponente laueft, bei Tastenbetaetigung anhalten
raw_input("Eingabetaste druecken zum Ausschalten")

# ------------------- #
# Netzwerkkomponente ausschalten
client.stop()
# ------------------- #
