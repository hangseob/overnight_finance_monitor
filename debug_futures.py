import mojito
import pandas as pd
from datetime import datetime

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

broker = mojito.KoreaInvestment(
    api_key=APP_KEY,
    api_secret=APP_SECRET,
    acc_no=ACC_NO,
    mock=False  # 실전투자
)
print("[OK] API 연결 성공!")

# 코스피200 선물 연속 조회
symbol = "101SC000"
print(f"\n{symbol} 분봉 데이터 조회 중...")

resp = broker.fetch_today_1m_ohlcv(symbol)

if 'output2' in resp and resp['output2']:
    df = pd.DataFrame(resp['output2'])
    print(f"[OK] {len(df)}개의 분봉 데이터 수신")
    
    # 원시 데이터 확인
    print("\n[원시 데이터 - 처음 10개]")
    print(df.head(10))
    
    print("\n[원시 데이터 - 마지막 10개]")
    print(df.tail(10))
    
    # 유효한 데이터 필터링 (가격이 0이 아닌 것)
    df['close'] = pd.to_numeric(df['stck_prpr'], errors='coerce')
    valid_df = df[df['close'] > 0]
    print(f"\n[유효한 데이터: {len(valid_df)}개]")
    
    if len(valid_df) > 0:
        print(valid_df[['stck_bsop_date', 'stck_cntg_hour', 'stck_prpr', 'stck_hgpr', 'stck_lwpr', 'cntg_vol']].head(10))
        print("\n...")
        print(valid_df[['stck_bsop_date', 'stck_cntg_hour', 'stck_prpr', 'stck_hgpr', 'stck_lwpr', 'cntg_vol']].tail(10))
else:
    print("[WARNING] 데이터 없음")
    print(resp)
