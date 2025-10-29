# Gestione Anagrafica Clienti

Questo progetto contiene una serie di script per elaborare e interrogare i dati dell'anagrafica clienti esportati dal gestionale Prodware.

## Scopo

L'obiettivo principale è trasformare i dati grezzi, esportati in 8 file CSV con un formato complesso, in un unico file CSV pulito e strutturato (`anagrafica_pulita.csv`). Vengono forniti anche script per interrogare i dati puliti.

## Scripts

### `process_anagrafica.py`

Questo è lo script principale del progetto. Legge tutti i file `anagrafica_*.csv` presenti nella directory, elabora i dati per estrarre le informazioni di ogni cliente e li consolida in un unico file CSV. **Lo script è stato corretto e ora funziona come previsto, generando `anagrafica_pulita.csv` con i dati estratti.**

**Utilizzo:**
```bash
python process_anagrafica.py
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
Assicurati di avere Streamlit installato:
```bash
pip install streamlit pandas
```

**Utilizzo:**
Per avviare l'applicazione, naviga nella directory del progetto tramite il terminale ed esegui:
```bash
streamlit run app.py
```
L'applicazione si aprirà automaticamente nel tuo browser web.

---
*Ultimo aggiornamento: mercoledì 29 ottobre 2025*
