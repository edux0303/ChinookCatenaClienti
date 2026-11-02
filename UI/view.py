import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP - ChinookCatenaClienti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - ChinookCatenaClienti", color="blue", size=24)
        self._page.controls.append(self._title)

        # ---------- PUNTO 1 ----------
        self._ddAnnoDa = ft.Dropdown(label="Anno da")
        self._ddAnnoA = ft.Dropdown(label="Anno a")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                               on_click=self._controller.handleCreaGrafo)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa Info",
                                                on_click=self._controller.handleStampaInfo)

        row1 = ft.Row([ft.Container(self._ddAnnoDa, width=150),
                       ft.Container(self._ddAnnoA, width=150),
                       ft.Container(self._btnCreaGrafo, width=150),
                       ft.Container(self._btnStampaInfo, width=150)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # ---------- PUNTO 2 ----------
        self._ddClienti = ft.Dropdown(label="Cliente di partenza")
        self._txtInL = ft.TextField(label="L (numero di archi)")
        self._btnCammino = ft.ElevatedButton(text="Trova cammino",
                                             on_click=self._controller.handleCammino)

        row2 = ft.Row([ft.Container(self._ddClienti, width=300),
                       ft.Container(self._txtInL, width=150),
                       ft.Container(self._btnCammino, width=150)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)

        # riempio gli anni all'avvio
        self._controller.fillDDAnni()

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()