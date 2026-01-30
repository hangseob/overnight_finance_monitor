import mojito
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def load_kis_api_info(filepath):
    """KIS API 정보를 외부 파일에서 읽어옵니다."""
    api_info = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '\t' in line:
                key, value = line.split('\t', 1)
                api_info[key] = value
    return api_info

def plot_kospi_futures_from_kis():
    """
    한국투자증권 API를 사용하여 코스피200 선물 분봉 데이터를 가져와 차트를 그립니다.
    """
    # API 정보 로드
    API_INFO_PATH = r"C:\Users\hangs\OneDrive\GitRepositories_related_private_data\KIS_API_INFO.txt"
    api_info = load_kis_api_info(API_INFO_PATH)
    
    APP_KEY = api_info.get('APP_KEY')
    APP_SECRET = api_info.get('APP_Secret')
    ACC_NO = api_info.get('account_number')
    
    print("한국투자증권 API 연결 중...")
    
    # 실전투자 모드로 연결 (시세 조회용)
    broker = mojito.KoreaInvestment(
        api_key=APP_KEY,
        api_secret=APP_SECRET,
        acc_no=ACC_NO,
        mock=False  # 실전투자 모드
    )
    print("[OK] API 연결 성공!")
    
    # 코스피200 선물 연속 (24시간 연속선물 포함)
    # 101SC000: 코스피200 선물 연속 (근월물 기준)
    symbol = "101SC000"  # 코스피200 선물 연속
    
    print(f"\n{symbol} 분봉 데이터 조회 중...")
    
    try:
        # 분봉 데이터 조회 (1분봉)
        resp = broker.fetch_today_1m_ohlcv(symbol)
        
        if 'output2' in resp and resp['output2']:
            df = pd.DataFrame(resp['output2'])
            print(f"[OK] {len(df)}개의 분봉 데이터 수신")
            
            # 데이터 전처리 - 날짜와 시간을 결합
            df['close'] = pd.to_numeric(df['stck_prpr'], errors='coerce')
            df['high'] = pd.to_numeric(df['stck_hgpr'], errors='coerce')
            df['low'] = pd.to_numeric(df['stck_lwpr'], errors='coerce')
            df['open'] = pd.to_numeric(df['stck_oprc'], errors='coerce')
            df['volume'] = pd.to_numeric(df['cntg_vol'], errors='coerce')
            
            # 유효한 데이터만 필터링 (가격이 0보다 큰 것)
            df = df[df['close'] > 0]
            print(f"[OK] 유효한 데이터: {len(df)}개")
            
            if len(df) == 0:
                print("[WARNING] 유효한 데이터가 없습니다.")
                return None
            
            # 날짜+시간 결합 (stck_bsop_date + stck_cntg_hour)
            df['time'] = pd.to_datetime(
                df['stck_bsop_date'].astype(str) + df['stck_cntg_hour'].astype(str).str.zfill(6),
                format='%Y%m%d%H%M%S'
            )
            
            # 중복 제거 및 시간순 정렬
            df = df.drop_duplicates(subset=['time']).sort_values('time')
            
            # 차트 그리기
            plt.figure(figsize=(15, 8))
            plt.plot(df['time'], df['close'], label=f'KOSPI200 Futures ({symbol}) - 1m', color='purple', linewidth=1)
            
            # 데이터에 포함된 날짜들에 대해 오전 9시, 오후 3시 30분 표시
            unique_dates = df['time'].dt.date.unique()
            for i, day in enumerate(unique_dates):
                kst_0900 = datetime.combine(day, datetime.strptime("09:00:00", "%H:%M:%S").time())
                kst_1530 = datetime.combine(day, datetime.strptime("15:30:00", "%H:%M:%S").time())
                
                # 범례는 첫 번째만 표시
                label_0900 = '09:00' if i == 0 else None
                label_1530 = '15:30' if i == 0 else None
                
                plt.axvline(x=kst_0900, color='red', linestyle='--', alpha=0.6, label=label_0900)
                plt.axvline(x=kst_1530, color='green', linestyle='--', alpha=0.6, label=label_1530)
            
            plt.title(f'KOSPI200 Futures ({symbol}) - Today 1m Interval (KIS API)')
            plt.xlabel('Time (KST)')
            plt.ylabel('Price')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # 파일로 저장
            output_file = "kospi_futures_kis_1m.png"
            plt.savefig(output_file)
            print(f"\n[OK] 차트가 '{output_file}'로 저장되었습니다.")
            
            # 최근 데이터 출력
            print("\n[최근 5분 데이터]")
            print(df[['time', 'close', 'high', 'low', 'volume']].tail())
            
            return df
        else:
            print("[WARNING] 분봉 데이터가 없습니다.")
            print("응답:", resp)
            return None
            
    except Exception as e:
        print(f"[ERROR] 분봉 데이터 조회 실패: {e}")
        return None

if __name__ == "__main__":
    plot_kospi_futures_from_kis()
