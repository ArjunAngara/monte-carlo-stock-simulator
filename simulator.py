# Monte Carlo Stock Simulator

import yfinance as yf
import numpy as np

stock = "AAPL"

print(f"Fetching data for {stock}...")
data = yf.download(stock, period="1y", interval="1d", progress=False)

close = data["Close"]

# calculate daily returns and volatility
daily_returns = close.pct_change().dropna()
mean_return = float(daily_returns.mean())
volatility = float(daily_returns.std())
current_price = float(close.iloc[-1])

print(f"Current price: ${round(current_price, 2)}")

# run 1000 simulations and store all final prices
days = 30
simulations = 1000
final_prices = []

print(f"\nRunning {simulations} simulations over {days} days...")

for sim in range(simulations):
    prices = [current_price]
    for _ in range(days):
        random_return = np.random.normal(mean_return, volatility)
        next_price = prices[-1] * (1 + random_return)
        prices.append(next_price)
    final_prices.append(round(prices[-1], 2))

print(f"Simulations complete")
print(f"Average final price: ${round(sum(final_prices) / len(final_prices), 2)}")
print(f"Highest final price: ${max(final_prices)}")
print(f"Lowest final price: ${min(final_prices)}")
