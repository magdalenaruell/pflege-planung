import streamlit as st
import pandas as pd

# 🏥 Titelbild laden und zentrieren
st.markdown(
    """
    <style>
    .centered-image {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Bild zentriert mit `st.image()` laden
st.markdown('<div class="centered-image">', unsafe_allow_html=True)
st.image("IMG_07283.PNG", width=300)  # Stelle sicher, dass das Bild im App-Ordner liegt
st.markdown('</div>', unsafe_allow_html=True)

# Titel der Anwendung
st.title("MediMetrics")

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


# 🔗 GitHub-Repository, in dem die Excel-Dateien liegen
GITHUB_BASE_URL = "https://raw.githubusercontent.com/magdalenaruell/pflege-planung/main/"  # <-- ÄNDERE das Repo

# 📂 Liste der Excel-Dateien im GitHub-Repo (MUSS manuell gepflegt werden oder mit einer API automatisiert werden)
EXCEL_FILES = [
    "01_WebAnwendung_250128_NBO_DIN.xlsx",
    "02_WebAnwendung_250128_NBO_DIN.xlsx",
    "03_WebAnwendung_250128_NBO_DIN.xlsx",
    "04_WebAnwendung_250128_NBO_DIN.xlsx",
    "05_WebAnwendung_250128_NBO_DIN.xlsx",
    "06_WebAnwendung_250128_NBO_DIN.xlsx",
    "07_WebAnwendung_250128_NBO_DIN.xlsx",
    "08_WebAnwendung_250128_NBO_DIN.xlsx",
    "09_WebAnwendung_250128_NBO_DIN.xlsx",
    "10_WebAnwendung_250128_NBO_DIN.xlsx",
    "11_WebAnwendung_250128_NBO_DIN.xlsx",
    "12_WebAnwendung_250128_NBO_DIN.xlsx",
    "13_WebAnwendung_250128_NBO_DIN.xlsx",
    "14_WebAnwendung_250128_NBO_DIN.xlsx",
]

# 📌 **Excel-Datei auswählen**
st.subheader("📂 Wähle eine Excel-Datei")
selected_file = st.selectbox("📑 Wähle eine Datei:", EXCEL_FILES)

if selected_file:
    file_url = GITHUB_BASE_URL + selected_file  # URL zur Datei generieren

    try:
        # Lade die Excel-Datei direkt aus GitHub
        xls = pd.ExcelFile(file_url)
        sheet_names = xls.sheet_names
        st.success(f"📄 Datei erfolgreich geladen: `{selected_file}`")
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Datei: {str(e)}")
        st.stop()
    
    # 📊 **Tabellenblatt auswählen**
    st.subheader("📄 Wähle ein Tabellenblatt")
    selected_sheet = st.selectbox("📄 Tabellenblatt:", sheet_names)
