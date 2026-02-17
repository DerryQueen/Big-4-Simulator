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

        # 1. Login Screen
        print("Checking Login Screen...")
        if page.is_visible("#login-screen"):
            print("PASS: Login screen visible.")
        else:
            print("FAIL: Login screen missing.")

        page.fill("#username-input", "TEST_USER")
        page.click("#start-btn")

        # 2. Check HUD
        page.wait_for_selector("#hud")
        user_display = page.inner_text("#user-display")
        print(f"HUD User Display: {user_display}")

        if "TEST_USER" in user_display:
            print("PASS: Username displayed correctly.")
        else:
            print("FAIL: Username incorrect.")

        # Check Initial Stats
        # Wealth starts at 1000, but initGame triggers event which adds Salary?
        # Wait for event trigger
        time.sleep(2) # Typewriter delay

        wealth_text = page.inner_text("#wealth-val")
        print(f"Wealth after init: {wealth_text}")

        # Salary for A1 is 500. Initial is 1000. Should be 1500?
        # triggerEvent adds salary.
        # But wait, triggerEvent is called inside initGame via setTimeout(..., 1000).

        # 3. Check Event Interaction
        # Wait for buttons
        try:
            page.wait_for_selector(".control-btn", timeout=5000)
            buttons = page.locator(".control-btn").all_inner_texts()
            print(f"Event Buttons: {buttons}")

            # Click first option
            page.click(".control-btn >> nth=0")

            # Wait for result log
            time.sleep(1)

            # Check for Next Button
            next_btn = page.locator("text=PROCEED TO NEXT QUARTER")
            if next_btn.is_visible():
                print("PASS: Next Quarter button appeared.")
                next_btn.click()
            else:
                print("FAIL: Next Quarter button not found.")

        except Exception as e:
            print(f"FAIL: Interaction error: {e}")

        # Screenshot
        page.screenshot(path="verification/refactor_gameplay.png")
        print("Screenshot taken.")

        browser.close()

if __name__ == "__main__":
    run()
