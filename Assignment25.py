"""
(03/04/2026)
Assignment 25: NLP Mini App - Keyword Extractor using TF-IDF

Features implemented:
1. Accepts user input text (supports multiple inputs).
2. Preprocesses text (lowercase + stopword removal).
3. Extracts top 5 keywords using TF-IDF.
4. Displays keywords with scores in a clean format.
5. Prints explanation, applications, and limitations at the end.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS


def preprocess_text(text):
	"""Convert text to lowercase and remove English stopwords."""
	# Convert to lowercase
	text = text.lower()

	# Extract words (keeps only alphabetic tokens)
	tokens = re.findall(r"[a-zA-Z]+", text)

	# Remove stopwords such as 'the', 'is', 'and', etc.
	filtered_tokens = [word for word in tokens if word not in ENGLISH_STOP_WORDS]

	# Return the cleaned text
	return " ".join(filtered_tokens)


def get_user_inputs():
	"""Collect one or more text inputs from the user."""
	texts = []

	print("=" * 78)
	print("NLP MINI APP: KEYWORD EXTRACTOR (TF-IDF)")
	print("=" * 78)
	print("Enter your text inputs one by one.")
	print("Type 'done' when you finish entering inputs.\n")

	while True:
		user_text = input(f"Input {len(texts) + 1}: ").strip()

		if user_text.lower() == "done":
			break

		if user_text:
			texts.append(user_text)
		else:
			print("Please enter non-empty text.")

	return texts


def extract_top_keywords(original_texts, top_n=5):
	"""
	Extract top keywords and their TF-IDF scores for each input text.
	Returns a list of results for each text.
	"""
	# Preprocess all texts first
	cleaned_texts = [preprocess_text(text) for text in original_texts]

	# Create TF-IDF vectorizer
	# We keep lowercase=False because preprocessing already lowercases text.
	vectorizer = TfidfVectorizer(lowercase=False)

	# Fit and transform all texts into a TF-IDF matrix
	tfidf_matrix = vectorizer.fit_transform(cleaned_texts)
	feature_names = vectorizer.get_feature_names_out()

	all_results = []

	# Process each text row in the TF-IDF matrix
	for index, original_text in enumerate(original_texts):
		row_scores = tfidf_matrix[index].toarray().flatten()

		# Get top non-zero score indices in descending order
		sorted_indices = row_scores.argsort()[::-1]

		keywords_with_scores = []
		for idx in sorted_indices:
			score = row_scores[idx]
			if score <= 0:
				continue

			keyword = feature_names[idx]
			keywords_with_scores.append((keyword, score))

			if len(keywords_with_scores) == top_n:
				break

		all_results.append(
			{
				"original_text": original_text,
				"cleaned_text": cleaned_texts[index],
				"keywords": keywords_with_scores,
			}
		)

	return all_results


def display_results(results):
	"""Display extracted keywords and scores clearly for each input text."""
	print("\n" + "=" * 78)
	print("EXTRACTED KEYWORDS")
	print("=" * 78)

	for i, result in enumerate(results, start=1):
		print(f"\nText {i}:")
		print(f"Original Text : {result['original_text']}")
		print(f"Processed Text: {result['cleaned_text']}")
		print("Top Keywords (with TF-IDF scores):")

		if not result["keywords"]:
			print("  No keywords found after preprocessing.")
			continue

		for rank, (keyword, score) in enumerate(result["keywords"], start=1):
			print(f"  {rank}. {keyword:<20} Score: {score:.4f}")


def print_explanation():
	"""Print assignment explanation after code output."""
	print("\n" + "=" * 78)
	print("EXPLANATION")
	print("=" * 78)

	print("\n1. What is TF-IDF?")
	print("- TF (Term Frequency): Measures how often a word appears in a text.")
	print("- IDF (Inverse Document Frequency): Reduces weight of very common words")
	print("  across many texts and increases weight of more unique words.")
	print("- TF-IDF score helps identify words that are important in a specific text.")

	print("\n2. How this app works")
	print("- Takes one or more user text inputs.")
	print("- Converts text to lowercase and removes stopwords.")
	print("- Uses TfidfVectorizer from sklearn to compute scores.")
	print("- Shows top 5 keywords with the highest TF-IDF scores.")

	print("\n3. Applications")
	print("- Search engines: finding important terms in documents.")
	print("- Text summarization: selecting key words/topics from large text.")
	print("- Information retrieval: improving ranking of relevant content.")

	print("\n4. Limitations")
	print("- TF-IDF does not understand full context or meaning of words.")
	print("- Different forms of a word (run/running) are treated separately.")
	print("- It may miss semantic relationships (similar meaning, synonyms).")


def main():
	"""Main function to run the NLP Mini App."""
	user_texts = get_user_inputs()

	if not user_texts:
		print("\nNo input received. Exiting program.")
		return

	results = extract_top_keywords(user_texts, top_n=5)
	display_results(results)
	print_explanation()


if __name__ == "__main__":
	main()
