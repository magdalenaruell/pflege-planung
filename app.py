import streamlit as st
import pandas as pd

# Definition der Teilstellen des Funktionsbereichs Pflege mit spezifischen Zimmeranforderungen
pflege_teilstellen = [
    {
        "Teilstelle": "Ausgewählt": False. "2.01 Allgemeine Pflege",
        "Räume": [
            {"Name": "Arztraum", "Raumgrößen": "mind. 12 m²", "Bedarf": "1 pro Station", "Lageanforderungen": "Zentral gelegen", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Basisdiagnostik", "Technik": "EDV-Anbindung"},
            {"Name": "Dienstplatz", "Raumgrößen": "mind. 10 m²", "Bedarf": "Pro Pflegebereich", "Lageanforderungen": "Nahe Patientenzimmer", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Optional", "Technik": "EDV-System"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.02 Neugeborenenstation",
        "Räume": [
            {"Name": "Pflege-Wöchnerinnen", "Raumgrößen": "mind. 18 m²", "Bedarf": "Pro Mutter", "Lageanforderungen": "Nahe Stillzimmer", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Beruhigte Lage", "Technik": "Basisdiagnostik"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.03 Intensivstation",
        "Räume": [
            {"Name": "Intensivtherapie", "Raumgrößen": "mind. 25 m²", "Bedarf": "1 pro Patient", "Lageanforderungen": "Zentral", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Schalldicht", "Technik": "Spezialsteckdosen (Sauerstoff, Vakuum, Druckluft)"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.04 Dialyse",
        "Räume": [
            {"Name": "Behandlungsraum", "Raumgrößen": "mind. 20 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Nahe Technikraum", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Hygienebereich", "Technik": "Dialysegeräte"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.05 Kinder- und Jugendkrankenpflege",
        "Räume": [
            {"Name": "Kinderzimmer", "Raumgrößen": "mind. 15 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Nahe Spielraum", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Farbenfrohes Design", "Technik": "Optional"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.06 Isolationskrankenpflege",
        "Räume": [
            {"Name": "Isoliereinheit", "Raumgrößen": "mind. 25 m²", "Bedarf": "1 pro Patient", "Lageanforderungen": "Separat", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Schleusen", "Technik": "Raumlufttechnik mit Überdrucksystem"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.07 Pflege psychisch Kranker",
        "Räume": [
            {"Name": "Therapieraum", "Raumgrößen": "mind. 20 m²", "Bedarf": "1 pro Station", "Lageanforderungen": "Nahe Aufenthaltsraum", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Beruhigte Atmosphäre", "Technik": "Optional"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.08 Pflege - Nuklearmedizin",
        "Räume": [
            {"Name": "Behandlungsraum", "Raumgrößen": "mind. 25 m²", "Bedarf": "1 pro Patient", "Lageanforderungen": "Nahe Diagnostik", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Strahlenschutz", "Technik": "Spezialgeräte"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.09 Aufnahmepflege",
        "Räume": [
            {"Name": "Aufnahmezimmer", "Raumgrößen": "mind. 15 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Nahe Eingang", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Diskretion", "Technik": "EDV-System"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.10 Pflege - Geriatrie",
        "Räume": [
            {"Name": "Patientenzimmer", "Raumgrößen": "mind. 20 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Nahe Aufenthaltsraum", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Barrierefrei", "Technik": "TV, Notrufsystem"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.11 Tagesklinik",
        "Räume": [
            {"Name": "Therapieraum", "Raumgrößen": "mind. 15 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Zentral", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Flexible Ausstattung", "Technik": "Optional"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.12 Palliativmedizin",
        "Räume": [
            {"Name": "Patientenzimmer", "Raumgrößen": "mind. 25 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Ruhig gelegen", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Komfort", "Technik": "Klimatisierung, TV"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.13 Rehabilitation",
        "Räume": [
            {"Name": "Trainingsraum", "Raumgrößen": "mind. 30 m²", "Bedarf": "Pro Einheit", "Lageanforderungen": "Nahe Physiotherapie", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Bewegungsfläche", "Technik": "Trainingsgeräte"}
        ]
    },
    {
        "Teilstelle": "Ausgewählt": False. "2.14 Komfortstation",
        "Räume": [
            {"Name": "Patientenzimmer", "Raumgrößen": "mind. 30 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Ruhig", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Luxuriöse Ausstattung", "Technik": "Klimatisierung, TV, WLAN"}
        ]
    }
]

# Auswahl der vorhandenen Teilstellen in der Einrichtung
st.header("🏥 Wähle die vorhandenen Teilstellen in der Einrichtung")
selected_teilstellen = st.multiselect("Welche Teilstellen sind in der Einrichtung vorhanden?", [t["Teilstelle"] for t in pflege_teilstellen], default=[t["Teilstelle"] for t in pflege_teilstellen])

# Szenarien-Beschreibungen
szenarien = {
    "Szenario 1": "Fehlendes Fachpersonal: Eine Neugeborenenstation wird geschlossen. Es wird geprüft, welche Pflegeeinheit stattdessen eingerichtet werden kann.",
    "Szenario 2": "Personalmangel: Stationen müssen zusammengelegt werden. Es wird geprüft, welche Bereiche ähnliche Anforderungen haben.",
    "Szenario 3": "Pandemie: Es besteht ein erhöhter Bedarf an Intensivmedizin und Isolierstationen.",
    "Szenario 4": "Umbau: Während einer Gebäuderenovierung muss eine Station vorübergehend verlagert werden."
}

# Umwandeln in DataFrame für Anzeige
pflege_df = []
for teilstelle in pflege_teilstellen:
    for raum in teilstelle["Räume"]:
        pflege_df.append({"Teilstelle": teilstelle["Teilstelle"], **raum})

pflege_df = pd.DataFrame(pflege_df)

# Streamlit-Anzeige
st.title("Pflegebereichs-Szenario-Simulation")

# Anzeige der vollständigen Tabelle aller Teilstellen und Räume
st.header("📋 Übersicht der Teilstellen und Räume")
st.dataframe(pflege_df)

# Szenario Auswahl
st.header("📌 Wähle ein Szenario")
scenario_choice = st.selectbox("Szenario auswählen", list(szenarien.keys()))
st.write("**Beschreibung:**", szenarien[scenario_choice])

# Teilstelle Auswahl
st.header("🏥 Wähle eine Teilstelle")
teilstelle_choice = st.selectbox("Teilstelle auswählen", [t["Teilstelle"] for t in pflege_teilstellen])

# Anzeige der Raumanforderungen der gewählten Teilstelle
st.header("📋 Anforderungen der gewählten Teilstelle")
selected_teilstelle = next((t for t in pflege_teilstellen if t["Teilstelle"] == teilstelle_choice), None)
if selected_teilstelle:
    st.dataframe(pd.DataFrame(selected_teilstelle["Räume"]))

# Lösungsdarstellung basierend auf Anforderungen
st.header("🔍 Lösungsvorschlag")
if scenario_choice == "Szenario 1":
    if any("Basisdiagnostik" in raum["Technik"] for raum in selected_teilstelle["Räume"]):
        st.write("Die Teilstelle verfügt über geeignete diagnostische Einrichtungen, um die Neugeborenenversorgung zu übernehmen. Eine Anpassung der Räume zur spezifischen Betreuung könnte erforderlich sein.")
    else:
        st.write("Diese Teilstelle erfüllt nicht die technischen Anforderungen für die Neugeborenenpflege.")

elif scenario_choice == "Szenario 2":
    if any("EDV-System" in raum["Technik"] for raum in selected_teilstelle["Räume"]):
        st.write("Diese Teilstelle verfügt über digitale Infrastruktur, die eine effiziente Zusammenlegung mit anderen Einheiten ermöglicht.")
    else:
        st.write("Es könnten zusätzliche EDV-Anbindungen erforderlich sein, um eine Zusammenlegung zu erleichtern.")

elif scenario_choice == "Szenario 3":
    if any("Spezialsteckdosen" in raum["Technik"] for raum in selected_teilstelle["Räume"]):
        st.write("Diese Teilstelle ist für Intensivmedizin geeignet und könnte erweitert werden, um die Anforderungen der Pandemie zu erfüllen.")
    else:
        st.write("Zusätzliche technische Einrichtungen sind erforderlich, um diese Teilstelle für Intensivmedizin zu nutzen.")

elif scenario_choice == "Szenario 4":
    if any("Schalldicht" in raum["Bestimmte Raumeigenschaften"] for raum in selected_teilstelle["Räume"]):
        st.write("Diese Teilstelle bietet eine ruhige Umgebung, die für eine temporäre Verlagerung geeignet ist.")
    else:
        st.write("Es könnten zusätzliche Anpassungen erforderlich sein, um diese Teilstelle für die Verlagerung nutzbar zu machen.")

