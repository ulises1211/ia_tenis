# archivo mejorado: modelo_puro_enriched.py

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# 📂 Rutas
#data_path = "./data/processed_silver_enriched/atp_matches_enriched.csv"
data_path = "./data/processed_silver_enriched/wta_matches_enriched.csv"
output_model_folder = "./modelos/"
os.makedirs(output_model_folder, exist_ok=True)

# 📥 Cargar datos
df = pd.read_csv(data_path)

# 🧹 Limpiar datos críticos
df = df.dropna(subset=['rank_diff', 'points_diff', 'fav_winner', 'round_importance'])

# 🎯 Features y Target
features = [
    'rank_diff', 'points_diff',
    'surface_Hard', 'surface_Clay', 'surface_Grass',
    'is_grand_slam', 'round_importance'
]
X = df[features]
y = df['fav_winner']

# 🔀 División en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ================================
# 🎯 Logistic Regression
# ================================
print("📈 Entrenando Logistic Regression...")
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

# 🔥 Evaluación
print("\n📋 Logistic Regression Report:")
print(classification_report(y_test, y_pred_lr))
print(f"🎯 Accuracy: {accuracy_score(y_test, y_pred_lr):.4f}")

# 💾 Guardar modelo Logistic Regression
#joblib.dump(lr_model, os.path.join(output_model_folder, "logistic_model_tenis.joblib"))
joblib.dump(lr_model, os.path.join(output_model_folder, "wta_logistic_model_tenis.joblib"))
print("✅ Logistic Regression model guardado en './modelos/wta_logistic_model_tenis.joblib'")

# ================================
# 🌳 Random Forest Mejorado
# ================================
print("\n🌳 Entrenando Random Forest Mejorado...")
rf_model = RandomForestClassifier(
    n_estimators=500,
    min_samples_split=2,
    min_samples_leaf=2,
    max_features=None,
    max_depth=5,
    random_state=42
)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# 🔥 Evaluación
print("\n📋 Random Forest Report:")
print(classification_report(y_test, y_pred_rf))
print(f"🎯 Accuracy: {accuracy_score(y_test, y_pred_rf):.4f}")

# 💾 Guardar modelo Random Forest
#joblib.dump(rf_model, os.path.join(output_model_folder, "random_forest_model_tenis.joblib"))
joblib.dump(rf_model, os.path.join(output_model_folder, "wta_random_forest_model_tenis.joblib"))
print("✅ Random Forest model guardado en './modelos/wta_random_forest_model_tenis.joblib'")

# ================================
# 🔥 Comparar matrices de confusión
# ================================
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Matriz Logistic Regression
cm_lr = confusion_matrix(y_test, y_pred_lr)
sns.heatmap(cm_lr, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axs[0])
axs[0].set_title("Logistic Regression")
axs[0].set_xlabel('Predicho')
axs[0].set_ylabel('Real')

# Matriz Random Forest
cm_rf = confusion_matrix(y_test, y_pred_rf)
sns.heatmap(cm_rf, annot=True, fmt="d", cmap="Greens", cbar=False, ax=axs[1])
axs[1].set_title("Random Forest Mejorado")
axs[1].set_xlabel('Predicho')
axs[1].set_ylabel('Real')

plt.tight_layout()
plt.show()
