"""Una semplice interfaccia grafica per l'immissione dei file e dei metadati"""
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import datetime
import os
from Immissione import inserisci_metadati, sposta_file, campi_db, conn

campi_maschera : dict['str', 'tk.Entry']= {}
campi_automatici = ['nome_file', 'id']

def invia():
    #controllo che la data sia nel formato corretto
    try:
        datetime.datetime.strptime(campi_maschera['data'].get(), '%d/%m/%Y')
    except ValueError:
        tkinter.messagebox.showerror("Errore", "La data non è nel formato GG/MM/AAAA.")
        return
    file = tkinter.filedialog.askopenfilename()
    sposta_file(file)
    # Inserimento dei metadati
    log = dict((campo, campi_maschera[campo].get()) for campo in [campo for campo in campi_db if campo not in campi_automatici])
    log['nome_file'] = os.path.basename(file)
    try:
        inserisci_metadati(log)
    except ValueError as e:
        tkinter.messagebox.showerror("Errore", str(e))
        return
    
def chiudi():
    conn.close()
    finestra.destroy()

#Struttura interfaccia grafica
finestra = tk.Tk()
finestra.title("Immissione metadati")
for i, campo in enumerate([campo for campo in campi_db if campo not in campi_automatici]):
    tk.Label(finestra, text=campo).grid(row=i, column=0)
    campi_maschera[campo] = tk.Entry(finestra)
    campi_maschera[campo].grid(row=i, column=1)
invio = tk.Button(finestra, text="Invia", command=invia)
invio.grid(row=len(campi_maschera) + 1, column=1)

finestra.mainloop()