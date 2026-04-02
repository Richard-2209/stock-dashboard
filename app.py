import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

ticker = None  # Initialize ticker variable


def main():
    st.set_page_config(page_title="Stock Dashboard", layout="wide")

    # -----------------------------
    # Titel und Beschreibung
    # -----------------------------
    st.title("Stock Dashboard")
    st.write("Wähle eine Aktie und einen time_range aus, um den Kursverlauf zu analysieren.")

    # -----------------------------
    # Eingaben
    # -----------------------------
    st.sidebar.header("Einstellungen")

    ticker = st.sidebar.selectbox(
        "Type stock", input("Type stock"))
    time_range = st.sidebar.selectbox(
        "time_range auswählen",
        ["1mo", "6mo", "1y", "5y"],
        index=0  # Default to the first option
    )

    # -----------------------------
    # Daten laden
    # -----------------------------
    df = yf.download(ticker, period=time_range)

    # -----------------------------
    # Daten prüfen
    if ticker:
        df = yf.download(ticker, period=time_range)
    else:
        df = None
    if df.empty:
        st.error("Keine Daten gefunden. Bitte wähle einen anderen Ticker oder time_range.")
    else:
        st.subheader("Rohdaten")
        st.dataframe(df.tail())

        # -----------------------------
        # Kennzahlen berechnen
        # -----------------------------
        aktueller_kurs = df["Close"].iloc[-1]
        hoch = df["Close"].max()
        tief = df["Close"].min()
        durchschnitt = df["Close"].mean()
        veraenderung = ((df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]) * 100

        # -----------------------------
        # Kennzahlen anzeigen
        # -----------------------------
        st.subheader("Kennzahlen")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Aktueller Kurs", f"{aktueller_kurs:.2f}")
        col2.metric("Hoch", f"{hoch:.2f}")
        col3.metric("Tief", f"{tief:.2f}")
        col4.metric("Durchschnitt", f"{durchschnitt:.2f}")

        st.write(f"Veränderung im time_range: {veraenderung:.2f}%")

        # -----------------------------
        # Diagramm
        # -----------------------------
        st.subheader("Kursverlauf")
        fig, ax = plt.subplots()
        ax.plot(df.index, df["Close"])
        ax.set_xlabel("Datum")
        ax.set_ylabel("Schlusskurs")
        ax.set_title(f"{ticker} - Kursverlauf")
        st.pyplot(fig)

        # -----------------------------
        # Einfache Interpretation
        # -----------------------------
        st.subheader("Kurzinterpretation")
        if veraenderung > 0:
            st.write("Die Aktie ist im gewählten time_range insgesamt gestiegen.")
        elif veraenderung < 0:
            st.write("Die Aktie ist im gewählten time_range insgesamt gefallen.")
        else:
            st.write("Die Aktie hat sich im gewählten time_range kaum verändert.")