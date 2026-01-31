import yfinance as yf
from datetime import datetime, timedelta

def check_yfinance_1m_historical(ticker="ES=F"):
    print(f"Checking 1-minute data historical limit for {ticker} using start/end...")
    
    end_dt = datetime.now()
    
    # Try to go back 10 days, 15 days, 25 days, 35 days
    offsets = [10, 15, 25, 35]
    
    for days_back in offsets:
        start_dt = end_dt - timedelta(days=days_back)
        # We still need to respect the 7-day window per request if the error message was literal, 
        # but let's see if we can get a small window from X days ago.
        test_start = start_dt
        test_end = start_dt + timedelta(days=1)
        
        print(f"\nTrying to fetch 1m data from {days_back} days ago ({test_start.date()} to {test_end.date()})...")
        try:
            data = yf.download(ticker, start=test_start.strftime('%Y-%m-%d'), 
                               end=test_end.strftime('%Y-%m-%d'), interval="1m", progress=False)
            if not data.empty:
                print(f"Success! Fetched {len(data)} rows.")
            else:
                print(f"No data returned for start date {test_start.date()}.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_yfinance_1m_historical()
