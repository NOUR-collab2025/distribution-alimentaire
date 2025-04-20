import pulp

# Hypothèses de données
food_items = [
    {"id": 1, "name": "Rice", "quantity": 100, "expiration_date": "2025-01-01", "category": "Grain"},
    {"id": 2, "name": "Beans", "quantity": 50, "expiration_date": "2025-02-01", "category": "Legume"},
    {"id": 3, "name": "Tomato", "quantity": 30, "expiration_date": "2024-12-01", "category": "Vegetable"},
]

recipients = [
    {"id": 1, "name": "Charity A", "priority_level": 3, "capacity": 60},
    {"id": 2, "name": "Charity B", "priority_level": 1, "capacity": 40},
    {"id": 3, "name": "Charity C", "priority_level": 2, "capacity": 80},
]

# Création du problème d'optimisation
prob = pulp.LpProblem("Distribution_Aliments", pulp.LpMaximize)

# Variables de décision : allocation de FoodItems à des Recipients
allocations = pulp.LpVariable.dicts("Alloc", (range(len(food_items)), range(len(recipients))), 0, 1, pulp.LpBinary)

# Fonction objectif : maximiser la distribution selon la priorité
prob += pulp.lpSum([allocations[i][j] * recipients[j]["priority_level"] for i in range(len(food_items)) for j in range(len(recipients))])

# Contraintes
# 1. La quantité de chaque aliment ne doit pas être dépassée
for i in range(len(food_items)):
    prob += pulp.lpSum([allocations[i][j] for j in range(len(recipients))]) <= food_items[i]["quantity"]

# 2. La capacité des bénéficiaires ne doit pas être dépassée
for j in range(len(recipients)):
    prob += pulp.lpSum([allocations[i][j] * food_items[i]["quantity"] for i in range(len(food_items))]) <= recipients[j]["capacity"]

# Résolution du problème
prob.solve()

# Affichage des résultats
for i in range(len(food_items)):
    for j in range(len(recipients)):
        if pulp.value(allocations[i][j]) == 1:
            print(f"Aliment {food_items[i]['name']} (quantité {food_items[i]['quantity']} kg) envoyé à {recipients[j]['name']} (priorité {recipients[j]['priority_level']})")
# Greedy: attribuer les aliments aux bénéficiaires en fonction de leur priorité
# On commence par le bénéficiaire avec la priorité la plus élevée et on lui attribue la quantité qu'il peut recevoir

# Trier les bénéficiaires par priorité (d'abord ceux avec la priorité la plus élevée)
recipients.sort(key=lambda x: -x["priority_level"])

# Distribution greedy
for recipient in recipients:
    remaining_capacity = recipient["capacity"]
    for food in food_items:
        if remaining_capacity > 0 and food["quantity"] > 0:
            allocation = min(food["quantity"], remaining_capacity)
            food["quantity"] -= allocation
            remaining_capacity -= allocation
            print(f"{allocation} kg de {food['name']} attribués à {recipient['name']}")

        if remaining_capacity <= 0:
            break