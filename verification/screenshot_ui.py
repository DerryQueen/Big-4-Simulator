import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        cwd = os.getcwd()
        filepath = os.path.join(cwd, 'index.html')
        page.goto(f'file://{filepath}')

        # Take screenshot of the initial state showing Q1/4
        page.screenshot(path='verification/q1_start.png')

        # Trigger Year End Screen manually to show the UI
        page.evaluate("""() => {
            gameState.quarter = 4;
            gameState.stats.performance = 85; // Good enough for promotion
            endYearAssessment();
        }""")

        # Take screenshot of the End Year Summary
        page.screenshot(path='verification/end_year_summary.png')

        browser.close()

if __name__ == "__main__":
    run()
