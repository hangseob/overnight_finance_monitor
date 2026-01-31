import mojito
import pandas as pd

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

# API 정보 로드
API_INFO_PATH = r"C:\Users\hangs\OneDrive\GitRepositories_related_private_data\KIS_API_INFO.txt"
api_info = load_kis_api_info(API_INFO_PATH)

APP_KEY = api_info.get('APP_KEY')
APP_SECRET = api_info.get('APP_Secret')
ACC_NO = api_info.get('account_number')

print("한국투자증권 API 연결 중 (실전투자 모드)...")

# 한국투자증권 API 객체 생성
korea_invest = mojito.KoreaInvestment(
    api_key=APP_KEY,
    api_secret=APP_SECRET,
    acc_no=ACC_NO,
    mock=False  # 실전투자
)
print("[OK] API 연결 성공!")

def get_kospi200_futures_minute_data(symbol="101V3000"):
    """
    KOSPI 200 선물 분봉 데이터를 조회하여 DataFrame으로 반환합니다.
    symbol: 종목코드 (예: 101V3000 - 2026년 3월물)
    """
    print(f"\n{symbol} 분봉 데이터 조회 중...")
    
    # fetch_ohlcv 메서드 사용
    res = korea_invest.fetch_ohlcv(
        symbol=symbol,
        timeframe='m',  # 'm'은 분봉
        adj_price=True
    )
    
    print(f"[DEBUG] 응답 키: {res.keys() if isinstance(res, dict) else type(res)}")
    
    if 'output2' in res and res['output2']:
        df = pd.DataFrame(res['output2'])
        print(f"[OK] {len(df)}개의 분봉 데이터 수신")
        print(f"[DEBUG] 컬럼: {df.columns.tolist()}")
        print(df.head(3))
        
        # 필요한 컬럼 선택 (컬럼명이 다를 수 있음)
        available_cols = df.columns.tolist()
        print(f"\n사용 가능한 컬럼: {available_cols}")
        
        # 가격 데이터 확인
        price_cols = [c for c in available_cols if 'prpr' in c or 'oprc' in c or 'hgpr' in c or 'lwpr' in c]
        print(f"가격 관련 컬럼: {price_cols}")
        
        return df
    elif 'output' in res:
        print(f"[INFO] output 데이터 확인")
        print(res['output'])
        return None
    else:
        print(f"[WARNING] 데이터 조회 실패")
        print(f"응답: {res}")
        return None

# 다양한 종목코드 시도
symbols_to_try = [
    "101V3000",  # 2026년 3월물 (V = 3월)
    "101SC000",  # 코스피200 선물 연속
    "101S3000",  # 코스피200 선물 근월물
]

print("\n=== 코스피200 선물 분봉 데이터 조회 테스트 ===")

for symbol in symbols_to_try:
    print(f"\n{'='*50}")
    futures_df = get_kospi200_futures_minute_data(symbol)
    
    if futures_df is not None and len(futures_df) > 0:
        # 가격이 유효한 데이터가 있는지 확인
        if 'stck_prpr' in futures_df.columns:
            futures_df['close'] = pd.to_numeric(futures_df['stck_prpr'], errors='coerce')
            valid_data = futures_df[futures_df['close'] > 0]
            if len(valid_data) > 0:
                print(f"\n[SUCCESS] {symbol}: 유효한 데이터 {len(valid_data)}개 발견!")
                print(valid_data.head(10))
                break
            else:
                print(f"[INFO] {symbol}: 데이터는 있지만 가격이 모두 0")
        elif 'futs_prpr' in futures_df.columns:
            futures_df['close'] = pd.to_numeric(futures_df['futs_prpr'], errors='coerce')
            valid_data = futures_df[futures_df['close'] > 0]
            if len(valid_data) > 0:
                print(f"\n[SUCCESS] {symbol}: 유효한 데이터 {len(valid_data)}개 발견!")
                print(valid_data.head(10))
                break
