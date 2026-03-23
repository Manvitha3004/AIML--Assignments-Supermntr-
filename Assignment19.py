"""
Assignment (21/03/2026)
Assignment Name : Build a Text Cleaner
Description : Write code to remove punctuation, lowercase text, remove stopwords and test it.

Run:
    pip install nltk          (optional — built-in stopwords are used if NLTK unavailable)
    python text_cleaner.py
"""

import re
import string
import time

# ─────────────────────────────────────────────────────────────
# STOPWORDS  (built-in list — no external library needed)
# If NLTK is installed, its larger corpus is used automatically.
# ─────────────────────────────────────────────────────────────
BUILTIN_STOPWORDS = {
    "i","me","my","myself","we","our","ours","ourselves","you","your","yours",
    "yourself","yourselves","he","him","his","himself","she","her","hers",
    "herself","it","its","itself","they","them","their","theirs","themselves",
    "what","which","who","whom","this","that","these","those","am","is","are",
    "was","were","be","been","being","have","has","had","having","do","does",
    "did","doing","a","an","the","and","but","if","or","because","as","until",
    "while","of","at","by","for","with","about","against","between","into",
    "through","during","before","after","above","below","to","from","up","down",
    "in","out","on","off","over","under","again","further","then","once","here",
    "there","when","where","why","how","all","both","each","few","more","most",
    "other","some","such","no","nor","not","only","own","same","so","than",
    "too","very","s","t","can","will","just","don","should","now","d","ll","m",
    "o","re","ve","y","ain","aren","couldn","didn","doesn","hadn","hasn",
    "haven","isn","ma","mightn","mustn","needn","shan","shouldn","wasn",
    "weren","won","wouldn",
}

def get_stopwords():
    try:
        from nltk.corpus import stopwords as nltk_sw
        import nltk
        nltk.download("stopwords", quiet=True)
        sw = set(nltk_sw.words("english"))
        print("  [INFO] Using NLTK stopwords corpus.")
        return sw
    except Exception:
        print("  [INFO] NLTK not available — using built-in stopwords list.")
        return BUILTIN_STOPWORDS

# ─────────────────────────────────────────────────────────────
# TEXT CLEANER CLASS
# ─────────────────────────────────────────────────────────────
class TextCleaner:
    """
    A complete NLP text cleaning pipeline.

    Steps (applied in order):
        1. Lowercase
        2. Remove URLs
        3. Remove HTML tags
        4. Remove emojis
        5. Remove punctuation
        6. Remove extra whitespace
        7. Remove stopwords
    """

    def __init__(self, stopwords=None, keep_numbers=False):
        self.stopwords    = stopwords if stopwords else get_stopwords()
        self.keep_numbers = keep_numbers
        # Emoji regex pattern (covers all Unicode emoji ranges)
        self._emoji_re = re.compile(
            "["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            u"\U00002700-\U000027BF"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )

    # ── individual steps ──────────────────────────────────────

    def to_lowercase(self, text: str) -> str:
        """Convert all characters to lowercase."""
        return text.lower()

    def remove_urls(self, text: str) -> str:
        """Remove http/https URLs."""
        return re.sub(r"https?://\S+|www\.\S+", "", text)

    def remove_html(self, text: str) -> str:
        """Strip HTML / XML tags."""
        return re.sub(r"<[^>]+>", "", text)

    def remove_emojis(self, text: str) -> str:
        """Remove emoji characters."""
        return self._emoji_re.sub("", text)

    def remove_punctuation(self, text: str) -> str:
        """Remove all punctuation marks."""
        return text.translate(str.maketrans("", "", string.punctuation))

    def remove_numbers(self, text: str) -> str:
        """Remove standalone numeric tokens."""
        return re.sub(r"\b\d+\b", "", text)

    def remove_extra_spaces(self, text: str) -> str:
        """Collapse multiple spaces into one and strip edges."""
        return re.sub(r"\s+", " ", text).strip()

    def remove_stopwords(self, text: str) -> str:
        """Remove common English stopwords."""
        tokens = text.split()
        filtered = [w for w in tokens if w.lower() not in self.stopwords]
        return " ".join(filtered)

    # ── full pipeline ─────────────────────────────────────────

    def clean(self, text: str, verbose: bool = False) -> str:
        """
        Apply full cleaning pipeline.
        Set verbose=True to see intermediate steps.
        """
        steps = [
            ("Lowercase",         self.to_lowercase),
            ("Remove URLs",       self.remove_urls),
            ("Remove HTML",       self.remove_html),
            ("Remove Emojis",     self.remove_emojis),
            ("Remove Punctuation",self.remove_punctuation),
        ]
        if not self.keep_numbers:
            steps.append(("Remove Numbers", self.remove_numbers))
        steps += [
            ("Remove Extra Spaces", self.remove_extra_spaces),
            ("Remove Stopwords",    self.remove_stopwords),
            ("Final Trim",          self.remove_extra_spaces),
        ]

        result = text
        if verbose:
            print(f"  ORIGINAL : {text}")
        for name, fn in steps:
            result = fn(result)
            if verbose:
                print(f"  {name:<22}: {result}")
        return result

    def clean_batch(self, texts: list) -> list:
        """Clean a list of sentences."""
        return [self.clean(t) for t in texts]

    def stats(self, original: str, cleaned: str) -> dict:
        """Return cleaning statistics."""
        orig_words    = original.split()
        cleaned_words = cleaned.split()
        removed       = len(orig_words) - len(cleaned_words)
        return {
            "original_chars"  : len(original),
            "cleaned_chars"   : len(cleaned),
            "original_words"  : len(orig_words),
            "cleaned_words"   : len(cleaned_words),
            "words_removed"   : removed,
            "reduction_pct"   : round(removed / max(len(orig_words), 1) * 100, 1),
        }


# ─────────────────────────────────────────────────────────────
# TEST SUITE
# ─────────────────────────────────────────────────────────────
TEST_SENTENCES = [
    # (label, input_text)
    ("Basic messy text",
     "Hello!! This is a SAMPLE sentence, with some punctuation..."),

    ("Stopwords heavy",
     "I am going to the store and I will be back soon."),

    ("Emojis + slang",
     "omg this pizza is sooo good!! 😍😍 I luv it so much 🍕🔥"),

    ("URL + HTML",
     "Check out <b>our website</b> at https://www.example.com for more info!!!"),

    ("Numbers + noise",
     "The 2026 Olympics will have 10,000 athletes from 200 countries."),

    ("All lowercase already",
     "natural language processing is a field of artificial intelligence."),

    ("Mixed caps + punctuation",
     "WHAT?! Are YOU serious??? This CAN'T be right... or can it??"),

    ("Social media style",
     "Just posted a new blog @ medium.com — likes & retweets appreciated!! #NLP #AI"),

    ("Long paragraph",
     "Machine learning is a subset of artificial intelligence that enables computers "
     "to learn from data without being explicitly programmed. It is widely used in "
     "many applications such as recommendation systems, fraud detection, and image recognition."),

    ("Empty / whitespace edge case",
     "   "),
]

def run_tests(cleaner: TextCleaner):
    PASS = 0
    FAIL = 0
    WIDTH = 62

    print("\n" + "=" * WIDTH)
    print("   TEXT CLEANER — TEST RESULTS")
    print("=" * WIDTH)

    for label, text in TEST_SENTENCES:
        start   = time.perf_counter()
        cleaned = cleaner.clean(text)
        elapsed = (time.perf_counter() - start) * 1000
        s       = cleaner.stats(text, cleaned)

        # Pass conditions
        has_upper = any(c.isupper() for c in cleaned)
        has_punct = any(c in string.punctuation for c in cleaned)
        ok = not has_upper and not has_punct

        status = "PASS" if ok else "FAIL"
        if ok: PASS += 1
        else:  FAIL += 1

        print(f"\n  [{status}] {label}")
        print(f"  IN  : {text[:70]}{'...' if len(text) > 70 else ''}")
        print(f"  OUT : {cleaned[:70]}{'...' if len(cleaned) > 70 else ''}")
        print(f"  Words: {s['original_words']} -> {s['cleaned_words']} "
              f"({s['reduction_pct']}% reduction)  |  {elapsed:.2f} ms")

    print("\n" + "-" * WIDTH)
    print(f"  Results:  {PASS} PASSED  |  {FAIL} FAILED  |  {PASS+FAIL} TOTAL")
    print("=" * WIDTH)

def verbose_demo(cleaner: TextCleaner):
    """Show step-by-step cleaning for one sentence."""
    sample = "WOW!! Check out https://example.com — it's the BEST site 😎 for ML & AI learning..."
    print("\n\n" + "=" * 62)
    print("   STEP-BY-STEP DEMO")
    print("=" * 62)
    cleaner.clean(sample, verbose=True)
    print()


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 62)
    print("   BUILD A TEXT CLEANER  —  Assignment 21/03/2026")
    print("=" * 62)

    # Initialise cleaner
    cleaner = TextCleaner()

    # Run all tests
    run_tests(cleaner)

    # Show verbose step-by-step on one example
    verbose_demo(cleaner)

    # Interactive batch demo
    batch = [
        "The quick Brown Fox jumped over the LAZY dog!!!",
        "I was watching Netflix at 3am and it was amazing 😂😂",
        "Please visit www.google.com for all your search needs.",
    ]
    print("BATCH CLEAN DEMO")
    print("-" * 62)
    results = cleaner.clean_batch(batch)
    for orig, cleaned in zip(batch, results):
        print(f"  IN  : {orig}")
        print(f"  OUT : {cleaned}\n")