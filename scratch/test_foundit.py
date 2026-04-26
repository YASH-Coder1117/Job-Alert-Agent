from playwright.sync_api import sync_playwright
import time

def test_foundit():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.foundit.in/srp?query=AI+Engineer")
        time.sleep(5) # wait for load
        
        html = page.content()
        with open("scratch/foundit.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("HTML saved to scratch/foundit.html")
        browser.close()

if __name__ == "__main__":
    test_foundit()
