import networkx as nx
from database.DAO import DAO
from itertools import combinations

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._titoli = {}
    # ==================== PUNTO 1 ====================
    def getAnni(self):
        return DAO.getAllYears()

    def getGeneri(self):
        return DAO.getGeneri()

    def buildGraph(self,anno1,anno2):
        self._grafo.clear()
        self._idMap = {}

        nodi = DAO.getNodi(anno1,anno2)
        self._idMap = {at.id: at for at in nodi}
        self._grafo.add_nodes_from(nodi)
        for c,a in DAO.getCoppia(anno1,anno2):
            if c in self._idMap:
                self._idMap[c].album.add(a)

        for a, b in combinations(nodi, 2):
            comuni = a.album & b.album
            if len(comuni) > 0:
                self._grafo.add_edge(a, b, weight=len(comuni))

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda x: str(x))

    # a) cliente con spesa maggiore
    def getSpesaMaggiore(self):
        best = max(self._grafo.nodes, key=lambda c: c.spesa)
        return best, best.spesa

    # b) clienti con più album diversi (anche a pari merito)
    def getPiuAlbum(self):
        maxAlbum = max(len(c.album) for c in self._grafo.nodes)
        migliori = [c for c in self._grafo.nodes if len(c.album) == maxAlbum]
        migliori.sort(key=lambda c: (c.cognome, c.name))
        return migliori, maxAlbum

    # c) clienti con grado maggiore (anche a pari merito)
    def getGradoMaggiore(self):
        maxGrado = max(self._grafo.degree(c) for c in self._grafo.nodes)
        migliori = [c for c in self._grafo.nodes if self._grafo.degree(c) == maxGrado]
        migliori.sort(key=lambda c: (c.cognome, c.name))
        return migliori, maxGrado

    # d) 5 archi di peso maggiore
    def getTop5Archi(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            nomi = sorted([str(u), str(v)])  # prima il nome minore
            archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0], x[1]))
        return archi[:5]

    # e) componenti connesse
    def getInfoComponenti(self):
        componenti = list(nx.connected_components(self._grafo))
        piuGrande = max(componenti, key=len)
        isolati = 0
        for comp in componenti:
            if len(comp) == 1:
                isolati += 1
        return len(componenti), len(piuGrande), isolati


    # f) numero di paesi diversi e il paese com piu clienti

    def getPaesi(self):
        paesi = {}
        for n in self._grafo.nodes:
            paesi[n.paese] = paesi.get(n.paese, 0) + 1

        maxPaesi = max(paesi.values())
        migliori = sorted([p for p in paesi if paesi[p]== maxPaesi])
        return len(paesi), migliori, maxPaesi

    # g) album acquistato dal maggior numero di clienti
    def getAlbumPiuClienti(self):
        conta = {}  # {AlbumId: numero di clienti}
        for c in self._grafo.nodes:
            for idA in c.album:
                conta[idA] = conta.get(idA, 0) + 1
        maxClienti = max(conta.values())
        if len(self._titoli) == 0:
            self._titoli = DAO.getTitoliAlbum()  # {AlbumId: titolo}
        migliori = sorted([self._titoli[idA] for idA in conta if conta[idA] == maxClienti])
        return migliori, maxClienti

    # h) peso medio degli archi
    def getPesoMedio(self):
        if self._grafo.number_of_edges() == 0:
            return 0
        totale = 0
        for u, v, dati in self._grafo.edges(data=True):
            totale += dati["weight"]
        return totale / self._grafo.number_of_edges()

    def getCammino(self, partenza, L):
        self._L = L
        self._camminoBest = []
        self._pesoBest = -1
        self._ricorsione([partenza], 0)
        return self._camminoBest, self._pesoBest

    def _ricorsione(self, parziale, pesoParziale):
        # caso terminale: ho esattamente L archi
        if len(parziale) - 1 == self._L:
            if pesoParziale > self._pesoBest:
                self._pesoBest = pesoParziale
                self._camminoBest = list(parziale)
            return

        ultimo = parziale[-1]
        for vicino in self._grafo.neighbors(ultimo):
            if vicino in parziale:
                continue
            if vicino.paese == ultimo.paese:  # paese diverso SOLO dall'ultimo
                continue
            peso = self._grafo[ultimo][vicino]["weight"]
            parziale.append(vicino)
            self._ricorsione(parziale, pesoParziale + peso)
            parziale.pop()

    def getCliente(self, idC):
        return self._idMap.get(idC)

    def getPesoArco(self, c1, c2):
        return self._grafo[c1][c2]["weight"]
