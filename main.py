from src.data_loader import DataLoader
from src.features import FeatureEngineer
from src.strategies import MACrossoverStrategy, MLStrategy
from src.backtester import Backtester
from src.evaluation import Evaluator
import matplotlib.pyplot as plt
import pandas as pd

def run_demo():
    print("=== Quantitative Trading Project Demo ===")
    
    # 1. Data Collection
    print("\n[1] Fetching data...")
    loader = DataLoader()
    # Fetch 9 years of data
    raw_data = loader.fetch_data('SPY', '2015-01-01', '2024-01-01')
    if raw_data is None:
        print("Failed to fetch data.")
        return
        
    data = loader.clean_data(raw_data)
    print(f"Data Loaded: {len(data)} rows.")
    
    # 2. Feature Engineering
    print("\n[2] Engineering features...")
    fe = FeatureEngineer()
    data = fe.add_features(data)
    data = data.dropna()
    print("Features added: SMA_50, SMA_200, RSI, MACD, Volatility.")
    
    # Split for ML (Train: 2015-2021, Test: 2022-2023)
    train_end_date = '2021-12-31'
    test_start_date = '2022-01-01'
    
    train_data = data.loc[:train_end_date]
    test_data = data.loc[test_start_date:]
    
    print(f"Train Set: {len(train_data)} rows ({train_data.index[0].date()} to {train_data.index[-1].date()})")
    print(f"Test Set: {len(test_data)} rows ({test_data.index[0].date()} to {test_data.index[-1].date()})")
    
    # 3. Strategy Implementation
    
    # A. Rule-based
    print("\n[3] Running MA Crossover Strategy...")
    ma_strategy = MACrossoverStrategy(short_window=50, long_window=200)
    
    # B. ML-based
    print("\n[4] Training ML Strategy (Random Forest)...")
    ml_strategy = MLStrategy()
    ml_strategy.train_model(train_data)
    
    # 4. Backtesting (on Test Data)
    backtester = Backtester(transaction_cost_pct=0.001) # 0.1% per trade
    
    print("\n[5] Backtesting MA Strategy on Test Data...")
    ma_results = backtester.run(test_data, ma_strategy)
    
    print("Backtesting ML Strategy on Test Data...")
    ml_results = backtester.run(test_data, ml_strategy)
    
    # 5. Evaluation
    print("\n=== MA Strategy Performance ===")
    ma_eval = Evaluator(ma_results)
    ma_metrics = ma_eval.calculate_metrics()
    for k, v in ma_metrics.items():
        print(f"{k}: {v:.4f}")
    
    print("\n=== ML Strategy Performance ===")
    ml_eval = Evaluator(ml_results)
    ml_metrics = ml_eval.calculate_metrics()
    for k, v in ml_metrics.items():
        print(f"{k}: {v:.4f}")
    
    print("\n=== Benchmark (Buy & Hold) Performance ===")
    initial_price = test_data['close'].iloc[0]
    final_price = test_data['close'].iloc[-1]
    benchmark_return = (final_price / initial_price) - 1
    print(f"Cumulative Return: {benchmark_return:.4f}")

    # Plot
    print("\n[6] Generating Plot...")
    plt.figure(figsize=(14, 7))
    plt.plot(ma_results.index, ma_results['Portfolio Value'], label=f'MA Crossover (Sharpe: {ma_metrics.get("Sharpe Ratio",0):.2f})')
    plt.plot(ml_results.index, ml_results['Portfolio Value'], label=f'ML Random Forest (Sharpe: {ml_metrics.get("Sharpe Ratio",0):.2f})')
    
    # Adds Benchmark
    initial_capital = ma_results['Portfolio Value'].iloc[0]
    benchmark_val = (test_data['close'] / test_data['close'].iloc[0]) * initial_capital
    plt.plot(benchmark_val.index, benchmark_val, label='Buy & Hold (SPY)', alpha=0.6, linestyle='--', color='gray')
    
    plt.title('Strategy Comparison: MA vs ML vs Benchmark (2022-2023)')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    
    save_path = 'strategy_comparison.png'
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

if __name__ == "__main__":
    run_demo()
