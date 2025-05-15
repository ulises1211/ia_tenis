import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar dataset limpio ATP
data_path = "./data/processed_silver/atp_matches_ready.csv"
df = pd.read_csv(data_path)

# Eliminar filas con datos críticos faltantes
df = df.dropna(subset=['rank_diff', 'points_diff', 'fav_winner'])

# Feature set
features = ['rank_diff', 'points_diff', 'fav_winner', 'surface_Hard', 'surface_Clay', 'surface_Grass']

# Asegurarse que las columnas existen
for feature in features:
    if feature not in df.columns:
        df[feature] = 0

# Definir X (features) e y (target)
X = df[features]
y = df['fav_winner']

# Split entrenamiento y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# =========================
# Logistic Regression Model
# =========================
print("📈 Logistic Regression Model")
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

print("🎯 Accuracy:", accuracy_score(y_test, y_pred_lr))
print("\n📋 Classification Report:\n", classification_report(y_test, y_pred_lr))

# =========================
# Random Forest Model
# =========================
print("\n🌳 Random Forest Classifier Model")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

print("🎯 Accuracy:", accuracy_score(y_test, y_pred_rf))
print("\n📋 Classification Report:\n", classification_report(y_test, y_pred_rf))

# =========================
# Comparar matrices de confusión
# =========================
fig, axs = plt.subplots(1, 2, figsize=(12,5))

# Matriz Logistic Regression
cm_lr = confusion_matrix(y_test, y_pred_lr)
sns.heatmap(cm_lr, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axs[0])
axs[0].set_title("Logistic Regression")
axs[0].set_xlabel('Predicho')
axs[0].set_ylabel('Real')

# Matriz Random Forest
cm_rf = confusion_matrix(y_test, y_pred_rf)
sns.heatmap(cm_rf, annot=True, fmt="d", cmap="Greens", cbar=False, ax=axs[1])
axs[1].set_title("Random Forest Classifier")
axs[1].set_xlabel('Predicho')
axs[1].set_ylabel('Real')

plt.tight_layout()
plt.show()
