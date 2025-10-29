import pandas as pd

try:
    df = pd.read_csv('anagrafica_pulita.csv')
    output_filename = 'clienti_germania.txt'

    if 'Nazione' in df.columns:
        is_german = df['Nazione'].str.contains('DE', na=False)
        clienti_germania = df[is_german]

        colonne = ['Codice', 'Ragione Sociale']
        risultato = clienti_germania[colonne].sort_values(by='Ragione Sociale')

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("Elenco dei clienti in Germania:\n\n")
            f.write(risultato.to_string(index=False))
        
        print(f"File '{output_filename}' creato con successo.")
        print(f"Trovati {len(risultato)} clienti.")

    else:
        print("Errore: Colonna 'Nazione' non trovata.")

except FileNotFoundError:
    print("Errore: File 'anagrafica_pulita.csv' non trovato.")
except Exception as e:
    print(f"Si è verificato un errore: {e}")
