import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Definition der Teilstellen des Funktionsbereichs Pflege mit spezifischen Zimmeranforderungen
pflege_teilstellen = [
    {
        "Teilstelle": "2.01 Allgemeine Pflege",
        "Räume": [
            {"Name": "Arztraum", "mind. Fläche (m²)": "12", "Technik": "Basisdiagnostik", "Sanitär": "Nein"},
            {"Name": "Dienstplatz", "mind. Fläche (m²)": "10", "Technik": "EDV-Anbindung", "Sanitär": "Nein"},
            {"Name": "Personalaufenthaltsräume", "mind. Fläche (m²)": "15", "Technik": "Optional", "Sanitär": "Ja"},
            {"Name": "Patientenzimmer (Einzel)", "mind. Fläche (m²)": "20", "Technik": "Klimatisierung, TV", "Sanitär": "Ja"}
        ],
        "mind. Raumbreite": "3m",
        "mind. Türbreite": "1.26m",
        "Fläche (m²)": "16-20",
        "Technik": "Klimatisierung, Raumlufttechnik",
        "Sanitär": "Bad an Bettenzimmer (WC, Waschbecken, Dusche)",
        "Besonderheiten": "Barrierefreiheit, erhöhte Hygieneanforderungen"
    },
    {
        "Teilstelle": "2.02 Neugeborenenstation",
        "Räume": [
            {"Name": "Pflege-Wöchnerinnen", "mind. Fläche (m²)": "18", "Technik": "Basisdiagnostik", "Sanitär": "Ja"},
            {"Name": "Stillzimmer", "mind. Fläche (m²)": "10", "Technik": "Optional", "Sanitär": "Ja"}
        ],
        "mind. Raumbreite": "3m",
        "mind. Türbreite": "1.30m",
        "Fläche (m²)": "15-18",
        "Technik": "Klimatisierung, Raumlufttechnik",
        "Sanitär": "Bad an Bettenzimmer (WC, Waschbecken, Dusche)",
        "Besonderheiten": "Spezielle Ausstattung für Neugeborene"
    },
    {
        "Teilstelle": "2.03 Intensivstation",
        "Räume": [
            {"Name": "Intensivtherapie", "mind. Fläche (m²)": "25", "Technik": "Spezialsteckdosen (Sauerstoff, Vakuum, Druckluft)", "Sanitär": "Ja"},
            {"Name": "Stroke Unit", "mind. Fläche (m²)": "20", "Technik": "Monitoring-System", "Sanitär": "Ja"}
        ],
        "mind. Raumbreite": "4m",
        "mind. Türbreite": "1.40m",
        "Fläche (m²)": "20-25",
        "Technik": "Spezialsteckdosen (Sauerstoff, Vakuum, Druckluft), Klimatisierung, Raumlufttechnik",
        "Sanitär": "Bad an Bettenzimmer (WC, Waschbecken, Dusche)",
        "Besonderheiten": "Isolationsmöglichkeiten, Überdruck- und Unterdrucksysteme"
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
pflege_df = pd.DataFrame(pflege_teilstellen)

# Streamlit-Anzeige
st.title("Funktionsbereich Pflege - Szenarien und Lösungen")

# Szenarien anzeigen
st.header("📌 Szenarien und Lösungen")
for name, details in szenarien.items():
    st.subheader(name)
    st.write("**Beschreibung:**", details["Beschreibung"])
    st.write("**Lösungsvorschlag:**", details["Lösung"])

st.header("📋 Anforderungen der Teilstellen im Funktionsbereich Pflege")
for teilstelle in pflege_teilstellen:
    st.subheader(teilstelle["Teilstelle"])
    st.write(pd.DataFrame(teilstelle["Räume"]))

# Interaktive Filter
st.header("🔍 Anforderungen filtern")
min_flaeche = st.slider("Minimale Fläche (m²):", 0, 50, 15)
spezialtechnik = st.checkbox("Nur mit spezieller Technik anzeigen")

ergebnis = [
    {
        "Teilstelle": teilstelle["Teilstelle"],
        "Räume": [raum for raum in teilstelle["Räume"] if int(raum["mind. Fläche (m²)"]) >= min_flaeche and (not spezialtechnik or "Spezial" in raum["Technik"])]
    }
    for teilstelle in pflege_teilstellen
]

st.subheader("Gefilterte Ergebnisse")
for res in ergebnis:
    st.subheader(res["Teilstelle"])
    st.write(pd.DataFrame(res["Räume"]))

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

