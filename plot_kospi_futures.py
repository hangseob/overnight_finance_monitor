import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def plot_kospi_futures_1m():
    """
    코스피 200 지수(^KS200) 데이터를 1분 단위로 가져와서 최근 3일치를 차트로 그립니다.
    (yfinance에서 한국 선물 24시간 데이터는 제공이 제한적이므로 지수 데이터로 대체합니다.)
    """
    ticker = "^KS200"
    print(f"{ticker} 1분 단위 데이터를 3일치 불러오는 중...")
    
    # yfinance에서 1분 단위 데이터 수집 (period='3d', interval='1m')
    data = yf.download(ticker, period="3d", interval="1m")
    
    if data.empty:
        print(f"'{ticker}' 데이터를 불러오지 못했습니다. 티커가 유효한지 확인하세요.")
        return

    # 'Close' 가격 컬럼 선택 (MultiIndex 대응)
    if isinstance(data.columns, pd.MultiIndex):
        close_prices = data['Close'][ticker]
    else:
        close_prices = data['Close']

    # 인덱스를 한국 시간(KST)으로 변환
    close_prices.index = close_prices.index.tz_convert('Asia/Seoul')

    # 차트 그리기
    plt.figure(figsize=(15, 8))
    plt.plot(close_prices.index, close_prices.values, label=f'KOSPI Futures ({ticker}) - 1m', color='purple', linewidth=1)
    
    # 한국 시간 기준 오전 9시와 오후 3시 30분 표시 및 변동률 계산
    unique_days = sorted(pd.Series(close_prices.index.date).unique())
    
    for i in range(len(unique_days)):
        day = unique_days[i]
        
        # 1. 당일 오후 15:30 (KST)
        kst_1530 = pd.Timestamp(year=day.year, month=day.month, day=day.day, hour=15, minute=30, tz='Asia/Seoul')
        
        # 2. 다음날 오전 09:00 (KST)
        if i + 1 < len(unique_days):
            next_day = unique_days[i+1]
            kst_0900_next = pd.Timestamp(year=next_day.year, month=next_day.month, day=next_day.day, hour=9, minute=0, tz='Asia/Seoul')
            
            # 두 시점의 데이터가 모두 존재하는지 확인
            if kst_1530 in close_prices.index and kst_0900_next in close_prices.index:
                price_1530 = close_prices.loc[kst_1530]
                price_0900 = close_prices.loc[kst_0900_next]
                change = price_0900 - price_1530
                pct_change = (change / price_1530) * 100
                
                # 오버나이트 구간 음영 표시 (15:30 ~ 익일 09:00)
                plt.axvspan(kst_1530, kst_0900_next, color='gray', alpha=0.1)
                
                # 변동폭 텍스트 표시
                mid_point = kst_1530 + (kst_0900_next - kst_1530) / 2
                plt.text(mid_point, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) * 0.1, 
                         f'Overnight: {change:+.2f} ({pct_change:+.2f}%)', 
                         color='darkblue', fontweight='bold', horizontalalignment='center')

        # 오전 9:00 (KST) 수직선
        kst_0900 = pd.Timestamp(year=day.year, month=day.month, day=day.day, hour=9, minute=0, tz='Asia/Seoul')
        if kst_0900 in close_prices.index:
            plt.axvline(x=kst_0900, color='red', linestyle='--', alpha=0.6)
            plt.text(kst_0900, plt.ylim()[1], ' 09:00', color='red', verticalalignment='bottom', rotation=90)
            
        # 오후 3:30 (KST) 수직선
        if kst_1530 in close_prices.index:
            plt.axvline(x=kst_1530, color='green', linestyle='--', alpha=0.6)
            plt.text(kst_1530, plt.ylim()[1], ' 15:30', color='green', verticalalignment='bottom', rotation=90)

    plt.title(f'KOSPI Futures ({ticker}) - Last 3 Days (KST Overnight Markers)')
    plt.xlabel('Time (KST)')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 파일로 저장
    output_file = "kospi_futures_3d_1m.png"
    plt.savefig(output_file)
    print(f"차트가 '{output_file}'로 저장되었습니다.")
    
    # 최근 데이터 일부 출력
    print("\n[최근 5분 데이터]")
    print(close_prices.tail())

if __name__ == "__main__":
    plot_kospi_futures_1m()
