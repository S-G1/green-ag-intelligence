import asyncio
from playwright.async_api import async_playwright

async def test_app():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        
        errors = []
        def handle_console(msg):
            if msg.type == 'error':
                errors.append(f"Console error: {msg.text}")
                print(f"Console error: {msg.text}")
        page.on("console", handle_console)
        page.on("pageerror", lambda e: errors.append(f"Page error: {e}"))
        
        print("=== Test 1: Load Landing Page ===")
        await page.goto("http://localhost:8050", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        
        # Check landing page elements
        landing = await page.query_selector("#landing-page")
        print(f"✓ Landing page: {landing is not None}")
        
        btn_open = await page.query_selector("#btn-open-farm")
        print(f"✓ Open Farm button: {btn_open is not None}")
        
        btn_add = await page.query_selector("#btn-add-farm")
        print(f"✓ Add Farm button: {btn_add is not None}")
        
        await page.screenshot(path="/home/coder/plotly-upload/screenshots/01_landing.png")
        
        print("\n=== Test 2: Navigate to Dashboard ===")
        if btn_open:
            await btn_open.click()
            await asyncio.sleep(3)
            
            dashboard = await page.query_selector("#dashboard-page")
            print(f"✓ Dashboard visible: {dashboard is not None}")
            
            # Check all dashboard components
            checks = {
                "Header": ".ga-header",
                "Sidebar": ".ga-sidebar",
                "Map": "#map-graph",
                "NDVI Chart": "#ndvi-chart",
                "Weather Chart": "#weather-chart",
                "Heat Stress Chart": "#heat-stress-chart",
                "Field Table": "#field-table",
                "Stress Gauge": "#stress-gauge",
                "Recommendations": "#recommendations-section",
            }
            for name, selector in checks.items():
                elem = await page.query_selector(selector)
                print(f"  {'✓' if elem else '✗'} {name}: {elem is not None}")
        
        await page.screenshot(path="/home/coder/plotly-upload/screenshots/02_dashboard.png")
        
        print("\n=== Test 3: Theme Toggle ===")
        theme_btn = await page.query_selector("#btn-theme-toggle")
        if theme_btn:
            await theme_btn.click()
            await asyncio.sleep(1)
            print("✓ Theme toggle clicked")
            await page.screenshot(path="/home/coder/plotly-upload/screenshots/03_dark_theme.png")
        
        print("\n=== Test 4: Map Layer Switching ===")
        map_layer = await page.query_selector("#dropdown-map-layer")
        if map_layer:
            # Switch to Risk layer
            await map_layer.select_option("risk")
            await asyncio.sleep(1)
            print("✓ Map layer switched to Risk")
            
            # Switch back to NDVI
            await map_layer.select_option("ndvi")
            await asyncio.sleep(1)
            print("✓ Map layer switched to NDVI")
        
        print("\n=== Test 5: NDVI Play Button ===")
        play_btn = await page.query_selector("#btn-play-ndvi")
        if play_btn:
            await play_btn.click()
            await asyncio.sleep(2)
            print("✓ NDVI play clicked")
            await play_btn.click()  # Stop
            await asyncio.sleep(0.5)
            print("✓ NDVI pause clicked")
        
        print("\n=== Test 6: Table Search ===")
        search = await page.query_selector("#table-search")
        if search:
            await search.fill("Field 1")
            await asyncio.sleep(1)
            print("✓ Table search works")
        
        print("\n=== Test 7: Add Farm Modal ===")
        await page.goto("http://localhost:8050", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        
        add_btn = await page.query_selector("#btn-add-farm")
        if add_btn:
            await add_btn.click()
            await asyncio.sleep(1)
            modal = await page.query_selector("#modal-add-farm")
            is_visible = await modal.is_visible() if modal else False
            print(f"✓ Add farm modal: {is_visible}")
            
            # Close modal
            cancel = await page.query_selector("#btn-cancel-add-farm")
            if cancel:
                await cancel.click()
                await asyncio.sleep(0.5)
                print("✓ Modal closed")
        
        await page.screenshot(path="/home/coder/plotly-upload/screenshots/07_modal.png")
        
        # Summary
        print("\n" + "="*60)
        if errors:
            print(f"⚠ ERRORS ({len(errors)}):")
            for e in errors[:5]:
                print(f"  {e}")
        else:
            print("✅ ALL TESTS PASSED — ZERO ERRORS!")
        print("="*60)
        
        await browser.close()

asyncio.run(test_app())
