import streamlit as st
import yfinance as yf
import pandas as pd


# --------------------------------------------------
# Seitenkonfiguration
# --------------------------------------------------
st.set_page_config(
    page_title="Stock Dashboard",
    layout="wide"
)


# --------------------------------------------------
# Titel / Einleitung
# --------------------------------------------------
st.title("Stock Dashboard")
st.write("Gib ein Ticker-Kürzel ein und lade die zugehörigen Unternehmens- und Kursdaten.")


# --------------------------------------------------
# Sidebar: Eingaben
# --------------------------------------------------
st.sidebar.header("Einstellungen")

ticker = st.sidebar.text_input(
    "Wähle den Ticker",
    value="AAPL"
).upper()

period = st.sidebar.selectbox(
    "Wähle einen Zeitraum",
    ["1mo", "6mo", "1y", "5y"],
    index=2
)


# --------------------------------------------------
# Daten laden
# --------------------------------------------------
@st.cache_data
def load_stock_data(ticker_symbol, selected_period):
    stock = yf.Ticker(ticker_symbol)
    df = stock.history(period=selected_period)
    return df


# --------------------------------------------------
# Nur laden, wenn ein Ticker eingegeben wurde
# --------------------------------------------------
if not ticker.strip():
    st.warning("Bitte gib ein Ticker-Kürzel ein.")
    st.stop()

df = load_stock_data(ticker, period)


# --------------------------------------------------
# Daten prüfen
# --------------------------------------------------
if df.empty:
    st.error("Keine Daten gefunden. Prüfe das Ticker-Kürzel oder wähle einen anderen Zeitraum.")
    st.stop()


# --------------------------------------------------
# Grundlayout
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Überblick", "Kursdaten", "Unternehmensinfos"])


# --------------------------------------------------
# Tab 1: Überblick
# --------------------------------------------------
with tab1:
    st.subheader("Allgemeiner Überblick")

    st.write(f"**Ausgewählter Ticker:** {ticker}")
    st.write(f"**Gewählter Zeitraum:** {period}")
    st.write(f"**Anzahl der Datenpunkte:** {len(df)}")

    st.write("Hier kannst du später selbst ergänzen:")
    st.write("- Kennzahlen")
    st.write("- Performance-Berechnungen")
    st.write("- Renditen")
    st.write("- Volatilität")
    st.write("- eigene Interpretation")


# --------------------------------------------------
# Tab 2: Kursdaten
# --------------------------------------------------
with tab2:
    st.subheader("Rohdaten")
    st.dataframe(df)

    st.subheader("Letzte Beobachtungen")
    st.dataframe(df.tail())

    st.write("Hier kannst du später selbst ergänzen:")
    st.write("- eigene Filter")
    st.write("- bereinigte Daten")
    st.write("- zusätzliche Spalten")
    st.write("- eigene Charts")


# --------------------------------------------------
# Tab 3: Unternehmensinfos
# --------------------------------------------------
with tab3:
    st.subheader("Unternehmensinformationen")

    try:
        info = yf.Ticker(ticker).info

        st.write(f"**Name:** {info.get('longName', 'Nicht verfügbar')}")
        st.write(f"**Sektor:** {info.get('sector', 'Nicht verfügbar')}")
        st.write(f"**Branche:** {info.get('industry', 'Nicht verfügbar')}")
        st.write(f"**Land:** {info.get('country', 'Nicht verfügbar')}")
        st.write(f"**Währung:** {info.get('currency', 'Nicht verfügbar')}")

    except Exception:
        st.warning("Unternehmensinformationen konnten momentan nicht geladen werden.")


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.write("Dieses Gerüst ist bewusst einfach gehalten, damit du Analytics und Visualisierungen selbst ergänzen kannst.")