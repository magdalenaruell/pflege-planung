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

# ✅ **Nur Zeilen mit einer gültigen 'ID' auswählen**
df_filtered = df[df["ID"].notna()]

# ✅ **Nur dreistellige IDs für die Auswahl filtern**
dreistellige_spalten = [col for col in df_filtered.columns if col.replace('.', '').isdigit() and len(col.replace('.', '')) == 3]

# 🔹 Auswahl der Teilstellen (nur dreistellige IDs)
st.subheader("📌 Wählen Sie die dreistelligen Teilstellen")
selected_part_areas = st.multiselect("🔍 Verfügbare Teilstellen:", dreistellige_spalten)

if selected_part_areas:
    # 🔹 Filtere das DataFrame nur für die gewählten dreistelligen Teilstellen
    selected_df = df_filtered[selected_part_areas]
    st.subheader("✅ Ausgewählte Teilstellen")
    st.dataframe(selected_df, use_container_width=True)

    # 🔹 Finde dazugehörige **sechsstellige Räume**
    sechsstellige_spalten = [col for col in df_filtered.columns if col.replace('.', '').isdigit() and len(col.replace('.', '')) == 6]
    matched_rooms = {}

    for part_area in selected_part_areas:
        # Suche alle sechsstelligen Räume, die mit der dreistelligen ID beginnen
        related_rooms = [col for col in sechsstellige_spalten if col.startswith(part_area)]
        if related_rooms:
            matched_rooms[part_area] = related_rooms

    # 🔹 Zeige die Räume als separate Tabellen
    if matched_rooms:
        st.subheader("🏠 Zugehörige Räume der ausgewählten Teilstellen")
        for part_area, rooms in matched_rooms.items():
            st.markdown(f"### 🏥 Räume für Teilstelle **{part_area}**")
            st.dataframe(df_filtered[rooms], use_container_width=True)

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
    st.write(df_filtered[compare_options])
