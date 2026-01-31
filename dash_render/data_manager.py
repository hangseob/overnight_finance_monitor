import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_sp500_futures_at_time(target_time):
    """
    특정 시점(target_time)의 S&P 500 선물 데이터를 가져옵니다.
    1분 단위 데이터를 가져오기 위해 target_time 전후로 짧은 범위를 조회합니다.
    """
    ticker = "ES=F"
    # target_time이 포함된 날의 데이터를 가져오기 위해 start/end 설정
    start_date = (target_time - timedelta(minutes=10)).strftime('%Y-%m-%d')
    end_date = (target_time + timedelta(days=1)).strftime('%Y-%m-%d')
    
    logger.info(f"Fetching data for {ticker} around {target_time} (Start: {start_date}, End: {end_date})")
    
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval="1m", progress=False)
        
        if data.empty:
            logger.warning(f"No data returned for {ticker} in the range {start_date} to {end_date}")
            return None

        logger.info(f"Downloaded {len(data)} rows of data.")

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        # target_time과 가장 가까운(이전) 데이터 1개를 찾음
        if data.index.tz is not None and target_time.tzinfo is None:
            import pytz
            target_time = pytz.utc.localize(target_time)
        
        # target_time 직전의 데이터 필터링
        point = data[data.index <= target_time].tail(1)
        
        if not point.empty:
            res = {
                "Time": point.index[0].strftime('%Y-%m-%d %H:%M'),
                "Price": float(point['Close'].iloc[0])
            }
            logger.info(f"Successfully found data point: {res}")
            return res
        
        logger.warning(f"No data point found exactly before or at {target_time}")
        return None
    except Exception as e:
        logger.error(f"Error in get_sp500_futures_at_time: {e}", exc_info=True)
        return None
