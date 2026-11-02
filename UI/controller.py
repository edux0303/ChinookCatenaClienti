import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def _errore(self, msg):
        self._view._txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDDAnni(self):
        for a in self._model.getAnni():
            self._view._ddAnnoDa.options.append(ft.dropdown.Option(str(a)))
            self._view._ddAnnoA.options.append(ft.dropdown.Option(str(a)))

    def handleCreaGrafo(self, e):
        # 1. pulisco l'output
        self._view._txt_result.controls.clear()

        # 2. leggo i due anni (il dropdown restituisce una stringa, oppure None)
        if self._view._ddAnnoDa.value is None or self._view._ddAnnoA.value is None:
            self._errore("Selezionare entrambi gli anni!")
            return
        anno1 = int(self._view._ddAnnoDa.value)
        anno2 = int(self._view._ddAnnoA.value)

        # 3. controllo l'ordine
        if anno1 > anno2:
            self._errore("L'anno di inizio non può essere successivo all'anno di fine!")
            return

        # 4. creo il grafo
        self._model.buildGraph(anno1, anno2)
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        # riempio il dropdown degli attori (punto 2)
        self._view._ddClienti.options.clear()
        self._view._ddClienti.value = None
        for a in self._model.getNodiOrdinati():
            self._view._ddClienti.options.append(ft.dropdown.Option(key=a.id, text=str(a)))

        self._view.update_page()

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        res = self._view._txt_result.controls

        # a) spesa maggiore
        cliente, spesa = self._model.getSpesaMaggiore()
        res.append(ft.Text(f"a) Cliente con spesa maggiore: {cliente} ({spesa:.2f} $)"))

        # b) più album diversi
        lista, n = self._model.getPiuAlbum()
        res.append(ft.Text(f"b) Cliente con più album diversi ({n}): {', '.join(str(c) for c in lista)}"))

        # c) grado maggiore
        lista, grado = self._model.getGradoMaggiore()
        res.append(ft.Text(f"c) Cliente con grado maggiore ({grado}): {', '.join(str(c) for c in lista)}"))

        # d) top 5 archi
        res.append(ft.Text("d) I 5 archi di peso maggiore:"))
        for n1, n2, peso in self._model.getTop5Archi():
            res.append(ft.Text(f"     {n1} – {n2}: {peso}"))

        # e) componenti
        nComp, dimMax, isolati = self._model.getInfoComponenti()
        res.append(ft.Text(f"e) Componenti connesse: {nComp}"))
        res.append(ft.Text(f"     Dimensione della più grande: {dimMax}"))
        res.append(ft.Text(f"     Clienti isolati: {isolati}"))

        # f) paesi
        nPaesi, paesi, nClienti = self._model.getPaesi()
        res.append(ft.Text(f"f) Paesi diversi: {nPaesi}"))
        res.append(ft.Text(f"     Paese con più clienti ({nClienti}): {', '.join(paesi)}"))

        # g) album acquistato da più clienti
        titoli, nClienti = self._model.getAlbumPiuClienti()
        res.append(ft.Text(f"g) Album acquistato da più clienti ({nClienti}): {', '.join(titoli)}"))

        # h) peso medio
        res.append(ft.Text(f"h) Peso medio degli archi: {self._model.getPesoMedio():.2f}"))

        self._view.update_page()

    def handleCammino(self, e):
        self._view._txt_result.controls.clear()

        # 1. grafo creato?
        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        # 2. cliente di partenza
        if self._view._ddClienti.value is None:
            self._errore("Seleziona un cliente di partenza!")
            return
        partenza = self._model.getCliente(int(self._view._ddClienti.value))
        if partenza is None:
            self._errore("Cliente non presente nel grafo!")
            return

        # 3. L
        try:
            L = int(self._view._txtInL.value)
        except (ValueError, TypeError):
            self._errore("L deve essere un numero intero!")
            return
        if L < 1 or L > 6:
            self._errore("L deve essere compreso tra 1 e 6!")
            return

        # 4. ricorsione
        cammino, peso = self._model.getCammino(partenza, L)

        if len(cammino) == 0:
            self._errore(f"Nessun cammino di {L} archi a partire da {partenza}.")
            return

        # 5. stampo
        res = self._view._txt_result.controls
        res.append(ft.Text(f"Cammino di {L} archi a partire da {partenza}:", color="green"))
        res.append(ft.Text(f"     {cammino[0]} ({cammino[0].paese})"))
        for i in range(1, len(cammino)):
            p = self._model.getPesoArco(cammino[i - 1], cammino[i])
            res.append(ft.Text(f"     → {cammino[i]} ({cammino[i].paese}) [peso {p}]"))
        res.append(ft.Text(f"Peso totale: {peso}"))

        self._view.update_page()