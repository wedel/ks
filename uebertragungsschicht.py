# uebertragungsschicht.py
# Wird von Stack importiert

import threading, Queue
from socket import timeout
from basisklassen import Schicht
from protokoll_datentypen import *

class Uebertragungsschicht(Schicht):
    # Wird aufgerufen wenn eine neue Uebertragungsschicht instanziiert wird
    def __init__(self):
        Schicht.__init__(self)
        self._kanal = Queue.Queue()

 # --------------------------------------------------------------------------- #

    def binde(self, adapter):
        # adapter: Hash-Feld mit Netzwerkadaptern
        self._adapter = adapter

        for key in self._adapter.keys():
            # Adapter binden
            self._adapter[key].binde(self._kanal)
        
        # Thread erstellen
        threading.Thread(target=self._von_adaptern, args=(self._kanal,)).start()

# --------------------------------------------------------------------------- #

    def _von_adaptern(self, kanal):
        # Thread liest Daten von Adapter(n)
        while not self.stop_thread: # um Thread sauber beenden zu koennen
            # Daten von Adapter empfangen
            adapter_nr, u_pdu = kanal.get()
            print "Uebertragung Empfang: ", adapter_nr, u_pdu
            
            # hier Funktionaliaet einfuegen
            # z.B. Mac-Adresse auswerten (z.B. u_pdu.pci.mac_dest)
            # ...

            u_idu = U_IDU()
            u_idu.sdu = u_pdu.sdu # == V_PDU
            # Daten an die darueberliegende Schicht hochreichen
            self.an_n_plus_1(u_idu)

# --------------------------------------------------------------------------- #

    def von_n_plus_1(self, u_idu):
        # Daten von der darueberliegenden Schicht verarbeiten
        print "Uebertragung Senden:", u_idu
        
        # hier Funktionaliaet einfuegen
        # z.B. aus u_idu.ici die Netzwerkadapternummer auswerten
        # ...

        # PDU erzeugen
        u_pdu = U_PDU()
        u_pdu.sdu = u_idu.sdu
        
        # Adapter auswaehlen (z.B. aus u_idu.ici.adapter_nr)
        adapter = self._adapter[1]
        # schreiben
        adapter.senden(u_pdu)
