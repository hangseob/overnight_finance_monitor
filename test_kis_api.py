import mojito

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

# API 정보 파일 경로
API_INFO_PATH = r"C:\Users\hangs\OneDrive\GitRepositories_related_private_data\KIS_API_INFO.txt"

# API 정보 로드
api_info = load_kis_api_info(API_INFO_PATH)
APP_KEY = api_info.get('APP_KEY')
APP_SECRET = api_info.get('APP_Secret')
ACC_NO = api_info.get('account_number')

print("한국투자증권 API 연결 테스트 시작...")
print(f"- 계좌번호: {ACC_NO}")

try:
    # 모의투자 모드로 연결 (mock=True)
    broker = mojito.KoreaInvestment(
        api_key=APP_KEY,
        api_secret=APP_SECRET,
        acc_no=ACC_NO,
        mock=True  # 모의투자
    )
    print("[OK] API 연결 성공!")
    
    # 삼성전자(005930) 현재가 조회 테스트
    print("\n삼성전자(005930) 현재가 조회 중...")
    price = broker.fetch_price("005930")
    
    if 'output' in price:
        current_price = price['output'].get('stck_prpr', 'N/A')
        stock_name = price['output'].get('stck_shrn_iscd', '삼성전자')
        print(f"[OK] 삼성전자 현재가: {current_price}원")
    else:
        print("응답 데이터:")
        print(price)
        
except Exception as e:
    print(f"[ERROR] 오류 발생: {e}")
    print("\n[디버깅 정보]")
    print(f"- APP_KEY 길이: {len(APP_KEY) if APP_KEY else 0}")
    print(f"- APP_SECRET 길이: {len(APP_SECRET) if APP_SECRET else 0}")
    print(f"- 계좌번호: {ACC_NO}")
