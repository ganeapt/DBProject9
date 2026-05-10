import customtkinter as ctk
from tkinter import messagebox
from transactions import TransactionService

class User:
    def __init__(self, app, client_id):
        self.app = app
        self.client_id = client_id
        self.menu_expanded = False
        self.app.db_config = self.app.all_configs['user']
        self.transaction_service = TransactionService(self.app.db)
        self.app.curata_pagina()

        self.sidebar = ctk.CTkFrame(self.app, width=200, corner_radius=0, fg_color=self.app.theme["bg_panel"])
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = ctk.CTkFrame(self.app, fg_color="transparent")
        self.content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        self.toggle_button = ctk.CTkButton(self.sidebar, text="☰", width=40, height=40, fg_color="transparent", hover_color=self.app.theme["btn_hover"], command=self.toggle_menu)
        self.toggle_button.pack(anchor="nw", pady=10, padx=10)
        
        self.button_situatie = ctk.CTkButton(self.sidebar, text="Situație Conturi", command=self.afiseaza_situatie_conturi, **self.app.styles["card"])
        self.button_situatie.pack(pady=10, padx=10, fill="x")

        self.button_logout = ctk.CTkButton(self.sidebar, text="Log Out", fg_color=self.app.theme["danger"], hover_color=self.app.theme["danger_hover"], command=self.app.afiseaza_dashboard)
        self.button_logout.pack(side="bottom", pady=20, padx=10, fill="x")

        first_acccount = self.app.ruleaza_query("SELECT iban FROM v_dashboard_conturi WHERE id_client = %s LIMIT 1", (self.client_id,))
        if first_acccount:
            self.display_account_hub(first_acccount[0][0])
        else:
            self.afiseaza_situatie_conturi()

    def curata_content(self):
        """Șterge doar ce e în frame-ul din dreapta."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def toggle_menu(self):
        if self.menu_expanded:
            self.button_situatie.pack_forget()
            self.button_logout.configure(text="X")
            self.sidebar.configure(width=60)
            self.menu_expanded = False
        else:
            self.sidebar.configure(width=200)
            self.button_situatie.pack(pady=10, padx=10, fill="x")
            self.button_logout.configure(text="Log Out")
            self.button_logout.pack_forget()
            self.button_logout.pack(side="bottom", pady=20, padx=10, fill="x")
            self.menu_expanded = True


    def afiseaza_situatie_conturi(self):
        self.curata_content()
        self.app.add_label(self.content, "Alege Contul", type="h1", pady=(10, 20))

        sql = "SELECT iban, sold, moneda FROM v_dashboard_conturi WHERE id_client = %s"
        date = self.app.ruleaza_query(sql, (self.client_id,))
        numar_conturi_reale = len(date) if date else 0

        for i in range(1, 6):
            if i <= numar_conturi_reale:
                iban, sold, moneda = date[i-1]
                btn_text = f"CONT {i} | {iban}\nSOLD: {sold} {moneda}"
                border_width = 2
                state = "normal"
                cmd = lambda iban_s=iban: self.display_account_hub(iban_s)
            else:
                btn_text = f"CONT {i} | Slot Disponibil"
                state = "disabled"
                border_width = 0
                cmd = None

            ctk.CTkButton(
                self.content,
                text=btn_text,
                width=500,
                height=60,
                state=state,
                font=("Courier New", 13, "bold") if i <= numar_conturi_reale else ("Roboto", 12),
                command=cmd,
                **{**self.app.styles["card"], "border_width": border_width}
            ).pack(pady=8)

    def display_account_hub(self, iban):
            self.curata_content()
            
            query = "SELECT sold, moneda FROM v_dashboard_conturi WHERE iban = %s"
            details = self.app.ruleaza_query(query, (iban,))
            balance, currency = details[0] if details else (0, "N/A")

            self.app.add_label(self.content, f"Account: {iban}", type="tech", pady=(10, 0))
            self.app.add_label(self.content, f"{balance} {currency}", type="h1", pady=(0, 20))

            actions_frame = ctk.CTkFrame(self.content, fg_color="transparent")
            actions_frame.pack(expand=True)

            buttons = [
                ("New Transfer", lambda: self.display_contacts(iban)),
                ("History", lambda: print("History Page")),
                ("Statement", lambda: print("Statement Page")),
                ("Beneficiaries", lambda: print("Contacts Page"))
            ]

            for i, (text, cmd) in enumerate(buttons):
                row, col = divmod(i, 2)
                ctk.CTkButton(
                    actions_frame, 
                    text=text, 
                    width=180, 
                    height=100, 
                    font=("Roboto", 14, "bold"),
                    command=cmd,
                    **self.app.styles["card"]
                ).grid(row=row, column=col, padx=10, pady=10)

    def new_transfer(self, source_iban):
        iban = self.recipient_iban_entry.get()
        amount = self.amount_entry.get()
        details = self.details_entry.get()

        success = self.transaction_service.executa_transfer(source_iban, iban, amount, details)
        if success:
            self.display_account_hub(source_iban)


    def display_contacts(self, source_iban):
        self.curata_content()
        self.app.add_label(self.content, "SELECT RECIPIENT", type="h1", pady=20)

        scroll_frame = ctk.CTkScrollableFrame(self.content, width=500, height=300, fg_color=self.app.theme["bg_dark"])
        scroll_frame.pack(pady=10, padx=10)

        contacts = self.app.ruleaza_query("SELECT nume_beneficiar, iban_beneficiar FROM beneficiari WHERE id_client = %s", (self.client_id,))

        if not contacts:
            self.app.add_label(scroll_frame, "No contacts found.", type="tech", pady=20)
        else:
            for name, iban in contacts:
                ctk.CTkButton(
                    scroll_frame,
                    text=f"{name}\n{iban}",
                    width=450,
                    height=60,
                    anchor="w",
                    command=lambda n=name, i=iban: self.display_amount_entry(source_iban, n, i),
                    **self.app.styles["card"]
                ).pack(pady=5)

        ctk.CTkButton(self.content, text="Enter IBAN Manually", fg_color="transparent", border_width=2, border_color=self.app.theme["btn_main"], text_color=self.app.theme["text_main"],
                    command=lambda: self.display_amount_entry(source_iban, "Manual Entry", "")).pack(pady=10)
        
    def display_amount_entry(self, source_iban, recipient_name, target_iban):
        self.curata_content()
        
        self.app.add_label(self.content, "TRANSFER DETAILS", type="h2", pady=10)

        self.app.add_label(self.content, f"From: {source_iban}", type="tech")
        self.app.add_label(self.content, f"To: {recipient_name}", type="form", pady=5)

        self.app.add_label(self.content, "Recipient IBAN:", type="form", pady=(5, 0))
        self.recipient_iban_entry = ctk.CTkEntry(self.content, width=350, **self.app.styles["input"])
        self.recipient_iban_entry.insert(0, target_iban)
        self.recipient_iban_entry.pack(pady=2)

        self.app.add_label(self.content, "Amount:", type="form", pady=(5, 0))
        self.amount_entry = ctk.CTkEntry(self.content, width=350, placeholder_text="0.00", **self.app.styles["input"])
        self.amount_entry.pack(pady=2)

        self.app.add_label(self.content, "Details:", type="form", pady=(5, 0))
        self.details_entry = ctk.CTkEntry(self.content, width=350, placeholder_text="Reason for payment", **self.app.styles["input"])
        self.details_entry.pack(pady=2)

        ctk.CTkButton(
            self.content, 
            text="CONFIRM & SEND", 
            fg_color=self.app.theme["success"],
            hover_color=self.app.theme["success_hover"],
            text_color=self.app.theme["bg_dark"],
            width=180, height=35,
            font=("Roboto", 13, "bold"),
            command=lambda: self.new_transfer(source_iban)
        ).pack(pady=20)

        ctk.CTkButton(self.content, text="← Back to contacts", fg_color="transparent", text_color=self.app.theme["text_dim"], 
                      command=lambda: self.display_contacts(source_iban)).pack()
    