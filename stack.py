# Modul stack.py

import threading, time

from basisklassen import Schicht

# Schichten importieren
from transportschicht import Transportschicht
from vermittlungsschicht import Vermittlungsschicht
from uebertragungsschicht import Uebertragungsschicht

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

# wird spaeter an Anwendung() uebergeben
class Stack:
    def __init__(self):
        self.netzwerkAdresse = None # wird nur in gerouteten Netzen benoetigt
#        self.defaultRouter = None # wird nur in gerouteten Netzen benoetigt
#        self.nameServer = None
        pass # leere Anweisung
    
# Objekt Interface ---------------------------------------------------------- #

    def hole_kanal(self):
        # liefert Kommunikationskanal fuer darueberliegende Schicht (Anwendung)
        return self.kanal
	   
# --------------------------------------------------------------------------- #

    def binde(self, adapter):
        # bindet Protokollstack an Netzwerkadapter
        # adapter: hashfeld mit Netzwerkadaptern
        self._adapter = adapter

# --------------------------------------------------------------------------- #

    def start(self):
        # den Protokollstack zusammensetzen
        # instanziiere Uebertragungsschicht,
        self.uebertragungsschicht = Uebertragungsschicht()
        self.uebertragungsschicht.binde(self._adapter)

        # kanal: kommunikationskanal zwischen zwei angrenzenden Schichten
        kanal = self.uebertragungsschicht.hole_kanal()
        # instanziiere Vermittlungsschicht
        self.vermittlungsschicht = Vermittlungsschicht(kanal, self.netzwerkAdresse)

        kanal = self.vermittlungsschicht.hole_kanal()
        # instanziiere Transportschicht
        # Benoetigt ausser dem Kommunikationskanal keine Daten
        self.transportschicht = Transportschicht(kanal)
        self.kanal = self.transportschicht.hole_kanal()
            
# --------------------------------------------------------------------------- #

    # Threads stoppen
    def stop(self):
        self.transportschicht.stop()
        self.vermittlungsschicht.stop()
        self.uebertragungsschicht.stop()

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #
                
