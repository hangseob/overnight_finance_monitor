import requests
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

def get_access_token(app_key, app_secret, is_mock=False):
    """Access Token 발급"""
    if is_mock:
        base_url = "https://openapivts.koreainvestment.com:29443"
    else:
        base_url = "https://openapi.koreainvestment.com:9443"
    
    url = f"{base_url}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": app_key,
        "appsecret": app_secret
    }
    
    res = requests.post(url, headers=headers, json=body)
    return res.json().get("access_token"), base_url

def fetch_futures_current_price(base_url, access_token, app_key, app_secret, symbol):
    """
    선물 현재가 조회 (API 연결 테스트용)
    """
    url = f"{base_url}/uapi/domestic-futureoption/v1/quotations/inquire-price"
    
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": app_key,
        "appsecret": app_secret,
        "tr_id": "FHMIF10000000",  # 선물 현재가 조회
        "custtype": "P"
    }
    
    params = {
        "FID_COND_MRKT_DIV_CODE": "F",  # F: 선물
        "FID_INPUT_ISCD": symbol
    }
    
    print(f"[DEBUG] 선물 현재가 조회: {symbol}")
    res = requests.get(url, headers=headers, params=params)
    
    if res.status_code == 200:
        data = res.json()
        print(f"[DEBUG] 응답 코드: {data.get('rt_cd')}, 메시지: {data.get('msg1')}")
        if data.get('rt_cd') == '0' and 'output' in data:
            output = data['output']
            print(f"[OK] 현재가: {output.get('futs_prpr', 'N/A')}")
            print(f"    - 고가: {output.get('futs_hgpr', 'N/A')}")
            print(f"    - 저가: {output.get('futs_lwpr', 'N/A')}")
            print(f"    - 전일대비: {output.get('futs_prdy_vrss', 'N/A')}")
            print(f"    - 거래량: {output.get('acml_vol', 'N/A')}")
        return data
    else:
        print(f"[ERROR] HTTP {res.status_code}")
        return None

def fetch_futures_minute_chart(base_url, access_token, app_key, app_secret, symbol, time_unit="1"):
    """
    선물 분봉 데이터 조회 (한국투자증권 API 직접 호출)
    
    symbol: 선물 종목코드 (예: 101SC000 - 코스피200 선물 연속)
    time_unit: 분봉 단위 (1, 3, 5, 10, 15, 30, 45, 60)
    """
    # 선물 분봉 조회 API 엔드포인트
    url = f"{base_url}/uapi/domestic-futureoption/v1/quotations/inquire-time-futuroptprice"
    
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": app_key,
        "appsecret": app_secret,
        "tr_id": "FHMIF10020000",  # 선물 시간별 체결가 조회
        "custtype": "P"  # 개인
    }
    
    # 현재 시간
    now = datetime.now()
    end_time = now.strftime("%H%M%S")
    
    params = {
        "FID_COND_MRKT_DIV_CODE": "F",  # F: 선물
        "FID_INPUT_ISCD": symbol,
        "FID_INPUT_HOUR_1": end_time,
        "FID_PW_DATA_INCU_YN": "Y"  # 과거 데이터 포함
    }
    
    print(f"[DEBUG] 요청 URL: {url}")
    print(f"[DEBUG] 종목코드: {symbol}")
    
    res = requests.get(url, headers=headers, params=params)
    
    if res.status_code == 200:
        data = res.json()
        print(f"[DEBUG] 응답 코드: {data.get('rt_cd')}, 메시지: {data.get('msg1')}")
        return data
    else:
        print(f"[ERROR] HTTP {res.status_code}: {res.text[:200]}")
        return None

def plot_kospi200_futures():
    """코스피200 24시간 연속선물 분봉 차트 생성"""
    
    # API 정보 로드
    API_INFO_PATH = r"C:\Users\hangs\OneDrive\GitRepositories_related_private_data\KIS_API_INFO.txt"
    api_info = load_kis_api_info(API_INFO_PATH)
    
    APP_KEY = api_info.get('APP_KEY')
    APP_SECRET = api_info.get('APP_Secret')
    
    print("한국투자증권 선물 API 연결 중 (실전투자 모드)...")
    
    # Access Token 발급 (실전투자)
    access_token, base_url = get_access_token(APP_KEY, APP_SECRET, is_mock=False)
    
    if not access_token:
        print("[ERROR] Access Token 발급 실패")
        return None
    
    print(f"[OK] Access Token 발급 성공")
    
    # 코스피200 선물 종목코드
    # 101SC000: 코스피200 선물 연속 (근월물 기준)
    symbol = "101SC000"
    
    # 먼저 현재가 조회로 API 연결 테스트
    print(f"\n{symbol} 선물 현재가 조회 중...")
    price_data = fetch_futures_current_price(base_url, access_token, APP_KEY, APP_SECRET, symbol)
    
    print(f"\n{symbol} 선물 분봉 데이터 조회 중...")
    
    # 선물 분봉 데이터 조회
    data = fetch_futures_minute_chart(base_url, access_token, APP_KEY, APP_SECRET, symbol, time_unit="1")
    
    if data and data.get('rt_cd') == '0':
        output2 = data.get('output2', [])
        
        if output2:
            df = pd.DataFrame(output2)
            print(f"[OK] {len(df)}개의 분봉 데이터 수신")
            
            # 데이터 구조 확인
            print(f"\n[DEBUG] 컬럼: {df.columns.tolist()}")
            print(df.head(5))
            
            # 데이터 전처리
            # 선물 API 응답 필드: stck_bsop_date, stck_cntg_hour, futs_prpr, futs_hgpr, futs_lwpr, futs_oprc, cntg_vol
            if 'futs_prpr' in df.columns:
                df['close'] = pd.to_numeric(df['futs_prpr'], errors='coerce')
            elif 'stck_prpr' in df.columns:
                df['close'] = pd.to_numeric(df['stck_prpr'], errors='coerce')
            else:
                print("[WARNING] 가격 컬럼을 찾을 수 없습니다.")
                print(f"사용 가능한 컬럼: {df.columns.tolist()}")
                return None
            
            # 유효한 데이터 필터링
            df = df[df['close'] > 0]
            print(f"[OK] 유효한 데이터: {len(df)}개")
            
            if len(df) == 0:
                print("[WARNING] 유효한 데이터가 없습니다.")
                return None
            
            # 날짜+시간 결합
            if 'stck_bsop_date' in df.columns:
                df['time'] = pd.to_datetime(
                    df['stck_bsop_date'].astype(str) + df['stck_cntg_hour'].astype(str).str.zfill(6),
                    format='%Y%m%d%H%M%S'
                )
            else:
                today = datetime.now().date()
                df['time'] = df['stck_cntg_hour'].apply(
                    lambda x: datetime.combine(today, datetime.strptime(str(x).zfill(6), '%H%M%S').time())
                )
            
            # 시간순 정렬
            df = df.drop_duplicates(subset=['time']).sort_values('time')
            
            # 차트 그리기
            plt.figure(figsize=(15, 8))
            plt.plot(df['time'], df['close'], label=f'KOSPI200 Futures ({symbol}) - 1m', color='purple', linewidth=1)
            
            # 데이터에 포함된 날짜들에 대해 오전 9시, 오후 3시 30분 표시
            unique_dates = df['time'].dt.date.unique()
            for i, day in enumerate(unique_dates):
                kst_0900 = datetime.combine(day, datetime.strptime("09:00:00", "%H:%M:%S").time())
                kst_1530 = datetime.combine(day, datetime.strptime("15:30:00", "%H:%M:%S").time())
                
                label_0900 = '09:00 (KST)' if i == 0 else None
                label_1530 = '15:30 (KST)' if i == 0 else None
                
                plt.axvline(x=kst_0900, color='red', linestyle='--', alpha=0.6, label=label_0900)
                plt.axvline(x=kst_1530, color='green', linestyle='--', alpha=0.6, label=label_1530)
            
            plt.title(f'KOSPI200 24H Futures ({symbol}) - 1m Interval (KIS API)')
            plt.xlabel('Time (KST)')
            plt.ylabel('Price')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # 파일로 저장
            output_file = "kospi200_futures_1m.png"
            plt.savefig(output_file)
            print(f"\n[OK] 차트가 '{output_file}'로 저장되었습니다.")
            
            # 최근 데이터 출력
            print("\n[최근 10분 데이터]")
            print(df[['time', 'close']].tail(10))
            
            return df
        else:
            print("[WARNING] output2 데이터가 비어있습니다.")
            print(f"전체 응답: {data}")
    else:
        print("[ERROR] API 호출 실패")
        if data:
            print(f"응답: {data}")
    
    return None

if __name__ == "__main__":
    plot_kospi200_futures()
