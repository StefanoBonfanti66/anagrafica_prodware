import pandas as pd

try:
    df = pd.read_csv('anagrafica_pulita.csv')
    if 'Nazione' in df.columns:
        # Filtra per i clienti in Germania (DE)
        clienti_germania = df[df['Nazione'].str.contains('DE', na=False)]
        numero_clienti = len(clienti_germania)
        print(f"Risultato: {numero_clienti}")
    else:
        print("Errore: Colonna 'Nazione' non trovata.")
except FileNotFoundError:
    print("Errore: File 'anagrafica_pulita.csv' non trovato.")
except Exception as e:
    print(f"Errore: {e}")
