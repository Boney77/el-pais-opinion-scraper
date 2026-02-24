
from config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#setup
def get_driver_options(browser_type, cap, thread_id):#Generates Selenium options based on browser type and capabilities, including BrowserStack authentication.
	from selenium import webdriver #Lazy import - Faster startup, Avoid import issues
	if browser_type == 'firefox': #Chooses correct browser settings based on input.
		options = webdriver.FirefoxOptions()
	elif browser_type == 'edge':
		options = webdriver.EdgeOptions()
	else:
		options = webdriver.ChromeOptions()

	options.set_capability('bstack:options', { #Logs into BrowserStack and starts a named cloud test session
		'userName': BROWSERSTACK_USERNAME,
		'accessKey': BROWSERSTACK_ACCESS_KEY,
		'sessionName': f'Thread {thread_id} - {cap.get('browser', cap.get('device', 'Unknown'))}',
	})
	for key, value in cap.items():#Adds all browser settings dynamically and fixes BrowserStack naming differences
		if key not in ['browser', 'browser_version']:
			options.set_capability(key, value)
		elif key == 'browser_version':
			options.set_capability('browserVersion', value)
	return options

def create_driver(options): #Creates a remote Selenium driver that runs tests on BrowserStack cloud.
	from selenium import webdriver
	from selenium.webdriver.remote.client_config import ClientConfig #Remote connection settings
	client_config = ClientConfig( #Created ClientConfig Object for for remote connection.
		remote_server_addr="https://hub-cloud.browserstack.com/wd/hub",
		username=BROWSERSTACK_USERNAME, 
		password=BROWSERSTACK_ACCESS_KEY,
	)
	return webdriver.Remote( #Run browser on cloud
		command_executor="https://hub-cloud.browserstack.com/wd/hub", #Tell Selenium where to send commands (BrowserStack server).
		options=options, #Passes browser settings.
		client_config=client_config #Passes authentication config.
	)

 