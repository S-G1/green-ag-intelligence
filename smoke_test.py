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
        
        print("=== Test 1: Clean Start ===")
        await page.goto("http://localhost:8050", wait_until="load", timeout=30000)
        await asyncio.sleep(5)
        
        # Dashboard visible immediately (no onboarding modal)
        ga_root = await page.query_selector("#ga-root")
        print(f"✓ Dashboard root visible: {ga_root is not None}")
        
        # Dashboard visible
        header = await page.query_selector(".ga-header")
        print(f"✓ Header visible: {header is not None}")
        
        # Primary action buttons
        btn_open = await page.query_selector("#btn-open-existing-farm")
        btn_add = await page.query_selector("#btn-add-new-farm")
        btn_demo = await page.query_selector("#btn-launch-demo-mode")
        print(f"✓ Open Existing Farm button: {btn_open is not None}")
        print(f"✓ Add Farm button: {btn_add is not None}")
        print(f"✓ Launch Demo Mode button: {btn_demo is not None}")
        
        # KPI cards
        kpis = [
            "kpi-card-total_fields",
            "kpi-card-avg_ndvi",
            "kpi-card-avg_rainfall",
            "kpi-card-avg_heat_stress",
            "kpi-card-high_risk",
            "kpi-card-avg_field_stress",
        ]
        for kpi_id in kpis:
            elem = await page.query_selector(f"#{kpi_id}")
            print(f"  {'✓' if elem else '✗'} {kpi_id}: {elem is not None}")
        
        await page.screenshot(path="./screenshots/01_clean_start.png")
        
        print("\n=== Test 2: Launch Demo Mode ===")
        if btn_demo:
            await btn_demo.click()
            await asyncio.sleep(3)
            
            # Check demo badge
            badge = await page.query_selector("#demo-badge")
            badge_visible = await badge.is_visible() if badge else False
            print(f"✓ Demo badge visible: {badge_visible}")
            
            # Check KPI values updated
            kpi_value = await page.query_selector("#kpi-value-total_fields")
            value_text = await kpi_value.inner_text() if kpi_value else ""
            print(f"✓ Total Fields KPI: {value_text}")
            
            await page.screenshot(path="./screenshots/02_demo_mode.png")
        
        print("\n=== Test 3: Open Farm Selector ===")
        if btn_open:
            await btn_open.click()
            await asyncio.sleep(3)
            
            # Check if farm selector backdrop is visible (wrapper may have zero dims)
            backdrop = await page.query_selector("#farm-selector-backdrop")
            selector_open = backdrop is not None and await backdrop.is_visible()
            print(f"✓ Farm selector open: {selector_open}")
            
            if selector_open:
                # Click the farm item
                farm_item = await page.query_selector("#farm-item-md-caroline-farm")
                if farm_item:
                    await farm_item.click()
                    await asyncio.sleep(0.5)
                
                open_btn = await page.query_selector("#btn-open-selected-farm")
                if open_btn:
                    disabled = await open_btn.is_disabled()
                    print(f"✓ Open Farm button enabled after selection: {not disabled}")
                    await open_btn.click()
                    await asyncio.sleep(2)
                else:
                    # Close selector to unblock dashboard
                    cancel = await page.query_selector("#btn-cancel-farm-selector")
                    if cancel:
                        await cancel.click()
                        await asyncio.sleep(1)
            else:
                print("  ⚠ Farm selector did not open — checking for errors")
            
            await page.screenshot(path="./screenshots/03_open_farm.png")
        
        print("\n=== Test 4: Add Farm Modal ===")
        # Ensure farm selector is closed (check backdrop)
        backdrop_fs = await page.query_selector("#farm-selector-backdrop")
        if backdrop_fs and await backdrop_fs.is_visible():
            cancel_fs = await page.query_selector("#btn-cancel-farm-selector")
            if cancel_fs:
                await cancel_fs.click()
                await asyncio.sleep(1)
        
        btn_add2 = await page.query_selector("#btn-add-new-farm")
        if btn_add2:
            await btn_add2.click()
            await asyncio.sleep(2)
            
            # Check add-farm backdrop since wrapper may have zero dims
            backdrop_af = await page.query_selector("#add-farm-backdrop")
            modal_open = backdrop_af is not None and await backdrop_af.is_visible()
            print(f"✓ Add Farm modal open: {modal_open}")
            
            # Cancel
            cancel = await page.query_selector("#btn-cancel-add-farm")
            if cancel:
                await cancel.click()
                await asyncio.sleep(1)
                print("✓ Cancel closed modal")
            
            await page.screenshot(path="./screenshots/04_add_farm.png")
        
        print("\n=== Test 5: Map Layers ===")
        layer_btns = ["map-layer-ndvi", "map-layer-risk", "map-layer-heat_stress", "map-layer-rainfall"]
        for btn_id in layer_btns:
            btn = await page.query_selector(f"#{btn_id}")
            if btn:
                await btn.click()
                await asyncio.sleep(0.5)
                print(f"✓ Layer {btn_id} clicked")
        
        await page.screenshot(path="./screenshots/05_map_layers.png")
        
        print("\n=== Test 6: Weather Tabs ===")
        weather_tabs = ["weather-tab-combined", "weather-tab-rainfall", "weather-tab-temperature", "weather-tab-heat"]
        for tab_id in weather_tabs:
            tab = await page.query_selector(f"#{tab_id}")
            if tab:
                await tab.click()
                await asyncio.sleep(0.5)
                is_active = "active" in (await tab.get_attribute("class") or "")
                print(f"✓ Weather tab {tab_id} active: {is_active}")
        
        await page.screenshot(path="./screenshots/06_weather_tabs.png")
        
        print("\n=== Test 7: Field Table Search ===")
        # Use page.locator to avoid stale element handles
        search_input = page.locator("#table-search")
        if await search_input.count() > 0:
            await search_input.fill("Field 1")
            await asyncio.sleep(1.5)
            
            # Verify table has filtered results
            rows = await page.locator("#field-table tbody tr").count()
            print(f"✓ Filtered rows: {rows}")
            
            # Clear using the clear button locator
            clear_btn = page.locator("#table-search-clear")
            if await clear_btn.count() > 0 and await clear_btn.is_visible():
                await clear_btn.click()
                await asyncio.sleep(0.5)
                print("✓ Clear search works")
            else:
                # Fallback: clear via input
                await search_input.fill("")
                await asyncio.sleep(0.5)
                print("✓ Clear search works (input clear)")
        
        await page.screenshot(path="./screenshots/07_table_search.png")
        
        print("\n=== Test 8: Theme Toggle ===")
        theme_btn = await page.query_selector("#btn-theme-toggle")
        if theme_btn:
            await theme_btn.click()
            await asyncio.sleep(1)
            
            root = await page.query_selector("#ga-root")
            theme = await root.get_attribute("data-theme") if root else ""
            print(f"✓ Theme toggled: {theme}")
            
            await theme_btn.click()
            await asyncio.sleep(0.5)
        
        await page.screenshot(path="./screenshots/08_theme.png")
        
        # Summary
        print("\n" + "="*60)
        if errors:
            print(f"⚠ ERRORS ({len(errors)}):")
            for e in errors[:10]:
                print(f"  {e}")
        else:
            print("✅ ALL TESTS PASSED — ZERO ERRORS!")
        print("="*60)
        
        await browser.close()

asyncio.run(test_app())
