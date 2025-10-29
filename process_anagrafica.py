
'''
Script per elaborare i file CSV dell'anagrafica clienti, 
convertendoli da un formato report a una tabella strutturata.
'''
import pandas as pd
import glob
import csv

def process_customer_files(file_pattern):
    """
    Legge tutti i file CSV che corrispondono al pattern, analizza i dati dei clienti,
    e restituisce un singolo DataFrame di pandas.
    """
    all_customers = []
    files = glob.glob(file_pattern)
    output_file_name = 'anagrafica_pulita.csv'
    if output_file_name in files:
        files.remove(output_file_name)

    if not files:
        print(f"Attenzione: Nessun file CSV sorgente trovato con il pattern '{file_pattern}'")
        return pd.DataFrame()

    for file in files:
        print(f"Elaborazione del file: {file}")
        customer_data = {}
        with open(file, 'r', encoding='utf-8', errors='ignore') as infile:
            reader = csv.reader(infile, delimiter=';')
            for row in reader:
                if not any(row): continue

                # La label "Codice" è nella prima colonna (indice 0)
                if len(row) > 5 and row[0].strip() == 'Codice' and row[4]:
                    if customer_data:
                        all_customers.append(customer_data)
                    customer_data = {
                        'Codice': row[4],
                        'Ragione Sociale': row[11] if len(row) > 11 else '',
                        'Indirizzo': '', 'Partita IVA': '', 'CAP': '', 'Cod. Fiscale': '',
                        'Città': '', 'Provincia': '', 'Nazione': '', 'Telefono 1': '',
                        'Tipo Azienda': '', 'Telefono 2': '', 'Telefax': '', 'Pagamento': '',
                        'Banca': '', 'Agente': '', 'Condizione': ''
                    }

                if not customer_data: continue

                label_col_A = row[0].strip() if len(row) > 0 else ''
                label_col_S = row[18].strip() if len(row) > 18 else ''

                if label_col_A == 'Indirizzo' and len(row) > 7: customer_data['Indirizzo'] = row[7]
                if label_col_A == 'CAP' and len(row) > 7: customer_data['CAP'] = row[7]
                if label_col_A == 'Città' and len(row) > 7: customer_data['Città'] = row[7]
                if label_col_A == 'Provincia' and len(row) > 7: customer_data['Provincia'] = row[7]
                if label_col_A == 'Nazione' and len(row) > 9: customer_data['Nazione'] = f"{row[7]} ({row[9]})"
                if label_col_A == 'Telefono 1' and len(row) > 7: customer_data['Telefono 1'] = row[7]
                if label_col_A == 'Telefono 2' and len(row) > 7: customer_data['Telefono 2'] = row[7]
                if label_col_A == 'Telefax' and len(row) > 7: customer_data['Telefax'] = row[7]
                if label_col_A == 'Pagamento' and len(row) > 9: customer_data['Pagamento'] = f"{row[7]} - {row[9]}"
                if label_col_A == 'Banca Pag.to' and len(row) > 11: customer_data['Banca'] = row[11]
                if label_col_A == 'Agente' and len(row) > 7: customer_data['Agente'] = row[7]
                if label_col_A == 'Condizione' and len(row) > 9: customer_data['Condizione'] = f"{row[7]} - {row[9]}"

                if label_col_S == 'Partita IVA' and len(row) > 24: customer_data['Partita IVA'] = row[24]
                if label_col_S == 'Cod. Fiscale' and len(row) > 24: customer_data['Cod. Fiscale'] = row[24]
                if label_col_S == 'Tipo azienda' and len(row) > 30: customer_data['Tipo Azienda'] = f"{row[24]} - {row[30]}"
                if label_col_S == 'Cod. Fiscale' and len(row) > 25: customer_data['Cod. Fiscale'] = row[25]
                if label_col_S == 'Tipo azienda' and len(row) > 31: customer_data['Tipo Azienda'] = f"{row[25]} - {row[31]}"

            if customer_data:
                all_customers.append(customer_data)

    if not all_customers:
        print("Nessun dato cliente trovato nei file.")
        return pd.DataFrame()

    df = pd.DataFrame(all_customers)
    df = df.drop_duplicates(subset=['Codice'], keep='last')
    return df

def main():
    """
    Funzione principale per eseguire lo script.
    """
    print("Questo script serve per elaborare i file CSV dell'anagrafica.")
    print("Per eseguirlo, assicurati di aver prima esportato i fogli Excel in file CSV.")
    
    # Esempio di come usare la funzione
    # 1. Prova con un file di esempio CSV (da creare da esempio_anagrafica.xlsx)
    # file_pattern_esempio = 'esempio_anagrafica.csv'
    # print(f"\n--- Prova con file di esempio '{file_pattern_esempio}' ---")
    # df_esempio = process_customer_files(file_pattern_esempio)
    # if not df_esempio.empty:
    #     print("Dati estratti dal file di esempio:")
    #     print(df_esempio.to_string())

    # 2. Esecuzione sui file completi
    file_pattern_completo = 'anagrafica_*.csv'
    print(f"\n--- Elaborazione dei file completi '{file_pattern_completo}' ---")
    df_completo = process_customer_files(file_pattern_completo)
    
    if not df_completo.empty:
        print(f"Elaborazione completata. Trovati {len(df_completo)} clienti in totale.")
        print("Prime 5 righe del DataFrame completo:")
        print(df_completo.head().to_string())
        
        # Salva il risultato in un unico file CSV pulito
        output_filename = 'anagrafica_pulita.csv'
        df_completo.to_csv(output_filename, index=False, quoting=csv.QUOTE_ALL)
        print(f"\nDati salvati in '{output_filename}'")

if __name__ == '__main__':
    main()
