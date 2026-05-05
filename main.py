import customtkinter as ctk
import mysql.connector
import json
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class User:
    def __init__(self, app):
        self.app = app
        self.app.db_config = self.app.all_configs['user']
        self.app.curata_pagina()

        self.titlu = ctk.CTkLabel(self.app, text="CLIENT INTERFACE", font=("Roboto", 26, "bold"))
        self.titlu.pack(pady=50)

        self.btn_back = ctk.CTkButton(self.app, text="← Meniu Principal", command=self.app.afiseaza_dashboard)
        self.btn_back.pack(pady=10)

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
            command=lambda: User(self)
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