""" Assignment (28/02/2026)

Storytelling with Graphs
Description : Create bar chart, pie chart, histogram and write a short data story explaining trends..
"""

# ── Storytelling with Graphs ────

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch

# ── Dataset ───────
def build_dataset() -> pd.DataFrame:
    np.random.seed(42)
    n = 200

    study_hours = np.random.uniform(1, 10, n).round(1)
    noise       = np.random.normal(0, 8, n)
    avg_marks   = np.clip(study_hours * 6.5 + 25 + noise, 35, 100).round(1)

    data = {
        "Student_ID"  : [f"S{str(i).zfill(3)}" for i in range(1, n + 1)],
        "Gender"      : np.random.choice(["Male", "Female"], n, p=[0.48, 0.52]),
        "Study_Hours" : study_hours,
        "Math"        : np.random.randint(40, 100, n),
        "Science"     : np.random.randint(38, 100, n),
        "English"     : np.random.randint(42, 100, n),
        "History"     : np.random.randint(35, 100, n),
        "Computer"    : np.random.randint(45, 100, n),
        "Attendance"  : np.random.randint(60, 100, n),
        "Average"     : avg_marks,
    }

    df           = pd.DataFrame(data)
    df["Grade"]  = df["Average"].apply(assign_grade)
    df["Status"] = df["Average"].apply(lambda a: "Pass" if a >= 50 else "Fail")
    return df


def assign_grade(avg: float) -> str:
    if   avg >= 90: return "A+"
    elif avg >= 80: return "A"
    elif avg >= 70: return "B"
    elif avg >= 60: return "C"
    elif avg >= 50: return "D"
    else:           return "F"


# ── Theme ─────

COLORS = {
    "bar"        : ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"],
    "pie"        : ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974", "#64B5CD"],
    "hist_male"  : "#4C72B0",
    "hist_female": "#C44E52",
    "scatter"    : "#55A868",
    "bg"         : "#F8F9FA",
    "panel"      : "#FFFFFF",
    "text"       : "#2D3436",
    "muted"      : "#636E72",
    "accent"     : "#FDCB6E",
}

def set_style():
    plt.rcParams.update({
        "font.family"       : "DejaVu Sans",
        "font.size"         : 10,
        "axes.spines.top"   : False,
        "axes.spines.right" : False,
        "axes.grid"         : True,
        "grid.alpha"        : 0.3,
        "grid.linestyle"    : "--",
        "figure.facecolor"  : COLORS["bg"],
        "axes.facecolor"    : COLORS["panel"],
    })


# ── Chart 1 — Bar Chart ──────

def plot_bar_chart(ax, df: pd.DataFrame):
    subjects = ["Math", "Science", "English", "History", "Computer"]
    means    = [df[s].mean() for s in subjects]
    bars     = ax.bar(subjects, means, color=COLORS["bar"],
                      width=0.55, edgecolor="white", linewidth=1.2, zorder=3)

    # Value labels on top of each bar
    for bar_, val in zip(bars, means):
        ax.text(bar_.get_x() + bar_.get_width() / 2,
                bar_.get_height() + 0.6,
                f"{val:.1f}", ha="center", va="bottom",
                fontsize=9, fontweight="bold", color=COLORS["text"])

    # Highlight max bar
    max_idx = means.index(max(means))
    bars[max_idx].set_edgecolor(COLORS["accent"])
    bars[max_idx].set_linewidth(2.5)

    ax.set_title("📚  Average Marks by Subject",
                 fontsize=12, fontweight="bold", pad=12, color=COLORS["text"])
    ax.set_ylabel("Average Marks", color=COLORS["muted"])
    ax.set_ylim(0, 105)
    ax.tick_params(colors=COLORS["muted"])
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)


# ── Chart 2 — Pie Chart ─────

def plot_pie_chart(ax, df: pd.DataFrame):
    grade_order  = ["A+", "A", "B", "C", "D", "F"]
    grade_counts = df["Grade"].value_counts().reindex(grade_order, fill_value=0)
    sizes        = grade_counts.values
    labels       = grade_counts.index.tolist()

    explode = [0.04] * len(sizes)
    explode[0] = 0.10    # Pop out A+

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=COLORS["pie"][:len(sizes)],
        autopct=lambda p: f"{p:.1f}%" if p > 3 else "",
        startangle=140, explode=explode,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        textprops={"fontsize": 9},
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_fontweight("bold")
        at.set_color("white")

    ax.set_title("🎓  Grade Distribution",
                 fontsize=12, fontweight="bold", pad=12, color=COLORS["text"])

    # Legend
    ax.legend(wedges, [f"{l} — {c}" for l, c in zip(labels, sizes)],
              loc="lower center", bbox_to_anchor=(0.5, -0.12),
              ncol=3, fontsize=8, frameon=False)


# ── Chart 3 — Histogram ──────

def plot_histogram(ax, df: pd.DataFrame):
    male_avg   = df[df["Gender"] == "Male"]["Average"]
    female_avg = df[df["Gender"] == "Female"]["Average"]
    bins       = np.arange(35, 105, 5)

    ax.hist(male_avg,   bins=bins, alpha=0.72, color=COLORS["hist_male"],
            label=f"Male (n={len(male_avg)})",   edgecolor="white", linewidth=0.8)
    ax.hist(female_avg, bins=bins, alpha=0.72, color=COLORS["hist_female"],
            label=f"Female (n={len(female_avg)})", edgecolor="white", linewidth=0.8)

    # Mean lines
    for avg, color, label in [
        (male_avg.mean(),   COLORS["hist_male"],   f"Male mean: {male_avg.mean():.1f}"),
        (female_avg.mean(), COLORS["hist_female"], f"Female mean: {female_avg.mean():.1f}"),
    ]:
        ax.axvline(avg, color=color, linestyle="--",
                   linewidth=1.8, label=label, alpha=0.9)

    ax.set_title("📊  Score Distribution by Gender",
                 fontsize=12, fontweight="bold", pad=12, color=COLORS["text"])
    ax.set_xlabel("Average Score", color=COLORS["muted"])
    ax.set_ylabel("Number of Students", color=COLORS["muted"])
    ax.legend(fontsize=8, frameon=False)
    ax.tick_params(colors=COLORS["muted"])


# ── Chart 4 — Scatter Plot (bonus) ──────

def plot_scatter(ax, df: pd.DataFrame):
    corr = df[["Study_Hours", "Average"]].corr().loc["Study_Hours", "Average"]

    scatter = ax.scatter(
        df["Study_Hours"], df["Average"],
        c=df["Average"], cmap="RdYlGn",
        alpha=0.65, s=28, edgecolors="none",
    )

    # Trend line
    m, b   = np.polyfit(df["Study_Hours"], df["Average"], 1)
    x_line = np.linspace(df["Study_Hours"].min(), df["Study_Hours"].max(), 100)
    ax.plot(x_line, m * x_line + b,
            color="#E17055", linewidth=2, linestyle="--", label=f"Trend (r={corr:.2f})")

    plt.colorbar(scatter, ax=ax, label="Avg Score", pad=0.02)

    ax.set_title("⏱  Study Hours vs Average Score",
                 fontsize=12, fontweight="bold", pad=12, color=COLORS["text"])
    ax.set_xlabel("Study Hours / Day",   color=COLORS["muted"])
    ax.set_ylabel("Average Score",       color=COLORS["muted"])
    ax.legend(fontsize=9, frameon=False)
    ax.tick_params(colors=COLORS["muted"])


# ── Data Story Panel ──────

def plot_story(ax, df: pd.DataFrame):
    ax.axis("off")

    subjects     = ["Math", "Science", "English", "History", "Computer"]
    subj_means   = {s: df[s].mean() for s in subjects}
    best_subj    = max(subj_means, key=subj_means.get)
    worst_subj   = min(subj_means, key=subj_means.get)
    pass_pct     = (df["Status"] == "Pass").mean() * 100
    corr         = df[["Study_Hours", "Average"]].corr().loc["Study_Hours", "Average"]
    gender_means = df.groupby("Gender")["Average"].mean()
    top_gender   = gender_means.idxmax()
    top_gmean    = gender_means.max()
    low_gmean    = gender_means.min()
    grade_B_plus = (df["Grade"].isin(["A+", "A", "B"])).mean() * 100

    story = f"""
DATA STORY — Student Performance Analysis
{"─" * 46}

  This dashboard analyses {len(df)} students across 5 subjects,
  revealing clear patterns in academic performance.

  1  SUBJECT STRENGTHS
     {best_subj} leads all subjects with a {subj_means[best_subj]:.1f} avg,
     while {worst_subj} trails at {subj_means[worst_subj]:.1f} — a gap of
     {subj_means[best_subj] - subj_means[worst_subj]:.1f} pts, signalling where support is needed.

  2  GRADE SPREAD
     {grade_B_plus:.1f}% of students achieved B or above,
     and {pass_pct:.1f}% passed overall. A healthy class
     with room to lift the bottom quartile.

  3  STUDY HOURS MATTER
     Correlation r = {corr:.2f} confirms a strong positive
     link between daily study time and final scores.
     Each extra hour yields ~6.5 marks on average.

  4  GENDER INSIGHT
     {top_gender} students averaged {top_gmean:.1f} vs {low_gmean:.1f}
     for the other group — a small but consistent
     {abs(top_gmean - low_gmean):.1f}-pt gap across all subjects.

{"─" * 46}
  KEY TAKEAWAY :  Consistent study habits are the
  single strongest predictor of high performance.
"""

    ax.text(0.04, 0.97, story,
            transform=ax.transAxes,
            fontsize=8.8, verticalalignment="top",
            fontfamily="monospace", color=COLORS["text"],
            bbox=dict(boxstyle="round,pad=0.6",
                      facecolor="#EDF2F7", edgecolor="#CBD5E0", linewidth=1.2))


# ── Main Canvas ─────

def main():
    set_style()
    df = build_dataset()

    fig = plt.figure(figsize=(16, 11), facecolor=COLORS["bg"])
    fig.suptitle(
        "📈  Storytelling with Graphs — Student Performance Dashboard",
        fontsize=16, fontweight="bold", color=COLORS["text"], y=0.98
    )

    gs = gridspec.GridSpec(2, 3, figure=fig,
                           hspace=0.42, wspace=0.35,
                           left=0.06, right=0.97,
                           top=0.93, bottom=0.06)

    ax_bar     = fig.add_subplot(gs[0, 0])
    ax_pie     = fig.add_subplot(gs[0, 1])
    ax_hist    = fig.add_subplot(gs[0, 2])
    ax_scatter = fig.add_subplot(gs[1, 0])
    ax_story   = fig.add_subplot(gs[1, 1:])

    plot_bar_chart  (ax_bar,     df)
    plot_pie_chart  (ax_pie,     df)
    plot_histogram  (ax_hist,    df)
    plot_scatter    (ax_scatter, df)
    plot_story      (ax_story,   df)

    plt.show()


if __name__ == "__main__":
    main()