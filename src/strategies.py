from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, data):
        """
        Generate trading signals.
        
        Args:
            data (pd.DataFrame): DataFrame with features.
            
        Returns:
            pd.Series: Series of signals (1: Buy, -1: Sell, 0: Hold/Neutral).
        """
        pass

class MACrossoverStrategy(Strategy):
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        """
        Buy when Short MA > Long MA.
        Sell when Short MA < Long MA.
        """
        signals = pd.Series(0, index=data.index)
        
        # Check if features exist, else compute them (assuming data has 'close') or rely on existing columns
        short_col = f'SMA_{self.short_window}'
        long_col = f'SMA_{self.long_window}'
        
        if short_col not in data.columns or long_col not in data.columns:
            # Fallback if not pre-computed (though we assume features.py did it)
            # For simplicity, we assume they attend
             raise ValueError(f"Columns {short_col} and {long_col} required.")
        
        # Generate signal: 1 if Short > Long, -1 if Short < Long
        # We transform this to 1 (Long position) and 0 (Cash/Neutral) or -1 (Short)
        # For this backtest, let's assume Long-Only or Long/Short.
        # Let's simple model: Hold (1) when SMA_S > SMA_L else Cash (0)
        
        # The signal represents the TARGET POSITION.
        # 1 = "I want to be long"
        # 0 = "I want to be in cash"
        
        signals[data[short_col] > data[long_col]] = 1
        signals[data[short_col] <= data[long_col]] = 0
        
        # Convert position signal to trade signal (diff) if needed by backtester,
        # but usually strategies return the Desired Position.
        # Let's return Desired Position.
        return signals

class MLStrategy(Strategy):
    def __init__(self, features=['RSI', 'MACD', 'Volatility_20', 'Log_Return']):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.features = features

    def train_model(self, data):
        """
        Train the model to predict next day's return sign.
        """
        df = data.copy().dropna()
        
        # Target: 1 if Close moves up tomorrow, 0 otherwise
        df['Target'] = (df['close'].shift(-1) > df['close']).astype(int)
        
        # Drop last row as it has no target
        df = df.dropna()
        
        X = df[self.features]
        y = df['Target']
        
        # Train/Test logic could be external, but here we just train on provided data
        self.model.fit(X, y)
        print("Model trained.")

    def generate_signals(self, data):
        """
        Predict signals using trained model.
        Assumes model is trained.
        """
        # We need to handle NaN in features because ML model can't handle them
        # We fill NaNs or skip
        
        data_clean = data[self.features].fillna(0) # Simple imputation for demo
        
        predictions = self.model.predict(data_clean)
        
        # Predictions are 0 or 1.
        # 0 -> Cash, 1 -> Long
        signals = pd.Series(predictions, index=data.index)
        return signals
