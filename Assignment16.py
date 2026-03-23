""" 
Assignment (18/03/2026)
Assignment Name : Customer Segmentation
Description : Perform K-Means clustering on a mall dataset and describe customer groups.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────
# 1. CREATE MALL CUSTOMER DATASET
# ─────────────────────────────────────────────────────
np.random.seed(42)

n = 200
customer_ids = np.arange(1, n + 1)
genders      = np.random.choice(["Male", "Female"], n, p=[0.44, 0.56])
ages         = np.concatenate([
    np.random.randint(18, 35, 80),   # young adults
    np.random.randint(30, 55, 80),   # middle-aged
    np.random.randint(50, 70, 40),   # older adults
])
np.random.shuffle(ages)

# Annual Income (k$) — 5 natural groups
income = np.concatenate([
    np.random.normal(20,  5,  40),   # low income
    np.random.normal(40,  6,  40),   # lower-mid
    np.random.normal(60,  8,  40),   # mid
    np.random.normal(80,  7,  40),   # upper-mid
    np.random.normal(100, 8,  40),   # high
])
np.random.shuffle(income)
income = np.clip(income, 10, 140).astype(int)

# Spending Score (1–100) — correlated loosely with income segments
spending = np.concatenate([
    np.random.normal(20,  8,  40),   # careful spenders
    np.random.normal(50, 12,  40),   # moderate
    np.random.normal(80,  8,  40),   # big spenders
    np.random.normal(30,  8,  40),   # high income, low spend
    np.random.normal(70,  8,  40),   # high income, high spend
])
np.random.shuffle(spending)
spending = np.clip(spending, 1, 100).astype(int)

df = pd.DataFrame({
    "CustomerID"    : customer_ids,
    "Gender"        : genders,
    "Age"           : ages,
    "AnnualIncome"  : income,
    "SpendingScore" : spending,
})

print("=" * 58)
print("   CUSTOMER SEGMENTATION — K-Means Clustering")
print("=" * 58)
print(f"\n📋 Dataset Shape : {df.shape}")
print(f"\n{df.head(8).to_string(index=False)}")
print(f"\n📊 Basic Statistics:\n{df[['Age','AnnualIncome','SpendingScore']].describe().round(1)}")

# ─────────────────────────────────────────────────────
# 2. FEATURE SELECTION & SCALING
# ─────────────────────────────────────────────────────
features = ["AnnualIncome", "SpendingScore"]
X = df[features].values

scaler   = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ─────────────────────────────────────────────────────
# 3. ELBOW METHOD — Find Optimal K
# ─────────────────────────────────────────────────────
inertias    = []
sil_scores  = []
K_range     = range(2, 11)

for k in K_range:
    km  = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, km.labels_))

optimal_k = 5   # classic mall segmentation answer

# ─────────────────────────────────────────────────────
# 4. FINAL K-MEANS MODEL (k=5)
# ─────────────────────────────────────────────────────
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X_scaled)

# Map cluster labels to descriptive names
centers_orig = scaler.inverse_transform(kmeans.cluster_centers_)
cluster_df   = pd.DataFrame(centers_orig, columns=["Income_C", "Spending_C"])
cluster_df["Cluster"] = range(optimal_k)
cluster_df.sort_values("Income_C", inplace=True)

# Auto-label by income × spending quadrant
def label_cluster(inc, spen):
    if inc < 50 and spen < 50:   return ("💰 Low Income\nLow Spender",    "#FF6B6B")
    if inc < 50 and spen >= 50:  return ("🛍️ Low Income\nHigh Spender",   "#FFA07A")
    if inc >= 50 and spen < 50:  return ("💼 High Income\nLow Spender",   "#4ECDC4")
    if inc >= 50 and spen >= 50: return ("👑 High Income\nHigh Spender",  "#45B7D1")
    return ("📊 Average\nCustomer",  "#96CEB4")

label_map  = {}
color_map  = {}
used_labels = set()

# Sort centers for stable assignment
center_income   = centers_orig[:, 0]
center_spending = centers_orig[:, 1]

# Assign names to each cluster index
segment_info = {
    0: ("💰 Careful\nSpenders",    "#FF6B6B", "Low income, low spending — budget-conscious shoppers"),
    1: ("🛍️ Impulsive\nBuyers",    "#FF9F43", "Low income but high spending — spontaneous shoppers"),
    2: ("📊 Standard\nCustomers",  "#A29BFE", "Mid income, mid spending — average mall-goers"),
    3: ("💼 Conservative\nRich",   "#00CEC9", "High income, low spending — selective, quality buyers"),
    4: ("👑 Target\nCustomers",    "#FDCB6E", "High income, high spending — most valuable customers"),
}

# Sort clusters by income center for consistent labelling
sorted_idx = np.argsort(center_income)
for rank, cidx in enumerate(sorted_idx):
    label_map[cidx] = segment_info[rank][0]
    color_map[cidx] = segment_info[rank][1]

df["Segment"]      = df["Cluster"].map(label_map)
df["SegmentColor"] = df["Cluster"].map(color_map)

# ─────────────────────────────────────────────────────
# 5. CLUSTER SUMMARY
# ─────────────────────────────────────────────────────
print("\n\n📌 CLUSTER SUMMARY")
print("─" * 58)
summary = df.groupby("Cluster").agg(
    Count        =("CustomerID",   "count"),
    Avg_Age      =("Age",          "mean"),
    Avg_Income   =("AnnualIncome", "mean"),
    Avg_Spending =("SpendingScore","mean"),
    Segment      =("Segment",      "first"),
).round(1)
print(summary.to_string())

# ─────────────────────────────────────────────────────
# 6. VISUALISATION — 4-panel dashboard
# ─────────────────────────────────────────────────────
BG  = "#0F0F1A"
FG  = "#E8E8F0"
GRID= "#2A2A3E"

fig = plt.figure(figsize=(18, 13), facecolor=BG)
fig.suptitle(
    "Mall Customer Segmentation  ·  K-Means Clustering (k = 5)",
    fontsize=17, fontweight="bold", color=FG, y=0.98
)

gs = GridSpec(2, 3, figure=fig, hspace=0.38, wspace=0.32,
              left=0.06, right=0.97, top=0.93, bottom=0.07)

colors = [color_map[i] for i in range(optimal_k)]

# ── Panel 1: Elbow Curve ──────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(BG)
ax1.plot(K_range, inertias, "o-", color="#A29BFE", lw=2.5,
         markersize=7, markerfacecolor="#FDCB6E", markeredgecolor="#FDCB6E")
ax1.axvline(optimal_k, color="#FF6B6B", lw=1.8, ls="--", alpha=0.8)
ax1.text(optimal_k + 0.15, max(inertias)*0.85, f"  k = {optimal_k}\n  optimal",
         color="#FF6B6B", fontsize=9)
ax1.set_title("Elbow Method", color=FG, fontsize=11, fontweight="bold")
ax1.set_xlabel("Number of Clusters (k)", color=FG, fontsize=9)
ax1.set_ylabel("Inertia (WCSS)", color=FG, fontsize=9)
ax1.tick_params(colors=FG)
for spine in ax1.spines.values(): spine.set_edgecolor(GRID)
ax1.set_facecolor(BG)

# ── Panel 2: Silhouette Scores ────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(BG)
bar_colors = ["#FF6B6B" if k == optimal_k else "#4ECDC4" for k in K_range]
ax2.bar(K_range, sil_scores, color=bar_colors, edgecolor=BG, linewidth=0.5)
ax2.set_title("Silhouette Score per k", color=FG, fontsize=11, fontweight="bold")
ax2.set_xlabel("Number of Clusters (k)", color=FG, fontsize=9)
ax2.set_ylabel("Silhouette Score", color=FG, fontsize=9)
ax2.tick_params(colors=FG)
for spine in ax2.spines.values(): spine.set_edgecolor(GRID)

# ── Panel 3: Age Distribution per Cluster ────────
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor(BG)
for cid in range(optimal_k):
    ages_c = df[df["Cluster"] == cid]["Age"]
    ax3.hist(ages_c, bins=10, alpha=0.65, color=color_map[cid],
             edgecolor="none", label=f"C{cid}")
ax3.set_title("Age Distribution by Cluster", color=FG, fontsize=11, fontweight="bold")
ax3.set_xlabel("Age", color=FG, fontsize=9)
ax3.set_ylabel("Count", color=FG, fontsize=9)
ax3.tick_params(colors=FG)
for spine in ax3.spines.values(): spine.set_edgecolor(GRID)
ax3.legend(fontsize=8, labelcolor=FG, facecolor=GRID, edgecolor="none")

# ── Panel 4 (main): Cluster Scatter Plot ─────────
ax4 = fig.add_subplot(gs[1, :2])
ax4.set_facecolor(BG)

for cid in range(optimal_k):
    mask = df["Cluster"] == cid
    ax4.scatter(
        df.loc[mask, "AnnualIncome"],
        df.loc[mask, "SpendingScore"],
        c=color_map[cid], s=65, alpha=0.82,
        edgecolors="white", linewidths=0.3,
        label=label_map[cid].replace("\n", " ")
    )

# Plot centroids
cx = scaler.inverse_transform(kmeans.cluster_centers_)[:, 0]
cy = scaler.inverse_transform(kmeans.cluster_centers_)[:, 1]
ax4.scatter(cx, cy, c="white", s=200, marker="*",
            edgecolors="#222", linewidths=0.8, zorder=5, label="Centroid ★")

ax4.set_title("Annual Income vs Spending Score — Customer Clusters",
              color=FG, fontsize=12, fontweight="bold")
ax4.set_xlabel("Annual Income (k$)", color=FG, fontsize=10)
ax4.set_ylabel("Spending Score (1–100)", color=FG, fontsize=10)
ax4.tick_params(colors=FG)
for spine in ax4.spines.values(): spine.set_edgecolor(GRID)
ax4.legend(fontsize=8.5, labelcolor=FG, facecolor=GRID,
           edgecolor="none", loc="upper left", ncol=2)

# ── Panel 5: Segment Cards ────────────────────────
ax5 = fig.add_subplot(gs[1, 2])
ax5.set_facecolor(BG)
ax5.axis("off")
ax5.set_title("Customer Segments", color=FG, fontsize=11, fontweight="bold")

descriptions = [
    ("💰 Careful Spenders",   "Low income · Low spend\nBudget-conscious shoppers"),
    ("🛍️ Impulsive Buyers",   "Low income · High spend\nSpontaneous, trend-driven"),
    ("📊 Standard Customers", "Mid income · Mid spend\nTypical mall visitors"),
    ("💼 Conservative Rich",  "High income · Low spend\nSelective, quality-focused"),
    ("👑 Target Customers",   "High income · High spend\nMost valuable segment"),
]

sorted_colors = [color_map[i] for i in np.argsort(center_income)]

for i, ((title, desc), col) in enumerate(zip(descriptions, sorted_colors)):
    y_pos = 0.92 - i * 0.19
    rect = mpatches.FancyBboxPatch(
        (0.01, y_pos - 0.06), 0.98, 0.15,
        boxstyle="round,pad=0.01",
        facecolor=col + "30", edgecolor=col,
        linewidth=1.2, transform=ax5.transAxes
    )
    ax5.add_patch(rect)
    ax5.text(0.06, y_pos + 0.035, title, transform=ax5.transAxes,
             fontsize=8.5, fontweight="bold", color=col, va="center")
    ax5.text(0.06, y_pos - 0.025, desc, transform=ax5.transAxes,
             fontsize=7.5, color=FG, va="center", alpha=0.85)

plt.savefig("/mnt/user-data/outputs/customer_segmentation.png",
            dpi=150, bbox_inches="tight", facecolor=BG)
print("\n✅ Plot saved → customer_segmentation.png")
plt.show()

# ─────────────────────────────────────────────────────
# 7. SAVE SEGMENTED DATA TO CSV
# ─────────────────────────────────────────────────────
df_out = df[["CustomerID","Gender","Age","AnnualIncome","SpendingScore","Cluster","Segment"]]
df_out.to_csv("/mnt/user-data/outputs/customer_segments.csv", index=False)
print("✅ Data  saved → customer_segments.csv")

print("\n── Final Segment Counts ──────────────────────────")
print(df.groupby("Segment")["CustomerID"].count().to_string())