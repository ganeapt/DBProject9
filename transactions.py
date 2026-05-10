from tkinter import messagebox

class TransactionService:
    def __init__(self, db_manager):
        self.db = db_manager

    def executa_transfer(self, source_iban, target_iban, amount, details):
        clean_target = target_iban.strip()
        clean_amount = amount.strip()
        clean_details = details.strip() or "Banking Transfer"

        if not clean_target or not clean_amount:
            messagebox.showwarning("Câmpuri Goale", "Introdu IBAN-ul și Suma!")
            return False

        sql = "CALL EfectueazaTransfer(%s, %s, %s, %s)"
        params = (source_iban, clean_target, clean_amount, clean_details)

        try:
            self.db.ruleaza_query(sql, params, fetch=False)
            messagebox.showinfo("Succes", f"Transfer de {clean_amount} realizat cu succes!")
            return True
        except Exception as e:
            messagebox.showerror("Eroare Transfer", str(e))
            return False