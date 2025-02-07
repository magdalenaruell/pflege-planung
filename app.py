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
    
    # Zeige alle verfügbaren Tabellenblätter als Buttons nebeneinander
    st.subheader("📄 Wählen Sie ein Tabellenblatt:")
    
    # **Speichere die Auswahl mit Session-State**
    if "selected_sheet" not in st.session_state:
        st.session_state.selected_sheet = list(sheets.keys())[0]  # Standardwert: Erstes Blatt

    cols = st.columns(len(sheets))  # Erzeuge Spalten für die Buttons

    for i, sheet in enumerate(sheets.keys()):
        if cols[i].button(sheet):  # Falls der Button geklickt wird, setze das Blatt
            st.session_state.selected_sheet = sheet

    # Lade das ausgewählte Tabellenblatt als DataFrame
    df_filtered = sheets[st.session_state.selected_sheet]

    # Zeige alle Zeilen des gewählten Tabellenblatts
    st.subheader(f"📄 Alle Daten aus {st.session_state.selected_sheet}")
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
st.subheader("📊 Wählen Sie die Spalten, die Sie vergleichen möchten")
compare_options = st.multiselect("🔍 Spalten auswählen:", df_filtered.columns)

if compare_options:
    st.subheader("📊 Vergleich der gewählten Spalten")
    st.dataframe(df_filtered[compare_options], use_container_width=True, height=600)


