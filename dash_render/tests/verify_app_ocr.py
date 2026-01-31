import asyncio
from playwright.async_api import async_playwright
import os
import easyocr
import numpy as np
from PIL import Image

async def verify_dash_app_with_ocr():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "http://127.0.0.1:8050"
        print(f"Connecting to {url} for OCR verification...")
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=10000)
        except Exception as e:
            print(f"Connection failed: {e}")
            await browser.close()
            return

        # 데이터가 렌더링될 때까지 충분히 대기
        print("Waiting for UI to stabilize...")
        await asyncio.sleep(10)

        # 스크린샷 저장
        screenshot_path = "dash_render/tests/app_screenshot_for_ocr.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved for OCR: {screenshot_path}")

        # DOM에서 텍스트 직접 추출 (비교용)
        dom_price = await page.inner_text("#current-delayed-price")
        print(f"DOM Price: {dom_price}")

        await browser.close()

        # OCR 수행
        print("Starting OCR analysis using EasyOCR...")
        reader = easyocr.Reader(['ko', 'en']) # 한국어와 영어 지원
        results = reader.readtext(screenshot_path)

        print("\n--- OCR Detected Text ---")
        found_price_visually = False
        for (bbox, text, prob) in results:
            print(f"Text: {text} (Confidence: {prob:.2f})")
            # DOM에서 가져온 가격이 OCR 결과에 포함되어 있는지 확인
            if dom_price.replace("$", "").replace(",", "") in text.replace(",", ""):
                found_price_visually = True

        print("\n--- Verification Summary ---")
        if found_price_visually:
            print(f"SUCCESS: OCR successfully detected the price '{dom_price}' on the screen.")
        else:
            print(f"WARNING: OCR could not clearly match the price '{dom_price}'. Visual glitches may exist.")

if __name__ == "__main__":
    asyncio.run(verify_dash_app_with_ocr())
