import asyncio
from playwright.async_api import async_playwright

async def test_cables():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        
        # 1. Load SLD page
        print("1. Loading SLD view...")
        await page.goto("http://localhost:8000/clients/zoetis/b4/sld", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # 2. Check for feeder edges in SVG
        edges = await page.query_selector_all("g.feeder-edge, g.edge")
        print(f"Found {len(edges)} edges in SLD graph")
        assert len(edges) > 0, "No edges found in SLD diagram"

        # 3. Test clicking an edge in SLD
        print("2. Clicking first edge...")
        await edges[0].click(force=True)
        await page.wait_for_timeout(500)

        # Verify cable drawer is visible
        cable_drawer = await page.query_selector("[aria-labelledby='cable-drawer-title']")
        is_visible = await cable_drawer.is_visible() if cable_drawer else False
        print(f"Cable drawer visible after edge click: {is_visible}")
        assert is_visible, "Cable drawer did not open on edge click"

        # 4. Take screenshot of Cable Drawer
        await page.screenshot(path="scratch/cable_drawer_screenshot.png")
        print("Captured scratch/cable_drawer_screenshot.png")

        # 5. Close cable drawer
        close_btn = await page.query_selector("[aria-labelledby='cable-drawer-title'] button:has-text('✕')")
        if close_btn:
            await close_btn.click()
            await page.wait_for_timeout(300)

        # 6. Test opening Feeder Schedule modal from Toolbox
        print("3. Opening Toolbox and Feeder Schedule Modal...")
        toolbox_btn = await page.query_selector("button:has-text('Toolbox')")
        if toolbox_btn:
            await toolbox_btn.click()
            await page.wait_for_timeout(400)

            # Click Open Feeder Schedule button
            open_feeder_btn = await page.query_selector("button:has-text('Open Feeder Schedule')")
            if open_feeder_btn:
                await open_feeder_btn.click()
                await page.wait_for_timeout(500)

        feeder_modal = await page.query_selector("[aria-labelledby='feeder-schedule-modal-title']")
        modal_visible = await feeder_modal.is_visible() if feeder_modal else False
        print(f"Feeder Schedule Modal visible: {modal_visible}")
        assert modal_visible, "Feeder Schedule Modal did not open"

        # 7. Check rows in feeder schedule table
        rows = await page.query_selector_all("[aria-labelledby='feeder-schedule-modal-title'] tbody tr")
        print(f"Found {len(rows)} rows in Feeder Schedule Table")

        # 8. Take screenshot of Feeder Schedule
        await page.screenshot(path="scratch/feeder_schedule_screenshot.png")
        print("Captured scratch/feeder_schedule_screenshot.png")

        # 9. Test clicking an endpoint in the table
        from_pills = await page.query_selector_all("[aria-labelledby='feeder-schedule-modal-title'] tbody button:has-text('⚡')")
        if len(from_pills) > 0:
            print("4. Clicking From Endpoint pill in Feeder Table...")
            await from_pills[0].click()
            await page.wait_for_timeout(500)

            # Verify Edit Drawer opened for that equipment
            edit_drawer = await page.query_selector("[aria-labelledby='slide-over-title']")
            edit_visible = await edit_drawer.is_visible() if edit_drawer else False
            print(f"Equipment Edit Drawer visible after clicking From Endpoint: {edit_visible}")
            assert edit_visible, "Equipment Edit Drawer did not open when clicking From Endpoint in table"
            await page.screenshot(path="scratch/equipment_from_table_screenshot.png")

        await browser.close()
        print("All UI checks PASSED successfully!")

if __name__ == "__main__":
    asyncio.run(test_cables())
