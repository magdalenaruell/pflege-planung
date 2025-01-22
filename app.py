import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Definition der Teilstellen des Funktionsbereichs Pflege mit spezifischen Zimmeranforderungen
pflege_teilstellen = [
    {
        "Teilstelle": "2.01 Allgemeine Pflege",
        "Räume": [
            {"Name": "Arztraum", "Raumgrößen": "mind. 12 m²", "Bedarf": "1 pro Station", "Lageanforderungen": "Zentral gelegen", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Basisdiagnostik", "Technik": "EDV-Anbindung"},
            {"Name": "Dienstplatz", "Raumgrößen": "mind. 10 m²", "Bedarf": "Pro Pflegebereich", "Lageanforderungen": "Nahe Patientenzimmer", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Optional", "Technik": "EDV-System"}
        ]
    },
    {
        "Teilstelle": "2.02 Neugeborenenstation",
        "Räume": [
            {"Name": "Pflege-Wöchnerinnen", "Raumgrößen": "mind. 18 m²", "Bedarf": "Pro Mutter", "Lageanforderungen": "Nahe Stillzimmer", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Beruhigte Lage", "Technik": "Basisdiagnostik"}
        ]
    },
    {
        "Teilstelle": "2.03 Intensivstation",
        "Räume": [
            {"Name": "Intensivtherapie", "Raumgrößen": "mind. 25 m²", "Bedarf": "1 pro Patient", "Lageanforderungen": "Zentral", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Schalldicht", "Technik": "Spezialsteckdosen (Sauerstoff, Vakuum, Druckluft)"}
        ]
    },
    {
        "Teilstelle": "2.04 Dialyse",
        "Räume": [
            {"Name": "Behandlungsraum", "Raumgrößen": "mind. 20 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Nahe Technikraum", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Hygienebereich", "Technik": "Dialysegeräte"}
        ]
    },
    {
        "Teilstelle": "2.05 Kinder- und Jugendkrankenpflege",
        "Räume": [
            {"Name": "Kinderzimmer", "Raumgrößen": "mind. 15 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Nahe Spielraum", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Farbenfrohes Design", "Technik": "Optional"}
        ]
    },
    {
        "Teilstelle": "2.06 Isolationskrankenpflege",
        "Räume": [
            {"Name": "Isoliereinheit", "Raumgrößen": "mind. 25 m²", "Bedarf": "1 pro Patient", "Lageanforderungen": "Separat", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Schleusen", "Technik": "Raumlufttechnik mit Überdrucksystem"}
        ]
    },
    {
        "Teilstelle": "2.07 Pflege psychisch Kranker",
        "Räume": [
            {"Name": "Therapieraum", "Raumgrößen": "mind. 20 m²", "Bedarf": "1 pro Station", "Lageanforderungen": "Nahe Aufenthaltsraum", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Beruhigte Atmosphäre", "Technik": "Optional"}
        ]
    },
    {
        "Teilstelle": "2.08 Pflege - Nuklearmedizin",
        "Räume": [
            {"Name": "Behandlungsraum", "Raumgrößen": "mind. 25 m²", "Bedarf": "1 pro Patient", "Lageanforderungen": "Nahe Diagnostik", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Strahlenschutz", "Technik": "Spezialgeräte"}
        ]
    },
    {
        "Teilstelle": "2.09 Aufnahmepflege",
        "Räume": [
            {"Name": "Aufnahmezimmer", "Raumgrößen": "mind. 15 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Nahe Eingang", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Diskretion", "Technik": "EDV-System"}
        ]
    },
    {
        "Teilstelle": "2.10 Pflege - Geriatrie",
        "Räume": [
            {"Name": "Patientenzimmer", "Raumgrößen": "mind. 20 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Nahe Aufenthaltsraum", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Barrierefrei", "Technik": "TV, Notrufsystem"}
        ]
    },
    {
        "Teilstelle": "2.11 Tagesklinik",
        "Räume": [
            {"Name": "Therapieraum", "Raumgrößen": "mind. 15 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Zentral", "Sanitär": "Nein", "Bestimmte Raumeigenschaften": "Flexible Ausstattung", "Technik": "Optional"}
        ]
    },
    {
        "Teilstelle": "2.12 Palliativmedizin",
        "Räume": [
            {"Name": "Patientenzimmer", "Raumgrößen": "mind. 25 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Ruhig gelegen", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Komfort", "Technik": "Klimatisierung, TV"}
        ]
    },
    {
        "Teilstelle": "2.13 Rehabilitation",
        "Räume": [
            {"Name": "Trainingsraum", "Raumgrößen": "mind. 30 m²", "Bedarf": "Pro Einheit", "Lageanforderungen": "Nahe Physiotherapie", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Bewegungsfläche", "Technik": "Trainingsgeräte"}
        ]
    },
    {
        "Teilstelle": "2.14 Komfortstation",
        "Räume": [
            {"Name": "Patientenzimmer", "Raumgrößen": "mind. 30 m²", "Bedarf": "Pro Patient", "Lageanforderungen": "Ruhig", "Sanitär": "Ja", "Bestimmte Raumeigenschaften": "Luxuriöse Ausstattung", "Technik": "Klimatisierung, TV, WLAN"}
        ]
    }
]

# Szenarien-Beschreibungen und Lösungsvorschläge
szenarien = {
    "Szenario 1": {
        "Beschreibung": "Fehlendes Fachpersonal: Eine Neugeborenenstation wird geschlossen. Es wird geprüft, welche Pflegeeinheit stattdessen eingerichtet werden kann.",
        "Lösung": "Die Intensivstation (2.03) könnte als Alternative dienen, da sie ähnliche technische Anforderungen wie Klimatisierung und Raumlufttechnik hat. Ein Stillzimmer könnte eingerichtet werden, und die Ausstattung für Neugeborene müsste ergänzt werden."
    },
    "Szenario 2": {
        "Beschreibung": "Personalmangel: Stationen müssen zusammengelegt werden. Es wird geprüft, welche Bereiche ähnliche Anforderungen haben.",
        "Lösung": "Die Allgemeine Pflege (2.01) und die Geriatrie könnten zusammengelegt werden. Gemeinsam genutzte Ressourcen wie Medikamentenräume und Personalaufenthaltsräume können die Effizienz steigern."
    },
    "Szenario 3": {
        "Beschreibung": "Pandemie: Es besteht ein erhöhter Bedarf an Intensivmedizin und Isolierstationen.",
        "Lösung": "Allgemeine Pflegezimmer (z. B. 3-Bett-Zimmer) könnten in temporäre Isoliereinheiten umgewandelt werden. Die Stroke Unit und Chest-Pain-Unit innerhalb der Intensivstation könnten erweitert werden, da diese bereits über spezialisierte Technik verfügen."
    },
    "Szenario 4": {
        "Beschreibung": "Umbau: Während einer Gebäuderenovierung muss eine Station vorübergehend verlagert werden.",
        "Lösung": "Räume der Tagesklinik oder Rehabilitation könnten temporär genutzt werden. Nicht genutzte Lagerbereiche könnten für die Lagerung von Technik und Möbeln während des Umbaus verwendet werden."
    }
}

# Umwandeln in DataFrame für Anzeige
pflege_df = []
for teilstelle in pflege_teilstellen:
    for raum in teilstelle["Räume"]:
        pflege_df.append({"Teilstelle": teilstelle["Teilstelle"], **raum})

pflege_df = pd.DataFrame(pflege_df)

# Streamlit-Anzeige
st.title("Funktionsbereich Pflege - Übersicht und Szenarien")

# Anzeige der Tabelle aller Teilstellen und Räume
st.header("📋 Übersicht der Teilstellen und Räume")
st.dataframe(pflege_df)

# Szenarien anzeigen
st.header("📌 Szenarien und Lösungen")
for name, details in szenarien.items():
    st.subheader(name)
    st.write("**Beschreibung:**", details["Beschreibung"])
    st.write("**Lösungsvorschlag:**", details["Lösung"])

# Interaktive Filter
st.header("🔍 Anforderungen filtern")
min_flaeche = st.slider("Minimale Fläche (m²):", 0, 50, 15)
spezialtechnik = st.checkbox("Nur mit spezieller Technik anzeigen")

ergebnis = pflege_df[
    (pflege_df["Raumgrößen"].str.extract(r'(\d+)').astype(int) >= min_flaeche).any(axis=1) &
    (pflege_df["Technik"].str.contains("Spezial") if spezialtechnik else True)
]

st.subheader("Gefilterte Ergebnisse")
st.dataframe(ergebnis)

# Interaktive Karte
st.header("📍 Interaktive Krankenhauskarte")

# Standard-Koordinaten für Beispielkarte
m = folium.Map(location=[52.52, 13.405], zoom_start=15)

# Beispielpunkte hinzufügen
stationen = {
    "Allgemeine Pflege": [52.522, 13.404],
    "Neugeborenenstation": [52.523, 13.405],
    "Intensivstation": [52.521, 13.406]
}

for name, coord in stationen.items():
    folium.Marker(coord, popup=name, tooltip=name).add_to(m)

# Karte in Streamlit anzeigen
st_data = st_folium(m, width=700, height=500)

