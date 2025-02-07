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
st.text("Ein Krankenhaus erlebt eine massive Zunahme an Patienten aufgrund einer hochansteckenden Atemwegserkrankung  die sich zu einer Pandemie ausgeweitet hat. Bei manchen Patienten löst die Krankheit einen milden Symptomverlauf aus, bei anderen einen schwerwiegenden. Einige dieser Patienten benötigen intensivmedizinische Betreuung, während andere mit leichteren Symptomen isoliert werden müssen, um eine weitere Verbreitung der Krankheit zu verhindern. Gleichzeitig müssen weiterhin Patienten mit anderen Erkrankungen versorgt werden, wie Unfallopfer, Herzinfarkt- oder Krebspatienten, die ebenfalls auf lebenswichtige Behandlungen angewiesen sind. Durch die Pandemie erhöht sich der Bedarf an Flächen der Intensivmedizin (2.03) und der Isolationskrankenpflege (2.06). Um eine ausreichende Versorgung zu schaffen müssen kurzfristig und übergangsweise neue Fläche zur Verfügung gestellt werden, die die Pflege von erkrankten Patienten sicherstellt, dazu können kurzzeitig andere Flächen umgenutzt werden.")

# Button Szenarioergebnisse darstellen

# Ergebnisdarstellung als blanker Text 

# Vergleichsmöglichkeit 
st.subheader ("Wählen Sie die Teilstellen, die Sie Vergleichen möchten")

