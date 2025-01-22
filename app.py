import streamlit as st
import pandas as pd
import pdfplumber

# Definition der 14 Teilstellen des Funktionsbereichs Pflege mit spezifischen Zimmeranforderungen
pflege_teilstellen = [
    {"Teilstelle": "2.01 Allgemeine Pflege", "Ausgewählt": False, "Räume": [
        "Arztraum", "Dienstplatz", "Personalaufenthaltsräume", "Teeküche", "Medikamentenräume", "Waschräume",
        "Arbeitsraum unrein", "Ver- und Entsorgung Wäsche", "Ver- und Entsorgung Abfall", "Ver- und Entsorgung Speisen",
        "Ver- und Entsorgung Medikamente", "Bettenzimmer", "Patientenzimmer (3-Bett)", "Patientenzimmer (2-Bett)",
        "Patientenzimmer (Einzel)", "WC Personal", "WC Besucher", "Patientenaufenthaltsraum", "Technikraum"
    ]},
    {"Teilstelle": "2.02 Wöchnerinnen- und Neugeborenenpflege", "Ausgewählt": False, "Räume": [
        "Pflege - Wöchnerinnen", "Pflege - Neugeborene"
    ]},
    {"Teilstelle": "2.03 Intensivmedizin", "Ausgewählt": False, "Räume": [
        "Intensivtherapie", "Intensivüberwachung", "Stroke Unit", "Chest-Pain-Unit", "Schwerstbrandverletzte"
    ]},
    {"Teilstelle": "2.04 Dialyse", "Ausgewählt": False, "Räume": [
        "Aktudialyse", "Chronische Dialyse"
    ]},
    {"Teilstelle": "2.05 Säuglings-, Kinder- und Jugendkrankenpflege", "Ausgewählt": False, "Räume": [
        "Allgemeine Kinder- und Jugendkrankenpflege", "Säuglingskrankenpflege", "Kinderintensivpflege", "Neonatologie"
    ]},
    {"Teilstelle": "2.06 Isolationskrankenpflege", "Ausgewählt": False, "Räume": [
        "Infektionskrankenpflege", "Umkehrisolation"
    ]},
    {"Teilstelle": "2.07 Pflege psychisch Kranker", "Ausgewählt": False, "Räume": [
        "Allgemeine Psychiatrie", "Forensische Psychiatrie", "Gerontopsychatrie", "Psychosomatik", "Kinder- und Jugendpsychiatrie"
    ]},
    {"Teilstelle": "2.08 Pflege - Nuklearmedizin", "Ausgewählt": False, "Räume": []},
    {"Teilstelle": "2.09 Aufnahmepflege", "Ausgewählt": False, "Räume": []},
    {"Teilstelle": "2.10 Pflege - Geriatrie", "Ausgewählt": False, "Räume": []},
    {"Teilstelle": "2.11 Tagesklinik", "Ausgewählt": False, "Räume": []},
    {"Teilstelle": "2.12 Palliativmedizin", "Ausgewählt": False, "Räume": []},
    {"Teilstelle": "2.13 Rehabilitation", "Ausgewählt": False, "Räume": []},
    {"Teilstelle": "2.14 Komfortstation", "Ausgewählt": False, "Räume": []}
]

# Szenarien-Beschreibungen
szenarien = {
    "Szenario 1": "Fehlendes Fachpersonal: Eine Neugeborenenstation wird geschlossen. Es wird geprüft, welche Pflegeeinheit stattdessen eingerichtet werden kann.",
    "Szenario 2": "Personalmangel: Stationen müssen zusammengelegt werden. Es wird geprüft, welche Bereiche ähnliche Anforderungen haben.",
    "Szenario 3": "Pandemie: Es besteht ein erhöhter Bedarf an Intensivmedizin und Isolierstationen.",
    "Szenario 4": "Umbau: Während einer Gebäuderenovierung muss eine Station vorübergehend verlagert werden."
}

# Umwandeln in DataFrame für Anzeige
pflege_df = pd.DataFrame(pflege_teilstellen)

# Streamlit-Anzeige
st.title("Pflegebereichs-Szenario-Simulation")

# Anzeige der vollständigen Tabelle aller Teilstellen mit Auswahlmöglichkeit
st.header("📋 Wähle die in der Einrichtung vorhandenen Teilstellen")
edited_df = st.data_editor(pflege_df, use_container_width=True, num_rows="dynamic", disabled=["Räume"])

# Filtern der ausgewählten Teilstellen
selected_teilstellen = edited_df[edited_df["Ausgewählt"] == True]["Teilstelle"].tolist()

# Szenario Auswahl
st.header("📌 Wähle ein Szenario")
scenario_choice = st.selectbox("Szenario auswählen", list(szenarien.keys()))
st.write("**Beschreibung:**", szenarien[scenario_choice])

# Simulation der Szenarien basierend auf Raumanforderungen
st.header("🔍 Simulationsergebnisse")
for teilstelle in selected_teilstellen:
    st.subheader(f"Ergebnis für {teilstelle}")
    if scenario_choice == "Szenario 1" and "Neugeborene" in str(teilstelle):
        st.write("Diese Teilstelle kann angepasst werden, um die Betreuung von Neugeborenen zu ermöglichen. Zusätzliche Ausstattung könnte erforderlich sein.")
    elif scenario_choice == "Szenario 2" and "Geriatrie" in str(teilstelle):
        st.write("Die Geriatrie könnte mit einer anderen Pflegeeinheit kombiniert werden, um Personalmangel auszugleichen.")
    elif scenario_choice == "Szenario 3" and "Intensivmedizin" in str(teilstelle):
        st.write("Diese Teilstelle ist für die Pandemie-Bewältigung gut geeignet. Mögliche Erweiterungen für Intensivbetten könnten geprüft werden.")
    elif scenario_choice == "Szenario 4" and "Tagesklinik" in str(teilstelle):
        st.write("Die Tagesklinik könnte temporär als alternative Pflegeeinheit genutzt werden.")
    else:
        st.write("Keine spezifische Anpassung erforderlich oder nicht optimal für dieses Szenario.")

