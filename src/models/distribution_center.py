import random

class DistributionCenter:
    def __init__(self, receivers):
        self.receivers = receivers

    def receive_donation(self, food_item, env, donor_name):
        if food_item.is_expired(env.now):
            print(f"[t={env.now}] {donor_name}'s don de {food_item.name} est périmé. Jeté.")
            return
        receiver = random.choice(self.receivers)
        yield env.timeout(1)
        receiver.receive(food_item, env)
