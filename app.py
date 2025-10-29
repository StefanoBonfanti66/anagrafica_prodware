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

        # Changed model name from 'gemini-pro' to 'gemini-pro-latest'
        model = genai.GenerativeModel('gemini-pro-latest')

        st.success("Gemini API configurata con successo!")

        user_question = st.text_area("Fai la tua domanda sui clienti:", key="user_question_input")

        if st.button("Chiedi a Gemini", key="ask_gemini_button"):
            if not user_question:
                st.warning("Per favore, inserisci una domanda.")
            elif df_anagrafica.empty:
                st.warning("Non ci sono dati clienti da interrogare. Elabora prima l'anagrafica.")
            else:
                with st.spinner("Gemini sta elaborando la tua richiesta..."):
                    data_context = df_anagrafica.to_csv(index=False)

                    prompt = f"""
                    Sei un assistente che risponde a domande sui dati dei clienti.
                    I dati dei clienti sono forniti qui sotto in formato CSV.
                    Rispondi alla domanda dell'utente basandoti ESCLUSIVAMENTE sui dati forniti.
                    Se la risposta non può essere trovata nei dati, indica che non hai informazioni.

                    Dati dei clienti (CSV):
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