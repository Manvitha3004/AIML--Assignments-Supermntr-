""" Assignment (24/02/2026)

Dataset Detective
Description: Load a dataset, display top rows, find highest value column, count missing values, share 5 insights.
""" 

# ── Dataset Detective ────

import numpy as np
import pandas as pd

# ── Dataset Builder ─────

def build_dataset() -> pd.DataFrame:
    """Create a realistic student performance dataset with intentional missing values."""
    np.random.seed(42)
    n = 100

    data = {
        "Student_ID"  : [f"S{str(i).zfill(3)}" for i in range(1, n + 1)],
        "Name"        : [f"Student_{i}"         for i in range(1, n + 1)],
        "Age"         : np.random.randint(16, 22, n),
        "Gender"      : np.random.choice(["Male", "Female"], n),
        "Math"        : np.random.randint(40, 100, n).astype(float),
        "Science"     : np.random.randint(40, 100, n).astype(float),
        "English"     : np.random.randint(40, 100, n).astype(float),
        "History"     : np.random.randint(40, 100, n).astype(float),
        "Computer"    : np.random.randint(40, 100, n).astype(float),
        "Attendance"  : np.random.randint(60, 100, n).astype(float),
        "Study_Hours" : np.random.uniform(1.0, 8.0, n).round(1),
    }

    df = pd.DataFrame(data)

    # Inject realistic missing values (~5–8% per numeric column)
    for col in ["Math", "Science", "English", "History", "Computer",
                "Attendance", "Study_Hours"]:
        mask = np.random.choice([True, False], size=n, p=[0.06, 0.94])
        df.loc[mask, col] = np.nan

    # Compute derived columns
    subject_cols   = ["Math", "Science", "English", "History", "Computer"]
    df["Average"]  = df[subject_cols].mean(axis=1).round(2)
    df["Grade"]    = df["Average"].apply(assign_grade)
    df["Status"]   = df["Average"].apply(lambda a: "Pass" if a >= 50 else "Fail")

    return df


# ── Helper Functions ──────

def assign_grade(avg: float) -> str:
    if   pd.isna(avg): return "N/A"
    elif avg >= 90:    return "A+"
    elif avg >= 80:    return "A"
    elif avg >= 70:    return "B"
    elif avg >= 60:    return "C"
    elif avg >= 50:    return "D"
    else:              return "F"


def bar(value: float, max_val: float = 100, width: int = 25) -> str:
    """Return a scaled █ bar for terminal charts."""
    filled = int((value / max_val) * width)
    return "█" * filled + "░" * (width - filled)


def divider(char: str = "─", width: int = 65) -> str:
    return char * width


# ── Section Printers ──────

def show_top_rows(df: pd.DataFrame, n: int = 5) -> None:
    """Display the first n rows in a formatted table."""
    cols = ["Student_ID", "Age", "Gender", "Math", "Science",
            "English", "Average", "Grade", "Status"]

    print("\n" + "=" * 65)
    print("   👀  Top Rows Preview  (first 5 records)")
    print("=" * 65)

    # Header
    print(f"  {'ID':<8} {'Age':>4} {'Gender':<8} {'Math':>5} "
          f"{'Sci':>5} {'Eng':>5} {'Avg':>6}  {'Grd':>4}  Status")
    print(f"  {divider('─', 63)}")

    for _, row in df[cols].head(n).iterrows():
        print(f"  {row['Student_ID']:<8} {int(row['Age']):>4} {row['Gender']:<8} "
              f"{row['Math']:>5.1f} {row['Science']:>5.1f} {row['English']:>5.1f} "
              f"{row['Average']:>6.2f}  {row['Grade']:>4}  {row['Status']}")

    print(f"  {divider('─', 63)}")
    print(f"  Total rows: {len(df):,}  |  Total columns: {len(df.columns)}")
    print("=" * 65)


def show_dataset_shape(df: pd.DataFrame) -> None:
    """Print dataset dimensions and column types."""
    print("\n" + "=" * 65)
    print("   📐  Dataset Shape & Columns")
    print("=" * 65)
    print(f"  Rows    : {len(df):,}")
    print(f"  Columns : {len(df.columns)}")
    print()
    print(f"  {'Column':<15} {'Type':<12} {'Non-Null':>8}  {'Null':>5}")
    print(f"  {divider('─', 45)}")

    for col in df.columns:
        dtype    = str(df[col].dtype)
        non_null = df[col].notna().sum()
        null     = df[col].isna().sum()
        print(f"  {col:<15} {dtype:<12} {non_null:>8}  {null:>5}")

    print("=" * 65)


def show_missing_values(df: pd.DataFrame) -> None:
    """Display missing value counts and percentages per column."""
    print("\n" + "=" * 65)
    print("   🔍  Missing Value Report")
    print("=" * 65)

    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("  ✅  No missing values found!")
    else:
        total_missing = missing.sum()
        total_cells   = df.shape[0] * df.shape[1]

        print(f"  Total missing cells : {total_missing} / {total_cells} "
              f"({total_missing / total_cells * 100:.2f}%)\n")
        print(f"  {'Column':<15} {'Missing':>8}  {'Pct':>6}  Chart")
        print(f"  {divider('─', 55)}")

        for col, count in missing.items():
            pct   = count / len(df) * 100
            chart = "█" * int(pct / 2)
            print(f"  {col:<15} {count:>8}  {pct:>5.1f}%  {chart}")

    print("=" * 65)


def show_highest_value_column(df: pd.DataFrame) -> None:
    """Find and display the numeric column with the highest mean value."""
    print("\n" + "=" * 65)
    print("   🏆  Highest Value Column (by Mean)")
    print("=" * 65)

    numeric_df = df.select_dtypes(include="number").drop(
        columns=["Age"], errors="ignore"
    )
    col_means  = numeric_df.mean().sort_values(ascending=False)
    top_col    = col_means.idxmax()
    top_val    = col_means.max()

    print(f"\n  {'Column':<16} {'Mean':>7}  {'Max':>6}  {'Min':>6}  Bar")
    print(f"  {divider('─', 60)}")

    for col, mean in col_means.items():
        marker = " ◀ HIGHEST" if col == top_col else ""
        b      = bar(mean, max_val=col_means.max(), width=20)
        print(f"  {col:<16} {mean:>7.2f}  "
              f"{df[col].max():>6.2f}  {df[col].min():>6.2f}  {b}{marker}")

    print(f"\n  🥇  Highest Mean Column : {top_col}  ({top_val:.2f} avg)")
    print("=" * 65)


def show_grade_distribution(df: pd.DataFrame) -> None:
    """Show grade and pass/fail distribution."""
    print("\n" + "=" * 65)
    print("   📊  Grade & Pass/Fail Distribution")
    print("=" * 65)

    grade_order = ["A+", "A", "B", "C", "D", "F", "N/A"]
    grade_counts = df["Grade"].value_counts().reindex(grade_order, fill_value=0)

    print(f"\n  {'Grade':<8} {'Count':>6}  {'Pct':>6}  Chart")
    print(f"  {divider('─', 50)}")

    for grade, count in grade_counts.items():
        pct   = count / len(df) * 100
        chart = bar(pct, max_val=100, width=20)
        print(f"  {grade:<8} {count:>6}  {pct:>5.1f}%  {chart}")

    # Pass / Fail
    pass_count = (df["Status"] == "Pass").sum()
    fail_count = (df["Status"] == "Fail").sum()
    print(f"\n  ✅ Pass : {pass_count}  ({pass_count / len(df) * 100:.1f}%)")
    print(f"  ❌ Fail : {fail_count}  ({fail_count / len(df) * 100:.1f}%)")
    print("=" * 65)


def show_five_insights(df: pd.DataFrame) -> None:
    """Compute and display 5 data-driven insights."""
    print("\n" + "=" * 65)
    print("   💡  5 Key Insights from the Dataset")
    print("=" * 65)

    subject_cols = ["Math", "Science", "English", "History", "Computer"]

    # 1. Subject averages
    subj_means  = df[subject_cols].mean().sort_values(ascending=False)
    best_subj   = subj_means.idxmax()
    worst_subj  = subj_means.idxmin()

    # 2. Top performer
    top_idx     = df["Average"].idxmax()
    top_student = df.loc[top_idx, "Student_ID"]
    top_avg     = df.loc[top_idx, "Average"]

    # 3. Study Hours vs Average correlation
    corr = df[["Study_Hours", "Average"]].dropna().corr().loc[
        "Study_Hours", "Average"
    ]

    # 4. Gender performance gap
    gender_avg = df.groupby("Gender")["Average"].mean()

    # 5. Attendance impact
    high_att = df[df["Attendance"] >= 85]["Average"].mean()
    low_att  = df[df["Attendance"] <  85]["Average"].mean()

    insights = [
        (
            "Subject Performance Gap",
            f"'{best_subj}' is the strongest subject (avg {subj_means[best_subj]:.1f}) "
            f"while '{worst_subj}' is weakest (avg {subj_means[worst_subj]:.1f}) — "
            f"a {subj_means[best_subj] - subj_means[worst_subj]:.1f} pt gap."
        ),
        (
            "Top Performer",
            f"{top_student} leads with an average of {top_avg:.2f}, "
            f"earning a Grade {assign_grade(top_avg)}. "
            f"Strong all-round performance across all 5 subjects."
        ),
        (
            "Study Hours → Higher Scores",
            f"Correlation between study hours and average = {corr:.2f}. "
            f"{'Positive' if corr > 0 else 'Negative'} link — students who "
            f"study more tend to score {'higher' if corr > 0 else 'lower'}."
        ),
        (
            "Gender Performance Gap",
            f"{gender_avg.idxmax()} students score higher on average "
            f"({gender_avg.max():.1f} vs {gender_avg.min():.1f}), "
            f"a difference of {abs(gender_avg.max() - gender_avg.min()):.1f} pts."
        ),
        (
            "Attendance Boosts Grades",
            f"Students with ≥85% attendance averaged {high_att:.1f} marks, "
            f"vs {low_att:.1f} for those below 85% — "
            f"a {high_att - low_att:.1f} pt advantage for regular attendees."
        ),
    ]

    for i, (title, detail) in enumerate(insights, 1):
        print(f"\n  {i}. {title}")
        # Word-wrap detail to 58 chars
        words, line = detail.split(), ""
        for word in words:
            if len(line) + len(word) + 1 > 58:
                print(f"     {line}")
                line = word
            else:
                line = (line + " " + word).strip()
        if line:
            print(f"     {line}")

    print("\n" + "=" * 65 + "\n")


# ── Main ────

def main():
    print("\n  Welcome to Dataset Detective!")

    df = build_dataset()

    show_top_rows(df)
    show_dataset_shape(df)
    show_missing_values(df)
    show_highest_value_column(df)
    show_grade_distribution(df)
    show_five_insights(df)


if __name__ == "__main__":
    main()