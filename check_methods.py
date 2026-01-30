import mojito

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

broker = mojito.KoreaInvestment(
    api_key=api_info.get('APP_KEY'),
    api_secret=api_info.get('APP_Secret'),
    acc_no=api_info.get('account_number'),
    mock=False
)

print("=== mojito.KoreaInvestment 사용 가능한 모든 메서드 ===\n")

# 모든 public 메서드 출력
methods = [m for m in dir(broker) if not m.startswith('_')]
for m in sorted(methods):
    print(f"  - {m}")

print(f"\n총 {len(methods)}개 메서드")

# 선물/옵션 관련 메서드 찾기
print("\n=== 선물/옵션 관련 메서드 ===")
future_methods = [m for m in methods if any(kw in m.lower() for kw in ['future', 'ftr', 'option', 'opt', 'deriv'])]
for m in future_methods:
    print(f"  - {m}")

if not future_methods:
    print("  (선물 관련 메서드 없음)")
