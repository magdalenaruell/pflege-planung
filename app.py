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
file_path = "Allin13_WebAnwendung_250128_NBO_DIN.xlsx"  # Feste Datei

try:
    xls = pd.ExcelFile(file_path)
    sheets = xls.sheet_names  # Liste der vorhandenen Tabellenblätter
    st.info(f"ℹ️ Standard-Excel-Datei geladen: {file_path}")
except Exception as e:
    st.error(f"❌ Fehler beim Laden der Standarddatei: {str(e)}")
    st.stop()

# 📄 **Tabellenblätter auswählen**
st.subheader("📄 Wählen Sie die relevanten Tabellenblätter aus")

if "selected_sheets" not in st.session_state:
    st.session_state.selected_sheets = []

selected_sheets = st.multiselect("🔍 Wählen Sie die Tabellenblätter:", sheets, default=st.session_state.selected_sheets)

# Falls keine Auswahl getroffen wurde
if not selected_sheets:
    st.warning("⚠️ Bitte wählen Sie mindestens ein Tabellenblatt aus.")
    st.stop()

# Speichert die Auswahl für spätere Sitzungen
st.session_state.selected_sheets = selected_sheets

# ✅ **Nur die ausgewählten Tabellenblätter anzeigen**
for sheet in selected_sheets:
    try:
        df_filtered = pd.read_excel(xls, sheet_name=sheet)
        st.subheader(f"📄 Daten aus: {sheet}")
        st.dataframe(df_filtered, use_container_width=True, height=600)
    except Exception as e:
        st.error(f"❌ Fehler beim Laden des Tabellenblatts '{sheet}': {str(e)}")

# ✅ **Vergleich der Tabellenblätter mit einer Referenz (3 oder 6)**
try:
    if "3" in sheets and "6" in sheets:
        st.subheader("🔎 Wählen Sie eine Referenz-Teilstelle")

        reference_sheet = st.selectbox("📌 Referenz-Tabellenblatt wählen:", ["3", "6"])

        # Wähle ein Vergleichsblatt aus den bereits gewählten Tabellenblättern (ohne Referenz)
        available_comparison_sheets = [s for s in selected_sheets if s not in ["3", "6"]]

        if available_comparison_sheets:
            compare_sheet = st.selectbox("📊 Wählen Sie eine Teilstelle für den Vergleich:", available_comparison_sheets)

            # Lade die beiden zu vergleichenden Tabellenblätter
            df_reference = pd.read_excel(xls, sheet_name=reference_sheet)
            df_compare = pd.read_excel(xls, sheet_name=compare_sheet)

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

