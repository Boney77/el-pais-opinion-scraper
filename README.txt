# Selenium News Scraper

This project scrapes news articles, images, and content from online sources using Selenium and BeautifulSoup, then performs text analysis and translation.

## Features
- Automated browser scraping with Selenium
- Article and image extraction
- Text analysis (see text_analysis/analyzer.py)
- Translation (see translator/translator.py)
- Parallel scraping support

## Requirements
Install dependencies with:

    pip install -r requirements.txt

## Main Dependencies
- selenium
- beautifulsoup4
- requests
- Google Translation
- python-dotenv

## Usage
Run the main script:

    python main.py

## Project Structure
- main.py: Entry point
- config.py: Configuration
- scraper/: Scraping logic
- text_analysis/: Text analysis
- translator/: Translation logic
- utils/: Utilities (browser, helpers, parallel)
- data/: Output data (articles, images)
- logs/: Log files

## Parallel Execution with BrowserStack

To enable parallel browser execution using BrowserStack, you need to provide your BrowserStack credentials. These are used for authenticating automated browser sessions.

### Setting Credentials

You can set your BrowserStack username and access key in the config.py file:

    BROWSERSTACK_USERNAME = "your_browserstack_username"
    BROWSERSTACK_ACCESS_KEY = "your_browserstack_access_key"

##Note

- Requires Python 3.8+
- Make sure ChromeDriver or the appropriate WebDriver is installed and in your PATH.
- For translation, an internet connection is required.

---

