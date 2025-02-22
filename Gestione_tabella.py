"""Questo file contiene i comandi per la creazione della tabella per i metadati, eseguirlo se si desidera cambiare la struttura della tabella"""

import sqlite3

#Questo è l'elenco dei campi che verranno inseriti nella tabella, è possibile aggiungere campi ed essi verranno inseriti automaticamente modificando la tabella già esistente
campi = [   'numero_IGM',
            'nome_file',
            'data',
            'strisciata',
            'numero_fotogramma',
            'latitudine',
            'longitudine',
            'altitudine', 
        ]

conn = sqlite3.connect('metadati.db')
c = conn.cursor()

# Verifica se la tabella esiste già
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metadati'")
table_exists = c.fetchone()

if not table_exists:
    #Creazione della tabella
    c.execute('''
              CREATE TABLE metadati (id INTEGER PRIMARY KEY AUTOINCREMENT, ''' + ', '.join([campo + ' TEXT' for campo in campi]) + ''')
              ''')

else:
    #Aggiunta di campi mancanti
    c.execute("PRAGMA table_info(metadati)")
    campi_esistenti = [row[1] for row in c.fetchall()]

    for campo in campi:
        if campo not in campi_esistenti:
            c.execute("ALTER TABLE metadati ADD COLUMN " + campo + " TEXT")

conn.commit()
conn.close()