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

# 📂 Standard-Excel-Datei laden
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

# ✅ **Nur die ausgewählten Tabellenblätter separat anzeigen & vergleichen**
dataframes = {}

for sheet in selected_sheets:
    try:
        df = pd.read_excel(xls, sheet_name=sheet)
        dataframes[sheet] = df  # Speichert nur die ausgewählten Tabellen
    except Exception as e:
        st.error(f"❌ Fehler beim Laden des Tabellenblatts '{sheet}': {str(e)}")

# **Jetzt wirklich nur die ausgewählten Blätter einzeln anzeigen**
for sheet, df in dataframes.items():
    st.subheader(f"📄 Daten aus: {sheet}")  # **Jedes Blatt wird separat betitelt**
    st.dataframe(df, use_container_width=True, height=400)  # **Zeigt nur das jeweilige Blatt**

# 🔎 **Vergleich der Tabellenblätter auf Basis von Spalte B (2. Spalte)**
if len(selected_sheets) >= 2:
    st.subheader("📊 Vergleich der ausgewählten Tabellenblätter nach Spalte B")

    # Jedes Tabellenblatt bleibt für sich – KEIN Zusammenfügen!
    comparison_results = []
    for sheet, df in dataframes.items():
        if df.shape[1] > 1:  # Sicherstellen, dass mindestens zwei Spalten existieren
            df = df.iloc[:, :].copy()  # Kopie, um Änderungen zu vermeiden

            # Falls Spalte B fehlt, stoppen
            if df.shape[1] < 2:
                st.error(f"❌ Spalte B fehlt in '{sheet}'. Überprüfen Sie das Tabellenblatt.")
                continue

            column_b = df.columns[1]  # **Jetzt wird explizit Spalte B (Index 1) genommen**

            grouped = df.groupby(column_b)

            for title, group in grouped:
                unique_rows = group.drop_duplicates().reset_index(drop=True)

                # Prüfe Übereinstimmungen Zelle für Zelle
                row_styles = []
                for col in unique_rows.columns[2:]:  # Ab Spalte 3
                    if unique_rows[col].nunique() == 1:
                        row_styles.append(f"<td style='background-color: #90EE90;'>{unique_rows[col].values[0]}</td>")  # Grün
                    elif unique_rows[col].nunique() > 1:
                        row_styles.append(f"<td style='background-color: #FF4500; font-weight:bold;'>{unique_rows[col].values[0]}</td>")  # Rot
                    else:
                        row_styles.append(f"<td>{unique_rows[col].values[0]}</td>")  # Standard

                match_status = "✅" if all("background-color: #90EE90;" in s for s in row_styles) else "🟠" if any("background-color: #FF4500;" in s for s in row_styles) else "🔴"

                comparison_results.append((match_status, title, row_styles))

    # **Ergebnisse formatieren und anzeigen**
    if comparison_results:
        styled_rows = []
        for status, title, row_styles in comparison_results:
            styled_row = f"<tr><td>{status}</td><td>{title}</td>{''.join(row_styles)}</tr>"
            styled_rows.append(styled_row)

        table_html = f"""
        <table class='compact-table'>
            <tr>
                <th>Vergleich</th>
                <th>Titel (Spalte B)</th>
                <th>Details</th>
            </tr>
            {''.join(styled_rows)}
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)
