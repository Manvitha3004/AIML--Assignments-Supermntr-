# ============================================================================
# (24/03/2026)
# Assignment 20: Word Importance Explorer using TF-IDF
# ============================================================================
# This program demonstrates how to identify the most important words in
# multiple documents using TF-IDF (Term Frequency-Inverse Document Frequency).
# ============================================================================

# Import necessary libraries
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# ===========================================
# Step 1: Define 5 Sample Text Documents
# ===========================================
# These documents represent different topics to showcase how TF-IDF identifies
# words that are important in specific documents while downweighting common words.

documents = [
    # Document 1: About Python Programming
    "Python is a powerful programming language. Python is widely used for web development, "
    "data science, and automation. Python code is clean and easy to read.",
    
    # Document 2: About Machine Learning
    "Machine learning is a subset of artificial intelligence. Machine learning algorithms "
    "help computers learn from data without being explicitly programmed. Deep learning is "
    "a powerful technique in machine learning.",
    
    # Document 3: About Natural Language Processing
    "Natural language processing focuses on understanding and processing human language. "
    "NLP techniques are used in text classification, sentiment analysis, and machine translation. "
    "Language models have revolutionized natural language processing.",
    
    # Document 4: About Data Science
    "Data science combines statistics, mathematics, and programming. Data scientists analyze "
    "large datasets to extract insights. Data visualization helps present findings clearly.",
    
    # Document 5: About Web Development
    "Web development involves creating websites and web applications. Web developers use HTML, "
    "CSS, and JavaScript. Web development frameworks like Django and Flask make development faster."
]

# ===========================================
# Step 2: Create and Configure TfidfVectorizer
# ===========================================
# TfidfVectorizer automatically handles:
# - Converting text to lowercase
# - Removing English stopwords (common words like 'is', 'the', 'and', etc.)
# - Splitting text into tokens
# - Computing TF-IDF scores

vectorizer = TfidfVectorizer(
    lowercase=True,              # Convert all text to lowercase
    stop_words='english',        # Remove English stopwords automatically
    max_features=100,            # Limit to top 100 features (words)
    ngram_range=(1, 1)           # Use single words only (not word combinations)
)

# ===========================================
# Step 3: Compute TF-IDF Scores
# ===========================================
# fit_transform() does two things:
# 1. Learn the vocabulary from all documents
# 2. Transform documents into TF-IDF score vectors

tfidf_matrix = vectorizer.fit_transform(documents)

# Get the vocabulary (mapping of word to column index)
feature_names = vectorizer.get_feature_names_out()

# ===========================================
# Step 4: Extract and Display Top 3 Keywords
# ===========================================
# For each document, find the 3 words with highest TF-IDF scores

print("=" * 80)
print("WORD IMPORTANCE EXPLORER - TF-IDF ANALYSIS RESULTS")
print("=" * 80)
print()

# Iterate through each document
for doc_index in range(len(documents)):
    print(f"{'─' * 80}")
    print(f"DOCUMENT {doc_index + 1}:")
    print(f"{'─' * 80}")
    print(f"Original Text (First 100 characters):")
    print(f"{documents[doc_index][:100]}...")
    print()
    
    # Get the TF-IDF scores for the current document
    # tfidf_matrix[doc_index] is a sparse matrix row, convert to dense array
    tfidf_scores = tfidf_matrix[doc_index].toarray()[0]
    
    # Get indices of the three highest scores
    # argsort() returns indices sorted in ascending order, so we take the last 3
    top_3_indices = tfidf_scores.argsort()[-3:][::-1]  # Reverse to get descending order
    
    # Display top 3 keywords with their TF-IDF scores
    print("Top 3 Keywords by TF-IDF Score:")
    print()
    for rank, idx in enumerate(top_3_indices, 1):
        keyword = feature_names[idx]
        score = tfidf_scores[idx]
        print(f"  {rank}. Keyword: '{keyword:20s}' | TF-IDF Score: {score:.4f}")
    
    print()

print("=" * 80)
print("EXPLANATION OF OUTPUT")
print("=" * 80)
print()

print("WHY CERTAIN WORDS HAVE HIGHER TF-IDF SCORES:")
print("-" * 80)
print("""
1. TERM FREQUENCY (TF): Words that appear frequently in a specific document
   get higher scores. For example, 'Python' appears multiple times in Document 1,
   so it gets a higher TF component.

2. INVERSE DOCUMENT FREQUENCY (IDF): Words that appear in fewer documents get
   higher scores. This means unique or specialized words score higher than common words.
   For example, 'Python' appears mainly in Document 1, so it gets a high IDF score.

3. COMBINED EFFECT: TF-IDF = TF × IDF. This means words that are:
   - Frequent in the document (high TF)
   - Rare across other documents (high IDF)
   ...receive the highest scores.

Example from Document 1:
   - 'Python' appears 3 times in Doc 1, but rarely in other documents → HIGH TF-IDF
   - 'programming' appears 2 times, rarely in other docs → HIGH TF-IDF
   - 'language' appears 1 time, appears in Document 3 too → LOWER TF-IDF
""")

print()
print("WHY COMMON WORDS HAVE LOWER SCORES:")
print("-" * 80)
print("""
1. STOPWORDS ARE REMOVED: The TfidfVectorizer automatically removes English
   stopwords (is, the, a, and, etc.) because they appear in almost all documents
   and don't help differentiate document topics.

2. EVEN IF NOT REMOVED: Words like 'is', 'data', 'analysis' that appear across
   multiple documents have lower IDF scores because they're not unique to any
   single document.

3. PRINCIPLE: TF-IDF is designed to find words that are:
   - IMPORTANT for distinguishing a document's content
   - NOT common across all documents
   - Unique/specific to the document's topic

Example:
   - 'data' appears in Documents 3, 4, and 5 → LOW IDF (appears in many docs)
   - 'python' appears mainly in Document 1 → HIGH IDF (appears in few docs)
""")

print()
print("KEY INSIGHTS:")
print("-" * 80)
print("""
✓ TF-IDF is useful for: Identifying topic-specific words, document similarity,
  search engine ranking, and information retrieval.

✓ Higher Scores = More Important for that document's classification

✓ The algorithm automatically focuses on words that matter most for
  distinguishing between documents.

✓ Common knowledge words are automatically downweighted in favor of
  domain-specific terminology.
""")

print("=" * 80)
