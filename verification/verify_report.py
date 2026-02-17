import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        cwd = os.getcwd()
        filepath = os.path.join(cwd, 'index.html')
        page.goto(f'file://{filepath}')

        # Login
        page.fill("#username-input", "TEST_USER")
        page.click("#start-btn")

        # Wait for init
        time.sleep(2)

        # Trigger Report (Q4 End)
        print("Forcing Year End Report...")
        page.evaluate("gameState.quarter = 5; triggerEvent();")

        # Check Report Screen visibility
        if page.is_visible("#report-screen"):
            print("PASS: Report screen visible.")

            # Check content
            content = page.inner_text("#report-content")
            print(f"Report Content Snippet: {content[:50]}...")

            # Close Report (Start Year 2)
            page.click("#report-close-btn")
            time.sleep(1)

            # Check Year 2 on HUD
            hud_text = page.inner_text("#time-display")
            print(f"HUD Time: {hud_text}")
            if "Y2 Q1" in hud_text:
                print("PASS: Year advanced to Y2 Q1.")
            else:
                print("FAIL: Year did not advance correctly.")

        else:
            print("FAIL: Report screen not visible.")

        browser.close()

if __name__ == "__main__":
    run()
