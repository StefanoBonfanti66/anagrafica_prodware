# Gestione Anagrafica Clienti

Questo progetto contiene una serie di script per elaborare e interrogare i dati dell'anagrafica clienti esportati dal gestionale Prodware.

## Esportazione Anagrafica da Prodware (Registrazione Azioni Utente)

Per garantire la riproducibilità e facilitare l'aggiornamento dell'anagrafica, è fondamentale documentare i passaggi esatti per esportare il file `sanagr01.xlsx` (o `sanagr01.xls`) dal gestionale Prodware. Si consiglia di utilizzare lo strumento "Registrazione azioni utente" (Steps Recorder su Windows) per catturare questi passaggi.

**Come registrare i passaggi:**

1.  **Avvia "Registrazione azioni utente"**: Cerca "Registrazione azioni utente" (o "Steps Recorder") nel menu Start di Windows e aprilo.
2.  **Avvia la registrazione**: Clicca su "Avvia registrazione".
3.  **Esegui l'esportazione da Prodware**: Procedi con l'esportazione del file dell'anagrafica clienti da Prodware, assicurandoti di catturare tutti i clic e le finestre di dialogo rilevanti.
4.  **Interrompi la registrazione**: Una volta completata l'esportazione, clicca su "Interrompi registrazione".
5.  **Salva la registrazione**: Salva il file risultante (solitamente un file `.zip` contenente un report HTML) in una posizione accessibile.

**Dopo aver generato il report, si prega di aggiornare questa sezione del README con un link al report o incorporando direttamente i passaggi chiave qui.**

## Scopo

L'obiettivo principale è trasformare i dati grezzi, esportati in 8 file CSV con un formato complesso, in un unico file CSV pulito e strutturato (`anagrafica_pulita.csv`). Vengono forniti anche script per interrogare i dati puliti.

## Scripts

### `process_excel_anagrafica.py`

Questo script è il nuovo strumento principale per l'elaborazione dei dati dell'anagrafica clienti. Legge direttamente il file Excel `sanagr01.xlsx` (o `sanagr01.xls` se il primo non è presente), analizza i dati da ogni foglio per estrarre le informazioni di ogni cliente e li consolida in un unico file CSV pulito e strutturato (`anagrafica_pulita.csv`). Questo script sostituisce il precedente `process_anagrafica.py` che elaborava i file CSV.

**Utilizzo:**
Per aggiornare l'anagrafica, è sufficiente sostituire il file `sanagr01.xlsx` (o `sanagr01.xls`) con la nuova estrazione da Prodware ed eseguire lo script:
```bash
python process_excel_anagrafica.py
```
Lo script genererà (o sovrascriverà) il file `anagrafica_pulita.csv`.

### `export_gb.py`

Questo script estrae l'elenco dei clienti attivi della Gran Bretagna (`Nazione` contiene 'GB' e `Condizione` è 'N - Attivi') dal file `anagrafica_pulita.csv` e lo salva in un file di testo.

**Utilizzo:**
```bash
python export_gb.py
```
Lo script genererà (o sovrascriverà) il file `clienti_gran_bretagna.txt` con l'elenco dei clienti trovati.

### `find_customer_by_code.py`

Questo script permette di cercare un cliente all'interno del file `anagrafica_pulita.csv` fornendo il suo codice.

**Utilizzo:**
```bash
python find_customer_by_code.py <codice_cliente>
```
**Esempio:**
```bash
python find_customer_by_code.py 00000072
```
Lo script stamperà a schermo i dati del cliente trovato.

## Applicazione Web Interattiva (Streamlit)

Per rendere l'interazione con i dati più user-friendly, è stata creata un'applicazione web interattiva utilizzando Streamlit.

### `app.py`

Questo script avvia l'applicazione Streamlit che permette di elaborare i dati, visualizzare l'anagrafica e in futuro implementare funzionalità di ricerca e filtro tramite un'interfaccia grafica.

**Prerequisiti:**
Assicurati di avere Streamlit, xlrd e openpyxl installati:
```bash
pip install streamlit pandas xlrd openpyxl
```

**Utilizzo:**
Per avviare l'applicazione, naviga nella directory del progetto tramite il terminale ed esegui:
```bash
streamlit run app.py
```
L'applicazione si aprirà automaticamente nel tuo browser web.

---
*Ultimo aggiornamento: giovedì 13 novembre 2025*
