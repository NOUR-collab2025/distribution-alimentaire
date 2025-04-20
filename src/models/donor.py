import random
from src.models.fooditem import FoodItem

class Donor:
    def __init__(self, name):
        self.name = name

    def donate(self, env, distribution_center):
        while True:
            food = FoodItem(
                name=random.choice(["Pâtes", "Riz", "Lait", "Pommes"]),
                quantity=random.randint(5, 15),
                expiration_day=env.now + random.randint(1, 5)
            )
            print(f"[t={env.now}] {self.name} propose un don de {food.quantity}x {food.name} (exp: J+{food.expiration_day})")
            yield env.timeout(1)
            yield env.process(distribution_center.receive_donation(food, env, self.name))
