import customtkinter as ctk

class User:
    def __init__(self, app, client_id):
        self.app = app
        self.client_id = client_id
        self.app.db_config = self.app.all_configs['user']
        self.app.curata_pagina()

        self.sidebar = ctk.CTkFrame(self.app, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self.app, fg_color="transparent")
        self.content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self.sidebar, text="MENU CLIENT", font=("Roboto", 20, "bold")).pack(pady=20, padx=10)
        
        ctk.CTkButton(self.sidebar, text="Situație Conturi", command=self.afiseaza_situatie_conturi).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="Transfer Nou", command=lambda: print("Transfer")).pack(pady=10, padx=10)
        
        ctk.CTkButton(self.sidebar, text="Log Out", fg_color="darkred", command=self.app.afiseaza_dashboard).pack(side="bottom", pady=20)

        self.afiseaza_situatie_conturi()

    def curata_content(self):
        """Șterge doar ce e în frame-ul din dreapta."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def afiseaza_situatie_conturi(self):
        self.curata_content()
        ctk.CTkLabel(self.content, text="SITUAȚIE CONTURI", font=("Roboto", 24, "bold")).pack(pady=10)
        
        sql = "SELECT iban, sold, moneda FROM v_dashboard_conturi WHERE id_client = %s"
        date = self.app.ruleaza_query(sql, (self.client_id,))
        
        if date:
            for r in date:
                card = ctk.CTkFrame(self.content)
                card.pack(fill="x", pady=5)
                ctk.CTkLabel(card, text=f"{r[0]} | {r[1]} {r[2]}", font=("Courier New", 14)).pack(padx=10, pady=5)
        else:
            ctk.CTkLabel(self.content, text="Nu ai conturi active.").pack()
