import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


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
st.write("Analysiere Aktienkurse und Unternehmensdaten in einem einfachen Dashboard.")


# --------------------------------------------------
# Sidebar: Eingaben
# --------------------------------------------------
st.sidebar.header("Einstellungen")

ticker = st.sidebar.selectbox(
    "Wähle einen Ticker",
    ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
)

period = st.sidebar.selectbox(
    "Wähle einen Zeitraum",
    ["1mo", "6mo", "1y", "5y"]
)


# --------------------------------------------------
# Daten laden
# --------------------------------------------------
@st.cache_data
def load_stock_data(ticker_symbol, selected_period):
    df = yf.download(
        ticker_symbol,
        period=selected_period,
        multi_level_index=False
    )
    return df


df = load_stock_data(ticker, period)


# --------------------------------------------------
# Daten prüfen
# --------------------------------------------------
if df.empty:
    st.error("Keine Daten gefunden. Bitte versuche einen anderen Ticker oder Zeitraum.")
    st.stop()

if "Close" not in df.columns:
    st.error("Die Close-Spalte wurde nicht gefunden.")
    st.stop()


# --------------------------------------------------
# Close-Spalte sicher als Series behandeln
# --------------------------------------------------
close_series = df["Close"]

if isinstance(close_series, pd.DataFrame):
    close_series = close_series.iloc[:, 0]

close_series = pd.to_numeric(close_series, errors="coerce").dropna()

if close_series.empty:
    st.error("Keine gültigen Schlusskurse gefunden.")
    st.stop()


# --------------------------------------------------
# Grundlayout
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Überblick", "Kursdaten", "Unternehmensinfos"])


# --------------------------------------------------
# Tab 1: Überblick
# --------------------------------------------------
with tab1:
    st.subheader("Kennzahlen")

    current_price = float(close_series.iloc[-1])
    max_price = float(close_series.max())
    min_price = float(close_series.min())
    avg_price = float(close_series.mean())

    if len(close_series) > 1:
        pct_change = ((close_series.iloc[-1] - close_series.iloc[0]) / close_series.iloc[0]) * 100
        pct_change = float(pct_change)
    else:
        pct_change = 0.0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Aktueller Kurs", f"{current_price:.2f}")
    col2.metric("Hoch", f"{max_price:.2f}")
    col3.metric("Tief", f"{min_price:.2f}")
    col4.metric("Durchschnitt", f"{avg_price:.2f}")

    st.metric("Veränderung im Zeitraum", f"{pct_change:.2f}%")

    st.subheader("Kursverlauf")

    fig, ax = plt.subplots()
    ax.plot(close_series.index, close_series)
    ax.set_title(f"{ticker} - Schlusskurs")
    ax.set_xlabel("Datum")
    ax.set_ylabel("Preis")
    st.pyplot(fig)

    st.subheader("Kurzinterpretation")

    if len(close_series) > 1:
        if pct_change > 0:
            st.write("Die Aktie ist im gewählten Zeitraum insgesamt gestiegen.")
        elif pct_change < 0:
            st.write("Die Aktie ist im gewählten Zeitraum insgesamt gefallen.")
        else:
            st.write("Die Aktie hat sich im gewählten Zeitraum kaum verändert.")
    else:
        st.write("Für den gewählten Zeitraum sind zu wenige Daten für eine Interpretation vorhanden.")


# --------------------------------------------------
# Tab 2: Kursdaten
# --------------------------------------------------
with tab2:
    st.subheader("Rohdaten")
    st.dataframe(df)

    st.subheader("Letzte Beobachtungen")
    st.dataframe(df.tail())


# --------------------------------------------------
# Tab 3: Unternehmensinfos
# --------------------------------------------------
with tab3:
    st.subheader("Unternehmensinformationen")

    st.write("Hier kannst du später weitere Informationen ergänzen, zum Beispiel:")
    st.write("- Firmenname")
    st.write("- Branche")
    st.write("- Marktkapitalisierung")
    st.write("- KGV")
    st.write("- Umsatz / Gewinn")
    st.write("- Geschäftsmodell / Kurzbeschreibung")

    # Platzhalter:
    # company = yf.Ticker(ticker)
    # info = company.info
    # Danach einzelne Kennzahlen aus info ziehen und anzeigen.


# --------------------------------------------------
# Footer / Nächste Schritte
# --------------------------------------------------
st.markdown("---")
st.write("Nächste sinnvolle Erweiterungen:")
st.write("1. Zweiten Ticker zum Vergleich hinzufügen")
st.write("2. Volumen als weiteren Plot einbauen")
st.write("3. Unternehmenskennzahlen aus yfinance ergänzen")
st.write("4. Zeitraum flexibler machen")