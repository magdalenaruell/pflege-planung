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
st.subheader("Tabellenansicht")
selected_rows = st.data_editor(df, height=500, num_rows="dynamic")

# Anzeige der ausgewählten Zeilen
st.subheader("Ausgewählte Zeilen")
st.write(selected_rows)
