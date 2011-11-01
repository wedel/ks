# Modul basisklassen.py

import threading, time
from Queue import Queue, Empty, Full

# ########################################################################### #

# Kommunikationskanal zwischen angrenzenden Schichten
class Kanal:
    def __init__(self, q1=None, q2=None):
        # Das sind die Queue Elemente
        self.q1 = q1
        self.q2 = q2
        if not q1: self.q1 = Queue()
        if not q2: self.q2 = Queue()

        self.to = 1 # queue-timeout

# --------------------------------------------------------------------------- #

    def lies_von_n_plus_1(self):
        idu = ()
        if self.q1: idu = self.q1.get(timeout=self.to)
        return idu
        
# --------------------------------------------------------------------------- #

    def lies_von_n_minus_1(self):
        idu = ()
        if self.q2: idu = self.q2.get(timeout=self.to)
        return idu
        
# --------------------------------------------------------------------------- #

    def schreib_an_n_plus_1(self, idu):
        if self.q2: self.q2.put(idu, timeout=self.to)
        
# --------------------------------------------------------------------------- #

    def schreib_an_n_minus_1(self, idu):
        if self.q1: self.q1.put(idu, timeout=self.to)
        
# --------------------------------------------------------------------------- #

    # von Schicht n-1 lesen
    def lies(self):
        return self.lies_von_n_minus_1()

# --------------------------------------------------------------------------- #

    # an Schicht n-1 schreiben
    def schreib(self, idu):
        self.schreib_an_n_minus_1(idu)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

# ruft zyklisch mit Periode "verzoegerung" die "methode"
class TimeOut:
    stop = False
    def __init__(self, methode, verzoegerung=1):
        self.methode = methode
        self.verzoegerung = verzoegerung
        threading.Thread(target=self.lauf).start()
        
# --------------------------------------------------------------------------- #

    def lauf(self):
        while not TimeOut.stop:
            time.sleep(self.verzoegerung)
            self.methode()

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

class Schicht:
    '''Basisklasse fuer Schichten'''
    def __init__(self, n_minus_1=None):
        self.n_minus_1 = n_minus_1
        self.n_plus_1 = Kanal()

        self.stop_thread = False # um Thread sauber beenden zu koennen
        
        # auf von oben und unten kommende Daten warten
        if n_minus_1: threading.Thread(target=self._von_n_minus_1).start()
        threading.Thread(target=self._von_n_plus_1).start()
        
# --------------------------------------------------------------------------- #

    def _von_n_minus_1(self):
        while not self.stop_thread: # um Thread sauber beenden zu koennen
            try:        # um Thread sauber beenden zu koennen
                # Daten von n-1 empfangen
                idu = self.n_minus_1.lies_von_n_minus_1()
                self.von_n_minus_1(idu)
            # um Thread sauber beenden zu koennen:
            except Empty:
                pass
    
# --------------------------------------------------------------------------- #

    def _von_n_plus_1(self):
        while not self.stop_thread: # um Thread sauber beenden zu koennen
            try:        # um Thread sauber beenden zu koennen
                # Daten von n+1 empfangen
                idu = self.n_plus_1.lies_von_n_plus_1()
                self.von_n_plus_1(idu)
            # um Thread sauber beenden zu koennen:
            except Empty:
                pass
        
# diese Methoden werden verwendet bzw. implementiert --------------------- #
    
    def an_n_plus_1(self, idu):
        # schreibt in die Queue um von der darueberliegenden
        # Schicht ausgelesen zu werden
        self.n_plus_1.schreib_an_n_plus_1(idu)
        
# --------------------------------------------------------------------------- #

    def an_n_minus_1(self, idu):
        # schreibt in die Queue um von der darunterliegenden
        # Schicht ausgelesen zu werden
        self.n_minus_1.schreib_an_n_minus_1(idu)
        
# --------------------------------------------------------------------------- #

    # diese Methode muss von Kindklasse implementiert werden
    def von_n_minus_1(self, idu):
        raise NotImplementedError("Noch nicht implementiert!")

# --------------------------------------------------------------------------- #
    
    # diese Methode muss von Kindklasse implementiert werden
    def von_n_plus_1(self, idu):
        raise NotImplementedError("Noch nicht implementiert!")

# Objekt Interface ---------------------------------------------------------- #

    def hole_kanal(self):
        # liefert Kommunikationskanal fuer darueberliegende Schicht
        return self.n_plus_1
    
# --------------------------------------------------------------------------- #
    
    def stop(self):
        TimeOut.stop = True
        self.stop_thread = True
        
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

class Anwendung:
    '''Basisklasse fuer Anwendungen'''
    # Vererbt an alle Anwendungen
    def __init__(self):
        pass

# threads -------------------------------------------------------------------- #

    def _von_netzwerk(self):
        # Daten erwarten
        while not self.stop_thread: # um Thread sauber beenden zu koennen
            try:        # um Thread sauber beenden zu koennen
                # Daten vom Netzwerk empfangen
                idu = self.netzwerk.lies()
                self.von_netzwerk(idu)
            # um Thread sauber beenden zu koennen:
            except Empty:
                pass

# abstrakte Methoden -------------------------------------------------------- #

    # Methode muss implementiert werden
    # erhaelt Daten vom Netzwerk (idu)
    def von_netzwerk(self, idu):
        raise NotImplementedError("von_netzwerk: Noch nicht implementiert!")

# --------------------------------------------------------------------------- #

    # diese Methode kann von Kindklasse implementiert werden
    def start_anwendung(self):
        pass

# Methoden ------------------------------------------------------------------ #

    # uebergibt Daten an das Netzwerk
    def an_netzwerk(self, idu):
        self.netzwerk.schreib(idu)
        
# Objekt Interface ---------------------------------------------------------- #
    
    def start(self, *a, **kwa):
        # starten
        # wird von jeder Anwendung aufgerufen
        self.netzwerk = self.stack.hole_kanal() # Kommunikationskanal Netzwerk - Anwendung
        self.stop_thread = False # um Thread sauber beenden zu koennen
        threading.Thread(target=self._von_netzwerk).start()

        self.start_anwendung(*a, **kwa)
        
# --------------------------------------------------------------------------- #
    
    def stop(self):
        # stoppen
        self.stop_thread = True

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

class Netzwerkadapter:
    def __init__(self):
        self._run = True
        self._verbunden = False
        self.MAC_Adresse = None
        self._puffer = Queue() # Sendepuffer
        self._kanal = None

# --------------------------------------------------------------------------- #
    
    def _empfang(self, idu):
        # Daten hochreichen
        self._kanal.put(idu)
        
# kann von Kindklasse ueberschrieben werden --------------------------------- #

    def _verbinde(self):
        pass

# ende ueberschreiben -------------------------------------------------------- #

# muessen von Kindklasse implementiert werden ------------------------------- #

    def _von_kabel(self, nr, kabel):
        # Thread versucht Daten vom Kabel zu lesen
        raise NotImplementedError()
        
# --------------------------------------------------------------------------- #

    def _an_kabel(self, kabel):
        # Thread versucht Daten an Kabel zu schreiben
        raise NotImplementedError()            

# oeffentliche Methoden ----------------------------------------------------- #

    # bindet Adapter an Protokollschicht (Rueckkanal)
    def binde(self, kanal):
        # kanal: typ: Queue.Queue
        self._kanal = kanal

# --------------------------------------------------------------------------- #

    def stop(self):
        self._run = False

# --------------------------------------------------------------------------- #
    
    # Verbindet ueber Netzwerkkabel mit anderen Netzwerkkomponenten 
    # bzw. deren Netzwerkadaptern
    def verbinde(self, kabel1, kabel2=None):
        # kabel1, kabel2: ein oder zwei Kabel
        # kabel1: Empfang/Senden oder Empfang, kabel2: Senden
        self._kabel1 = kabel1
        if not kabel2: kabel2 = kabel1
        self._kabel2 = kabel2
        self._verbinde()    # Ergaenzungen
        self._verbunden = True
        
# --------------------------------------------------------------------------- #

    def start(self):
        if self._verbunden:
            # Thread erstellen und
            # Interface Nummer uebergeben
            threading.Thread(target=self._von_kabel, args=(self._interfaceNr,
                                               self._kabel1)).start()
            threading.Thread(target=self._an_kabel, args=(self._kabel2,)).start()

# --------------------------------------------------------------------------- #

    # Daten zum Senden uebergeben
    def senden(self, daten):
        # Daten zwischenspeichern
        self._puffer.put(daten)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

class NetzwerkKomponente:
    def __init__(self):
        # vier Netzwerkadapter moeglich
        self.adapter1 = None
        self.adapter2 = None
        self.adapter3 = None
        self.adapter4 = None
        self._adapter = {}
        self._netzwerk_protokollstack = None
        self._netzwerk_anwendung = None   

# --------------------------------------------------------------------------- #

    def insertAdapter1(self, adapter):
        self._adapter[1] = adapter
        self.adapter1 = self._adapter[1]
        self.adapter1._interfaceNr = 1
        
# --------------------------------------------------------------------------- #

    def insertAdapter2(self, adapter):
        self._adapter[2] = adapter
        self.adapter2 = self._adapter[2]
        self.adapter2._interfaceNr = 2
        
# --------------------------------------------------------------------------- #

    def insertAdapter3(self, adapter):
        self._adapter[3] = adapter
        self.adapter3 = self._adapter[3]
        self.adapter3._interfaceNr = 3
        
# --------------------------------------------------------------------------- #

    def insertAdapter4(self, adapter):
        self._adapter[4] = adapter
        self.adapter4 = self._adapter[4]
        self.adapter4._interfaceNr = 4
        
# --------------------------------------------------------------------------- #

    def insertProtokollstack(self, pstack):
        # binden der Netzwerkadapter
        pstack.binde(self._adapter)
        self._netzwerk_protokollstack = pstack

# --------------------------------------------------------------------------- #

    def insertAnwendung(self, anwendung):
        self._netzwerk_anwendung = anwendung
        self._netzwerk_anwendung.stack = self._netzwerk_protokollstack

# --------------------------------------------------------------------------- #

    def start(self):
        for key in self._adapter.keys():
            self._adapter[key].start()
        self._netzwerk_protokollstack.start()
        self._netzwerk_anwendung.start()

        print "Netzwerkkomponente ist eingeschaltet"
 
# --------------------------------------------------------------------------- #

    def stop(self):
        self._netzwerk_anwendung.stop()
        time.sleep(1.5)
        self._netzwerk_protokollstack.stop()
        time.sleep(1.5)
        for key in self._adapter.keys():
            self._adapter[key].stop()
        time.sleep(1.5)

        print "Netzwerkkomponente ist ausgeschaltet"
        
