import streamlit as st
import pandas as pd

# Titel der Anwendung
st.title("🏥 Krankenhaus-Planungstabelle")

# 📂 Datei-Upload oder Fallback auf feste Datei
uploaded_file = st.file_uploader("📂 Laden Sie eine Excel-Datei hoch oder verwenden Sie die Standarddatei", type=["xlsx"])
file_path = "WebAnwendung_250128_NBO_DIN3.xlsx"  # Fallback-Datei

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

# Wähle das Tabellenblatt
sheet_name = "Paulina"
df = pd.read_excel(xls, sheet_name=sheet_name)

# Spaltennamen bereinigen (entfernt "Unnamed" Spaltennamen)
df.columns = [f"Spalte_{i}" if "Unnamed" in str(col) else col for i, col in enumerate(df.columns)]

# ✅ **Prüfen, ob eine "ID"-Spalte vorhanden ist**
if "ID" not in df.columns:
    st.error("❌ Die Spalte 'ID' wurde nicht gefunden. Bitte prüfen Sie die Datei.")
    st.stop()

# ✅ **Nur Zeilen mit erlaubten Werten in der "ID"-Spalte auswählen**
erlaubte_werte = ["2.01", "2.02", "2.03", "2.04", "2.05", "2.06", "2.07", "2.08", "2.09", "2.10", "2.11", "2.12", "2.13", "2.14"]
df_filtered = df[df["ID"].astype(str).isin(erlaubte_werte)]

# 🔹 Auswahl der ID-Werte
st.subheader("📌 Wählen Sie eine ID")
selected_id = st.selectbox("🔍 Verfügbare IDs:", df_filtered["ID"].unique())

# 🔹 Zeige die Zeilen für die ausgewählte ID
filtered_data = df_filtered[df_filtered["ID"] == selected_id]

st.subheader(f"✅ Zeilen für ID: {selected_id}")
st.dataframe(filtered_data, use_container_width=True)

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
st.subheader("📊 Wählen Sie die Teilstellen, die Sie vergleichen möchten")
compare_options = st.multiselect("🔍 Teilstellen auswählen:", df_filtered.columns)

if compare_options:
    st.subheader("📊 Vergleich der gewählten Teilstellen")
    st.dataframe(df_filtered[compare_options], use_container_width=True)
