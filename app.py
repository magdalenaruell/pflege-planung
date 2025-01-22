import streamlit as st
import pandas as pd
import pdfplumber

# Definition der 14 Teilstellen des Funktionsbereichs Pflege mit spezifischen Zimmeranforderungen
csv_url = "https://raw.githubusercontent.com/magdalenaruell/pflege-planung/main/250122_Excel-AnfordeungenDIN.csv"

df = pd.read_csv(csv_url)

import streamlit as st
st.write(df)

# Szenarien-Beschreibungen
szenarien = {
    "Szenario 1": "Fehlendes Fachpersonal: Eine Teilstelle wird geschlossen. Es wird geprüft, welche Pflegeeinheit stattdessen eingerichtet werden kann.",
    "Szenario 2": "Personalmangel: Teilstellen müssen zusammengelegt werden. Es wird geprüft, welche Bereiche ähnliche Anforderungen haben.",
    "Szenario 3": "Pandemie: Erhöhter Bedarf an Intensivmedizin (2.03) und Isolierstation (2.05). Es wird geprüft, welche Interimsnutzungen möglich sind.",
    "Szenario 4": "Umbau: Eine Teilstelle muss während der Renovierung in einer anderen untergebracht werden."
}

# Streamlit-Anzeige
st.title("Pflegebereichs-Szenario-Simulation")

# Auswahl der Teilstellen
st.header("📋 Wähle die in der Einrichtung vorhandenen Teilstellen")
edited_df = st.data_editor(pd.DataFrame(pflege_teilstellen), use_container_width=True, num_rows="dynamic", disabled=["Räume"])
selected_teilstellen = edited_df[edited_df["Ausgewählt"] == True]["Teilstelle"].tolist()

# PDF-Upload oder Manuelle Eingabe
st.header("📂 Lade einen PDF-Plan hoch oder gib die relevanten Daten manuell ein")
pdf_file = st.file_uploader("Lade einen PDF-Plan mit Raumtypen und Größen hoch", type=["pdf"])

# Option zum Fortfahren ohne Daten
st.write("Falls kein PDF vorhanden ist und keine manuelle Eingabe erfolgen soll, kannst du ohne Daten fortfahren.")
fortfahren = st.checkbox("Ohne Daten fortfahren")

raumdaten = []
if pdf_file:
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raumdaten.extend(text.split("\n"))
    st.write("Extrahierte Raumdaten:")
    st.write(raumdaten)
elif not fortfahren:
    st.write("📌 Falls kein PDF vorhanden ist, gib die relevanten Daten manuell ein:")
    for teilstelle in selected_teilstellen:
        st.subheader(f"{teilstelle} - Manuelle Eingabe")
        for raum in next(t["Räume"] for t in pflege_teilstellen if t["Teilstelle"] == teilstelle):
            st.text_input(f"{raum} - Größe (m²)")

# Szenario Auswahl
st.header("📌 Wähle ein Szenario")
scenario_choice = st.selectbox("Szenario auswählen", list(szenarien.keys()))
st.write("**Beschreibung:**", szenarien[scenario_choice])

# Dynamische Analyse und Simulation
st.header("🔍 Simulationsergebnisse")
if not selected_teilstellen:
    st.write("⚠ Bitte wähle mindestens eine Teilstelle aus.")
else:
    for teilstelle in selected_teilstellen:
        st.subheader(f"Ergebnis für {teilstelle}")
        vergleich_df = pd.DataFrame([{ "Teilstelle": teilstelle, "Raumgrößen": next(t.get("Raumgrößen", "N/A") for t in pflege_teilstellen if t["Teilstelle"] == teilstelle), "Technik": next(t.get("Technik", "N/A") for t in pflege_teilstellen if t["Teilstelle"] == teilstelle) }])
        st.dataframe(vergleich_df)
        st.write("Detaillierte Lösungsvorschläge basierend auf Raumgrößen, Technik und Bedarf...")
