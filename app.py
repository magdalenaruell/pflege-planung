import streamlit as st
import pandas as pd

# Titel der Anwendung
st.title("Krankenhaus-Planungstabelle")

# Datei laden
file_path = "WebAnwendung_250128_NBO_DIN.xlsx"

# Excel Datei einlesen
xls = pd.ExcelFile(file_path)
df = pd.read_excel(file_path, engine="openpyxl")

# Festes Tabellenblatt wählen
sheet_name = "Paulina"
df = pd.read_excel(xls, sheet_name=sheet_name)

# Ersetze Unnamed-Spalten durch etwas Lesbares
df.columns = [f"Spalte_{i}" if "Unnamed" in str(col) else col for i, col in enumerate(df.columns)]

# Tabelle anzeigen mit Zeilenauswahl
st.subheader("Wählen Sie die in Ihrer Einrichtung vorhandenen Funktionsbereiche und Teilstellen")
selected_rows = st.data_editor(df, height=500, num_rows="dynamic")

# Anzeige der ausgewählten Zeilen
st.subheader("Ausgewählte Zeilen")
st.write(selected_rows)

# Auswahl optionale Datenzugabe 

# Szenario Pandemie
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

# Button Szenarioergebnisse darstellen

# Ergebnisdarstellung als blanker Text 

# Vergleichsmöglichkeit 
st.subheader ("Wählen Sie die Teilstellen, die Sie Vergleichen möchten")
compare_options = st.multiselect("Wählen Sie die Teilstellen, die Sie vergleichen möchten", df.columns)
if compare_options:
    st.write(df[compare_options])
