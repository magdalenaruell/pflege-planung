import streamlit as st
import pandas as pd

# 🏥 Titelbild laden und zentrieren
st.markdown(
    """
    <style>
    .centered-image {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Bild zentriert mit `st.image()` laden
st.markdown('<div class="centered-image">', unsafe_allow_html=True)
st.image("IMG_07283.PNG", width=300)  # Stelle sicher, dass das Bild im App-Ordner liegt
st.markdown('</div>', unsafe_allow_html=True)

# Titel der Anwendung
st.title("MediMetrics")

# 🦠 **Szenario Pandemie** (Schöner formatiert)
st.markdown("""
    <h3>🦠 Szenario: Pandemie</h3>
    <p style="font-size:18px; line-height:1.6;">
    Ein Krankenhaus erlebt eine massive Zunahme an Patienten aufgrund einer <b>hochansteckenden Atemwegserkrankung</b>, 
    die sich zu einer <b>Pandemie</b> ausgeweitet hat. Bei manchen Patienten löst die Krankheit einen 
    <span style="color:green;"><b>milden Verlauf</b></span> aus, bei anderen einen <span style="color:red;"><b>schwerwiegenden</b></span>.
    </p>
    
    <p style="font-size:18px;">
    Einige dieser Patienten benötigen <b>intensivmedizinische Betreuung</b>, während andere mit leichteren Symptomen isoliert werden müssen, 
    um eine weitere Verbreitung der Krankheit zu verhindern. Gleichzeitig müssen weiterhin Patienten mit anderen Erkrankungen versorgt werden, 
    wie <b>Unfallopfer, Herzinfarkt- oder Krebspatienten</b>, die ebenfalls auf lebenswichtige Behandlungen angewiesen sind.
    </p>
    
    <p style="font-size:18px;">
    Durch die Pandemie erhöht sich der Bedarf an Flächen der <b>Intensivmedizin (2.03)</b> und der <b>Isolationskrankenpflege (2.06)</b>. 
    Um eine ausreichende Versorgung zu schaffen, müssen kurzfristig und übergangsweise neue Flächen zur Verfügung gestellt werden, 
    die die Pflege von erkrankten Patienten sicherstellen. Dazu können kurzzeitig andere Flächen umgenutzt werden.
    </p>
    """, unsafe_allow_html=True)

# 📂 Standard-Excel-Datei laden (ohne Upload)
file_path = "Allin13_WebAnwendung_250128_NBO_DIN.xlsx"

try:
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    st.info(f"ℹ️ Standard-Excel-Datei geladen: {file_path}")
except Exception as e:
    st.error(f"❌ Fehler beim Laden der Standarddatei: {str(e)}")
    st.stop()

# 📄 **Tabellenblätter auswählen**
st.subheader("📄 Wählen Sie die relevanten Tabellenblätter aus")

selected_sheets = st.multiselect(
    "🔍 Wählen Sie die Tabellenblätter:",
    sheet_names,
    default=[]
)

# Falls keine Auswahl getroffen wurde, Warnung anzeigen und stoppen
if not selected_sheets:
    st.warning("⚠️ Bitte wählen Sie mindestens ein Tabellenblatt aus.")
    st.stop()

# ✅ **Nur die ausgewählten Tabellenblätter anzeigen & Daten sammeln**
dataframes = {}

for sheet in selected_sheets:
    try:
        df = pd.read_excel(xls, sheet_name=sheet)
        dataframes[sheet] = df
        st.subheader(f"📄 Daten aus: {sheet}")
        st.dataframe(df, use_container_width=True, height=600)
    except Exception as e:
        st.error(f"❌ Fehler beim Laden des Tabellenblatts '{sheet}': {str(e)}")

# ✅ **Vergleich der Tabellenblätter auf Basis von Spalte B**
if len(selected_sheets) >= 2:
    st.subheader("📊 Vergleich der ausgewählten Tabellenblätter")

    # Führe alle Tabellen zusammen basierend auf Spalte B
    merged_df = pd.concat(dataframes.values(), keys=dataframes.keys(), names=["Tabelle", "Index"])
    
    # Gruppiere nach Spalte B (Titel) und überprüfe Übereinstimmungen
    grouped = merged_df.groupby("B")

    comparison_results = []
    for title, group in grouped:
        unique_rows = group.drop_duplicates().reset_index(drop=True)

        if len(unique_rows) == 1:
            match_status = "✅"
            color = "green"
        elif unique_rows.iloc[:, 1:].nunique().sum() == 0:
            match_status = "🔴"
            color = "red"
        else:
            match_status = "🟠"
            color = "orange"

        comparison_results.append((match_status, title, unique_rows, color))

    # **Ergebnisse formatieren und anzeigen**
    styled_rows = []
    for status, title, rows, color in comparison_results:
        rows_html = rows.to_html(index=False, escape=False)
        styled_row = f"<tr style='background-color: {color};'><td>{status}</td><td>{title}</td><td>{rows_html}</td></tr>"
        styled_rows.append(styled_row)

    table_html = f"""
    <table border='1' style='border-collapse: collapse; width: 100%; text-align: left;'>
        <tr>
            <th>Vergleich</th>
            <th>Titel (Spalte B)</th>
            <th>Details</th>
        </tr>
        {''.join(styled_rows)}
    </table>
    """

    st.markdown(table_html, unsafe_allow_html=True)
