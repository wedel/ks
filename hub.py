
from time import sleep
from threading import Thread
from Queue import Queue
from socket import timeout

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

class Port:

    def __init__(self, id, inqueue, outqueue):
        self._id = id
        self._kabel = None
        self._inqueue = inqueue
        self._outqueue = outqueue
        
# -------------------------------------------------------------- #
    def __del__(self):
        self.disconnect()
# -------------------------------------------------------------- #

    def _lies_kabel(self):
        while self._run: # um Thread sauber beenden zu koennen
            try:
                # Daten von Kabel empfangen
                frame = self._kabel.lies()
                # Daten verteilen
                if self._inqueue:
                    self._inqueue.put((self._id, frame))
            except timeout:
                pass

# -------------------------------------------------------------- #

    def _schreib_kabel(self):
        while self._run:
            if self._outqueue:
                # frame aus Verteiler lesen
                frame = self._outqueue.get()
                self._kabel.schreib(frame)
                
# -------------------------------------------------------------- #

    def connect(self, kabel):
        self._kabel = kabel
        self._run = True
        Thread(None, self._lies_kabel, '').start()
        Thread(None, self._schreib_kabel, '').start()

# -------------------------------------------------------------- #

    def disconnect(self):
        self._run = False

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

# 8-Port-HUB
class HUB:

    def __init__(self):
        def createPort(self, id, inqueue):
            outq = Queue()
            self._outQueues.append((id, outq))
            port = Port(id, inqueue, outq)
            self._ports.append(port)
            return port
        
        self._run = False
        self._ports = []
        self._inqueue = Queue()
        self._outQueues = []
        self.port1 = createPort(self, 1, self._inqueue)
        self.port2 = createPort(self, 2, self._inqueue)
        self.port3 = createPort(self, 3, self._inqueue)
        self.port4 = createPort(self, 4, self._inqueue)
        self.port5 = createPort(self, 5, self._inqueue)
        self.port6 = createPort(self, 6, self._inqueue)
        self.port7 = createPort(self, 7, self._inqueue)
        self.port8 = createPort(self, 8, self._inqueue)

# -------------------------------------------------------------- #
    def start(self):
        self._run = True
        Thread(None, self._doit, '').start()
# -------------------------------------------------------------- #
    def stop(self):
        self._run = False
        for  p in self._ports:
            p.disconnect()
            
        for  q in self._outQueues:
            oid, outqueue = q
            if id == oid:
                self._outQueues.remove(q)
# -------------------------------------------------------------- #
    def _doit(self):
        while self._run:
            if self._inqueue.empty():
                sleep(0.1)
            else:
                # blocking read
                iid, data = self._inqueue.get()
                for oid, outqueue in self._outQueues:
                    if iid != oid:
                        outqueue.put(data)

# -------------------------------------------------------------- #
