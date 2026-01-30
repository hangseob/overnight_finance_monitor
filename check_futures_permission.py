import requests

def load_kis_api_info(filepath):
    api_info = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '\t' in line:
                key, value = line.split('\t', 1)
                api_info[key] = value
    return api_info

API_INFO_PATH = r"C:\Users\hangs\OneDrive\GitRepositories_related_private_data\KIS_API_INFO.txt"
api_info = load_kis_api_info(API_INFO_PATH)

APP_KEY = api_info.get('APP_KEY')
APP_SECRET = api_info.get('APP_Secret')

# Access Token 발급
print("Access Token 발급 중...")
token_url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
token_body = {
    "grant_type": "client_credentials",
    "appkey": APP_KEY,
    "appsecret": APP_SECRET
}

token_res = requests.post(token_url, json=token_body)
if token_res.status_code == 200:
    access_token = token_res.json().get("access_token")
    print(f"[OK] Access Token 발급 성공 (길이: {len(access_token)})")
else:
    print(f"[ERROR] Token 발급 실패: {token_res.text}")
    exit()

# 선물 현재가 조회 (권한 테스트)
print("\n=== 코스피200 선물 현재가 조회 (권한 테스트) ===")

url = "https://openapi.koreainvestment.com:9443/uapi/domestic-futureoption/v1/quotations/inquire-price"

headers = {
    "content-type": "application/json; charset=utf-8",
    "authorization": f"Bearer {access_token}",
    "appkey": APP_KEY,
    "appsecret": APP_SECRET,
    "tr_id": "FHMIF10000000",  # 선물 현재가 조회
    "custtype": "P"
}

params = {
    "FID_COND_MRKT_DIV_CODE": "F",  # F: 선물
    "FID_INPUT_ISCD": "101SC000"    # 코스피200 선물 연속
}

res = requests.get(url, headers=headers, params=params)

print(f"HTTP 상태: {res.status_code}")

if res.status_code == 200:
    data = res.json()
    print(f"응답 코드: {data.get('rt_cd')}")
    print(f"메시지: {data.get('msg1')}")
    
    if data.get('rt_cd') == '0':
        output = data.get('output', {})
        futs_prpr = output.get('futs_prpr', 'N/A')
        
        if futs_prpr and futs_prpr != '0' and futs_prpr != 'N/A':
            print(f"\n[SUCCESS] 선물 현재가: {futs_prpr}")
            print(f"    고가: {output.get('futs_hgpr')}")
            print(f"    저가: {output.get('futs_lwpr')}")
            print(f"    거래량: {output.get('acml_vol')}")
            print("\n>>> 파생상품 권한이 정상적으로 설정되어 있습니다!")
        else:
            print(f"\n[WARNING] 선물 현재가가 0입니다.")
            print(f"    - 장 마감 후라 시세가 없을 수 있습니다.")
            print(f"    - 또는 파생상품 권한이 없을 수 있습니다.")
            print(f"\n원시 응답: {output}")
    else:
        print(f"\n[ERROR] API 오류")
        print(f"메시지 코드: {data.get('msg_cd')}")
        print(f"상세 메시지: {data.get('msg1')}")
        
        if 'EGW' in data.get('msg_cd', ''):
            print("\n>>> 파생상품 권한이 없을 가능성이 높습니다!")
            print(">>> KIS Developers 포털에서 권한을 확인해주세요.")
else:
    print(f"[ERROR] HTTP 오류: {res.text[:500]}")
