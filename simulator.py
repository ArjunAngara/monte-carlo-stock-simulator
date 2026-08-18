# Monte Carlo Stock Simulator

import yfinance as yf
import numpy as np

stock = "AAPL"

print(f"Fetching data for {stock}...")
data = yf.download(stock, period="1y", interval="1d", progress=False)

close = data["Close"]

# calculate daily returns
daily_returns = close.pct_change().dropna()

print(f"Average daily return: {round(float(daily_returns.mean()), 4)}")
print(f"Daily volatility: {round(float(daily_returns.std()), 4)}")
