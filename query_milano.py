import pandas as pd

try:
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    df = pd.read_csv('anagrafica_pulita.csv')

    if 'Provincia' in df.columns:
        is_milano = df['Provincia'].str.strip().str.upper() == 'MI'
        clienti_milano = df[is_milano.fillna(False)]

        colonne_richieste = [
            'Ragione Sociale', 'Indirizzo', 'CAP', 'Città', 
            'Provincia', 'Partita IVA', 'Cod. Fiscale'
        ]
        colonne_da_mostrare = [col for col in colonne_richieste if col in clienti_milano.columns]

        if not colonne_da_mostrare:
            print("Errore: Nessuna delle colonne richieste è stata trovata.")
        elif clienti_milano.empty:
            print("Nessun cliente trovato per la provincia di Milano (MI).")
        else:
            print("Elenco dei clienti di Milano e provincia:")
            print(clienti_milano[colonne_da_mostrare].to_string())
    else:
        print("Errore: Colonna 'Provincia' non trovata.")

except FileNotFoundError:
    print("Errore: File 'anagrafica_pulita.csv' non trovato.")
except Exception as e:
    print(f"Si è verificato un errore: {e}")
