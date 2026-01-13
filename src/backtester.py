import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, initial_capital=10000.0, transaction_cost_pct=0.001, slippage_pct=0.0005):
        """
        Initialize the Backtester.
        
        Args:
            initial_capital (float): Starting cash.
            transaction_cost_pct (float): Cost per trade (e.g. 0.001 for 0.1%).
            slippage_pct (float): Estimated price slippage (e.g. 0.0005 for 0.05%).
        """
        self.initial_capital = initial_capital
        self.transaction_cost_pct = transaction_cost_pct
        self.slippage_pct = slippage_pct

    def run(self, data, strategy):
        """
        Run the backtest.
        
        Args:
            data (pd.DataFrame): Date-indexed DataFrame with 'close' price.
            strategy (Strategy): Feature-aware strategy instance.
            
        Returns:
            pd.DataFrame: Portfolio result with 'Portfolio Value', 'Cash', 'Holdings'.
        """
        # Ensure data is sorted
        data = data.sort_index()
        
        # Get target positions (0 or 1) from strategy
        # Strategy should use info available up to t to signal position for t+1 open/close.
        # Here we assume strategies execute at CLOSE of the signal day (or Open of next, but simpler is Close).
        signals = strategy.generate_signals(data)
        
        # Initialize
        cash = self.initial_capital
        position = 0.0 # shares
        portfolio_history = []
        
        # Iterate daily
        prev_signal = 0
        
        for date, row in data.iterrows():
            current_signal = signals.loc[date]
            price = row['close']
            
            # If signal changes, execute trade
            # In this simple model, signal=1 means WE WANT TO BE LONG.
            # signal=0 means WE WANT TO BE FLAT.
            
            # Calculate Target Shares
            if current_signal == 1:
                # We want to be fully invested
                if position == 0:
                    # BUY
                    effective_price = price * (1 + self.slippage_pct)
                    shares_to_buy = int(cash / effective_price)
                    cost = shares_to_buy * effective_price
                    fee = cost * self.transaction_cost_pct
                    
                    if cash >= cost + fee:
                        cash -= (cost + fee)
                        position = shares_to_buy
            
            elif current_signal == 0:
                # We want to be cash
                if position > 0:
                    # SELL
                    effective_price = price * (1 - self.slippage_pct)
                    revenue = position * effective_price
                    fee = revenue * self.transaction_cost_pct
                    
                    cash += (revenue - fee)
                    position = 0
            
            # Mark to Market
            holdings_value = position * price
            total_value = cash + holdings_value
            
            portfolio_history.append({
                'Date': date,
                'Cash': cash,
                'Holdings': holdings_value,
                'Portfolio Value': total_value,
                'Position': position
            })
            
            prev_signal = current_signal

        results = pd.DataFrame(portfolio_history)
        results = results.set_index('Date')
        return results
