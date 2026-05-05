import customtkinter as ctk
import mysql.connector
import json
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppBancara(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Bancar Proiect 9")
        self.geometry("800x500")

        with open('config.json', 'r') as f:
            self.db_config = json.load(f)

        self.label = ctk.CTkLabel(self, text="Digital Banking System", font=("Roboto", 20, "bold"))
        self.label.pack(pady=20)

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