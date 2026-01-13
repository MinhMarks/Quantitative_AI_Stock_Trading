# Quantitative Trading Strategy Backtesting

A comprehensive Python framework for designing, backtesting, and evaluating quantitative trading strategies. This project demonstrates skills in Data Science, Machine Learning, and Financial Engineering.

## 📂 Documentation
Full documentation is available in the `docs/` folder:

-   **[Setup Guide](docs/setup_guide.md)**: Instructions for installing and running the project.
-   **[Architecture & Logic](docs/architecture_and_logic.md)**: Detailed explanation of the strategies and math behind the indicators.
-   **[GitHub Push Guide](docs/github_guide.md)**: Step-by-step guide to uploading this project to GitHub.
-   **[Docker Guide](docs/docker_guide.md)**: Instructions for building and running with Docker.
-   **[Deployment Guide](docs/deploy_guide.md)**: How to host the Web App on Streamlit Cloud.
-   **[Reference Paper](docs/references/Quantitative_Trading_Strategy_Backtesting_and_Perf.pdf)**: Theoretical background and references.

## 🚀 Quick Start
1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the demo**:
    ```bash
    python main.py
    ```

## 📊 Features
-   **Automated Data Pipeline**: Fetches and cleans OHLCV data via `yfinance`.
-   **Multi-Strategy Support**:
    -   *Rule-Based*: Moving Average Crossover.
    -   *ML-Based*: Random Forest Directional Predictor.
-   **Robust Backtesting**: Includes transaction costs (0.1%) and slippage simulation.
-   **Performance Metrics**: Sharpe Ratio, Maximum Drawdown, Cumulative Returns.

## 📈 Sample Result
*Running `main.py` generates a comparison of strategies against the Buy & Hold benchmark.*
