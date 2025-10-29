import pandas as pd

CUSTOMER_CODE = '00000508'

try:
    df = pd.read_csv('anagrafica_pulita.csv')
    df['Codice'] = df['Codice'].astype(str)

    customer_record = df[df['Codice'] == CUSTOMER_CODE]

    if not customer_record.empty:
        print(f"Trovato record per il cliente con codice {CUSTOMER_CODE}:")
        print(customer_record.iloc[0].to_string())
    else:
        print(f"ATTENZIONE: Nessun cliente trovato con il codice {CUSTOMER_CODE} nel file 'anagrafica_pulita.csv'.")

except FileNotFoundError:
    print("Errore: File 'anagrafica_pulita.csv' non trovato.")
except Exception as e:
    print(f"Si è verificato un errore: {e}")
