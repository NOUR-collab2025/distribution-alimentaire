import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Charger les données
try:
    df = pd.read_csv('../cleaned_food_wastage_data.csv')
    print('Données chargées:', df.shape)
except Exception as e:
    print('Erreur de chargement:', e)

# Encodage
df['type_code'] = df['type_of_food'].astype('category').cat.codes

# Variables features et target
X = df[['quantity_of_food', 'quantity_squared', 'quantity_log']].values
y = df['type_code'].values

# Séparation en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modèle Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prédictions
y_pred = model.predict(X_test)

# Évaluation
print('Accuracy:', accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d')
plt.title('Matrice de confusion')
plt.show()
