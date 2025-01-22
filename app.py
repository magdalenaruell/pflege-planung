import streamlit as st
import pandas as pd

# Definition der Teilstellen des Funktionsbereichs Pflege mit spezifischen Zimmeranforderungen
pflege_teilstellen = [
    {"Teilstelle": "2.01 Allgemeine Pflege", "Ausgewählt": False, "Räume": [
        {"Name": "Arztraum", "Raumgrößen": "mind. 12 m²", "Bedarf": "1 pro Station", "Lageanforderungen": "Zentral gelegen", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Basisdiagnostik", "Technik": "EDV-Anbindung"},
        {"Name": "Dienstplatz", "Raumgrößen": "mind. 10 m²", "Bedarf": "Pro Pflegebereich", "Lageanforderungen": "Nahe Patientenzimmer", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Optional", "Technik": "EDV-System"}
    ]},
    {"Teilstelle": "2.02 Neugeborenenstation", "Ausgewählt": False, "Räume": [
        {"Name": "Pflege-Wöchnerinnen", "Raumgrößen": "mind. 18 m²", "Bedarf": "Pro Mutter", "Lageanforderungen": "Nahe Stillzimmer", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Beruhigte Lage", "Technik": "Basisdiagnostik"}
    ]},
    {"Teilstelle": "2.03 Intensivstation", "Ausgewählt": False, "Räume": [
        {"Name": "Intensivtherapie", "Raumgrößen": "mind. 25 m²", "Bedarf": "1 pro Patient", "Lageanforderungen": "Zentral", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Schalldicht", "Technik": "Spezialsteckdosen (Sauerstoff, Vakuum, Druckluft)"}
    ]}
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
edited_df = st.data_editor(pflege_df, use_container_width=True, num_rows="dynamic")

# Filtern der ausgewählten Teilstellen
selected_teilstellen = edited_df[edited_df["Ausgewählt"] == True]["Teilstelle"].tolist()

if not selected_teilstellen:
    st.warning("Bitte wähle mindestens eine Teilstelle aus der Tabelle aus.")
    st.stop()

# Szenario Auswahl
st.header("📌 Wähle ein Szenario")
scenario_choice = st.selectbox("Szenario auswählen", list(szenarien.keys()))
st.write("**Beschreibung:**", szenarien[scenario_choice])

# Teilstelle Auswahl - Alle Teilstellen zur Auswahl ermöglichen
st.header("🏥 Wähle eine Teilstelle")
teilstelle_choice = st.selectbox("Teilstelle auswählen", [t["Teilstelle"] for t in pflege_teilstellen])

# Lösungsdarstellung basierend auf Anforderungen
st.header("🔍 Lösungsvorschlag")
if scenario_choice == "Szenario 1":
    if teilstelle_choice == "2.03 Intensivstation":
        st.write("Die Intensivstation könnte als Alternative dienen, da sie ähnliche technische Anforderungen wie Klimatisierung und Raumlufttechnik hat. Ein Stillzimmer könnte eingerichtet werden, und die Ausstattung für Neugeborene müsste ergänzt werden.")
    else:
        st.write("Diese Teilstelle ist für das Szenario weniger geeignet.")

elif scenario_choice == "Szenario 2":
    if teilstelle_choice in ["2.01 Allgemeine Pflege", "2.10 Pflege - Geriatrie"]:
        st.write("Diese Teilstellen könnten zusammengelegt werden. Gemeinsam genutzte Ressourcen wie Medikamentenräume und Personalaufenthaltsräume können die Effizienz steigern.")
    else:
        st.write("Diese Teilstelle ist für das Szenario weniger geeignet.")

elif scenario_choice == "Szenario 3":
    if teilstelle_choice in ["2.03 Intensivstation", "2.06 Isolationskrankenpflege"]:
        st.write("Allgemeine Pflegezimmer könnten in temporäre Isoliereinheiten umgewandelt werden. Die Stroke Unit und Chest-Pain-Unit innerhalb der Intensivstation könnten erweitert werden, da diese bereits über spezialisierte Technik verfügen.")
    else:
        st.write("Diese Teilstelle ist für das Szenario weniger geeignet.")

elif scenario_choice == "Szenario 4":
    if teilstelle_choice in ["2.11 Tagesklinik", "2.13 Rehabilitation"]:
        st.write("Räume dieser Teilstellen könnten temporär genutzt werden. Nicht genutzte Lagerbereiche könnten für die Lagerung von Technik und Möbeln während des Umbaus verwendet werden.")
    else:
        st.write("Diese Teilstelle ist für das Szenario weniger geeignet.")
