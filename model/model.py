import copy
import networkx as nx
from networkx.classes import nodes
from networkx.generators.classic import null_graph

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.id_costruttori = {}
        self.lista = []
        self.valore = 10000000000

    def get_years(self):
        return DAO.getAllYears()

    def crea_grafo(self, anno1, anno2):
        self._grafo.clear()
        self.id_costruttori = {}

        nodi = DAO.get_nodi(anno1, anno2)
        for n in nodi:
            self.id_costruttori[n.constructorId] = n

        archi = DAO.get_archi(self.id_costruttori, anno1, anno2)

        self._grafo.add_nodes_from(nodi)
        for a in archi:
            self._grafo.add_edge(a[0], a[1], weight=a[2])


    def dim_grafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_dettagli(self):
        archi = [(a, b, self._grafo[a][b]["weight"]) for a, b in self._grafo.edges]
        archi.sort(key=lambda x: x[2], reverse=True)
        componenti = list(nx.connected_components(self._grafo))
        componenti.sort(key=lambda x:len(x), reverse=True)
        maggiore = componenti[0]
        res = []
        for n in maggiore:
            res.append((n, self._grafo.degree(n)))
        res.sort(key=lambda x:x[1], reverse=True)

        if len(archi) > 3:
            return archi[0:3], len(componenti), res
        else:
            return archi, len(componenti), res

    def cerca_ottimo(self, num):
        self.lista = []
        self.valore = 10000000000

        self._ricorsione([], num, list(nx.connected_components(self._grafo)))


        ord = sorted(self.lista, key=lambda x:x.oldest_driver_dob)

        if len(ord) > 1:
            return self.lista, self.valore, ord[0], ord[-1]
        else:
            return self.lista, self.valore, ord, ord


    def _ricorsione(self, parziale, num, componenti):
        # caso terminale
        if len(parziale) == num:
            i = self.calcola(parziale)
            if i < self.valore:
                self.lista = copy.deepcopy(parziale)
                self.valore = i
        # caso ricorsivo
        else:
            for c in componenti:
                for n in c:
                    parziale.append(n)
                    if self.controlla_data(parziale):
                        componenti.remove(c)
                        self._ricorsione(parziale, num, componenti)
                        componenti.append(c)
                    parziale.pop()



    def controlla_data(self, parziale):
        if self.calcola(parziale) < self.valore:
            return True

        return False

    def calcola(self, parziale):
        minimo = min([c.oldest_driver_dob for c in parziale])
        massimo = max([c.oldest_driver_dob for c in parziale])
        return (massimo - minimo).total_seconds() / 86400


