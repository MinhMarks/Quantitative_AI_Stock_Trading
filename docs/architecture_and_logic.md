# Architecture and Strategy Logic

## System Architecture

The project is structured into modular components to separate concerns:

1.  **Data Layer (`data_loader.py`)**:
    -   Handles communication with Yahoo Finance API via `yfinance`.
    -   Manages local caching (CSV files) to avoid redundant network calls.
    -   Specifically handles `MultiIndex` columns often returned by newer `yfinance` versions.

2.  **Feature Layer (`features.py`)**:
    -   Computes technical indicators.
    -   **SMA (Simple Moving Average)**: Used for trend identification.
    -   **RSI (Relative Strength Index)**: Momentum oscillator to identify overbought/oversold conditions.
    -   **MACD**: Trend-following momentum indicator.
    -   **Volatility**: Rolling standard deviation of log returns.

3.  **Strategy Layer (`strategies.py`)**:
    -   **Base Class**: Abstract base class defining the `generate_signals` interface.
    -   **MA Crossover**: A rule-based strategy.
        -   *Logic*: Buy when SMA_50 > SMA_200 (Golden Cross). Sell/Cash/Short when SMA_50 < SMA_200 (Death Cross).
    -   **ML Strategy**: A machine learning approach.
        -   *Model*: Random Forest Classifier.
        -   *Features*: RSI, MACD, Volatility, previous Log Returns.
        -   *Target*: Binary classification (1 if next day Price > current Price, else 0).

4.  **Backtest Engine (`backtester.py`)**:
    -   Event-driven approach simulation (iterating daily).
    -   **Transaction Logic**:
        -   Calculates slippage (price impact) on entry/exit.
        -   Deducts transaction costs (commissions/fees).
    -   **Portfolio Tracking**: Maintains cash and share balances daily.

## Mathematical Details

### Indicators
-   **RSI**: $RSI = 100 - \frac{100}{1 + RS}$ where $RS = \frac{\text{Average Gain}}{\text{Average Loss}}$.
-   **MACD**: $\text{EMA}_{12} - \text{EMA}_{26}$. Signal Line: $\text{EMA}_9(\text{MACD})$.

### Metrics
-   **Sharpe Ratio**: $\frac{R_p - R_f}{\sigma_p}$
    -   Currently assumes $R_f = 0$ for simplicity.
    -   Annualized by multiplying by $\sqrt{252}$.
-   **Max Drawdown**: $\min \left( \frac{\text{Value}_t - \text{Peak}_{t}}{\text{Peak}_{t}} \right)$.
