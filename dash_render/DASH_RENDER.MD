# DASH TEST PROJECT: S&P 500 Delayed Monitor

본 문서는 Dash를 이용한 S&P 500 선물 모니터링 시스템 구축 및 Render 배포 과정을 요약한 문서입니다.

## 1. 프로젝트 목표
- yfinance를 사용하여 S&P 500 선물(ES=F) 데이터를 1분 단위로 수집.
- 주말 등 시장 휴장 시에도 실시간 업데이트 로직을 확인하기 위해 **48시간 전 데이터**를 1분마다 하나씩 가져와 출력하는 기능을 구현.
- Dash를 이용한 모바일/PC 대응 반응형 웹 대시보드 제작.
- 클라우드 서비스(Render.com)를 통한 24시간 무중단 배포 성공.

## 2. 주요 진행 사항
- **데이터 로직:** `yfinance` API의 1분봉 수집 한계(최대 7~8일)를 확인하고, 정확히 T-48시간 시점의 데이터 포인트 1개를 추출하는 로직 구현.
- **Dash 앱 구축:** 
  - `dash-bootstrap-components`를 활용한 레이아웃 구성.
  - `dcc.Interval`을 이용한 1분 단위 자동 갱신 및 데이터 누적 표시.
- **환경 최적화:** 
  - Python 3.13 환경에서의 `threading` 이슈 해결을 위해 `debug=False` 설정.
  - Windows PowerShell 환경에서의 한글 깨짐 방지를 위한 UTF-8 및 시스템 환경 변수 설정.
- **검증 자동화:** 
  - Playwright를 통한 브라우저 렌더링 확인.
  - EasyOCR을 이용해 실제 화면에 찍힌 가격 정보를 인식하여 데이터 정합성 최종 검증.
- **클라우드 배포:** 
  - `requirements.txt` 최신화로 빌드 속도 개선.
  - Render CLI 설치 및 GitHub 연동을 통해 자동 배포 및 모니터링 체계 구축.

## 3. 최종 결과
- **배포 성공:** [https://overnight-finance-monitor-test.onrender.com/](https://overnight-finance-monitor-test.onrender.com/)
- **작동 확인:** T-48시간 전의 가격을 1분 간격으로 수집하여 실시간으로 테이블에 누적하는 것을 시각적으로 확인 완료.

## 4. 향후 계획
- 수집된 데이터를 영구 저장하기 위한 데이터베이스(DB) 연동.
- 주식 차트(Candlestick) 기능 고도화 및 타 종목 확장.

---
**DASH TEST PROJECT RENDER를 통한 배포까지 성공**
