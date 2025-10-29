
import csv

count = 0
with open('anagrafica_pulita.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        if row['Nazione'] == 'GB (GRAN BRETAGNA)' and row['Condizione'] == 'N - Attivi':
            count += 1

print(f"Numero di clienti attivi in Gran Bretagna: {count}")
