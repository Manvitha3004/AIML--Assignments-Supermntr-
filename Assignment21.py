"""
 (26/03/2026)
Assignment 21: Movie Review Analyzer

This program uses a simple rule-based sentiment analyzer to classify
movie reviews as Positive or Negative.
"""

import string


# Step 1: Create exactly 5 sample movie reviews (mixed positive and negative).
reviews = [
	"I loved this movie! The acting was brilliant and the story was amazing.",
	"This film was boring, slow, and a complete waste of time.",
	"Great visuals and excellent music made this movie enjoyable.",
	"The plot was terrible and the characters were dull and annoying.",
	"An awesome and heartwarming film with fantastic performances.",
]


# Step 2: Define simple positive and negative word lists.
# These words are used to score each review.
positive_words = {
	"love",
	"loved",
	"brilliant",
	"amazing",
	"great",
	"excellent",
	"enjoyable",
	"awesome",
	"heartwarming",
	"fantastic",
	"good",
	"best",
}

negative_words = {
	"boring",
	"slow",
	"waste",
	"terrible",
	"dull",
	"annoying",
	"bad",
	"worst",
	"poor",
	"awful",
	"hate",
	"hated",
}


# Step 3: Preprocess each review.
# - Convert text to lowercase
# - Remove punctuation
def preprocess_text(text):
	"""Return a cleaned version of the text for sentiment checking."""
	text = text.lower()
	text = text.translate(str.maketrans("", "", string.punctuation))
	return text


# Step 4: Predict sentiment using a basic rule-based approach.
# Count positive and negative words after preprocessing.
def predict_sentiment(review):
	"""Classify a review as Positive or Negative based on word counts."""
	cleaned_review = preprocess_text(review)
	words = cleaned_review.split()

	positive_score = sum(1 for word in words if word in positive_words)
	negative_score = sum(1 for word in words if word in negative_words)

	if positive_score > negative_score:
		sentiment = "Positive"
	else:
		# If negative score is higher OR both are equal, mark as Negative.
		sentiment = "Negative"

	return sentiment, cleaned_review, positive_score, negative_score


# Step 5: Display the result neatly for each review.
print("=" * 70)
print("MOVIE REVIEW ANALYZER (Rule-Based Sentiment Analysis)")
print("=" * 70)

for i, review in enumerate(reviews, start=1):
	sentiment, cleaned_review, positive_score, negative_score = predict_sentiment(review)

	print(f"\nReview {i}:")
	print(f"Original   : {review}")
	print(f"Processed  : {cleaned_review}")
	print(f"Prediction : {sentiment}")
	print(f"Scores     : Positive={positive_score}, Negative={negative_score}")
	print("-" * 70)


# ----------------------------------------------------------------------
# Explanation
# ----------------------------------------------------------------------
# 1. How the sentiment analyzer works:
#    - The review text is converted to lowercase and punctuation is removed.
#    - The cleaned text is split into words.
#    - The program counts how many words appear in a positive word list
#      and how many appear in a negative word list.
#    - If positive count is greater than negative count, the review is
#      classified as Positive; otherwise it is classified as Negative.
#
# 2. Why each review is classified as positive or negative:
#    - Reviews with words like "loved", "amazing", "great", "excellent",
#      "awesome", and "fantastic" get higher positive scores.
#    - Reviews with words like "boring", "waste", "terrible", "dull",
#      and "annoying" get higher negative scores.
#    - The final label depends on which score is larger.
#
# 3. Limitations of this approach:
#    - It depends only on a small fixed word list.
#    - It cannot understand context, sarcasm, or complex sentences.
#    - It may misclassify reviews if important sentiment words are missing
#      from the word lists.
#    - It does not consider grammar or intensity (for example, "very good"
#      vs "good").
