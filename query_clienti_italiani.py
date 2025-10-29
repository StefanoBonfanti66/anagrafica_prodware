import pandas as pd

try:
    # Imposta pandas per mostrare tutte le righe
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    df = pd.read_csv('anagrafica_pulita.csv')

    # Filtra i clienti italiani (considerando 'IT' e i campi vuoti)
    is_italian = df['Nazione'].fillna('IT').str.strip().str.upper() == 'IT'
    clienti_italiani = df[is_italian]

    # Seleziona le colonne richieste
    colonne_richieste = [
        'Ragione Sociale', 'Indirizzo', 'CAP', 'Città', 
        'Provincia', 'Partita IVA', 'Cod. Fiscale'
    ]
    
    # Filtra le colonne effettivamente presenti nel DataFrame per evitare errori
    colonne_da_mostrare = [col for col in colonne_richieste if col in clienti_italiani.columns]
    
    if not colonne_da_mostrare:
         print("Errore: Nessuna delle colonne richieste è stata trovata.")
    else:
        risultato = clienti_italiani[colonne_da_mostrare]
        print("Elenco completo dei clienti italiani:")
        print(risultato.to_string())

except FileNotFoundError:
    print("Errore: File 'anagrafica_pulita.csv' non trovato.")
except Exception as e:
    print(f"Si è verificato un errore: {e}")
