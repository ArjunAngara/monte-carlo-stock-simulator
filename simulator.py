# Monte Carlo Stock Simulator

import yfinance as yf
import numpy as np
import os
import datetime


def get_stock_data(stock, period="1y"):
    print(f"Fetching data for {stock}...")
    data = yf.download(stock, period=period, interval="1d", progress=False)
    return data["Close"]


def calculate_parameters(close):
    daily_returns = close.pct_change().dropna()
    mean_return = float(daily_returns.mean())
    volatility = float(daily_returns.std())
    current_price = float(close.iloc[-1])
    return mean_return, volatility, current_price


def run_simulation(current_price, mean_return, volatility, days=30, simulations=1000):
    final_prices = []
    all_paths = []

    for _ in range(simulations):
        prices = [current_price]
        for _ in range(days):
            random_return = np.random.normal(mean_return, volatility)
            prices.append(prices[-1] * (1 + random_return))
        final_prices.append(round(prices[-1], 2))
        all_paths.append(prices)

    return final_prices, all_paths


def save_csv(stock, final_prices):
    os.makedirs("output", exist_ok=True)
    filename = datetime.datetime.now().strftime(f"{stock}_simulation_%Y%m%d_%H%M%S.csv")
    filepath = os.path.join("output", filename)

    with open(filepath, "w") as f:
        f.write("Simulation,Final Price\n")
        for i, price in enumerate(final_prices):
            f.write(f"{i + 1},{price}\n")

    print(f"Results saved to {filepath}")


def print_summary(stock, current_price, final_prices, simulations):
    final_prices.sort()
    avg = round(sum(final_prices) / len(final_prices), 2)
    above = len([p for p in final_prices if p > current_price])
    below = len([p for p in final_prices if p < current_price])
    var_95 = final_prices[int(simulations * 0.05)]
    var_99 = final_prices[int(simulations * 0.01)]

    print("=" * 40)
    print(f"SIMULATION RESULTS — {stock}")
    print("=" * 40)
    print(f"Current Price: ${round(current_price, 2)}")
    print(f"Average Simulated Price: ${avg}")
    print(f"Highest: ${max(final_prices)}")
    print(f"Lowest: ${min(final_prices)}")
    print(f"Probability of Profit: {round((above / simulations) * 100, 2)}%")
    print(f"Probability of Loss: {round((below / simulations) * 100, 2)}%")
    print(f"Value at Risk (95%): ${var_95}")
    print(f"Value at Risk (99%): ${var_99}")


def compare_stocks(results):
    # compare all stocks and find the one with highest average simulated price
    print("\n" + "=" * 40)
    print("STOCK COMPARISON")
    print("=" * 40)
    for stock, avg, current in results:
        change = round(((avg - current) / current) * 100, 2)
        print(f"  {stock}: ${current} → ${avg} ({change:+.2f}%)")


stocks = ["AAPL", "MSFT", "TSLA", "NVDA"]
comparison_results = []

for stock in stocks:
    close = get_stock_data(stock)
    mean_return, volatility, current_price = calculate_parameters(close)
    final_prices, all_paths = run_simulation(current_price, mean_return, volatility)
    print_summary(stock, current_price, final_prices, 1000)
    save_csv(stock, final_prices)
    avg = round(sum(final_prices) / len(final_prices), 2)
    comparison_results.append((stock, avg, current_price))
    print()

compare_stocks(comparison_results)
