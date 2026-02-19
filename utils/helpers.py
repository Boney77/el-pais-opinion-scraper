
import os
from config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_driver_options(browser_type, cap, thread_id):
	from selenium import webdriver
	if browser_type == 'firefox':
		options = webdriver.FirefoxOptions()
	elif browser_type == 'edge':
		options = webdriver.EdgeOptions()
	else:
		options = webdriver.ChromeOptions()
	options.set_capability('bstack:options', {
		'userName': BROWSERSTACK_USERNAME,
		'accessKey': BROWSERSTACK_ACCESS_KEY,
		'sessionName': f'Thread {thread_id} - {cap.get('browser', cap.get('device', 'Unknown'))}',
	})
	for key, value in cap.items():
		if key not in ['browser', 'browser_version']:
			options.set_capability(key, value)
		elif key == 'browser_version':
			options.set_capability('browserVersion', value)
	return options

def create_driver(options):
	from selenium import webdriver
	from selenium.webdriver.remote.client_config import ClientConfig
	client_config = ClientConfig(
		remote_server_addr="https://hub-cloud.browserstack.com/wd/hub",
		username=BROWSERSTACK_USERNAME,
		password=BROWSERSTACK_ACCESS_KEY,
	)
	return webdriver.Remote(
		command_executor="https://hub-cloud.browserstack.com/wd/hub",
		options=options,
		client_config=client_config
	)
