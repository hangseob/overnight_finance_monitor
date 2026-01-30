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

def plot_kospi200_futures_from_kis():
    """
    한국투자증권 API를 사용하여 코스피200 24시간 연속선물 분봉 데이터를 가져와 차트를 그립니다.
    """
    # API 정보 로드
    API_INFO_PATH = r"C:\Users\hangs\OneDrive\GitRepositories_related_private_data\KIS_API_INFO.txt"
    api_info = load_kis_api_info(API_INFO_PATH)
    
    APP_KEY = api_info.get('APP_KEY')
    APP_SECRET = api_info.get('APP_Secret')
    ACC_NO = api_info.get('account_number')
    
    print("한국투자증권 API 연결 중...")
    
    # 모의투자 모드로 연결
    broker = mojito.KoreaInvestment(
        api_key=APP_KEY,
        api_secret=APP_SECRET,
        acc_no=ACC_NO,
        mock=True
    )
    print("[OK] API 연결 성공!")
    
    # 코스피200 선물 종목코드 확인을 위해 사용 가능한 메서드 확인
    print("\n[INFO] mojito 객체의 선물 관련 메서드 확인...")
    methods = [m for m in dir(broker) if 'future' in m.lower() or 'ftr' in m.lower() or 'ohlcv' in m.lower()]
    print(f"관련 메서드: {methods}")
    
    # 코스피200 선물 종목코드 (24시간 연속선물)
    # 101SC000: 코스피200 선물 연속 (근월물 기준)
    # 시도할 종목코드들
    future_codes = [
        "101SC000",   # 코스피200 선물 연속
        "101S3000",   # 코스피200 선물 근월물
        "201SC000",   # 24시간 연속선물 시도
    ]
    
    for symbol in future_codes:
        print(f"\n{symbol} 선물 분봉 데이터 조회 시도...")
        
        try:
            # 선물 분봉 데이터 조회 시도
            resp = broker.fetch_today_1m_ohlcv(symbol)
            
            if 'output2' in resp and resp['output2']:
                df = pd.DataFrame(resp['output2'])
                print(f"[OK] {symbol}: {len(df)}개의 분봉 데이터 수신!")
                
                # 응답 데이터 구조 확인
                print(f"컬럼: {df.columns.tolist()}")
                print(df.head(3))
                
                return df, symbol
            else:
                print(f"[INFO] {symbol}: 데이터 없음")
                if 'msg1' in resp:
                    print(f"  메시지: {resp.get('msg1', '')}")
                    
        except Exception as e:
            print(f"[ERROR] {symbol}: {e}")
    
    # 다른 방법 시도: 해외선물 API 사용
    print("\n[INFO] 해외선물 API로 코스피200 야간선물 조회 시도...")
    try:
        # 해외 선물 시세 조회 (SGX 코스피200 선물)
        resp = broker.fetch_price("KQ")  # SGX KOSPI 200 futures
        print(f"SGX 코스피200 선물 응답: {resp}")
    except Exception as e:
        print(f"[ERROR] SGX 시도 실패: {e}")
    
    return None, None

if __name__ == "__main__":
    df, symbol = plot_kospi200_futures_from_kis()
    
    if df is None:
        print("\n" + "="*60)
        print("[안내] 코스피200 24시간 연속선물 종목코드 확인이 필요합니다.")
        print("한국투자증권 HTS/MTS에서 정확한 종목코드를 확인해 주세요.")
        print("="*60)
