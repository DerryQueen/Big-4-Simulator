import os
import json
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        cwd = os.getcwd()
        filepath = os.path.join(cwd, 'index.html')
        page.goto(f'file://{filepath}')

        # Verify gameEvents array length
        length = page.evaluate("gameEvents.length")
        print(f"Total events found: {length}")

        # Check an old event
        event1 = page.evaluate("gameEvents.find(e => e.id === 1)")
        if event1:
            print("PASS: Old event (ID 1) exists.")
        else:
            print("FAIL: Old event (ID 1) missing.")

        # Check a new event
        event101 = page.evaluate("gameEvents.find(e => e.id === 101)")
        if event101 and "贴发票" in event101['text']:
            print("PASS: New event (ID 101) exists and content matches.")
        else:
            print("FAIL: New event (ID 101) missing or incorrect.")

        # Trigger event filtering check for a new event (ID 101 is level 0-2)
        # Set level to 1 (A2), Quarter 1. ID 101 should be available.
        # But random selection makes it hard to guarantee.
        # Let's just verify the array integrity.

        browser.close()

if __name__ == "__main__":
    run()
