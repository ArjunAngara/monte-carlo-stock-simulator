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
print(f"Average daily return: {round(mean_return, 4)}")
print(f"Daily volatility: {round(volatility, 4)}")

# run 10 simulations and print each final price
days = 30
simulations = 10

print(f"\nRunning {simulations} simulations over {days} days...")

for sim in range(simulations):
    prices = [current_price]
    for _ in range(days):
        random_return = np.random.normal(mean_return, volatility)
        next_price = prices[-1] * (1 + random_return)
        prices.append(round(next_price, 2))
    print(f"  Simulation {sim + 1}: ${prices[-1]}")
