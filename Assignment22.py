"""
(27/03/2026)
Assignment 22: Semantic Meaning

This beginner-friendly program computes semantic similarity between word pairs
using WordNet from NLTK. It prints similarity scores, classifies each score
as High/Medium/Low, and explains the results.
"""

import nltk
from nltk.corpus import wordnet as wn


def ensure_wordnet_data():
	"""Make sure required WordNet resources are available before use."""
	try:
		wn.synsets("test")
	except LookupError:
		print("Downloading WordNet data (first run only)...")
		nltk.download("wordnet", quiet=True)
		nltk.download("omw-1.4", quiet=True)


def semantic_similarity(word1, word2):
	"""Return the best Wu-Palmer similarity score between two words."""
	synsets1 = wn.synsets(word1)
	synsets2 = wn.synsets(word2)

	# If no meaning entries are found for either word, return 0.0.
	if not synsets1 or not synsets2:
		return 0.0

	max_score = 0.0

	# Compare every sense of word1 with every sense of word2
	# and keep the highest similarity score.
	for s1 in synsets1:
		for s2 in synsets2:
			score = s1.wup_similarity(s2)
			if score is not None and score > max_score:
				max_score = score

	return max_score


def classify_similarity(score):
	"""Classify score into High, Medium, or Low similarity."""
	if score >= 0.75:
		return "High"
	if score >= 0.40:
		return "Medium"
	return "Low"


def print_results_table(results):
	"""Print all pair results in a clean table format."""
	print("\n" + "=" * 72)
	print("SEMANTIC SIMILARITY RESULTS")
	print("=" * 72)
	print(f"{'Word Pair':<28}{'Score':<12}{'Level':<10}")
	print("-" * 72)

	for row in results:
		pair_label = f"{row['word1']} - {row['word2']}"
		print(f"{pair_label:<28}{row['score']:<12.4f}{row['level']:<10}")

	print("=" * 72)


def print_explanations(results):
	"""Print explanation sections requested in the assignment."""
	print("\nEXPLANATION: WHAT IS SEMANTIC SIMILARITY?")
	print("- Semantic similarity measures how close two words are in meaning.")
	print("- For example, synonyms like 'happy' and 'joyful' usually score high.")
	print("- Unrelated words like 'car' and 'banana' usually score low.")

	print("\nCOMPARISON OF ALL WORD PAIRS (Highest to Lowest Score):")
	sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
	for i, row in enumerate(sorted_results, start=1):
		pair_label = f"{row['word1']} - {row['word2']}"
		print(f"{i}. {pair_label:<24} Score: {row['score']:.4f} ({row['level']})")

	print("\nREAL-WORLD APPLICATIONS:")
	print("1. Search Engines: Understand similar terms and improve search quality.")
	print("2. Chatbots: Match user words to related intents and responses.")
	print("3. Recommendations: Suggest related products, movies, or content.")

	print("\nLIMITATIONS OF THIS APPROACH:")
	print("1. Word sense ambiguity: A word can have multiple meanings.")
	print("2. Context is limited: Single words are compared without full sentences.")
	print("3. Knowledge base limits: Results depend on WordNet coverage.")
	print("4. Domain-specific terms may not be handled well.")


def main():
	"""Main driver function for the assignment."""
	ensure_wordnet_data()

	# Exactly 5 word pairs:
	# - Synonyms
	# - Related words
	# - Unrelated words
	word_pairs = [
		("happy", "joyful"),      # Synonyms
		("big", "large"),         # Synonyms
		("doctor", "hospital"),  # Related words
		("teacher", "student"),  # Related words
		("car", "banana"),       # Unrelated words
	]

	results = []

	# Compute score and level for each pair.
	for word1, word2 in word_pairs:
		score = semantic_similarity(word1, word2)
		level = classify_similarity(score)

		results.append(
			{
				"word1": word1,
				"word2": word2,
				"score": score,
				"level": level,
			}
		)

	print_results_table(results)
	print_explanations(results)


if __name__ == "__main__":
	main()
