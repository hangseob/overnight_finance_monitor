import dash
from dash import dcc, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
from data_manager import get_sp500_futures_at_time
import pandas as pd
from datetime import datetime, timedelta
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Starting Dash App initialization...")

try:
    # Dash 앱 초기화
    app = dash.Dash(
        __name__, 
        external_stylesheets=[dbc.themes.FLATLY],
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
    )
    server = app.server
    logger.info("Dash App and Server initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Dash App: {e}", exc_info=True)
    raise

app.layout = dbc.Container([
    dcc.Store(id='data-history-store', data=[]), # 과거 데이터 저장소
    
    dbc.Row([
        dbc.Col(html.H1("S&P 500 Delayed Monitor (T-48h)", className="text-center my-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.P("이 화면은 매 1분마다 '48시간 전'의 1분봉 종가를 가져와 테이블에 추가합니다.", className="lead"),
                html.P("주말 동안 실시간 데이터가 없을 때, 화면 업데이트 및 로직 테스트를 위한 용도입니다.", className="text-muted")
            ], className="text-center mb-4")
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Latest Delayed Price (48h ago)"),
                dbc.CardBody([
                    html.H2(id="current-delayed-price", className="text-primary text-center"),
                    html.P(id="current-delayed-time", className="text-center text-muted")
                ])
            ], className="mb-4")
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("History of Fetched Points"),
                dbc.CardBody(
                    dash_table.DataTable(
                        id='history-table',
                        columns=[
                            {"name": "Historical Time (T-48h)", "id": "Time"},
                            {"name": "Price", "id": "Price"}
                        ],
                        data=[],
                        page_size=15,
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'center'},
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    )
                )
            ])
        ], width=12)
    ]),
    
    dcc.Interval(
        id='interval-component',
        interval=60*1000, # 1분마다 실행
        n_intervals=0
    )
], fluid=True)

@app.callback(
    [Output('data-history-store', 'data'),
     Output('current-delayed-price', 'children'),
     Output('current-delayed-time', 'children'),
     Output('history-table', 'data')],
    [Input('interval-component', 'n_intervals')],
    [State('data-history-store', 'data')]
)
def update_delayed_data(n_intervals, existing_data):
    logger.info(f"Interval triggered (n_intervals={n_intervals}). Fetching delayed data...")
    
    # 현재 시간 기준 48시간 전 계산
    target_time = datetime.now() - timedelta(hours=48)
    logger.info(f"Targeting historical time: {target_time}")
    
    # 데이터 가져오기
    try:
        new_point = get_sp500_futures_at_time(target_time)
        
        if new_point:
            # 중복 체크
            if not any(d['Time'] == new_point['Time'] for d in existing_data):
                existing_data.insert(0, new_point)
                logger.info(f"New data point added to history: {new_point}")
            else:
                logger.info("Data point already exists in history. Skipping.")
        else:
            logger.warning("No new data point found for the target time.")
    except Exception as e:
        logger.error(f"Error during callback update: {e}", exc_info=True)
    
    # 최대 1000개까지만 유지
    updated_history = existing_data[:1000]
    
    if not updated_history:
        return [], "No Data", "Fetching...", []
        
    latest = updated_history[0]
    price_display = f"${latest['Price']:,.2f}"
    time_display = f"Target Time: {latest['Time']}"
    
    return updated_history, price_display, time_display, updated_history

if __name__ == '__main__':
    logger.info("Running Dash server on http://127.0.0.1:8050/")
    # debug=True에서 발생하는 threading 이슈 방지를 위해 debug=False 설정
    app.run(debug=False)
