import pandas as pd

CUSTOMER_CODE = '00015282'

try:
    df = pd.read_csv('anagrafica_pulita.csv')

    # Converte la colonna 'Codice' in stringa per la corrispondenza
    df['Codice'] = df['Codice'].astype(str)

    customer_record = df[df['Codice'] == CUSTOMER_CODE]

    if not customer_record.empty:
        print(f"Dettagli per il cliente con codice {CUSTOMER_CODE}:")
        # Stampa i dati trasposti per una migliore leggibilità
        print(customer_record.iloc[0].to_string())
    else:
        print(f"Nessun cliente trovato con il codice {CUSTOMER_CODE}.")

except FileNotFoundError:
    print("Errore: File 'anagrafica_pulita.csv' non trovato.")
except Exception as e:
    print(f"Si è verificato un errore: {e}")
