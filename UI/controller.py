import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self,e):
        self._view.txt_result.controls.clear()
        anno1 = self._view._ddAnno1.value
        anno2 = self._view._ddAnno2.value

        if anno1 is None or anno2 is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare il range", color="red"))
            self._view.update_page()
            return
        anno1 = int(anno1)
        anno2 = int(anno2)

        self._model.crea_grafo(anno1, anno2)

        n, m = self._model.dim_grafo()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {m}"))
        self._view._btnstampa.disabled = False
        self._view.update_page()

    def handleDettagli(self, e):
        archi, numero, componente = self._model.get_dettagli()

        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore:", color="green"))
        for a in archi:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} -> {a[1]} ({a[2]} piloti condivisi)"))

        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numero} componenti connesse:", color="green"))

        self._view.txt_result.controls.append(ft.Text(f"Componente connessa maggiore:", color="green"))
        for c in componente:
            self._view.txt_result.controls.append(ft.Text(f"{c[0]} (grado {c[1]})"))

        self._view.update_page()



    def handleCerca(self, e):
        num = self._view._txtInK.value
        if num is None or num == "":
            self._view.txt_result.controls.append(ft.Text("Inserire un numero", color="red"))
            self._view.update_page()
            return

        try:
            num = int(num)
        except:
            self._view.txt_result.controls.append(ft.Text("Inserire un numero intero", color="red"))
            self._view.update_page()
            return

        if num < 0:
            self._view.txt_result.controls.append(ft.Text("Inserire un numero positivo", color="red"))
            self._view.update_page()
            return

        lista, valore, minimo, massimo = self._model.cerca_ottimo(num)
        self._model.getListaCostruttoriOttima(num)

        self._view.txt_result.controls.append(ft.Text(f"Trovata lista con valore {valore}", color="green"))
        for l in lista:
            self._view.txt_result.controls.append(ft.Text(f"{l} - {l.oldest_driver_dob}"))

        self._view.txt_result.controls.append(ft.Text(f"Minimo: {minimo}", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Massimo: {massimo}", color="green"))

        self._view.update_page()



    def fill_dd_anni(self):
        for y in self._model.get_years():
            self._view._ddAnno1.options.append(ft.dropdown.Option(y))
            self._view._ddAnno2.options.append(ft.dropdown.Option(y))

        self._view.update_page()


