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

        # 1. Login
        page.fill("#username-input", "TEST_USER")
        page.click("#start-btn")

        # 2. Wait for Event Buttons (inside #controls, visible)
        print("Waiting for event buttons...")
        try:
            # Wait for buttons inside #controls to appear
            page.wait_for_selector("#controls .control-btn", state="visible", timeout=10000)

            buttons = page.locator("#controls .control-btn").all_inner_texts()
            print(f"Event Choices: {buttons}")

            # Click first choice
            page.locator("#controls .control-btn").first.click()
            print("Clicked choice.")

            # Wait for 'Next Quarter' button
            # It appears after typewriter effect of result log (text length * 15ms) + 1000ms delay
            page.wait_for_selector("text=PROCEED TO NEXT QUARTER", timeout=10000)
            print("PASS: Next Quarter button appeared.")

            # Verify Stats Changed (e.g. Sanity/Wealth)
            # Just take screenshot
            page.screenshot(path="verification/refactor_gameplay_success.png")

        except Exception as e:
            print(f"FAIL: {e}")
            page.screenshot(path="verification/refactor_fail.png")

        browser.close()

if __name__ == "__main__":
    run()
