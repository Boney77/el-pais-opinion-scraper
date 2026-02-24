"""
Simple BrowserStack connection test
This script tests a single browser without threading to diagnose connection issues
"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities # Used to specify browser capabilities for Selenium WebDriver (older way)
from selenium.webdriver.remote.client_config import ClientConfig
from config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY
import urllib3
import ssl

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("Testing BrowserStack connection...")
print(f"Username: {BROWSERSTACK_USERNAME}")
print(f"Access Key: {'(not set)' if not BROWSERSTACK_ACCESS_KEY else BROWSERSTACK_ACCESS_KEY[:4] + '...' }") #Show only first 4 characters of access key for security

try:
    # Simple Chrome test with basic capabilities
    capabilities = {
        'browserName': 'Chrome',
        'browserVersion': 'latest',
        'os': 'Windows',
        'osVersion': '11',
        'sessionName': 'El Pais Test',
        'buildName': 'Selenium Test Build'
    }
    
    # Create Chrome options
    options = webdriver.ChromeOptions()
    
    # Set BrowserStack credentials
    options.set_capability('bstack:options', { 
        'userName': BROWSERSTACK_USERNAME,
        'accessKey': BROWSERSTACK_ACCESS_KEY,
    })
    
    # Add other capabilities
    for key, value in capabilities.items(): #Add all capabilities dynamically and fix BrowserStack naming differences
        if key not in ['browserName']:
            options.set_capability(key, value)
    
    print("\nConnecting to BrowserStack using ClientConfig (no credentials in URL)...")

    # Build a ClientConfig to provide credentials without embedding them in the URL
    client_config = ClientConfig(
        remote_server_addr="https://hub-cloud.browserstack.com/wd/hub",
        username=BROWSERSTACK_USERNAME or None,
        password=BROWSERSTACK_ACCESS_KEY or None,
    )

    driver = webdriver.Remote(
        command_executor="https://hub-cloud.browserstack.com/wd/hub",
        options=options,
        client_config=client_config,
    )
    
    print("✓ Connected successfully!")
    
    print("Loading elpais.com...")
    driver.get("https://elpais.com/")
    
    print(f"✓ Page Title: {driver.title}")
    print(f"✓ Session ID: {driver.session_id}")
    
    driver.quit()
    print("\n✓ Test completed successfully!")
    print("\nView your test at: https://automate.browserstack.com/dashboard/v2")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nPossible issues:")
    print("1. SSL certificate verification failing (corporate network)")
    print("2. BrowserStack credentials incorrect")
    print("3. Network firewall blocking access")
    print("\nSuggested fix: Run from a personal network or contact IT about SSL interception")
