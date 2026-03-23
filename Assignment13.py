"""
Assignment (10/03/2026)
Assignment Name : Spam Classifier Thinking
Description : Design a spam detection system: features, data needed, possible mistakes.

"""

# ============================================================
# ASSIGNMENT: Spam Classifier Thinking
# Date: 10/03/2026
# Description: Design a spam detection system:
#              features, data needed, possible mistakes
# ============================================================

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, confusion_matrix)

# ============================================================
# STEP 1: DATASET (Simulated SMS Messages)
# ============================================================

messages = [
    # SPAM
    ("Win a FREE iPhone now! Click here: bit.ly/win999",          "spam"),
    ("URGENT: Your account has been compromised. Verify NOW!",    "spam"),
    ("Congratulations! You've won $5000. Call 1800-PRIZE",        "spam"),
    ("Get rich quick! Work from home, earn $500/day guaranteed",  "spam"),
    ("FREE entry: win a luxury cruise. Text WIN to 80800",        "spam"),
    ("ALERT: Your bank account is suspended. Login immediately",  "spam"),
    ("You are selected for a cash prize of $10,000. Claim now!",  "spam"),
    ("Cheap meds online! No prescription needed. Order today!",   "spam"),
    ("Hot singles in your area! Click to meet them now",          "spam"),
    ("Your loan is approved! Get $50,000 instantly. Apply here",  "spam"),
    ("Double your investment in 24hrs. 100% guaranteed returns",  "spam"),
    ("Free gift card! You are our lucky winner today. Tap here",  "spam"),

    # HAM
    ("Hey, are we still meeting for lunch tomorrow?",             "ham"),
    ("Your OTP for login is 482910. Do not share with anyone.",   "ham"),
    ("Mom, I will be home by 7pm. Don't worry.",                  "ham"),
    ("Meeting rescheduled to 3pm. Please confirm attendance.",    "ham"),
    ("Your order #4521 has been shipped. Expected by Friday.",    "ham"),
    ("Can you please send me the project report by tonight?",     "ham"),
    ("Happy birthday! Hope you have a wonderful day ahead.",      "ham"),
    ("Reminder: Doctor appointment at 10am tomorrow.",            "ham"),
    ("The match starts at 8pm. Let's watch it together!",         "ham"),
    ("Your subscription renewal is due on 15th of this month.",   "ham"),
    ("Please review the attached document and give feedback.",    "ham"),
    ("Thanks for your help yesterday. Really appreciated it!",    "ham"),
]

df = pd.DataFrame(messages, columns=["message", "label"])

print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)
print(f"Total messages : {len(df)}")
print(f"Spam messages  : {len(df[df.label == 'spam'])}")
print(f"Ham messages   : {len(df[df.label == 'ham'])}")
print()
print(df.to_string(index=False))
print()

# ============================================================
# STEP 2: FEATURE ENGINEERING
# ============================================================

print("=" * 60)
print("FEATURE ENGINEERING")
print("=" * 60)

def extract_features(text):
    """Extract handcrafted features from raw message text."""
    return {
        "length"          : len(text),
        "word_count"      : len(text.split()),
        "uppercase_count" : sum(1 for c in text if c.isupper()),
        "exclaim_count"   : text.count("!"),
        "has_url"         : int(any(w in text.lower()
                                for w in ["http", "bit.ly", "click", "www"])),
        "has_money"       : int(any(w in text.lower()
                                for w in ["$", "£", "cash", "prize",
                                          "win", "free", "loan"])),
        "has_urgency"     : int(any(w in text.lower()
                                for w in ["urgent", "immediately", "now",
                                          "alert", "verify", "suspended"])),
        "digit_count"     : sum(1 for c in text if c.isdigit()),
    }

feature_rows = [extract_features(m) for m in df["message"]]
feature_df   = pd.DataFrame(feature_rows)

print("Handcrafted features extracted:")
print(feature_df.to_string(index=False))
print()

# ============================================================
# STEP 3: TF-IDF VECTORIZATION
# ============================================================

print("=" * 60)
print("TF-IDF VECTORIZATION")
print("=" * 60)

df["label_num"] = df["label"].map({"ham": 0, "spam": 1})

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=50,
    ngram_range=(1, 2)   # unigrams + bigrams
)

X_tfidf = vectorizer.fit_transform(df["message"]).toarray()
y        = df["label_num"].values

print(f"Vocabulary size (top features) : {len(vectorizer.get_feature_names_out())}")
print(f"Top 20 TF-IDF features         : "
      f"{list(vectorizer.get_feature_names_out()[:20])}")
print(f"TF-IDF matrix shape            : {X_tfidf.shape}")
print()

# ============================================================
# STEP 4: TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.25, random_state=42, stratify=y
)

print("=" * 60)
print("TRAIN / TEST SPLIT")
print("=" * 60)
print(f"Training samples : {len(X_train)}")
print(f"Testing  samples : {len(X_test)}")
print()

# ============================================================
# STEP 5: TRAIN TWO MODELS
# ============================================================

models = {
    "Naive Bayes"        : MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
}

results = {}

print("=" * 60)
print("MODEL TRAINING & EVALUATION")
print("=" * 60)

for name, clf in models.items():
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec  = recall_score(y_test, y_pred, zero_division=0)
    f1   = f1_score(y_test, y_pred, zero_division=0)
    cm   = confusion_matrix(y_test, y_pred)

    results[name] = {
        "model"    : clf,
        "accuracy" : acc,
        "precision": prec,
        "recall"   : rec,
        "f1"       : f1,
        "cm"       : cm,
        "y_pred"   : y_pred,
    }

    print(f"Model     : {name}")
    print(f"Accuracy  : {acc:.4f}")
    print(f"Precision : {prec:.4f}  (of predicted spam, how many were actually spam?)")
    print(f"Recall    : {rec:.4f}  (of actual spam, how many did we catch?)")
    print(f"F1 Score  : {f1:.4f}  (harmonic mean of precision & recall)")
    print()
    print("Confusion Matrix:")
    print(f"                  Predicted Ham   Predicted Spam")
    print(f"  Actual Ham    :      {cm[0][0]}               {cm[0][1]}")
    print(f"  Actual Spam   :      {cm[1][0]}               {cm[1][1]}")
    print()

    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (cm[0,0], 0, 0, cm[1,1])
    print(f"  True Negatives  (Ham  correctly identified) : {tn}")
    print(f"  False Positives (Ham  wrongly flagged spam) : {fp}  <-- DANGEROUS")
    print(f"  False Negatives (Spam missed by classifier) : {fn}  <-- ANNOYING")
    print(f"  True Positives  (Spam correctly caught)     : {tp}")
    print("-" * 60)
    print()

# ============================================================
# STEP 6: POSSIBLE MISTAKES (Error Analysis)
# ============================================================

print("=" * 60)
print("POSSIBLE MISTAKES & FAILURE ANALYSIS")
print("=" * 60)

mistakes = [
    {
        "type"   : "False Positive (Type I Error)",
        "what"   : "Ham classified as Spam",
        "example": "Your OTP is 482910 → flagged as spam (has digits + urgency words)",
        "impact" : "CRITICAL — user misses important messages",
        "fix"    : "Lower spam threshold; whitelist known senders",
    },
    {
        "type"   : "False Negative (Type II Error)",
        "what"   : "Spam classified as Ham",
        "example": "Cleverly worded phishing email with no trigger words",
        "impact" : "HIGH — user exposed to scam or malware",
        "fix"    : "Use character n-grams; add URL reputation checking",
    },
    {
        "type"   : "Vocabulary Mismatch",
        "what"   : "New spam words not in training vocabulary",
        "example": "'Cr1ck3t' or 'Fr33' (leet-speak to bypass filters)",
        "impact" : "MEDIUM — adversarial spammers bypass the model",
        "fix"    : "Character-level models; continuous retraining",
    },
    {
        "type"   : "Class Imbalance",
        "what"   : "Far more ham than spam in training data",
        "example": "99% ham → model learns to always predict ham",
        "impact" : "HIGH — recall for spam drops to near zero",
        "fix"    : "Oversample spam (SMOTE); use class_weight='balanced'",
    },
    {
        "type"   : "Context Blindness",
        "what"   : "Model reads words, not intent",
        "example": "'Win' in 'I hope you win the match' flagged as spam",
        "impact" : "MEDIUM — false positives on innocent messages",
        "fix"    : "Use sentence embeddings (BERT) for context",
    },
    {
        "type"   : "Language/Script Variation",
        "what"   : "Model trained on English fails on Hindi/Hinglish",
        "example": "'Aapka account band ho gaya' not detected as spam",
        "impact" : "HIGH — non-English spam bypasses classifier",
        "fix"    : "Multilingual training data; language detection layer",
    },
]

for i, m in enumerate(mistakes, 1):
    print(f"Mistake #{i}: {m['type']}")
    print(f"  What    : {m['what']}")
    print(f"  Example : {m['example']}")
    print(f"  Impact  : {m['impact']}")
    print(f"  Fix     : {m['fix']}")
    print()

# ============================================================
# STEP 7: DATA NEEDED FOR A REAL SYSTEM
# ============================================================

print("=" * 60)
print("DATA NEEDED FOR A REAL SPAM CLASSIFIER")
print("=" * 60)

data_requirements = [
    ("Labeled messages",        "Thousands of spam + ham examples with correct labels"),
    ("Sender metadata",         "Sender ID, domain reputation, send frequency"),
    ("Time patterns",           "Spam often sent in bulk at unusual hours"),
    ("URL data",                "Whether links are on known phishing blacklists"),
    ("User feedback",           "Manual 'Mark as spam' clicks from real users"),
    ("Language diversity",      "Messages in multiple languages and scripts"),
    ("Adversarial examples",    "Known spam evasion tactics to train robustness"),
    ("Class balance",           "Roughly equal spam/ham or use resampling"),
]

print(f"{'Data Type':<25} {'Why It's Needed'}")
print("-" * 60)
for dtype, reason in data_requirements:
    print(f"  {dtype:<23} {reason}")
print()

# ============================================================
# STEP 8: PREDICT NEW MESSAGES
# ============================================================

print("=" * 60)
print("TESTING WITH NEW MESSAGES")
print("=" * 60)

best_model_name = max(results, key=lambda k: results[k]["f1"])
best_clf        = results[best_model_name]["model"]

print(f"Using best model: {best_model_name}")
print()

new_messages = [
    "You have won a free vacation! Claim your prize now.",
    "Can we reschedule our meeting to 4pm?",
    "URGENT: Click here to unlock your blocked account!",
    "Your package will arrive between 2pm and 5pm today.",
    "Earn $1000 daily from home. No experience needed!!!",
]

X_new    = vectorizer.transform(new_messages).toarray()
y_new    = best_clf.predict(X_new)
y_prob   = best_clf.predict_proba(X_new)[:, 1] \
           if hasattr(best_clf, "predict_proba") else [None] * len(new_messages)

label_map = {0: "HAM", 1: "SPAM"}

print(f"{'#':<3} {'Message':<50} {'Label':<6} {'Spam Prob':>10}")
print("-" * 75)
for i, (msg, label, prob) in enumerate(zip(new_messages, y_new, y_prob), 1):
    short  = msg[:47] + "..." if len(msg) > 47 else msg
    prob_s = f"{prob:.4f}" if prob is not None else "N/A"
    print(f"{i:<3} {short:<50} {label_map[label]:<6} {prob_s:>10}")

print()
print("=" * 60)
print("DONE")
print("=" * 60)