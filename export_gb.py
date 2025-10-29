import pandas as pd

try:
    df = pd.read_csv('anagrafica_pulita.csv')
    output_filename = 'clienti_gran_bretagna.txt'

    if 'Nazione' in df.columns:
        is_gb = df['Nazione'].str.contains('GB', na=False)
        is_attivo = df['Condizione'] == 'N - Attivi'
        clienti_gb = df[is_gb & is_attivo]

        colonne = ['Codice', 'Ragione Sociale']
        risultato = clienti_gb[colonne].sort_values(by='Ragione Sociale')

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("Elenco dei clienti in Gran Bretagna (GB):\n\n")
            f.write(risultato.to_string(index=False))
        
        print(f"File '{output_filename}' creato con successo.")
        print(f"Trovati {len(risultato)} clienti.")

    else:
        print("Errore: Colonna 'Nazione' non trovata.")

except FileNotFoundError:
    print("Errore: File 'anagrafica_pulita.csv' non trovato.")
except Exception as e:
    print(f"Si è verificato un errore: {e}")
