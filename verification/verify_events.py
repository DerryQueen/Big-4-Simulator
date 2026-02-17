import os
import random
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the file
        cwd = os.getcwd()
        filepath = os.path.join(cwd, 'index.html')
        page.goto(f'file://{filepath}')

        # Take initial screenshot
        page.screenshot(path='verification/step1_start.png')
        print("Initial state screenshot taken.")

        # Click "开始工作"
        page.get_by_role("button", name="开始工作").click()
        page.wait_for_timeout(500)

        # Take screenshot of event
        page.screenshot(path='verification/step2_event.png')
        print("Event screenshot taken.")

        # Get buttons
        buttons = page.locator("#controls button")
        count = buttons.count()
        print(f"Found {count} choices.")

        # Click the first choice
        buttons.first.click()
        page.wait_for_timeout(500)

        # Take screenshot of result
        page.screenshot(path='verification/step3_result.png')
        print("Result screenshot taken.")

        # Verify "Next Week / Continue" button
        next_btn = page.get_by_role("button", name="下一周 / 继续")
        if next_btn.is_visible():
            print("Next Week button visible.")
            next_btn.click()
            page.wait_for_timeout(500)
            page.screenshot(path='verification/step4_next_event.png')
            print("Next event screenshot taken.")
        else:
            print("Next Week button NOT visible (maybe Game Over?).")

        browser.close()

if __name__ == "__main__":
    run()
