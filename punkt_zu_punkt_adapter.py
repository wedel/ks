# Punkt zu Punkt Netzwerkadapter

import basisklassen

class Netzwerkadapter(basisklassen.Netzwerkadapter):
    def __init__(self):
        basisklassen.Netzwerkadapter.__init__(self)

# --------------------------------------------------------------------------- #

    def _verbinde(self):
        pass

# --------------------------------------------------------------------------- #

    def _von_kabel(self, nr, kabel):
        # Thread versucht Daten vom Kabel zu lesen
        interface_nr = nr
        while self._run: # um Thread sauber beenden zu koennen
            try:        # um Thread sauber beenden zu koennen
                # Daten von Kabel empfangen
                daten = kabel.lies()
                
                # Daten weitergeben
                self._empfang((interface_nr, daten))
            # um Thread sauber beenden zu koennen:
            except:
                pass

# --------------------------------------------------------------------------- #

    def _an_kabel(self, kabel):
        # Thread versucht Daten an Kabel zu schreiben
        while self._run: # um Thread sauber beenden zu koennen
            try:        # um Thread sauber beenden zu koennen
                # Daten von Puffer lesen
                daten = self._puffer.get(timeout=1)
                # Daten senden
                kabel.schreib(daten)
            except:
                pass
            
