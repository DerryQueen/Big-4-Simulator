import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        cwd = os.getcwd()
        filepath = os.path.join(cwd, 'index.html')
        page.goto(f'file://{filepath}')

        print("--- Test 1: Promotion ---")
        # Setup: Q4, High Performance
        page.evaluate("""() => {
            gameState.quarter = 4;
            gameState.stats.performance = 90;
            gameState.stats.health = 50;
            gameState.stats.sanity = 50;
            updateUI();
            // Manually trigger the button rendering for end of year choice
            // We need to simulate being at the end of a Q4 choice.
            // The handleChoice function renders the button.
            // Let's just call endYearAssessment directly for testing?
            // Or better, set up a dummy event and click through it.
            // Let's just call endYearAssessment() directly.
            endYearAssessment();
        }""")

        # Verify Promotion Text
        content = page.content()
        if "恭喜！你的绩效评分高达 90" in content and "晋升为：Audit Associate 2 (A2)" in content:
            print("PASS: Promotion logic verified.")
        else:
            print("FAIL: Promotion logic not found.")

        # Verify Reset
        # We need to click "Start Year 2" to see the UI update fully or check gameState
        # But endYearAssessment updates gameState immediately.
        year = page.evaluate("gameState.year")
        kpi = page.evaluate("gameState.stats.performance")
        level = page.evaluate("gameState.levelIndex")

        if year == 2 and kpi == 50 and level == 1:
             print(f"PASS: State reset verified (Year {year}, KPI {kpi}, LevelIndex {level}).")
        else:
             print(f"FAIL: State reset failed (Year {year}, KPI {kpi}, LevelIndex {level}).")


        print("\n--- Test 2: Termination ---")
        page.reload()
        page.evaluate("""() => {
            gameState.quarter = 4;
            gameState.stats.performance = 30;
            endYearAssessment();
        }""")
        content = page.content()
        if "被列入 PIP" in content and "游戏结束" in content:
            print("PASS: Termination logic verified.")
        else:
            print("FAIL: Termination logic not found.")

        print("\n--- Test 3: Victory ---")
        page.reload()
        page.evaluate("""() => {
            gameState.quarter = 4;
            gameState.levelIndex = 7; // Senior Manager
            gameState.stats.performance = 100;
            endYearAssessment();
        }""")
        content = page.content()
        if "晋升为：Partner (Par)" in content and "VICTORY - 游戏通关" in content:
             print("PASS: Victory logic verified.")
        else:
             print("FAIL: Victory logic not found.")

        browser.close()

if __name__ == "__main__":
    run()
