# Modul kabel.py
# virtuelle Kabel

import socket, pickle

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

class Kabel:

    class Stecker:
        def __init__(self, ip_selbst, port_selbst, ip_ziel, port_ziel):
            # IPs und Ports speichern
            self.ip_selbst = ip_selbst
            self.port_selbst = port_selbst
            self.ip_ziel = ip_ziel
            self.port_ziel = port_ziel
        
# ---------------------------------------------------------------------------- #            
        
        def verbinde(self):
            # Socket ("Kabel") eroeffnen
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.ip_selbst, self.port_selbst)) # einstellen unserer Schicht-2-Adresse
            self.socket.settimeout(1) # fuer bessere Behandlung

# ---------------------------------------------------------------------------- #            
        
        def schreib(self, daten):
            # Auf Socket ("Kabel") schreiben
            self.socket.sendto(pickle.dumps(daten), 0, (self.ip_ziel, self.port_ziel))

# ---------------------------------------------------------------------------- #            
    
        def lies(self):
            # Von Socket ("Kabel") empfangen
            daten, adresse = self.socket.recvfrom(1024)
            return pickle.loads(daten)
    
# ---------------------------------------------------------------------------- #
            
    def __init__(self, ip_a, port_a, ip_b, port_b):
        # Ruft Stecker fuer hin- und zurueck-Socket auf
        # denn die Kabel sind bidirektional!
        self.stecker_a = self.Stecker(ip_a, port_a, ip_b, port_b)
        self.stecker_b = self.Stecker(ip_b, port_b, ip_a, port_a)
        self.stecker = None
            
# ---------------------------------------------------------------------------- #            
        
    def lies(self):
        daten = self.stecker.lies()
        return daten

# ---------------------------------------------------------------------------- #            
        
    def schreib(self, daten):
        self.stecker.schreib(daten)

# ---------------------------------------------------------------------------- #            
        
    def anschluss_a(self):
        self.stecker_a.verbinde()
        self.stecker = self.stecker_a
        return self

# ---------------------------------------------------------------------------- #            
        
    def anschluss_b(self):
        self.stecker_b.verbinde()
        self.stecker = self.stecker_b
        return self

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

# "Kabel": die Netzwerkanschluesse

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

# ANPASSEN ################################################################### # 

# !!!DIESE EINSTELLUNGEN MUESSEN AUF ALLEN RECHNERN IDENTISCH SEIN!!!

# Netzwerkkabel-Konfiguration
# Alle Kabel sind bidirektional und haben einen Anschluss A und B
# Kabel(Stecker A: IP-Adresse, UDP-Port, Stecker B: IP-Adresse, UDP-Port)
kabel1 = Kabel('127.0.0.1', 3001, '127.0.0.1', 3002)
kabel2 = Kabel('127.0.0.1', 3003, '127.0.0.1', 3004)
kabel3 = Kabel('127.0.0.1', 3005, '127.0.0.1', 3006)
kabel4 = Kabel('127.0.0.1', 3007, '127.0.0.1', 3008)
kabel5 = Kabel('127.0.0.1', 3009, '127.0.0.1', 3010)
kabel6 = Kabel('127.0.0.1', 3011, '127.0.0.1', 3012)
kabel7 = Kabel('127.0.0.1', 3013, '127.0.0.1', 3014)
kabel8 = Kabel('127.0.0.1', 3015, '127.0.0.1', 3016)
kabel9 = Kabel('127.0.0.1', 3017, '127.0.0.1', 3018)
kabel10 = Kabel('127.0.0.1', 3019, '127.0.0.1', 3020)
kabel11 = Kabel('127.0.0.1', 3021, '127.0.0.1', 3022)
kabel12 = Kabel('127.0.0.1', 3023, '127.0.0.1', 3024)
kabel13 = Kabel('127.0.0.1', 3025, '127.0.0.1', 3026)
kabel14 = Kabel('127.0.0.1', 3027, '127.0.0.1', 3028)
kabel15 = Kabel('127.0.0.1', 3029, '127.0.0.1', 3030) 

# Spaetere Interaktionen:
#   anschluss = kabel1.anschluss_a() # oder kabel1.anschluss_b()
#   daten = anschluss.lies()
#   anschluss.schreib(daten)

# ANPASSEN ENDE ############################################################## #

