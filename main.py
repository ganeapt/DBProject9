import customtkinter as ctk
import mysql.connector
import json
from tkinter import messagebox

from user import User
from admin import Admin

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


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
        
        ctk.CTkLabel(self, text="LOGIN CLIENT", font=("Roboto", 24, "bold")).pack(pady=40)
        
        ctk.CTkLabel(self, text="Introdu adresa de email pentru acces:").pack(pady=5)
        self.email_entry = ctk.CTkEntry(self, width=300, placeholder_text="exemplu@email.com")
        self.email_entry.pack(pady=10)

        ctk.CTkButton(self, text="Acces Cont", command=self.verifica_login_client).pack(pady=20)
        
        ctk.CTkButton(self, text="← Înapoi", command=self.afiseaza_dashboard, fg_color="transparent").pack(pady=10)

    def verifica_login_client(self):
        email_introdus = self.email_entry.get().strip()
        
        if not email_introdus:
            messagebox.showwarning("Atenție", "Te rugăm să introduci un email!")
            return

        self.db_config = self.all_configs['admin']
        rezultat = self.ruleaza_query("SELECT id_client FROM clienti WHERE email = %s", (email_introdus,))

        if rezultat:
            id_gasit = rezultat[0][0]
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
            raise e
        finally:
            if connection and connection.is_connected(): 
                connection.close()

if __name__ == "__main__":
    app = AppBancara()
    app.mainloop()