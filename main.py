
from scraper.scraper import scrape_opinion_articles
from translator.translator import translate_titles
from text_analysis.analyzer import analyze_repeated_words

def get_driver():
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def run_scraper():
    print("\n==============================")
    print("🚀 SCRAPING STARTED")
    print("==============================\n")

    driver = get_driver()
    driver.get("https://elpais.com/")

    # STEP 1 — Scrape (article info prints to console as each article is opened)
    articles = scrape_opinion_articles(driver, wait=None, num_articles=5)

    print("\n==============================")
    print("🧾 SCRAPING COMPLETE")
    print("==============================\n")

    # STEP 2 — Translate
    print("\n==============================")
    print("🌍 TRANSLATION STARTED")
    print("==============================\n")
    translated_titles = translate_titles(articles)
    for idx, (article, translated) in enumerate(zip(articles, translated_titles), 1):
        print(f"\nArticle {idx}")
        print(f"Spanish Title: {article['title']}")
        print(f"English Title: {translated}")
    print("\n==============================")
    print("🌍 TRANSLATION COMPLETE")
    print("==============================\n")

    # STEP 3 — Analyze
    print("\n==============================")
    print("🔎 ANALYZER STARTED")
    print("==============================\n")
    analyze_repeated_words(translated_titles)
    print("\n==============================")
    print("🔎 ANALYZER COMPLETE")
    print("==============================\n")

    driver.quit()

if __name__ == "__main__":
    run_scraper()