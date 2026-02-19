
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from deep_translator import GoogleTranslator
from collections import Counter
import time
import os
from utils.helpers import get_driver_options, create_driver

def download_image(url, filename):
	try:
		import requests
		if not os.path.exists("data/images"):
			os.makedirs("data/images")
		response = requests.get(url)
		with open(f"data/images/{filename}.jpg", "wb") as f:
			f.write(response.content)
	except Exception as e:
		print(f"Image error: {e}")

def run_test(driver, thread_id, browser_name='Unknown'):
	wait = WebDriverWait(driver, 15)
	try:
		# Accept cookies first — mandatory on all browsers
		print(f"[Thread {thread_id}] 🍪 [{browser_name}] Checking for cookie popup...")
		try:
			accept_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Accept' or normalize-space()='Aceptar' or contains(text(),'Accept') or contains(text(),'Aceptar')]")))
			accept_btn.click()
			print(f"[Thread {thread_id}] ✅ [{browser_name}] Cookies accepted")
			time.sleep(2)
		except:
			print(f"[Thread {thread_id}] ⚠ [{browser_name}] No cookie popup found, continuing...")

		print(f"[Thread {thread_id}] 🔍 [{browser_name}] Navigating to Opinion section...")
		try:
			opinion_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Opinión")))
			opinion_link.click()
		except:
			try:
				opinion_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Opini")
				opinion_link.click()
			except:
				print(f"[Thread {thread_id}] ⚠ [{browser_name}] Direct navigation to opinion section")
				driver.get("https://elpais.com/opinion/")
		time.sleep(4)
		driver.execute_script("window.scrollTo(0, 200);")
		time.sleep(1)

		print(f"[Thread {thread_id}] ✅ [{browser_name}] Opinion section loaded")
		articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))
		print(f"[Thread {thread_id}] 📰 [{browser_name}] Found {len(articles)} articles, using first 5")
		
		translated_titles = []
		num_articles = min(5, len(articles))
		
		for i in range(num_articles):
			try:
				time.sleep(1)
				articles = driver.find_elements(By.CSS_SELECTOR, "article")
				if i >= len(articles):
					print(f"[Thread {thread_id}] ⚠ [{browser_name}] Article {i+1} not found, skipping")
					continue

				# Try multiple selectors for title
				title = ""
				try:
					title = articles[i].find_element(By.TAG_NAME, "h2").text
				except:
					try:
						title = articles[i].find_element(By.CSS_SELECTOR, "h2 a").text
					except:
						try:
							title = articles[i].find_element(By.CSS_SELECTOR, ".c_t").text
						except:
							try:
								title = articles[i].text.split('\n')[0]
							except:
								pass

				if not title or title.strip() == "":
					print(f"[Thread {thread_id}] ⚠ [{browser_name}] Article {i+1}: No title found, skipping")
					continue

				print(f"\n[Thread {thread_id}] 📰 [{browser_name}] Article {i+1}:")
				print(f"[Thread {thread_id}]   📌 Spanish Title: {title}")
				print(f"[Thread {thread_id}]   🖱 Clicking article {i+1}...")
				
				try:
					driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", articles[i])
					time.sleep(1)
					articles[i].click()
				except:
					try:
						driver.execute_script("arguments[0].click();", articles[i])
					except:
						print(f"[Thread {thread_id}] ⚠ [{browser_name}] Could not click article {i+1}, skipping")
						continue

				time.sleep(3)
				driver.execute_script("window.scrollTo(0, 200);")
				time.sleep(1)

				print(f"[Thread {thread_id}]   📄 [{browser_name}] Reading article content...")
				paragraphs = driver.find_elements(By.TAG_NAME, "p")
				content = " ".join([p.text for p in paragraphs[:5]])
				if content.strip():
					print(f"[Thread {thread_id}]   📄 Content: {content[:200]}...")
				else:
					print(f"[Thread {thread_id}]   📄 Content: (no content found)")

				try:
					image = driver.find_element(By.CSS_SELECTOR, "article img, figure img, .a_m img")
					img_url = image.get_attribute("src")
					if img_url:
						print(f"[Thread {thread_id}]   🖼 Image: {img_url[:80]}...")
						download_image(img_url, f"thread{thread_id}_article_{i+1}_photo")
					else:
						print(f"[Thread {thread_id}]   🖼 No image URL found")
				except:
					print(f"[Thread {thread_id}]   🖼 No image found")

				print(f"[Thread {thread_id}]   🌍 [{browser_name}] Translating title...")
				try:
					translated = GoogleTranslator(source='es', target='en').translate(title)
					translated_titles.append(translated)
					print(f"[Thread {thread_id}]   🌍 English Title: {translated}")
				except Exception as te:
					print(f"[Thread {thread_id}]   ⚠ Translation failed: {str(te)[:50]}")

				print(f"[Thread {thread_id}]   ⬅ Going back to Opinion section...")
				driver.back()
				time.sleep(3)
				driver.execute_script("window.scrollTo(0, 200);")
				time.sleep(1)

			except Exception as e:
				print(f"[Thread {thread_id}] ❌ [{browser_name}] Article {i+1} error: {str(e)[:80]}")
				try:
					driver.back()
					time.sleep(2)
				except:
					pass

		print(f"\n[Thread {thread_id}] 🔎 [{browser_name}] Analyzing repeated words...")
		if translated_titles:
			words = " ".join(translated_titles).lower().split()
			counter = Counter(words)
			found = False
			for word, count in counter.items():
				if count > 2:
					print(f"[Thread {thread_id}]   {word}: {count}")
					found = True
			if not found:
				print(f"[Thread {thread_id}]   (No words repeated more than 2 times)")
		else:
			print(f"[Thread {thread_id}]   (No titles were translated)")

		print(f"[Thread {thread_id}] ✅ [{browser_name}] Test completed successfully!")
		driver.quit()
	except Exception as e:
		print(f"[Thread {thread_id}] ❌ [{browser_name}] Error: {str(e)[:150]}")
		try:
			driver.quit()
		except:
			pass
