# S&P 500 Delayed Monitor (Dash + Render)

본 프로젝트는 S&P 500 선물(ES=F) 데이터를 Dash를 이용해 시각화하고, Render를 통해 배포하기 위한 대시보드입니다. 
특히 주말 동안 데이터 업데이트가 없을 때를 대비하여, **현재 시간 기준 48시간 전의 데이터**를 1분마다 하나씩 가져와 실시간 업데이트 로직을 테스트할 수 있도록 설계되었습니다.

## 주요 기능
- **T-48h 지연 모니터링:** 매 1분마다 48시간 전의 1분봉 종가를 수집하여 대시보드에 업데이트합니다.
- **실시간 데이터 누적:** 수집된 과거 데이터를 세션 동안 메모리에 누적하여 테이블 형태로 표시합니다.
- **반응형 UI:** `dash-bootstrap-components`를 사용하여 PC와 모바일 브라우저 모두에 최적화된 레이아웃을 제공합니다.
- **자동 갱신:** `dcc.Interval`을 통해 브라우저 새로고침 없이 1분마다 새로운 데이터 포인트가 추가됩니다.

## 프로젝트 구조
```text
dash_render/
├── app.py              # Dash 앱 메인 (UI, Callback, Server)
├── data_manager.py     # yfinance 데이터 수집 로직
├── requirements.txt    # 배포 의존성 목록
└── tests/              # 검증 및 테스트 코드
    ├── test_data.py        # 데이터 수집 기능 테스트
    ├── verify_app.py       # Playwright 브라우저 자동화 검증
    └── verify_app_ocr.py   # EasyOCR을 이용한 시각적 렌더링 검증
```

## 검증 완료 사항
- [x] **데이터 수집:** `yfinance`를 통한 특정 시점(T-48h) 1분봉 데이터 추출 성공.
- [x] **UI 렌더링:** Playwright를 이용한 브라우저 자동 접속 및 요소 확인 성공.
- [x] **시각적 검증:** EasyOCR을 사용하여 화면에 표시된 가격 정보가 실제 데이터와 일치함을 확인.
- [x] **호환성:** Python 3.13 환경에서 발생하는 threading 이슈 해결 (`debug=False`).

## 배포 가이드 (Render)
1. **Service Type:** Web Service
2. **Build Command:** `pip install -r requirements.txt`
3. **Start Command:** `gunicorn app:server`
4. **Environment:** Python 3.x (3.10 이상 추천)
