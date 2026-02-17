import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        cwd = os.getcwd()
        filepath = os.path.join(cwd, 'index.html')
        page.goto(f'file://{filepath}')

        # Trigger Year End Screen manually
        page.evaluate("""() => {
            gameState.quarter = 4;
            gameState.stats.performance = 85;
            endYearAssessment();
        }""")

        # Wait for animation
        page.wait_for_timeout(1000)

        # Take screenshot of the End Year Summary
        page.screenshot(path='verification/end_year_summary_fixed.png')

        browser.close()

if __name__ == "__main__":
    run()
