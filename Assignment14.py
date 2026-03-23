"""Assignment (11/03/2026)
Assignment Name: Customer Segmentation
Description: Perform K-Means clustering on a mall dataset and describe customer groups.
"""

# ============================================================
# ASSIGNMENT: Customer Segmentation
# Date: 11/03/2026
# Model: K-Means Clustering
# Dataset: Mall Customers (simulated)
# ============================================================

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# ============================================================
# STEP 1: DATASET (Simulated Mall Customer Data)
# ============================================================

np.random.seed(42)

data = {
    "CustomerID": range(1, 51),
    "Age": [
        22, 25, 19, 35, 45, 52, 60, 38, 29, 31,
        48, 55, 23, 27, 40, 62, 33, 21, 50, 44,
        26, 30, 58, 36, 24, 47, 53, 28, 41, 39,
        20, 34, 49, 57, 32, 46, 18, 37, 51, 43,
        23, 29, 55, 38, 42, 61, 27, 33, 48, 35
    ],
    "Annual_Income_k": [
        15, 18, 20, 55, 60, 75, 80, 58, 25, 30,
        70, 78, 17, 22, 62, 85, 45, 16, 72, 65,
        19, 28, 82, 50, 21, 68, 77, 24, 63, 57,
        14, 48, 73, 80, 42, 66, 12, 53, 76, 61,
        18, 27, 79, 55, 64, 88, 23, 46, 71, 52
    ],
    "Spending_Score": [
        80, 75, 85, 50, 45, 20, 15, 55, 78, 70,
        30, 18, 82, 72, 48, 12, 60, 88, 25, 40,
        77, 65, 10, 52, 83, 35, 22, 68, 43, 58,
        90, 56, 28, 14, 62, 38, 92, 47, 20, 44,
        79, 71, 16, 53, 41, 08, 74, 59, 32, 49
    ],
    "Gender": [
        "F","M","F","M","F","M","F","M","F","M",
        "F","M","F","M","F","M","F","M","F","M",
        "F","M","F","M","F","M","F","M","F","M",
        "F","M","F","M","F","M","F","M","F","M",
        "F","M","F","M","F","M","F","M","F","M",
    ]
}

df = pd.DataFrame(data)

print("=" * 65)
print("MALL CUSTOMER DATASET")
print("=" * 65)
print(f"Total Customers  : {len(df)}")
print(f"Features         : Age, Annual Income, Spending Score, Gender")
print()
print(df.to_string(index=False))
print()

# ============================================================
# STEP 2: EXPLORATORY DATA ANALYSIS
# ============================================================

print("=" * 65)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 65)

print("\nBasic Statistics:")
print(df[["Age", "Annual_Income_k", "Spending_Score"]].describe().round(2).to_string())
print()

print(f"Gender Distribution:")
print(df["Gender"].value_counts().to_string())
print()

print(f"Age Groups:")
bins   = [0, 25, 35, 45, 60, 100]
labels = ["18-25", "26-35", "36-45", "46-60", "60+"]
df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels)
print(df["Age_Group"].value_counts().sort_index().to_string())
print()

# ============================================================
# STEP 3: FEATURE SELECTION & SCALING
# ============================================================

print("=" * 65)
print("FEATURE SCALING (StandardScaler)")
print("=" * 65)

features       = ["Age", "Annual_Income_k", "Spending_Score"]
X              = df[features].values
scaler         = StandardScaler()
X_scaled       = scaler.fit_transform(X)

print(f"Features used : {features}")
print(f"Scaling method: StandardScaler (mean=0, std=1)")
print()
print("Before Scaling (first 5 rows):")
print(pd.DataFrame(X[:5], columns=features).round(2).to_string(index=False))
print()
print("After Scaling (first 5 rows):")
print(pd.DataFrame(X_scaled[:5], columns=features).round(4).to_string(index=False))
print()

# ============================================================
# STEP 4: FIND OPTIMAL K (ELBOW METHOD)
# ============================================================

print("=" * 65)
print("ELBOW METHOD — FINDING OPTIMAL K")
print("=" * 65)

inertia_vals    = []
silhouette_vals = []
k_range         = range(2, 9)

for k in k_range:
    km  = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertia_vals.append(km.inertia_)
    sil = silhouette_score(X_scaled, km.labels_)
    silhouette_vals.append(sil)

print(f"{'K':<5} {'Inertia':>12} {'Silhouette Score':>18} {'Recommendation'}")
print("-" * 55)
best_k = k_range.start + silhouette_vals.index(max(silhouette_vals))
for i, k in enumerate(k_range):
    tag = "<-- BEST" if k == best_k else ""
    print(f"{k:<5} {inertia_vals[i]:>12.2f} {silhouette_vals[i]:>18.4f}  {tag}")

print(f"\nOptimal K selected : {best_k} (highest silhouette score)")
print()

# ============================================================
# STEP 5: TRAIN FINAL K-MEANS MODEL
# ============================================================

print("=" * 65)
print(f"K-MEANS CLUSTERING  (K = {best_k})")
print("=" * 65)

kmeans         = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df["Cluster"]  = kmeans.fit_predict(X_scaled)

centers_scaled = kmeans.cluster_centers_
centers_orig   = scaler.inverse_transform(centers_scaled)

print(f"Final Inertia      : {kmeans.inertia_:.4f}")
print(f"Silhouette Score   : {silhouette_score(X_scaled, df['Cluster']):.4f}")
print()

print("Cluster Centroids (original scale):")
print(f"{'Cluster':<10} {'Avg Age':>10} {'Avg Income (k)':>16} {'Avg Spending':>14}")
print("-" * 55)
for i, c in enumerate(centers_orig):
    print(f"Cluster {i:<3} {c[0]:>10.1f} {c[1]:>16.1f} {c[2]:>14.1f}")
print()

# ============================================================
# STEP 6: CLUSTER ANALYSIS & CUSTOMER PROFILES
# ============================================================

print("=" * 65)
print("CLUSTER ANALYSIS — CUSTOMER GROUP PROFILES")
print("=" * 65)

cluster_stats = df.groupby("Cluster")[features].mean().round(1)
cluster_stats["Count"]          = df.groupby("Cluster").size()
cluster_stats["Female_%"]       = (
    df[df["Gender"] == "F"].groupby("Cluster").size() /
    df.groupby("Cluster").size() * 100
).round(1)

print(cluster_stats.to_string())
print()

# Human-readable segment labels based on income vs spending
segment_labels = {}
for i, c in enumerate(centers_orig):
    age     = c[0]
    income  = c[1]
    spend   = c[2]

    if income >= 60 and spend >= 55:
        label = "HIGH INCOME  | HIGH SPENDERS  — Premium Customers"
    elif income >= 60 and spend < 40:
        label = "HIGH INCOME  | LOW SPENDERS   — Careful Savers"
    elif income < 40 and spend >= 60:
        label = "LOW INCOME   | HIGH SPENDERS  — Impulsive Buyers"
    elif income < 40 and spend < 40:
        label = "LOW INCOME   | LOW SPENDERS   — Budget Shoppers"
    else:
        label = "AVERAGE INCOME | AVERAGE SPEND — Typical Customers"

    segment_labels[i] = label

print("Segment Descriptions:")
print("-" * 65)
for cluster_id, label in segment_labels.items():
    count = cluster_stats.loc[cluster_id, "Count"]
    print(f"  Cluster {cluster_id} ({count:>2} customers) : {label}")

print()

# ============================================================
# STEP 7: DETAILED CUSTOMER GROUP DESCRIPTION
# ============================================================

print("=" * 65)
print("DETAILED CUSTOMER GROUP DESCRIPTIONS")
print("=" * 65)

descriptions = {
    "HIGH INCOME  | HIGH SPENDERS  — Premium Customers": {
        "profile"  : "Young-to-middle-aged, high earners who love to spend.",
        "behavior" : "Buys premium brands, responds to luxury promotions.",
        "strategy" : "Offer loyalty rewards, exclusive memberships, VIP deals.",
    },
    "HIGH INCOME  | LOW SPENDERS   — Careful Savers": {
        "profile"  : "Older, high-earning customers with conservative spending.",
        "behavior" : "Shops selectively; prefers value-for-money over impulse.",
        "strategy" : "Target with investment products, quality over quantity.",
    },
    "LOW INCOME   | HIGH SPENDERS  — Impulsive Buyers": {
        "profile"  : "Young customers with modest income but high spending score.",
        "behavior" : "Emotionally driven purchases; responds to discounts & FOMO.",
        "strategy" : "Flash sales, EMI offers, limited-time deals work best.",
    },
    "LOW INCOME   | LOW SPENDERS   — Budget Shoppers": {
        "profile"  : "Older customers with low income and minimal spending.",
        "behavior" : "Buys only essentials; very price-sensitive.",
        "strategy" : "Bulk deals, combo offers, everyday low-price campaigns.",
    },
    "AVERAGE INCOME | AVERAGE SPEND — Typical Customers": {
        "profile"  : "Middle-aged, middle-income customers — the core segment.",
        "behavior" : "Balanced shoppers; responds to moderate discounts.",
        "strategy" : "Seasonal promotions, referral programs, bundle offers.",
    },
}

for cluster_id, label in segment_labels.items():
    desc = descriptions.get(label, {})
    print(f"Cluster {cluster_id}: {label}")
    if desc:
        print(f"  Profile   : {desc['profile']}")
        print(f"  Behavior  : {desc['behavior']}")
        print(f"  Strategy  : {desc['strategy']}")
    print()

# ============================================================
# STEP 8: ASSIGN LABELS TO FULL DATASET
# ============================================================

print("=" * 65)
print("FINAL LABELED DATASET (First 20 Customers)")
print("=" * 65)

df["Segment"] = df["Cluster"].map(
    {k: v.split("—")[-1].strip() for k, v in segment_labels.items()}
)

print(df[["CustomerID", "Age", "Annual_Income_k",
          "Spending_Score", "Gender", "Cluster", "Segment"]]
      .head(20).to_string(index=False))
print()

# ============================================================
# STEP 9: PREDICT SEGMENT FOR A NEW CUSTOMER
# ============================================================

print("=" * 65)
print("TESTING WITH NEW CUSTOMERS")
print("=" * 65)

new_customers = [
    {"Age": 28, "Annual_Income_k": 75, "Spending_Score": 80},
    {"Age": 55, "Annual_Income_k": 20, "Spending_Score": 15},
    {"Age": 35, "Annual_Income_k": 50, "Spending_Score": 50},
    {"Age": 22, "Annual_Income_k": 18, "Spending_Score": 85},
]

new_df        = pd.DataFrame(new_customers)
new_scaled    = scaler.transform(new_df[features])
new_clusters  = kmeans.predict(new_scaled)

print(f"{'#':<4} {'Age':>5} {'Income':>8} {'Spend':>7} "
      f"{'Cluster':>9} {'Segment'}")
print("-" * 70)

for i, (row, cluster) in enumerate(zip(new_customers, new_clusters), 1):
    seg = segment_labels[cluster].split("—")[-1].strip()
    print(f"{i:<4} {row['Age']:>5} {row['Annual_Income_k']:>8} "
          f"{row['Spending_Score']:>7} {cluster:>9}   {seg}")

print()
print("=" * 65)
print("DONE")
print("=" * 65)