# transportschicht.py
# Wird von Stack importiert


import threading

from protokoll_datentypen import *
from basisklassen import Schicht, TimeOut


class Transportschicht(Schicht):
    def __init__(self, kanal):
        Schicht.__init__(self, kanal)

#        # Beispiel fuer Timeout bei Empfangsbestaetigung
#        self.sende_mutex = threading.Lock()
#        self.sende_puffer = None
#        self.sende_timer = None
#        TimeOut(self.sende_timeout, verzoegerung=2)
# interne Methoden ---------------------------------------------------------- #

#    # Beispiel fuer Timeout bei Empfangsbestaetigung
#    # Thread-Methode
#    def sende_timeout(self):
#        self.sende_mutex.acquire()
#        if self.sende_timer is not None:
#            self.sende_timer -= 1
#            if not self.sende_timer:
#                # Timer abgelaufen, Paket senden
#                self.an_n_minus_1(self.sende_puffer)
#                self.sende_puffer = None
#                self.sende_timer = None
#        self.sende_mutex.release()

# --------------------------------------------------------------------------- #

#    # Beispiel fuer Timeout bei Empfangsbestaetigung
#    def schreib_in_sende_puffer(self, data, zeit):
#        self.sende_mutex.acquire()
#        if not zeit > 0: zeit = 1
#        self.sende_timer = zeit
#        self.sende_puffer = data
#        self.sende_mutex.release()

# Objekt Interface ---------------------------------------------------------- #

    def von_n_minus_1(self, v_idu):
        # Daten von Vermittlungsschicht-Schicht (an_n_plus_1)  empfangen
        print "Transport Empfang: ", v_idu
        t_pdu = v_idu.sdu

        # hier Funktionaliaet einfuegen
        # z.B. v_idu.ici und t_pdu.pci auswerten
        

        t_idu = T_IDU()
        t_idu.sdu = t_pdu.sdu
        # Daten an die Anwendung schicken
        self.an_n_plus_1(t_idu)

#        # TEST des Sende Timeouts
#        self.schreib_in_sende_puffer(v_idu, zeit=2)

# --------------------------------------------------------------------------- #

    def von_n_plus_1(self, t_idu):
        # Daten von Anwendung (an_netzwerk) empfangen
        print "Transport Senden:", t_idu
        
        # hier Funktionaliaet einfuegen
        # ...

        # PDU erzeugen
        t_pdu = T_PDU()
        t_pdu.sdu = t_idu.sdu

        # IDU erzeugen
        v_idu = V_IDU()
        v_idu.sdu = t_pdu
        # Paket an die naechste Schicht weiterleiten
        self.an_n_minus_1(v_idu)
