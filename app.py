import streamlit as st
import pandas as pd

# Titel der Anwendung
st.title("Krankenhaus-Planungstabelle")

# Datei hochladen
uploaded_file = st.file_uploader("📂 Laden Sie eine Excel-Datei hoch", type=["xlsx"])

if uploaded_file is not None:
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = "Paulina"
    df = pd.read_excel(xls, sheet_name=sheet_name)

    # Spaltennamen bereinigen (entfernt "Unnamed" Spaltennamen)
    df.columns = [f"Spalte_{i}" if "Unnamed" in str(col) else col for i, col in enumerate(df.columns)]

    # ✅ **Filtern nur dreistelliger IDs für die Auswahl**
    dreistellige_spalten = [col for col in df.columns if col.replace('.', '').isdigit() and len(col.replace('.', '')) == 3]

    # 🔹 Auswahl der Teilstellen (nur dreistellige IDs)
    st.subheader("📌 Wählen Sie die dreistelligen Teilstellen")
    selected_part_areas = st.multiselect("🔍 Verfügbare Teilstellen:", dreistellige_spalten)

    if selected_part_areas:
        # 🔹 Filtere das DataFrame nur für die gewählten dreistelligen Teilstellen
        selected_df = df[selected_part_areas]
        st.subheader("✅ Ausgewählte Teilstellen")
        st.dataframe(selected_df, use_container_width=True)

        # 🔹 Finde dazugehörige **sechsstellige Räume**
        sechsstellige_spalten = [col for col in df.columns if col.replace('.', '').isdigit() and len(col.replace('.', '')) == 6]
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
                st.dataframe(df[rooms], use_container_width=True)

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
    compare_options = st.multiselect("🔍 Teilstellen auswählen:", df.columns)
    if compare_options:
        st.write(df[compare_options])

    # 📊 **Vergleichsmöglichkeit**
    st.subheader("📊 Wählen Sie die Teilstellen, die Sie vergleichen möchten")
    compare_options = st.multiselect("🔍 Teilstellen auswählen:", df.columns)
    if compare_options:
        st.write(df[compare_options])

# Button Szenarioergebnisse darstellen

# Ergebnisdarstellung als blanker Text 

# Vergleichsmöglichkeit 
st.subheader ("Wählen Sie die Teilstellen, die Sie Vergleichen möchten")
compare_options = st.multiselect("Wählen Sie die Teilstellen, die Sie vergleichen möchten", df.columns)
if compare_options:
    st.write(df[compare_options])
