""" 
Assignment (03/03/2026)
Assignment Name: Build Your First Dataset
Description: Create a dataset (e.g., study hours vs marks), identify features & labels, predict relationship.

"""

# ── Build Your First Dataset ─────

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats

# ── Dataset Builder ──────

def build_dataset() -> pd.DataFrame:
    """
    Build a realistic Study Hours vs Marks dataset.
    Features  : Study_Hours, Sleep_Hours, Attendance, Prev_Score
    Label     : Final_Marks (target variable to predict)
    """
    np.random.seed(42)
    n = 120

    study_hours = np.round(np.random.uniform(1.0, 10.0, n), 1)
    sleep_hours = np.round(np.random.uniform(4.0,  9.0, n), 1)
    attendance  = np.random.randint(55, 100, n).astype(float)
    prev_score  = np.round(np.random.uniform(35.0, 95.0, n), 1)

    # Label = weighted combination + noise (realistic relationship)
    noise       = np.random.normal(0, 4, n)
    final_marks = np.clip(
        study_hours * 5.2 +
        sleep_hours * 1.8 +
        attendance  * 0.3 +
        prev_score  * 0.25 +
        noise,
        35, 100
    ).round(1)

    df = pd.DataFrame({
        "Student_ID"  : [f"S{str(i).zfill(3)}" for i in range(1, n + 1)],
        "Study_Hours" : study_hours,
        "Sleep_Hours" : sleep_hours,
        "Attendance"  : attendance,
        "Prev_Score"  : prev_score,
        "Final_Marks" : final_marks,
    })

    df["Grade"]  = df["Final_Marks"].apply(assign_grade)
    df["Status"] = df["Final_Marks"].apply(lambda m: "Pass" if m >= 50 else "Fail")
    return df


def assign_grade(marks: float) -> str:
    if   marks >= 90: return "A+"
    elif marks >= 80: return "A"
    elif marks >= 70: return "B"
    elif marks >= 60: return "C"
    elif marks >= 50: return "D"
    else:             return "F"


# ── Simple Linear Regression (from scratch) ──────

def linear_regression(x: np.ndarray, y: np.ndarray) -> dict:
    """
    Compute slope, intercept, R², and predictions manually.
    Formula:  y = mx + b
    """
    n    = len(x)
    x_m  = x.mean()
    y_m  = y.mean()

    # Slope (m) and Intercept (b)
    m    = np.sum((x - x_m) * (y - y_m)) / np.sum((x - x_m) ** 2)
    b    = y_m - m * x_m

    # Predictions
    y_pred = m * x + b

    # R² — goodness of fit
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y_m)    ** 2)
    r2     = 1 - (ss_res / ss_tot)

    # Mean Absolute Error
    mae    = np.mean(np.abs(y - y_pred))

    return {"m": m, "b": b, "r2": r2, "mae": mae, "y_pred": y_pred}


def predict(study_hours: float, model: dict) -> float:
    """Predict final marks for a given number of study hours."""
    return round(model["m"] * study_hours + model["b"], 2)


# ── Correlation Matrix ──────
def compute_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Return Pearson correlation of all numeric features with Final_Marks."""
    numeric_cols = ["Study_Hours", "Sleep_Hours", "Attendance",
                    "Prev_Score", "Final_Marks"]
    return df[numeric_cols].corr()[["Final_Marks"]].drop("Final_Marks").round(3)


# ── Console Report ──────

def print_report(df: pd.DataFrame, model: dict, corr: pd.DataFrame):

    divider = lambda c="─", w=65: c * w

    print("\n" + "=" * 65)
    print("   📦  Build Your First Dataset — Study Hours vs Marks")
    print("=" * 65)

    # ── 1. Dataset preview ─────
    print("\n  👀  Dataset Preview  (first 8 rows)")
    print(f"\n  {'ID':<7} {'Study':>6} {'Sleep':>6} {'Att%':>5} "
          f"{'Prev':>6} {'Final':>6}  {'Grd':>4}  Status")
    print(f"  {divider('─', 58)}")
    for _, row in df.head(8).iterrows():
        print(f"  {row['Student_ID']:<7} {row['Study_Hours']:>6.1f} "
              f"{row['Sleep_Hours']:>6.1f} {row['Attendance']:>5.0f} "
              f"{row['Prev_Score']:>6.1f} {row['Final_Marks']:>6.1f}  "
              f"{row['Grade']:>4}  {row['Status']}")
    print(f"  {divider('─', 58)}")
    print(f"  Total rows: {len(df)}  |  Features: 4  |  Label: Final_Marks")

    # ── 2. Features & Label ──────
    print("\n" + "=" * 65)
    print("  🏷   Features  &  Label")
    print("=" * 65)
    features = [
        ("Study_Hours", "float", "Input", "Daily study time in hours (1–10)"),
        ("Sleep_Hours", "float", "Input", "Nightly sleep duration  (4–9)"),
        ("Attendance",  "int",   "Input", "Class attendance percentage (55–100)"),
        ("Prev_Score",  "float", "Input", "Previous exam score (35–95)"),
        ("Final_Marks", "float", "LABEL", "★ Target variable to predict (35–100)"),
    ]
    print(f"\n  {'Column':<14} {'Type':<7} {'Role':<8}  Description")
    print(f"  {divider('─', 60)}")
    for col, dtype, role, desc in features:
        star = " ◀" if role == "LABEL" else ""
        print(f"  {col:<14} {dtype:<7} {role:<8}  {desc}{star}")

    # ── 3. Descriptive statistics ─────
    print("  📐  Descriptive Statistics")
    print("=" * 65)
    cols = ["Study_Hours", "Sleep_Hours", "Attendance", "Prev_Score", "Final_Marks"]
    print(f"\n  {'Column':<14} {'Mean':>7} {'Median':>7} "
          f"{'Std':>7} {'Min':>6} {'Max':>6}")
    print(f"  {divider('─', 52)}")
    for col in cols:
        s = df[col]
        print(f"  {col:<14} {s.mean():>7.2f} {s.median():>7.2f} "
              f"{s.std():>7.2f} {s.min():>6.1f} {s.max():>6.1f}")

    # ── 4. Correlation ─────
    print("\n" + "=" * 65)
    print("  🔗  Feature Correlation with Final_Marks")
    print("=" * 65)
    print(f"\n  {'Feature':<16} {'Pearson r':>10}  {'Strength':<14}  Bar")
    print(f"  {divider('─', 58)}")
    for feat, row in corr.iterrows():
        r   = row["Final_Marks"]
        abs_r = abs(r)
        strength = ("Very Strong" if abs_r >= 0.8 else
                    "Strong"      if abs_r >= 0.6 else
                    "Moderate"    if abs_r >= 0.4 else
                    "Weak")
        bar  = "█" * int(abs_r * 20)
        sign = "+" if r >= 0 else "-"
        print(f"  {feat:<16} {r:>10.3f}  {strength:<14}  {sign}{bar}")

    # ── 5. Linear Regression model ─────
    print("\n" + "=" * 65)
    print("  📈  Linear Regression — Study Hours → Final Marks")
    print("=" * 65)
    print(f"\n  Model  :  Final_Marks = {model['m']:.2f} × Study_Hours + {model['b']:.2f}")
    print(f"  R²     :  {model['r2']:.4f}  "
          f"({'Excellent' if model['r2'] > 0.8 else 'Good' if model['r2'] > 0.6 else 'Moderate'} fit)")
    print(f"  MAE    :  {model['mae']:.2f} marks  (mean prediction error)")

    # ── 6. Predictions ─────
    print("\n" + "=" * 65)
    print("  🔮  Sample Predictions  (Study Hours → Predicted Marks)")
    print("=" * 65)
    print(f"\n  {'Study Hrs':>10} {'Predicted':>10} {'Grade':>7}  Bar")
    print(f"  {divider('─', 48)}")
    for hrs in [2, 4, 5, 6, 7, 8, 9, 10]:
        pred  = predict(hrs, model)
        grade = assign_grade(pred)
        bar   = "█" * int(pred / 5)
        print(f"  {hrs:>10.1f} {pred:>10.2f} {grade:>7}  {bar}")

    # ── 7. Insights ──────
    top_feat  = corr["Final_Marks"].abs().idxmax()
    top_corr  = corr["Final_Marks"].abs().max()
    pass_rate = (df["Status"] == "Pass").mean() * 100
    avg_study = df["Study_Hours"].mean()
    avg_marks = df["Final_Marks"].mean()

    print("\n" + "=" * 65)
    print("  💡  Key Insights")
    print("=" * 65)
    insights = [
        f"Every +1 study hour adds ~{model['m']:.1f} marks "
        f"(slope of regression line).",
        f"'{top_feat}' is the strongest predictor "
        f"(r = {top_corr:.2f}).",
        f"Average student studies {avg_study:.1f} hrs/day "
        f"and scores {avg_marks:.1f} marks.",
        f"{pass_rate:.1f}% of students passed "
        f"(Final_Marks ≥ 50).",
        f"R² = {model['r2']:.2f} — the model explains "
        f"{model['r2']*100:.0f}% of mark variance.",
    ]
    for i, insight in enumerate(insights, 1):
        print(f"\n  {i}. {insight}")

    print("\n" + "=" * 65 + "\n")


# ── Visualisation ──────
COLORS = {
    "blue"   : "#4C72B0",
    "green"  : "#55A868",
    "red"    : "#C44E52",
    "purple" : "#8172B2",
    "orange" : "#DD8452",
    "bg"     : "#F8F9FA",
    "panel"  : "#FFFFFF",
    "text"   : "#2D3436",
    "muted"  : "#636E72",
    "gold"   : "#FDCB6E",
}

def set_style():
    plt.rcParams.update({
        "font.family"       : "DejaVu Sans",
        "axes.spines.top"   : False,
        "axes.spines.right" : False,
        "axes.grid"         : True,
        "grid.alpha"        : 0.3,
        "grid.linestyle"    : "--",
        "figure.facecolor"  : COLORS["bg"],
        "axes.facecolor"    : COLORS["panel"],
    })


def plot_scatter_regression(ax, df, model):
    """Scatter plot with regression line."""
    x = df["Study_Hours"].values
    y = df["Final_Marks"].values

    ax.scatter(x, y, color=COLORS["blue"], alpha=0.55,
               s=35, edgecolors="white", linewidth=0.5, zorder=3)

    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = model["m"] * x_line + model["b"]
    ax.plot(x_line, y_line, color=COLORS["red"],
            linewidth=2.2, linestyle="--",
            label=f"y = {model['m']:.2f}x + {model['b']:.2f}  (R²={model['r2']:.2f})")

    ax.set_title("📈  Study Hours vs Final Marks",
                 fontweight="bold", fontsize=11, color=COLORS["text"])
    ax.set_xlabel("Study Hours / Day", color=COLORS["muted"])
    ax.set_ylabel("Final Marks",       color=COLORS["muted"])
    ax.legend(fontsize=8, frameon=False)


def plot_correlation_bar(ax, corr):
    """Horizontal bar chart of feature correlations."""
    features = corr.index.tolist()
    values   = corr["Final_Marks"].tolist()
    colors   = [COLORS["green"] if v >= 0 else COLORS["red"] for v in values]

    bars = ax.barh(features, values, color=colors,
                   height=0.5, edgecolor="white", linewidth=0.8)
    for bar_, val in zip(bars, values):
        ax.text(val + 0.01, bar_.get_y() + bar_.get_height() / 2,
                f"{val:.3f}", va="center", fontsize=8.5,
                fontweight="bold", color=COLORS["text"])

    ax.axvline(0, color=COLORS["muted"], linewidth=0.8)
    ax.set_xlim(-0.1, 1.05)
    ax.set_title("🔗  Feature Correlation with Final Marks",
                 fontweight="bold", fontsize=11, color=COLORS["text"])
    ax.set_xlabel("Pearson r", color=COLORS["muted"])


def plot_grade_distribution(ax, df):
    """Bar chart of grade distribution."""
    order  = ["A+", "A", "B", "C", "D", "F"]
    colors = [COLORS["green"], COLORS["blue"], COLORS["purple"],
              COLORS["orange"], COLORS["gold"], COLORS["red"]]
    counts = df["Grade"].value_counts().reindex(order, fill_value=0)

    bars = ax.bar(counts.index, counts.values,
                  color=colors, edgecolor="white",
                  linewidth=1.2, width=0.6)
    for b, v in zip(bars, counts.values):
        ax.text(b.get_x() + b.get_width() / 2,
                b.get_height() + 0.4,
                str(v), ha="center", fontsize=9,
                fontweight="bold", color=COLORS["text"])

    ax.set_title("🎓  Grade Distribution",
                 fontweight="bold", fontsize=11, color=COLORS["text"])
    ax.set_ylabel("Number of Students", color=COLORS["muted"])
    ax.set_ylim(0, counts.max() + 6)


def plot_prediction_line(ax, model):
    """Show predicted marks for study hours 1–10."""
    hours  = np.arange(1, 10.5, 0.5)
    marks  = [predict(h, model) for h in hours]
    colors_map = [
        COLORS["red"]    if m < 50  else
        COLORS["gold"]   if m < 60  else
        COLORS["blue"]   if m < 75  else
        COLORS["green"]
        for m in marks
    ]

    ax.scatter(hours, marks, c=colors_map, s=55,
               zorder=4, edgecolors="white", linewidth=0.6)
    ax.plot(hours, marks, color=COLORS["muted"],
            linewidth=1.4, linestyle="-", alpha=0.5, zorder=3)
    ax.axhline(50, color=COLORS["red"],   linestyle=":", linewidth=1.2,
               label="Pass line (50)")
    ax.axhline(80, color=COLORS["green"], linestyle=":", linewidth=1.2,
               label="Distinction (80)")

    ax.set_title("🔮  Predicted Marks vs Study Hours",
                 fontweight="bold", fontsize=11, color=COLORS["text"])
    ax.set_xlabel("Study Hours / Day", color=COLORS["muted"])
    ax.set_ylabel("Predicted Final Marks", color=COLORS["muted"])
    ax.legend(fontsize=8, frameon=False)
    ax.set_ylim(30, 105)


def plot_feature_vs_marks(ax, df):
    """Scatter: Attendance vs Final Marks, sized by Study Hours."""
    sc = ax.scatter(
        df["Attendance"], df["Final_Marks"],
        c=df["Study_Hours"], cmap="RdYlGn",
        s=df["Study_Hours"] * 7,
        alpha=0.6, edgecolors="white", linewidth=0.4
    )
    plt.colorbar(sc, ax=ax, label="Study Hours", pad=0.02)
    ax.set_title("🏫  Attendance vs Final Marks\n(size & colour = Study Hours)",
                 fontweight="bold", fontsize=10, color=COLORS["text"])
    ax.set_xlabel("Attendance %",   color=COLORS["muted"])
    ax.set_ylabel("Final Marks",    color=COLORS["muted"])


def plot_histogram(ax, df):
    """Distribution of Final Marks."""
    ax.hist(df["Final_Marks"], bins=15, color=COLORS["blue"],
            edgecolor="white", linewidth=0.8, alpha=0.85)
    ax.axvline(df["Final_Marks"].mean(), color=COLORS["red"],
               linestyle="--", linewidth=2,
               label=f"Mean: {df['Final_Marks'].mean():.1f}")
    ax.axvline(df["Final_Marks"].median(), color=COLORS["gold"],
               linestyle="--", linewidth=2,
               label=f"Median: {df['Final_Marks'].median():.1f}")
    ax.set_title("📊  Final Marks Distribution",
                 fontweight="bold", fontsize=11, color=COLORS["text"])
    ax.set_xlabel("Final Marks",          color=COLORS["muted"])
    ax.set_ylabel("Number of Students",   color=COLORS["muted"])
    ax.legend(fontsize=8, frameon=False)


def build_dashboard(df, model, corr):
    set_style()

    fig = plt.figure(figsize=(17, 11), facecolor=COLORS["bg"])
    fig.suptitle(
        "📚  Build Your First Dataset — Study Hours vs Marks",
        fontsize=15, fontweight="bold",
        color=COLORS["text"], y=0.98
    )

    gs = gridspec.GridSpec(
        2, 3, figure=fig,
        hspace=0.42, wspace=0.35,
        left=0.06, right=0.97,
        top=0.93, bottom=0.06
    )

    plot_scatter_regression (fig.add_subplot(gs[0, 0]), df, model)
    plot_correlation_bar    (fig.add_subplot(gs[0, 1]), corr)
    plot_grade_distribution (fig.add_subplot(gs[0, 2]), df)
    plot_prediction_line    (fig.add_subplot(gs[1, 0]), model)
    plot_feature_vs_marks   (fig.add_subplot(gs[1, 1]), df)
    plot_histogram          (fig.add_subplot(gs[1, 2]), df)

    plt.savefig("first_dataset.png", dpi=150,
                bbox_inches="tight", facecolor=COLORS["bg"])
    print("  ✅  Dashboard saved → first_dataset.png\n")
    plt.show()


# ── Main ────

def main():
    print("\n  Welcome to — Build Your First Dataset!\n")

    df    = build_dataset()
    x     = df["Study_Hours"].values
    y     = df["Final_Marks"].values
    model = linear_regression(x, y)
    corr  = compute_correlations(df)

    print_report(df, model, corr)
    build_dashboard(df, model, corr)


if __name__ == "__main__":
    main()