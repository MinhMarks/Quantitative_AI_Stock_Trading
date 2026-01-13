import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.data_loader import DataLoader
from src.features import FeatureEngineer
from src.strategies import MACrossoverStrategy, MLStrategy
from src.backtester import Backtester
from src.evaluation import Evaluator

# Set page config
st.set_page_config(page_title="Quantitative Backtesting Demo", layout="wide")

st.title("📈 Quantitative Trading Strategy Backtesting")
st.markdown("""
App này minh họa hệ thống backtesting định lượng với 2 chiến lược chính:
1. **Machine Learning**: Dùng Random Forest dự đoán xu hướng.
2. **Rule-Based**: Moving Average Crossover (Golden Cross).
""")

# Sidebar settings
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Ticker Symbol", value="SPY")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2015-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-01-01"))
initial_capital = st.sidebar.number_input("Initial Capital ($)", value=10000)

if st.sidebar.button("Run Simulation"):
    with st.spinner("Fetching data and running backtest..."):
        # 1. Data Loading
        loader = DataLoader()
        raw_data = loader.fetch_data(ticker, str(start_date), str(end_date))
        
        if raw_data is None or raw_data.empty:
            st.error("No data found!")
        else:
            data = loader.clean_data(raw_data)
            
            # 2. Feature Engineering
            fe = FeatureEngineer()
            data = fe.add_features(data)
            data = data.dropna()
            
            # Split Data
            train_end_date = '2021-12-31'
            test_start_date = '2022-01-01'
            
            # Ensure dates are within range
            if pd.to_datetime(train_end_date) > data.index[-1] or pd.to_datetime(test_start_date) > data.index[-1]:
                 st.warning("Data range is too short for the default train/test split (2015-2021 | 2022-2023). Using generic 80/20 split.")
                 split_idx = int(len(data) * 0.8)
                 train_data = data.iloc[:split_idx]
                 test_data = data.iloc[split_idx:]
            else:
                 train_data = data.loc[:train_end_date]
                 test_data = data.loc[test_start_date:]
            
            st.write(f"**Data Loaded:** {len(data)} rows. **Test Period:** {test_data.index[0].date()} to {test_data.index[-1].date()}")

            # 3. Strategies
            # MA
            ma_strategy = MACrossoverStrategy(50, 200)
            
            # ML
            ml_strategy = MLStrategy()
            ml_strategy.train_model(train_data)
            
            # 4. Backtest
            backtester = Backtester(initial_capital=initial_capital, transaction_cost_pct=0.001)
            ma_results = backtester.run(test_data, ma_strategy)
            ml_results = backtester.run(test_data, ml_strategy)
            
            # 5. Evaluation
            ma_eval = Evaluator(ma_results).calculate_metrics()
            ml_eval = Evaluator(ml_results).calculate_metrics()
            
            # Benchmark
            initial_price = test_data['close'].iloc[0]
            final_price = test_data['close'].iloc[-1]
            benchmark_return = (final_price / initial_price) - 1
            
            # Display Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("MA Strategy")
                st.metric("Return", f"{ma_eval.get('Cumulative Return', 0):.2%}")
                st.metric("Sharpe", f"{ma_eval.get('Sharpe Ratio', 0):.2f}")
                st.metric("Max DD", f"{ma_eval.get('Max Drawdown', 0):.2%}")
                
            with col2:
                st.subheader("ML Strategy")
                st.metric("Return", f"{ml_eval.get('Cumulative Return', 0):.2%}")
                st.metric("Sharpe", f"{ml_eval.get('Sharpe Ratio', 0):.2f}")
                st.metric("Max DD", f"{ml_eval.get('Max Drawdown', 0):.2%}")
                
            with col3:
                st.subheader("Benchmark (Buy & Hold)")
                st.metric("Return", f"{benchmark_return:.2%}")
                
            # Plot
            st.subheader("Equity Curve")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(ma_results.index, ma_results['Portfolio Value'], label='MA Crossover')
            ax.plot(ml_results.index, ml_results['Portfolio Value'], label='ML Random Forest')
            
            # Benchmark Curve
            bench_val = (test_data['close'] / test_data['close'].iloc[0]) * initial_capital
            ax.plot(bench_val.index, bench_val, label='Buy & Hold', color='gray', linestyle='--', alpha=0.5)
            
            ax.set_ylabel("Portfolio Value ($)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
