import argparse
import os
import datetime
import logging

from model import FoodDeliveryModel  # ton modèle Mesa

# Configuration des logs
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"run-{datetime.date.today()}.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(levelname)s] %(message)s')

# Argument parser
parser = argparse.ArgumentParser(description="Lancer la simulation de livraison alimentaire.")
parser.add_argument("--donors", type=int, default=10)
parser.add_argument("--recipients", type=int, default=5)
parser.add_argument("--transporters", type=int, default=3)
parser.add_argument("--steps", type=int, default=100)
parser.add_argument("--width", type=int, default=20)
parser.add_argument("--height", type=int, default=20)
args = parser.parse_args()

# Initialiser le modèle
logging.info(f"Step 1: Initialized model with {args.donors} donors and {args.recipients} recipients")
model = FoodDeliveryModel(
    num_donors=args.donors,
    num_recipients=args.recipients,
    num_transporters=args.transporters,
    width=args.width,
    height=args.height
)

# Simulation
for step in range(1, args.steps + 1):
    model.step()

    if step == args.steps // 2:
        delivered = model.successful_deliveries if hasattr(model, "successful_deliveries") else "N/A"
        logging.info(f"Step {step}: Optimization complete. {delivered} deliveries dispatched")

# Fin de simulation
logging.info(f"Step {args.steps}: Simulation ended. Log saved to {log_file}")
print(f"✅ Simulation terminée avec succès. Voir les logs : {log_file}")
