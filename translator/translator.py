

# Uses Google Translate API via deep_translator to translate text to English.
from deep_translator import GoogleTranslator


def translate_text(text, source_lang='es', target_lang='en'):
	"""
	Translate a single string from source_lang to target_lang using Google Translate API (via deep_translator).
	Prints the original and translated text for debugging.
	"""
	try:
		translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
		return translated
	except Exception as e:
		return f"Translation error: {e}"

def translate_titles(articles, source_lang='es', target_lang='en'):
	"""
	Translate the title of each article in a list of article dicts to English.
	Returns a list of translated titles.
	"""
	return [translate_text(article['title'], source_lang, target_lang) for article in articles]
