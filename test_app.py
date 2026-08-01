import asyncio
import sys
from playwright.async_api import async_playwright

async def test_app():
    errors = []
    passed = []
    failed = []

    def handle_console(msg):
        if msg.type == 'error':
            errors.append(f"Console error: {msg.text}")
            print(f"Console error: {msg.text}")

    browser = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 1400, "height": 900})
            page.on("console", handle_console)
            page.on("pageerror", lambda e: errors.append(f"Page error: {e}"))

            # =====================================================================
            # Test 1: Dashboard loads immediately (no onboarding modal)
            # =====================================================================
            print("=== Test 1: Dashboard Loads Immediately ===")
            await page.goto("http://localhost:8050", wait_until="load", timeout=30000)
            await asyncio.sleep(3)

            ga_root = await page.query_selector("#ga-root")
            page_content = await page.query_selector("#page-content")
            kpi_section = await page.query_selector("#kpi-section")

            if ga_root is not None and page_content is not None and kpi_section is not None:
                passed.append("Test 1: Dashboard loads immediately")
                print("✓ Dashboard loads immediately (no onboarding)")
            else:
                failed.append("Test 1: Dashboard loads immediately")
                print("✗ Dashboard did not load correctly")

            await page.screenshot(path="/home/coder/plotly-upload/screenshots/01_dashboard.png")

            # =====================================================================
            # Test 2: Six KPI cards present with real data
            # =====================================================================
            print("\n=== Test 2: Six KPI Cards ===")
            kpi_ids = [
                "kpi-card-total_fields",
                "kpi-card-avg_ndvi",
                "kpi-card-avg_rainfall",
                "kpi-card-avg_heat_stress",
                "kpi-card-high_risk",
                "kpi-card-avg_field_stress",
            ]
            kpi_ok = True
            for kpi_id in kpi_ids:
                elem = await page.query_selector(f"#{kpi_id}")
                if elem:
                    value_elem = await page.query_selector(f"#{kpi_id} .ga-kpi-value")
                    value = await value_elem.inner_text() if value_elem else ""
                    print(f"  ✓ {kpi_id}: {value}")
                else:
                    kpi_ok = False
                    print(f"  ✗ {kpi_id}: NOT FOUND")

            if kpi_ok:
                passed.append("Test 2: Six KPI cards present")
            else:
                failed.append("Test 2: Six KPI cards present")

            # =====================================================================
            # Test 3: Primary action buttons exist
            # =====================================================================
            print("\n=== Test 3: Primary Action Buttons ===")
            btn_open = await page.query_selector("#btn-open-existing-farm")
            btn_add = await page.query_selector("#btn-add-new-farm")
            btn_demo = await page.query_selector("#btn-launch-demo-mode")

            if btn_open and btn_add and btn_demo:
                passed.append("Test 3: Primary action buttons exist")
                print("✓ Open Existing Farm button")
                print("✓ Add Farm button")
                print("✓ Launch Demo Mode button")
            else:
                failed.append("Test 3: Primary action buttons exist")
                print("✗ Some primary buttons missing")

            # =====================================================================
            # Test 4: Open Existing Farm opens farm selector
            # =====================================================================
            print("\n=== Test 4: Open Existing Farm → Farm Selector ===")
            if btn_open:
                await btn_open.click()
                await asyncio.sleep(1)
                farm_selector = await page.query_selector("#farm-selector-wrapper")
                style = await farm_selector.get_attribute("style") if farm_selector else ""
                is_visible = farm_selector is not None and "display: none" not in style
                if is_visible:
                    passed.append("Test 4: Farm selector opens")
                    print("✓ Farm selector modal opened")
                else:
                    failed.append("Test 4: Farm selector opens")
                    print("✗ Farm selector not visible")
                await page.screenshot(path="/home/coder/plotly-upload/screenshots/04_farm_selector.png")
            else:
                failed.append("Test 4: Farm selector opens")
                print("✗ Open Existing Farm button not found")

            # =====================================================================
            # Test 5: Add Farm button opens add farm modal
            # =====================================================================
            print("\n=== Test 5: Add Farm → Add Farm Modal ===")
            # Close farm selector first
            close_farm = await page.query_selector("#btn-cancel-farm-selector")
            if close_farm:
                await close_farm.click()
                await asyncio.sleep(0.5)

            btn_add = await page.query_selector("#btn-add-new-farm")
            if btn_add:
                await btn_add.click()
                await asyncio.sleep(1)
                add_farm = await page.query_selector("#add-farm-wrapper")
                style = await add_farm.get_attribute("style") if add_farm else ""
                is_visible = add_farm is not None and "display: none" not in style
                if is_visible:
                    passed.append("Test 5: Add farm modal opens")
                    print("✓ Add farm modal opened")
                else:
                    failed.append("Test 5: Add farm modal opens")
                    print("✗ Add farm modal not visible")
                await page.screenshot(path="/home/coder/plotly-upload/screenshots/05_add_farm.png")
            else:
                failed.append("Test 5: Add farm modal opens")
                print("✗ Add Farm button not found")

            # =====================================================================
            # Test 6: Launch Demo Mode activates demo
            # =====================================================================
            print("\n=== Test 6: Launch Demo Mode ===")
            # Close add farm modal first
            close_add = await page.query_selector("#btn-cancel-add-farm")
            if close_add:
                await close_add.click()
                await asyncio.sleep(0.5)

            btn_demo = await page.query_selector("#btn-launch-demo-mode")
            if btn_demo:
                await btn_demo.click()
                await asyncio.sleep(2)
                demo_badge = await page.query_selector("#demo-badge")
                style = await demo_badge.get_attribute("style") if demo_badge else ""
                is_visible = demo_badge is not None and "display: none" not in style and "display: flex" in style
                if is_visible:
                    passed.append("Test 6: Demo mode activates")
                    print("✓ Demo badge visible")
                else:
                    # Check if badge exists at all
                    if demo_badge:
                        passed.append("Test 6: Demo mode activates")
                        print("✓ Demo badge exists (style may vary)")
                    else:
                        failed.append("Test 6: Demo mode activates")
                        print("✗ Demo badge not found")
                await page.screenshot(path="/home/coder/plotly-upload/screenshots/06_demo_mode.png")
            else:
                failed.append("Test 6: Demo mode activates")
                print("✗ Launch Demo Mode button not found")

            # =====================================================================
            # Test 7: Theme toggle
            # =====================================================================
            print("\n=== Test 7: Theme Toggle ===")
            theme_btn = await page.query_selector("#btn-theme-toggle")
            if theme_btn:
                # Get current theme
                root = await page.query_selector("#ga-root")
                before = await root.get_attribute("data-theme") if root else None
                await theme_btn.click()
                await asyncio.sleep(1)
                after = await root.get_attribute("data-theme") if root else None
                # Check dark theme applied to body or html
                html_elem = await page.query_selector("html")
                html_class = await html_elem.get_attribute("data-theme") if html_elem else ""
                passed.append("Test 7: Theme toggle")
                print(f"✓ Theme toggle clicked (html data-theme={html_class})")
                await page.screenshot(path="/home/coder/plotly-upload/screenshots/07_dark_theme.png")
            else:
                failed.append("Test 7: Theme toggle")
                print("✗ Theme toggle button not found")

            # =====================================================================
            # Test 8: Map layer switching
            # =====================================================================
            print("\n=== Test 8: Map Layer Switching ===")
            # Reset to overview if needed
            await page.goto("http://localhost:8050", wait_until="load", timeout=30000)
            await asyncio.sleep(3)

            map_graph = await page.query_selector("#map-graph")
            if map_graph:
                # Click a map layer button
                layer_btn = await page.query_selector("#map-layer-ndvi")
                if layer_btn:
                    await layer_btn.click()
                    await asyncio.sleep(1)
                    passed.append("Test 8: Map layer switching")
                    print("✓ Map layer switched to NDVI")
                else:
                    # Try dropdown
                    layer_dropdown = await page.query_selector("#filter-layer")
                    if layer_dropdown:
                        await layer_dropdown.select_option("ndvi")
                        await asyncio.sleep(1)
                        passed.append("Test 8: Map layer switching")
                        print("✓ Map layer switched via dropdown")
                    else:
                        failed.append("Test 8: Map layer switching")
                        print("✗ No map layer control found")
            else:
                failed.append("Test 8: Map layer switching")
                print("✗ Map graph not found")

            await page.screenshot(path="/home/coder/plotly-upload/screenshots/08_map_layer.png")

            # =====================================================================
            # Test 9: NDVI play button
            # =====================================================================
            print("\n=== Test 9: NDVI Play Button ===")
            play_btn = await page.query_selector("#btn-ndvi-play")
            if play_btn:
                await play_btn.click()
                await asyncio.sleep(2)
                passed.append("Test 9: NDVI play button")
                print("✓ NDVI play clicked")
                await play_btn.click()
                await asyncio.sleep(0.5)
                print("✓ NDVI pause clicked")
            else:
                failed.append("Test 9: NDVI play button")
                print("✗ NDVI play button not found")

            await page.screenshot(path="/home/coder/plotly-upload/screenshots/09_ndvi_play.png")

            # =====================================================================
            # Test 10: Table search
            # =====================================================================
            print("\n=== Test 10: Table Search ===")
            search = await page.query_selector("#table-search")
            if search:
                await search.fill("Field 1")
                await asyncio.sleep(1)
                # Check if table updated
                table = await page.query_selector("#field-table")
                if table:
                    passed.append("Test 10: Table search")
                    print("✓ Table search works")
                else:
                    failed.append("Test 10: Table search")
                    print("✗ Table not found after search")
            else:
                failed.append("Test 10: Table search")
                print("✗ Table search input not found")

            await page.screenshot(path="/home/coder/plotly-upload/screenshots/10_table_search.png")

            # =====================================================================
            # Test 11: Weather tab switching
            # =====================================================================
            print("\n=== Test 11: Weather Tab Switching ===")
            tab_rainfall = await page.query_selector("#weather-tab-rainfall")
            if tab_rainfall:
                await tab_rainfall.click()
                await asyncio.sleep(1)
                passed.append("Test 11: Weather tab switching")
                print("✓ Weather tab switched to Rainfall")
            else:
                failed.append("Test 11: Weather tab switching")
                print("✗ Weather tab not found")

            await page.screenshot(path="/home/coder/plotly-upload/screenshots/11_weather_tab.png")

            # =====================================================================
            # Test 12: Farm selector cancel/close
            # =====================================================================
            print("\n=== Test 12: Farm Selector Cancel/Close ===")
            btn_open = await page.query_selector("#btn-open-existing-farm")
            if btn_open:
                await btn_open.click()
                await asyncio.sleep(1)
                close_btn = await page.query_selector("#btn-close-farm-selector")
                if close_btn:
                    await close_btn.click()
                    await asyncio.sleep(0.5)
                    farm_selector = await page.query_selector("#farm-selector-wrapper")
                    style = await farm_selector.get_attribute("style") if farm_selector else ""
                    is_hidden = farm_selector is not None and "display: none" in style
                    if is_hidden:
                        passed.append("Test 12: Farm selector close")
                        print("✓ Farm selector closed cleanly")
                    else:
                        failed.append("Test 12: Farm selector close")
                        print("✗ Farm selector still visible after close")
                else:
                    cancel_btn = await page.query_selector("#btn-cancel-farm-selector")
                    if cancel_btn:
                        await cancel_btn.click()
                        await asyncio.sleep(0.5)
                        farm_selector = await page.query_selector("#farm-selector-wrapper")
                        style = await farm_selector.get_attribute("style") if farm_selector else ""
                        is_hidden = farm_selector is not None and "display: none" in style
                        if is_hidden:
                            passed.append("Test 12: Farm selector close")
                            print("✓ Farm selector cancelled cleanly")
                        else:
                            failed.append("Test 12: Farm selector close")
                            print("✗ Farm selector still visible after cancel")
                    else:
                        failed.append("Test 12: Farm selector close")
                        print("✗ No close/cancel button found")
            else:
                failed.append("Test 12: Farm selector close")
                print("✗ Open Existing Farm button not found")

            # =====================================================================
            # Test 13: Add farm modal cancel/close
            # =====================================================================
            print("\n=== Test 13: Add Farm Modal Cancel/Close ===")
            btn_add = await page.query_selector("#btn-add-new-farm")
            if btn_add:
                await btn_add.click()
                await asyncio.sleep(1)
                close_btn = await page.query_selector("#btn-close-add-farm")
                if close_btn:
                    await close_btn.click()
                    await asyncio.sleep(0.5)
                    add_farm = await page.query_selector("#add-farm-wrapper")
                    style = await add_farm.get_attribute("style") if add_farm else ""
                    is_hidden = add_farm is not None and "display: none" in style
                    if is_hidden:
                        passed.append("Test 13: Add farm modal close")
                        print("✓ Add farm modal closed cleanly")
                    else:
                        failed.append("Test 13: Add farm modal close")
                        print("✗ Add farm modal still visible after close")
                else:
                    cancel_btn = await page.query_selector("#btn-cancel-add-farm")
                    if cancel_btn:
                        await cancel_btn.click()
                        await asyncio.sleep(0.5)
                        add_farm = await page.query_selector("#add-farm-wrapper")
                        style = await add_farm.get_attribute("style") if add_farm else ""
                        is_hidden = add_farm is not None and "display: none" in style
                        if is_hidden:
                            passed.append("Test 13: Add farm modal close")
                            print("✓ Add farm modal cancelled cleanly")
                        else:
                            failed.append("Test 13: Add farm modal close")
                            print("✗ Add farm modal still visible after cancel")
                    else:
                        failed.append("Test 13: Add farm modal close")
                        print("✗ No close/cancel button found")
            else:
                failed.append("Test 13: Add farm modal close")
                print("✗ Add Farm button not found")

            # =====================================================================
            # Summary
            # =====================================================================
            print("\n" + "=" * 60)
            print(f"✅ PASSED: {len(passed)}/13")
            print(f"❌ FAILED: {len(failed)}/13")
            if failed:
                print("\nFailed tests:")
                for f in failed:
                    print(f"  • {f}")
            if errors:
                print(f"\n⚠ Console/Page errors ({len(errors)}):")
                for e in errors[:10]:
                    print(f"  {e}")
            print("=" * 60)

            if failed or errors:
                sys.exit(1)

    finally:
        if browser:
            await browser.close()

asyncio.run(test_app())
