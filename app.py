import streamlit as st
import pandas as pd
import pdfplumber

# Definition der 14 Teilstellen des Funktionsbereichs Pflege mit spezifischen Zimmeranforderungen
pflege_teilstellen = [
    {"Teilstelle": "2.01 Allgemeine Pflege", "Ausgewählt": False, "Raumgrößen": 20, "Technik": "EDV-Anbindung, Notrufsystem"},
    {"Teilstelle": "2.02 Wöchnerinnen- und Neugeborenenpflege", "Ausgewählt": False, "Raumgrößen": 18, "Technik": "Basisdiagnostik, Neugeborenenversorgung"},
    {"Teilstelle": "2.03 Intensivmedizin", "Ausgewählt": False, "Raumgrößen": 25, "Technik": "Spezialsteckdosen (Sauerstoff, Vakuum, Druckluft), Monitoring-System"},
    {"Teilstelle": "2.04 Dialyse", "Ausgewählt": False, "Raumgrößen": 22, "Technik": "Dialysegeräte, Langzeit-Dialyse"},
    {"Teilstelle": "2.05 Säuglings-, Kinder- und Jugendkrankenpflege", "Ausgewählt": False, "Raumgrößen": 16, "Technik": "Kinderbetten, Wärmebett, Monitoring"},
    {"Teilstelle": "2.06 Isolationskrankenpflege", "Ausgewählt": False, "Raumgrößen": 24, "Technik": "Überdrucksystem, Schutzschleusen"},
    {"Teilstelle": "2.07 Pflege psychisch Kranker", "Ausgewählt": False, "Raumgrößen": 20, "Technik": "Sichere Einrichtung"},
    {"Teilstelle": "2.08 Pflege - Nuklearmedizin", "Ausgewählt": False, "Raumgrößen": 25, "Technik": "Strahlenschutz, Spezialgeräte"},
    {"Teilstelle": "2.09 Aufnahmepflege", "Ausgewählt": False, "Raumgrößen": 15, "Technik": "EDV-System, Notrufsystem"},
    {"Teilstelle": "2.10 Pflege - Geriatrie", "Ausgewählt": False, "Raumgrößen": 22, "Technik": "Barrierefrei, Notrufsystem"},
    {"Teilstelle": "2.11 Tagesklinik", "Ausgewählt": False, "Raumgrößen": 20, "Technik": "Flexible Ausstattung"},
    {"Teilstelle": "2.12 Palliativmedizin", "Ausgewählt": False, "Raumgrößen": 25, "Technik": "Klimatisierung, Komfortausstattung"},
    {"Teilstelle": "2.13 Rehabilitation", "Ausgewählt": False, "Raumgrößen": 30, "Technik": "Therapiegeräte, Bewegungsfläche"},
    {"Teilstelle": "2.14 Komfortstation", "Ausgewählt": False, "Raumgrößen": 30, "Technik": "Luxuriöse Ausstattung, WLAN"}
]

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
edited_df = st.data_editor(pd.DataFrame(pflege_teilstellen), use_container_width=True, num_rows="dynamic")
selected_teilstellen = edited_df[edited_df["Ausgewählt"] == True]["Teilstelle"].tolist()

# Szenario Auswahl
st.header("📌 Wähle ein Szenario")
scenario_choice = st.selectbox("Szenario auswählen", list(szenarien.keys()))
st.write("**Beschreibung:**", szenarien[scenario_choice])

# Dynamische Analyse und Simulation
st.header("🔍 Simulationsergebnisse")
for teilstelle in selected_teilstellen:
    st.subheader(f"Ergebnis für {teilstelle}")
    st.write("Vergleich der Anforderungen mit Szenario-Anforderungen...")
    
    # Vergleich der Anforderungen
    vergleich_df = pd.DataFrame([{ "Teilstelle": teilstelle, "Raumgrößen": next(t["Raumgrößen"] for t in pflege_teilstellen if t["Teilstelle"] == teilstelle), "Technik": next(t["Technik"] for t in pflege_teilstellen if t["Teilstelle"] == teilstelle) }])
    st.dataframe(vergleich_df)
    
    # Detaillierte Lösungsvorschläge
    if scenario_choice == "Szenario 1" and "Neugeborenenpflege" in teilstelle:
        st.write("Diese Teilstelle kann umgewandelt werden, benötigt jedoch zusätzliche Ausstattung für die Betreuung von Neugeborenen.")
    elif scenario_choice == "Szenario 2" and "Geriatrie" in teilstelle:
        st.write("Diese Teilstelle kann mit einer anderen Pflegeeinheit kombiniert werden, um den Personalmangel auszugleichen.")
    elif scenario_choice == "Szenario 3" and "Intensivmedizin" in teilstelle:
        st.write("Diese Teilstelle ist für eine Pandemie-Situation gut geeignet. Zusätzliche Betten könnten eingerichtet werden.")
    elif scenario_choice == "Szenario 4" and "Tagesklinik" in teilstelle:
        st.write("Die Tagesklinik kann temporär für Interimsnutzungen während des Umbaus genutzt werden.")
    else:
        st.write("Keine spezifische Anpassung erforderlich oder nicht optimal für dieses Szenario.")
