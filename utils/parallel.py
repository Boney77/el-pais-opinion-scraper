from threading import Thread
from utils.helpers import get_driver_options, create_driver
from utils.browser_driver import run_test
from config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY

caps = [
    {"browser": "Chrome", "browser_version": "latest", "os": "Windows", "os_version": "11"},
    {"browser": "Firefox", "browser_version": "latest", "os": "Windows", "os_version": "10"},
    {"browser": "Edge", "browser_version": "latest", "os": "Windows", "os_version": "11"},
    {"device": "iPhone 14", "real_mobile": "true", "os_version": "16"},
    {"device": "Samsung Galaxy S23", "real_mobile": "true", "os_version": "13"},
]

def run_parallel():
    print("Starting BrowserStack tests...")
    print(f"Using credentials: Username={BROWSERSTACK_USERNAME}")
    
    # Quick credential check
    import requests
    resp = requests.get(
        "https://api.browserstack.com/automate/plan.json",
        auth=(BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY)
    )
    if resp.status_code == 401:
        print("\n❌ ERROR: BrowserStack credentials are INVALID or EXPIRED.")
        print("Please update BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY in config.py")
        print(f"Current username: {BROWSERSTACK_USERNAME}")
        return
    elif resp.status_code == 200:
        print(f"✅ BrowserStack credentials valid. Plan: {resp.json()}")
    
    threads = []
    for idx, cap in enumerate(caps, 1):
        def thread_task(cap=cap, idx=idx):
            try:
                browser_name = cap.get('browser', cap.get('device', 'Unknown'))
                os_info = cap.get('os', cap.get('os_version', ''))
                os_ver = cap.get('os_version', '')
                print(f"\n[Thread {idx}] 🌐 Opening {browser_name} on {os_info} {os_ver}...")
                browser_type = cap.get('browser', 'chrome').lower() if 'browser' in cap else 'chrome'
                options = get_driver_options(browser_type, cap, idx)
                driver = create_driver(options)
                print(f"[Thread {idx}] ✅ {browser_name} session started successfully")
                print(f"[Thread {idx}] 🔗 Navigating to https://elpais.com/")
                driver.get("https://elpais.com/")
                print(f"[Thread {idx}] 📄 Page loaded on {browser_name}")
                run_test(driver, idx, browser_name)
            except Exception as e:
                print(f"[Thread {idx}] ❌ Error on {cap.get('browser', cap.get('device', 'Unknown'))}: {str(e)[:150]}")
        t = Thread(target=thread_task)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("\nAll tests completed!")
