import yfinance as yf
import pandas as pd
import os

class DataLoader:
    def __init__(self, data_dir='data'):
        """
        Initialize the DataLoader.
        
        Args:
            data_dir (str): Directory where data will be saved/loaded.
        """
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def fetch_data(self, ticker, start_date, end_date):
        """
        Fetch historical data from Yahoo Finance.
        
        Args:
            ticker (str): Stock ticker symbol (e.g., 'SPY').
            start_date (str): Start date in 'YYYY-MM-DD' format.
            end_date (str): End date in 'YYYY-MM-DD' format.
            
        Returns:
            pd.DataFrame: DataFrame with OHLCV data.
        """
        file_path = os.path.join(self.data_dir, f"{ticker}_{start_date}_{end_date}.csv")
        
        # Check if data already exists locally
        if os.path.exists(file_path):
            print(f"Loading data for {ticker} from local storage...")
            df = pd.read_csv(file_path, index_col=0, parse_dates=True)
        else:
            print(f"Downloading data for {ticker} from Yahoo Finance...")
            df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
            if df.empty:
                print(f"No data found for {ticker}.")
                return None
            
            # Reset index to insure it is datetime
            df.index = pd.to_datetime(df.index)

            # Flatten MultiIndex columns if present (e.g. ('Close', 'SPY') -> 'Close')
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Save to CSV
            df.to_csv(file_path)
            print(f"Data saved to {file_path}")
            
        return df

    def clean_data(self, df):
        """
        Perform basic data cleaning.
        
        Args:
            df (pd.DataFrame): Raw DataFrame.
            
        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        # Drop rows with missing values
        df = df.dropna()
        
        # Ensure columns are standard
        # yfinance auto_adjust=True returns: Open, High, Low, Close, Volume
        # Sometimes 'Adj Close' is present if auto_adjust=False.
        # We will standardize column names to lowercase for consistency
        df.columns = [c.lower() for c in df.columns]
        
        return df

if __name__ == "__main__":
    # Test
    loader = DataLoader()
    data = loader.fetch_data('SPY', '2020-01-01', '2023-01-01')
    if data is not None:
        print(data.head())
        clean_data = loader.clean_data(data)
        print(clean_data.head())
