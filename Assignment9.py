"""
Assignment (02/03/2026)
Assignment Name: ML Idea Generator
Description: Suggest ML problems in college, healthcare, shopping and describe input → output.

"""

# ── ML Idea Generator ────

from datetime import datetime

# ── Dataset ────

ML_IDEAS = {
    "College": [
        {
            "id"         : "C01",
            "title"      : "Student Dropout Predictor",
            "problem"    : "Identify students at risk of dropping out early.",
            "ml_type"    : "Classification",
            "algorithm"  : "Random Forest / XGBoost",
            "inputs"     : ["Attendance %", "Assignment scores", "GPA trend",
                            "Fee payment status", "Participation in events"],
            "output"     : "Risk label — High / Medium / Low dropout probability",
            "real_world" : "Universities reduce dropout rates by 30% using early alerts.",
            "difficulty" : "⭐⭐⭐",
        },
        {
            "id"         : "C02",
            "title"      : "Smart Course Recommender",
            "problem"    : "Recommend electives best suited for each student.",
            "ml_type"    : "Recommendation System",
            "algorithm"  : "Collaborative Filtering / Matrix Factorization",
            "inputs"     : ["Past subject grades", "Career goal", "Interests survey",
                            "Peer enrollment patterns", "Faculty ratings"],
            "output"     : "Ranked list of top 5 recommended elective courses",
            "real_world" : "Used by Coursera and edX to personalise learning paths.",
            "difficulty" : "⭐⭐⭐⭐",
        },
        {
            "id"         : "C03",
            "title"      : "Exam Score Predictor",
            "problem"    : "Predict final exam scores from mid-term behaviour.",
            "ml_type"    : "Regression",
            "algorithm"  : "Linear Regression / Gradient Boosting",
            "inputs"     : ["Mid-term scores", "Study hours/week", "Attendance",
                            "Assignment completion %", "Online resource usage"],
            "output"     : "Predicted final exam score (0–100)",
            "real_world" : "Helps educators intervene before final exams.",
            "difficulty" : "⭐⭐",
        },
        {
            "id"         : "C04",
            "title"      : "Plagiarism Detection System",
            "problem"    : "Detect plagiarised content in student assignments.",
            "ml_type"    : "NLP / Similarity Detection",
            "algorithm"  : "TF-IDF + Cosine Similarity / BERT Embeddings",
            "inputs"     : ["Student essay text", "Reference corpus",
                            "Past submissions", "Web content snapshot"],
            "output"     : "Similarity score (%) + flagged sentence spans",
            "real_world" : "Turnitin processes 1M+ papers daily using similar tech.",
            "difficulty" : "⭐⭐⭐⭐",
        },
        {
            "id"         : "C05",
            "title"      : "Campus Placement Predictor",
            "problem"    : "Predict whether a student will get placed in campus hiring.",
            "ml_type"    : "Binary Classification",
            "algorithm"  : "Logistic Regression / SVM",
            "inputs"     : ["CGPA", "Internship count", "Coding skills score",
                            "Communication rating", "Backlogs count"],
            "output"     : "Placed / Not Placed  +  Expected salary range",
            "real_world" : "TPO teams use this to focus training resources.",
            "difficulty" : "⭐⭐",
        },
    ],

    "Healthcare": [
        {
            "id"         : "H01",
            "title"      : "Disease Risk Screener",
            "problem"    : "Predict likelihood of diabetes / heart disease early.",
            "ml_type"    : "Classification",
            "algorithm"  : "Logistic Regression / Neural Network",
            "inputs"     : ["Age", "BMI", "Blood pressure", "Glucose level",
                            "Family history", "Lifestyle habits"],
            "output"     : "Risk probability (%) + suggested medical tests",
            "real_world" : "Google Health uses similar models for diabetic retinopathy.",
            "difficulty" : "⭐⭐⭐",
        },
        {
            "id"         : "H02",
            "title"      : "Medical Image Analyser",
            "problem"    : "Detect tumours or anomalies in X-rays / MRI scans.",
            "ml_type"    : "Computer Vision / CNN",
            "algorithm"  : "ResNet-50 / U-Net / Vision Transformer",
            "inputs"     : ["X-ray / MRI image", "Patient age", "Scan region",
                            "Previous scan history"],
            "output"     : "Bounding box around anomaly + confidence score",
            "real_world" : "FDA-approved AI detects lung cancer in CT scans.",
            "difficulty" : "⭐⭐⭐⭐⭐",
        },
        {
            "id"         : "H03",
            "title"      : "Drug Interaction Checker",
            "problem"    : "Flag dangerous combinations in a patient prescription.",
            "ml_type"    : "Graph Neural Network / NLP",
            "algorithm"  : "Knowledge Graph + GNN",
            "inputs"     : ["List of prescribed drugs", "Patient age", "Weight",
                            "Existing conditions", "Allergy history"],
            "output"     : "Interaction severity — Safe / Caution / Dangerous",
            "real_world" : "IBM Watson Health checks 10,000+ drug pairs per query.",
            "difficulty" : "⭐⭐⭐⭐",
        },
        {
            "id"         : "H04",
            "title"      : "Patient Readmission Predictor",
            "problem"    : "Predict if a discharged patient will be readmitted in 30 days.",
            "ml_type"    : "Classification",
            "algorithm"  : "XGBoost / LSTM (time-series vitals)",
            "inputs"     : ["Discharge diagnosis", "Vitals trend", "Age",
                            "Comorbidities", "Medication adherence score"],
            "output"     : "Readmission risk (%) + recommended follow-up interval",
            "real_world" : "Reduces hospital costs by $15,000 per avoided readmission.",
            "difficulty" : "⭐⭐⭐",
        },
        {
            "id"         : "H05",
            "title"      : "Mental Health Sentiment Tracker",
            "problem"    : "Detect early signs of depression from patient journal entries.",
            "ml_type"    : "NLP / Sentiment Analysis",
            "algorithm"  : "BERT Fine-tuned / VADER + LSTM",
            "inputs"     : ["Daily journal text", "Sleep hours", "Activity level",
                            "PHQ-9 survey score", "Social interaction frequency"],
            "output"     : "Mood trend graph + Depression risk flag (Low/Med/High)",
            "real_world" : "Woebot and Wysa use NLP to support 5M+ users globally.",
            "difficulty" : "⭐⭐⭐⭐",
        },
    ],

    "Shopping": [
        {
            "id"         : "S01",
            "title"      : "Product Recommendation Engine",
            "problem"    : "Recommend products a user is likely to buy next.",
            "ml_type"    : "Recommendation System",
            "algorithm"  : "ALS Matrix Factorization / Deep FM",
            "inputs"     : ["Browse history", "Purchase history", "Cart items",
                            "Wishlist", "Similar user behaviour"],
            "output"     : "Top-10 personalised product recommendations",
            "real_world" : "Amazon's engine drives 35% of total revenue.",
            "difficulty" : "⭐⭐⭐⭐",
        },
        {
            "id"         : "S02",
            "title"      : "Dynamic Pricing Optimiser",
            "problem"    : "Automatically adjust prices based on demand & competition.",
            "ml_type"    : "Regression / Reinforcement Learning",
            "algorithm"  : "Gradient Boosting / Q-Learning",
            "inputs"     : ["Current demand", "Competitor prices", "Stock level",
                            "Time of day/week", "User price sensitivity"],
            "output"     : "Optimal price point to maximise revenue",
            "real_world" : "Uber surge pricing and airline fares use this technique.",
            "difficulty" : "⭐⭐⭐⭐⭐",
        },
        {
            "id"         : "S03",
            "title"      : "Fake Review Detector",
            "problem"    : "Identify fraudulent or bot-generated product reviews.",
            "ml_type"    : "NLP / Anomaly Detection",
            "algorithm"  : "BERT + Isolation Forest",
            "inputs"     : ["Review text", "Reviewer history", "Rating pattern",
                            "Account age", "Verified purchase flag"],
            "output"     : "Genuine / Suspicious / Fake label + confidence %",
            "real_world" : "Amazon removes 200M+ fake reviews yearly using ML.",
            "difficulty" : "⭐⭐⭐",
        },
        {
            "id"         : "S04",
            "title"      : "Customer Churn Predictor",
            "problem"    : "Identify customers likely to stop shopping on the platform.",
            "ml_type"    : "Binary Classification",
            "algorithm"  : "Random Forest / Neural Network",
            "inputs"     : ["Days since last purchase", "Order frequency",
                            "Average spend", "Support complaints", "App usage"],
            "output"     : "Churn probability + personalised retention offer",
            "real_world" : "Reducing churn by 5% increases profits by up to 25%.",
            "difficulty" : "⭐⭐⭐",
        },
        {
            "id"         : "S05",
            "title"      : "Visual Search Engine",
            "problem"    : "Let users search products by uploading a photo.",
            "ml_type"    : "Computer Vision",
            "algorithm"  : "Siamese Network / CLIP (OpenAI)",
            "inputs"     : ["User-uploaded image", "Colour palette",
                            "Shape features", "Texture embeddings"],
            "output"     : "Visually similar products ranked by similarity score",
            "real_world" : "Pinterest Lens and ASOS use this for fashion discovery.",
            "difficulty" : "⭐⭐⭐⭐",
        },
    ],
}

# ── Display Utilities ─────

def divider(char: str = "─", width: int = 65) -> str:
    return char * width

def print_header():
    print("\n" + "=" * 65)
    print("       🤖  ML Idea Generator — Domain Explorer")
    print(f"       📅  {datetime.now().strftime('%d %B %Y  |  %I:%M %p')}")
    print("=" * 65)

def print_idea_card(idea: dict, index: int):
    """Print one ML idea in a formatted card."""
    print(f"\n  ┌─ {idea['id']}  {idea['title']} {'─' * (40 - len(idea['title']))}")
    print(f"  │  🎯 Problem    : {idea['problem']}")
    print(f"  │  🧠 ML Type    : {idea['ml_type']}")
    print(f"  │  ⚙  Algorithm  : {idea['algorithm']}")
    print(f"  │  📥 Inputs     :")
    for inp in idea["inputs"]:
        print(f"  │      • {inp}")
    print(f"  │  📤 Output     : {idea['output']}")
    print(f"  │  🌍 Real World : {idea['real_world']}")
    print(f"  │  🔥 Difficulty : {idea['difficulty']}")
    print(f"  └{'─' * 62}")

def print_domain(domain: str):
    """Print all ML ideas for a given domain."""
    icon = {"College": "🎓", "Healthcare": "🏥", "Shopping": "🛒"}.get(domain, "📌")
    ideas = ML_IDEAS[domain]

    print("\n" + "=" * 65)
    print(f"   {icon}  Domain : {domain}  ({len(ideas)} ML Ideas)")
    print("=" * 65)

    for i, idea in enumerate(ideas, 1):
        print_idea_card(idea, i)

def print_summary_table():
    """Print a compact summary of all 15 ideas."""
    print("\n" + "=" * 65)
    print("   📊  Summary Table — All 15 ML Ideas")
    print("=" * 65)
    print(f"  {'ID':<5} {'Title':<35} {'Type':<20} {'Diff'}")
    print(f"  {divider('─', 61)}")

    for domain, ideas in ML_IDEAS.items():
        icon = {"College": "🎓", "Healthcare": "🏥", "Shopping": "🛒"}[domain]
        print(f"\n  {icon}  {domain}")
        for idea in ideas:
            title  = idea["title"][:33]
            ml_t   = idea["ml_type"][:18]
            diff   = idea["difficulty"]
            print(f"  {idea['id']:<5} {title:<35} {ml_t:<20} {diff}")

    print("\n" + "=" * 65)

def print_ml_type_stats():
    """Show how ML types are distributed across all ideas."""
    print("\n" + "=" * 65)
    print("   🔬  ML Type Distribution Across All Ideas")
    print("=" * 65)

    from collections import Counter
    all_types = []
    for ideas in ML_IDEAS.values():
        for idea in ideas:
            # Grab the primary type (before /)
            primary = idea["ml_type"].split("/")[0].strip()
            all_types.append(primary)

    counts = Counter(all_types).most_common()
    max_c  = counts[0][1]

    for ml_type, count in counts:
        bar   = "█" * (count * 6)
        print(f"  {ml_type:<35} {count:>2}x  {bar}")

    print("=" * 65)

def print_input_output_flow():
    """Print a visual Input → Model → Output flow for each domain."""
    print("\n" + "=" * 65)
    print("   🔄  Input → Model → Output Flow")
    print("=" * 65)

    for domain, ideas in ML_IDEAS.items():
        icon = {"College": "🎓", "Healthcare": "🏥", "Shopping": "🛒"}[domain]
        print(f"\n  {icon}  {domain}")
        print(f"  {divider('─', 62)}")
        for idea in ideas:
            inputs_str = ", ".join(idea["inputs"][:3]) + " ..."
            print(f"  [{inputs_str}]")
            print(f"      ↓  {idea['algorithm']}")
            print(f"      ✅  {idea['output']}\n")

# ── Main ─────

def main():
    print_header()

    for domain in ML_IDEAS:
        print_domain(domain)

    print_summary_table()
    print_ml_type_stats()
    print_input_output_flow()

    print("\n  ✅  ML Idea Generator complete!\n")

if __name__ == "__main__":
    main()