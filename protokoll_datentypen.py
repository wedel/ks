# Modul protokoll_datentypen.py

# beinhaltet die DU (Data Unit) - Definitionen

# Anwendung
# PDU (Protocol Data Unit)
class A_PDU:
    def __init__(self):
        self.kommando = None # eigentlich: PCI (Protocol Control Information)
        self.text = None # eigentlich: SDU (Service Data Unit)

    # wandelt pdu in einen String und zerteilt ihn in size grosse Teile
    # liefert eine Liste mit den Teilen
    def teile(self, size):
      # anpassen:
      sdata = "%s#%s" % (self.kommando, self.text) # Typ von kommando: string
      # anpassen ende
      adata = []
      i = 0
      l = len(sdata)
      while i < l:
        adata.append(sdata[i:i+size])
        i += size
      return adata

    # fuegt die Listenelemente aus adata zusammen und setzt die Attribute
    def fuege(self, adata):
      sdata = ""
      for teil in adata:
        sdata += teil
      # anpassen:
      self.kommando, self.text = sdata.split('#',1)
      # anpassen ende

# Transportschicht
# IDU (Interface Data Unit)
class T_IDU:
    def __init__(self):
        self.ici = None # z.B. Auftrag an das Netzwerk, Dienstadresse, Status
        self.sdu = None # Inhalt: A_PDU

# PDU
class T_PDU:
    def __init__(self):
        self.pci = None # z.B. Kommando, Status
        self.sdu = None # Inhalt: A_PDU

# Vermittlungsschicht
# IDU
class V_IDU:
    def __init__(self):
        self.ici = None # z.B. Netzwerkadressen
        self.sdu = None # Inhalt: T_PDU

# PDU
class V_PDU:
    def __init__(self):
        self.pci = None # z.B. Netzwerkadressen
        self.sdu = None # Inhalt: T_PDU

# Uebertragungsschicht
# IDU
class U_IDU:
    def __init__(self):
        self.ici = None # z.B. Netzwerkinterface-Nummern
        self.sdu = None # Inhalt: V_PDU

# PDU (im Kern: MAC-Frame)
class U_PDU:
    def __init__(self):
        self.pci = None # z.B. MAC-Adressen 
        self.sdu = None # Inhalt: V_PDU


if __name__ == "__main__":
  pp = A_PDU()
  pp.kommando = "L"
  pp.text = "Hallo Rudi!"

  t = pp.teile(5)
  print t

  xx = A_PDU()
  xx.fuege(t)
  print xx.kommando,',', xx.text

