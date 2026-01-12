# Quantitative Trading Strategy Backtesting

A Python-based backtesting framework for quantitative trading strategies, featuring data collection, feature engineering (SMA, RSI, MACD), and both rule-based and ML-based strategy evaluation.

## Features
- **Data Loader**: Auto-fetch OHLCV data from Yahoo Finance.
- **Technical Indicators**: SMA, RSI, MACD, Bollinger Bands/Volatility.
- **Strategies**:
  - `MACrossoverStrategy`: Classic trend-following.
  - `MLStrategy`: Random Forest classifier for direction prediction.
- **Backtester**: Simulates trading with transaction costs and slippage.
- **Evaluation**: Sharpe Ratio, Maximum Drawdown, Equity Curve visualization.

## Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd quant_project
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the main demo script:
```bash
python main.py
```
This will fetch data for SPY, train the models, run backtests, and generate a performance plot `strategy_comparison.png`.

## Project Structure
- `data/`: Stored historical data (CSV).
- `src/`: Source code modules.
- `main.py`: Entry point.
