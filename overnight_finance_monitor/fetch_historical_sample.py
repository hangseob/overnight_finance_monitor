import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def fetch_specific_window(ticker="ES=F"):
    now = datetime.now()
    start_dt = now - timedelta(hours=5*24)
    end_dt = start_dt + timedelta(hours=1)
    
    print(f"Fetching 1-minute data for {ticker}")
    print(f"Window: {start_dt} to {end_dt}")
    
    try:
        data = yf.download(
            ticker, 
            start=start_dt.strftime('%Y-%m-%d'), 
            end=(end_dt + timedelta(days=1)).strftime('%Y-%m-%d'),
            interval="1m", 
            progress=False
        )
        
        if not data.empty:
            if data.index.tz is not None:
                start_dt_tz = start_dt.astimezone(data.index.tz)
                end_dt_tz = end_dt.astimezone(data.index.tz)
                filtered_data = data[(data.index >= start_dt_tz) & (data.index <= end_dt_tz)]
            else:
                filtered_data = data[(data.index >= start_dt) & (data.index <= end_dt)]
                
            if not filtered_data.empty:
                print(f"\nFound {len(filtered_data)} data points:")
                
                # Check column structure
                if isinstance(filtered_data.columns, pd.MultiIndex):
                    # MultiIndex structure (Ticker, PriceType)
                    close_col = ('Close', ticker)
                else:
                    close_col = 'Close'
                
                for ts, row in filtered_data.iterrows():
                    # Handle potential multi-column results
                    price = row[close_col]
                    if isinstance(price, pd.Series):
                        price = price.iloc[0]
                    print(f"{ts} | Close: {float(price):.2f}")
            else:
                print("\nNo data found in the specific 1-hour window.")
        else:
            print("No data returned from yfinance.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_specific_window()
