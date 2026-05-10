import customtkinter as ctk
import mysql.connector
import json
from tkinter import messagebox

from user import User
from admin import Admin
from database import DatabaseManager
from transactions import TransactionService
from theme import THEME, STYLES

ctk.set_appearance_mode("dark")

class AppBancara(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.theme = THEME
        self.styles = STYLES
        self.title("Sistem Bancar Proiect 9")
        self.geometry("800x500")
        self.configure(fg_color=self.theme["bg_dark"])

        with open('config.json', 'r') as f:
            self.all_configs = json.load(f)

        self.db = DatabaseManager(self.all_configs['admin'])

        self.afiseaza_dashboard()

    def curata_pagina(self):
        """Șterge toate elementele vizuale de pe fereastră."""
        for widget in self.winfo_children():
            widget.destroy()

    def add_label(self, master, text, type="h1", pady=10):
        styles = {
            "h1": {"font": ("Roboto", 24, "bold"), "text_color": self.theme["text_main"]},
            "h2": {"font": ("Roboto", 22, "bold"), "text_color": self.theme["text_main"]},
            "tech": {"font": ("Courier New", 12, "bold"), "text_color": self.theme["text_dim"]},
            "form": {"font": ("Roboto", 13), "text_color": self.theme["text_main"]},
            "dim": {"font": ("Roboto", 14), "text_color": self.theme["text_dim"]}
        }
        style = styles.get(type, styles["h1"])
        
        label = ctk.CTkLabel(master, text=text, **style)
        label.pack(pady=pady)
        return label

    def afiseaza_dashboard(self):
        """Afișează meniul principal de selecție (User/Admin)."""
        self.curata_pagina()

        self.label = ctk.CTkLabel(self, text="Digital Banking System", font=("Roboto", 26, "bold"), text_color=self.theme["text_main"])
        self.label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(expand=True)

        # Buton USER
        self.btn_user = ctk.CTkButton(
            self.button_frame,
            text="USER", 
            width=200, height=200, 
            font=("Roboto", 20),
            command=self.selectie_utilizator,
            **self.styles["card"]
        )
        self.btn_user.pack(side="left", padx=20)

        # Buton ADMIN
        self.btn_admin = ctk.CTkButton(
            self.button_frame, 
            text="ADMIN", 
            width=200, height=200, 
            font=("Roboto", 20),
            command=lambda: Admin(self),
            **self.styles["card"]
        )
        self.btn_admin.pack(side="left", padx=20)

    def selectie_utilizator(self):
        self.curata_pagina()
        
        ctk.CTkLabel(self, text="LOGIN CLIENT", font=("Roboto", 24, "bold"), text_color=self.theme["text_main"]).pack(pady=40)
        
        ctk.CTkLabel(self, text="Introdu adresa de email pentru acces:", text_color=self.theme["text_dim"]).pack(pady=5)
        self.email_entry = ctk.CTkEntry(self, width=300, placeholder_text="exemplu@email.com", fg_color=self.theme["card_inner"], border_color=self.theme["btn_accent"], text_color=self.theme["text_main"])
        self.email_entry.pack(pady=10)

        ctk.CTkButton(self, text="Acces Cont", fg_color=self.theme["btn_accent"], hover_color=self.theme["btn_hover"], command=self.verifica_login_client).pack(pady=20)
        
        ctk.CTkButton(self, text="← Înapoi", fg_color="transparent", text_color=self.theme["text_dim"], hover_color=self.theme["btn_hover"], command=self.afiseaza_dashboard).pack(pady=10)

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
        return self.db.ruleaza_query(sql, params, fetch)

if __name__ == "__main__":
    app = AppBancara()
    app.mainloop()