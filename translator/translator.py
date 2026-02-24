

# Uses Google Translate API via deep_translator to translate text to English.
from deep_translator import GoogleTranslator 


def translate_text(text, source_lang='es', target_lang='en'):
	try:
		translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
		return translated
	except Exception as e:
		return f"Translation error: {e}"

def translate_titles(articles, source_lang='es', target_lang='en'):
	#For each article:Take title, Translate it , Add to list(List comprehension)
	return [translate_text(article['title'], source_lang, target_lang) for article in articles] 
