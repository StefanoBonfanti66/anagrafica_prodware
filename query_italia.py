import pandas as pd

try:
    df = pd.read_csv('anagrafica_pulita.csv')
    if 'Nazione' in df.columns:
        clienti_italia = df[df['Nazione'].str.strip().str.upper() == 'IT']
        numero_clienti_italia = len(clienti_italia)
        print(f"Risultato: {numero_clienti_italia}")
    else:
        print("Errore: Colonna 'Nazione' non trovata.")
except FileNotFoundError:
    print("Errore: File 'anagrafica_pulita.csv' non trovato.")
except Exception as e:
    print(f"Errore: {e}")
