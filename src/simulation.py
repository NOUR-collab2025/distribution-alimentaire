import simpy
import random
from collections import defaultdict
from datetime import date
import matplotlib.pyplot as plt
import networkx as nx  # Pour les graphes
from aco import ACO  # Ton module ACO

# Environnement SimPy
env = simpy.Environment()

# Récepteurs
receivers = [
    {"id": 0, "name": "Banque Alimentaire", "location": "Tunis", "capacity": 300, "received_qty": 0},
    {"id": 1, "name": "Association Nour", "location": "Ariana", "capacity": 200, "received_qty": 0},
    {"id": 2, "name": "Croissant Rouge", "location": "Sfax", "capacity": 250, "received_qty": 0}
]

# Agents
agents = [
    {"id": 1, "name": "Ali Transport", "type": "Camion", "capacity": 100},
    {"id": 2, "name": "Khaled Express", "type": "Fourgon", "capacity": 80},
    {"id": 3, "name": "Sami Delivery", "type": "Camionnette", "capacity": 60}
]

# Centres
centers = [
    {"id": 1, "name": "Centre Central", "location": "Ben Arous", "stock": []},
    {"id": 2, "name": "Centre Sud", "location": "Sfax", "stock": []}
]

# Distances entre récepteurs
distances = {
    (0, 1): 5,
    (1, 0): 5,
    (0, 2): 270,
    (2, 0): 270,
    (1, 2): 265,
    (2, 1): 265
}

# Donneurs
donors = [
    {"id": 1, "name": "Supermarche MG", "location": "La Marsa"},
    {"id": 2, "name": "Carrefour", "location": "Lac 1"},
    {"id": 3, "name": "Monoprix", "location": "Centre Ville"}
]

# Processus de donation et distribution
def donate_and_distribute(env, donor, center, agents, aco, food_id_start, daily_data):
    food_names = ["Riz", "Lait", "Pates", "Huile"]
    liquid_items = ["Lait", "Huile", "Jus", "Eau"]
    food_id = food_id_start
    redistribution_id = 500 + donor["id"] * 100

    while True:
        yield env.timeout(1)
        name = random.choice(food_names)
        qty = random.randint(20, 100)
        unit = "L" if name in liquid_items else "kg"
        expiration = "2025-12-31"
        category = "Liquide" if unit == "L" else "Sec"

        food = {"id": food_id, "name": name, "quantity": qty, "unit": unit, "category": category}
        center["stock"].append(food)
        print(f"[Jour {env.now}] {donor['name']} a donné {qty}{unit} de {name} au {center['name']}")

        best_path, _ = aco.run(start_node=center["id"] - 1)

        for recipient_id in best_path:
            recipient = receivers[recipient_id]
            if food["quantity"] <= 0:
                break
            accepted_qty = min(food["quantity"], recipient["capacity"])
            if accepted_qty > 0:
                agent = random.choice(agents)
                redistribution = {
                    "id": redistribution_id,
                    "food_id": food["id"],
                    "recipient_id": recipient["id"],
                    "agent_id": agent["id"],
                    "date": str(date.today()),
                    "status": "Livré"
                }
                recipient["received_qty"] += accepted_qty
                print(f"  -> {accepted_qty}{unit} envoyés à {recipient['name']} via {agent['name']}")
                food["quantity"] -= accepted_qty
                redistribution_id += 1

        daily_data[env.now] = {receiver["name"]: receiver["received_qty"] for receiver in receivers}
        food_id += 1

# Initialisation
aco = ACO(distances, n_ants=10, n_iterations=50)
daily_data = defaultdict(dict)

# Lancement de la simulation
for i, donor in enumerate(donors):
    center = centers[i % len(centers)]
    env.process(donate_and_distribute(env, donor, center, agents, aco, food_id_start=100 + i * 10, daily_data=daily_data))

env.run(until=3)

# Résumé final
print("\n===== RECAPITULATIF DES DISTRIBUTIONS =====")
for recipient in receivers:
    print(f"{recipient['name']}: {recipient['received_qty']} unité(s) reçue(s).")

# ➤ Graphique de la distribution par jour
days = list(daily_data.keys())
for recipient in receivers:
    quantities = [daily_data[day].get(recipient['name'], 0) for day in days]
    plt.plot(days, quantities, label=recipient['name'])

plt.xlabel('Jour')
plt.ylabel('Quantité envoyée (unité)')
plt.title('Distribution alimentaire au fil du temps')
plt.legend()
plt.grid(True)
plt.show()

# ➤ Graphe du meilleur chemin avec NetworkX
G = nx.Graph()

# Ajout des nœuds
for centre in centers:
    G.add_node(centre["name"], type='centre')
for recipient in receivers:
    G.add_node(recipient["name"], type='recepteur')

# Ajout des arêtes en fonction des meilleurs chemins
for i, donor in enumerate(donors):
    center = centers[i % len(centers)]
    best_path, _ = aco.run(start_node=center["id"] - 1)
    for j in range(len(best_path)):
        centre_name = center["name"]
        recepteur_name = receivers[best_path[j]]["name"]
        G.add_edge(centre_name, recepteur_name)

# Dessiner le graphe NetworkX
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
node_colors = ['skyblue' if G.nodes[n].get("type") == "centre" else 'lightgreen' for n in G.nodes]
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, font_size=9, edge_color='gray')
plt.title("Graphe du meilleur chemin de distribution (ACO)")
plt.tight_layout()
plt.show()

# ➤ Courbe d'évolution de la distance ACO
distance_evolution = aco.get_distance_evolution()
iterations = list(range(len(distance_evolution)))

plt.figure(figsize=(10, 5))
plt.plot(iterations, distance_evolution, marker='o', linestyle='-', color='blue', label='Distance totale')
plt.axhline(y=min(distance_evolution), color='green', linestyle='--', label='Distance minimale atteinte')
plt.title("Évolution de la distance du meilleur chemin trouvé (ACO)")
plt.xlabel("Itération")
plt.ylabel("Distance totale du chemin")
plt.grid(True)
plt.legend()

# Annotations des améliorations
for i in range(1, len(distance_evolution)):
    if distance_evolution[i] < distance_evolution[i - 1]:
        plt.annotate(f"{distance_evolution[i]:.1f}", 
                     (i, distance_evolution[i]), 
                     textcoords="offset points", 
                     xytext=(0, -10), 
                     ha='center', fontsize=8, color='darkred')

plt.tight_layout()
plt.show()

