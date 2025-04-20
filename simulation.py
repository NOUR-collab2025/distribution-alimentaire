import simpy
import random
from collections import defaultdict
from src.models.donor import Donor
from src.models.recipient import Recipient
from src.models.fooditem import FoodItem
from src.models.transportAgent import TransportAgent
from src.models.redistribution import Redistribution
from src.models.distribution_center import DistributionCenter
from datetime import date

# Environnement SimPy
env = simpy.Environment()

# Création des récepteurs
receivers = [
    Recipient(1, "Banque Alimentaire", "Tunis", "contact@banque.tn", 300, "Haute"),
    Recipient(2, "Association Nour", "Ariana", "info@nour.tn", 200, "Moyenne"),
    Recipient(3, "Croissant Rouge", "Sfax", "croissant@rouge.tn", 250, "Haute")
]

# Création des agents de transport
agents = [
    TransportAgent(1, "Ali Transport", "Camion", 100, True),
    TransportAgent(2, "Khaled Express", "Fourgon", 80, True),
    TransportAgent(3, "Sami Delivery", "Camionnette", 60, True)
]

# Création de plusieurs centres de distribution
centers = [
    DistributionCenter(1, "Centre Central", "Ben Arous", 1000, 0),
    DistributionCenter(2, "Centre Sud", "Sfax", 800, 0)
]

# Assignation des récepteurs à chaque centre
centers[0].receivers = [receivers[0], receivers[1]]
centers[1].receivers = [receivers[2]]

for center in centers:
    center.stock = []

# Création des donneurs
donors = [
    Donor(1, "Supermarché MG", "La Marsa", "contact@mg.tn"),
    Donor(2, "Carrefour", "Lac 1", "contact@carrefour.tn"),
    Donor(3, "Monoprix", "Centre Ville", "contact@monoprix.tn")
]

# Statistiques
distributions_log = []

# Méthode de donation
def donate_and_distribute(env, donor, center, agents, food_id_start):
    food_names = ["Riz", "Lait", "Pâtes", "Huile"]
    liquid_items = ["Lait", "Huile", "Jus", "Eau"]
    food_id = food_id_start
    redistribution_id = 500 + donor.id * 100
    while True:
        yield env.timeout(1)
        name = random.choice(food_names)
        qty = random.randint(20, 100)
        unit = "L" if name in liquid_items else "kg"
        expiration = "2025-12-31"
        category = "Liquide" if unit == "L" else "Sec"

        food = FoodItem(food_id, name, qty, expiration, category, donor.id)
        center.stock.append(food)
        center.current_stock += qty

        print(f"[Jour {env.now}] {donor.name} a donné {qty}{unit} de {name} au {center.name}")

        for recipient in center.receivers:
            if food.quantity <= 0:
                break
            accepted_qty = min(food.quantity, recipient.capacity)
            if accepted_qty > 0:
                agent = random.choice(agents)
                redistribution = Redistribution(
                    redistribution_id,
                    food.id,
                    recipient.id,
                    agent.id,
                    str(date.today()),
                    "Livré"
                )
                distributions_log.append((recipient.name, food.name, accepted_qty, agent.name, unit, center.name))
                food.quantity -= accepted_qty
                center.current_stock -= accepted_qty
                print(f"  -> {accepted_qty}{unit} envoyés à {recipient.name} via {agent.name}")
                redistribution_id += 1
        food_id += 1

# Lancer un processus pour chaque donneur associé à un centre
for i, donor in enumerate(donors):
    center = centers[i % len(centers)]
    env.process(donate_and_distribute(env, donor, center, agents, food_id_start=100 + i * 10))

# Simulation sur 7 jours
env.run(until=7)

# Résumé final groupé
print("\n===== RÉCAPITULATIF DES DISTRIBUTIONS GROUPE PAR PRODUIT =====")
grouped = defaultdict(lambda: {"total": 0, "détails": []})

for recipient, food, qty, agent, unit, center in distributions_log:
    grouped[food]["total"] += qty
    grouped[food]["unit"] = unit
    grouped[food]["détails"].append((recipient, qty, agent, center))

for food, data in grouped.items():
    print(f"{food}: {data['total']}{data['unit']}")
    for detail in data["détails"]:
        print(f"  -> {detail[0]} ({detail[1]}{data['unit']}) via {detail[2]} ({detail[3]})")

