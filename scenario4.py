import pulp

# Hypothèses de données
distribution_center = {
    "capacity": 200,  # Capacité du centre de distribution
    "current_stock": 150,  # Stock actuel
}

recipients = [
    {"id": 1, "name": "Charity A", "food_needs": 80},
    {"id": 2, "name": "Charity B", "food_needs": 70},
]

# Création du problème d'optimisation
prob = pulp.LpProblem("Optimisation_Stock_Distribution", pulp.LpMaximize)

# Variables de décision : distribution de nourriture à chaque bénéficiaire
allocations = pulp.LpVariable.dicts("Alloc", (range(len(recipients))), 0, 1, pulp.LpBinary)

# Fonction objectif : maximiser l'utilisation du stock tout en évitant le gaspillage
prob += pulp.lpSum([allocations[i] * recipients[i]["food_needs"] for i in range(len(recipients))])

# Contraintes
prob += pulp.lpSum([allocations[i] * recipients[i]["food_needs"] for i in range(len(recipients))]) <= distribution_center["current_stock"]

# Résolution du problème
prob.solve()

# Affichage des résultats
for i in range(len(recipients)):
    if pulp.value(allocations[i]) == 1:
        print(f"Redistribution de {recipients[i]['food_needs']} kg de nourriture à {recipients[i]['name']}")

# Greedy : On attribue la nourriture aux bénéficiaires jusqu'à ce que le stock soit épuisé
# On commence par distribuer aux bénéficiaires qui en ont le plus besoin

# Trier les bénéficiaires par besoins alimentaires (d'abord ceux avec le plus de besoins)
recipients.sort(key=lambda x: -x["food_needs"])

# Distribution greedy
remaining_stock = distribution_center["current_stock"]
for recipient in recipients:
    if remaining_stock >= recipient["food_needs"]:
        remaining_stock -= recipient["food_needs"]
        print(f"{recipient['food_needs']} kg de nourriture attribués à {recipient['name']}")
    else:
        print(f"{remaining_stock} kg de nourriture attribués à {recipient['name']} (partiellement satisfait)")
        remaining_stock = 0

    if remaining_stock <= 0:
        break