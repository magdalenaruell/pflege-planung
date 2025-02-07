import streamlit as st
import pandas as pd

# Titel der Anwendung
st.title("🏥 Krankenhaus-Planungstabelle")

# 📂 Datei-Upload oder Fallback auf feste Datei
uploaded_file = st.file_uploader("📂 Laden Sie eine Excel-Datei hoch oder verwenden Sie die Standarddatei", type=["xlsx"])
file_path = "Allin13_WebAnwendung_250128_NBO_DIN.xlsx"  # Fallback-Datei

if uploaded_file is not None:
    # Wenn eine Datei hochgeladen wurde, verwende sie
    xls = pd.ExcelFile(uploaded_file)
    st.info("✅ Eigene hochgeladene Datei wird verwendet.")
else:
    # Wenn keine Datei hochgeladen wurde, verwende die feste Datei
    try:
        xls = pd.ExcelFile(file_path)
        st.info(f"ℹ️ Keine Datei hochgeladen. Verwende die Standarddatei: {file_path}")
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Standarddatei: {str(e)}")
        st.stop()

# ✅ **Lese alle Tabellenblätter aus der gewählten Datei**
try:
    sheets = pd.read_excel(xls, sheet_name=None)  # `None` lädt alle Tabellenblätter
    
    if not sheets:  # Falls die Datei leer ist
        st.error("❌ Die Excel-Datei enthält keine Tabellenblätter.")
        st.stop()
    
    # Zeige alle verfügbaren Tabellenblätter als Multi-Select
    st.subheader("📄 Wählen Sie die Tabellenblätter aus:")
    
    # **Session-State für Auswahl der Tabellenblätter**
    if "selected_sheets" not in st.session_state:
        st.session_state.selected_sheets = []  # Standardwert: Keine Auswahl
    
    selected_sheets = st.multiselect("🔍 Wählen Sie die Tabellenblätter:", list(sheets.keys()), default=st.session_state.selected_sheets)

    # Speichere die Auswahl in Session-State, damit sie bestehen bleibt
    st.session_state.selected_sheets = selected_sheets

    # Zeige die Daten für die ausgewählten Tabellenblätter
    if selected_sheets:
        for sheet in selected_sheets:
            df_filtered = sheets[sheet]  # Lade das Tabellenblatt
            st.subheader(f"📄 Alle Daten aus {sheet}")
            st.dataframe(df_filtered, use_container_width=True, height=600)  # Scrollbare Tabelle

except Exception as e:
    st.error(f"❌ Fehler beim Laden der Excel-Datei: {str(e)}")

# 🦠 **Szenario Pandemie** (Schöner formatiert)
st.markdown("""
    <h3>🦠 Szenario: Pandemie</h3>
    <p style="font-size:18px; line-height:1.6;">
    Ein Krankenhaus erlebt eine massive Zunahme an Patienten aufgrund einer <b>hochansteckenden Atemwegserkrankung</b>, 
    die sich zu einer <b>Pandemie</b> ausgeweitet hat. Bei manchen Patienten löst die Krankheit einen 
    <span style="color:green;"><b>milden Verlauf</b></span> aus, bei anderen einen <span style="color:red;"><b>schwerwiegenden</b></span>.
    </p>
    
    <p style="font-size:18px;">
    Einige dieser Patienten benötigen <b>intensivmedizinische Betreuung</b>, während andere mit leichteren Symptomen isoliert werden müssen, 
    um eine weitere Verbreitung der Krankheit zu verhindern. Gleichzeitig müssen weiterhin Patienten mit anderen Erkrankungen versorgt werden, 
    wie <b>Unfallopfer, Herzinfarkt- oder Krebspatienten</b>, die ebenfalls auf lebenswichtige Behandlungen angewiesen sind.
    </p>
    
    <p style="font-size:18px;">
    Durch die Pandemie erhöht sich der Bedarf an Flächen der <b>Intensivmedizin (2.03)</b> und der <b>Isolationskrankenpflege (2.06)</b>. 
    Um eine ausreichende Versorgung zu schaffen, müssen kurzfristig und übergangsweise neue Flächen zur Verfügung gestellt werden, 
    die die Pflege von erkrankten Patienten sicherstellen. Dazu können kurzzeitig andere Flächen umgenutzt werden.
    </p>
    """, unsafe_allow_html=True)

# 📊 **Vergleichsmöglichkeit**
if selected_sheets:
    st.subheader("📊 Wählen Sie die Spalten, die Sie vergleichen möchten")

    # Kombiniere alle gewählten Tabellenblätter zu einer gemeinsamen Auswahl
    all_columns = []
    for sheet in selected_sheets:
        all_columns.extend(sheets[sheet].columns)

    # Einzigartige Spalten anzeigen
    all_columns = list(set(all_columns))

    compare_options = st.multiselect("🔍 Spalten auswählen:", all_columns)

    if compare_options:
        st.subheader("📊 Vergleich der gewählten Spalten")
        combined_data = pd.concat([sheets[sheet][compare_options] for sheet in selected_sheets], ignore_index=True)
        st.dataframe(combined_data, use_container_width=True, height=600)

