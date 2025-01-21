import streamlit as st
import folium
from streamlit_folium import st_folium
import fitz  # PyMuPDF für PDF-Analyse
import pdfplumber

# Definition der Pflegebereiche mit Anforderungen
pflegebereiche = {
    "2.01": "Allgemeine Pflege",
    "2.02": "Neugeborenenstation",
    "2.03": "Intensivstation",
    "2.04": "Geriatrie",
    "2.05": "Isolierstation"
}

# Szenario-Funktionen
def ersatz_fuer_neugeborenenstation():
    return ["Intensivstation"]

def kombinierbare_stationen():
    return [("Allgemeine Pflege", "Geriatrie"), ("Intensivstation", "Isolierstation")]

def interimsnutzung_pandemie():
    return ["Intensivstation", "Isolierstation"]

def temporaere_unterbringung():
    return {bereich: "Alternativen prüfen" for bereich in pflegebereiche.values()}

# Funktion zur Extraktion von Raumdaten aus PDFs
def extrahiere_raumnamen(pdf_file):
    raumnamen = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split('\n'):
                    if any(keyword in line.lower() for keyword in ["raum", "station", "bereich"]):
                        raumnamen.append(line.strip())
    return list(set(raumnamen))

# Streamlit GUI
st.title("Pflegebereichs-Planung mit interaktiver Karte")

# Szenario-Auswahl
option = st.selectbox("Wähle ein Szenario:", [
    "Ersatz für Neugeborenenstation",
    "Kombinierbare Stationen",
    "Interimsnutzung bei Pandemie",
    "Temporäre Unterbringung bei Umbau"
])

if st.button("Lösung anzeigen"):
    if option == "Ersatz für Neugeborenenstation":
        st.write(ersatz_fuer_neugeborenenstation())
    elif option == "Kombinierbare Stationen":
        st.write(kombinierbare_stationen())
    elif option == "Interimsnutzung bei Pandemie":
        st.write(interimsnutzung_pandemie())
    elif option == "Temporäre Unterbringung bei Umbau":
        st.write(temporaere_unterbringung())

# Hochladen und Anzeigen von Krankenhausplänen
st.header("📂 Krankenhausplan hochladen")
pdf_file = st.file_uploader("Lade einen PDF-Plan des Krankenhauses hoch", type=["pdf"])
if pdf_file:
    raumnamen = extrahiere_raumnamen(pdf_file)
    if raumnamen:
        st.subheader("Extrahierte Raumnamen:")
        st.write(raumnamen)
    else:
        st.write("Keine Raumnamen gefunden.")

# Interaktive Krankenhauskarte erstellen
st.header("📍 Interaktive Krankenhauskarte")

# Standard-Koordinaten für Beispielkarte
m = folium.Map(location=[52.52, 13.405], zoom_start=15)

# Beispielpunkte hinzufügen
stationen = {
    "Intensivstation": [52.521, 13.407],
    "Isolierstation": [52.520, 13.406],
    "Allgemeine Pflege": [52.522, 13.404]
}

for name, coord in stationen.items():
    folium.Marker(coord, popup=name, tooltip=name).add_to(m)

# Karte in Streamlit anzeigen
st_data = st_folium(m, width=700, height=500)
