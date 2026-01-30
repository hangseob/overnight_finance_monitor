import yfinance as yf

def fetch_sp500_futures():
    """
    S&P 500 선물(ES=F) 데이터를 30분 단위로 가져옵니다.
    period='2d': 최근 2일치 데이터를 가져와서 24시간 범위를 포함하도록 합니다.
    interval='30m': 30분 단위 (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h 등 가능)
    """
    print("S&P 500 선물(ES=F) 30분 단위 데이터를 불러오는 중...")
    
    # 데이터 다운로드
    data = yf.download("ES=F", period="2d", interval="30m")
    
    if data.empty:
        print("데이터를 불러오지 못했습니다. 티커(ES=F) 또는 네트워크 연결을 확인하세요.")
        return None

    # 최근 24시간 데이터 (30분 단위 기준 약 48개 행) 출력
    print("\n[최근 데이터 확인]")
    print(data.tail(48))
    
    return data

if __name__ == "__main__":
    fetch_sp500_futures()
