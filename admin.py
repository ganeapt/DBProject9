import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox

class Admin:
    def __init__(self, app, admin_id):
        self.app = app
        self.admin_id = admin_id
        self.app.db_config = self.app.all_configs['admin']
        self.app.curata_pagina()

        self.content = ctk.CTkFrame(self.app, fg_color="transparent")
        self.content.pack(expand=True, fill="both", padx=20, pady=20)

        self.is_viewing_audit = False

        self.afiseaza_dashboard()

    def curata_content(self):
        """Șterge tot ce este afișat pe ecranul curent."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def afiseaza_dashboard(self):
        """Ecranul principal."""
        self.curata_content()

        ctk.CTkLabel(self.content, text="Admin Dashboard", font=("Roboto", 26, "bold"), text_color=self.app.theme["text_main"]).pack(pady=20)

        grid_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        grid_frame.pack(expand=True)

        btn_audit = ctk.CTkButton(grid_frame, text="Audit Solduri", command=self.afiseaza_audit, **self.app.styles["btn_options"])
        btn_audit.grid(row=0, column=0, padx=15, pady=15)

        btn_alerte = ctk.CTkButton(grid_frame, text="Trimite Alertă", command=self.afiseaza_alerte, **self.app.styles["btn_options"])
        btn_alerte.grid(row=0, column=1, padx=15, pady=15)

        btn_frauda = ctk.CTkButton(grid_frame, text="Tranzacții Suspecte", command=self.afiseaza_frauda, **self.app.styles["btn_options"])
        btn_frauda.grid(row=0, column=2, padx=15, pady=15)

        self.btn_logout = ctk.CTkButton(
            self.content, 
            text="Log Out", 
            fg_color=self.app.theme["danger"], 
            hover_color=self.app.theme["danger_hover"], 
            command=self.app.afiseaza_dashboard
        )
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
        """Inițializează pagina de audit în format tabelar."""
        self.curata_content()
        self.is_viewing_audit = True 

        self.app.add_label(self.content, "AUDIT TRAIL: MODIFICĂRI SOLDURI", type="h1", pady=(10, 20))

        frame_date = ctk.CTkFrame(self.content, fg_color="transparent")
        frame_date.pack(padx=20, pady=10, fill="both", expand=True)

        stil = ttk.Style()
        stil.theme_use("clam")
        
        stil.configure("Treeview", 
                       background=self.app.theme["bg_panel"], 
                       fieldbackground=self.app.theme["bg_panel"], 
                       foreground=self.app.theme["text_main"],
                       font=("Roboto", 14), 
                       rowheight=35)        
                       
        stil.configure("Treeview.Heading", 
                       background=self.app.theme["card_inner"], 
                       foreground=self.app.theme["text_main"], 
                       font=("Roboto", 14, "bold"), 
                       borderwidth=0)

        coloane = ("ID Audit", "ID Cont", "Nume Client", "Sold Vechi", "Sold Nou")
        self.tabel = ttk.Treeview(frame_date, columns=coloane, show="headings")
        
        latimi_coloane = {
            "ID Audit": 120, 
            "ID Cont": 120, 
            "Nume Client": 280, 
            "Sold Vechi": 140, 
            "Sold Nou": 140
        }
        
        for col in coloane:
            self.tabel.heading(col, text=col)
            self.tabel.column(col, width=latimi_coloane[col], anchor="center")
            
        self.tabel.pack(side="left", fill="both", expand=True)
        self.tabel.tag_configure("Blocat", background=self.app.theme["danger"], foreground=self.app.theme["text_main"])
        self.tabel.tag_configure("Activ", background=self.app.theme["bg_panel"], foreground=self.app.theme["text_main"])

        scrollbar = ctk.CTkScrollbar(
            frame_date, 
            orientation="vertical", 
            command=self.tabel.yview,
            button_color=self.app.theme["btn_accent"],       
            button_hover_color=self.app.theme["btn_hover"]   
        )
        scrollbar.pack(side="right", fill="y")
        self.tabel.configure(yscrollcommand=scrollbar.set)
        
        bottom_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=20, pady=(10, 20))

        ctk.CTkButton(
            bottom_frame, 
            text="← Înapoi la Dashboard", 
            command=self.paraseste_audit,
            **self.app.styles["btn_back"],
        ).pack(side="left")

        ctk.CTkButton(
            bottom_frame, 
            text="Deblochează Cont", 
            fg_color=self.app.theme["success"], 
            hover_color=self.app.theme["success_hover"], 
            text_color=self.app.theme["bg_dark"], 
            font=("Roboto", 14, "bold"), 
            command=lambda: self.schimba_status_selectat("Activ")
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            bottom_frame, 
            text="Blochează Cont", 
            fg_color=self.app.theme["danger"], 
            hover_color=self.app.theme["danger_hover"], 
            font=("Roboto", 14, "bold"), 
            command=lambda: self.schimba_status_selectat("Blocat")
        ).pack(side="right", padx=(0, 10))

        self.incarca_date_audit()

    def schimba_status_selectat(self, noul_status):
        """Identifică ID Cont din rândul selectat și îi modifică starea în DB."""
        selectie = self.tabel.selection()
        
        if not selectie:
            messagebox.showwarning("Atenție", "Nu ai selectat niciun rand!")
            return

        try:
            valori = self.tabel.item(selectie[0])["values"]
            if not valori:
                return
                
            id_cont = valori[1]

            self.app.ruleaza_query(
                "UPDATE conturi SET status = %s WHERE id_cont = %s", 
                (noul_status, id_cont), 
                fetch=False
            )
            
            messagebox.showinfo("Succes", f"Contul ID {id_cont} a fost marcat ca fiind '{noul_status}' in baza de date!")
            
            self.incarca_date_audit()
        except Exception as e:
            messagebox.showerror("Eroare", f"A aparut o problema la comunicarea cu DB: {str(e)}")

    def incarca_date_audit(self):
        """Curăță și inserează rândurile în Treeview."""
        if not self.is_viewing_audit:
            return

        selectie_veche = self.tabel.selection()
        id_audit_selectat = None
        if selectie_veche:
            valori_vechi = self.tabel.item(selectie_veche[0])["values"]
            if valori_vechi:
                id_audit_selectat = valori_vechi[0]

        for item in self.tabel.get_children():
            self.tabel.delete(item)

        sql = """
            SELECT 
                a.id_audit, 
                a.id_cont, 
                COALESCE(CONCAT(pf.nume, ' ', pf.prenume), pj.denumire_firma, cl.email) AS nume_complet,
                a.sold_vechi, 
                a.sold_nou,
                c.status 
            FROM audit_solduri a
            JOIN conturi c ON a.id_cont = c.id_cont
            JOIN clienti cl ON c.id_client = cl.id_client
            LEFT JOIN detalii_pf pf ON cl.id_client = pf.id_client
            LEFT JOIN detalii_pj pj ON cl.id_client = pj.id_client
            ORDER BY a.id_audit DESC
        """
        
        rezultat = self.app.ruleaza_query(sql)
        if rezultat:
            for row in rezultat:
                item_id = self.tabel.insert("", "end", values=row[:5], tags=(row[5],))
                
                if id_audit_selectat and row[0] == id_audit_selectat:
                    self.tabel.selection_set(item_id)
                    self.tabel.focus(item_id)

        self.app.after(3000, self.incarca_date_audit)

    def paraseste_audit(self):
        """Oprește complet loop-ul de query-uri și revine în dashboard."""
        self.is_viewing_audit = False
        self.afiseaza_dashboard()

    def afiseaza_alerte(self):
        self.curata_content()
        self.app.add_label(self.content, "TRIMITE NOTIFICARE DIRECTĂ", type="h1", pady=(10, 20))
        self._add_back_button()

    def afiseaza_frauda(self):
        self.curata_content()
        self.app.add_label(self.content, "DETECTOR DE FRAUDĂ: TRANZACȚII SUSPECTE", type="h1", pady=(10, 20))
        self._add_back_button()