# evaluation_ml.py
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Charger les données enregistrées
model = joblib.load("model.pkl")
X_test, y_test, predictions = joblib.load("predictions.pkl")

# Précision globale
accuracy = accuracy_score(y_test, predictions)
print(f"\n Précision du modèle : {accuracy:.2f}")

# Rapport de classification
print("\n Rapport de classification :")
print(classification_report(y_test, predictions, zero_division=0))

# Matrice de confusion
cm = confusion_matrix(y_test, predictions)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel("Prédictions")
plt.ylabel("Véritables")
plt.title("Matrice de confusion")
plt.tight_layout()
plt.show()
