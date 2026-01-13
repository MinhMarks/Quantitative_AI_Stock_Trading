import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

class FeatureEngineer:
    def __init__(self, use_ta_lib=True):
        """
        Initialize FeatureEngineer.
        
        Args:
            use_ta_lib (bool): Whether to use the 'ta' library or manual implementation.
        """
        self.use_ta_lib = use_ta_lib

    def add_features(self, df):
        """
        Add technical indicators to the DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame with 'close' column.
            
        Returns:
            pd.DataFrame: DataFrame with added features.
        """
        df = df.copy()
        
        if self.use_ta_lib:
            # Simple Moving Averages
            df['SMA_50'] = SMAIndicator(close=df['close'], window=50).sma_indicator()
            df['SMA_200'] = SMAIndicator(close=df['close'], window=200).sma_indicator()
            
            # RSI
            df['RSI'] = RSIIndicator(close=df['close'], window=14).rsi()
            
            # MACD
            macd = MACD(close=df['close'])
            df['MACD'] = macd.macd()
            df['MACD_Signal'] = macd.macd_signal()
            df['MACD_Diff'] = macd.macd_diff()
            
            # Rolling Volatility (Standard Deviation of log returns for 20 days)
            df['Log_Return'] = np.log(df['close'] / df['close'].shift(1))
            df['Volatility_20'] = df['Log_Return'].rolling(window=20).std()
            
        else:
            # Manual Implementation (fallback)
            df['SMA_50'] = df['close'].rolling(window=50).mean()
            df['SMA_200'] = df['close'].rolling(window=200).mean()
            
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD: 12ema - 26ema
            ema12 = df['close'].ewm(span=12, adjust=False).mean()
            ema26 = df['close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema12 - ema26
            df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            df['MACD_Diff'] = df['MACD'] - df['MACD_Signal']
            
            df['Log_Return'] = np.log(df['close'] / df['close'].shift(1))
            df['Volatility_20'] = df['Log_Return'].rolling(window=20).std()

        return df

if __name__ == "__main__":
    # Test
    from data_loader import DataLoader
    
    loader = DataLoader()
    # Fetch a generic ticker for testing
    data = loader.fetch_data('SPY', '2020-01-01', '2023-01-01')
    if data is not None:
        data = loader.clean_data(data)
        fe = FeatureEngineer()
        data_with_features = fe.add_features(data)
        print(data_with_features[['close', 'SMA_50', 'RSI', 'MACD', 'Volatility_20']].tail())
