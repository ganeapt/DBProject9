import customtkinter as ctk

class Admin:
    def __init__(self, app):
        self.app = app
        self.app.db_config = self.app.all_configs['admin']
        self.app.curata_pagina()

        self.titlu = ctk.CTkLabel(self.app, text="ADMIN PANEL", font=("Roboto", 26, "bold"))
        self.titlu.pack(pady=50)

        self.btn_back = ctk.CTkButton(self.app, text="← Meniu Principal", command=self.app.afiseaza_dashboard)
        self.btn_back.pack(pady=10)

