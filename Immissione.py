"""Questo programma permette di inserire i metadati di un'immagine nella tabella metadati e sposta il file nella cartella immagini"""

import sqlite3
import os

# Connessione al database
conn = sqlite3.connect('metadati.db')
c = conn.cursor()
campi_db = [row[1] for row in c.execute("PRAGMA table_info(metadati)")]

def inserisci_metadati(log : dict) -> None:
    """Inserisce i metadati di un'immagine nella tabella metadati e sposta il file nella cartella immagini"""
    # Controllo che i campi siano presenti nel dizionario
    for campo in campi_db:
        if campo not in log:
            raise ValueError(f"Il campo {campo} non è presente nel dizionario")
    
    # Inserimento dei metadati
    c.execute("INSERT INTO metadati (" + ', '.join(log.keys()) + ") VALUES (" + ', '.join(['?' for _ in log.keys()]) + ")", list(log.values()))
    conn.commit()
    
# Spostamento del file
def sposta_file(nome_file : str) -> None:
    """Sposta il file nella cartella immagini"""
    if not os.path.exists('immagini'):
        os.mkdir('immagini')
    os.rename(nome_file, os.path.join('immagini', nome_file))
    
if __name__ == '__main__':
    print ("Si presume che il file immagine sia presente nella cartella corrente")
    # Inserimento dei metadati
    log = {}
    for campo in campi_db:
        valore = input(f"Inserire il valore per il campo {campo}: ")
        log[campo] = valore
    inserisci_metadati(log)
    sposta_file(log['nome_file'])
    print("Operazione completata con successo")
    conn.close()