# vermittlungsschicht.py
# Wird von stack importiert


from basisklassen import Schicht
from protokoll_datentypen import *


class Vermittlungsschicht(Schicht):
    # wird aufgerufen wenn eine neue Vermittlungsschicht instanziiert wird
    def __init__(self, kanal, nw_adresse=None):
        Schicht.__init__(self, kanal)
        self.netzwerkAdresse = nw_adresse # verwendet?
        # Hier muesste eine Routing-Tabelle geladen werden

# --------------------------------------------------------------------------- #

    def von_n_minus_1(self, u_idu):
        # Daten von Uebertragungs-Schicht (an_n_plus_1) empfangen
        print "Vermittlung Empfang:", u_idu
        
        # hier Funktionaliaet einfuegen
        # ...
        
        v_pdu = u_idu.sdu
        t_pdu = v_pdu.sdu
        v_idu = V_IDU()
        v_idu.sdu = t_pdu
         
        # Daten an Transportschicht hochreichen
        self.an_n_plus_1(v_idu)

# --------------------------------------------------------------------------- #

    def von_n_plus_1(self, v_idu):
        # Daten von Transport-Schicht (an_n_minus_1) empfangen
        print "Vermittlung Senden:", v_idu
        
        # hier Funktionaliaet einfuegen
        # ...

        # PDU erzeugen
        v_pdu = V_PDU()
        v_pdu.sdu = v_idu.sdu

        # IDU erzeugen
        u_idu = U_IDU()
        u_idu.sdu = v_pdu
        
        # Daten an Uebertragungsschicht runterreichen
        self.an_n_minus_1(u_idu)
