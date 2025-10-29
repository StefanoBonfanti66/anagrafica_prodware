
import csv
import sys

if len(sys.argv) < 2:
    print("Usage: python find_customer_by_code.py <customer_code>")
    sys.exit(1)

customer_code_to_find = sys.argv[1]

with open('anagrafica_pulita.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    reader = csv.reader(infile)
    header = next(reader)  # Skip header
    found = False
    for row in reader:
        if customer_code_to_find in row[0]:
            print(f"Trovato nel file: {infile.name}")
            print(dict(zip(header, row)))
            found = True
    
    if not found:
        print(f"Nessun cliente trovato con codice contenente '{customer_code_to_find}'.")
