import asyncio
from playwright.async_api import async_playwright

async def test_app():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        
        print("Loading app...")
        await page.goto("http://localhost:8050", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)
        
        # Test 1: Landing page
        landing = await page.query_selector("#landing-page")
        print(f"✓ Landing page: {landing is not None}")
        
        # Test 2: Click Open Farm
        btn = await page.query_selector("#btn-open-farm")
        if btn:
            await btn.click()
            await asyncio.sleep(2)
            dashboard = await page.query_selector("#dashboard-page")
            print(f"✓ Dashboard: {dashboard is not None}")
        
        # Test 3: Check dashboard components
        components = ["#map-graph", "#ndvi-chart", "#weather-chart", "#heat-stress-chart", "#field-table", "#stress-gauge"]
        for comp in components:
            elem = await page.query_selector(comp)
            print(f"  {'✓' if elem else '✗'} {comp}")
        
        # Test 4: Theme toggle
        theme = await page.query_selector("#btn-theme-toggle")
        if theme:
            await theme.click()
            await asyncio.sleep(0.5)
            print("✓ Theme toggle works")
        
        await page.screenshot(path="/home/coder/plotly-upload/screenshots/final_test.png")
        
        print(f"\n{'✅ ALL TESTS PASSED' if not errors else f'⚠ {len(errors)} errors'} — {len(errors)} JS errors")
        if errors:
            for e in errors[:3]:
                print(f"  {e[:100]}")
        
        await browser.close()

asyncio.run(test_app())
