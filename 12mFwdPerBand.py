import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define stock ticker
ticker = "AMZN"  # Change this to your stock symbol
stock = yf.Ticker(ticker)

# Fetch historical stock prices (last 12 months)
df = stock.history(period="12mo")
dates = df.index
stock_price = df["Close"]

# Forward EPS (replace with real forward EPS estimates)
eps_fwd =  stock.info['forwardPE'] 

# Calculate current PER
current_price = stock_price.iloc[-1]  # Most recent stock price
current_per = current_price / eps_fwd

# Define PER levels (Current PER ±5 and ±10)
per_levels = [current_per*0.7, current_per*0.9, current_per, current_per*1.1 , current_per*1.3]

# Choose a starting price for all PER bands (first stock price)
start_price = stock_price.iloc[0]

# Generate PER bands with different slopes
time = np.linspace(0, 1, len(dates))  # Normalize time from 0 to 1
band_prices = {per: start_price + (eps_fwd * per - start_price) * time for per in per_levels}

# Plot stock price
plt.figure(figsize=(10, 5))
plt.plot(dates, stock_price, label="Stock Price", color="blue", linewidth=2)

# Plot PER bands (same start, different slopes)
for per, prices in band_prices.items():
    plt.plot(dates, prices, linestyle="dashed", label=f"PER {per:.1f}x", alpha=0.6)

plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.title(f"{ticker} 12M Forward PER Band")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()
