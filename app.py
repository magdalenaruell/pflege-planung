import streamlit as st
import pandas as pd

# 🏥 Titelbild zentriert anzeigen mit HTML & CSS
st.markdown(
    """
    <div style="text-align: center;">
        <img src="IMG_0728.PNG" style="width: 50%; max-width: 600px;">
    </div>
    """, 
    unsafe_allow_html=True
)

# Titel der Anwendung
st.title("🏥 MediMetrics")

# 📂 Datei-Upload oder Fallback auf feste Datei
uploaded_file = st.file_uploader("📂 Laden Sie eine Excel-Datei hoch oder verwenden Sie die Standarddatei", type=["xlsx"])
file_path = "Allin13_WebAnwendung_250128_NBO_DIN.xlsx"  # Fallback-Datei

if uploaded_file is not None:
    xls = pd.ExcelFile(uploaded_file)
    st.info("✅ Eigene hochgeladene Datei wird verwendet.")
else:
    try:
        xls = pd.ExcelFile(file_path)
        st.info(f"ℹ️ Keine Datei hochgeladen. Verwende die Standarddatei: {file_path}")
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Standarddatei: {str(e)}")
        st.stop()

# ✅ **Lese alle Tabellenblätter aus der gewählten Datei**
try:
    sheets = pd.read_excel(xls, sheet_name=None)  # `None` lädt alle Tabellenblätter
    
    if not sheets:
        st.error("❌ Die Excel-Datei enthält keine Tabellenblätter.")
        st.stop()
    
    # Zeige alle verfügbaren Tabellenblätter als Multi-Select
    st.subheader("📄 Wählen Sie die Tabellenblätter aus:")
    
    if "selected_sheets" not in st.session_state:
        st.session_state.selected_sheets = []  
    
    selected_sheets = st.multiselect("🔍 Wählen Sie die Tabellenblätter:", list(sheets.keys()), default=st.session_state.selected_sheets)

    st.session_state.selected_sheets = selected_sheets

    # Zeige die Daten für die ausgewählten Tabellenblätter
    if selected_sheets:
        for sheet in selected_sheets:
            df_filtered = sheets[sheet]  
            st.subheader(f"📄 Alle Daten aus {sheet}")
            st.dataframe(df_filtered, use_container_width=True, height=600)

except Exception as e:
    st.error(f"❌ Fehler beim Laden der Excel-Datei: {str(e)}")
    st.stop()  # Programm an dieser Stelle beenden, falls ein Fehler auftritt

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

# ✅ **Vergleich der Tabellenblätter mit einer Referenz (3 oder 6)**
try:
    if "3" in sheets.keys() and "6" in sheets.keys():
        st.subheader("🔎 Wählen Sie ein Referenztabellenblatt (3 oder 6)")

        reference_sheet = st.selectbox("📌 Referenztabellenblatt wählen:", ["3", "6"])

        # Wähle ein Vergleichsblatt aus den bereits gewählten Tabellenblättern (ohne Referenz)
        available_comparison_sheets = [s for s in selected_sheets if s not in ["3", "6"]]

        if available_comparison_sheets:
            compare_sheet = st.selectbox("📊 Wählen Sie ein Tabellenblatt für den Vergleich:", available_comparison_sheets)

            # Lade die beiden zu vergleichenden Tabellenblätter
            df_reference = sheets[reference_sheet]
            df_compare = sheets[compare_sheet]

            # ✅ **Zeige die beiden Tabellenblätter nebeneinander**
            st.subheader(f"📌 Vergleich zwischen **{reference_sheet}** (Referenz) und **{compare_sheet}**")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f"📄 {reference_sheet} (Referenz)")
                st.dataframe(df_reference, use_container_width=True, height=600)

            with col2:
                st.subheader(f"📄 {compare_sheet} (Vergleich)")
                st.dataframe(df_compare, use_container_width=True, height=600)

            # ✅ **Vergleiche Unterschiede zwischen den beiden Tabellen**
            st.subheader("📊 Unterschiede zwischen den Tabellen")

            if df_reference.shape != df_compare.shape:
                st.warning("⚠️ Die Tabellen haben unterschiedliche Dimensionen! Unterschiede sind möglicherweise schwer vergleichbar.")

            # Finde Spalten, die in beiden Tabellen existieren
            common_columns = list(set(df_reference.columns) & set(df_compare.columns))

            if common_columns:
                differences = df_reference[common_columns].compare(df_compare[common_columns])

                if not differences.empty:
                    st.warning("⚠️ Es gibt Unterschiede in den gemeinsamen Spalten!")
                    st.dataframe(differences, use_container_width=True)
                else:
                    st.success("✅ Die Tabellen sind in den gemeinsamen Spalten identisch.")
            else:
                st.error("❌ Keine gemeinsamen Spalten gefunden. Vergleich nicht möglich.")

        else:
            st.warning("⚠️ Kein weiteres Tabellenblatt ausgewählt, das mit der Referenz verglichen werden kann.")
except Exception as e:
    st.error(f"❌ Fehler beim Vergleich der Tabellenblätter: {str(e)}")

# 📊 **Vergleichsmöglichkeit für alle ausgewählten Tabellenblätter**
if selected_sheets:
    st.subheader("📊 Wählen Sie die Spalten, die Sie vergleichen möchten")

    all_columns = []
    for sheet in selected_sheets:
        all_columns.extend(sheets[sheet].columns)

    all_columns = list(set(all_columns))

    compare_options = st.multiselect("🔍 Spalten auswählen:", all_columns)

    if compare_options:
        st.subheader("📊 Vergleich der gewählten Spalten")
        combined_data = pd.concat([sheets[sheet][compare_options] for sheet in selected_sheets], ignore_index=True)
        st.dataframe(combined_data, use_container_width=True, height=600)

