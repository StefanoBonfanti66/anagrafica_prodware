import pandas as pd

try:
    df = pd.read_csv('anagrafica_pulita.csv')
    if 'Nazione' in df.columns:
        # Riempi i valori NaN (vuoti) con un testo segnaposto per contarli
        counts = df['Nazione'].fillna('NON SPECIFICATO').value_counts()
        print("Conteggio dei clienti per nazione:")
        print(counts.to_string())
    else:
        print("Errore: Colonna 'Nazione' non trovata.")
except Exception as e:
    print(f"Si è verificato un errore: {e}")
