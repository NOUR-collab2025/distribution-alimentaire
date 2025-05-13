import simpy
import random
from collections import defaultdict
from datetime import date
import matplotlib.pyplot as plt
import networkx as nx

from aco import ACO  # Ton module d'optimisation ACO

# --- Initialisation de l'environnement ---
env = simpy.Environment()

receivers = [
    {"id": 0, "name": "Banque Alimentaire", "location": "Tunis", "capacity": 300, "received_qty": 0},
    {"id": 1, "name": "Association Nour", "location": "Ariana", "capacity": 200, "received_qty": 0},
    {"id": 2, "name": "Croissant Rouge", "location": "Sfax", "capacity": 250, "received_qty": 0}
]

agents = [
    {"id": 1, "name": "Ali Transport", "type": "Camion", "capacity": 100},
    {"id": 2, "name": "Khaled Express", "type": "Fourgon", "capacity": 80},
    {"id": 3, "name": "Sami Delivery", "type": "Camionnette", "capacity": 60}
]

centers = [
    {"id": 1, "name": "Centre Central", "location": "Ben Arous", "stock": []},
    {"id": 2, "name": "Centre Sud", "location": "Sfax", "stock": []}
]

distances = {
    (0, 1): 5,
    (1, 0): 5,
    (0, 2): 270,
    (2, 0): 270,
    (1, 2): 265,
    (2, 1): 265
}

donors = [
    {"id": 1, "name": "Supermarche MG", "location": "La Marsa"},
    {"id": 2, "name": "Carrefour", "location": "Lac 1"},
    {"id": 3, "name": "Monoprix", "location": "Centre Ville"}
]

total_donated_qty = 0
total_delivered_qty = 0

def donate_and_distribute(env, donor, center, agents, aco, food_id_start, daily_data):
    global total_donated_qty, total_delivered_qty
    food_names = ["Riz", "Lait", "Pates", "Huile"]
    liquid_items = ["Lait", "Huile", "Jus", "Eau"]
    food_id = food_id_start
    redistribution_id = 500 + donor["id"] * 100

    while True:
        yield env.timeout(1)
        name = random.choice(food_names)
        qty = random.randint(150, 300)
        unit = "L" if name in liquid_items else "kg"
        category = "Liquide" if unit == "L" else "Sec"

        food = {"id": food_id, "name": name, "quantity": qty, "unit": unit, "category": category}
        center["stock"].append(food)
        total_donated_qty += qty
        print(f"[Jour {env.now}] {donor['name']} a donne {qty}{unit} de {name} au {center['name']}")

        best_path, _ = aco.run(start_node=center["id"] - 1)

        for recipient_id in best_path:
            recipient = receivers[recipient_id]
            if food["quantity"] <= 0:
                break
            remaining_capacity = recipient["capacity"] - recipient["received_qty"]
            accepted_qty = min(food["quantity"], remaining_capacity)
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
                total_delivered_qty += accepted_qty
                print(f"  -> {accepted_qty}{unit} envoyes a {recipient['name']} via {agent['name']}")
                food["quantity"] -= accepted_qty
                redistribution_id += 1

        daily_data[env.now] = {receiver["name"]: receiver["received_qty"] for receiver in receivers}
        food_id += 1

# --- Simulation ---
aco = ACO(distances, n_ants=10, n_iterations=50)
daily_data = defaultdict(dict)

for i, donor in enumerate(donors):
    center = centers[i % len(centers)]
    env.process(donate_and_distribute(env, donor, center, agents, aco, food_id_start=100 + i * 10, daily_data=daily_data))

env.run(until=7)

# --- Récapitulatif ---
print("\n===== RECAPITULATIF DES DISTRIBUTIONS =====")
for recipient in receivers:
    print(f"{recipient['name']}: {recipient['received_qty']} unite(s) recue(s).")

waste_qty = total_donated_qty - total_delivered_qty
waste_rate = 100 * waste_qty / total_donated_qty if total_donated_qty > 0 else 0
print(f"\nTaux de gaspillage alimentaire : {waste_rate:.2f}% ({waste_qty} unite(s) perdues)")

# --- Graphique de distribution par jour ---
days = sorted(daily_data.keys())
recipient_names = [r["name"] for r in receivers]
stacked_values = {name: [] for name in recipient_names}

for day in days:
    for name in recipient_names:
        stacked_values[name].append(daily_data[day].get(name, 0))

bottom = [0] * len(days)
plt.figure(figsize=(10, 6))
for name in recipient_names:
    plt.bar(days, stacked_values[name], label=name, bottom=bottom)
    bottom = [i + j for i, j in zip(bottom, stacked_values[name])]

plt.xlabel("Jour")
plt.ylabel("Quantité cumulée distribuée")
plt.title("Distribution alimentaire quotidienne")
plt.legend()
plt.grid(axis="y")
plt.tight_layout()
plt.show()

# --- Graphe du meilleur chemin avec agents ---
G = nx.DiGraph()

for centre in centers:
    G.add_node(centre["name"], type='centre')
for recipient in receivers:
    G.add_node(recipient["name"], type='recepteur')
for agent in agents:
    G.add_node(agent["name"], type='agent')

for i, donor in enumerate(donors):
    center = centers[i % len(centers)]
    best_path, _ = aco.run(start_node=center["id"] - 1)
    for rid in best_path:
        recipient = receivers[rid]
        agent = random.choice(agents)
        G.add_edge(center["name"], agent["name"])
        G.add_edge(agent["name"], recipient["name"])

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
node_colors = []
for n in G.nodes:
    t = G.nodes[n].get("type", "")
    if t == "centre":
        node_colors.append("skyblue")
    elif t == "agent":
        node_colors.append("orange")
    elif t == "recepteur":
        node_colors.append("lightgreen")
    else:
        node_colors.append("gray")

nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=9, edge_color='gray', arrows=True)
plt.title("Graphe du meilleur chemin ACO avec agents de transport")
plt.tight_layout()
plt.show()

# --- Évolution des distances ACO ---
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
plt.tight_layout()
plt.show()
