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
        print("Checking Login...")
        page.fill("#username-input", "ModernUser")
        page.click("#start-btn")

        # 2. Check UI Layout
        page.wait_for_selector("#app-container")
        print("PASS: App container visible.")

        # Check background color (approximate)
        bg_color = page.evaluate("window.getComputedStyle(document.body).backgroundColor")
        print(f"Background Color: {bg_color}")
        # Should be rgb(248, 249, 250) for #F8F9FA

        # 3. Check Stats
        money_text = page.inner_text("#val-money")
        print(f"Money: {money_text}")
        if "w" in money_text:
            print("PASS: Money unit is 'w' (Wan).")
        else:
            print("FAIL: Money unit incorrect.")

        stress_text = page.inner_text("#val-stress")
        print(f"Stress: {stress_text}")

        # 4. Interact with Event
        # Wait for Typewriter
        time.sleep(2)

        buttons = page.locator(".choice-btn").all_inner_texts()
        print(f"Choices: {buttons}")

        if len(buttons) > 0:
            page.locator(".choice-btn").first.click()
            print("Clicked first choice.")

            # Wait for log update
            time.sleep(1)
            log_entries = page.locator(".log-content").all_inner_texts()
            print(f"Latest Log: {log_entries[0] if log_entries else 'None'}")

            if log_entries:
                print("PASS: Log updated.")
            else:
                print("FAIL: Log empty.")

        else:
            print("FAIL: No choices rendered.")

        # Screenshot
        page.screenshot(path="verification/modern_ui.png")
        print("Screenshot taken.")

        browser.close()

if __name__ == "__main__":
    run()
