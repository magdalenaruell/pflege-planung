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


# 📂 **Excel-Datei laden**
file_path = "Allin13_WebAnwendung_250128_NBO_DIN.xlsx"

try:
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    st.success(f"📄 Excel-Datei erfolgreich geladen: `{file_path}`")
except Exception as e:
    st.error(f"❌ Fehler beim Laden der Datei: {str(e)}")
    st.stop()
    
xls = pd.ExcelFile("Allin13_WebAnwendung_250128_NBO_DIN.xlsx")
print(xls.sheet_names)  # Gibt eine Liste der Tabellenblattnamen zurück

# 📊 **Erstellung eines Dictionary mit Tabellenblatt-Namen**
sheets_dict = {index: name for index, name in enumerate(sheet_names)}
st.write("📌 **Verfügbare Tabellenblätter:**")
st.json(sheets_dict)  # Zeigt das Dictionary an

# 📄 **Tabellenblatt auswählen**
st.subheader("📄 Wählen Sie ein Tabellenblatt aus")
selected_sheet_key = st.selectbox("🔍 Wählen Sie ein Tabellenblatt:", list(sheet_dict.keys()), format_func=lambda x: sheet_dict[x], key="sheet_select")
selected_sheet_name = sheet_dict[selected_sheet_key]

# Daten anzeigen, aber nur für das aktuell ausgewählte Tabellenblatt
if selected_sheet_name:
    st.subheader(f"📄 Daten aus: {selected_sheet_name}")
    df = pd.read_excel(xls, sheet_name=selected_sheet_name)
    st.dataframe(df, use_container_width=True, height=400)


# 📄 **Zweites Tabellenblatt auswählen**
st.subheader("📄 Wählen Sie das zweite Tabellenblatt aus")
second_sheet_key = st.selectbox("🔍 Wählen Sie das zweite Tabellenblatt:", list(sheets_dict.keys()), index=1, format_func=lambda x: sheets_dict[x])
second_sheet_name = sheets_dict[second_sheet_key]
df2 = pd.read_excel(xls, sheet_name=second_sheet_name)

st.subheader(f"📄 Daten aus: {second_sheet_name}")
st.dataframe(df2, use_container_width=True, height=400)

# 🔎 **Vergleich der Tabellenblätter auf Basis von Spalte B**
if not df1.empty and not df2.empty:
    st.subheader("📊 Vergleich der gewählten Tabellenblätter nach Spalte B")
    
    if df1.shape[1] < 2 or df2.shape[1] < 2:
        st.error("❌ Mindestens eine der Tabellen hat nicht genügend Spalten für den Vergleich.")
        st.stop()
    
    column_b = df1.columns[1]  # Explizit Spalte B (Index 1)
    df1_grouped = df1.set_index(column_b)
    df2_grouped = df2.set_index(column_b)
    common_titles = df1_grouped.index.intersection(df2_grouped.index)
    
    comparison_results = []
    for title in common_titles:
        row1 = df1_grouped.loc[title]
        row2 = df2_grouped.loc[title]

        row1 = row1.to_frame().T if isinstance(row1, pd.Series) else row1
        row2 = row2.to_frame().T if isinstance(row2, pd.Series) else row2
        
        row_styles = []
        for col in row1.columns:
            if col not in row2.columns:
                continue
            val1, val2 = row1[col].values[0], row2[col].values[0]
            
            if pd.isna(val1) and pd.isna(val2):
                row_styles.append(f"<td>{val1}</td>")
            elif val1 == val2:
                row_styles.append(f"<td style='background-color: #90EE90;'>{val1}</td>")
            else:
                row_styles.append(f"<td style='background-color: #FF4500; font-weight:bold;'>{val1} | {val2}</td>")
        
        match_status = "✅" if all("#90EE90" in s for s in row_styles) else "🟠" if any("#FF4500" in s for s in row_styles) else "🔴"
        comparison_results.append((match_status, title, row_styles))
    
    if comparison_results:
        styled_rows = [f"<tr><td>{status}</td><td>{title}</td>{''.join(row_styles)}</tr>" for status, title, row_styles in comparison_results]
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
