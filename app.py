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


# 🔗 GitHub-Repository, in dem die Excel-Dateien liegen
GITHUB_BASE_URL = "https://raw.githubusercontent.com/user/repository/main/"  # <-- ÄNDERE das Repo

# 📂 Liste der Excel-Dateien im GitHub-Repo (MUSS manuell gepflegt werden oder mit einer API automatisiert werden)
EXCEL_FILES = [
    "01_WebAnwendung_250128_NBO_DIN.xlsx",
    "02_WebAnwendung_250128_NBO_DIN.xlsx",
    "03_WebAnwendung_250128_NBO_DIN.xlsx",
    "04_WebAnwendung_250128_NBO_DIN.xlsx",
    "05_WebAnwendung_250128_NBO_DIN.xlsx",
    "06_WebAnwendung_250128_NBO_DIN.xlsx",
    "07_WebAnwendung_250128_NBO_DIN.xlsx",
    "08_WebAnwendung_250128_NBO_DIN.xlsx",
    "09_WebAnwendung_250128_NBO_DIN.xlsx",
    "10_WebAnwendung_250128_NBO_DIN.xlsx",
    "11_WebAnwendung_250128_NBO_DIN.xlsx",
    "12_WebAnwendung_250128_NBO_DIN.xlsx",
    "13_WebAnwendung_250128_NBO_DIN.xlsx",
    "14_WebAnwendung_250128_NBO_DIN.xlsx",
]

# 📌 **Excel-Datei auswählen**
st.subheader("📂 Wähle eine Excel-Datei")
selected_file = st.selectbox("📑 Wähle eine Datei:", EXCEL_FILES)

if selected_file:
    file_url = GITHUB_BASE_URL + selected_file  # URL zur Datei generieren

    try:
        # Lade die Excel-Datei direkt aus GitHub
        xls = pd.ExcelFile(file_url)
        sheet_names = xls.sheet_names
        st.success(f"📄 Datei erfolgreich geladen: `{selected_file}`")
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Datei: {str(e)}")
        st.stop()
    
    # 📊 **Tabellenblatt auswählen**
    st.subheader("📄 Wähle ein Tabellenblatt")
    selected_sheet = st.selectbox("📄 Tabellenblatt:", sheet_names)

    # 📊 **Daten aus dem gewählten Tabellenblatt anzeigen**
    if selected_sheet:
        df = pd.read_excel(xls, sheet_name=selected_sheet)
        st.subheader(f"📊 Daten aus: {selected_sheet} in `{selected_file}`")
        st.dataframe(df, use_container_width=True, height=500)
    

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
