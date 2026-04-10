import yfinance as yf
import pandas as pd

df = yf.Ticker("AAPL")
print(df.history().describe())