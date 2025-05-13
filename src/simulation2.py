import simpy
import random
from collections import defaultdict
from datetime import date
import matplotlib.pyplot as plt
import networkx as nx

# --- Algorithme de Backtracking Optimisé ---
def optimized_distribution(food_qty, recipients, max_waste_percentage=10):
    total_capacity = sum(r["capacity"] - r["received_qty"] for r in recipients)
    max_possible_delivered = food_qty * (1 - max_waste_percentage / 100)

    # Trier les récepteurs par leur capacité restante (de la plus faible à la plus grande)
    recipients_sorted = sorted(recipients, key=lambda r: r["capacity"] - r["received_qty"])

    remaining_qty = food_qty
    distribution_plan = []

    for recipient in recipients_sorted:
        available_capacity = recipient["capacity"] - recipient["received_qty"]
        qty_to_send = min(remaining_qty, available_capacity)

        # Si la quantité restante est suffisante, l'envoyer
        distribution_plan.append((recipient, qty_to_send))
        recipient["received_qty"] += qty_to_send
        remaining_qty -= qty_to_send

        if remaining_qty <= 0:
            break

    # Si on a encore des quantités non distribuées, on les garde comme gaspillage
    waste_qty = remaining_qty
    waste_rate = (waste_qty / food_qty) * 100
    if waste_rate > max_waste_percentage:
        print(f"Attention: Le gaspillage alimentaire dépasse le seuil de {max_waste_percentage}%!")

    return distribution_plan, waste_qty, waste_rate


# --- Données et initialisation ---
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

donors = [
    {"id": 1, "name": "Supermarche MG", "location": "La Marsa"},
    {"id": 2, "name": "Carrefour", "location": "Lac 1"},
    {"id": 3, "name": "Monoprix", "location": "Centre Ville"}
]

total_donated_qty = 0
total_delivered_qty = 0

daily_data = defaultdict(dict)
distribution_records = []


def donate_and_distribute(env, donor, center, agents, food_id_start, daily_data):
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

        # Optimiser la distribution avec la nouvelle fonction
        distribution_plan, waste_qty, waste_rate = optimized_distribution(food["quantity"], receivers)

        if distribution_plan:
            for recipient, dist_qty in distribution_plan:
                if dist_qty > 0:
                    agent = random.choice(agents)
                    redistribution = {
                        "id": redistribution_id,
                        "food_id": food["id"],
                        "recipient_id": recipient["id"],
                        "agent_id": agent["id"],
                        "center_name": center["name"],
                        "agent_name": agent["name"],
                        "recipient_name": recipient["name"],
                        "quantity": dist_qty,
                        "unit": unit,
                        "day": env.now
                    }
                    total_delivered_qty += dist_qty
                    distribution_records.append(redistribution)
                    print(f"  -> {dist_qty}{unit} envoyes a {recipient['name']} via {agent['name']}")
                    redistribution_id += 1
            food["quantity"] = 0

        daily_data[env.now] = {receiver["name"]: receiver["received_qty"] for receiver in receivers}
        food_id += 1

    # Afficher le taux de gaspillage
    print(f"Taux de gaspillage alimentaire : {waste_rate:.2f}% ({waste_qty} unité(s) perdues)")


# --- Simulation ---
for i, donor in enumerate(donors):
    center = centers[i % len(centers)]
    env.process(donate_and_distribute(env, donor, center, agents, food_id_start=100 + i * 10, daily_data=daily_data))

env.run(until=3)

# --- Résumé ---
print("\n===== RECAPITULATIF DES DISTRIBUTIONS =====")
for recipient in receivers:
    print(f"{recipient['name']}: {recipient['received_qty']} unite(s) reçue(s).")

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
plt.ylabel("Quantite cumulee distribuee")
plt.title("Distribution alimentaire quotidienne")
plt.legend()
plt.grid(axis="y")
plt.tight_layout()
plt.show()

# --- Graphe enrichi de la chaîne de distribution ---
G = nx.DiGraph()

for center in centers:
    G.add_node(center["name"], type="centre")
for agent in agents:
    G.add_node(agent["name"], type="agent")
for receiver in receivers:
    G.add_node(receiver["name"], type="recepteur")

# Ajouter les arêtes Centre → Agent → Recepteur
for record in distribution_records:
    c = record["center_name"]
    a = record["agent_name"]
    r = record["recipient_name"]
    q = record["quantity"]

    G.add_edge(c, a)
    if G.has_edge(a, r):
        G[a][r]["weight"] += q
    else:
        G.add_edge(a, r, weight=q)

# Affichage du graphe
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

edge_labels = {(u, v): f"{d['weight']} u" for u, v, d in G.edges(data=True) if "weight" in d}

nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=9, edge_color='gray', arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)

plt.title("Chaîne de distribution alimentaire (Centre → Agent → Récepteur)")
plt.tight_layout()
plt.show()
