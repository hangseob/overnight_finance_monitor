import asyncio
from playwright.async_api import async_playwright
import os
import time

async def verify_dash_app():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "http://127.0.0.1:8050"
        print(f"Connecting to {url}...")
        
        # 앱이 뜰 때까지 최대 30초 대기
        max_retries = 10
        for i in range(max_retries):
            try:
                await page.goto(url, wait_until="networkidle", timeout=5000)
                print("Successfully connected to the app.")
                break
            except Exception as e:
                if i == max_retries - 1:
                    print(f"Failed to connect after {max_retries} retries: {e}")
                    await browser.close()
                    return
                print(f"Retry {i+1}/{max_retries}...")
                await asyncio.sleep(3)

        # 페이지 제목 확인
        title = await page.title()
        print(f"Page Title: {title}")

        # 데이터가 로드될 때까지 잠시 대기 (interval 실행 대기)
        print("Waiting for data to load...")
        await asyncio.sleep(5)

        # 스크린샷 저장
        screenshot_path = "dash_render/tests/app_screenshot.png"
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        # 주요 요소 텍스트 추출
        price_text = await page.inner_text("#current-delayed-price")
        time_text = await page.inner_text("#current-delayed-time")
        
        print(f"Detected Price: {price_text}")
        print(f"Detected Time: {time_text}")

        # 테이블 행 개수 확인
        rows = await page.query_selector_all("#history-table tr")
        print(f"Number of rows in history table: {len(rows)}")

        if "No Data" in price_text:
            print("WARNING: Price display shows 'No Data'. Check data_manager logic.")
        else:
            print("SUCCESS: App seems to be displaying data correctly.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_dash_app())
