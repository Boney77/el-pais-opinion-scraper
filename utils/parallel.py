from threading import Thread
from utils.helpers import get_driver_options, create_driver
from utils.browser_driver import run_test
from config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY

caps = [ #Which browsers/devices to test.
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
    resp = requests.get( #BrowserStack API Call
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
    for idx, cap in enumerate(caps, 1): #Loop through each environment and give numbering || idx = thread number, cap = browser/device config
        def thread_task(cap=cap, idx=idx): #Defines function that will run inside a thread | | (Default args prevent closure issues)
            try:
                browser_name = cap.get('browser', cap.get('device', 'Unknown'))
                os_info = cap.get('os', cap.get('os_version', ''))
                os_ver = cap.get('os_version', '')
                print(f"\n[Thread {idx}] 🌐 Opening {browser_name} on {os_info} {os_ver}...")
                browser_type = cap.get('browser', 'chrome').lower() if 'browser' in cap else 'chrome' #Decide which options class to use (Chrome/Firefox/etc.)

                options = get_driver_options(browser_type, cap, idx) #Called get_driver_options to generate Selenium options based on browser type and capabilities, including BrowserStack authentication.
                driver = create_driver(options) #Called create_driver to create a remote Selenium driver that runs tests on BrowserStack cloud.

                print(f"[Thread {idx}] ✅ {browser_name} session started successfully")
                print(f"[Thread {idx}] 🔗 Navigating to https://elpais.com/")
                driver.get("https://elpais.com/") #Opens target website in cloud browser.
                print(f"[Thread {idx}] 📄 Page loaded on {browser_name}")

                run_test(driver, idx, browser_name) #Called run_test to perform the scraping and analysis tasks on the opened browser session.
            except Exception as e:
                print(f"[Thread {idx}] ❌ Error on {cap.get('browser', cap.get('device', 'Unknown'))}: {str(e)[:150]}")
                
        t = Thread(target=thread_task) #Creates a new thread for each browser/device configuration, running the defined task.
        t.start()
        threads.append(t)
    for t in threads:
        t.join() #Wait until ALL threads finish || Without this: Program might exit early ❌
    print("\nAll tests completed!")
