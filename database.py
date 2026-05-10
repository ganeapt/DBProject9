import mysql.connector
from tkinter import messagebox

class DatabaseManager:
    def __init__(self, config):
        self.config = config

    def ruleaza_query(self, sql, params=None, fetch=True):
        connection = None
        try:
            connection = mysql.connector.connect(**self.config)
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