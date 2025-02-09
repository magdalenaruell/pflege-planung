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

# 📄 **Erstes Tabellenblatt auswählen**
st.subheader("📄 Wählen Sie das erste Tabellenblatt aus")
first_sheet = st.selectbox("🔍 Wählen Sie das erste Tabellenblatt:", sheet_names)

# ✅ **Erstes Tabellenblatt anzeigen**
df1 = pd.read_excel(xls, sheet_name=first_sheet)
st.subheader(f"📄 Daten aus: {first_sheet}")
st.dataframe(df1, use_container_width=True, height=400)

# 📄 **Zweites Tabellenblatt auswählen**
st.subheader("📄 Wählen Sie das zweite Tabellenblatt aus")
second_sheet = st.selectbox("🔍 Wählen Sie das zweite Tabellenblatt:", sheet_names, index=1)

# ✅ **Zweites Tabellenblatt anzeigen**
df2 = pd.read_excel(xls, sheet_name=second_sheet)
st.subheader(f"📄 Daten aus: {second_sheet}")
st.dataframe(df2, use_container_width=True, height=400)

# 🔎 **Vergleich der Tabellenblätter auf Basis von Spalte B**
if first_sheet and second_sheet:
    st.subheader("📊 Vergleich der gewählten Tabellenblätter nach Spalte B")

    # Sicherstellen, dass beide Tabellen mindestens zwei Spalten haben
    if df1.shape[1] < 2 or df2.shape[1] < 2:
        st.error("❌ Mindestens eine der Tabellen hat nicht genügend Spalten für den Vergleich.")
        st.stop()

    column_b = df1.columns[1]  # **Jetzt wird explizit Spalte B (Index 1) genommen**

    # Gruppiere nach Spalte B (Titel)
    df1_grouped = df1.set_index(column_b)
    df2_grouped = df2.set_index(column_b)

    common_titles = df1_grouped.index.intersection(df2_grouped.index)  # Gemeinsame Titel aus Spalte B

    comparison_results = []
    for title in common_titles:
        row1 = df1_grouped.loc[title]
        row2 = df2_grouped.loc[title]

        # Falls nur eine Zeile pro Titel vorhanden ist, setze es als DataFrame
        if isinstance(row1, pd.Series):
            row1 = row1.to_frame().T
        if isinstance(row2, pd.Series):
            row2 = row2.to_frame().T

        # Bereite den Vergleich vor
        row_styles = []
        for col in row1.columns:
            if col not in row2.columns:
                continue  # Falls Spalten nicht übereinstimmen, überspringen

            val1 = row1[col].values[0]
            val2 = row2[col].values[0]

            if pd.isna(val1) and pd.isna(val2):  # Beide sind NaN
                row_styles.append(f"<td>{val1}</td>")
            elif val1 == val2:  # Werte sind identisch
                row_styles.append(f"<td style='background-color: #90EE90;'>{val1}</td>")  # Grün
            elif val1 != val2:  # Werte sind unterschiedlich
                row_styles.append(f"<td style='background-color: #FF4500; font-weight:bold;'>{val1} | {val2}</td>")  # Rot
            else:
                row_styles.append(f"<td>{val1}</td>")

        # Bestimme das Gesamtergebnis für die Zeile (Grün = alles gleich, Orange = teilweise, Rot = alles unterschiedlich)
        if all("background-color: #90EE90;" in s for s in row_styles):
            match_status = "✅"
            color = "green"
        elif any("background-color: #FF4500;" in s for s in row_styles):
            match_status = "🟠"
            color = "orange"
        else:
            match_status = "🔴"
            color = "red"

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
