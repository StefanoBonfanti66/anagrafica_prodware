import streamlit as st
import pandas as pd
import os
from process_anagrafica import process_customer_files
import google.generativeai as genai

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ANAGRAFICA_PULITA_PATH = os.path.join(PROJECT_ROOT, 'anagrafica_pulita.csv')
FILE_PATTERN_COMPLETO = os.path.join(PROJECT_ROOT, 'anagrafica_*.csv')

# --- Streamlit App ---
st.set_page_config(page_title="Gestione Anagrafica Clienti", layout="wide")
st.title("Gestione Anagrafica Clienti")

st.write("Benvenuta/o nell'applicazione per la gestione dell'anagrafica clienti.")

# --- Data Processing Section ---
st.header("Elaborazione Dati Anagrafici")
st.write("Clicca il pulsante qui sotto per elaborare i file CSV grezzi e generare `anagrafica_pulita.csv`.")

if st.button("Elabora Anagrafica"):
    with st.spinner("Elaborazione in corso..."):
        try:
            df_completo = process_customer_files(FILE_PATTERN_COMPLETO)
            if not df_completo.empty:
                df_completo.to_csv(ANAGRAFICA_PULITA_PATH, index=False)
                st.success(f"Elaborazione completata! Trovati {len(df_completo)} clienti in totale.")
                st.write("Prime 5 righe del DataFrame:")
                st.dataframe(df_completo.head())
            else:
                st.warning("Nessun dato cliente trovato nei file sorgente.")
        except Exception as e:
            st.error(f"Si è verificato un errore durante l'elaborazione: {e}")

# --- Display Current Data Section ---
st.header("Dati Clienti Attuali")
df_anagrafica = pd.DataFrame() # Initialize empty DataFrame
if os.path.exists(ANAGRAFICA_PULITA_PATH):
    try:
        df_anagrafica = pd.read_csv(ANAGRAFICA_PULITA_PATH)
        st.write(f"Il file `anagrafica_pulita.csv` contiene {len(df_anagrafica)} clienti.")
        st.dataframe(df_anagrafica)
    except Exception as e:
        st.error(f"Errore durante la lettura di `anagrafica_pulita.csv`: {e}")
else:
    st.info("Il file `anagrafica_pulita.csv` non è ancora stato generato. Elabora i dati per visualizzarli.")

# --- Gemini AI Query Section ---
st.header("Interrogazione con AI (Gemini)")
st.write("Fai domande sui dati dei clienti utilizzando l'intelligenza artificiale di Gemini.")

# API Key Input
gemini_api_key = st.text_input("Inserisci la tua Gemini API Key", type="password", key="gemini_api_key_input")

if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)

        model = genai.GenerativeModel('gemini-pro-latest')

        st.success("Gemini API configurata con successo!")

        # --- Filtering UI for Gemini Context ---
        st.subheader("Filtra i dati per la query Gemini")
        
        # General search input
        search_query = st.text_input("Cerca per Codice o Ragione Sociale (opzionale):", key="search_query_input")

        # Nazione filter
        unique_nazioni = ['Tutte'] + sorted(df_anagrafica['Nazione'].dropna().unique().tolist())
        selected_nazione = st.selectbox("Filtra per Nazione:", unique_nazioni, key="nazione_filter_select")

        # Condizione filter
        unique_condizioni = ['Tutte'] + sorted(df_anagrafica['Condizione'].dropna().unique().tolist())
        selected_condizione = st.selectbox("Filtra per Condizione:", unique_condizioni, key="condizione_filter_select")

        df_filtered = df_anagrafica.copy()

        # Apply filters
        if search_query:
            df_filtered = df_filtered[
                df_filtered['Codice'].astype(str).str.contains(search_query, case=False, na=False) |
                df_filtered['Ragione Sociale'].astype(str).str.contains(search_query, case=False, na=False)
            ]
        if selected_nazione != 'Tutte':
            df_filtered = df_filtered[df_filtered['Nazione'] == selected_nazione]
        if selected_condizione != 'Tutte':
            df_filtered = df_filtered[df_filtered['Condizione'] == selected_condizione]

        st.write(f"Dati filtrati per Gemini: {len(df_filtered)} clienti.")
        st.dataframe(df_filtered) # Display filtered data for user to see what's being sent

        # --- End Filtering UI ---

        user_question = st.text_area("Fai la tua domanda sui clienti filtrati:", key="user_question_input")

        if st.button("Chiedi a Gemini", key="ask_gemini_button"):
            if not user_question:
                st.warning("Per favore, inserisci una domanda.")
            elif df_filtered.empty:
                st.warning("Non ci sono dati clienti filtrati da interrogare. Applica i filtri o elabora l'anagrafica.")
            else:
                with st.spinner("Gemini sta elaborando la tua richiesta..."):
                    # Pass the filtered DataFrame as context
                    data_context = df_filtered.to_csv(index=False)

                    prompt = f"""
                    Sei un assistente che risponde a domande sui dati dei clienti.
                    I dati dei clienti sono forniti qui sotto in formato CSV.
                    Rispondi alla domanda dell'utente basandoti ESCLUSIVAMENTE sui dati forniti.
                    Se la risposta non può essere trovata nei dati, indica che non hai informazioni.

                    Dati dei clienti (CSV filtrati):
                    ```csv
                    {data_context}
                    ```

                    Domanda dell'utente: {user_question}
                    """
                    try:
                        response = model.generate_content(prompt)
                        st.write("### Risposta di Gemini:")
                        st.write(response.text)
                    except Exception as gemini_e:
                        st.error(f"Errore durante la chiamata a Gemini API: {gemini_e}")

    except Exception as e:
        st.error(f"Errore durante la configurazione della Gemini API: {e}")
else:
    st.info("Inserisci la tua Gemini API Key per abilitare l'interrogazione AI.")