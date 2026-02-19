
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.remote.client_config import ClientConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
	bs_user = os.environ.get("BROWSERSTACK_USERNAME")
	bs_key = os.environ.get("BROWSERSTACK_ACCESS_KEY")
	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	if bs_user and bs_key:
		options.set_capability('bstack:options', {
			'userName': bs_user,
			'accessKey': bs_key,
			'sessionName': 'El Pais Test',
		})
		client_config = ClientConfig(
			remote_server_addr="https://hub-cloud.browserstack.com/wd/hub",
			username=bs_user,
			password=bs_key,
		)
		return webdriver.Remote(command_executor="https://hub-cloud.browserstack.com/wd/hub", options=options, client_config=client_config)
	return webdriver.Chrome(options=options)

def scrape_opinion_articles(driver, wait, num_articles=5):
	# Ensure wait is set
	if wait is None:
		from selenium.webdriver.support.ui import WebDriverWait
		wait = WebDriverWait(driver, 10)
	# Accept cookies - mandatory before proceeding
	try:
		accept_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Accept' or normalize-space()='Aceptar']")))
		accept_btn.click()
		time.sleep(1)
	except Exception:
		raise RuntimeError("Cookie consent popup not found or could not be accepted. Scraper cannot proceed.")
	try:
		try:
			opinion_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Opinión")))
			opinion_link.click()
		except:
			try:
				opinion_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Opini")
				opinion_link.click()
			except:
				driver.get("https://elpais.com/opinion/")
		time.sleep(3)
		driver.execute_script("window.scrollBy(0, 200);")
		time.sleep(1)
		articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))[:num_articles]
		if not articles:
			logging.error("No articles found")
			return []
		results = []
		for i in range(len(articles)):
			try:
				articles = driver.find_elements(By.CSS_SELECTOR, "article")
				article_index = i if i < num_articles-1 else num_articles  # Use next article for the last one
				title = articles[article_index].find_element(By.TAG_NAME, "h2").text
				print(f"\n[Scraper] Opening Article {i+1}...")
				articles[article_index].click()
				time.sleep(1)
				# Scroll down a bit to skip top ad, then hide all ads
				driver.execute_script("window.scrollTo(0, 200);")
				time.sleep(1)
				ad_selectors = [
					'[id*="ad" i]', '[class*="ad" i]', '[id*="banner" i]', '[class*="banner" i]',
					'[id*="cookie" i]', '[class*="cookie" i]', '[id*="promo" i]', '[class*="promo" i]',
					'[id*="sticky" i]', '[class*="sticky" i]', '[id*="popup" i]', '[class*="popup" i]',
					'[id*="overlay" i]', '[class*="overlay" i]', 'iframe'
				]
				for sel in ad_selectors:
					driver.execute_script(f"for(let el of document.querySelectorAll('{sel}')){{el.style.display='none';}}")
				# Stay scrolled down past the top ad
				driver.execute_script("window.scrollTo(0, 200);")
				time.sleep(1)
				paragraphs = driver.find_elements(By.TAG_NAME, "p")
				content = " ".join([p.text for p in paragraphs[:5]])
				# Try to get cover/article image
				try:
					img_el = driver.find_element(By.CSS_SELECTOR, "article img")
					image_url = img_el.get_attribute("src")
				except:
					image_url = "N/A"
				if not os.path.exists("data/images"):
					os.makedirs("data/images")
				screenshot_path = f"data/images/article_{i+1}_cover.png"
				driver.save_screenshot(screenshot_path)
				# Print article info to console immediately
				print(f"\n{'='*60}")
				print(f"📰 ARTICLE {i+1}")
				print(f"{'='*60}")
				print(f"\n📌 TITLE (ES): {title}")
				print(f"📄 CONTENT SNIPPET: {content[:400]}")
				print(f"🖼 COVER IMAGE: {screenshot_path}")
				print(f"{'='*60}\n")
				time.sleep(3)
				results.append({
					'title': title,
					'content': content,
					'image': screenshot_path
				})
				driver.back()
				time.sleep(3)
				driver.execute_script("window.scrollTo(0, 0);")
				time.sleep(1)
			except Exception as e:
				logging.error(e)
				driver.back()
		return results
	except Exception as e:
		logging.error(f"Scraping error: {e}")
		return []
