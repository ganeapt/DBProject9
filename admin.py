import customtkinter as ctk

class Admin:
    def __init__(self, app, admin_id):
        self.app = app
        self.admin_id = admin_id
        self.app.db_config = self.app.all_configs['admin']
        self.app.curata_pagina()

        self.content = ctk.CTkFrame(self.app, fg_color="transparent")
        self.content.pack(expand=True, fill="both", padx=20, pady=20)

        # Încărcăm direct Dashboard-ul identic ca stil cu cel de User
        self.afiseaza_dashboard()

    def curata_content(self):
        """Șterge tot ce este afișat pe ecranul curent."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def afiseaza_dashboard(self):
        """Ecranul principal cu cele 4 butoane mari și Log Out în jos-stânga."""
        self.curata_content()
        

        ctk.CTkLabel(self.content, text="Admin Dashboard", font=("Roboto", 26, "bold"), text_color=self.app.theme["text_main"]).pack(pady=20)

        grid_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        grid_frame.pack(expand=True)

        btn_audit = ctk.CTkButton(grid_frame, text="Audit Solduri", command=self.afiseaza_audit, **self.app.styles["btn_options"])
        btn_audit.grid(row=0, column=0, padx=15, pady=15)

        btn_gestiune = ctk.CTkButton(grid_frame, text="Blocare Conturi", command=self.afiseaza_gestiune, **self.app.styles["btn_options"])
        btn_gestiune.grid(row=0, column=1, padx=15, pady=15)

        btn_alerte = ctk.CTkButton(grid_frame, text="Trimite Alertă", command=self.afiseaza_alerte, **self.app.styles["btn_options"])
        btn_alerte.grid(row=1, column=0, padx=15, pady=15)

        btn_frauda = ctk.CTkButton(grid_frame, text="Tranzacții Suspecte", command=self.afiseaza_frauda, **self.app.styles["btn_options"])
        btn_frauda.grid(row=1, column=1, padx=15, pady=15)

        # Butonul de Log Out poziționat în colțul de jos-stânga al frame-ului principal
        self.btn_logout = ctk.CTkButton(
            self.content, 
            text="Log Out", 
            fg_color=self.app.theme["danger"], 
            hover_color=self.app.theme["danger_hover"], 
            command=self.app.afiseaza_dashboard
        )
        
        # --- Aici e modificarea ---
        # Folosim side="bottom" pentru a-l împinge jos de tot
        # Folosim anchor="sw" pentru a-l alinia în stânga
        # Folosim padx=20 pentru a-l decala de la marginea ferestrei
        self.btn_logout.pack(side="bottom", anchor="sw", padx=20, pady=(20, 10))


    def _add_back_button(self):
        """Metodă privată pentru a pune rapid butonul de înapoi."""
        ctk.CTkButton(
            self.content, 
            text="← Înapoi la Dashboard", 
            command=self.afiseaza_dashboard,
            **self.app.styles["btn_back"]
        ).pack(pady=30)

    def afiseaza_audit(self):
        self.curata_content()
        self.app.add_label(self.content, "AUDIT TRAIL: MODIFICĂRI SOLDURI", type="h1", pady=(10, 20))
        self._add_back_button()

    def afiseaza_gestiune(self):
        self.curata_content()
        self.app.add_label(self.content, "GESTIUNE CONTURI BANCARE", type="h1", pady=(10, 20))
        self._add_back_button()

    def afiseaza_alerte(self):
        self.curata_content()
        self.app.add_label(self.content, "TRIMITE NOTIFICARE DIRECTĂ", type="h1", pady=(10, 20))
        self._add_back_button()

    def afiseaza_frauda(self):
        self.curata_content()
        self.app.add_label(self.content, "DETECTOR DE FRAUDĂ: TRANZACȚII SUSPECTE", type="h1", pady=(10, 20))
        self._add_back_button()