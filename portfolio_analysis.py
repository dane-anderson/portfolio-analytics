import pandas as pd
import yfinance as yf

# Load your portfolio
df = pd.read_csv("Portfolio.csv")

print("\nYour Portfolio:")
print(df)

# Get current stock prices
def get_price(ticker):
    ticker = str(ticker).strip().upper()
    print(f"Checking ticker: {repr(ticker)}")

    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")

        if history.empty:
            print(f"No price data found for {ticker}")
            return None

        return history["Close"].iloc[-1]

    except Exception as e:
        print(f"Error getting price for {ticker}: {e}")
        return None

# Apply price function
df["Current_Price"] = df["Ticker"].apply(get_price)

# Drop any bad tickers
df = df.dropna(subset=["Current_Price"])

# Calculate values
df["Position_Value"] = df["Shares"] * df["Current_Price"]
df["Cost_Basis"] = df["Shares"] * df["Buy_Price"]
df["Return_%"] = (df["Current_Price"] - df["Buy_Price"]) / df["Buy_Price"] * 100

print("\nUpdated Portfolio:")
print(df)

# Analysis
print("\nAverage Return by Category:")
print(df.groupby("Category")["Return_%"].mean())

print("\nAverage Return by Conviction:")
print(df.groupby("Conviction")["Return_%"].mean())

print("\nBest Performers:")
print(df.sort_values("Return_%", ascending=False)[["Ticker", "Return_%"]])

print("\nWorst Performers:")
print(df.sort_values("Return_%", ascending=True)[["Ticker", "Return_%"]])

# NEW SECTION 🔥
print("\nTotal Portfolio Value:")
print(df["Position_Value"].sum())

print("\nTop 3 Positions by Size:")
print(df.sort_values("Position_Value", ascending=False)[["Ticker", "Position_Value"]].head(3))
print("\nNumber of Trades by Category:")
print(df["Category"].value_counts())

print("\nNumber of Trades by Conviction:")
print(df["Conviction"].value_counts())
import matplotlib.pyplot as plt

# Average return by category
category_returns = df.groupby("Category")["Return_%"].mean()

category_returns.plot(kind="bar")
plt.title("Average Return by Category")
plt.ylabel("Return (%)")
plt.show()
# What if analysis: remove TikTok trades
no_tiktok = df[df["Category"] != "tiktok"]

print("\nPortfolio WITHOUT TikTok trades:")
print("Total Value:", no_tiktok["Position_Value"].sum())
print("Average Return:", no_tiktok["Return_%"].mean())
# Weighted return (real portfolio return)
weighted_return = (df["Position_Value"].sum() - df["Cost_Basis"].sum()) / df["Cost_Basis"].sum() * 100

print("\nREAL Portfolio Return (Weighted):")
print(weighted_return)

weighted_no_tiktok = (no_tiktok["Position_Value"].sum() - no_tiktok["Cost_Basis"].sum()) / no_tiktok["Cost_Basis"].sum() * 100

print("\nREAL Return WITHOUT TikTok:")
print(weighted_no_tiktok)
print("\nTOTAL INVESTED (Cost Basis):")
print(df["Cost_Basis"].sum())

print("\nCURRENT VALUE:")
print(df["Position_Value"].sum())

profit = df["Position_Value"].sum() - df["Cost_Basis"].sum()

print("\nTOTAL PROFIT ($):")
print(profit)
only_long = df[df["Category"] == "long"]

weighted_long = (only_long["Position_Value"].sum() - only_long["Cost_Basis"].sum()) / only_long["Cost_Basis"].sum() * 100

print("\nREAL Return ONLY Long Strategy:")
print(weighted_long)
print("\nTop 5 Positions by % of Portfolio:")
df["Weight_%"] = df["Position_Value"] / df["Position_Value"].sum() * 100
print(df.sort_values("Weight_%", ascending=False)[["Ticker", "Weight_%"]].head(5))
# Cap losses at -50% to simulate stop-loss discipline
df["Capped_Return_%"] = df["Return_%"].clip(lower=-50)

capped_weighted = (df["Position_Value"].sum() * (df["Capped_Return_%"].mean()/100))

print("\nCAPPED downside (simulated discipline):")
print("Avg Capped Return:", df["Capped_Return_%"].mean())
# Portfolio Analytics & Strategy Evaluation

## Overview
This project analyzes a personal investment portfolio using Python to evaluate strategy performance, decision-making patterns, and risk management.

## Key Insights

- **Long-term strategy significantly outperformed**
  - Long-only return: ~28.9%
  - Total portfolio return: ~4.9%

- **Speculative / trend-based trades underperformed**
  - "TikTok" category averaged negative returns

- **Concentration risk identified**
  - One position (GM) represented ~46% of total portfolio

- **Risk management improvement opportunity**
  - Applying simple downside controls improved average returns to ~5.45%

## Features

- Real-time stock price retrieval using `yfinance`
- Portfolio return calculations (weighted and average)
- Strategy-based performance analysis
- Trade categorization (long, speculative, etc.)
- Visualization of returns by category
- Scenario analysis:
  - Portfolio without speculative trades
  - Long-only strategy
  - Downside risk control simulation

## Technologies Used

- Python
- pandas
- yfinance
- matplotlib

## Example Output

- Portfolio return analysis
- Strategy comparison charts
- Risk-adjusted performance scenarios

## Key Takeaway

Data-driven analysis revealed that portfolio performance was driven by a strong core strategy, but diluted by over-allocation to lower-quality trades and lack of downside risk management.

## Future Improvements

- Add automated data ingestion
- Introduce portfolio optimization
- Apply machine learning for return prediction
- Build dashboard visualization