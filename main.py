import customtkinter as ctk
import mysql.connector
import json
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class User:
    def __init__(self, app, client_id):
        self.app = app
        self.client_id = client_id
        self.app.db_config = self.app.all_configs['user']
        self.app.curata_pagina()

        self.sidebar = ctk.CTkFrame(self.app, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        # 2. Cream Frame-ul de conținut (dreapta)
        self.content = ctk.CTkFrame(self.app, fg_color="transparent")
        self.content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        # 3. Adăugăm butoanele în Sidebar
        ctk.CTkLabel(self.sidebar, text="MENU CLIENT", font=("Roboto", 20, "bold")).pack(pady=20, padx=10)
        
        ctk.CTkButton(self.sidebar, text="Situație Conturi", command=self.afiseaza_situatie_conturi).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="Transfer Nou", command=lambda: print("Transfer")).pack(pady=10, padx=10)
        
        # Buton de Logout (Back to Launcher)
        ctk.CTkButton(self.sidebar, text="Log Out", fg_color="darkred", command=self.app.afiseaza_dashboard).pack(side="bottom", pady=20)

        # Afișăm ceva implicit la început
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

class Admin:
    def __init__(self, app):
        self.app = app
        self.app.db_config = self.app.all_configs['admin']
        self.app.curata_pagina()

        self.titlu = ctk.CTkLabel(self.app, text="ADMIN PANEL", font=("Roboto", 26, "bold"))
        self.titlu.pack(pady=50)

        self.btn_back = ctk.CTkButton(self.app, text="← Meniu Principal", command=self.app.afiseaza_dashboard)
        self.btn_back.pack(pady=10)


class AppBancara(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Bancar Proiect 9")
        self.geometry("800x500")

        with open('config.json', 'r') as f:
            self.all_configs = json.load(f)

        self.afiseaza_dashboard()

    def curata_pagina(self):
        """Șterge toate elementele vizuale de pe fereastră."""
        for widget in self.winfo_children():
            widget.destroy()

    def afiseaza_dashboard(self):
        """Afișează meniul principal de selecție (User/Admin)."""
        self.curata_pagina()

        self.label = ctk.CTkLabel(self, text="Digital Banking System", font=("Roboto", 26, "bold"))
        self.label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(expand=True)

        # Buton USER
        self.btn_user = ctk.CTkButton(
            self.button_frame,
            text="USER", 
            width=200, height=200, 
            font=("Roboto", 20),
            command=self.selectie_utilizator
        )
        self.btn_user.pack(side="left", padx=20)

        # Buton ADMIN
        self.btn_admin = ctk.CTkButton(
            self.button_frame, 
            text="ADMIN", 
            width=200, height=200, 
            font=("Roboto", 20),
            command=lambda: Admin(self)
        )
        self.btn_admin.pack(side="left", padx=20)

    def selectie_utilizator(self):
        self.curata_pagina()
        
        # Titlu
        ctk.CTkLabel(self, text="LOGIN CLIENT", font=("Roboto", 24, "bold")).pack(pady=40)
        
        # Input pentru email
        ctk.CTkLabel(self, text="Introdu adresa de email pentru acces:").pack(pady=5)
        self.email_entry = ctk.CTkEntry(self, width=300, placeholder_text="exemplu@email.com")
        self.email_entry.pack(pady=10)

        # Buton de login
        ctk.CTkButton(self, text="Acces Cont", command=self.verifica_login_client).pack(pady=20)
        
        ctk.CTkButton(self, text="← Înapoi", command=self.afiseaza_dashboard, fg_color="transparent").pack(pady=10)

    def verifica_login_client(self):
        email_introdus = self.email_entry.get().strip()
        
        if not email_introdus:
            messagebox.showwarning("Atenție", "Te rugăm să introduci un email!")
            return

        # Folosim admin pentru a verifica existenta email-ului (el are SELECT pe clienti)
        self.db_config = self.all_configs['admin']
        rezultat = self.ruleaza_query("SELECT id_client FROM clienti WHERE email = %s", (email_introdus,))

        if rezultat:
            id_gasit = rezultat[0][0]
            # Succes! Trecem la clasa User cu ID-ul găsit
            User(self, id_gasit)
        else:
            messagebox.showerror("Eroare", "Acest email nu este înregistrat în sistemul nostru.")

    def ruleaza_query(self, sql, params=None, fetch=True):
        """Logica de conectare la baza de date."""
        connection = None
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute(sql, params or ())
            rezultat = cursor.fetchall() if fetch else None

            if not fetch:
                connection.commit()
            return rezultat
        
        except Exception as e:
            messagebox.showerror("Eroare Baza de Date", str(e))
            return None
        finally:
            if connection and connection.is_connected(): 
                connection.close()

if __name__ == "__main__":
    app = AppBancara()
    app.mainloop()