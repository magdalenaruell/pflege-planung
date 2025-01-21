import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Spezifische Daten der BG Unfallklinik Frankfurt am Main
bg_unfallklinik_daten = {
    "Standorte": {
        "Allgemeine Pflege": [50.0865, 8.6297],
        "Neugeborenenstation": [50.0867, 8.6300],
        "Intensivstation": [50.0869, 8.6295],
        "Tagesklinik": [50.0871, 8.6292],
        "Rehabilitation": [50.0863, 8.6299]
    },
    "Ressourcen": {
        "Freie Räume": [
            {"Name": "Zimmer A", "Fläche (m²)": 20, "Technik": "Klimatisierung, Raumlufttechnik", "Sanitär": "Ja"},
            {"Name": "Zimmer B", "Fläche (m²)": 18, "Technik": "Optional", "Sanitär": "Nein"}
        ],
        "Personalkapazitäten": "80% verfügbar"
    }
}

# Szenarien-Beschreibungen und Lösungsvorschläge mit Klinikdaten
szenarien = {
    "Szenario 1": {
        "Beschreibung": "Fehlendes Fachpersonal: Eine Neugeborenenstation wird geschlossen. Es wird geprüft, welche Pflegeeinheit stattdessen eingerichtet werden kann.",
        "Lösung": "Die Intensivstation (50.0869, 8.6295) könnte als Alternative dienen. Freie Räume wie Zimmer A können für zusätzliche Funktionen angepasst werden."
    },
    "Szenario 2": {
        "Beschreibung": "Personalmangel: Stationen müssen zusammengelegt werden. Es wird geprüft, welche Bereiche ähnliche Anforderungen haben.",
        "Lösung": "Die Allgemeine Pflege (50.0865, 8.6297) und die Tagesklinik (50.0871, 8.6292) könnten zusammengelegt werden. Freie Ressourcen können effizient genutzt werden."
    },
    "Szenario 3": {
        "Beschreibung": "Pandemie: Es besteht ein erhöhter Bedarf an Intensivmedizin und Isolierstationen.",
        "Lösung": "Allgemeine Pflegezimmer können temporär in Isoliereinheiten umgewandelt werden. Die Stroke Unit innerhalb der Intensivstation kann erweitert werden."
    },
    "Szenario 4": {
        "Beschreibung": "Umbau: Während einer Gebäuderenovierung muss eine Station vorübergehend verlagert werden.",
        "Lösung": "Räume der Rehabilitation (50.0863, 8.6299) könnten temporär genutzt werden. Lagerflächen könnten während des Umbaus für Technik und Möbel genutzt werden."
    }
}

# Streamlit-Anzeige
st.title("BG Unfallklinik Frankfurt am Main - Szenarien und Lösungen")

# Szenarien anzeigen
st.header("📌 Szenarien und Lösungen")
for name, details in szenarien.items():
    st.subheader(name)
    st.write("**Beschreibung:**", details["Beschreibung"])
    st.write("**Lösungsvorschlag:**", details["Lösung"])

st.header("📍 Interaktive Krankenhauskarte")

# Interaktive Karte der BG Unfallklinik Frankfurt
m = folium.Map(location=[50.0865, 8.6297], zoom_start=17)

# Standorte hinzufügen
for name, coord in bg_unfallklinik_daten["Standorte"].items():
    folium.Marker(coord, popup=name, tooltip=name).add_to(m)

# Karte in Streamlit anzeigen
st_data = st_folium(m, width=700, height=500)

# Ressourcenübersicht
st.header("🛠 Ressourcenübersicht")
for ressource in bg_unfallklinik_daten["Ressourcen"]["Freie Räume"]:
    st.write(ressource)

st.write("**Personalkapazitäten:**", bg_unfallklinik_daten["Ressourcen"]["Personalkapazitäten"])


