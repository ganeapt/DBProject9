import customtkinter as ctk
from tkinter import messagebox

class User:
    def __init__(self, app, client_id):
        self.app = app
        self.client_id = client_id
        self.menu_expanded = False
        self.app.db_config = self.app.all_configs['user']
        self.app.curata_pagina()

        self.sidebar = ctk.CTkFrame(self.app, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = ctk.CTkFrame(self.app, fg_color="transparent")
        self.content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        self.toggle_button = ctk.CTkButton(self.sidebar, text="☰", width=40, height=40, fg_color="transparent", hover_color="#333333", command=self.toggle_menu)
        self.toggle_button.pack(anchor="nw", pady=10, padx=10)
        
        self.button_situatie = ctk.CTkButton(self.sidebar, text="Situație Conturi", command=self.afiseaza_situatie_conturi)
        self.button_situatie.pack(pady=10, padx=10, fill="x")

        self.button_logout = ctk.CTkButton(self.sidebar, text="Log Out", fg_color="darkred", command=self.app.afiseaza_dashboard)
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
        ctk.CTkLabel(self.content, text="Alege Contul", font=("Roboto", 24, "bold")).pack(pady=(10, 20))

        sql = "SELECT iban, sold, moneda FROM v_dashboard_conturi WHERE id_client = %s"
        date = self.app.ruleaza_query(sql, (self.client_id,))
        numar_conturi_reale = len(date) if date else 0

        for i in range(1, 6):
            if i <= numar_conturi_reale:
                iban, sold, moneda = date[i-1]
                btn_text = f"CONT {i} | {iban}\nSOLD: {sold} {moneda}"
                color = "#1f538d"
                state = "normal"
                cmd = lambda iban_s=iban: self.display_account_hub(iban_s)
            else:
                btn_text = f"CONT {i} | Slot Disponibil"
                color = "#2b2b2b"
                state = "disabled"
                cmd = None

            ctk.CTkButton(
                self.content,
                text=btn_text,
                width=500,
                height=60,
                fg_color=color,
                state=state,
                font=("Courier New", 13, "bold") if i <= numar_conturi_reale else ("Roboto", 12),
                command=cmd
            ).pack(pady=8)

    def display_account_hub(self, iban):
            self.curata_content()
            
            query = "SELECT sold, moneda FROM v_dashboard_conturi WHERE iban = %s"
            details = self.app.ruleaza_query(query, (iban,))
            balance, currency = details[0] if details else (0, "N/A")

            ctk.CTkLabel(self.content, text=f"Account: {iban}", font=("Courier New", 18, "bold")).pack(pady=(10, 0))
            ctk.CTkLabel(self.content, text=f"{balance} {currency}", font=("Roboto", 32, "bold")).pack(pady=(0, 20))

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
                    command=cmd
                ).grid(row=row, column=col, padx=10, pady=10)

    def display_contacts(self, source_iban):
        self.curata_content()
        ctk.CTkLabel(self.content, text="SELECT RECIPIENT", font=("Roboto", 22, "bold")).pack(pady=20)

        scroll_frame = ctk.CTkScrollableFrame(self.content, width=500, height=300)
        scroll_frame.pack(pady=10, padx=10)

        # Fetch contacts from DB
        contacts = self.app.ruleaza_query("SELECT nume_beneficiar, iban_beneficiar FROM beneficiari WHERE id_client = %s", (self.client_id,))

        if not contacts:
            ctk.CTkLabel(scroll_frame, text="No contacts found.").pack(pady=20)
        else:
            for name, iban in contacts:
                # Each contact is a wide button
                ctk.CTkButton(
                    scroll_frame,
                    text=f"{name}\n{iban}",
                    width=450,
                    height=60,
                    anchor="w", # Text aligned to the left
                    command=lambda n=name, i=iban: self.display_amount_entry(source_iban, n, i)
                ).pack(pady=5)

        # Manual entry button at the bottom
        ctk.CTkButton(self.content, text="Enter IBAN Manually", fg_color="transparent", border_width=2,
                    command=lambda: self.display_amount_entry(source_iban, "Manual Entry", "")).pack(pady=10)
        
    def display_amount_entry(self, source_iban, recipient_name, target_iban):
        self.curata_content()
        
        # Reducem pady-urile ca să încapă totul pe 500px înălțime
        ctk.CTkLabel(self.content, text="TRANSFER DETAILS", font=("Roboto", 22, "bold")).pack(pady=10)

        ctk.CTkLabel(self.content, text=f"From: {source_iban}", font=("Courier New", 11)).pack()
        ctk.CTkLabel(self.content, text=f"To: {recipient_name}", font=("Roboto", 14, "bold"), text_color="#1f538d").pack(pady=5)

        # Recipient IBAN
        ctk.CTkLabel(self.content, text="Recipient IBAN:").pack(pady=(5, 0))
        self.recipient_iban_entry = ctk.CTkEntry(self.content, width=350)
        self.recipient_iban_entry.insert(0, target_iban)
        self.recipient_iban_entry.pack(pady=2)

        # Amount
        ctk.CTkLabel(self.content, text="Amount:").pack(pady=(5, 0))
        self.amount_entry = ctk.CTkEntry(self.content, width=350, placeholder_text="0.00")
        self.amount_entry.pack(pady=2)

        # Details
        ctk.CTkLabel(self.content, text="Details:").pack(pady=(5, 0))
        self.details_entry = ctk.CTkEntry(self.content, width=350, placeholder_text="Reason for payment")
        self.details_entry.pack(pady=2)

        # Butonul de trimitere (Confirm)
        ctk.CTkButton(
            self.content, 
            text="CONFIRM & SEND", 
            fg_color="green", 
            width=180, height=35,
            font=("Roboto", 13, "bold"),
            command=lambda: self.initiate_transfer(source_iban)
        ).pack(pady=15)

        # Butonul de înapoi (Fixat denumirea metodei aici)
        ctk.CTkButton(self.content, text="← Back to contacts", fg_color="transparent", 
                      command=lambda: self.display_contacts(source_iban)).pack()
    def initiate_transfer(self, source_iban):
        raw_target_iban = self.recipient_iban_entry.get()
        raw_amount = self.amount_entry.get()
        raw_details = self.details_entry.get()

        # .strip() elimina spatiile de la inceput si sfarsit
        clean_target_iban = raw_target_iban.strip()
        clean_amount = raw_amount.strip()
        clean_details = raw_details.strip()

        if clean_target_iban == "" or clean_amount == "":
            messagebox.showwarning("Empty Fields", "Please enter both IBAN and Amount!")
            return

        if clean_details == "":
            clean_details = "Banking Transfer"

        sql_command = "CALL EfectueazaTransfer(%s, %s, %s, %s)"
        params = (source_iban, clean_target_iban, clean_amount, clean_details)

        try:
            self.app.ruleaza_query(sql_command, params, fetch=False)
            messagebox.showinfo("Success", f"Transfer of {clean_amount} RON was successful!")
            self.display_account_hub(source_iban)

        except Exception as error:
            messagebox.showerror("Transfer Error", str(error))