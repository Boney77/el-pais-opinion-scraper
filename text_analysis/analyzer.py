
from collections import Counter


def analyze_repeated_words(headers):
	"""
	From the translated headers, identify any words that are repeated more than twice across all headers combined.
	Print each repeated word along with the count of its occurrences.
	"""
	words = " ".join(headers).lower().split()
	counter = Counter(words)
	found = False
	print("Repeated Words in Titles (>2 times):")
	for word, count in counter.items():
		if count > 2:
			print(f"{word}: {count}")
			found = True
	if not found:
		print("(None found)")
