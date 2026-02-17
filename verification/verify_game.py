import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the file
        cwd = os.getcwd()
        filepath = os.path.join(cwd, 'index.html')
        page.goto(f'file://{filepath}')

        # Check title
        print("Page title:", page.title())

        # Take initial screenshot
        page.screenshot(path='verification/initial_state.png')

        # Interact: Click "开始工作"
        # The button text is "开始工作 (消耗体力)"
        page.get_by_text("开始工作").click()

        # Wait a bit for animation/update
        page.wait_for_timeout(1000)

        # Take updated screenshot
        page.screenshot(path='verification/after_action.png')

        browser.close()

if __name__ == "__main__":
    run()
