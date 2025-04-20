# modele_ml.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib  # pour enregistrer les données

# Charger les données
data = pd.read_csv("cleaned_food_wastage_data.csv")

# Encodage si nécessaire
if "type_code" not in data.columns:
    data["type_code"] = data["type_of_food"].astype("category").cat.codes

# Définir X et y
X = data[["quantity_of_food"]]
y = data["type_code"]

# Séparation des données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Créer et entraîner le modèle
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Prédictions
predictions = model.predict(X_test)

# Enregistrer le modèle et les variables pour réutilisation
joblib.dump(model, "model.pkl")
joblib.dump((X_test, y_test, predictions), "predictions.pkl")

print(" Modèle entraîné et prédictions enregistrées.")
