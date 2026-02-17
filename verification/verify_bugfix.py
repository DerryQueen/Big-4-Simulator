import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        cwd = os.getcwd()
        filepath = os.path.join(cwd, 'index.html')
        page.goto(f'file://{filepath}')

        print("--- Test 1: Event Filtering by Level ---")
        # Set level to 7 (Senior Manager)
        # Event 7 is the only one for level 7 (min 5, max 8)
        # Event 1 is min 0, max 1. Should NOT trigger.
        page.evaluate("""() => {
            gameState.levelIndex = 7;
            gameState.quarter = 1;
            triggerEvent();
        }""")

        content = page.content()
        if "合伙人让你去 BD" in content:
            print("PASS: Correct event triggered for Senior Manager (Level 7).")
        else:
            print("FAIL: Expected Senior Manager event not found.")

        if "入职第一周" in content:
             print("FAIL: Low level event triggered for Senior Manager.")
        else:
             print("PASS: Low level event correctly filtered out.")

        print("\n--- Test 2: Quarter Loop Enforce ---")
        # Set to Q4, trigger event choice handling
        # We simulate clicking a button which calls handleChoice
        # We need to spy on renderButtons or check what buttons are rendered

        # Reset to clean slate
        page.reload()
        page.evaluate("""() => {
            gameState.quarter = 4;
            handleChoice({effect:{}, log:"Test Choice"});
        }""")

        buttons_text = page.locator("#controls button").all_inner_texts()
        print(f"Buttons at end of Q4: {buttons_text}")

        if "年终总结与评估" in buttons_text and "进入下一季度" not in buttons_text:
            print("PASS: Q4 correctly offers ONLY 'Year End Assessment'.")
        else:
            print("FAIL: Q4 logic incorrect.")

        # Click it
        page.get_by_text("年终总结与评估").click()

        # Check reset
        year = page.evaluate("gameState.year")
        quarter = page.evaluate("gameState.quarter")
        print(f"After Year End: Year {year}, Quarter {quarter}")

        if year == 2 and quarter == 1:
            print("PASS: Year/Quarter reset correctly.")
        else:
             print("FAIL: Year/Quarter reset incorrect.")

        browser.close()

if __name__ == "__main__":
    run()
