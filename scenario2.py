import pulp

# Hypothèses de données
transport_agents = [
    {"id": 1, "name": "Agent 1", "capacity": 100, "cost_per_km": 2},
    {"id": 2, "name": "Agent 2", "capacity": 150, "cost_per_km": 3},
]

recipients = [
    {"id": 1, "name": "Charity A", "location": (10, 20), "food_needs": 80},
    {"id": 2, "name": "Charity B", "location": (15, 25), "food_needs": 60},
]

# Hypothèse de la distance entre les agents et les bénéficiaires (calcul simplifié)
distances = {
    (1, 1): 10,  # Distance entre Agent 1 et Charity A
    (1, 2): 15,  # Distance entre Agent 1 et Charity B
    (2, 1): 20,  # Distance entre Agent 2 et Charity A
    (2, 2): 25,  # Distance entre Agent 2 et Charity B
}

# Création du problème d'optimisation
prob = pulp.LpProblem("Minimiser_Coût_Transport", pulp.LpMinimize)

# Variables de décision : combien de nourriture chaque transporteur transporte
assignments = pulp.LpVariable.dicts("Assign", (range(len(transport_agents)), range(len(recipients))), 0, 1, pulp.LpBinary)

# Fonction objectif : minimiser les coûts de transport
prob += pulp.lpSum([assignments[i][j] * transport_agents[i]["cost_per_km"] * distances[(i+1, j+1)] for i in range(len(transport_agents)) for j in range(len(recipients))])

# Contraintes
# 1. La quantité de nourriture transportée par chaque agent ne doit pas dépasser sa capacité
for i in range(len(transport_agents)):
    prob += pulp.lpSum([assignments[i][j] * recipients[j]["food_needs"] for j in range(len(recipients))]) <= transport_agents[i]["capacity"]

# 2. Chaque bénéficiaire doit recevoir la nourriture nécessaire
for j in range(len(recipients)):
    prob += pulp.lpSum([assignments[i][j] * recipients[j]["food_needs"] for i in range(len(transport_agents))]) == recipients[j]["food_needs"]

# Résolution du problème
prob.solve()

# Affichage des résultats
for i in range(len(transport_agents)):
    for j in range(len(recipients)):
        if pulp.value(assignments[i][j]) == 1:
            print(f"Agent {transport_agents[i]['name']} transporte {recipients[j]['food_needs']} kg de nourriture à {recipients[j]['name']}")

# Greedy: Minimiser le coût du transport en attribuant l'agent avec le coût le plus bas
# On commence par l'agent avec le coût le plus faible et on lui attribue autant de nourriture qu'il peut transporter

# Trier les agents par coût (le moins cher d'abord)
transport_agents.sort(key=lambda x: x["cost_per_km"])

# Distribution greedy
for recipient in recipients:
    food_needs = recipient["food_needs"]
    for agent in transport_agents:
        if food_needs > 0 and agent["capacity"] > 0:
            allocation = min(agent["capacity"], food_needs)
            food_needs -= allocation
            agent["capacity"] -= allocation
            print(f"{allocation} kg de nourriture transportés à {recipient['name']} par {agent['name']}")
        
        if food_needs <= 0:
            break
