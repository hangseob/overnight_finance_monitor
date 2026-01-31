
한국시간 오후 3시반이 되면 나스닥 & s&p선물 가격을 oracle DB에 입력한다. 

오라클 연결은 C:\GitRepositories\financeDataAccumulation\basic_library\oracle_client.py 참조

현ㅈ

한국시간 오후 3시반이 되면 나스닥 & s&p선물 가격을 oracle DB에 입력한다. 


*코스피24시간 선물은 한국투자증권 API사용하면 될듯

## Dash 기반 S&P 500 선물 모니터링 (dash_render/)
- **목적:** Dash와 Plotly를 이용한 실시간 선물 가격 모니터링 대시보드 구축 및 Render 배포 테스트.
- **특징:** 주말 테스트를 위한 48시간 지연 데이터 업데이트 로직 구현.
- **상세 내용:** [dash_render/README_SUMMARY.md](dash_render/README_SUMMARY.md) 참조