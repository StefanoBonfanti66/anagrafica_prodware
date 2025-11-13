import pandas as pd
import os
import csv

def process_excel_file(file_path):
    """
    Legge un file Excel, analizza i dati dei clienti da ogni foglio
    e restituisce un singolo DataFrame di pandas.
    """
    try:
        excel_file = pd.ExcelFile(file_path)
    except FileNotFoundError:
        print(f"Errore: Il file '{file_path}' non è stato trovato.")
        return pd.DataFrame()

    all_customers = []
    print(f"Elaborazione del file: {file_path}")

    for sheet_name in excel_file.sheet_names:
        print(f"Elaborazione del foglio: {sheet_name}")
        df = excel_file.parse(sheet_name, header=None)
        customer_data = {}
        
        for index, row in df.iterrows():
            # Convert row to list of strings, handling potential float values
            row = [str(item) if pd.notna(item) else '' for item in row]

            if not any(row): continue

            if row[1].strip() == 'Codice': # Corrected index from 0 to 1
                # The actual customer code is in row[5]
                if len(row) > 5 and row[5]: # Check if row[5] exists and is not empty
                    if customer_data:
                        all_customers.append(customer_data)
                    customer_data = {
                        'Codice': row[5],
                        'Ragione Sociale': row[12] if len(row) > 12 else '', # Corrected from 11 to 12
                        'Indirizzo': '', 'Partita IVA': '', 'CAP': '', 'Cod. Fiscale': '',
                        'Città': '', 'Provincia': '', 'Nazione': '', 'Telefono 1': '',
                        'Tipo Azienda': '', 'Telefono 2': '', 'Telefax': '', 'Pagamento': '',
                        'Banca': '', 'Agente': '', 'Condizione': ''
                    }
                else:
                    print(f"Avviso: 'Codice' trovato in row[1] ma row[5] è vuoto o fuori limiti: {row}")
                    customer_data = {} # Reset customer_data if no valid code found
            
            if not customer_data: continue

            label_col_A = row[1].strip() if len(row) > 1 else ''
            label_col_S = row[19].strip() if len(row) > 19 else ''

            if label_col_A == 'Indirizzo' and len(row) > 8: customer_data['Indirizzo'] = row[8]
            if label_col_A == 'CAP' and len(row) > 8: customer_data['CAP'] = row[8]
            if label_col_A == 'Città' and len(row) > 8: customer_data['Città'] = row[8]
            if label_col_A == 'Provincia' and len(row) > 8: customer_data['Provincia'] = row[8]
            if label_col_A == 'Nazione' and len(row) > 10: customer_data['Nazione'] = f"{row[8]} ({row[10]})"
            if label_col_A == 'Telefono 1' and len(row) > 8: customer_data['Telefono 1'] = row[8]
            if label_col_A == 'Telefono 2' and len(row) > 8: customer_data['Telefono 2'] = row[8]
            if label_col_A == 'Telefax' and len(row) > 8: customer_data['Telefax'] = row[8]
            if label_col_A == 'Pagamento' and len(row) > 10: customer_data['Pagamento'] = f"{row[8]} - {row[10]}"
            if label_col_A == 'Banca Pag.to' and len(row) > 12: customer_data['Banca'] = row[12]
            if label_col_A == 'Agente' and len(row) > 8: customer_data['Agente'] = row[8]
            if label_col_A == 'Condizione' and len(row) > 10: customer_data['Condizione'] = f"{row[8]} - {row[10]}"

            if label_col_S == 'Partita IVA' and len(row) > 25: customer_data['Partita IVA'] = row[25]
            if label_col_S == 'Cod. Fiscale' and len(row) > 25: customer_data['Cod. Fiscale'] = row[25]
            if label_col_S == 'Tipo azienda' and len(row) > 31: customer_data['Tipo Azienda'] = f"{row[25]} - {row[31]}"
            if label_col_S == 'Cod. Fiscale' and len(row) > 26: customer_data['Cod. Fiscale'] = row[26]
            if label_col_S == 'Tipo azienda' and len(row) > 32: customer_data['Tipo Azienda'] = f"{row[26]} - {row[32]}"

        if customer_data:
            all_customers.append(customer_data)

    if not all_customers:
        print("Nessun dato cliente trovato nel file.")
        return pd.DataFrame()

    df = pd.DataFrame(all_customers)
    df = df.drop_duplicates(subset=['Codice'], keep='last')
    return df

def main():
    """
    Funzione principale per eseguire lo script.
    """
    print("Questo script serve per elaborare il file Excel dell'anagrafica clienti.")
    
    input_filename = None
    if os.path.exists('sanagr01.xlsx'):
        input_filename = 'sanagr01.xlsx'
    elif os.path.exists('sanagr01.xls'):
        input_filename = 'sanagr01.xls'
    
    if not input_filename:
        print("Errore: Nessun file 'sanagr01.xlsx' o 'sanagr01.xls' trovato.")
        return

    df_completo = process_excel_file(input_filename)
    
    if not df_completo.empty:
        print(f"Elaborazione completata. Trovati {len(df_completo)} clienti in totale.")
        print("Prime 5 righe del DataFrame completo:")
        print(df_completo.head().to_string())
        
        output_filename = 'anagrafica_pulita.csv'
        df_completo.to_csv(output_filename, index=False, quoting=csv.QUOTE_ALL)
        print(f"\nDati salvati in '{output_filename}'")

if __name__ == '__main__':
    main()
