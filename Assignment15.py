"""Assignment (12/03/2026)
Assignment Name : Decision Tree on Paper
Description : Draw a decision tree predicting whether you should play outside.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn import tree

# ─────────────────────────────────────────────
# 1. DATASET
# ─────────────────────────────────────────────
# Features: [Weather(0=Sunny,1=Cloudy,2=Rainy), Wind(0=Low,1=High), Temperature(0=Cold,1=Warm,2=Hot)]
# Label   : 1 = Play Outside, 0 = Stay Inside

data = [
    # Weather, Wind, Temperature → Play?
    [0, 0, 1],  # Sunny, Low Wind, Warm  → YES
    [0, 0, 2],  # Sunny, Low Wind, Hot   → YES
    [0, 1, 2],  # Sunny, High Wind, Hot  → NO
    [0, 0, 0],  # Sunny, Low Wind, Cold  → NO
    [1, 0, 1],  # Cloudy, Low Wind, Warm → YES
    [1, 1, 1],  # Cloudy, High Wind, Warm→ NO
    [1, 0, 2],  # Cloudy, Low Wind, Hot  → YES
    [1, 1, 0],  # Cloudy, High Wind, Cold→ NO
    [2, 0, 1],  # Rainy, Low Wind, Warm  → NO
    [2, 0, 2],  # Rainy, Low Wind, Hot   → NO
    [2, 1, 1],  # Rainy, High Wind, Warm → NO
    [0, 0, 1],  # Sunny, Low Wind, Warm  → YES (repeat)
    [1, 0, 0],  # Cloudy, Low Wind, Cold → NO
    [0, 1, 1],  # Sunny, High Wind, Warm → YES
]

labels = [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1]

feature_names = ["Weather", "Wind", "Temperature"]
class_names   = ["Stay Inside", "Play Outside"]

X = np.array(data)
y = np.array(labels)

# ─────────────────────────────────────────────
# 2. TRAIN DECISION TREE
# ─────────────────────────────────────────────
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X, y)

# Print text representation
print("=" * 55)
print("   DECISION TREE — Should I Play Outside?")
print("=" * 55)
print(export_text(clf, feature_names=feature_names))

# ─────────────────────────────────────────────
# 3. VISUALISE — "On Paper" Style
# ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
fig.patch.set_facecolor("#FFFDF5")       # warm paper background

# ── Left: sklearn tree plot ──────────────────
ax1 = axes[0]
ax1.set_facecolor("#FFFDF5")
tree.plot_tree(
    clf,
    feature_names=feature_names,
    class_names=class_names,
    filled=True,
    rounded=True,
    fontsize=10,
    ax=ax1,
    impurity=False,
    precision=2,
)
ax1.set_title(
    "sklearn Decision Tree\n(Should I Play Outside?)",
    fontsize=13, fontweight="bold", pad=14,
    color="#2C2C2C"
)

# ── Right: Hand-drawn "on-paper" diagram ─────
ax2 = axes[1]
ax2.set_facecolor("#FFFDF5")
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")
ax2.set_title(
    "Hand-Drawn Style Decision Tree",
    fontsize=13, fontweight="bold", pad=14,
    color="#2C2C2C"
)

# Colour palette
C_DECISION = "#D4E8FF"   # blue — decision nodes
C_YES      = "#C8F0C8"   # green — play outside
C_NO       = "#FFD6D6"   # red   — stay inside
C_BORDER   = "#444444"
C_TEXT     = "#1A1A1A"
C_ARROW    = "#555555"

def draw_node(ax, x, y, text, color, w=1.8, h=0.55, fs=8.5):
    box = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.08",
        facecolor=color, edgecolor=C_BORDER, linewidth=1.5,
        zorder=3
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fs, color=C_TEXT, fontweight="bold",
            zorder=4, wrap=True,
            fontfamily="DejaVu Sans")

def arrow(ax, x1, y1, x2, y2, label="", side="left"):
    ax.annotate(
        "", xy=(x2, y2 + 0.27), xytext=(x1, y1 - 0.27),
        arrowprops=dict(arrowstyle="-|>", color=C_ARROW,
                        lw=1.4, connectionstyle="arc3,rad=0.0"),
        zorder=2
    )
    mx, my = (x1+x2)/2, (y1+y2)/2
    offset = -0.35 if side == "left" else 0.35
    ax.text(mx + offset, my, label, fontsize=7.5,
            color="#555", ha="center", va="center", style="italic")

# ── Tree structure (manually laid out) ───────
# Level 0 — root
draw_node(ax2, 5, 9.0, "Weather?", C_DECISION, w=2.0)

# Level 1
draw_node(ax2, 2.2, 7.2, "Wind?", C_DECISION)          # Sunny branch
draw_node(ax2, 5.0, 7.2, "Wind?", C_DECISION)          # Cloudy branch
draw_node(ax2, 7.8, 7.2, "🌧 Rainy", C_NO, w=2.0)     # Rainy → NO

# Arrows L0 → L1
arrow(ax2, 5, 9.0, 2.2, 7.2, "Sunny",  "left")
arrow(ax2, 5, 9.0, 5.0, 7.2, "Cloudy", "left")
arrow(ax2, 5, 9.0, 7.8, 7.2, "Rainy",  "right")

# Level 2 — Sunny branch
draw_node(ax2, 1.0, 5.4, "Temp?", C_DECISION)
draw_node(ax2, 3.4, 5.4, "Temp?", C_DECISION)

arrow(ax2, 2.2, 7.2, 1.0, 5.4, "Low",  "left")
arrow(ax2, 2.2, 7.2, 3.4, 5.4, "High", "right")

# Level 2 — Cloudy branch
draw_node(ax2, 4.2, 5.4, "Temp?", C_DECISION)
draw_node(ax2, 5.9, 5.4, "✖ No", C_NO)

arrow(ax2, 5.0, 7.2, 4.2, 5.4, "Low",  "left")
arrow(ax2, 5.0, 7.2, 5.9, 5.4, "High", "right")

# Level 3 — Sunny+Low Wind
draw_node(ax2, 0.4, 3.7, "✖ Cold\nStay In", C_NO,  w=1.5, h=0.65)
draw_node(ax2, 1.6, 3.7, "✔ Warm\nPlay!", C_YES, w=1.5, h=0.65)

arrow(ax2, 1.0, 5.4, 0.4, 3.7, "Cold",  "left")
arrow(ax2, 1.0, 5.4, 1.6, 3.7, "Warm/Hot", "right")

# Level 3 — Sunny+High Wind
draw_node(ax2, 2.8, 3.7, "✔ Play!", C_YES, w=1.4)
draw_node(ax2, 4.0, 3.7, "✖ No",   C_NO,  w=1.4)

arrow(ax2, 3.4, 5.4, 2.8, 3.7, "Warm", "left")
arrow(ax2, 3.4, 5.4, 4.0, 3.7, "Hot",  "right")

# Level 3 — Cloudy+Low
draw_node(ax2, 3.7, 3.7, "✔ Play!", C_YES, w=1.4)
draw_node(ax2, 4.8, 3.7, "✖ Cold", C_NO,  w=1.4)

arrow(ax2, 4.2, 5.4, 3.7, 3.7, "Warm/Hot", "left")
arrow(ax2, 4.2, 5.4, 4.8, 3.7, "Cold",     "right")

# Rainy leaf (already at level 1)
draw_node(ax2, 7.8, 5.6, "✖ Stay Inside", C_NO, w=2.0)
arrow(ax2, 7.8, 7.2, 7.8, 5.6, "Always", "right")

# Legend
legend_patches = [
    mpatches.Patch(facecolor=C_DECISION, edgecolor=C_BORDER, label="Decision Node"),
    mpatches.Patch(facecolor=C_YES,      edgecolor=C_BORDER, label="▶ Play Outside"),
    mpatches.Patch(facecolor=C_NO,       edgecolor=C_BORDER, label="▶ Stay Inside"),
]
ax2.legend(handles=legend_patches, loc="lower right",
           fontsize=8, framealpha=0.8, edgecolor="#bbb")

# ── Final styling ─────────────────────────────
plt.suptitle(
    "Decision Tree: Should I Play Outside?",
    fontsize=16, fontweight="bold", color="#1A1A1A", y=1.01
)
plt.tight_layout(pad=2.0)

out_path = "/mnt/user-data/outputs/decision_tree_play_outside.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="#FFFDF5")
print(f"\n✅ Diagram saved → {out_path}")
plt.show()

# ─────────────────────────────────────────────
# 4. QUICK PREDICTION DEMO
# ─────────────────────────────────────────────
print("\n── Sample Predictions ──────────────────────")
test_cases = [
    ([0, 0, 1], "Sunny, Low Wind, Warm"),
    ([2, 1, 1], "Rainy, High Wind, Warm"),
    ([1, 0, 2], "Cloudy, Low Wind, Hot"),
    ([0, 0, 0], "Sunny, Low Wind, Cold"),
]
for features, desc in test_cases:
    pred = clf.predict([features])[0]
    label = class_names[pred]
    icon  = "✔" if pred == 1 else "✖"
    print(f"  {icon}  {desc:35s} → {label}")