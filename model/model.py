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

        self._ricorsione1([], num, list(nx.connected_components(self._grafo)))


        ord = sorted(self.lista, key=lambda x:x.oldest_driver_dob)

        if len(ord) > 1:
            return self.lista, self.valore, ord[0], ord[-1]
        else:
            return self.lista, self.valore, ord, ord


    def _ricorsione1(self, parziale, num, componenti):
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
                        self._ricorsione1(parziale, num, componenti)
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

    def getListaCostruttoriOttima(self, k):
        self._optListaCostruttori = []
        self._optScore = 365 * 100  # 100 years in days


        components = list(nx.connected_components(self._grafo))



        parziale = []
        self._ricorsione(components, k, parziale, 0)
        print(self._optListaCostruttori, self._optScore)

    def _ricorsione(self, componenti, k, parziale, index_componente):
        # Base case: found k constructors
        if len(parziale) == k:
            # Check if all constructors have oldest_driver_dob
            dobs = [c.oldest_driver_dob for c in parziale if c.oldest_driver_dob is not None]
            if len(dobs) != k:
                return  # Skip if some constructors don't have data

            diff_attuale = (max(dobs) - min(dobs)).days

            if diff_attuale < self._optScore:
                self._optScore = diff_attuale
                self._optListaCostruttori = copy.deepcopy(parziale)
            return

        # Termination conditions
        if index_componente >= len(componenti):
            return
        if (len(componenti) - index_componente) < (k - len(parziale)):
            return

        # Option 1: Skip this component
        self._ricorsione(componenti, k, parziale, index_componente + 1)

        # Option 2: Choose one constructor from this component
        componente_corrente = componenti[index_componente]
        for costruttore in componente_corrente:
            if costruttore.oldest_driver_dob is not None:
                parziale.append(costruttore)
                self._ricorsione(componenti, k, parziale, index_componente + 1)
                parziale.pop()


