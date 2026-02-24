
from collections import Counter


def analyze_repeated_words(headers):
	
	words = " ".join(headers).lower().split()
	counter = Counter(words) # Count occurrences of each word
	found = False
	print("Repeated Words in Titles (>2 times):")
	for word, count in counter.items(): # Loop through word counts
		if count > 2:
			print(f"{word}: {count}")
			found = True
	if not found:
		print("(None found)")
		
