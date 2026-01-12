import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Evaluator:
    def __init__(self, portfolio_data):
        """
        Initialize Evaluator.
        
        Args:
            portfolio_data (pd.DataFrame): DataFrame from Backtester with 'Portfolio Value'.
        """
        self.data = portfolio_data
        
    def calculate_metrics(self):
        """
        Calculate performance metrics.
        
        Returns:
            dict: Metrics dictionary.
        """
        # Daily Returns using 'Portfolio Value' instead of 'close' of the stock
        returns = self.data['Portfolio Value'].pct_change().dropna()
        
        if returns.empty:
            return {}
        
        # Cumulative Return
        total_return = (self.data['Portfolio Value'].iloc[-1] / self.data['Portfolio Value'].iloc[0]) - 1
        
        # Sharpe Ratio (Annualized, assuming risk-free rate = 0)
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
        
        # Max Drawdown
        rolling_max = self.data['Portfolio Value'].cummax()
        drawdown = (self.data['Portfolio Value'] - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        return {
            "Cumulative Return": total_return,
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown": max_drawdown
        }

    def plot_equity_curve(self, benchmark_data=None, save_path=None):
        """
        Plot the equity curve of the strategy vs benchmark.
        
        Args:
            benchmark_data (pd.DataFrame, optional): Benchmark OHLCV data.
            save_path (str, optional): Path to save the plot.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data['Portfolio Value'], label='Strategy')
        
        if benchmark_data is not None:
            # Normalize benchmark to initial capital
            benchmark_initial = benchmark_data['close'].iloc[0]
            initial_capital = self.data['Portfolio Value'].iloc[0]
            
            # Align dates
            bench_aligned = benchmark_data.reindex(self.data.index)
            # Forward fill simpler than dropping if trading days mismatch slightly, 
            # though usually they match if using same source.
            bench_aligned = bench_aligned.ffill() 
            
            normalized_benchmark = (bench_aligned['close'] / benchmark_initial) * initial_capital
            plt.plot(bench_aligned.index, normalized_benchmark, label='Benchmark (Buy & Hold)', alpha=0.7)
            
        plt.title('Equity Curve')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value ($)')
        plt.legend()
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")
        else:
            plt.show()

if __name__ == "__main__":
    pass
