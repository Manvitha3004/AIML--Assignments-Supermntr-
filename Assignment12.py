""" 
Assignment (09/03/2026)
Assignment Name : House Price Predictor
Description : Train a Linear Regression model, predict prices, and test with new input.

"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# ============================================================
# STEP 1: DATASET
# ============================================================

data = {
    "Size_sqft": [850, 1200, 1500, 900, 2000, 1100, 1800, 750, 1600, 2200],
    "Bedrooms":  [2, 3, 3, 2, 4, 3, 4, 2, 3, 5],
    "Age_years": [5, 8, 3, 12, 1, 10, 6, 15, 4, 2],
    "Price_lakhs": [45, 62, 80, 40, 115, 55, 98, 35, 88, 130]
}

df = pd.DataFrame(data)

print("=" * 50)
print("TRAINING DATASET")
print("=" * 50)
print(df.to_string(index=False))
print()

# ============================================================
# STEP 2: FEATURES AND TARGET
# ============================================================

X = df[["Size_sqft", "Bedrooms", "Age_years"]].values
y = df["Price_lakhs"].values

# ============================================================
# STEP 3: TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples : {len(X_train)}")
print(f"Testing  samples : {len(X_test)}")
print()

# ============================================================
# STEP 4: TRAIN THE MODEL
# ============================================================

model = LinearRegression()
model.fit(X_train, y_train)

print("=" * 50)
print("LEARNED MODEL EQUATION")
print("=" * 50)
print(f"Intercept (b)        : {model.intercept_:.4f}")
print(f"Weight - Size_sqft   : {model.coef_[0]:.4f}")
print(f"Weight - Bedrooms    : {model.coef_[1]:.4f}")
print(f"Weight - Age_years   : {model.coef_[2]:.4f}")
print()
print("Price = {:.4f}".format(model.intercept_),
      "+ ({:.4f} x Size)".format(model.coef_[0]),
      "+ ({:.4f} x Bedrooms)".format(model.coef_[1]),
      "+ ({:.4f} x Age)".format(model.coef_[2]))
print()

# ============================================================
# STEP 5: PREDICT ON TEST SET
# ============================================================

y_pred = model.predict(X_test)

print("=" * 50)
print("PREDICTIONS vs ACTUAL (Test Set)")
print("=" * 50)
print(f"{'House':<8} {'Actual (L)':>12} {'Predicted (L)':>15} {'Error (L)':>12}")
print("-" * 50)
for i in range(len(y_test)):
    error = y_test[i] - y_pred[i]
    print(f"H{i+1:<7} {y_test[i]:>12.2f} {y_pred[i]:>15.2f} {error:>12.2f}")
print()

# ============================================================
# STEP 6: EVALUATE THE MODEL
# ============================================================

mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, y_pred)
mae  = np.mean(np.abs(y_test - y_pred))

print("=" * 50)
print("MODEL PERFORMANCE METRICS")
print("=" * 50)
print(f"MSE  (Mean Squared Error)       : {mse:.4f}")
print(f"RMSE (Root Mean Squared Error)  : {rmse:.4f}")
print(f"MAE  (Mean Absolute Error)      : {mae:.4f}")
print(f"R²   (R-squared Score)          : {r2:.4f}")
print()

if r2 >= 0.90:
    print("Model quality: EXCELLENT (R² >= 0.90)")
elif r2 >= 0.75:
    print("Model quality: GOOD (R² >= 0.75)")
else:
    print("Model quality: NEEDS IMPROVEMENT (R² < 0.75)")
print()

# ============================================================
# STEP 7: PREDICT WITH NEW INPUT
# ============================================================

print("=" * 50)
print("TESTING WITH NEW HOUSE INPUT")
print("=" * 50)

new_houses = [
    [1300, 3, 7],   # House A
    [1750, 4, 5],   # House B
    [950,  2, 10],  # House C
]

labels = ["House A", "House B", "House C"]

print(f"{'House':<10} {'Size':>6} {'Beds':>6} {'Age':>6} {'Predicted Price':>18}")
print("-" * 50)

for label, house in zip(labels, new_houses):
    price = model.predict([house])[0]
    print(f"{label:<10} {house[0]:>6} {house[1]:>6} {house[2]:>6} {'₹ {:.2f} Lakhs'.format(price):>18}")

print()
print("=" * 50)
print("DONE")
print("=" * 50)