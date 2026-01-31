import yfinance as yf
from datetime import datetime, timedelta

def check_yfinance_1m_limit(ticker="ES=F"):
    print(f"Checking 1-minute data limit for {ticker}...")
    
    # Try different periods
    periods = ["1d", "5d", "7d", "30d", "60d"]
    
    for period in periods:
        print(f"\nTrying period='{period}', interval='1m'...")
        try:
            data = yf.download(ticker, period=period, interval="1m", progress=False)
            if not data.empty:
                start_date = data.index.min()
                end_date = data.index.max()
                count = len(data)
                print(f"Success! Fetched {count} rows.")
                print(f"Range: {start_date} to {end_date}")
            else:
                print(f"No data returned for period='{period}'.")
        except Exception as e:
            print(f"Error for period='{period}': {e}")

if __name__ == "__main__":
    check_yfinance_1m_limit()
