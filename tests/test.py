import pandas as pd

# Charger le fichier CSV
df = pd.read_csv("food_wastage_data.csv")

# 1. Afficher un aperçu de base
print("Aperçu du fichier :")
print(df.head())
print("\nColonnes d'origine :", df.columns)

# 2. Supprimer les lignes avec valeurs manquantes
df.dropna(inplace=True)

# 3. Nettoyer les noms de colonnes (uniformiser)
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

# 4. Vérification des infos après nettoyage
print("\nColonnes après nettoyage :", df.columns)
print("\nInfo sur les données :")
print(df.info())
print("\nStatistiques générales :")
print(df.describe())

# 5. Vérifier les types d’aliments
print("\nTypes d’aliments :")
print(df["type_of_food"].value_counts())

# 6. Supprimer les valeurs aberrantes (quantité <= 0)
df = df[df["quantity_of_food"] > 0]

# 7. Encodage de la colonne "type_of_food" en numérique
df["type_code"] = df["type_of_food"].astype("category").cat.codes

# 8. Sauvegarder le fichier nettoyé
df.to_csv("cleaned_food_wastage_data.csv", index=False)
print("\n Données nettoyées et enregistrées dans 'cleaned_food_wastage_data.csv'")
