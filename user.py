import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
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
                ("History", lambda: self.afiseaza_istoric(iban)),
                ("Statement", lambda: self.statements_interface(iban)),
                ("Beneficiaries", lambda: self.display_beneficiaries(iban))
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

        scroll_frame = ctk.CTkScrollableFrame(self.content, width=500, height=300, fg_color=self.app.theme["bg_dark"], **self.app.styles["scrollbar"])
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

        ctk.CTkButton(self.content, text="Enter IBAN Manually", fg_color="transparent", border_width=2, border_color=self.app.theme["btn_accent"], text_color=self.app.theme["text_main"],
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
            width=180, height=35,
            command=lambda: self.new_transfer(source_iban),
            **self.app.styles["btn_confirm"]
        ).pack(pady=20)

        ctk.CTkButton(self.content, text="← Înapoi",command=lambda: self.display_contacts(source_iban), **self.app.styles["btn_back"]).pack()
        

    def _add_row_label(self, container, text, type):
        lbl = self.app.add_label(container, text, type=type)
        lbl.configure(height=0) 
        lbl.pack(anchor="w", pady=0)
        return lbl
    
    def afiseaza_istoric(self, iban_ales):
        sql = "SELECT data_tranzactie, entitate, suma, tip_tranzactie, iban_partener, motiv_plata FROM v_istoric_tranzactii WHERE iban_cont = %s ORDER BY data_tranzactie DESC"
        tranzactii = self.app.ruleaza_query(sql, (iban_ales,))
    
        self.content.pack_forget()
        self.curata_content()
        
        self._construieste_istoric_ui(iban_ales, tranzactii)
        self.content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

    def _construieste_istoric_ui(self, iban_ales, tranzactii):
        self.app.add_label(self.content, f"ISTORIC: {iban_ales}", type="h2")

        scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent", **self.app.styles["scrollbar"])
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        if not tranzactii:
            self.app.add_label(scroll, "Nu există tranzacții.", type="dim")
        else:
            for t in tranzactii:
                self._creeaza_rand_tranzactie(scroll, t)

        nav_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        nav_frame.pack(side="bottom", fill="x", pady=10)
        ctk.CTkButton(nav_frame, text="← Înapoi", command=lambda: self.display_account_hub(iban_ales), **self.app.styles["btn_back"]).pack()

    def _creeaza_rand_tranzactie(self, parent, data_t):
        data, entitate, suma, tip, iban_partener, motiv_plata = data_t
        
        if tip == 'Iesire':
            color = self.app.theme["danger"]
            semn = "-"
        else:
            color = self.app.theme["success"]
            semn = "+"

        rand = ctk.CTkFrame(parent, **self.app.styles["transaction_row"], corner_radius=12)
        rand.pack(pady=5, fill="x", padx=5)

        txt_col = ctk.CTkFrame(rand, fg_color="transparent")
        txt_col.pack(side="left", padx=15, pady=8)

        self._add_row_label(txt_col, data.strftime('%H:%M'), "lbl_data")
        self._add_row_label(txt_col, entitate, "lbl_primary")
        self._add_row_label(txt_col, iban_partener or "-", "lbl_data")
        self._add_row_label(txt_col, f"Motiv: {motiv_plata or '-'}", "lbl_secondary")

        ctk.CTkLabel(rand, text=f"{semn}{suma} RON", text_color=color, font=("Roboto", 16, "bold")).pack(side="right", padx=20)



    def _create_date_selector(self, parent, title, days, months, years, d_day, d_month, d_year):
        """Helper function to create a row of 3 dropdowns."""
        self.app.add_label(parent, title, type="form").pack(anchor="center")
        selector_frame = ctk.CTkFrame(parent, fg_color="transparent")
        selector_frame.pack(pady=(5, 15))
        
        day_cb = ctk.CTkComboBox(selector_frame, values=days, width=75, **self.app.styles["combobox"])
        day_cb.set(d_day); day_cb.pack(side="left", padx=2)
        
        month_cb = ctk.CTkComboBox(selector_frame, values=months, width=75, **self.app.styles["combobox"])
        month_cb.set(d_month); month_cb.pack(side="left", padx=2)
        
        year_cb = ctk.CTkComboBox(selector_frame, values=years, width=95, **self.app.styles["combobox"])
        year_cb.set(d_year); year_cb.pack(side="left", padx=2)
        
        return day_cb, month_cb, year_cb



    def statements_interface(self, iban):
        self.curata_content()
        main_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=10, pady=5)

        self.app.add_label(main_frame, "CONFIGURARE EXTRAS", type="h2").pack(pady=(0, 25))

        days = [str(i).zfill(2) for i in range(1, 32)]
        months = [str(i).zfill(2) for i in range(1, 13)]
        years = ["2024", "2025", "2026"]

        self.start_day, self.start_month, self.start_year = self._create_date_selector(
            main_frame, "Data Început:", days, months, years, "01", "01", "2026"
        )
        
        self.end_day, self.end_month, self.end_year = self._create_date_selector(
            main_frame, "Data Sfârșit:", days, months, years, "31", "12", "2026"
        )

        buttons_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_container.pack(pady=(60, 0))

        ctk.CTkButton(
            buttons_container, 
            text="Generează Extras (.txt)", 
            width=250, height=40,
            command=lambda: self.process_statement_generation(
                iban, 
                self.start_day.get(), self.start_month.get(), self.start_year.get(),
                self.end_day.get(), self.end_month.get(), self.end_year.get()
            ),
            **self.app.styles["btn_action"]
        ).pack(pady=5)

        ctk.CTkButton(
            buttons_container, 
            text="← Înapoi",
            command=lambda: self.display_account_hub(iban),
            **self.app.styles["btn_back"]
        ).pack(pady=5)



    def format_as_mysql_table(self, headers, data):
        widths = []
        for i in range(len(headers)):
            max_w = len(headers[i])
            for row in data:
                val_len = len(str(row[i]))
                if val_len > max_w:
                    max_w = val_len
            widths.append(max_w)

        separator = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
        lines = [separator]

        header_line = "|" + "|".join(f" {headers[i]:<{widths[i]}} " for i in range(len(headers))) + "|"
        lines.append(header_line)
        lines.append(separator)
        
        for row in data:
            formatted_row = []
            for i in range(len(row)):
                val = str(row[i])
                formatted_row.append(f" {val:<{widths[i]}} ")
            lines.append("|" + "|".join(formatted_row) + "|")
        
        lines.append(separator)
        return "\n".join(lines)



    def process_statement_generation(self, iban, start_d, start_m, start_y, end_d, end_m, end_y):
        start_date = f"{start_y}-{start_m.zfill(2)}-{start_d.zfill(2)} 00:00:00"
        end_date = f"{end_y}-{end_m.zfill(2)}-{end_d.zfill(2)} 23:59:59"

        sql = "CALL GenereazaExtras(%s, %s, %s)"
        statement_data = self.app.ruleaza_query(sql, (iban, start_date, end_date))

        if not statement_data:
            messagebox.showinfo("Info", "Nu există tranzacții în perioada selectată.")
            return

        headers = ["DATA", "TIP", "SUMA", "PARTENER", "MOTIV"]
        rows = []
        for d, t, s, p, m in statement_data:
            if t == 'Iesire':
                sign = "-"
            else:
                sign = "+"

            rows.append([
                d.strftime('%d.%m.%Y %H:%M'), 
                t, 
                f"{sign}{s:.2f}", 
                str(p), 
                str(m)
            ])

        mysql_table = self.format_as_mysql_table(headers, rows)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"Extras_{iban}.txt",
            title="Salvează Extrasul"
        )
        
        if not file_path: 
            return
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"EXTRAS CONT: {iban}\n")
                f.write(f"PERIOADA: {start_date} - {end_date}\n")
                f.write(f"GENERAT LA: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")
                
                f.write(mysql_table)
                
                f.write(f"\n\nDocument generat de Sistem Bancar Proiect 9\n")
            
            messagebox.showinfo("Succes", "Extras salvat în format MariaDB!")
            self.display_account_hub(iban)
            
        except Exception as e:
            messagebox.showerror("Eroare la scriere", f"Eroare: {e}")



    
    def display_beneficiaries(self, source_iban=None):
        self.content.pack_forget()
        self.curata_content()
        self.app.add_label(self.content, "AGENDA BENEFICIARI", type="h1", pady=(10, 20))

        search_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=5)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Caută după nume sau IBAN...", width=350, **self.app.styles["input"])
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_beneficiary_table())

        ctk.CTkButton(search_frame, text="+ Adaugă", width=100, fg_color=self.app.theme["success"], command=self.add_beneficiary_form).pack(side="right", padx=5)

        self.table_frame = ctk.CTkScrollableFrame(self.content, fg_color=self.app.theme["bg_dark"], **self.app.styles["scrollbar"])
        self.table_frame.pack(pady=10, fill="both", expand=True)

        ctk.CTkButton(
            self.content, 
            text="← Înapoi", 
            command=lambda: self.display_account_hub(source_iban),
            **self.app.styles["btn_back"]
        ).pack(pady=(2, 2))

        self.content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        self.app.bind("<Button-1>", lambda e: self.app.focus() if "entry" not in str(e.widget).lower() else None)

        self.refresh_beneficiary_table()

    def get_bank_info(self, iban):
        code = iban[4:8].upper()    # Extrage codul băncii (ex: BTRL)
        bm = self.app.theme.get("bank_map", {})
        return bm.get(code, bm.get("GENERIC", {"name": "???", "color": "#404040", "text": "#FFFFFF"}))


    def refresh_beneficiary_table(self):
        search_query = self.search_entry.get().lower() if hasattr(self, 'search_entry') else ""
        
        for widget in self.table_frame.winfo_children(): widget.destroy()

        contacts = self.app.ruleaza_query("SELECT nume_beneficiar, iban_beneficiar FROM beneficiari WHERE id_client = %s ORDER BY nume_beneficiar ASC", (self.client_id,))

        has_results = False
        for name, iban in contacts:
            if search_query and search_query not in name.lower() and search_query not in iban.lower():
                continue
            
            has_results = True
            bank = self.get_bank_info(iban)

            b_color = bank["color"]
            
            row = ctk.CTkFrame(self.table_frame, **self.app.styles["transaction_row"], height=55, corner_radius=12)
            row.pack(fill="x", pady=4, padx=5)
            row.pack_propagate(False)

            BADGE_WIDTH = 45
            BADGE_HEIGHT = 25

            badge = ctk.CTkFrame(
                row, 
                width=BADGE_WIDTH, 
                height=BADGE_HEIGHT, 
                fg_color="transparent", 
                border_width=2, 
                border_color=b_color, 
                corner_radius=6
            )
            badge.pack(side="left", padx=(15, 5), pady=12)
            badge.pack_propagate(False)

            ctk.CTkLabel(
                badge, 
                text=bank["name"], 
                font=("Roboto", 10, "bold"), 
                text_color=b_color
            ).pack(expand=True, fill="both")

            info_col = ctk.CTkFrame(row, fg_color="transparent")
            info_col.pack(side="left", padx=10, fill="y", pady=5)
            ctk.CTkLabel(info_col, text=name, font=("Roboto", 13, "bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info_col, text=iban, font=("Courier New", 11), text_color=self.app.theme["text_dim"], anchor="w").pack(fill="x")

            btn_del = ctk.CTkButton(
                row, text="🗑", width=30, height=30, 
                fg_color="transparent", 
                text_color=self.app.theme["danger"],
                hover_color="#331a1a",
                command=lambda i=iban: self.delete_specific_beneficiary(i)
            )
            btn_del.pack(side="right", padx=15)

        if not has_results:
            self.app.add_label(self.table_frame, "Niciun rezultat găsit.", type="dim", pady=20)


 
    def delete_selected_beneficiary(self):
        if not self.selected_beneficiary_iban: return

        if messagebox.askyesno("Confirmare", f"Sigur vrei să ștergi beneficiarul cu IBAN-ul {self.selected_beneficiary_iban}?"):
            sql = "DELETE FROM beneficiari WHERE id_client = %s AND iban_beneficiar = %s"

            self.app.ruleaza_query(sql, (self.client_id, self.selected_beneficiary_iban), fetch=False)
            messagebox.showinfo("Succes", "Beneficiarul a fost eliminat cu succes din agenda ta!")

            self.selected_row_frame = None 
            self.selected_beneficiary_iban = None
            self.delete_btn.configure(state="disabled")

            self.refresh_beneficiary_table()



    def delete_specific_beneficiary(self, iban):
        if messagebox.askyesno("Confirmare", f"Sigur vrei să ștergi beneficiarul cu IBAN-ul {iban}?"):
            sql = "DELETE FROM beneficiari WHERE id_client = %s AND iban_beneficiar = %s"
            self.app.ruleaza_query(sql, (self.client_id, iban), fetch=False)
            messagebox.showinfo("Succes", "Beneficiar șters!")
            self.refresh_beneficiary_table()




    def add_beneficiary_form(self):
        self.curata_content()
        self.app.add_label(self.content, "ADĂUGARE BENEFICIAR", type="h2", pady=10)

        form_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        form_frame.pack(expand=True)

        self.app.add_label(form_frame, "Nume Complet:", type="form")
        name_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text = "Ion Popescu", **self.app.styles["input"])
        name_entry.pack(pady=(0, 15))

        self.app.add_label(form_frame, "IBAN Beneficiar:", type="form")
        iban_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="RO00 BTRL 0000 0000 0000 0000", **self.app.styles["input"])
        iban_entry.pack(pady=(0, 25))

        btn_save = ctk.CTkButton(
            form_frame, text="SALVEAZĂ", 
            width=200, height=35,
            command=lambda: self._save_beneficiary(name_entry.get(), iban_entry.get()),
            **self.app.styles["btn_confirm"]
        )
        btn_save.pack(pady=10)

        ctk.CTkButton(form_frame, text="Anulează", command=self.display_beneficiaries, **self.app.styles["btn_back"]).pack()

    def _save_beneficiary(self, name, iban):
        name = name.strip().title()
        iban = iban.replace(" ", "").strip().upper()

        if not name or not iban:
            messagebox.showwarning("Eroare", "Toate câmpurile sunt obligatorii!")
            return
        
        check_sql = "SELECT id_beneficiar FROM beneficiari WHERE id_client = %s AND iban_beneficiar = %s"
        exista = self.app.ruleaza_query(check_sql, (self.client_id, iban))
        
        if exista:
            messagebox.showwarning("Atenție", "Acest beneficiar există deja în agenda ta!")
            return
        
        if len(iban) != 24:
            messagebox.showerror("Eroare", "IBAN-ul trebuie să aibă exact 24 de caractere!")
            return
        
        sql = "INSERT INTO beneficiari (id_client, nume_beneficiar, iban_beneficiar) VALUES (%s, %s, %s)"
        
        self.app.ruleaza_query(sql, (self.client_id, name, iban), False)
        messagebox.showinfo("Succes", "Beneficiar adăugat!")
        self.display_beneficiaries()