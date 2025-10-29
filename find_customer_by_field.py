
import csv
import sys

if len(sys.argv) < 3:
    print("Usage: python find_customer_by_field.py <field_name> <value>")
    sys.exit(1)

field_to_search = sys.argv[1]
value_to_find = sys.argv[2]

with open('anagrafica_pulita.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    reader = csv.DictReader(infile)
    found = False
    for row in reader:
        if value_to_find in row[field_to_search]:
            print(row)
            found = True
    
    if not found:
        print(f"Nessun cliente trovato con {field_to_search} contenente '{value_to_find}'.")
