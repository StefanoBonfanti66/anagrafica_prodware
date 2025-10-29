
import csv
import sys

if len(sys.argv) < 2:
    print("Usage: python list_unique_values.py <field_name>")
    sys.exit(1)

field_to_search = sys.argv[1]

values = set()
with open('anagrafica_pulita.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        values.add(row[field_to_search])

for value in sorted(list(values)):
    print(value)
